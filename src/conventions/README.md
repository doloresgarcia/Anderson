# Conventions

The files in this directory define the **domain logic** of Anderson:

| File | Defines |
|------|---------|
| `error_categories.md` | The five error categories, their color scheme, evidence standards, and severity order |
| `claim_taxonomy.md` | What counts as a claim, the type set used in `CLAIMS.md` |
| `graph_schema.md` | Node and edge types, IDs, properties of the claim graph |
| `verification.md` | Domain-specific verification refinements on top of `error_categories.md` |
| `confidence.md` | The single discrete confidence scale used across all artifacts |

These are **user-defined**. The skeleton ships placeholders — agents detect a
placeholder and degrade gracefully (mark every claim `UNCLASSIFIED`, every
category unchecked, etc.) but the system cannot produce useful output until
they are written.

## Why these are kept separate from `methodology/`

Methodology = how the orchestrator runs (phases, dispatch, review). Stable.

Conventions = what the orchestrator is reasoning about (graph shape, claim types,
verification rules). Domain-specific and likely to change as the project matures.

If you find yourself editing files in `methodology/` to make a domain change, the
domain logic is leaking. Push it back into `conventions/`.
