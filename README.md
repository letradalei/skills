# letradalei/skills

Claude Code **plugin marketplace** for the Letra da Lei legal skills.

This repo is the source of truth for the `letra-da-lei` plugin — a bundle of Brazilian legal skills (statute + case-law research and processual drafting) that connect to the Letra da Lei MCP for authoritative, citable sources. It is installable directly from GitHub.

## Install (Claude Code)

```bash
/plugin marketplace add letradalei/skills
/plugin install letra-da-lei@letradalei
```

After install, the skills are available namespaced by the plugin, e.g. `/letra-da-lei:pesquisa-juridica`, `/letra-da-lei:peticao-inicial`. The bundled `.mcp.json` connects the `letradalei` MCP server (`https://mcp.letradalei.com/mcp`) automatically.

## Repository structure

This repo follows the Claude Code marketplace layout: a root marketplace manifest points at the bundled plugin, whose skills each live in their own `SKILL.md` directory.

```text
.
├── .claude-plugin/
│   └── marketplace.json              ← catalog: lists the letra-da-lei plugin
├── plugins/
│   └── letra-da-lei/
│       ├── .claude-plugin/plugin.json
│       ├── .mcp.json                 ← bundles the letradalei MCP server
│       ├── README.md
│       └── skills/
│           ├── pesquisa-juridica/SKILL.md        ← MCP research (skill-base)
│           ├── peticao-inicial/SKILL.md
│           ├── contestacao/SKILL.md
│           ├── fundamentacao-judicial/SKILL.md
│           └── analise-processual-minuta/SKILL.md
├── skills/
│   └── skill-template/SKILL.md       ← authoring template (not shipped in the plugin)
├── scripts/validate-skills.sh
└── .github/workflows/validate.yml
```

## The plugin

`letra-da-lei` bundles five skills. **`pesquisa-juridica`** is the skill-base: it documents how to use the MCP (legislation + jurisprudence tools, parameters, vigência/`situacao` checks, integral-text retrieval, gap reporting). The four drafting skills **load `pesquisa-juridica`** for every legal lookup instead of repeating the MCP contract.

| Skill | Does |
|---|---|
| `pesquisa-juridica` | Search and cite legislation + jurisprudence via the MCP. Loaded by the others. |
| `peticao-inicial` | Drafts a petição inicial (CPC art. 319). |
| `contestacao` | Drafts a contestação (CPC arts. 335–342). |
| `fundamentacao-judicial` | Structures judicial reasoning against CPC art. 489, § 1º. |
| `analise-processual-minuta` | Diagnoses the procedural stage and drafts the fitting peça. |

## Skill layout

Each skill lives at `plugins/letra-da-lei/skills/<slug>/SKILL.md`.

- **`name:` must be bare kebab-case** (e.g. `peticao-inicial`) — Claude Code applies the `letra-da-lei:` namespace automatically. A colon in `name:` is invalid.
- `description:` is recommended; Claude uses it to decide when to invoke the skill.
- Optional `references/` holds material the agent reads only when needed.

## Authoring principles

- Skill bodies are in Portuguese (Brazilian legal practice).
- Keep the core procedure inside `SKILL.md`; move long material to `references/`.
- Ground legal output in retrieved law/precedents, never model memory; route through `pesquisa-juridica`.
- Preserve the boundary between retrieved source, synthesis, and legal advice. The MCP remains the source of truth for coverage, article text, and source URLs.
- Signal over noise: don't repeat the MCP contract per skill — load `pesquisa-juridica`.

## Validation

```bash
bash ./scripts/validate-skills.sh
```

Checks that `marketplace.json` exists and is valid JSON, that any `plugin.json` is valid JSON, and that every `SKILL.md` has `name:` + `description:` frontmatter with a bare (colon-free) name. The GitHub Actions workflow runs the same validation on pushes and pull requests.

## Creating a new skill

1. Copy `skills/skill-template/` into `plugins/letra-da-lei/skills/<slug>/`.
2. Rewrite `SKILL.md` around one concrete job; set `name:` to the bare slug.
3. If it needs the MCP, tell it to load `letra-da-lei:pesquisa-juridica` rather than re-documenting the tools.
4. Run `bash ./scripts/validate-skills.sh` before committing.
