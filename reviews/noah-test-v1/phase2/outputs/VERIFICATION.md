# VERIFICATION.md — noah-test-v1

Assembled from five checker section files in severity order.

Summary:
- unreferenced: 25 FLAGGED
- ambiguous: 9 FLAGGED
- internal_contradiction: 3 FLAGGED (2 contradiction pairs + 1 standalone)
- literature_collision: 0 FLAGGED, 2 INCONCLUSIVE
- domain_violation: 3 FLAGGED, 2 INCONCLUSIVE

---

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

### claim-0031 — FLAGGED — confidence: high
- evidence: paper.txt:108
- reasoning: Claims L-GATr includes "a maximally expressive linear map." This is a strong architectural novelty claim about expressiveness. No citation is provided, and no proof is offered in the abstract context. Needs: proof reference or citation to expressiveness result.

### claim-0043 — FLAGGED — confidence: medium
- evidence: paper.txt:120
- reasoning: Describes geometric algebra as "a mathematical framework that represents certain geometric objects and operations in a unified language" without citation. cite_keys field is empty. The GA literature (Hestenes) should be cited here. Needs: foundational GA reference (e.g., hestenes1966space).

### claim-0079 — FLAGGED — confidence: medium
- evidence: paper.txt:190
- reasoning: Claims "the spacetime algebra naturally structures relevant objects like parity-violating transition amplitudes." No citation. This is a non-obvious physical claim about the algebraic structure of amplitudes. Needs: citation to amplitude decomposition in GA or spacetime algebra literature.

### claim-0100 — FLAGGED — confidence: high
- evidence: paper.txt:230
- reasoning: Claims "the spacetime algebra G_{1,3} covers only a limited range of Lorentz tensor representations." No citation. This is a factual algebraic limitation claim. Needs: citation to representation theory literature or GA textbook.

### claim-0101 — FLAGGED — confidence: high
- evidence: paper.txt:230
- reasoning: Claims G_{1,3} "cannot represent symmetric rank-2 tensors." No citation. Verifiable algebraic claim without reference. Needs: citation to GA or representation theory source.

### claim-0132 — FLAGGED — confidence: medium
- evidence: paper.txt:289
- reasoning: Claims "the specific value of ε has a negligible impact on the performance." Empirical claim with no citation and no figure/table reference. Needs: ablation results or table reference within the paper.

### claim-0146 — FLAGGED — confidence: medium
- evidence: paper.txt:332
- reasoning: Claims "In many LHC contexts, Lorentz symmetry is only partially preserved." No citation. Accurate general statement but asserted without reference. Needs: citation to LHC symmetry-breaking literature or prior equivariant network papers.

### claim-0162 — FLAGGED — confidence: medium
- evidence: paper.txt:339
- reasoning: Claims "the detector setup can compromise the symmetry of the observables with respect to relativistic boosts." No citation. Needs: citation supporting detector-induced symmetry breaking claim.

### claim-0195 — FLAGGED — confidence: high
- evidence: paper.txt:360
- reasoning: Claims use of FlashAttention but provides no cite_key. cite_keys field is empty. FlashAttention is a specific external method and must be cited. Needs: citation to Dao et al. (FlashAttention paper).

### claim-0202 — FLAGGED — confidence: high
- evidence: paper.txt:381
- reasoning: Claims "standard neural networks struggle to reach sufficient accuracy for a high amount of external particles." No citation. Strong claim about limitations of standard networks for high-multiplicity amplitude regression. Needs: citation to published amplitude regression results showing this limitation.

### claim-0237 — FLAGGED — confidence: medium
- evidence: paper.txt:440
- reasoning: Claims "Two approaches stand out as top performers: transformer-based architectures and equivariant networks." No citation. Broad comparative claim about the jet tagging literature. Needs: citation to benchmark study or review (e.g., Kasieczka:2019dbj).

