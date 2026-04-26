PASS

# Phase 2 Arbitration — slug: easy — round 2

Reviewers: critical_reviewer (3 A RESOLVED, 6 B RESOLVED, 2 B NOT_RESOLVED, 2 C carried) + constructive_reviewer (4 B RESOLVED-or-downgraded, 4 C carried, 3 new C; explicit PASS recommendation). Round 2 (post-fixer round 1).

## Deduplicated finding table — round-1 → round-2 status

| Merged ID | Round-1 Severity | Round-1 subject | Round-1 fixer pass | Round-2 reviewer status | Final round-2 disposition |
|-----------|------------------|-----------------|--------------------|--------------------------|----------------------------|
| M1 | A | C068 graph node missing `violated_principle` and `canonical_source` for FLAGGED domain_violation | Fixer round 1 added violated_principle stabilizer computation + Weinberg §2.5 with explanatory note + paper quote to C068 evidence array | RESOLVED (critical) / RESOLVED (constructive) | RESOLVED |
| M2 | A | C183/C185 graph nodes had `evidence: []` despite FLAGGED internal_contradiction (auto-A) | Fixer round 1 added the unreferenced-section note, primary passage, and contradicting passage to both nodes | RESOLVED (critical) / RESOLVED (constructive) | RESOLVED |
| M3 | A | C157 literature_collision lacked corrected-citation note | Fixer round 1 added corrected-citation note evaluating heimel2023madnis and concluding no in-bib candidate supports the claim; no fabricated key | RESOLVED (critical) / RESOLVED (constructive) | RESOLVED |
| M4 | B | C068 confidence/canonical_source clarification (Weinberg §2.5 indirect) | Fixer round 1 added little-group/stabilizer connection note; confidence retained at medium (defensible) | RESOLVED | RESOLVED |
| M5 | B | C002 absent from unreferenced section | Fixer round 1 added C002 CLEAR entry with reasoning | RESOLVED | RESOLVED |
| M6 | B | Ambiguous count 29 vs. 27 discrepancy | Fixer round 1 added HTML comment enumerating all 27 FLAGGED claims | RESOLVED | RESOLVED |
| M7 | B | C157 cross-reference missing between unreferenced CLEAR and lit-collision FLAGGED | Fixer round 1 added cross-reference note in unreferenced section pointing to literature_collision FLAGGED | RESOLVED | RESOLVED |
| M8 | B | Bare CLEAR Tier-1 entries (C100, C101, C104, C112, C117, C129, C131, C138, C180-185, C193, C195, C197, C198) | Fixer round 1 added one-line evidence pointers to paper tables/figures/line ranges for all 17 entries | RESOLVED | RESOLVED |
| M9 | B | Five high-importance unreferenced claims missing (C029, C031, C036, C041, C054) | Fixer round 1 added five CLEAR entries with paper line ranges and reasoning | RESOLVED | RESOLVED |
| M10 | B | Duplicate evidence strings in graph.v2.json (C001, C003, C070, C191, C193) | Fixer round 1 edited graph.v2.json directly; graph_builder round-2 regenerate from un-deduplicated section.md re-introduced the duplicates | NOT_RESOLVED-B (critical) / PARTIALLY-RESOLVED-C downgrade (constructive) | DOWNGRADED to C — cosmetic only; no missing evidence, no schema break, no downstream blocker (see rationale) |
| F-R2-1 | NEW (B per critical) | Same root cause as M10: dedup not persisted in artifact after graph_builder regenerate | n/a (round-2 finding) | NEW B (critical) | DOWNGRADED to C — same root cause, same severity reasoning as M10 |
| F-R2-2 | NEW (B per critical) | New evidence duplicates introduced for C180, C184, C197 by M8+regenerate interaction (support note + paper quote covering same line range per node) | n/a (round-2 finding) | NEW B (critical) — constructive does not file separately | DOWNGRADED to C — same class as M10; informative content present, only redundant |
| F-CON-09 | NEW (C per constructive) | M10 dedup overwritten by graph_builder regenerate; recommends Phase-3 graph_builder dedup post-processing or section.md normalization | n/a (round-2 finding) | NEW C (constructive) | C — recorded; recommendation forwarded to Phase 3 |
| F-CON-10 | NEW (C per constructive) | C157 corrected-citation note is long inline in evidence array; visually mixed with paper-provenance entries | n/a (round-2 finding) | NEW C | C — Phase-3 report_writer should split `[corrected-citation]` entries into a separate "author action" list |
| F-CON-11 | NEW (C per constructive) | C002 entry uses `reasoning:` field label instead of `evidence:`; minor inconsistency with M8-added entries | n/a (round-2 finding) | NEW C | C — minor; no functional impact since CLEAR unreferenced entries do not feed highlighted spans |
| M11 | C | C183↔C185 contradiction edge missing from graph.edges | Not addressed (arbiter directed carry-forward) | CARRY-FORWARD C | C — recorded |
| M12 | C | C068 secondary evidence from paper.txt:553-554 not added | Not addressed (arbiter directed carry-forward) | CARRY-FORWARD C | C — recorded |
| M13 | C | checker_ambiguous coverage skews architectural | n/a | CARRY-FORWARD C | C — recorded |
| M14 | C | VERIFICATION.md lacks executive summary preamble | n/a | CARRY-FORWARD C | C — recorded |
| M15 | C | C077 INCONCLUSIVE thin Phase-3 disposition | n/a | CARRY-FORWARD C | C — recorded |
| M16 | C | Phase-1 carry-over C003/C005 off-by-one (informational) | n/a | CARRY-FORWARD C | C — recorded |

