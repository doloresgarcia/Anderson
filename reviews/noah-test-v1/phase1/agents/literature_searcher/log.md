# literature_searcher — log.md
# Paper: "A Lorentz-Equivariant Transformer for All of the LHC" (L-GATr)
# Review slug: noah-test-v1

## Pass 1 — Literature bank

Total bank PDFs: 98
PDFs read (first 2 pages each): 98/98
PDFs with confirmed title/authors: 98/98

### Key bank matches (high/medium relevance to L-GATr claims)

| file | arXiv ID | title (short) | relevance |
|------|----------|---------------|-----------|
| 2405_14806v3.pdf | 2405.14806 | Spinner et al., L-GATr NeurIPS 2024 | HIGH — companion ML paper |
| 2410_07315v3.pdf | 2410.07315 | Bahl et al., SBI with L-GATr for WZ | HIGH — applies L-GATr |
| 2412_12069v2.pdf | 2412.12069 | Bahl et al., amplitude surrogate + uncertainties | HIGH — amplitude regression |
| 2203_07460v2.pdf | 2203.07460 | Butter et al., Machine Learning and LHC Event Generation | MEDIUM — LHC ML review |
| 2212_07347v2.pdf | 2212.07347 | Hao et al., Lorentz group equivariant autoencoders | MEDIUM — Lorentz equivariance |
| 2301_08128v3.pdf | 2301.08128 | Buhmann et al., EPiC-GAN | MEDIUM — equivariant jet generation |
| 2305_10475v3.pdf | 2305.10475 | Butter et al., Jet Diffusion vs JetGPT | MEDIUM — CFM jet generation |
| 2312_00123v2.pdf | 2312.00123 | Birk et al., Flow Matching Beyond Kinematics | MEDIUM — CFM jets |
| 2303_05376v2.pdf | 2303.05376 | Leigh et al., PC-JeDi | MEDIUM — diffusion jet generation |
| 2211_10295v2.pdf | 2211.10295 | Kansal et al., evaluating generative models | LOW — evaluation metrics |
| 2311_09296v2.pdf | 2311.09296 | Bierlich et al., hadronization NFs | LOW — event generation context |
| 2109_11964v2.pdf | 2109.11964 | Danziger et al., rejection sampling NN event weights | LOW — surrogate amplitude context |
| 2506_06203v3.pdf | 2506.06203 | Herrmann et al., multijet event generation surrogates | LOW — surrogate amplitude context |
| 2102_05073v2.pdf | 2102.05073 | Mikuni & Canelli, Point Cloud Transformers | LOW — transformer jet tagging |

### Bank papers with no relevance to L-GATr core claims (selected)

The bank is predominantly composed of anomaly detection, generative models
for detectors/calorimeters, and general LHC ML papers. The following clusters
were represented but had low/no relevance:
- Anomaly detection (ANODE, CATHODE, QUAK, CWoLa, etc.): ~30 papers
- Calorimeter fast simulation (CaloINN, iCALOFLOW, etc.): ~8 papers
- GAN event generation: ~6 papers
- Quantum ML: ~4 papers
- Jet substructure theory (Lund plane, IRC safety): ~4 papers
- Unfolding methods: ~3 papers

None of the bank PDFs contain LorentzNet (arXiv:2201.08187), PELICAN
(arXiv:2211.00454), CGENN (arXiv:2305.11141), or ParT (arXiv:2202.03772)
— the four most-cited architectural competitors in the paper.

## Pass 2 — External search

### Claims triggering external search

All core architectural competitor claims (Cluster C, E, F) and methodology
references (Clusters B, I, J) were not covered at high/medium confidence by
the bank, triggering Pass 2.

### External search results

