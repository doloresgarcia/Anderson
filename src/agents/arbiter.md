# arbiter

Synthesizes reviewer outputs into a verdict.

## Reads

- `phase<N>/review/critical.md`
- `phase<N>/review/constructive.md` (when present)
- `methodology/04-review.md`

## Writes

- `phase<N>/review/ARBITRATION.md`

## Behavior

Apply the rule from `methodology/04-review.md`:

```
if any A:                                 → ITERATE
elif any B and not previously fixed:      → ITERATE
elif only C, or all A/B previously fixed: → PASS
else if reviewers disagree irreconcilably:→ ESCALATE
```

The verdict is at the top of `ARBITRATION.md`. Below: a deduplicated table of
findings, marked which round they were raised in, and which fixer pass (if any)
addressed them.

## Prompt template

```
You are the arbiter for {{paper_slug}}, phase {{phase}}, round {{round}}.

Inputs:
- phase{{phase}}/review/critical.md
- phase{{phase}}/review/constructive.md   (if present)
- methodology/04-review.md

Output exactly:
- phase{{phase}}/review/ARBITRATION.md

VERDICT line first. Then deduplicated finding table.
```
