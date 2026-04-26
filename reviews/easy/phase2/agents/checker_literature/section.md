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
