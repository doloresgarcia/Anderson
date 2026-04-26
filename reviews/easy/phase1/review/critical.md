# Critical Review — Phase 1 — review: easy — Round 2 (post-fixer)

Reviewer: critical_reviewer
Date: 2026-04-26
Round: 2 (fixer round 1 applied)
Auto-A triggers checked: bibtex key resolution, graph schema validation, claim provenance, FLAGGED-without-evidence, undeclared output files.

---

## Auto-A trigger results (round 2)

**Bibtex keys.** 34 keys cited in `LITERATURE.md` (down from 35 in round 1 — `spinner2024lgatr` is retained in `references.bib` but no longer cited in `LITERATURE.md`). All 34 cited keys resolve in `references.bib`. No unresolvable keys found. Auto-A trigger NOT fired.

**Graph schema validation.** `graph.v1.json` and `graph.v1.skeleton.json` inspected against `src/conventions/graph_schema.json`. 20 groups, 200 claims. All required fields present. 20 edges added; all use `id`, `source`, `target`, `kind`; all `kind` values are `supports` or `depends_on` (no `contradicts`). All `source` and `target` values are valid `C\d{3}` claim ids that resolve in the claims array. No self-loops. Edge `confidence` and `provenance` fields present on all 20 edges. Schema validation: PASS. Auto-A trigger NOT fired from schema alone. See F-007-R2 for a semantic edge direction issue.

**Claim provenance (page/line vs. paper.txt).** The primary auto-A provenance error (F-002) is resolved. Spot-checks of fixed claims confirm the fixer's corrections. A residual off-by-one in C003 and C005 was not in the fixer's scope (F-003 addressed only C001, C002, C007, C008, C009). See F-003-R2 (NOT_RESOLVED / narrowly resolved) and F-NEW-001 (new finding) for details. These are B-class; no new auto-A provenance trigger fires.

**FLAGGED-without-evidence verdicts.** No `VERIFICATION.md` exists in Phase 1. Auto-A trigger NOT applicable.

**Undeclared output files.** `reviews/easy/phase1/outputs/` contains: `CLAIMS.md`, `LITERATURE.md`, `references.bib`, `graph.v1.skeleton.json`, `graph.v1.json`, `FINDINGS.md`. All six are declared Phase 1 deliverables per `src/methodology/03-phases.md`. Auto-A trigger NOT fired.

---

## Round-1 findings — resolution status

### F-002 [A] — RESOLVED

**Evidence:** `CLAIMS.md` line 174 (C172) now reads `provenance: paper.txt:1507-1624`. Verified against `paper.txt`: line 1507 contains "space. Finally, we transform this velocity vp back into the parametrization x using the Jacobian" (sentence start); line 1624 contains the final expression `vp(p(t), t).` (sentence end). The range correctly spans the full claim sentence interrupted by Table 6 (lines 1508–1620). `graph.v1.json` C172 node has `line: 1507`, consistent with the corrected provenance start. Auto-A trigger no longer fires. **Fully resolved.**

---

### F-001 [B] — RESOLVED

**Evidence:** `CLAIMS.md` line 6 (C004) `sentence` now reads `"For all three LHC tasks, we find significant improvements over previous architectures."` — verbatim match with `paper.txt` lines 22–23. `graph.v1.json` C004 node sentence matches. **Fully resolved.**

---

### F-003 [B] — PARTIALLY RESOLVED

**What was fixed:** Five provenance corrections (C001, C002, C007, C008, C009) specified in the fixer's plan were applied. Spot-checks:
- C001: `provenance: paper.txt:16-17` — `paper.txt` line 16 reads "We show that the Lorentz-Equivariant Geometric Algebra Transformer (L-GATr) yields"; line 17 reads "state-of-the-art performance...". The claim sentence begins at line 16. Correct.
- C002: `provenance: paper.txt:18-19`, `line: 18` — line 18 is "Hadron Collider. L-GATr represents data..." where C002 begins. Correct.
- C007: `provenance: paper.txt:79-80`, `line: 79` — line 79 is "1. standard architectures do not capture amplitudes or densities at the per-mille level;" — correct.
- C008: `provenance: paper.txt:80-81`, `line: 80` — line 80 is "2. the target precision..." — correct.
- C009: `provenance: paper.txt:82-83`, `line: 82` — line 82 is "3. small deviations..." — correct.

