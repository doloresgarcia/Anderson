## internal_contradiction

---

### claim-0165 — FLAGGED — confidence: high

**Cross-reference:** also flags claim-0441

- evidence:
  - paper.txt:341 — "In both cases, while symmetry breaking can be beneficial, the network still performs comparably even with full Lorentz equivariance, suggesting that the architecture itself compensates for any symmetry mismatch."
  - paper.txt:772 — "Once again, we observe that including reference multivectors for both beam and time directions is essential; omitting them leads to inferior performance of the L-GATr generator compared to a non-equivariant transformer."
- reasoning: Line 341 claims that for both jet tagging and event generation the network "still performs comparably even with full Lorentz equivariance" (i.e., without reference multivectors). Line 772 says that for event generation, including reference multivectors is "essential" and omitting them "leads to inferior performance." These cannot both be true for the generation case. Table 6 (tab:symbreak_comparison_generation, line ~783) makes the data explicit: the no-reference-vector row gives NLL = 29.36 ± 1.34 and AUC = 0.996 ± 0.001, while the default (with beam + time reference) gives NLL = −32.64 ± 0.02 and AUC = 0.514 ± 0.006 — a qualitative collapse in performance, not a comparable result. The claim on line 341 is therefore directly contradicted by the measurement reported on line 772.

---

### claim-0441 — FLAGGED — confidence: high

**Cross-reference:** also flags claim-0165

- evidence:
  - paper.txt:772 — "Once again, we observe that including reference multivectors for both beam and time directions is essential; omitting them leads to inferior performance of the L-GATr generator compared to a non-equivariant transformer."
  - paper.txt:341 — "In both cases, while symmetry breaking can be beneficial, the network still performs comparably even with full Lorentz equivariance, suggesting that the architecture itself compensates for any symmetry mismatch."
- reasoning: Same contradiction as claim-0165 above, viewed from the other side. The "essential" language in the generation section and Table 6's dramatic performance gap (AUC 0.996 → 0.514 without reference multivectors) directly contradict the earlier blanket statement that the network "performs comparably even with full Lorentz equivariance" in both cases.

---

### claim-0365 — FLAGGED — confidence: high

- evidence:
  - paper.txt:620 — "L-GATr matches the performance of the best fine-tuned networks in the literature across all metrics."
  - paper.txt:480 — (Table 1, ParT-f.t. row) `\result{691}{15}` for $1/\epsilon_B$ ($\epsilon_S = 0.5$)
  - paper.txt:482 — (Table 1, L-GATr-f.t. row) `\result{651}{11}` for $1/\epsilon_B$ ($\epsilon_S = 0.5$)
- reasoning: The claim says L-GATr-f.t. matches the best fine-tuned networks "across all metrics." Table 1 (tab:toptagging) shows that for $1/\epsilon_B$ at $\epsilon_S = 0.5$, L-GATr-f.t. achieves 651 ± 11 while ParT-f.t. achieves 691 ± 15. The central values differ by 40, and the difference exceeds 2σ (using combined error ≈ √(11² + 15²) ≈ 19). L-GATr-f.t. does lead on AUC (0.98793 vs 0.9877/0.9878) and on $1/\epsilon_B$ at $\epsilon_S = 0.3$ (2894 vs 2789/2766), but "across all metrics" is directly falsified by the $1/\epsilon_S = 0.5$ column, where L-GATr-f.t. is not the best performer.

---

### claim-0004 — CLEAR — confidence: medium

Abstract states "state-of-the-art performance for a wide range of tasks." The paper demonstrates L-GATr leading on JetClass multiclass (Table 3), amplitude regression at high multiplicity (Fig. 2), and generation (Fig. 4/5). For top tagging without fine-tuning, L-GATr matches equivariant baselines (same AUC 0.9870). The phrase "wide range of tasks" is hedged enough to be consistent with mixed results across individual metrics.

### claim-0008 — CLEAR — confidence: medium

