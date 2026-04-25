# graph_builder (phase 1, skeleton pass) — plan

## Goal

Produce `phase1/outputs/graph.v1.skeleton.json`: a structural-only graph with
217 claim nodes (one per row in `CLAIMS.md`) clustered into ≤20 thematic group
nodes. No literature merging, no verdicts, no fabricated edges.

## Inputs

- `phase1/outputs/CLAIMS.md` (217 claims, C001–C217)
- `conventions/graph_schema.md` (definitive schema, palette, clustering algorithm,
  validation rules)
- `conventions/claim_taxonomy.md`
- `conventions/confidence.md`

## Outputs (declared)

- `phase1/outputs/graph.v1.skeleton.json`
- `phase1/agents/graph_builder/plan.md` (this file)
- `phase1/agents/graph_builder/log.md`

## Procedure

1. **Parse `CLAIMS.md`**: 217 rows, fields `claim_id, type, sentence, hedged,
   confidence, page, line, section, provenance`.

2. **Run the clustering algorithm in `conventions/graph_schema.md` verbatim**:

   - **Step 1 (degenerate)**: N=217 > 20 → continue.
   - **Step 2 (initial clusters)**: group by `(section, type)`. This yields 40
     initial clusters (computed; see section breakdown below).
   - **Step 3 (split oversized)**: any cluster with > 15 claims is split. The
     three oversized clusters at this stage are:
     - `(App.A, method)` → 28 claims
     - `(5, method)` → 21 claims
     - `(2.1, background_fact)` → 18 claims
     - `(4, method)` → 18 claims
     Split first by sub-section (the existing `section` column is already
     fine-grained: e.g. `2.1`, `2.2`, `2.3`, `2.4` are sub-sections of §2 and
     are already separate). Where no finer sub-section labels exist, split by
     paragraph proximity: contiguous runs of `claim_id` (which are emitted in
     paper order) form the natural paragraph chunks. For each oversized cluster
     I split into chunks of ≤ 15 by consecutive claim id within the cluster.
   - **Step 4 (merge until ≤ 20)**: while `|clusters| > 20`, pick the two
     smallest clusters that share `section` or `type`; merge. Tie-break by
     section adjacency in the paper's reading order
     (`Abstract → 1 → 2.1 → 2.2 → 2.3 → 2.4 → 3 → 4 → 5 → 6 → Code → App.A`).
   - **Step 5 (floor)**: 217 claims and ≤ 20 clusters → at least one cluster
     will hold many claims; floor (< 5 clusters) is not at risk here.
   - **Step 6 (title and caption)**: 2–3-word title from the dominant noun
     phrase of the most central claim; one-sentence caption ≤ 25 words. The
     "most central" claim is taken to be the median-position claim in the
     cluster (deterministic given the input ordering); if that claim is too
     specific to title the cluster, pick the cluster's most type-typical claim.
   - **Step 7 (cross-cluster edges)**: extractor produced no structural-edge
     sidecar this run, so the skeleton has zero edges. This is allowed in
     phase 1 per `graph_builder.md`.

3. **Emit one `claim` node per row** with fields per
   `conventions/graph_schema.md`:
   `id, kind="claim", parent, type, sentence, hedged, confidence, verdict="NOT_CHECKED",
   color="#95A5A6", page, line, section`. Phase-1 skeleton has no v2 fields
   (`verdict_confidence`, `verdict_reason`, `evidence`).

4. **Emit one `group` node per cluster** with fields:
   `id, kind="group", title, caption, claim_ids, dominant_type,
   verdict="NOT_CHECKED", color="#95A5A6", section, page_range`.
   `dominant_type` = most common claim type in the cluster, or `"mixed"` if no
   type holds > 60%. `section` = the cluster's anchoring section, or
   `"multiple"` if the cluster spans more than one. `page_range` = `[min, max]`
   over constituent claims (the `page` column in CLAIMS.md is a placeholder
   `?` for every row, so I use the `line` column as a proxy and document this
   in `log.md`).

5. **Validate** against the rules in `conventions/graph_schema.md`:
   - `len(groups) ≤ 20`
   - `1 ≤ len(group.claim_ids) ≤ 15` for every group
   - every `claim.parent` resolves to a group, and the claim id is in that
     group's `claim_ids`
   - every `edge.source`/`edge.target` resolves to a `claim` (skeleton has no
     edges → vacuous)
   - no `source == target` edges (vacuous)
   - color hex matches the verdict per the palette (all gray here, since all
     claims are `NOT_CHECKED`)
   - no inferred-low-confidence `contradicts` edges (vacuous)
   - every node carries provenance (claims carry `paper.txt:line`; groups
     inherit from their children) — recorded in the JSON.

6. **Write the JSON** in the exact shape from `conventions/graph_schema.md`:
   `{paper, groups, claims, edges, schema_version}`.

7. **Log** all step-5/step-6 judgment calls in `log.md`.

## Cluster sketch (target ≤ 20)

Pre-merge, after step-3 splits, the 40 (section, type) buckets become ~43
chunks. The merge step contracts them to 20 by repeatedly merging the two
smallest neighbours that share a section or a type, with tie-breaking by
paper-section adjacency. The deterministic output of this procedure is what
gets emitted; I do not pre-decide the final partition here, the algorithm
does.

## Hard constraints

- No invented edges.
- No verdict layer beyond `NOT_CHECKED`.
- No literature-derived nodes/edges (those come in the next dispatch).
- Only the three declared output files.
