# STRATEGY.md — Phase 2 — review: easy

Paper: *A Lorentz-Equivariant Transformer for All of the LHC* (L-GATr).
Authors: Brehmer, Bresó, de Haan, Plehn, Qu, Spinner, Thaler.
Claims: 200 (C001–C200). LITERATURE coverage: 88 COVERED, 112 UNCOVERED.

All five checker agents run against all claims. This table guides their
prioritization: every `importance=high` claim must receive thorough attention.
`importance=medium` and `importance=low` claims are still checked but may
receive proportionally less effort.

Categories are selected from: `unreferenced`, `ambiguous`,
`internal_contradiction`, `literature_collision`, `domain_violation`.

---

| claim_id | importance | checkability | categories | rationale |
|----------|------------|--------------|------------|-----------|
| C001 | high | high | unreferenced, internal_contradiction, literature_collision | Headline abstract result; must cohere with every per-task numerical result in the paper and not overstate what benchmarks show. UNCOVERED by external evidence. |
| C002 | high | high | domain_violation, unreferenced | Claims exact Lorentz equivariance and geometric-algebra representation; both are formal mathematical properties verifiable against established equivariance theory. |
| C003 | high | medium | domain_violation, ambiguous | Claims transformer "breaks symmetries if needed"; mechanism and conditions for symmetry breaking are underspecified without the reference multivector context. |
| C004 | high | high | unreferenced, internal_contradiction, literature_collision | Asserts "significant improvements" across all three tasks; UNCOVERED; must not overstate vs. table numbers and vs. baseline results already in the literature. |
| C005 | medium | high | unreferenced, literature_collision | Broad LHC ML scope claim; COVERED by plehn2022modern/badger2023mllhc but the specific enumeration of applications should be checkable against those references. |
| C006 | low | low | ambiguous | Interpretive framing ("optimal and resilient") without a metric; low checkability. |
| C007 | high | medium | unreferenced, ambiguous | Asserts standard architectures "do not capture amplitudes at the per-mille level" — quantitative threshold requiring a citation; COVERED only weakly by aylett2021diphoton. |
| C008 | medium | low | unreferenced | Precision requirement claim; COVERED by plehn2022modern but the specific quantitative claim is asserted without a hard citation. |
| C009 | medium | low | unreferenced | Simulation-measurement tuning claim; COVERED only by a related plehn2022modern snippet; low independent checkability. |
| C010 | high | high | unreferenced, literature_collision | "Learning Minkowski metric is a known challenge" — a factual claim about the field; checkable against butter2018lorentz and LorentzNet literature. |
| C011 | medium | medium | unreferenced | Interpretation about Lorentz-covariant representations; COVERED by related butter2018lorentz/gong2022lorentznet but framing is the paper's own. |
| C012 | medium | high | unreferenced, literature_collision | Claims about the history of jet tagging; COVERED; checkable against kasieczka2019toptagger/cogan2015jetimages for accuracy. |
| C013 | medium | high | unreferenced, literature_collision | Claims about Lorentz-equivariant taggers under experimental study; COVERED by gong2022lorentznet/pelican2024jhep; factual checkability high. |
| C014 | high | high | unreferenced, literature_collision | L-GATr based on GATr for E(3) symmetry; COVERED by brehmer2023gatr; relationship between GATr and L-GATr should be checked against that reference. |
| C015 | high | high | domain_violation, unreferenced | Claims L-GATr generalizes GATr with "maximally expressive" linear map, attention, and LayerNorm — "maximally expressive" is a strong formal claim requiring proof or literature support. |
| C016 | medium | medium | unreferenced | UNCOVERED; states prior arXiv version applied to amplitude regression, top tagging, event generation; self-referential but technically checkable via arXiv. |
| C017 | medium | medium | ambiguous | Claims "extend", "improve", "deliver" relative to prior work; comparison basis is underspecified without quantification. |
| C018 | high | high | domain_violation, unreferenced | Defines geometric algebra as an extension with geometric product; foundational definition verifiable against Hestenes 1966 / standard texts. |
| C019 | high | high | domain_violation | Formal decomposition of geometric product: symmetric (inner) and antisymmetric (outer); directly checkable against established geometric algebra. |
| C020 | high | high | domain_violation | Defines spacetime algebra G1,3 with metric diag(1,-1,-1,-1) and anticommutation {γμ,γν}=2gμν; standard physics identity — verifiable. |
| C021 | high | high | domain_violation, ambiguous | Claims {γμ,γν}=2gμν is "the defining property of the Dirac algebra"; technically correct but the identification of real spacetime algebra with complex Dirac algebra carries subtleties flagged in C026. |
| C022 | high | high | domain_violation | γμγν = gμν + σμν; grade-2 bivector definition — verifiable against standard algebra. |
| C023 | high | medium | domain_violation | σμν as "plane defined by μ and ν in Minkowski space" — geometric interpretation claim; verifiable against standard bivector geometry. |
| C024 | high | high | domain_violation | Pseudoscalar γ5 = γ0γ1γ2γ3 definition and epsilon-tensor form; verifiable against Hestenes 1966 and standard QFT texts. |
| C025 | high | medium | domain_violation | Pseudoscalars act as parity reversal and axial vectors as γμγ5; standard result but verifiable. |
| C026 | high | medium | domain_violation, ambiguous | Claims "missing factor i" distinguishes real spacetime algebra from complex Dirac algebra; subtle distinction with multiple interpretations depending on metric convention. |
| C027 | high | high | domain_violation | Multivector decomposition into 5 grades (16 real components total); verifiable against standard spacetime algebra. |
| C028 | high | medium | domain_violation, unreferenced | Claims multivectors represent both spacetime objects AND Lorentz transformations; COVERED by hestenes1966 but dual-role claim warrants domain check. |
| C029 | high | medium | unreferenced, ambiguous | Particle representation via (xS=PID, xV=pμ, others=0); UNCOVERED; the specific encoding is novel and should be stated as such but is presented matter-of-factly. |
| C030 | medium | medium | domain_violation, unreferenced | Claims spacetime algebra "naturally structures" parity-violating amplitudes; COVERED by hestenes1966 but "naturally" is a non-trivial claim. |
| C031 | high | high | domain_violation, unreferenced | Matrix element decomposition |M|² = |ME|² + |MO|² + 2Re(M*E MO); UNCOVERED; this is a formal identity verifiable against QFT. |
| C032 | high | high | domain_violation | Sandwich product Λv(x)=vxv⁻¹ for Lorentz transformations; verifiable against standard spin-group / geometric algebra theory. |
| C033 | medium | medium | domain_violation, ambiguous | Invariant multivector "also represents the transformation itself" — self-referential interpretation; correct for scalar invariants but potentially misleading in general. |
| C034 | high | high | domain_violation | Boost v=exp(ωσ03/2)=cosh(ω/2)+σ03·sinh(ω/2); verifiable exponential of a bivector. |
| C035 | high | high | domain_violation | "Lorentz transformations never mix grades"; this is a standard property of the pin/spin group action on geometric algebra — verifiable. |
| C036 | high | medium | domain_violation, unreferenced | G1,3 "cannot represent symmetric rank-2 tensors"; UNCOVERED; this is a representation-theory claim that can be checked against standard Lorentz representation theory. |
| C037 | medium | low | unreferenced, ambiguous | "Not a substantial limitation for most LHC applications"; interpretive claim with no checkable metric; UNCOVERED. |
| C038 | high | high | domain_violation, unreferenced | L-GATr exact Lorentz equivariance L-GATr(Λ(x))=Λ(L-GATr(x)); COVERED only by related brehmer2023gatr; the equivariance proof is the paper's core formal claim. |
| C039 | high | high | domain_violation, unreferenced | "All multivector components of the same grade transform equally under all network operations"; UNCOVERED; requires formal verification of every layer. |
| C040 | high | medium | ambiguous, unreferenced | Claims L-GATr "adapts" standard transformer operations to multivectors; COVERED by vaswani2017 only distantly; the adaptation correctness is the key architectural claim. |
| C041 | high | high | domain_violation, unreferenced | Formal definition of the equivariant linear layer; UNCOVERED; "most general linear combination" is a completeness claim — verifiable against representation theory. |
| C042 | high | high | domain_violation, unreferenced | The γ5 term breaks symmetry to special orthochronous Lorentz group; UNCOVERED; domain claim about which subgroup is preserved. |
| C043 | high | high | domain_violation, unreferenced | Multivector attention with G1,3 inner product; UNCOVERED; equivariance of the attention mechanism requires verification. |
| C044 | high | medium | domain_violation, unreferenced | G1,3 inner product as list of signs + Euclidean product; UNCOVERED; mathematical identity verifiable. |
| C045 | high | high | domain_violation, unreferenced | LayerNorm definition for multivectors with absolute value of grade norms; UNCOVERED; the use of |⟨·,·⟩| with potentially negative norm requires justification. |
| C046 | high | medium | domain_violation | "G1,3 norm can have zero and negative contributions"; standard property of indefinite-signature metric — verifiable. |
| C047 | low | low | unreferenced | ε value has negligible impact; UNCOVERED; empirical claim but low importance. |
| C048 | high | high | domain_violation, unreferenced | "Activation functions directly on multivectors break equivariance"; UNCOVERED; standard equivariance argument — verifiable formally. |
| C049 | high | high | domain_violation, unreferenced | Scalar-gated activation Activation(x)=GELU(⟨x⟩0)·x preserves equivariance; UNCOVERED; requires formal proof that multiplying by a scalar scalar function preserves grade structure. |
| C050 | high | high | domain_violation, unreferenced | Geometric product GP(vxv⁻¹,vyv⁻¹)=v·GP(x,y)·v⁻¹ equivariance; UNCOVERED; verifiable algebraically. |
| C051 | high | medium | unreferenced, ambiguous | Full L-GATr block structure; UNCOVERED; the specific composition and residual connections are novel; "ambiguous" because the nesting order is underspecified in prose. |
| C052 | medium | medium | unreferenced, ambiguous | Scalar channels as smooth transition to standard transformers; UNCOVERED; "smooth transition" is underspecified. |
| C053 | medium | medium | unreferenced, literature_collision | "Lorentz symmetry is only partially preserved in many LHC contexts"; UNCOVERED; checkable against standard LHC phenomenology. |
| C054 | high | medium | unreferenced, ambiguous | "Performance can degrade significantly" without symmetry-breaking treatment; UNCOVERED; "significantly" is unquantified. |
| C055 | high | medium | domain_violation, unreferenced | Equivariant architecture treats Lorentz-related inputs as equivalent — correct by definition but UNCOVERED; a domain claim about equivariant network behavior. |
| C056 | high | medium | domain_violation, unreferenced | "Blind to differences when symmetry is broken"; follows from equivariance definition — verifiable formally; UNCOVERED. |
| C057 | high | medium | unreferenced, ambiguous | Symmetry breaking via reference multivectors described as "tunable"; UNCOVERED; "tunable" is vague. |
| C058 | high | high | domain_violation, unreferenced | Any network operation involving a reference vector "violates equivariance, breaking to a subgroup where the reference direction is fixed"; UNCOVERED; formal claim verifiable. |
| C059 | medium | low | unreferenced | Network can "tune out" reference vectors; UNCOVERED; interpretive/design claim. |
| C060 | high | medium | unreferenced, literature_collision | "Enforcing symmetry then breaking with reference vectors produces better results"; UNCOVERED; comparative performance claim requiring experimental support. |
| C061 | medium | low | unreferenced | Technical detail of reference vector insertion; UNCOVERED. |
| C062 | medium | medium | domain_violation, unreferenced | Data augmentation instruction (augment inputs only, then append references); UNCOVERED; correctness follows from equivariance argument. |
| C063 | high | high | domain_violation, unreferenced | Beam direction breaks Lorentz group to rotations + boosts along beam axis; UNCOVERED; standard LHC physics — verifiable against field knowledge. |
| C064 | high | high | domain_violation, unreferenced | Specific beam-direction multivectors x V± = (0,0,0,±1) or xB12=1; UNCOVERED; claims these implement the beam subgroup — domain verifiable. |
| C065 | medium | medium | unreferenced, internal_contradiction | "Similar performance for both beam direction representations"; UNCOVERED; internal numerical claim — check against tables. |
| C066 | medium | medium | domain_violation, unreferenced | Detector setup compromises boost symmetry of observables; UNCOVERED; standard experimental physics claim. |
| C067 | high | high | domain_violation, unreferenced | Breaking to SO(3) via xV=(1,0,0,0); UNCOVERED; domain verifiable against Lorentz subgroup theory. |
| C068 | high | high | domain_violation, unreferenced | Reference xV±=(1,0,0,±1) breaks Lorentz to SO(3) spatial rotations; UNCOVERED; domain verifiable. |
| C069 | medium | medium | internal_contradiction, unreferenced | "Reference multivectors as extra tokens for jet tagging, extra channels for generation"; UNCOVERED; should cohere with Sections 4 and 5. |
| C070 | high | medium | unreferenced, ambiguous | "Symmetry breaking is crucial and has strong impact on performance"; UNCOVERED; "crucial" and "strong impact" are unquantified. |
| C071 | medium | medium | domain_violation, unreferenced | Kinematic inputs (pT, E, ΔR) embedded as scalars — only invariant under rotations around beam axis; UNCOVERED; domain claim about which subgroup those quantities respect. |
| C072 | medium | medium | unreferenced, ambiguous | Overwriting pT and m velocity components with scalar outputs; UNCOVERED; specific methodological choice. |
| C073 | medium | medium | unreferenced, literature_collision | GNNs and transformers both process sets with permutation symmetry; COVERED by vaswani2017/zaheer2017; factual but worth checking against those references. |
| C074 | medium | medium | unreferenced, ambiguous | "Resource efficiency is where GNNs and transformers differ most"; COVERED by flashattention reference but "most" is an unquantified comparative. |
| C075 | medium | low | unreferenced | Benchmark methodology description (H100 GPU); UNCOVERED; low importance but no citation for the comparison protocol. |
| C076 | low | low | unreferenced | Architecture parameter for scaling test (72 channels, 4 heads); UNCOVERED; implementation detail. |
| C077 | low | low | unreferenced | L-GATr 8 multivector + 16 scalar = 72 attention input channels; UNCOVERED; implementation detail, internally checkable. |
| C078 | high | high | unreferenced, internal_contradiction | Parameter counts: L-GATr 2.3×10⁴, transformer 6.7×10⁵, CGENN 2.5×10⁴; UNCOVERED; specific numerical claim — internally verifiable. |
| C079 | medium | high | unreferenced, literature_collision | Evaluation time: constant for few tokens then quadratic; COVERED by vaswani2017; standard transformer complexity — checkable. |
| C080 | medium | medium | unreferenced, ambiguous | "Transition to quadratic when attention becomes limiting" — standard but COVERED by dao2022flashattention; interpretation rather than a novel claim. |
| C081 | high | high | unreferenced, internal_contradiction | L-GATr scales like standard transformer in many-token regime; COVERED by dao2022flashattention; should cohere with C082 and C084. |
| C082 | high | high | unreferenced, internal_contradiction | L-GATr slower than transformer for few tokens due to expensive linear layers; UNCOVERED; must cohere with C081 and scaling figures. |
| C083 | high | high | unreferenced, literature_collision | CGENN slower than L-GATr for few tokens, quadratic scaling takes off sooner; COVERED by ruhe2023clifford context; checkable against that baseline. |
| C084 | high | high | unreferenced, internal_contradiction | L-GATr and transformer display same linear memory scaling; COVERED by dao2022flashattention; must cohere with C081/C082/C085. |
| C085 | high | high | unreferenced, literature_collision | CGENN scales quadratically in memory, runs out at 1000 particles; COVERED by ruhe2023clifford; specific numerical threshold checkable. |
| C086 | medium | low | ambiguous | Difference in memory scaling attributed to "different degree of optimization"; vague interpretation, low checkability. |
| C087 | medium | high | unreferenced, literature_collision | L-GATr uses FlashAttention; COVERED by dao2022flashattention; verifiable. |
| C088 | medium | medium | unreferenced, literature_collision | GNNs optimized for sparse graphs, efficiency degrades for fully connected; COVERED by ruhe2023clifford context; standard claim. |
| C089 | medium | high | unreferenced, literature_collision | Partonic amplitudes calculable exactly as function of phase space; COVERED by aylett2021diphoton/maitre2021; verifiable. |
| C090 | medium | high | unreferenced, literature_collision | Amplitude evaluation expensive for high-order corrections / many particles; COVERED by badger2023loopamps; verifiable. |
| C091 | medium | high | unreferenced, literature_collision | Amplitude surrogates speed up event generators; COVERED by aylett2021diphoton/badger2023loopamps; verifiable. |
| C092 | high | medium | unreferenced, literature_collision | "Standard neural networks struggle to reach sufficient accuracy for high-multiplicity amplitudes"; COVERED by badger2023loopamps; requires quantitative support. |
| C093 | high | medium | unreferenced, ambiguous | L-GATr uses "partial permutation symmetry to scale to high multiplicities"; UNCOVERED; "partial permutation symmetry" is underspecified. |
| C094 | high | high | domain_violation, unreferenced | "L-GATr guarantees exact Lorentz invariance of the amplitude"; UNCOVERED; strong formal claim — requires proof that the output is a Lorentz scalar. |
| C095 | medium | high | unreferenced, literature_collision | Training data: 4×10⁵ points per multiplicity from MadGraph at LO; COVERED by alwall2014madgraph; verifiable. |
| C096 | medium | medium | unreferenced | Phase space cuts (pT>20 GeV, ΔR>0.4); UNCOVERED; standard but uncited. |
| C097 | medium | medium | unreferenced, ambiguous | Training on standardized log amplitudes A=(log A − log Ā)/σ; UNCOVERED; normalization choice not cited. |
| C098 | medium | high | unreferenced, literature_collision | Benchmarks: MLP, transformer, GAP, DSI, CGENN; COVERED partially; should match published descriptions of those baselines. |
| C099 | medium | medium | unreferenced | 4-momenta inputs except DSI (also Minkowski products); UNCOVERED; setup detail. |
| C100 | high | high | unreferenced, literature_collision | "Transformer and graph networks scale better than MLPs for Z+ng"; UNCOVERED; key result — should align with or supersede published MLP/transformer comparisons. |
| C101 | high | high | unreferenced, literature_collision | "L-GATr roughly on par with DSI for small gluon count, leads for higher multiplicity"; UNCOVERED; headline comparison result. |
| C102 | high | medium | unreferenced, literature_collision | Scaling improvement consistent with equivariant approximation theorem; COVERED by maitre2024optimal; theoretical support claim — checkable against that reference. |
| C103 | medium | medium | unreferenced | L-GATr performs well trained on all processes jointly; UNCOVERED; positive result but no comparison baseline given. |
| C104 | high | high | unreferenced, literature_collision | "L-GATr stands as top performer on all training regimes when scaling with dataset size"; UNCOVERED; broad headline claim. |
| C105 | high | medium | unreferenced, literature_collision | "L-GATr and CGENN very efficient for small training sets due to equivariance"; UNCOVERED; comparative efficiency claim. |
| C106 | medium | low | unreferenced | Architecture size reduction for Z+5g (4×10⁴ params, 4×10⁴ data points); UNCOVERED. |
| C107 | medium | low | unreferenced | Dataset reduction to 4×10⁴ for Z+5g; UNCOVERED; methodology detail. |
| C108 | medium | medium | unreferenced | L-GATr reproduces scaling for Z+5g; UNCOVERED; positive result claim. |
| C109 | low | low | unreferenced | Small-data comparison setup (transformer and DSI); UNCOVERED. |
| C110 | medium | high | unreferenced, literature_collision | "Jet tagging is the LHC task most impacted by modern ML"; COVERED by kasieczka2019toptagger/plehn2022modern; checkable. |
| C111 | high | high | unreferenced, literature_collision | "Two approaches stand out: transformer-based and equivariant networks"; COVERED by qu2022part/gong2022lorentznet/pelican2024jhep; verifiable. |
| C112 | high | high | unreferenced, literature_collision, internal_contradiction | "L-GATr sets a new record for jet tagging"; UNCOVERED; must cohere with C117/C129/C138 and not overstate vs. literature baselines. |
| C113 | medium | high | unreferenced, literature_collision | Top tagging dataset: 2M jets pT=550-650 GeV; COVERED by kasieczka2019dataset; verifiable. |
| C114 | medium | high | unreferenced, literature_collision | Generated with Pythia8 + Delphes ATLAS card; COVERED by sjostrand2015pythia/delphes2014; verifiable. |
| C115 | medium | high | unreferenced, literature_collision | Train/val/test split 1.2/0.4/0.4M; COVERED by kasieczka2019dataset; verifiable. |
| C116 | medium | high | unreferenced, literature_collision | Baselines: LorentzNet, PELICAN, CGENN, ParT, MIParT; COVERED by corresponding references; verifiable that descriptions match published values. |
| C117 | high | high | unreferenced, literature_collision, internal_contradiction | "L-GATr at least on par with leading equivariant baselines on top tagging"; UNCOVERED; must cohere with C112 and with published baseline numbers. |
| C118 | medium | medium | unreferenced | Reference vectors (beam bivector xB12=1 and time xV=(1,0,0,0)) for tagging; UNCOVERED. |
| C119 | high | medium | unreferenced, internal_contradiction | "Including both beam direction and time reference significantly boosts tagging"; UNCOVERED; must cohere with ablation tables. |
| C120 | low | low | unreferenced | Best setup selected by AUC; UNCOVERED; methodological choice. |
| C121 | low | low | unreferenced, ambiguous | Background rejection not used as deciding factor due to "larger uncertainty"; UNCOVERED; vague justification. |
| C122 | medium | high | unreferenced, literature_collision | JetClass dataset description (10 classes, various jets); COVERED by qu2022part; verifiable. |
| C123 | medium | high | unreferenced, literature_collision | JetClass generated with MadGraph+Pythia, Delphes CMS card; COVERED by alwall2014madgraph/sjostrand2015pythia/delphes2014; verifiable. |
| C124 | medium | high | unreferenced, literature_collision | JetClass kinematic cuts pT=500-1000 GeV, |η|<2.0; COVERED by qu2022part; verifiable. |
| C125 | medium | high | unreferenced, literature_collision | JetClass: 100M jets, 10 classes equally distributed; COVERED by qu2022part; verifiable. |
| C126 | medium | high | unreferenced, literature_collision | JetClass input features (4-momenta, kinematics, PID, trajectory displacement); COVERED by qu2022part; verifiable. |
| C127 | medium | medium | unreferenced | Non-4-momenta JetClass features embedded as scalars; UNCOVERED. |
| C128 | low | low | unreferenced | Same architecture as top tagging used for JetClass; UNCOVERED. |
| C129 | high | high | unreferenced, literature_collision, internal_contradiction | "Significant improvement over ParT and MIParT in essentially all signal types on JetClass"; COVERED by qu2022part/wu2024mipart; must match table numbers and not conflict with those references' own claims. |
| C130 | high | medium | unreferenced, internal_contradiction | "L-GATr quality steadily increases as more features added"; UNCOVERED; must cohere with feature-ablation tables. |
| C131 | high | high | unreferenced, literature_collision | "L-GATr achieves similar performance to ParT/MIParT with only 10% of jets"; UNCOVERED; strong data-efficiency claim — must not contradict published ParT data-efficiency results. |
| C132 | medium | medium | unreferenced, literature_collision | Pre-training motivation from large transformer capacity; COVERED by qu2022part; verifiable. |
| C133 | medium | medium | unreferenced | Pre-trained on JetClass, fine-tuned for top tagging; UNCOVERED. |
| C134 | medium | low | unreferenced | Pre-training limited to 4-momenta and kinematic variables; UNCOVERED. |
| C135 | medium | medium | unreferenced, literature_collision | Pre-training/fine-tuning procedure follows ParT (Ref. [59]); COVERED by qu2022part; verifiable that the procedure matches. |
| C136 | medium | low | unreferenced | Fine-tuning: last layer re-initialized; UNCOVERED. |
| C137 | medium | low | unreferenced, ambiguous | Fine-tuning uses smaller LR for pre-trained weights; UNCOVERED; "might dismiss all information" is informal. |
| C138 | high | high | unreferenced, literature_collision, internal_contradiction | "L-GATr matches performance of best fine-tuned networks across all metrics"; UNCOVERED; must cohere with C112/C117/C129 and with published fine-tuned baseline numbers. |
| C139 | medium | low | ambiguous | "Superior performance illustrates combined impact of equivariance and pre-training"; interpretive, low checkability. |
| C140 | medium | high | unreferenced, literature_collision | "Generating LHC events is a key benchmark"; COVERED by badger2023mllhc/butter2019howtoganevents; verifiable. |
| C141 | medium | medium | unreferenced | Event generation required for importance sampling, unfolding, inference; COVERED by heimel2023madnis; checkable. |
| C142 | high | medium | unreferenced, ambiguous | "Per-mille-level (or at least percent-level) accuracy required for event generation"; UNCOVERED; the numeric threshold is asserted without citation. |
| C143 | medium | medium | unreferenced | Reference process pp→tt̄h+nj, n=0-4; UNCOVERED; process choice unlinked to external motivation. |
| C144 | medium | high | unreferenced, literature_collision | Simulation chain: MadGraph3.5.1+Pythia8+Delphes3+anti-kT R=0.4; COVERED by alwall2014madgraph/sjostrand2015pythia/delphes2014/cacciari2008antikt; verifiable. |
| C145 | medium | medium | unreferenced | Pythia without MPI, default ATLAS card; COVERED by sjostrand2015pythia; checkable. |
| C146 | medium | medium | unreferenced | Phase space cuts for event generation (pT>22 GeV, ΔRjj>0.5, |η|<5, 2 b-tags); UNCOVERED. |
| C147 | medium | low | unreferenced | χ2-based reconstruction + pT ordering; UNCOVERED. |
| C148 | medium | medium | unreferenced, internal_contradiction | Dataset sizes 9.8M/7.2M/3.7M/1.5M/480k for n=0-4; UNCOVERED; internal cross-check possible. |
| C149 | high | high | unreferenced, literature_collision | CNFs learn transition between latent and phase space; COVERED by chen2018node/lipman2022flowmatching; foundational claim verifiable. |
| C150 | high | high | domain_violation, unreferenced | ODE/continuity equation formulation of CNFs; COVERED by chen2018node/lipman2022flowmatching; verifiable against those references. |
| C151 | high | high | domain_violation, unreferenced | Diffusion process boundary conditions t→0/t→1; COVERED by lipman2022flowmatching; verifiable. |
| C152 | high | high | unreferenced, literature_collision | Linear interpolation x(t)=(1-t)x0+tx1 as CFM training objective; COVERED by lipman2022flowmatching; verifiable. |
| C153 | high | high | unreferenced, literature_collision | MSE loss encoding CFM-velocity vθ≈x1−x0; COVERED by lipman2022flowmatching; verifiable. |
| C154 | high | medium | unreferenced, literature_collision | Unconditional matches conditional velocity field; COVERED by lipman2022flowmatching; verifiable. |
| C155 | high | high | unreferenced, literature_collision | ODE solver for generation x0=x1−∫vθ dt; COVERED by chen2018node; verifiable. |
| C156 | medium | medium | unreferenced | Comparison architectures: MLP, transformer, E(3)-GATr as CFM baselines; UNCOVERED except brehmer2023gatr context. |
| C157 | high | high | unreferenced, literature_collision | "CFM is currently the leading technique for precision LHC event generation"; COVERED by butter2023jetdiffusion; verifiable but "currently" is time-sensitive. |
| C158 | medium | medium | domain_violation, unreferenced | E(3)-GATr translational features omitted (not needed for this task); UNCOVERED; domain claim about what translational equivariance contributes. |
| C159 | medium | medium | domain_violation, unreferenced | Process symmetric only under rotations around beam axis, hence symmetry breaking; UNCOVERED; standard LHC physics claim. |
| C160 | medium | medium | unreferenced | E(3)-GATr reference: plane orthogonal to beam; UNCOVERED. |
| C161 | medium | medium | domain_violation, unreferenced | L-GATr also needs time reference because distribution not invariant under beam boosts; UNCOVERED; domain claim. |
| C162 | high | high | domain_violation, unreferenced | "Impossible to construct a normalized density invariant under a non-compact group"; UNCOVERED; this is a standard mathematical result — verifiable. |
| C163 | medium | medium | unreferenced, literature_collision | Equivariant generator uses symmetry-invariant base distribution; COVERED by lipman2022flowmatching; verifiable. |
| C164 | medium | medium | unreferenced | Gaussian base distribution in (px,py,pz,log m²); UNCOVERED. |
| C165 | medium | medium | unreferenced | Rejection sampling for phase space constraints; UNCOVERED. |
| C166 | medium | low | unreferenced, ambiguous | "Phase space parametrization for straight trajectories is crucial"; UNCOVERED; "crucial" unquantified. |
| C167 | medium | low | unreferenced | MLP/transformer parametrization f⁻¹(p)=(log(pT-pTmin), log m², η, φ); UNCOVERED. |
| C168 | low | low | unreferenced | Standardization of x-coordinates; UNCOVERED. |
| C169 | low | low | unreferenced | Azimuthal angle periodicity handling; UNCOVERED. |
| C170 | low | low | unreferenced | Minimum-distance path crossing φ=±π boundary; UNCOVERED. |
| C171 | medium | medium | unreferenced, ambiguous | L-GATr velocity pipeline: f(x)→p→L-GATr→vp; UNCOVERED; multi-step transformation described at high level. |
| C172 | medium | medium | unreferenced, domain_violation | Jacobian-based velocity transformation vx=(∂f⁻¹/∂p)vp; UNCOVERED; requires verification that the chain rule is applied correctly. |
| C173 | medium | medium | unreferenced, domain_violation | Large Jacobian from log transformations near m≈0 and pT≈pTmin causes instability; UNCOVERED; domain claim about numerical conditioning. |
| C174 | medium | medium | unreferenced | Overwriting problematic velocity components with scalar L-GATr outputs; UNCOVERED. |
| C175 | medium | low | unreferenced, ambiguous | This adds "additional redundant source of symmetry breaking"; UNCOVERED; "redundant" is ambiguous. |
| C176 | low | low | unreferenced | E(3)-GATr uses (px,py,pz) as vector and xm as scalar; UNCOVERED. |
| C177 | low | low | unreferenced | E(3)-GATr same transformation without changing xm; UNCOVERED. |
| C178 | medium | medium | unreferenced, internal_contradiction | Table 6 studies data representation/base distribution/trajectory choices; UNCOVERED; internally checkable. |
| C179 | medium | medium | unreferenced, internal_contradiction | Table 7 compares symmetry breaking schemes; UNCOVERED; internally checkable. |
| C180 | high | high | unreferenced, literature_collision, internal_contradiction | "L-GATr outperforms baselines across all 1D distributions"; UNCOVERED; headline generation result — must cohere with tables and baseline results. |
| C181 | high | high | unreferenced, literature_collision, internal_contradiction | "Angular correlations benefit most from equivariance, enabling percent-level precision for the first time"; UNCOVERED; "for the first time" requires citation support. |
| C182 | high | medium | unreferenced, ambiguous | "Main weakness: intermediate top mass poles requiring 3-body correlation"; UNCOVERED; "main weakness" is interpretive but checkable against generation quality figures. |
| C183 | high | high | unreferenced, literature_collision, internal_contradiction | "Clear performance improvement: MLP < transformer < E(3)-GATr < L-GATr"; UNCOVERED; ordered comparison requires numerical support for each step. |
| C184 | high | high | unreferenced, internal_contradiction | "Superior L-GATr performance mainly from boost-equivariance"; UNCOVERED; must cohere with C185 and ablation. |
| C185 | high | high | unreferenced, internal_contradiction, literature_collision | "E(3)-GATr only marginally better than plain transformer"; UNCOVERED; must cohere with C183/C184 ordering and not conflict with brehmer2023gatr claims. |
| C186 | high | medium | unreferenced, ambiguous | "Enforcing then breaking equivariance outperforms non-equivariant networks"; UNCOVERED; "outperforms" unquantified in this claim. |
| C187 | low | low | ambiguous | "Modern ML has evolved from concept development to first applications"; vague historical claim. |
| C188 | low | low | ambiguous | "Performance is the main goal in LHC applications"; interpretive framing. |
| C189 | low | low | ambiguous | "LHC physics is in the lucky situation that known phase space structure can be used"; interpretive. |
| C190 | medium | medium | unreferenced, literature_collision | Encoding Lorentz symmetry avoids learning it; COVERED by butter2018lorentz; verifiable. |
| C191 | high | high | unreferenced, literature_collision | "Lorentz-group representation enhances performance of essentially every ML application on relativistic phase space"; UNCOVERED; very broad headline claim. |
| C192 | high | medium | unreferenced, ambiguous | Equivariant network can break symmetries using reference frames; UNCOVERED; mechanism described vaguely. |
| C193 | high | high | unreferenced, literature_collision, internal_contradiction | "Breaking symmetries with reference frames leads to significantly better performance than removing equivariance"; UNCOVERED; must cohere with ablation tables. |
| C194 | medium | medium | unreferenced | L-GATr described as "versatile equivariant transformer for regression, classification, generation"; UNCOVERED; summary claim. |
| C195 | high | high | unreferenced, literature_collision, internal_contradiction | "L-GATr best for amplitude regression with >3 particles"; UNCOVERED; must cohere with C100/C101/C104 and with competitor results. |
| C196 | high | medium | unreferenced, ambiguous | "Best performance comes from superior data efficiency and improved scaling with phase space dimensionality"; UNCOVERED; causal attribution is ambiguous. |
| C197 | high | high | unreferenced, literature_collision, internal_contradiction | "Jet tagging: L-GATr at least on par with best available tagger"; UNCOVERED; must cohere with C112/C117/C129/C138. |
| C198 | high | high | unreferenced, literature_collision, internal_contradiction | "L-GATr+CFM faithfully reproduces pp→tt̄h+nj phase space better than all other CFM setups"; UNCOVERED; broadest generation headline claim — must cohere with C180/C183. |
| C199 | low | medium | unreferenced | GitHub URL for code availability; UNCOVERED; verifiable factually. |
| C200 | low | medium | unreferenced | GitHub URL for reproduction; UNCOVERED; verifiable factually. |

