# claim_extractor — log

## Summary

- Total claims extracted: **217** (`C001`–`C217`).
- Hedged claims: **4** (`C089`, `C109`, `C136`, `C179`).
- Per-type histogram (canonical, mechanically counted from `CLAIMS.md`):
  - `method` — 104
  - `result` — 46
  - `background_fact` — 46
  - `interpretation` — 8
  - `definition` — 7
  - `prior_work` — 5
  - `assumption` — 1
  - `UNCLASSIFIED` — 0

The paper is overwhelmingly methodological/empirical (150 of 217 rows, ≈ 69%, are `method` or `result`), with a substantial `background_fact` tail because §2.1 spells out a lot of geometric-algebra facts as common knowledge.

## Page approximations

- `paper.txt` is the LaTeX source. There are no native page numbers, so every `page` cell is `?`.
- `line` is set equal to the line number in `paper.txt` where the sentence begins.
- `section` uses the LaTeX section structure: `Abstract`, `1`, `2.1`, `2.2`, `2.3`, `2.4`, `3`, `4`, `5`, `6`, `Code`, `App.A`. Subsubsection-headed paragraphs (e.g. *Performance*, *Top tagging with JetClass pre-training*) are folded into their parent section number.
- `provenance` always points at the line where the **first** word of the quoted sentence begins. Multi-line sentences in the LaTeX source still resolve to one provenance.

## Boundary decisions

### Compound sentence splits

Several abstract / introduction sentences had to be split:

- The abstract sentence beginning "We demonstrate the power of L-GATr for amplitude regression and jet classification, and then benchmark it as the first Lorentz-equivariant generative network." was kept as one row (`C004`). The "first Lorentz-equivariant generative network" assertion is part of the same act of demonstration, so I did not split it.
- "We extend the amplitude regression analysis, improve the classification through pre-training and multi-class tagging, and deliver a competitive generative network for Monte Carlo event generation." → kept as one row (`C015`) because it lists the same act (the contributions of *this* paper), each clause typed uniformly as `method`.
- The §2.1 sentence about the "main limitation" was split into `C041` and `C042` (general limitation + specific consequence) and `C043` (the assumption clause "For most LHC applications…this is not a substantial limitation") and `C044` (the universal-approximation claim). All three are independently verifiable.
- §2.4 paragraph in line 358 was split into multiple `method` claims (`C077`–`C082`) because it asserts several distinct measurable facts (architecture, GPU, channel counts, parameter counts).
- §4 line 502 contains four claims about symmetry-breaking experiments; I split into `C118`, `C119`, `C120`, `C121`.
- §5 line 833 split into `C172`–`C176` (five distinct propositions about distributions, learnability, outperformance, angular precision, top-mass weakness).

### Hedging notes

- `C089` ("We attribute this to the different degree of optimization") — `we attribute` is a hedge marker, so `hedged=true`. Type `interpretation`.
- `C109` ("Jet tagging is, arguably, the LHC task…") — `arguably` is a hedge.
- `C136` ("During fine-tuning, the pre-trained model weights have to be updated…otherwise the network might dismiss…") — `might` hedge. Borderline `method`/`interpretation`; chose `method` because it's a procedural statement with a hedged justification.
- `C179` ("This might come as a surprise…") — `might` hedge; type `interpretation`.
- Sentences using "we expect" / "we observe" inside introductions were treated as non-hedged when they describe a measured outcome (e.g. `C169`, `C170`).

### Items deliberately skipped

