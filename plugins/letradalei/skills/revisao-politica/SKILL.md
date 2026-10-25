---
name: revisao-politica
description: Revisa uma política interna de compliance (.docx) contra a regulação e a legislação brasileiras vigentes e gera um pacote pronto para aprovação em PDF e .docx, com achados por cláusula, o que mudou desde a última revisão, exposição judicial, tarefas por responsável e registro de auditoria. Use quando o usuário enviar uma política, manual ou norma interna (ex.: prevenção a fraudes, Pix, PLD, LGPD) ou pedir "revise esta política", "o que mudou desde a última revisão", "a política está em dia?", "como estaria em <data>". Não use para peças processuais (há skills próprias) nem para pesquisa avulsa (use pesquisa).
argument-hint: "[caminho da política .docx] [opcional: 'como em AAAA-MM-DD' para replay]"
compatibility: "Requer o MCP da Letra da Lei; as ferramentas de conformidade (gateway de produto) são preferidas e, sem elas, a skill usa as públicas e avisa. Requer reportlab e python-docx (pip install reportlab python-docx) para gerar o PDF e o .docx."
metadata:
  version: "0.1.0"
---

# Revisão de política contra a Letra da Lei

O usuário solta o arquivo; a skill faz o trabalho inteiro e devolve um pacote para a pessoa responsável aprovar. Não pergunte nada que o documento responda. A única entrada opcional é uma data de replay ("como em 2026-07-01", "as of 2026-07-01").

O pacote **não é parecer jurídico**: é um rascunho verificável. Quem aprova é a pessoa responsável pela política (compliance, jurídico, diretoria).

## Regras inegociáveis

1. **Nada de memória.** Toda regra, data e precedente vem das ferramentas da Letra da Lei, lido no texto retornado. Toda afirmação do pacote cita ato, dispositivo e data, com `source_url`.
2. **Não invente prazo.** Prazo só entra quando a regra o fixa (dispositivo ou cláusula de vigência). Sem prazo na regra: "sem prazo próprio".
3. **Marque o que faltou.** O que não foi encontrado vai como `[NÃO ENCONTRADO ...]` ou `[VERIFICAR ...]` e em `auditoria.nao_encontrado`. Falha do acervo também vai para `acervo · reclame_aqui`.
4. **Diga quais ferramentas usou.** Sem as de conformidade, o PDF e a resposta no chat dizem isso (ver `references/consultas.md`, seção 2).
5. **Cláusula conforme também é achado.** Registre as cláusulas operativas conferidas sem lacuna como `conforme`: mostram o que foi checado.

## Passo 0, ferramentas

- Confirme que o MCP `letradalei` responde (uma chamada leve, ex.: `acervo · listar` com `dominio: "legislacao-infralegal"`). Se não responder, pare e avise: sem fonte não há revisão.
- Procure na lista de ferramentas as de conformidade (`conformidade · conceito`, `conformidade · alteracoes`). Anote `conformidade_disponivel = true|false`.
- Leia `references/consultas.md` (como chamar cada ferramenta, fallback, replay, severidade) e `references/esquema-resultado.md` (o JSON que o renderizador espera).

## Passo 1, ler a política

Extraia o texto com python-docx (cabeçalho e rodapé incluídos, porque avisos e datas costumam estar lá):

```bash
python - "<caminho.docx>" <<'PY'
import sys
from docx import Document
d = Document(sys.argv[1])
for s in d.sections:
    for p in s.header.paragraphs + s.footer.paragraphs:
        if p.text.strip(): print("[cab/rod]", p.text)
for p in d.paragraphs:
    if p.text.strip(): print(p.text)
for t in d.tables:
    for r in t.rows: print(" | ".join(c.text for c in r.cells))
print("[core] modified:", d.core_properties.modified, "| created:", d.core_properties.created)
PY
```

PDF ou texto colado também servem: leia o conteúdo direto.

- **Data de revisão:** a data de aprovação ou da última revisão declarada no documento (capa, "aprovada em", "vigência a partir de", histórico de versões). Havendo várias, use a mais recente aprovação. Guarde o trecho em `fonte_data_revisao`. Sem data no texto: use a data de modificação do arquivo e marque `[VERIFICAR: data de revisão não declarada no documento; usada a data do arquivo]`.
- **Data-base** = data de revisão. **Data de referência** = hoje, ou a data do replay.
- **Cláusulas:** liste cada item numerado com o texto literal. **Operativa é todo item numerado**, exceto os das seções cujo título é de objetivo, abrangência, definições, governança/aprovação, papéis/responsabilidades ou revisão da própria política. Não decida item a item: aplique a regra pelo título da seção e liste o resultado em `politica.clausulas_operativas`. As de governança entram como achado só quando uma regra as alcança (aprovação pelo conselho, destinatários de relatório, revisão vencida).

## Passo 2, mapear cláusulas a conceitos

Agrupe as cláusulas operativas por tema (ex.: numa política de fraudes de instituição de pagamento: MED e devoluções; contas suspeitas e restrições; chaves Pix; bloqueio cautelar; autenticação; registros e reporte).

