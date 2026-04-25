# Graph conventions (pointer)

The graph schema, claim taxonomy, and verification rules are deliberately **not**
specified in `methodology/`. They live in `src/conventions/`:

- `conventions/graph_schema.md` — node and edge types, IDs, properties
- `conventions/claim_taxonomy.md` — what counts as a claim, claim labels
- `conventions/verification.md` — verification methods, pass/fail criteria

These three files are user-defined. Until they are filled in, agents will produce
schema-correct but semantically empty graphs (e.g., one node per sentence with no
typing). That is expected behavior for a skeleton run — it confirms the orchestration
loop works end-to-end before the domain logic is added.

When the convention files change, no agent role file or methodology file should need
to change. If you find yourself editing role files to accommodate a schema change,
the schema is leaking — push the change back into the convention file.
