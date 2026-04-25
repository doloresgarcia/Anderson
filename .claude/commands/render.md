---
description: Re-run the deterministic Phase-3 Python renderers (graph, stats, highlight, usage) without LLM dispatch.
argument-hint: <slug>
arguments: [slug]
---

# /render — re-run deterministic phase-3 outputs

You are the orchestrator. The user invoked `/render $0`.

`$0` is the review slug. If empty, tell the user `/render <slug>` is required
and stop.

This command does **not** dispatch any subagents. It just re-runs the
deterministic Python scripts wrapped by the Makefile. Useful while iterating
on conventions, the renderer, the stats script, or the highlighter without
spending tokens on a full phase-3 redo.

## Preflight

Verify `reviews/$0/` exists. If not, tell the user to scaffold first and stop.

## Steps

Run each `make` target via Bash. Use the absolute repo-root working directory
so the Makefile resolves correctly.

1. **Graph render**

   ```
   make graph REVIEW=reviews/$0
   ```

   The target prefers `phase3/outputs/graph.final.json` and falls back to
   `phase2/outputs/graph.v2.json`. If neither exists, the target exits
   non-zero — surface its stderr and continue.

2. **Stats refresh**

   ```
   make stats REVIEW=reviews/$0
   ```

   Writes `reviews/$0/phase3/outputs/STATS.md` (or wherever
   `src/claim_stats.py` puts it).

3. **Highlight**

   ```
   make highlight REVIEW=reviews/$0
   ```

   Picks `highlight_paper.py` if a PDF is present, else `highlight_text.py`.

4. **Usage aggregation**

   ```
   make usage REVIEW=reviews/$0
   ```

   Writes `reviews/$0/USAGE.md` from the parsed subagent transcripts.

## Print outputs

After running, list the regenerated files so the user knows what to open:

- `reviews/$0/phase3/outputs/graph.final.html` (or `graph.v2.html` if
  fallback) — graph render
- `reviews/$0/phase3/outputs/STATS.md` — refreshed stats
- `reviews/$0/phase3/outputs/paper.highlighted.pdf` (or `.html`) —
  highlights
- `reviews/$0/USAGE.md` — token usage summary

If any step failed, summarize which one and its error so the user can fix
the underlying issue.
