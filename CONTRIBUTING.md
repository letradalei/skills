# Contribuindo

Obrigado por contribuir com as skills da Letra da Lei! Este repositório é um **marketplace de plugins do Claude Code**. Toda contribuição passa por validação automática e revisão.

## Pré-requisitos

- [Claude Code](https://claude.com/claude-code) instalado.
- Acesso ao servidor MCP `letra-da-lei` (`https://mcp.letradalei.com/mcp`) para testar skills que consultam lei ou jurisprudência.

## Onde ficam as skills

```
plugins/letra-da-lei/skills/<slug>/SKILL.md
```

Cada skill é uma pasta com um `SKILL.md`. Material extenso (módulos, tabelas longas) vai em `references/` ao lado, carregado **sob demanda** — veja `analise` como exemplo.

## Convenções

- **Idioma:** corpo das skills em **português** (são peças e consultas do direito brasileiro).
- **`name` em kebab-case puro** (ex.: `peticao`). **Não** use dois-pontos — o prefixo `letradalei:` é aplicado automaticamente na invocação. Nome com `:` é inválido e reprova na validação.
- **`description` curta e específica:** o que a skill faz, gatilhos de uso e quando **não** usar. Evite `: ` (dois-pontos seguido de espaço) em valor YAML não-aspeado — quebra o parser; use travessão (`—`) ou aspas.
- **Acesso ao MCP:** carregue a skill `letradalei:pesquisa` em vez de repetir o contrato das ferramentas. Ela centraliza ferramentas, parâmetros, verificação de vigência e formato de citação.
- **Fundamentação verificada:** nunca cite lei ou precedente de memória — tudo vem do MCP. Marque lacunas (`[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS]`, `[VERIFICAR]`) em vez de inventar.
- **Skills grandes:** mantenha o `SKILL.md` enxuto (diagnóstico + roteamento) e mova módulos mutuamente exclusivos para `references/`. Carregar tudo a cada invocação desperdiça contexto.
- **Sem dados sensíveis:** nada de PII, credenciais ou peças com dados reais de clientes no repositório. Documentos gerados (`outputs/`, `*.docx`) são ignorados pelo `.gitignore` — mantenha assim.

## Criando uma skill nova

1. Copie `skills/skill-template/` para `plugins/letra-da-lei/skills/<slug>/`.
2. Reescreva o `SKILL.md` em torno de **uma** tarefa concreta; ajuste `name` (kebab puro) e `description`.
3. Se precisar do MCP, instrua a carregar `letradalei:pesquisa`.
4. Valide: `bash ./scripts/validate-skills.sh`.

## Fluxo de Pull Request

1. Crie um branch a partir de `main`.
2. Faça as alterações e rode `bash ./scripts/validate-skills.sh` localmente.
3. Abra um PR descrevendo **o quê** e **o porquê**. O CI roda a mesma validação.
4. Aguarde a revisão. Mantenha o PR focado em uma mudança coerente.

## Código de Conduta

Ao participar, você concorda com o [Código de Conduta](CODE_OF_CONDUCT.md).

## Licença

Ao contribuir, você concorda em licenciar sua contribuição sob a licença [MIT](LICENSE) do projeto.
