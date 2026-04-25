## unreferenced

### claim-0004 — FLAGGED — confidence: high
- evidence: paper.txt:53
- reasoning: Claims L-GATr yields "state-of-the-art performance for a wide range of machine learning tasks at the LHC." No inline citation supports this sweeping comparative claim. Needs: comparative performance table or citation to external benchmark.

### claim-0007 — FLAGGED — confidence: high
- evidence: paper.txt:60
- reasoning: Claims L-GATr is "the first Lorentz-equivariant generative network." Priority claim requires a literature survey citation or explicit acknowledgement of prior art to rule out earlier work. No cite_keys present. Needs: citation or explicit prior-art search supporting the priority claim.

### claim-0008 — FLAGGED — confidence: high
- evidence: paper.txt:62
- reasoning: Claims "significant improvements over previous architectures" for all three LHC tasks. No citation; "significant" is undefined. This is a comparative performance claim summarizing results not yet presented at this point in the abstract. Needs: forward reference to results or citation.

### claim-0009 — FLAGGED — confidence: medium
- evidence: paper.txt:79
- reasoning: Broad landscape claim enumerating LHC ML applications (triggering, data acquisition, object identification, anomaly searches, non-perturbative input, theory and detector simulations, simulation-based inference) with no supporting citations. Needs: review citation (e.g., Butter:2022rso or similar).

### claim-0014 — FLAGGED — confidence: medium
- evidence: paper.txt:90
- reasoning: States "standard architectures already capture amplitudes and densities at the per-mille level in most practical scenarios." Specific quantitative threshold claim with no citation. Needs: citation to published amplitude or density regression benchmarks demonstrating per-mille accuracy.

### claim-0018 — FLAGGED — confidence: medium
- evidence: paper.txt:95
- reasoning: Claims that "much of this knowledge is reflected in complex symmetry structures, from the detector geometry to the relativistic phase space, eventually including the underlying theory." General background physics claim asserted without citation. Needs: a review or pedagogical reference.

### claim-0019 — FLAGGED — confidence: medium
- evidence: paper.txt:95
- reasoning: States "Learning the Minkowski metric is a known challenge for all networks working on relativistic phase space." No citation supports this characterization. Needs: citation to equivariant network literature that motivates this challenge.

### claim-0021 — CLEAR — confidence: high
- reasoning: Footnote claim that "equivariant networks are an established subfield of ML." Common knowledge in the ML/HEP community; low-stakes footnote. No citation strictly required.

### claim-0024 — CLEAR — confidence: high
- reasoning: Interpretive framing sentence ("paved the way for a new phase"). No external factual claim. CLEAR.

### claim-0025 — CLEAR — confidence: high
- reasoning: cite_keys present: Butter:2022rso, Campbell:2022qmc, Paganini:2017dwg. Properly cited.

### claim-0026 — CLEAR — confidence: high
- reasoning: cite_keys present: Ghosh:2020kkt, Buhmann:2020pmy, Buhmann:2023kdg, Krause:2024avx. Properly cited.

### claim-0027 — CLEAR — confidence: high
- reasoning: cite_keys present: Otten:2019hhl, Hashemi:2019fkn, Butter:2019cae, Heimel:2022wyj, Ghosh:2022zdz, Bierlich:2023zzd, Janssen:2023lgz. Properly cited.

### claim-0031 — FLAGGED — confidence: high
- evidence: paper.txt:108
- reasoning: Claims L-GATr includes "a maximally expressive linear map." This is a strong architectural novelty claim about expressiveness. No citation is provided, and no proof is offered in the abstract context. Needs: proof reference or citation to expressiveness result.

### claim-0036 — CLEAR — confidence: medium
- reasoning: Forward reference claim about amplitude regression results; the results are presented later in the paper. Paper's own novel result. CLEAR.

### claim-0038 — CLEAR — confidence: medium
- reasoning: Forward reference claim about pre-training benefits. Paper's own novel result. CLEAR.

### claim-0040 — CLEAR — confidence: high
- reasoning: Paper's own experimental finding about event generation performance. No external citation required.

### claim-0043 — FLAGGED — confidence: medium
- evidence: paper.txt:120
- reasoning: Describes geometric algebra as "a mathematical framework that represents certain geometric objects and operations in a unified language" without citation. cite_keys field is empty. The GA literature (Hestenes) should be cited here. Needs: foundational GA reference (e.g., hestenes1966space).

### claim-0044 — CLEAR — confidence: medium
- reasoning: Relative architectural claim about ease of building equivariant layers using GA. No external fact asserted. CLEAR.

### claim-0045 — CLEAR — confidence: medium
- reasoning: Paper's own contribution (reference vector mechanism for subgroup equivariance). CLEAR.

