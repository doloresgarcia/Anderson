# claim_extractor

Runs `src/extract_claims.py` on the paper and writes `claims.jsonl`. Mechanical wrapper — no judgment, no post-processing, no review.

## Reads

- `paper/paper.tex`

## Writes

- `phase1/outputs/claims.jsonl` — canonical claim list (schema: `src/claims_schema.md`)
- `phase1/agents/claim_extractor/log.md` — captures the script's stderr summary

## Behavior

Run the script, write the JSONL, capture stderr to `log.md`. That's it. Quality review of the output is `claim_reviewer`'s job.

## Prompt template

```
You are the claim_extractor for {{paper_slug}}.

Run from the repo root:

  python src/extract_claims.py paper/paper.tex -o phase1/outputs/claims.jsonl 2> phase1/agents/claim_extractor/log.md

That's the whole job. Don't read claims.jsonl. Don't reformat anything.
Don't filter or judge. claim_reviewer runs next.
```
