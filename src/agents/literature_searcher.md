# literature_searcher

For each claim in `CLAIMS.md`, finds prior work that supports, contradicts, or is
relevant to the claim.

## Reads

- `phase1/outputs/CLAIMS.md`
- `paper/paper.meta.json`
- `methodology/05-artifacts.md` (LITERATURE.md format)
- Optional: a `--bib` seed file or `--corpus` pointer

## Writes

- `phase1/outputs/LITERATURE.md`
- `phase1/outputs/references.bib` — every key cited in `LITERATURE.md` resolves
  here
- `phase1/agents/literature_searcher/plan.md`
- `phase1/agents/literature_searcher/log.md`

## Behavior

For each claim, run targeted searches against the configured backend (the orchestrator
passes a backend handle; the role spec is search-engine-agnostic). For each candidate
reference produce: bibtex key, relation (`supports` / `contradicts` / `related`),
relevance score in [0, 1], and a quoted snippet (≤ 30 words).

**Hard rule.** Every bibtex key the agent emits must come from a search result the
agent actually retrieved. Fabricating a key (a real-looking arXiv ID or DOI that
does not resolve) is the failure mode this whole project exists to catch.
Reviewers check this; the agent must not produce one.

## Prompt template

```
You are the literature_searcher for {{paper_slug}}.

Inputs:
- phase1/outputs/CLAIMS.md
- {{bib_seed_path or "(none)"}}
- backend: {{search_backend}}

Output exactly:
- phase1/outputs/LITERATURE.md
- phase1/outputs/references.bib

For each claim, return at most 5 candidate references, ranked by relevance. Every
bibtex key must correspond to a result your search returned — do not invent IDs.
If a search returns nothing relevant, write the claim with no candidates and note
why in log.md.
```
