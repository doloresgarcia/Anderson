---
mode: A
slug: easy
date: 2026-04-26
---

# Literature Searcher Plan — easy

## Pass 1: Literature Bank

The `literature_bank/` directory exists at repo root. PDFs cannot be read
because `pdftoppm` is not installed (poppler-utils unavailable on this host).
All claims are therefore **uncovered** after Pass 1 and will proceed to
external search.

Bank status: UNREADABLE (pdftoppm missing). All claims forwarded to Pass 2.

## Pass 2: External Search Strategy

The paper's own reference list (pages 22–26 of paper.txt) provides authoritative
mappings from numbered citations to bibliographic records. I use this list as the
primary source for any claim that cites a numbered reference. Where the paper
does NOT cite a specific reference for a claim, I perform targeted WebSearch.

### Claim grouping for external search

With 200 claims, I group by theme and search per group rather than per claim:

**Group A — L-GATr / GATr architecture** (C001–C003, C014–C017, C038–C052,
C073–C088, C194–C200): Core architecture references are [33] (GATr NeurIPS 2023),
[34] (Euclidean/projective/conformal GATr AISTATS 2024), [35] (arXiv 2405.14806
L-GATr preprint), [38] (Attention is all you need), [39] (Layer norm in
transformer), [44] (FlashAttention), [87].

**Group B — Geometric algebra / Spacetime algebra** (C018–C037): Primary
references are [36] (Hestenes 1966 textbook) and [35].

**Group C — Amplitude regression** (C089–C109): References [45–49], [72] (MadGraph5).

**Group D — Jet tagging** (C110–C139): References [2–14], [51–60], [61] (top
quark dataset), [59] (ParT).

**Group E — Event generation / CFM** (C140–C186): References [17–32], [76–80].

**Group F — Interpretive / background claims** (C005–C013, C187–C193):
References [1], [15], [16].

### Key external searches planned

1. Verify arXiv 2405.14806 (L-GATr preprint, ref [35])
2. Verify GATr NeurIPS 2023 (arXiv 2305.18415, ref [33])
3. Verify Attention is All You Need (arXiv 1706.03762, ref [38])
4. Verify LorentzNet (arXiv 2201.08187, ref [10])
5. Verify PELICAN (arXiv 2211.00454, ref [12])
6. Verify ParT (arXiv 2202.03772, ref [59])
7. Verify MIParT (arXiv 2407.08682, ref [60])
8. Verify FlashAttention (arXiv 2205.14135, ref [44])
9. Verify JetClass dataset (arXiv with [59])
10. Verify MadGraph5 (arXiv 1405.0301, ref [49]/[62])
11. Verify Conditional Flow Matching (arXiv 2210.02747, ref [78])
12. Verify Hestenes space-time algebra textbook (ref [36])
13. Verify Plehn et al. Modern ML for LHC Physicists (arXiv 2211.01421, ref [1])
14. Verify Butter et al. ML landscape of top taggers (arXiv 1902.09914, ref [2])
15. Verify CGENN / Clifford group equivariant NN (arXiv 2305.11141, ref [14])

### Output limit

At most 5 candidates per claim. Bank candidates (none here) appear before
external candidates. Claims with no verifiable candidate are marked UNCOVERED.
