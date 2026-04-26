# Critical Review — Phase 2 — slug: easy — Round 2 (post-fixer)

Reviewer: critical_reviewer
Round: 2 (re-review after fixer round 1)
Date: 2026-04-26

---

## Round-1 A findings — resolution status

### M1 (C068 evidence): RESOLVED

File: `reviews/easy/phase2/outputs/graph.v2.json`, C068 node (line ~1784).

The C068 node now carries 3 evidence entries:
1. `paper.txt:549-554` — paper-text quote (pre-existing).
2. `[violated_principle]` — full stabilizer computation explaining why the stabilizer of {(1,0,0,1),(1,0,0,-1)} is SO(2) not SO(3).
3. `[canonical_source]` — Weinberg "The Quantum Theory of Fields" Vol. 1, §2.5, with explanatory note added per M4.

The evidence array now meets the domain_violation standard in `src/conventions/error_categories.md` (violated_principle stated, canonical source named, paper passage quoted). The `corrected_source` note in `checker_domain/section.md` (line 184) further elaborates the little-group formalism connection. M1 is RESOLVED.

### M2 (C183/C185 evidence): RESOLVED

File: `reviews/easy/phase2/outputs/graph.v2.json`, C183 node (~line 3787) and C185 node (~line 3830).

C183 evidence array now has 3 entries: the unreferenced-section note, the primary passage (paper.txt:1660-1661, 1926), and the contradicting passage (paper.txt:1928). C185 evidence array now has 3 entries: the unreferenced-section note, the primary passage (paper.txt:1928), and the contradicting passage (paper.txt:1660-1661, 1926). Both nodes' `flagged_categories` correctly list `["internal_contradiction"]` and color is orange (`#FF6D00`).

Evidence standard for `internal_contradiction` is met: both contradicting passages are quoted with provenance. M2 is RESOLVED.

### M3 (C157 corrected-citation note): RESOLVED

File: `reviews/easy/phase2/agents/checker_literature/section.md`, C157 FLAGGED entry, corrected-citation note at line ~258. Also reflected in `reviews/easy/phase2/outputs/VERIFICATION.md` at line ~783, and in `graph.v2.json` C157 node evidence array entry 3.

The note states that no clearly-correct citation is found in references.bib; it explicitly evaluates `heimel2023madnis` as an in-bib candidate and concludes it does not support the claim; no fabricated bibtex key was introduced. The corrected-citation note does NOT introduce any new bibtex key into the artifact. M3 is RESOLVED.

---

## Round-1 B findings — resolution status

### M4 (C068 confidence/canonical_source clarification): RESOLVED

File: `reviews/easy/phase2/agents/checker_domain/section.md`, C068 canonical_source field (line ~184).

