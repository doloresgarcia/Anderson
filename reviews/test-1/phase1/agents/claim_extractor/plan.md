# claim_extractor — plan

## Inputs
- `paper/paper.txt` (977 lines, LaTeX source for "A Lorentz-Equivariant Transformer for All of the LHC")
- `paper/paper.meta.json` (mostly null, slug=test-1)

## Outputs (declared)
- `phase1/outputs/CLAIMS.md`
- `phase1/agents/claim_extractor/plan.md` (this file)
- `phase1/agents/claim_extractor/log.md`

## Strategy

1. **Scan the paper sequentially** by section. The paper has the structure:
   - Abstract (lines 53-65)
   - §1 Introduction (lines 78-114)
   - §2 L-GATr architecture (lines 117-362)
     - §2.1 Spacetime Geometric Algebra
     - §2.2 Constructing a Lorentz-Equivariant Architecture
     - §2.3 Breaking Lorentz Symmetry
     - §2.4 Scaling with Number of Particles
   - §3 Amplitude Regression (lines 366-434)
   - §4 Jet Tagging (lines 437-620)
   - §5 Event Generation (lines 623-835)
   - §6 Outlook (lines 838-850)
   - Code availability + Acknowledgements (skip — not claims)
   - Appendix A — Network and training details (lines 875-end)

2. **What I extract**:
   - Abstract claims (top-level results).
   - Background statements in §1 (asserted as common knowledge → background_fact or prior_work if cited).
   - Architecture/method statements (e.g. "We extend the scaled dot-product attention…") → `method`.
   - Mathematical/property assertions about the algebra and L-GATr (e.g. "Lorentz transformations will never mix grades") → `background_fact` or `definition`.
   - Numerical results from prose (not table rows themselves, but textual claims about the table outcomes).
   - Comparative claims (X outperforms Y, X is on par with Y) → `result`.
   - Hyperparameter and dataset statements in the appendix → `method`.

3. **What I skip**:
   - Pure procedural sentences ("Section 3 presents…", "We discuss the principles below").
   - Captions that simply describe figures without asserting facts (e.g. "Overview of marginal distributions for…").
   - Citation lists ("see [12] for details").
   - Acknowledgements, code availability section.
   - Future work / outlook intentions ("we look forward to…").
   - Pure equations and bare numbers without surrounding propositions.

4. **Granularity**: split compound sentences into one row per proposition. Most paper sentences are single-proposition; common splits are sentences with "and" joining two distinct claims, or "X, where Y" structures.

5. **Type assignment** (per `conventions/claim_taxonomy.md`):
   - `result` — numerical/comparative output of L-GATr or its baselines.
   - `method` — architecture, hyperparameters, training, dataset choice.
   - `prior_work` — claim attributed via citation key.
   - `background_fact` — domain fact stated as common knowledge.
   - `assumption` — explicitly stated assumption.
   - `interpretation` — causal/explanatory statement about results.
   - `definition` — formal definition.

6. **Hedge detection**: scan each candidate sentence for hedge markers `we suggest`, `we believe`, `may`, `might`, `appears to`, `it is likely that`, `we expect`, `arguably`, `we attribute`. Set `hedged=true` when present.

7. **Confidence**:
   - `high` — single proposition, unambiguous type, sentence essentially copied verbatim, no hedge.
   - `medium` — type sits between two categories, OR row split from compound, OR hedged.
   - `low` — paraphrase needed for standalone, OR ambiguous proposition, OR three-way type judgment.

8. **Provenance**: `paper.txt:<line>` of the line where the sentence starts. The paper is LaTeX → page is left as `?`. `section` is the LaTeX section number/label (e.g. `1`, `2.1`, `3`, `4`, `5`, `6`, `App.A`, `Abstract`).

## Verbatim quoting

Each `sentence` value is double-quoted verbatim. I keep LaTeX commands (`\cite`, `$…$`, `\ref`) intact. Where a paper sentence spans multiple lines in the LaTeX source, I quote it as a single logical sentence and use the line number where it begins.

For sentences split into multiple propositions (compound), each proposition is quoted as a clean sub-sentence in double quotes (the paper's exact wording for that clause). When unavoidable a tiny paraphrase is logged in `log.md`.

## Order of execution

1. Pass 1 — abstract → flag candidates.
2. Pass 2 — §1 Introduction.
3. Pass 3 — §2 (subsections) — heavy section, lots of method/definition/background_fact.
4. Pass 4 — §3 Amplitude Regression.
5. Pass 5 — §4 Jet Tagging.
6. Pass 6 — §5 Event Generation.
7. Pass 7 — §6 Outlook (mostly result-summary statements, some interpretation).
8. Pass 8 — Appendix A method/hyperparameter claims.
9. Renumber claim_ids sequentially `C001…`.
10. Write `CLAIMS.md`. Write `log.md` with boundary notes.
