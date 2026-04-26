#!/usr/bin/env python3
"""Aggregate Anderson subagent token usage from saved transcripts.

This is a post-hoc reporter. It reads `usage.jsonl` records that the
SubagentStop hook (`.claude/hooks/usage_log.py`, Phase D) appends under
`reviews/<slug>/phase<N>/agents/<role>/usage.jsonl`, then opens the
referenced subagent transcript JSONL files (under
`~/.claude/projects/<project>/<sessionId>/subagents/agent-<agentId>.jsonl`)
and sums the `usage` fields on assistant messages.

Usage:
    python3 src/token_log.py reviews/<slug>            # write USAGE.md
    python3 src/token_log.py reviews/<slug> --json     # also write USAGE.json
    python3 src/token_log.py --review reviews/<slug>   # alternate flag form

Behavior:
  * If no usage.jsonl records exist anywhere in the review tree, write a
    single USAGE.md noting "no usage recorded for this review yet" and
    exit 0.
  * If a transcript file is missing for a record, count its dispatch
    duration but record zero tokens, and list the dispatch under
    "missing transcripts".

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Token counting
# ---------------------------------------------------------------------------

TOKEN_FIELDS = (
    "input_tokens",
    "output_tokens",
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
)


def _empty_tokens() -> Dict[str, int]:
    return {k: 0 for k in TOKEN_FIELDS}


def _add_tokens(into: Dict[str, int], src: Dict[str, Any]) -> None:
    for k in TOKEN_FIELDS:
        v = src.get(k)
        if isinstance(v, (int, float)):
            into[k] += int(v)


def _extract_usage(line: str) -> Optional[Dict[str, Any]]:
    """Return the `usage` dict on an assistant API response line, or None."""
    line = line.strip()
    if not line:
        return None
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None
    # Claude Code transcripts wrap the API response under `message`.
    msg = obj.get("message")
    if isinstance(msg, dict) and isinstance(msg.get("usage"), dict):
        return msg["usage"]
    # Defensive: some lines store usage at the top level.
    if isinstance(obj.get("usage"), dict):
        return obj["usage"]
    return None


def sum_transcript_tokens(transcript_path: Path) -> Dict[str, int]:
    totals = _empty_tokens()
    try:
        with transcript_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                u = _extract_usage(line)
                if u is not None:
                    _add_tokens(totals, u)
    except OSError:
        # Caller decides how to report missing/unreadable transcripts.
        raise
    return totals


# ---------------------------------------------------------------------------
# Loading dispatch records
# ---------------------------------------------------------------------------

def _expand(p: str) -> Path:
    return Path(os.path.expanduser(os.path.expandvars(p)))


def iter_usage_records(review_dir: Path) -> Iterable[Tuple[int, str, Dict[str, Any]]]:
    """Yield (phase, role, record) for every line in every usage.jsonl."""
    for phase in (1, 2, 3):
        agents_root = review_dir / f"phase{phase}" / "agents"
        if not agents_root.is_dir():
            continue
        for role_dir in sorted(agents_root.iterdir()):
            if not role_dir.is_dir():
                continue
            log = role_dir / "usage.jsonl"
            if not log.is_file():
                continue
            with log.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if not isinstance(rec, dict):
                        continue
                    yield phase, role_dir.name, rec


def _duration_seconds(rec: Dict[str, Any]) -> float:
    for k in ("duration_seconds", "duration_s", "duration"):
        v = rec.get(k)
        if isinstance(v, (int, float)):
            return float(v)
    start = rec.get("start_time") or rec.get("started_at")
    end = rec.get("end_time") or rec.get("ended_at") or rec.get("stopped_at")
    if isinstance(start, (int, float)) and isinstance(end, (int, float)):
        return float(end) - float(start)
    return 0.0


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

class Aggregate:
    def __init__(self) -> None:
        self.tokens = _empty_tokens()
        self.duration_s = 0.0
        self.dispatches = 0

    def add(self, tokens: Dict[str, int], duration_s: float) -> None:
        for k in TOKEN_FIELDS:
            self.tokens[k] += tokens.get(k, 0)
        self.duration_s += duration_s
        self.dispatches += 1

    def to_dict(self) -> Dict[str, Any]:
        d = dict(self.tokens)
        d["duration_s"] = round(self.duration_s, 2)
        d["dispatches"] = self.dispatches
        return d


def build_report(review_dir: Path) -> Dict[str, Any]:
    overall = Aggregate()
    by_phase: Dict[int, Aggregate] = {}
    by_agent: Dict[Tuple[int, str], Aggregate] = {}
    rows: List[Dict[str, Any]] = []
    missing: List[Dict[str, Any]] = []

    for phase, role, rec in iter_usage_records(review_dir):
        duration_s = _duration_seconds(rec)
        # Prefer agent_transcript_path (the subagent's own transcript) per
        # Claude Code SubagentStop hook docs. Fall back to transcript_path
        # only when older usage_log records don't carry the agent path.
        # transcript_path is the main session transcript; reading it would
        # over-count main-session tokens against the subagent.
        agent_transcript = rec.get("agent_transcript_path") or rec.get("agentTranscriptPath")
        main_transcript = rec.get("transcript_path") or rec.get("transcriptPath")
        transcript = agent_transcript or main_transcript
        tokens = _empty_tokens()
        transcript_status = "ok"
        if not transcript:
            transcript_status = "missing-field"
        else:
            tpath = _expand(transcript)
            if not tpath.is_file():
                transcript_status = "missing-file"
            else:
                try:
                    tokens = sum_transcript_tokens(tpath)
                except OSError:
                    transcript_status = "unreadable"

        overall.add(tokens, duration_s)
        by_phase.setdefault(phase, Aggregate()).add(tokens, duration_s)
        by_agent.setdefault((phase, role), Aggregate()).add(tokens, duration_s)

        row = {
            "phase": phase,
            "role": role,
            "agent_id": rec.get("agent_id"),
            "session_id": rec.get("session_id"),
            "agent_transcript_path": agent_transcript,
            "main_transcript_path": main_transcript,
            "transcript_path": transcript,
            "transcript_status": transcript_status,
            "duration_s": round(duration_s, 2),
            **tokens,
        }
        rows.append(row)
        if transcript_status != "ok":
            missing.append({
                "phase": phase,
                "role": role,
                "agent_id": rec.get("agent_id"),
                "agent_transcript_path": agent_transcript,
                "main_transcript_path": main_transcript,
                "transcript_path": transcript,
                "status": transcript_status,
            })

    return {
        "review": str(review_dir),
        "overall": overall.to_dict(),
        "by_phase": {p: a.to_dict() for p, a in sorted(by_phase.items())},
        "by_agent": {
            f"phase{p}/{role}": a.to_dict()
            for (p, role), a in sorted(by_agent.items())
        },
        "dispatches": rows,
        "missing_transcripts": missing,
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _fmt_int(n: int) -> str:
    return f"{n:,}"


def _fmt_dur(seconds: float) -> str:
    s = int(round(seconds))
    if s < 60:
        return f"{s}s"
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m}m{s:02d}s"
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m{s:02d}s"


def render_md(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(f"# Token usage — {report['review']}")
    lines.append("")

    overall = report["overall"]
    lines.append("## Headline")
    lines.append("")
    lines.append(f"- Dispatches: **{overall['dispatches']}**")
    lines.append(f"- Wall-clock (sum of dispatches): **{_fmt_dur(overall['duration_s'])}**")
    lines.append(f"- Input tokens: **{_fmt_int(overall['input_tokens'])}**")
    lines.append(f"- Output tokens: **{_fmt_int(overall['output_tokens'])}**")
    lines.append(f"- Cache read tokens: **{_fmt_int(overall['cache_read_input_tokens'])}**")
    lines.append(f"- Cache creation tokens: **{_fmt_int(overall['cache_creation_input_tokens'])}**")
    lines.append("")

    # Per-phase
    lines.append("## Per phase")
    lines.append("")
    lines.append("| phase | dispatches | duration | input | output | cache_read | cache_create |")
    lines.append("|------:|-----------:|---------:|------:|-------:|-----------:|-------------:|")
    for phase, a in sorted(report["by_phase"].items()):
        lines.append(
            f"| {phase} | {a['dispatches']} | {_fmt_dur(a['duration_s'])} | "
            f"{_fmt_int(a['input_tokens'])} | {_fmt_int(a['output_tokens'])} | "
            f"{_fmt_int(a['cache_read_input_tokens'])} | {_fmt_int(a['cache_creation_input_tokens'])} |"
        )
    lines.append("")

    # Per agent
    lines.append("## Per agent (sorted by output tokens, desc)")
    lines.append("")
    lines.append("| phase | role | dispatches | duration | input | output | cache_read | cache_create |")
    lines.append("|------:|------|-----------:|---------:|------:|-------:|-----------:|-------------:|")
    agent_rows = []
    for key, a in report["by_agent"].items():
        # key like "phase2/checker_literature"
        phase_str, _, role = key.partition("/")
        phase = int(phase_str.replace("phase", ""))
        agent_rows.append((phase, role, a))
    agent_rows.sort(key=lambda r: r[2]["output_tokens"], reverse=True)
    for phase, role, a in agent_rows:
        lines.append(
            f"| {phase} | `{role}` | {a['dispatches']} | {_fmt_dur(a['duration_s'])} | "
            f"{_fmt_int(a['input_tokens'])} | {_fmt_int(a['output_tokens'])} | "
            f"{_fmt_int(a['cache_read_input_tokens'])} | {_fmt_int(a['cache_creation_input_tokens'])} |"
        )
    lines.append("")

    # Per dispatch
    lines.append("## Per dispatch")
    lines.append("")
    lines.append("| phase | role | agent_id | duration | input | output | cache_read | status |")
    lines.append("|------:|------|----------|---------:|------:|-------:|-----------:|--------|")
    for r in report["dispatches"]:
        agent_id = (r.get("agent_id") or "")[:12]
        lines.append(
            f"| {r['phase']} | `{r['role']}` | `{agent_id}` | {_fmt_dur(r['duration_s'])} | "
            f"{_fmt_int(r['input_tokens'])} | {_fmt_int(r['output_tokens'])} | "
            f"{_fmt_int(r['cache_read_input_tokens'])} | {r['transcript_status']} |"
        )
    lines.append("")

    if report["missing_transcripts"]:
        lines.append("## Missing transcripts")
        lines.append("")
        lines.append("These dispatches contributed duration but no token counts:")
        lines.append("")
        for m in report["missing_transcripts"]:
            tp = m.get("transcript_path") or "(no path recorded)"
            lines.append(
                f"- phase {m['phase']} `{m['role']}` agent `{m.get('agent_id') or '?'}` "
                f"— {m['status']} — `{tp}`"
            )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="token_log",
        description=(
            "Aggregate Anderson subagent token usage from saved transcripts. "
            "Walks reviews/<slug>/phase{1,2,3}/agents/*/usage.jsonl, opens "
            "each referenced transcript, and writes USAGE.md (and optionally "
            "USAGE.json) under the review directory."
        ),
    )
    p.add_argument(
        "review",
        nargs="?",
        help="Path to the review directory, e.g. reviews/my-paper",
    )
    p.add_argument(
        "--review",
        dest="review_flag",
        help="Alternative form: --review reviews/my-paper",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Also write USAGE.json alongside USAGE.md",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    ns = parse_args(list(sys.argv[1:] if argv is None else argv))
    review_str = ns.review or ns.review_flag
    if not review_str:
        print("error: review directory is required (positional or --review)", file=sys.stderr)
        return 2

    review_dir = Path(review_str).resolve()
    if not review_dir.is_dir():
        print(f"error: not a directory: {review_dir}", file=sys.stderr)
        return 2

    # Quick existence check for any usage.jsonl.
    has_any = any(True for _ in iter_usage_records(review_dir))
    out_md = review_dir / "USAGE.md"
    if not has_any:
        out_md.write_text(
            f"# Token usage — {review_dir}\n\n"
            "No usage recorded for this review yet. "
            "The SubagentStop hook (`.claude/hooks/usage_log.py`) writes "
            "`usage.jsonl` records under "
            "`<review>/phase<N>/agents/<role>/`; once subagents have run, "
            "re-run `python3 src/token_log.py <review>` to populate this report.\n",
            encoding="utf-8",
        )
        print(f"wrote {out_md} (no usage records found)")
        return 0

    report = build_report(review_dir)
    out_md.write_text(render_md(report), encoding="utf-8")
    print(f"wrote {out_md}")

    if ns.json:
        out_json = review_dir / "USAGE.json"
        out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
