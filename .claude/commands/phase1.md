---
description: Run Phase 1 (ingest, claim extraction, literature search, graph v1) end-to-end with review and commit.
argument-hint: <slug>
arguments: [slug]
---

# /phase1 — Ingest & Map

You are the orchestrator. The user invoked `/phase1 $0`.

`$0` is the review slug. If empty, tell the user `/phase1 <slug>` is required
and stop.

## 0. Preflight

1. Verify `reviews/$0/` exists. If not, tell the user to run
   `/scaffold $0 <source>` first and stop.
2. Verify `reviews/$0/paper/paper.txt` exists and is non-empty. If not, the
   review was scaffolded from `--arxiv` / `--doi` / `--url` (which only
   record the identifier in `paper.meta.json` and do not fetch). Stop and
   tell the user to either supply the paper text manually or re-run
   `/scaffold $0 <local.pdf|local.txt>`.
3. Read `reviews/$0/CLAUDE.md` for paper meta.
4. Read `reviews/$0/prompt.md`. If it is empty or absent, write the user's
   exact `/phase1 $0` invocation (and any surrounding free-text from the
   user's message) into it as the first action — this is the orchestrator's
   prompt-of-record for the run.
5. Read the relevant methodology so the dispatch is faithful to spec:
   - `src/methodology/03-phases.md` § Phase 1
   - `src/methodology/03a-orchestration.md` § Parallelism (Phase 1)
   - `src/methodology/04-review.md`

Loop: **EXECUTE → REVIEW → CHECK → COMMIT**. Pause before ADVANCE; the user
runs `/phase2 $0` to advance.

## 1. EXECUTE

Dispatch subagents flat from this main session per their registered
frontmatters in `.claude/agents/`. Do not rewrite their prompts; pass inputs,
output paths, and the methodology/convention pointers.

### 1a. claim_extractor (sequential, first)

Dispatch `.claude/agents/claim_extractor.md` with:

- inputs:
  - `reviews/$0/paper/paper.txt`
  - `reviews/$0/paper/paper.meta.json`
  - `src/conventions/claim_taxonomy.md`
  - `src/methodology/05-artifacts.md`
- output:
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - working dir: `reviews/$0/phase1/agents/claim_extractor/` (`plan.md`, `log.md`)

Wait for completion. If `CLAIMS.md` is missing, stop and surface the failure.

### 1b. literature_searcher ‖ graph_builder (skeleton) — in parallel

In a single message, dispatch both subagents simultaneously:

- `.claude/agents/literature_searcher.md`:
  - inputs: `reviews/$0/phase1/outputs/CLAIMS.md`,
    `reviews/$0/paper/paper.txt`, `literature_bank/`,
    `src/conventions/claim_taxonomy.md`
  - output: `reviews/$0/phase1/outputs/LITERATURE.md` and
    `reviews/$0/phase1/outputs/references.bib`
  - working dir: `reviews/$0/phase1/agents/literature_searcher/`
- `.claude/agents/graph_builder.md` (skeleton pass — claims only, no
  literature edges yet):
  - inputs: `reviews/$0/phase1/outputs/CLAIMS.md`,
    `src/conventions/graph_schema.json`,
    `src/conventions/claim_taxonomy.md`
  - output: `reviews/$0/phase1/outputs/graph.v1.skeleton.json`
  - working dir: `reviews/$0/phase1/agents/graph_builder_skeleton/`

Wait for both. Their outputs are disjoint, so parallel writes are safe.

### 1c. graph_builder (final pass, sequential)

Dispatch `.claude/agents/graph_builder.md` again to merge literature into the
skeleton:

- inputs:
  - `reviews/$0/phase1/outputs/graph.v1.skeleton.json`
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - `reviews/$0/phase1/outputs/LITERATURE.md`
  - `reviews/$0/phase1/outputs/references.bib`
  - `src/conventions/graph_schema.json`
- output: `reviews/$0/phase1/outputs/graph.v1.json`
- working dir: `reviews/$0/phase1/agents/graph_builder/`

### 1d. Orchestrator-authored FINDINGS.md

You (the orchestrator, **not** a subagent) write
`reviews/$0/phase1/outputs/FINDINGS.md` with:

- claim counts (total, plus distribution by taxonomy type — count
  `UNCLASSIFIED` separately)
- literature coverage (claims with ≥1 candidate vs. uncovered)
- gaps you noticed (e.g. taxonomy placeholder still in effect, empty
  literature bank, claims without provenance)
- pointers to the four output files

Keep it short — one screen.

## 2. REVIEW (single-bot for phase 1)

Dispatch `.claude/agents/critical_reviewer.md`:

- inputs: every file in `reviews/$0/phase1/outputs/`,
  `reviews/$0/paper/paper.txt`, `src/conventions/`,
  `src/methodology/04-review.md`
- output: `reviews/$0/phase1/review/critical.md`

Wait for completion, then dispatch `.claude/agents/arbiter.md` (single-bot
mode — only `critical.md` is present):

- inputs: `reviews/$0/phase1/review/critical.md`,
  `src/methodology/04-review.md`
- output: `reviews/$0/phase1/review/ARBITRATION.md`

## 3. CHECK

Read `reviews/$0/phase1/review/ARBITRATION.md`. The verdict is on the first
line.

- **PASS** → proceed to COMMIT.
- **ITERATE** → dispatch `.claude/agents/fixer.md` with the listed Category A
  and B findings as the prompt, the relevant phase-1 outputs as inputs, and
  the same output paths the original agents used. After fixer completes,
  re-dispatch `critical_reviewer` and then `arbiter`. Iterate at most **once**;
  if the second arbiter verdict is still ITERATE, escalate to the user.
- **ESCALATE** → surface the arbiter's reasoning to the user verbatim and
  stop.

## 4. COMMIT

Once the arbiter verdict is PASS:

```
git add reviews/$0/phase1/
git commit -m "phase1(ingest): extract claims, lit search, build graph.v1 [$0]"
```

## 5. Pause (no auto-advance)

Print to the user:

> Phase 1 complete for `$0`. Outputs in `reviews/$0/phase1/outputs/`.
> Review verdict: <PASS / iterated → PASS / escalated>.
> Run `/phase2 $0` when you are ready to proceed.

Do **not** automatically run `/phase2`.
