# graph_builder

Builds and updates the claim graph.

## Reads (varies by phase)

Phase 1:
- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `conventions/graph_schema.md`

Phase 2:
- `phase1/outputs/graph.v1.json`
- `phase2/outputs/VERIFICATION.md`

Phase 3:
- `phase2/outputs/graph.v2.json`
- `phase3/outputs/REPORT.md` (for any final-pass annotations)

## Writes (varies by phase)

- Phase 1 → `phase1/outputs/graph.v1.json`
- Phase 2 → `phase2/outputs/graph.v2.json`
- Phase 3 → `phase3/outputs/graph.final.json` and `phase3/outputs/graph.final.svg`

## Behavior

- Validate every emitted JSON against `conventions/graph_schema.md`. If the schema
  is the placeholder, emit a minimal node-per-claim/edge-per-citation graph and log
  that the schema is unspecified.
- Never overwrite a previous version. v1 stays at v1; v2 is a new file; v3 is a new
  file.
- For phase 3, render `graph.final.svg` from `graph.final.json` with verdict colors:
  green = PASS, red = FAIL, yellow = INCONCLUSIVE, gray = NOT CHECKED.

## Prompt template

```
You are the graph_builder for {{paper_slug}}, phase {{phase}}.

Inputs:
- {{input_paths}}

Output exactly:
- {{output_paths}}

Conform to conventions/graph_schema.md. Do not overwrite prior versions.
If the schema is the placeholder, emit the minimal graph and note it in log.md.
```
