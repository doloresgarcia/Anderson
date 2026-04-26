# Phase 1 — FINDINGS for `easy` (round 2, post-fixer)

Author: orchestrator (not a subagent). Companion to `CLAIMS.md`,
`LITERATURE.md`, `references.bib`, `graph.v1.skeleton.json`, and
`graph.v1.json`. This file was re-derived after the round-1 fixer pass per
the dependency-closure rule in `src/methodology/03a-orchestration.md`.

## Paper

- Title: *A Lorentz-Equivariant Transformer for All of the LHC* (L-GATr).
- Authors: Brehmer, Bresó, de Haan, Plehn, Qu, Spinner, Thaler.
- Venue / id: SciPost Physics submission, MIT-CTP/5802. Date string in
  paper.txt: April 25, 2026.
- arXiv id (inferred): **2405.14806** — the paper under review *is* (a
  revision of) the L-GATr arXiv preprint. This identification was made
  during the round-1 fixer pass after the reviewer flagged
  `spinner2024lgatr` as a self-citation.
- Source: `papers/annotated/paper_corrupted.pdf` (the file name signals
  pre-marked annotations; pymupdf extraction produced a clean
  `paper.txt` with no observed gross OCR loss).

## Claim counts

- Total claims: **200** (`C001`–`C200`).
- UNCLASSIFIED: **0** — `claim_taxonomy.md` is the real taxonomy, not the
  placeholder, so every claim is typed.
