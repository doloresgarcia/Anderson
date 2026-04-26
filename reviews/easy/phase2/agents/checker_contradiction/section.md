## internal_contradiction

### C001 — CLEAR — confidence: medium

- evidence: paper.txt:16-17 ("L-GATr yields state-of-the-art performance for a wide range of machine learning tasks at the Large Hadron Collider.")
- reasoning: The claim is broad and hedged by "wide range," which does not require every sub-case to achieve SOTA. Per-task results in Sections 3, 4, and 5 show that L-GATr is at or near SOTA for all three tasks considered (amplitude regression at higher multiplicities, jet tagging on JetClass and fine-tuned top tagging, event generation). No single passage in the paper directly contradicts the global "wide range" framing.

### C002 — CLEAR — confidence: medium

- evidence: paper.txt:18-19 ("L-GATr represents data in a geometric algebra over space-time and is equivariant under Lorentz transformations.")
- reasoning: The abstract describes the base architectural property. Section 2.3 (paper.txt:514-557) explicitly details how optional reference multivectors break equivariance. The full paper makes clear that "equivariant under Lorentz transformations" describes the core architecture before optional symmetry breaking, which the abstract does not disclaim. No logical contradiction exists between stating the architecture is equivariant and separately explaining its optional symmetry-breaking extension.

### C003 — CLEAR — confidence: medium

- evidence: paper.txt:18-19 ("which is able to break symmetries if needed")
- reasoning: The "break symmetries if needed" mechanism is fully described in Section 2.3 via reference multivectors. The base architecture (C038, paper.txt:311-320) is exactly equivariant; symmetry breaking is an optional extension. These co-exist logically — the architecture is equivariant by default, and capable of breaking symmetry when reference multivectors are added. No contradiction with C038 or C094.

### C004 — FLAGGED — confidence: high

- evidence:
  - paper.txt:22-23 — "For all three LHC tasks, we find significant improvements over previous architectures."
  - paper.txt:750-751 — "We find that L-GATr is roughly on par with the leading DSI network for a small number of gluons, but its improved scaling gives it the lead for higher-multiplicity final states."
- reasoning: The abstract asserts "significant improvements" for "all three LHC tasks," which must include amplitude regression. However, Section 3 explicitly qualifies that for amplitude regression at small gluon multiplicity (Z+1g, Z+2g), L-GATr is only "roughly on par" with the leading DSI network, not significantly better. A "significant improvement" over previous architectures for amplitude regression is incompatible with being "roughly on par" at the lowest multiplicities. The lead is established only at higher multiplicities (Z+3g, Z+4g, Z+5g). The abstract's unqualified universal claim ("all three LHC tasks, significant improvements") cannot both be true simultaneously with Section 3's acknowledgement of parity at low multiplicities.

### C038 — CLEAR — confidence: high

- evidence: paper.txt:311-320
- reasoning: The equivariance claim L-GATr(Λ(x)) = Λ(L-GATr(x)) describes the base architecture before any reference-multivector symmetry breaking. Section 2.3 explains when and how equivariance is voluntarily broken. This is architecturally consistent: the network layers satisfy equivariance by construction, and symmetry breaking through reference multivectors is an additive input mechanism that does not alter the equivariance of the layers themselves. No internal contradiction.

### C060 — CLEAR — confidence: medium

- evidence: paper.txt:531-532 ("this strategy produces better results than a network where the symmetry is completely broken")
- reasoning: C060 is supported quantitatively by Table 3 (jet tagging ablation, lines 913-1002) and Table 7 (generation ablation, lines 1554-1620). In both tables, configurations with reference multivectors outperform configurations with no symmetry breaking. The claim is consistent across Sections 2.3, 4, and 5.

### C065 — CLEAR — confidence: medium