---

## Priority summary for checker agents

### Tier 1 — Highest priority (importance=high, checkability=high)

Every claim in the table with `importance=high` and `checkability=high` must
receive a thorough verdict from every checker. The following claim clusters
are the most consequential:

**Headline performance claims (cross-section of all three tasks):**
C001, C004, C100, C101, C104, C112, C117, C129, C131, C138, C180, C181,
C183, C184, C185, C191, C193, C195, C197, C198

These are the paper's core empirical contribution. They are almost all
UNCOVERED and must be checked for (a) internal consistency with tables,
(b) consistency with published baseline numbers, and (c) whether "significant
improvement" or "new record" language is warranted.

**Algebraic / architectural correctness claims:**
C019, C020, C022, C024, C027, C032, C034, C035, C038, C039, C041, C043,
C044, C045, C048, C049, C050, C094

These are the paper's core formal claims. Errors here would undermine the
architecture's stated equivariance guarantee. Primary category: `domain_violation`.

**CFM theoretical framework claims:**
C149, C150, C151, C152, C153, C154, C155, C162

Standard CNF/CFM mathematics — verifiable against lipman2022flowmatching and
chen2018node; any mismatch is a `literature_collision` or `domain_violation`.

### Tier 2 — Medium priority (importance=high, checkability=medium)

