# Arbitration — phase 1 (test-1)

VERDICT: ITERATE
Round: 1

Single-bot review mode (critical_reviewer only). Verdict applies the rule
from `methodology/04-review.md` literally: zero Category-A findings, but eight
Category-B findings exist and none have been previously fixed (round 1), so
the verdict is **ITERATE**.

## Deduplicated findings

| id  | category | locus | finding (one-line synopsis) | source-review | round-raised | fixer-pass-that-addressed-it |
|-----|----------|-------|------------------------------|---------------|--------------|------------------------------|
| F01 | B | `CLAIMS.md` rows C001–C217 (`page` column); all claim nodes in `graph.v1.json` | All 217 claims have `page = ?` / `page = null`; group `page_range` is line range, not page range. | critical | 1 | — |
| F02 | B | `phase1/agents/graph_builder/build_v1.py` | graph_builder dropped a helper script in its working dir, exceeding role spec's declared writes. | critical | 1 | — |
| F03 | B | `CLAIMS.md` `confidence` column (217 rows) | Extractor used only `high`/`medium`; zero `low` despite the extractor's own log flagging genuine ambiguity (e.g. C036, C044, C046, C060, C148, C152). | critical | 1 | — |
| F04 | B | `CLAIMS.md` row C015 (line 108) | Triple compound contributions sentence kept as a single row; `claim_taxonomy.md` requires it to be split into three. | critical | 1 | — |
| F05 | B | `CLAIMS.md` rows C188, C189 (line 855) | Code-availability URL statements tagged `method`; not propositional per `claim_taxonomy.md`. | critical | 1 | — |
| F06 | B | `CLAIMS.md` rows C036, C044, C060 | Three expressivity claims at high/medium confidence despite searcher flagging open question; either demote to `low` or re-tag as `prior_work`. | critical | 1 | — |
| F07 | B | `LITERATURE.md` C006 (line 95) | Three references attached at `high`/`medium` `supports` to an "order of magnitude more training data" claim that none of them actually quantifies. | critical | 1 | — |
| F08 | B | `LITERATURE.md` C148 (line 680) | `lipman2023flowmatching` tagged `supports medium` for an OT-CFM claim, but vanilla CFM (Lipman 2023) does not provide optimal-transport paths; mis-relation. | critical | 1 | — |
| F09 | C | `graph.v1.json` `paper.title`/`paper.authors`; `paper.meta.json` | `paper.meta.json` is empty; DOI / arXiv ID for paper exist publicly (arXiv:2411.00446) but were not retrieved. | critical | 1 | — |
| F10 | C | `references.bib` (11 unused entries) | Eleven keys present in `references.bib` but not cited from any `LITERATURE.md` bullet (3 are `\cite`d in paper.txt line 106). `delphes` is duplicate of `deFavereau:2013fsa`. | critical | 1 | — |
| F11 | C | `CLAIMS.md` row C111 | Meta-sentence "we show how L-GATr sets a new record…" — descriptive, duplicates substantive `C129`. | critical | 1 | — |
| F12 | C | `FINDINGS.md` §5 | Wording conflates "unused-by-LITERATURE.md" (11 keys) with "uncited-in-paper" (8 keys). | critical | 1 | — |

Auto-A trigger checks (bibtex resolution 34/34; 13/34 sampled refs verified
live against arXiv; graph schema validation; CLAIMS.md provenance sample
25/25 verbatim; phase-1 deliverables list complete) all passed. No
fabricated-citation finding.

## Next steps

Forward all eight Category-B findings (F01–F08) to the fixer. Category-C
findings (F09–F12) may be addressed at the orchestrator's discretion; they do
not block PASS once the B-set is resolved, and the orchestrator may de-scope
them. Specific notes:

- **F01 — defer to phase 3.** The critical_reviewer themselves wrote that F01
  "remains B (does not block phase 1 advancement) but must be fixed before
  phase 3 highlighting." The page-number recovery is naturally a phase-3
  concern (re-render LaTeX, or run `paper.txt` through `src/highlight_text.py`
  during highlighter dispatch). Forward F01 as a **tracked-but-deferred**
  item, not a blocking phase-1 fix. The arbiter accepts F01 being open for
  the round-2 review provided the fixer/orchestrator records the deferral
  explicitly in `FINDINGS.md`.
- **F02 — fixer scope.** Either move `build_v1.py` under `src/` (cleanest), or
  amend `agents/graph_builder.md` "Writes" section to permit reproducibility
  helpers in the agent working directory. Either path closes the finding.
- **F03, F04, F05, F06 — re-dispatch claim_extractor.** These are claim-level
  fixes (confidence re-grading, splitting C015, dropping/merging C188–C189,
  demoting/re-tagging C036/C044/C060). After the extractor revises
  `CLAIMS.md`, the **graph_builder** must re-run to re-emit `graph.v1.json`
  with the updated claim count and group memberships.
- **F07, F08 — re-dispatch literature_searcher.** These are
  attribution-confidence fixes inside `LITERATURE.md`. No bibtex churn
  required (all referenced keys remain valid); only relation/confidence
  retags. The graph_builder rebuild after F03–F06 should pick up the new
  literature attachments.
- **F09 (C, suggested).** Pure orchestrator action — populate
  `paper.meta.json` from arXiv:2411.00446 once. Does not require a
  subagent dispatch.
- **F10–F12 (C, suggested).** Optional polish; orchestrator may de-scope.

After the fixer pass, re-review by `critical_reviewer` only (single-bot mode
holds for phase 1).