- evidence: paper.txt:545-546 ("We find similar performance for both choices.")
- reasoning: Table 3 (tagging ablation) shows, for rows with the same time reference: x V_3 = ±1 achieves AUC 0.9869 ± 0.0001 while x B_12 = 1 achieves AUC 0.9870 ± 0.0001. These are consistent within the reported uncertainties, confirming "similar performance for both choices." No contradiction.

### C069 — CLEAR — confidence: high

- evidence: paper.txt:555 ("We include such reference multivectors as extra tokens for jet tagging in Sec. 4, and as extra channels for generation in Sec. 5.")
- reasoning: Table 3 (jet tagging ablation, line 995-997) shows the default configuration as "Token" embedding with x B_12=1, x V_0=1 — consistent with "extra tokens" for jet tagging. Table 7 (generation ablation, lines 1607-1614) shows the default configuration as "Channel" — consistent with "extra channels" for generation. The description in Section 2.3 agrees with both experimental sections. No contradiction.

### C077 — INCONCLUSIVE — confidence: low

- evidence: paper.txt:578-580 — "the attention receives inputs with 72 channels from 4 attention heads. In the case of L-GATr, we achieve this by building the architecture with 8 multivector channels and 16 scalar channels."
- reasoning: The paper claims that 8 multivector channels + 16 scalar channels achieves "72 total attention input channels." The arithmetic does not immediately resolve: 8 × 16 (components per multivector) + 16 scalars = 144, not 72; alternatively, treating each multivector as a single channel gives 8 + 16 = 24, also not 72. There may be a non-obvious implementation convention (e.g., a specific projection into attention heads that reduces effective dimensionality, or a convention where "channels" refers to an attention-head-local count) that is not spelled out in the text. The checker cannot confirm or refute the equivalence without access to the implementation code.
- INCONCLUSIVE reason: The term "channels" in the context of L-GATr attention may use an architecture-specific counting convention not defined in the paper, making it impossible to resolve the apparent arithmetic discrepancy from the text alone.

### C078 — CLEAR — confidence: medium

- evidence: paper.txt:583-589 ("In total, L-GATr consists of 2.3 × 10^4 parameters, the transformer consists of 6.7 × 10^5 parameters, and CGENN consists of 2.5 × 10^4 parameters.")
- reasoning: These three parameter counts are stated once in Section 2.4 and are not repeated or contradicted elsewhere in the paper. No second passage gives conflicting counts for the scaling-test architectures.

### C081 — CLEAR — confidence: high

- evidence: paper.txt:593-595 ("L-GATr scales like a standard transformer in the many-token regime because they both use the same attention module. For few tokens, L-GATr is slower because of the more expensive linear layers.")
- reasoning: C081 (many-token scaling equivalent) and C082 (few-token L-GATr slower) describe different regimes and are consistent with each other and with C084 (linear memory scaling). No contradiction across these claims.

### C082 — CLEAR — confidence: high

- evidence: paper.txt:594-595; paper.txt:593-594
- reasoning: See C081 reasoning. The few-token regime statement (C082) and many-token regime statement (C081) are explicitly stated as regime-dependent and are not contradictory.

### C084 — CLEAR — confidence: high

- evidence: paper.txt:597-599
- reasoning: Consistent with C081. Both claim L-GATr and the standard transformer share the same attention module and hence the same asymptotic memory scaling. No contradiction.

### C094 — CLEAR — confidence: high

- evidence: paper.txt:613-614 ("L-GATr guarantees the exact Lorentz invariance of the amplitude.")
- reasoning: For amplitude regression, the output is a Lorentz scalar (the squared amplitude), and L-GATr's base architecture is exactly Lorentz equivariant (C038). Section 3 does not include reference multivectors that would break equivariance. The scalar output of an equivariant network acting on Lorentz-covariant inputs is indeed Lorentz invariant. No internal contradiction.

### C101 — CLEAR — confidence: medium