"Significant improvements over previous architectures." For JetClass (Table 3), L-GATr achieves 0.9885 vs ParT/MIParT at 0.9877/0.9878 — improvements in essentially all per-class metrics. For generation (Fig. 5), L-GATr clearly outperforms transformer and E(3)-GATr. For amplitude regression (Fig. 2), L-GATr leads at higher multiplicity. "Previous architectures" and "significant" are vague enough to be consistent with the data; the ambiguity is a separate `ambiguous` concern, not a logical self-contradiction.

### claim-0032 — CLEAR — confidence: high

States the architecture was "originally developed for an ML audience" — consistent with Spinner:2024hjm being the prior reference; no internal contradiction.

### claim-0033 — CLEAR — confidence: high

Claims extensions vs Spinner:2024hjm: pre-training, multi-class, competitive generation. All are confirmed by the paper's sections on JetClass pre-training (new, confirmed line 440) and multi-class (new, confirmed line 440).

### claim-0040 — CLEAR — confidence: high

"Generates LHC events for t-tbar+4jets better than all benchmarks." Consistent with Fig. 5 generation results showing L-GATr outperforming MLP, transformer, and E(3)-GATr across multiplicities.

### claim-0056 — CLEAR — confidence: high

"Recovers all algebra properties from Ref." — a forward reference to Spinner:2024hjm; no internal contradiction detectable.

### claim-0098 — CLEAR — confidence: high

"Lorentz transformations will never mix grades." The same sentence (line 230) immediately qualifies this for composite multivector states. Authors are distinguishing (1) the grade-preserving property of the sandwich product acting on pure-grade elements vs. (2) grade mixing that arises from composite states under combined group operations. This is a careful technical qualification in continuous prose, not a logical contradiction between separate passages.

### claim-0099 — CLEAR — confidence: high

"In practice grade mixing can occur through the combined action of boosts and rotations on composite multivector states." This is the explicit qualification immediately following claim-0098 in the same sentence. Both are true simultaneously: single-grade elements never mix under the sandwich product; composite states can have grade mixing under sequences of transformations. Not a contradiction.

### claim-0122 — CLEAR — confidence: high

"Second term breaks the symmetry down to the special orthochronous Lorentz group, the fully-connected subgroup that leaves out parity and time reversal."

### claim-0143 — CLEAR — confidence: high

"Second term in the L-GATr linear layer is optional and breaks the Lorentz group down to its fully connected subgroup." Consistent with claim-0122; both refer to the same term in Eq. (linear layer), using equivalent language.

### claim-0155 — CLEAR — confidence: medium

"This strategy produces better results than a network where the symmetry is completely broken." Table 2 (tab:symbreak_comparison) and Table 6 (tab:symbreak_comparison_generation) both support that reference-vector-based partial breaking outperforms no equivariance. Consistent with Tables 2 and 6.

### claim-0185 — CLEAR — confidence: high

L-GATr 2.3×10^4 parameters in the scaling test. This is a single-block test configuration (explicitly stated line 358: "All networks consist of a single network block"). Different from the 1.1×10^6 tagging configuration. No contradiction.

### claim-0186 — CLEAR — confidence: high

CGENN 2.5×10^4 parameters in the scaling test — same single-block test configuration. Consistent.

### claim-0192 — CLEAR — confidence: high

Linear memory scaling for L-GATr and transformer for many tokens. Consistent with the use of FlashAttention and the architecture description.

### claim-0221 — CLEAR — confidence: high

"All networks trained with 4-momenta inputs except DSI." Consistent with Table (tab:amp_build) where DSI is distinguished as taking momentum invariants.

### claim-0224 — CLEAR — confidence: medium

"Transformer and graph networks scale better with the number of external particles." Consistent with Fig. 2 left panel description, where transformer and L-GATr (a graph-attention network) outperform MLP and DSI at higher multiplicities.

### claim-0225 — CLEAR — confidence: medium