- All section-pointer sentences ("After reviewing the construction of L-GATr in Sec.~\ref{sec:lgatr}, we demonstrate…" — describing what the paper does, not asserting a verifiable fact).
- Acknowledgements (line 858–866) — funding/personal acknowledgements.
- Pure equation lines — bare formulas without surrounding propositions.
- Captions of figures and tables — inspected, but not extracted because they restate claims already made in the body. The scaling caption (line 353) and the trajectory caption (line 734) duplicate prose claims already captured (`C083`–`C088` and `C159`–`C164`).
- Footnote at line 166 (supersymmetric multiplets) — inspected; the propositional content ("multivectors do not include all higher-rank irreps; supersymmetry does, via vector and chiral superfields") is a `background_fact` but the footnote phrasing is digressive. I chose to skip it because extraction would require substantive paraphrase. Logged here so a reviewer can decide whether to add it back.
- The list "Our reference process is $pp\to t_h \bar t_h + n j$" with cuts (lines 626–640) — the process description is captured in `C140`–`C143` and the cuts table is essentially a method specification absorbed into `C141`–`C142`. The bare equation $p_{T,j}>22$ etc. is not extracted as a standalone claim because the surrounding prose already covers it.
- The contents of Tables (toptagging, jctagging, trajectories, symbreak comparisons) — per the taxonomy, table numbers are not claims. The textual interpretations of those tables are extracted (`C117`, `C129`, `C137`, etc.).
- The list of contributions and architecture choices in Tab.~\ref{tab:layers} (line 311) is a structural diagram, not a propositional claim — captured by `C048` and the linear-layer claim `C050`.

### Ambiguous type decisions

- `C036` ("This decomposition is unique to the geometric algebra framework…") — could be `background_fact` (mathematical fact) or `result`. I tagged `result` because the sentence presents the decomposition as an outcome of *this* paper's framework choice, and the uniqueness claim is what the verifier would check.
- `C044` (multivector representation is "provably the most compact equivariant representation") — could be `prior_work` (since it is implicitly attributed) or `result`. I tagged `result` because the paper does not cite a specific reference for this claim and presents it as an own assertion.
- `C046` ("It is exactly equivariant under Lorentz group transformations Λ") — borderline `definition`/`result`. I tagged `result` because exact equivariance is a property the paper claims to have proved/constructed, not a defining axiom.
- `C060` ("It can be shown that this architecture is maximally expressive among all Lorentz-equivariant transformer designs.") — borderline `result`/`prior_work`. Tagged `result`. The proof is presumably elsewhere; the verifier should chase it.
- `C148` (CFM provides "optimal transport paths…uniquely suited") — borderline `result`/`background_fact`/`interpretation`. Tagged `result` with `medium` confidence; this is a normative/comparative claim.
- `C152` ("Strictly speaking, the underlying process is only symmetric under rotations around the beam axis.") — `background_fact` over `assumption` because the sentence is asserting a property of the data, not introducing an explicit assumption the paper depends on.
- `C181`, `C182` (outlook/summary) — interpretive generalizations across all three tasks; tagged `interpretation`. The claim "L-GATr improves on all three tasks" is `C187`, which is also `interpretation` (universally beneficial inductive bias) rather than `result` because it generalises beyond the measurements shown.

### Items the reviewer may want to revisit

1. The taxonomy split between `method` and `definition` is fuzzy for many architecture statements (e.g. `C054` "we define layer normalization using…"). I tagged these as `method` because they describe what the paper does, but they could equally be `definition` (the paper introducing a formal object).
2. Several `background_fact` entries in §2.1 (e.g. `C022`, `C026`–`C030`) restate textbook geometric-algebra facts. They are still verifiable against textbooks/PDG-style references and so are kept; a reviewer may opt to drop them as too elementary.
3. The list `C188`/`C189` (code availability URLs) — these are method claims (about reproducibility / code availability), not pure references. I included them; if the convention prefers to skip them, they can be removed.
4. `C015` (paper's contributions sentence) — kept whole; could alternatively be split into three rows (extend amplitude regression / improve classification via pre-training / deliver competitive generative network). The paper's structure (one section per contribution) means the more granular claims appear elsewhere.

## Hedged-row final tally

Explicit hedge markers detected and tagged `hedged=true`:
- `C089` ("we attribute")
- `C109` ("arguably")
- `C136` ("might")
- `C179` ("might")

Total hedged rows: **4**. (No hedge for "we believe", "we suggest", "we expect" etc. occurred in the paper text outside these four cases. "we observe"/"we find" were treated as direct observation reports, not hedges.)
