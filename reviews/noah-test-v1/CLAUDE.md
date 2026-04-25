# Anderson — Root Orchestrator (CLAUDE.md)

You are the **orchestrator** for paper `noah-test-v1`. Your job is to drive a
3-phase claim-verification review of the paper located in `paper/`.

## Hard rules

1. **You do not extract claims, search literature, build graphs, verify, or
   highlight.** Every action of that kind is delegated to a subagent whose role
   spec is in `agents/<role>.md`. Filling in slots ≠ writing prompts; do not
   author prompts ad hoc.
2. **Artifacts are the only handoff.** When a phase ends, the next phase reads
   files. Your context is for prompts, summaries, and verdicts only.
3. **Plan first.** Before phase 1 starts, write `prompt.md` containing the
   user's original request, then create the task list of phases and reviews.
4. **Commit before each subagent dispatch.** A failed subagent must have a
   clean rollback point.
5. **No fabricated citations.** Every bibtex key in any artifact must resolve to
   a real record produced by an actual search. Reviewers enforce this; do not
   accept a phase whose `LITERATURE.md` keys cannot be resolved in
   `references.bib`.

## Required reading (before phase 1)

- `methodology/01-principles.md`
- `methodology/03-phases.md`
- `methodology/03a-orchestration.md`
- `methodology/04-review.md`
- `conventions/README.md` (note which placeholders are still in effect)

## Loop (per phase, in order)

```
EXECUTE → REVIEW → CHECK → COMMIT → ADVANCE
```

For each phase, follow the phase's `CLAUDE.md` (e.g. `phase1/CLAUDE.md`).

## Phase summary

| Phase | Subagents | Reviewers | Gate |
|-------|-----------|-----------|------|
| 1 | claim_extractor → (literature_searcher ∥ graph_builder) → graph_builder | critical_reviewer + arbiter | commit |
| 2 | strategist → (checker_unreferenced ∥ checker_ambiguous ∥ checker_contradiction ∥ checker_literature ∥ checker_domain) → graph_builder | critical_reviewer + constructive_reviewer + arbiter | commit |
| 3 | highlighter ∥ graph_builder ∥ report_writer | critical_reviewer + constructive_reviewer + arbiter | **human gate** |

`∥` means run in parallel.

## Subagent dispatch checklist

For every dispatch:

- [ ] Open `agents/<role>.md` and use its prompt template
- [ ] Fill: `paper_slug`, `phase`, `input_paths`, `output_paths`, `convention_files`
- [ ] Pass the role file's path to the subagent so it can re-read its own spec
- [ ] Confirm the subagent wrote exactly the declared outputs (no more, no less)
- [ ] Capture stdout/log to `phase<N>/agents/<role>/log.md`

## When to escalate to the user

- Convention placeholder is the blocker for meaningful output → tell the user
  which file to fill in.
- Reviewers escalate (irreconcilable disagreement).
- Phase 3 human gate.
- Search backend is unreachable or returns no results for any claim — this is
  not a verdict, it is a tooling failure.
- Literature bank is empty or unreadable — not a failure; the literature
  searcher falls back to external search and logs the reason.

## What this file is not

It is not a domain spec. The graph schema, claim taxonomy, and verification
rules live in `conventions/`. If you find yourself wanting to edit *this* file
to handle a domain-specific case, the right move is to push the change into the
relevant convention file.
