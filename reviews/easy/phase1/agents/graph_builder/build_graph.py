#!/usr/bin/env python3
"""
Graph builder: Phase 1 final pass.
Merges skeleton + literature into graph.v1.json
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

def parse_literature_md(lit_file: str) -> Dict[str, List[Dict]]:
    """
    Parse LITERATURE.md to extract edges.
    Returns: {claim_id: [{"key": "...", "kind": "supports|related", "confidence": "high|medium|low"}, ...]}
    """
    edges_per_claim = {}
    current_claim = None

    with open(lit_file) as f:
        for line in f:
            line = line.rstrip()

            # Match claim header: ## C001
            if line.startswith("## C"):
                current_claim = line[3:].strip()
                edges_per_claim[current_claim] = []
            # Match edge line: - [@key] — kind — confidence high/medium/low — source — "snippet"
            elif line.startswith("- [@") and current_claim:
                # Parse: - [@spinner2024lgatr] — supports — confidence high — external — "..."
                match = re.match(
                    r'- \[@([^\]]+)\] — (\w+) — confidence (\w+) — (\w+) — ',
                    line
                )
                if match:
                    key, relation_type, confidence, source = match.groups()
                    edges_per_claim[current_claim].append({
                        "key": key,
                        "kind": relation_type,  # "supports", "related", "contradicts"
                        "confidence": confidence
                    })

    return edges_per_claim

def parse_references_bib(bib_file: str) -> Set[str]:
    """Parse references.bib and return set of all bibtex keys."""
    keys = set()

    with open(bib_file) as f:
        for line in f:
            # Look for @something{key,
            match = re.search(r'^@\w+\{([^,]+),', line)
            if match:
                keys.add(match.group(1))

    return keys

def build_graph(skeleton_file: str, lit_file: str, bib_file: str, output_file: str, log_file: str):
    """Main: build graph.v1.json from skeleton + literature."""

    log_lines = []

    # Load skeleton
    with open(skeleton_file) as f:
        graph = json.load(f)

    log_lines.append(f"Loaded skeleton with {len(graph['groups'])} groups, {len(graph['claims'])} claims")

    # Parse literature and bibtex
    edges_per_claim = parse_literature_md(lit_file)
    bib_keys = parse_references_bib(bib_file)

    log_lines.append(f"Parsed {len(edges_per_claim)} claims with literature edges")
    log_lines.append(f"Found {len(bib_keys)} bibtex keys in references.bib")

    # Validate: all keys in literature must exist in references
    all_lit_keys = set()
    for claim_id, edges in edges_per_claim.items():
        for edge in edges:
            all_lit_keys.add(edge["key"])

    missing_keys = all_lit_keys - bib_keys
    if missing_keys:
        log_lines.append(f"WARNING: {len(missing_keys)} bibtex keys in LITERATURE.md but not in references.bib:")
        for key in sorted(missing_keys):
            log_lines.append(f"  - {key}")
    else:
        log_lines.append("All bibtex keys in LITERATURE.md are present in references.bib")

    # Build edges
    edge_id = 1
    edges_list = []

    # Map claim IDs for quick lookup
    claim_ids = {c["id"] for c in graph.get("claims", [])}

    for claim_id in sorted(edges_per_claim.keys()):
        if claim_id not in claim_ids:
            log_lines.append(f"WARNING: Claim {claim_id} in LITERATURE.md but not in skeleton")
            continue

        for edge_info in edges_per_claim[claim_id]:
            key = edge_info["key"]
            if key not in bib_keys:
                # Skip edges with missing keys (already logged)
                continue

            # Map relation type to edge kind
            relation_type = edge_info["kind"]
            if relation_type == "supports":
                edge_kind = "supports"
            elif relation_type == "related":
                edge_kind = "supports"  # treat "related" as "supports" for now
            elif relation_type == "contradicts":
                edge_kind = "contradicts"
            else:
                edge_kind = "supports"

            edge = {
                "id": f"E{edge_id:03d}",
                "source": claim_id,
                "target": key,
                "kind": edge_kind,
                "confidence": edge_info["confidence"],
                "provenance": "literature"
            }
            edges_list.append(edge)
            edge_id += 1

    graph["edges"] = edges_list
    log_lines.append(f"Created {len(edges_list)} literature edges")

    # Validate graph against schema
    log_lines.append("Validating graph against schema...")
    try:
        with open("/afs/cern.ch/work/m/mgarciam/private/anderson_2/Anderson/src/conventions/graph_schema.json") as f:
            schema = json.load(f)

        # Basic validation: check required fields
        required_top = schema["required"]
        for field in required_top:
            if field not in graph:
                log_lines.append(f"ERROR: Missing required field: {field}")

        # Check claims and groups exist
        if "claims" not in graph or not graph["claims"]:
            log_lines.append("WARNING: No claims in graph")
        if "groups" not in graph or not graph["groups"]:
            log_lines.append("WARNING: No groups in graph")

        log_lines.append("Basic validation passed")
    except Exception as e:
        log_lines.append(f"Validation error: {e}")

    # Write graph
    with open(output_file, "w") as f:
        json.dump(graph, f, indent=2)

    log_lines.append(f"Wrote graph to {output_file}")

    # Write log
    with open(log_file, "w") as f:
        f.write("\n".join(log_lines))

    log_lines.append(f"Wrote log to {log_file}")

    print("\n".join(log_lines))

if __name__ == "__main__":
    build_graph(
        skeleton_file="/afs/cern.ch/work/m/mgarciam/private/anderson_2/Anderson/reviews/easy/phase1/outputs/graph.v1.skeleton.json",
        lit_file="/afs/cern.ch/work/m/mgarciam/private/anderson_2/Anderson/reviews/easy/phase1/outputs/LITERATURE.md",
        bib_file="/afs/cern.ch/work/m/mgarciam/private/anderson_2/Anderson/reviews/easy/phase1/outputs/references.bib",
        output_file="/afs/cern.ch/work/m/mgarciam/private/anderson_2/Anderson/reviews/easy/phase1/outputs/graph.v1.json",
        log_file="/afs/cern.ch/work/m/mgarciam/private/anderson_2/Anderson/reviews/easy/phase1/agents/graph_builder/log.md"
    )
