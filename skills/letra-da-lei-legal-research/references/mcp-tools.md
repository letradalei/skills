# Ferramentas MCP da Letra da Lei

A MCP da Letra da Lei expõe ferramentas organizadas em grupos. Referencie sempre o **grupo · operação**. O acervo cobre **legislação federal** e **jurisprudência** (federal: STF/STJ/TST/CARF; estadual: IRDRs dos TJs). Não cobre legislação estadual/municipal nem acórdãos estaduais comuns.

Postura geral: **pesquise primeiro, responda depois**; prefira citações em nível de artigo/precedente; se faltar cobertura, diga — e registre via `reclame_aqui`.

---

## `acervo · listar` — descobrir cobertura

Param obrigatório: `dominio` (`"legislacao"` ou `"jurisprudencia"`).

- `dominio: "legislacao"`:
  - sem `area` → índice de áreas do direito (slug + nº de leis por área).
  - com `area` (um slug, ou `"all"` para o catálogo inteiro) → as leis daquela área (sigla/slug/título) para usar como `norma` em `buscar_artigos`/`consultar`.
- `dominio: "jurisprudencia"` + `esfera` (`"federal"` ou `"estadual"`) → tribunais (`autoridade`), tipos de precedente, força vinculante (`eficacia`) com contagens, e o vocabulário de `area`.

## `legislacao-federal · buscar_artigos` — busca de artigos

Params: `query` (linguagem natural ou palavras-chave, PT), `norma` (sigla/slug opcional, ex.: `CDC`, `CF-1988`, `Lei-8078-1990`), `area` (slugs separados por vírgula, opcional), `limit` (padrão 5, máx 10).

Campos retornados por resultado: `search_id`, `numero`, `citacao` (ex.: `"CDC, art. 14"`), `lei_slug`, `lei_titulo`, `texto`, `is_truncated`, `situacao` (`vigente`|`revogado`|`vetado`|`superada`), `score` (0–1; 1.0 = referência direta), `breadcrumb`, `section_id`, `source_url`.

Notas:
- Para um artigo já conhecido (norma + número), prefira `acervo · consultar`.
- `score` baixo (~0.5–0.6) pode indicar correspondência fraca — leia o `texto` e avalie a pertinência.

## `legislacao-federal · explorar_contexto` — sumário e relações

Navega o índice da lei **um nível por vez** e, para um artigo, traz as relações mapeadas (`cita`/`citado_por`/`altera`).

Params: `search_id` (um artigo — traz suas relações) **ou** `norma` + `section_id` (uma seção; `section_id` vazio = nível superior). `direction` (`cita`/`citado_por`/vazio), `limit`/`offset` para paginar artigos da seção.

Atenção: as relações vêm de remissões explícitas e alterações do texto oficial — **não** são exaustivas das remissões em prosa ("na forma do art. X"). `relacoes` vazio não significa ausência de citações.

## `acervo · consultar` — texto integral (não truncado)

Param obrigatório: `dominio`.

- `dominio: "legislacao"`: `search_ids` (handles de `buscar_artigos`/`explorar_contexto`, podem cruzar leis) **ou** `norma` + `numeros` (até 5 artigos da MESMA lei, ex.: `["121", "121-A", "129"]`). Cada artigo traz `situacao`, `breadcrumb`, `section_id`.
- `dominio: "jurisprudencia"` + `esfera` (`"federal"`/`"estadual"`): `search_ids` **ou** uma `citacao` conhecida (ex.: `"STF SV 11"`, `"STJ Tema 69"`, `"STJ Súmula 7"`, `"TST OJ 191"`; estadual: `"TJAM IRDR Tema 5"`). Retorna o registro **mesmo se não vigente** — verifique `situacao` antes de citar. Cada precedente traz `legislacao_citada` (artigos citados, cada um com `search_id` para saltar via `consultar`).

Retorna até 5 registros por chamada; o excedente e os não encontrados voltam em `omitidos`.

## `jurisprudencia-federal · buscar_precedentes` — busca ampla

Cobre STF, STJ, TST, CARF: súmulas, súmulas vinculantes, temas de repercussão geral e repetitivos, OJs, enunciados, acórdãos, informativos.

Params: `query`, `autoridade` (`STF`,`STJ`,`TST`,`CARF` — vírgula para vários), `tipo`, `eficacia` (`vinculante`|`obrigatoria`|`persuasiva`), `area`, `incluir_nao_vigentes` (padrão false), `limit` (máx 10).

Campos: `eficacia`, `situacao`, enunciado (veja `is_truncated`), `search_id`, `score`. Dica: restrinja por `autoridade` para evitar ruído (penal/civil/constitucional → `STF,STJ`; trabalhista → `TST`; tributário administrativo → `CARF`).

## `jurisprudencia-federal · buscar_vinculantes` — só vinculantes (art. 927 CPC)

Restrito a súmulas vinculantes do STF, temas de repercussão geral (STF) e temas repetitivos (STJ). Todos com `eficacia: vinculante` e (por padrão) `situacao: vigente`.

Params: `query`, `autoridade` (`STF`,`STJ`), `area`, `incluir_nao_vigentes`, `limit`.

## `jurisprudencia-estadual · buscar_vinculantes` — IRDRs dos TJs

IRDRs (art. 927, III, CPC). Um IRDR vincula **apenas** no âmbito do TJ que o decidiu (a UF correspondente); fora dela é persuasivo.

Params: `localidade` (**obrigatório** — sigla da UF, ex.: `"AM"`, `"SP"`; ou exatamente `"BR"` para busca nacional), `query`, `incluir_nao_vigentes`, `limit` (máx 10). Cada resultado traz `eficacia`, `situacao`, `uf`, órgão julgador, `search_id`, `score`.

## `acervo · reclame_aqui` — feedback do agente

Canal do agente para a equipe da Letra da Lei. **Registre sempre que perceber** um problema ao usar qualquer ferramenta deste MCP. Uma chamada por problema.

Params: `category` (**obrigatório**: `gap` | `inconsistencia` | `erro_factual` | `resultado_irrelevante` | `cobertura_ausente` | `outro`), `description` (**obrigatório**, específica e acionável), `context` (a consulta + resultados problemáticos), `dominio`, `esfera`, `tool`, `search_id`, `severity` (`baixa`/`media`/`alta`) — opcionais. Na dúvida sobre registrar, registre.

---

## Checklist antes de citar

- Conferiu `situacao`? Só `vigente` entra sem ressalva.
- Texto `is_truncated: true`? Buscou o integral via `acervo · consultar`.
- Tem `citacao` + `source_url` (legislação) ou `search_id` + `eficacia` (jurisprudência)?
- Resultado fraco/ausente? Registrou via `acervo · reclame_aqui` e sinalizou a lacuna ao usuário.
