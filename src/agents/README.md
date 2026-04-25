# Agents

One file per role. Each file is the **complete, auditable specification** the
orchestrator uses to spawn that role. Files contain: role description, reads
(allowed inputs), writes (mandatory outputs), methodology references, and a literal
prompt template with `{{slot}}` placeholders the orchestrator fills.

| Role | Phase(s) | Kind |
|------|----------|------|
| `executor` | all | generic; specializations below inherit from it |
| `claim_extractor` | 1 | executor specialization |
| `literature_searcher` | 1 | executor specialization |
| `graph_builder` | 1, 2, 3 | executor specialization |
| `strategist` | 2 | executor specialization |
| `checker_unreferenced` | 2 | executor specialization — missing citations |
| `checker_ambiguous` | 2 | executor specialization — unclear statements |
| `checker_contradiction` | 2 | executor specialization — internal contradictions |
| `checker_literature` | 2 | executor specialization — literature collisions |
| `checker_domain` | 2 | executor specialization — domain violations |
| `highlighter` | 3 | executor specialization |
| `report_writer` | 3 | executor specialization |
| `fixer` | all | executor specialization, applies review-driven fixes |
| `critical_reviewer` | 1, 2, 3 | reviewer |
| `constructive_reviewer` | 2, 3 | reviewer |
| `arbiter` | all | adjudicator |

The orchestrator never writes a prompt for a role from scratch. It opens the role
file, fills slots, and dispatches.
