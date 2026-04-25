# Phase 2 — Strategy & Verify (CLAUDE.md)

**Goal.** Decide which claims to verify, verify them, update the graph.

## Required reading (orchestrator)

- `methodology/03-phases.md` — Phase 2 section
- `methodology/05-artifacts.md` — `STRATEGY.md`, `VERIFICATION.md`, `graph.v2.json`
- `conventions/verification.md`
- `conventions/graph_schema.md`

## Execution order

1. **strategist** — sequential, first.
   - Inputs: `phase1/outputs/{graph.v1.json, CLAIMS.md, LITERATURE.md, FINDINGS.md}`,
     `conventions/verification.md`
   - Output: `phase2/outputs/STRATEGY.md`
2. **verifier × N** — parallel, one subagent per claim (or batch) on the
   strategist's selection list.
   - Inputs: `phase2/outputs/STRATEGY.md` (their row),
     `phase1/outputs/LITERATURE.md`, `phase1/outputs/references.bib`,
     `conventions/verification.md`, `paper/paper.txt`
   - Output: appended section in `phase2/outputs/VERIFICATION.md`
   - Use one subdirectory per claim: `phase2/agents/verifier/<claim_id>/`
3. **graph_builder** — sequential, after all verifiers finish.
   - Inputs: `phase1/outputs/graph.v1.json`, `phase2/outputs/VERIFICATION.md`
   - Output: `phase2/outputs/graph.v2.json`

## Review

3-bot:
- `critical_reviewer` → `phase2/review/critical.md`
- `constructive_reviewer` → `phase2/review/constructive.md`
- `arbiter` → `phase2/review/ARBITRATION.md`

## Check

- `PASS` → commit, advance.
- `ITERATE` → fixer + re-review. Common phase-2 fixes:
  - A `FAIL` verdict without concrete contradicting evidence → demote to
    `INCONCLUSIVE` or supply the evidence.
  - Strategist skipped an `importance=high` claim → add to selection, re-run
    that verifier.
- `ESCALATE` → surface.

## Commit

```
git commit -m "phase2(verify): strategy, verification verdicts, graph.v2"
```

## Advance

Hand off to `phase3/CLAUDE.md`.

## Phase-2 specific gotchas

- If `conventions/verification.md` is the placeholder, every method is `TBD`
  and every verdict is `INCONCLUSIVE`. Phase 3 will still run, but the report
  will say "not checked" for almost everything. Surface this prominently.
- Verifier subagents are independent; do not let them write to the same file
  simultaneously. Each writes its own section first under
  `phase2/agents/verifier/<claim_id>/section.md`; a final concat step assembles
  `VERIFICATION.md`.
- Concurrency cap: keep parallel verifiers ≤ N (configured by user, default 4).
  Going wider regularly trips rate limits.
