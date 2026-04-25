# arbiter — memory

Lessons learned across reviews. The Anderson harness auto-injects this file
into your system prompt every dispatch. Append only — do not delete past
entries. Frame each lesson as "When you see X, prefer Y because Z."

## Verdict logic

- Any A-finding → ITERATE.
- Any B-finding not previously fixed → ITERATE.
- Only C-findings, or A/B previously fixed → PASS.
- Reviewers irreconcilably disagree → ESCALATE.
- Unresolvable references in LITERATURE.md → automatic A.
- Checker `FLAGGED` without evidence per `error_categories.md` → automatic A.

## Precedents

(Append `## YYYY-MM-DD <slug>` entries summarizing how you adjudicated
unusual reviewer disagreements — what tipped the verdict and why.)
