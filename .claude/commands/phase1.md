---
description: Run Phase 1 (ingest, claim extraction, literature search, graph v1) end-to-end with review and commit.
argument-hint: <slug> [--large]
arguments: [slug, mode]
---

# /phase1 — Ingest & Map

You are the orchestrator. The user invoked `/phase1 $0 $1`.

`$0` is the review slug. If empty, tell the user `/phase1 <slug>` is required
and stop.

`$1` is optional. If empty, run ordinary Phase 1. If it is `--large`, run the
large-paper orchestration path below. If `$1` is anything else, tell the user the
valid invocations are `/phase1 <slug>` and `/phase1 <slug> --large`, then stop.

## 0. Preflight

1. Verify `reviews/$0/` exists. If not, tell the user to run
   `/scaffold $0 <source>` first and stop.
2. Verify the scaffold control files and directories exist:
   `reviews/$0/CLAUDE.md`, `reviews/$0/prompt.md`,
   `reviews/$0/paper/paper.meta.json`, and
   `reviews/$0/phase1/{outputs,agents,review,logs}/`. If any are missing, tell
   the user the scaffold is incomplete and stop.
3. Verify `reviews/$0/paper/paper.txt` exists and is non-empty. If not, the
   review was scaffolded from `--arxiv` / `--doi` / `--url` (which only
   record the identifier in `paper.meta.json` and do not fetch). Stop and
   tell the user to either supply the paper text manually or re-run
   `/scaffold $0 <local.pdf|local.txt>`.
