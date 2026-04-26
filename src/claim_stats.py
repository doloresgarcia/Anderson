"""Compute claim statistics for a review and emit STATS.md.

    python3 src/claim_stats.py reviews/foo
    # writes reviews/foo/phase3/outputs/STATS.md and prints a one-line summary

Reads:
- reviews/<slug>/phase1/outputs/CLAIMS.md
- reviews/<slug>/phase2/outputs/VERIFICATION.md  (optional)
- reviews/<slug>/phase2/outputs/graph.v2.json    (optional, for group-level rows)

Writes:
- reviews/<slug>/phase3/outputs/STATS.md

The numbers are mechanical — no LLM. STATS.md is data; REPORT.md is prose
written by the report_writer agent that consumes STATS.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from highlight_paper import (  # noqa: E402
    CATEGORIES,
    SEVERITY,
    ClaimsParseError,
    parse_claims_md,
    parse_verification_md,
    trust_score,
    claim_aggregate_verdict,
    flagged_categories,
)

# Closed lists from the conventions, used to keep table row order stable.
CLAIM_TYPES = (
    "result", "method", "prior_work", "background_fact",
    "assumption", "interpretation", "definition", "UNCLASSIFIED",
)
VERDICTS = ("CLEAR", "FLAGGED", "INCONCLUSIVE", "NOT_CHECKED")
CONFIDENCES = ("high", "medium", "low")
# Categories listed in severity order (highest first), matching the report.
CATEGORIES_BY_SEVERITY = SEVERITY


def md_table(rows: list[list[str]], header: list[str]) -> str:
    widths = [max(len(str(r[i])) for r in [header, *rows]) for i in range(len(header))]
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    def fmt(cells):
        return "| " + " | ".join(str(c).ljust(w) for c, w in zip(cells, widths)) + " |"
    return "\n".join([fmt(header), sep, *(fmt(r) for r in rows)])


def stats(claims: dict, verdicts: dict, graph: dict | None) -> dict:
    n = len(claims)

    # By type.
    type_counts = Counter(c.get("type") or "UNCLASSIFIED" for c in claims.values())

    # Extraction confidence.
    confidence_counts = Counter(c.get("confidence", "") or "(unknown)" for c in claims.values())

    # Hedged.
    hedged_counts = Counter(
        "hedged" if str(c.get("hedged", "")).lower() == "true" else "not hedged"
        for c in claims.values()
    )

    # Per-claim aggregate verdict (CLEAR / FLAGGED / INCONCLUSIVE / NOT_CHECKED).
    per_claim_verdict: dict[str, str] = {
        cid: claim_aggregate_verdict(verdicts.get(cid, {})) for cid in claims
    }
    verdict_counts = Counter(per_claim_verdict.values())

    # Type × verdict.
    type_verdict: dict[tuple[str, str], int] = Counter()
    for cid, claim in claims.items():
        t = claim.get("type") or "UNCLASSIFIED"
        type_verdict[(t, per_claim_verdict[cid])] += 1

    # Per-category breakdown: counts of FLAGGED / INCONCLUSIVE / CLEAR per category.
    category_counts: dict[str, dict[str, int]] = {
        cat: {"FLAGGED": 0, "INCONCLUSIVE": 0, "CLEAR": 0}
        for cat in CATEGORIES_BY_SEVERITY
    }
    for cid, record in verdicts.items():
        for cat, entry in record.items():
            v = entry.get("verdict")
            if cat in category_counts and v in category_counts[cat]:
                category_counts[cat][v] += 1

    # Flagged-category co-occurrence: how many claims are flagged in each
    # category? (counts a claim once per category it's flagged in)
    flagged_in_category = Counter()
    for record in verdicts.values():
        for cat in flagged_categories(record):
            flagged_in_category[cat] += 1

    # INCONCLUSIVE reasons across all checkers.
    reason_counts = Counter(
        entry["reason"]
        for record in verdicts.values()
        for entry in record.values()
        if entry.get("verdict") == "INCONCLUSIVE" and entry.get("reason")
    )

    # Coverage (per-claim).
    cleared = verdict_counts.get("CLEAR", 0)
    flagged = verdict_counts.get("FLAGGED", 0)
    inconclusive = verdict_counts.get("INCONCLUSIVE", 0)
    not_checked = verdict_counts.get("NOT_CHECKED", 0)
    attempted = cleared + flagged + inconclusive

    # Per group (if graph available).
    groups_summary = []
    if graph:
        group_by_id = {g["id"]: g for g in graph.get("groups", [])}
        members: dict[str, list[str]] = {gid: [] for gid in group_by_id}
        for c in graph.get("claims", []):
            if c.get("parent") in members:
                members[c["parent"]].append(c["id"])
        for gid, g in group_by_id.items():
            child_ids = members.get(gid, [])
            child_verdicts = Counter(per_claim_verdict.get(cid, "NOT_CHECKED") for cid in child_ids)
            groups_summary.append({
                "id": gid,
                "title": g.get("title", gid),
                "claim_count": len(child_ids),
                "verdict": g.get("verdict", "NOT_CHECKED"),
                "breakdown": dict(child_verdicts),
            })

    return {
        "n_claims": n,
        "n_groups": len(graph.get("groups", [])) if graph else None,
        "type_counts": type_counts,
        "confidence_counts": confidence_counts,
        "hedged_counts": hedged_counts,
        "verdict_counts": verdict_counts,
        "type_verdict": type_verdict,
        "category_counts": category_counts,
        "flagged_in_category": flagged_in_category,
        "reason_counts": reason_counts,
        "attempted": attempted,
        "cleared": cleared,
        "flagged": flagged,
        "inconclusive": inconclusive,
        "not_checked": not_checked,
        "groups_summary": groups_summary,
    }


def _trust_block(t: dict, n_claims: int) -> list[str]:
    if t["score"] is None:
        return [
            "## Trust score",
            "",
            "**no claims checked yet** — trust score will populate once",
            "phase 2 verification has run.",
            "",
        ]
    label = {"high": "high trust", "medium": "medium trust", "low": "low trust"}[t["bucket"]]
    return [
        "## Trust score",
        "",
        f"**{t['score']} / 100** — {label}",
        "",
        f"`{t['clear']} clear · {t['flagged']} flagged · {t['inconclusive']} inconclusive`"
        f" — out of {t['attempted']} attempted of {n_claims} total claims",
        "",
        "Weighting: CLEAR = 1.0, INCONCLUSIVE = 0.5, FLAGGED = 0.0; NOT_CHECKED",
        "claims are excluded from the denominator. Buckets: ≥85 high, ≥60",
        "medium, <60 low.",
        "",
    ]


def render_stats_md(slug: str, s: dict, t: dict) -> str:
    n = s["n_claims"]
    out: list[str] = [
        f"# Claim statistics — {slug}",
        "",
        "Generated by `src/claim_stats.py`. Numbers are mechanical from",
        "`CLAIMS.md`, `VERIFICATION.md`, and (if present) `graph.v2.json`.",
        "",
        *_trust_block(t, n),
        "## Totals",
        "",
        f"- **{n}** claims extracted",
    ]
    if s["n_groups"] is not None:
        out.append(f"- **{s['n_groups']}** groups in the graph")
    out.append("")

    # By type.
    out += [
        "## By type",
        "",
        md_table(
            [[t, str(s["type_counts"].get(t, 0))]
             for t in CLAIM_TYPES if s["type_counts"].get(t, 0)],
            ["type", "count"],
        ),
        "",
    ]

    # Extraction confidence.
    out += [
        "## By extraction confidence",
        "",
        md_table(
            [[c, str(s["confidence_counts"].get(c, 0))]
             for c in (*CONFIDENCES, "(unknown)")
             if s["confidence_counts"].get(c, 0)],
            ["confidence", "count"],
        ),
        "",
    ]

    # Hedged.
    out += [
        "## Hedging",
        "",
        f"- {s['hedged_counts'].get('hedged', 0)} hedged",
        f"- {s['hedged_counts'].get('not hedged', 0)} not hedged",
        "",
    ]

    # Verdict.
    out += [
        "## By verdict",
        "",
        md_table(
            [[v, str(s["verdict_counts"].get(v, 0))] for v in VERDICTS],
            ["verdict", "count"],
        ),
        "",
    ]

    # Type × verdict.
    types_present = [t for t in CLAIM_TYPES if s["type_counts"].get(t, 0)]
    if types_present:
        rows = []
        for t in types_present:
            rows.append([
                t,
                *(str(s["type_verdict"].get((t, v), 0)) for v in VERDICTS),
            ])
        out += [
            "## Type × verdict",
            "",
            md_table(rows, ["type", *VERDICTS]),
            "",
        ]

    # Coverage.
    pct = lambda num, denom: f"{(100 * num / denom):.1f}%" if denom else "—"
    out += [
        "## Coverage",
        "",
        f"- {s['attempted']} / {n} claims ({pct(s['attempted'], n)}) had at least one checker verdict",
    ]
    if s["attempted"]:
        out += [
            f"- {s['cleared']} / {s['attempted']} ({pct(s['cleared'], s['attempted'])}) all CLEAR",
            f"- {s['flagged']} / {s['attempted']} ({pct(s['flagged'], s['attempted'])}) FLAGGED in at least one category",
            f"- {s['inconclusive']} / {s['attempted']} ({pct(s['inconclusive'], s['attempted'])}) INCONCLUSIVE only",
        ]
    out.append("")

    # Per-category counts (severity-ordered).
    cat_rows = []
    for cat in CATEGORIES_BY_SEVERITY:
        cnt = s["category_counts"].get(cat, {})
        cat_rows.append([
            cat,
            str(cnt.get("FLAGGED", 0)),
            str(cnt.get("INCONCLUSIVE", 0)),
            str(cnt.get("CLEAR", 0)),
        ])
    out += [
        "## By error category",
        "",
        md_table(cat_rows, ["category", "FLAGGED", "INCONCLUSIVE", "CLEAR"]),
        "",
    ]

    # INCONCLUSIVE reasons across all checkers.
    if s["reason_counts"]:
        out += [
            "## INCONCLUSIVE reasons",
            "",
            md_table(
                [[r, str(c)] for r, c in s["reason_counts"].most_common()],
                ["reason", "count"],
            ),
            "",
        ]

    # Per group.
    if s["groups_summary"]:
        rows = []
        for g in s["groups_summary"]:
            bd = g["breakdown"]
            bd_str = ", ".join(f"{k} {v}" for k, v in bd.items()) or "—"
            rows.append([
                g["id"],
                g["title"],
                str(g["claim_count"]),
                g["verdict"],
                bd_str,
            ])
        out += [
            "## Per group",
            "",
            md_table(rows, ["id", "title", "claims", "group_verdict", "breakdown"]),
            "",
        ]

    return "\n".join(out)


def one_line_summary(slug: str, s: dict, t: dict) -> str:
    score_str = f"{t['score']}/100 ({t['bucket']})" if t["score"] is not None else "—"
    return (
        f"{slug}: trust {score_str} · {s['n_claims']} claims · "
        f"CLEAR={s['cleared']} FLAGGED={s['flagged']} "
        f"INCONCLUSIVE={s['inconclusive']} NOT_CHECKED={s['not_checked']}"
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("review_dir", type=Path, help="path to reviews/<slug>/")
    p.add_argument("--out", type=Path, help="override STATS.md path")
    p.add_argument("--print", action="store_true",
                   help="also print STATS.md content to stdout")
    args = p.parse_args()

    review = args.review_dir
    if not review.is_dir():
        print(f"error: {review} is not a directory", file=sys.stderr)
        return 2

    claims_md = review / "phase1" / "outputs" / "CLAIMS.md"
    verification_md = review / "phase2" / "outputs" / "VERIFICATION.md"
    graph_v2_json = review / "phase2" / "outputs" / "graph.v2.json"
    out_path = args.out or (review / "phase3" / "outputs" / "STATS.md")

    if not claims_md.exists():
        print(f"error: CLAIMS.md not found at {claims_md}", file=sys.stderr)
        return 2

    try:
        claims = parse_claims_md(claims_md)
    except ClaimsParseError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    verdicts = parse_verification_md(verification_md)
    graph = json.loads(graph_v2_json.read_text()) if graph_v2_json.exists() else None

    s = stats(claims, verdicts, graph)
    t = trust_score(verdicts)
    md = render_stats_md(review.name, s, t)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md + "\n")
    print(f"wrote {out_path}")
    print(f"  {one_line_summary(review.name, s, t)}")
    if args.print:
        print()
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
