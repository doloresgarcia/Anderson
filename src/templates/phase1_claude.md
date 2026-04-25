# Phase 1 — Ingest & Map (CLAUDE.md)

**Goal.** Read the paper, extract its claims, run literature search, emit
`graph.v1.json` and a summary `FINDINGS.md`.

## Required reading (orchestrator)

- `methodology/03-phases.md` — Phase 1 section
- `methodology/05-artifacts.md` — formats of `claims.jsonl`, `LITERATURE.md`,
  `graph.v*.json`
- `src/claims_schema.md` — JSONL schema for the canonical claim list
- `conventions/graph_schema.md`

## Execution order

1. **claim_extractor** — sequential, runs first. Mechanical wrapper around
   `src/extract_claims.py`.
   - Inputs: `paper/paper.tex`
   - Output: `phase1/outputs/claims.jsonl`
2. **claim_reviewer** — sequential, after extractor. Cautious quality pass over
   the JSONL: drops unambiguous junk rows, flags suspected issues, defaults to
   leaving rows alone.
   - Inputs: `phase1/outputs/claims.jsonl`, `paper/paper.tex`
   - Outputs: `phase1/outputs/claims.jsonl` (modified in place),
     `phase1/outputs/CLAIM_REVIEW.md`
3. **literature_searcher** ∥ **graph_builder (skeleton)** — parallel.
   - literature_searcher inputs: `phase1/outputs/claims.jsonl`,
     `paper/paper.meta.json`
   - literature_searcher outputs: `phase1/outputs/LITERATURE.md`,
     `phase1/outputs/references.bib`
   - graph_builder skeleton inputs: `phase1/outputs/claims.jsonl`,
     `conventions/graph_schema.md`
   - graph_builder skeleton output: `phase1/outputs/graph.v1.skeleton.json`
4. **graph_builder (final phase-1 pass)** — sequential, after both above finish.
   - Merges literature into the skeleton.
   - Output: `phase1/outputs/graph.v1.json`
5. **executor (FINDINGS scribe)** — sequential, last.
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

- `claim_extractor` is deterministic — the same `paper.tex` always produces
  the same `claims.jsonl`. If the script's output looks broken, fix the script
  (`src/extract_claims.py`), don't paper over it in the agent layer.
- `claim_reviewer`'s default action is "leave alone." It only edits
  `claims.jsonl` for unambiguous junk; everything else gets flagged in
  `CLAIM_REVIEW.md`. Reviewer over-edits are recoverable (we commit after every
  step), reviewer overreach is not.
- `references.bib` must contain every key that appears in `LITERATURE.md`.
  Mismatches are auto-Category-A.
