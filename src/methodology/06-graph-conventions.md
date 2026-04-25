# Conventions (pointer)

Domain logic — the graph schema, claim taxonomy, verification rules, and
confidence scale — is deliberately **not** specified in `methodology/`. It lives
in `src/conventions/`:

- `conventions/graph_schema.md` — node and edge types, IDs, properties
- `conventions/claim_taxonomy.md` — what counts as a claim, claim labels
- `conventions/verification.md` — verification methods, pass/fail criteria
- `conventions/confidence.md` — single discrete confidence scale used everywhere

`graph_schema.md` is still a placeholder; the other three are filled in. While
`graph_schema.md` is a placeholder, `graph_builder` produces a minimal
node-per-claim graph and reviewers raise a Category B finding noting the gap.
That degraded mode lets the orchestration loop be exercised end-to-end before
the schema is nailed down.

When convention files change, no agent role file or methodology file should
need to change. If you find yourself editing role files to accommodate a
convention change, the domain logic is leaking — push the change back into the
relevant convention file.
