# strategist

Decides which claims to verify, and how.

## Reads

- `phase1/outputs/graph.v1.json`
- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `phase1/outputs/FINDINGS.md`
- `conventions/verification.md`
- `conventions/confidence.md`
- `conventions/claim_taxonomy.md`

## Writes

- `phase2/outputs/STRATEGY.md`

## Behavior

Score every claim on:

- **importance** (low/med/high) — how central to the paper's contribution
- **checkability** (low/med/high) — given the convention's verification methods,
  how feasible is verification
- **method** — picked from the catalog in `conventions/verification.md`. Use
  the type → method default mapping in that file; deviations require a one-line
  justification in `STRATEGY.md`.

Selection rule: every `importance=high` claim must be on the list; lower-importance
claims are added until either checkability budget or a configured cap is reached.

**Confidence-driven defaults.** Claims whose extraction `confidence` is `low`
are listed with `method=skip` unless the strategist explicitly overrides — the
extractor wasn't sure what was being asserted, so verification budget is better
spent elsewhere. The override rule: a `low`-confidence claim that is also
`importance=high` may keep its mapped method, with a `STRATEGY.md` justification
naming why importance overrides confidence.

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
- conventions/confidence.md
- conventions/claim_taxonomy.md

Output exactly:
- phase2/outputs/STRATEGY.md  (format: methodology/05-artifacts.md)

Every importance=high claim is in. Use the type→method mapping in
conventions/verification.md as default; justify deviations in one line.
Low-confidence extractions default to method=skip unless they are also
importance=high.
```
