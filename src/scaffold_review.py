"""Create a new per-paper review directory tree.

    python src/scaffold_review.py --paper /path/to/paper.pdf --slug my-slug
    python src/scaffold_review.py --arxiv 2401.12345 --slug my-slug
    python src/scaffold_review.py --doi 10.1234/abcde --slug my-slug

Produces:

    reviews/<slug>/
      CLAUDE.md                       # rendered from templates/root_claude.md
      prompt.md                       # blank, orchestrator fills first
      methodology -> ../../src/methodology
      conventions -> ../../src/conventions
      agents      -> ../../src/agents
      paper/
        paper.pdf                     # if --paper given
        paper.meta.json               # stub; user/agent fills
      phase1/
        CLAUDE.md
        outputs/  agents/  review/  logs/
      phase2/
        CLAUDE.md
        outputs/  agents/  review/  logs/
      phase3/
        CLAUDE.md
        outputs/  agents/  review/  logs/

This script does *not* fetch papers from arXiv/DOI/URL. It records the
identifier in `paper/paper.meta.json` and leaves fetching to the orchestrator's
ingest step (which will run inside phase 1's first subagent dispatch). Keeping
fetching out of scaffolding makes the script offline-safe and idempotent.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
TEMPLATES = SRC / "templates"
REVIEWS = REPO_ROOT / "reviews"

PHASES = ("phase1", "phase2", "phase3")
PHASE_SUBDIRS = ("outputs", "agents", "review", "logs")


def render_template(template_path: Path, slots: dict[str, str]) -> str:
    text = template_path.read_text()
    for key, value in slots.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def ensure_symlink(link: Path, target: Path) -> None:
    if link.is_symlink() or link.exists():
        if link.is_symlink() and Path(link.readlink()) == target:
            return
        raise SystemExit(f"refusing to overwrite existing path: {link}")
    link.symlink_to(target)


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
    }
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--paper", type=Path, help="path to a local PDF")
    src.add_argument("--arxiv", help="arXiv ID, e.g. 2401.12345")
    src.add_argument("--doi", help="DOI, e.g. 10.1234/abcde")
    src.add_argument("--url", help="URL to a PDF or paper landing page")
    parser.add_argument("--slug", required=True, help="short identifier, becomes reviews/<slug>/")
    parser.add_argument("--bib", type=Path, help="optional seed bibliography")
    parser.add_argument("--force", action="store_true", help="overwrite existing reviews/<slug>/")
    args = parser.parse_args()

    review_dir = REVIEWS / args.slug
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

    ensure_symlink(review_dir / "methodology", (SRC / "methodology").resolve())
    ensure_symlink(review_dir / "conventions", (SRC / "conventions").resolve())
    ensure_symlink(review_dir / "agents", (SRC / "agents").resolve())

    slots = {"paper_slug": args.slug}
    (review_dir / "CLAUDE.md").write_text(
        render_template(TEMPLATES / "root_claude.md", slots)
    )
    for i, phase in enumerate(PHASES, start=1):
        slots_phase = dict(slots, phase=str(i))
        (review_dir / phase / "CLAUDE.md").write_text(
            render_template(TEMPLATES / f"{phase}_claude.md", slots_phase)
        )

    (review_dir / "paper" / "paper.meta.json").write_text(
        json.dumps(make_meta(args), indent=2) + "\n"
    )

    if args.paper is not None:
        if not args.paper.exists():
            print(f"warning: --paper {args.paper} does not exist; copy skipped", file=sys.stderr)
        else:
            shutil.copy(args.paper, review_dir / "paper" / "paper.pdf")

    if args.bib is not None:
        if not args.bib.exists():
            print(f"warning: --bib {args.bib} does not exist; copy skipped", file=sys.stderr)
        else:
            shutil.copy(args.bib, review_dir / "paper" / "seed.bib")

    literature_bank = REPO_ROOT / "literature_bank"
    if literature_bank.is_dir():
        ensure_symlink(review_dir / "literature_bank", literature_bank.resolve())
    else:
        print("warning: literature_bank/ not found at repo root; bank search will be skipped",
              file=sys.stderr)

    (review_dir / "prompt.md").write_text("")

    print(f"scaffolded {review_dir}")
    print("next: cd into it and start the orchestrator with that dir as the working dir")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
