# Arbitration — phase 1 round 2 (test-1)

VERDICT: PASS
Round: 2

Single-bot review mode (critical_reviewer only). Round-2 audit returned 0
Category-A, 2 Category-B (G01, G02), 1 Category-C (G03). All eight round-1
B findings (F01–F08) are RESOLVED or DEFERRED-ACCEPTED, substantiated by
the round-2 reviewer's independent reads of the post-fixer artifacts; the
auto-A trigger checks (bibtex 34/34; graph schema; CLAIMS.md provenance
sample 12/12; deliverables list) all pass.

## Policy rule applied

Two methodology rules are in tension on a round-2 review:

- `methodology/04-review.md` (strict arbiter logic):
  > "elif any B and not previously fixed: → ITERATE (spawn fixer, re-review)"

- `methodology/03a-orchestration.md` (operative CHECK-step policy):
  > "Category B → spawn fixer once, accept on re-review unless new A."

This dispatch is explicitly instructed to take the orchestration policy as
the operative rule for the round-2 verdict: a fixer pass has already
executed (round 1 → fixer → graph_builder rebuild → round 2). The round-2
reviewer introduced **zero Category-A findings**. Per
`methodology/03a-orchestration.md` the verdict is therefore PASS, and any
new-but-non-blocking B findings (G01, G02) are recorded as tracked items —
analogous to F01's phase-3 deferral accepted in round-1 ARBITRATION. Only
new As would have forced ITERATE.

Auto-A trigger checks audited in `critical_round2.md`:
- bibtex resolution 34/34, no churn since round 1;
- graph.v1.json schema validation passes (20 groups; |claim_ids| ∈ [7, 14];
  parent/child consistency; 217-claim id set = `{C001..C187, C190..C219}`;
  C188/C189 absent; C218/C219 in G002; C036/C044/C060/C148 carry
  `confidence: "low"`; edges empty; all colors `#95A5A6`);
- CLAIMS.md provenance 12-row sample matches `paper.txt` verbatim;
- `phase1/outputs/` contains exactly the six declared deliverables.

No fabricated-citation finding either round.

## Deduplicated findings (rounds 1 + 2)

| id  | category | locus | finding (one-line synopsis) | source-review | round-raised | fixer-pass-that-addressed-it | current-status |
|-----|----------|-------|------------------------------|---------------|--------------|------------------------------|----------------|
| F01 | B | `CLAIMS.md` `page` column (217 rows); claim nodes in `graph.v1.json` | All claims `page = ?` / `page = null`; `page_range` is line range. | critical (round 1) | 1 | round-1 fixer (deferral recorded in `FINDINGS.md` §8) | DEFERRED-ACCEPTED (phase 3) |
| F02 | B | `phase1/agents/graph_builder/build_v1.py` | graph_builder dropped helper script in working dir, exceeding role spec writes. | critical (round 1) | 1 | round-1 fixer (script moved to `src/build_graph_v1.py`) | RESOLVED |
| F03 | B | `CLAIMS.md` confidence column | Extractor used only `high`/`medium`; zero `low` despite extractor's own ambiguity flags. | critical (round 1) | 1 | round-1 fixer (4 rows demoted to `low`) | RESOLVED |
| F04 | B | `CLAIMS.md` row C015 | Triple compound contributions sentence kept as one row; taxonomy requires split. | critical (round 1) | 1 | round-1 fixer (split into C015 / C218 / C219; graph rebuilt) | RESOLVED structurally (paraphrase tightness raised separately as G02) |
| F05 | B | `CLAIMS.md` C188, C189 | Code-availability URL statements tagged `method`; not propositional. | critical (round 1) | 1 | round-1 fixer (rows dropped; ID gap preserved) | RESOLVED |
| F06 | B | `CLAIMS.md` C036, C044, C060 | Three expressivity claims at high/medium confidence with no flat support. | critical (round 1) | 1 | round-1 fixer (subsumed by F03 demotion to `low`) | RESOLVED |
| F07 | B | `LITERATURE.md` C006 | Three references attached at `supports high/medium` to a quantitative claim none of them sources. | critical (round 1) | 1 | round-1 fixer (retagged to `related medium` + Note line) | RESOLVED |
| F08 | B | `LITERATURE.md` C148 | `lipman2023flowmatching` tagged `supports medium` for OT-CFM claim that vanilla CFM does not source. | critical (round 1) | 1 | round-1 fixer (retagged to `related medium` + Note line) | RESOLVED |
| F09 | C | `graph.v1.json` `paper.title`/`paper.authors`; `paper.meta.json` | `paper.meta.json` empty; arXiv:2411.00446 not retrieved. | critical (round 1) | 1 | — (orchestrator-discretion C; not addressed) | OPEN (C, de-scopable) |
| F10 | C | `references.bib` (11 unused entries) | Eleven keys not cited from any `LITERATURE.md` bullet; `delphes` is a duplicate of `deFavereau:2013fsa`. | critical (round 1) | 1 | — | OPEN (C, de-scopable) |
| F11 | C | `CLAIMS.md` row C111 | Meta-sentence "we show how L-GATr sets a new record…" duplicates substantive C129. | critical (round 1) | 1 | — | OPEN (C, de-scopable) |
| F12 | C | `FINDINGS.md` §5 wording | Conflates "unused-by-LITERATURE.md" (11) with "uncited-in-paper" (8). | critical (round 1) | 1 | — | OPEN (C, de-scopable) |
| G01 | B | `phase1/outputs/FINDINGS.md` §3, §5, §6.4, §6.5 | Stale post-fixer numbers/prose in FINDINGS.md (confidence dist, relation dist, C148 label, C015/C188/C189 narrative). | critical (round 2) | 2 | — | TRACKED-ACCEPTED |
| G02 | B | `CLAIMS.md` C015 / C218 / C219 (line 108) | F04 split paraphrases drift from `paper.txt:108` (insertion of "high-multiplicity LHC events"; drop of "multi-class tagging"; substitution of "Lorentz-equivariant"; drop of "for Monte Carlo event generation"). | critical (round 2) | 2 | — | TRACKED-ACCEPTED |
| G03 | C | `LITERATURE.md` C006 / C148 ("Note:" lines) | Free-form `Note:` lines added under headings; `methodology/05-artifacts.md` is silent on the form. | critical (round 2) | 2 | — | TRACKED-ACCEPTED |

