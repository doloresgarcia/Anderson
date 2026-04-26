# Graph Builder — Phase 1 Final Pass

## Objective
Merge the skeleton graph (claims + groups, 0 edges) with literature references from LITERATURE.md and references.bib to produce graph.v1.json.

## Inputs
- `graph.v1.skeleton.json` — skeleton with groups and claims, no edges
- `LITERATURE.md` — per-claim literature candidates with bibtex keys
- `references.bib` — resolved bibtex records
- `src/conventions/graph_schema.json` — validation schema

## Plan
1. Load and parse the skeleton JSON
2. Parse LITERATURE.md to extract edges per claim (claim → bibtex keys)
3. Validate that all bibtex keys in LITERATURE.md exist in references.bib
4. Add literature edges to the graph (source=claim, target=key, kind=supports/related/contradicts)
5. Ensure all nodes (claims, groups) are present in the output
6. Validate the final graph against graph_schema.json
7. Write graph.v1.json
8. Log any mismatches or warnings

## Notes
- Each literature entry in LITERATURE.md for a claim becomes one edge in the graph
- Edge kind is inferred from the literature entry's relation type (supports → "supports", related → "supports", etc.)
- Confidence is preserved in the edge
- All reference nodes (bibtex keys) are implicit; the graph treats them as document identifiers
- No claim-to-claim dependencies are added in this pass (they are added in Phase 2 after verification)
