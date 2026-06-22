#!/usr/bin/env python3
"""
UTE Automated Truth Index and Graph Generator v1

Generates both internal and public topology files from Fact Vault metadata.
"""

from pathlib import Path
import json
import math

ROOT = Path.cwd()
VAULT = ROOT / "001-fact-vault"
MACHINE = ROOT / "003-machine-readable"
DOCS_DATA = ROOT / "docs" / "data"

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "id": path.parent.name,
            "title": path.parent.name,
            "domain": "Unknown",
            "statement": "",
            "dependencies": [],
            "error": str(exc)
        }

def truth_number(tid):
    try:
        return int(tid.replace("UTE-FV-", ""))
    except Exception:
        return 999999

def stable_coordinate(index, total):
    angle = (2 * math.pi * index) / max(total, 1)
    radius = 120 + (index % 5) * 35
    return {
        "x": round(math.cos(angle) * radius, 3),
        "y": round(math.sin(angle) * radius, 3),
        "z": (index % 7) * 25 - 75
    }

def main():
    if not VAULT.exists():
        raise SystemExit("ERROR: 001-fact-vault not found. Run from repository root.")

    MACHINE.mkdir(parents=True, exist_ok=True)
    DOCS_DATA.mkdir(parents=True, exist_ok=True)

    truth_folders = sorted(
        [p for p in VAULT.glob("UTE-FV-*") if p.is_dir()],
        key=lambda p: truth_number(p.name)
    )

    truths = []
    for folder in truth_folders:
        metadata_path = folder / "metadata.json"
        metadata = read_json(metadata_path) if metadata_path.exists() else {}

        tid = metadata.get("id") or folder.name
        title = metadata.get("title") or tid
        domain = metadata.get("domain") or metadata.get("category") or "Unknown"
        statement = metadata.get("statement") or metadata.get("claim") or ""
        dependencies = metadata.get("dependencies") or []
        if not isinstance(dependencies, list):
            dependencies = []

        truths.append({
            "id": tid,
            "title": title,
            "domain": domain,
            "category": domain,
            "statement": statement,
            "confidence_level": metadata.get("confidence", metadata.get("confidence_level", 5)),
            "dependencies": dependencies,
            "summary": f"{title} is a Core Truth in the Universal Truth Engine.",
            "entry_file": "../001-fact-vault/" + tid + "/entry.md",
            "proof_file": "../001-fact-vault/" + tid + "/proof.md",
            "metadata_file": "../001-fact-vault/" + tid + "/metadata.json"
        })

    ids = {t["id"] for t in truths}
    depended_on_by = {tid: [] for tid in ids}
    edges = []

    for truth in truths:
        for dep in truth["dependencies"]:
            if dep in ids:
                edges.append({
                    "source": truth["id"],
                    "target": dep,
                    "type": "depends_on",
                    "weight": 1.0
                })
                depended_on_by[dep].append(truth["id"])

    total = len(truths)
    for idx, truth in enumerate(truths):
        tid = truth["id"]
        truth["depended_on_by"] = sorted(depended_on_by.get(tid, []), key=truth_number)
        truth["dependency_centrality"] = len(truth["depended_on_by"])
        truth["recursive_dependency_centrality"] = 0
        truth["bridge_score"] = 1 if "/" in truth.get("domain", "") else 0
        truth["stable_coordinates"] = stable_coordinate(idx, total)

    index = {
        "index_id": "UTE-TRUTH-INDEX-V1",
        "generated_by": "UTE Automated Truth Index and Graph Generator v1",
        "truth_count": len(truths),
        "truths": [
            {
                "id": t["id"],
                "title": t["title"],
                "domain": t["domain"],
                "statement": t["statement"],
                "dependencies": t["dependencies"],
                "entry_file": t["entry_file"],
                "proof_file": t["proof_file"],
                "metadata_file": t["metadata_file"]
            }
            for t in truths
        ]
    }

    graph = {
        "map_id": "UTE-TRUTH-GRAPH-V1",
        "generated_by": "UTE Automated Truth Index and Graph Generator v1",
        "node_count": len(truths),
        "edge_count": len(edges),
        "nodes": truths,
        "edges": edges
    }

    index_text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    graph_text = json.dumps(graph, indent=2, ensure_ascii=False) + "\n"

    (MACHINE / "truth-index-v1.json").write_text(index_text, encoding="utf-8")
    (MACHINE / "truth-graph.json").write_text(graph_text, encoding="utf-8")
    (DOCS_DATA / "truth-index-v1.json").write_text(index_text, encoding="utf-8")
    (DOCS_DATA / "truth-map-v1.json").write_text(graph_text, encoding="utf-8")

    print("UTE topology generation complete.")
    print(f"Truths: {len(truths)}")
    print(f"Edges: {len(edges)}")
    print("Wrote: 003-machine-readable/truth-index-v1.json")
    print("Wrote: 003-machine-readable/truth-graph.json")
    print("Wrote: docs/data/truth-index-v1.json")
    print("Wrote: docs/data/truth-map-v1.json")

if __name__ == "__main__":
    main()
