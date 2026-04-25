# report_writer

Writes the final human-facing summary, organized by error category.

## Reads

- `paper/paper.meta.json`
- `phase1/outputs/FINDINGS.md`
- `phase2/outputs/STRATEGY.md`
- `phase2/outputs/VERIFICATION.md`
- `phase2/outputs/graph.v2.json`
- `conventions/error_categories.md`

## Writes

- `phase3/outputs/REPORT.md`

## Behavior

Sections, in order:

1. **Overview** — paper identification, what was reviewed.
2. **Method** — what conventions and error categories were used (cite
   `conventions/error_categories.md` and checker agent specs).
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

Prose only — no new findings. The report describes what the checker agents
already recorded; it does not introduce verdicts of its own.

## Prompt template

```
You are the report_writer for {{paper_slug}}.

Inputs:
- paper/paper.meta.json
- phase1/outputs/FINDINGS.md
- phase2/outputs/STRATEGY.md
- phase2/outputs/VERIFICATION.md
- phase2/outputs/graph.v2.json
- conventions/error_categories.md

Output exactly:
- phase3/outputs/REPORT.md

Sections: Overview, Method, What we checked, Findings by category,
Inconclusive, Limitations.
Findings grouped by error category in severity order. Do not introduce
findings — only describe what is already in the artifacts.
```
