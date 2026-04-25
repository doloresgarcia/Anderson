# Phase 1 — Ingest & Map (CLAUDE.md)

**Goal.** Read the paper, extract its claims, run literature search, emit
`graph.v1.json` and a summary `FINDINGS.md`.

## Required reading (orchestrator)

- `methodology/03-phases.md` — Phase 1 section
- `methodology/05-artifacts.md` — formats of `CLAIMS.md`, `LITERATURE.md`,
  `graph.v*.json`
- `conventions/claim_taxonomy.md`
- `conventions/graph_schema.md`

## Execution order

1. **claim_extractor** — sequential, runs first.
   - Inputs: `paper/paper.txt`, `paper/paper.meta.json`, `conventions/claim_taxonomy.md`
   - Output: `phase1/outputs/CLAIMS.md`
2. **literature_searcher** ∥ **graph_builder (skeleton)** — parallel.
   - literature_searcher inputs: `phase1/outputs/CLAIMS.md`,
     `paper/paper.meta.json`, `literature_bank/`
   - literature_searcher outputs: `phase1/outputs/LITERATURE.md`,
     `phase1/outputs/references.bib`
   - graph_builder skeleton inputs: `phase1/outputs/CLAIMS.md`,
     `conventions/graph_schema.md`
   - graph_builder skeleton output: `phase1/outputs/graph.v1.skeleton.json`
3. **graph_builder (final phase-1 pass)** — sequential, after both above finish.
   - Merges literature into the skeleton.
   - Output: `phase1/outputs/graph.v1.json`
4. **executor (FINDINGS scribe)** — sequential, last.
   - Output: `phase1/outputs/FINDINGS.md` — counts, type distribution, gaps.

## Review

1 round, single-bot:
- `critical_reviewer` → `phase1/review/critical.md`
- `arbiter` → `phase1/review/ARBITRATION.md`

## Check

- ARBITRATION verdict `PASS` → commit and advance.
- `ITERATE` → spawn `fixer` with the listed findings, re-review.
- `ESCALATE` → surface to user.

## Commit

```
git commit -m "phase1(ingest): extract claims, lit search, build graph.v1"
```

## Advance

Hand off to `phase2/CLAUDE.md`.

## Phase-1 specific gotchas

- If `conventions/claim_taxonomy.md` is the placeholder, every claim will be
  `UNCLASSIFIED`. The `critical_reviewer` will raise that as Category B; that is
  expected. Surface the gap in the dispatch summary, do not block on it.
- `references.bib` must contain every key that appears in `LITERATURE.md`.
  Mismatches are auto-Category-A.
- The `literature_bank/` symlink is expected (scaffold_review.py creates it
  automatically). The literature searcher always searches the bank before any
  external call. If the bank is missing, empty, or unreadable, the searcher
  logs this and falls back to external search — this is not a phase failure.