- evidence: paper.txt:749-751
- reasoning: C101 says L-GATr is "roughly on par with the leading DSI network for a small number of gluons" and takes the lead at higher multiplicities. The Figure 2 description at lines 748-756 supports both aspects. The phrasing accurately describes the relative performance trend shown in the figure. The tension with C004 is captured under C004 (FLAGGED). Within Section 3 itself, C101 is internally consistent.

### C104 — CLEAR — confidence: medium

- evidence: paper.txt:757-758 ("L-GATr stands as a top performer on all training regimes.")
- reasoning: "Top performer on all training regimes" refers to performance vs. training dataset size (the right panel of Fig. 2), not vs. particle multiplicity. The right panel shows that for every training-data fraction tested, L-GATr is among the best or the best performers. This is consistent with the figure description and does not contradict C101 (which discusses multiplicity scaling) since they address different dimensions of performance.

### C112 — INCONCLUSIVE — confidence: medium

- evidence:
  - paper.txt:772-773 — "we show how L-GATr sets a new record for jet tagging by combining the merits of both ideas."
  - paper.txt:1003-1004 — "In Tab. 2, we see how L-GATr is at least on par with the leading equivariant baselines."
  - paper.txt:1339-1340 — "L-GATr matches the performance of the best fine-tuned networks in the literature across all metrics."
- reasoning: There is tension between "sets a new record" (C112, line 773) and "at least on par" / "matches" (C117/C138, lines 1003, 1339). From Table 2, non-fine-tuned L-GATr achieves AUC 0.9870 ± 0.0001, matching PELICAN and CGENN but not strictly exceeding them — this is "at least on par," not a new record. Fine-tuned L-GATr achieves AUC 0.98793, marginally ahead of MIParT-f.t. 0.9878. The section heading claim "sets a new record" applies specifically to the fine-tuned configuration, which is the primary new contribution of Section 4. The "at least on par" statement (C117) refers to the non-fine-tuned configuration already published in Ref. [35]. These two claims refer to different experimental configurations, so the tension can be resolved by interpretation: "new record" = fine-tuned, "at least on par" = non-fine-tuned. However, because "new record" language in a section intro could be read as applying to L-GATr generally, the checker cannot definitively resolve whether this constitutes a contradiction without additional qualification by the authors.
- INCONCLUSIVE reason: "New record" could refer to either the fine-tuned or non-fine-tuned result, and whether the marginal improvement of fine-tuned L-GATr (0.98793 vs. 0.9878) constitutes a "new record" vs. merely "matching" is an interpretation that cannot be resolved purely from the text.

### C117 — CLEAR — confidence: high

- evidence: paper.txt:1003-1004
- reasoning: Table 2 shows L-GATr (non-fine-tuned) with AUC 0.9870 ± 0.0001, equal to PELICAN 0.9870 ± 0.0001 and slightly above CGENN 0.9869. "At least on par with the leading equivariant baselines" accurately describes this result. No contradiction within Section 4's data.

### C119 — CLEAR — confidence: high

- evidence: paper.txt:1014-1015 ("including both the beam direction and the time reference significantly contributes to boosting the tagging performance")
- reasoning: Table 3 (lines 913-1002) supports this: without beam reference, AUC = 0.9846 ± 0.0002; without time reference, AUC = 0.9854 ± 0.0005; with both, AUC = 0.9870 ± 0.0001. The improvement from 0.9846 to 0.9870 is quantifiable and the claim is consistent with the ablation table.

### C129 — CLEAR — confidence: high

- evidence: paper.txt:1036-1038 ("The L-GATr tagger achieves a significant improvement over the previous state-of-the-art, ParT and MIParT, in essentially all signal types on JetClass.")
- reasoning: Table 4 (lines 1044-1106) shows L-GATr outperforming ParT and MIParT across all ten signal classes: L-GATr Accuracy 0.866 vs. ParT/MIParT 0.861; L-GATr AUC 0.9885 vs. ParT 0.9877/MIParT 0.9878. The claim is consistent with the table data across all reported classes. No contradiction.

