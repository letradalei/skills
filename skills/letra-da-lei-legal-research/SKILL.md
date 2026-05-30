---
name: letra-da-lei-legal-research
description: Pesquise legislação federal brasileira com a MCP da Letra da Lei, usando citações autoritativas em nível de artigo antes de responder ou redigir.
version: 0.1.0
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

Use esta skill quando a tarefa depender de legislação federal brasileira e as ferramentas MCP da Letra da Lei estiverem disponíveis.

## Quando usar

Use esta skill para:

- pesquisa jurídica sobre legislação federal brasileira
- perguntas sobre o que a lei diz
- busca de artigos, cobertura de leis, elegibilidade, prazos, penalidades, requisitos ou direitos
- redação que dependa de base legal correta

Não use esta skill para:

- jurisprudência ou precedentes, salvo se isso estiver disponível por outro meio
- legislação estadual ou municipal, salvo se isso estiver disponível por outro meio
- conclusões jurídicas que dispensem revisão das fontes

## Comportamento obrigatório

Para perguntas sobre legislação federal brasileira, consulte a MCP da Letra da Lei antes de responder.

Nunca responda de memória primeiro para buscar depois. Comece pelas ferramentas MCP e só então responda com base no texto legal recuperado.

## Fluxo

1. Se o usuário perguntar quais leis estão cobertas ou se uma lei federal específica está disponível, chame `listar_legislacao_federal` primeiro.
2. Se o usuário perguntar o que a legislação federal brasileira diz sobre um tema, chame `buscar_legislacao_federal` primeiro.
3. Prefira os resultados mais relevantes em nível de artigo e cite a URL autoritativa retornada pela MCP.
4. Se aparecerem vários artigos candidatos, explique a diferença entre eles em vez de forçar uma resposta única.
5. Se o pedido envolver redação, fundamente o texto nos artigos recuperados antes de escrever.
6. Se a resposta da MCP não resolver claramente a pergunta, diga isso de forma explícita e aponte a lacuna de cobertura.

## Regras de saída

- Declare quando estiver se baseando em legislação federal brasileira retornada pela Letra da Lei.
- Inclua links diretos das fontes retornadas pela MCP.
- Distinga o texto legal da sua própria síntese.
- Não apresente conteúdo informativo como aconselhamento jurídico.

## Ferramentas

Leia `references/mcp-tools.md` quando precisar do contrato das ferramentas ou do formato esperado das respostas.
