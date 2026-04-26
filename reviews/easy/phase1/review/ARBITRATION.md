ITERATE

# Phase 1 Arbitration — review: easy

Arbiter: arbiter (single-bot mode; only critical_reviewer ran)
Date: 2026-04-26
Round: 2 (post-fixer round 1)

## Verdict rationale

Round-2 critical review finds 0 Category-A triggers (the auto-A F-002 is
fully resolved and no new auto-A trigger fires) and 5 Category-C findings
that are non-blocking. However, three Category-B findings remain open and
have never been through a fixer pass:

1. **F-003 (B, partially resolved)** — C003 and C005 still carry the
   off-by-one provenance pattern that the fixer corrected for
   C001/C002/C007/C008/C009. They sit in the same semantic family as F-003
   but were outside the fixer's declared scope, so they are *not* "previously
   fixed" within the meaning of `04-review.md` — the fix targeted five
   specific claim IDs and stopped there.
2. **F-NEW-001 (B, new)** — the C003/C005 corrections themselves, restated
   as a stand-alone finding by the round-2 reviewer.
3. **F-NEW-002 (B, new)** — graph.v1.json edge E017 has `kind: "supports"`
   while its provenance note ("follows directly from") describes a
   `depends_on` relation. The combination of direction and kind is
   internally inconsistent.

Per `src/methodology/04-review.md`:

```
elif any B and not previously fixed:      → ITERATE
```

These three B findings are unfixed, so the rubric mandates ITERATE. They
are mechanically narrow (two `line`/`provenance` corrections in CLAIMS.md
mirrored in graph.v1.json, plus a one-field edit on E017), but the rubric
does not have a "trivial enough to wave through" branch — that decision
belongs to the human at the iteration-cap escalation, not to the arbiter.
Single-bot mode rules out ESCALATE-via-disagreement; the verdict is
unambiguous on the rubric. The orchestrator should now apply the
phase-1 iteration cap of one and escalate to the user with this
arbitration as evidence.

## Deduplication logic (round-2)

I reconciled the round-1 finding set, the round-2 reviewer's resolution
status updates, and the three new findings. No findings are merged or
dropped:

- F-003 vs. F-NEW-001 — F-003 is the round-1 finding (now partially
  resolved for C001/C002/C007/C008/C009); F-NEW-001 is the round-2
  re-statement that lifts C003/C005 to a stand-alone B-class entry. They
  describe the same off-by-one pattern but cover disjoint claim sets and
  carry different statuses; both are kept for traceability. The fixer
  should treat them as one work item in any iterate pass.
- F-NEW-002 stands alone (graph edge semantics, not provenance).
- F-NEW-003 is a process-only Category-C note about the
  orchestrator-reconstructed fixer log; recorded, not blocking.
- All round-1 C findings (F-009, F-010, F-011, F-012) carry forward
  unchanged or with cosmetic improvement (F-012); not blocking.

## Deduplicated finding table

| ID | Severity | File / Location | Round introduced | Status (round 2) | Fixer pass that addressed it |
|----|----------|-----------------|------------------|------------------|------------------------------|
| F-002 | A | `phase1/outputs/CLAIMS.md` C172 (auto-A) | R1 | RESOLVED | round-1 fixer |
| F-001 | B | `phase1/outputs/CLAIMS.md` C004 | R1 | RESOLVED | round-1 fixer |
| F-003 | B | `phase1/outputs/CLAIMS.md` C001/C002/C007/C008/C009 (C003/C005 missed) | R1 | PARTIALLY RESOLVED — C003/C005 still off-by-one | round-1 fixer (scope: 5 of 7 claims) |
| F-004 | B | `phase1/outputs/LITERATURE.md`; `references.bib` `spinner2024lgatr` | R1 | RESOLVED | round-1 fixer |
| F-005 | B | `phase1/outputs/graph.v1.json` group titles | R1 | RESOLVED | round-1 fixer |
| F-006 | B | `phase1/outputs/graph.v1.json` group captions | R1 | RESOLVED | round-1 fixer |
| F-007 | B | `phase1/outputs/graph.v1.json` G002 dominant_type audit | R1 | RESOLVED — round-1 reviewer miscount; G002 7/10 background_fact = 70%, fixer correct | round-1 fixer (re-audit, no edit) |
| F-008 | B | `phase1/outputs/graph.v1.json` edges | R1 | RESOLVED — 20 edges added, schema-conformant (E017 semantics tracked separately as F-NEW-002) | round-1 fixer |
| F-NEW-001 | B | `phase1/outputs/CLAIMS.md` C003 (line/provenance), C005 (line/provenance); mirrored in `graph.v1.json` | R2 | OPEN — never fixed | (none) |
| F-NEW-002 | B | `phase1/outputs/graph.v1.json` edge E017 (`kind` vs. provenance note) | R2 | OPEN — never fixed | (none) |
| F-009 | C | `phase1/outputs/LITERATURE.md` `related` relation type (73×) | R1 | CARRIED FORWARD (non-blocking) | (none — out of fixer scope) |
| F-010 | C | `phase1/outputs/graph.v1.json` claim node `provenance` field | R1 | CARRIED FORWARD (non-blocking) | (none — out of fixer scope) |
| F-011 | C | `phase1/outputs/references.bib` `hestenes1966` DOI/ISBN | R1 | CARRIED FORWARD (non-blocking) | (none — out of fixer scope) |
| F-012 | C | `phase1/outputs/FINDINGS.md` hedged=0 Phase 2 flag | R1 | PARTIALLY ADDRESSED — slight improvement, not fully specific | round-1 fixer (cosmetic) |
| F-NEW-003 | C | `phase1/agents/fixer/round_1/log.md` (orchestrator-reconstructed) | R2 | NOTED (process; non-blocking) | n/a |

**Summary counts (round 2):** A = 0; B open = 3 (F-003 partial, F-NEW-001,
F-NEW-002); B previously fixed = 7 (F-001, F-003 [5/7 claim subset],
F-004 – F-008); C = 5 (F-009, F-010, F-011, F-012, F-NEW-003).

## Required fixer actions if iteration proceeds

The three open B findings are mechanically narrow:

1. **F-NEW-001 / F-003 residual** — In `CLAIMS.md`: set C003
   `line: 19`, `provenance: paper.txt:19-20`; set C005 `line: 67`,
   `provenance: paper.txt:67-70`. Mirror the `line` corrections in
   `graph.v1.json` C003 and C005 nodes. (No further off-by-ones found by
   the round-2 reviewer in adjacent spot-checks.)
2. **F-NEW-002** — Either change E017 `kind` from `"supports"` to
   `"depends_on"`, or reverse the edge to `source: C038, target: C094,
   kind: "depends_on"`. Either fix is acceptable; the current combination
   is internally inconsistent with the provenance note.

## Iteration-cap note (orchestrator)

This is round 2 of arbitration. Per `src/methodology/03-phases.md` and
`phase1.md`, the iteration cap is 1, which has now been reached. The
orchestrator must escalate this verdict to the user with this arbitration
as the evidence. The arbiter has applied the rubric honestly and not
softened the verdict to avoid escalation; the open B findings genuinely
warrant another fixer pass under the methodology, and the user is the
correct gatekeeper for whether to (a) authorize a second fixer pass,
(b) accept the open B findings and PASS by override, or (c) take some
other corrective action.
