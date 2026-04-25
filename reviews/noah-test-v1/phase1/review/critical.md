# Critical Review — Phase 1 — noah-test-v1

Reviewer: critical_reviewer
Date: 2026-04-25

---

## F001 — B — LITERATURE.md format deviates from spec

**What:** `LITERATURE.md` uses cluster-based sections (`## Cluster A — …`) with multiple claims grouped under each heading and a markdown table for candidates. The spec in `05-artifacts.md` requires per-claim subsections (`## C001`, `## C002`, …), one section per claim, with bullet-list entries in the form `- [@key] — relation — confidence level — source — "snippet"`.

**Where:** `phase1/outputs/LITERATURE.md`, entire file. `methodology/05-artifacts.md` §LITERATURE.md.

**Why wrong:** `05-artifacts.md` states the format as:
```
## C001
- [@smith2020] — supports — confidence high — bank — "snippet from paper text"
- [@jones2019] — contradicts — confidence medium — external — "snippet"
```
The cluster format groups 2–18 claims per section and uses a pipe-table. This is machine-parseable but does not match the contract. Downstream agents (`graph_builder`, checkers) that expect `## C001` anchors will fail to find them.

**Resolution:** Reformat `LITERATURE.md` with one `## claim-XXXX` subsection per claim that has literature coverage. Duplicate rows across multiple claims as needed (the spec allows this — `literature_searcher` "filters/iterates `claims.jsonl` via `jq`"). The cluster annotation grouping can remain in an additional non-normative notes section.

---

## F002 — B — `related` is not a valid relation value in LITERATURE.md

**What:** 14 rows in `LITERATURE.md` use `related` as the second field (relation). The spec in `05-artifacts.md` shows only `supports` and `contradicts` as valid relation values.

**Where:** `phase1/outputs/LITERATURE.md`, all 14 rows with `| … | related | … |`:
`Bahl:2024meb`, `Bahl:2024sib`, `Hao:2022xuv`, `Bogatskiy:2020tje`, `Badger:2022hwf`, `Danziger:2021nec`, `Herrmann:2025abc`, `Mikuni:2021pou`, `Butter:2023fov`, `Buhmann:2023kdg`, `Leigh:2023doe`, `Campbell:2022qmc`, `Kansal:2022spb`, `Bierlich:2023zzd`.

**Why wrong:** `05-artifacts.md` example shows only `supports` and `contradicts`. `related` has no defined semantics in the convention. It cannot be parsed by downstream agents that branch on the relation field, and it is semantically ambiguous (neither supporting evidence nor contradicting evidence).

**Resolution:** Reclassify each `related` row as either `supports` (reference provides partial evidence for the claim) or remove from the cluster if it merely shares a topic but does not bear on the claim's truth. A third `related` category should not be introduced without updating `05-artifacts.md`.

---

## F003 — A — `Badger:2022hwf` author field appears to be fabricated

**What:** The `references.bib` entry for `Badger:2022hwf` (arXiv:2206.14831) lists authors as `Badger, Simon and Butter, Anja and Sherrat, Matthew and Sherrat, Jessica and Sherrat, Luke`. The same last name "Sherrat" repeated three times with different first names, combined with co-author "Butter, Anja" who is not a known author of this paper, is a strong hallucination signal. The actual authors of arXiv:2206.14831 are Simon Badger, Ryan Moodie, and Jan Klan.

**Where:** `phase1/outputs/references.bib`, `@article{Badger:2022hwf, …}` entry.

**Why wrong:** Per `methodology/04-review.md` §"Hard rule: unresolvable references": "LLM-fabricated citations are the most common failure mode of this kind of system; the reviewers exist primarily to catch them." A resolved record that contradicts the real paper is auto-Category-A. The `author` field does not match the real paper's authorship.

**Resolution:** Verify arXiv:2206.14831 directly (title "Loop Amplitudes from Precision Networks" is correct; author list is not). Correct the entry to the real authors. If the paper cannot be confirmed to address the annotated claims in `LITERATURE.md` Cluster D, remove the entry.

---

## F004 — B — `graph.v1.skeleton.json` is a non-declared deliverable in the outputs directory

**What:** `phase1/outputs/graph.v1.skeleton.json` exists alongside the declared deliverables. It is not listed in `methodology/05-artifacts.md` as a phase-1 deliverable. `phase1/CLAUDE.md` lists it as the intermediate output of the skeleton pass, consumed by the graph_builder final pass, and not a persistent artifact.

**Where:** `phase1/outputs/graph.v1.skeleton.json`. Role spec auto-A trigger: "Output file outside the phase's declared deliverables list."

**Why wrong:** The role spec lists auto-A for "output file outside the phase's declared deliverables." `05-artifacts.md` declares: `claims.jsonl`, `CLAIM_REVIEW.md`, `LITERATURE.md`, `references.bib`, `graph.v1.json`, `FINDINGS.md`. The skeleton file is not among them.

**Assessment:** This is the weakest A trigger. `phase1/CLAUDE.md` explicitly names it as the graph_builder skeleton output and it is referenced in the graph_builder log. The skeleton is a documented intermediate, not an accidental stray. Downgrading to **B**: it should be moved to `phase1/agents/graph_builder/` (intermediate workspace) rather than left in `outputs/` where downstream agents may pick it up as a v1 variant.

**Resolution:** Move `graph.v1.skeleton.json` to `phase1/agents/graph_builder/graph.v1.skeleton.json` (or delete it, since `graph.v1.json` supersedes it). Update the graph_builder log accordingly.

---

## F005 — A — 14/20 groups violate the `≤ 15 claims per group` schema rule

