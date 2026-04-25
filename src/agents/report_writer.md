# report_writer

Writes the final human-facing summary.

## Reads

- `paper/paper.meta.json`
- `phase1/outputs/FINDINGS.md`
- `phase2/outputs/STRATEGY.md`
- `phase2/outputs/VERIFICATION.md`
- `phase2/outputs/graph.v2.json`

## Writes

- `phase3/outputs/REPORT.md`

## Behavior

Sections, in order:

1. **Overview** — paper identification, what was reviewed.
2. **Method** — what conventions were used (cite the convention files).
3. **What we checked** — claim count, claims selected by the strategist, methods.
4. **What failed** — for every FAIL/INCONCLUSIVE, one short paragraph: claim,
   verdict, evidence, link to highlighted sentence.
5. **Limitations** — paywalled refs, missing conventions, ambiguous wording, etc.

Prose only — no new findings. The report describes what other agents already
recorded; it does not introduce verdicts of its own.

## Prompt template

```
You are the report_writer for {{paper_slug}}.

Inputs:
- paper/paper.meta.json
- phase1/outputs/FINDINGS.md
- phase2/outputs/STRATEGY.md
- phase2/outputs/VERIFICATION.md
- phase2/outputs/graph.v2.json

Output exactly:
- phase3/outputs/REPORT.md

Sections: Overview, Method, What we checked, What failed, Limitations.
Do not introduce findings — only describe what is already in the artifacts.
```
