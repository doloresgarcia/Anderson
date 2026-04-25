# Literature Searcher — Log

## Inputs read

- `phase1/outputs/CLAIMS.md` (217 claims, C001–C217)
- `paper/paper.meta.json`
- `paper/paper.txt` (for disambiguation only)

## Backends used

- Inspire-HEP API/web (texkey lookups for HEP citations)
- arXiv (direct abs page fetch for confirmation)
- Zenodo (top tagging dataset DOI)
- General WebSearch (fallback for ML / Snowmass references)

## Procedure

1. Extracted the set of bibtex keys actually used in the paper body
   (`paper.txt`) via `\cite[...]{...}` regex. Result: 39 unique keys spanning
   prior_work, method (FlashAttention, GELU, optimizers, MadGraph, Pythia,
   Delphes, transformer ML papers), and background_fact.
2. Resolved each key one-by-one via Inspire-HEP texkey lookup or direct arXiv
   abs page. Cross-checked with the public bbl of arXiv:2411.00446 (the L-GATr
   paper itself) and arXiv:2405.14806 (Spinner:2024hjm, predecessor) to
   identify ambiguous keys (e.g. ATLAS:2020ccu = arXiv:2006.09274, JHEP 01
   (2021) 033 — the all-hadronic ttbar differential cross-section paper).
3. For every confirmed key, fetched at least one record (arXiv abs, Inspire
   API, Zenodo) and entered it in `references.bib` with arXiv ID and DOI/URL.
4. Authored `LITERATURE.md` with one heading per claim, attaching only
   confirmed bibkeys and verbatim short snippets (paper or abstract titles
   are quoted; ≤ 30 words each).

## No-search claims

The following claims were intentionally not searched because they describe
internal architecture, hyperparameters, dataset splits, or numerical
details that have no external comparator:

- C049, C054, C055, C061, C078–C082, C089, C090 (architecture sizing /
  H100 throughput / FlashAttention details — Flash entry attached to C090
  only because it is named there).
- C096, C098, C106–C108 (training-set sizes and MSE setup specific to this
  paper).
- C112, C118–C121, C127, C128, C130, C134–C136 (this paper's training
  and pre-training procedure; verified internally in phase 2).
- C139, C140, C142, C144, C149, C150–C171 (CFM implementation details and
  reference-multivector bookkeeping specific to this paper).
- C172–C189 (results and interpretation specific to this paper; checked
  internally in phase 2).
- C191–C217 except where a named external technique appears (Lion optimizer
  → C198, Adam → C215, Deep Sets → C190, ParT preprocessing → C205).

These are listed as "no-search" rather than "no-results" — the search policy
is to not waste effort on internal-method claims that phase 2 will check by
internal consistency.

## No-result claims (search ran, no relevant candidate)

Tier-2 background_fact claims about geometric algebra basics
(C016–C020, C022, C026–C030 etc.) intentionally have no candidate: this is
textbook GA material rather than something to attribute to a specific paper.
The paper itself uses Hestenes 1966 internally (`hestenes1966space`) for
similar context but it is not actually `\cite`d in any of the 217 extracted
sentences, so I did not add it to `LITERATURE.md` (would have been
fabrication-by-extension).

C036 (uniqueness claim) and C044 (universal-approximation claim) reference
results that are stated but not externally cited; I attached
`brehmer2023geometric` and `ruhe2023clifford` as related candidates (medium
confidence) since they discuss expressivity of geometric-algebra equivariant
networks, but neither flatly supports the wording in the paper. Phase 2
verifier should treat these as INCONCLUSIVE candidates.

## Possibly-contradicting prior work

None observed. The cited reference set is composed of either (a) prior work
named explicitly by the authors, or (b) standard ML / generator tools the
paper uses. No retrieved record disagrees with any extracted claim.

## Counts

- Claim headings written: 217 (one per claim)
- Claims with ≥1 candidate: 73
- Claims with zero candidates: 144
  - of which "no-search" (internal-method by policy): ~110
  - of which "no-results" (search ran, nothing relevant): ~34, mostly
    background_fact textbook content and pure interpretation
- Unique bibtex entries in `references.bib`: 45

The 45 bib entries cover: every external citation that appears in
`paper.txt` (39 keys) plus 6 supporting ML / utility references
(`hendrycks2016gaussian`, `dao2022flashattention`, `lipman2023flowmatching`,
`Cacciari:2008gp`, `Cacciari:2011ma`) that are referenced in the paper's
own `.bib` and used in claim-attribution snippets here. Every key emitted
in `LITERATURE.md` is present in `references.bib`; cross-check passed.

## Hard-rule confirmation

- No fabricated arXiv IDs / DOIs: each entry was retrieved live from
  arXiv abs pages or Inspire-HEP API and the ID was the one returned by the
  service.
- For ATLAS:2020ccu (the only key the Inspire texkey API did not directly
  resolve), I disambiguated by reading the bbl of the precursor paper
  (2405.14806) and then fetched arXiv:2006.09274 directly to confirm title,
  journal, and DOI before adding the entry.
