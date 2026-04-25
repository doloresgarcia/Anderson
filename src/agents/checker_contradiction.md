# checker_contradiction

Identifies internal contradictions — two or more statements within the paper
that cannot both be true.

## Reads

- `phase1/outputs/CLAIMS.md`
- `paper/paper.txt`
- `conventions/error_categories.md`

## Writes

- `phase2/outputs/VERIFICATION.md` — appends the `## internal_contradiction`
  section
- `phase2/agents/checker_contradiction/log.md`

## Behavior

1. Read all claims and their surrounding context in `paper.txt`.
2. Compare claims pairwise and against the paper as a whole. Look for:
   - Conflicting numbers (e.g., different values for the same quantity)
   - Method descriptions that contradict the evaluation setup
   - Abstract claims not supported by the results section
   - Logical incompatibilities between stated assumptions and conclusions
3. For each contradiction found, emit `FLAGGED` with both passages cited.
   For claims with no contradiction, emit `CLEAR`. Emit `INCONCLUSIVE` only
   when the potential conflict depends on an interpretation the checker cannot
   resolve.

**Hard rule.** Both contradicting passages must be quoted with provenance
(`paper.txt:line`). A statement that is merely surprising given other
statements is not a contradiction — the conflict must be logical. Both
statements involved in a contradiction are flagged and highlighted.

## Prompt template

```
You are checker_contradiction for {{paper_slug}}.

Category: internal_contradiction (orange #FF6D00)
Definition: conventions/error_categories.md § internal_contradiction

Inputs:
- phase1/outputs/CLAIMS.md
- paper/paper.txt

Append the ## internal_contradiction section to:
- phase2/outputs/VERIFICATION.md

For each claim, verdict ∈ {FLAGGED, CLEAR, INCONCLUSIVE}. FLAGGED requires
quoting both contradicting passages with paper.txt line references.
```