### claim-0047 — CLEAR — confidence: high
- reasoning: cite_keys: hestenes1966space present. Properly cited definition.

### claim-0079 — FLAGGED — confidence: medium
- evidence: paper.txt:190
- reasoning: Claims "the spacetime algebra naturally structures relevant objects like parity-violating transition amplitudes." No citation. This is a non-obvious physical claim about the algebraic structure of amplitudes. Needs: citation to amplitude decomposition in GA or spacetime algebra literature.

### claim-0085 — CLEAR — confidence: medium
- reasoning: Paper's own derivation result (multivector separates scalar/pseudoscalar). Novel result, no citation needed.

### claim-0100 — FLAGGED — confidence: high
- evidence: paper.txt:230
- reasoning: Claims "the spacetime algebra G_{1,3} covers only a limited range of Lorentz tensor representations." No citation. This is a factual algebraic limitation claim. Needs: citation to representation theory literature or GA textbook.

### claim-0101 — FLAGGED — confidence: high
- evidence: paper.txt:230
- reasoning: Claims G_{1,3} "cannot represent symmetric rank-2 tensors." No citation. Verifiable algebraic claim without reference. Needs: citation to GA or representation theory source.

### claim-0104 — CLEAR — confidence: medium
- reasoning: cite_keys: DBLP:journals/corr/abs-2106-06610 present. Properly cited (hedged open question).

### claim-0109 — CLEAR — confidence: high
- reasoning: cite_keys: vaswani2017attention, xiong2020layer present. Properly cited.

### claim-0129 — FLAGGED — confidence: medium
- evidence: paper.txt:283
- reasoning: Novel layer normalization design using absolute value of grade inner products. No external citation for this specific design. However, this is the paper's own architectural contribution, so CLEAR per hard rule.

### claim-0129 — CLEAR — confidence: medium
- reasoning: Reconsidered: this is the paper's own novel architectural design. Hard rule: do not flag novel contributions. CLEAR.

### claim-0132 — FLAGGED — confidence: medium
- evidence: paper.txt:289
- reasoning: Claims "the specific value of ε has a negligible impact on the performance." Empirical claim with no citation and no figure/table reference. Needs: ablation results or table reference within the paper (no reference provided in this claim).

### claim-0146 — FLAGGED — confidence: medium
- evidence: paper.txt:332
- reasoning: Claims "In many LHC contexts, Lorentz symmetry is only partially preserved." No citation. Accurate general statement but asserted without reference. Needs: citation to LHC symmetry-breaking literature or prior equivariant network papers.

### claim-0151 — CLEAR — confidence: high
- reasoning: Paper's own novel contribution (reference multivector mechanism). Hard rule: do not flag. CLEAR.

### claim-0155 — CLEAR — confidence: high
- reasoning: Paper's own experimental finding. Forward reference to results. CLEAR.

### claim-0162 — FLAGGED — confidence: medium
- evidence: paper.txt:339
- reasoning: Claims "the detector setup can compromise the symmetry of the observables with respect to relativistic boosts." No citation. Needs: citation supporting detector-induced symmetry breaking claim.

### claim-0174 — FLAGGED — confidence: medium
- evidence: paper.txt:358
- reasoning: Claims "Resource efficiency is where the two architectures differ most." Comparative assertion about transformers vs GNNs with no citation. Needs: empirical reference or pointer to scaling measurements within the paper (though these are presented later, no explicit forward reference is given).

### claim-0187 — CLEAR — confidence: high
- reasoning: Paper's own experimental measurement (scaling behavior observed in Fig.). CLEAR.

### claim-0189 — CLEAR — confidence: high
- reasoning: Paper's own architectural explanation grounded in shared attention module. CLEAR.

### claim-0191 — FLAGGED — confidence: medium
- evidence: paper.txt:360
- reasoning: Claims "CGENN is slower than L-GATr for few tokens, and the quadratic scaling due to the expensive message passing operation takes off sooner." No citation to CGENN paper for comparison basis. This is a comparison claim against an external system without citing the CGENN paper for the baseline architecture. Needs: citation to ruhe2023clifford is present in other claims but not here.

### claim-0191 — CLEAR — confidence: medium
- reasoning: Reconsidered: claim-0191 appears to be the paper's own empirical measurement comparing architectures. No external citation needed for the paper's own experimental findings. CLEAR.

### claim-0195 — FLAGGED — confidence: high
- evidence: paper.txt:360
- reasoning: Claims use of FlashAttention but provides no cite_key. cite_keys field is empty. FlashAttention is a specific external method and must be cited. Needs: citation to Dao et al. (FlashAttention paper).

### claim-0200 — CLEAR — confidence: high
- reasoning: cite_keys: Maitre:2023dqz present. Properly cited.

