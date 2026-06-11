---
name: skill-template
description: Modelo mínimo para uma nova skill da Letra da Lei. Substitua por uma descrição real — o que a skill faz, gatilhos de uso e quando não usar.
argument-hint: "[descrição curta do argumento, se houver]"
---

# Skill Modelo

Use este modelo ao criar uma nova skill. Copie esta pasta para `plugins/letra-da-lei/skills/<slug>/` e reescreva.

## Convenções

- `name` em **kebab-case puro** (sem `:` — o prefixo `letra-da-lei:` é aplicado automaticamente).
- Corpo em **português**.
- Para consultar lei ou jurisprudência, **carregue a skill `letra-da-lei:pesquisa-juridica`** em vez de repetir o contrato do MCP.
- Material de apoio extenso vai em `references/` ao lado, carregado sob demanda.

## Fluxo de autoria

1. Renomeie a pasta para o slug final da skill.
2. Ajuste o frontmatter (`name` kebab puro, `description` curta e específica).
3. Reescreva as instruções em torno de **uma** tarefa concreta.
4. Remova este texto de modelo.
5. Valide: `bash ./scripts/validate-skills.sh`.
