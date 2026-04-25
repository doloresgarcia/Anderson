# FINDINGS — test-1, phase 1

## 1. Overview

- **Paper title:** *A Lorentz-Equivariant Transformer for All of the LHC*
- **Authors:** Brehmer, Bresó, de Haan, Plehn, Qu, Spinner, Thaler
- **Slug:** `test-1`
- **Source:** `paper/paper.txt` (LaTeX source; `paper.meta.json` has every bibliographic field `null` and points at `reviews/review_1/paper_no_cite.tex`).

Phase 1 ingested the paper, extracted **217 claims** (`C001`–`C217`) tagged with the seven-type taxonomy from `conventions/claim_taxonomy.md`, ran a targeted external search yielding **45 bibtex entries** in `references.bib`, attached candidate references to **73 of the 217 claims** in `LITERATURE.md`, and built a first-pass graph of **20 groups** with **217 claim nodes and 0 edges** in `graph.v1.json`. The paper is dominated by methodological / empirical statements (≈ 69% `method` + `result`), with a sizable `background_fact` tail in §2.1 (geometric-algebra preliminaries).

## 2. Claim counts

- **Total claims:** 217 (`C001`–`C217`).
- **UNCLASSIFIED:** 0.
- **Hedged (`hedged=true`):** 4 — `C089` ("we attribute"), `C109` ("arguably"), `C136` ("might"), `C179` ("might"). All four carry `confidence=medium`.

Per-type histogram (mechanically counted from `CLAIMS.md`):

| type | count |
|---|---|
| `method` | 104 |
| `result` | 46 |
| `background_fact` | 46 |
| `interpretation` | 8 |
| `definition` | 7 |
| `prior_work` | 5 |
| `assumption` | 1 |
| `UNCLASSIFIED` | 0 |
| **total** | **217** |

## 3. Confidence distribution

Extraction confidence per `conventions/confidence.md`, taken from the `confidence` column of `CLAIMS.md`:

| level | count |
|---|---|
| `high` | 153 |
| `medium` | 64 |
| `low` | 0 |

The four hedged rows are all `medium`; the remaining 60 `medium` rows correspond to ambiguous-type decisions or compound-sentence splits flagged in the extractor's log. There are **no `low`-confidence rows**, so no claim will be auto-skipped by the strategist's confidence rule.

## 4. Group structure

`graph.v1.json` partitions the 217 claims into **20 groups** with sizes in [7, 14] (mean 10.85). Sizes: 14, 13, 13, 13, 12, 12, 12, 12, 12, 12, 12, 11, 10, 10, 10, 8, 8, 8, 8, 7. No group exceeds the schema cap of 15.

| id | title | size | dominant_type | section(s) |
|---|---|---|---|---|
| G001 | paper claims | 10 | method | Abstract + 5 |
| G002 | introduction context | 10 | mixed | 1 + Code |
| G003 | pre-training scheme | 8 | method | 1 + 2.1 + 4 |
| G004 | multivector basics | 12 | mixed | 2.1 |
| G005 | geometric product | 12 | background_fact | 2.1 |
| G006 | equivariance benefits | 13 | result | 2.1 + 2.3 + 6 |
| G007 | L-GATr layers | 11 | method | 2.2 |
| G008 | equivariance properties | 12 | background_fact | 2.2 + 2.3 |
| G009 | input handling | 8 | mixed | 2.3 + 2.4 |
| G010 | scaling benchmarks | 13 | mixed | 2.4 |
| G011 | amplitude regression | 12 | mixed | 3 + 5 |
| G012 | amplitude training | 7 | method | 3 |
| G013 | jet tagging results | 13 | mixed | 4 + 5 |
| G014 | tagging setup | 14 | method | 4 |
| G015 | generator setup | 12 | mixed | 5 |
| G016 | generation quality | 12 | result | 5 |
| G017 | CFM coordinates | 10 | method | 5 |
| G018 | DSI baseline | 8 | method | App.A |
| G019 | training hyperparameters | 12 | method | App.A |
| G020 | classifier evaluation | 8 | method | App.A |

Groups marked "multiple" sections (G001, G002, G003, G006, G008, G009, G011, G013) span section boundaries because the schema's smallest-pair-with-shared-type merge rule pulled in singleton/duplicate prior-work and interpretation rows; this is faithful to the algorithm, not editorial.

## 5. Literature coverage