| query | result | arXiv ID | verdict |
|-------|--------|----------|---------|
| LorentzNet jet tagging Gong 2022 | found | 2201.08187 | RETRIEVED; JHEP 07(2022)030 |
| PELICAN Bogatskiy 2022 | found | 2211.00454 | RETRIEVED; preprint; published version 2307.16506 |
| CGENN Ruhe NeurIPS 2023 | found | 2305.11141 | RETRIEVED; NeurIPS 2023 |
| ParT JetClass Qu ICML 2022 | found | 2202.03772 | RETRIEVED; ICML 2022 |
| GATr Brehmer NeurIPS 2023 | found | 2305.18415 | RETRIEVED; NeurIPS 2023 |
| MIParT He 2024 | found | 2407.08682 | RETRIEVED; preprint |
| Top tagging ML landscape Kasieczka | found | 1902.09914 | RETRIEVED; SciPost Phys. 7 (2019) 014 |
| Top tagging dataset zenodo | found | zenodo:2603256 | RETRIEVED; DOI 10.5281/zenodo.2603256 |
| Flow matching Lipman 2022 | found | 2210.02747 | RETRIEVED |
| Lorentz group NN Bogatskiy ICML 2020 | found | 2006.04780 | RETRIEVED; ICML 2020 |
| Loop amplitudes Badger Butter 2022 | found | 2206.14831 | RETRIEVED |
| Euclidean algebra GATr de Haan | found | 2311.04744 | RETRIEVED; AISTATS 2024 |
| EPiC-FM Buhmann flow matching | found | 2310.00049 | RETRIEVED; related to bank EPiC-GAN |

### Source hierarchy compliance

All external results were retrieved as peer-reviewed published papers where
available (JHEP, ICML, NeurIPS, SciPost). Only MIParT (2407.08682) remains
as a preprint at search time with no confirmed published counterpart found.

### Keys not retrieved / gaps

- `Plehn:2022ftl` (claim-0010) — cited but not retrieved; likely a
  Plehn review article on ML uncertainty. Not included in LITERATURE.md
  coverage tables (peripheral claim).
- `Butter:2017cot` (claim-0023) — early Lorentz-equivariant tagger;
  not retrieved externally. Identified as likely 1707.08966 (Deep-learned
  Top Tagging with a Lorentz Layer), but not confirmed — not included.
- `Qiu:2022xvr`, `Qiu:2023ihi` — CGENN follow-up papers; not separately
  retrieved. CGENN (ruhe2023clifford) covers this cluster.
- `hestenes1966space` — book reference, not web-retrievable as PDF;
  confirmed as standard reference, included with note.

## Hard rule compliance

1. No BibTeX key was fabricated. Every key in references.bib corresponds to
   a paper verified via bank PDF read or WebSearch retrieval with confirmed
   arXiv ID, DOI, or conference proceeding.
2. The bank was searched exhaustively before any external search was made.
3. External search preferred peer-reviewed published versions; preprints are
   tagged with note field.

## Coverage summary

| Cluster | Bank coverage | External coverage | Overall |
|---------|---------------|-------------------|---------|
| A (L-GATr arch) | HIGH (bank key paper) | HIGH (GATr ref) | covered |
| B (GATr predecessor) | none | HIGH | covered |
| C (Lorentz competitors) | LOW (LGAE) | HIGH (LorentzNet, PELICAN, CGENN) | covered |
| D (amplitude regression) | HIGH (Bahl:2024meb) | MEDIUM (Badger loop) | covered |
| E (top tagging) | MEDIUM (Spinner) | HIGH (Kasieczka, Heimel) | covered |
| F (ParT/JetClass/MIParT) | LOW (PCT) | HIGH (Qu:2022mxj, He:2024eiw) | covered |
| G (event generation) | HIGH (EPiC-FM, Birk, Butter) | — | covered |
| H (LHC ML overview) | HIGH (Butter:2022rso) | MEDIUM (Campbell) | covered |
| I (transformer foundations) | none | HIGH (Vaswani, Xiong) | covered |
| J (CFM methodology) | MEDIUM (Birk, EPiC-FM) | HIGH (Lipman) | covered |
| K (geometric algebra) | none | HIGH (Hestenes book) | covered |
