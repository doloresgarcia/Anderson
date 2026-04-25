# Executor contract (shared)

This contract is inherited by every Anderson executor specialization
(`claim_extractor`, `literature_searcher`, `graph_builder`, `strategist`, the
five `checker_*`, `highlighter`, `report_writer`, `fixer`). It is referenced
from each agent body by relative path; the dispatching slash command may also
point the agent here.

## Architecture invariant

You are dispatched flat from the main `claude` session (the orchestrator). You
do not spawn other subagents. If your work needs another role, return that as
a recommendation in your output and let the orchestrator dispatch.

## Contract

- **Plan first, write second.** Before producing any output file, write a
  `plan.md` in the agent's working directory listing what you intend to do, in
  what order, and which inputs you will read. Then execute the plan.
- **Read-only outside the working dir.** Inputs are listed in the dispatch
  message. Do not read other files.
- **Write only declared outputs.** Files outside the declared output list are
  forbidden, except `plan.md` and `log.md` in the agent's own working dir
  (`reviews/<slug>/phase<N>/agents/<role>/`).
- **Cite or abstain.** If a finding requires an external source and the source
  cannot be resolved, the finding is `INCONCLUSIVE`, not invented.
- **Disjoint outputs.** Two parallel agents never write to the same file.
  Where a logical artifact is the union of several agents' work (e.g.
  `VERIFICATION.md`), each agent writes a section file under its own working
  dir and a sequential concat step assembles the final artifact.
- **Logs.** End with a `log.md` in your working dir summarizing what you read,
  what you wrote, what (if anything) you abstained on, and any gaps the
  orchestrator should know about.

## Universal reads

Every executor specialization reads:

- `src/methodology/03-phases.md` — your phase section
- `src/methodology/05-artifacts.md` — output formats
- the role file (`.claude/agents/<your_name>.md`) — your specialization
- the agent-specific reads listed in your role file

## Universal output discipline

If you cannot complete an output, write what you have and explain in `log.md`.
Do not fabricate. Reviewers (critical/constructive/arbiter) check that every
declared output exists, that nothing extra exists, and that no claim, citation,
or graph node is invented.
