#!/usr/bin/env python3
"""
UTE Automated Assurance Tool v1

Run from repository root:
python 006-tools/assurance/run-assurance-v1.py
"""

from pathlib import Path
import json
import sys

ROOT = Path.cwd()
VAULT = ROOT / "001-fact-vault"
DOCS_DATA = ROOT / "docs" / "data"
MACHINE = ROOT / "003-machine-readable"

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__error__": str(exc)}

def collect_truths():
    truths = {}
    errors = []
    if not VAULT.exists():
        errors.append("001-fact-vault folder missing.")
        return truths, errors

    for folder in sorted(VAULT.glob("UTE-FV-*")):
        if not folder.is_dir():
            continue
        tid = folder.name
        entry = folder / "entry.md"
        proof = folder / "proof.md"
        metadata = folder / "metadata.json"
        data = {}

        if metadata.exists():
            data = read_json(metadata)
            if "__error__" in data:
                errors.append(f"{tid}: metadata.json invalid JSON: {data['__error__']}")
            elif data.get("id") != tid:
                errors.append(f"{tid}: metadata id does not match folder name.")
        else:
            errors.append(f"{tid}: missing metadata.json")

        if not entry.exists():
            errors.append(f"{tid}: missing entry.md")
        if not proof.exists():
            errors.append(f"{tid}: missing proof.md")

        truths[tid] = {
            "metadata": data,
            "entry_exists": entry.exists(),
            "proof_exists": proof.exists(),
            "metadata_exists": metadata.exists()
        }

    return truths, errors

def check_dependencies(truths):
    ids = set(truths.keys())
    missing = []
    self_refs = []

    for tid, item in truths.items():
        deps = item.get("metadata", {}).get("dependencies", [])
        if not isinstance(deps, list):
            missing.append({"truth": tid, "issue": "dependencies is not a list"})
            continue
        for dep in deps:
            if dep not in ids:
                missing.append({"truth": tid, "missing_dependency": dep})
            if dep == tid:
                self_refs.append(tid)

    return missing, self_refs

def find_package_readmes():
    found = []
    for path in ROOT.rglob("PACKAGE-README.md"):
        if ".git" not in path.parts:
            found.append(str(path.relative_to(ROOT)).replace("\\", "/"))
    return found

def check_index_map(truths):
    truth_ids = set(truths.keys())
    result = {
        "truth_index_exists": False,
        "truth_map_exists": False,
        "truth_index_json_valid": False,
        "truth_map_json_valid": False,
        "truth_index_count": None,
        "truth_map_node_count": None,
        "missing_from_index": [],
        "extra_in_index": [],
        "missing_from_map": [],
        "extra_in_map": [],
        "map_edges_with_missing_ids": []
    }

    index_path = DOCS_DATA / "truth-index-v1.json"
    map_path = DOCS_DATA / "truth-map-v1.json"

    if index_path.exists():
        result["truth_index_exists"] = True
        index = read_json(index_path)
        if "__error__" not in index:
            result["truth_index_json_valid"] = True
            index_ids = {item.get("id") for item in index.get("truths", []) if item.get("id")}
            result["truth_index_count"] = len(index_ids)
            result["missing_from_index"] = sorted(truth_ids - index_ids)
            result["extra_in_index"] = sorted(index_ids - truth_ids)

    if map_path.exists():
        result["truth_map_exists"] = True
        graph = read_json(map_path)
        if "__error__" not in graph:
            result["truth_map_json_valid"] = True
            map_ids = {item.get("id") for item in graph.get("nodes", []) if item.get("id")}
            result["truth_map_node_count"] = len(map_ids)
            result["missing_from_map"] = sorted(truth_ids - map_ids)
            result["extra_in_map"] = sorted(map_ids - truth_ids)

            for edge in graph.get("edges", []):
                if edge.get("source") not in truth_ids or edge.get("target") not in truth_ids:
                    result["map_edges_with_missing_ids"].append(edge)

    return result

def check_browser_proofs(truths):
    missing = []
    for tid in sorted(truths.keys()):
        path = DOCS_DATA / "proofs" / f"{tid}-proof.md"
        if not path.exists():
            missing.append(tid)
    return missing

def main():
    MACHINE.mkdir(parents=True, exist_ok=True)

    truths, vault_errors = collect_truths()
    missing_dependencies, self_refs = check_dependencies(truths)
    package_readmes = find_package_readmes()
    index_map = check_index_map(truths)
    missing_browser_proofs = check_browser_proofs(truths)

    failures = []
    failures.extend(vault_errors)

    if missing_dependencies:
        failures.append("Missing dependency references detected.")
    if self_refs:
        failures.append("Self-referential dependencies detected.")
    if package_readmes:
        failures.append("Deprecated PACKAGE-README.md files detected.")
    if index_map["missing_from_index"] or index_map["extra_in_index"]:
        failures.append("Truth index does not match Fact Vault.")
    if index_map["missing_from_map"] or index_map["extra_in_map"]:
        failures.append("Truth map does not match Fact Vault.")
    if index_map["map_edges_with_missing_ids"]:
        failures.append("Truth map has edges referencing missing IDs.")
    if missing_browser_proofs:
        failures.append("Browser proof copies missing.")

    status = "pass" if not failures else "fail"

    report = {
        "report_id": "UTE-AUTOMATED-ASSURANCE-GENERATED-V1",
        "generated_by": "UTE Automated Assurance Tool v1",
        "status": status,
        "truth_count": len(truths),
        "failures": failures,
        "vault_errors": vault_errors,
        "missing_dependencies": missing_dependencies,
        "self_referential_dependencies": self_refs,
        "deprecated_package_readmes": package_readmes,
        "index_and_map_checks": index_map,
        "missing_browser_proofs": missing_browser_proofs,
        "recommendation": "Proceed" if status == "pass" else "Repair failures before external review or major expansion."
    }

    out = MACHINE / "assurance-report-generated-v1.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"UTE Automated Assurance Tool v1: {status.upper()}")
    print(f"Truth count: {len(truths)}")
    print(f"Report written to: {out}")

    if failures:
        print("\nFailures:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

if __name__ == "__main__":
    main()