"L-GATr roughly on par with DSI for a small number of gluons." Consistent with Fig. 2 left panel.

### claim-0226 — CLEAR — confidence: medium

"Improved scaling gives it the lead for higher-multiplicity final states." Consistent with Fig. 2 left panel.

### claim-0229 — CLEAR — confidence: medium

"L-GATr stands as a top performer on all training regimes." Refers to the right panel of Fig. 2 (training data size scaling). Consistent with described results.

### claim-0234 — CLEAR — confidence: medium

"Reproduce L-GATr scaling behavior despite more complex Z+5g process." Consistent with Fig. 3 description.

### claim-0238 — CLEAR — confidence: high

"All results related to pre-training and multiclass tagging are new to this paper." Consistent with the introduction (line 108) stating these are extensions beyond Spinner:2024hjm.

### claim-0241 — CLEAR — confidence: high

"2M top quark and QCD jets." Dataset size is consistent with the 1.2/0.4/0.4M split (claim-0244), which sums to 2.0M.

### claim-0244 — CLEAR — confidence: high

Train/val/test split 1.2/0.4/0.4M = 2.0M total. Consistent with claim-0241 ("2M jets").

### claim-0293 — CLEAR — confidence: high

"L-GATr is at least on par with the leading equivariant baselines." Table 1 confirms: L-GATr* AUC = 0.9870 matches LorentzNet* (0.9868), CGENN* (0.9869), PELICAN* (0.9870). Consistent.

### claim-0298 — CLEAR — confidence: medium

"Including both the beam direction and the time reference significantly contributes to boosting the tagging performance." Table 2 supports this: AUC goes from 0.9846 (no reference vectors) to 0.9870 (with beam + time). This is consistent with Table 2. The contradiction with claim-0165 is already flagged under claim-0165/0441; within the tagging section alone, the Table 2 data is internally consistent with claim-0298.

### claim-0327 — CLEAR — confidence: high

"The last line is our default used in all other tagging experiments." Table 2 last line: Beam $x_{12}^B=1$, Time $x^V_0=1$, Token embedding, no extra features, AUC = 0.9870. The L-GATr* entry in Table 1 ($1/\epsilon_B = 2240$) corresponds to the configuration without extra features, consistent with Table 2 last line (AUC 0.9870, $1/\epsilon_B$ = 2240). Consistent.

### claim-0341 — CLEAR — confidence: high

"L-GATr achieves significant improvement over ParT and MIParT in essentially all signal types." Table 3 (tab:jctagging): L-GATr beats ParT and MIParT on all 9 signal-class rejection columns and overall AUC (0.9885 vs 0.9877/0.9878). The single exception is the $H\to gg$ column where all three are nearly identical (128 vs 123/123). "Essentially all" is consistent with the data.

### claim-0344 — CLEAR — confidence: medium

"L-GATr achieves similar performance to ParT and MIParT with only 10% of jets." Table 4 at 10M: L-GATr (10M) AUC = 0.9875 vs ParT (100M) = 0.9877 and MIParT (100M) = 0.9878. Broadly consistent with "similar performance."

### claim-0378 — CLEAR — confidence: high

Dataset sizes 9.8M, 7.2M, 3.7M, 1.5M, 480k for n=0..4. No other internal reference contradicts these numbers.

### claim-0421 — CLEAR — confidence: high

"All networks trained on t-tbar+0j dataset." Caption of Table 5 (tab:trajectories, line 734) confirms: "All networks are trained on the $t\bar t+0j$ dataset." Consistent.

### claim-0436 — CLEAR — confidence: high

"For E(3)-GATr, encode (px, py, pz) as a vector and x_m as a scalar." Consistent with the architecture description for E(3)-GATr in the generation section (line 768).

### claim-0443 — CLEAR — confidence: medium

