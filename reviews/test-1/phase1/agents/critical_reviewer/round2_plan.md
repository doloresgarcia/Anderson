# Plan — critical_reviewer phase 1 ROUND 2 (test-1)

Round 2 of the single-bot review. Round 1 raised 0 A, 8 B (F01–F08) + 4 C
(F09–F12). The fixer addressed F01–F08; F09–F12 were de-scoped by the
orchestrator. The graph_builder then re-emitted `graph.v1.json` to keep it
consistent with the fixer's edits to `CLAIMS.md` and `LITERATURE.md`.

## Steps

1. Re-read role spec, methodology/04-review.md, methodology/05-artifacts.md,
   and the relevant conventions (claim_taxonomy, graph_schema, confidence).
2. Read the round-1 critical.md and ARBITRATION.md so I know the exact
   resolution criteria for each F-finding.
3. Read fixer/log.md and graph_builder/log.md (round-2 rebuild section) to
   understand the precise edits applied.
4. Read the post-fixer artifacts:
   - `CLAIMS.md` (post-fix; expected 217 rows, ids 1–187 ∪ 190–219)
   - `LITERATURE.md` (post-fix retags at C006 / C148; new headings C218/C219)
   - `references.bib` (unchanged per fixer log)
   - `graph.v1.json` (rebuilt; G002 membership churn)
   - `graph.v1.skeleton.json` (frozen; sanity check)
   - `FINDINGS.md` (with new §8 deferral note for F01)
5. Re-run all auto-A triggers:
   - Set-intersection of LITERATURE.md bibtex keys vs references.bib keys
     (no new keys added so this should still pass; verify mechanically).
   - graph.v1.json schema validation per conventions/graph_schema.md
     (groups ≤ 20; per-group claim_ids in [1,15]; parent consistency;
     edge endpoints; color hex matches verdict; inferred-low-contradicts
     ban). Round-2 rebuild changed G002 — re-validate.
   - CLAIMS.md provenance sample of ≥ 10 rows (mix unchanged + fixer-touched:
     C001, C036, C044, C060, C148, C015, C218, C219, C100, C129, C217, C006).
     Read `paper.txt` at the cited line and confirm the quoted sentence
     matches.
   - Phase-1 outputs directory listing: confirm only the six declared
     deliverables present (CLAIMS.md, LITERATURE.md, references.bib,
     graph.v1.json, graph.v1.skeleton.json, FINDINGS.md). Per orchestrator
     note, build_v1.py was moved to src/build_graph_v1.py — check that
     phase1/agents/graph_builder/ no longer contains a Python file.
6. Resolve each round-1 B finding (F01–F08) using fresh artifact reads, not
   fixer assertion.
   - F01: confirm FINDINGS.md §8 records the deferral.
   - F02: confirm no .py file in phase1/agents/; presence of
     src/build_graph_v1.py verifies the move.
   - F03: confirm C036, C044, C060, C148 carry confidence=low in CLAIMS.md
     and graph.v1.json.
   - F04: confirm C015 row now contains only the first sub-claim and that
     C218 / C219 exist with the other two sub-claims.
   - F05: confirm C188 and C189 absent from CLAIMS.md, LITERATURE.md, and
     graph.v1.json claim set.
   - F06: subsumed by F03 (same row demotions).
   - F07: confirm C006 LITERATURE.md retags and phase-2 note.
   - F08: confirm C148 LITERATURE.md retag and OT-CFM note.
7. Hunt for NEW issues introduced by the fixer pass or round-2 rebuild:
   - Did the fixer over-edit (touched fields outside the listed findings)?
   - Are CLAIMS.md and LITERATURE.md still consistent (same claim ID set)?
   - Does graph.v1.json claim set match CLAIMS.md exactly?
   - Are FINDINGS.md numbers consistent with the post-fixer state, or stale?
   - Did the round-2 rebuild change any group structurally without
     justification?
   - Any auto-A trigger fires?
8. Tag each new finding A/B/C per methodology/04-review.md. Use IDs G01,
   G02, … to distinguish from F-series.
9. Write `phase1/review/critical_round2.md` per the role spec format.
10. Final concise report (< 200 words).

## Tools

- Read for files
- Bash for grep / Python set ops / paper.txt line lookups

## Hard constraints

- Read-only on phase-1 outputs.
- Auto-A triggers stay A even if "feels minor."
- Stale FINDINGS.md numbers after a fixer pass are typically B (weakening
  the report) but not A (not blocking the phase).
- No new fabricated citations were possible (no bibtex churn) but I still
  re-run the set-intersection check.
