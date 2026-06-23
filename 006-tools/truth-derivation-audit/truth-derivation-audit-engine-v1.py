#!/usr/bin/env python3
"""
UTE Truth Derivation Audit Engine v1

Run from repository root:

    python 006-tools/truth-derivation-audit/truth-derivation-audit-engine-v1.py

Purpose:
    Explain why candidate truths were proposed from existing truths.

This tool does not admit truths.
It audits derivation reasoning only.

Reads:
    003-machine-readable/truth-index-v1.json
    003-machine-readable/truth-graph.json

Writes:
    003-machine-readable/truth-derivation-audit-report-v1.json
    003-machine-readable/truth-derivation-audit-report-v1.md
    docs/data/truth-derivation-audit-report-v1.json
"""

from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path.cwd()
MACHINE = ROOT / "003-machine-readable"
DOCS_DATA = ROOT / "docs" / "data"

INDEX_PATH = MACHINE / "truth-index-v1.json"
GRAPH_PATH = MACHINE / "truth-graph.json"

OUT_JSON_INTERNAL = MACHINE / "truth-derivation-audit-report-v1.json"
OUT_MD_INTERNAL = MACHINE / "truth-derivation-audit-report-v1.md"
OUT_JSON_PUBLIC = DOCS_DATA / "truth-derivation-audit-report-v1.json"

DERIVATION_AUDIT_RULES = [
    {
        "audit_id": "UTE-DA-0001",
        "candidate_title": "Multiplication",
        "source_titles": ["Addition"],
        "derivation_claim": "Repeated addition motivates multiplication.",
        "reasoning_steps": [
            "Addition combines quantities.",
            "Repeated application of addition creates structured repeated combination.",
            "A compact operation for repeated addition is multiplication."
        ],
        "expected_status_if_present": "already_present_chain",
        "derivation_type": "iteration"
    },
    {
        "audit_id": "UTE-DA-0002",
        "candidate_title": "Exponents",
        "source_titles": ["Multiplication"],
        "derivation_claim": "Repeated multiplication motivates exponents.",
        "reasoning_steps": [
            "Multiplication combines equal factors.",
            "Repeated multiplication creates a recurring operation pattern.",
            "A compact notation and truth for repeated multiplication is exponents."
        ],
        "expected_status_if_present": "already_present_chain",
        "derivation_type": "iteration"
    },
    {
        "audit_id": "UTE-DA-0003",
        "candidate_title": "Division",
        "source_titles": ["Multiplication"],
        "derivation_claim": "The inverse or partitioning question associated with multiplication motivates division.",
        "reasoning_steps": [
            "Multiplication combines factors into a product.",
            "One can ask what factor or equal group produced the product.",
            "That inverse or partitioning relation is captured by division."
        ],
        "expected_status_if_present": "already_present_chain",
        "derivation_type": "inverse_operation"
    },
    {
        "audit_id": "UTE-DA-0004",
        "candidate_title": "Integer",
        "source_titles": ["Natural Number", "Negative Numbers"],
        "derivation_claim": "Natural numbers and negative numbers motivate a unified whole-number class.",
        "reasoning_steps": [
            "Natural numbers represent counting values.",
            "Negative numbers represent values below a defined zero point.",
            "A unified whole-number class can include positive whole numbers, zero, and negative whole numbers."
        ],
        "expected_status_if_present": "already_present_chain",
        "derivation_type": "number_system_extension"
    },
    {
        "audit_id": "UTE-DA-0005",
        "candidate_title": "Space",
        "source_titles": ["Point", "Position", "Separation / Distance", "Direction", "Line", "Plane", "Dimension"],
        "derivation_claim": "Several geometry truths imply a shared spatial framework.",
        "reasoning_steps": [
            "Point represents position without dimension.",
            "Position, distance, direction, line, plane, and dimension all rely on spatial relations.",
            "A shared framework for these relations can be represented as Space."
        ],
        "expected_status_if_present": "candidate_review_required",
        "derivation_type": "shared_framework_abstraction"
    },
    {
        "audit_id": "UTE-DA-0006",
        "candidate_title": "Numerical Representation",
        "source_titles": ["Number", "Ratio", "Measurement", "Scale"],
        "derivation_claim": "Arithmetic and measurement require a bridge explaining how quantities are represented numerically.",
        "reasoning_steps": [
            "Number represents quantity, order, or relation.",
            "Ratio compares quantities.",
            "Measurement compares a target against a reference.",
            "Scale defines how measured values correspond to ordered positions or ratios.",
            "Together these imply a bridge truth: numerical representation."
        ],
        "expected_status_if_present": "candidate_review_required",
        "derivation_type": "bridge_abstraction"
    }
]

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm(text):
    return (text or "").strip().lower()

