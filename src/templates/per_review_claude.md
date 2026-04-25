# Review — {{paper_slug}}

Per-paper context for the Anderson orchestrator. The orchestrator itself lives
at the **repo-root `CLAUDE.md`**; this file is just paper-specific framing.

## Paper

- meta: `reviews/{{paper_slug}}/paper/paper.meta.json`
- text: `reviews/{{paper_slug}}/paper/paper.txt`
- pdf:  `reviews/{{paper_slug}}/paper/paper.pdf` (if present)

## Phase outputs

- phase 1: `reviews/{{paper_slug}}/phase1/outputs/` — CLAIMS.md, LITERATURE.md, references.bib, graph.v1.json, FINDINGS.md
- phase 2: `reviews/{{paper_slug}}/phase2/outputs/` — STRATEGY.md, VERIFICATION.md, graph.v2.json
- phase 3: `reviews/{{paper_slug}}/phase3/outputs/` — graph.final.json + graph.final.html, paper.highlighted.{pdf,html}, REPORT.md, STATS.md

## Notes

Reviews are **not** self-contained. Agents and conventions resolve via the
repo (`.claude/agents/`, `src/methodology/`, `src/conventions/`,
`literature_bank/`), not via per-review symlinks. To run this review, invoke
the slash commands from the repo root:

- `/phase1 {{paper_slug}}`
- `/phase2 {{paper_slug}}`
- `/phase3 {{paper_slug}}`
- `/render {{paper_slug}}` (re-run deterministic Phase-3 renderers)