The canonical_source field now includes the explanatory note connecting Weinberg §2.5 to the little-group formalism and its applicability to the stabilizer computation. Confidence retained at medium (fixer's decision to not raise to high is defensible). M4 is RESOLVED.

### M5 (C002 unreferenced entry): RESOLVED

File: `reviews/easy/phase2/agents/checker_unreferenced/section.md`, C002 entry (lines 6-7); also reflected in `reviews/easy/phase2/outputs/VERIFICATION.md` lines 6-7.

A `### C002 — CLEAR — confidence: high` entry was added with appropriate reasoning: self-describing architectural claim requiring no external citation. M5 is RESOLVED.

### M6 (ambiguous count reconciliation): RESOLVED

File: `reviews/easy/phase2/agents/checker_ambiguous/section.md`, HTML comment at line 3; also reflected in `reviews/easy/phase2/outputs/VERIFICATION.md` line 117.

An HTML comment was added enumerating all 27 FLAGGED ambiguous claims and explaining the summary-text overcount (29 vs. 27). The artifact count of 27 is authoritative. M6 is RESOLVED.

### M7 (C157 cross-reference in unreferenced section): RESOLVED

File: `reviews/easy/phase2/agents/checker_unreferenced/section.md`, C157 CLEAR entry (line 76-77); reflected in `reviews/easy/phase2/outputs/VERIFICATION.md` line 76-77.

The C157 unreferenced CLEAR entry now reads: "Claim has a citation [77] (butter2023jetdiffusion); citation content does not support the claim — see literature_collision section for the FLAGGED verdict." The cross-reference is present and correctly directs the reader. M7 is RESOLVED.

### M8 (evidence one-liners for bare CLEAR Tier-1 entries): RESOLVED

File: `reviews/easy/phase2/agents/checker_unreferenced/section.md`, entries for C100, C101, C104, C112, C117, C129, C131, C138, C180, C181, C183, C184, C185, C193, C195, C197, C198.

All listed Tier-1 claims now carry at least one evidence one-liner pointing to a paper table, figure, or line range. M8 is RESOLVED.

### M9 (unreferenced entries for C029, C031, C036, C041, C054): RESOLVED

File: `reviews/easy/phase2/agents/checker_unreferenced/section.md`, new entries inserted at lines 17-30; reflected in `reviews/easy/phase2/outputs/VERIFICATION.md` lines 17-30.

All five entries are present with CLEAR verdicts and evidence pointing to paper.txt line ranges. The reasoning in each is appropriate (self-describing architectural claims, elementary mathematical identities, or ablation-supported design observations). M9 is RESOLVED.

### M10 (graph.v2.json deduplication): NOT_RESOLVED

File: `reviews/easy/phase2/outputs/graph.v2.json`, nodes C001, C003, C070, C191, C193.

The fixer log (`reviews/easy/phase2/agents/fixer/round_1/log.md`) documents M10 as RESOLVED and specifies that C001 was reduced from 3 entries to 1, C003 from 2 to 1, C070 bare entry removed, C191 bare entry removed, C193 near-duplicate removed. However, the actual `graph.v2.json` artifact does not reflect these edits:

- **C001** (graph.v2.json line ~602-607): still has 4 evidence entries, including a bare `"paper.txt:16-17"` entry and two near-identical quoted-snippet entries alongside the fixer's M8 support note.
- **C003** (graph.v2.json line ~645-648): still has 2 entries with different but overlapping line ranges (paper.txt:18-20 and paper.txt:18-19).
- **C070** (graph.v2.json line ~1828-1830): still has both `"paper.txt:555–556"` (bare, en-dash) and `"paper.txt:555-557 — \"...\""` (informative).
- **C191** (graph.v2.json line ~3940-3942): still has both `"paper.txt:1947–1949"` (bare, en-dash) and `"paper.txt:1947-1949 — \"...\""` (informative).
- **C193** (graph.v2.json line ~3982-3986): still has 3 entries, two of which are near-duplicates of the paper.txt:1950-1952 quote (one em-dash format, one parenthesis format).

The fixer's log documents edits to graph.v2.json that are not present in the actual file. Most likely the direct graph.v2.json edits were overwritten when the graph_builder re-generated the file from section.md sources. Since the deduplication edits were applied to graph.v2.json directly (not to the section.md files, which contain single evidence lines per claim), the graph_builder re-run would have regenerated the duplicates from the multiple evidence sources in the checker section.md files.

Why it remains B: duplicate evidence entries in graph.v2.json do not themselves constitute a "FLAGGED without required evidence" auto-A violation (the evidence is present, just redundant). The issue is cosmetic quality and downstream rendering noise, but not blocking per `src/methodology/04-review.md`.

Resolution: The fixer must deduplicate the evidence arrays in graph.v2.json directly, or ensure the section.md source files contain only single evidence entries per claim so that graph_builder re-generation does not reintroduce duplicates. Given the root cause (graph_builder overwrites direct edits), the preferred fix is to suppress duplicate evidence in the section.md files themselves.

---

## Auto-A trigger checks (fresh sweep, round 2)

### T1. Bibtex key resolution

All [@key] citations in VERIFICATION.md and checker_literature/section.md post-fixer were cross-checked against `reviews/easy/phase1/outputs/references.bib` (35 entries). The M3 corrected-citation note references `heimel2023madnis` as a candidate that does NOT support the claim — this is a descriptive reference, not a new citation claim. No new bibtex key was fabricated by the fixer.

**No unresolvable bibtex keys found.**

### T2. graph.v2.json schema validation

The fixer's edits to graph.v2.json were confined to string content within existing `"evidence"` arrays. No structural properties were added or removed. The schema allows `"evidence"` as an array of strings. The claims count (200), groups count (20), and edges count (20) remain unchanged.

**No schema failure detected.**

### T3. Claim provenance vs. paper.txt

Re-checked FLAGGED claims' cited line numbers:
- C068: paper.txt:549-554 confirmed — "A pair of multivectors xV± = (1,0,0,±1)..." at those lines.
- C183: paper.txt:1660-1661 confirmed — "In Fig. 7 we find a clear performance improvement..." split continues at 1926 after figure captions.
- C185: paper.txt:1928 confirmed — "equivariant E(3)-GATr performs only marginally better than the plain transformer."
- C157: paper.txt:1421-1422 confirmed — "They share the generative CFM setup, which is currently the leading technique..."
- C004: paper.txt:22-23 and paper.txt:750-751 both confirmed.

**No provenance-line mismatches detected.**

### T4. FLAGGED verdicts without required evidence (complete sweep)

All 35 FLAGGED claim nodes in graph.v2.json were checked against the evidence standards in `src/conventions/error_categories.md`:

- **C007** (unreferenced): bare evidence pointer `paper.txt:79–80`; reasoning is in checker_unreferenced/section.md (VERIFICATION.md lines 12-15). The evidence standard for unreferenced requires explanation in the checker output, not necessarily in the graph node. Adequate.
- **C060** (unreferenced): evidence paper.txt:531-532 with reasoning in section.md. Adequate.
- **C070** (ambiguous + unreferenced): evidence present (two entries, see M10 duplication issue — non-blocking). The ambiguous standard is met (two interpretations given in ambiguous checker). Adequate.
- **C094** (unreferenced): evidence paper.txt:613-614 with reasoning. Adequate.
- **C142** (ambiguous + unreferenced): evidence paper.txt:1346-1347 with reasoning. Adequate.
- **C162** (unreferenced): evidence paper.txt:1432-1433 with reasoning. Adequate.
- **C004** (internal_contradiction + ambiguous): both contradicting passages quoted. Adequate.
- **C183** (internal_contradiction): both passages now present. Adequate. [M2 RESOLVED]
- **C185** (internal_contradiction): both passages now present. Adequate. [M2 RESOLVED]
- **C068** (domain_violation): violated_principle, canonical_source, paper quote all present. Adequate. [M1 RESOLVED]
- **C157** (literature_collision): paper passage and @butter2023jetdiffusion snippet both present. Adequate.
- All ambiguous FLAGGED entries (C001, C003, C015, C017, C026, C029, C033, C040, C052, C054, C057, C074, C086, C093, C129, C142, C166, C175, C181, C182, C186, C191, C192, C193, C196): each provides at minimum two distinct interpretations and a reasoning field in the ambiguous checker section. Standard met.

**No new "FLAGGED without evidence" violations found. All previously flagged A-triggers (M1, M2) are resolved.**

### T5. Color/severity-order consistency for FLAGGED nodes

Spot-checked multi-category FLAGGED nodes:
- C004 (`ambiguous` + `internal_contradiction`): color `#FF6D00` (orange = internal_contradiction, rank 3). Correct — internal_contradiction outranks ambiguous.
- C070 (`ambiguous` + `unreferenced`): color `#FFBF00` (amber = ambiguous, rank 4). Correct — ambiguous outranks unreferenced.
- C191 (`ambiguous` + `unreferenced`): color `#FFBF00` (amber). Correct.
- C193 (`ambiguous`): color `#FFBF00` (amber). Correct (single category).
- C157 (`literature_collision`): color `#D32F2F` (red). Correct (single category, rank 2).
- C068 (`domain_violation`): color `#7B1FA2` (purple). Correct (rank 1).
- C183 (`internal_contradiction`): color `#FF6D00` (orange). Correct (rank 3).
- C185 (`internal_contradiction`): color `#FF6D00` (orange). Correct (rank 3).

**No color/severity mismatches found.**

### T6. Output files outside declared deliverables

Phase 2 declared outputs: STRATEGY.md, VERIFICATION.md, graph.v2.json. Fixer edits are within phase2/agents/ (permitted intermediates) and phase2/outputs/. No undeclared output files observed.

**No out-of-scope files.**

---

## New issues introduced by the fixer

**F-R2-1 [B] — M10 deduplication edits to graph.v2.json not persisted in the artifact.**

File: `reviews/easy/phase2/outputs/graph.v2.json`, nodes C001 (lines ~602-607), C003 (lines ~645-648), C070 (lines ~1828-1830), C191 (lines ~3940-3942), C193 (lines ~3982-3986).

See M10 status above (NOT_RESOLVED). The fixer log documents changes that do not appear in the file. This is the continuation of the round-1 M10 B finding: the root-cause is that direct graph.v2.json edits are overwritten by graph_builder re-runs. The graph still carries duplicate/redundant evidence strings for these 5 nodes, degrading readability of the Phase 3 output.

Classification: B (same severity as original M10). Does not constitute an auto-A trigger since evidence is present (not absent); however, the fixer's stated RESOLVED status is misleading.

**F-R2-2 [B] — New evidence duplicates introduced by M8 into graph.v2.json for C180 and C197.**

File: `reviews/easy/phase2/outputs/graph.v2.json`, C180 node (lines ~3722-3725) and C197 node (lines ~4061-4063).

During M8, the fixer added evidence one-liners to the unreferenced section.md entries for C180 and C197. When the graph was re-generated (or when the fixer also edited graph.v2.json directly), these additions resulted in two evidence entries for each node — one a narrative support note and one a direct paper quote — covering the same line range. For C180: evidence [0] is "Supported by Fig. 6 showing..." and evidence [1] is `(\"L-GATr outperforms the baselines across all distributions.\")`. For C197: evidence [0] is "Supported by Table 2 (fine-tuning results)..." and evidence [1] is a direct paper quote from paper.txt:1957-1958.

These are not harmful to verdict correctness, but they are redundant evidence entries that M10 was supposed to prevent and that now exist in newly fixed nodes. This weakens the M10 fix's scope.

Classification: B (same category as M10). Resolution: deduplicate to retain the most informative entry per node, consistent with the M10 strategy.

Note: C184 similarly has 2 evidence entries (support note + paper quote at paper.txt:1927-1928). Same issue, same category.

---

## Verification of no new fabricated citations

The fixer's edits to checker_literature/section.md (M3), checker_unreferenced/section.md (M5, M7, M8, M9), checker_ambiguous/section.md (M6), checker_domain/section.md (M4), and graph.v2.json (M1, M2, M10) were scanned for [@key] references. The only bibtex key mentioned in M3 context is `heimel2023madnis` and `butter2023jetdiffusion` — both confirmed present in references.bib. No new key was introduced. The M3 note does not cite either as supporting the claim; it documents why they do NOT support it.

**No fabricated citations found.**

---

## C findings (round-1 carry-overs, unchanged)

The following round-1 C findings remain unaddressed, as directed by the arbiter:

- **M11 (C183↔C185 contradiction edge)**: Still no `contradicts` edge between C183 and C185 in graph.v2.json edges section. Non-blocking. Carry forward as C.
- **M12 (C068 secondary evidence from paper.txt:553-554)**: Not added. Non-blocking. Carry forward as C.
- **M13–M16**: Non-findings or confirmed no-action items per arbiter round-1 ruling.

---

## Summary table

| ID | Category | Severity | Round-1 Finding | Status |
|----|----------|----------|-----------------|--------|
| M1 | FLAGGED without required evidence (graph) | A | C068 domain_violation evidence empty | RESOLVED |
| M2 | FLAGGED without required evidence (graph) | A | C183/C185 contradiction evidence empty | RESOLVED |
| M3 | Corrected-citation note missing | A | C157 literature_collision no corrected-citation note | RESOLVED |
| M4 | Checker confidence/canonical_source | B | C068 medium confidence; Weinberg §2.5 indirect | RESOLVED |
| M5 | Strategist coverage gap | B | C002 absent from unreferenced section | RESOLVED |
| M6 | Ambiguous count discrepancy | B | Summary said 29, artifact has 27 | RESOLVED |
| M7 | C157 cross-reference missing | B | No cross-ref from unreferenced CLEAR to lit-collision FLAGGED | RESOLVED |
| M8 | Bare CLEAR Tier-1 entries | B | No evidence one-liners for high-importance CLEAR entries | RESOLVED |
| M9 | Five high-importance unreferenced claims missing | B | C029, C031, C036, C041, C054 absent from unreferenced checker | RESOLVED |
| M10 | graph.v2.json deduplication | B | Duplicate evidence arrays in C001, C003, C070, C191, C193 | NOT_RESOLVED |
| F-R2-1 | M10 carry-forward: dedup edits not persisted | B | graph.v2.json still has all pre-fixer duplicates | NEW (continuation of M10) |
| F-R2-2 | New redundant evidence introduced by M8 | B | C180, C184, C197 now have two evidence entries covering same line range | NEW |
| M11 | Missing contradiction edge | C | C183↔C185 no `contradicts` edge | CARRY-FORWARD (non-blocking) |
| M12 | C068 secondary evidence | C | paper.txt:553-554 not added as secondary evidence | CARRY-FORWARD (non-blocking) |

**Blocking A findings: NONE.** All three round-1 A findings (M1, M2, M3) are fully resolved.

**Active B findings: 3** (M10/F-R2-1 is the same unresolved item; F-R2-2 is new from the fixer's M8 scope expansion).

**Recommendation:** The round-2 arbiter should assess whether the remaining B findings (unresolved M10 deduplication in graph.v2.json) are sufficient to mandate another ITERATE. Per the arbiter logic in `src/methodology/04-review.md`: "elif any B and not previously fixed: ITERATE." M10 was previously filed as B and is not fixed; F-R2-2 is a new B finding. Under strict reading, these mandate another fixer pass. However, the findings are cosmetic (redundant evidence, not missing evidence), and the arbiter may elect to PASS with a note if the constructive reviewer concurs that the remaining B items are sufficiently minor.
