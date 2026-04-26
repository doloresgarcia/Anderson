---
description: Run Phase 2 (strategy, five parallel checkers, verification, graph v2) end-to-end with three-bot review and commit.
argument-hint: <slug>
arguments: [slug]
---

# /phase2 — Strategy & Check

You are the orchestrator. The user invoked `/phase2 $0`.

`$0` is the review slug. If empty, tell the user `/phase2 <slug>` is required
and stop.

## 0. Preflight

1. Verify all required Phase 1 deliverables exist:
   `reviews/$0/phase1/outputs/CLAIMS.md`,
   `reviews/$0/phase1/outputs/LITERATURE.md`,
   `reviews/$0/phase1/outputs/references.bib`,
   `reviews/$0/phase1/outputs/graph.v1.json`, and
   `reviews/$0/phase1/outputs/FINDINGS.md`. If not, tell the user to run
   `/phase1 $0` first and stop. `CLAIMS.md`, `LITERATURE.md`,
   `graph.v1.json`, and `FINDINGS.md` must be non-empty; `references.bib`
   may be empty only if `LITERATURE.md` contains no citation keys.
2. Verify `reviews/$0/phase1/review/ARBITRATION.md` exists and its first line
   is `PASS`. If not, do not advance; surface the prior verdict and stop.
3. Verify `reviews/$0/paper/paper.txt` still exists and is non-empty.
4. Skim `reviews/$0/phase1/outputs/FINDINGS.md` so you know the claim count
   and any gaps the strategist should be aware of.
5. Read methodology:
   - `src/methodology/03-phases.md` § Phase 2
   - `src/methodology/03a-orchestration.md` § Parallelism (Phase 2)
   - `src/methodology/04-review.md`
   - `src/conventions/error_categories.md`

Loop: **EXECUTE → REVIEW → CHECK → COMMIT**. Pause before ADVANCE.

## 1. EXECUTE

### 1a. strategist (sequential, first)

Dispatch `.claude/agents/strategist.md`:

- inputs:
  - `reviews/$0/phase1/outputs/graph.v1.json`
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - `reviews/$0/phase1/outputs/LITERATURE.md`
  - `reviews/$0/phase1/outputs/FINDINGS.md`
  - `src/conventions/error_categories.md`
- output: `reviews/$0/phase2/outputs/STRATEGY.md`
- working dir: `reviews/$0/phase2/agents/strategist/`

### 1b. Five checkers, in parallel

Dispatch all five checkers simultaneously (single message, five tool calls).
Each writes to its **own** working dir's `section.md` so writes are disjoint.

For each checker `<role>` ∈ {`checker_unreferenced`, `checker_ambiguous`,
`checker_contradiction`, `checker_literature`, `checker_domain`}:

- agent file: `.claude/agents/<role>.md`
- inputs (common):
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - `reviews/$0/phase1/outputs/LITERATURE.md`
  - `reviews/$0/phase1/outputs/references.bib`
  - `reviews/$0/phase1/outputs/graph.v1.json`
  - `reviews/$0/phase2/outputs/STRATEGY.md`
  - `reviews/$0/paper/paper.txt`
  - `reviews/$0/paper/paper.meta.json`
  - `src/conventions/error_categories.md`
  - `src/conventions/claim_taxonomy.md`
  - `src/conventions/confidence.md`
  - `src/methodology/05-artifacts.md`
  - `literature_bank/` (for `checker_literature` and `checker_domain`)
- output: `reviews/$0/phase2/agents/<role>/section.md`
- working dir: `reviews/$0/phase2/agents/<role>/`

Wait for all five to complete.

### 1c. Orchestrator-authored VERIFICATION.md (deterministic concat)

You (the orchestrator, **not** a subagent) write
`reviews/$0/phase2/outputs/VERIFICATION.md` by concatenating the five
checker sections in canonical section order. This is a deterministic merge
order, not a severity ranking; no LLM judgment is needed, and no subagent owns
this artifact:

```bash
cat reviews/$0/phase2/agents/checker_unreferenced/section.md \
    reviews/$0/phase2/agents/checker_ambiguous/section.md \
    reviews/$0/phase2/agents/checker_contradiction/section.md \
    reviews/$0/phase2/agents/checker_literature/section.md \
    reviews/$0/phase2/agents/checker_domain/section.md \
    > reviews/$0/phase2/outputs/VERIFICATION.md
```

If any section file is missing (a checker failed to write), stop and
re-dispatch that checker before continuing — VERIFICATION.md must
contain all five sections.

### 1d. graph_builder (sequential, after VERIFICATION.md exists)

Dispatch `.claude/agents/graph_builder.md` to merge the verdicts into
`graph.v2.json`:

- inputs:
  - `reviews/$0/phase1/outputs/graph.v1.json`
  - `reviews/$0/phase2/outputs/VERIFICATION.md` (already concatenated above)
  - `src/conventions/graph_schema.json`
  - `src/conventions/graph_schema.md`
  - `src/conventions/error_categories.md`
- output: `reviews/$0/phase2/outputs/graph.v2.json`
- working dir: `reviews/$0/phase2/agents/graph_builder/`

## 2. REVIEW (three-bot)

Dispatch `critical_reviewer` ‖ `constructive_reviewer` in parallel:

- `.claude/agents/critical_reviewer.md`:
  - inputs: everything in `reviews/$0/phase2/outputs/`,
    plus phase-1 outputs for cross-check,
    `reviews/$0/paper/paper.txt`, `src/conventions/`,
    `src/methodology/04-review.md`
  - output: `reviews/$0/phase2/review/critical.md`
- `.claude/agents/constructive_reviewer.md`:
  - same inputs
  - output: `reviews/$0/phase2/review/constructive.md`

Wait for both, then dispatch `.claude/agents/arbiter.md`:

- inputs:
  - `reviews/$0/phase2/review/critical.md`
  - `reviews/$0/phase2/review/constructive.md`
  - `src/methodology/04-review.md`
- output: `reviews/$0/phase2/review/ARBITRATION.md`

## 3. CHECK

Read `reviews/$0/phase2/review/ARBITRATION.md` (verdict on line 1).

- **PASS** → COMMIT.
- **ITERATE** → dispatch `.claude/agents/fixer.md` with the A/B findings.
  Apply the dependency closure before re-review: if `STRATEGY.md` changed,
  re-dispatch all five checkers; if any checker section changed or any checker
  was re-run, re-concatenate `VERIFICATION.md` in canonical section order and
  re-dispatch `graph_builder` for `graph.v2.json`. If the graph alone changed,
  re-dispatch `graph_builder` or validate the corrected `graph.v2.json` before
  review. Then re-dispatch both reviewers and the arbiter. At most **one**
  iterate cycle; second ITERATE → escalate to the user.
- **ESCALATE** → surface verbatim and stop.

## 4. COMMIT

```
git add reviews/$0/phase2/
git commit -m "phase2(check): five checkers + graph.v2 [$0]"
```

## 5. Pause

Print to the user:

> Phase 2 complete for `$0`. Outputs in `reviews/$0/phase2/outputs/`.
> Review verdict: <…>.
> Run `/phase3 $0` when ready.

Do **not** auto-run `/phase3`.
