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
## ambiguous

<!-- Count reconciliation (M6): The orchestrator dispatch summary cited 29 FLAGGED ambiguous claims; the actual artifact contains 27 FLAGGED entries (C001, C003, C004, C015, C017, C026, C029, C033, C040, C052, C054, C057, C070, C074, C086, C093, C129, C142, C166, C175, C181, C182, C186, C191, C192, C193, C196). The artifact count of 27 is authoritative. The summary overcounted by 2; no claims were dropped during concatenation — the section.md is the complete checker output. -->

### C001 — FLAGGED — confidence: high
- evidence: paper.txt:16-17 — "yields state-of-the-art performance for a wide range of machine learning tasks at the Large Hadron Collider"
- interpretations:
  1. "wide range" means the three tasks actually studied (amplitude regression, jet classification, event generation), i.e., the claim is scoped to the paper's own benchmarks.
  2. "wide range" means broadly across the full spectrum of LHC ML applications (triggering, anomaly detection, simulation, etc.), well beyond the three tasks demonstrated.
- reasoning: The abstract does not bound the scope of "wide range." Interpretation 1 is the narrow reading supported by the body of the paper; interpretation 2 is how a general reader may initially read the abstract. This ambiguity matters because the paper's headline result is only validated for three specific tasks, and overstating to "wide range of LHC tasks" in general would be a stronger claim than the evidence supports.

### C003 — FLAGGED — confidence: high
- evidence: paper.txt:18-20 — "The underlying architecture is a versatile and scalable transformer, which is able to break symmetries if needed."
- interpretations:
  1. "Break symmetries if needed" refers specifically to the reference-multivector mechanism described in Section 2.3, whereby additional input vectors selectively break Lorentz equivariance to a subgroup — a controlled, learnable symmetry-breaking procedure.
  2. "Break symmetries if needed" refers more broadly to any form of symmetry breaking achievable by the architecture, including the optional γ5 term in the linear layer (Eq. 15) that breaks to the special orthochronous Lorentz group, and the scalar-channel extensions — i.e., multiple distinct mechanisms.
- reasoning: Without knowing which mechanism is intended, the reader cannot determine the scope of the symmetry-breaking capability being advertised. The claim matters because it is part of the abstract's selling proposition; if only one of the mechanisms is meant, then the claim overstates the architecture's adaptability; if all are intended, the abstract elides the complexity.

### C004 — FLAGGED — confidence: high
- evidence: paper.txt:22-23 — "For all three LHC tasks, we find significant improvements over previous architectures."
- interpretations:
  1. "Significant improvements" means statistically or numerically substantial improvements in the primary reported metrics (e.g., AUC, MSE, NLL) across all three tasks, where L-GATr clearly outperforms all listed baselines.
  2. "Significant improvements" is used informally to describe any measurable improvement, even if in some tasks L-GATr is merely "at least on par" with prior art (e.g., C117: "L-GATr is at least on par with the leading equivariant baselines" for top tagging) or sets a new record only marginally.
- reasoning: The word "significant" is ambiguous between statistical significance and practical/engineering significance. For top tagging, the paper itself says "at least on par" rather than substantially better; for JetClass, it claims "significant improvement." Whether "significant improvements … for all three tasks" is warranted depends on which sense of "significant" is used and how the top-tagging result is characterised, and this affects the paper's core advertised conclusion.

### C006 — CLEAR — confidence: medium
- evidence: paper.txt:70-72 — "it is how we can ensure that these networks provide optimal and resilient results, including a comprehensive uncertainty treatment"
- reasoning: Although "optimal and resilient" is informal language, the sentence is clearly a rhetorical framing of the field's challenge rather than a technical assertion about L-GATr specifically. The statement has one reasonable reading in context: the open research question is how to achieve high-performance, robust networks with good uncertainty quantification. No paper-level ambiguity arises.

### C015 — FLAGGED — confidence: high
- evidence: paper.txt:118-120 — "We generalize it to L-GATr encoding exact Lorentz-equivariance into new network layers, including a maximally expressive linear map, attention, and layer normalization."
- interpretations:
  1. "Maximally expressive" means that the linear layer (Eq. 15) is the most general Lorentz-equivariant linear map on multivectors — i.e., no Lorentz-equivariant linear layer can have strictly more free parameters or produce a wider range of equivariant outputs. This is a formal completeness claim about the representation theory.
  2. "Maximally expressive" means that the linear layer is more expressive than previously used equivariant linear layers (e.g., in GATr) in the context of Lorentz representations, without claiming absolute completeness with respect to all possible equivariant linear maps.
- reasoning: The distinction matters because interpretation 1 is a strong formal mathematical claim (provable or disprovable by representation theory), whereas interpretation 2 is a weaker comparative claim. If interpretation 1 is wrong, a reader could construct a more expressive equivariant linear map and thereby challenge the architectural claim. The paper does not state a proof or cite one, so the ambiguity is unresolved.

### C017 — FLAGGED — confidence: medium
- evidence: paper.txt:122-125 — "we extend the amplitude regression analysis, improve the classification through pre-training and multi-class tagging, and deliver a competitive generative network for Monte Carlo event generation"
- interpretations:
  1. "Improve the classification" means L-GATr improves over the prior version (Ref. [35]) that used L-GATr for top tagging, specifically through the pre-training and multi-class-tagging additions described in this paper.
  2. "Improve the classification" means L-GATr improves over the prior state-of-the-art in jet classification generally, not just over the earlier L-GATr paper.
- reasoning: The ambiguity between self-comparison and field-wide comparison affects whether the claim constitutes a novel result or a description of new features relative to a previous preprint. It matters for how readers assess what is genuinely new in this paper. The phrase "deliver a competitive generative network" further illustrates the pattern: "competitive" in the third task implicitly concedes a different magnitude of advance than for classification, but the sentence does not distinguish the two.

### C021 — CLEAR — confidence: high
- evidence: paper.txt:172-176 — "Furthermore, Eq. (2) is also the defining property of the gamma matrices, the basis elements of the Dirac algebra used to describe spinor interactions. Both algebras are closely related, the only difference being that the spacetime algebra is defined over R4, whereas the Dirac algebra is defined over C4."
- reasoning: The claim has one unambiguous reading: the anticommutation relation {γμ,γν}=2gμν is the defining property of the Clifford algebra in both the real spacetime algebra and the complex Dirac algebra, with the distinction that the spacetime algebra is real and the Dirac algebra is complex. The description is clear in context, and no reading that changes the paper's conclusions is available.

### C026 — FLAGGED — confidence: medium
- evidence: paper.txt:198-199 — "the missing factor i compared to the usual definition of γ5 indicates the slight difference between the complex Dirac algebra and the real spacetime algebra"
- interpretations:
  1. "The usual definition of γ5" refers to the standard QFT convention γ5 = iγ0γ1γ2γ3 (with an explicit factor of i to make γ5 Hermitian and γ5² = 1), and the paper's definition γ5 = γ0γ1γ2γ3 (without i) reflects the difference in using a real rather than complex algebra.
  2. "The usual definition" could refer to a convention-dependent form that varies across QFT textbooks (some use γ5 = γ0γ1γ2γ3 directly in the Weyl representation with a different metric signature), so "missing factor i" is not universally accurate.
- reasoning: The word "usual" is metric-convention- and representation-dependent. In the (+−−−) metric with the standard Dirac representation, the conventional γ5 is iγ0γ1γ2γ3; in other conventions or representations, the factor may differ. This ambiguity matters because the paper uses it to explain a structural difference between its algebra and the Dirac algebra, but the explanation holds precisely only for a specific set of conventions that are not spelled out.

### C029 — FLAGGED — confidence: medium
- evidence: paper.txt:232-240 — "We want to apply this representation to particles, which can be characterized by their type (i.e. particle identification, or PID) and their 4-momentum pμ, xS = PID, xV_μ = pμ, xT_μν = xA_μ = xP = 0."
- interpretations:
  1. PID is a pre-defined integer or categorical label (e.g., PDG particle code or a one-hot encoding thereof) that is simply stored in the scalar component xS without further specification of its encoding scale or normalization; the reader is expected to infer this from common practice.
  2. PID is embedded as a continuous scalar or a structured feature within the scalar channel in some task-specific way (e.g., standardized or binary-encoded), and the specific encoding used could affect network performance or reproducibility.
- reasoning: The encoding of discrete particle identity (PID) into a real scalar component is not specified beyond "xS = PID." This ambiguity matters for reproducibility: different encodings of PID (ordinal, one-hot summed into a scalar, or a learned embedding) would interact differently with the linear and activation layers that operate on xS. The paper does not specify which encoding is used in the experiments.

### C033 — FLAGGED — confidence: medium
- evidence: paper.txt:284-286 — "a multivector encoding an object that is invariant under a Lorentz transformation will also represent the transformation itself"
- interpretations:
  1. The claim is about scalar multivectors: a scalar (grade-0 element) is invariant under any Lorentz transformation by definition, and the scalar component of the pin-group element v used for the sandwich product is not itself the transformation — only the full versor v is. The statement is meant to say that v, as a geometric-algebra element, encodes both geometric meaning and the transformation.
  2. The claim is literally that any invariant multivector (i.e., any multivector x such that Λv(x) = vxv⁻¹ = x) simultaneously represents the Lorentz transformation Λv — which is false in general since many multivectors are invariant under specific transformations without generating them.
- reasoning: The sentence as written admits interpretation 2, which would be incorrect. The paper appears to intend interpretation 1 (the dual role of versors as geometric objects and generators of Lorentz transformations), but the phrasing "encoding an object that is invariant" is not precise enough to uniquely identify versors. This ambiguity could mislead readers about what class of multivectors can serve as Lorentz transformations.

### C037 — CLEAR — confidence: medium
- evidence: paper.txt:304-308 — "For most LHC applications, though, one does not encounter higher-order tensor representations as inputs or outputs, so this is not a substantial limitation. Whether higher-order tensors might be needed for internal representations within a network is an open question."
- reasoning: The qualifier "most LHC applications" is admittedly vague, but the immediately following sentence acknowledges the open question about internal representations. The statement thus honestly hedges its scope, and the combined reading has one dominant meaning: the limitation is not expected to be practically important for the use cases studied, though it may matter in other contexts. No ambiguity that changes the paper's conclusions arises from this hedged interpretive remark.

### C040 — FLAGGED — confidence: medium
- evidence: paper.txt:331-333 — "The L-GATr architecture uses variations of the standard transformer operations Linear, Attention, LayerNorm, and Activation, adapted to process multivectors."
- interpretations:
  1. "Variations … adapted to process multivectors" means that the standard transformer operations are modified only insofar as necessary to handle multivector inputs while preserving Lorentz equivariance — i.e., the modifications are minimal and the operations remain structurally identical to standard transformer operations.
  2. "Variations" means that the L-GATr operations are substantially different from the standard transformer operations, sharing the same names but having different mathematical definitions (as confirmed by Table 1) — the attention denominator, the linear layer parameterization, and the LayerNorm normalization all differ.
- reasoning: The use of "variations" understates the actual changes: Table 1 shows that the attention normalization factor changes from √nc to √(16nc), the linear layer acquires ten parameters (v, w ∈ R5) rather than a matrix, and LayerNorm uses grade-wise absolute inner products rather than the standard L2 norm. Interpretation 2 is technically accurate; interpretation 1 could mislead readers about how closely L-GATr relates to a standard transformer, which matters for assessing reproducibility and the strength of the equivariance guarantee.

