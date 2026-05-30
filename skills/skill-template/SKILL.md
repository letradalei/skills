---
name: skill-template
description: Skill modelo com a estrutura mínima para uma skill portátil neste repositório.
version: 0.1.0
authors:
  - letradalei
tags:
  - template
  - agent-skills
license: Proprietary
repository: https://github.com/letradalei/skills
---

# Skill Modelo

Use este modelo ao criar uma nova skill neste repositório.

## Regras

- Mantenha o fluxo principal neste arquivo.
- Mova material de apoio extenso para `references/` apenas quando necessário.
- Adicione auxiliares determinísticos em `scripts/` quando repetição ou confiabilidade importarem.
- Remova o texto de modelo antes de publicar uma skill real.

## Fluxo de autoria

1. Renomeie a pasta para o slug final da skill.
2. Substitua o frontmatter pelo nome, descrição e tags reais.
3. Reescreva as instruções em torno de uma tarefa concreta.
4. Adicione `agents/openai.yaml` quando a skill precisar aparecer corretamente nas interfaces dos agentes.
