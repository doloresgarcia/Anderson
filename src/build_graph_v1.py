#!/usr/bin/env python3
"""Phase-1 graph_builder FINAL pass: merge LITERATURE.md into graph.v1.skeleton.json.

Output: phase1/outputs/graph.v1.json with a `references` array on each claim
node that has at least one literature candidate.
Hard rules:
  - Do not modify the set of claim/group nodes or their structural fields.
  - No new claim-to-claim edges (skeleton has none, keep none).
  - Every reference key used must appear in references.bib.
  - Validate against conventions/graph_schema.md before writing.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path("/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1")
SKEL = ROOT / "phase1/outputs/graph.v1.skeleton.json"
LIT = ROOT / "phase1/outputs/LITERATURE.md"
BIB = ROOT / "phase1/outputs/references.bib"
OUT = ROOT / "phase1/outputs/graph.v1.json"


def parse_bib_keys(bib_path: Path) -> set[str]:
    """Extract every cite key from a bibtex file."""
    text = bib_path.read_text()
    # @type{key, ... } — capture the key.
    keys = set(re.findall(r"^@\w+\s*\{\s*([^,\s]+)\s*,", text, flags=re.M))
    return keys


def parse_literature(lit_path: Path) -> dict[str, list[dict]]:
    """Parse LITERATURE.md per-claim. Returns {claim_id: [ {key, relation, confidence, snippet}, ... ]}."""
    text = lit_path.read_text()
    out: dict[str, list[dict]] = {}
    current: str | None = None
    # bullet form: - [@key] — relation — confidence X — "snippet"
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
            out[current].append(
                {
                    "key": key,
                    "relation": relation.lower(),
                    "confidence": confidence.lower(),
                    "snippet": snippet,
                }
            )
    # drop empty headings (claims with no candidates)
    return {cid: refs for cid, refs in out.items() if refs}


def main() -> int:
    skel = json.loads(SKEL.read_text())
    bib_keys = parse_bib_keys(BIB)
    lit = parse_literature(LIT)

    # Cross-check every literature key resolves to references.bib.
    used_keys: set[str] = set()
    for refs in lit.values():
        for r in refs:
            used_keys.add(r["key"])
    missing = sorted(used_keys - bib_keys)
    if missing:
        print(f"FAIL: literature keys missing from references.bib: {missing}", file=sys.stderr)
        return 2
    print(f"OK: {len(used_keys)} unique literature keys; all resolve in references.bib")

    # Vocabulary checks.
    allowed_relations = {"supports", "contradicts", "related"}
    allowed_confidences = {"high", "medium", "low"}
    for cid, refs in lit.items():
        for r in refs:
            if r["relation"] not in allowed_relations:
                print(f"FAIL: unknown relation {r['relation']!r} on {cid}", file=sys.stderr)
                return 3
            if r["confidence"] not in allowed_confidences:
                print(
                    f"FAIL: unknown confidence {r['confidence']!r} on {cid}",
                    file=sys.stderr,
                )
                return 3

    # Build a copy of the skeleton; do not mutate original.
    out = json.loads(json.dumps(skel))

    # Index of claim ids (frozen).
    skel_claim_ids = {c["id"] for c in skel["claims"]}

    # Sanity: every literature heading should match a real claim id in the skeleton.
    unknown_claim_ids = sorted(set(lit.keys()) - skel_claim_ids)
    if unknown_claim_ids:
        print(
            f"FAIL: LITERATURE.md references unknown claim ids: {unknown_claim_ids}",
            file=sys.stderr,
        )
        return 4

    # Attach references property to claims that have candidates.
    enriched = 0
    for claim in out["claims"]:
        cid = claim["id"]
        refs = lit.get(cid)
        if not refs:
            continue
        claim["references"] = [
            {
                "key": r["key"],
                "relation": r["relation"],
                "confidence": r["confidence"],
                "snippet": r["snippet"],
                "provenance": f"LITERATURE.md:{cid}",
            }
            for r in refs
        ]
        enriched += 1
    print(f"OK: attached references to {enriched} claims")

    # Validate hard structural invariants vs. skeleton.
    skel_claim_index = {c["id"]: c for c in skel["claims"]}
    out_claim_index = {c["id"]: c for c in out["claims"]}
    if set(skel_claim_index) != set(out_claim_index):
        print("FAIL: claim id set changed", file=sys.stderr)
        return 5
    structural_keys = {
        "id",
        "kind",
        "parent",
        "type",
        "sentence",
        "hedged",
        "confidence",
        "verdict",
        "color",
        "page",
        "line",
        "section",
    }
    for cid, sc in skel_claim_index.items():
        oc = out_claim_index[cid]
        for k in structural_keys:
            if sc.get(k) != oc.get(k):
                print(
                    f"FAIL: claim {cid} structural field {k!r} changed: {sc.get(k)!r} -> {oc.get(k)!r}",
                    file=sys.stderr,
                )
                return 6

    # Group nodes must be byte-equivalent.
    if json.dumps(skel["groups"], sort_keys=True) != json.dumps(out["groups"], sort_keys=True):
        print("FAIL: group nodes changed", file=sys.stderr)
        return 7

    # Edges: skeleton had none; v1 must still have none (no new claim-to-claim edges).
    if out["edges"] != skel["edges"]:
        print("FAIL: edges changed (none allowed in this dispatch)", file=sys.stderr)
        return 8

    # Schema validation rules from conventions/graph_schema.md.
    groups = out["groups"]
    claims = out["claims"]
    edges = out["edges"]

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
            print(
                f"FAIL: claim {c['id']} not in group {gid}'s claim_ids",
                file=sys.stderr,
            )
            return 13

    cid_set = set(cid_to_parent)
    for e in edges:
        if e["source"] not in cid_set or e["target"] not in cid_set:
            print(f"FAIL: edge endpoint not a claim: {e}", file=sys.stderr)
            return 14
        if e["source"] == e["target"]:
            print(f"FAIL: self-edge: {e}", file=sys.stderr)
            return 15
        if (
            e["kind"] == "contradicts"
            and e.get("confidence") == "low"
            and e.get("provenance") == "inferred"
        ):
            print(f"FAIL: inferred low-confidence contradicts edge: {e}", file=sys.stderr)
            return 16

    palette = {
        "PASS": "#2ECC71",
        "INCONCLUSIVE": "#F1C40F",
        "FAIL": "#E74C3C",
        "NOT_CHECKED": "#95A5A6",
    }
    for c in claims:
        if c["verdict"] != "NOT_CHECKED":
            print(f"FAIL: phase-1 claim {c['id']} has non-NOT_CHECKED verdict", file=sys.stderr)
            return 17
        if c["color"] != palette[c["verdict"]]:
            print(f"FAIL: claim {c['id']} color/verdict mismatch", file=sys.stderr)
            return 18
    for g in groups:
        if g["verdict"] != "NOT_CHECKED":
            print(f"FAIL: phase-1 group {g['id']} has non-NOT_CHECKED verdict", file=sys.stderr)
            return 19
        if g["color"] != palette[g["verdict"]]:
            print(f"FAIL: group {g['id']} color/verdict mismatch", file=sys.stderr)
            return 20

    # Counts for the report.
    claim_count = len(claims)
    group_count = len(groups)
    edge_count_by_kind: dict[str, int] = {}
    for e in edges:
        edge_count_by_kind[e["kind"]] = edge_count_by_kind.get(e["kind"], 0) + 1
    print(f"OK: validation passed. groups={group_count} claims={claim_count} edges={len(edges)}")
    print(f"OK: claims with literature evidence = {enriched}")
    print(f"OK: unique reference keys used = {len(used_keys)}")

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"WROTE {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
