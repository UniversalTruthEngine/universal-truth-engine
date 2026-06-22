#!/usr/bin/env python3
"""
UTE Truth Frontier Engine v1

Run from repository root:

    python 006-tools/truth-frontier/generate-truth-frontier-v1.py

Purpose:
    Identify candidate next truths enabled by the current truth network.

This tool does not accept truths automatically.
It only proposes frontier candidates for human and LLM review.

Reads:
    003-machine-readable/truth-index-v1.json
    003-machine-readable/truth-derivation-schema-v1.json
    002-truth-topology/arithmetic-frontier-seeds-v1.json

Writes:
    003-machine-readable/truth-frontier-candidates-v1.json
"""

from pathlib import Path
import json

ROOT = Path.cwd()
MACHINE = ROOT / "003-machine-readable"
TOPOLOGY = ROOT / "002-truth-topology"

INDEX_PATH = MACHINE / "truth-index-v1.json"
SEEDS_PATH = TOPOLOGY / "arithmetic-frontier-seeds-v1.json"
OUT_PATH = MACHINE / "truth-frontier-candidates-v1.json"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    if not INDEX_PATH.exists():
        raise SystemExit("ERROR: truth-index-v1.json not found. Run topology generator first.")

    if not SEEDS_PATH.exists():
        raise SystemExit("ERROR: arithmetic-frontier-seeds-v1.json not found.")

    index = read_json(INDEX_PATH)
    seeds = read_json(SEEDS_PATH)

    known_ids = {truth["id"] for truth in index.get("truths", [])}
    known_titles = {truth.get("title", "").lower() for truth in index.get("truths", [])}

    candidates = []

    for seed in seeds.get("frontier_candidates", []):
        title = seed.get("proposed_title", "")
        required = set(seed.get("enabled_by", []))
        already_known = title.lower() in known_titles
        enabled = required.issubset(known_ids)

        if enabled and not already_known:
            candidates.append({
                "candidate_id": seed.get("candidate_id"),
                "proposed_title": title,
                "proposed_statement": seed.get("proposed_statement"),
                "enabled_by": seed.get("enabled_by", []),
                "depends_on": seed.get("depends_on", []),
                "derivation_class": seed.get("derivation_class", "derived_truth"),
                "derivation_rationale": seed.get("derivation_rationale", ""),
                "review_status": "candidate",
                "recommended_next_action": "Human and LLM review required before Fact Vault admission."
            })

    report = {
        "report_id": "UTE-TRUTH-FRONTIER-CANDIDATES-V1",
        "generated_by": "UTE Truth Frontier Engine v1",
        "known_truth_count": len(known_ids),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "governance_rule": "Candidate truths are proposals only. They require human/LLM review and must pass assurance and soundness before admission."
    }

    OUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("UTE Truth Frontier Engine v1 complete.")
    print(f"Known truths: {len(known_ids)}")
    print(f"Candidate frontier truths: {len(candidates)}")
    print(f"Wrote: {OUT_PATH}")

if __name__ == "__main__":
    main()