### claim-0294 — FLAGGED — confidence: high
- evidence: paper.txt:500
- reasoning: Claims "non-equivariant architectures generally achieve higher accuracy than equivariant ones when sufficient training data is available, as the additional architectural constraints limit the representation capacity." No citation. This is a general architectural claim that goes beyond the paper's own results. Needs: citation to literature supporting this general observation.

### claim-0336 — FLAGGED — confidence: high
- evidence: paper.txt:542
- reasoning: Claims "JetClass contains 100M jets equally distributed across 10 classes." No cite_keys in this specific claim. This is an external dataset fact that requires citation to Qu:2022mxj. Needs: citation to JetClass paper (Qu:2022mxj).

### claim-0368 — FLAGGED — confidence: medium
- evidence: paper.txt:626
- reasoning: Claims "we should reach per-mille-level (or at the very least percent-level) accuracy on the underlying phase space density." No citation for this specific accuracy target. Needs: citation to generation benchmark or precision requirement paper.

### claim-0402 — FLAGGED — confidence: high
- evidence: paper.txt:707
- reasoning: Claims "it is not possible to construct a normalized density that is invariant under a non-compact group." Strong mathematical claim. No citation. Needs: citation to topology/measure theory result or Lie group reference.

### claim-0472 — FLAGGED — confidence: high
- evidence: paper.txt:833
- reasoning: Claims "enabling percent-level precision in these variables for the first time." Priority claim ("for the first time") with no citation to rule out prior work. Needs: citation or explicit statement that no prior work has achieved this.

### claim-0483 — FLAGGED — confidence: medium
- evidence: paper.txt:839
- reasoning: Claims "we can encode the Lorentz symmetry or Minkowski metric into the network architecture to avoid learning it." Standard inductive bias argument stated without citation. Needs: citation to equivariant network motivation literature.

### claim-0484 — FLAGGED — confidence: high
- evidence: paper.txt:841
- reasoning: Claims "An appropriate internal or latent representation of the Lorentz group then enhances the performance of, essentially, every ML-application working on relativistic phase space objects." Very strong general claim with no citation. Needs: citation or qualification that this is supported by the paper's own three case studies.

All other checked claims: CLEAR.

---

## ambiguous

### claim-0008 — FLAGGED — confidence: high
- evidence: paper.txt:64
- text: "For all three LHC tasks, we find significant improvements over previous architectures."
- interpretations:
  1. "Significant" means statistically and practically meaningful improvements across all three tasks (amplitude regression, top tagging, event generation) and across all metrics reported — i.e., L-GATr strictly dominates every baseline on every metric.
  2. "Significant" means improvements that are noticeable in at least some metrics or tasks, even if other baselines match or exceed L-GATr on specific metrics or tasks — consistent with a mixed result where L-GATr leads on some dimensions but not all.
- reasoning: The ambiguity matters because Table 1 (top tagging) shows L-GATr is "at least on par" with leading equivariant baselines but explicitly does not exceed non-equivariant ParT/MIParT without pre-training. Interpretation 1 would be contradicted by the tables; interpretation 2 is supportable. A reader evaluating the abstract's claim as implying strict dominance across all tasks and metrics would reach a different conclusion about the paper's contribution than one reading it as "wins on balance."

### claim-0099 — FLAGGED — confidence: high
- evidence: paper.txt:230
- text: "Each algebra grade transforms under a separate sub-representation of the Lorentz group, although in practice grade mixing can occur through the combined action of boosts and rotations on composite multivector states."
- interpretations:
  1. "Grade mixing" refers to a phenomenon where a composite multivector state has its grades mixed when different individual elements transform, so the composite mixes grades even though individual pure-grade elements do not.
  2. "Grade mixing" means that even individual-grade elements can appear to change grade under certain combined Lorentz operations, so the grade-separation claim of the preceding sentence is only approximate.
- reasoning: Consequential because claim-0098 asserts "Lorentz transformations will never mix grades" as the justification for grade-structured equivariant layers. If interpretation 2 is correct, the architectural claim breaks down. The authors do not define "composite multivector states" precisely enough to resolve this.