### claim-0201 — CLEAR — confidence: high
- reasoning: cite_keys: Aylett-Bullock:2021hmo, Maitre:2021uaa, Badger:2022hwf, Maitre:2023dqz present. Properly cited.

### claim-0202 — FLAGGED — confidence: high
- evidence: paper.txt:381
- reasoning: Claims "standard neural networks struggle to reach sufficient accuracy for a high amount of external particles." No citation. Strong claim about limitations of standard networks for high-multiplicity amplitude regression. Needs: citation to published amplitude regression results showing this limitation.

### claim-0203 — CLEAR — confidence: high
- reasoning: Paper's own architectural contribution (using partial permutation symmetry for scaling). CLEAR.

### claim-0204 — CLEAR — confidence: high
- reasoning: Paper's own architectural claim (exact Lorentz invariance guaranteed by construction). CLEAR.

### claim-0224 — CLEAR — confidence: high
- reasoning: Paper's own experimental finding from Fig. results. CLEAR.

### claim-0225 — CLEAR — confidence: high
- reasoning: Paper's own experimental result. CLEAR.

### claim-0226 — CLEAR — confidence: high
- reasoning: Paper's own experimental result. CLEAR.

### claim-0229 — CLEAR — confidence: high
- reasoning: Paper's own experimental result. CLEAR.

