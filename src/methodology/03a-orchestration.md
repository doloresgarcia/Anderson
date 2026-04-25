# Orchestration

## Loop (per phase)

```
EXECUTE → REVIEW → CHECK → COMMIT → ADVANCE
```

1. **EXECUTE.** Spawn each phase's subagents. Pass them: their role file
   (`agents/<role>.md`), the relevant methodology sections, the relevant convention
   files, and the upstream artifact paths. Do **not** rewrite role prompts ad hoc.
2. **REVIEW.** Spawn the reviewers prescribed for this phase. Each reviewer reads
   the phase artifacts and emits a review file under `phase<N>/review/`.
3. **CHECK.** Read reviewer findings.
   - Category A → spawn `fixer` (a specialization of `executor`), re-review.
   - Category B → spawn `fixer` once, accept on re-review unless new A.
   - Category C → record, do not re-review.
4. **COMMIT.** Conventional commit `<type>(phase<N>): <description>`.
5. **ADVANCE.** Move to the next phase, or to the human gate.

## Dispatch contract

Every subagent invocation must receive:

- **Role file** — `agents/<role>.md` defines its prompt template. The orchestrator
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
  parallel; `graph_builder` re-runs once to merge.
- Phase 2: `strategist` runs first. The five checker agents
  (`checker_unreferenced`, `checker_ambiguous`, `checker_contradiction`,
  `checker_literature`, `checker_domain`) then run in parallel — one agent per
  error category, each examining all claims.
- Phase 3: `highlighter`, `graph_builder` (final), and `report_writer` run in
  parallel; they write to different files.

Cross-phase work is strictly sequential.

## Context budget

The orchestrator's own context stays compact. Each subagent receives at most:

- ~1 page of bird's-eye framing (the root CLAUDE.md plus the phase CLAUDE.md).
- 2–5 pages of relevant methodology and conventions.
- The minimum set of upstream artifacts needed for its job.

If a subagent needs more, it asks via its review/log channel; the orchestrator does
not preemptively flood it.

## Health monitoring

- Commit before each subagent dispatch so any failure has a clean rollback point.
- Long-running agents (>10 min with no new output) are respawned from the last
  commit.
- Append the original user prompt to `reviews/<slug>/prompt.md` as the very first
  action of the orchestrator.
