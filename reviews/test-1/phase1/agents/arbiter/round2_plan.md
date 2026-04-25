# Arbiter round-2 plan — phase 1 (test-1)

## Goal

Synthesize a verdict for round-2 review of phase 1, given:
- 8 round-1 B findings (F01–F08) handled by a single fixer pass + a
  graph_builder rebuild, with F01 accepted as deferred to phase 3 in the
  round-1 ARBITRATION;
- 4 round-1 C findings (F09–F12) intentionally left for orchestrator
  discretion;
- a round-2 critical review introducing 0 A, 2 new B (G01, G02), 1 new C
  (G03), and substantiating each round-1 finding's resolution by an
  independent re-read of the post-fixer artifacts.

## Policy interaction (the central question)

Two methodology rules can produce opposite verdicts on a round-2 review:

- `methodology/04-review.md`:
  "elif any B and not previously fixed: → ITERATE"
  — strict reading: G01 and G02 are previously-unraised Bs, so ITERATE.

- `methodology/03a-orchestration.md`:
  "Category B → spawn fixer once, accept on re-review unless new A."
  — operative reading: a fixer has already run; no new A appeared, so
  PASS, with G01/G02/G03 carried forward as tracked items.

The dispatch from the orchestrator explicitly designates
`03a-orchestration.md` as the operative rule for the round-2 verdict.
Quote it verbatim in `ARBITRATION_round2.md` so the audit trail is
preserved and any future reviewer can see which rule was applied and
why. This is structurally identical to F01's round-1 deferral
(round-1 ARBITRATION accepted F01 as a tracked item rather than blocking
on it), so the precedent is in-corpus.

## Decision

Verdict: **PASS** (because round-2 introduces zero new Category-A
findings; a fixer pass has already executed; the orchestration policy
mandates accept-on-re-review unless new A).

Tracked items carried forward:

- **F01** — phase-3 deferral, already documented in `FINDINGS.md` §8.
- **G01** — stale FINDINGS.md post-fixer numbers/prose. Mechanical
  regen via `src/claim_stats.py` cheap; orchestrator may handle during
  phase-2 inheritance, or de-scope.
- **G02** — paraphrase looseness on C015 / C218 / C219 (F04 split).
  Phase-2 strategist must be alerted to treat the three rows as
  paraphrases rather than verbatim sub-propositions when scoring
  evidence.
- **G03** — free-form `Note:` lines in LITERATURE.md C006 / C148.
  Format silent in spec; pure C; de-scopable.

Open C items from round 1 (F09–F12) remain at orchestrator discretion;
none block PASS.

## Format requirements for ARBITRATION_round2.md

1. VERDICT line first (PASS, all caps).
2. Round number on next line.
3. Cite `03a-orchestration.md` rule verbatim, name the tension with
   `04-review.md`, explain why orchestration is operative.
4. Deduplicated finding table covering rounds 1 and 2: id, category,
   locus, one-line synopsis, source-review, round-raised,
   fixer-pass-that-addressed-it, current-status from
   {RESOLVED, DEFERRED-ACCEPTED, TRACKED-ACCEPTED, OPEN}.
5. Explicit tracked-but-accepted list: F01 (phase 3); G01 (FINDINGS.md
   regen); G02 (paraphrase awareness for phase-2 strategist);
   G03 (LITERATURE.md note format).
6. Next steps: instruct orchestrator to commit phase-1 deliverables
   and advance to phase 2.

## Outputs to write

- `phase1/review/ARBITRATION_round2.md` (the verdict)
- `phase1/agents/arbiter/round2_plan.md` (this file)
- `phase1/agents/arbiter/round2_log.md` (the run log)

No other writes.
