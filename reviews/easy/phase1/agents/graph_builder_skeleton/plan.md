# Phase 1 Skeleton Pass — Plan

**Task:** Build `reviews/easy/phase1/outputs/graph.v1.skeleton.json` from 200 extracted claims (C001–C200) with no literature edges.

## Input sources
- `CLAIMS.md`: 200 rows, columns: claim_id, type, sentence, hedged, confidence, page, line, section, provenance
- `graph_schema.json`: validation schema (executable)
- `graph_schema.md`: prose clustering algorithm and color model

## Process

1. **Parse claims** — read all 200 rows, extract required fields
2. **Initial clustering** — group by (section, type) per schema §Clustering algorithm step 2
3. **Split oversized clusters** — handle any with >15 claims per §3
4. **Merge until ≤20 clusters** — per §4
5. **Floor rule** — if <5 clusters and any has >5 claims, apply §5 (logged)
6. **Generate titles and captions** — per §6
7. **Serialize to JSON** — with required fields per schema
8. **Validate** — check against `graph_schema.json`
9. **No literature edges** — edges array will be empty (claims-only skeleton)

## Output path
- `reviews/easy/phase1/outputs/graph.v1.skeleton.json`

## Validation targets
- `len(groups) ≤ 20`
- `1 ≤ len(claim_ids) ≤ 15` per group
- all claims have correct parent references
- colors derived from verdict (all NOT_CHECKED at skeleton → gray)
- JSON validates against `src/conventions/graph_schema.json`

## Deferred
- Literature edges (next graph_builder pass, phase 1 final)
- Claim verdicts (phase 2 after verification)
