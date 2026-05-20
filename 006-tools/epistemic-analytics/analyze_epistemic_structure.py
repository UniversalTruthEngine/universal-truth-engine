#!/usr/bin/env python3
"""
UTE Epistemic Analytics v1

Scans 001-fact-vault/**/metadata.json and produces:
- 003-machine-readable/epistemic-analytics-generated-v1.json

Usage:
python 006-tools/epistemic-analytics/analyze_epistemic_structure.py
"""

from pathlib import Path
import json
from collections import defaultdict, deque

ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / "001-fact-vault"
OUT = ROOT / "003-machine-readable"

def load_truths():
    truths = {}
    for path in VAULT.rglob("metadata.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        tid = data.get("id")
        if not tid:
            continue
        data["_metadata_path"] = path
        data["_folder"] = path.parent
        truths[tid] = data
    return truths

def recursive_dependents(target, reverse):
    seen = set()
    queue = deque(reverse.get(target, []))
    while queue:
        item = queue.popleft()
        if item in seen:
            continue
        seen.add(item)
        queue.extend(reverse.get(item, []))
    return seen

def proof_score(folder):
    proof = folder / "proof.md"
    entry = folder / "entry.md"
    review = folder / "review-history.md"
    metadata = folder / "metadata.json"
    score = 0
    total = 4
    if metadata.exists(): score += 1
    if entry.exists(): score += 1
    if review.exists(): score += 1
    if proof.exists() and len(proof.read_text(encoding="utf-8", errors="ignore")) > 1000:
        score += 1
    elif proof.exists():
        score += 0.5
    return score / total

def main():
    truths = load_truths()
    reverse = defaultdict(list)
    missing_dependencies = []

    for tid, truth in truths.items():
        for dep in truth.get("dependencies", []):
            if dep not in truths:
                missing_dependencies.append({"truth": tid, "missing_dependency": dep})
            reverse[dep].append(tid)

    nodes = []
    for tid, truth in truths.items():
        direct = reverse.get(tid, [])
        recursive = recursive_dependents(tid, reverse)
        score = proof_score(truth["_folder"])
        risk_flags = []

        if score < 0.75:
            risk_flags.append("proof_incomplete")
        if len(direct) >= 3 and score < 0.75:
            risk_flags.append("high_centrality_weak_proof")
        if not truth.get("domain"):
            risk_flags.append("domain_missing")
        if truth.get("confidence_level") is None:
            risk_flags.append("confidence_missing")
        if not truth.get("dependencies") and not direct:
            risk_flags.append("orphan_node_or_root_candidate")

        nodes.append({
            "id": tid,
            "title": truth.get("title", ""),
            "domain": truth.get("domain", ""),
            "dependency_centrality": len(direct),
            "recursive_dependency_centrality": len(recursive),
            "proof_completeness_score": score,
            "risk_flags": risk_flags
        })

    nodes_sorted = sorted(nodes, key=lambda x: x["dependency_centrality"], reverse=True)

    output = {
        "generated_by": "UTE Epistemic Analytics v1",
        "truth_count": len(truths),
        "missing_dependencies": missing_dependencies,
        "highest_dependency_centrality": nodes_sorted[:10],
        "risk_nodes": [n for n in nodes if n["risk_flags"]],
        "all_nodes": sorted(nodes, key=lambda x: x["id"])
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "epistemic-analytics-generated-v1.json").write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"Analysed {len(truths)} truths.")
    print("Wrote 003-machine-readable/epistemic-analytics-generated-v1.json")

if __name__ == "__main__":
    main()
