## unreferenced

### C001 — CLEAR — confidence: high
- evidence: paper.txt:16-17 — Supported by Table 2 (top tagging), Table 4 (JetClass), and Fig. 7 (event generation) in paper.txt.

### C002 — CLEAR — confidence: high
- reasoning: L-GATr represents data in G_{1,3} and is equivariant under Lorentz transformations by architectural construction. This is the paper's own self-describing architectural claim; no external citation is required for a self-describing architectural property. CLEAR as novel contribution.

### C004 — CLEAR — confidence: high
- evidence: paper.txt:22-23 — Supported by Tables 2, 4, and Fig. 7 in paper.txt showing results for all three LHC tasks.

### C007 — FLAGGED — confidence: high

- evidence: paper.txt:79–80
- reasoning: Claims that standard architectures do not capture amplitudes at the per-mille level. This quantitative threshold is asserted as a field fact but presented without citation. LITERATURE.md marks C007 as COVERED only weakly by [@aylett2021diphoton] with "related" confidence, which addresses the "challenge of reaching high precision" but does not directly support the specific per-mille-level threshold. A citation to a published benchmark or prior result establishing this precision limitation is needed.

### C029 — CLEAR — confidence: high
- evidence: paper.txt:232-240 — Novel representation choice (xS = PID, xV_µ = pµ) for encoding particles as multivectors; this is the paper's own design decision and does not require an external citation. CLEAR as self-describing architectural/methodological contribution.

### C031 — CLEAR — confidence: high
- evidence: paper.txt:242-248 — The decomposition |M|² = |ME|² + |MO|² + 2Re(M*_E M_O) is elementary complex algebra applied to M = ME + MO; standard identity requiring no external citation. CLEAR as established mathematical identity.

### C036 — CLEAR — confidence: high
- evidence: paper.txt:303-304 — The limitation that G_{1,3} cannot represent symmetric rank-2 tensors is stated as an acknowledged design constraint of the geometric algebra approach; it is a known result of Clifford algebra representation theory (confirmed by checker_domain). The paper presents this as a limitation, not a novel discovery, and the absence of a citation is acceptable for a well-known algebraic fact. CLEAR.

### C041 — CLEAR — confidence: high
- evidence: paper.txt:371-390 — The "most general linear combination" completeness claim follows from Schur's lemma applied to the grade-irrep structure of G_{1,3} (confirmed by checker_domain). This is a standard representation-theory result and the paper's linear layer construction is a novel application of it. A supporting citation to a group-theory textbook would strengthen the claim, but the claim is self-contained given the surrounding derivation. CLEAR as novel architectural contribution grounded in standard representation theory.

### C054 — CLEAR — confidence: high
- evidence: paper.txt:515-516 — The claim that performance "can degrade significantly" if partial symmetry breaking is not accounted for is the paper's own design motivation, substantiated by the ablation in Table 3 (paper.txt:913-1002) and Table 7. The claim is hedged ("can degrade") and the ablation data provides the supporting evidence within the paper. No external citation strictly required for this design-observation claim. CLEAR.

### C060 — FLAGGED — confidence: medium

- evidence: paper.txt:531–532
- reasoning: Comparative performance claim asserting that "enforcing symmetry then breaking it with reference vectors produces better results than completely removing symmetry." Marked UNCOVERED in LITERATURE.md. The claim is presented without citation in the surrounding context. While the paper provides ablation studies later (Tables 3, 5), they are not referenced adjacent to the claim, leaving this assertion temporarily unsupported.

### C070 — FLAGGED — confidence: medium

- evidence: paper.txt:555–556
- reasoning: Claims that "symmetry breaking is crucial...and has a strong impact on performance" using unquantified superlatives. Marked UNCOVERED in LITERATURE.md. While ablation tables (3, 7) exist nearby, they are not cited in this sentence. The words "crucial" and "strong impact" require supporting evidence in adjacent context.

### C094 — FLAGGED — confidence: high

- evidence: paper.txt:613–614
- reasoning: Claims that "L-GATr guarantees the exact Lorentz invariance of the amplitude." This is a formal mathematical assertion about the output's properties, marking it as a Lorentz scalar. Marked UNCOVERED in LITERATURE.md. The claim is stated without proof or reference to equivariance theory. While Section 2 claims layer-wise equivariance, the logical chain to scalar invariance of the amplitude output is not explicitly made in or near the claim.

### C100 — CLEAR — confidence: high
- evidence: paper.txt:747-751 — Supported by Fig. 2 (left panel) showing transformer and graph network scaling with multiplicity.

### C101 — CLEAR — confidence: high
- evidence: paper.txt:749-751 — Supported by Fig. 2 (left panel) showing L-GATr vs. DSI performance across gluon multiplicities.

