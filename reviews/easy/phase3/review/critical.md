# Critical review — Phase 3 — easy

Reviewer: critical_reviewer  
Phase: 3  
Date: 2026-04-26

---

## Auto-A trigger checks

### 1. Bibtex key resolution
All bibtex keys cited in VERIFICATION.md resolve in `reviews/easy/phase1/outputs/references.bib`. No fabricated citations found. Auto-A trigger: CLEAR.

### 2. Graph schema validation
See findings F1 and F2 below.

### 3. VERIFICATION.md FLAGGED evidence standards
- C068 (domain_violation): evidence field includes violated principle, Weinberg §2.5 canonical source, and paper statement at `paper.txt:549-554`. Meets standard.
- C157 (literature_collision): cites `paper.txt:1421-1422` and `[@butter2023jetdiffusion] §Abstract` with snippet. Snippet is ≤30 words. Source is real and resolves. Meets standard.
- All 7 unreferenced FLAGGED claims: each has `evidence: paper.txt:line` and states what kind of source is required and confirms no adjacent citation. Meets standard.
- All 27 ambiguous FLAGGED claims: each provides ≥2 distinct interpretations with a stated reason why the ambiguity matters. Meets standard.
- All 3 internal_contradiction FLAGGED claims (C004, C183, C185): each quotes both contradicting passages with `paper.txt:line`. Meets standard.
Auto-A trigger: CLEAR.

### 4. Phase-3 prose-summary new verdicts
REPORT.md introduces no verdict type absent from VERIFICATION.md. No old-style PASS/FAIL verdicts found. Auto-A trigger: CLEAR.

### 5. Output files outside declared deliverables
Declared deliverables for PDF-input Phase 3: `graph.final.json`, `graph.final.html`, `paper.highlighted.pdf`, `STATS.md`, `REPORT.md`. All five are present. No extra files found in `reviews/easy/phase3/outputs/`. Auto-A trigger: CLEAR.

---

## Findings

### F1 — [A] Group verdict/color wrong for five all-INCONCLUSIVE groups

**What:** Groups G006, G015, G016, G017, G018 all carry `"verdict": "CLEAR"` and `"color": "#2ECC71"` (green) in `graph.final.json`, yet every child claim in each group has `verdict: "INCONCLUSIVE"`.

**Where:**
- `reviews/easy/phase3/outputs/graph.final.json` lines 173-174 (G006); lines 429-430 (G015); lines 456-457 (G016); lines 487-488 (G017); lines 512-513 (G018)
- Confirmed by `reviews/easy/phase3/outputs/STATS.md` per-group breakdown (G006: INCONCLUSIVE 12; G015: INCONCLUSIVE 8; G016: INCONCLUSIVE 9; G017: INCONCLUSIVE 10; G018: INCONCLUSIVE 14)

**Why:** `src/conventions/graph_schema.md` lines 163-168 define group verdict aggregation:
```
if any child verdict is FLAGGED:   group = FLAGGED
elif any child verdict is INCONCLUSIVE: group = INCONCLUSIVE, yellow
elif every child verdict is CLEAR: group = CLEAR, green
```
All children INCONCLUSIVE → group must be INCONCLUSIVE with color `#F1C40F` (yellow). CLEAR/green is incorrect and misleads the reader into thinking these groups are verified clean.

**Resolution:** Set `"verdict": "INCONCLUSIVE"` and `"color": "#F1C40F"` for G006, G015, G016, G017, and G018 in `graph.final.json`. Re-render `graph.final.html`.

---

### F2 — [A] STATS.md "By verdict" totals contradict graph.final.json claim verdicts

**What:** `STATS.md` reports `CLEAR: 0` in the "By verdict" table and the trust-score line "0 clear · 35 flagged · 165 inconclusive." However, `graph.final.json` shows many individual claims with `"verdict": "CLEAR"` — for example C002, C005, C006, C008, C009, C010, C019, C020, C022, C024, C027 (and many more) all carry `"verdict": "CLEAR"`.

**Where:**
- `reviews/easy/phase3/outputs/STATS.md` line 10 ("0 clear · 35 flagged · 165 inconclusive") and the "By verdict" table (lines 48-52)
- `reviews/easy/phase3/outputs/graph.final.json`: C002 at approximately offset 610, C005 at approximately offset 680, all G006 claims, etc.

