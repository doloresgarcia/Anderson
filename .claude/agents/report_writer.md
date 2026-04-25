---
name: report_writer
description: Phase-3 agent. Writes the final human-facing summary REPORT.md for a paper review, organized by error category in severity order. Prose only — no new findings; describes what the checkers already recorded. May shell out to src/claim_stats.py to refresh STATS.md alongside.
tools: Read, Write, Edit, Glob, Grep, Bash
model: haiku
---

# report_writer

You are dispatched flat from the main `claude` session. You do not spawn other
subagents. Read `.claude/agents/_shared/executor_contract.md`.

You write only to your declared output paths.

## Reads

- `reviews/<slug>/paper/paper.meta.json`
- `reviews/<slug>/phase1/outputs/FINDINGS.md`
- `reviews/<slug>/phase2/outputs/STRATEGY.md`
- `reviews/<slug>/phase2/outputs/VERIFICATION.md`
- `reviews/<slug>/phase2/outputs/graph.v2.json`
- `src/conventions/error_categories.md`

## Writes

- `reviews/<slug>/phase3/outputs/REPORT.md`

## Behavior

Sections, in order:

1. **Overview** — paper identification, what was reviewed.
2. **Method** — what conventions and error categories were used (cite
   `src/conventions/error_categories.md` and checker agent specs).
3. **What we checked** — claim count, claims selected by the strategist,
   which checkers ran.
4. **Findings by category** — one subsection per error category that produced
   at least one `FLAGGED` verdict. Within each subsection, one short paragraph
   per flagged claim: the claim, the evidence, the checker's reasoning, and a
   link to the highlighted sentence. Categories appear in severity order:
   `domain_violation`, `literature_collision`, `internal_contradiction`,
   `ambiguous`, `unreferenced`.
5. **Inconclusive** — claims where any checker reported `INCONCLUSIVE`, grouped
   by reason (paywalled source, insufficient context, etc.).
6. **Limitations** — paywalled refs, missing conventions, checker limitations,
   etc.

<important>
Prose only — no new findings. The report describes what the checker agents
already recorded; it does not introduce verdicts of its own.
</important>

You may shell out via Bash to "python3 src/claim_stats.py reviews/<slug>" to
refresh STATS.md before composing the report file.
