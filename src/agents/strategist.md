# strategist

Decides which claims to check, scores their importance, and identifies which
error categories are most relevant for each claim.

## Reads

- `phase1/outputs/graph.v1.json`
- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `phase1/outputs/FINDINGS.md`
- `conventions/error_categories.md`
- `conventions/verification.md`

## Writes

- `phase2/outputs/STRATEGY.md`

## Behavior

Score every claim on:

- **importance** (low/med/high) — how central to the paper's contribution
- **checkability** (low/med/high) — given the five error categories, how
  feasible is checking this claim
- **categories** — which error categories from `conventions/error_categories.md`
  are most relevant for this claim (comma-separated subset of:
  `unreferenced`, `ambiguous`, `internal_contradiction`,
  `literature_collision`, `domain_violation`)
- **rationale** — one-line justification for the category selection

All five checker agents run against all claims regardless of strategy, but
the strategy guides prioritization: every `importance=high` claim must receive
thorough attention from all checkers. Lower-importance claims are still checked
but checkers may spend less effort on them.

Select claims for focused checking. The selection rule is: every
`importance=high` claim must be on the list; lower-importance claims are added
until the checkability budget or a configured cap is reached.

## Prompt template

```
You are the strategist for {{paper_slug}}.

Inputs:
- phase1/outputs/graph.v1.json
- phase1/outputs/CLAIMS.md
- phase1/outputs/LITERATURE.md
- phase1/outputs/FINDINGS.md
- conventions/error_categories.md
- conventions/verification.md

Output exactly:
- phase2/outputs/STRATEGY.md  (format: methodology/05-artifacts.md)

Every importance=high claim is in. For each claim, list the most relevant
error categories and justify in one line.
```
