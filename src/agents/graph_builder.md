# graph_builder

Builds and updates the claim graph per `conventions/graph_schema.md`.

## Reads (varies by phase)

Phase 1:
- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `conventions/graph_schema.md`
- `conventions/claim_taxonomy.md`
- `conventions/confidence.md`

Phase 2:
- `phase1/outputs/graph.v1.json`
- `phase2/outputs/VERIFICATION.md`
- `conventions/graph_schema.md`

Phase 3:
- `phase2/outputs/graph.v2.json`
- `phase3/outputs/REPORT.md` (for any final-pass annotations)
- `conventions/graph_schema.md`

## Writes (varies by phase)

- Phase 1 → `phase1/outputs/graph.v1.json`
- Phase 2 → `phase2/outputs/graph.v2.json`
- Phase 3 → `phase3/outputs/graph.final.json`,
  `phase3/outputs/graph.final.html`,
  `phase3/outputs/graph.final.svg`

## Behavior

### Phase 1 — structural pass

1. Run the **clustering algorithm** in `conventions/graph_schema.md` to produce
   ≤ 20 `group` nodes from the claims in `CLAIMS.md`.
2. Emit one `claim` node per `CLAIMS.md` row, each with `parent` pointing to its
   group.
3. Carry over claim-to-claim edges identified by the extractor's structural
   pass (or none if the extractor did not produce any). Do not invent edges in
   phase 1; missing edges is fine.
4. Set every claim's `verdict` to `NOT_CHECKED` (no verification has happened
   yet). Group verdicts aggregate to `NOT_CHECKED` / gray.
5. Validate against the schema's validation rules; reject the build if any
   fails.

### Phase 2 — verdict pass

1. Read `graph.v1.json` and `VERIFICATION.md`.
2. For each claim with a row in `VERIFICATION.md`, populate `verdict`,
   `verdict_confidence`, `verdict_reason` (if INCONCLUSIVE), and `evidence`.
3. Recompute `color` for every claim from the palette.
4. Re-aggregate every group's `verdict` and `color` per the aggregation rule.
5. Emit `graph.v2.json`. The set of nodes and structural edges must equal
   `graph.v1.json` — phase 2 only adds verdict-layer fields. New nodes or
   edges in phase 2 are auto-Category-A.

### Phase 3 — final pass + render

1. Copy `graph.v2.json` content into `graph.final.json` (no edits unless
   `REPORT.md` flags a final-pass correction; document any such correction in
   `log.md`).
2. Render `graph.final.html` by invoking the bundled utility script — do
   **not** write the Cytoscape.js HTML by hand:

   ```bash
   python3 ../../src/render_graph.py phase3/outputs/graph.final.json
   ```

   The script reads the schema's color palette and produces a Cytoscape.js
   compound-graph view. If you need to override styling, edit the script
   rather than hand-rolling HTML — keeps one source of truth.
3. Render `graph.final.svg` as a static snapshot. (The renderer does not yet
   emit SVG directly; for now produce the SVG by opening `graph.final.html`
   in a headless browser, or skip and log the gap. SVG is for static reports
   only — the HTML is the primary visual.)

### Universal rules

- **Never overwrite a previous version.** v1 stays v1; v2 is a new file; final
  is a new file.
- **Validate before writing.** Any of the schema's validation rules failing →
  do not write the output, log the failure in `log.md`, and exit with a
  non-zero status.
- **No invented edges.** Every edge has either a paper-anchor `provenance`
  (e.g. `paper.txt:142`) or `provenance: "inferred"` with `confidence` ≤
  `medium`. An `inferred` edge of kind `contradicts` with `low` confidence is
  forbidden.

## Prompt template

```
You are the graph_builder for {{paper_slug}}, phase {{phase}}.

Inputs:
- {{input_paths}}

Output exactly:
- {{output_paths}}

Conform to conventions/graph_schema.md (schema, palette, clustering algorithm,
HTML spec). Validate before writing. Do not overwrite prior versions. Phase 2
only adds verdict-layer fields — same nodes and structural edges as v1.
```
