# Phase 2 Strategy — noah-test-v1
**Paper:** "A Lorentz-Equivariant Transformer for All of the LHC" (L-GATr, arXiv:2312.07897)

---

## Preamble

418 prose claims assessed (545 total; 33 equations, 17 captions, 77 table_cell skipped; 9 table-as-prose and 1 fragment deprioritized per FINDINGS.md). Importance breakdown: **high 64**, **medium 142**, **low 212**. The most prevalent error categories are `unreferenced` (dominant across motivation and performance claims lacking inline citations) and `ambiguous` (vague quantifiers like "significant improvement", "best performance", "per-mille level" with no metric definition). `literature_collision` is the third-ranked risk: LorentzNet, PELICAN, CGENN, and ParT are the principal competitors and are absent from the literature bank, so any claim that characterizes their performance or places L-GATr ahead of them must be verified against external retrieval only. `internal_contradiction` is a moderate risk around numerical consistency between tables, the abstract, and the Outlook. `domain_violation` is the lowest risk — the spacetime algebra exposition is standard, but two specific claims about grade mixing and the Dirac/spacetime algebra relationship warrant checking. Paper-specific caution: the "first Lorentz-equivariant generative network" priority claim (claim-0007) is a novelty assertion that directly invites `literature_collision`. The fine-tuned L-GATr top-tagging results (claim-0281) are marked "(new)" and have no external support yet. Checkers should note that claims 0346 and 0352 carry a `2c` LaTeX artifact prefix; claims 0514–0515 are split table rows; claim-0066 is a fragment.

---

## Strategy Table

