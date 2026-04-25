# Phase 2 — Strategy & Check (CLAUDE.md)

**Goal.** Decide which claims to check, run five specialized checker agents,
update the graph.

## Required reading (orchestrator)

- `methodology/03-phases.md` — Phase 2 section
- `methodology/05-artifacts.md` — `STRATEGY.md`, `VERIFICATION.md`, `graph.v2.json`
- `conventions/error_categories.md`
- `conventions/verification.md`
- `conventions/graph_schema.md`

## Execution order

1. **strategist** — sequential, first.
   - Inputs: `phase1/outputs/{graph.v1.json, CLAIMS.md, LITERATURE.md, FINDINGS.md}`,
     `conventions/error_categories.md`, `conventions/verification.md`
   - Output: `phase2/outputs/STRATEGY.md`
2. **Five checker agents** — all five run in parallel. Each checks all claims
   for its error category and writes its own section of `VERIFICATION.md`.
   - **checker_unreferenced**
     - Inputs: `phase1/outputs/CLAIMS.md`, `paper/paper.txt`,
       `conventions/error_categories.md`
     - Output: `## unreferenced` section in `phase2/outputs/VERIFICATION.md`
     - Workdir: `phase2/agents/checker_unreferenced/`
   - **checker_ambiguous**
     - Inputs: `phase1/outputs/CLAIMS.md`, `paper/paper.txt`,
       `conventions/error_categories.md`
     - Output: `## ambiguous` section in `phase2/outputs/VERIFICATION.md`
     - Workdir: `phase2/agents/checker_ambiguous/`
   - **checker_contradiction**
     - Inputs: `phase1/outputs/CLAIMS.md`, `paper/paper.txt`,
       `conventions/error_categories.md`
     - Output: `## internal_contradiction` section in `phase2/outputs/VERIFICATION.md`
     - Workdir: `phase2/agents/checker_contradiction/`
   - **checker_literature**
     - Inputs: `phase1/outputs/CLAIMS.md`, `phase1/outputs/LITERATURE.md`,
       `phase1/outputs/references.bib`, `literature_bank/`, `paper/paper.txt`,
       `conventions/error_categories.md`
     - Output: `## literature_collision` section in `phase2/outputs/VERIFICATION.md`
     - Workdir: `phase2/agents/checker_literature/`
   - **checker_domain**
     - Inputs: `phase1/outputs/CLAIMS.md`, `paper/paper.txt`,
       `paper/paper.meta.json`, `conventions/error_categories.md`
     - Output: `## domain_violation` section in `phase2/outputs/VERIFICATION.md`
     - Workdir: `phase2/agents/checker_domain/`
3. **Concat step** — sequential, after all checkers finish. Assemble the five
   section files into the final `phase2/outputs/VERIFICATION.md`.
4. **graph_builder** — sequential, after concat.
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
  - A `FLAGGED` verdict without the evidence required by
    `conventions/error_categories.md` → demote to `INCONCLUSIVE` or supply
    the evidence.
  - Strategist skipped an `importance=high` claim → re-run checkers for it.
  - A checker used the wrong category → reassign the finding.
- `ESCALATE` → surface.

## Commit

```
git commit -m "phase2(check): strategy, checker verdicts, graph.v2"
```

## Advance

Hand off to `phase3/CLAUDE.md`.

## Phase-2 specific gotchas

- Checker agents are independent; do not let them write to the same file
  simultaneously. Each writes its section first under
  `phase2/agents/<checker_name>/section.md`; the concat step assembles
  `VERIFICATION.md` in category severity order: `unreferenced`, `ambiguous`,
  `internal_contradiction`, `literature_collision`, `domain_violation`.
- All five checkers always run. If a checker finds nothing to flag for any
  claim, its section still appears in `VERIFICATION.md` with all `CLEAR`
  entries.
- Concurrency: all five checkers run in parallel (one agent per category, not
  per claim). This keeps the total agent count at 5 regardless of claim count.