### claim-0147 — FLAGGED — confidence: high
- evidence: paper.txt:334
- text: "If this partial symmetry breaking is not accounted for when applying a Lorentz-equivariant architecture, performance can degrade significantly."
- interpretations:
  1. "Significantly" refers to a numerically large, practically important performance drop (several AUC points or a factor-of-several error increase).
  2. "Significantly" refers to any statistically detectable performance drop relative to a symmetry-breaking-aware network, which could be modest in absolute terms.
- reasoning: Table 2 shows that omitting all reference vectors drops AUC from ~0.9870 to ~0.9846 (a 0.0024 difference), which may or may not be "significant" depending on the reading. A reader applying interpretation 1 would expect a much larger gap; interpretation 2 is consistent with the actual results.

### claim-0150 — FLAGGED — confidence: medium
- evidence: paper.txt:334
- text: "A fully Lorentz-equivariant architecture is, by construction, blind to these differences, which can limit its effectiveness."
- interpretations:
  1. The network is completely unable to distinguish inputs related by global Lorentz transformations — strict equivariance meaning identical outputs for boosted events.
  2. The network is blind specifically to physical differences only visible after a symmetry-breaking transformation (beam direction), but can still distinguish events differing in Lorentz-invariant quantities.
- reasoning: Interpretation 1 is mathematically accurate but overstates the practical consequence; interpretation 2 is more nuanced and physically accurate. The sentence does not specify which "differences" are meant.

### claim-0165 — FLAGGED — confidence: medium
- evidence: paper.txt:341
- text: "In both cases, while symmetry breaking can be beneficial, the network still performs comparably even with full Lorentz equivariance, suggesting that the architecture itself compensates for any symmetry mismatch."
- interpretations:
  1. "Any symmetry mismatch" means the architecture broadly compensates for any degree of symmetry mismatch in any LHC task, implying the reference multivector mechanism is largely optional.
  2. "Any symmetry mismatch" refers specifically to the two cases studied (jet tagging and event generation with full equivariance), with "comparably" meaning within the tested configurations only.
- reasoning: The claim uses "any symmetry mismatch" universally, but the evidence is restricted to two specific experimental settings. Also flagged as internal_contradiction: this claim directly contradicts line 772 for the generation case.

### claim-0202 — FLAGGED — confidence: high
- evidence: paper.txt:381
- text: "However, standard neural networks struggle to reach sufficient accuracy for a high amount of external particles."
- interpretations:
  1. "Sufficient accuracy" is defined by an application-specific precision threshold (per-mille level), so the claim means standard networks fail to meet that threshold for high multiplicity.
  2. "Sufficient accuracy" is undefined and means only that standard networks perform worse than equivariant ones at high multiplicity — a relative comparison claim.
- reasoning: This claim directly motivates the L-GATr amplitude regression work. If interpretation 1, it is a falsifiable quantitative claim that requires evidence (no citation provided). If interpretation 2, it is a qualitative comparative claim that is supported by the figures but carries less force.

### claim-0368 — FLAGGED — confidence: high
- evidence: paper.txt:626
- text: "For all these tasks we should reach per-mille-level (or at the very least percent-level) accuracy on the underlying phase space density."
- interpretations:
  1. "Per-mille or percent level accuracy" is a precision target for the density itself — the generated distribution must match the true phase space density to within 0.1% or 1% everywhere.
  2. "Accuracy" refers to some unspecified metric of distributional similarity (e.g., classifier AUC, NLL), and per-mille/percent is an informal order-of-magnitude description.
- reasoning: The generation section uses AUC and NLL as metrics, neither of which maps directly to "per-mille accuracy on phase space density." If interpretation 1, the paper should demonstrate meeting this threshold on the density, but the metrics reported do not directly measure this.

### claim-0484 — FLAGGED — confidence: high
- evidence: paper.txt:843
- text: "An appropriate internal or latent representation of the Lorentz group then enhances the performance of, essentially, every ML-application working on relativistic phase space objects."
- interpretations:
  1. "Essentially every" means nearly all ML applications on relativistic phase space — a broad empirical claim generalizing beyond the three tasks studied.
  2. "Essentially every" is qualified by "essentially" to mean only those applications similar to the three studied, with the qualifier functioning as a hedge against untested domains.