### C130 — CLEAR — confidence: medium

- evidence: paper.txt:1108-1109 ("the quality of L-GATr predictions steadily increases as we add more features to the training data")
- reasoning: This is stated as a result of a separate study mentioned inline, with the full data efficiency results shown in Figure 4 (left panel) and Table 5. Table 5 shows L-GATr improving from AUC 0.9842 (2M jets) to 0.9875 (10M) to 0.9885 (100M), consistent with steady improvement as dataset size grows. No contradiction.

### C131 — CLEAR — confidence: high

- evidence: paper.txt:1111-1112 ("L-GATr achieves a performance similar to the non-equivariant ParT and MIParT taggers even if trained with only 10% of all available jets.")
- reasoning: Table 5 and Figure 4 left panel: L-GATr trained on 10M jets (10% of 100M) achieves AUC 0.9875, while ParT trained on the full 100M achieves 0.9877 and MIParT 0.9878. These are essentially equal, confirming the data-efficiency claim. No contradiction.

### C138 — CLEAR — confidence: medium

- evidence: paper.txt:1339-1340 ("L-GATr matches the performance of the best fine-tuned networks in the literature across all metrics.")
- reasoning: Table 2 shows L-GATr-f.t. achieving AUC 0.98793 ± 0.00001 vs. MIParT-f.t. 0.9878 ± 0.0001 (estimated) and ParT-f.t. 0.9877. The reported L-GATr-f.t. results are comparable or marginally better across all metrics reported (Accuracy, AUC, 1/εB at εS=0.5 and εS=0.3). The word "matches" (C138) is consistent with the marginal lead or near-equality seen in Table 2. The tension with C112 ("new record") is discussed under C112 (INCONCLUSIVE).

### C148 — CLEAR — confidence: medium

- evidence: paper.txt:1363-1364 ("resulting in 9.8M, 7.2M, 3.7M, 1.5M and 480k events for n = 0...4")
- reasoning: These dataset sizes are stated once. No other passage in the paper contradicts these numbers. The stated trend (decreasing dataset size with increasing n) is physically plausible given that higher-multiplicity tt̄ + nj events are less frequent. No contradiction.

### C180 — CLEAR — confidence: medium

- evidence: paper.txt:1649-1651 ("L-GATr outperforms the baselines across all distributions.")
- reasoning: Figure 6 (lines 1646-1852) shows one-dimensional distributions for tt̄ + 1,2,3,4 jets. The E(3)-GATr results are omitted from Figure 6 (line 1851: "as they are very similar to the standard transformer"), but L-GATr is compared to MLP, Transformer, and L-GATr. The text is consistent with the figures shown: L-GATr visibly outperforms MLP and Transformer in the shown distributions (mass poles, angular correlations). The claim is qualified to the displayed distributions, not a quantitative metric across all observables, and is not contradicted elsewhere.

### C183 — FLAGGED — confidence: high

- evidence:
  - paper.txt:1660-1661, 1926 — "In Fig. 7 we find a clear performance improvement as symmetry awareness increases, from the unstructured MLP over the permutation-equivariant transformer to the rotation-equivariant GATr and the Lorentz-equivariant L-GATr."
  - paper.txt:1928 — "the rotation-equivariant E(3)-GATr performs only marginally better than the plain transformer."
- reasoning: The first passage asserts a "clear performance improvement" at each step in the symmetry-awareness hierarchy, explicitly including the transformer-to-GATr step. The second passage, in the same paragraph, states that the GATr improvement over the transformer is "only marginal." A "clear improvement" and an "only marginal improvement" are logically incompatible descriptions of the same quantity (the performance gap between the standard transformer and E(3)-GATr). A marginal improvement is by definition not a clear improvement, and vice versa. Both statements appear within the same continuous paragraph of Section 5 (pages 19-20 of the paper).

### C184 — CLEAR — confidence: high

