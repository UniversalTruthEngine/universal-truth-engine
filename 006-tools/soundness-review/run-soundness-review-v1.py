#!/usr/bin/env python3
"""
UTE Core Truth Soundness Review v1

Run from repository root:

    python 006-tools/soundness-review/run-soundness-review-v1.py

Purpose:
    Performs a lightweight conceptual soundness review of Core Truth entries.

This does not prove truths automatically.
It flags review risks for human/AI inspection.
"""

from pathlib import Path
import json
import re

ROOT = Path.cwd()
VAULT = ROOT / "001-fact-vault"
MACHINE = ROOT / "003-machine-readable"

RISK_WORDS = [
    "always",
    "never",
    "obvious",
    "clearly",
    "simply",
    "absolute",
    "universal",
    "undeniable"
]

REQUIRED_PROOF_SECTIONS = [
    "Claim",
    "Plain-Language Explanation",
    "Dependencies",
    "Reconstruction Method",
    "Conditions of Validity",
    "Failure Cases"
]

def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__error__": str(exc)}

def has_heading(text, heading):
    pattern = r"^##\s+" + re.escape(heading) + r"\s*$"
    return re.search(pattern, text, flags=re.MULTILINE) is not None

def review_truth(folder):
    tid = folder.name
    entry_path = folder / "entry.md"
    proof_path = folder / "proof.md"
    metadata_path = folder / "metadata.json"

    entry = read_text(entry_path)
    proof = read_text(proof_path)
    metadata = read_json(metadata_path) if metadata_path.exists() else {}

    warnings = []
    strengths = []

    if not entry:
        warnings.append("Missing or empty entry.md.")
    else:
        strengths.append("Entry file present.")

    if not proof:
        warnings.append("Missing or empty proof.md.")
    else:
        strengths.append("Proof file present.")

    if not metadata_path.exists():
        warnings.append("Missing metadata.json.")
    elif "__error__" in metadata:
        warnings.append("metadata.json is invalid JSON.")
    else:
        strengths.append("Metadata file present and parseable.")
        if metadata.get("id") != tid:
            warnings.append("Metadata ID does not match folder ID.")
        if not metadata.get("dependencies") and tid not in ["UTE-FV-0015"]:
            warnings.append("No dependencies listed; check whether this is genuinely foundational.")
        if not metadata.get("statement") and not metadata.get("claim"):
            warnings.append("Metadata lacks statement/claim field.")

    if proof:
        for heading in REQUIRED_PROOF_SECTIONS:
            if not has_heading(proof, heading):
                warnings.append(f"Proof missing section: {heading}")

        if len(proof.split()) < 120:
            warnings.append("Proof appears short; may need deeper explanation.")

        lower = proof.lower()
        found_risk_words = [word for word in RISK_WORDS if word in lower]
        if found_risk_words:
            warnings.append("Potential overclaiming language present: " + ", ".join(sorted(set(found_risk_words))))

    if entry:
        if "## Statement" not in entry and "## Claim" not in entry:
            warnings.append("Entry lacks clear Statement or Claim section.")
        if "## Dependencies" not in entry:
            warnings.append("Entry lacks Dependencies section.")

    risk_level = "low"
    if len(warnings) >= 5:
        risk_level = "high"
    elif len(warnings) >= 2:
        risk_level = "medium"

    return {
        "id": tid,
        "risk_level": risk_level,
        "warnings": warnings,
        "strengths": strengths,
        "recommended_action": "Review required" if warnings else "No immediate action"
    }

def main():
    MACHINE.mkdir(parents=True, exist_ok=True)

    if not VAULT.exists():
        raise SystemExit("ERROR: 001-fact-vault not found. Run from repository root.")

    reviews = []
    for folder in sorted(VAULT.glob("UTE-FV-*")):
        if folder.is_dir():
            reviews.append(review_truth(folder))

    high = [r for r in reviews if r["risk_level"] == "high"]
    medium = [r for r in reviews if r["risk_level"] == "medium"]

    report = {
        "report_id": "UTE-CORE-TRUTH-SOUNDNESS-REVIEW-V1",
        "generated_by": "UTE Core Truth Soundness Review v1",
        "truth_count": len(reviews),
        "high_risk_count": len(high),
        "medium_risk_count": len(medium),
        "review_scope": [
            "statement clarity",
            "proof section completeness",
            "metadata consistency",
            "dependency presence",
            "overclaiming language",
            "proof depth heuristic"
        ],
        "reviews": reviews,
        "recommended_next_steps": [
            "Prioritise high-risk truths for human review.",
            "Improve proof depth for short proofs.",
            "Add missing proof sections.",
            "Check dependency choices for truths with no dependencies.",
            "Treat this as a triage tool, not an automated proof validator."
        ]
    }

    out = MACHINE / "core-truth-soundness-review-v1.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("UTE Core Truth Soundness Review v1 complete.")
    print(f"Truths reviewed: {len(reviews)}")
    print(f"High risk: {len(high)}")
    print(f"Medium risk: {len(medium)}")
    print(f"Report written to: {out}")

if __name__ == "__main__":
    main()