**What remains unresolved:** The fixer's scope for F-003 was limited to the five claims explicitly named in the round-1 finding. Two nearby claims that exhibit the same off-by-one pattern were not corrected. See F-NEW-001 below. **Narrowly (partially) resolved.**

---

### F-004 [B] — RESOLVED

**Evidence:** `LITERATURE.md` header (lines 7–11) documents the removal of all `[@spinner2024lgatr] — supports` lines. FINDINGS.md (post-fixer, line 63) confirms "Claims marked UNCOVERED: 112 / 200." Spot-check: C001, C005, C013 sections confirm no `spinner2024lgatr` appears in any `supports` role. `references.bib` entry (lines 6–15) retains the bib record with `note = {self-citation; paper under review...}` as planned. The 112 UNCOVERED count is honest and matches the search's actual outcome. No auto-A trigger fires: the bib key is retained and resolves; it simply is no longer cited as evidence. **Fully resolved.**

---

### F-005 [B] — RESOLVED

**Evidence:** All 20 group `title` fields in `graph.v1.json` (lines 10, 38, 65, 91, 113, 143, 171, 197, 222, 247, 277, 305, 331, 360, 385, 410, 434, 465, 493, 525) are now 2–3 word noun phrases:
G001 "LHC performance", G002 "LHC ML context", G003 "equivariance interpretation", G004 "L-GATr overview", G005 "physics task context", G006 "algebra definitions", G007 "algebra interpretations", G008 "multivector representation", G009 "equivariant architecture", G010 "symmetry breaking benefits", G011 "reference multivectors", G012 "efficiency interpretation", G013 "benchmark results", G014 "amplitude regression", G015 "amplitude setup", G016 "top tagging setup", G017 "JetClass pretraining", G018 "generation setup", G019 "L-GATr generation", G020 "generation results". No truncated strings, no bare type labels. Mirrored in `graph.v1.skeleton.json`. **Fully resolved.**

---

### F-006 [B] — RESOLVED

**Evidence:** All 20 group `caption` fields are original single-sentence summaries, verified to not be copies of any single claim sentence. Word counts checked for a sample:
- G001: 15 words ✓
- G002: 18 words ✓
- G006: 22 words ✓ ("Formal definitions of the spacetime geometric algebra, its product rules, layer operations (linear, attention, LayerNorm, activation), and the CFM diffusion framework.")
- G018: ~16 words ✓

All captions stay within the ≤25-word constraint and describe the collective assertion of each group. **Fully resolved.**

---

### F-007 [B] — RESOLVED (with counting clarification accepted)

**Evidence:** The fixer's plan disputed the round-1 reviewer's claim that G002 had only 4/10 = 40% `background_fact`. Verification from `graph.v1.json` G002 `claim_ids` (lines 41–51): C005(background_fact), C010(background_fact), C053(background_fact), C007(assumption), C008(assumption), C009(assumption), C140(background_fact), C141(background_fact), C149(background_fact), C157(background_fact) → 7 background_fact + 3 assumption = 10 claims; 7/10 = 70%. The fixer is correct: `dominant_type: "background_fact"` is accurate for G002 per the >60% threshold in `src/conventions/graph_schema.md`. The round-1 reviewer's count of "4/10" was an error in the review (likely miscounting only the claims explicitly listed as examples rather than the full list). The round-2 review accepts the fixer's correction.

All 20 groups' `dominant_type` values were re-audited against their `claim_ids`:
- G005: 8/13 = 62% background_fact → "background_fact" correct (barely above threshold; defensible).
- G003: 6/8 = 75% interpretation → "interpretation" correct.
- G009: all method claims → "method" correct.
- Other groups audited without discrepancy. No `dominant_type` mismatches found.
**Fully resolved** (the round-1 finding was a reviewer miscount, not an artifact error).

