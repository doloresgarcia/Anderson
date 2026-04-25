# strategist

Decides which claims to verify, and how.

## Reads

- `phase1/outputs/graph.v1.json`
- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `phase1/outputs/FINDINGS.md`
- `conventions/verification.md`

## Writes

- `phase2/outputs/STRATEGY.md`

## Behavior

Score every claim on:

- **importance** (low/med/high) — how central to the paper's contribution
- **checkability** (low/med/high) — given the convention's verification methods,
  how feasible is verification
- **method** — which method from `conventions/verification.md` applies

Select claims to verify. The selection rule is: every `importance=high` claim must
be on the list; lower-importance claims are added until either checkability budget
or a configured cap is reached.

If `conventions/verification.md` is the placeholder, the strategist still emits a
ranked list but marks every method as `TBD` and logs the gap.

## Prompt template

```
You are the strategist for {{paper_slug}}.

Inputs:
- phase1/outputs/graph.v1.json
- phase1/outputs/CLAIMS.md
- phase1/outputs/LITERATURE.md
- phase1/outputs/FINDINGS.md
- conventions/verification.md

Output exactly:
- phase2/outputs/STRATEGY.md  (format: methodology/05-artifacts.md)

Every importance=high claim is in. Justify each method choice in one line.
If the verification conventions are unspecified, mark methods as TBD and note it.
```
