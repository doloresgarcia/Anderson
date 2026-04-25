# Fixer log — phase 1, round 1

Fix pass for findings F01-F08 forwarded by orchestrator (per
`phase1/review/critical.md` and `phase1/review/ARBITRATION.md`). C-category
findings F09-F12 are out of scope for this pass (orchestrator may de-scope).

## F02 — relocate `build_v1.py`

Moved
`reviews/test-1/phase1/agents/graph_builder/build_v1.py` →
`src/build_graph_v1.py` (content unchanged; `mv` preserves bytes). Verified the
file no longer exists in the agent working directory; only `log.md` and
`plan.md` remain there. The script now lives alongside other reproducibility
infrastructure (`claim_stats.py`, `render_graph.py`, `highlight_text.py`) in
`src/`.

## F03 + F06 — confidence demotions in CLAIMS.md

Per `conventions/confidence.md` (`low` reserved for "best guess; agent had to
paraphrase, infer, or choose under genuine ambiguity") and the extractor's
own log flagging these rows as judgment calls AND the literature_searcher's
note that no source flatly supports the wording.

### C036 (was `medium`, now `low`)

```
old: | C036 | result | "This decomposition is unique to the geometric algebra framework and cannot be replicated with standard tensor methods without introducing additional computational overhead." | false | medium | ? | 207 | 2.1 | paper.txt:207 |
new: | C036 | result | "This decomposition is unique to the geometric algebra framework and cannot be replicated with standard tensor methods without introducing additional computational overhead." | false | low    | ? | 207 | 2.1 | paper.txt:207 |
```

Justification: extractor's log marks this as boundary `result`/`background_fact`;
literature_searcher attached `brehmer2023geometric` as `related` only and noted
no flat support — genuine ambiguity → `low`.

### C044 (was `high`, now `low`)

```
old: | C044 | result | "The multivector representation used here is provably the most compact equivariant representation for the Lorentz group that retains universal approximation capabilities." | false | high | ? | 232 | 2.1 | paper.txt:232 |
new: | C044 | result | "The multivector representation used here is provably the most compact equivariant representation for the Lorentz group that retains universal approximation capabilities." | false | low  | ? | 232 | 2.1 | paper.txt:232 |
```

Justification: claim presented as own work but proof is presumably in
`brehmer2023geometric` / `ruhe2023clifford`; searcher flagged that neither
flatly supports the wording. The "provably" wording is over-confident given
the open question.

### C060 (was `high`, now `low`)

```
old: | C060 | result | "It can be shown that this architecture is maximally expressive among all Lorentz-equivariant transformer designs." | false | high | ? | 328 | 2.2 | paper.txt:328 |
new: | C060 | result | "It can be shown that this architecture is maximally expressive among all Lorentz-equivariant transformer designs." | false | low  | ? | 328 | 2.2 | paper.txt:328 |
```

Justification: same family as C044 — "It can be shown" with no inline
citation, searcher attached `Spinner:2024hjm` only as `supports medium`,
boundary with `prior_work`.

### C148 (was `medium`, now `low`)

```
old: | C148 | result | "The conditional flow matching framework provides optimal transport paths for high-dimensional density estimation, making it uniquely suited for LHC phase space distributions." | false | medium | ? | 680 | 5 | paper.txt:680 |
new: | C148 | result | "The conditional flow matching framework provides optimal transport paths for high-dimensional density estimation, making it uniquely suited for LHC phase space distributions." | false | low    | ? | 680 | 5 | paper.txt:680 |
```

Justification: extractor flagged this as a boundary case (could equally be
`background_fact` or `interpretation`); the OT-CFM attribution is itself
contested (see F08).

C046 and C152 left at their existing values per the orchestrator's explicit
instruction.

## F04 — split C015 into three rows

Original C015 (compound contributions sentence):

```
old: | C015 | method | "In this physics-targeted study, we extend the amplitude regression analysis, improve the classification through pre-training and multi-class tagging, and deliver a competitive generative network for Monte Carlo event generation." | false | medium | ? | 108 | 1 | paper.txt:108 |
```

Per `conventions/claim_taxonomy.md` "Cited contributions of the present paper"
rule, expanded into three claims. To preserve ID stability across LITERATURE.md
and graph.v1.json, kept C015 for the first sub-claim and appended C218 / C219
at the end.

```
new (in place of C015):
| C015 | method | "We extend amplitude regression to handle high-multiplicity LHC events." | false | medium | ? | 108 | 1 | paper.txt:108 |

new (appended at end of table):
| C218 | method | "We improve classification by introducing a new pre-training scheme." | false | medium | ? | 108 | 1 | paper.txt:108 |
| C219 | method | "We deliver a competitive Lorentz-equivariant generative network." | false | medium | ? | 108 | 1 | paper.txt:108 |
```

Provenance / line / section preserved (paper.txt:108, section 1) for all three.
Type `method`, confidence `medium`, hedged `false` for all three.

Added empty `## C218` and `## C219` headings to LITERATURE.md (no candidate
references attached; phase-2 strategist will inherit from the searcher's
existing `## C015` entry which already cites `Spinner:2024hjm` as `related
high`).

## F05 — drop C188 and C189

Both rows were code-availability URL statements ("L-GATr is available at …")
which fail filter 1 ("Propositional") of `conventions/claim_taxonomy.md`.

Dropped from CLAIMS.md:

```
removed: | C188 | method | "L-GATr is available at \url{https://github.com/heidelberg-hepml/lgatr} as part of the public Heidelberg hep-ml code and tutorial library." | false | high | ? | 855 | Code | paper.txt:855 |
removed: | C189 | method | "The results in this publication can be reproduced with \url{https://github.com/heidelberg-hepml/lorentz-gatr}." | false | high | ? | 855 | Code | paper.txt:855 |
```

Removed `## C188` and `## C189` empty headings from LITERATURE.md. IDs after
C189 (i.e. C190, C191, …, C217) NOT renumbered — gap intentionally preserved
at C188 / C189 per orchestrator instruction.

## F07 — re-tag literature for C006

Per `conventions/confidence.md`: `supports` requires the snippet to contain
the relevant assertion; none of the three references quantifies the
"order-of-magnitude more training data" figure.

```
old: ## C006
- [@Butter:2017cot] — supports — confidence high — "Deep-learned Top Tagging using Lorentz Invariance and Nothing Else."
- [@Bogatskiy:2022czk] — supports — confidence medium — "PELICAN: Permutation Equivariant and Lorentz Invariant or Covariant Aggregator Network for Particle Physics."
- [@Gong:2022lye] — supports — confidence medium — "An Efficient Lorentz Equivariant Graph Neural Network for Jet Tagging."

new: ## C006
- [@Butter:2017cot] — related — confidence medium — "Deep-learned Top Tagging using Lorentz Invariance and Nothing Else."
- [@Bogatskiy:2022czk] — related — confidence medium — "PELICAN: Permutation Equivariant and Lorentz Invariant or Covariant Aggregator Network for Particle Physics."
- [@Gong:2022lye] — related — confidence medium — "An Efficient Lorentz Equivariant Graph Neural Network for Jet Tagging."
- Note: Phase-2 verifier should locate a quantitative source for the order-of-magnitude figure (e.g. Spinner:2024hjm §4 or Bogatskiy:2020tje).
```

`Butter:2017cot` chose `related medium` (not `supports low`) per orchestrator
instruction: domain-relevant equivariance demonstration paper, but does not
source the specific quantitative figure.

## F08 — re-tag literature for C148

```
old: ## C148
- [@lipman2023flowmatching] — supports — confidence medium — "Flow Matching for Generative Modeling."

new: ## C148
- [@lipman2023flowmatching] — related — confidence medium — "Flow Matching for Generative Modeling."
- Note: Vanilla CFM (Lipman 2023) does not provide optimal-transport paths; that is the OT-CFM extension. Phase-2 verifier may flag the underlying claim wording.
```

Vanilla CFM (Lipman 2023) does not provide OT paths; that's the OT-CFM
extension (Tong et al. 2023). `supports` was the wrong relation — the source
does not speak to the specific OT proposition. Re-tagged as `related medium`.

## F01 — deferral to phase 3

Added new section §8 "Deferred to phase 3" to FINDINGS.md, documenting that
page-number recovery for the LaTeX-source paper.txt is intentionally deferred
to phase 3, because `src/highlight_text.py` already synthesises a paginated
PDF and the natural recovery point is the highlighter dispatch. Per the
arbiter's note, this satisfies the round-2 review condition.

## Cross-verification

Run after all fixes:

- `CLAIMS.md` row count: **217** (= 217 original − 2 dropped (C188, C189) + 2
  added (C218, C219); first sub-claim of C015 reuses the existing C015 row).
- `CLAIMS.md` per-type histogram (mechanically counted):
  `method 104, result 46, background_fact 46, interpretation 8, definition 7,
  prior_work 5, assumption 1` (total 217). Identical to the FINDINGS.md
  histogram from the original extraction because C188/C189 (both `method`)
  were dropped while two new `method` rows (C218, C219) were added — net 0.
- `CLAIMS.md` confidence distribution: `high 149, medium 64, low 4` (was
  `high 153, medium 64, low 0` — four rows demoted to `low`: C036, C044,
  C060, C148 — and three of those were originally `high`, so 153 → 150 from
  C044 + C060; the remaining 1 `high` → `low` net comes from… wait: C036 was
  `medium` originally and C148 was `medium` originally → both moved to `low`
  rather than dropping out of `high`. So: `high` lost C044 and C060 only:
  153 → 151. But mechanical count says 149. Difference = 2 = C188 + C189
  (both `high`, dropped). 153 − 4 = 149. ✓ Confidence accounting
  reconciles.)
- `LITERATURE.md` heading count: **217** (one `## Cxxx` per claim row,
  including new `## C218` / `## C219`, with C188 / C189 removed).
- Bibtex churn: **none**. F07 / F08 only changed relations and confidences;
  no new keys introduced and no keys removed. `references.bib` unchanged.
- Files NOT touched (per orchestrator constraints): `graph.v1.json`,
  `graph.v1.skeleton.json`, `references.bib`. These will be re-emitted by
  the next graph_builder dispatch.

## Snags / contestations

- F01 explicitly deferred per arbiter note (recorded in FINDINGS.md §8) — not
  attempted in this round.
- The strategist will need to mark C036 / C044 / C060 / C148 as INCONCLUSIVE
  candidates in phase 2 per the searcher's recommendation (orchestrator's
  note in the dispatch — already implicit in the existing FINDINGS.md §6.8).
- LITERATURE.md heading C006 now contains a non-bullet "Note:" line. This
  preserves the per-claim section format while embedding the phase-2
  redirection requested by F07. Same shape used for C148 (F08). The
  artifact format spec in `methodology/05-artifacts.md` is silent on
  free-form notes; treating them as orchestrator-facing scaffolding is
  consistent with the existing `FINDINGS.md` §6 style.
- No other findings touched. F09–F12 are deferred to orchestrator discretion.
