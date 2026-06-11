# Letra da Lei — Skills

Marketplace de plugins do [Claude Code](https://claude.com/claude-code) com as skills jurídicas da **Letra da Lei**: pesquisa de legislação e jurisprudência brasileiras (via MCP) e redação de peças processuais com fundamentação verificada.

> Projeto open source sob licença [MIT](LICENSE). Contribuições são bem-vindas — veja o [CONTRIBUTING.md](CONTRIBUTING.md).

## Instalação (Claude Code)

```bash
/plugin marketplace add letradalei/skills
/plugin install letra-da-lei@letradalei
```

Após instalar, as skills ficam disponíveis com o prefixo do plugin, ex.: `/letra-da-lei:pesquisa-juridica`, `/letra-da-lei:peticao-inicial`. O `.mcp.json` do plugin conecta automaticamente o servidor MCP `letradalei` (`https://mcp.letradalei.com/mcp`).

## As skills

| Skill | O que faz |
|---|---|
| `pesquisa-juridica` | Pesquisa e cita legislação e jurisprudência pelo MCP. **Skill-base** — as demais a carregam. |
| `peticao-inicial` | Redige petição inicial (CPC art. 319). |
| `contestacao` | Redige contestação cível (CPC arts. 335–342). |
| `fundamentacao-judicial` | Estrutura a fundamentação judicial conforme o art. 489, § 1º do CPC. |
| `analise-processual-minuta` | Diagnostica a fase processual e redige a peça cabível (réplica, recursos, cumprimento, embargos, ações autônomas etc.). |

As skills de redação produzem **rascunhos revisáveis**, não peças prontas. Quem assina, decide estratégia e protocola é o(a) advogado(a) ou magistrado(a) habilitado(a).

## Estrutura do repositório

```text
.
├── .claude-plugin/marketplace.json     ← catálogo (lista o plugin letra-da-lei)
├── plugins/letra-da-lei/
│   ├── .claude-plugin/plugin.json
│   ├── .mcp.json                       ← conecta o MCP letradalei
│   ├── README.md
│   └── skills/<slug>/SKILL.md          ← uma pasta por skill
├── skills/skill-template/SKILL.md      ← modelo para novas skills
├── scripts/validate-skills.sh
└── .github/workflows/validate.yml
```

## Pré-requisito: o MCP

As skills consultam o servidor MCP `letradalei` para obter texto autoritativo de lei e jurisprudência — **nunca a memória do modelo**. Sem o MCP conectado, a skill avisa e para. A `pesquisa-juridica` é a skill-base que centraliza o uso do MCP (ferramentas, parâmetros, verificação de vigência e citação); as peças a carregam em vez de repetir o contrato.

## Como contribuir

Leia o [CONTRIBUTING.md](CONTRIBUTING.md). Em resumo:

- Skills ficam em `plugins/letra-da-lei/skills/<slug>/SKILL.md`.
- `name` no frontmatter é **kebab-case puro** (o prefixo `letra-da-lei:` é aplicado automaticamente).
- Corpo das skills em **português**.
- Para acesso ao MCP, **carregue a skill `pesquisa-juridica`** em vez de repetir o contrato das ferramentas.
- Valide antes de abrir PR: `bash ./scripts/validate-skills.sh`.

## Validação

```bash
bash ./scripts/validate-skills.sh
```

Verifica o `marketplace.json`, os `plugin.json` e o frontmatter de cada `SKILL.md` (campos `name`/`description` e nome sem dois-pontos). O GitHub Actions roda a mesma validação em pushes e pull requests.

## Licença

[MIT](LICENSE) © Letra da Lei.
