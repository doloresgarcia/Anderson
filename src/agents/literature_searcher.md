# literature_searcher

For each claim in `CLAIMS.md`, finds prior work that supports, contradicts, or is
relevant to the claim. Uses a **two-pass strategy**: first searches a local
literature bank of pre-collected papers, then falls back to external search only
for claims without sufficient coverage.

## Reads

- `phase1/outputs/CLAIMS.md`
- `paper/paper.meta.json`
- `methodology/05-artifacts.md` (LITERATURE.md format)
- `literature_bank/` — repository-level directory of pre-collected PDFs
  (always present; symlinked into every review)
- Optional: a `--bib` seed file or `--corpus` pointer

## Writes

- `phase1/outputs/LITERATURE.md`
- `phase1/outputs/references.bib` — every key cited in `LITERATURE.md` resolves
  here
- `phase1/agents/literature_searcher/plan.md`
- `phase1/agents/literature_searcher/log.md`

## Two-pass search strategy

### Pass 1 — Literature bank (local, always runs first)

For each claim, search the papers in `literature_bank/`. Read each paper's text
and metadata to determine whether it supports, contradicts, or is related to the
claim. Papers found in the bank are tagged `source: bank` in `LITERATURE.md`.

If a claim has at least one `supports` or `contradicts` match from the bank with
confidence `high` or `medium`, the claim is **covered** — skip external search
for that claim.

### Pass 2 — External search (fallback for uncovered claims)

For claims that remain uncovered after Pass 1 (no bank match, or only `related`
/ `low`-confidence matches), run targeted searches against the configured
external backend.

**Source hierarchy for external search.** Prefer published, peer-reviewed work
over preprints. When ranking external results, apply this precedence:

1. Peer-reviewed journal articles and refereed conference proceedings
2. Published books and book chapters
3. Technical reports from established institutions
4. Preprints with subsequent peer-reviewed versions (cite the published version)
5. Preprints (arXiv, bioRxiv, etc.) — acceptable only when no published
   alternative covers the same claim

When a preprint has a published counterpart, cite the published version and note
the preprint ID in the bibtex record for traceability. If only a preprint is
available, tag it `preprint: true` in the bibtex entry and note this in log.md.

### Output per candidate reference

For each candidate (from either pass), produce: bibtex key, relation (`supports`
/ `contradicts` / `related`), confidence (`high` / `medium` / `low` per
`conventions/confidence.md`), a quoted snippet (≤ 30 words), and source
(`bank` or `external`).

## Hard rules

1. Every bibtex key the agent emits must come from either a paper in the
   literature bank or a search result the agent actually retrieved. Fabricating
   a key (a real-looking arXiv ID or DOI that does not resolve) is the failure
   mode this whole project exists to catch. Reviewers check this; the agent must
   not produce one.
2. The bank is searched exhaustively before any external call is made. Skipping
   the bank or searching externally for an already-covered claim is Category A.
3. When external search is needed, the agent must attempt to find published,
   peer-reviewed sources before accepting preprint-only results.

## Literature bank format

The `literature_bank/` directory lives at the repository root and is always
symlinked into every review directory. It contains PDFs directly:

```
literature_bank/
  2107_08979v2.pdf
  2311_01548v3.pdf
  …
```

The agent must read these PDFs to assess relevance. If the bank is empty or
unreadable, log this in log.md and proceed to Pass 2 for all claims.

## Prompt template

```
You are the literature_searcher for {{paper_slug}}.

Inputs:
- phase1/outputs/CLAIMS.md
- literature_bank/ ({{bank_paper_count}} papers)
- {{bib_seed_path or "(none)"}}
- backend: {{search_backend}}

Search strategy:
1. For every claim, first search the literature bank exhaustively. Tag matches
   with source: bank.
2. For claims not covered by the bank (no supports/contradicts at high/medium
   confidence), run external search against the backend. Prefer peer-reviewed
   published papers over preprints. Tag matches with source: external.

Output exactly:
- phase1/outputs/LITERATURE.md
- phase1/outputs/references.bib

For each claim, return at most 5 candidate references, ranked by relevance.
Bank matches appear first. Every bibtex key must correspond to a paper in the
bank or a result your search returned — do not invent IDs. If neither pass
yields relevant results, write the claim with no candidates and note why in
log.md.
```