| claim_id | importance | checkability | categories | rationale |
|----------|------------|--------------|------------|-----------|
| claim-0001 | low | low | ambiguous | Paper title only; not a factual claim requiring verification. |
| claim-0002 | low | low | unreferenced | Author list; no factual claim. |
| claim-0003 | low | low | unreferenced | Affiliation list; no factual claim. |
| claim-0004 | high | high | unreferenced, internal_contradiction | Core contribution claim: "state-of-the-art performance for a wide range of tasks"; no inline citation; must agree with results in G011, G013, G017. |
| claim-0005 | high | high | domain_violation | Architectural claim: L-GATr represents data in geometric algebra and is Lorentz-equivariant; verifiable against Hestenes and GATr literature. |
| claim-0006 | medium | medium | ambiguous | "Versatile and scalable" with no metric; "break symmetries if needed" is clarified later. |
| claim-0007 | high | high | unreferenced, literature_collision | "First Lorentz-equivariant generative network" — priority claim requiring lit search to rule out earlier work. |
| claim-0008 | high | high | ambiguous, internal_contradiction | "Significant improvements over previous architectures" — must be reconciled with actual table results; "significant" is undefined. |
| claim-0009 | medium | medium | unreferenced | Broad LHC-ML landscape claim; no citation; standard review territory but not cited. |
| claim-0010 | medium | high | unreferenced | Claim about shift toward resilience and uncertainty — cite Plehn:2022ftl present but bank gap noted. |
| claim-0011 | low | medium | unreferenced | Historical claim about training data abundance assumption; uncited. |
| claim-0012 | low | low | ambiguous | Hedged historical claim; low stakes. |
| claim-0013 | low | low | ambiguous | Transitional framing sentence; no factual content. |
| claim-0014 | medium | medium | unreferenced, ambiguous | "Per-mille level in most practical scenarios" — quantitative but uncited; "most" is vague. |
| claim-0015 | medium | low | ambiguous | "Huge datasets" — vague; no metric. |
| claim-0016 | low | low | ambiguous | Contextual motivation; hedged. |
| claim-0017 | low | low | ambiguous | Generic methodological statement. |
| claim-0018 | low | low | unreferenced | Background claim; no citation. |
| claim-0019 | medium | medium | ambiguous | "Known challenge for all networks" — broad, uncited; could be flagged. |
| claim-0020 | low | low | ambiguous | Footnote explaining covariant vs. equivariant terminology; no factual risk. |
| claim-0021 | low | medium | unreferenced | "Equivariant networks are an established subfield" — uncited; verifiable but low stakes. |
| claim-0022 | medium | high | literature_collision | Claim about jet taggers using low-level info; well-cited; check that cite_keys match the right papers. |
| claim-0023 | high | high | literature_collision | "Lorentz-equivariant jet taggers, currently under experimental study" — cites Gong:2022lye, Bogatskiy:2022czk, Qiu; check that these are actually Lorentz-equivariant. |
| claim-0024 | medium | low | ambiguous | "Paved the way for a new phase" — interpretive; low checkability. |
| claim-0025 | medium | high | unreferenced | LHC reliance on precision simulations; cited Butter:2022rso, Campbell:2022qmc. |
| claim-0026 | medium | high | unreferenced | GAN-based detector simulation generalization; cited; bank coverage exists. |
| claim-0027 | medium | high | unreferenced | ML-generator development from partonic events; multiple citations; check that the progression claim holds. |
| claim-0028 | low | low | ambiguous | Goal statement; not verifiable. |
| claim-0029 | medium | low | ambiguous | "Appropriate internal representation" — design claim; low checkability. |
| claim-0030 | high | high | literature_collision | L-GATr is based on GATr (brehmer2023geometric); check that the parent architecture is accurately characterized. |
| claim-0031 | high | high | unreferenced | "Maximally expressive linear map" — a strong architectural novelty claim; no citation; should be proven or sourced. |
| claim-0032 | medium | high | internal_contradiction | States architecture was "originally developed for an ML audience"; should agree with Spinner:2024hjm description. |
| claim-0033 | medium | medium | internal_contradiction | Claims extensions vs. Spinner:2024hjm: amplitude, pre-training, multi-class, competitive generation; check these are not overstated. |
| claim-0034 | low | low | ambiguous | "Comprehensive benchmarking" — self-description; not independently checkable. |
| claim-0035 | low | low | ambiguous | Road-map sentence; no factual claim. |
| claim-0036 | medium | medium | unreferenced | Claim about Z+5g amplitude regression; forward reference only. |
| claim-0037 | low | low | ambiguous | Transition sentence. |
| claim-0038 | medium | medium | unreferenced | Claim that L-GATr benefits from pre-training; forward reference. |
| claim-0039 | low | low | ambiguous | Transition sentence with typo ("diffusion" vs. CFM). |
| claim-0040 | high | high | internal_contradiction | "Generates LHC events for t-tbar+4jets better than all benchmarks" — must match results in G017. |
| claim-0041 | low | low | ambiguous | Filler/transition. |
| claim-0042 | low | low | ambiguous | Filler/transition. |
| claim-0043 | medium | high | domain_violation, unreferenced | GA is "a mathematical framework representing geometric objects in a unified language" — accurate but should cite Hestenes. |
| claim-0044 | medium | medium | ambiguous | "Straightforward to build exactly equivariant layers" — relative claim; no quantification. |
| claim-0045 | medium | medium | unreferenced | Reference multivector mechanism for subgroup equivariance; no citation. |
| claim-0046 | low | low | ambiguous | Scaling study preview; forward reference. |
| claim-0047 | medium | high | domain_violation | Definition of geometric algebra with geometric product; cites Hestenes; check definition is accurate. |
| claim-0048 | medium | high | domain_violation | Decomposition of geometric product into symmetric/antisymmetric; check formula matches standard GA texts. |
| claim-0050 | medium | high | domain_violation | Anti-commutator = inner product claim; check algebraic identity. |
| claim-0051 | medium | high | domain_violation | Bivector as area element; check standard GA interpretation. |
| claim-0052 | medium | high | domain_violation | "Geometric product preserves commutativity when acting on elements of the same grade" — check this statement; it is not obvious (grade-k elements don't generally commute). |
| claim-0053 | medium | high | domain_violation | Basis vectors satisfying {γ^μ, γ^ν} = 2g^μν; check against Dirac algebra conventions. |
| claim-0055 | low | high | domain_violation | "Establishes orthogonality and fixes normalization" — follow-up to equation; check. |
| claim-0056 | medium | high | internal_contradiction | "Recovers all algebra properties from Ref." (Spinner:2024hjm); should be internally consistent. |
| claim-0057 | medium | high | domain_violation | Anti-commutation relation is defining property of Dirac algebra; accurate; check that claim about shared property is correct. |
| claim-0058 | high | high | domain_violation | "Only difference between spacetime algebra and Dirac algebra is R^4 vs C^4" — strong and checkable statement; potential oversimplification. |
| claim-0061 | medium | high | domain_violation | σ^{μν} as plane in Minkowski space interpretation. |
| claim-0062 | medium | high | domain_violation | "Symmetric term reduces grade, antisymmetric increases it" — check against standard GA grade arithmetic. |
| claim-0063 | medium | high | domain_violation | Trivector and pseudoscalar derivation; check γ^5 definition. |
| claim-0065 | low | medium | ambiguous | Fragment continuation of pseudoscalar definition; partially parseable. |
| claim-0066 | low | low | ambiguous | Fragment claim (malformed extraction); exclude from metrics. |
| claim-0067 | low | low | ambiguous | Footnote analogy to SUSY; not a factual claim requiring verification. |
| claim-0068 | low | low | domain_violation | Footnote claim about SUSY multiplet algebra; accurate but peripheral. |
| claim-0069 | low | low | domain_violation | Footnote claim about superspace Grassmann expansion; standard. |
| claim-0070 | low | low | ambiguous | Footnote about limitation of multivectors vs. superfields; interpretive. |
| claim-0071 | medium | high | domain_violation | "Geometric products with more than four γ^μ reduce to lower-grade structures" — verifiable algebraic fact. |
| claim-0072 | low | low | ambiguous | Transition sentence. |
| claim-0074 | low | medium | ambiguous | "Only nonzero and independent entries in the bivector" — needs context of bivector dimension count. |
| claim-0075 | low | low | ambiguous | Definition of "multivector"; terminological. |
| claim-0076 | medium | high | domain_violation | "Multivectors can represent both spacetime objects and Lorentz transformations" — dual interpretation; check. |
| claim-0079 | medium | medium | unreferenced | "Spacetime algebra naturally structures parity-violating amplitudes" — no citation; verifiable against physics. |
| claim-0080 | medium | high | domain_violation | Amplitude decomposition into parity-even and parity-odd terms; check physics of CP-odd contributions. |
| claim-0082 | medium | high | domain_violation | "First two terms scalar, last term pseudoscalar" in |M|^2 — check decomposition. |
| claim-0085 | medium | medium | unreferenced | Result of amplitude as multivector separating scalar/pseudoscalar; no citation. |
| claim-0086 | medium | high | domain_violation | Lorentz transformation via sandwich product vxv^{-1}; check against standard spinor algebra. |
| claim-0088 | medium | high | domain_violation | v^{-1} definition claim; check invertibility conditions. |
| claim-0089 | medium | high | domain_violation | "Invariant multivector under Lorentz = transformation generator" — dual interpretation; check. |
| claim-0091 | medium | high | domain_violation | "Boosts along z-axis generated by σ^{03}" — check against standard boost generators. |
| claim-0096 | medium | high | domain_violation | "This is exactly what we expect from the Lorentz boost" — internal check of boost formula. |
| claim-0097 | medium | high | domain_violation | GA boost applies to any algebra element, not just vectors; check grade-preservation under sandwich. |
| claim-0098 | high | high | domain_violation, internal_contradiction | "Lorentz transformations will never mix grades" — strong claim; caveated in 0099; check consistency. |
| claim-0099 | high | high | domain_violation, ambiguous | "Grade mixing can occur through combined boosts and rotations on composite states" — contradicts or qualifies claim-0098; check physical accuracy. |
| claim-0100 | high | medium | ambiguous, unreferenced | "Main limitation: spacetime algebra covers only limited range of Lorentz tensor representations" — significant caveat on scope; uncited. |
| claim-0101 | high | high | domain_violation | "Cannot represent symmetric rank-2 tensors" — verifiable algebraic fact about G_{1,3}. |
| claim-0102 | medium | low | ambiguous | "Most LHC applications don't use higher-order tensors as inputs/outputs" — broad claim, uncited. |
| claim-0103 | low | low | ambiguous | "Not a substantial limitation" — subjective. |
| claim-0104 | medium | medium | unreferenced | "Higher-order tensors for internal representations is open question" — cites DBLP paper; check appropriateness. |
| claim-0106 | high | high | domain_violation, unreferenced | "Exactly equivariant under Lorentz group transformations" — central architectural claim; must be verified against proof or referenced construction. |
| claim-0108 | high | high | domain_violation | Grade sub-representations claim; cites brehmer2023geometric and Spinner:2024hjm; check accuracy. |
| claim-0109 | high | high | unreferenced, literature_collision | Uses "variations of standard transformer operations"; cites Vaswani and Xiong; check that cited operations match described modifications. |
| claim-0112 | low | low | ambiguous | Definition of "tokens". |
| claim-0117 | high | high | domain_violation | "Equivariant operations process components within the same grade equally" — core equivariance design claim. |
| claim-0119 | high | high | domain_violation, unreferenced | "Most general linear combination of independently-transforming multivector components" — maximality claim; uncited. |
| claim-0122 | high | high | domain_violation | "Second term breaks symmetry to special orthochronous Lorentz group" — check that γ^5 mixing achieves this and not something else. |
| claim-0123 | high | high | domain_violation | "In fully-connected subgroup, discrete transformations not present, so γ^5 mixing doesn't break equivariance" — check algebra. |
| claim-0127 | medium | high | domain_violation | Inner product pre-computable as signs + Euclidean inner product; implementation claim; verifiable. |
| claim-0128 | high | high | domain_violation | "G_{1,3} norm can have zero and negative contributions" — known but important; check against indefinite metric. |
| claim-0129 | medium | high | unreferenced | Layer normalization using absolute value of grade inner products; no external reference for this design choice. |
| claim-0131 | medium | medium | ambiguous | ε=10^{-2} normalization constant; specific hyperparameter. |
| claim-0132 | medium | low | unreferenced | "ε has negligible impact" — empirical claim without citation. |
| claim-0133 | medium | high | domain_violation | "Activation functions applied directly on multivectors break equivariance" — check this claim (it is generally true). |
| claim-0134 | high | high | literature_collision | Scalar-gated activation citing brehmer2023geometric and GELU; check that GATr citation is correct for this technique. |
| claim-0138 | high | high | domain_violation | "Geometric product is equivariant" — check formal equivariance of GP under sandwich product. |
| claim-0140 | low | low | ambiguous | Table-as-prose (flagged by reviewer); skip. |
| claim-0141 | low | low | ambiguous | Caption prose; low stakes. |
| claim-0142 | low | low | ambiguous | Caption continuation; low stakes. |
| claim-0143 | medium | medium | internal_contradiction | "Second term breaks Lorentz group to fully connected subgroup" — check consistency with claim-0122. |
| claim-0144 | medium | medium | ambiguous | "Strictly generalize standard scalar transformers" — check this generalization claim. |
| claim-0145 | low | low | ambiguous | Design rationale for extra scalar channels. |
| claim-0146 | medium | medium | unreferenced | "In many LHC contexts, Lorentz symmetry is only partially preserved" — accurate but uncited. |
| claim-0147 | high | medium | domain_violation, ambiguous | "Performance can degrade significantly" if partial breaking not accounted for — significant claim; ambiguous "significantly". |
| claim-0148 | high | high | domain_violation | "Equivariant architectures treat Lorentz-related inputs as equivalent" — core design principle; check domain accuracy. |
| claim-0150 | high | medium | ambiguous | "Fully Lorentz-equivariant architecture is blind to differences" — strong claim; check against actual experimental comparisons. |
| claim-0151 | high | high | unreferenced | Reference multivector mechanism for tunable symmetry breaking — novel mechanism, no external citation. |
| claim-0152 | high | high | domain_violation | "Any operation involving reference vector violates equivariance, breaking to subgroup" — check this is exactly true. |
| claim-0155 | high | high | internal_contradiction | "Reference vectors produce better results than complete symmetry breaking" — must match results in Tables. |
| claim-0160 | high | high | literature_collision | LHC beam direction breaks Lorentz to subgroup of rotations + boosts along beam; cites Maitre:2024hzp, Bogatskiy, ruhe, Gong; check that literature supports this framing. |
| claim-0161 | medium | medium | ambiguous | "Similar performance for beam ± or bivector embedding" — check against ablation table. |
| claim-0162 | medium | medium | unreferenced | Detector setup compromises boost symmetry; no citation. |
| claim-0163 | high | high | domain_violation | "x^V = (1,0,0,0) breaks to SO(3); x^V_± = (1,0,0,±1) breaks to SO(2)" — check that these reference vectors achieve the stated symmetry reductions. |
| claim-0165 | high | medium | ambiguous, internal_contradiction | "Architecture compensates for any symmetry mismatch" — strong claim; check against ablation tables. |
| claim-0172 | medium | high | literature_collision | GNNs closely resemble transformers; cites bronstein2021geometric and Gong/Bogatskiy; check that citation supports claim. |
| claim-0174 | medium | medium | unreferenced | "Resource efficiency is where the two architectures differ most" — comparative claim; uncited. |
| claim-0185 | medium | high | internal_contradiction | L-GATr: 2.3×10^4 params; transformer: 6.7×10^5 — check these numbers internally. |
| claim-0186 | medium | high | internal_contradiction | CGENN: 2.5×10^4 params — check. |
| claim-0187 | medium | medium | unreferenced | Scaling behavior description: quadratic at large tokens. |
| claim-0189 | high | high | domain_violation | "L-GATr scales like standard transformer in many-token regime because they use same attention module" — verify this architectural claim. |
| claim-0191 | high | medium | unreferenced, literature_collision | "CGENN slower than L-GATr for few tokens, quadratic scaling takes off sooner" — compare against CGENN paper. |
| claim-0192 | medium | medium | internal_contradiction | Linear memory scaling claim for L-GATr and transformer; check against Fig. |
| claim-0193 | medium | medium | ambiguous | CGENN "near-linear memory" claim; hedged with "may encounter constraints". |
| claim-0195 | medium | medium | unreferenced | FlashAttention citation missing (no cite_key); check that FlashAttention is properly referenced. |
| claim-0196 | medium | medium | domain_violation | "GNNs optimized for sparse graphs degrade for fully connected" — accurate general claim; check. |
| claim-0199 | low | medium | unreferenced | "Partonic amplitudes can be calculated exactly" — standard physics; no citation needed. |
| claim-0200 | medium | high | unreferenced | Evaluation becomes expensive at high multiplicity/high order; cites Maitre:2023dqz. |
| claim-0201 | high | high | literature_collision | "Amplitude surrogates speed up precision predictions" — cites Aylett-Bullock, Maitre, Badger; check these are speed-up papers. |
| claim-0202 | high | medium | unreferenced, ambiguous | "Standard neural networks struggle for high multiplicity" — strong claim, uncited; "sufficient accuracy" undefined. |
| claim-0203 | high | high | unreferenced | L-GATr uses partial permutation symmetry for high-multiplicity scaling — novel claim, uncited. |
| claim-0204 | high | high | domain_violation | "Guarantees exact Lorentz invariance of the amplitude" — very strong claim for a regression network; check what this means. |
| claim-0207 | medium | medium | unreferenced | MSE loss for amplitude training; standard. |
| claim-0208 | high | high | unreferenced | 4×10^5 training points, MadGraph at LO — verifiable against dataset description. |
| claim-0213 | medium | medium | unreferenced | Standardized logarithmic amplitudes; methodology. |
| claim-0221 | medium | medium | internal_contradiction | "All networks take 4-momenta except DSI" — check against hyperparameter table. |
| claim-0224 | high | high | unreferenced, internal_contradiction | "Transformer and graph networks scale better with particles" — must match Fig. 2 left panel. |
| claim-0225 | high | high | internal_contradiction | "L-GATr roughly on par with DSI for few gluons" — check against Fig. results. |
| claim-0226 | high | high | internal_contradiction | "Improved scaling gives L-GATr the lead for higher multiplicity" — check against Fig. |
| claim-0229 | high | high | internal_contradiction | "L-GATr is top performer across all training regimes" — strong claim; check Fig. right panel. |
| claim-0230 | high | medium | unreferenced | L-GATr and CGENN efficient due to equivariance for small training sets — plausible but uncited. |
| claim-0234 | high | medium | internal_contradiction | "Reproduces L-GATr scaling despite more complex Z+5g process" — check Fig. 3. |
| claim-0236 | medium | low | ambiguous | "Jet tagging is arguably the LHC task most impacted by modern ML" — hedged; subjective. |
| claim-0237 | medium | medium | unreferenced | "Transformer-based and equivariant networks stand out as top performers" — uncited. |
| claim-0238 | high | medium | internal_contradiction | "All pre-training and multiclass results are new to this paper" — check against Spinner:2024hjm. |
| claim-0241 | high | high | internal_contradiction | "2M top/QCD jets" with pT 550–650 GeV — check dataset description against Kasieczka benchmark. |
| claim-0243 | medium | high | literature_collision | "Generated with Pythia8 and Delphes, default ATLAS card" — check against Heimel:2018mkt dataset description. |
| claim-0244 | medium | high | internal_contradiction | Train/val/test split 1.2/0.4/0.4M — check consistency with dataset size claim (2M total). |
| claim-0279 | low | medium | internal_contradiction | Partial table row (claim is table fragment); low reliability. |
| claim-0280 | low | medium | internal_contradiction | Partial table row; low reliability. |
| claim-0281 | low | medium | internal_contradiction | Partial table row: L-GATr-f.t. 0.9446 AUC — check against other table rows. |
| claim-0282 | medium | high | literature_collision | Caption citing Heimel:2018mkt and Kasieczka:2019dbj — check cite keys are correct. |
| claim-0283 | low | low | ambiguous | Descriptor sentence about asterisk notation. |
| claim-0284 | low | low | ambiguous | Descriptor sentence about horizontal line notation. |
| claim-0285 | medium | medium | internal_contradiction | "Entries with two citations = results from global analysis" — check citation logic. |
| claim-0286 | medium | low | unreferenced | Error bars from 5 seeds — standard; unremarkable. |
| claim-0288 | high | high | literature_collision | LorentzNet described as "equivariant graph network based on functions of Minkowski dot products" — check Gong:2022lye. |
| claim-0289 | high | high | literature_collision | PELICAN described as "permutation equivariant aggregation" — check Bogatskiy:2023nnw. |
| claim-0290 | high | high | literature_collision | CGENN described as "multivector graph network" — check ruhe2023clifford. |
| claim-0291 | high | high | literature_collision | ParT described as "transformer with pairwise interaction as attention bias" — check Qu:2022mxj. |
| claim-0292 | high | high | literature_collision | MIParT described as "extension of ParT with specialized interaction blocks" — check Wu:2024thh. |
| claim-0293 | high | high | internal_contradiction | "L-GATr at least on par with leading equivariant baselines" — check Table 1 numbers. |
| claim-0294 | high | medium | unreferenced, literature_collision | "Non-equivariant architectures achieve higher accuracy when sufficient data available" — strong claim; partially supported by Table 1 but needs lit context. |
| claim-0295 | high | medium | unreferenced | "Key ingredient: symmetry breaking prescription" — architectural claim, uncited. |
| claim-0298 | high | high | internal_contradiction | "Including beam and time reference significantly boosts performance" — check Table 2 numbers. |
| claim-0323 | low | low | ambiguous | Table-as-prose (flagged); skip. |
| claim-0324 | low | low | ambiguous | Caption title only. |
| claim-0325 | low | medium | internal_contradiction | Caption reference to dataset; check cite key kasieczka_gregor_2019_2603256. |
| claim-0326 | low | low | unreferenced | Error bar method statement. |
| claim-0327 | low | low | internal_contradiction | "Last line is default for all tagging" — check that Table 2 last row matches Table 1 default. |
| claim-0328 | medium | medium | unreferenced | "Further study of L-GATr for JetClass multiclass" — transition sentence. |
| claim-0329 | low | medium | unreferenced | "JetClass covers wide variety" — check claim against dataset description. |
| claim-0330 | medium | high | literature_collision | Signal events from top, W, Z, H decays — check JetClass dataset. |
| claim-0331 | medium | high | literature_collision | Background = light quark and gluon jets — check JetClass. |
| claim-0332 | medium | high | literature_collision | Generated with MadGraph and Pythia — check Qu:2022mxj dataset description. |
| claim-0333 | medium | high | literature_collision | Detector effects with Delphes CMS card — check Qu:2022mxj. |
| claim-0336 | high | high | literature_collision | "JetClass contains 100M jets across 10 classes" — verify against Qu:2022mxj. |
| claim-0337 | medium | high | literature_collision | JetClass features: 4-momenta, kinematic variables, PID, trajectory displacement — check Qu:2022mxj. |
| claim-0341 | high | high | internal_contradiction, literature_collision | "L-GATr achieves significant improvement over ParT and MIParT in essentially all signal types" — check Table 3; verify ParT/MIParT numbers against published results. |
| claim-0344 | high | high | internal_contradiction | "L-GATr achieves similar performance to non-equivariant ParT/MIParT with only 10% of jets" — check Table 4 at 10M. |
| claim-0346 | low | low | ambiguous | Table-as-prose with 2c prefix artifact; skip. |
| claim-0347 | medium | medium | unreferenced | Caption reference to JetClass dataset. |
| claim-0348 | low | low | ambiguous | AUC computation method description. |
| claim-0349 | low | low | ambiguous | Acceptance computation method. |
| claim-0352 | low | low | ambiguous | Table-as-prose with 2c prefix artifact; skip. |
| claim-0353 | medium | medium | internal_contradiction | Caption: "different sizes of JetClass" — check Table 4 labels. |
| claim-0354 | medium | high | literature_collision | "Metrics from other models taken from published results" — check that ParT/MIParT numbers match Qu:2022mxj and Wu:2024thh. |
| claim-0355 | high | high | literature_collision | "Large capacity of transformers motivates pre-training" — cites Qu:2022mxj; check that ParT paper advocates this. |
| claim-0359 | medium | medium | internal_contradiction | "Follow Ref. for pre-training and fine-tuning procedures" — check that procedure matches Qu:2022mxj. |
| claim-0361 | medium | medium | domain_violation | "Pre-trained weights need smaller LR else network dismisses pre-training" — standard claim; accurate. |
| claim-0363 | low | low | ambiguous | Footnote about Kasieczka:2017nvn title prediction; peripheral. |
| claim-0365 | high | high | internal_contradiction | "L-GATr matches best fine-tuned networks across all metrics" — check Table 1 fine-tuned rows. |
| claim-0367 | medium | medium | unreferenced | Event generation as key benchmark; cites Bellagente, Backes, Shmakov. |
| claim-0368 | high | medium | ambiguous | "Per-mille or percent level accuracy on phase space density" — defined requirement but not cited. |
| claim-0373 | high | high | unreferenced | MadGraph3.5.1 with MadEvent, Pythia8, Delphes3, anti-kT R=0.4, FastJet — verify these are correctly named. |
| claim-0374 | medium | medium | unreferenced | "Pythia without multi-parton interactions, default ATLAS card" — specific configuration; no citation. |
| claim-0378 | high | high | internal_contradiction | Dataset sizes: 9.8M, 7.2M, 3.7M, 1.5M, 480k for n=0..4 — check internal consistency and Spinner:2024hjm. |
| claim-0379 | medium | medium | internal_contradiction | "Identical particles ordered by pT" — check against generation setup. |
| claim-0380 | medium | high | unreferenced, literature_collision | CFM framing: ODE/continuity equation duality; cites Chen, Plehn, Butter. |
| claim-0382 | medium | high | domain_violation | Diffusion t=0→1 interpolation between phase space and base distribution; check convention matches lipman2022flow. |
| claim-0384 | high | high | literature_collision | Linear interpolation x(t) = (1-t)x_0 + t x_1 for CFM; cites lipman2023flow and albergo2023stochastic; check correct citation. |
| claim-0391 | medium | medium | unreferenced | Benchmark set for generation: MLP, transformer, E(3)-GATr. |
| claim-0393 | medium | high | literature_collision | "Standard transformer" generation baseline cites Huetsch:2024quz — check that this is the correct reference for the transformer CFM. |
| claim-0394 | medium | high | literature_collision | E(3)-GATr cited as brehmer2023geometric — check this is the correct reference. |
| claim-0395 | high | high | unreferenced, literature_collision | "CFM is currently leading technique in precision generation; calorimeter uses ViT" — cites Butter:2023fov and Favaro:2024rle; check that these support the claim. |
| claim-0396 | medium | low | domain_violation | "Task does not require translation-equivariant representations" — physics claim; check against event generation context. |
| claim-0399 | high | high | domain_violation | "Process is only symmetric under rotations around beam axis" — check physics of ppbar events at LHC. |
| claim-0401 | high | high | domain_violation | "L-GATr includes time reference because distribution not invariant under boosts along beam axis" — physics claim; check. |
| claim-0402 | high | high | domain_violation | "Not possible to construct normalized density invariant under non-compact group" — strong mathematical claim; check topology argument. |
| claim-0403 | medium | high | domain_violation | "Equivariant generator requires symmetric base distribution" — check this requirement in flow matching literature. |
| claim-0404 | medium | medium | unreferenced | Gaussian base in (px, py, pz, log m^2) coordinates; specific design choice. |
| claim-0405 | medium | medium | unreferenced | Rejection sampling to enforce phase space cuts at base level. |
| claim-0418 | low | low | ambiguous | Table header fragment (table-as-prose boundary); low value. |
| claim-0419 | low | low | ambiguous | Table-as-prose partial; see flagged table-as-prose list (claim-0462). |
| claim-0420 | low | low | ambiguous | Caption descriptor for trajectory table. |
| claim-0421 | medium | medium | internal_contradiction | "All networks trained on t-tbar+0j" — check consistency with generation setup. |
| claim-0423 | high | high | unreferenced | "Phase space parametrization for straight trajectories is crucial for generator performance" — strong methodological claim; no citation. |
| claim-0424 | medium | medium | unreferenced | MLP/transformer use x parametrization directly; methodological. |
| claim-0427 | medium | medium | domain_violation | Azimuthal angle periodic; wrapping by 2π — check periodicity handling is correct. |
| claim-0429 | high | high | unreferenced | L-GATr flow: p → x, L-GATr(p) → v_p → v_x via Jacobian; novel design claim. |
| claim-0432 | high | high | unreferenced | "Large Jacobian components from log transforms cause unstable training" — specific engineering claim; no citation. |
| claim-0434 | high | medium | unreferenced | Overwrites two velocity components with scalar outputs to avoid instability — novel design choice. |
| claim-0436 | medium | medium | internal_contradiction | E(3)-GATr encodes (px, py, pz) as vector, x_m as scalar — check consistency with architecture description. |
| claim-0438 | medium | medium | internal_contradiction | "Study effect of choice of data representation, base distribution, and trajectories in Tab." — check Table 5 is about these. |
| claim-0441 | high | high | internal_contradiction | "Including beam and time reference is essential; omitting leads to inferior performance" — check Table 6. |
| claim-0443 | medium | medium | internal_contradiction | "Specific beam representation less critical than in tagging" — check comparison Tables 2 vs. 6. |
| claim-0444 | medium | medium | unreferenced | Tokens add cost for low particle count; choosing channels instead — design claim. |
| claim-0462 | low | low | ambiguous | Table-as-prose (flagged); skip. |
| claim-0463 | low | low | ambiguous | Caption title only. |
| claim-0464 | low | low | internal_contradiction | Caption: "compare on t-tbar+0j dataset" — check Table 6 is about 0j. |
| claim-0465 | low | low | internal_contradiction | "Last line is default for all generation experiments" — check Table 6 last row matches generation results. |
| claim-0466 | low | low | unreferenced | Error bar method for generation. |
| claim-0471 | high | high | internal_contradiction | "L-GATr outperforms baselines across all distributions" — check Fig. 4 marginals. |
| claim-0472 | high | high | unreferenced | "Angular correlations benefit from equivariance; percent-level precision for first time" — strong novelty claim; "first time" needs citation. |
| claim-0473 | medium | medium | domain_violation | "Main weakness: intermediate top mass poles require correlation of three 4-vectors" — physics claim; check. |
| claim-0475 | high | high | internal_contradiction | "Clear improvement from MLP → transformer → GATr → L-GATr" — check Fig. 5 ordering. |
| claim-0476 | high | high | internal_contradiction, unreferenced | "Superior L-GATr performance mainly from boost-equivariance" — strong attribution claim; check Fig. 5. |
| claim-0477 | high | medium | ambiguous | "This might come as a surprise" — framing for boost-breaking with reference vectors; check logic. |
| claim-0478 | high | high | internal_contradiction | "Enforcing equivariance and then breaking with reference multivectors outperforms non-equivariant networks" — central claim; check against Tables 5/6. |
| claim-0479 | low | low | ambiguous | Outlook framing statement. |
| claim-0480 | low | low | ambiguous | Outlook motivation. |
| claim-0481 | low | low | ambiguous | Outlook statement. |
| claim-0482 | medium | low | ambiguous | "Leading symmetry is Lorentz symmetry" — partially subjective. |
| claim-0483 | medium | low | unreferenced | "Encoding Lorentz symmetry avoids learning it" — standard inductive bias argument; no citation. |
| claim-0484 | high | medium | unreferenced, ambiguous | "Appropriate internal Lorentz representation enhances performance of essentially every ML application" — strong general claim. |
| claim-0485 | high | high | internal_contradiction | "Equivariance with breakable reference frames outperforms removing equivariance altogether" — must match ablation results. |
| claim-0486 | medium | low | ambiguous | L-GATr "versatile equivariant transformer" — self-description. |
| claim-0487 | high | high | internal_contradiction | "L-GATr best performance for >3 particles in final state" — must match Fig. 2 amplitude results. |
| claim-0488 | high | medium | ambiguous, internal_contradiction | "L-GATr at least on par with best subjet tagger" — check against Table 1 fine-tuned; "at least on par" is ambiguous. |
| claim-0489 | high | high | internal_contradiction | "L-GATr+CFM faithfully reproduces ttbar+jets better than all other CFM setups" — must match Fig. 5 generation results. |
| claim-0490 | low | low | ambiguous | Forward-looking statement. |
| claim-0491 | low | medium | unreferenced | GitHub URL for L-GATr code; verifiable but low scientific stakes. |
| claim-0492 | low | medium | unreferenced | GitHub URL for reproduction; verifiable. |
| claim-0493 | low | low | ambiguous | Acknowledgement; no scientific claim. |
| claim-0494 | low | low | ambiguous | Acknowledgement. |
| claim-0495 | low | low | unreferenced | Grant numbers; not factual scientific claims. |
| claim-0496 | low | low | unreferenced | Grant numbers. |
| claim-0497 | low | low | unreferenced | Grant numbers. |
| claim-0498 | low | low | unreferenced | Grant numbers. |
| claim-0499 | low | low | unreferenced | Grant numbers. |
| claim-0500 | low | low | unreferenced | Grant numbers. |
| claim-0501 | medium | high | literature_collision | DSI described as combining momentum invariants as Deep Sets input — check zaheer2017deep. |
| claim-0502 | low | low | ambiguous | "Works in three stages" — structure description. |
| claim-0503 | low | low | ambiguous | DSI stage 1 description. |
| claim-0504 | medium | medium | domain_violation | "Summing over identical particle types imposes permutation invariance" — check if this is a sufficient condition. |
| claim-0505 | low | low | ambiguous | DSI stage 3 description. |
| claim-0506 | medium | low | ambiguous | "Achieves combination of Lorentz and permutation invariants in imperfect way" — evaluative. |
| claim-0507 | medium | low | unreferenced | "Hyperparameters chosen to maximize performance of each architecture" — standard but uncited. |
| claim-0508 | medium | medium | domain_violation | Common normalization for L-GATr 4-momenta to preserve equivariance — check that this is necessary/sufficient. |
| claim-0514 | low | low | ambiguous | Table-as-prose fragment (flagged); skip. |
| claim-0515 | low | low | ambiguous | Table-as-prose fragment (flagged); skip. |
| claim-0516 | low | low | ambiguous | Caption descriptor. |
| claim-0517 | medium | medium | internal_contradiction | DSI latent space dimensionality 64 — check against hyperparameter table. |
| claim-0518 | medium | medium | internal_contradiction | CGENN: node features = scalar channels, edge features = multivector channels — check against ruhe2023clifford. |
| claim-0520 | medium | high | internal_contradiction | L-GATr hyperparameters for top tagging: 32 scalar, 16 multivector, 8 heads, 12 blocks, 1.1×10^6 params — check consistency. |
| claim-0522 | medium | medium | literature_collision | "Lion optimizer as upgrade to Adam" — cites chen2023symbolic; check that this claim is accurate. |
| claim-0523 | low | low | unreferenced | 20 GeV scale factor for preprocessing. |
| claim-0524 | low | low | unreferenced | Binary cross entropy loss for top tagging. |
| claim-0525 | medium | high | internal_contradiction | "Pre-training on full 100M events over 10^6 iterations" — check against JetClass claim-0336. |
| claim-0527 | medium | medium | internal_contradiction | "10 output channels for multiclass" — check matches 10 JetClass classes. |
| claim-0528 | low | low | unreferenced | Batch size 512 for JetClass. |
| claim-0529 | medium | medium | internal_contradiction | "20 GeV scale factor same as top tagging" — check consistency. |
| claim-0530 | medium | medium | literature_collision | "Kinematic functions standardized following Qu:2022mxj" — check that preprocessing matches ParT. |
| claim-0531 | low | low | unreferenced | Fine-tuning: reset output layer. |
| claim-0532 | medium | high | internal_contradiction | Pre-trained LR = 3×10^{-5}; weight decay 0.01; batch 128 — cross-check with main text. |
| claim-0533 | medium | high | internal_contradiction | New layer LR = 3×10^{-3} — check 100× ratio relative to pre-trained LR. |
| claim-0534 | medium | medium | internal_contradiction | 10^5 fine-tuning iterations. |
| claim-0535 | medium | medium | unreferenced | 98/1/1 train/val/test split. |
| claim-0537 | low | low | unreferenced | MLP classifier for AUC evaluation. |
| claim-0538 | medium | medium | internal_contradiction | Classifier architecture: 3 layers, 256 channels; inputs include ΔR pairwise and reconstructed particles. |
| claim-0539 | medium | medium | unreferenced | Classifier: 500 epochs, batch 1024, dropout 0.1. |
| claim-0540 | medium | medium | unreferenced | Classifier LR schedule: reduce by 10 after 5 epochs no improvement. |
| claim-0541 | medium | high | internal_contradiction | "Full truth data + 1M generated events, 80/10/10 split" — check against dataset sizes. |
| claim-0543 | low | low | ambiguous | Table-as-prose (flagged); skip. |
| claim-0544 | low | low | ambiguous | Caption descriptor. |
| claim-0545 | medium | medium | unreferenced | Validation every 10^3 iterations, LR reduced by 10 after 20 steps. |
