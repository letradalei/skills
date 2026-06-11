---
name: letra-da-lei-legal-research
description: Pesquise legislação federal e jurisprudência brasileiras com a MCP da Letra da Lei, usando citações autoritativas em nível de artigo/precedente antes de responder ou redigir.
version: 0.2.0
authors:
  - letradalei
tags:
  - brazil-law
  - legal-research
  - mcp
  - citations
platforms:
  - codex
  - claude-code
  - cursor
license: Proprietary
repository: https://github.com/letradalei/skills
---

# Pesquisa Jurídica Letra da Lei

Use esta skill quando a tarefa depender de legislação federal ou jurisprudência brasileiras e as ferramentas MCP da Letra da Lei estiverem disponíveis.

## Quando usar

Use esta skill para:

- pesquisa sobre legislação federal brasileira (o que a lei diz, prazos, requisitos, penalidades, direitos)
- pesquisa de jurisprudência federal (STF, STJ, TST, CARF) e de IRDRs estaduais (TJs)
- descoberta de cobertura: quais leis/tribunais o acervo indexa
- redação que dependa de base legal ou de precedentes corretos

Não use esta skill para:

- legislação estadual ou municipal (fora do acervo), salvo se disponível por outro meio
- conclusões jurídicas que dispensem revisão das fontes

## Comportamento obrigatório

Para qualquer pergunta sobre legislação federal ou jurisprudência brasileiras, **consulte a MCP da Letra da Lei antes de responder.** Nunca responda de memória primeiro para buscar depois — comece pelas ferramentas e só então responda com base no texto recuperado.

## Ferramentas (nomes reais expostos pela MCP)

A MCP expõe ferramentas em grupos. Use sempre o nome do grupo + operação:

| Grupo · operação | Para quê |
|---|---|
| `acervo · listar` | Descobrir cobertura. `dominio: "legislacao"` (sem `area` → índice de áreas; com `area` → leis daquela área) ou `dominio: "jurisprudencia"` + `esfera` (tribunais, tipos, eficácia). |
| `legislacao-federal · buscar_artigos` | Busca semântica de artigos. Params: `query`, `norma` (sigla/slug, opcional), `area` (opcional), `limit`. |
| `legislacao-federal · explorar_contexto` | Navega o sumário da lei (um nível por vez) e as relações de um artigo (`cita`/`citado_por`/`altera`). |
| `acervo · consultar` | Texto **integral** (não truncado). `dominio: "legislacao"` (`search_ids`, ou `norma` + `numeros`) ou `dominio: "jurisprudencia"` (`esfera` + `search_ids`/`citacao`). |
| `jurisprudencia-federal · buscar_precedentes` | Busca ampla (súmulas, temas, OJs, acórdãos). Filtros: `autoridade`, `tipo`, `eficacia`, `area`. |
| `jurisprudencia-federal · buscar_vinculantes` | Só vinculantes do art. 927 CPC (SV, repercussão geral, repetitivos). |
| `jurisprudencia-estadual · buscar_vinculantes` | IRDRs dos TJs. Param **obrigatório** `localidade` (UF, ou `"BR"`). |
| `acervo · reclame_aqui` | Registrar lacuna/erro/resultado irrelevante do acervo. Use sempre que a MCP falhar. |

Leia `references/mcp-tools.md` para o contrato completo de cada ferramenta (params, campos retornados, exemplos).

## Fluxo

1. Se o usuário perguntar quais leis/tribunais estão cobertos, ou se uma fonte específica existe, chame `acervo · listar` primeiro.
2. Se a pergunta for sobre legislação, chame `legislacao-federal · buscar_artigos` (restrinja com `norma` quando souber a lei).
3. **Antes de citar texto verbatim, confirme com `acervo · consultar`** — especialmente se o resultado vier com `is_truncated: true`.
4. **Confira `situacao`** (`vigente`|`revogado`|`vetado`|`superada`): nunca cite como vigente um dispositivo revogado/vetado/superado.
5. Se a pergunta for sobre jurisprudência, use `buscar_precedentes` (amplo) ou `buscar_vinculantes` (só vinculantes); para IRDRs estaduais, `jurisprudencia-estadual · buscar_vinculantes` com `localidade`. Confira `eficacia` e `situacao`.
6. Se vários artigos/precedentes forem candidatos, explique a diferença em vez de forçar uma resposta única.
7. Se o pedido envolver redação, fundamente o texto nas fontes recuperadas antes de escrever.
8. Se a MCP não resolver a pergunta (zero resultados, cobertura fina, resultado irrelevante), **registre com `acervo · reclame_aqui`** e diga ao usuário, de forma explícita, qual é a lacuna de cobertura.

## Regras de saída

- Declare quando estiver se baseando em fontes retornadas pela Letra da Lei.
- Inclua o `source_url` e a `citacao` retornados pela MCP (e o `search_id` quando útil para reconsulta).
- Distinga o texto legal/precedente da sua própria síntese.
- Não apresente conteúdo informativo como aconselhamento jurídico.
