# literature_searcher — memory

Lessons learned across reviews. The Anderson harness auto-injects this file
into your system prompt every dispatch. Append only — do not delete past
entries. Frame each lesson as "When you see X, prefer Y because Z."

## Backends

- Always search `literature_bank/` (PDFs at the repo root) BEFORE any
  external search. Tag bank matches with `source: bank` in LITERATURE.md.
- For external search, prefer DOI- or arXiv-resolvable records over web
  results. Bias toward peer-reviewed published work over preprints.
- LLM-fabricated citations are this pipeline's #1 failure mode. Every
  bibtex key in references.bib must come from a real, retrievable record.

## Domain notes

(Append `### <domain>` subheadings as you encounter new domains.)
