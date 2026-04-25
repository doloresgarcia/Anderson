# Critical review — phase 1 round 2 (test-1)

Single-bot review (the arbiter follows). Findings are flat A/B/C tagged
per `methodology/04-review.md`. Round-1 findings are referenced as F01–F12;
new round-2 findings use IDs G01, G02, ….

## Round-1 finding resolution audit

Each row was substantiated by a fresh independent read of the post-fixer
artifacts; the fixer's log was used only to locate the alleged change, not
as evidence of resolution.

| finding | status | evidence |
|---|---|---|
| F01 | DEFERRED — accepted | `phase1/outputs/FINDINGS.md` §8 "Deferred to phase 3" records the deferral verbatim, citing the round-1 ARBITRATION.md acceptance. Page-number recovery happens in phase 3 via `src/highlight_text.py`. |
| F02 | RESOLVED | `find phase1/agents -name "*.py"` returns nothing; `phase1/agents/graph_builder/` contains only `log.md` and `plan.md`. The equivalent script lives at `/afs/cern.ch/work/m/mgarciam/private/anderson/src/build_graph_v1.py` (and `build_graph_v1_round2.py` for the round-2 rebuild), alongside the other reproducibility scripts (`claim_stats.py`, `render_graph.py`, `highlight_text.py`). |
| F03 | RESOLVED | Mechanical count of `CLAIMS.md` confidence column: `{high: 149, medium: 64, low: 4}` (was `{153, 64, 0}`). The four `low` rows are exactly C036, C044, C060, C148 — matching the round-1 critical.md prescription. The same four rows carry `confidence: "low"` on their nodes in `graph.v1.json`. |
| F04 | RESOLVED structurally | C015 row sentence updated to "We extend amplitude regression to handle high-multiplicity LHC events." (first sub-claim only). New rows C218 ("We improve classification by introducing a new pre-training scheme.") and C219 ("We deliver a competitive Lorentz-equivariant generative network.") appended at the end of CLAIMS.md, both `method`, `medium`, line 108, parent G002. The paraphrasing in the three new sentences introduces drift from the source contributions sentence — see new finding G02. |
| F05 | RESOLVED | C188 and C189 absent from CLAIMS.md (no row), LITERATURE.md (no heading), and graph.v1.json (no claim node and not listed in any `claim_ids`). Id gap preserved — no renumbering. |
| F06 | RESOLVED | Subsumed by F03. C036, C044, C060 now `low`; the literature-mediated INCONCLUSIVE flagging is captured in the existing FINDINGS.md §6.8 narrative and in the strategist's input. |
| F07 | RESOLVED | `LITERATURE.md` ## C006 now lists three bullets all retagged from `supports`/(high or medium) to `related medium`, plus a "Note:" line directing the phase-2 verifier to `Spinner:2024hjm` §4 or `Bogatskiy:2020tje` for the order-of-magnitude figure. |
| F08 | RESOLVED | `LITERATURE.md` ## C148's single bullet retagged from `supports medium` to `related medium`, plus a "Note:" line flagging that vanilla CFM (Lipman 2023) does not provide OT paths and that phase-2 verifier may flag the underlying claim wording. |

## Auto-A trigger checks

- **Bibtex resolution.** All 34 cited keys in `LITERATURE.md` resolve in
  `references.bib` (set intersection: 34/34, 0 unresolved). No bibtex churn
  versus round 1 — F07/F08 were re-tags only, so the round-1 independent
  arXiv-pull verification of 13/34 entries still stands.
- **graph.v1.json schema validation.** Re-run on the rebuilt JSON: 20 groups
  (≤ 20); every group's `claim_ids` size in `[1, 15]` (range [7, 14]); every
  claim's `parent` resolves to an existing group, and the claim id is listed
  in that group's `claim_ids`; group-listed id set equals the 217-element
  claim id set; edges empty (vacuous endpoint / self-loop / inferred-low
  contradicts checks); every claim color = `#95A5A6` matching `NOT_CHECKED`;
  C188 / C189 absent; C218 / C219 present in G002; C036, C044, C060, C148
  carry `confidence: "low"` on the node. PASS.
- **CLAIMS.md provenance sample.** 12 rows sampled (mix unchanged + fixer-
  touched): C001, C006, C036, C044, C060, C100, C129, C148, C217 verified
  verbatim against `paper.txt`. C015, C218, C219 are paraphrases of the
  contributions sentence at line 108 (intended by F04) — split-from-compound
  is permitted by `claim_taxonomy.md`, but the paraphrase quality is the
  subject of new finding G02. **No row's `line` value disagrees with the
  paper.** No auto-A provenance failure.
- **Phase-1 outputs list.** `phase1/outputs/` contains exactly the six
  declared deliverables (CLAIMS.md, LITERATURE.md, references.bib,
  graph.v1.json, graph.v1.skeleton.json, FINDINGS.md). No extras.

**No auto-A trigger fired.**

## New findings (introduced this round)

