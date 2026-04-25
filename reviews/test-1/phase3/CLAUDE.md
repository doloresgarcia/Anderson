# Phase 3 — Report (CLAUDE.md)

**Goal.** Produce the final, human-facing artifacts: final graph, highlighted
paper, and report.

## Required reading (orchestrator)

- `methodology/03-phases.md` — Phase 3 section
- `methodology/05-artifacts.md` — REPORT, highlighted-paper specs

## Execution order

1. **highlighter** ∥ **graph_builder (final)** ∥ **report_writer** — all three
   in parallel; they write to different files.
   - highlighter inputs: `paper/paper.pdf`, `paper/paper.txt`,
     `phase2/outputs/VERIFICATION.md`, `phase2/outputs/graph.v2.json`
   - highlighter outputs: `phase3/outputs/paper.highlighted.{pdf,html}`
   - graph_builder inputs: `phase2/outputs/graph.v2.json`
   - graph_builder outputs: `phase3/outputs/graph.final.json`,
     `phase3/outputs/graph.final.svg`
   - report_writer inputs: `paper/paper.meta.json`,
     `phase1/outputs/FINDINGS.md`, `phase2/outputs/{STRATEGY,VERIFICATION}.md`,
     `phase2/outputs/graph.v2.json`
   - report_writer output: `phase3/outputs/REPORT.md`

## Review

3-bot:
- `critical_reviewer` → `phase3/review/critical.md`
- `constructive_reviewer` → `phase3/review/constructive.md`
- `arbiter` → `phase3/review/ARBITRATION.md`

Phase-3 specific Category-A triggers (in addition to the global ones):

- A highlight in `paper.highlighted.pdf` whose claim_id has no entry in
  `VERIFICATION.md`, or whose color disagrees with the `VERIFICATION.md` verdict.
- A node in `graph.final.json` lacking the verdict layer when `graph.v2.json`
  had it.
- `REPORT.md` introducing a verdict that is not in `VERIFICATION.md`.

## Check

- `PASS` → commit, present to human.
- `ITERATE` → fixer + re-review.
- `ESCALATE` → surface.

## Commit

```
git commit -m "phase3(report): final graph, highlighted paper, REPORT"
```

## Human gate

Present `paper.highlighted.pdf` plus `REPORT.md` to the user. Possible
responses:

- **APPROVE** — done.
- **ITERATE** — fix in phase-3 scope, re-review, re-present.
- **REGRESS(N)** — re-open phase N. Spawn the relevant phase agents again
  starting from N, propagate downstream.

## Phase-3 specific gotchas

- If most claims in `VERIFICATION.md` are `INCONCLUSIVE` because the verification
  conventions are the placeholder, the highlighted PDF will be mostly yellow
  and `REPORT.md` will say "not checked" a lot. That is the intended degraded
  output, not a phase-3 bug. Tell the user; do not paper over it.
