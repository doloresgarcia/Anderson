# Review protocol

## Reviewer roles

- **`critical_reviewer`** — looks for correctness and completeness gaps. Has access
  to the paper, all phase artifacts, and the convention files. Produces a list of
  findings.
- **`constructive_reviewer`** — looks for clarity, missing checks, and presentation
  issues that weaken the report.
- **`arbiter`** — reads both reviews, synthesizes a verdict (PASS / ITERATE /
  ESCALATE), and writes `phase<N>/review/ARBITRATION.md`.

Phase 1 uses a single reviewer + arbiter (single-bot mode). Phase 2 uses both
reviewers + arbiter. Phase 3 uses both reviewers + arbiter, then a human gate.

## Finding classification

Reviewers tag every finding with one of:

- **A — Blocking.** Must resolve before the phase can advance. Examples: claim list
  missing claims that are demonstrably in the paper; graph fails schema validation;
  a verification verdict cites a reference that does not resolve.
- **B — Weakening.** Must fix before PASS but does not block advancement on its own.
  Examples: a claim was extracted but mistyped; a verification's supporting evidence
  is thin; the strategy ranking is poorly justified.
- **C — Suggestion.** Style or polish. Recorded; not blocking.

## Arbiter logic

```
if any A:                                 → ITERATE (spawn fixer, re-review)
elif any B and not previously fixed:      → ITERATE (spawn fixer, re-review)
elif only C, or all A/B previously fixed: → PASS
else if reviewers disagree irreconcilably:→ ESCALATE (human)
```

## Hard rule: unresolvable references

If `LITERATURE.md` or `VERIFICATION.md` cites a paper that the reviewer cannot
resolve to a real record (DOI, arXiv ID, conference paper retrievable via the
configured search backend), that is automatically Category A. LLM-fabricated
citations are the most common failure mode of this kind of system; the reviewers
exist primarily to catch them.

## Hard rule: checker evidence standards

If a checker emits `FLAGGED` without meeting the evidence standard defined in
`conventions/error_categories.md` for that category, that is automatically
Category A. The fixer must either supply the required evidence or demote the
verdict to `INCONCLUSIVE`.
