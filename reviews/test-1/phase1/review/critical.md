# Critical review — phase 1 (test-1)

Single-bot review (an arbiter follows). Findings are flat A/B/C tagged. Every
finding cites file + line/row and the methodology / convention rule it bears
on.

## Auto-A trigger checks (executed first)

- **Bibtex resolution.** All 34 cited keys in `LITERATURE.md` resolve in
  `references.bib` (independent set-intersection: 34/34, 0 unresolved).
- **Independent reference verification.** I sampled **13** of the 34 cited
  bibtex entries and pulled the live arXiv abstract page for each. All 13
  match `references.bib` (title + authors + arXiv ID): `Spinner:2024hjm`
  (2405.14806), `vaswani2017attention` (1706.03762), `brehmer2023geometric`
  (2305.18415), `Qu:2022mxj` (2202.03772), `ruhe2023clifford` (2305.11141),
  `Sjostrand:2014zea` (1410.3012), `lipman2023flowmatching` (2210.02747),
  `Wu:2024thh` (2407.08682), `chen2023symbolic` (2302.06675),
  `dao2022flashattention` (2205.14135), `Heimel:2018mkt` (1808.08979),
  `ATLAS:2020ccu` (2006.09274), `Cacciari:2008gp` (0802.1189). **No
  fabricated reference detected.**
- **Graph schema validation.** `graph.v1.json` passes every rule in
  `conventions/graph_schema.md`: 20 groups (≤ 20); every group has
  `1 ≤ |claim_ids| ≤ 15` (range [7, 14]); every claim's parent resolves and
  the claim is listed in that group's `claim_ids`; 217 distinct claim ids
  matching the 217 group-listed ids; no edges (vacuous source/target/loop
  checks); every node's color matches its verdict per the palette
  (all gray / `NOT_CHECKED`); `dominant_type` recomputed and matches for
  every group; the inferred-`contradicts`-with-low-confidence ban is vacuous.
- **CLAIMS.md provenance sample.** I sampled 25 rows (`C001`, `C006`, `C007`,
  `C012`, `C014`, `C022`, `C023`, `C031`, `C032`, `C051`, `C052`, `C062`,
  `C065`, `C066`, `C067`, `C083`–`C089`, `C111`, `C129`, `C148`, `C172`,
  `C186`, `C188`, `C190`) by reading `paper.txt` at the cited line and
  confirming the quoted sentence appears verbatim there. **All 25 match.**
- **Phase-1 deliverables list.** Phase 1 declared in
  `methodology/03-phases.md`: `CLAIMS.md`, `LITERATURE.md`, `graph.v1.json`,
  `FINDINGS.md`. `phase1/CLAUDE.md` additionally requires `references.bib`
  and `graph.v1.skeleton.json` (literature_searcher and graph_builder
  intermediates). All six are present in `phase1/outputs/`. One extra file
  (`build_v1.py`) lives in the agent's working directory — see F02 below.

No auto-A trigger fired.

## Findings

