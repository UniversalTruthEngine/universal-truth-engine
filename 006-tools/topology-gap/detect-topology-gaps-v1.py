#!/usr/bin/env python3
"""
UTE Topology Gap Detector v1

Run from repository root:
    python 006-tools/topology-gap/detect-topology-gaps-v1.py

Detects frontier boundary nodes: truths with no downstream dependants.

Reads:
    003-machine-readable/truth-graph.json or docs/data/truth-map-v1.json

Writes:
    003-machine-readable/topology-gap-report-v1.json
    docs/data/topology-gap-report-v1.json
"""

from pathlib import Path
import json

ROOT = Path.cwd()
MACHINE = ROOT / "003-machine-readable"
DOCS_DATA = ROOT / "docs" / "data"

GRAPH_CANDIDATES = [
    MACHINE / "truth-graph.json",
    DOCS_DATA / "truth-map-v1.json"
]

OUT_INTERNAL = MACHINE / "topology-gap-report-v1.json"
OUT_PUBLIC = DOCS_DATA / "topology-gap-report-v1.json"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def choose_graph():
    for path in GRAPH_CANDIDATES:
        if path.exists():
            return path
    raise SystemExit("ERROR: no truth graph found. Run topology generator first.")

def score_gap(node):
    score = 0.55
    domain = node.get("domain", "")
    centrality = node.get("dependency_centrality", 0) or 0
    bridge = node.get("bridge_score", 0) or 0

    if "Arithmetic" in domain:
        score += 0.15
    if "Measurement" in domain:
        score += 0.10
    if "Geometry" in domain:
        score += 0.10
    if bridge:
        score += 0.10
    if centrality >= 3:
        score += 0.10

    return round(min(score, 0.95), 2)

def main():
    graph_path = choose_graph()
    graph = read_json(graph_path)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    ids = {node.get("id") for node in nodes if node.get("id")}
    has_dependants = {tid: False for tid in ids}

    # Edge convention: source depends_on target, so target has a dependant.
    for edge in edges:
        target = edge.get("target")
        if target in has_dependants:
            has_dependants[target] = True

    gaps = []
    for node in nodes:
        tid = node.get("id")
        if not tid:
            continue
        if not has_dependants.get(tid, False):
            gaps.append({
                "gap_id": "UTE-GAP-" + str(len(gaps) + 1).zfill(4),
                "gap_type": "frontier_boundary",
                "truth_id": tid,
                "truth_title": node.get("title", tid),
                "domain": node.get("domain", "Unknown"),
                "gap_score": score_gap(node),
                "reason": "No downstream truths currently depend on this truth.",
                "recommended_review": "Review whether this is a natural endpoint or should enable further candidate truths.",
                "status": "detected"
            })

    gaps = sorted(gaps, key=lambda g: g["gap_score"], reverse=True)

    report = {
        "report_id": "UTE-TOPOLOGY-GAP-REPORT-V1",
        "generated_by": "UTE Topology Gap Detector v1",
        "graph_source": str(graph_path),
        "truth_count": len(nodes),
        "edge_count": len(edges),
        "gap_count": len(gaps),
        "gaps": gaps,
        "governance_rule": "Detected gaps are review prompts only. They are not candidate truths and do not imply admission."
    }

    MACHINE.mkdir(parents=True, exist_ok=True)
    DOCS_DATA.mkdir(parents=True, exist_ok=True)

    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    OUT_INTERNAL.write_text(text, encoding="utf-8")
    OUT_PUBLIC.write_text(text, encoding="utf-8")

    print("UTE Topology Gap Detector v1 complete.")
    print("Graph source:", graph_path)
    print("Truths:", len(nodes))
    print("Edges:", len(edges))
    print("Gaps detected:", len(gaps))
    for gap in gaps[:10]:
        print("-", gap["truth_id"], gap["truth_title"], "(" + str(gap["gap_score"]) + ")")
    print("Wrote:", OUT_INTERNAL)
    print("Wrote:", OUT_PUBLIC)

if __name__ == "__main__":
    main()