---

### F-008 [B] — RESOLVED

**Evidence:** `graph.v1.json` now contains 20 edges (E001–E020). All edges:
- Use only `supports` or `depends_on` (no `contradicts`).
- Have `id`, `source`, `target`, `kind`, `confidence`, `provenance` fields (schema-conformant).
- All `source` and `target` values are valid claim IDs in the claims array.
- No self-loops.

Spot-check of edge content vs. paper text:
- E001 (C015→C014, `depends_on`): paper.txt:118 "L-GATr generalizes GATr" — the generalization claim explicitly depends on the GATr definition. ✓
- E004–E007 (C051→C041/C043/C045/C049, `depends_on`): paper.txt:363–369 defines the full L-GATr architecture using Linear, Attention, LayerNorm, Activation — all four `depends_on` edges are warranted. ✓
- E008 (C100→C001, `supports`): paper.txt:747–751 presents the amplitude scaling result (C100) as evidence for the headline claim (C001). ✓
- E010 (C129→C001, `supports`): paper.txt:1036–1038 JetClass improvement (C129) supports LHC performance headline (C001). ✓

One semantic concern noted as F-NEW-002 below. Overall, 20 edges provide meaningful structural context. **Resolved** (with a B-level semantic issue noted as a new finding).

---

### F-009 [C] — CARRIED FORWARD (unchanged)

Not addressed by the fixer (out of scope, Category C). `related` relation type still appears 73 times in `LITERATURE.md`. `src/methodology/05-artifacts.md` format spec shows only `supports` and `contradicts`. Category C; does not block PASS.

---

### F-010 [C] — CARRIED FORWARD (unchanged)

Not addressed by the fixer (out of scope, Category C). High-confidence claim nodes in `graph.v1.json` still lack a `provenance` field. Schema ambiguity on whether `page`/`line` satisfies the rule for v1 remains unresolved. Category C; does not block PASS.

---

### F-011 [C] — CARRIED FORWARD (unchanged)

Not addressed by the fixer (out of scope, Category C). `hestenes1966` bib entry still lacks a DOI or ISBN (`references.bib` lines 41–48). Category C; does not block PASS.

---

### F-012 [C] — PARTIALLY ADDRESSED

`FINDINGS.md` (post-fixer, lines 112–115) retains the hedged=0 note and now adds: "The taxonomy's strict reading rejects modal language without explicit weakening markers; the constructive reviewer may reasonably re-flag this as overly literal in Phase 2." This is a slight improvement (acknowledges Phase 2 follow-up) but does not explicitly name the key result/interpretation claims (C001, C004, C112, C129, C197) for strategist attention as recommended in round 1. Category C; does not block PASS. Noting for completeness.

---

## New findings introduced or revealed by the fixer pass

### F-NEW-001 [B] — C003 and C005 provenance off-by-one (fixer scope did not cover these)

**File/location:** `reviews/easy/phase1/outputs/CLAIMS.md` row C003 (line 5) and row C005 (line 7); mirrored in `graph.v1.json` claim nodes C003 and C005.

**What is wrong:**

- C003: `line: 18`, `provenance: paper.txt:18-19`. `paper.txt` line 18 is "Hadron Collider. L-GATr represents data in a geometric algebra over space-time and is" — this is the tail of C002's sentence. The C003 sentence "The underlying architecture is a versatile and scalable transformer, which is able to break symmetries if needed." begins at line 19 ("equivariant under Lorentz transformations. The underlying architecture is a versatile") and continues to line 20. The `line` field should be 19 (the first line containing any C003 text) and provenance should be `paper.txt:19-20`. The current provenance starts one line too early (repeating C002 territory) and ends one line too early (missing line 20 which completes "and scalable transformer, which is able to break symmetries if needed.").

