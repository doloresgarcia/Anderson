# Literature Searcher — Plan (phase 1, test-1)

Paper: "A Lorentz-Equivariant Transformer for All of the LHC" — Brehmer,
Bresó, de Haan, Plehn, Qu, Spinner, Thaler.

## Search policy by claim type

- **prior_work** — the citation is named in the sentence; the search target is
  the cited record itself. These get the highest priority. We must resolve
  every named bibtex key (`Spinner:2024hjm`, `Heimel:2018mkt`, `Qu:2022mxj`,
  `ATLAS:2020ccu`, `deOliveira:2015xxd`, `Kasieczka:2017nvn`, `Butter:2017cot`,
  `Butter:2022rso`, `Campbell:2022qmc`, `brehmer2023geometric`, `vaswani2017attention`,
  `xiong2020layer`, `Gong:2022lye`, `Bogatskiy:2022czk`, `ruhe2023clifford`,
  `zaheer2017deep`, `chen2023symbolic`, `Alwall:2014hca`, `Sjostrand:2014zea`,
  `delphes`, `Alwall:2011uj`, `deFavereau:2013fsa`, `Plehn:2022ftl`,
  `Butter:2023fov`, `Kasieczka:2019dbj`, `Nachman:2022emq`).
- **method** — most are internal architecture / hyperparameter / training
  choices. Where a method invokes a named external technique (FlashAttention,
  Lion optimizer, GELU, MadGraph, Pythia, Delphes, FastJet, GATr, ParT, MIParT,
  CGENN, Deep Sets, conditional flow matching, transformer attention) we cite
  the reference paper. Pure internal-numerics methods get no candidates.
- **result** — most results are internal to this paper; we cite external
  references only when the comparison is to a named baseline (ParT, MIParT,
  DSI, CGENN, Spinner:2024hjm).
- **background_fact** — cite the standard reference if one exists (Lorentz
  equivariance benchmarks, GAN detector simulation, GA primer, gamma matrices /
  Dirac algebra textbook), otherwise leave empty.
- **definition** — definitional / textbook content; cite a canonical reference
  (geometric algebra textbook, CFM original) where applicable.
- **assumption / interpretation** — usually no external lit; left empty.

## Backends

- arXiv search (`arxiv.org/a` + Inspire-HEP) via WebFetch / WebSearch
- Inspire-HEP (`inspirehep.net/literature`) via WebFetch — for HEP citation
  keys with the `Author:YYYYabcd` format
- Google Scholar / direct WebSearch for ML / generic CS papers

## Batching

Group searches by named-citation cluster. Most named bibkeys appear in several
claims; resolve each unique key once, then attach it to all claims that quote
it.

## Risk: fabrication

Hard rule: every emitted bibkey must be backed by an actual fetched record
with arXiv ID / DOI / Inspire ID. If a search comes up empty I drop the
candidate rather than guess. Empty entries are recorded in log.md.

## Output structure

- `LITERATURE.md` — one `## Cxxx` heading per claim ID (all 217), with at
  most 5 ranked candidates, or empty under heading.
- `references.bib` — one entry per unique cited bibkey, each with arXiv
  ID / DOI / URL. Keys reuse the paper's own naming where present so the
  graph_builder downstream can cross-reference.
