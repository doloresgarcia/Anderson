# verifier (DEPRECATED)

> **This role has been replaced by five specialized checker agents.** See
> `conventions/error_categories.md` for the full specification.
>
> - `checker_unreferenced` — missing citations
> - `checker_ambiguous` — unclear or underspecified statements
> - `checker_contradiction` — internal contradictions
> - `checker_literature` — conflicts with published literature
> - `checker_domain` — violations of established domain knowledge
>
> Each checker writes its own section in `phase2/outputs/VERIFICATION.md`
> and uses the verdict set `FLAGGED` / `CLEAR` / `INCONCLUSIVE` instead of
> the old `PASS` / `FAIL` / `INCONCLUSIVE`.
>
> Do not dispatch this agent. The orchestrator dispatches the five checkers
> in parallel during phase 2.
