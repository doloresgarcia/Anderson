# Inputs

## Accepted forms

A review is launched against exactly one paper. `scaffold_review.py` (also
invoked via `/scaffold <slug> <source>`) accepts:

- A local PDF: `--paper /path/to/file.pdf`
- A local plain-text paper: `--text /path/to/paper.txt`
- An arXiv ID: `--arxiv 2401.12345`
- A DOI: `--doi 10.1234/abcde`
- A URL: `--url https://example.com/paper.pdf`

**Important.** `--paper` and `--text` produce a working `paper/paper.txt`
that phase 1 can read immediately. `--arxiv` / `--doi` / `--url` only
record the identifier in `paper/paper.meta.json` — they do **not** fetch
the paper. Either supply the text yourself before `/phase1`, or re-scaffold
with `--paper` / `--text` once you have a local copy.

`scaffold_review.py` produces:

```
reviews/<slug>/
  CLAUDE.md            # thin per-review pointer (paper meta + phase paths)
  prompt.md            # blank; orchestrator fills with the user's invocation
  paper/
    paper.pdf          # if --paper was supplied
    paper.txt          # extracted from --paper PDF, or copied from --text
    paper.meta.json    # title/authors/year/venue stub + DOI/arXiv/URL identifier
  phase1/  {outputs/, agents/, review/, logs/, prompt.md}
  phase2/  {outputs/, agents/, review/, logs/, prompt.md}
  phase3/  {outputs/, agents/, review/, logs/, prompt.md}
```

`paper.txt` is the artifact subagents read for claim extraction. `paper.pdf`
(when present) is the artifact phase 3 annotates.

## Literature bank

The repository contains `literature_bank/` at the root with pre-collected
PDFs. The `literature_searcher` subagent reads it directly via the
repo-root path — no per-review symlink. The bank is searched **first**;
external search (WebFetch / WebSearch / configured MCP) runs only for
claims the bank does not cover. See `.claude/agents/literature_searcher.md`.

## Optional input

- `--bib /path/to/refs.bib` — pre-supplied bibliography to seed the
  literature search.

## What is not an input

- Author intent, supplementary material the authors did not publish, or
  anything behind a paywall the system cannot resolve. Missing access is
  itself a finding.
