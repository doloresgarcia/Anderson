#!/usr/bin/env python3
"""PostToolUse hook: cross-check LITERATURE.md citations against references.bib.

Triggers on Write|Edit. Filters by path: only acts on
reviews/<slug>/phase<N>/outputs/{LITERATURE.md, references.bib}. Parses both
files in the same outputs/ dir; flags any [@key] citation in LITERATURE.md
that is not defined in references.bib. Orphan bib entries are not flagged
(they're often parked references). Exits 2 with a structured stderr message
when dangling keys are found.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

LIT_NAME = "LITERATURE.md"
BIB_NAME = "references.bib"
PATH_RE = re.compile(r"reviews/[^/]+/phase\d+/outputs/(LITERATURE\.md|references\.bib)$")
CITATION_RE = re.compile(r"\[@([A-Za-z0-9_:.\-]+)\]")
BIB_KEY_RE = re.compile(r"^\s*@\w+\s*\{\s*([A-Za-z0-9_:.\-]+)\s*,", re.MULTILINE)


def _exit_ok():
    sys.exit(0)


def _exit_block(message: str, file_path: str = ""):
    payload = {
        "decision": "block",
        "reason": message,
        "file_path": file_path,
    }
    print(json.dumps(payload), file=sys.stderr)
    sys.exit(2)


def _extract_citations(text: str) -> set[str]:
    return set(CITATION_RE.findall(text))


def _extract_bib_keys(text: str) -> set[str]:
    try:
        import bibtexparser  # type: ignore

        parser = bibtexparser.bparser.BibTexParser(common_strings=True, ignore_nonstandard_types=False)
        db = bibtexparser.loads(text, parser=parser)
        keys = {entry.get("ID", "") for entry in db.entries if entry.get("ID")}
        if keys:
            return keys
    except ImportError:
        pass
    except Exception:
        pass
    return set(BIB_KEY_RE.findall(text))


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        _exit_ok()

    tool_name = payload.get("tool_name") or payload.get("toolName") or ""
    if tool_name not in ("Write", "Edit", "MultiEdit"):
        _exit_ok()

    tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
    file_path = tool_input.get("file_path") or tool_input.get("filePath") or ""
    if not file_path or not PATH_RE.search(file_path):
        _exit_ok()

    outputs_dir = Path(file_path).parent
    lit_path = outputs_dir / LIT_NAME
    bib_path = outputs_dir / BIB_NAME

    if not lit_path.exists():
        print(f"validate_bib: {lit_path} not present yet; skipping consistency check", file=sys.stderr)
        _exit_ok()

    try:
        lit_text = lit_path.read_text()
    except Exception:
        _exit_ok()

    citations = _extract_citations(lit_text)
    if not citations:
        _exit_ok()

    if not bib_path.exists():
        msg = (
            f"{lit_path.name} cites {len(citations)} key(s) but {bib_path.name} does not exist. "
            f"Every [@key] in LITERATURE.md must resolve to an entry in references.bib. "
            f"Missing keys: {sorted(citations)}"
        )
        _exit_block(msg, file_path)

    try:
        bib_text = bib_path.read_text()
    except Exception:
        _exit_ok()

    bib_keys = _extract_bib_keys(bib_text)
    dangling = sorted(citations - bib_keys)
    if dangling:
        msg = (
            f"{lit_path.name} cites {len(dangling)} key(s) not defined in {bib_path.name}: {dangling}. "
            f"Add bib entries (with DOI/arXiv ID resolvable to a real record) before proceeding. "
            f"LLM-fabricated citations are this pipeline's #1 failure mode."
        )
        _exit_block(msg, file_path)

    _exit_ok()


if __name__ == "__main__":
    main()
