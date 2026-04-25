#!/usr/bin/env python3
"""SubagentStop hook: append a per-dispatch usage record.

Records dispatch metadata to a JSONL file the orchestrator and `src/token_log.py`
later read. SubagentStop has no documented token-count fields, so this hook
only records routing info (transcript_path is the load-bearing field —
src/token_log.py post-hoc reads the transcript JSONL for token sums).

NEVER blocks. NEVER raises. Always exits 0. Runs on every SubagentStop in
the project, including ones unrelated to Anderson reviews.

Routing heuristic:
  1. If cwd matches reviews/<slug>/phase<N>/..., write to that review's
     phase<N>/agents/<role>/usage.jsonl.
  2. Else if cwd matches the repo root, attempt to infer the active slug
     from the most recent commit message tagged [<slug>] (best effort).
  3. Fallback: .claude/agent-memory/_global/usage.jsonl.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

CWD_REVIEW_RE = re.compile(r"(.+/reviews/([^/]+))(?:/(phase(\d+))(?:/.*)?)?$")
PHASE_DIR_RE = re.compile(r"^phase(\d+)$")
RECENCY_WINDOW_S = 600  # 10 minutes


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _project_dir() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parent.parent.parent


def _infer_slug_phase_from_recent_commit(project_dir: Path) -> tuple[str | None, int | None]:
    try:
        out = subprocess.run(
            ["git", "-C", str(project_dir), "log", "-20", "--pretty=%s"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        if out.returncode != 0:
            return None, None
        for line in out.stdout.splitlines():
            m = re.match(r"phase(\d+)\([^)]*\):.*\[([^\]]+)\]", line)
            if m:
                return m.group(2), int(m.group(1))
    except Exception:
        pass
    return None, None


def _infer_slug_phase_from_recent_activity(project_dir: Path) -> tuple[str | None, int | None]:
    """Find the reviews/<slug>/phase<N>/ dir with the most recent file mtime
    within RECENCY_WINDOW_S seconds. Works for fresh slugs that have no
    phase-tagged commits yet — covers the gap _infer_..._from_recent_commit
    misses on the first dispatch of a new review."""
    reviews_root = project_dir / "reviews"
    if not reviews_root.exists():
        return None, None
    now = time.time()
    best: tuple[float, str, int] | None = None
    try:
        for slug_dir in reviews_root.iterdir():
            if not slug_dir.is_dir() or slug_dir.name.startswith("."):
                continue
            for phase_dir in slug_dir.iterdir():
                if not phase_dir.is_dir():
                    continue
                m = PHASE_DIR_RE.match(phase_dir.name)
                if not m:
                    continue
                phase_num = int(m.group(1))
                # Walk a few levels deep for the freshest mtime; cap depth
                # to keep this hook fast.
                phase_mtime = phase_dir.stat().st_mtime
                for entry in phase_dir.rglob("*"):
                    try:
                        mt = entry.stat().st_mtime
                        if mt > phase_mtime:
                            phase_mtime = mt
                    except Exception:
                        continue
                if now - phase_mtime > RECENCY_WINDOW_S:
                    continue
                if best is None or phase_mtime > best[0]:
                    best = (phase_mtime, slug_dir.name, phase_num)
    except Exception:
        return None, None
    if best is None:
        return None, None
    return best[1], best[2]


def _resolve_target(cwd: str, agent_type: str, project_dir: Path) -> Path:
    review_dir = None
    phase_num = None
    slug = None

    m = CWD_REVIEW_RE.match(cwd or "")
    if m:
        review_dir = Path(m.group(1))
        slug = m.group(2)
        if m.group(4):
            phase_num = int(m.group(4))

    if review_dir is None or phase_num is None:
        slug2, phase2 = _infer_slug_phase_from_recent_activity(project_dir)
        if slug2 and phase2:
            review_dir = project_dir / "reviews" / slug2
            slug = slug2
            phase_num = phase2

    if review_dir is None or phase_num is None:
        slug3, phase3 = _infer_slug_phase_from_recent_commit(project_dir)
        if slug3:
            review_dir = project_dir / "reviews" / slug3
            slug = slug3
            phase_num = phase3

    if review_dir is None or phase_num is None:
        global_dir = project_dir / ".claude" / "agent-memory" / "_global"
        try:
            global_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            return Path("/tmp/anderson_usage_global.jsonl")
        return global_dir / "usage.jsonl"

    role = agent_type or "unknown_agent"
    target_dir = review_dir / f"phase{phase_num}" / "agents" / role
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        return Path("/tmp/anderson_usage_global.jsonl")
    return target_dir / "usage.jsonl"


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    record = {
        "timestamp": _now_iso(),
        "agent_type": payload.get("agent_type") or payload.get("agentType") or "",
        "agent_id": payload.get("agent_id") or payload.get("agentId") or "",
        "session_id": payload.get("session_id") or payload.get("sessionId") or "",
        "transcript_path": payload.get("transcript_path") or payload.get("transcriptPath") or "",
        "cwd": payload.get("cwd") or "",
    }

    project_dir = _project_dir()
    try:
        target = _resolve_target(record["cwd"], record["agent_type"], project_dir)
        with open(target, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