**What:** 14 of 20 groups in `graph.v1.json` exceed the `≤ 15 claim_ids` cap defined in `conventions/graph_schema.md` §Validation rules. The violations range from 21 (G003) to 51 (G015).

**Where:** `phase1/outputs/graph.v1.json`, groups G003, G004, G005, G006, G008, G009, G010, G012, G013, G014, G015, G016, G018, G019. `conventions/graph_schema.md` §Validation rules: "every `group` has `1 ≤ len(claim_ids) ≤ 15`" and "Failure of any rule is auto-Category-A."

**Why wrong:** The schema is unambiguous: the ≤ 15 cap is a hard validation rule that triggers auto-Category-A on failure. The graph_builder correctly identified the conflict in its log, documented it as a schema constraint conflict, and chose to prioritize the ≤ 20 group cap. That rationale is sound and the log is transparent. However, the schema itself designates this as auto-A regardless of documented justification.

**Assessment:** The conflict is real and mathematically inevitable for a 545-claim paper (⌈545/20⌉ = 28 minimum). The constraint was designed for typical ~100–150-claim papers. The graph_builder's decision was correct given the input, and the schema is the defective artifact. Nevertheless, per the rule, this is **A**.

**Resolution options (one of):**
1. **Schema fix (preferred):** Update `conventions/graph_schema.md` to replace the hard ≤ 15 cap with a soft guideline, or add a documented escape hatch for papers where the arithmetic makes the cap unsatisfiable. Reference: `graph_schema.md` §Step 3 says "split by paragraph proximity" for clusters > 15, but Step 4 merges them back — the schema does not handle the case where N/20 > 15.
2. **Increase group count:** Allow more than 20 groups for large papers (e.g., ≤ 30 for papers > 300 claims). Requires schema update.
3. **Accept with documented waiver:** Add a machine-readable `constraint_waivers` field to `graph.v1.json` listing which rules are waived and why, allowing downstream tools to suppress the validation failure.

The graph_builder log already documents the conflict. A schema patch is the cleanest resolution.

---

## F006 — C — `hendrycks2016gaussian` is in `references.bib` but not cited in `LITERATURE.md`

**What:** `references.bib` contains an entry for `hendrycks2016gaussian` (GELU activation paper, arXiv:1606.08415) with `note = {GELU activation function; external context}`. It does not appear in any `LITERATURE.md` cluster.

**Where:** `phase1/outputs/references.bib`, final external-search section. `phase1/outputs/LITERATURE.md`, no occurrence of `hendrycks2016gaussian`.

**Why wrong:** `05-artifacts.md` states "Bibtex keys must resolve in `references.bib`" — the inverse (all bib keys must appear in `LITERATURE.md`) is not a hard rule, but orphan entries in `references.bib` create noise and may indicate a citation that was generated but never justified. The entry is flagged `external context` which suggests it was included prophylactically rather than as a live literature match.

**Resolution:** Remove `hendrycks2016gaussian` from `references.bib` if it is not cited in any LITERATURE.md cluster, or add it to an appropriate cluster (e.g., Cluster A — architecture, for the GELU layer used in L-GATr). Similarly, `DBLP:journals/corr/abs-2106-06610` is in `references.bib` as a passthrough for `claim-0104`'s `cite_keys` field but is not in LITERATURE.md; acceptable as a passthrough (paper's own citation, not a literature search result) — no action needed for the DBLP entry.

---

## F007 — C — `Bogatskiy:2020tje` is typed `@article` but is a conference paper

**What:** `references.bib` entry `Bogatskiy:2020tje` uses `@article` as the entry type but has a `booktitle` field (`Proceedings of ICML 2020`), which is the field for `@inproceedings`. The entry type conflicts with the fields used.

**Where:** `phase1/outputs/references.bib`, `@article{Bogatskiy:2020tje, …}`.

**Why wrong:** BibTeX `@article` entries should not have a `booktitle` field; that belongs to `@inproceedings`. This will produce BibTeX warnings and may be formatted incorrectly in the final report bibliography. Not a citation-validity issue (the arXiv ID 2006.04780 is real and the paper is real).

**Resolution:** Change entry type to `@inproceedings`.

---

## Auto-A trigger checklist

| Trigger | Result |
|---|---|
| Every bibtex key in LITERATURE.md resolves in references.bib | PASS — all 31 keys resolve |
| Resolved record matches the snippet | PARTIAL FAIL — `Badger:2022hwf` author list contradicts real paper (F003) |
| graph.v1.json passes schema validation | FAIL — ≤ 15 claims/group violated for 14/20 groups (F005) |
| LITERATURE.md format correct per 05-artifacts.md | FAIL — cluster format, not per-claim format (F001) |
| All declared deliverables present | PASS — all 6 deliverables present |
| No output files outside declared deliverables | PARTIAL — graph.v1.skeleton.json in outputs/ (F004) |

---

## Summary

| ID | Severity | Description |
|---|---|---|
| F001 | B | LITERATURE.md cluster format vs. per-claim spec |
| F002 | B | `related` is not a valid relation value |
| F003 | A | `Badger:2022hwf` author field contradicts real paper |
| F004 | B | `graph.v1.skeleton.json` in outputs/ instead of agent workspace |
| F005 | A | 14/20 groups exceed ≤ 15-claim cap (schema constraint conflict) |
| F006 | C | Orphan `hendrycks2016gaussian` in references.bib |
| F007 | C | `Bogatskiy:2020tje` typed @article with booktitle field |

**Blocking findings: 2 (F003, F005).** F005 requires a schema clarification rather than a data fix; the graph_builder's choice was correct. F003 requires author verification and possible entry correction.