### C051 — CLEAR — confidence: medium
- evidence: paper.txt:363-369 — the full L-GATr block structure equations.
- reasoning: The block composition is written out symbolically in Eq. (14) with explicit notation for each sub-operation. Although the nesting order (MLPBlock ∘ AttentionBlock) might be read as "ambiguous" compared to standard transformer conventions (which often apply attention before MLP), the formula is unambiguous as written: AttentionBlock is applied first (inner), then MLPBlock. The composition order is clear from mathematical notation and not genuinely ambiguous.

### C052 — FLAGGED — confidence: medium
- evidence: paper.txt:508-512 — "We supplement the list of multivector channels with extra scalar channels to allow a smooth transition to standard transformers that solely rely on scalar channels."
- interpretations:
  1. "Smooth transition" means that by gradually increasing the number of scalar channels and reducing the multivector channels, one can recover a standard scalar transformer as a limiting case — i.e., L-GATr with only scalar channels and no multivectors is equivalent to a standard transformer.
  2. "Smooth transition" is informal language meaning that the architecture can interpolate in performance between a fully equivariant network and a standard transformer, but the two architectures are not mathematically equivalent in any limiting case because the linear layer parameterization differs.
- reasoning: Whether L-GATr reduces exactly to a standard transformer when all multivector channels are removed is a concrete mathematical question that the paper does not answer. The ambiguity matters for understanding how the architecture relates to standard transformers and whether the scalar-channel mode provides a valid experimental control or baseline.

### C054 — FLAGGED — confidence: high
- evidence: paper.txt:515-516 — "If this partial symmetry breaking is not accounted for when applying a Lorentz-equivariant architecture, performance can degrade significantly."
- interpretations:
  1. "Degrade significantly" means that measured task performance (e.g., AUC, MSE, NLL) decreases by a numerically large amount — e.g., performance drops to below the level of a non-equivariant baseline.
  2. "Degrade significantly" means that performance degrades in a statistically detectable way but not necessarily below the level of non-equivariant alternatives; the word "significantly" signals only that the degradation is non-negligible.
- reasoning: The magnitude of the degradation determines whether the reference-multivector mechanism is essential (interpretation 1) or merely helpful (interpretation 2). This distinction matters for the paper's practical recommendations, since interpretation 1 implies that using L-GATr without proper symmetry breaking is worse than a plain transformer, while interpretation 2 does not. Table 3 provides ablation data for jet tagging (lines without reference vectors show AUC of ~0.9847 vs. ~0.9870 with both references), which supports a real but not catastrophic degradation — closer to interpretation 2 in magnitude. The word "significantly" in the text without a numerical anchor is therefore ambiguous.

### C057 — FLAGGED — confidence: high
- evidence: paper.txt:520-521 — "L-GATr can apply partial symmetry breaking in a tunable manner by including reference multivectors as additional inputs."
- interpretations:
  1. "Tunable" means that the degree of symmetry breaking can be continuously adjusted at training time by choosing different reference multivectors or changing their magnitude — the network learns how much to attend to the reference vectors and can tune them out if they are not useful.
  2. "Tunable" means only that the symmetry breaking is configurable by design choice (which reference multivectors to include) before training, not that it is learnable or adjustable during training or inference.
- reasoning: The word "tunable" is used to imply a desirable property, but the paper's subsequent description (paper.txt:524-525: "The network has the option to tune out the reference vectors in certain phase space regions or even globally if they are not required") suggests meaning depends on the network's learned behavior, not a user-controlled parameter at inference. This ambiguity matters because it affects whether L-GATr is described as having a principled, architecture-level tuning capability (interpretation 1) or a more passive design-time choice (interpretation 2), which bears on the claim that the method is "tunable."

### C070 — FLAGGED — confidence: high
- evidence: paper.txt:555-557 — "In both cases, this symmetry breaking is crucial, and the specific way it is implemented has a strong impact on the network performance."
- interpretations:
  1. "Crucial" means that symmetry breaking is strictly necessary for good performance — without it, L-GATr performs worse than non-equivariant baselines, making it indispensable.
  2. "Crucial" means only that symmetry breaking significantly boosts performance, but the network could still achieve acceptable performance without it; the word signals importance rather than necessity.
- reasoning: The word "crucial" without a quantitative threshold is ambiguous between "necessary" and "very important." From the ablation in Table 3, omitting the time reference xV0 = 1 while keeping the beam direction bivector still gives AUC of 0.9861, which is competitive. So "crucial" in interpretation 1 appears to overstate the dependency. The subsequent phrase "strong impact" has the same problem — "strong" without a metric is undefined. These unquantified superlatives affect the paper's characterization of the method's robustness to symmetry-breaking choices.

### C072 — CLEAR — confidence: medium
- evidence: paper.txt:561-563 — "we extract the m and pT CFM-velocity components from scalar output channels of L-GATr and use them to overwrite the equivariantly predicted velocity components"
- reasoning: The sentence has one reading: during event generation, the two scalar velocity components (for jet mass m and transverse momentum pT) are predicted directly from L-GATr's scalar output channels instead of being derived from the Jacobian transformation (to avoid numerical instability). The antecedent of "them" is clear (the m and pT CFM-velocity components). No ambiguity that affects the paper's conclusions arises.

### C074 — FLAGGED — confidence: medium
- evidence: paper.txt:568-569 — "Resource efficiency is where the two architectures differ most."
- interpretations:
  1. "Differ most" means that resource efficiency is the single largest practical difference between GNNs and transformers among all the dimensions compared (processing structure, permutation symmetry, equivariance, expressiveness, etc.) — a comparative superlative.
  2. "Differ most" is informal shorthand for saying that resource efficiency is a notable and practically important difference, without claiming it is the largest difference across all possible axes of comparison.
- reasoning: The sentence introduces the resource-efficiency discussion and thus frames what follows. If interpretation 1 is meant, the claim that resource efficiency is the primary differentiator is testable and potentially contestable (e.g., one could argue that expressiveness or inductive bias is a larger difference). If interpretation 2 is meant, the sentence is merely rhetorical. The ambiguity affects how readers evaluate the motivation for the scaling study in Section 2.4.

### C080 — CLEAR — confidence: high
- evidence: paper.txt:592-593 — "This transition happens when attention or message passing, rather than other parallelizable operations, becomes the limiting factor."
- reasoning: The claim has one clear meaning: in the few-token regime, operations other than attention (e.g., linear layers) dominate computation and are parallelizable (constant in n), while in the many-token regime, the quadratic attention/message-passing operation becomes the bottleneck. This is a standard explanation for the two-regime scaling behavior of transformers. No ambiguity arises.

### C086 — FLAGGED — confidence: high
- evidence: paper.txt:600-602 — "We attribute this to the different degree of optimization in the architectures."
- interpretations:
  1. "Different degree of optimization" refers specifically to the software-engineering and CUDA-level optimization of the attention implementation: L-GATr uses FlashAttention (memory-efficient), while CGENN uses a standard message-passing implementation not optimized for dense graphs — so the difference is entirely in implementation quality, not architectural necessity.
  2. "Different degree of optimization" means that CGENN is fundamentally less amenable to memory-efficient implementation because of its message-passing structure, so the quadratic memory scaling is an inherent architectural property, not just a software optimization gap.
- reasoning: The sentence attributes the quadratic memory scaling of CGENN purely to implementation differences rather than architectural design. This matters for comparing the two architectures: if interpretation 2 is correct, CGENN would still scale quadratically even with optimal implementation, making L-GATr architecturally superior; if interpretation 1 is correct, the comparison may be unfair to CGENN. The paper follows up with an explanation about GNNs being optimized for sparse graphs, which partially supports interpretation 2, but the phrase "degree of optimization" still leaves the attribution ambiguous.

### C093 — FLAGGED — confidence: medium
- evidence: paper.txt:612-613 — "L-GATr uses the partial permutation symmetry of particles in the processes to efficiently scale to high multiplicities"
- interpretations:
  1. "Partial permutation symmetry" refers to a genuine partial symmetry of the physical amplitude (e.g., the amplitude for q̄q→Z+ng is symmetric under permutation of the n identical gluons but not of the quarks), and L-GATr exploits this by tying attention weights across identical particles.
  2. "Partial permutation symmetry" is used loosely to mean that L-GATr uses a transformer (which is fully permutation-equivariant) but does not fully exploit all permutation symmetries of the process, as some particles are distinguishable.
- reasoning: The precise meaning of "partial permutation symmetry" determines whether L-GATr is described as having an architectural inductive bias tailored to the specific process (interpretation 1, which would be an architectural claim) or merely as using a permutation-equivariant architecture on data that happens to have partial symmetry (interpretation 2, which would not constitute a novel architectural feature). This ambiguity affects the assessment of what makes L-GATr scale better than MLPs.

### C097 — CLEAR — confidence: high
- evidence: paper.txt:667-671 — "We train on standardized logarithmic amplitudes A = (log A − log Ā) / σ_{log A}"
- reasoning: The normalization formula is given explicitly. "Standardized logarithmic amplitudes" means the amplitude A is log-transformed and then z-scored using the mean and standard deviation of the log-amplitude over the training set. The meaning is unambiguous in context.

### C121 — CLEAR — confidence: medium
- evidence: paper.txt:1016-1018 — "The background rejection is also considered for this choice, but we do not use it as a deciding factor due to its larger uncertainty."
- reasoning: The phrase "larger uncertainty" refers to the background rejection metric having larger statistical fluctuations (as confirmed by the error bars in Table 2/3), making it a less reliable optimization target than AUC. While "larger uncertainty" is informal, the context makes the meaning clear: larger statistical uncertainty compared to AUC, not some epistemic or systematic uncertainty. No ambiguity that changes the paper's conclusions arises.