**Why:** `src/methodology/05-artifacts.md` lines 231-234 state STATS.md is "derived from `CLAIMS.md` and `VERIFICATION.md`." STATS.md correctly reports 0 CLEAR at the aggregate level — a claim can only be CLEAR in aggregate if every checker that examined it returned CLEAR (and per-claim coverage in VERIFICATION.md shows many claims were not examined by all 5 checkers). But `graph.final.json` assigns `"verdict": "CLEAR"` to claims not fully examined, contradicting `src/conventions/graph_schema.md` lines 152-159 (claim.verdict must equal the VERIFICATION.md aggregate). Claims not examined by all checkers should carry `NOT_CHECKED` or `INCONCLUSIVE`, not `CLEAR`.

This creates a false impression in the interactive graph that many claims are verified clean.

**Resolution:** Re-run `graph_builder` to recompute per-claim aggregate verdicts from VERIFICATION.md. For any claim not appearing in a checker's section at all, the checker's contribution is NOT_CHECKED. The aggregate should be INCONCLUSIVE (not CLEAR) unless every checker that could apply explicitly returned CLEAR. Then re-run STATS.md or verify that the script's 0 CLEAR count matches the updated graph. Also fix group verdicts (F1 follows from fixing this).

---

### F3 — [B] REPORT.md ambiguous section says "27 claims flagged" but enumerates only 26

**What:** The ambiguous section of REPORT.md (line 116) states "**27 claims flagged.**" The detailed write-up that follows lists 26 claim headings. Two claims that VERIFICATION.md marks as ambiguous FLAGGED — C017 and C086 — are absent from the write-up.

**Where:**
- `reviews/easy/phase3/outputs/REPORT.md` line 116 (count header) and lines 118-229 (enumerated claims)
- `reviews/easy/phase2/outputs/VERIFICATION.md` ambiguous section: C017 FLAGGED (around line 151) and C086 FLAGGED (around line 241)
- `reviews/easy/phase3/outputs/graph.final.json`: C017 `"verdict": "FLAGGED", "flagged_categories": ["ambiguous"]` (around offset 880); C086 same pattern (around offset 2100)

**Why:** REPORT.md must enumerate all FLAGGED claims per category per `src/methodology/03-phases.md` Phase 3 intent ("REPORT.md summarizing what was checked, what failed, and why"). Missing two claims makes the section count inconsistent and leaves two findings unreported to the reader.

**Resolution:** Add write-up entries for C017 ("improve the classification" — ambiguity between self-comparison and field-wide comparison) and C086 ("different degree of optimization" — ambiguity between software vs. architectural explanation) to REPORT.md's ambiguous section.

---

### F4 — [B] REPORT.md per-group STATS.md breakdown omits CLEAR counts, inflating INCONCLUSIVE

**What:** STATS.md "Per group" table shows breakdowns that appear to omit CLEAR claims and only count FLAGGED and INCONCLUSIVE. For G001: STATS.md says `FLAGGED 5, INCONCLUSIVE 6` (total 11), but from graph.final.json, G001 has FLAGGED:5, INCONCLUSIVE:1 (C195 only), CLEAR:5 (C002, C065, C069, C197, C198). The INCONCLUSIVE count of 6 in the table is wrong; it is apparently absorbing the 5 CLEAR claims.

**Where:**
- `reviews/easy/phase3/outputs/STATS.md` lines 86-107 (Per group table)
- `reviews/easy/phase3/outputs/graph.final.json`: G001 children C002 (verdict CLEAR), C065 (verdict CLEAR), C069 (verdict CLEAR), C197 (verdict CLEAR), C198 (verdict CLEAR), C195 (verdict INCONCLUSIVE)

**Why:** `src/methodology/05-artifacts.md` says STATS.md is computed from VERIFICATION.md. If the script is treating "not mentioned in a checker section" as INCONCLUSIVE in the per-group breakdown, CLEAR claims that were not explicitly covered by all checkers appear in the INCONCLUSIVE bin, yielding inflated INCONCLUSIVE counts in the per-group table. This misrepresents group-level quality to the reader.