Final tally after round-2 adjudication: 0 A · 0 unfixed B · 9 C (carried + new). All round-1 A and B findings are either RESOLVED in artifact or DOWNGRADED to C on the merits.

## Adjudication of the severity dispute (M10 / F-R2-1 / F-R2-2 / F-CON-09)

The two reviewers describe the same evidence: graph.v2.json evidence arrays for C001, C003, C070, C180, C184, C191, C193, C197 contain redundant entries that survived the fixer's M10 dedup because graph_builder round-2 regenerated the graph from un-deduplicated section.md sources. Critical tags this B (with the verbatim caveat "cosmetic quality and downstream rendering noise, but not blocking"); constructive tags it C and recommends PASS.

I rule for the C classification on these grounds:

1. Definitional fit. `04-review.md` defines B as "Weakening — must fix before PASS but does not block advancement on its own," with examples "a claim was extracted but mistyped; a verification's supporting evidence is thin; the strategy ranking is poorly justified." All three examples concern correctness or sufficiency of *content*. C is defined as "Suggestion. Style or polish." Redundant-but-correct evidence strings are a style/polish defect, not a correctness or sufficiency defect. Every FLAGGED node retains the required evidence per `error_categories.md`; critical's own T4 sweep confirms this and explicitly states the issue is not an auto-A trigger because "evidence is present, just redundant."

2. Critical's own framing. Critical labels the issue "cosmetic" and "rendering noise" twice, and the closing recommendation explicitly invites the arbiter to PASS "if the constructive reviewer concurs that the remaining B items are sufficiently minor." Constructive does concur and recommends PASS. The reviewer disagreement is therefore narrow: it is about the label, not the underlying severity description, and critical pre-emptively delegated the call to the arbiter.

3. Downstream impact. Phase 3's consumers (highlighter, report_writer, graph_builder render) are not blocked. The highlighter can tolerate duplicate spans on the same line range; the report_writer can dedup programmatically; graph_builder can add a per-node evidence dedup as a post-processing step (recommended by F-CON-09). No Phase-3 deliverable is broken.

4. Architectural reality. The duplicates are an emergent property of the section.md-to-graph regenerate pipeline. A B-classified ITERATE would direct the fixer to normalize section.md sources, but the better fix lives in graph_builder (single point of dedup). Forwarding this to Phase 3 as a graph_builder post-process is the correct remediation locus, which is exactly what F-CON-09 recommends.

This is not a soften-to-avoid-the-cap call. If the duplicates were *missing* evidence rather than redundant evidence, this would be auto-A. If they introduced verdict ambiguity, this would be B. They do neither.

## Verdict

PASS. All three round-1 A findings (M1, M2, M3) are fully resolved in the artifact. Six of the seven round-1 B findings (M4–M9) are fully resolved. The remaining round-1 B (M10) and the two round-2 reviewer-introduced items in the same family (F-R2-1, F-R2-2) are reclassified C on the merits per the rubric definitions. Only C-class findings remain. Per `04-review.md`: "elif only C, or all A/B previously fixed: → PASS."

## Forwarded items for Phase 3

The orchestrator should pass these C-class items to the Phase-3 dispatch as advisory inputs (not blockers):

- **F-CON-09 / M10 / F-R2-1 / F-R2-2**: graph_builder for Phase 3 should deduplicate evidence arrays per node as a post-processing step (preferred), or the orchestrator should normalize section.md to a single evidence entry per claim per checker before re-running graph_builder.
- **F-CON-10**: report_writer should filter evidence entries beginning with `[corrected-citation]` (and similarly tagged tokens) into a separate "author action required" list rather than treat them as paper provenance.
- **F-CON-11**: parsing of checker_unreferenced should accept either `reasoning:` or `evidence:` field labels for CLEAR entries; consider normalizing.
- **M11**: optional — add a `contradicts` edge between C183 and C185 when graph.final.json is built.
- **M12, M13, M14, M15, M16**: recorded; non-blocking.
