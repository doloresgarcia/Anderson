"""Create a new per-paper review directory tree.

    python src/scaffold_review.py --paper /path/to/paper.pdf --slug my-slug
    python src/scaffold_review.py --text  /path/to/paper.txt --slug my-slug
    python src/scaffold_review.py --arxiv 2401.12345 --slug my-slug
    python src/scaffold_review.py --doi 10.1234/abcde --slug my-slug
    python src/scaffold_review.py --url https://example.com/paper.pdf --slug my-slug

Produces:

    reviews/<slug>/
      CLAUDE.md                       # rendered from src/templates/per_review_claude.md
      prompt.md                       # blank, orchestrator fills first
      paper/
        paper.pdf                     # if --paper given
        paper.txt                     # extracted from PDF, or copied from --text
        paper.meta.json               # stub; user/agent fills
      phase1/  outputs/  agents/  review/  logs/  prompt.md
      phase2/  outputs/  agents/  review/  logs/  prompt.md
      phase3/  outputs/  agents/  review/  logs/  prompt.md

This script does *not* fetch papers from arXiv/DOI/URL. It records the
identifier in `paper/paper.meta.json` and leaves fetching to the orchestrator's
ingest step (which will run inside phase 1's first subagent dispatch). Keeping
fetching out of scaffolding makes the script offline-safe and idempotent.

Reviews are NOT self-contained. There are no per-review symlinks for
methodology, conventions, agents, or the literature bank — those resolve via
the repo (`.claude/agents/`, `src/methodology/`, `src/conventions/`,
`literature_bank/`). The orchestrator at the repo-root `CLAUDE.md` dispatches
subagents with absolute repo-rooted paths.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
TEMPLATES = SRC / "templates"
REVIEWS = REPO_ROOT / "reviews"

PHASES = ("phase1", "phase2", "phase3")
PHASE_SUBDIRS = ("outputs", "agents", "review", "logs")

SLUG_RE = re.compile(r"^(?:__)?[A-Za-z0-9][A-Za-z0-9_-]*(?:__)?$")


def extract_pdf_text(pdf_path: Path, out_path: Path) -> str:
    """Extract text from a PDF with page markers. Returns the backend used.

    Tries PyMuPDF first (preserves layout best, used by highlight_paper.py
    too), falls back to the `pdftotext` system binary, then `pypdf`. Page
    boundaries are marked with `=== PAGE N ===` lines so downstream agents can
    map line numbers back to PDF pages.
    """
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        chunks = []
        for i, page in enumerate(doc, start=1):
            chunks.append(f"=== PAGE {i} ===")
            chunks.append(page.get_text())
        doc.close()
        out_path.write_text("\n".join(chunks))
        return "pymupdf"
    except ImportError:
        pass

    if shutil.which("pdftotext"):
        with subprocess.Popen(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            stdout=subprocess.PIPE,
        ) as proc:
            text, _ = proc.communicate()
        if proc.returncode == 0:
            out_path.write_text(text.decode("utf-8", errors="replace"))
            return "pdftotext"

    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        chunks = []
        for i, page in enumerate(reader.pages, start=1):
            chunks.append(f"=== PAGE {i} ===")
            chunks.append(page.extract_text() or "")
        out_path.write_text("\n".join(chunks))
        return "pypdf"
    except ImportError:
        pass

    raise RuntimeError(
        "no PDF text extractor available. Install one of:\n"
        "  pip install pymupdf      (recommended, also used by highlight_paper.py)\n"
        "  apt install poppler-utils  (provides pdftotext)\n"
        "  pip install pypdf"
    )


def render_template(template_path: Path, slots: dict[str, str]) -> str:
    text = template_path.read_text()
    for key, value in slots.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def make_meta(args: argparse.Namespace) -> dict:
    meta: dict = {
        "slug": args.slug,
        "title": None,
        "authors": None,
        "year": None,
        "venue": None,
        "doi": args.doi,
        "arxiv": args.arxiv,
        "url": args.url,
        "source_pdf": str(args.paper) if args.paper else None,
        "source_text": str(args.text) if args.text else None,
    }
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--paper", type=Path, help="path to a local PDF")
    src.add_argument("--text", type=Path, help="path to a plain-text paper (skips PDF extraction)")
    src.add_argument("--arxiv", help="arXiv ID, e.g. 2401.12345")
    src.add_argument("--doi", help="DOI, e.g. 10.1234/abcde")
    src.add_argument("--url", help="URL to a PDF or paper landing page")
    parser.add_argument("--slug", required=True, help="short identifier, becomes reviews/<slug>/")
    parser.add_argument("--bib", type=Path, help="optional seed bibliography")
    parser.add_argument("--force", action="store_true", help="overwrite existing reviews/<slug>/")
    args = parser.parse_args()

    if not SLUG_RE.match(args.slug):
        print(
            f"error: invalid --slug {args.slug!r}; must match {SLUG_RE.pattern} "
            "(letters/digits/_/-, optional surrounding __ for scratch slugs; "
            "no path separators or '..')",
            file=sys.stderr,
        )
        return 2

    review_dir = (REVIEWS / args.slug).resolve()
    if review_dir.parent != REVIEWS.resolve():
        print(
            f"error: --slug {args.slug!r} resolves outside reviews/ "
            f"({review_dir}); refusing",
            file=sys.stderr,
        )
        return 2

    if review_dir.exists():
        if not args.force:
            print(f"error: {review_dir} exists; pass --force to overwrite", file=sys.stderr)
            return 2
        shutil.rmtree(review_dir)

    review_dir.mkdir(parents=True)
    (review_dir / "paper").mkdir()
    for phase in PHASES:
        for sub in PHASE_SUBDIRS:
            (review_dir / phase / sub).mkdir(parents=True)
        (review_dir / phase / "prompt.md").write_text("")

    slots = {"paper_slug": args.slug}
    (review_dir / "CLAUDE.md").write_text(
        render_template(TEMPLATES / "per_review_claude.md", slots)
    )

    (review_dir / "paper" / "paper.meta.json").write_text(
        json.dumps(make_meta(args), indent=2) + "\n"
    )

    if args.paper is not None:
        if not args.paper.exists():
            print(f"warning: --paper {args.paper} does not exist; copy skipped", file=sys.stderr)
        else:
            paper_pdf = review_dir / "paper" / "paper.pdf"
            shutil.copy(args.paper, paper_pdf)
            try:
                backend = extract_pdf_text(paper_pdf, review_dir / "paper" / "paper.txt")
                print(f"extracted paper.txt via {backend}")
            except RuntimeError as e:
                print(f"warning: paper.txt not produced: {e}", file=sys.stderr)
                print("  (orchestrator will need to extract it as a phase-1 step.)", file=sys.stderr)

    if args.text is not None:
        if not args.text.exists():
            print(f"warning: --text {args.text} does not exist; copy skipped", file=sys.stderr)
        else:
            shutil.copy(args.text, review_dir / "paper" / "paper.txt")
            print("copied paper.txt directly (no PDF; phase 3 will produce paper.highlighted.html)")

    if args.bib is not None:
        if not args.bib.exists():
            print(f"warning: --bib {args.bib} does not exist; copy skipped", file=sys.stderr)
        else:
            shutil.copy(args.bib, review_dir / "paper" / "seed.bib")

    (review_dir / "prompt.md").write_text("")

    print(f"scaffolded {review_dir}")
    print("next: from the repo root, run `claude` and dispatch `/phase1 " + args.slug + "`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