- reasoning: This is the Outlook's central take-away. Interpretation 1 invites a much broader conclusion than the evidence supports (three LHC tasks), while interpretation 2 is defensible but depends on reading "essentially" as a strong domain restriction.

### claim-0488 — FLAGGED — confidence: high
- evidence: paper.txt:847
- text: "For subjet tagging, L-GATr combines the benefit of equivariance with pre-training on large datasets and is at least on par with the best available subjet tagger."
- interpretations:
  1. "At least on par" means L-GATr matches or exceeds the best subjet tagger on all reported metrics including AUC, accuracy, and background rejection.
  2. "At least on par" means L-GATr is not definitively worse overall, allowing it to trail on some individual metrics while leading on others.
- reasoning: Table 1 shows L-GATr-f.t. leads on AUC and $1/\epsilon_B(\epsilon_S=0.3)$ but trails on $1/\epsilon_B(\epsilon_S=0.5)$ vs. ParT-f.t. (651±11 vs 691±15). Interpretation 1 is not fully supported; interpretation 2 is the more defensible reading.

Medium/low importance claims: CLEAR (batch).

---

## internal_contradiction

### claim-0165 — FLAGGED — confidence: high

**Cross-reference:** also flags claim-0441

- evidence:
  - paper.txt:341 — "In both cases, while symmetry breaking can be beneficial, the network still performs comparably even with full Lorentz equivariance, suggesting that the architecture itself compensates for any symmetry mismatch."
  - paper.txt:772 — "Once again, we observe that including reference multivectors for both beam and time directions is essential; omitting them leads to inferior performance of the L-GATr generator compared to a non-equivariant transformer."
- reasoning: Line 341 claims that for both jet tagging and event generation the network "still performs comparably even with full Lorentz equivariance" (i.e., without reference multivectors). Line 772 says that for event generation, including reference multivectors is "essential" and omitting them "leads to inferior performance." These cannot both be true for the generation case. Table 6 makes the data explicit: the no-reference-vector row gives NLL = 29.36 ± 1.34 and AUC = 0.996 ± 0.001 (a failed generator), while the default (with beam + time reference) gives NLL = −32.64 ± 0.02 and AUC = 0.514 ± 0.006 (good generator). The claim on line 341 is therefore directly contradicted by the measurement reported on line 772.

### claim-0441 — FLAGGED — confidence: high

**Cross-reference:** also flags claim-0165

- evidence:
  - paper.txt:772 — "Once again, we observe that including reference multivectors for both beam and time directions is essential; omitting them leads to inferior performance of the L-GATr generator compared to a non-equivariant transformer."
  - paper.txt:341 — "In both cases, while symmetry breaking can be beneficial, the network still performs comparably even with full Lorentz equivariance, suggesting that the architecture itself compensates for any symmetry mismatch."
- reasoning: Same contradiction as claim-0165 above, viewed from the other side. The "essential" language in the generation section and Table 6's dramatic performance gap (AUC 0.996 → 0.514 without reference multivectors) directly contradict the earlier blanket statement that the network "performs comparably even with full Lorentz equivariance" in both cases.

### claim-0365 — FLAGGED — confidence: high

- evidence:
  - paper.txt:620 — "L-GATr matches the performance of the best fine-tuned networks in the literature across all metrics."
  - paper.txt:480 — (Table 1, ParT-f.t. row) `\result{691}{15}` for $1/\epsilon_B$ ($\epsilon_S = 0.5$)
  - paper.txt:482 — (Table 1, L-GATr-f.t. row) `\result{651}{11}` for $1/\epsilon_B$ ($\epsilon_S = 0.5$)
