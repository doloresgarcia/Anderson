## literature_collision

### claim-0384 — INCONCLUSIVE — confidence: low
- reason: The paper cites `lipman2023flowmatchinggenerativemodeling` and `albergo2023stochastic` for the linear interpolation CFM training procedure. Neither key appears in references.bib (only `lipman2022flow` arXiv:2210.02747 is present). The description is almost certainly consistent with lipman2022flow, but since the exact cited keys are absent from references.bib, formal verification is not possible.

### claim-0522 — INCONCLUSIVE — confidence: low
- reason: The paper cites `chen2023symbolic` for the Lion optimizer characterization in the appendix. This key is absent from references.bib. Cannot verify the description against the actual cited document.

### claim-0023 — CLEAR — confidence: high
- reasoning: Cited keys Gong:2022lye, Bogatskiy:2022czk, ruhe2023clifford, Hao:2022xuv, Bogatskiy:2020tje all resolve in references.bib; LITERATURE.md descriptions of LorentzNet, PELICAN, CGENN, and related equivariant networks are consistent with what those bib entries describe.

### claim-0030 — CLEAR — confidence: high
- reasoning: Cited keys brehmer2023geometric and de2023euclidean both resolve in references.bib; LITERATURE.md description of the GATr architecture as equivariant under E(3) using geometric algebra is consistent with the bib entries.

### claim-0109 — CLEAR — confidence: high
- reasoning: Cited keys Spinner:2024hjm, brehmer2023geometric, vaswani2017attention, xiong2020layer, Bahl:2024meb, Bahl:2024sib all resolve in references.bib; LITERATURE.md descriptions of L-GATr transformer blocks with attention and layer normalization are consistent with those entries.

### claim-0160 — CLEAR — confidence: high
- reasoning: Cited keys Gong:2022lye, Bogatskiy:2022czk, ruhe2023clifford, Hao:2022xuv, Bogatskiy:2020tje all resolve in references.bib; LITERATURE.md descriptions of equivariant network baselines are consistent with the bib entries.

### claim-0201 — CLEAR — confidence: high
- reasoning: Cited keys Spinner:2024hjm and Bahl:2024meb both resolve in references.bib; LITERATURE.md descriptions of L-GATr amplitude regression are consistent with those entries.

### claim-0288 — CLEAR — confidence: high
- reasoning: Cited key Gong:2022lye resolves in references.bib; LITERATURE.md description of LorentzNet as an equivariant graph network using Minkowski dot product attention is consistent with the bib entry.

### claim-0289 — INCONCLUSIVE — confidence: low
- reasoning: The paper cites Bogatskiy:2023nnw at lines 476 and 494 for PELICAN, but references.bib contains only Bogatskiy:2022czk. The cite-key mismatch means the exact cited source cannot be located; formal verification of the PELICAN description against the cited document is not possible.

### claim-0290 — CLEAR — confidence: high
- reasoning: Cited key ruhe2023clifford resolves in references.bib; LITERATURE.md description of CGENN as an equivariant graph network operating on multivectors (Clifford group equivariant) is consistent with the bib entry.

### claim-0291 — CLEAR — confidence: high
- reasoning: Cited key Qu:2022mxj resolves in references.bib; LITERATURE.md description of ParT as a transformer with pairwise interaction features as attention bias is consistent with the bib entry.

### claim-0292 — INCONCLUSIVE — confidence: low
- reasoning: The paper cites Wu:2024thh for MIParT but this key is absent from references.bib (only He:2024eiw, covering a different MIParT entry, is present). Cannot formally verify the MIParT description against the cited source.

### claim-0341 — CLEAR — confidence: high
- reasoning: Claim has no cite_keys and no literature entries in LITERATURE.md; there are no cited sources to resolve or collide with, so no literature collision is possible.

### claim-0355 — CLEAR — confidence: high
- reasoning: Cited keys Spinner:2024hjm, Buhmann:2023pmh, Birk:2023ind, Butter:2023fov, Buhmann:2023kdg, Leigh:2023doe, lipman2022flow all resolve in references.bib; LITERATURE.md descriptions of flow matching and generative network baselines are consistent with those entries.

### claim-0395 — CLEAR — confidence: high
- reasoning: Cited keys Spinner:2024hjm, Buhmann:2023pmh, Birk:2023ind, Butter:2023fov, Buhmann:2023kdg, Leigh:2023doe all resolve in references.bib; LITERATURE.md descriptions of event generation baselines are consistent with those entries.

All other claims with literature entries: CLEAR.

Key notes:
- No genuine literature collision detected across all 52 claims with literature entries.
- Benchmark numbers for ParT (AUC 0.9877) and MIParT (AUC 0.9878) in Tables 3 and 4 are consistent with the published results in LITERATURE.md.
- "First Lorentz-equivariant generative network" (claim-0007): companion paper Spinner:2024hjm makes the same claim with "to the best of our knowledge." Flat assertion in this paper is a potential unreferenced/ambiguous issue, not a literature collision.
- LorentzNet, PELICAN, CGENN, ParT descriptions accurately characterize those architectures per available literature snippets.
- JetClass dataset description (100M jets, 10 classes) is accurate per Qu:2022mxj.
- Cite-key mismatch: paper uses `Bogatskiy:2023nnw` at lines 476, 494 but references.bib contains `Bogatskiy:2022czk`. Bibliography management gap, not a literature collision.
- GATr scalar-gated activation (claim-0134): confirmed by Spinner:2024hjm bank PDF.