def main():
    if not INDEX_PATH.exists():
        raise SystemExit("ERROR: truth-index-v1.json not found.")
    if not GRAPH_PATH.exists():
        raise SystemExit("ERROR: truth-graph.json not found.")

    index = read_json(INDEX_PATH)
    graph = read_json(GRAPH_PATH)

    truths = index.get("truths", [])
    title_to_truths = {}
    known_titles = set()

    for truth in truths:
        title = truth.get("title", "")
        if title:
            known_titles.add(norm(title))
            title_to_truths.setdefault(norm(title), []).append(truth)

    audits = []

    for rule in DERIVATION_AUDIT_RULES:
        source_truths = []
        missing_sources = []

        for source_title in rule["source_titles"]:
            matches = title_to_truths.get(norm(source_title), [])
            if matches:
                for match in matches:
                    source_truths.append({
                        "id": match.get("id"),
                        "title": match.get("title"),
                        "domain": match.get("domain"),
                        "statement": match.get("statement"),
                        "dependencies": match.get("dependencies", [])
                    })
            else:
                missing_sources.append(source_title)

        candidate_matches = title_to_truths.get(norm(rule["candidate_title"]), [])
        candidate_already_exists = bool(candidate_matches)

        if missing_sources:
            audit_status = "blocked_missing_sources"
        elif candidate_already_exists:
            audit_status = "already_present"
        else:
            audit_status = "candidate_review_required"

        duplicate_risk = "high" if candidate_already_exists else "low"

        audits.append({
            "audit_id": rule["audit_id"],
            "candidate_title": rule["candidate_title"],
            "derivation_type": rule["derivation_type"],
            "derivation_claim": rule["derivation_claim"],
            "reasoning_steps": rule["reasoning_steps"],
            "source_truths": source_truths,
            "missing_sources": missing_sources,
            "candidate_already_exists": candidate_already_exists,
            "existing_candidate_matches": [
                {
                    "id": match.get("id"),
                    "title": match.get("title"),
                    "domain": match.get("domain"),
                    "statement": match.get("statement"),
                    "dependencies": match.get("dependencies", [])
                }
                for match in candidate_matches
            ],
            "duplicate_risk": duplicate_risk,
            "audit_status": audit_status,
            "recommended_action": (
                "review_as_duplicate_or_existing_chain"
                if candidate_already_exists else
                "send_to_candidate_review"
                if not missing_sources else
                "do_not_proceed_until_sources_exist"
            )
        })

    report = {
        "report_id": "UTE-TRUTH-DERIVATION-AUDIT-REPORT-V1",
        "generated_by": "UTE Truth Derivation Audit Engine v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "truth_count": len(truths),
        "graph_node_count": graph.get("node_count", len(graph.get("nodes", []))),
        "graph_edge_count": graph.get("edge_count", len(graph.get("edges", []))),
        "audit_count": len(audits),
        "audits": audits,
        "governance_rule": "Derivation audit explains candidate reasoning. It does not admit truths."
    }

    MACHINE.mkdir(parents=True, exist_ok=True)
    DOCS_DATA.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    OUT_JSON_INTERNAL.write_text(json_text, encoding="utf-8")
    OUT_JSON_PUBLIC.write_text(json_text, encoding="utf-8")

    md = [
        "# UTE Truth Derivation Audit Report v1",
        "",
        f"Generated by: {report['generated_by']}",
        f"Truth count: {report['truth_count']}",
        f"Graph nodes: {report['graph_node_count']}",
        f"Graph edges: {report['graph_edge_count']}",
        f"Audit count: {report['audit_count']}",
        "",
        "Derivation audit explains why candidate truths were proposed. It does not admit truths.",
        ""
    ]

    for audit in audits:
        md.extend([
            f"## {audit['candidate_title']}",
            "",
            f"Audit ID: `{audit['audit_id']}`",
            f"Derivation type: `{audit['derivation_type']}`",
            f"Audit status: `{audit['audit_status']}`",
            f"Duplicate risk: `{audit['duplicate_risk']}`",
            f"Recommended action: `{audit['recommended_action']}`",
            "",
            "### Derivation claim",
            "",
            audit["derivation_claim"],
            "",
            "### Reasoning steps",
            ""
        ])
        for step in audit["reasoning_steps"]:
            md.append(f"- {step}")

        md.extend(["", "### Source truths", ""])
        if not audit["source_truths"]:
            md.append("No source truths found.")
        for source in audit["source_truths"]:
            md.append(f"- `{source['id']}` — {source['title']} ({source.get('domain')})")

        md.extend(["", "### Existing candidate matches", ""])
        if not audit["existing_candidate_matches"]:
            md.append("No existing candidate match found.")
        for match in audit["existing_candidate_matches"]:
            md.append(f"- `{match['id']}` — {match['title']} ({match.get('domain')})")

        md.append("")

    OUT_MD_INTERNAL.write_text("\n".join(md), encoding="utf-8")

    print("UTE Truth Derivation Audit Engine v1 complete.")
    print("Truths:", len(truths))
    print("Audits:", len(audits))
    for audit in audits:
        print("-", audit["candidate_title"], audit["audit_status"], "duplicate risk:", audit["duplicate_risk"])
    print("Wrote:", OUT_JSON_INTERNAL)
    print("Wrote:", OUT_MD_INTERNAL)
    print("Wrote:", OUT_JSON_PUBLIC)

if __name__ == "__main__":
    main()
