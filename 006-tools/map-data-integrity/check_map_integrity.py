#!/usr/bin/env python3
"""
UTE Map Data Integrity Checker v1

Checks alignment between:
- 001-fact-vault/**/metadata.json
- docs/data/truth-map-v1.json
- docs/data/truth-map-generated-preview.json if present

Usage from repo root:
python 006-tools/map-data-integrity/check_map_integrity.py
"""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / "001-fact-vault"
DOCS_DATA = ROOT / "docs" / "data"
OUT = ROOT / "003-machine-readable"

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def vault_truths():
    truths = {}
    for path in VAULT.rglob("metadata.json"):
        data = read_json(path)
        if not data or not data.get("id"):
            continue
        truths[data["id"]] = {
            "metadata": path,
            "folder": path.parent,
            "data": data
        }
    return truths

def map_nodes(path):
    data = read_json(path)
    if not data:
        return {}
    return {n.get("id"): n for n in data.get("nodes", []) if n.get("id")}

def check():
    truths = vault_truths()
    curated = map_nodes(DOCS_DATA / "truth-map-v1.json")
    generated = map_nodes(DOCS_DATA / "truth-map-generated-preview.json")

    truth_ids = set(truths)
    curated_ids = set(curated)
    generated_ids = set(generated)

    missing_from_curated = sorted(truth_ids - curated_ids)
    missing_from_generated = sorted(truth_ids - generated_ids) if generated_ids else []
    curated_not_in_vault = sorted(curated_ids - truth_ids)
    generated_not_in_vault = sorted(generated_ids - truth_ids) if generated_ids else []

    missing_files = []
    missing_dependency_refs = []

    for tid, item in truths.items():
        folder = item["folder"]
        data = item["data"]
        entry = folder / data.get("entry_file", "entry.md")
        proof = folder / data.get("proof_file", "proof.md")
        if not entry.exists():
            missing_files.append({"id": tid, "missing": "entry.md"})
        if not proof.exists():
            missing_files.append({"id": tid, "missing": "proof.md"})
        for dep in data.get("dependencies", []):
            if dep not in truth_ids:
                missing_dependency_refs.append({"id": tid, "missing_dependency": dep})

    report = {
        "generated_by": "UTE Map Data Integrity Checker v1",
        "vault_truth_count": len(truth_ids),
        "curated_map_node_count": len(curated_ids),
        "generated_preview_node_count": len(generated_ids),
        "missing_from_curated_map": missing_from_curated,
        "missing_from_generated_preview": missing_from_generated,
        "curated_nodes_not_in_vault": curated_not_in_vault,
        "generated_nodes_not_in_vault": generated_not_in_vault,
        "missing_files": missing_files,
        "missing_dependency_references": missing_dependency_refs
    }

    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "map-data-integrity-generated-v1.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    check()
