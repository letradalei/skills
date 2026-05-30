# letradalei/skills

Repository for portable agent skills used by Letra da Lei.

This repo is the source of truth for `SKILL.md`-based skills that can be installed into Codex, Claude Code, Cursor, and other compatible agent runtimes. The goal is to keep Letradalei-specific behavior in one place, version it cleanly, and make it easy to test skills directly from GitHub.

## Purpose

This repository exists to:

- store reusable agent skills in a standard format
- mirror Letra da Lei product behavior as portable agent instructions
- keep legal research and drafting workflows close to the MCP contract
- support fast install and testing through existing skill tooling

The design assumption is:

- `SKILL.md` is the packaging standard for reusable workflows
- MCP is the capability layer for authoritative tools and data
- this repository should describe how the agent behaves around Letra da Lei, not reimplement the MCP itself

## Repository structure

```text
.
├── .github/workflows/
│   └── validate.yml
├── scripts/
│   └── validate-skills.sh
└── skills/
    ├── letra-da-lei-legal-research/
    │   ├── agents/openai.yaml
    │   ├── references/mcp-tools.md
    │   └── SKILL.md
    └── skill-template/
        ├── agents/openai.yaml
        └── SKILL.md
```

## Skill layout

Each installable skill lives under `skills/<skill-slug>/`.

Required:

- `SKILL.md`: frontmatter plus the core workflow

Recommended:

- `agents/openai.yaml`: UI metadata for agents that support display names and starter prompts

Optional:

- `references/`: supporting material the agent should read only when needed
- `scripts/`: deterministic helpers for repeatable tasks
- `assets/`: output resources or templates

## Authoring principles

Keep skills small, concrete, and biased toward execution.

- Write the skill body in Portuguese when the intended user is Brazilian.
- Keep the core procedure inside `SKILL.md`.
- Move longer supporting material into `references/` instead of bloating the main skill file.
- Use `scripts/` only when determinism or repetition justifies it.
- Prefer explicit tool-routing instructions when legal accuracy depends on MCP use.
- Do not duplicate large chunks of product docs unless the agent actually needs them to operate.

## Letra da Lei-specific guidance

This repo should mirror the behavior of the Letra da Lei legal plugin stack.

That means:

- skills should instruct the agent to use Letra da Lei MCP before answering federal-law questions
- legal answers should be grounded in retrieved statutory text, not model memory
- skills should preserve the boundary between retrieved law, synthesis, and legal advice
- the MCP server remains the source of truth for coverage, article text, and source URLs

This repo should not:

- embed the law corpus itself
- pretend to replace the MCP server
- hardcode large legal reference sets when the MCP can return authoritative results

## Current skills

### `letra-da-lei-legal-research`

Primary legal research skill for Brazilian federal law.

It tells the agent to:

- call `listar_legislacao_federal` when coverage or `law_key` discovery is needed
- call `buscar_legislacao_federal` before answering statutory questions
- cite authoritative source URLs returned by the MCP
- acknowledge coverage gaps instead of guessing

### `skill-template`

Starter template for new skills in this repository.

Use it when creating additional Letradalei skills such as:

- legal drafting grounded in retrieved statutes
- corpus coverage and onboarding helpers
- citation-safe memo writing workflows
- agent behaviors for internal legal teams

## Language policy

Repository plumbing may remain in English when it helps external tooling or collaborators.

Skill-facing content should default to Portuguese when:

- the end user is Brazilian
- the workflow is legal or regulatory
- the wording needs to match Brazilian legal usage closely

If a skill is meant for international operators, bilingual metadata can be added deliberately instead of mixing languages by accident.

## Validation

Run:

```bash
bash ./scripts/validate-skills.sh
```

The validator currently checks that:

- a `skills/` directory exists
- at least one `SKILL.md` exists
- each `SKILL.md` includes `name:` and `description:` frontmatter

The GitHub Actions workflow runs the same validation on pushes and pull requests.

## Installation and testing

This repo is intended to work with GitHub-based skill installers.

Examples:

```bash
npx skills add letradalei/skills --list
npx skills add letradalei/skills --agent codex
```

Suggested testing loop:

1. Update or add a skill in this repo.
2. Run local validation.
3. Commit and push to GitHub.
4. Install the repo into the target agent runtime.
5. Test with realistic prompts that force the expected tool-routing behavior.

## Creating a new skill

1. Copy `skills/skill-template/` into a new slugged folder under `skills/`.
2. Rewrite `SKILL.md` around one concrete job.
3. Add `agents/openai.yaml` metadata that matches the real purpose of the skill.
4. Add `references/` only when the extra material is genuinely needed.
5. Validate the repo before committing.

## Contribution notes

When making changes:

- avoid expanding scope without a concrete skill use case
- keep instructions operational rather than aspirational
- prefer MCP-first legal workflows where applicable
- preserve portability across agent runtimes

If a future skill depends on a new MCP capability, document the dependency clearly in the skill and keep the protocol details in `references/`.