### claim-0230 — FLAGGED — confidence: medium
- evidence: paper.txt:429
- reasoning: Claims "for small training sets, L-GATr and CGENN are very efficient thanks to their equivariant operations." No citation. This is partially a general claim about equivariant architectures (not just L-GATr's own result) that would benefit from a reference. However, the bulk of this is the paper's own experimental observation. CLEAR on reconsideration — the paper's own experimental finding.

### claim-0230 — CLEAR — confidence: medium
- reasoning: Paper's own experimental observation. CLEAR.

### claim-0237 — FLAGGED — confidence: medium
- evidence: paper.txt:440
- reasoning: Claims "Two approaches stand out as top performers: transformer-based architectures and equivariant networks." No citation. Broad comparative claim about the jet tagging literature. Needs: citation to benchmark study or review (e.g., Kasieczka:2019dbj).

### claim-0294 — FLAGGED — confidence: high
- evidence: paper.txt:500
- reasoning: Claims "non-equivariant architectures generally achieve higher accuracy than equivariant ones when sufficient training data is available, as the additional architectural constraints limit the representation capacity." No citation. This is a general architectural claim that goes beyond the paper's own results. Needs: citation to literature supporting this general observation about equivariant vs non-equivariant tradeoffs.

### claim-0295 — FLAGGED — confidence: medium
- evidence: paper.txt:500
- reasoning: Claims "A key ingredient for the optimization of L-GATr is the symmetry breaking prescription." No citation. Architectural claim asserted without reference. This is partly the paper's own contribution, but the broader claim about the necessity of symmetry breaking is unsubstantiated. CLEAR on reconsideration — paper's own contribution.

### claim-0295 — CLEAR — confidence: medium
- reasoning: Paper's own architectural finding. CLEAR.

### claim-0329 — CLEAR — confidence: medium
- reasoning: "JetClass covers a wide variety of jet signatures." Low-importance descriptive claim about dataset covered by adjacent citation. CLEAR.

### claim-0336 — FLAGGED — confidence: high
- evidence: paper.txt:542
- reasoning: Claims "JetClass contains 100M jets equally distributed across 10 classes." No cite_keys in this specific claim. This is an external dataset fact that requires citation to Qu:2022mxj. Needs: citation to JetClass paper (Qu:2022mxj).

### claim-0341 — FLAGGED — confidence: high
- evidence: paper.txt:546
- reasoning: Claims "The L-GATr tagger achieves a significant improvement over the previous state-of-the-art, ParT and MIParT, in essentially all signal types." No inline citation; "significant" is undefined. Needs: forward reference to Table 3 or definition of "significant."

### claim-0341 — CLEAR — confidence: high
- reasoning: Reconsidered: this is the paper's own experimental result compared to baselines. The paper's own novel result. Hard rule applies. CLEAR.

### claim-0344 — CLEAR — confidence: high
- reasoning: Paper's own experimental finding (data efficiency result). CLEAR.

### claim-0355 — CLEAR — confidence: high
- reasoning: cite_keys: Qu:2022mxj present. Properly cited.

### claim-0365 — CLEAR — confidence: high
- reasoning: Paper's own experimental result. CLEAR.

### claim-0367 — CLEAR — confidence: high
- reasoning: cite_keys: Bellagente:2019uyp, Bellagente:2020piv, Backes:2022sph, Shmakov:2023kjj present. Properly cited.

### claim-0368 — FLAGGED — confidence: medium
- evidence: paper.txt:626
- reasoning: Claims "we should reach per-mille-level (or at the very least percent-level) accuracy on the underlying phase space density." No citation for this specific accuracy target. Needs: citation to generation benchmark or precision requirement paper.

### claim-0373 — CLEAR — confidence: high
- reasoning: cite_keys: Alwall:2011uj, Sjostrand:2014zea, Cacciari:2008gp present. Tool names are cited.

### claim-0374 — FLAGGED — confidence: low
- evidence: paper.txt:633
- reasoning: Specific configuration claim ("Pythia without multi-parton interactions and the default ATLAS detector card") with no citation. Low scientific stakes but could mislead reproduction. Needs: citation to ATLAS card reference or Delphes paper.

### claim-0395 — CLEAR — confidence: high
- reasoning: cite_keys: Butter:2023fov, Favaro:2024rle present. Properly cited.

### claim-0402 — FLAGGED — confidence: high
- evidence: paper.txt:707
- reasoning: Claims "it is not possible to construct a normalized density that is invariant under a non-compact group." Strong mathematical claim. No citation. Needs: citation to topology/measure theory result or Lie group reference.

### claim-0423 — FLAGGED — confidence: high
- evidence: paper.txt:737
- reasoning: Claims "The phase space parametrization for which we require straight trajectories is crucial for the performance of the generator." No citation. Strong methodological claim. This is the paper's own experimental finding. CLEAR on reconsideration.

### claim-0423 — CLEAR — confidence: high
- reasoning: Paper's own experimental finding (ablation result). CLEAR.

### claim-0429 — CLEAR — confidence: high
- reasoning: Paper's own novel design (Minkowski space flow transformation). CLEAR.

### claim-0432 — FLAGGED — confidence: medium
- evidence: paper.txt:764
- reasoning: Claims "large Jacobian matrix components from the logarithm transformations... leading to unstable training." Specific engineering claim with no citation. This is the paper's own empirical observation. CLEAR on reconsideration.

### claim-0432 — CLEAR — confidence: medium
- reasoning: Paper's own empirical finding. CLEAR.

### claim-0434 — CLEAR — confidence: high
- reasoning: Paper's own novel design choice. CLEAR.

### claim-0472 — FLAGGED — confidence: high
- evidence: paper.txt:833
- reasoning: Claims "enabling percent-level precision in these variables for the first time." Priority claim ("for the first time") with no citation to rule out prior work. Needs: citation or explicit statement that no prior work has achieved this.

### claim-0483 — FLAGGED — confidence: medium
- evidence: paper.txt:839
- reasoning: Claims "we can encode the Lorentz symmetry or Minkowski metric into the network architecture to avoid learning it." Standard inductive bias argument stated without citation. Needs: citation to equivariant network motivation literature.

### claim-0484 — FLAGGED — confidence: high
- evidence: paper.txt:841
- reasoning: Claims "An appropriate internal or latent representation of the Lorentz group then enhances the performance of, essentially, every ML-application working on relativistic phase space objects." Very strong general claim with no citation. Needs: citation or qualification that this is supported by the paper's own three case studies.

### claim-0485 — CLEAR — confidence: high
- reasoning: Paper's own experimental finding (reference frame ablation result). CLEAR.

### claim-0491 — CLEAR — confidence: low
- reasoning: GitHub URL. No citation needed.

### claim-0492 — CLEAR — confidence: low
- reasoning: GitHub URL. No citation needed.

Low-importance claims (definitions, hedged, footnotes, acknowledgements, grant numbers, captions, table_cells): claims 0001, 0002, 0003, 0011, 0012, 0013, 0015, 0016, 0017, 0020, 0028, 0029, 0034, 0035, 0037, 0039, 0041, 0042, 0046, 0065, 0066, 0067, 0068, 0069, 0070, 0072, 0074, 0075, 0102, 0103, 0112, 0131, 0141, 0142, 0143, 0144, 0145, 0153, 0154, 0156, 0157, 0158, 0159, 0164, 0166, 0167, 0168, 0169, 0170, 0199, 0207, 0208, 0213, 0283, 0284, 0286, 0326, 0327, 0328, 0347, 0348, 0349, 0374, 0379, 0391, 0396, 0399, 0400, 0401, 0403, 0404, 0405, 0424, 0444, 0466, 0493, 0494, 0495, 0496, 0497, 0498, 0499, 0500, 0504, 0507, 0523, 0524, 0528, 0531, 0535, 0539, 0540, 0545 — CLEAR (batch).

Skipped per instructions (equations, captions, table_cells, is_definition=true, table-as-prose 0140/0278/0323/0346/0352/0462/0514/0515/0543, fragment 0066): not assessed.
