# claim_extractor

Extracts the set of claims a paper makes.

## Reads

- `paper/paper.txt`
- `paper/paper.meta.json`
- `conventions/claim_taxonomy.md` (defines what counts as a claim and the type set)
- `methodology/05-artifacts.md` (CLAIMS.md format)

## Writes

- `phase1/outputs/CLAIMS.md`
- `phase1/agents/claim_extractor/plan.md`
- `phase1/agents/claim_extractor/log.md`

## Behavior

For every sentence (or sentence group) that asserts a verifiable proposition, emit
one row in `CLAIMS.md` with:

- a stable `claim_id` (`C001`, `C002`, …)
- the type from the taxonomy (or `UNCLASSIFIED` if the taxonomy file is the
  placeholder)
- the literal sentence
- page, line, section
- byte/line provenance into `paper.txt`

If the taxonomy file is the placeholder, every claim is tagged `UNCLASSIFIED` and
the issue is logged in `log.md`. The orchestrator will surface this as a Category B
finding so the user knows the taxonomy needs filling in.

## Prompt template

```
You are the claim_extractor for {{paper_slug}}.

Inputs:
- paper/paper.txt
- paper/paper.meta.json
- conventions/claim_taxonomy.md

Output exactly:
- phase1/outputs/CLAIMS.md  (format: methodology/05-artifacts.md)

Extract every verifiable claim. Use the taxonomy. If the taxonomy is empty,
tag all claims UNCLASSIFIED and note this in log.md. Do not paraphrase the
sentence column — quote verbatim with quotes.
```