"Specific representation of beam reference multivector is less critical here than in the top-tagging case." Table 6 shows beam representations giving NLL from −32.64 to −32.66, all within statistical uncertainty. Table 2 shows more spread across beam options for tagging. Consistent.

### claim-0464 — CLEAR — confidence: high

"Compare L-GATr performance on t-tbar+0j dataset" — Table 6 caption (line 793) confirms this. Consistent.

### claim-0465 — CLEAR — confidence: high

"The last line is our default used in all other generation experiments." Table 6 last line: Beam $x_{12}^B=1$, Time $x^V_0=1$, Channel embedding, NLL = −32.64 ± 0.02, AUC = 0.514 ± 0.006. This is not the best-performing row (which is $x_0^V=\sqrt{2}, x_3^V=\pm 1$ at NLL = −32.66, AUC = 0.510). The choice of default is stated as the last table row, but note the best row (line 787) achieves marginally better NLL. This is an editorial choice, not a contradiction — the differences are within uncertainty.

### claim-0471 — CLEAR — confidence: medium

"L-GATr outperforms the baselines across all distributions." Consistent with Fig. 4 description and the general results.

### claim-0475 — CLEAR — confidence: medium

"Clear performance improvement from MLP → transformer → GATr → L-GATr." Consistent with Fig. 5 description showing monotonic improvement with increasing symmetry awareness.

### claim-0476 — CLEAR — confidence: medium

"Superior L-GATr performance mainly originates from boost-equivariance." This is an attribution claim based on the comparison with E(3)-GATr; the paper provides the comparison in Fig. 5 and discusses it on line 835. No internal contradiction.

### claim-0478 — CLEAR — confidence: medium

"Enforcing equivariance then breaking with reference multivectors outperforms standard non-equivariant networks." Consistent with Fig. 5 and Table 5/6 showing L-GATr with reference vectors outperforming the plain transformer.

### claim-0485 — CLEAR — confidence: medium

Outlook restatement of claim-0478. Same evidence applies. Consistent.

### claim-0487 — CLEAR — confidence: medium

"L-GATr shows best performance for more than three particles in the final state." Consistent with Fig. 2 left panel amplitude results.

### claim-0488 — CLEAR — confidence: medium

"At least on par with the best available subjet tagger." In the Outlook this refers to the fine-tuned comparison. With fine-tuning, L-GATr-f.t. leads on AUC and $\epsilon_S=0.3$ rejection (Table 1). The phrase "at least on par" is not falsified (note: the contradiction with "across all metrics" is already flagged in claim-0365).

### claim-0489 — CLEAR — confidence: medium

"Faithfully reproduces phase space distribution of top pair production with up to four jets better than all other CFM setups." Consistent with Fig. 4 marginal distributions and Fig. 5 scaling, where L-GATr is described as the best performer.

### claim-0520 — CLEAR — confidence: high

L-GATr top tagging: 32 scalar, 16 multivector, 8 heads, 12 blocks, 1.1×10^6 parameters. Table (tab:top_build, line 918) confirms all these values. Internally consistent.

### claim-0525 — CLEAR — confidence: high

"Pre-training on full 100M events over 10^6 iterations." Consistent with JetClass dataset size claim (100M jets, claim-0336) and training setup description.

### claim-0527 — CLEAR — confidence: high

"10 output channels for multiclass." Consistent with JetClass having 10 classes (claim-0336, "10 classes").

### claim-0529 — CLEAR — confidence: high

"4-momenta scaled by 20 GeV scale factor — same as top tagging." Both top tagging (line 941) and JetClass training (line 943) use 20 GeV scale. Consistent.

### claim-0532 — CLEAR — confidence: high

Pre-trained LR = 3×10^{-5}; weight decay 0.01; batch 128. Table (tab_top_build implied, line 945) gives these same values. Consistent.

### claim-0533 — CLEAR — confidence: high

New layer LR = 3×10^{-3}. Ratio of 100× relative to pre-trained LR is an unusual but deliberate choice. No other passage contradicts it.
