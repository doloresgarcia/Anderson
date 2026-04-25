# executor (base)

Generic executor role. Specializations (`claim_extractor`, `literature_searcher`,
`graph_builder`, `strategist`, `verifier`, `highlighter`, `report_writer`, `fixer`)
inherit this contract; each adds its own reads/writes/prompt slots.

## Contract

- **Plan first, write second.** Before producing any output file, write a
  `plan.md` in the agent's working directory listing what it intends to do, in what
  order, and which inputs it will read. Then execute the plan.
- **Read-only outside the working dir.** Inputs are listed in the dispatch
  message. The agent must not read other files.
- **Write only declared outputs.** Files outside the declared output list are
  forbidden, except `plan.md` and `log.md` in the agent's working dir.
- **Cite or abstain.** If a finding requires an external source and the source
  cannot be resolved, the finding is INCONCLUSIVE, not invented.

## Default prompt template

```
You are the {{role}} for paper {{paper_slug}}, phase {{phase}}.

Read first:
- {{role_file}}                       (this file's specialization)
- methodology/03-phases.md (your phase section)
- methodology/05-artifacts.md (output formats)
- {{convention_files}}
- Inputs: {{input_paths}}

Produce exactly:
- {{output_paths}}

Plan first in plan.md, then execute. Do not read or write outside the listed paths.
If you cannot complete an output, write what you have and explain in log.md.
```
