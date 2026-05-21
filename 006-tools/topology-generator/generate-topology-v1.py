#!/usr/bin/env python3
"""
UTE Automated Topology Generator v1

Run from repository root:
python 006-tools/topology-generator/generate-topology-v1.py
"""

from pathlib import Path
import json
import math
from collections import defaultdict

ROOT = Path.cwd()
VAULT = ROOT / "001-fact-vault"
DOCS_DATA = ROOT / "docs" / "data"
MACHINE = ROOT / "003-machine-readable"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def confidence_value(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        for n in ["5", "4", "3", "2", "1"]:
            if n in value:
                return int(n)
    return 5

def load_truths():
    truths = {}
    for meta in sorted(VAULT.rglob("metadata.json")):
        data = read_json(meta)
        tid = data.get("id") or meta.parent.name
        title = data.get("title") or tid
        statement = data.get("statement") or data.get("claim") or data.get("summary") or ""
        domain = data.get("domain") or data.get("category") or "Unclassified"
        dependencies = data.get("dependencies") or []
        if not isinstance(dependencies, list):
            dependencies = []
        folder = meta.parent
        truths[tid] = {
            "id": tid,
            "title": title,
            "statement": statement,
            "domain": domain,
            "dependencies": dependencies,
            "confidence_level": confidence_value(data.get("confidence") or data.get("confidence_level")),
            "metadata_file": str(meta.relative_to(ROOT)).replace("\\", "/"),
            "entry_file": str((folder / "entry.md").relative_to(ROOT)).replace("\\", "/"),
            "repo_proof_file": str((folder / "proof.md").relative_to(ROOT)).replace("\\", "/"),
            "entry_exists": (folder / "entry.md").exists(),
            "proof_exists": (folder / "proof.md").exists()
        }
    return truths

def coordinate(i, truth):
    tid = truth["id"]
    domain = truth["domain"]
    if tid == "UTE-FV-0015":
        return {"x": 0, "y": 0, "z": 0}
    if tid == "UTE-FV-0002":
        return {"x": 40, "y": -25, "z": 20}
    if "Logic" in domain and "Measurement" not in domain and "Arithmetic" not in domain:
        return {"x": round(math.cos(i * 0.73) * 120, 2), "y": round(120 + math.sin(i * 0.73) * 80, 2), "z": (i % 4) * 35}
    if "Arithmetic" in domain:
        return {"x": round(-190 + math.cos(i * 0.48) * 125, 2), "y": round(-65 + math.sin(i * 0.48) * 135, 2), "z": ((i % 5) - 2) * 36}
    if "Measurement" in domain and "Geometry" not in domain:
        return {"x": round(175 + math.cos(i * 0.54) * 130, 2), "y": round(-85 + math.sin(i * 0.54) * 140, 2), "z": ((i % 5) - 2) * 42}
    if "Geometry" in domain:
        return {"x": round(80 + math.cos(i * 0.61) * 145, 2), "y": round(120 + math.sin(i * 0.61) * 120, 2), "z": 105 + ((i % 4) - 2) * 34}
    return {"x": round(math.cos(i * 0.5) * 100, 2), "y": round(math.sin(i * 0.5) * 100, 2), "z": 0}

def generate():
    truths = load_truths()
    if not truths:
        raise SystemExit("No metadata.json files found.")

    ids = set(truths)
    reverse = defaultdict(list)
    edges = []
    missing_dependencies = []

    for tid, truth in truths.items():
        for dep in truth["dependencies"]:
            edges.append({"source": tid, "target": dep, "type": "depends_on", "weight": 1.0})
            reverse[dep].append(tid)
            if dep not in ids:
                missing_dependencies.append({"truth": tid, "missing_dependency": dep})

    nodes = []
    missing_entries = []
    missing_proofs = []
    missing_browser_proofs = []

    for i, tid in enumerate(sorted(truths)):
        truth = truths[tid]
        if not truth["entry_exists"]:
            missing_entries.append(tid)
        if not truth["proof_exists"]:
            missing_proofs.append(tid)
        browser_proof = DOCS_DATA / "proofs" / f"{tid}-proof.md"
        if not browser_proof.exists():
            missing_browser_proofs.append(tid)
        depended_on_by = sorted(reverse.get(tid, []))
        nodes.append({
            "id": tid,
            "title": truth["title"],
            "domain": truth["domain"],
            "category": truth["domain"],
            "confidence_level": truth["confidence_level"],
            "dependencies": truth["dependencies"],
            "depended_on_by": depended_on_by,
            "dependency_centrality": len(depended_on_by),
            "summary": truth["statement"] or f"{truth['title']} is a Core Truth in the Universal Truth Engine.",
            "stable_coordinates": coordinate(i, truth),
            "entry_file": truth["entry_file"],
            "proof_file": f"data/proofs/{tid}-proof.md",
            "metadata_file": truth["metadata_file"]
        })

    truth_index = {
        "index_id": "UTE-TRUTH-INDEX-GENERATED-V1",
        "generated_by": "UTE Automated Topology Generator v1",
        "truth_count": len(nodes),
        "highest_truth_id": sorted(ids)[-1],
        "truths": [{"id": n["id"], "title": n["title"], "domain": n["domain"], "dependencies": n["dependencies"]} for n in nodes]
    }

    truth_map = {
        "map_id": "UTE-TRUTH-MAP-GENERATED-V1",
        "generated_by": "UTE Automated Topology Generator v1",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges
    }

    health = {
        "report_id": "UTE-TOPOLOGY-HEALTH-GENERATED-V1",
        "truth_count": len(nodes),
        "edge_count": len(edges),
        "missing_dependencies": missing_dependencies,
        "missing_entries": missing_entries,
        "missing_proofs": missing_proofs,
        "missing_browser_proofs": missing_browser_proofs,
        "high_centrality_nodes": sorted(
            [{"id": n["id"], "title": n["title"], "dependency_centrality": n["dependency_centrality"]} for n in nodes],
            key=lambda x: x["dependency_centrality"],
            reverse=True
        )[:10]
    }

    write_json(DOCS_DATA / "truth-index-v1.json", truth_index)
    write_json(DOCS_DATA / "truth-map-v1.json", truth_map)
    write_json(DOCS_DATA / "truth-map-generated-preview.json", truth_map)
    write_json(DOCS_DATA / "topology-health-preview.json", health)

    write_json(MACHINE / "truth-index-v1.json", truth_index)
    write_json(MACHINE / "truth-graph-generated-v1.json", truth_map)
    write_json(MACHINE / "topology-health-generated-v1.json", health)

    print(f"Generated {len(nodes)} truths and {len(edges)} dependency links.")
    if missing_dependencies:
        print("WARNING: missing dependencies detected.")
    if missing_browser_proofs:
        print("NOTICE: missing browser proof copies detected.")

if __name__ == "__main__":
    generate()