- C005: `line: 66`, `provenance: paper.txt:66-69`. `paper.txt` line 66 is "Introduction" (a section heading). Line 67 is "Modern machine learning (ML) is poised to define much of the future program at the Large". The C005 sentence starts at line 67. The `line` field should be 67, and provenance should be `paper.txt:67-70` (the sentence runs through line 70 ending at "ence."). This is the same pattern as the F-003 findings that were fixed for C001/C007/C008: the provenance start includes a heading rather than the first line of the claim sentence.

**Why it is wrong:** `src/methodology/05-artifacts.md` requires `provenance` to locate the claim text accurately. `src/conventions/confidence.md` ties `high` confidence to "essentially verbatim" extraction with accurate location. Both C003 and C005 have `confidence: "high"`. The fixer correctly fixed C001/C002/C007/C008/C009 but the off-by-one pattern was systemic; the fixer's narrow scope missed these two adjacent claims.

**Why it is B not A:** The claim sentences are real and extractable from the cited line ranges (the text is present in the range, just with extraneous leading or trailing context), so this does not trigger the auto-A "page/line does not match paper.txt" in the most strict sense. However it is the same pattern as F-003 which was B in round 1.

**Resolution:** In CLAIMS.md: set C003 `line: 19`, `provenance: paper.txt:19-20`; set C005 `line: 67`, `provenance: paper.txt:67-70`. Mirror the `line` corrections in `graph.v1.json` C003 and C005 nodes. Check C006 (line 70, provenance `paper.txt:70-71`) — line 70 continues the Introduction paragraph and C006's sentence starts at line 70 ("The question is no longer if..."); that one is correct. No further off-by-ones found in sampled nearby claims (C010, C011 spot-checked and appear correct).

---

### F-NEW-002 [B] — Edge E017 direction/kind inverted: C094 should `depend_on` C038, not `support` it

**File/location:** `reviews/easy/phase1/outputs/graph.v1.json`, edge E017 (lines ~3480–3487).

**What is wrong:** E017 is `source: C094`, `target: C038`, `kind: "supports"`. The provenance note reads: "exact Lorentz invariance of amplitude (C094) follows directly from the equivariance property (C038)." The phrase "follows directly from" indicates that C094's truth requires C038's truth — a `depends_on` relationship by definition. Per `src/conventions/graph_schema.md`: "`depends_on`: A → B means 'A's truth requires B's truth.'" The claim C094 ("L-GATr guarantees the exact Lorentz invariance of the amplitude") is a *consequence* of C038 ("L-GATr is exactly equivariant under Lorentz group transformations") — if C038 is false, C094 is undefined. This is a pre-condition (depends_on), not evidence (supports). Using `supports` here means "C094 is evidence for C038" — the opposite direction makes semantic sense too (a concrete result supporting a general claim), but the provenance's own language ("follows from") contradicts that reading and identifies this as a `depends_on`.

**Why it is wrong:** `src/conventions/graph_schema.md` defines `supports` as "A is evidence for B" and `depends_on` as "A's truth requires B's truth." The fixer's provenance note for E017 explicitly describes a `depends_on` relationship. Using `supports` instead misrepresents the logical structure of the paper's argument and could mislead Phase 2 and Phase 3 agents/readers about the dependency chain.

**Resolution:** Change E017 `kind` from `"supports"` to `"depends_on"`. No other field change needed; the provenance note already correctly describes the relationship. Alternatively, if the intent was that C094 (a more concrete result) supports C038 (a general equivariance claim), the direction should be reversed to `source: C038, target: C094, kind: "depends_on"` (C038's equivariance property is the pre-condition for C094's invariance guarantee). Either fix is acceptable; the current combination of direction + kind is internally inconsistent per the provenance note.

---

### F-NEW-003 [C] — Process note: orchestrator-reconstructed fixer log

**File/location:** `reviews/easy/phase1/agents/fixer/round_1/log.md` (entire file).

