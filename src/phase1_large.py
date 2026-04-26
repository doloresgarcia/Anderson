#!/usr/bin/env python3
"""Deterministic helpers for large-paper Phase 1 shard outputs.

This script does no LLM work. It validates and assembles mechanical Phase 1
artifacts that are awkward to merge by hand when a large paper is split across
claim/literature shards.

Examples:

    python3 src/phase1_large.py validate-claims reviews/foo/phase1/outputs/CLAIMS.md

    python3 src/phase1_large.py validate-citations \
        reviews/foo/phase1/outputs/LITERATURE.md \
        reviews/foo/phase1/outputs/references.bib

    python3 src/phase1_large.py merge-literature \
        --claims reviews/foo/phase1/outputs/CLAIMS.md \
        --literature-out reviews/foo/phase1/outputs/LITERATURE.md \
        --bib-out reviews/foo/phase1/outputs/references.bib \
        --force \
        reviews/foo/phase1/agents/literature_searcher/bank_batches/*

Shard arguments may be directories containing LITERATURE.part.md and
references.part.bib, or either of those files directly. The merge is stable:
claim sections are ordered by CLAIMS.md when provided, otherwise by claim ID;
BibTeX entries are deduped by DOI, arXiv/eprint, normalized title, then key.
Local citation keys are rewritten to the selected final keys.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


CLAIM_ID_RE = re.compile(r"^C\d{3,}$")
CLAIMS_ROW_RE = re.compile(r"^\s*\|\s*(C\d+)\s*\|")
LITERATURE_HEADING_RE = re.compile(r"^(##)\s+(C\d+)\b.*$")
BRACKET_CITATION_RE = re.compile(r"\[([^\[\]]*@[^][]*)\]")
CITATION_KEY_RE = re.compile(r"(?<![\w@])@([A-Za-z0-9_:.\-]+)")
BIB_ENTRY_START_RE = re.compile(
    r"(?m)^[ \t]*@([A-Za-z][A-Za-z0-9_-]*)\s*([({])\s*([^,\s]+)\s*,"
)
AUTHOR_YEAR_RE = re.compile(
    r"(?is)author\s*=\s*[{\"]\s*([^,{}\n\"]+)|year\s*=\s*[{\"]\s*([0-9]{4})"
)

LITERATURE_PART_NAME = "LITERATURE.part.md"
REFERENCES_PART_NAME = "references.part.bib"


class ValidationError(Exception):
    """Raised for deterministic artifact validation failures."""


@dataclass(frozen=True)
class LiteratureSection:
    claim_id: str
    body: str
    path: Path
    line_no: int


@dataclass(frozen=True)
class BibEntry:
    key: str
    text: str
    path: Path


@dataclass(frozen=True)
class FinalBibEntry:
    key: str
    text: str
    source: BibEntry


@dataclass(frozen=True)
class ShardPair:
    literature: Path
    references: Path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValidationError(f"{path} does not exist") from exc
    except OSError as exc:
        raise ValidationError(f"could not read {path}: {exc}") from exc


def claim_sort_key(claim_id: str) -> int:
    return int(claim_id[1:])


def extract_claim_ids_from_claims_md(path: Path) -> list[str]:
    ids: list[str] = []
    invalid: list[str] = []
    seen: dict[str, int] = {}
    duplicate_notes: list[str] = []

    for line_no, line in enumerate(read_text(path).splitlines(), start=1):
        match = CLAIMS_ROW_RE.match(line)
        if not match:
            continue
        claim_id = match.group(1)
        if not CLAIM_ID_RE.match(claim_id):
            invalid.append(f"{path}:{line_no}: {claim_id}")
            continue
        if claim_id in seen:
            duplicate_notes.append(
                f"{claim_id} at lines {seen[claim_id]} and {line_no}"
            )
        else:
            seen[claim_id] = line_no
        ids.append(claim_id)

    if not ids:
        raise ValidationError(f"{path}: no claim IDs found in CLAIMS.md table")
    if invalid:
        raise ValidationError(
            f"{path}: claim IDs must use C001, C002, ... format; invalid: "
            + ", ".join(invalid)
        )
    if duplicate_notes:
        raise ValidationError(f"{path}: duplicate claim IDs: " + "; ".join(duplicate_notes))

    return ids


def validate_claims(path: Path) -> int:
    ids = extract_claim_ids_from_claims_md(path)
    return len(ids)


def extract_citation_keys(text: str) -> list[str]:
    keys: list[str] = []
    for citation_group in BRACKET_CITATION_RE.findall(text):
        keys.extend(CITATION_KEY_RE.findall(citation_group))
    return keys


def extract_unique_citation_keys(text: str) -> set[str]:
    return set(extract_citation_keys(text))


def _find_bib_entry_end(text: str, open_pos: int, open_char: str) -> int:
    close_char = "}" if open_char == "{" else ")"
    depth = 0
    i = open_pos
    while i < len(text):
        char = text[i]
        if char == "\\":
            i += 2
            continue
        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def _normalize_identity_text(value: str) -> str:
    value = re.sub(r"[{}\"\\]", " ", value)
    value = re.sub(r"[^A-Za-z0-9]+", " ", value).strip().lower()
    return re.sub(r"\s+", " ", value)


def _extract_bib_field(entry: str, field_names: Iterable[str]) -> str | None:
    wanted = {name.lower() for name in field_names}
    for match in re.finditer(r"(?im)\b([A-Za-z][A-Za-z0-9_-]*)\s*=", entry):
        if match.group(1).lower() not in wanted:
            continue

        index = match.end()
        while index < len(entry) and entry[index].isspace():
            index += 1
        if index >= len(entry):
            continue

        opener = entry[index]
        if opener == "{":
            start = index + 1
            depth = 1
            index = start
            while index < len(entry):
                char = entry[index]
                if char == "\\":
                    index += 2
                    continue
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        return entry[start:index].strip()
                index += 1
            return None

        if opener == '"':
            start = index + 1
            index = start
            while index < len(entry):
                char = entry[index]
                if char == "\\":
                    index += 2
                    continue
                if char == '"':
                    return entry[start:index].strip()
                index += 1
            return None

        start = index
        while index < len(entry) and entry[index] not in ",\n\r":
            index += 1
        return entry[start:index].strip()

    return None


def _bib_identity(entry: BibEntry) -> tuple[str, str]:
    doi = _extract_bib_field(entry.text, ("doi",))
    if doi:
        return ("doi", _normalize_identity_text(doi))

    arxiv = _extract_bib_field(entry.text, ("arxiv", "eprint"))
    if arxiv:
        return ("arxiv", _normalize_identity_text(arxiv))

    title = _extract_bib_field(entry.text, ("title",))
    if title:
        return ("title", _normalize_identity_text(title))

    return ("key", entry.key)


def _slugify_key(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "", value)
    return value or "ref"


def _generated_bib_key(entry: BibEntry, used: set[str]) -> str:
    author = "ref"
    year = "0000"
    for match in AUTHOR_YEAR_RE.finditer(entry.text):
        if match.group(1):
            author = match.group(1).split()[-1]
        if match.group(2):
            year = match.group(2)

    title = _extract_bib_field(entry.text, ("title",)) or ""
    title_word = ""
    for word in _normalize_identity_text(title).split():
        if len(word) > 3:
            title_word = word
            break

    base = _slugify_key(author.lower() + year + title_word[:12])
    candidate = base
    suffix_ord = ord("a")
    while candidate in used:
        candidate = f"{base}{chr(suffix_ord)}"
        suffix_ord += 1
    return candidate


def _replace_bib_key(entry_text: str, new_key: str) -> str:
    return BIB_ENTRY_START_RE.sub(
        lambda match: f"@{match.group(1)}{match.group(2)}{new_key},",
        entry_text,
        count=1,
    )


def _rewrite_citations(text: str, key_map: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        return "@" + key_map.get(key, key)

    return CITATION_KEY_RE.sub(replace, text)


def parse_bib_entries(path: Path, required: bool = True) -> list[BibEntry]:
    if not path.exists():
        if required:
            raise ValidationError(f"{path} does not exist")
        return []

    text = read_text(path)
    entries: list[BibEntry] = []
    for match in BIB_ENTRY_START_RE.finditer(text):
        open_char = match.group(2)
        open_pos = match.start(2)
        end = _find_bib_entry_end(text, open_pos, open_char)
        if end < 0:
            raise ValidationError(
                f"{path}: BibTeX entry for key {match.group(3)!r} is not closed"
            )
        entries.append(
            BibEntry(
                key=match.group(3).strip(),
                text=text[match.start():end].strip(),
                path=path,
            )
        )
    return entries


def extract_bib_keys(path: Path) -> set[str]:
    return {entry.key for entry in parse_bib_entries(path)}


def validate_citations(literature_path: Path, bib_path: Path) -> tuple[int, int]:
    literature = read_text(literature_path)
    citation_keys = extract_unique_citation_keys(literature)
    bib_entries = parse_bib_entries(bib_path)
    bib_key_counts: dict[str, int] = {}
    for entry in bib_entries:
        bib_key_counts[entry.key] = bib_key_counts.get(entry.key, 0) + 1

    duplicate_keys = sorted(key for key, count in bib_key_counts.items() if count > 1)
    if duplicate_keys:
        raise ValidationError(
            f"{bib_path}: duplicate BibTeX keys: " + ", ".join(duplicate_keys)
        )

    bib_keys = set(bib_key_counts)
    missing = sorted(citation_keys - bib_keys)
    if missing:
        raise ValidationError(
            f"{literature_path}: citations missing from {bib_path}: "
            + ", ".join(missing)
        )
    return len(citation_keys), len(bib_keys)


def parse_literature_sections(path: Path) -> list[LiteratureSection]:
    text = read_text(path)
    lines = text.splitlines()
    sections: list[LiteratureSection] = []
    current_id: str | None = None
    current_line = 0
    body_start = 0

    def finish(until_index: int) -> None:
        if current_id is None:
            return
        body = "\n".join(lines[body_start:until_index]).strip()
        sections.append(
            LiteratureSection(
                claim_id=current_id,
                body=body,
                path=path,
                line_no=current_line,
            )
        )

    for index, line in enumerate(lines):
        match = LITERATURE_HEADING_RE.match(line)
        if not match:
            continue
        claim_id = match.group(2)
        if not CLAIM_ID_RE.match(claim_id):
            raise ValidationError(
                f"{path}:{index + 1}: claim heading must use C001, C002, ... format"
            )
        finish(index)
        current_id = claim_id
        current_line = index + 1
        body_start = index + 1

    finish(len(lines))
    return sections


def collect_shard_pairs(paths: Iterable[Path]) -> list[ShardPair]:
    pairs: OrderedDict[tuple[Path, Path], ShardPair] = OrderedDict()
    errors: list[str] = []

    for raw_path in paths:
        path = raw_path
        if path.is_dir():
            lit = path / LITERATURE_PART_NAME
            bib = path / REFERENCES_PART_NAME
        elif path.name == LITERATURE_PART_NAME:
            lit = path
            bib = path.with_name(REFERENCES_PART_NAME)
        elif path.name == REFERENCES_PART_NAME:
            bib = path
            lit = path.with_name(LITERATURE_PART_NAME)
        else:
            errors.append(
                f"{path}: expected a shard directory, {LITERATURE_PART_NAME}, "
                f"or {REFERENCES_PART_NAME}"
            )
            continue

        if not lit.exists():
            errors.append(f"{lit}: missing literature part")
        key = (lit.resolve(), bib.resolve())
        pairs[key] = ShardPair(literature=lit, references=bib)

    if errors:
        raise ValidationError("; ".join(errors))
    if not pairs:
        raise ValidationError("no shard parts provided")
    return list(pairs.values())


def _pair_stage(pair: ShardPair) -> int:
    path_parts = set(pair.literature.parts) | set(pair.references.parts)
    if "external_batches" in path_parts:
        return 1
    return 0


def _select_final_bib_entries(
    entries_by_pair: dict[tuple[Path, Path], list[BibEntry]],
) -> tuple[OrderedDict[str, FinalBibEntry], dict[tuple[Path, Path], dict[str, str]]]:
    by_identity: OrderedDict[tuple[str, str], list[BibEntry]] = OrderedDict()
    for entries in entries_by_pair.values():
        for entry in entries:
            by_identity.setdefault(_bib_identity(entry), []).append(entry)

    used_final_keys: set[str] = set()
    final_entries: OrderedDict[str, FinalBibEntry] = OrderedDict()
    final_key_by_identity: dict[tuple[str, str], str] = {}

    for identity, entries in by_identity.items():
        canonical = entries[0]
        desired_key = canonical.key
        final_key = desired_key
        if final_key in used_final_keys:
            final_key = _generated_bib_key(canonical, used_final_keys)
        used_final_keys.add(final_key)
        final_key_by_identity[identity] = final_key
        final_entries[final_key] = FinalBibEntry(
            key=final_key,
            text=_replace_bib_key(canonical.text, final_key),
            source=canonical,
        )

    key_maps: dict[tuple[Path, Path], dict[str, str]] = {}
    for pair_key, entries in entries_by_pair.items():
        mapping: dict[str, str] = {}
        for entry in entries:
            identity = _bib_identity(entry)
            final_key = final_key_by_identity[identity]
            existing = mapping.get(entry.key)
            if existing is not None and existing != final_key:
                raise ValidationError(
                    f"{entry.path}: key {entry.key!r} maps to multiple records"
                )
            mapping[entry.key] = final_key
        key_maps[pair_key] = mapping

    return final_entries, key_maps


def render_literature(
    ordered_claim_ids: list[str],
    sections_by_claim: dict[str, list[tuple[int, str, LiteratureSection]]],
    shard_count: int,
) -> str:
    lines = [
        "# LITERATURE",
        "",
        f"Generated by `src/phase1_large.py merge-literature` from {shard_count} shard part(s).",
        "",
    ]
    for claim_id in ordered_claim_ids:
        lines.append(f"## {claim_id}")
        lines.append("")
        body_lines: list[str] = []
        for _, _, section in sorted(
            sections_by_claim.get(claim_id, []),
            key=lambda item: (item[0], item[1], item[2].line_no),
        ):
            body = section.body
            if not body:
                continue
            if body_lines:
                body_lines.append("")
            body_lines.extend(body.splitlines())
        if body_lines:
            lines.extend(body_lines)
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_bib(
    entries_by_key: OrderedDict[str, FinalBibEntry],
    citation_order: list[str],
    shard_count: int,
) -> str:
    emitted: set[str] = set()
    ordered_entries: list[FinalBibEntry] = []

    for key in citation_order:
        if key in entries_by_key and key not in emitted:
            ordered_entries.append(entries_by_key[key])
            emitted.add(key)

    for key, entry in entries_by_key.items():
        if key not in emitted:
            ordered_entries.append(entry)
            emitted.add(key)

    lines = [
        f"% Generated by `src/phase1_large.py merge-literature` from {shard_count} shard part(s).",
        "",
    ]
    for entry in ordered_entries:
        lines.append(entry.text)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_output(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def ensure_outputs_writable(paths: Iterable[Path], force: bool) -> None:
    existing = [path for path in paths if path.exists()]
    if existing and not force:
        raise ValidationError(
            "output file(s) already exist; pass --force to overwrite: "
            + ", ".join(str(path) for path in existing)
        )


def merge_literature(
    shard_paths: list[Path],
    claims_path: Path | None,
    literature_out: Path,
    bib_out: Path,
    force: bool,
) -> tuple[int, int, int]:
    expected_claims = extract_claim_ids_from_claims_md(claims_path) if claims_path else None
    shard_pairs = collect_shard_pairs(shard_paths)

    sections_by_claim: dict[str, list[tuple[int, str, LiteratureSection]]] = {}
    seen_stage_by_claim: dict[str, dict[int, LiteratureSection]] = {}
    entries_by_pair: dict[tuple[Path, Path], list[BibEntry]] = {}
    duplicate_sections: list[str] = []

    parsed_pairs: list[
        tuple[int, int, str, ShardPair, list[LiteratureSection], list[BibEntry]]
    ] = []
    for pair in shard_pairs:
        sections = parse_literature_sections(pair.literature)
        min_claim = min(
            (claim_sort_key(section.claim_id) for section in sections),
            default=sys.maxsize,
        )
        stage = _pair_stage(pair)
        entries = parse_bib_entries(pair.references, required=False)
        parsed_pairs.append((min_claim, stage, str(pair.literature), pair, sections, entries))

    for _, _, _, pair, _, entries in sorted(parsed_pairs):
        entries_by_pair[(pair.literature.resolve(), pair.references.resolve())] = entries

    entries_by_key, citation_key_maps = _select_final_bib_entries(entries_by_pair)

    for _, stage, path_sort, pair, sections, entries in sorted(parsed_pairs):
        pair_key = (pair.literature.resolve(), pair.references.resolve())
        citation_key_map = citation_key_maps.get(pair_key, {})
        for section in sections:
            existing = seen_stage_by_claim.setdefault(section.claim_id, {}).get(stage)
            if existing is not None:
                duplicate_sections.append(
                    f"{section.claim_id} in same merge stage at "
                    f"{existing.path}:{existing.line_no} "
                    f"and {section.path}:{section.line_no}"
                )
                continue
            rewritten = LiteratureSection(
                claim_id=section.claim_id,
                body=_rewrite_citations(section.body, citation_key_map),
                path=section.path,
                line_no=section.line_no,
            )
            seen_stage_by_claim[section.claim_id][stage] = rewritten
            sections_by_claim.setdefault(section.claim_id, []).append(
                (stage, path_sort, rewritten)
            )

    if duplicate_sections:
        raise ValidationError(
            "duplicate literature claim sections: " + "; ".join(duplicate_sections)
        )

    if expected_claims is not None:
        expected_set = set(expected_claims)
        observed_set = set(sections_by_claim)
        unknown = sorted(observed_set - expected_set, key=claim_sort_key)
        if unknown:
            raise ValidationError("unknown sections " + ", ".join(unknown[:10]))
        ordered_claims = expected_claims
    else:
        ordered_claims = sorted(sections_by_claim, key=claim_sort_key)

    literature_text = render_literature(ordered_claims, sections_by_claim, len(shard_pairs))
    citation_order = extract_citation_keys(literature_text)
    missing_bib = sorted(set(citation_order) - set(entries_by_key))
    if missing_bib:
        raise ValidationError(
            "merged literature contains citations missing from shard bib files: "
            + ", ".join(missing_bib)
        )

    bib_text = render_bib(entries_by_key, citation_order, len(shard_pairs))
    ensure_outputs_writable([literature_out, bib_out], force=force)
    write_output(literature_out, literature_text)
    write_output(bib_out, bib_text)

    validate_citations(literature_out, bib_out)
    return len(ordered_claims), len(extract_unique_citation_keys(literature_text)), len(entries_by_key)


def validate_review(review: Path) -> tuple[int, int, int]:
    outputs = review / "phase1" / "outputs"
    claim_count = validate_claims(outputs / "CLAIMS.md")
    citation_count, bib_count = validate_citations(
        outputs / "LITERATURE.md",
        outputs / "references.bib",
    )
    return claim_count, citation_count, bib_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and merge deterministic large-paper Phase 1 shard artifacts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    claims = subparsers.add_parser(
        "validate-claims",
        help="validate CLAIMS.md has valid unique C001-style IDs",
    )
    claims.add_argument("claims_md", type=Path)

    citations = subparsers.add_parser(
        "validate-citations",
        help="validate every [@key] in LITERATURE.md resolves in references.bib",
    )
    citations.add_argument("literature_md", type=Path)
    citations.add_argument("references_bib", type=Path)

    merge = subparsers.add_parser(
        "merge-literature",
        help=f"merge shard {LITERATURE_PART_NAME} and {REFERENCES_PART_NAME} files",
    )
    merge.add_argument(
        "parts",
        nargs="+",
        type=Path,
        help=(
            f"shard directories, {LITERATURE_PART_NAME} files, or "
            f"{REFERENCES_PART_NAME} files"
        ),
    )
    merge.add_argument(
        "--claims",
        type=Path,
        help="CLAIMS.md used to validate coverage and set final claim order",
    )
    merge.add_argument(
        "--literature-out",
        required=True,
        type=Path,
        help="path to write merged LITERATURE.md",
    )
    merge.add_argument(
        "--bib-out",
        required=True,
        type=Path,
        help="path to write merged references.bib",
    )
    merge.add_argument(
        "--force",
        action="store_true",
        help="overwrite output files if they already exist",
    )

    review = subparsers.add_parser(
        "validate-review",
        help="validate phase1/outputs CLAIMS.md, LITERATURE.md, and references.bib",
    )
    review.add_argument("review", type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "validate-claims":
            count = validate_claims(args.claims_md)
            print(f"OK: {args.claims_md} has {count} valid unique claim ID(s)")
        elif args.command == "validate-citations":
            citations, bib_entries = validate_citations(args.literature_md, args.references_bib)
            print(
                f"OK: {args.literature_md} cites {citations} key(s); "
                f"{args.references_bib} defines {bib_entries} key(s)"
            )
        elif args.command == "merge-literature":
            claims, citations, bib_entries = merge_literature(
                shard_paths=args.parts,
                claims_path=args.claims,
                literature_out=args.literature_out,
                bib_out=args.bib_out,
                force=args.force,
            )
            print(
                f"OK: wrote {args.literature_out} and {args.bib_out} "
                f"({claims} claim section(s), {citations} cited key(s), "
                f"{bib_entries} unique bib entry/entries)"
            )
        elif args.command == "validate-review":
            claims, citations, bib_entries = validate_review(args.review)
            print(
                f"OK: {args.review} phase1 outputs validate "
                f"({claims} claims, {citations} cited key(s), {bib_entries} bib entry/entries)"
            )
        else:
            parser.error(f"unknown command {args.command!r}")
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