| id  | category | locus | finding | rule | resolution |
|-----|----------|-------|---------|------|------------|
| F01 | B | `CLAIMS.md` rows C001–C217, `page` column | Every one of 217 rows has `page = ?` and every claim node in `graph.v1.json` has `page: null`. Group `page_range` is a line range, not a page range. | `methodology/05-artifacts.md` shows `page` as an integer in the canonical row format; `conventions/graph_schema.md` lists `page` as a required claim field (integer). | Re-render the LaTeX once in phase 3 (or pipe `paper.txt` through `src/highlight_text.py` first) to recover page coordinates and back-fill. The phase-1 gotcha note acknowledges the gap; it remains B (does not block phase 1 advancement) but must be fixed before phase 3 highlighting. |
| F02 | B | `phase1/agents/graph_builder/build_v1.py` | The graph_builder dispatched a Python helper script into its own working directory, alongside `plan.md` / `log.md`. `agents/graph_builder.md` declares only `phase1/outputs/graph.v1.json` as the phase-1 write; `methodology/03a-orchestration` treats output beyond the declared spec as a Category-A finding *if* it lands in the deliverables area. This script is not in `outputs/`, so it is a deviation from the role spec but not a deliverable contamination. | `agents/graph_builder.md`, "Writes" section. | Either (a) extend the role spec to permit reproducibility scripts in the agent working directory (treat as plan/log analogues), or (b) move `build_v1.py` under `src/` like `claim_stats.py` and `render_graph.py`. Pure documentation fix — keeps the phase-1 outputs untouched. |
| F03 | B | `CLAIMS.md` `confidence` column, all 217 rows | The extractor used only `high` (153) and `medium` (64); zero `low` rows. `conventions/confidence.md` reserves `low` for "best guess; agent had to paraphrase, infer, or choose under genuine ambiguity," which describes the 7 boundary-type cases the extractor itself flagged in its `log.md` (`C036`, `C044`, `C046`, `C060`, `C148`, `C152`). Selecting `medium` for all of those amounts to a silent choice not to use the bottom of the scale. | `conventions/confidence.md` ("Use `high` sparingly… the default for routine work is `medium`; `low` is reserved…") | Re-grade the rows the extractor's log flagged as judgment calls. Plausible candidates for demotion to `low`: `C036`, `C044`, `C060`, `C148`. The extractor must justify any change in `log.md` per `conventions/confidence.md` "When to override". |
| F04 | B | `CLAIMS.md` row C015 (line 108, "we extend… improve… deliver…") | `C015` keeps a triple compound contributions sentence as a single row, contrary to `claim_taxonomy.md` "Cited contributions of the present paper" → "expands into three claims." The extractor's `log.md` acknowledges this and notes that the per-section claims appear elsewhere — but that does not satisfy the rule, which requires the contributions list itself to split. | `conventions/claim_taxonomy.md`, "Cited contributions of the present paper." | Split `C015` into three rows (extend amplitude regression / improve classification via pre-training / deliver competitive generative network), each typed `method` with `medium` confidence. Adjust `graph.v1.json` claim count and `G002`/`G003` membership accordingly. |
| F05 | B | `CLAIMS.md` rows C188, C189 (line 855, code-availability URLs) | Code-availability URL statements ("L-GATr is available at https://github.com/…") were tagged `method`, but `conventions/claim_taxonomy.md` says claims must be "verifiable propositions" — a URL by itself is closer to "pure description of what the paper does" than to a verifiable proposition. The extractor's `log.md` invites the reviewer to drop them. | `conventions/claim_taxonomy.md`, "What counts as a claim" filter 1 (propositional) and "Future work / limitations" boundary case. | Drop `C188` and `C189` (and their `paper claims`/`introduction context` group memberships), or convert them into a single combined `method` claim like "the L-GATr code is publicly released for reproducibility." |
| F06 | B | `CLAIMS.md` rows C036, C044, C060 | Three "presented as own work but stated without citation" expressivity claims (uniqueness of GA decomposition; provably most compact equivariant representation with universal approximation; maximally expressive Lorentz-equivariant transformer). The extractor's log marks them as `result` but explicitly notes the boundary with `prior_work` because the proofs are presumably in earlier references. The literature_searcher attached `brehmer2023geometric` and `ruhe2023clifford` as `related` (medium) but flagged that neither flatly supports the wording. Rows are presented at `confidence=high` (C044, C060) and `medium` (C036), which is over-confident given the searcher's open question. | `conventions/claim_taxonomy.md` `prior_work` definition; `conventions/confidence.md` `high` definition ("agent would defend this without caveats"). | Either (a) demote `C036`, `C044`, `C060` to `confidence=low` (matching the genuine ambiguity), or (b) re-tag as `prior_work` if the verifier can locate a citation in `brehmer2023geometric` / `ruhe2023clifford`. The strategist should pre-flag these for phase-2 INCONCLUSIVE handling per the literature_searcher's recommendation. |
| F07 | B | `LITERATURE.md` C006 (line 95, "unconstrained networks require at least an order of magnitude more training data") | The claim is anchored to *no* citation in `paper.txt` ("it has been established that…"), yet `LITERATURE.md` attaches three references (`Butter:2017cot`, `Bogatskiy:2022czk`, `Gong:2022lye`) with `confidence high` for `Butter:2017cot` and `medium` for the other two. None of those papers actually quantifies "an order of magnitude more training data" — they are equivariance demonstrations, not data-efficiency benchmarks. The snippet titles attached are paper titles, not assertions of the order-of-magnitude figure. | `conventions/confidence.md` literature relevance: `high` requires "the quoted snippet contains the relevant assertion." | Demote `Butter:2017cot` to `medium` or `related`; demote the other two to `related`. Add a phase-2 verification flag noting the order-of-magnitude figure may need a different reference (Spinner:2024hjm Sec. 4 or Bogatskiy:2020tje) for sourcing. |
| F08 | B | `LITERATURE.md` C148 (line 680) — but also the underlying claim text | The extracted sentence is "The conditional flow matching framework provides optimal transport paths for high-dimensional density estimation, making it uniquely suited for LHC phase space distributions." `LITERATURE.md` attaches `lipman2023flowmatching` `supports medium`. However, vanilla CFM (Lipman et al. 2023) does not provide *optimal-transport* paths — that is the OT-CFM extension (Tong et al. 2023). The snippet "Flow Matching for Generative Modeling" supports the existence of CFM, not the optimal-transport claim. The `supports` tag misrepresents what the cited paper says. | `conventions/confidence.md` literature relevance: `supports` `medium` requires "same domain and topic, but does not speak to the specific proposition; reading the full reference would be needed to confirm relevance" — but `supports` is the wrong relation when the source doesn't speak to the proposition. | Re-tag the bullet as `related medium` (same domain, doesn't speak to the OT claim). Phase 2 verifier should also note that the extracted claim itself may be inaccurate to the OT-CFM literature; that is a phase-2 concern, but the phase-1 attribution should not paper over it. |
| F09 | C | `graph.v1.json` `paper.title` and `paper.authors`, `paper.meta.json` | `paper.meta.json` is empty (`title: null`, `authors: null`, `doi: null`, `arxiv: null`). `graph.v1.json` filled the title and authors from the heading of `CLAIMS.md`; the DOI / arXiv ID for this paper exist publicly (arXiv:2411.00446) but were not retrieved. | `methodology/05-artifacts.md` (graph schema requires a populated `paper` block); `agents/literature_searcher.md` log already retrieved the paper's identity. | Populate `paper.meta.json` once (orchestrator action, not a re-dispatch) so phase 3's `paper` block resolves a DOI / arXiv link in the rendered HTML. Pure C — does not block phase 1. |
| F10 | C | `references.bib` 11 unused entries (`ATLAS:2018wis`, `Butter:2019cae`, `DBLP:journals/corr/LoshchilovH16a`, `delphes`, `Hashemi:2019fkn`, `Huetsch:2024quz`, `Komiske:2018cqr`, `Louppe:2017ipp`, `Moore:2018lsr`, `Otten:2019hhl`, `Qu:2019gqs`) | Eleven keys are present in `references.bib` but not cited from any `LITERATURE.md` bullet. Three of them (`Otten:2019hhl`, `Hashemi:2019fkn`, `Butter:2019cae`) are actually `\cite`d in the paper at line 106 — that paragraph generated *no* claim row in `CLAIMS.md`, hence no LITERATURE.md heading uses them. None are fabricated; FINDINGS.md §5 already documents the situation. | `methodology/05-artifacts.md` is silent on orphans; this is hygiene, not correctness. | Either (a) trim orphans from `references.bib` once phase-2 verification confirms it does not need them, or (b) split a "ML generators on the theory side" claim out of line 106 so the three theory-generator keys are actually used. `delphes` is an exact alias of `deFavereau:2013fsa` — deduplicate. |
| F11 | C | `CLAIMS.md` row C111 ("we show how L-GATr sets a new record for jet tagging by combining the merits of both ideas") | Tagged `result` `confidence=high`. Strictly speaking this is a meta-sentence describing what the section will demonstrate (same family as "Section 3 presents the results", which `claim_taxonomy.md` excludes). The actual numerical record-setting claim is the table-derived `C129` ("achieves a significant improvement over… ParT and MIParT"). | `conventions/claim_taxonomy.md`, filter 1 (propositional, not "what the paper does"). | Either drop `C111` as descriptive, or re-anchor the claim to the headline `result` in Tab.~\ref{tab:jctagging} so the verifier has a number to check. C, since `C129` already covers the substantive proposition. |
| F12 | C | `FINDINGS.md` §5 wording "Unused entries in `references.bib`" | The list flagged 11 keys as "never cited by any `LITERATURE.md` bullet". That is correct for `LITERATURE.md`, but three of those keys (`Otten:2019hhl`, `Hashemi:2019fkn`, `Butter:2019cae`) *are* cited inside `paper.txt` (line 106). FINDINGS.md should distinguish "unused by the literature_searcher's claim attachments" from "uncited in the paper proper" — they differ. | `methodology/05-artifacts.md` general accuracy of summary numbers. | One-line edit to `FINDINGS.md` §5: distinguish "unused-by-LITERATURE.md" (11 keys) from "uncited-in-paper" (8 keys). C, no count changes. |

## Section A — Blocking findings

(none)

## Section B — Weakening findings

F01, F02, F03, F04, F05, F06, F07, F08

## Section C — Suggestions

F09, F10, F11, F12
