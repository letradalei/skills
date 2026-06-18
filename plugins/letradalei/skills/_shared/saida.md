# Saída e revisão (contrato compartilhado das peças)

Material de apoio das skills de redação. Define os arquivos de saída e como sinalizar, para o(a) revisor(a) humano(a), tudo o que ficou pendente.

## Dois arquivos

Salve sempre:
- `outputs/<tipo>-<slug>-<AAAA-MM-DD>.docx` — a peça. `<tipo>` é o prefixo que a skill indica (ex.: `peticao`, `contestacao`).
- `outputs/<tipo>-<slug>-NOTAS.md` — o bloco de notas de revisão (esqueleto abaixo).

## Montagem do `.docx`

Não reimplemente a formatação a cada peça. Use os utilitários de `${CLAUDE_PLUGIN_ROOT}/scripts/montar_docx.py`, que já aplicam o padrão forense (corpo justificado em Times New Roman 12pt; blocos de citação recuados 1,25 cm em 11pt, sem aspas, com a linha `Fonte:` logo abaixo). Importe as funções no seu script de geração:

```python
import sys; sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
from montar_docx import nova_peca, paragrafo, titulo, bloco_citacao, salvar

doc = nova_peca()
titulo(doc, "AÇÃO DE INDENIZAÇÃO POR DANOS MORAIS")
paragrafo(doc, "I, DOS FATOS", negrito=True)
paragrafo(doc, "No dia [VERIFICAR: data], a parte autora ...")
bloco_citacao(doc, "Art. 14. ...", "Fonte: CDC, art. 14 | <source_url> | situação: vigente | lei: Lei-8078-1990")
salvar(doc, "outputs/<tipo>-<slug>-<AAAA-MM-DD>.docx")
```

Assim a formatação fica num único lugar e cada peça herda o mesmo padrão. (`${CLAUDE_PLUGIN_ROOT}` é a raiz do plugin; os scripts ficam em `scripts/` na raiz, **não** dentro de `skills/`.)

## Marcadores em vermelho

Os marcadores (`[VERIFICAR]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS]`, `[JURISPRUDÊNCIA…]`, `[DOC. A NUMERAR]` e os próprios de cada peça) sinalizam o que o(a) profissional precisa resolver antes de assinar. Para que saltem aos olhos, recolora-os em vermelho/negrito depois de gerar o `.docx`:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/colorir_marcadores.py" outputs/<tipo>-<slug>-<AAAA-MM-DD>.docx
```

O script sobrescreve o arquivo e só toca marcadores de revisão (deixa placeholders comuns como `[Cidade]` intactos). Requer `python-docx`. Se indisponível, aplique a cor `#FF0000` manualmente a cada marcador.

## Aviso ao usuário (incluir sempre, após entregar a minuta)

> ⚠️ **ITENS EM VERMELHO — VERIFICAÇÃO NECESSÁRIA ANTES DO PROTOCOLO**
> Os trechos em vermelho indicam pontos que o(a) advogado(a) precisa resolver antes de assinar e protocolar:
> - `[VERIFICAR: ...]` — dado não confirmado, presumido ou ausente
> - `[CITAÇÃO PENDENTE]` — dispositivo não localizado via MCP; inserir manualmente com fonte verificada
> - `[FORA DO CORPUS]` — norma estadual/municipal ou tabela do tribunal; conferir na fonte local
> - `[JURISPRUDÊNCIA, a ser inserida pelo(a) advogado(a)]` — espaço para súmula/julgado a critério do(a) advogado(a)
> - `[JURISPRUDÊNCIA PERSUASIVA, ...]` — precedente persuasivo; revisar a pertinência ao caso antes do protocolo
> - `[DOC. A NUMERAR]` — documento referenciado sem número; numerar ao juntar
>
> Nenhum desses marcadores pode permanecer na peça no momento do protocolo.

(Inclua na lista os marcadores específicos da peça, se houver.)

## Esqueleto do `NOTAS.md`

```
## Notas de revisão, [Peça], [data]

**Skill:** [nome] (Letra da Lei)
**Fonte da legislação:** MCP Letra da Lei (texto verbatim do Planalto)

### Marcadores inline a resolver
- `[VERIFICAR: ...]`, N
- `[CITAÇÃO PENDENTE]`, N
- `[FORA DO CORPUS]`, N
- `[JURISPRUDÊNCIA, ...]`, N

### Dispositivos citados (todos verificados via MCP)
- [lei_slug]-[Art-N], [source_url]

### Pontos abertos para o(a) advogado(a)
- [premissas a confirmar; decisões estratégicas que a skill não toma]

### O que esta skill NÃO fez
- [limites: jurisprudência não encontrada, prazos não calculados, nada protocolado etc.]
```
