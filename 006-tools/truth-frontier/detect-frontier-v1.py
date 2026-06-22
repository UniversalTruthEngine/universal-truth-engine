#!/usr/bin/env python3
"""
UTE Automated Frontier Detection v1

Run from repository root:

    python 006-tools/truth-frontier/detect-frontier-v1.py

Purpose:
    Detect plausible next candidate truths from the current UTE truth network.

This tool does not accept truths.
It generates review candidates only.

Reads:
    003-machine-readable/truth-index-v1.json

Writes:
    003-machine-readable/truth-frontier-report-v1.json
"""

from pathlib import Path
import json

ROOT = Path.cwd()
MACHINE = ROOT / "003-machine-readable"

INDEX_PATH = MACHINE / "truth-index-v1.json"
OUT_PATH = MACHINE / "truth-frontier-report-v1.json"

# Initial controlled derivation rules.
# These are deliberately conservative and arithmetic-focused.
DERIVATION_RULES = [
    {
        "candidate_id": "UTE-FV-CAND-AUTO-0001",
        "proposed_title": "Fraction",
        "proposed_statement": "A fraction represents a quantity as a ratio or division of quantities.",
        "requires_titles": ["Division", "Ratio"],
        "depends_on_titles": ["Number", "Division", "Ratio"],
        "derivation_class": "derived_truth",
        "confidence": 0.92,
        "rationale": "Division and ratio together enable part-whole and quotient representation."
    },
    {
        "candidate_id": "UTE-FV-CAND-AUTO-0002",
        "proposed_title": "Proportion",
        "proposed_statement": "A proportion is an equality between ratios.",
        "requires_titles": ["Ratio", "Equality / Identity of Quantity"],
        "depends_on_titles": ["Ratio", "Equality / Identity of Quantity"],
        "derivation_class": "composite_truth",
        "confidence": 0.88,
        "rationale": "Ratio combined with equality enables equal-ratio relationships."
    },
    {
        "candidate_id": "UTE-FV-CAND-AUTO-0003",
        "proposed_title": "Integer",
        "proposed_statement": "An integer is a whole number that may represent positive quantity, zero, or negative quantity.",
        "requires_titles": ["Natural Number", "Subtraction"],
        "depends_on_titles": ["Natural Number", "Subtraction"],
        "derivation_class": "derived_truth",
        "confidence": 0.82,
        "rationale": "Natural numbers and subtraction motivate extension to zero and negative whole-number values."
    },
    {
        "candidate_id": "UTE-FV-CAND-AUTO-0004",
        "proposed_title": "Scale",
        "proposed_statement": "Scale is a consistent ratio-based relationship between representation and reference.",
        "requires_titles": ["Measurement", "Ratio"],
        "depends_on_titles": ["Measurement", "Ratio"],
        "derivation_class": "emergent_truth",
        "confidence": 0.76,
        "rationale": "Measurement and ratio enable scaled representation relative to a reference."
    }
]

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm(title):
    return (title or "").strip().lower()

def main():
    if not INDEX_PATH.exists():
        raise SystemExit("ERROR: truth-index-v1.json not found. Run topology generator first.")

    index = read_json(INDEX_PATH)
    truths = index.get("truths", [])

    title_to_id = {}
    known_titles = set()

    for truth in truths:
        title = truth.get("title", "")
        tid = truth.get("id", "")
        if title:
            known_titles.add(norm(title))
            title_to_id[norm(title)] = tid

    candidates = []

    for rule in DERIVATION_RULES:
        candidate_title = norm(rule["proposed_title"])

        # Do not propose truths already present.
        if candidate_title in known_titles:
            continue

        required = [norm(t) for t in rule.get("requires_titles", [])]
        requirements_met = [t for t in required if t in known_titles]
        requirements_missing = [t for t in required if t not in known_titles]

        if not requirements_missing:
            depends_on = []
            for title in rule.get("depends_on_titles", []):
                tid = title_to_id.get(norm(title))
                if tid:
                    depends_on.append(tid)

            candidates.append({
                "candidate_id": rule["candidate_id"],
                "proposed_title": rule["proposed_title"],
                "proposed_statement": rule["proposed_statement"],
                "depends_on": depends_on,
                "enabled_by_titles": rule["requires_titles"],
                "derivation_class": rule["derivation_class"],
                "confidence": rule["confidence"],
                "derivation_rationale": rule["rationale"],
                "review_status": "candidate",
                "recommended_next_action": "Human and LLM review before Fact Vault admission."
            })

    report = {
        "report_id": "UTE-AUTOMATED-FRONTIER-REPORT-V1",
        "generated_by": "UTE Automated Frontier Detection v1",
        "known_truth_count": len(truths),
        "candidate_count": len(candidates),
        "candidates": sorted(candidates, key=lambda c: c["confidence"], reverse=True),
        "governance_rule": "Automated frontier detection proposes candidate truths only. It does not accept them."
    }

    OUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("UTE Automated Frontier Detection v1 complete.")
    print(f"Known truths: {len(truths)}")
    print(f"Candidates detected: {len(candidates)}")
    for candidate in report["candidates"]:
        print(f"- {candidate['proposed_title']} ({candidate['confidence']})")
    print(f"Wrote: {OUT_PATH}")

if __name__ == "__main__":
    main()
