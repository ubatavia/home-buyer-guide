# Home Buyer Guide — a Claude Code research workspace

A template for researching a home purchase with Claude Code subagents: compare builders and communities with a consistent schema, score them with weights you choose, and run affordability math without putting your finances in git.

This repo contains the **method only**. Your personal data lives in files that are gitignored.

## How it works

| Piece | What it does |
|---|---|
| `docs/framework.md` | Research schema (YAML frontmatter), scoring method, rules-and-programs log |
| `.claude/agents/builder-researcher.md` | Researches one builder into `builders/<slug>.md` |
| `.claude/agents/community-researcher.md` | Researches one community into `communities/<slug>.md` |
| `.claude/agents/decision-scorer.md` | Builds the scoring matrix from the research files |
| `.claude/agents/financial-analyst.md` | Mortgage, stress-test and all-in cost math, shown with inputs |
| `PRIVATE-FINANCES.template.md` | Copy to `PRIVATE-FINANCES.md` and fill in (gitignored) |
| `PROJECT-GUIDE.template.md` | Copy to `PROJECT-GUIDE.md`: your requirements and location (gitignored) |

## Getting started

1. Use this repo as a template (or clone it), then open it in Claude Code.
2. `cp PRIVATE-FINANCES.template.md PRIVATE-FINANCES.md` and `cp PROJECT-GUIDE.template.md PROJECT-GUIDE.md`. Fill both in. Both are gitignored.
3. Ask Claude to research a builder or community. The subagents write into `builders/` and `communities/`, which are also gitignored so your shortlist stays private.
4. Ask the decision-scorer to build the matrix once you've set weights in `docs/framework.md`.

## Principles

- **No invented numbers.** Unknowns stay `null`; every figure needs a source and date.
- **Rules change.** Mortgage stress tests, program limits and rebates are re-verified each time, never taken from memory.
- **Privacy by default.** Personal finances, requirements, shortlist and field notes never leave your machine.
- **Not financial advice.** Confirm anything important with a licensed mortgage broker, lawyer or accountant.
