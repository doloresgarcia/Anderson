# Constructive Review — Phase 3 — easy

## Overview

Phase 3 artifacts are generally clear and well-organized. The REPORT is readable
and the graph has real edge structure (21 edges across 200 claims). Findings
below focus on completeness and presentation gaps, not correctness.

---

## Findings

### [B-1] REPORT silently omits the 3 INCONCLUSIVE claims under internal_contradiction

STATS.md (line 79) shows `internal_contradiction: FLAGGED=3, INCONCLUSIVE=3,
CLEAR=26`. The three INCONCLUSIVE claims in this category are never mentioned or
explained anywhere in REPORT.md. The report covers the 3 FLAGGED
internal_contradiction claims in full, but a reader examining STATS will notice
the 3 INCONCLUSIVE entries and find no explanation. The INCONCLUSIVE section of
the report covers only the high-level driver categories (method design, result
comparisons, paywalled sources, domain context), none of which obviously explains
why internal_contradiction would yield INCONCLUSIVE rather than CLEAR or FLAGGED.

Fix: add a brief note in the Inconclusive section identifying which claims
received INCONCLUSIVE under internal_contradiction and why (e.g., the checker
identified candidate contradictions but insufficient context to confirm them).

**Category: B**

---

### [B-2] graph.final.json missing paper metadata fields required by schema

`graph_schema.md` shows the example paper object includes `title`, `doi`, and
`arxiv` fields. The actual JSON at `graph.final.json:1–5` contains only `slug`.
The paper's arXiv ID (2405.14806) and DOI are available in REPORT.md line 9 and
should populate these fields. Downstream consumers or renderers that expect
`paper.title` or `paper.arxiv` will silently get undefined.

Fix: add `"title": "A Lorentz-Equivariant Transformer for All of the LHC"`,
`"arxiv": "2405.14806"` to the `paper` object in graph.final.json (and
graph.final.html if it embeds the same JSON).

**Category: B**

---

### [B-3] Edge E021 has invalid provenance value

Edge E021 (`C183 contradicts C185`, `confidence: "medium"`) has
`"provenance": "paper.txt:analysis"`. The schema requires provenance to be either
a `paper.txt:line` pointer or the literal string `"inferred"`. The value
`"paper.txt:analysis"` matches neither form. This means the contradiction edge
between C183 and C185 — the only `contradicts` edge in the graph — has
unverifiable provenance. Schema validation rule "no edge of kind `contradicts`
has confidence `low` and `provenance: "inferred"`" does not cover this case, but
the spirit of the rule is that contradictions need anchored evidence.

Fix: change provenance to a specific line range (e.g.,
`"paper.txt:1660-1661,1928"`) that anchors both sides of the contradiction, or to
`"inferred"` with the confidence downgraded to `"low"` if no specific anchor is
available.

**Category: B**

---

### [B-4] REPORT trust score explanation omits the weighting formula

REPORT.md line 54 states "Trust score: 41/100 (low)" and STATS.md provides the
formula (CLEAR=1.0, INCONCLUSIVE=0.5, FLAGGED=0.0). The REPORT does not include
or reference the formula, so a reader cannot verify or reproduce the score from
the stated raw counts. With 0 CLEAR, 35 FLAGGED, and 165 INCONCLUSIVE out of 200
claims: `(0×1.0 + 165×0.5 + 35×0.0) / 200 = 82.5/200 = 0.4125 ≈ 41/100`. That
arithmetic checks out, but the REPORT should either reproduce the formula inline
or reference STATS.md explicitly so the score is not a black box to the reader.

Fix: add one sentence in the "What we checked" section giving the scoring formula
and the bucket thresholds, or add a cross-reference to STATS.md.

**Category: B**

---

### [C-1] 0 hedged claims across 200 is implausible and goes unaddressed

STATS.md reports "0 hedged / 200 not hedged." The paper contains many explicitly
hedged claims — e.g., C037 ("for most LHC applications"), C052 ("smooth
transition"), C166 ("crucial"), C181 ("for the first time"). These were all marked
`hedged: false` in CLAIMS.md, indicating the claim extractor did not detect
hedging. Neither REPORT.md nor STATS.md flags this as unusual. While this is
a Phase 1 artifact defect that the current phase cannot fix, the REPORT should
acknowledge that hedging detection may be incomplete, since it affects how
readers interpret the ambiguous-claims findings (many of the 27 ambiguous
FLAGGED claims involve hedging language that was treated as unhedged assertions).

Fix: add a note in the Limitations section that 0 hedged claims is an
extractor artifact and that hedging coverage may affect interpretation of the
ambiguous-claims tally.

**Category: C**

---

### [C-2] REPORT Section 4 (Ambiguous) listing is dense and hard to scan

The ambiguous section lists 27 claims, each with a single sentence of description.
For a 27-item list, this is hard to read. There is no sub-grouping by theme even
though the findings fall into natural clusters: (a) unquantified superlatives
("crucial," "significant," "essentially every"), (b) scope ambiguities ("wide
range," "essentially all"), (c) definitional ambiguities ("usual definition,"
"partial permutation symmetry"). Grouping by theme would allow a reader — or the
paper authors — to see the pattern rather than reading 27 independent items.

Fix: introduce 3–4 thematic sub-headings within the ambiguous section and group
claims under them. No content changes required.

**Category: C**

---

### [C-3] REPORT "Coverage gaps" mentions 112 UNCOVERED claims without table

REPORT.md line 301 states "112 of 200 claims are UNCOVERED in LITERATURE.md —
their only literature candidate was the self-citation." This is a useful
observation, but no breakdown by claim type is given. STATS.md's type×verdict
table (method=85 INCONCLUSIVE, interpretation=21 INCONCLUSIVE) implicitly conveys
this, but a reader of REPORT.md alone cannot tell which types dominate the
UNCOVERED population. Adding even a one-line sentence ("UNCOVERED claims are
predominantly method claims (85/94) and interpretation claims (21/35)") would
contextualize why the high INCONCLUSIVE rate is expected.

**Category: C**

---

### [C-4] REPORT source path is wrong

REPORT.md line 11 states: `**Source:** Paper extracted from
\`papers/annotated/paper_corrupted.pdf\``. The actual paper path for this review
is `reviews/easy/paper/paper.pdf` (or `paper.txt`). The path
`papers/annotated/paper_corrupted.pdf` does not exist in the repo. This is likely
a leftover from a different review or a placeholder. It is harmless to a human
reader but incorrect metadata.

Fix: change to `reviews/easy/paper/paper.pdf`.

**Category: C**

---

## Summary

- 1 finding that weakens the report's internal consistency (B-1: missing
  explanation for INCONCLUSIVE internal_contradiction claims).
- 2 findings that weaken artifact completeness (B-2: missing paper metadata in
  graph JSON; B-3: invalid edge provenance).
- 1 finding that makes a key metric opaque (B-4: trust score formula absent).
- 3 style/polish suggestions (C-1 through C-4).

No Category A findings.
