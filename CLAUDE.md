# Home Buyer Guide

Research workspace for a home purchase. Method lives in `docs/framework.md`; subagents in `.claude/agents/`.

- Personal inputs: `PRIVATE-FINANCES.md` and `PROJECT-GUIDE.md` (gitignored). If they don't exist, copy from the `.template.md` files and ask the user to fill them in.
- Research output (`builders/`, `communities/`, `fieldwork/`) is gitignored and stays local.
- Never commit personal finances, names, addresses, quotes or credentials. Before any commit, check `git status` for anything that looks personal.
- Never invent figures. Unknown means `null` / "unknown".