- **Claim headings in `LITERATURE.md`:** 217 (one per claim).
- **Claims with ≥ 1 candidate reference:** **73**.
- **Claims with 0 candidates:** **144** (per the searcher's log: ≈ 110 policy-driven "no-search" internal-method/hyperparameter claims plus ≈ 34 "no-result" claims that ran searches but found no relevant external comparator — mostly textbook-level geometric-algebra background facts and pure interpretations).
- **Total candidate-reference bullets:** 113.
- **Unique cited bibtex keys (used in `LITERATURE.md`):** 34.
- **Total entries in `references.bib`:** 45.
- **Unused entries in `references.bib`** (present in the bib but never cited by any `LITERATURE.md` bullet): **11** — `ATLAS:2018wis`, `Butter:2019cae`, `DBLP:journals/corr/LoshchilovH16a`, `delphes`, `Hashemi:2019fkn`, `Huetsch:2024quz`, `Komiske:2018cqr`, `Louppe:2017ipp`, `Moore:2018lsr`, `Otten:2019hhl`, `Qu:2019gqs`. Note that `delphes` is an alias for `deFavereau:2013fsa` (same arXiv ID 1307.6346); `LITERATURE.md` consistently uses the latter, leaving the alias orphaned.

Distribution by relation across all 113 candidate bullets:

| relation | count |
|---|---|
| `supports` | 74 |
| `related` | 39 |
| `contradicts` | 0 |

Confidence on candidate bullets is dominated by `high` (consistent with the searcher's policy of attaching only confirmed hits; tier-2 background_fact / textbook claims have empty buckets rather than `low`-confidence guesses).

## 6. Gaps identified

The following are concrete gaps that downstream phases should be aware of. Every item is traceable to an agent log or directly observable in the artifacts.

1. **No native page numbers.** `paper.txt` is the LaTeX source, so the `page` column in `CLAIMS.md` is `?` for all 217 rows and `paper.page=null` for every claim node in `graph.v1.json`. Group `page_range` fields are line ranges, not page ranges. The phase-3 highlighter (which expects to mark a PDF) will need to recover page coordinates by re-rendering the LaTeX or by mapping line numbers through the synthesized PDF produced by `src/highlight_text.py`. *(claim_extractor/log.md, graph_builder/log.md.)*
2. **No structural claim-to-claim edges.** `graph.v1.json` has `"edges": []`. The skeleton-pass graph_builder log is explicit that the schema permits this in phase 1 ("missing edges is fine"), but it means the phase-2 strategist cannot use `depends_on` topology to prioritise. Phase 2's graph_builder will not introduce edges either without an extractor sidecar pass; reviewers may want to revisit. *(graph_builder/log.md, "Step 7" and "Notes / known gaps".)*
3. **No `low`-confidence rows.** The extractor used only `high` and `medium`; none of the 217 rows is `low`. Either every claim is genuinely solid or the extractor under-used the `low` bucket. Reviewer should confirm. *(observed directly in CLAIMS.md.)*
4. **Ambiguous-type rows the extractor flagged.** The extractor's log lists boundary cases the reviewer / strategist may want to revisit:
   - `C036` (`result` chosen over `background_fact`) — uniqueness claim about the GA framework decomposition.
   - `C044` (`result` over `prior_work`) — universal-approximation claim with no explicit citation, attributed to the present paper.
   - `C046` (`result` over `definition`) — exact equivariance statement.
   - `C060` (`result` over `prior_work`) — "It can be shown that this architecture is maximally expressive" with no inline citation.
   - `C148` (`result`, `medium` confidence) — CFM "optimal transport paths… uniquely suited" — could equally be `background_fact` or `interpretation`.
   - `C152` (`background_fact` over `assumption`).
   - The taxonomy split `method` vs. `definition` for many architecture statements (e.g. `C054` "we define layer normalization using…") is fuzzy; the extractor consistently chose `method`.
   - `C181`, `C182`, `C187` — outlook/summary claims tagged `interpretation` rather than `result` because they generalise beyond the measurements shown.
   *(claim_extractor/log.md, "Ambiguous type decisions" and "Items the reviewer may want to revisit".)*
5. **Skipped items the reviewer may want to add back.**
   - The geometric-algebra footnote at `paper.txt:166` (supersymmetric multiplets / higher-rank irreps) was skipped because it required substantive paraphrase.
   - Code-availability URL claims `C188`, `C189` were *kept* but the extractor flags them as removable if the convention prefers to skip code-availability statements.
   - `C015` (paper's contributions) was kept whole; could be split into three rows.
   *(claim_extractor/log.md, "Items deliberately skipped" / "Items the reviewer may want to revisit".)*
6. **No retrievable contradictory literature.** The literature_searcher found zero `contradicts` candidates across all 217 claims. This is not surprising for a methodology paper, but it means phase 2 cannot FAIL any claim purely on a literature mismatch and must rely on internal consistency, numerical recheck, or canonical-reference audit for FAIL verdicts. *(literature_searcher/log.md, "Possibly-contradicting prior work".)*
7. **Tier-2 background-fact claims with no candidate.** §2.1 contains a long run of textbook geometric-algebra facts (e.g. C016–C020, C022, C026–C030) that the searcher intentionally left without candidates because they are textbook material rather than citable-paper assertions. The extractor's log explicitly invites the reviewer to drop them as too elementary; the searcher chose not to attach a Hestenes-1966-style reference because the paper itself does not `\cite` it. Phase 2 verifier will need to decide which of these to skip vs. check against a textbook. *(claim_extractor/log.md item 2; literature_searcher/log.md "No-result claims".)*
8. **Stated-but-uncited expressivity claims (C036, C044, C060).** These present own-work assertions — uniqueness of the GA decomposition, most-compact-equivariant-representation / universal-approximation, maximally expressive among Lorentz-equivariant transformers — without naming a proof reference. The searcher attached `brehmer2023geometric` and `ruhe2023clifford` as `related` (medium-confidence) candidates but flagged that neither flatly supports the wording, recommending phase 2 treat these as INCONCLUSIVE candidates. *(literature_searcher/log.md, "No-result claims".)*
9. **Unused / aliased bibtex entries.** Eleven keys exist in `references.bib` but are not cited by any `LITERATURE.md` bullet (listed in §5). One of them (`delphes`) is an exact alias of `deFavereau:2013fsa` and could be deduplicated; the other ten were apparently retrieved as background but never attached. None of these is a fabricated key — they all resolve to real arXiv records per the searcher's log — but the bib will look noisier than necessary to a reviewer. *(observed directly by set diff between `references.bib` and `LITERATURE.md`.)*
10. **`paper.meta.json` is empty.** Title, authors, year, venue, DOI, arxiv, url, source_pdf are all `null`; only `slug` and `source_text` are set. The graph_builder filled `paper.title` and `paper.authors` in `graph.v1.json` from the title line at the top of `CLAIMS.md`, not from the meta file. Phase 3 will need a populated meta file (or accept the title from `CLAIMS.md` as canonical). *(graph_builder/log.md "Notes / known gaps".)*

## 7. Phase-2 prompts (suggestions only, not commitments)

The strategist owns method choice; the notes below only flag where the counts in §§2–6 suggest concentration of effort.

- **High-yield groups for verification.** The 46 `result` rows and the 46 `background_fact` rows are the two largest verification surfaces. Within `result`, G016 (generation quality, 12 claims) and G006 (equivariance benefits, 13 claims, dominated by results and outlook interpretations) carry the paper's headline performance assertions (C111, C129, C137, C174, C175, C177, C178, C184–C187) and should receive priority. G011 (amplitude regression, 12 claims) carries the scaling-with-multiplicity argument (C100–C108).
- **Citation-audit candidates.** The `prior_work` type has only 5 rows (C007, C014, C023, C113, C145), four of which point at the predecessor paper `Spinner:2024hjm`. These are cheap, high-value audits — the only `prior_work` row that *isn't* a self-citation is C007 (the four-key jet-tagger genealogy citation block), which is also low-risk because each candidate has a `high`-confidence `supports` bullet.
- **Internal-consistency-only claims.** The 144 claims with no literature candidate (mostly `method` rows in App.A and §5) are by construction phase-2 internal-consistency checks; the strategist should be prepared to allocate a sizeable share of budget to consistency rather than literature.
- **Hedged + interpretation rows.** The four hedged rows and the eight `interpretation` rows (C063, C089, C105, C179–C182, C187) are the hardest to FAIL outright (taxonomy says default `INCONCLUSIVE`); the strategist may want to flag them as low-priority unless they appear in the abstract / conclusion (C181, C182, C187 do, and probably warrant a check despite the hedge ceiling).
- **Boundary cases listed in §6.4** are the rows where a re-read by phase 2 is most likely to change the type — worth pre-flagging in `STRATEGY.md` so the verifier does not relitigate the type at verification time.
