---
description: Run Phase 3 (highlights, final graph, report) in parallel, three-bot review, commit, then human gate.
argument-hint: <slug>
arguments: [slug]
---

# /phase3 — Report

You are the orchestrator. The user invoked `/phase3 $0`.

`$0` is the review slug. If empty, tell the user `/phase3 <slug>` is required
and stop.

## 0. Preflight

1. Verify `reviews/$0/phase2/outputs/graph.v2.json` and
   `reviews/$0/phase2/outputs/VERIFICATION.md` exist. If not, tell the user
   to run `/phase2 $0` first and stop.
2. Read methodology:
   - `src/methodology/03-phases.md` § Phase 3
   - `src/methodology/03a-orchestration.md` § Parallelism (Phase 3)
   - `src/methodology/04-review.md`

Loop: **EXECUTE → REVIEW → CHECK → COMMIT → HUMAN GATE**.

## 1. EXECUTE — three subagents in parallel

Dispatch all three in a single message. Their outputs are disjoint files.

### 1a. highlighter

Dispatch `.claude/agents/highlighter.md`:

- inputs:
  - `reviews/$0/phase2/outputs/graph.v2.json`
  - `reviews/$0/phase2/outputs/VERIFICATION.md`
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - `reviews/$0/paper/paper.pdf` (if present) or `reviews/$0/paper/paper.txt`
  - `src/conventions/error_categories.md`
- behavior: if `paper.pdf` is present, invoke
  `python3 src/highlight_paper.py reviews/$0` (writes PDF only). If no PDF,
  invoke `python3 src/highlight_text.py reviews/$0` (writes both HTML and,
  if PyMuPDF is installed, a synthesized PDF).
- outputs:
  - `reviews/$0/phase3/outputs/paper.highlighted.pdf` (always, if highlighter ran without error)
  - `reviews/$0/phase3/outputs/paper.highlighted.html` (text-input mode only)
- working dir: `reviews/$0/phase3/agents/highlighter/`

### 1b. graph_builder (final)

Dispatch `.claude/agents/graph_builder.md`:

- inputs:
  - `reviews/$0/phase2/outputs/graph.v2.json`
  - `src/conventions/graph_schema.json`
- behavior: copy `graph.v2.json` to `graph.final.json`, then invoke
  `python3 src/render_graph.py reviews/$0/phase3/outputs/graph.final.json`.
- outputs:
  - `reviews/$0/phase3/outputs/graph.final.json`
  - `reviews/$0/phase3/outputs/graph.final.html` (and/or `.svg`) from the
    renderer
- working dir: `reviews/$0/phase3/agents/graph_builder/`

### 1c. report_writer

Dispatch `.claude/agents/report_writer.md`:

- inputs:
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - `reviews/$0/phase1/outputs/FINDINGS.md`
  - `reviews/$0/phase2/outputs/STRATEGY.md`
  - `reviews/$0/phase2/outputs/VERIFICATION.md`
  - `reviews/$0/phase2/outputs/graph.v2.json`
  - `src/conventions/error_categories.md`
- behavior: invoke `python3 src/claim_stats.py reviews/$0` to refresh
  `STATS.md`, then write the report.
- outputs:
  - `reviews/$0/phase3/outputs/STATS.md`
  - `reviews/$0/phase3/outputs/REPORT.md`
- working dir: `reviews/$0/phase3/agents/report_writer/`

Wait for all three to complete.

## 2. REVIEW (three-bot)

Dispatch `critical_reviewer` ‖ `constructive_reviewer` in parallel:

- `.claude/agents/critical_reviewer.md`:
  - inputs: everything in `reviews/$0/phase3/outputs/`,
    plus `reviews/$0/phase2/outputs/VERIFICATION.md`,
    `reviews/$0/phase2/outputs/graph.v2.json`,
    `reviews/$0/paper/paper.txt`,
    `src/conventions/`, `src/methodology/04-review.md`
  - output: `reviews/$0/phase3/review/critical.md`
- `.claude/agents/constructive_reviewer.md`:
  - same inputs
  - output: `reviews/$0/phase3/review/constructive.md`

Then dispatch `.claude/agents/arbiter.md`:

- inputs: both reviews, `src/methodology/04-review.md`
- output: `reviews/$0/phase3/review/ARBITRATION.md`

## 3. CHECK

Read `reviews/$0/phase3/review/ARBITRATION.md`.

- **PASS** → COMMIT.
- **ITERATE** → dispatch `.claude/agents/fixer.md` with the A/B findings.
  Re-dispatch only the affected agent(s) (e.g. just `report_writer` if the
  finding is in `REPORT.md`), then re-run both reviewers and the arbiter. At
  most one iterate cycle; second ITERATE → escalate.
- **ESCALATE** → surface verbatim and stop (do **not** proceed to the human
  gate without a PASS).

## 4. COMMIT

```
git add reviews/$0/phase3/
git commit -m "phase3(report): highlights + final graph + report [$0]"
```

## 5. HUMAN GATE

Print a summary to the user listing the four expected outputs and asking
for explicit confirmation. Do **not** dispatch anything else, do **not**
modify files, and do **not** declare the run finished until the user
responds.

```
Phase 3 complete for $0. Expected outputs:

  - reviews/$0/phase3/outputs/paper.highlighted.pdf
  - reviews/$0/phase3/outputs/graph.final.html
  - reviews/$0/phase3/outputs/STATS.md
  - reviews/$0/phase3/outputs/REPORT.md

Please review the highlighted PDF, the rendered graph, the stats, and the
report. Reply with one of:

  - APPROVE     — accept the run as final.
  - ITERATE: <notes> — fix within phase-3 scope and re-run review.
  - REGRESS N: <notes> — re-open phase N (1 or 2).
```

Stop and wait for the user's response. Do nothing further until then.