- evidence: paper.txt:1927-1928 ("the superior L-GATr performance mainly originates from boost-equivariance")
- reasoning: This is supported by the fact that E(3)-GATr (rotation-equivariant, no boost equivariance) performs only marginally better than the transformer, while L-GATr (Lorentz-equivariant, including boost equivariance) performs significantly better. The attribution to boost-equivariance is consistent with the data in Figure 7 and the discussion in lines 1926-1932. No contradiction with other paper passages.

### C185 — FLAGGED — confidence: high

- evidence:
  - paper.txt:1928 — "the rotation-equivariant E(3)-GATr performs only marginally better than the plain transformer."
  - paper.txt:1660-1661, 1926 — "In Fig. 7 we find a clear performance improvement as symmetry awareness increases, from the unstructured MLP over the permutation-equivariant transformer to the rotation-equivariant GATr and the Lorentz-equivariant L-GATr."
- reasoning: This is the reciprocal of C183. C185 states E(3)-GATr is "only marginally better" than the transformer; C183 states there is a "clear performance improvement" at each step including the transformer-to-GATr step. These two characterizations are directly incompatible. Both are flagged as they are both parties to the contradiction.

### C193 — CLEAR — confidence: high

- evidence: paper.txt:1950-1952 ("leading to significantly better performance than removing the corresponding equivariance from the network altogether")
- reasoning: Section 6 (Outlook) claims that breaking symmetry with reference frames outperforms removing equivariance entirely. This is consistently supported by Tables 3 and 7, where removing symmetry breaking reference multivectors yields the worst performance, and by the generation results in Figure 7 where L-GATr (equivariant with controlled symmetry breaking) outperforms the MLP and standard transformer. The claim in Section 6 accurately summarizes the experimental evidence.

### C195 — INCONCLUSIVE — confidence: medium

- evidence:
  - paper.txt:1954-1955 — "For amplitude regression...L-GATr shows the best performance for more than three particles in the final state"
  - paper.txt:750-751 — "L-GATr is roughly on par with the leading DSI network for a small number of gluons, but its improved scaling gives it the lead for higher-multiplicity final states."
- reasoning: C195 says L-GATr leads "for more than three particles in the final state." Depending on whether "particles" counts only the gluons (n > 3 → Z+4g only) or all final-state particles including the Z boson (n+1 > 3 → n ≥ 3, i.e., Z+3g and above), the threshold differs. C101 says L-GATr leads at "higher-multiplicity final states," which from the figure appears to include Z+3g. If "more than three particles" in C195 means n+1 > 3 (≥ Z+3g), the claims are consistent. If it means n > 3 (≥ Z+4g only), they are inconsistent with C101. The paper does not explicitly define "particles" as gluons or total final-state particles in Section 6.
- INCONCLUSIVE reason: The referent of "three particles" in C195 is ambiguous (gluons vs. total final-state particles), and the checker cannot determine which interpretation is intended without additional context, making it impossible to conclusively confirm or deny a contradiction with C101.

### C197 — CLEAR — confidence: high

- evidence: paper.txt:1957-1958 ("For subjet tagging, L-GATr combines the benefit of equivariance with pre-training on large datasets and is at least on par with the best available subjet tagger.")
- reasoning: "At least on par" is consistent with Table 2 (non-fine-tuned: matches best equivariant baselines) and fine-tuned results (marginally exceeds ParT-f.t. and MIParT-f.t.). No contradiction with Section 4 data.

### C198 — CLEAR — confidence: high

- evidence: paper.txt:1959-1961 ("the combination of L-GATr with a CFM generator faithfully reproduces the phase space distribution of top pair production with up to four jets better than all other CFM setups")
- reasoning: Figure 7 (lines 1858-1925) shows L-GATr CFM outperforming MLP CFM, Transformer CFM, and E(3)-GATr CFM in both NLL and classifier AUC metrics across all tt̄+nj multiplicities. The claim is consistent with the figure data. No contradiction.