## Tracked-but-accepted items for downstream phases

The verdict is PASS subject to the following carry-forwards. The orchestrator
records each in the phase-1 commit message (or in `FINDINGS.md` §8) so the
phase-2 strategist and phase-3 highlighter inherit a clean handoff manifest.

- **F01 — page-number recovery.** Deferred to phase 3. Recovery happens
  during highlighter dispatch via `src/highlight_text.py`, which already
  synthesises a paginated PDF. `FINDINGS.md` §8 documents the deferral.
- **G01 — stale FINDINGS.md numbers and narrative.** The fixer's edits
  changed CLAIMS.md and LITERATURE.md but FINDINGS.md was not re-emitted.
  Concretely stale: §3 confidence histogram (`{153, 64, 0}` should be
  `{149, 64, 4}`); §3 narrative ("no `low`-confidence rows"); §5 relation
  histogram (`supports 74, related 39` should be `70, 43`); §6.4 C148
  confidence label; §6.5 C188/C189 "kept" + C015 "kept whole" sentences.
  Mechanical regen is cheap. **Recommendation:** the orchestrator either
  (a) regenerates FINDINGS.md once during phase-2 inheritance using
  `src/claim_stats.py` against the post-fixer artifacts (preserving §8),
  or (b) explicitly de-scopes G01 and lets phase-2 strategist read the
  numbers off CLAIMS.md and LITERATURE.md directly. (a) is preferred
  because it keeps FINDINGS.md authoritative.
- **G02 — paraphrase tightness on the C015 / C218 / C219 split.** The
  split itself satisfies F04 (taxonomy-mandated decomposition of the
  compound contributions sentence at line 108). The new sentences
  introduce drift from the source. **Phase-2 strategist must be aware
  that these three rows are slightly looser than verbatim-anchored** —
  in particular, when scoring evidence the strategist should treat
  C015's "high-multiplicity" qualifier and C218's missing "multi-class
  tagging" as paraphrase-level rewordings rather than precise paper
  propositions. Optional cheap fix: tighten the three sentences to
  faithful sub-propositions of line 108, or demote all three to
  `confidence: "low"`. Either path is acceptable; tightening is preferred.
- **G03 — `LITERATURE.md` `Note:` line format.** Free-form notes added
  under C006 and C148 to carry F07/F08 phase-2 redirections.
  `methodology/05-artifacts.md` is silent (not violated). Strict bullet
  parsers ignore them harmlessly. **Recommendation:** either extend
  `methodology/05-artifacts.md` to permit free-form notes, or move the
  redirections to `FINDINGS.md` §7. Pure C; orchestrator discretion.

## Next steps

PASS. The orchestrator should:

1. Optionally regenerate `FINDINGS.md` to retire G01 (mechanical;
   `src/claim_stats.py` against post-fixer artifacts; preserve §8).
2. Commit phase-1 deliverables with a conventional commit message per
   `phase1/CLAUDE.md` (e.g. `phase1(ingest): extract claims, lit search,
   build graph.v1`). Include in the commit message the tracked items
   F01, G01, G02, G03 so the audit trail is preserved.
3. Advance to phase 2, passing the tracked-items manifest above into the
   phase-2 strategist's dispatch context (in particular, alert the
   strategist to G02's paraphrase looseness on C015/C218/C219, and to the
   INCONCLUSIVE-candidate flagging on C036/C044/C060/C148 from
   `FINDINGS.md` §6.8).

No further fixer pass is required for phase 1.