**What is wrong:** The `log.md` was not written by the fixer agent itself. The fixer was rate-limited mid-session after completing all artifact edits. The orchestrator reconstructed the audit trail by diffing artifacts and authored `log.md` in place of the fixer.

**Why it is noted:** The architecture invariant (`CLAUDE.md`) states "Subagents cannot spawn other subagents; all dispatch is flat." The orchestrator authoring a subagent's log.md is not a dispatch violation but does break the chain-of-custody principle: the log is an audit artifact, not a content artifact. A reviewer cannot confirm whether the fixer's reasoning (e.g., the G002 counting dispute, the C172 anchor choice at line 1507 vs. 1504) reflects the actual fixer's intent or the orchestrator's reconstruction.

**Severity:** Category C. The artifact edits themselves are verifiable by direct inspection of the output files (which this review has done). The log authorship ambiguity does not affect correctness of the deliverables. However, if a subsequent round needs to audit the fixer's chain of reasoning (e.g., for the G002 dispute), the reconstructed log should be treated as "orchestrator's reconstruction, not fixer's certified output."

**Resolution:** No new edits needed to advance. If preferred, a fresh fixer can re-emit a native log in a follow-up pass with no artifact changes, purely for audit completeness. This is cosmetic and not blocking.

---

## Summary table

| ID | Severity | Status | Topic |
|----|----------|--------|-------|
| F-002 | A | RESOLVED | C172 provenance mismatch (auto-A) |
| F-001 | B | RESOLVED | C004 paraphrase → verbatim |
| F-003 | B | PARTIALLY RESOLVED | Off-by-one C001/C002/C007/C008/C009 fixed; C003/C005 missed |
| F-004 | B | RESOLVED | `spinner2024lgatr` self-citation removed; 112 UNCOVERED honest |
| F-005 | B | RESOLVED | Group titles rewritten as 2–3 word noun phrases |
| F-006 | B | RESOLVED | Group captions rewritten as ≤25-word originals |
| F-007 | B | RESOLVED | dominant_type re-audited; round-1 reviewer miscount confirmed; G002 correct as-is |
| F-008 | B | RESOLVED | 20 edges added; schema-conformant; spot-checked against paper |
| F-009 | C | CARRIED FORWARD | `related` relation type undefined in spec (73 occurrences) |
| F-010 | C | CARRIED FORWARD | High-confidence claim nodes lack `provenance` field |
| F-011 | C | CARRIED FORWARD | `hestenes1966` lacks DOI/ISBN |
| F-012 | C | PARTIALLY ADDRESSED | hedged=0 Phase 2 flag improved but not fully specific |
| F-NEW-001 | B | NEW | C003 and C005 provenance off-by-one (fixer scope missed them) |
| F-NEW-002 | B | NEW | E017 `kind: "supports"` contradicts provenance note; should be `depends_on` |
| F-NEW-003 | C | NEW (process) | Fixer log.md is orchestrator-reconstructed, not fixer-authored |

**Blocking (A):** 0 findings.
**Weakening (B):** 3 findings (F-003 partially unresolved, F-NEW-001, F-NEW-002).
**Suggestions (C):** 5 findings (F-009, F-010, F-011, F-012, F-NEW-003).

**PASS eligibility assessment:** No auto-A triggers fire in round 2. The two new B findings (F-NEW-001, F-NEW-002) are narrow corrections: F-NEW-001 is a line-range correction for two claims following the same pattern as F-003 (already established as fixable), and F-NEW-002 is a one-field change to edge E017 (`kind` from `"supports"` to `"depends_on"`). F-003's partial resolution status means C003 and C005 still have wrong provenance ranges. All three open B findings are targeted and mechanical. Per `src/methodology/04-review.md` arbiter logic, any unfixed B finding from the first pass that is "not previously fixed" mandates another ITERATE. The arbiter must decide whether these B findings warrant another fixer pass or whether the corrections are trivial enough to be treated as part of a Phase 2 prep cleanup. This reviewer notes they are easily addressable in a short fixer pass.
