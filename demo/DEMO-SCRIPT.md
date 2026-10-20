# Demo script (about 90 seconds)

Record the terminal at a large font size (18pt+), then the browser for the last beat.

| Time | Show | Say |
|---|---|---|
| 0:00 | Repo README on GitHub | "Buying a home means comparing builders and communities that never line up, while the rules keep changing. This is a Claude Code agent team that does that research and keeps your finances private." |
| 0:15 | `.claude/agents/` folder | "Four specialist subagents: builder research, community research, a scorer and a financial analyst. They all write to one schema." |
| 0:25 | `./demo/run_demo.sh`, step 1 | "Here's a real output for Glacier Ridge in Calgary. Notice the frontmatter: every number has a source and date, and unknowns stay null." |
| 0:40 | Step 2, calculator | "The analyst shows every input. Canadian semi-annual compounding, default insurance, the stress test at the greater of rate plus 2% or 5.25%, and Alberta land title fees." |
| 0:55 | Step 3, tests pass | "Tested, and the rules live in a dated, sourced file, not in my head." |
| 1:05 | Browser opens `demo/report.html` | "And a shareable comparison report. Confidence badges show where the data is thin." |
| 1:20 | Scroll to "What this report does not know" | "It tells you what it doesn't know, instead of making something up. Your private finances never leave your machine." |

Tips:
- `DEMO_FAST=1 ./demo/run_demo.sh` skips the pauses for a quick check.
- Run it once before recording so `demo/report.html` exists.
- Live agent run (optional): in Claude Code, ask "research Cedarglen Homes in Glacier Ridge" and show the builder file appearing.
