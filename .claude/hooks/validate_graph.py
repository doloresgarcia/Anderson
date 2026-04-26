#!/usr/bin/env python3
"""PostToolUse hook: validate Anderson graph JSON files against the schema.

Triggers on Write|Edit. Filters by file path: only acts on
reviews/<slug>/phase<N>/outputs/graph*.json. Validates against
src/conventions/graph_schema.json. Exits 2 with a structured stderr message
on failure so the harness surfaces it back to the agent for self-correction.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

GRAPH_PATH_RE = re.compile(r"reviews/[^/]+/phase\d+/outputs/graph[^/]*\.json$")
PALETTE_BY_VERDICT = {
    "CLEAR": "#2ECC71",
    "FLAGGED": "#E74C3C",
    "INCONCLUSIVE": "#F1C40F",
    "NOT_CHECKED": "#95A5A6",
}
CATEGORY_COLORS = {
    "unreferenced": "#4285F4",
    "ambiguous": "#FFBF00",
    "internal_contradiction": "#FF6D00",
    "literature_collision": "#D32F2F",
    "domain_violation": "#7B1FA2",
}
CATEGORY_SEVERITY = (
    "domain_violation",
    "literature_collision",
    "internal_contradiction",
    "ambiguous",
    "unreferenced",
)
PROVENANCE_PLACEHOLDER_VALUES = {"", "?", "unknown", "null", "none", "n/a", "na"}


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


def _present(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() not in PROVENANCE_PLACEHOLDER_VALUES
    return True


def _has_node_provenance(node: dict) -> bool:
    provenance = node.get("provenance")
    if _present(provenance):
        return True

    evidence = node.get("evidence")
    if isinstance(evidence, list) and any(_present(item) for item in evidence):
        return True
    if isinstance(evidence, str) and _present(evidence):
        return True

    # Older graph files carry provenance as page/line coordinates rather than
    # a literal "provenance" field. A paper.txt line is enough to anchor a node.
    return _present(node.get("line"))


def _flagged_categories(node: dict) -> list[str]:
    categories = node.get("flagged_categories")
    if not isinstance(categories, list):
        return []
    return [str(cat) for cat in categories if str(cat)]


def _most_severe_category(categories: list[str]) -> str | None:
    category_set = set(categories)
    for category in CATEGORY_SEVERITY:
        if category in category_set:
            return category
    return None


def _aggregate_group_verdict(child_verdicts: list[str]) -> str | None:
    if not child_verdicts:
        return None
    if any(v == "FLAGGED" for v in child_verdicts):
        return "FLAGGED"
    if any(v == "INCONCLUSIVE" for v in child_verdicts):
        return "INCONCLUSIVE"
    if all(v == "CLEAR" for v in child_verdicts):
        return "CLEAR"
    if any(v in PALETTE_BY_VERDICT for v in child_verdicts):
        return "NOT_CHECKED"
    return None


def _expected_color_for_node(node: dict, derived_categories: list[str] | None = None) -> tuple[str | None, str]:
    verdict = node.get("verdict")
    if verdict is None:
        return None, "missing verdict"
    if verdict not in PALETTE_BY_VERDICT:
        return None, f"unsupported verdict {verdict!r}"

    if verdict == "FLAGGED":
        categories = derived_categories if derived_categories is not None else _flagged_categories(node)
        unknown = sorted(set(categories) - set(CATEGORY_COLORS))
        if unknown:
            return None, f"unknown flagged_categories {unknown!r}"
        category = _most_severe_category(categories)
        if category:
            return CATEGORY_COLORS[category], f"most-severe flagged category {category!r}"

    return PALETTE_BY_VERDICT[verdict], f"verdict {verdict!r}"


def _validate_color(
    node: dict,
    label: str,
    errors: list[str],
    derived_categories: list[str] | None = None,
) -> None:
    verdict = node.get("verdict")
    color = node.get("color")
    if verdict is None and color is None:
        return
    expected, source = _expected_color_for_node(node, derived_categories)
    if expected is None:
        errors.append(f"{label} has {source}")
        return
    if color != expected:
        errors.append(f"{label} color {color!r} does not match {source}; expected {expected}")


def _validate_graph_rules(doc: dict) -> list[str]:
    errors: list[str] = []
    groups = doc.get("groups") or []
    claims = doc.get("claims") or []
    edges = doc.get("edges") or []

    if len(groups) > 20:
        errors.append(f"graph has {len(groups)} groups; maximum is 20")

    group_by_id = {group.get("id"): group for group in groups if isinstance(group, dict)}
    claim_by_id = {claim.get("id"): claim for claim in claims if isinstance(claim, dict)}

    for group in groups:
        if not isinstance(group, dict):
            continue
        group_id = group.get("id", "<missing group id>")
        claim_ids = group.get("claim_ids") or []
        if not isinstance(claim_ids, list):
            continue
        if not 1 <= len(claim_ids) <= 15:
            errors.append(f"group {group_id} has {len(claim_ids)} claim_ids; expected 1..15")
        child_claims: list[dict] = []
        for claim_id in claim_ids:
            claim = claim_by_id.get(claim_id)
            if claim is None:
                errors.append(f"group {group_id} claim_ids contains unresolved claim {claim_id!r}")
            elif claim.get("parent") != group_id:
                errors.append(
                    f"group {group_id} claim_ids contains {claim_id}, but that claim parent is {claim.get('parent')!r}"
                )
            else:
                child_claims.append(claim)
        child_verdicts = [claim["verdict"] for claim in child_claims if claim.get("verdict") in PALETTE_BY_VERDICT]
        expected_verdict = _aggregate_group_verdict(child_verdicts)
        if expected_verdict and group.get("verdict") and group.get("verdict") != expected_verdict:
            errors.append(
                f"group {group_id} verdict {group.get('verdict')!r} does not match child aggregate "
                f"{expected_verdict!r}"
            )
        derived_categories = [
            category
            for claim in child_claims
            for category in _flagged_categories(claim)
        ]
        _validate_color(group, f"group {group_id}", errors, derived_categories)

    for claim in claims:
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("id", "<missing claim id>")
        parent = claim.get("parent")
        parent_group = group_by_id.get(parent)
        if parent_group is None:
            errors.append(f"claim {claim_id} parent {parent!r} does not resolve to a group")
        else:
            claim_ids = parent_group.get("claim_ids") or []
            if isinstance(claim_ids, list) and claim_id not in claim_ids:
                errors.append(f"claim {claim_id} parent is {parent}, but {parent}.claim_ids does not include it")

        confidence = claim.get("confidence")
        if not _has_node_provenance(claim) and confidence not in ("low", "medium"):
            errors.append(
                f"claim {claim_id} lacks provenance/evidence and confidence is {confidence!r}; "
                "nodes without provenance must have confidence low or medium"
            )
        if claim.get("verdict") != "FLAGGED" and _flagged_categories(claim):
            errors.append(f"claim {claim_id} has flagged_categories but verdict is {claim.get('verdict')!r}")
        _validate_color(claim, f"claim {claim_id}", errors)

    for edge in edges:
        if not isinstance(edge, dict):
            continue
        edge_id = edge.get("id", "<missing edge id>")
        source = edge.get("source")
        target = edge.get("target")
        if source not in claim_by_id:
            errors.append(f"edge {edge_id} source {source!r} does not resolve to a claim")
        if target not in claim_by_id:
            errors.append(f"edge {edge_id} target {target!r} does not resolve to a claim")
        if source == target:
            errors.append(f"edge {edge_id} has identical source and target {source!r}")
        provenance = edge.get("provenance")
        if (
            edge.get("kind") == "contradicts"
            and edge.get("confidence") == "low"
            and isinstance(provenance, str)
            and provenance.strip().lower() == "inferred"
        ):
            errors.append(
                f"edge {edge_id} is a low-confidence inferred contradiction; "
                "add a paper anchor with higher confidence or drop the edge"
            )

    return errors


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
    if not file_path:
        _exit_ok()

    if not GRAPH_PATH_RE.search(file_path):
        _exit_ok()

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or str(Path(__file__).resolve().parent.parent.parent)
    schema_path = Path(project_dir) / "src" / "conventions" / "graph_schema.json"
    if not schema_path.exists():
        print(f"validate_graph: schema missing at {schema_path}", file=sys.stderr)
        _exit_ok()

    try:
        import jsonschema  # type: ignore
    except ImportError:
        print("validate_graph: jsonschema not installed; skipping (run pip install -r requirements.txt)", file=sys.stderr)
        _exit_ok()

    try:
        with open(file_path, "r") as f:
            doc = json.load(f)
    except FileNotFoundError:
        _exit_ok()
    except json.JSONDecodeError as e:
        _exit_block(f"graph file is not valid JSON: {e}", file_path)

    try:
        with open(schema_path, "r") as f:
            schema = json.load(f)
    except Exception as e:
        print(f"validate_graph: failed to load schema: {e}", file=sys.stderr)
        _exit_ok()

    try:
        jsonschema.validate(doc, schema)
    except jsonschema.ValidationError as e:
        path = ".".join(str(p) for p in e.absolute_path) or "<root>"
        msg = (
            f"graph schema violation at {path}: {e.message}. "
            f"Schema: src/conventions/graph_schema.json. "
            f"Prose source: src/conventions/graph_schema.md."
        )
        _exit_block(msg, file_path)
    except jsonschema.SchemaError as e:
        print(f"validate_graph: schema is itself invalid: {e}", file=sys.stderr)
        _exit_ok()

    prose_errors = _validate_graph_rules(doc)
    if prose_errors:
        shown = prose_errors[:12]
        more = "" if len(prose_errors) <= len(shown) else f" (+{len(prose_errors) - len(shown)} more)"
        msg = (
            "graph schema prose-rule violation(s): "
            + "; ".join(shown)
            + more
            + ". Prose source: src/conventions/graph_schema.md."
        )
        _exit_block(msg, file_path)

    _exit_ok()


if __name__ == "__main__":
    main()
