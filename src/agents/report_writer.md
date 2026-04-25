# report_writer

Writes the final human-facing summary.

## Reads

- `paper/paper.meta.json`
- `phase1/outputs/FINDINGS.md`
- `phase2/outputs/STRATEGY.md`
- `phase2/outputs/VERIFICATION.md`
- `phase2/outputs/graph.v2.json`
- `phase3/outputs/STATS.md` (produced by `src/claim_stats.py` — see below)

## Writes

- `phase3/outputs/REPORT.md`

## Behavior

**First step: regenerate STATS.md.** Always run the stats utility before
writing prose, so the numbers in the report are guaranteed to match the
underlying artifacts:

```bash
python3 ../../src/claim_stats.py .
```

This writes `phase3/outputs/STATS.md` with type counts, confidence counts,
verdict breakdown, type×verdict matrix, coverage, methods used, INCONCLUSIVE
reasons, and per-group rows.

Then write `REPORT.md` with these sections, in order:

1. **Trust score** — copy the score banner verbatim from `STATS.md`'s top
   section. This is the headline of the report; place it before everything
   else so a reader who reads only the first lines knows the verdict.
2. **Overview** — paper identification, what was reviewed.
3. **Method** — what conventions were used (cite the convention files).
4. **Statistics** — short prose summarizing the key numbers. **Quote** the
   relevant rows of `STATS.md` rather than recomputing them; embed
   `STATS.md`'s tables verbatim where they help.
5. **What we checked** — claim count, claims selected by the strategist,
   methods used.
6. **What failed** — for every FAIL/INCONCLUSIVE, one short paragraph:
   claim, verdict, evidence, link to highlighted sentence.
7. **Limitations** — paywalled refs, missing conventions, ambiguous wording,
   etc.

Prose only (apart from the verbatim STATS tables) — no new findings. The
report describes what other agents already recorded; it does not introduce
verdicts of its own. Numbers in prose must match `STATS.md` — if they
disagree, the report is wrong (the stats are mechanical).

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
