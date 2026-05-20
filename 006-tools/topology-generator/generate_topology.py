#!/usr/bin/env python3
"""
UTE Topology Generator v1

Scans 001-fact-vault/**/metadata.json and generates:
- truth-graph-generated.json
- topology-health-report-generated.json

Usage from repo root:
python 006-tools/topology-generator/generate_topology.py
"""

from pathlib import Path
import json
from collections import defaultdict, deque

ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / "001-fact-vault"
OUT = ROOT / "003-machine-readable"
DOCS_DATA = ROOT / "docs" / "data"

def load_truths():
    truths = {}
    for path in VAULT.rglob("metadata.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"Could not read {path}: {exc}")
            continue
        tid = data.get("id")
        if not tid:
            continue
        data["_metadata_path"] = str(path.relative_to(ROOT))
        data["_folder"] = str(path.parent.relative_to(ROOT))
        truths[tid] = data
    return truths

def recursive_dependents(target, reverse_deps):
    seen = set()
    queue = deque(reverse_deps.get(target, []))
    while queue:
        item = queue.popleft()
        if item in seen:
            continue
        seen.add(item)
        queue.extend(reverse_deps.get(item, []))
    return seen

def bridge_score(truth, truths):
    domains = set()
    for dep in truth.get("dependencies", []):
        dep_truth = truths.get(dep)
        if dep_truth:
            domains.add(dep_truth.get("domain", "Unknown"))
    own = truth.get("domain", "Unknown")
    domains.discard(own)
    return len(domains)

def generate():
    truths = load_truths()
    reverse_deps = defaultdict(list)
    edges = []

    for tid, truth in truths.items():
        for dep in truth.get("dependencies", []):
            reverse_deps[dep].append(tid)
            edges.append({
                "source": tid,
                "target": dep,
                "type": "depends_on",
                "weight": 1.0
            })

    nodes = []
    health = {
        "missing_dependencies": [],
        "missing_proofs": [],
        "missing_entries": [],
        "missing_domains": [],
        "missing_confidence": [],
        "high_centrality_nodes": []
    }

    for tid, truth in sorted(truths.items()):
        deps = truth.get("dependencies", [])
        depended_on_by = sorted(reverse_deps.get(tid, []))
        recursive = sorted(recursive_dependents(tid, reverse_deps))
        folder = Path(truth["_folder"])

        proof_file = truth.get("proof_file", "proof.md")
        entry_file = truth.get("entry_file", "entry.md")

        node = {
            "id": tid,
            "title": truth.get("title", ""),
            "domain": truth.get("domain", "Unknown"),
            "confidence_level": truth.get("confidence_level", None),
            "dependencies": deps,
            "depended_on_by": depended_on_by,
            "dependency_centrality": len(depended_on_by),
            "recursive_dependency_centrality": len(recursive),
            "bridge_score": bridge_score(truth, truths),
            "metadata_file": truth["_metadata_path"],
            "proof_file": str(folder / proof_file),
            "entry_file": str(folder / entry_file)
        }
        nodes.append(node)

        for dep in deps:
            if dep not in truths:
                health["missing_dependencies"].append({"truth": tid, "missing_dependency": dep})

        if not (ROOT / folder / proof_file).exists():
            health["missing_proofs"].append(tid)
        if not (ROOT / folder / entry_file).exists():
            health["missing_entries"].append(tid)
        if not truth.get("domain"):
            health["missing_domains"].append(tid)
        if truth.get("confidence_level") is None:
            health["missing_confidence"].append(tid)
        if len(depended_on_by) >= 3:
            health["high_centrality_nodes"].append({
                "id": tid,
                "dependency_centrality": len(depended_on_by),
                "recursive_dependency_centrality": len(recursive)
            })

    graph = {
        "generated_by": "UTE Topology Generator v1",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges
    }

    OUT.mkdir(parents=True, exist_ok=True)
    DOCS_DATA.mkdir(parents=True, exist_ok=True)

    (OUT / "truth-graph-generated.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    (OUT / "topology-health-report-generated.json").write_text(json.dumps(health, indent=2), encoding="utf-8")

    # Optional viewer data copy, not yet replacing the live handcrafted map
    (DOCS_DATA / "truth-map-generated-preview.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")

    print(f"Generated {len(nodes)} nodes and {len(edges)} edges.")
    print("Wrote 003-machine-readable/truth-graph-generated.json")
    print("Wrote 003-machine-readable/topology-health-report-generated.json")

if __name__ == "__main__":
    generate()
