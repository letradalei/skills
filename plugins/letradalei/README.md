# Letra da Lei

A Letra da Lei traz o acervo jurídico brasileiro para o Claude: **legislação** e **jurisprudência**, com texto autoritativo em nível de artigo/precedente, verificação de vigência e fontes verificáveis no Planalto. Sobre essa base de pesquisa, o plugin também **redige peças processuais** com fundamentação verificada dispositivo por dispositivo.

## Pré-requisito

O servidor MCP **`letradalei`** (`https://mcp.letradalei.com/mcp`) deve estar conectado, autenticação via **OAuth** (login no primeiro uso). As skills verificam a conexão antes de operar e nunca respondem de memória.

## Ferramentas do MCP (grupo · operação)

| Ferramenta | O que faz |
|---|---|
| `acervo · listar` | Descobre a cobertura, áreas e leis (`dominio: "legislacao"`) ou tribunais/tipos/eficácia (`dominio: "jurisprudencia"`). |
| `legislacao-federal · buscar_artigos` | Busca semântica de artigos; retorna `texto`, `citacao`, `situacao`, `source_url`. |
| `legislacao-federal · explorar_contexto` | Navega o sumário da lei e as relações de um artigo (`cita`/`citado_por`/`altera`). |
| `acervo · consultar` | Texto **integral** (não truncado) de artigos ou precedentes. |
| `jurisprudencia-federal · buscar_precedentes` | Súmulas, temas, OJs e acórdãos do STF/STJ/TST/CARF. |
| `jurisprudencia-federal · buscar_vinculantes` | Só precedentes vinculantes (art. 927 CPC). |
| `jurisprudencia-estadual · buscar_vinculantes` | IRDRs dos TJs (parâmetro `localidade` obrigatório). |
| `acervo · reclame_aqui` | Registra lacunas/erros do acervo para a equipe da Letra da Lei. |

Todas retornam `situacao` (vigência) e `is_truncated`, confira antes de citar.

## Skills

| Skill | Faz |
|---|---|
| `/letradalei:pesquisa` | **Skill-base.** Pesquisa e cita legislação e jurisprudência pelo MCP, com verificação de vigência e texto integral. As demais skills a carregam. |
| `/letradalei:peticao` | Redige petição inicial (CPC art. 319) com fundamentação verificada. |
| `/letradalei:contestacao` | Redige contestação cível (CPC arts. 335–342), preliminares, mérito e eventual reconvenção. |
| `/letradalei:fundamentacao` | Estrutura a fundamentação de sentença/decisão com checagem do art. 489, § 1º do CPC. |
| `/letradalei:analise` | Diagnostica a fase processual e redige a peça cabível (réplica, recursos, cumprimento, embargos, ações autônomas etc.). |
| `/letradalei:revisao-politica` | Revisa uma política interna (.docx) contra a regulação e a legislação vigentes e gera um pacote para aprovação (PDF e .docx): achados por cláusula com fonte, o que mudou desde a última revisão, exposição judicial, tarefas por responsável e registro de auditoria. Aceita replay ("como em AAAA-MM-DD"). |

As skills de redação produzem **rascunhos revisáveis**, não peças prontas: quem assina, decide estratégia e protocola é o(a) advogado(a) ou magistrado(a) habilitado(a). A peça é salva em `outputs/` e os pontos pendentes (`[VERIFICAR]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS]` etc.) ficam em **vermelho e negrito** no `.docx`, aplicados por `scripts/colorir_marcadores.py` (requer `python-docx`: `pip install python-docx`).

### Revisão de política (`revisao-politica`)

Usa as ferramentas de conformidade da Letra da Lei (`conformidade · conceito`, `conformidade · alteracoes`, disponíveis nos planos com acesso ao gateway de produto) quando conectadas; sem elas, usa as ferramentas públicas (inclusive `legislacao-infralegal · buscar_atos`) e diz isso no pacote. O PDF e o `.docx` são gerados por `scripts/montar_pacote_conformidade.py` a partir de um JSON (contrato em `skills/revisao-politica/references/esquema-resultado.md`):

```bash
pip install reportlab python-docx
python scripts/montar_pacote_conformidade.py skills/revisao-politica/exemplos/resultado-exemplo.json --pdf outputs/exemplo.pdf --docx outputs/exemplo.docx
python -m unittest discover -s scripts/tests -v
```

`skills/revisao-politica/exemplos/` traz uma política fictícia de prevenção a fraudes (documento de exemplo, sem relação com instituição real) e um resultado completo; o gabarito do backtest fica fora do plugin, em `evals/revisao-politica/` na raiz do repositório.

## Quando usar / não usar

- **Usar:** consultar o que a lei diz, localizar artigo/precedente, verificar uma citação, ou redigir uma peça com base legal verificada.
- **Não usar:** aconselhamento jurídico ou prognóstico, o plugin recupera e estrutura fontes; a aplicação aos fatos é do(a) profissional habilitado(a). Legislação estadual/municipal está fora do acervo; normas infralegais (BCB/CMN, CNJ, ANS e outros órgãos) estão em beta.

### Links

- **Site:** https://letradalei.com
- **Documentação:** https://letradalei.com/docs
- **Suporte:** suporte@letradalei.com
