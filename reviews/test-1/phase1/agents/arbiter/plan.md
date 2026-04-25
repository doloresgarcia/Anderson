# arbiter — plan (phase 1, round 1)

## Mode

Single-bot review (phase 1 protocol per `methodology/04-review.md`):
`critical_reviewer` only — no constructive_reviewer for this round.

## Inputs

- `phase1/review/critical.md` (sole reviewer input this round)
- `methodology/04-review.md` (verdict logic)
- `agents/arbiter.md` (role spec)

## Outputs

- `phase1/review/ARBITRATION.md`
- `phase1/agents/arbiter/plan.md` (this file)
- `phase1/agents/arbiter/log.md`

## Procedure

1. Re-read role spec (`agents/arbiter.md`) and verdict logic
   (`methodology/04-review.md`).
2. Read `phase1/review/critical.md` and tabulate findings by category (A / B
   / C).
3. Apply the verdict rule literally:
   - any A → ITERATE
   - else any B (not previously fixed) → ITERATE
   - else only C, or all A/B previously fixed → PASS
   - else reviewers irreconcilable → ESCALATE
4. Round 1 ⇒ no findings have been "previously fixed" yet, so a single B
   forces ITERATE.
5. Deduplicate findings across reviewer outputs. (Single reviewer this round
   ⇒ deduplication is trivial; preserve reviewer ids verbatim.)
6. Mark which findings the orchestrator should hand to the fixer vs. which
   are plausibly out-of-scope-for-phase-1 and should be tracked-but-deferred.
   The reviewer themselves explicitly flagged F01 as resolvable in phase 3
   ("remains B but must be fixed before phase 3"); call that out.
7. Write `ARBITRATION.md` with VERDICT line first.

## Expected verdict (pre-decision)

Critical review reports zero A, eight B (F01–F08), four C (F09–F12).
Therefore expected verdict: **ITERATE**, with eight B findings forwarded
(one of which — F01 — is flagged as deferrable to phase 3).

## What is not in scope for the arbiter

- Re-running auto-A trigger checks (bibtex resolution, graph schema, etc.) —
  the reviewer already executed these. Arbiter trusts the reviewer's report.
- Re-classifying findings (only the reviewers tag A/B/C; arbiter only
  applies the threshold rule).
- Issuing fix instructions — that is the fixer's role; arbiter only forwards
  the finding list.
