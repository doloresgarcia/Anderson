VERDICT: ITERATE

Arbiter: arbiter
Phase: 1 — Round 1
Date: 2026-04-25
Source: critical.md (single-bot mode; no constructive.md)

---

## Rationale

Two Category-A findings are present. Per the arbiter rule:

> if any A → ITERATE (spawn fixer, re-review)

F003 is a genuine data error (fabricated author metadata) requiring verification
and correction before the artifact can be trusted downstream.

F005 is reclassified by this arbitration. The ≤ 15 claims/group rule is
mathematically unsatisfiable for this paper: ⌈545/20⌉ = 28, which exceeds the
cap even with perfect distribution across the maximum-allowed 20 groups. The
graph_builder documented the conflict correctly; no graph restructuring can
resolve it within the ≤ 20 group constraint. **The defect lies in the schema,
not the data.** This arbitration downgrades F005's data component to Category C
(no graph change required) and introduces a new blocking requirement: the schema
wording must be patched (Category B, treated as blocking because it is the root
cause of the auto-A trigger). The fixer should update `conventions/graph_schema.md`
to add an explicit escape hatch for papers where ⌈N_claims / N_groups_max⌉ > 15,
replacing the hard cap with a soft guideline or a per-paper override mechanism.

F001 and F002 are Category B. They do not independently trigger ITERATE, but
they must be fixed before PASS. They are included in the fixer's scope.

F004 (skeleton file in outputs/) is Category B and is included in the fixer's
scope.

F006 and F007 are Category C suggestions; no fixer action required, but the
fixer may address them opportunistically.

---

## Finding Table

| ID   | Round | Severity | Status       | Description                                                        | Fixer action required |
|------|-------|----------|--------------|--------------------------------------------------------------------|----------------------|
| F001 | R1    | B        | Open         | LITERATURE.md uses cluster format; spec requires per-claim `## C001` sections | Yes — reformat |
| F002 | R1    | B        | Open         | `related` is not a valid relation value in LITERATURE.md           | Yes — reclassify each row as `supports` or remove |
| F003 | R1    | A        | Open         | `Badger:2022hwf` author field contradicts real paper (arXiv:2206.14831) | Yes — verify and correct authors |
| F004 | R1    | B        | Open         | `graph.v1.skeleton.json` in outputs/ instead of agent workspace    | Yes — move or delete |
| F005 | R1    | A→schema B | Reclassified | 14/20 groups exceed ≤ 15-claim cap; mathematically unavoidable (⌈545/20⌉=28); schema is defective | Yes — patch `conventions/graph_schema.md`; no graph change needed |
| F006 | R1    | C        | Open         | Orphan `hendrycks2016gaussian` in references.bib                   | Optional |
| F007 | R1    | C        | Open         | `Bogatskiy:2020tje` typed `@article` with `booktitle` field        | Optional |

---

## Fixer scope (blocking)

1. **F003** — Verify arXiv:2206.14831 authorship; correct or remove the `Badger:2022hwf` entry in `references.bib`. If the paper does not support the claims annotated under it in LITERATURE.md Cluster D, remove those rows.
2. **F005 (schema patch)** — Update `conventions/graph_schema.md` §Validation rules to replace the hard `len(claim_ids) ≤ 15` constraint with a soft guideline, and add a documented escape hatch (e.g., `max_claims_per_group = max(15, ⌈N_claims / N_groups⌉)`) for large papers. The existing `graph.v1.json` data is correct as-is.
3. **F001** — Reformat `phase1/outputs/LITERATURE.md` to use per-claim `## claim-XXXX` subsections as specified in `methodology/05-artifacts.md`.
4. **F002** — Reclassify all 14 `related` rows in LITERATURE.md as either `supports` or remove them. Do not introduce `related` without updating `05-artifacts.md`.
5. **F004** — Move or delete `phase1/outputs/graph.v1.skeleton.json`; it belongs in `phase1/agents/graph_builder/` or can be deleted since `graph.v1.json` supersedes it.

After fixes: re-run critical_reviewer → re-run arbiter (Round 2).