C002, C003, C007, C015, C021, C023, C025, C026, C028, C029, C031, C036,
C040, C046, C051, C054, C055, C056, C057, C058, C060, C063, C064, C067,
C068, C070, C078, C081, C082, C083, C084, C085, C092, C093, C102, C105,
C111, C119, C130, C142, C157, C186, C192, C196

### Tier 3 — Lower priority (importance=medium or low)

All remaining claims are still checked but checkers may allocate less time.
Claims with checkability=low and importance=low are the lowest priority.

---

## Notes for specific checkers

**checker_unreferenced:** Focus on UNCOVERED claims making quantitative or
comparative assertions: C001, C004, C007, C060, C070, C094, C100, C101,
C104, C112, C129, C131, C138, C142, C157, C162, C180, C181, C191, C193,
C195, C197, C198. "UNCOVERED" in LITERATURE.md is not itself a flag but is
strong motivation to inspect surrounding paper text for in-text citations.

**checker_domain:** Focus on algebraic definition/property claims: C019–C027,
C031, C032, C034, C035, C038–C050, C055, C056, C058, C063, C064, C067, C068,
C094, C150, C151, C162, C172, C173. Also: C026 (γ5 real vs complex) and
C046 (indefinite norm in LayerNorm).

**checker_contradiction:** Focus on abstract-vs-results coherence: C001↔C004,
C112↔C117↔C129↔C138↔C197, C180↔C183↔C184↔C185, C195↔C100↔C101↔C104,
C198↔C180↔C183. Also check C078 parameter counts against any other
parameter references, and C069 (reference vector insertion mode per section).

**checker_literature:** Focus on claims with published baseline comparisons:
C012, C013, C083, C085, C100, C101, C102, C104, C111, C112, C117, C129,
C131, C138, C152, C153, C154, C155, C157, C180, C181, C183, C185. Verify
that reported baseline numbers match the corresponding published papers.

**checker_ambiguous:** Focus on unquantified superlatives and vague
comparatives: C001 ("wide range"), C004 ("significant improvements"), C015
("maximally expressive"), C054 ("degrade significantly"), C070 ("strong
impact"), C086 ("different degree of optimization"), C129 ("essentially all
signal types"), C181 ("for the first time"), C191 ("essentially every
ML-application"), C193 ("significantly better performance").
