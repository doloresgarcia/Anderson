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

    _exit_ok()


if __name__ == "__main__":
    main()
