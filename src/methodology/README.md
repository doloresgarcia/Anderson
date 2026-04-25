# Methodology

These files define the rules of the game. The orchestrator and every subagent reads
the relevant subset before acting.

| File | Purpose |
|------|---------|
| `01-principles.md` | Scope, design principles, what the orchestrator does and does not do |
| `02-inputs.md` | What inputs Anderson accepts (paper PDF, URL, etc.) and how they are normalized |
| `03-phases.md` | The three phases, their deliverables, and gates between them |
| `03a-orchestration.md` | The orchestrator loop, subagent dispatch model, parallelism |
| `04-review.md` | Review protocol, classification (A/B/C), arbiter logic |
| `05-artifacts.md` | Required formats for every artifact a phase emits |
| `06-graph-conventions.md` | Pointer to the user-defined graph schema in `src/conventions/` |
