#!/usr/bin/env python3
"""Phase-1 graph_builder ROUND-2 rebuild.

Rebuilds graph.v1.json after the fixer applied F02-F08:
  - CLAIMS.md: dropped C188 and C189 (non-propositional code-availability rows);
    added C218 and C219 (split from compound C015 contributions sentence);
    rewrote C015 sentence; demoted C036, C044, C060, C148 confidence to low.
  - LITERATURE.md: re-tagged C006 and C148 (relations/confidence demoted);
    added empty headings for C218 and C219.

Strategy: minimal-shift rebuild from the FROZEN skeleton.
  - Cluster topology stays as in skeleton: 20 groups, same titles/captions/sections.
  - G002 (introduction context) loses C188/C189 (dropped entirely from the graph)
    and gains C218/C219 (which fit naturally — same line/section/type as
    C012, C013, C015, all already in G002).
  - All other group memberships are unchanged because no other claim ids moved.
  - Claim node fields are re-pulled from the post-fixer CLAIMS.md (so C015's
    new sentence and the four low-confidence values flow through).
  - References are re-attached from the post-fixer LITERATURE.md.

The skeleton at graph.v1.skeleton.json is read-only; it is NOT modified.
Validation against conventions/graph_schema.md runs before write; any failure
aborts the script with non-zero exit status and no file written.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path("/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1")
SKEL = ROOT / "phase1/outputs/graph.v1.skeleton.json"
CLAIMS = ROOT / "phase1/outputs/CLAIMS.md"
LIT = ROOT / "phase1/outputs/LITERATURE.md"
BIB = ROOT / "phase1/outputs/references.bib"
OUT = ROOT / "phase1/outputs/graph.v1.json"

PALETTE = {
    "PASS": "#2ECC71",
    "INCONCLUSIVE": "#F1C40F",
    "FAIL": "#E74C3C",
    "NOT_CHECKED": "#95A5A6",
}


def parse_bib_keys(bib_path: Path) -> set[str]:
    text = bib_path.read_text()
    return set(re.findall(r"^@\w+\s*\{\s*([^,\s]+)\s*,", text, flags=re.M))


def parse_claims(claims_path: Path) -> list[dict]:
    """Parse CLAIMS.md table rows. Returns list of dicts in row order."""
    text = claims_path.read_text()
    rows = []
    row_re = re.compile(r"^\|\s*(C\d{3})\s*\|")
    for line in text.splitlines():
        if not row_re.match(line):
            continue
        # split on '|' (skip leading/trailing empty)
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) != 9:
            print(f"WARN: unexpected col count: {parts}", file=sys.stderr)
            continue
        cid, ctype, sentence, hedged, confidence, page, line_no, section, provenance = parts
        # sentence is wrapped in quotes
        if sentence.startswith('"') and sentence.endswith('"'):
            sentence_clean = sentence[1:-1]
        else:
            sentence_clean = sentence
        rows.append({
            "id": cid,
            "type": ctype,
            "sentence": sentence_clean,
            "hedged": hedged.lower() == "true",
            "confidence": confidence,
            "page": None if page == "?" else int(page),
            "line": int(line_no),
            "section": section,
            "provenance": provenance,
        })
    return rows


def parse_literature(lit_path: Path) -> dict[str, list[dict]]:
    text = lit_path.read_text()
    out: dict[str, list[dict]] = {}
    current: str | None = None
    bullet_re = re.compile(
        r'^\s*-\s*\[@([^\]]+)\]\s*[—\-]+\s*([A-Za-z_]+)\s*[—\-]+\s*confidence\s+([A-Za-z]+)\s*[—\-]+\s*"(.*?)"\s*$'
    )
    head_re = re.compile(r"^##\s+(C\d{3})\s*$")
    for line in text.splitlines():
        m = head_re.match(line)
        if m:
            current = m.group(1)
            out.setdefault(current, [])
            continue
        if current is None:
            continue
        m = bullet_re.match(line)
        if m:
            key, relation, confidence, snippet = m.groups()
            out[current].append({
                "key": key,
                "relation": relation.lower(),
                "confidence": confidence.lower(),
                "snippet": snippet,
            })
    return {cid: refs for cid, refs in out.items() if refs}


def main() -> int:
    skel = json.loads(SKEL.read_text())
    claim_rows = parse_claims(CLAIMS)
    lit = parse_literature(LIT)
    bib_keys = parse_bib_keys(BIB)

    # Sanity: claim count and id-set
    expected_ids = (
        {f"C{i:03d}" for i in range(1, 188)}
        | {f"C{i:03d}" for i in range(190, 220)}  # 190..219
    )
    actual_ids = {r["id"] for r in claim_rows}
    if actual_ids != expected_ids:
        missing = sorted(expected_ids - actual_ids)
        extra = sorted(actual_ids - expected_ids)
        print(f"FAIL: claim id mismatch. missing={missing} extra={extra}", file=sys.stderr)
        return 1
    if len(claim_rows) != 217:
        print(f"FAIL: expected 217 claim rows, got {len(claim_rows)}", file=sys.stderr)
        return 1
    print(f"OK: 217 claims parsed, ids match expected set (1-187, 190-219)")

    # Literature: every key resolves in references.bib
    used_keys = {r["key"] for refs in lit.values() for r in refs}
    missing_keys = sorted(used_keys - bib_keys)
    if missing_keys:
        print(f"FAIL: literature keys not in references.bib: {missing_keys}", file=sys.stderr)
        return 2
    print(f"OK: {len(used_keys)} unique literature keys resolve in references.bib")

    # Vocabulary checks
    allowed_relations = {"supports", "contradicts", "related"}
    allowed_confidences = {"high", "medium", "low"}
    for cid, refs in lit.items():
        for r in refs:
            if r["relation"] not in allowed_relations:
                print(f"FAIL: relation {r['relation']!r} on {cid}", file=sys.stderr)
                return 3
            if r["confidence"] not in allowed_confidences:
                print(f"FAIL: confidence {r['confidence']!r} on {cid}", file=sys.stderr)
                return 3

    # Re-cluster: minimal shift from the skeleton.
    # The skeleton's group memberships are kept identical EXCEPT G002:
    # - drop C188 and C189 (they no longer exist as claims)
    # - add C218 and C219 (new contributions sub-claims; sec 1, line 108,
    #   type method — same bucket as existing G002 members C012/C013/C015)
    skel_groups = json.loads(json.dumps(skel["groups"]))  # deep copy
    g002 = next(g for g in skel_groups if g["id"] == "G002")
    g002_orig = list(g002["claim_ids"])
    g002["claim_ids"] = [c for c in g002["claim_ids"] if c not in {"C188", "C189"}]
    # Insert C218, C219 in the natural ordering — append at end, since the
    # claim_ids list in G002 was originally in id order (C006, C008, C009,
    # C010, C011, C012, C013, C015, C188, C189). After dropping C188/C189
    # and adding C218/C219, the new id-sorted order is:
    # C006, C008, C009, C010, C011, C012, C013, C015, C218, C219.
    g002["claim_ids"].extend(["C218", "C219"])
    # update page_range — both C218 and C219 are line=108 like C012/C015,
    # so the existing range [95, 855] tightens. Recompute from the post-fixer
    # claim rows. Since we drop C188/C189 (line 855) and add C218/C219
    # (line 108), the new max line for G002 drops to whatever the highest
    # remaining member's line is.
    by_id = {r["id"]: r for r in claim_rows}
    g002_lines = [by_id[cid]["line"] for cid in g002["claim_ids"]]
    g002["page_range"] = [min(g002_lines), max(g002_lines)]
    # title/caption/section/dominant_type all remain valid:
    # - title "introduction context" still describes contributions/intro framing
    # - caption mentions "high-level method statement"; the new C218/C219 are
    #   exactly those statements; remove the obsolete "public code release" tail.
    # The fixer's edit removed C188/C189 (the code-release rows), so the
    # caption's "including the public code release" wording is now stale.
    # Update the caption to reflect the new membership without the dropped rows.
    g002["caption"] = (
        "Introductory framing of Lorentz-equivariant ML for LHC and the "
        "paper's high-level contribution statement, including amplitude "
        "regression, classification, and generation goals."
    )

    # All other groups unchanged.

    # Assemble new claim nodes from CLAIMS.md (verdict NOT_CHECKED, gray).
    # Parent must be derivable from group memberships above.
    parent_of: dict[str, str] = {}
    for g in skel_groups:
        for cid in g["claim_ids"]:
            parent_of[cid] = g["id"]

    if set(parent_of.keys()) != actual_ids:
        miss = sorted(actual_ids - set(parent_of))
        ext = sorted(set(parent_of) - actual_ids)
        print(f"FAIL: group-membership claim set != CLAIMS.md set. "
              f"missing_in_groups={miss} extra_in_groups={ext}",
              file=sys.stderr)
        return 4

    new_claims = []
    for r in claim_rows:
        cid = r["id"]
        node = {
            "id": cid,
            "kind": "claim",
            "parent": parent_of[cid],
            "type": r["type"],
            "sentence": r["sentence"],
            "hedged": r["hedged"],
            "confidence": r["confidence"],
            "verdict": "NOT_CHECKED",
            "color": PALETTE["NOT_CHECKED"],
            "page": r["page"],
            "line": r["line"],
            "section": r["section"],
        }
        refs = lit.get(cid)
        if refs:
            node["references"] = [
                {
                    "key": rr["key"],
                    "relation": rr["relation"],
                    "confidence": rr["confidence"],
                    "snippet": rr["snippet"],
                    "provenance": f"LITERATURE.md:{cid}",
                }
                for rr in refs
            ]
        new_claims.append(node)

    new_graph = {
        "schema_version": skel["schema_version"],
        "paper": skel["paper"],
        "groups": skel_groups,
        "claims": new_claims,
        "edges": [],  # skeleton had none; this dispatch invents none
    }

    # ---- Schema validation (conventions/graph_schema.md) ----
    groups = new_graph["groups"]
    claims = new_graph["claims"]
    edges = new_graph["edges"]

    if len(groups) > 20:
        print(f"FAIL: groups > 20 ({len(groups)})", file=sys.stderr)
        return 10
    for g in groups:
        n = len(g["claim_ids"])
        if not (1 <= n <= 15):
            print(f"FAIL: group {g['id']} has {n} claims", file=sys.stderr)
            return 11

    cid_to_parent = {c["id"]: c["parent"] for c in claims}
    gid_to_children = {g["id"]: set(g["claim_ids"]) for g in groups}
    for c in claims:
        gid = c["parent"]
        if gid not in gid_to_children:
            print(f"FAIL: claim {c['id']} parent {gid} not a group", file=sys.stderr)
            return 12
        if c["id"] not in gid_to_children[gid]:
            print(f"FAIL: claim {c['id']} not in group {gid}'s claim_ids", file=sys.stderr)
            return 13

    # bidirectional: every claim_id in a group must resolve to a real claim
    all_claim_ids = set(cid_to_parent)
    for g in groups:
        for cid in g["claim_ids"]:
            if cid not in all_claim_ids:
                print(f"FAIL: group {g['id']} lists missing claim {cid}", file=sys.stderr)
                return 14

    for e in edges:
        if e["source"] not in all_claim_ids or e["target"] not in all_claim_ids:
            print(f"FAIL: edge endpoint not a claim: {e}", file=sys.stderr)
            return 15
        if e["source"] == e["target"]:
            print(f"FAIL: self-edge: {e}", file=sys.stderr)
            return 16
        if (e["kind"] == "contradicts"
                and e.get("confidence") == "low"
                and e.get("provenance") == "inferred"):
            print(f"FAIL: inferred low-confidence contradicts edge: {e}", file=sys.stderr)
            return 17

    for c in claims:
        if c["verdict"] != "NOT_CHECKED":
            print(f"FAIL: phase-1 claim {c['id']} has non-NOT_CHECKED verdict",
                  file=sys.stderr)
            return 18
        if c["color"] != PALETTE[c["verdict"]]:
            print(f"FAIL: claim {c['id']} color/verdict mismatch", file=sys.stderr)
            return 19
    for g in groups:
        if g["verdict"] != "NOT_CHECKED":
            print(f"FAIL: phase-1 group {g['id']} has non-NOT_CHECKED verdict",
                  file=sys.stderr)
            return 20
        if g["color"] != PALETTE[g["verdict"]]:
            print(f"FAIL: group {g['id']} color/verdict mismatch", file=sys.stderr)
            return 21

    # ---- Reporting ----
    n_with_refs = sum(1 for c in claims if "references" in c)
    print(f"OK: validation passed. groups={len(groups)} claims={len(claims)} "
          f"edges={len(edges)} claims_with_refs={n_with_refs}")

    print("\n=== Per-group sizes (round-2) vs round-1 skeleton ===")
    skel_sizes = {g["id"]: len(g["claim_ids"]) for g in skel["groups"]}
    new_sizes = {g["id"]: len(g["claim_ids"]) for g in groups}
    for gid in sorted(new_sizes):
        old = skel_sizes[gid]
        new = new_sizes[gid]
        marker = " (UNCHANGED)" if old == new and gid != "G002" else ""
        if gid == "G002":
            marker = f" (was {old}; dropped C188+C189; added C218+C219)"
        print(f"  {gid}: {old} -> {new}{marker}")

    # Confidence audit for the four targeted claims
    targets = ("C036", "C044", "C060", "C148")
    print("\n=== Low-confidence audit ===")
    by_id_claim = {c["id"]: c for c in claims}
    for cid in targets:
        c = by_id_claim[cid]
        print(f"  {cid}: confidence={c['confidence']} (expected: low)")
        if c["confidence"] != "low":
            print(f"FAIL: {cid} confidence != low", file=sys.stderr)
            return 22

    OUT.write_text(json.dumps(new_graph, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWROTE {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
