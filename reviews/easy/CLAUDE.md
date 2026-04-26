# Review — easy

Per-paper context for the Anderson orchestrator. The orchestrator itself lives
at the **repo-root `CLAUDE.md`**; this file is just paper-specific framing.

## Paper

- meta: `reviews/easy/paper/paper.meta.json`
- text: `reviews/easy/paper/paper.txt`
- pdf:  `reviews/easy/paper/paper.pdf` (if present)

## Phase outputs

- phase 1: `reviews/easy/phase1/outputs/` — CLAIMS.md, LITERATURE.md, references.bib, graph.v1.json, FINDINGS.md
- phase 2: `reviews/easy/phase2/outputs/` — STRATEGY.md, VERIFICATION.md, graph.v2.json
- phase 3: `reviews/easy/phase3/outputs/` — graph.final.json + graph.final.html, STATS.md, REPORT.md, paper.highlighted.pdf (PDF input; also text input if PyMuPDF is available), paper.highlighted.html (text input)

## Notes

Reviews are **not** self-contained. Agents and conventions resolve via the
repo (`.claude/agents/`, `src/methodology/`, `src/conventions/`,
`literature_bank/`), not via per-review symlinks. To run this review, invoke
the slash commands from the repo root:

- `/phase1 easy`
- `/phase2 easy`
- `/phase3 easy`
- `/render easy` (re-run deterministic Phase-3 renderers)
