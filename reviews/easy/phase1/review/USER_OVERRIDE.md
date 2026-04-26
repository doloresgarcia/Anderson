# User override — Phase 1, slug `easy`

Date: 2026-04-26
Decided by: user (orchestrator session)
Override applied to: `reviews/easy/phase1/review/ARBITRATION.md` round-2 verdict

## Arbiter's verdict (unchanged)

The round-2 arbiter returned **ITERATE** under the standing rubric in
`src/methodology/04-review.md`:

> elif any B and not previously fixed: → ITERATE

with three open Category-B findings:

- **F-003 residual** — C003 and C005 still carry the off-by-one provenance
  pattern that was fixed for C001/C002/C007/C008/C009 in round 1.
- **F-NEW-001** — same C003/C005 issue, restated as a stand-alone B by the
  round-2 reviewer.
- **F-NEW-002** — `graph.v1.json` edge E017 has `kind: "supports"` while
  its provenance note describes a `depends_on`-shaped relation; the
  combination is internally inconsistent.

The arbiter's reasoning (preserved verbatim in `ARBITRATION.md`) explicitly
notes that the open findings are mechanically narrow but the rubric does
not have a "trivial enough to wave through" branch — that decision belongs
to the user at the iteration-cap escalation.

## User decision: PASS by override (option B)

The user, having been presented with options (A) authorize a second fixer
pass, (B) accept-and-PASS by override, or (C) orchestrator applies edits
directly, **chose option B**: accept the three open Category-B findings as
a noted limitation and advance Phase 1 without a second fixer iteration.

## Carried-forward limitations into Phase 2

The following remain unaddressed and should be visible to Phase-2 agents
and reviewers:

| ID | File | Issue | Effect on Phase 2 |
|----|------|-------|-------------------|
| F-003 residual / F-NEW-001 | `phase1/outputs/CLAIMS.md` C003, C005 | C003 should be `line: 19, provenance: paper.txt:19-20`; C005 should be `line: 67, provenance: paper.txt:67-70`. Mirror in `graph.v1.json`. | Provenance line numbers for C003 and C005 are off by one in CLAIMS.md (and therefore in graph.v1.json). Phase-2 checkers reading those provenance ranges will land one line early; the page numbers and section labels are correct. Cross-checking against `paper.txt` will require ±1 line tolerance for these two claim ids. |
| F-NEW-002 | `phase1/outputs/graph.v1.json` edge E017 | `C094 → C038, kind: "supports"` is internally inconsistent with the provenance note describing a `depends_on` relation. | Edge E017 may mislead Phase-2 strategist if it weights `supports` chains differently from `depends_on` chains. Treat E017 as low-confidence semantically; otherwise the graph is consistent. |

## Carried-forward Category-C findings (unchanged from round 1 / round 2)

- F-009 — `related` relation type used in LITERATURE.md but not in the artifact spec.
- F-010 — graph schema ambiguity on whether `page`/`line` satisfy the `provenance` rule for high-confidence claim nodes.
- F-011 — `hestenes1966` reference lacks DOI / ISBN; relies on a Google Books URL.
- F-012 — `FINDINGS.md` notes `hedged=0` but does not flag a specific Phase-2 strategist follow-up.
- F-NEW-003 — round-1 fixer's `log.md` is orchestrator-reconstructed (the fixer was rate-limited before writing it). Process note; not blocking.

## Authoritative status for the orchestrator

For `phase2.md`'s preflight, treat Phase 1 as **PASS-by-user-override**.
Phase 2 may proceed when the user issues `/phase2 easy`.

## What was NOT changed by this override

- The arbiter's honest ITERATE verdict in `ARBITRATION.md` is preserved verbatim. Only this `USER_OVERRIDE.md` documents the user-level disposition.
- No additional edits were applied to any Phase-1 output. The artifacts on disk reflect the round-1 fixer's state plus the orchestrator's re-derivation of `FINDINGS.md`.
- No git commit was made for `reviews/easy/phase1/`; per the user's standing preference, review artifacts remain untracked on this dev branch (`dev_dolo`).
