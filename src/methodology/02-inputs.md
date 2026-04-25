# Inputs

## Accepted forms

A review is launched against exactly one paper, supplied as one of:

- A local PDF: `--paper /path/to/file.pdf`
- An arXiv ID: `--arxiv 2401.12345`
- A DOI: `--doi 10.1234/abcde`
- A URL pointing to a publicly accessible PDF or HTML version

`scaffold_review.py` normalizes these into:

```
reviews/<slug>/
  paper/
    paper.pdf            # canonical PDF
    paper.txt            # extracted plain text, page-numbered
    paper.meta.json      # title, authors, year, venue, DOI/arXiv id
```

`paper.txt` is the artifact agents read for claim extraction. `paper.pdf` is the
artifact phase 3 annotates.

## Optional inputs

- `--bib /path/to/refs.bib` — pre-supplied bibliography to seed the literature search.
- `--corpus <name>` — pointer to a domain corpus the literature searcher should
  prefer (e.g., a local arXiv slice or an MCP-mounted index).

## What is not an input

- Author intent, supplementary material the authors did not publish, or anything
  behind a paywall the system cannot resolve. Missing access is itself a finding.