**Note:** This finding is closely related to F2. If F2 is fixed (graph verdicts corrected), the per-group breakdown should also be corrected by rerunning `src/claim_stats.py`.

**Resolution:** After resolving F2, rerun `src/claim_stats.py` to regenerate STATS.md with accurate per-group breakdowns.

---

### F5 — [B] REPORT.md cites a nonexistent paper source path

**What:** REPORT.md line 10 states `"**Source:** Paper extracted from \`papers/annotated/paper_corrupted.pdf\`"`. This path does not exist in the repository.

**Where:** `reviews/easy/phase3/outputs/REPORT.md` line 10

**Why:** The actual paper files are at `reviews/easy/paper/paper.pdf` and `reviews/easy/paper/paper.txt` (confirmed by `reviews/easy/CLAUDE.md` lines 3-5). The path `papers/annotated/paper_corrupted.pdf` is a fabricated path that does not correspond to any file. This is factually incorrect metadata in the report header.

**Resolution:** Replace the Source line with `**Source:** `reviews/easy/paper/paper.pdf`` (and/or `paper.txt`).

---

### F6 — [B] Highlighter log reports 203 claims; actual count is 200

**What:** The highlighter log (`reviews/easy/phase3/agents/highlighter/log.md` line 13) states "Processed VERIFICATION.md containing verdicts for 203 claims." The actual claim count in VERIFICATION.md and STATS.md is 200.

**Where:** `reviews/easy/phase3/agents/highlighter/log.md` line 13

**Why:** STATS.md line 8 explicitly states "200 claims extracted" and the graph has exactly 200 claim nodes (C001–C200). CLAIMS.md has 200 rows. The discrepancy of 3 extra claims in the highlighter's count suggests it may have processed the file incorrectly or double-counted some entries. This could affect which claims were highlighted (the 19 that matched) vs. skipped.

**Resolution:** Investigate and fix the highlighter's claim-count parsing; confirm that the 19 matched highlights correspond to the correct FLAGGED/INCONCLUSIVE claims; re-run the highlighter if the count discrepancy affected output.

---

### F7 — [C] Only 19 of 200 non-CLEAR claims were highlighted in paper.highlighted.pdf

**What:** The highlighter log reports "Highlighted claims: 19; Skipped (no match in PDF): 181." Of 200 claims that have FLAGGED or INCONCLUSIVE verdicts (per STATS.md), only 19 were successfully matched in the PDF.

**Where:** `reviews/easy/phase3/agents/highlighter/log.md` lines 26-28

**Why:** `src/methodology/03-phases.md` Phase 3 goal is to produce a highlighted paper "with FLAGGED sentences color-coded by error category and INCONCLUSIVE sentences colored yellow." With 90.5% of targeted claims unlocated in the PDF, the highlighted paper is nearly empty of annotations. While text-matching between extracted claim sentences and PDF content is known to be imperfect, a 9.5% match rate is exceptionally low and substantially limits the utility of `paper.highlighted.pdf` as a human-facing artifact.

**Resolution:** Investigate why extracted claim sentences fail to match PDF text (likely paraphrasing during extraction); consider using the `paper.txt` line numbers stored in the graph to locate claims, then highlighting the corresponding PDF pages, rather than string-matching the extracted sentence.

---

### F8 — [C] Highlighter log trust score (41/465) inconsistent with STATS.md trust score (41/100)

**What:** `reviews/easy/phase3/agents/highlighter/log.md` line 29 says "Trust score: 41/465." STATS.md line 9 says "Trust score: 41/100."

**Where:** Highlighter log line 29; STATS.md line 9

**Why:** `src/methodology/05-artifacts.md` defines STATS.md trust score as computed by `src/claim_stats.py` with a 0-100 scale. The highlighter log is computing a different "trust score" (provenance-match confidence denominated out of 465, not the claim-count-weighted score) and using the same label. This could confuse anyone reading the log. The 41 numerator happens to coincide but refers to different things.

**Resolution:** Rename the highlighter's internal metric (e.g., "provenance match score") to avoid confusion with the STATS.md trust score.
