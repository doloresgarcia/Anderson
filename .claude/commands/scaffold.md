---
description: Scaffold a new review tree from a paper source (PDF, text, arXiv, DOI, or URL).
argument-hint: <slug> <source>
arguments: [slug, source]
---

# /scaffold — bootstrap a review tree

You are the orchestrator. The user invoked `/scaffold $0 $1`.

- `$0` is the review slug (e.g. `my-paper`).
- `$1` is the paper source. It is one of:
  - a filesystem path ending in `.pdf` → use `--paper`
  - a filesystem path ending in `.txt` → use `--text`
  - a string starting with `arxiv:` → use `--arxiv` and strip the `arxiv:` prefix
  - a string starting with `doi:` → use `--doi` and strip the `doi:` prefix
  - a string starting with `http://` or `https://` → use `--url`

If `$0` or `$1` is empty, tell the user the correct invocation
(`/scaffold <slug> <source>`) and stop.

## Steps

1. **Pick the flag.** Inspect `$1` and decide which scaffold flag to pass:
   - `*.pdf` → `--paper $1`
   - `*.txt` → `--text $1`
   - `arxiv:NNNN.NNNNN` → `--arxiv NNNN.NNNNN`
   - `doi:10.xxx/yyy` → `--doi 10.xxx/yyy`
   - `https://...` or `http://...` → `--url $1`
   - anything else → tell the user the source format is not recognized and stop.

2. **Run the scaffolder.** Use the Bash tool:

   ```
   python3 src/scaffold_review.py --slug $0 <flag> <value>
   ```

   (Substitute the flag and value chosen in step 1. Use the absolute repo-root
   working directory.)

3. **Confirm the tree.** Run `ls reviews/$0/` and `ls reviews/$0/phase1/` so
   the user sees the scaffolded directories. If the directory does not exist,
   surface the scaffolder's stderr verbatim and stop.

4. **Print next steps.** Make the final message conditional on the source type.
   For local `--paper` / `--text`, tell the user:

   > Scaffolded `reviews/$0/`. Edit `reviews/$0/paper/paper.meta.json` if
   > needed, then run `/phase1 $0` to begin.

   For remote `--arxiv` / `--doi` / `--url`, tell the user:

   > Scaffolded `reviews/$0/` with the remote identifier recorded in
   > `reviews/$0/paper/paper.meta.json`. The paper was not fetched; add
   > `reviews/$0/paper/paper.txt` manually or re-run `/scaffold $0
   > <local.pdf|local.txt>` before `/phase1 $0`.

Do not dispatch any subagents in this command. Scaffold is offline and
deterministic.