| id | category | locus | finding | rule | resolution |
|----|----------|-------|---------|------|------------|
| G01 | B | `phase1/outputs/FINDINGS.md` §3 (confidence-distribution table + narrative); §5 (relation-distribution table); §6.4 (C148 confidence label); §6.5 (C188/C189 "kept" + C015 "kept whole" sentences) | FINDINGS.md was not re-emitted after the fixer's edits and now contains stale numbers and prose. Concretely: §3 says `{high 153, medium 64, low 0}` but actual is `{149, 64, 4}`; §3 narrative still says "no `low`-confidence rows"; §5 says `supports 74, related 39` but actual is `70, 43` (the 4-bullet shift is exactly F07's three retags + F08's one retag); §6.4 still labels C148 as `medium` (now `low`); §6.5 still narrates C188/C189 as kept and C015 as not-yet-split (both now reversed by F05/F04). The §8 deferral note for F01 is correct; everything else listed above is stale. | `methodology/05-artifacts.md` — STATS.md / FINDINGS.md numbers must match the underlying CLAIMS.md and LITERATURE.md. Stale post-fixer counts weaken the report (B), but do not block phase advancement (not A). | Re-run `src/claim_stats.py` (or its FINDINGS-equivalent) against the post-fixer artifacts and write a refreshed FINDINGS.md, leaving §8 intact. Mechanical fix; no LLM judgment required. |
| G02 | B | `phase1/outputs/CLAIMS.md` rows C015 (line 108), C218 (line 108), C219 (line 108) | The F04 split paraphrased the contributions sentence at `paper.txt:108` ("we extend the amplitude regression analysis, improve the classification through pre-training and multi-class tagging, and deliver a competitive generative network for Monte Carlo event generation") in a way that introduces or drops content: (a) C015 inserts the qualifier "high-multiplicity LHC events" — that string does not appear at line 108 (it appears later in §3 around line 381), so the C015 sentence is over-specific relative to the contributions list; (b) C218 drops "multi-class tagging" entirely — the paper enumerates pre-training **and** multi-class tagging as the contribution to classification, but C218 reduces it to "a new pre-training scheme"; (c) C219 substitutes the descriptor "Lorentz-equivariant" (correct in spirit but not literally in line 108) and drops "for Monte Carlo event generation". The split itself is correct per `conventions/claim_taxonomy.md` "Cited contributions of the present paper"; the paraphrase quality is the issue. All three rows are tagged `confidence = medium`, but per `confidence.md` paraphrase that requires inferring or substantially rewriting the proposition warrants `low`. | `conventions/claim_taxonomy.md` "Cited contributions of the present paper" (split is correct; faithfulness to the source proposition is required); `conventions/confidence.md` ("low — best guess; agent had to paraphrase, infer, or choose under genuine ambiguity"). | Either (a) tighten the three sentences so each is a faithful sub-proposition of line 108 — e.g. C015 → "We extend the amplitude regression analysis."; C218 → "We improve classification through pre-training and multi-class tagging."; C219 → "We deliver a competitive generative network for Monte Carlo event generation." — keeping confidence `medium` (split-from-compound anchor); or (b) keep the current paraphrases but demote all three rows to `confidence = low` with a justification line in the fixer log per `confidence.md` "When to override". (a) is preferred because it preserves the paper's enumeration intact. |
| G03 | C | `phase1/outputs/LITERATURE.md` ## C006 ("Note:" line) and ## C148 ("Note:" line) | The fixer added free-form `- Note: …` lines under the C006 and C148 headings to carry the F07/F08 phase-2 redirections. The artifact format spec in `methodology/05-artifacts.md` shows only bulleted candidate-reference rows under each heading; it is silent on free-form notes. The fixer's log explicitly flags this as a scaffolding choice consistent with FINDINGS.md §6 style. Strict downstream parsers that match `^- \[@…\] —` will ignore them harmlessly, but a parser that walks all bullet lines might mis-classify them. | `methodology/05-artifacts.md` LITERATURE.md format — silent, not violated. | Either (a) extend `methodology/05-artifacts.md` to permit free-form notes after the bullet list; or (b) move the F07/F08 phase-2 redirections to FINDINGS.md §7 where free-form prose is the established home. Pure C — does not block. |

## Section A — Blocking findings

(none)

## Section B — Weakening findings

G01, G02

## Section C — Suggestions

G03

## Verdict recommendation

Per `methodology/04-review.md` arbiter logic: zero Category-A; two Category-B
findings (G01, G02) — neither previously fixed → **ITERATE** (round 3).

Both B fixes are small and mechanical. G01 is a regen-FINDINGS.md task
(no LLM judgment). G02 is either a sentence-tightening (preferred) or a
confidence demotion on three rows (one-line fix). G03 may be addressed in
passing or de-scoped at the arbiter's discretion.

The arbiter may alternatively choose to defer G01 and G02 as tracked items
(analogously to F01's deferral) if the round-3 cost is judged disproportionate;
that is an arbiter call.
