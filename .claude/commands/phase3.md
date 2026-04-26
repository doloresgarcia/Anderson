---
description: Run Phase 3 (highlights, final graph, report) in parallel, three-bot review, human gate, then final commit.
argument-hint: <slug>
arguments: [slug]
---

# /phase3 — Report

You are the orchestrator. The user invoked `/phase3 $0`.

`$0` is the review slug. If empty, tell the user `/phase3 <slug>` is required
and stop.

## 0. Preflight

1. Verify all required upstream deliverables exist and are non-empty:
   `reviews/$0/phase1/outputs/CLAIMS.md`,
   `reviews/$0/phase1/outputs/FINDINGS.md`,
   `reviews/$0/phase2/outputs/STRATEGY.md`,
   `reviews/$0/phase2/outputs/VERIFICATION.md`, and
   `reviews/$0/phase2/outputs/graph.v2.json`. If not, tell the user to run
   the missing prior phase first and stop.
2. Verify `reviews/$0/phase2/review/ARBITRATION.md` exists and its first line
   is `PASS`. If not, do not advance; surface the prior verdict and stop.
3. Verify `reviews/$0/paper/paper.txt` exists and is non-empty. For the
   highlighter, `reviews/$0/paper/paper.pdf` is preferred when present;
   otherwise text mode uses `paper.txt`.
4. Read methodology:
   - `src/methodology/03-phases.md` § Phase 3
   - `src/methodology/03a-orchestration.md` § Parallelism (Phase 3)
   - `src/methodology/04-review.md`

Loop: **EXECUTE → REVIEW → CHECK → HUMAN GATE → COMMIT**.

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
  - `reviews/$0/phase3/outputs/paper.highlighted.pdf` (PDF input; also text
    input when PyMuPDF is available)
  - `reviews/$0/phase3/outputs/paper.highlighted.html` (text-input mode)
- working dir: `reviews/$0/phase3/agents/highlighter/`

### 1b. graph_builder (final)

Dispatch `.claude/agents/graph_builder.md`:

- inputs:
  - `reviews/$0/phase2/outputs/graph.v2.json`
  - `src/conventions/graph_schema.json`
  - `src/conventions/graph_schema.md`
- behavior: copy `graph.v2.json` to `graph.final.json`, then invoke
  `python3 src/render_graph.py reviews/$0/phase3/outputs/graph.final.json`.
- outputs:
  - `reviews/$0/phase3/outputs/graph.final.json`
  - `reviews/$0/phase3/outputs/graph.final.html` from the renderer
- working dir: `reviews/$0/phase3/agents/graph_builder/`

### 1c. report_writer

Dispatch `.claude/agents/report_writer.md`:

- inputs:
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - `reviews/$0/phase1/outputs/FINDINGS.md`
  - `reviews/$0/paper/paper.meta.json`
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

- **PASS** → HUMAN GATE.
- **ITERATE** → dispatch `.claude/agents/fixer.md` with the A/B findings.
  Apply the dependency closure before re-review: highlighter findings require
  regenerated highlighted outputs; graph findings require `graph.final.json`
  and `graph.final.html`; report/stat findings require `STATS.md` and
  `REPORT.md`. Re-dispatch only the affected owning agent(s), then re-run both
  reviewers and the arbiter. At most one pre-gate iterate cycle; second
  ITERATE → escalate.
- **ESCALATE** → surface verbatim and stop (do **not** proceed to the human
  gate without a PASS).

## 4. HUMAN GATE

Print a summary to the user listing the expected outputs for the current input
mode and asking for explicit confirmation. Include only the highlighted output
bullet(s) that apply: PDF input expects `paper.highlighted.pdf`; text input
expects `paper.highlighted.html` and also `paper.highlighted.pdf` when PyMuPDF
is available. Do **not** commit yet, do **not** dispatch anything else, do
**not** modify files, and do **not** declare the run finished until the user
responds.

```
Phase 3 ready for human review for $0. Expected outputs:

  - reviews/$0/phase3/outputs/graph.final.json
  - reviews/$0/phase3/outputs/graph.final.html
  - reviews/$0/phase3/outputs/STATS.md
  - reviews/$0/phase3/outputs/REPORT.md
  - <applicable highlighted paper output(s) for this input mode>

Please review the highlighted paper, the rendered graph, the stats, and the
report. Reply with one of:

  - APPROVE     — accept the run as final and commit Phase 3.
  - ITERATE: <notes> — fix within phase-3 scope, re-run review, then return to this gate.
  - REGRESS N: <notes> — re-open phase N (1 or 2); no Phase 3 final commit.
```

Response handling:

- **APPROVE** → COMMIT.
- **ITERATE** → dispatch `fixer` with the human notes, regenerate the affected
  Phase 3 outputs through their owning path (highlighter, graph_builder, or
  report_writer / `claim_stats.py`), run REVIEW and CHECK again, then return to
  HUMAN GATE. Do not commit before the next APPROVE.
- **REGRESS N** → stop and tell the user to run `/phaseN $0` after addressing
  the notes. Do not make the final Phase 3 commit.

## 5. COMMIT

Only after human APPROVE:

```
git add reviews/$0/phase3/
git commit -m "phase3(report): highlights + final graph + report [$0]"
```

Then print:

> Phase 3 approved and committed for `$0`.