4. Read `reviews/$0/CLAUDE.md` for paper meta.
5. Read `reviews/$0/prompt.md`. If it is empty, write the user's
   exact `/phase1 ...` invocation (and any surrounding free-text from the
   user's message) into it as the first action — this is the orchestrator's
   prompt-of-record for the run.
6. Read the relevant methodology so the dispatch is faithful to spec:
   - `src/methodology/03-phases.md` § Phase 1
   - `src/methodology/03a-orchestration.md` § Parallelism (Phase 1)
   - `src/methodology/04-review.md`

Loop: **EXECUTE → REVIEW → CHECK → COMMIT**. Pause before ADVANCE; the user
runs `/phase2 $0` to advance.

## 1. EXECUTE

Dispatch subagents flat from this main session per their registered
frontmatters in `.claude/agents/`. Do not rewrite their prompts; pass inputs,
output paths, and the methodology/convention pointers.

If `$1` is empty, run the ordinary path in 1a-1d. If `$1` is `--large`, skip to
1L. In both modes, the review/check/commit path is identical after
`graph.v1.json` and `FINDINGS.md` exist.

### 1a. claim_extractor (sequential, first)

Dispatch `.claude/agents/claim_extractor.md` with:

- inputs:
  - `reviews/$0/paper/paper.txt`
  - `reviews/$0/paper/paper.meta.json`
  - `src/conventions/claim_taxonomy.md`
  - `src/conventions/confidence.md`
  - `src/methodology/05-artifacts.md`
- output:
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - working dir: `reviews/$0/phase1/agents/claim_extractor/` (`plan.md`, `log.md`)

Wait for completion. If `CLAIMS.md` is missing, stop and surface the failure.

### 1b. literature_searcher ‖ graph_builder (skeleton) — in parallel

In a single message, dispatch both subagents simultaneously:

- `.claude/agents/literature_searcher.md`:
  - inputs: `reviews/$0/phase1/outputs/CLAIMS.md`,
    `reviews/$0/paper/paper.txt`, `reviews/$0/paper/paper.meta.json`,
    `src/conventions/claim_taxonomy.md`, `src/conventions/confidence.md`,
    `src/methodology/05-artifacts.md`, `literature_bank/`
  - output: `reviews/$0/phase1/outputs/LITERATURE.md` and
    `reviews/$0/phase1/outputs/references.bib`
  - working dir: `reviews/$0/phase1/agents/literature_searcher/`
- `.claude/agents/graph_builder.md` (skeleton pass — claims only, no
  literature edges yet):
  - inputs: `reviews/$0/phase1/outputs/CLAIMS.md`,
    `src/conventions/graph_schema.json`,
    `src/conventions/graph_schema.md`
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
  - `src/conventions/graph_schema.md`
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
- pointers to the phase-1 output files, including both
  `graph.v1.skeleton.json` and `graph.v1.json`

Keep it short — one screen.

### 1L. Large-paper mode (`--large`)

Use this path for papers whose size makes one claim-extraction or literature
search pass unwieldy. The trigger is explicit only: do not auto-detect large
mode unless a future command spec says so.

Keep orchestration flat. The main session dispatches every shard and batch
worker directly; no subagent may spawn another subagent. Keep around **4 active
workers total** for L-GATr-scale papers. If there are more shards or batches,
run them in waves. Count the graph-skeleton worker as one active worker when it
runs alongside literature batches.

#### 1L-a. Plan shards and batches (serial preflight)

Before dispatching shard workers, the orchestrator serially chooses:

- claim shards: non-overlapping owned ranges of `paper.txt`, preferably by
  section/page boundaries. A shard prompt may include neighboring read-only
  context, but it may emit only claims whose provenance begins in its owned
  range.
- literature batch sizing policy. Assign concrete literature batches only after
  the serial claim merge creates canonical claim IDs.

This planning step may inspect structure and ranges, but it must not extract
claims, search literature, or judge evidence.

#### 1L-b. claim_extractor shards (parallel, capped)

Dispatch one `.claude/agents/claim_extractor.md` instance per shard, with at
most 4 active workers. Each shard worker owns only its declared working
directory and part file:

- inputs:
  - `reviews/$0/paper/paper.txt` restricted to the assigned range
  - `reviews/$0/paper/paper.meta.json`
  - `src/conventions/claim_taxonomy.md`
  - `src/conventions/confidence.md`
  - `src/methodology/05-artifacts.md`
- output:
  - `reviews/$0/phase1/agents/claim_extractor/shards/<NNN>/CLAIMS.part.md`
  - working dir:
    `reviews/$0/phase1/agents/claim_extractor/shards/<NNN>/`
    (`plan.md`, `log.md`)

Shard workers must not write `reviews/$0/phase1/outputs/CLAIMS.md`, sibling
shard directories, literature files, graph files, or review files.

After all shard workers finish, dispatch `.claude/agents/claim_extractor.md`
in **serial merge mode**:

- inputs: `reviews/$0/phase1/agents/claim_extractor/shards/*/CLAIMS.part.md`
  plus the optional existing `reviews/$0/phase1/outputs/CLAIMS.md` when
  iterating
- outputs:
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - `reviews/$0/phase1/agents/claim_extractor/merge/claim_id_map.md`
  - `reviews/$0/phase1/agents/claim_extractor/merge/plan.md`
  - `reviews/$0/phase1/agents/claim_extractor/merge/log.md`

The merge pass concatenates in paper order, removes exact duplicate boundary
claims, normalizes IDs/provenance, and writes the canonical `CLAIMS.md`. It
does not add new claims that no shard emitted.

If the canonical `CLAIMS.md` is missing or empty after merge, stop and surface
the failure.

#### 1L-c. graph skeleton and bank literature batches (parallel, capped)

After canonical `CLAIMS.md` exists, dispatch these in parallel while respecting
the 4-worker cap:

- `.claude/agents/graph_builder.md` (skeleton pass — claims only, no literature
  edges yet):
  - inputs: `reviews/$0/phase1/outputs/CLAIMS.md`,
    `src/conventions/graph_schema.json`,
    `src/conventions/graph_schema.md`
  - output: `reviews/$0/phase1/outputs/graph.v1.skeleton.json`
  - working dir: `reviews/$0/phase1/agents/graph_builder_skeleton/`
- `.claude/agents/literature_searcher.md` bank-batch workers, one per claim
  batch:
  - inputs: `reviews/$0/phase1/outputs/CLAIMS.md` restricted to the assigned
    claim IDs, `reviews/$0/paper/paper.txt`, `reviews/$0/paper/paper.meta.json`,
    `src/conventions/claim_taxonomy.md`, `src/conventions/confidence.md`,
    `src/methodology/05-artifacts.md`, `literature_bank/`
  - behavior: search only the local bank in this pass; do not run external
    search yet
  - outputs:
    - `reviews/$0/phase1/agents/literature_searcher/bank_batches/<NNN>/coverage.md`
    - `reviews/$0/phase1/agents/literature_searcher/bank_batches/<NNN>/LITERATURE.part.md`
    - `reviews/$0/phase1/agents/literature_searcher/bank_batches/<NNN>/references.part.bib`
  - working dir: `reviews/$0/phase1/agents/literature_searcher/bank_batches/<NNN>/`
    (`plan.md`, `log.md`)

Bank-batch workers must not write canonical `LITERATURE.md`, canonical
`references.bib`, graph files, sibling batch directories, or review files.

#### 1L-d. Bank barrier and uncovered-claim list (serial)

Wait for every bank batch and the graph skeleton to complete. Then, serially
read the bank part files and identify claim IDs with no bank candidate. Write
the uncovered list and merge notes under:

- `reviews/$0/phase1/agents/literature_searcher/barrier/uncovered.md`
- `reviews/$0/phase1/agents/literature_searcher/barrier/plan.md`
- `reviews/$0/phase1/agents/literature_searcher/barrier/log.md`

If there are no uncovered claims, skip external batches and proceed to the
literature merge.

#### 1L-e. External literature batches (parallel, capped)

For uncovered claims only, dispatch `.claude/agents/literature_searcher.md`
external-batch workers, again with at most 4 active workers:

- inputs: `reviews/$0/phase1/outputs/CLAIMS.md` restricted to the assigned
  uncovered claim IDs, `reviews/$0/paper/paper.txt`,
  `reviews/$0/paper/paper.meta.json`, `src/conventions/claim_taxonomy.md`,
  `src/conventions/confidence.md`, `src/methodology/05-artifacts.md`, and the
  bank part files for duplicate avoidance
- behavior: run external search for the assigned uncovered claims
- outputs:
  - `reviews/$0/phase1/agents/literature_searcher/external_batches/<NNN>/LITERATURE.part.md`
  - `reviews/$0/phase1/agents/literature_searcher/external_batches/<NNN>/references.part.bib`
- working dir: `reviews/$0/phase1/agents/literature_searcher/external_batches/<NNN>/`
  (`plan.md`, `log.md`)

External-batch workers must not write canonical `LITERATURE.md`, canonical
`references.bib`, graph files, sibling batch directories, or review files.

#### 1L-f. Literature merge (serial)

After bank and external batches finish, dispatch
`.claude/agents/literature_searcher.md` in **serial merge mode**:

- inputs:
  - `reviews/$0/phase1/agents/literature_searcher/bank_batches/*/coverage.md`
  - `reviews/$0/phase1/agents/literature_searcher/bank_batches/*/LITERATURE.part.md`
  - `reviews/$0/phase1/agents/literature_searcher/bank_batches/*/references.part.bib`
  - `reviews/$0/phase1/agents/literature_searcher/barrier/uncovered.md`
  - `reviews/$0/phase1/agents/literature_searcher/external_batches/*/LITERATURE.part.md`
  - `reviews/$0/phase1/agents/literature_searcher/external_batches/*/references.part.bib`
- outputs:
  - `reviews/$0/phase1/outputs/LITERATURE.md`
  - `reviews/$0/phase1/outputs/references.bib`
  - `reviews/$0/phase1/agents/literature_searcher/merge/plan.md`
  - `reviews/$0/phase1/agents/literature_searcher/merge/log.md`

The merge pass must:

- preserve claim order from canonical `CLAIMS.md`
- include only references emitted by literature workers; do not synthesize
  citations
- de-duplicate BibTeX entries by DOI, arXiv id, then normalized title; resolve
  key conflicts deterministically; and ensure every key used in `LITERATURE.md`
  resolves in `references.bib`
- record merge plan and notes in
  `reviews/$0/phase1/agents/literature_searcher/merge/{plan.md,log.md}`

If `LITERATURE.md` is missing, or citation keys cannot be resolved, stop and
surface the failure.

#### 1L-g. Final graph and FINDINGS (serial)

Run the same final graph merge as ordinary mode:

- inputs:
  - `reviews/$0/phase1/outputs/graph.v1.skeleton.json`
  - `reviews/$0/phase1/outputs/CLAIMS.md`
  - `reviews/$0/phase1/outputs/LITERATURE.md`
  - `reviews/$0/phase1/outputs/references.bib`
  - `src/conventions/graph_schema.json`
  - `src/conventions/graph_schema.md`
- output: `reviews/$0/phase1/outputs/graph.v1.json`
- working dir: `reviews/$0/phase1/agents/graph_builder/`

Then write `reviews/$0/phase1/outputs/FINDINGS.md` as in 1d. The review,
arbiter, and any fixer loop remain serial after this point.

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
  the same output paths the original agents used. After fixer completes, apply
  the dependency closure before review: if `CLAIMS.md` changed, re-dispatch
  `literature_searcher` and the `graph_builder` skeleton pass from the current
  claims, then re-run the final `graph_builder` merge. If only
  `LITERATURE.md`, `references.bib`, or `graph.v1.skeleton.json` changed,
  re-run the final `graph_builder` merge so `graph.v1.json` matches the
  current claim/literature set. In all cases, **re-derive `FINDINGS.md`** from
  the current `CLAIMS.md` / `LITERATURE.md` so counts and gap notes reflect the
  current state. For an initial `--large` run, preserve the large-mode
  dependency path: if any `CLAIMS.part.md` changes, redo the serial claim merge;
  if canonical `CLAIMS.md` changes, redo the graph skeleton plus bank-batch /
  barrier / external-batch / literature-merge sequence before the final graph
  merge. Then re-dispatch `critical_reviewer` and `arbiter`.
  Iterate at most **once**; if the second arbiter verdict is still ITERATE,
  escalate to the user.
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