- reasoning: The claim says L-GATr-f.t. matches the best fine-tuned networks "across all metrics." Table 1 shows that for $1/\epsilon_B$ at $\epsilon_S = 0.5$, L-GATr-f.t. achieves 651 ± 11 while ParT-f.t. achieves 691 ± 15. The central values differ by 40, and the difference exceeds 2σ (combined error ≈ 19). L-GATr-f.t. leads on AUC and $1/\epsilon_B$ at $\epsilon_S = 0.3$, but "across all metrics" is directly falsified by the $\epsilon_S = 0.5$ column.

All other checked claims: CLEAR.

---

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

---

## domain_violation

### claim-0052 — FLAGGED — confidence: high
- evidence: paper.txt:133
- violated_principle: The geometric product of two elements of the same grade is not generally commutative. Two grade-k elements (k ≥ 1) do not commute unless they satisfy special algebraic conditions (e.g., vectors are collinear). For vectors: xy = {x,y}/2 + [x,y]/2 but yx = {x,y}/2 − [x,y]/2, so xy = yx only if [x,y] = 0.
- canonical_source: Doran & Lasenby, *Geometric Algebra for Physicists* (Cambridge University Press, 2003), §2.4; Hestenes, *Space-Time Algebra* (1966).
- reasoning: The paper states "the geometric product preserves commutativity when acting on elements of the same grade." This is false. Grade-sameness does not imply commutativity in geometric algebra. Only grade-0 scalars commute with all elements automatically.

### claim-0058 — FLAGGED — confidence: high
- evidence: paper.txt:142
- violated_principle: The difference between G(1,3) (spacetime algebra) and the Dirac algebra is not merely the field of the underlying vector space (R vs C). Over R, C(1,3) ≅ M(2,H) (2×2 matrices over the quaternions), while the standard Dirac algebra is M(4,C). These are non-isomorphic as real algebras with different representations and centers.
- canonical_source: Lounesto, *Clifford Algebras and Spinors* (Cambridge University Press, 2nd ed., 2001), §15; Doran & Lasenby, *Geometric Algebra for Physicists* (2003), §2.5.
- reasoning: The paper states "the only difference being that the spacetime algebra is defined over R^4, whereas the Dirac algebra is defined over C^4." This is an oversimplification that misrepresents the algebraic relationship and would mislead readers about the structural connection.

### claim-0099 — FLAGGED — confidence: high
- evidence: paper.txt:229
- violated_principle: The sandwich product vxv^{-1} with v in the Clifford/Spin/Pin group is grade-preserving by the fundamental theorem of the versor representation. This holds for any v in the group — boosts, rotations, and all their compositions preserve grades.
- canonical_source: Lounesto, *Clifford Algebras and Spinors* (Cambridge University Press, 2001), §17 (versor representation); Doran & Lasenby, *Geometric Algebra for Physicists* (2003), §5.2.
- reasoning: The paper states "in practice grade mixing can occur through the combined action of boosts and rotations on composite multivector states." A product of group elements v₁v₂ is still in the group, and (v₁v₂)x(v₁v₂)^{-1} is still grade-preserving. This contradicts settled algebra.
- cross_reference: claim-0098 ("Lorentz transformations will never mix grades") is the correct statement of the grade-preservation theorem. claim-0099's qualification contradicts it.

### claim-0082 — INCONCLUSIVE — confidence: medium
- reason: The characterization of the interference term 2Re(M_E* M_O) as "a pseudoscalar function of the 4-momenta" is internally consistent with the paper's algebraic formalism (it maps to the γ^5 grade), but whether this constitutes a domain violation depends on interpretation. Insufficient certainty to flag.

### claim-0163 — INCONCLUSIVE — confidence: medium
- reason: The stabilizer of the null vector (1,0,0,±1) under the Lorentz group is the little group ISO(2) (the Euclidean group of the 2D plane), not simply SO(2) as stated. However, in the physical context of beam-axis reference vectors, the relevant symmetry is azimuthal SO(2), which may be what the authors mean. Expert scrutiny warranted but not a clear-cut domain violation.

All remaining claims: CLEAR.
