#!/usr/bin/env python3
"""
UTE Topology Analytics v1

Run from repository root:

    python 006-tools/topology-analytics/analyze-topology-v1.py

Reads:
    docs/data/truth-map-v1.json
    docs/data/truth-index-v1.json

Writes:
    003-machine-readable/topology-analytics-v1.json
    docs/data/topology-analytics-preview.json
"""

from pathlib import Path
import json
from collections import defaultdict, deque

ROOT = Path.cwd()
DOCS_DATA = ROOT / "docs" / "data"
MACHINE = ROOT / "003-machine-readable"

MAP_PATH = DOCS_DATA / "truth-map-v1.json"
INDEX_PATH = DOCS_DATA / "truth-index-v1.json"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def longest_dependency_chain(start, dependencies):
    best = []

    def walk(node, path):
        nonlocal best
        if node in path:
            return
        new_path = path + [node]
        deps = dependencies.get(node, [])
        if not deps:
            if len(new_path) > len(best):
                best = new_path
            return
        for dep in deps:
            walk(dep, new_path)

    walk(start, [])
    return best

def reachable_from(start, reverse):
    seen = set()
    q = deque(reverse.get(start, []))
    while q:
        item = q.popleft()
        if item in seen:
            continue
        seen.add(item)
        q.extend(reverse.get(item, []))
    return seen

def main():
    if not MAP_PATH.exists():
        raise SystemExit("ERROR: docs/data/truth-map-v1.json not found.")

    graph = read_json(MAP_PATH)
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    node_ids = {n["id"] for n in nodes if n.get("id")}
    node_by_id = {n["id"]: n for n in nodes if n.get("id")}

    dependencies = {n["id"]: n.get("dependencies", []) for n in nodes if n.get("id")}
    reverse = defaultdict(list)

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        if source and target:
            reverse[target].append(source)

    centrality = []
    for nid in sorted(node_ids):
        direct = len(reverse.get(nid, []))
        recursive = len(reachable_from(nid, reverse))
        centrality.append({
            "id": nid,
            "title": node_by_id[nid].get("title", nid),
            "domain": node_by_id[nid].get("domain", "Unknown"),
            "direct_dependents": direct,
            "recursive_dependents": recursive
        })

    centrality_sorted = sorted(
        centrality,
        key=lambda x: (x["recursive_dependents"], x["direct_dependents"]),
        reverse=True
    )

    isolated = []
    for nid in sorted(node_ids):
        if not dependencies.get(nid) and not reverse.get(nid):
            isolated.append({
                "id": nid,
                "title": node_by_id[nid].get("title", nid)
            })

    orphan_like = []
    for nid in sorted(node_ids):
        if not reverse.get(nid) and dependencies.get(nid):
            orphan_like.append({
                "id": nid,
                "title": node_by_id[nid].get("title", nid),
                "dependencies": dependencies.get(nid, [])
            })

    roots = []
    for nid in sorted(node_ids):
        if not dependencies.get(nid):
            roots.append({
                "id": nid,
                "title": node_by_id[nid].get("title", nid)
            })

    chains = []
    for nid in sorted(node_ids):
        chain = longest_dependency_chain(nid, dependencies)
        chains.append({
            "start": nid,
            "start_title": node_by_id[nid].get("title", nid),
            "chain_length": len(chain),
            "chain": chain
        })

    deepest_chains = sorted(chains, key=lambda x: x["chain_length"], reverse=True)[:10]

    domains = defaultdict(list)
    for node in nodes:
        domains[node.get("domain", "Unknown")].append(node.get("id"))

    domain_summary = [
        {
            "domain": domain,
            "truth_count": len(ids),
            "truths": sorted(ids)
        }
        for domain, ids in sorted(domains.items())
    ]

    bridge_truths = []
    for node in nodes:
        domain = node.get("domain", "")
        deps = node.get("dependencies", [])
        dep_domains = {node_by_id[d].get("domain") for d in deps if d in node_by_id}
        if len(dep_domains) > 1 or "/" in domain:
            bridge_truths.append({
                "id": node.get("id"),
                "title": node.get("title"),
                "domain": domain,
                "dependency_domains": sorted([d for d in dep_domains if d])
            })

    density = 0
    if len(node_ids) > 1:
        density = len(edges) / (len(node_ids) * (len(node_ids) - 1))

    analytics = {
        "report_id": "UTE-TOPOLOGY-ANALYTICS-V1",
        "generated_by": "UTE Topology Analytics v1",
        "truth_count": len(node_ids),
        "edge_count": len(edges),
        "dependency_density": density,
        "top_central_truths": centrality_sorted[:10],
        "root_truths": roots,
        "isolated_truths": isolated,
        "leaf_truths_with_dependencies": orphan_like,
        "deepest_dependency_chains": deepest_chains,
        "domain_summary": domain_summary,
        "bridge_truths": bridge_truths[:25],
        "recommended_review_focus": [
            "Deepen proofs for highest recursive centrality truths.",
            "Review leaf truths with dependencies to determine whether they need downstream expansion.",
            "Check bridge truths carefully because they connect conceptual regions.",
            "Use deepest chains to identify where reconstruction explanations may need improvement."
        ]
    }

    write_json(MACHINE / "topology-analytics-v1.json", analytics)
    write_json(DOCS_DATA / "topology-analytics-preview.json", analytics)

    print("UTE Topology Analytics v1 complete.")
    print(f"Truths: {len(node_ids)}")
    print(f"Edges: {len(edges)}")
    print(f"Top central truth: {centrality_sorted[0]['id'] if centrality_sorted else 'none'}")

if __name__ == "__main__":
    main()