- Hedged: **0** (per the taxonomy's strict "explicit weakening marker"
  definition — the extractor's `log.md` records this choice).

Distribution by taxonomy type (unchanged by the fixer pass; F-001/F-003
edited only sentence text and provenance, not types):

| type | count |
|---|---|
| method | 94 |
| result | 37 |
| interpretation | 35 |
| background_fact | 15 |
| definition | 12 |
| assumption | 5 |
| prior_work | 2 |

Distribution by paper section (rough): Section 5 (event generation): 46;
Section 4 (jet tagging): 29; Section 3 (amplitude regression): 21; Section 2
total (architecture): ~73; Introduction: 9; Abstract: 4; Section 6 (Outlook):
14. Coverage is biased toward methods/results in the three application
sections, as expected.

## Literature coverage (post-fixer)

- Bank pass: `literature_bank/` exists but its PDFs were unreadable in this
  run (`pdftoppm` not installed on host). The searcher logged the fallback
  and proceeded with external search — per methodology this is not a phase
  failure.
- External pass: 35 WebSearch calls, every cited record verified against
  arXiv abstract or journal DOI.
- **Self-citation removed (round 1, F-004).** `spinner2024lgatr`
  (arXiv:2405.14806) is the paper under review itself; the round-1 fixer
  removed it from every `supports` relation. The bib entry remains in
  `references.bib` annotated as a self-citation, but it is no longer cited
  in `LITERATURE.md`.
- **Claims with ≥1 independent external candidate: 88 / 200**.
- **Claims marked UNCOVERED: 112 / 200** — these are claims for which the
  only candidate produced this round was the self-cite. They are an honest
  signal that no independent external evidence was retrieved, not a search
  failure.
- 35 BibTeX entries in `references.bib`; 34 cited in `LITERATURE.md`; the
  one unused entry is `spinner2024lgatr`, intentionally retained with a
  `note = {self-citation; paper under review}`. No fabricated keys; no
  unresolvable cites.
- 3 external entries are flagged `preprint: true`
  (`hendrycks2016gelu`, `wu2024mipart`, `plehn2022modern`).

## Graph (post-fixer)

- `graph.v1.skeleton.json`: 20 groups (G001–G020), 200 claims, **0 edges**
  (skeleton is claim-only by design), validates against
  `src/conventions/graph_schema.json`.
- `graph.v1.json`: 20 groups, 200 claims, **20 edges** added by the round-1
  fixer to address F-008 — `depends_on` edges anchoring architecture/method
  claims to spacetime-algebra definitions, and `supports` edges from
  per-task numerical results to abstract-level headline claims. Validates
  against `src/conventions/graph_schema.json`.
- Group titles and captions rewritten by the fixer (F-005, F-006) — every
  group now has a 2–3 word noun-phrase title and an original ≤25-word
  caption summarizing the group's collective assertion.
- `dominant_type` re-audited (F-007); 0 mismatches across all 20 groups.
- All claim verdicts are `NOT_CHECKED`; node colors are gray accordingly.

## Gaps and notes for the round-2 reviewer

- **High UNCOVERED count is intentional.** 112 of 200 claims now lack any
  external citation because their only Pass-2 hit was the self-citation.
  Phase-2 `checker_unreferenced` will likely flag many of these; this is
  the expected, honest outcome. If the project wants better external
  coverage, run the bank-first pass on a host with `pdftoppm` installed and
  expand the `literature_bank/` for L-GATr-relevant priors (jet tagging,
  amplitude regression, equivariant networks, generative LHC ML).
- **Edge set is a starter set, not exhaustive.** The 20 added edges
  (F-008) anchor the most explicit `depends_on` and `supports` chains
  visible in the paper text. A future pass could add more, particularly
  within Section 5 (event generation) where multiple result/interpretation
  chains were not yet wired up.
- **Bank still unusable on this host.** `pdftoppm` (poppler-utils) was
  unavailable; bank-first pass remains a no-op. Installing `poppler-utils`
  would flip future runs to bank-first as designed.
- **Source PDF marked `_corrupted`.** Filename signals intentional
  corruption/annotations. The extracted `paper.txt` (2425 lines) has no
  obvious OCR damage and the extractor `log.md` records no aborted
  sentences. Phase-2 checkers should still be alert for subtle textual
  edits faithfully reproduced into claim provenance.
- **Hedged=0 for all 200 claims.** The taxonomy's strict reading rejects
  modal language without explicit weakening markers; the constructive
  reviewer may reasonably re-flag this as overly literal in Phase 2.
  Recorded as a Phase-1 stylistic note, not a blocker.
- **`log.md` for the round-1 fixer is orchestrator-reconstructed.** The
  fixer was rate-limited mid-task after writing all the artifact edits;
  the orchestrator wrote `reviews/easy/phase1/agents/fixer/round_1/log.md`
  by diffing the artifacts. The round-2 reviewer may flag this as a
  process note (not a Category A finding); a fresh fixer can re-emit a
  native log if preferred.

## Round-1 fixer outcome (pointer)

The round-1 fixer addressed:

- F-002 (A): C172 provenance — resolved.
- F-001, F-003 (B): C004 paraphrase + off-by-one provenance for
  C001/C002/C007/C008/C009 — resolved.
- F-004 (B): `spinner2024lgatr` self-citation — resolved.
- F-005, F-006, F-007, F-008 (B): group titles, captions, dominant_type,
  empty edges — resolved.

Category-C findings (F-009 `related` relation type, F-010 schema ambiguity,
F-011 `hestenes1966` DOI, F-012 hedged Phase-2 follow-up flag) were
recorded in round 1 ARBITRATION.md and not addressed; they are non-blocking
under the methodology's A/B/C rules. The round-2 reviewer may surface them
again or accept.

## File pointers

- Paper: `reviews/easy/paper/paper.txt`, `reviews/easy/paper/paper.pdf`
- Claims: `reviews/easy/phase1/outputs/CLAIMS.md` (200 rows)
- Literature: `reviews/easy/phase1/outputs/LITERATURE.md`,
  `reviews/easy/phase1/outputs/references.bib` (35 entries; 34 cited)
- Graphs: `reviews/easy/phase1/outputs/graph.v1.skeleton.json` (0 edges),
  `reviews/easy/phase1/outputs/graph.v1.json` (20 edges)
- Subagent working dirs (plans + logs):
  `reviews/easy/phase1/agents/{claim_extractor,literature_searcher,graph_builder_skeleton,graph_builder,fixer}/`
- Round-1 review: `reviews/easy/phase1/review/critical.md`,
  `reviews/easy/phase1/review/ARBITRATION.md`