### C104 — CLEAR — confidence: high
- evidence: paper.txt:757-758 — Supported by Fig. 2 (right panel) showing L-GATr as top performer across all training-data regimes.

### C112 — CLEAR — confidence: high
- evidence: paper.txt:772-773 — Supported by Table 2 (top tagging results) and Table 4 (JetClass results) at paper.txt:803-912 and 1044-1106.

### C117 — CLEAR — confidence: high
- evidence: paper.txt:1003-1004 — Supported by Table 2 at paper.txt:803-912 showing L-GATr AUC 0.9870 ± 0.0001 matching PELICAN and CGENN.

### C129 — CLEAR — confidence: high
- evidence: paper.txt:1036-1038 — Supported by Table 4 at paper.txt:1044-1106 showing L-GATr AUC 0.9885 vs. ParT 0.9877 and MIParT 0.9878 across all ten signal classes.

### C131 — CLEAR — confidence: high
- evidence: paper.txt:1111-1112 — Supported by Fig. 4 (left panel) and Table 5 showing L-GATr AUC 0.9875 at 10M jets (10% of 100M) near ParT/MIParT at 100M jets.

### C138 — CLEAR — confidence: high
- evidence: paper.txt:1339-1340 — Supported by Table 2 (fine-tuning rows) at paper.txt:878-912 showing L-GATr-f.t. matching or exceeding ParT-f.t. and MIParT-f.t. across all metrics.

### C142 — FLAGGED — confidence: medium

- evidence: paper.txt:1346–1347
- reasoning: Claims that "per-mille-level (or percent-level) accuracy on phase space density should be reached for event generation." This sets quantitative benchmarks without citation. LITERATURE.md marks C142 UNCOVERED; [@butter2019howtoganevents] is only "related," not directly supporting the specific numeric thresholds.

### C157 — CLEAR — confidence: high
- evidence: paper.txt:1421-1422 — Claim has a citation [77] (butter2023jetdiffusion); citation content does not support the claim — see literature_collision section for the FLAGGED verdict.

### C162 — FLAGGED — confidence: high

- evidence: paper.txt:1432–1433
- reasoning: Claims that "it is not possible to construct a normalized density invariant under a non-compact group." This is a domain-level mathematical fact about non-compact Lorentz group and measure theory. Marked UNCOVERED in LITERATURE.md. The statement stands without citation or reference to a mathematical foundation.

### C180 — CLEAR — confidence: high
- evidence: paper.txt:1649-1651 — Supported by Fig. 6 showing 1-dimensional distributions from different generators; L-GATr visibly outperforms baselines across shown distributions.

### C181 — CLEAR — confidence: high
- evidence: paper.txt:1650-1651 — Supported by Fig. 6 showing angular correlation distributions with percent-level precision for L-GATr.

### C183 — CLEAR — confidence: high
- evidence: paper.txt:1660-1661 — Supported by Fig. 7 scaling results (NLL and AUC vs. training data and particle multiplicity). Note: this claim also carries a FLAGGED internal_contradiction verdict; see internal_contradiction section.

### C184 — CLEAR — confidence: high
- evidence: paper.txt:1927-1928 — Supported by Fig. 7 showing L-GATr leading over E(3)-GATr in both NLL and AUC for event generation.

### C185 — CLEAR — confidence: high
- evidence: paper.txt:1928-1929 — Supported by Fig. 7 showing E(3)-GATr only marginally better than plain transformer in NLL/AUC. Note: this claim also carries a FLAGGED internal_contradiction verdict; see internal_contradiction section.

### C191 — FLAGGED — confidence: medium

- evidence: paper.txt:1947–1949
- reasoning: Claims that Lorentz-group representation "enhances performance of essentially every ML-application working on relativistic phase space." The phrase "essentially every" makes an unsupported generalization beyond the paper's three demonstrated applications (amplitude regression, jet tagging, event generation). Marked UNCOVERED in LITERATURE.md. No citations support this broader claim.

### C193 — CLEAR — confidence: high
- evidence: paper.txt:1950-1952 — Supported by Tables 3 and 7 showing reference-multivector configurations outperforming no-reference-multivector baselines.

### C195 — CLEAR — confidence: high
- evidence: paper.txt:1954-1956 — Supported by Fig. 2 (left panel) at paper.txt:718-722 showing L-GATr leading DSI and other baselines for Z+3g and higher multiplicities.

### C197 — CLEAR — confidence: high
- evidence: paper.txt:1957-1958 — Supported by Table 2 (fine-tuning results) at paper.txt:878-912 showing L-GATr-f.t. at or above ParT-f.t. and MIParT-f.t.

### C198 — CLEAR — confidence: high
- evidence: paper.txt:1959-1961 — Supported by Fig. 7 at paper.txt:1858-1925 showing L-GATr CFM outperforming MLP, Transformer, and E(3)-GATr CFM setups across all tt̄+nj multiplicities.