- **Com conformidade:** `conformidade · conceito` (`query` pelo tema, depois `id`; `desde = data_base`; no replay, `data_referencia`). Os `vinculos` dão os dispositivos a conferir e o rollup `alteracoes` dá o que mudou.
- **Sem conformidade:** as próprias referências da política (atos citados no objetivo) e `legislacao-infralegal · buscar_atos` / `legislacao-federal · buscar_artigos` por tema localizam os dispositivos.

## Passo 3, o que mudou desde a data-base

- **Com conformidade:** `conformidade · alteracoes` por `conceito` (e por `search_id` dos dispositivos centrais), `desde = data_base`, `ate = data de referência` no replay.
- **Sem conformidade:** notas de alteração do texto consolidado + leitura de cada ato alterador, inclusive a cláusula de vigência (seção 2 de `references/consultas.md`).
- Para cada alteração, registre data, tipo de data (vigência, efeitos), ato, dispositivos e o que mudou. Datas de efeitos posteriores à referência ficam "a vigorar".

## Passo 4, ler o texto vigente e comparar

Para cada dispositivo vinculado a uma cláusula, leia o texto integral (`acervo · consultar`) na data de referência e compare com a cláusula:

- **Toda cláusula operativa termina num achado**, lacuna ou `conforme`; nenhuma fica de fora. Liste-as em `politica.clausulas_operativas` (ex.: `["5.1","5.2",...]`); o renderizador recusa o JSON se alguma não aparecer em `achados[].clausula.ref`.
- Compare cada cláusula com **todos** os dispositivos de `regulacao` dos conceitos do seu tema (não só os que lembrar), no texto vigente na data de referência. Anote em `auditoria.verificacoes` uma linha por cláusula: cláusula → dispositivos lidos.
- Percorra cada dispositivo **parágrafo a parágrafo** (caput, §§, incisos, alíneas) que trate do assunto da cláusula: cada dever do texto que a cláusula não traz (inclusive comunicar o cliente, prazos, alcance) é lacuna. Não pare no primeiro dever conferido.
- A cláusula contraria, omite ou restringe o que a regra exige? É lacuna. Classifique pelas perguntas da seção 5 de `references/consultas.md`, na ordem, e grave o código em `criterio`.
- A regra mudou depois da data-base? Diga qual ato mudou, quando passou a valer e qual o prazo de implementação, se houver.
- Escreva `exige_hoje` em linguagem direta, fiel ao texto, sem acrescentar dever que o texto não traz.
- Proponha `nova_redacao` no estilo e na numeração da política, sem copiar o regulamento palavra por palavra quando uma frase operacional basta.

## Passo 5, aplicação pelos tribunais

Para os achados `alta` e `media`, busque como os tribunais tratam a lacuna (seção 3 de `references/consultas.md`): primeiro precedentes vinculantes e súmulas do STJ, depois acórdãos (TJs) sobre a mesma conduta. Cite o trecho literal, a eficácia e a data. Precedente não encontrado: marque, não preencha.

## Passo 6, tarefas por responsável

Uma tarefa por entrega, atribuída a `ops` (Operações), `juridico` (Jurídico) ou `fraude_compliance` (Prevenção a Fraudes e Compliance). Prazo só o que a regra fixar, com a base. Inclua a tarefa de levar a nova redação à instância que aprova a política (a própria política diz qual).

## Passo 7, montar o pacote

1. Grave o resultado em `outputs/revisao-politica-<slug>-<data_referencia>.json`, no formato de `references/esquema-resultado.md` (`"versao_esquema": "1.1"`).
2. Gere o PDF e o `.docx`:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/montar_pacote_conformidade.py" outputs/revisao-politica-<slug>-<data>.json
   ```
   O script valida o JSON. Se recusar, corrija o JSON e rode de novo; não contorne a validação.
3. Se quiser os marcadores do `.docx` em vermelho: `python "${CLAUDE_PLUGIN_ROOT}/scripts/colorir_marcadores.py" <arquivo>.docx`.

## Passo 8, resposta no chat

Curta. Diga: a política e a data-base; quantos achados por severidade e os de severidade alta numa linha cada (cláusula, regra, data); prazos vencidos e a vencer; os caminhos do PDF, do `.docx` e do JSON; o aviso de ferramentas, se a revisão usou o fallback; e o que ficou `[VERIFICAR]`.

## Política de exemplo

`exemplos/politica-prevencao-fraudes-exemplo.docx` é uma política fictícia (Exemplo Pagamentos IP S.A., "Documento de exemplo, sem relação com instituição real"), aprovada em 18/3/2025, para demonstração. Ao revisá-la, ponha `"exemplo": true` no JSON. `exemplos/resultado-exemplo.json` mostra um resultado completo. O gabarito do backtest fica fora do plugin e não deve ser lido durante a revisão.

## O que esta skill não faz

- Não aprova a política nem altera o documento original: entrega a proposta.
- Não cobre manuais operacionais fora do acervo (ex.: Manual Operacional do DICT); aponta `[VERIFICAR]` quando a regra remete a eles.
- Não dá prognóstico de causa: a exposição judicial mostra como os tribunais decidiram, com a eficácia de cada precedente.
