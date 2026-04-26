# Orchestration

## Loop (per phase)

```
Phases 1-2: EXECUTE → REVIEW → CHECK → COMMIT → ADVANCE
Phase 3:   EXECUTE → REVIEW → CHECK → HUMAN GATE → COMMIT
```

1. **EXECUTE.** Spawn each phase's subagents. Pass them: their role file
   (`.claude/agents/<role>.md`), the relevant methodology sections, the relevant convention
   files, and the upstream artifact paths. Do **not** rewrite role prompts ad hoc.
2. **REVIEW.** Spawn the reviewers prescribed for this phase. Each reviewer reads
   the phase artifacts and emits a review file under `phase<N>/review/`.
3. **CHECK.** Read reviewer findings.
   - Category A → spawn `fixer` (a specialization of `executor`), re-review.
   - Category B → spawn `fixer` once, accept on re-review unless new A.
   - Category C → record, do not re-review.
4. **COMMIT / GATE.** Phases 1 and 2 commit after arbiter PASS. Phase 3
   pauses for human review after arbiter PASS and commits only after APPROVE.
5. **ADVANCE.** Move to the next phase after a phase checkpoint commit. Phase 3
   has no automatic advance; ITERATE loops within phase 3 and REGRESS reopens
   the requested earlier phase.

## Dispatch contract

Every subagent invocation must receive:

- **Role file** — `.claude/agents/<role>.md` defines its prompt template. The orchestrator
  fills slots; it does not author the prompt.
- **Inputs list** — explicit file paths the agent is allowed to read.
- **Output spec** — exact file path(s) and format the agent must write.
- **Methodology pointers** — e.g., `methodology/05-artifacts.md` for format,
  `conventions/graph_schema.md` for the graph layout.

If an agent emits something outside its declared output spec, the orchestrator
treats that as a Category A finding.

## Parallelism

Within a phase, agents that write to disjoint files run in parallel:

- Phase 1: `claim_extractor` runs first (the others depend on `CLAIMS.md`).
  `literature_searcher` and a graph-skeleton pass of `graph_builder` then run in
  parallel; `graph_builder` re-runs once to merge. For explicit large-paper
  mode (`/phase1 <slug> --large`), Phase 1 uses the shard/batch sequence below.
- Phase 2: `strategist` runs first. The five checker agents
  (`checker_unreferenced`, `checker_ambiguous`, `checker_contradiction`,
  `checker_literature`, `checker_domain`) then run in parallel — one agent per
  error category, each examining all claims.
- Phase 3: `highlighter`, `graph_builder` (final), and `report_writer` run in
  parallel; they write to different files.

Cross-phase work is strictly sequential.

### Phase 1 large-paper mode

Large-paper mode is opt-in. The ordinary `/phase1 <slug>` flow remains valid
for normal papers; `/phase1 <slug> --large` switches only Phase 1 execution to
the following flat orchestration pattern.

Keep no more than about 4 active workers at once for L-GATr-scale papers. If
there are more claim shards or literature batches, run them in waves. The cap is
for total active workers, so a graph-skeleton worker running beside literature
batches counts against it.

The sequence is:

1. **Serial preflight and partitioning.** The orchestrator verifies scaffold
   inputs, then chooses non-overlapping owned paper ranges for claim shards.
   Shards may receive neighboring read-only context, but they emit claims only
   for their owned range. This step may inspect paper structure, but it does not
   extract claims.
2. **Parallel claim shards.** The orchestrator dispatches multiple
   `claim_extractor` instances directly. Each writes only
   `reviews/<slug>/phase1/agents/claim_extractor/shards/<NNN>/CLAIMS.part.md`
   plus its `plan.md` and `log.md`.
3. **Serial claim merge.** The orchestrator mechanically merges shard outputs
   into canonical `reviews/<slug>/phase1/outputs/CLAIMS.md`, preserving paper
   order and normalizing IDs without adding claims. The merge step owns
   `reviews/<slug>/phase1/agents/claim_extractor/merge/{claim_id_map.md,plan.md,log.md}`.
4. **Parallel graph skeleton plus bank batches.** The graph-skeleton
   `graph_builder` pass writes
   `reviews/<slug>/phase1/outputs/graph.v1.skeleton.json` while
   `literature_searcher` bank-batch workers write only
   `reviews/<slug>/phase1/agents/literature_searcher/bank_batches/<NNN>/coverage.md`,
   `LITERATURE.part.md`, and `references.part.bib`.
5. **Serial bank barrier.** The orchestrator waits for all bank batches and
   the skeleton, then records uncovered claim IDs under
   `reviews/<slug>/phase1/agents/literature_searcher/barrier/`.
6. **Parallel external batches.** For uncovered claims only,
   `literature_searcher` external-batch workers write only
   `reviews/<slug>/phase1/agents/literature_searcher/external_batches/<NNN>/LITERATURE.part.md`
   and `references.part.bib`.
7. **Serial literature merge.** The orchestrator merges bank and external part
   files into canonical `LITERATURE.md` and `references.bib`, de-duplicating
   keys without fabricating citations. The merge step owns
   `reviews/<slug>/phase1/agents/literature_searcher/merge/{plan.md,log.md}`.
8. **Serial finish.** The final `graph_builder` pass writes `graph.v1.json`,
   the orchestrator writes `FINDINGS.md`, and critical review plus arbiter run
   serially.

Agents never spawn agents in this mode. Parallel safety comes from disjoint
ownership paths; only serial merge steps write canonical Phase 1 outputs.

## Fixer dependency closures

After a fixer changes an upstream artifact, regenerate every deterministic
downstream artifact that depends on it before re-review:

- Phase 1: if `CLAIMS.md` changes, re-run `literature_searcher` and the
  `graph_builder` skeleton pass, then re-run the final `graph_builder` pass for
  `graph.v1.json`. If only `LITERATURE.md`, `references.bib`, or
  `graph.v1.skeleton.json` changes, re-run the final `graph_builder` pass. In
  all cases, re-derive `FINDINGS.md`. For a `--large` run, preserve the large
  dependency path: changed shard parts are merged serially into `CLAIMS.md`;
  changed canonical claims trigger graph skeleton plus bank batches, barrier,
  external batches, literature merge, final graph, and `FINDINGS.md`.
- Phase 2: if `STRATEGY.md` changes, re-run all checker sections; if any
  checker section changes, re-concatenate `VERIFICATION.md` in canonical
  section order and re-run `graph_builder` for `graph.v2.json`.
- Phase 3: regenerate the owning outputs for the affected surface: highlighter
  outputs for highlight issues, `graph.final.json` plus `graph.final.html` for
  graph issues, and `STATS.md` plus a fresh `report_writer` pass for
  report/stat issues.

## Context budget

The orchestrator's own context stays compact. Each subagent receives at most:

- ~1 page of bird's-eye framing (the root CLAUDE.md plus the phase CLAUDE.md).
- 2–5 pages of relevant methodology and conventions.
- The minimum set of upstream artifacts needed for its job.

If a subagent needs more, it asks via its review/log channel; the orchestrator does
not preemptively flood it.

## Health monitoring

- Use `git status` before dispatching risky work and keep partial outputs inside
  the phase working tree until the review/fix loop reaches a checkpoint.
- Long-running agents (>10 min with no new output) are respawned from the last
  phase checkpoint or clean pre-dispatch state.
- Append the original user prompt to `reviews/<slug>/prompt.md` as the very first
  action of the orchestrator.
