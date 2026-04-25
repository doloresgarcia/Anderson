# literature_searcher — plan.md
# Paper: "A Lorentz-Equivariant Transformer for All of the LHC" (L-GATr)
# Review slug: noah-test-v1

## Claim clustering

After reading claims.jsonl (499 rows), I identified the following prose-claim clusters
that require literature coverage:

| Cluster | Description | Representative claim IDs |
|---------|-------------|--------------------------|
| A | L-GATr architecture: geometric algebra, multivectors, Lorentz equivariance | 0004–0008, 0043–0145 |
| B | GATr (E(3) predecessor) | 0030, 0108, 0134 |
| C | Competitor Lorentz-equivariant networks (LorentzNet, PELICAN, CGENN, LGAE) | 0023, 0160, 0163 |
| D | Amplitude regression: Z+ng processes, MadGraph, surrogate models | 0172–0201 |
| E | Top tagging / jet classification datasets and benchmarks | 0022, 0219–0243 |
| F | ParT / JetClass / MIParT | 0239–0243 |
| G | Event generation: CFM, ttbar+jets | 0278–0395 |
| H | LHC ML program overview / generative AI at LHC | 0009, 0025–0027 |
| I | Transformer / attention foundational references | 0109 |
| J | Conditional flow matching methodology | 0354–0395 |

## Pass 1 strategy (bank)

Search all 98 PDFs in literature_bank/ exhaustively.
Tag each with arXiv ID from filename. Read first 2 pages to identify title/authors.
For each cluster, record which bank papers support/contradict/relate.

Bank PDFs cover: arXiv IDs from 1411.0665 (2016) through 2509.22059 (2025).

## Pass 2 strategy (external)

For claims not covered at high/medium confidence by the bank, run targeted
WebSearch queries on arxiv.org. Prefer published peer-reviewed versions.

Key external targets:
- LorentzNet (arXiv:2201.08187, Gong et al., JHEP 2022)
- PELICAN (arXiv:2211.00454, Bogatskiy et al.)
- CGENN (arXiv:2305.11141, Ruhe et al., NeurIPS 2023)
- ParT/JetClass (arXiv:2202.03772, Qu et al., ICML 2022)
- GATr (arXiv:2305.18415, Brehmer et al., NeurIPS 2023)
- MIParT (arXiv:2407.08682)
- Top tagging benchmark (arXiv:1902.09914, Kasieczka et al.)
- Kasieczka dataset (zenodo:2603256)
- Flow Matching (arXiv:2210.02747, Lipman et al.)
- Lorentz group NN (arXiv:2006.04780, Bogatskiy et al., ICML 2020)
- EPiC-FM (arXiv:2310.00049)

## Output plan

- LITERATURE.md: per-claim coverage table, ≤5 candidates per claim cluster
- references.bib: BibTeX for every key cited in LITERATURE.md
- Every key corresponds to a bank paper or an actually-retrieved external result