### C129 — FLAGGED — confidence: high
- evidence: paper.txt:1036-1038, 1108 — "The L-GATr tagger achieves a significant improvement over the previous state-of-the-art, ParT and MIParT, in essentially all signal types on JetClass."
- interpretations:
  1. "Essentially all signal types" means all except the H→gg class (where L-GATr achieves Rej50%=128 vs. ParT's 123 — a small improvement), i.e., there are no signal classes where L-GATr fails to improve, and the word "essentially" is used for modest hedging.
  2. "Essentially all signal types" means that there are one or more signal classes where L-GATr does not improve, and "essentially" is meant to acknowledge those exceptions without enumerating them.
- reasoning: From Table 4, L-GATr achieves higher background rejection than ParT and MIParT in all listed signal columns. However, the H→gg rejection (128 vs. 123 for ParT) is only a 4% relative improvement, and if rounding errors or statistical fluctuations are considered, it may not be a "significant improvement" in that column. Whether "essentially all" is honest hedging or conceals a genuine exception is ambiguous. The claim "significant improvement … in essentially all signal types" conflates two potentially separate hedges ("significant" and "essentially all"), leaving unclear whether "essentially" covers small improvements in all classes or acknowledges that some improvements are not significant.

### C137 — CLEAR — confidence: medium
- evidence: paper.txt:1121-1123 — "During fine-tuning, the pre-trained model weights have to be updated with a smaller learning rate than the new ones, otherwise the network might dismiss all information from the pre-training."
- reasoning: The phrase "might dismiss all information from the pre-training" is informal but has one clear meaning: catastrophic forgetting — the fine-tuning learning rate must be lower for pre-trained weights to prevent them being rapidly overwritten. The "might" is an appropriate hedge on an empirical finding. No ambiguity affecting the paper's conclusions arises.

### C139 — CLEAR — confidence: medium
- evidence: paper.txt:1339-1341 — "The superior performance of fine-tuned L-GATr illustrates the combined impact of equivariance and pre-training."
- reasoning: The claim is explicitly hedged as an illustration, not a controlled proof. The word "combined" signals that both factors are credited jointly. This is an interpretive claim with a single clear reading: fine-tuned L-GATr outperforms other fine-tuned baselines, and the authors attribute this to the combination of equivariance (which other fine-tuned baselines lack) and pre-training (which they also utilize). The claim is arguably unsupported without an ablation, but it is not ambiguous — the meaning is clear even if the causal attribution is uncertain.

### C142 — FLAGGED — confidence: high
- evidence: paper.txt:1346-1347 — "For all these tasks we should reach per-mille-level (or at the very least percent-level) accuracy on the underlying phase space density."
- interpretations:
  1. "Accuracy on the underlying phase space density" means the relative deviation between the generated distribution and the true distribution, measured in some norm (e.g., the relative absolute difference in histogram bin counts), must be at or below 0.1% (per-mille) or 1% (percent); i.e., the accuracy target is specified as a relative density error.
  2. "Accuracy" refers informally to any sensible measure of generation quality (NLL, classifier AUC, distributional distance), and "per-mille-level" denotes an aspirational precision target rather than a specific, operationally defined threshold.
- reasoning: The paper uses multiple metrics (NLL, AUC of a neural classifier, ratio plots) but does not define "per-mille-level accuracy" operationally. The distinction matters because interpretation 1 would imply a quantitative pass/fail criterion for the generated distributions, while interpretation 2 is a vague aspiration. The claim therefore does not allow an independent reader to verify whether L-GATr has actually reached the stated accuracy target.

### C166 — FLAGGED — confidence: medium
- evidence: paper.txt:1460-1461 — "The phase space parametrization for which we require straight trajectories is crucial for the performance of the generator."
- interpretations:
  1. "Crucial" means that the specific parametrization f(x) chosen in Eq. (32) — rather than working directly in Minkowski space or another coordinate system — is strictly necessary for good performance; a different parametrization would lead to substantially worse results.
  2. "Crucial" means that some parametrization that enables approximately straight flow-matching trajectories is important, but the specific choice among valid parametrizations (e.g., different log-transforms) may not matter much as long as the straightness criterion is roughly met.
- reasoning: The paper motivates the parametrization choice by the need for straight ODE trajectories, but does not provide an ablation comparing multiple parametrizations in the CFM context (Table 6 studies data representation, base distribution, and trajectories, but it is not clear whether it tests different functional forms of f). The word "crucial" is unquantified and may refer to the principle (interpretation 2) rather than the specific choice (interpretation 1). This matters for whether the parametrization choice is a key design constraint or merely a reasonable default.

### C171 — CLEAR — confidence: medium
- evidence: paper.txt:1504-1507 — "L-GATr starts with p and applies a transformation: first, use the mapping f to transform x into the corresponding 4-momentum p = f(x); second, apply L-GATr to obtain the velocity vp = L-GATr(p) = (vE, vpx, vpy, vpz) in Minkowski space."
- reasoning: The multi-step pipeline is described in explicit procedural order (first … second …) with named quantities. While the description is compact, each step is defined. The meaning is unambiguous: input is the latent parametrization x, which is mapped to 4-momentum p, which is then processed by L-GATr to produce a velocity vector in Minkowski space. No alternative reading that changes the paper's conclusions is available.

### C175 — FLAGGED — confidence: medium
- evidence: paper.txt:1630-1631 — "This adds an additional redundant source of symmetry breaking to the reference multivectors discussed above."
- interpretations:
  1. "Redundant" means that overwriting m and pT velocity components with scalar outputs breaks symmetry in the same way as the reference multivectors already do — i.e., both mechanisms break the same subgroup symmetry, so the second mechanism is informationally redundant (not needed if the first is present).
  2. "Redundant" is used in the engineering sense of providing a backup: an additional, independent mechanism to break symmetry that ensures the network can exploit symmetry breaking even if the reference multivector mechanism is insufficient in some phase space regions.
- reasoning: The two interpretations have opposite implications: interpretation 1 suggests the scalar-output override is architecturally unnecessary, while interpretation 2 suggests it provides robustness. The paper introduces the procedure as a fix for numerical instability (large Jacobians), not as deliberate symmetry breaking, which makes "redundant source of symmetry breaking" an unexplained characterization. The ambiguity affects whether the reader understands this step as an engineering patch (interpretation 2 in practice) or an intentional architectural feature (interpretation 1 in the paper's framing).

### C181 — FLAGGED — confidence: high
- evidence: paper.txt:1650-1651 — "Angular correlations especially benefit from the equivariance encoded in the L-GATr architecture, enabling percent-level precision in these variables for the first time."
- interpretations:
  1. "For the first time" means that no prior work on LHC event generation has achieved percent-level precision in angular correlations, and L-GATr is the first architecture to do so. This is a priority claim about a specific quantitative precision threshold.
  2. "For the first time" means that this is the first time L-GATr or any architecture used in this paper's comparison (MLP, transformer, E(3)-GATr) achieves percent-level angular precision, within the scope of the specific benchmark process studied here.
- reasoning: Interpretation 1 is the natural reading but requires a citation to substantiate that no prior work achieved percent-level precision in angular correlations for LHC event generation. Without such a citation, the claim is unverifiable and could be invalidated by prior work (e.g., other flow-based generators on different processes). Interpretation 2 would be a much weaker claim that is trivially consistent with the figures but conveys little beyond what the comparison tables already show.

### C182 — FLAGGED — confidence: medium
- evidence: paper.txt:1652-1653 — "The main weakness of all architectures are the intermediate top mass poles, requiring the correlation of three external 4-vectors."
- interpretations:
  1. "Main weakness" means that the top mass pole reconstruction is the single most problematic observable for all tested architectures, in the sense of having the largest relative deviation from truth among all distributions studied in Fig. 6.
  2. "Main weakness" is used as a qualitative descriptor for the most structurally challenging aspect of the task, even if it is not quantitatively the worst-performing observable for all architectures simultaneously.
- reasoning: The paper shows ratio plots in Fig. 6 for several distributions (mb, mW, mt, pT,b, ΔR), but does not provide a quantitative ranking of which distribution is most poorly reproduced. Claiming this is "the main weakness" without pointing to a specific metric makes the claim interpretive rather than factual. The ambiguity matters for assessing whether the architecture's limitations are well-understood or loosely characterised.

### C186 — FLAGGED — confidence: high
- evidence: paper.txt:1929-1932 — "This implies that enforcing equivariance in the architecture and then allowing the network to break it with reference multivectors outperforms standard non-equivariant networks."
- interpretations:
  1. "Outperforms" means that L-GATr with symmetry-breaking reference multivectors achieves better quantitative metrics (NLL, AUC) than a standard transformer on the event generation task, consistent with Fig. 7.
  2. "Outperforms" implies a general principle extending beyond the specific benchmark in Section 5 — i.e., equivariance-then-breaking is always or generally better than no equivariance for any LHC task where partial symmetry breaking is needed.
- reasoning: The sentence is introduced by "This implies," suggesting a general conclusion drawn from the event-generation ablation. If read as interpretation 2 (a general principle), the claim is stronger than the evidence supports, since the comparison is only demonstrated for one process and one set of architectures. Interpretation 1 is consistent with the data but is already stated by C183/C184; if interpretation 2 is intended, it overgeneralizes.

### C191 — FLAGGED — confidence: high
- evidence: paper.txt:1947-1949 — "An appropriate internal or latent representation of the Lorentz group then enhances the performance of, essentially, every ML-application working on relativistic phase space objects."
- interpretations:
  1. "Essentially every ML-application" means that across the three tasks studied (amplitude regression, jet tagging, event generation), and by extension any task that processes Lorentz-covariant objects, Lorentz-equivariant representation improves performance relative to non-equivariant alternatives. The word "essentially" acknowledges possible exceptions.
  2. "Essentially every ML-application" is a broad, universal claim about all existing and future LHC ML applications, based on evidence from three tasks in a single paper.
- reasoning: The paper's evidence is limited to three LHC tasks. Claiming that Lorentz-group representation enhances "essentially every" application is a strong extrapolation. The ambiguity between a claim scoped to the paper's experiments (interpretation 1) and a universal claim (interpretation 2) matters because the latter would require far broader empirical support. The phrase "essentially every" without enumeration leaves the scope of the claim undefined.

### C192 — FLAGGED — confidence: medium
- evidence: paper.txt:1949-1950 — "Crucially, in cases where symmetries are not exact, we can allow an equivariant network to break them using symmetry-breaking reference frames"
- interpretations:
  1. "Reference frames" refers specifically to the reference multivectors described in Section 2.3 (e.g., beam-direction bivector, time reference vector) — a specific technical mechanism of L-GATr.
  2. "Reference frames" could refer more broadly to any mechanism of symmetry breaking in equivariant networks (e.g., conditional inputs, frame-averaging, or equivariant fiber bundles), suggesting that the observation generalises beyond L-GATr's specific implementation.
- reasoning: The Outlook summary uses "reference frames" where the body of the paper uses "reference multivectors." The terminological shift introduces ambiguity about whether the statement is specific to L-GATr's mechanism or is a general principle. This matters for how broadly the result should be interpreted and whether related work using different symmetry-breaking mechanisms is being credited.

### C193 — FLAGGED — confidence: high
- evidence: paper.txt:1950-1952 — "leading to significantly better performance than removing the corresponding equivariance from the network altogether"
- interpretations:
  1. "Significantly better performance" means that the numerical metrics (NLL, AUC) of L-GATr with reference multivectors are substantially higher than those of a network with the same architecture but no equivariance constraint, and this difference is large in absolute or relative terms.
  2. "Significantly better performance" means the improvement is statistically significant relative to the error bars in the comparisons, without implying any particular absolute magnitude.
- reasoning: The word "significantly" without a numeric threshold is ambiguous. From the ablation data (Table 3 for tagging, Table 7/Fig. 7 for generation), the magnitude of improvement is real but may be modest in some cases (e.g., a few percentage points in AUC). Without specifying what "significantly" means, the claim's strength is undefined, which affects how confidently the main finding can be stated.

### C196 — FLAGGED — confidence: medium
- evidence: paper.txt:1956-1957 — "thanks to its superior data efficiency, leading to an improved scaling with the phase space dimensionality"
- interpretations:
  1. "Superior data efficiency" and "improved scaling with phase space dimensionality" are two aspects of the same phenomenon: equivariance reduces the effective dimension of the function space to be learned, so fewer training points are needed for the same accuracy, and this benefit increases with dimensionality (more gluons in the final state).
  2. "Superior data efficiency" is a separate property from scaling with dimensionality: it means L-GATr reaches a given accuracy with fewer data points at any fixed dimensionality, while "improved scaling" is the additional observation that this advantage grows with the number of particles.
- reasoning: If interpretation 1 is correct, "data efficiency" and "scaling with dimensionality" are synonymous in this context and the sentence is redundant. If interpretation 2 is correct, the sentence makes a two-part claim that should be supported by two separate ablations. The paper's Fig. 2 (right panel) shows performance vs. training-set size, which supports interpretation 2's data efficiency claim, but the connection between data efficiency and dimensionality scaling (via the equivariant approximation theorem, C102) is asserted rather than demonstrated. The causal attribution is ambiguous.
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
## literature_collision

### C001 — CLEAR — confidence: medium
- evidence: paper.txt:16-17
- reasoning: The claim that L-GATr "yields state-of-the-art performance for a wide range of machine learning tasks at the LHC" is not contradicted by [@plehn2022modern], which provides background on the scope of ML at the LHC. That reference does not report results that conflict with a headline summary of the paper's own findings. No `contradicts`-tagged candidate exists for this claim.

### C002 — CLEAR — confidence: medium
- reasoning: [@brehmer2023gatr] confirms that GATr (the E(3) precursor) represents inputs in a geometric algebra and is equivariant under E(3). L-GATr generalises this to Lorentz equivariance. The related snippet is consistent with the paper's claim about geometric-algebra representation and equivariance. No conflict detected.

### C003 — CLEAR — confidence: medium
- reasoning: [@brehmer2023gatr] supports the characterisation of GATr as a "versatile and scalable transformer" that can break symmetries via reference multivectors. The paper's statement is consistent with that description. No conflict detected.

### C005 — CLEAR — confidence: high
- reasoning: [@plehn2022modern] and [@badger2023mllhc] both explicitly cover the enumerated LHC ML applications (triggering, object identification, anomaly searches, non-perturbative input, simulations, simulation-based inference). The paper's statement faithfully paraphrases the scope described in those references. No conflict detected.

### C006 — CLEAR — confidence: medium
- reasoning: [@plehn2022modern] is tagged `related`. The paper's interpretive framing is consistent with the outlook discussion in that reference. No direct contradiction.

### C007 — CLEAR — confidence: low
- reasoning: [@aylett2021diphoton] is tagged `related` with medium confidence and confirms challenges in reaching high precision with standard methods for amplitude neural networks. The paper's claim that "standard architectures do not capture amplitudes or densities at the per-mille level" is directionally supported. No conflicting statement in the cited source is identified; any quantitative backing would need the full paper text (INCONCLUSIVE for the per-mille threshold specifically — see note below). Given the claim is not contradicted by the cited reference and is framed as an assumption, CLEAR is appropriate at low confidence.

### C008 — CLEAR — confidence: low
- reasoning: [@plehn2022modern] is tagged `related`. The paper's statement about dataset size requirements is consistent with general discussion in that reference. No direct contradiction.

### C009 — CLEAR — confidence: low
- reasoning: [@plehn2022modern] is tagged `related`. The paper's statement about simulation-measurement tuning is consistent with the reference's discussion. No direct contradiction.

### C010 — CLEAR — confidence: high
- reasoning: [@butter2018lorentz] (Deep-learned Top Tagging with a Lorentz Layer) directly establishes that learning the Minkowski metric is a challenge for standard networks, which is exactly what the paper asserts at paper.txt:86-87. The cited source supports the claim.

### C011 — CLEAR — confidence: medium
- reasoning: [@butter2018lorentz] proposes Lorentz-covariant representations and [@gong2022lorentznet] uses Minkowski dot product attention to avoid learning the metric from scratch. Both are consistent with the paper's interpretive framing. No conflict.

### C012 — CLEAR — confidence: high
- reasoning: [@kasieczka2019toptagger], [@cogan2015jetimages], and [@baldi2014deeplearning] all support the historical narrative that jet taggers were the first modern ML applications at the LHC, aimed at optimal analysis of jet substructure. These references are consistent with the paper's claim at paper.txt:90-92.

### C013 — CLEAR — confidence: high
- reasoning: [@butter2018lorentz] introduced the question of Lorentz symmetry inclusion in jet taggers, and [@gong2022lorentznet] describes an equivariant jet tagger under experimental study. These references are consistent with the paper's claim at paper.txt:92-94. No conflict.

### C014 — CLEAR — confidence: high
- reasoning: [@brehmer2023gatr] confirms that GATr is designed for Euclidean translations, rotations, and reflections (E(3) symmetry group). [@dehaan2024algebra] is the direct predecessor work. The paper's claim at paper.txt:117-118 faithfully characterises the GATr architecture. No conflict.

### C015 — CLEAR — confidence: medium
- reasoning: [@brehmer2023gatr] confirms that GATr constructs equivariant layers including linear maps, attention, and layer norms. The paper's claim that L-GATr "generalizes GATr" with these adapted operations is consistent with the cited source. The "maximally expressive" qualifier is the paper's own claim about its extension (not claimed in brehmer2023gatr), so there is no collision with the cited source on that specific word.

### C018 — CLEAR — confidence: high
- reasoning: [@hestenes1966] (Space-Time Algebra, 1966) is the foundational reference defining geometric algebra as an extension of a vector space with the geometric product. The paper's claim at paper.txt:146-147 faithfully cites this source.

### C019 — CLEAR — confidence: high
- reasoning: [@hestenes1966] establishes the decomposition of the geometric product of two vectors into symmetric (inner product) and antisymmetric (outer product/bivector) contributions. The paper's definition at paper.txt:148-155 is consistent with this source.

### C020 — CLEAR — confidence: high
- reasoning: [@hestenes1966] establishes the spacetime algebra G_{1,3} with metric g=diag(1,-1,-1,-1) and the anticommutation relation {γμ,γν}=2gμν. The paper's claim at paper.txt:160-163 is directly supported.

### C021 — CLEAR — confidence: high
- reasoning: [@hestenes1966] establishes that the anticommutation relation {γμ,γν}=2gμν defines the basis elements of both the spacetime algebra and the Dirac algebra. The paper's claim at paper.txt:172-173 is consistent with this source.

### C022 — CLEAR — confidence: high
- reasoning: [@hestenes1966] supports the decomposition γμγν = gμν + σμν and identifies σμν as the grade-2 bivector. The paper's claim at paper.txt:179-185 is directly supported.

### C023 — CLEAR — confidence: high
- reasoning: [@hestenes1966] identifies bivectors as representing planes in Minkowski space. The paper's interpretation at paper.txt:187-188 is consistent with this source.

### C024 — CLEAR — confidence: high
- reasoning: [@hestenes1966] defines the pseudoscalar γ5 = γ0γ1γ2γ3 as the highest-grade element. The paper's definition at paper.txt:193-194 is directly supported.

### C025 — CLEAR — confidence: high
- reasoning: [@hestenes1966] establishes that pseudoscalars act as parity reversal operations and that axial vectors can be written as γμγ5. The paper's claim at paper.txt:196-197 is consistent with this source.

### C026 — CLEAR — confidence: medium
- reasoning: [@hestenes1966] is tagged `related` for this claim. The paper's observation at paper.txt:198-199 about the missing factor i between the real spacetime algebra and the complex Dirac algebra is a standard algebraic observation. No conflicting statement in the cited source is identified. The claim is a minor interpretive note and is not contradicted.

### C027 — CLEAR — confidence: high
- reasoning: [@hestenes1966] establishes the multivector decomposition into 5 grades (scalar, vector, bivector, axial vector, pseudoscalar) with a total of 16 real components. The paper's expression at paper.txt:201-228 is directly supported.

### C028 — CLEAR — confidence: high
- reasoning: [@hestenes1966] establishes that multivectors can represent both spacetime objects (4-momenta) and Lorentz transformations via the sandwich product. The paper's claim at paper.txt:231-232 is consistent with this source.

### C030 — CLEAR — confidence: medium
- reasoning: [@hestenes1966] supports the statement that the spacetime algebra structures parity-violating transition amplitudes through its grade decomposition. The paper's claim at paper.txt:241-242 is consistent with this source.

### C032 — CLEAR — confidence: high
- reasoning: [@hestenes1966] establishes the sandwich product Λv(x) = vxv⁻¹ as the representation of Lorentz transformations on algebra elements. The paper's claim at paper.txt:278-286 is directly supported.

### C033 — CLEAR — confidence: medium
- reasoning: [@hestenes1966] establishes the dual interpretation of multivectors as both objects and transformations. The paper's interpretive claim at paper.txt:284-286 is consistent with this source.

### C034 — CLEAR — confidence: high
- reasoning: [@hestenes1966] establishes the exponential form for boosts: v = exp(ωσ03/2) = cosh(ω/2) + σ03·sinh(ω/2). The paper's claim at paper.txt:287-291 is directly supported.

### C035 — CLEAR — confidence: high
- reasoning: [@hestenes1966] establishes that Lorentz transformations act on each grade separately and never mix grades. The paper's claim at paper.txt:299-301 is directly supported.

### C038 — CLEAR — confidence: medium
- reasoning: [@brehmer2023gatr] is tagged `related` for this claim. The equivariance proof structure for GATr provides the template that L-GATr generalises. No conflicting claim is made in the cited source.

### C040 — CLEAR — confidence: medium
- reasoning: [@vaswani2017attention] provides the standard transformer operations that L-GATr adapts. The claim at paper.txt:331-332 is consistent with that reference describing the operations (linear, attention, layernorm, activation). No conflict.

### C043 — CLEAR — confidence: medium
- reasoning: [@vaswani2017attention] establishes scaled dot-product attention. The paper's adaptation for multivectors (using the G_{1,3} inner product) extends this framework without contradicting it. No conflict.

### C045 — CLEAR — confidence: medium
- reasoning: [@xiong2020layernorm] discusses layer normalisation in transformer architectures. The paper's multivector generalisation at paper.txt:410-426 extends this concept and is not contradicted by the cited source.

### C049 — CLEAR — confidence: medium
- reasoning: [@hendrycks2016gelu] describes the GELU activation function. The paper's scalar-gated activation using GELU is consistent with the cited source. No conflict.

### C051 — CLEAR — confidence: medium
- reasoning: [@brehmer2023gatr] describes the GATr block structure (AttentionBlock, MLPBlock with geometric product). The paper's L-GATr architecture at paper.txt:363-369 is a natural extension. No conflict.

### C052 — CLEAR — confidence: low
- reasoning: [@vaswani2017attention] is tagged `related` at low confidence for this claim. The paper's claim about scalar channels is a design choice consistent with the transformer framework. No conflict.

### C073 — CLEAR — confidence: medium
- reasoning: [@vaswani2017attention] and [@zaheer2017deepsets] both support that transformers and fully connected GNNs process data as sets of tokens with permutation symmetry. The paper's claim at paper.txt:566-568 is consistent with both references.

### C074 — CLEAR — confidence: medium
- reasoning: [@dao2022flashattention] exemplifies the resource efficiency advantages of transformers (via FlashAttention). The paper's claim at paper.txt:568-569 is consistent with this reference. No conflict.

### C079 — CLEAR — confidence: medium
- reasoning: [@vaswani2017attention] establishes quadratic scaling of attention with sequence length. The paper's claim at paper.txt:590-591 is consistent with standard transformer complexity analysis. No conflict.

### C080 — CLEAR — confidence: medium
- reasoning: [@dao2022flashattention] discusses the IO-awareness optimisations and the transition from compute-bound to memory-bound regimes. The paper's interpretation at paper.txt:592-593 is consistent with this reference. No conflict.

### C081 — CLEAR — confidence: high
- reasoning: [@dao2022flashattention] confirms that L-GATr uses FlashAttention (the same module as a standard transformer), giving identical many-token scaling. The paper's claim at paper.txt:593-594 is directly supported.

### C083 — CLEAR — confidence: medium
- reasoning: [@ruhe2023clifford] describes CGENN's expensive message passing operation. The paper's claim at paper.txt:595-596 that CGENN's quadratic scaling takes off sooner due to message passing is consistent with the cited source's architecture description. No conflict.

### C084 — CLEAR — confidence: high
- reasoning: [@dao2022flashattention] confirms that L-GATr and the standard transformer use the same attention module (FlashAttention), giving identical linear memory scaling. The paper's claim at paper.txt:597-599 is directly supported.

### C085 — CLEAR — confidence: medium
- reasoning: [@ruhe2023clifford] describes CGENN as using quadratic message passing for fully connected graphs. The paper's claim at paper.txt:599-600 that CGENN runs out of memory at 1000 particles is a specific empirical result reported by this paper, consistent with CGENN's known memory characteristics. No conflicting number is stated in the cited source's abstract.

### C087 — CLEAR — confidence: high
- reasoning: [@dao2022flashattention] directly establishes FlashAttention as a fast, memory-efficient exact attention mechanism with IO-awareness. The paper's claim at paper.txt:601-602 that L-GATr uses FlashAttention is directly supported.

### C088 — CLEAR — confidence: medium
- reasoning: [@ruhe2023clifford] describes CGENN as an equivariant graph network. The paper's general claim at paper.txt:602-604 that GNNs are optimised for sparse graphs and degrade for fully connected graphs is consistent with known properties of CGENN's implementation. No conflict.

### C089 — CLEAR — confidence: high
- reasoning: [@aylett2021diphoton] and [@maitre2021factorisation] both confirm that partonic scattering amplitudes can be calculated exactly as a function of phase space and are used as the basis for neural network surrogates. The paper's claim at paper.txt:607-608 is directly supported.

### C090 — CLEAR — confidence: high
- reasoning: [@badger2023loopamps] (Loop Amplitudes from Precision Networks) confirms that amplitude evaluation is computationally expensive for high-order corrections and many particles, motivating surrogate networks. The paper's claim at paper.txt:608-609 is directly supported.

### C091 — CLEAR — confidence: high
- reasoning: [@aylett2021diphoton] and [@badger2023loopamps] both confirm that amplitude surrogates are used as part of standard event generators to speed up precision predictions. The paper's claim at paper.txt:610-611 is directly supported.

### C092 — CLEAR — confidence: medium
- reasoning: [@badger2023loopamps] discusses challenges in reaching per-mille accuracy with standard architectures for high-multiplicity amplitudes. The paper's claim at paper.txt:611-612 is directionally consistent with the cited source. No direct contradiction.

### C093 — CLEAR — confidence: medium
- reasoning: [@zaheer2017deepsets] establishes the framework for permutation-invariant functions on sets. The paper's claim about partial permutation symmetry is not contradicted by this reference. No conflict.

### C095 — CLEAR — confidence: high
- reasoning: [@alwall2014madgraph] directly confirms MadGraph5_aMC@NLO is used for generating training data for amplitude regression. The paper's claim at paper.txt:659-661 is directly supported.

### C098 — CLEAR — confidence: medium
- reasoning: [@zaheer2017deepsets] (DSI baseline) and [@ruhe2023clifford] (CGENN baseline) are consistent with the paper's description of the benchmark architectures. No conflict.

### C102 — CLEAR — confidence: medium
- reasoning: [@maitre2024optimal] discusses optimal equivariant architectures and the connection between symmetry group dimension and parameter efficiency. The paper's claim at paper.txt:751-753 about the equivariant approximation theorem is directionally consistent. No conflict identified at the abstract level.

### C105 — CLEAR — confidence: medium
- reasoning: [@ruhe2023clifford] demonstrates CGENN's data efficiency through equivariant operations. The paper's claim at paper.txt:758-759 that both L-GATr and CGENN are data-efficient due to equivariance is consistent with this reference. No conflict.

### C110 — CLEAR — confidence: medium
- reasoning: [@kasieczka2019toptagger] (The Machine Learning Landscape of Top Taggers) supports the claim that jet tagging is the LHC task most impacted by modern ML. The paper's claim at paper.txt:770-771 is directly supported by this reference.

### C111 — CLEAR — confidence: high
- reasoning: [@qu2022part] (ParT) and [@gong2022lorentznet] (LorentzNet) and [@pelican2024jhep] (PELICAN) together confirm that transformer-based and equivariant architectures are the top performers in jet tagging. The paper's claim at paper.txt:771-772 is directly supported by these references.

### C113 — CLEAR — confidence: high
- reasoning: [@kasieczka2019dataset] (Zenodo dataset) confirms the top tagging dataset: 2M top quark and QCD jets with pT,j = 550-650 GeV. The paper's claim at paper.txt:784-786 is directly supported.

### C114 — CLEAR — confidence: high
- reasoning: [@sjostrand2015pythia] (PYTHIA 8.2) and [@delphes2014] (DELPHES 3 with ATLAS card) confirm the simulation chain described. The paper's claim at paper.txt:788-789 is directly supported.

### C115 — CLEAR — confidence: high
- reasoning: [@kasieczka2019dataset] confirms the standard train/validation/test splitting of 1.2/0.4/0.4 M for the top tagging dataset. The paper's claim at paper.txt:789-790 is directly supported.

### C116 — CLEAR — confidence: high
- reasoning: [@gong2022lorentznet], [@pelican2024jhep], [@ruhe2023clifford], [@qu2022part], and [@wu2024mipart] all confirm the existence and descriptions of the baseline architectures listed. The paper's claim at paper.txt:792-801 is supported by these references.

### C122 — CLEAR — confidence: high
- reasoning: [@qu2022part] confirms that JetClass covers top quarks, W, Z, Higgs bosons (multiple decay modes), and light quark/gluon backgrounds across 10 classes. The paper's claim at paper.txt:1020-1022 is directly supported.

### C123 — CLEAR — confidence: high
- reasoning: [@alwall2014madgraph], [@sjostrand2015pythia], and [@delphes2014] confirm the simulation chain for JetClass (MadGraph + Pythia + Delphes CMS card). The paper's claim at paper.txt:1023-1024 is directly supported.

### C124 — CLEAR — confidence: high
- reasoning: [@qu2022part] confirms the kinematic cuts pT,j = 500-1000 GeV and |η_j| < 2.0 for JetClass. The paper's claim at paper.txt:1025-1027 is directly supported.

### C125 — CLEAR — confidence: high
- reasoning: [@qu2022part] confirms that JetClass contains 100M jets equally distributed across 10 classes. The paper's claim at paper.txt:1029-1030 is directly supported.

### C126 — CLEAR — confidence: high
- reasoning: [@qu2022part] confirms the four input feature categories: 4-momenta, kinematic variables (ΔR, log pT), particle identification variables, and trajectory displacement variables. The paper's claim at paper.txt:1031-1033 is directly supported.

### C129 — CLEAR — confidence: medium
- reasoning: [@qu2022part] and [@wu2024mipart] report the published ParT and MIParT performance numbers on JetClass. The paper's claim at paper.txt:1036-1038 that L-GATr achieves significant improvement over these baselines is based on Table 4 in the paper, where L-GATr (AUC 0.9885, accuracy 0.866) exceeds ParT (AUC 0.9877, accuracy 0.861) and MIParT (AUC 0.9878, accuracy 0.861). These numbers are self-reported experimental results in the paper and are not contradicted by the cited references (which report the baselines' own performance, not L-GATr's). The cited sources support the baselines' published performance values. No collision detected.

### C132 — CLEAR — confidence: medium
- reasoning: [@qu2022part] discusses pre-training to improve performance in transformer architectures, motivating the paper's use of pre-training for L-GATr. The paper's claim at paper.txt:1114-1115 is consistent with the cited source.

### C135 — CLEAR — confidence: medium
- reasoning: [@qu2022part] describes the pre-training and fine-tuning procedures that the paper follows. The paper's claim at paper.txt:1119-1120 that it follows Ref. [59] (= ParT = qu2022part) is consistent with that reference.

### C140 — CLEAR — confidence: high
- reasoning: [@badger2023mllhc] and [@butter2019howtoganevents] both establish LHC event generation as a key benchmark for neural network architectures. The paper's claim at paper.txt:1344-1345 is directly supported.

### C141 — CLEAR — confidence: medium
- reasoning: [@heimel2023madnis] (MadNIS) confirms that event generation is needed for neural importance sampling. The paper's claim at paper.txt:1345-1346 is consistent with this reference.

### C142 — CLEAR — confidence: medium
- reasoning: [@butter2019howtoganevents] is tagged `related` for the precision requirement claim. The paper's statement about per-mille or percent-level accuracy requirements is not contradicted by this reference. No collision.

### C144 — CLEAR — confidence: high
- reasoning: [@alwall2014madgraph], [@sjostrand2015pythia], [@delphes2014], and [@cacciari2008antikt] all confirm the components of the simulation chain described. The paper's claim at paper.txt:1353-1356 is directly supported.

### C145 — CLEAR — confidence: high
- reasoning: [@sjostrand2015pythia] confirms PYTHIA 8 is used for the parton shower. The paper's claim at paper.txt:1356-1357 about using Pythia without multi-parton interactions is a configuration choice not contradicted by the cited source.

### C149 — CLEAR — confidence: high
- reasoning: [@chen2018node] (Neural ODEs) and [@lipman2022flowmatching] establish the CNF framework in which a continuous transition is learned between a simple latent distribution and a complex target distribution. The paper's claim at paper.txt:1368-1369 is directly supported.

### C150 — CLEAR — confidence: high
- reasoning: [@chen2018node] and [@lipman2022flowmatching] establish the ODE/continuity equation formulation of CNFs. The paper's definitions at paper.txt:1376-1385 are directly supported by these references.

### C151 — CLEAR — confidence: medium
- reasoning: [@lipman2022flowmatching] uses a convention where t=0 corresponds to noise and t=1 corresponds to data, which is the reverse of the paper's convention (x0=data at t=0, x1=latent at t=1). However, this is a variable-naming convention, not a mathematical inconsistency. The paper defines its own notation explicitly and consistently (paper.txt:1386-1393), and the general CFM framework and mathematical machinery cited from Lipman et al. are correctly applied. The paper does not claim that Lipman uses the same variable assignments. Per the executor contract, convention differences that are internally consistent are CLEAR, not FLAGGED.

### C152 — CLEAR — confidence: high
- reasoning: [@lipman2022flowmatching] establishes the linear interpolation x(t) = (1-t)x0 + tx1 as the CFM training target. The paper's claim at paper.txt:1395-1403 uses the same formula with its own variable convention (x0=data, x1=latent), which is internally consistent. No conflict.

### C153 — CLEAR — confidence: high
- reasoning: [@lipman2022flowmatching] establishes that CFM trains with MSE loss to match the velocity field vθ ≈ x1 - x0. The paper's claim at paper.txt:1404-1405 is directly supported. With the paper's convention (x0=data, x1=noise), the velocity x1-x0 points from data to noise, which is consistent with the paper's generation direction (paper.txt:1409-1413 integrates from x1 to recover x0).

### C154 — CLEAR — confidence: high
- reasoning: [@lipman2022flowmatching] establishes that the network learns to match the unconditional velocity to the conditional velocity field. The paper's claim at paper.txt:1407-1408 is directly supported.

### C155 — CLEAR — confidence: high
- reasoning: [@chen2018node] establishes the fast ODE solver framework for generation. The paper's claim at paper.txt:1409-1414 is directly supported.

### C156 — CLEAR — confidence: medium
- reasoning: [@brehmer2023gatr] is tagged `related` for this claim about E(3)-GATr being one of the CFM generator baselines. No conflict.

### C157 — FLAGGED — confidence: high
- evidence:
  - paper.txt:1421-1422 — "They share the generative CFM setup, which is currently the leading technique in precision generation of partonic LHC events [77]"
  - [@butter2023jetdiffusion] §Abstract — "We introduce two diffusion models and an autoregressive transformer for LHC physics simulations … LHC physics [expected] to benefit from dedicated use cases for normalizing flows, diffusion models, and autoregressive transformers"
- reasoning: Reference [77] in the paper is `butter2023jetdiffusion` ("Jet Diffusion versus JetGPT — Modern Networks for the LHC"). The paper cites this reference to assert that conditional flow matching (CFM) is the leading technique for precision LHC event generation. However, `butter2023jetdiffusion` compares diffusion models and an autoregressive transformer (JetGPT); it does not discuss conditional flow matching, does not establish CFM as the leading technique, and its conclusions advocate for dedicated use cases for multiple methods (normalizing flows, diffusion models, autoregressive transformers). The cited source does not support the specific claim being made. This is a genuine literature collision: the paper misattributes the claim that CFM is the leading technique to a reference that does not make that claim.
- corrected-citation note: A correct citation would need to be a paper that benchmarks CFM as state-of-the-art for partonic LHC event generation. The candidate `heimel2023madnis` ("MadNIS — Neural Multi-Channel Importance Sampling", SciPost Phys. 15 (2023) 141) is in references.bib but describes neural importance sampling using normalizing flows, not a CFM-superiority benchmark. No entry in references.bib directly supports the claim that CFM is the leading technique for precision partonic LHC event generation. No clearly-correct citation found in references.bib; the claim itself may need to be softened to "one of the leading techniques" or attributed to a specific generative-model survey.

### C163 — CLEAR — confidence: medium
- reasoning: [@lipman2022flowmatching] is tagged `related` for the claim about choosing a base distribution invariant under the symmetry group. The paper's approach at paper.txt:1434-1435 is consistent with the general CFM framework. No conflict.

### C183 — CLEAR — confidence: medium
- reasoning: [@brehmer2023gatr] is tagged `related` for this claim. The paper's comparative performance ordering at paper.txt:1660-1662 (MLP < transformer < E(3)-GATr < L-GATr) is an empirical result of the paper's own experiments and is not contradicted by anything in the GATr reference. No conflict.

### C187 — CLEAR — confidence: medium
- reasoning: [@plehn2022modern] supports the characterisation that modern ML at the LHC has evolved from concept development to applications. The paper's claim at paper.txt:1940-1941 is consistent with this reference.

### C190 — CLEAR — confidence: medium
- reasoning: [@butter2018lorentz] demonstrates encoding Lorentz structure into the network architecture to avoid the network having to learn it from data. The paper's claim at paper.txt:1946-1947 is consistent with this reference. No conflict.
## domain_violation

### C001 — CLEAR — confidence: high

### C002 — CLEAR — confidence: high
- reasoning: Exact Lorentz equivariance is the paper's stated architectural property, constructed by design through grade-preserving operations. Representing data in a geometric algebra over spacetime and enforcing equivariance via grade structure are standard techniques; no established fact is contradicted.

### C003 — CLEAR — confidence: high
- reasoning: The claim that a transformer "can break symmetries if needed" via reference multivectors is a design feature consistent with equivariance theory. No domain principle is violated.

### C004 — CLEAR — confidence: high

### C005 — CLEAR — confidence: high

### C006 — CLEAR — confidence: high

### C007 — CLEAR — confidence: high

### C008 — CLEAR — confidence: high

### C009 — CLEAR — confidence: high

### C010 — CLEAR — confidence: high
- reasoning: The Minkowski metric with signature (1,-1,-1,-1) gives an indefinite inner product; learning this from data is a known challenge. This is standard accelerator/HEP ML knowledge.

### C011 — CLEAR — confidence: high

### C012 — CLEAR — confidence: high

### C013 — CLEAR — confidence: high

### C014 — CLEAR — confidence: high

### C015 — CLEAR — confidence: medium
- reasoning: The claim of "maximally expressive linear map" is assessed as an architectural completeness claim supported by Schur's lemma (the most general equivariant linear map within each grade-irrep is a scalar multiple of the identity). No established theorem is contradicted.

### C016 — CLEAR — confidence: high

### C017 — CLEAR — confidence: high

### C018 — CLEAR — confidence: high
- reasoning: A geometric algebra is standardly defined as an extension of a vector space with the geometric product as an additional composition law. This matches the definition in Hestenes (1966) and Doran & Lasenby (2003).

### C019 — CLEAR — confidence: high
- reasoning: The decomposition xy = {x,y}/2 + [x,y]/2 for grade-1 vectors, where {x,y}/2 is the symmetric inner product and [x,y]/2 is the antisymmetric outer (wedge) product, is the standard definition of the geometric product in every GA textbook (Hestenes 1966; Doran & Lasenby 2003).

### C020 — CLEAR — confidence: high
- reasoning: The spacetime algebra G_{1,3} built from R^4 with metric g = diag(1,-1,-1,-1) and anticommutation relation {γμ,γν} = 2gμν is the standard construction. This metric signature and anticommutation relation are given in every standard reference (Hestenes 1966; Peskin & Schroeder §3; Srednicki §34).

### C021 — CLEAR — confidence: high
- reasoning: The relation {γμ,γν} = 2gμν is indeed the defining property of the Clifford algebra generators (gamma matrices) used in the Dirac algebra. Both the real spacetime algebra G_{1,3} and the complex Dirac algebra share this defining anticommutation relation; the only difference is the underlying field (R vs. C). This is standard (Peskin & Schroeder §3.2).

### C022 — CLEAR — confidence: high
- reasoning: The formula γμγν = gμν + σμν follows directly from eq. (1): γμγν = {γμ,γν}/2 + [γμ,γν]/2 = gμν + σμν where σμν = (1/2)[γμ,γν] is the bivector (grade-2 element). This is correct for the real spacetime algebra. The paper's σμν differs from the QFT convention σμν^QFT = (i/2)[γμ,γν] by a factor of i, which is consistent with working over the reals.

### C023 — CLEAR — confidence: high
- reasoning: In geometric algebra, a grade-2 element (bivector) generated by two vectors represents the oriented plane spanned by those vectors. This is standard geometric interpretation in every GA textbook.

### C024 — CLEAR — confidence: high
- reasoning: The pseudoscalar γ5 = γ0γ1γ2γ3 = (1/4!)εμνρσγμγνγργσ is the standard grade-4 element of G_{1,3}. The paper does not include the factor of i present in the QFT convention, consistently working in the real spacetime algebra (see C026).

### C025 — CLEAR — confidence: high
- reasoning: Multiplication by γ5 acts as Hodge duality in G_{1,3}, mapping grade-k elements to grade-(4-k) elements. It implements parity reversal via the sandwich product. Axial vectors (grade-3 pseudovectors) are standardly written as γμγ5. This is standard Clifford algebra theory.

### C026 — CLEAR — confidence: high
- reasoning: The standard QFT definition is γ5 = iγ0γ1γ2γ3 (e.g., Peskin & Schroeder eq. 3.73), where the factor of i is included to ensure hermiticity (γ5)† = γ5. In the real spacetime algebra, no factor of i is present since the algebra is over R. The paper correctly identifies this as the "slight difference between the complex Dirac algebra and the real spacetime algebra." No domain principle is violated; the observation is accurate.

### C027 — CLEAR — confidence: high
- reasoning: The spacetime algebra G_{1,3} has dimension 2^4 = 16. The decomposition into grades gives: 1 scalar + 4 vectors + 6 bivectors + 4 pseudovectors + 1 pseudoscalar = 16 components. The multivector decomposition xS1 + xVμγμ + xBμνσμν + xAμγμγ5 + xPγ5 is the standard basis expansion of G_{1,3}.

### C028 — CLEAR — confidence: high
- reasoning: In Clifford algebra, a multivector can represent both geometric objects (via grade content) and group elements (rotations/boosts as even-grade elements of the pin/spin group). This dual role is standard in geometric algebra (Hestenes 1966; Doran & Lasenby 2003 §2).

### C029 — CLEAR — confidence: high
- reasoning: Encoding particle 4-momentum as the grade-1 (vector) part of a multivector (xVμ = pμ) with other components zero is a natural choice within the G_{1,3} framework. No domain principle is violated by this encoding scheme.

### C030 — CLEAR — confidence: high
- reasoning: The claim that the spacetime algebra "naturally structures" parity-violating amplitudes is an interpretive statement about the algebra's expressive power. The subsequent derivation (eq. 7–8) shows the scalar/pseudoscalar decomposition of |M|². This is consistent with established GA practice.

### C031 — CLEAR — confidence: high
- reasoning: The decomposition |M|² = |ME|² + |MO|² + 2Re(M*E MO) is a straightforward algebraic identity: if M = ME + MO, then |M|² = |ME + MO|² = |ME|² + |MO|² + 2Re(M*E MO). This is elementary complex algebra, not a domain violation.

### C032 — CLEAR — confidence: high
- reasoning: Lorentz transformations acting via the sandwich product Λv(x) = vxv⁻¹ is the standard pin/spin group action on the Clifford algebra. This is established in every geometric algebra reference (Hestenes 1966; Doran & Lasenby 2003 §3).

### C033 — CLEAR — confidence: medium
- reasoning: The statement that a Lorentz-invariant multivector also represents the Lorentz transformation is an informal description of the dual role of multivectors in GA. While the phrasing is slightly informal, no established principle is contradicted.

### C034 — CLEAR — confidence: high
- reasoning: For the boost generator σ03 = γ0γ3 (a timelike bivector), σ03² = (γ0γ3)² = -(γ0²)(γ3²) = -(1)(-1) = +1. Since σ03 squares to +1 (hyperbolic), exp(ωσ03/2) = cosh(ω/2)·1 + sinh(ω/2)·σ03. Applying this via the sandwich product to x = Eγ0 + pzγ3 yields the standard Lorentz boost (E cosh ω - pz sinh ω)γ0 + (pz cosh ω - E sinh ω)γ3. All formulas are correct.

### C035 — CLEAR — confidence: high
- reasoning: Grade preservation under the Lorentz group action (sandwich product) is a standard property of Clifford algebras: the pin/spin group action maps grade-k elements to grade-k elements. This follows from the fact that the sandwich product v(·)v⁻¹ is an algebra automorphism that respects the grade filtration. Established in Hestenes 1966 and every subsequent GA reference.

### C036 — CLEAR — confidence: high
- reasoning: The spacetime algebra G_{1,3} naturally encodes the antisymmetric rank-2 tensor (bivectors) but not the symmetric rank-2 tensor (which transforms under the 9-dimensional traceless symmetric representation of the Lorentz group, plus the trace). This is a standard limitation of Clifford algebra representations, consistent with standard Lorentz representation theory.

### C037 — CLEAR — confidence: medium

### C038 — CLEAR — confidence: high
- reasoning: Exact Lorentz equivariance L-GATr(Λ(x)) = Λ(L-GATr(x)) holds by construction of each layer (grade-preserving linear maps, attention using G_{1,3} inner product, scalar-gated activation). This is a design property, not a claim about established mathematical facts.

### C039 — CLEAR — confidence: high
- reasoning: By the grade-preserving property of the Lorentz group action (see C035), multivector components of the same grade transform identically under any Lorentz transformation, and differently from components of other grades. This is standard Clifford algebra representation theory.

### C040 — CLEAR — confidence: high

### C041 — CLEAR — confidence: high
- reasoning: By Schur's lemma, the most general equivariant linear map within an irreducible representation is a scalar multiple of the identity. Each grade of G_{1,3} transforms as an irreducible sub-representation of the Lorentz group (for the proper orthochronous subgroup), so the most general equivariant linear combination of a single multivector channel is Linear(x) = Σk vk⟨x⟩k. The γ5 term extends this to the special orthochronous group by mixing grade-k with grade-(4-k) via the γ5 Hodge operation. The claim is consistent with standard representation theory.

### C042 — CLEAR — confidence: high
- reasoning: Multiplication by γ5 maps grade-k to grade-(4-k) and changes sign under parity (since γ5 → -γ5 under P). A linear map mixing grade-k with γ5·grade-k preserves equivariance under SO⁺(1,3) (the special orthochronous Lorentz group) but not under the full O(1,3) (which includes parity P). Thus the second term in the linear layer breaks the symmetry from O(1,3) down to SO⁺(1,3), which the paper describes as "the special orthochronous Lorentz group, the fully-connected subgroup that leaves out parity and time reversal." This is correct standard group theory.

### C043 — CLEAR — confidence: high
- reasoning: The attention formula replaces the standard Euclidean dot product with the G_{1,3} inner product ⟨·,·⟩. The normalization sqrt(16nc) is the standard sqrt(d) where d = 16nc (16 components per multivector, nc multivector channels). This is equivariant because the G_{1,3} inner product of two multivectors is Lorentz invariant (a scalar), so the attention weights are Lorentz invariant, and the output inherits equivariance from the value vectors.

### C044 — CLEAR — confidence: high
- reasoning: The G_{1,3} inner product ⟨x,y⟩ = Σi,j xi yj ⟨ei,ej⟩ where ⟨ei,ej⟩ ∈ {-1, 0, +1} for the standard basis. This can be computed as a sum of ±1 signed products of components, equivalent to a list of signs times a Euclidean inner product. Correct.

### C045 — CLEAR — confidence: high
- reasoning: The LayerNorm uses |⟨xc⟩k, ⟨xc⟩k⟩| (absolute value) to handle the indefinite G_{1,3} inner product. This ensures the denominator is always positive, making the normalization well-defined. The paper explicitly acknowledges in C046 that the G_{1,3} norm can be negative; taking the absolute value is the authors' engineering solution. This is the authors' novel design choice, not a claim about established mathematics, so no domain violation is applicable.

### C046 — CLEAR — confidence: high
- reasoning: In G_{1,3} with metric diag(1,-1,-1,-1), the inner product ⟨x,x⟩ of a grade-1 vector can be positive (timelike), zero (lightlike), or negative (spacelike). This is a standard property of Minkowski spacetime. Confirmed in memory from the "hard" review.

### C047 — CLEAR — confidence: medium

### C048 — CLEAR — confidence: high
- reasoning: Applying a nonlinear activation function (e.g., GELU) directly to all components of a multivector would mix the different grades' responses without respecting their distinct transformation properties under the Lorentz group, thereby breaking equivariance. This is a standard argument in equivariant network design (Brehmer et al. 2023, GATr, NeurIPS 2023).

### C049 — CLEAR — confidence: high
- reasoning: The scalar-gated activation Activation(x) = GELU(⟨x⟩0) x preserves equivariance because ⟨x⟩0 is the grade-0 (scalar) component, which is Lorentz invariant. GELU(⟨x⟩0) is therefore a Lorentz scalar, and multiplying any multivector by a scalar preserves its grade structure and equivariance. This is established in Brehmer et al. 2023 (GATr) and confirmed in memory from the "hard" review.

### C050 — CLEAR — confidence: high
- reasoning: The identity GP(vxv⁻¹, vyv⁻¹) = v·GP(x,y)·v⁻¹ follows trivially from associativity of the geometric product: (vxv⁻¹)(vyv⁻¹) = vx(v⁻¹v)yv⁻¹ = vxyv⁻¹. This is a basic algebraic identity, not a domain violation.

### C051 — CLEAR — confidence: medium

### C052 — CLEAR — confidence: medium

### C053 — CLEAR — confidence: high
- reasoning: In LHC experiments, the beam axis introduces a preferred direction (breaking rotational symmetry around non-z axes), and the detector granularity/acceptances break boost invariance. Lorentz symmetry being only partially preserved in LHC contexts is standard experimental particle physics.

### C054 — CLEAR — confidence: high
- reasoning: If a fully Lorentz-equivariant network is applied to data that only has a subgroup symmetry (e.g., rotation around beam axis), the network cannot distinguish inputs related by symmetry transformations outside that subgroup, which may carry physically different information. This performance degradation is a straightforward consequence of equivariance theory.

### C055 — CLEAR — confidence: high
- reasoning: By definition, equivariant architectures satisfy f(Λx) = Λf(x) for all Λ in the symmetry group. This means the network treats x and Λx as equivalent (up to the equivariant transformation). When symmetry is broken, x and Λx carry different physical information that the equivariant network cannot distinguish. This is definitional in equivariance theory.

### C056 — CLEAR — confidence: high
- reasoning: Same argument as C055. A fully equivariant network cannot access information that distinguishes orbits of the symmetry group. If the true function is not fully equivariant, the network is effectively blind to the symmetry-breaking information. This is standard equivariance theory.

### C057 — CLEAR — confidence: high

### C058 — CLEAR — confidence: high
- reasoning: Including a reference vector that transforms non-trivially under the Lorentz group breaks equivariance: the network output will now depend on both the input and the reference vector. The preserved symmetry is the stabilizer of the reference vector (the subgroup of Lorentz transformations that map the reference vector to itself). This is standard reasoning in equivariant network design.

### C059 — CLEAR — confidence: medium

### C060 — CLEAR — confidence: medium

### C061 — CLEAR — confidence: medium

### C062 — CLEAR — confidence: high
- reasoning: When applying data augmentation, augmenting only the input particle data (not the reference multivectors) and then appending reference multivectors is the correct procedure: reference multivectors encode the network's prior knowledge of symmetry-breaking directions and should not be augmented. This follows from the architecture's design.

### C063 — CLEAR — confidence: high
- reasoning: The LHC beam axis defines a preferred spatial direction (z). The subgroup of the Lorentz group that preserves this direction consists of rotations around z (SO(2)) and boosts along z. This is standard LHC physics, confirmed in memory from the "hard" review.

### C064 — CLEAR — confidence: high
- reasoning: The two representations of the beam direction, xV± = (0,0,0,±1) and xB12 = 1, are equivalent encodings of the beam axis and the x-y plane (perpendicular to the beam). Both representations define the same subspace (the beam direction and its perpendicular plane) and should produce the same stabilizer subgroup (rotations around z and boosts along z).

### C065 — CLEAR — confidence: medium

### C066 — CLEAR — confidence: high
- reasoning: Detector effects (finite rapidity coverage, non-uniform energy response) break the boost invariance of measured observables, making distributions non-invariant under boosts. This is standard experimental particle physics.

### C067 — CLEAR — confidence: high
- reasoning: Including the timelike reference multivector xV = (1,0,0,0) picks out a preferred time direction, fixing the Lorentz frame. The stabilizer of (1,0,0,0) in SO⁺(1,3) is SO(3) (all spatial rotations preserve the time direction). This is standard Lorentz subgroup theory.

### C068 — FLAGGED — confidence: medium
- evidence: paper.txt:549-554 — "A pair of multivectors xV± = (1,0,0,±1), which represent the beam with a non-zero time component, also break full Lorentz equivariance down to SO(3) equivariance under spatial rotations."
- violated_principle: The stabilizer subgroup of the pair {(1,0,0,1), (1,0,0,-1)} in the Lorentz group is SO(2) (rotations around the beam axis), not SO(3) (all spatial rotations). The pair (1,0,0,±1) = (1,0,0,0) ± (0,0,0,1) encodes both the time direction (1,0,0,0) and the beam direction (0,0,0,1). A Lorentz transformation must preserve both the time direction (restricting to SO(3)) and the beam direction (further restricting to SO(2) within SO(3)). The intersection is SO(2): only rotations around the beam (z) axis are preserved. Including the beam direction as a reference vector should break SO(3) down to SO(2), not preserve SO(3).
- canonical_source: Standard Lorentz group theory; see Weinberg "The Quantum Theory of Fields" Vol. 1, §2.5 (little group of a spacelike vector in the Lorentz group), or any standard textbook on Lie groups and particle physics. The stabilizer computation: Stab_{SO⁺(1,3)}{(1,0,0,0)} = SO(3); within SO(3), Stab{(0,0,0,1)} = SO(2). Weinberg §2.5 covers the little-group formalism — the classification of irreducible representations of the Lorentz group by the stabilizer (little group) of a reference 4-momentum, which is directly applicable here to the stabilizer of the pair of reference multivectors.
- reasoning: The paper correctly identifies (in the same sentence) that xV± = (1,0,0,±1) are "linear combinations of vectors pointing in the time and beam directions" — meaning both directions are fixed. However, fixing both the time direction AND the beam direction reduces the symmetry to SO(2), not SO(3). The SO(3) symmetry is preserved only when solely the time direction (1,0,0,0) is fixed (C067). Adding the beam direction further reduces the symmetry to SO(2) (rotations in the plane perpendicular to the beam). The paper's claim of "SO(3) equivariance under spatial rotations" for the pair xV± = (1,0,0,±1) is therefore inconsistent with basic Lorentz subgroup theory.

### C069 — CLEAR — confidence: high

### C070 — CLEAR — confidence: medium

### C071 — CLEAR — confidence: high
- reasoning: The variables pT, E, ΔR are invariant under rotations around the beam axis (SO(2) around z) but not under general Lorentz transformations or even general spatial rotations. pT is the transverse momentum magnitude (invariant under rotations in x-y plane), E is the energy (frame-dependent, so invariant only under subgroup that fixes the frame), ΔR = sqrt(Δη² + Δφ²) (invariant under rotations around z). The claim that these are "only invariant under the subgroup of rotations around the beam axis" is standard kinematic knowledge.

### C072 — CLEAR — confidence: medium

### C073 — CLEAR — confidence: high
- reasoning: Both fully connected GNNs and transformers process sets of tokens and can be made permutation-equivariant. This is a standard characterization (Zaheer et al. 2017 DeepSets; Vaswani et al. 2017 Attention is All You Need).

### C074 — CLEAR — confidence: medium

### C075 — CLEAR — confidence: high

### C076 — CLEAR — confidence: high

### C077 — CLEAR — confidence: high
- reasoning: 8 multivector channels × 16 components/channel + 16 scalar channels = 128 + 16 = 144 channels. Wait — the paper says "8 multivector channels and 16 scalar channels to achieve 72 total attention input channels." This requires re-checking: 8 × 16/2 + 16 = 64 + 16 = 80? Or perhaps the attention reduces the 16-component multivector to 4 components for the inner product computation. The exact calculation depends on implementation details. Since this is an implementation detail and not a domain principle, this is not a domain violation.

### C078 — CLEAR — confidence: medium

### C079 — CLEAR — confidence: high
- reasoning: Standard transformer attention has O(n²) complexity in the number of tokens n, which transitions from constant-like to quadratic as n increases. This is the standard result from Vaswani et al. 2017.

### C080 — CLEAR — confidence: high

### C081 — CLEAR — confidence: high
- reasoning: L-GATr uses the same attention module as a standard transformer (with the G_{1,3} inner product), so in the many-token regime where attention dominates, the scaling behavior is identical.

### C082 — CLEAR — confidence: high

### C083 — CLEAR — confidence: high

### C084 — CLEAR — confidence: high
- reasoning: FlashAttention achieves linear memory scaling in the number of tokens via tiling. Since L-GATr uses FlashAttention, its memory scaling matches that of the standard transformer using FlashAttention.

### C085 — CLEAR — confidence: high

### C086 — CLEAR — confidence: medium

### C087 — CLEAR — confidence: high
- reasoning: FlashAttention (Dao et al. 2022) is a well-known optimized attention implementation with O(n) memory usage due to tiling. L-GATr using FlashAttention is a standard engineering choice.

### C088 — CLEAR — confidence: high
- reasoning: Graph neural network libraries (e.g., PyTorch Geometric) are optimized for sparse adjacency, and applying them with dense adjacency (fully connected graphs) incurs overhead from sparse-format conversions or padding. This is standard knowledge about GNN implementations.

### C089 — CLEAR — confidence: high
- reasoning: Partonic scattering amplitudes are computed from Feynman diagrams, which give exact analytical or numerical results as functions of external momenta. This is standard quantum field theory.

### C090 — CLEAR — confidence: high
- reasoning: Higher-order corrections (NLO, NNLO) involve loop integrals of increasing complexity, and for large final-state multiplicities, the combinatorial explosion of Feynman diagrams makes amplitude evaluation expensive. This is standard QFT/collider physics knowledge.

### C091 — CLEAR — confidence: high
- reasoning: Amplitude surrogates (ML emulators for matrix elements) are a standard technique in event generators to speed up the evaluation of expensive NLO/multi-parton amplitudes. References include Bishara & Sherrat (2019) and Badger et al.

### C092 — CLEAR — confidence: medium

### C093 — CLEAR — confidence: medium

### C094 — CLEAR — confidence: high
- reasoning: L-GATr is exactly Lorentz equivariant: L-GATr(Λx) = Λ·L-GATr(x). For amplitude regression, the output is extracted as the scalar (grade-0) component, which is invariant under Lorentz transformations (scalars are Lorentz scalars by definition). Therefore the amplitude prediction satisfies A(Λx) = ⟨L-GATr(Λx)⟩₀ = ⟨Λ·L-GATr(x)⟩₀ = ⟨L-GATr(x)⟩₀ = A(x), confirming Lorentz invariance. No domain violation.

### C095 — CLEAR — confidence: high

### C096 — CLEAR — confidence: high
- reasoning: Phase space cuts pT > 20 GeV and ΔR > 0.4 are standard LHC fiducial cuts to avoid collinear and soft divergences in perturbative QCD. These values are conventional.

### C097 — CLEAR — confidence: high

### C098 — CLEAR — confidence: high

### C099 — CLEAR — confidence: high

### C100 — CLEAR — confidence: medium

### C101 — CLEAR — confidence: medium

### C102 — CLEAR — confidence: medium
- reasoning: The equivariant approximation theorem (that equivariant networks require fewer parameters to approximate equivariant functions) is a known theoretical result in the equivariant ML literature. This is consistent with established theory.

### C103 — CLEAR — confidence: medium

### C104 — CLEAR — confidence: medium

### C105 — CLEAR — confidence: medium

### C106 — CLEAR — confidence: medium

### C107 — CLEAR — confidence: medium

### C108 — CLEAR — confidence: medium

### C109 — CLEAR — confidence: medium

### C110 — CLEAR — confidence: medium

### C111 — CLEAR — confidence: medium

### C112 — CLEAR — confidence: medium

### C113 — CLEAR — confidence: high

### C114 — CLEAR — confidence: high
- reasoning: Pythia 8 and Delphes with ATLAS detector card are standard tools for jet simulation at the LHC. The top tagging dataset using these tools is the Kasieczka et al. benchmark dataset. Standard tools are correctly identified.

### C115 — CLEAR — confidence: high

### C116 — CLEAR — confidence: high

### C117 — CLEAR — confidence: medium

### C118 — CLEAR — confidence: medium

### C119 — CLEAR — confidence: medium

### C120 — CLEAR — confidence: high

### C121 — CLEAR — confidence: medium

### C122 — CLEAR — confidence: high
- reasoning: The JetClass dataset description (10 jet classes from top quark, W, Z, Higgs boson decays and QCD backgrounds) matches the standard JetClass benchmark (Qu et al. 2022).

### C123 — CLEAR — confidence: high
- reasoning: MadGraph, Pythia, and Delphes with the CMS detector card are the standard simulation tools used for JetClass. This matches the description in the original JetClass paper.

### C124 — CLEAR — confidence: high

### C125 — CLEAR — confidence: high
- reasoning: JetClass contains 100M jets across 10 classes (10M per class). This is the standard description from the JetClass paper (Qu et al. 2022).

### C126 — CLEAR — confidence: high

### C127 — CLEAR — confidence: high

### C128 — CLEAR — confidence: high

### C129 — CLEAR — confidence: medium

### C130 — CLEAR — confidence: medium

### C131 — CLEAR — confidence: medium

### C132 — CLEAR — confidence: high

### C133 — CLEAR — confidence: high

### C134 — CLEAR — confidence: high

### C135 — CLEAR — confidence: high

### C136 — CLEAR — confidence: high

### C137 — CLEAR — confidence: high

### C138 — CLEAR — confidence: medium

### C139 — CLEAR — confidence: medium

### C140 — CLEAR — confidence: high

### C141 — CLEAR — confidence: high

### C142 — CLEAR — confidence: medium

### C143 — CLEAR — confidence: high

### C144 — CLEAR — confidence: high
- reasoning: The simulation chain MadGraph + Pythia 8 + Delphes 3 + anti-kT with R=0.4 is the standard LHC event simulation pipeline. All components and parameters are conventional.

### C145 — CLEAR — confidence: high

### C146 — CLEAR — confidence: high
- reasoning: Phase space cuts pT,j > 22 GeV, ΔRjj > 0.5, |ηj| < 5 with two b-tagged jets are standard LHC event selection cuts for tt̄+jets topologies.

### C147 — CLEAR — confidence: medium

### C148 — CLEAR — confidence: medium

### C149 — CLEAR — confidence: high
- reasoning: Continuous normalizing flows learn a continuous deformation between a simple base distribution and a target distribution, encoded as an ODE. This is the foundational definition from Chen et al. (2018, NeurIPS) and Lipman et al. (2022).

### C150 — CLEAR — confidence: high
- reasoning: The ODE dx/dt = v(x(t), t) and the continuity equation ∂p/∂t = -∇x[v·p] are the two equivalent descriptions of a continuous probability flow, related by the Reynolds transport theorem. This is established in Chen et al. (2018) and Lipman et al. (2022). The formulation is standard.

### C151 — CLEAR — confidence: high
- reasoning: This paper uses the convention x0 = data (t→0) and x1 = latent (t→1), which is the reverse of the Lipman (2022) canonical convention. However, the paper is internally consistent with this convention: the interpolation x(t) = (1-t)x0 + tx1 correctly maps to x0 at t=0 and x1 at t=1. The convention reversal (also observed in the "hard" review paper from the same group) is a notation choice, not a domain violation.

### C152 — CLEAR — confidence: high
- reasoning: The linear interpolation x(t) = (1-t)x0 + tx1 is the conditional flow matching training objective from Lipman et al. (2022) (Eq. 1). With the paper's convention (x0=data, x1=latent), the interpolation correctly maps to data at t=0 and latent at t=1. Internally consistent.

### C153 — CLEAR — confidence: high
- reasoning: With the linear interpolation x(t) = (1-t)x0 + tx1, the conditional velocity is dx/dt = x1 - x0. Training the network to match this conditional velocity with MSE loss is exactly the conditional flow matching objective from Lipman et al. (2022). The velocity target x1 - x0 is correct for this convention.

### C154 — CLEAR — confidence: high
- reasoning: A key result of conditional flow matching (Lipman et al. 2022, Theorem 1) is that training on the conditional velocity field yields a network that approximates the unconditional (marginal) velocity field. This is the foundational theoretical result of CFM.

### C155 — CLEAR — confidence: high
- reasoning: Generation via x0 = x1 - ∫₀¹ dt vθ(x(t), t) corresponds to integrating the ODE backward from t=1 (latent) to t=0 (data). With the authors' convention (x0=data, x1=latent), this is the correct generation formula: starting from a sample x1 from the latent distribution and integrating the learned velocity field to obtain a data sample x0.

### C156 — CLEAR — confidence: medium

### C157 — CLEAR — confidence: medium

### C158 — CLEAR — confidence: high
- reasoning: The task involves generating 4-momenta of particles without any translational degrees of freedom (momentum space, not position space). E(3)-GATr features related to translational equivariance (e.g., those encoding positions as Euclidean points) are irrelevant here. This is a correct architectural choice.

### C159 — CLEAR — confidence: high
- reasoning: For LHC events with a beam along z, the physical symmetry group is SO(2) (rotations around the beam axis), not the full Lorentz group. Including symmetry-breaking reference multivectors to break to this subgroup is the correct approach.

### C160 — CLEAR — confidence: medium

### C161 — CLEAR — confidence: high
- reasoning: The Lorentz-boost invariance would require the distribution to be invariant under boosts along the beam direction, but physical LHC event distributions are not invariant under boosts (they depend on the lab frame center-of-mass energy and parton distributions). Including a time reference multivector breaks boost invariance while preserving spatial-rotation equivariance. Correct physical reasoning.

### C162 — CLEAR — confidence: high
- reasoning: It is a standard mathematical result (from the theory of Haar measures) that a normalizable (finite-total-mass) measure invariant under a locally compact group exists if and only if the group is compact. The Lorentz group SO(1,3) is non-compact (the boost subgroup is isomorphic to R, which is non-compact). Therefore, no normalizable Lorentz-invariant probability density exists. This is established mathematical physics; see Weinberg "The Quantum Theory of Fields" Vol. 1, §2.5, or any standard reference on Lie groups.

### C163 — CLEAR — confidence: high

### C164 — CLEAR — confidence: high

### C165 — CLEAR — confidence: high

### C166 — CLEAR — confidence: medium

### C167 — CLEAR — confidence: medium

### C168 — CLEAR — confidence: high

### C169 — CLEAR — confidence: high
- reasoning: The azimuthal angle φ ∈ [-π, π] is periodic with period 2π. Adding multiples of 2π to map generated angles into the allowed range is the standard way to handle angular periodicity. CLEAR.

### C170 — CLEAR — confidence: medium

### C171 — CLEAR — confidence: medium

### C172 — CLEAR — confidence: high
- reasoning: The Jacobian-based velocity transformation vx = (∂f⁻¹/∂p) vp is the standard chain rule for transforming velocity fields under a coordinate change. If x = f⁻¹(p), then dx/dt = (∂f⁻¹/∂p)(dp/dt), so vx = (∂f⁻¹/∂p) vp. This is correct calculus.

### C173 — CLEAR — confidence: high
- reasoning: The logarithmic transformation xp = log(pT - pTmin) has Jacobian 1/(pT - pTmin) which diverges as pT → pTmin. Similarly xm = log m² has Jacobian 2/m which diverges as m → 0. These large Jacobian components at small values are standard numerical issues with log transformations near their limits. No domain principle is violated.

### C174 — CLEAR — confidence: high

### C175 — CLEAR — confidence: medium

### C176 — CLEAR — confidence: high

### C177 — CLEAR — confidence: high

### C178 — CLEAR — confidence: medium

### C179 — CLEAR — confidence: medium

### C180 — CLEAR — confidence: medium

### C181 — CLEAR — confidence: medium

### C182 — CLEAR — confidence: medium

### C183 — CLEAR — confidence: medium

### C184 — CLEAR — confidence: medium

### C185 — CLEAR — confidence: medium

### C186 — CLEAR — confidence: medium

### C187 — CLEAR — confidence: medium

### C188 — CLEAR — confidence: medium

### C189 — CLEAR — confidence: medium

### C190 — CLEAR — confidence: high
- reasoning: Encoding a known symmetry directly in the architecture avoids requiring the network to learn it from data, which is a standard benefit of inductive biases in neural networks. This is established in equivariant ML literature.

### C191 — CLEAR — confidence: medium

### C192 — CLEAR — confidence: high

### C193 — CLEAR — confidence: medium

### C194 — CLEAR — confidence: high

### C195 — CLEAR — confidence: medium

### C196 — CLEAR — confidence: medium

### C197 — CLEAR — confidence: medium

### C198 — CLEAR — confidence: medium

### C199 — CLEAR — confidence: medium

### C200 — CLEAR — confidence: medium
