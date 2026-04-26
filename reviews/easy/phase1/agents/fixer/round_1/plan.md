# Fixer Round 1 — Plan

## Findings to address (in order)

### F-002 [A] — C172 provenance mismatch
- CLAIMS.md: change `line: 1507` (keep) and `provenance: paper.txt:1621-1624` to `provenance: paper.txt:1507-1624` with a note.
- The sentence begins on line 1507 ("L-GATr starts with p and applies the transformation...") then is interrupted by Table 6 (lines 1508-1620), and concludes at 1621-1624 with the equation.
- graph.v1.json and graph.v1.skeleton.json: C172 node `line` is already 1507 (correct). No change needed.

### F-001 [B] — C004 paraphrase
- CLAIMS.md: replace sentence with verbatim "For all three LHC tasks, we find significant improvements over previous architectures."
- graph.v1.json / graph.v1.skeleton.json: update C004 sentence.

### F-003 [B] — Off-by-one provenance C001, C002, C007, C008, C009
Corrections (verified against paper.txt):
- C001: provenance `paper.txt:15-16` → `paper.txt:16-17`; `line: 16` (keep)
- C002: provenance `paper.txt:17-18` → `paper.txt:18-19`; `line: 17` → `line: 18`
- C007: provenance `paper.txt:78-79` → `paper.txt:79-80`; `line: 78` → `line: 79`  
- C008: provenance `paper.txt:79-80` → `paper.txt:80-81`; `line: 79` → `line: 80`
- C009: provenance `paper.txt:81-82` → `paper.txt:82-83`; `line: 82` (keep, sentence begins at 82)
Mirror line corrections in graph.v1.json / graph.v1.skeleton.json.

Note: The reviewer says C009 starts at line 82 — paper.txt line 82 reads "3. small deviations between simulated and measured data require networks to be tuned on" and continues to line 83. So provenance should be 82-83.

### F-004 [B] — spinner2024lgatr self-citation
`spinner2024lgatr` is arXiv:2405.14806 = the paper under review. Action:
1. Remove every `[@spinner2024lgatr] — supports` line from LITERATURE.md for claims that are the paper's own content.
2. Claims that have no remaining candidates after removal → mark with `UNCOVERED` note.
3. Add `note = {self-citation; paper under review}` to the bib entry in references.bib but do NOT remove it (it is still used in the `related` or other citations in LITERATURE.md, and it may remain as a citation record).

After inspection: every spinner2024lgatr line has `relation: supports`. After removal, many claims will have only `related` entries. Those need the UNCOVERED marker.

### F-005 [B] — Group titles
Replace all 20 group title fields with 2-3 word noun phrases derived from most central claim.

### F-006 [B] — Group captions  
Replace all 20 group caption fields with original ≤25-word summaries.

### F-007 [B] — dominant_type arithmetic
Recompute for all 20 groups. Set "mixed" where no type ≥ 60%.

G002 claim types: C005(bf), C010(bf), C053(bf), C007(assumption), C008(assumption), C009(assumption), C140(bf), C141(bf), C149(bf), C157(bf)
→ background_fact: 7/10 = 70% → dominant_type stays background_fact (≥60%). Wait, reviewer says 4/10 = 40%...

Let me recount: G002 has C005, C010, C053, C007, C008, C009, C140, C141, C149, C157.
- background_fact: C005, C010, C053, C140, C141, C149, C157 = 7 claims
- assumption: C007, C008, C009 = 3 claims
7/10 = 70% → background_fact is dominant (≥60%).

The reviewer's finding says "4/10 claims (40%) are background_fact" but this appears incorrect based on the actual claim types. I will note this discrepancy in log.md and explain my reasoning.

Actually, the finding says G002 has C007, C008, C009 (assumption) alongside background_fact claims C005, C010, C053, C140, C141, C149, C157. Let me recount from the actual graph data:
G002 claim_ids: C005, C010, C053, C007, C008, C009, C140, C141, C149, C157 = 10 claims
background_fact: C005, C010, C053, C140, C141, C149, C157 = 7
assumption: C007, C008, C009 = 3
7/10 = 70% background_fact → dominant_type: "background_fact" is correct (≥60%).

The reviewer's count of "4/10" appears to be an error. I will contest this finding and set it as contested in log.md, but still audit all other groups.

### F-008 [B] — Zero edges
Add ~15-20 defensible structural edges.

## Files to modify
- reviews/easy/phase1/outputs/CLAIMS.md
- reviews/easy/phase1/outputs/LITERATURE.md
- reviews/easy/phase1/outputs/references.bib
- reviews/easy/phase1/outputs/graph.v1.json
- reviews/easy/phase1/outputs/graph.v1.skeleton.json
