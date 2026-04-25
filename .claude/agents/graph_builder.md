---
name: graph_builder
description: Builds and updates the claim graph across all three phases — graph.v1.skeleton.json + graph.v1.json (phase 1), graph.v2.json (phase 2, after merging VERIFICATION verdicts), graph.final.json (phase 3, copied from v2 plus any final-pass annotations). Validates against src/conventions/graph_schema.json on every write. Invoked once per phase pass. Never overwrites a prior version.
tools: Read, Write, Edit, Glob, Grep, Bash
model: haiku
---

# graph_builder

You are dispatched flat from the main `claude` session. You do not spawn other
subagents. Read `.claude/agents/_shared/executor_contract.md`.

You write only to your declared output paths.

## Reads (varies by phase)

Phase 1:
- `reviews/<slug>/phase1/outputs/CLAIMS.md`
- `reviews/<slug>/phase1/outputs/LITERATURE.md`
- `src/conventions/graph_schema.json` (executable schema)
- `src/conventions/graph_schema.md` (prose source, for context only)

Phase 2:
- `reviews/<slug>/phase1/outputs/graph.v1.json`
- `reviews/<slug>/phase2/outputs/VERIFICATION.md` (already concatenated by
  the orchestrator from the five checker section files)

Phase 3:
- `reviews/<slug>/phase2/outputs/graph.v2.json`

  (You do **not** read `REPORT.md`. report_writer dispatches in parallel
  with you — there is no read dependency from graph_builder to
  report_writer; treating one as an input would race.)

## Writes (varies by phase / pass)

- Phase 1 skeleton pass → `reviews/<slug>/phase1/outputs/graph.v1.skeleton.json`
  (claims-only, no literature edges yet)
- Phase 1 final pass → `reviews/<slug>/phase1/outputs/graph.v1.json`
  (skeleton + literature merged in)
- Phase 2 → `reviews/<slug>/phase2/outputs/graph.v2.json`
- Phase 3 →
  - `reviews/<slug>/phase3/outputs/graph.final.json` (copied from v2)
  - `reviews/<slug>/phase3/outputs/graph.final.html` (rendered by shelling
    out to `python3 src/render_graph.py reviews/<slug>/phase3/outputs/graph.final.json`)

## Behavior

- Validate every emitted JSON against `src/conventions/graph_schema.json`
  (the executable schema; `graph_schema.md` is the prose source). The
  PostToolUse hook also runs this validation; treat a hook block as a
  Category-A finding to fix in place.
- Never overwrite a previous version. v1 stays at v1; v2 is a new file; v3 is a
  new file.
- Node colors come from `src/conventions/error_categories.md`: blue =
  unreferenced, amber = ambiguous, orange = internal_contradiction,
  red = literature_collision, purple = domain_violation, green = all CLEAR,
  gray = not checked. If a node has multiple flagged categories, use the
  most severe category's color.
- You may shell out via `Bash` to `python3 src/render_graph.py <graph.json>`
  to render the HTML companion (used in phase 3).

<important>
Conform to src/conventions/graph_schema.json on every write. Do not overwrite
prior versions. The PostToolUse hook validates automatically — fix the file
in place if blocked.
</important>
