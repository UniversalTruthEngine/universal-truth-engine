#!/usr/bin/env python3
"""
UTE Truth Arithmetic Engine v1

Run from repository root:

    python 006-tools/truth-arithmetic/truth-arithmetic-engine-v1.py

Purpose:
    Identify truth-to-truth derivation chains and propose next truths
    from the existing UTE truth graph.

This tool does not admit truths.
It proposes derivation candidates for review.

Reads:
    003-machine-readable/truth-graph.json
    or docs/data/truth-map-v1.json

Writes:
    003-machine-readable/truth-arithmetic-report-v1.json
    003-machine-readable/truth-arithmetic-report-v1.md
    docs/data/truth-arithmetic-report-v1.json
"""

from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path.cwd()
MACHINE = ROOT / "003-machine-readable"
DOCS_DATA = ROOT / "docs" / "data"

GRAPH_CANDIDATES = [
    MACHINE / "truth-graph.json",
    DOCS_DATA / "truth-map-v1.json"
]

OUT_JSON_INTERNAL = MACHINE / "truth-arithmetic-report-v1.json"
OUT_MD_INTERNAL = MACHINE / "truth-arithmetic-report-v1.md"
OUT_JSON_PUBLIC = DOCS_DATA / "truth-arithmetic-report-v1.json"

TRUTH_ARITHMETIC_RULES = [
    {
        "chain_id": "UTE-TA-0001",
        "given_titles": ["Addition"],
        "candidate_title": "Multiplication",
        "candidate_statement": "Multiplication represents repeated addition or scaling by a quantity.",
        "derivation_pattern": "iteration",
        "confidence": 0.91,
        "rationale": "If addition combines quantities, repeated addition naturally enables multiplication."
    },
    {
        "chain_id": "UTE-TA-0002",
        "given_titles": ["Multiplication"],
        "candidate_title": "Exponents",
        "candidate_statement": "Exponents represent repeated multiplication.",
        "derivation_pattern": "iteration",
        "confidence": 0.89,
        "rationale": "If multiplication combines repeated equal factors, repeated multiplication naturally enables exponents."
    },
    {
        "chain_id": "UTE-TA-0003",
        "given_titles": ["Multiplication"],
        "candidate_title": "Division",
        "candidate_statement": "Division is the inverse or partitioning counterpart of multiplication.",
        "derivation_pattern": "inverse_operation",
        "confidence": 0.86,
        "rationale": "Multiplication implies the possibility of asking what factor or partition produced a product."
    },
    {
        "chain_id": "UTE-TA-0004",
        "given_titles": ["Division", "Fractions"],
        "candidate_title": "Ratio",
        "candidate_statement": "A ratio compares quantities through relative division or proportional relation.",
        "derivation_pattern": "comparison",
        "confidence": 0.84,
        "rationale": "Division and fractions enable comparison of one quantity with another."
    },
    {
        "chain_id": "UTE-TA-0005",
        "given_titles": ["Ratio", "Equality of Quantity"],
        "candidate_title": "Proportion",
        "candidate_statement": "A proportion states equality between ratios.",
        "derivation_pattern": "equality_relation",
        "confidence": 0.88,
        "rationale": "Ratio combined with equality enables the concept of equal ratios."
    },
    {
        "chain_id": "UTE-TA-0006",
        "given_titles": ["Natural Number", "Negative Numbers"],
        "candidate_title": "Integer",
        "candidate_statement": "An integer is a whole number that may be positive, zero, or negative.",
        "derivation_pattern": "number_system_extension",
        "confidence": 0.82,
        "rationale": "Natural numbers and negative numbers suggest a unified whole-number system."
    },
    {
        "chain_id": "UTE-TA-0007",
        "given_titles": ["Point", "Position", "Separation / Distance", "Direction", "Line", "Plane", "Dimension"],
        "candidate_title": "Space",
        "candidate_statement": "Space is the structured domain in which positions, distances, directions, dimensions, and geometric relations can be represented.",
        "derivation_pattern": "shared_framework_abstraction",
        "confidence": 0.74,
        "rationale": "Multiple geometry truths rely on an implicit spatial framework not yet represented as an explicit Core Truth."
    },
    {
        "chain_id": "UTE-TA-0008",
        "given_titles": ["Number", "Ratio", "Measurement", "Scale"],
        "candidate_title": "Numerical Representation",
        "candidate_statement": "Numerical representation maps quantities, measurements, or relations into numbers within a defined reference context.",
        "derivation_pattern": "bridge_abstraction",
        "confidence": 0.78,
        "rationale": "Number, ratio, measurement, and scale together bridge arithmetic and measurable reality."
    }
]

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def choose_graph():
    for path in GRAPH_CANDIDATES:
        if path.exists():
            return path
    raise SystemExit("ERROR: no truth graph found. Run topology generator first.")

def norm(text):
    return (text or "").strip().lower()

def main():
    graph_path = choose_graph()
    graph = read_json(graph_path)

    nodes = graph.get("nodes", [])
    title_to_nodes = {}
    known_titles = set()

    for node in nodes:
        title = node.get("title", "")
        if title:
            known_titles.add(norm(title))
            title_to_nodes.setdefault(norm(title), []).append(node)

    derivations = []
    already_known = []

    for rule in TRUTH_ARITHMETIC_RULES:
        required = [norm(t) for t in rule["given_titles"]]
        missing = [t for t in required if t not in known_titles]
        candidate_known = norm(rule["candidate_title"]) in known_titles

        depends_on = []
        for title in rule["given_titles"]:
            for node in title_to_nodes.get(norm(title), []):
                tid = node.get("id")
                if tid and tid not in depends_on:
                    depends_on.append(tid)

        record = {
            "chain_id": rule["chain_id"],
            "given_titles": rule["given_titles"],
            "depends_on": depends_on,
            "candidate_title": rule["candidate_title"],
            "candidate_statement": rule["candidate_statement"],
            "derivation_pattern": rule["derivation_pattern"],
            "confidence": rule["confidence"],
            "rationale": rule["rationale"],
            "review_status": "candidate" if not candidate_known and not missing else "not_actionable",
            "candidate_already_exists": candidate_known,
            "missing_required_titles": missing
        }

        if not missing and not candidate_known:
            derivations.append(record)
        elif not missing and candidate_known:
            record["review_status"] = "already_present"
            already_known.append(record)

    report = {
        "report_id": "UTE-TRUTH-ARITHMETIC-REPORT-V1",
        "generated_by": "UTE Truth Arithmetic Engine v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "graph_source": str(graph_path),
        "truth_count": len(nodes),
        "active_derivation_candidate_count": len(derivations),
        "already_present_chain_count": len(already_known),
        "active_derivation_candidates": sorted(derivations, key=lambda x: x["confidence"], reverse=True),
        "already_present_chains": sorted(already_known, key=lambda x: x["confidence"], reverse=True),
        "governance_rule": "Truth arithmetic proposes next truths from derivation chains. It does not admit truths."
    }

    MACHINE.mkdir(parents=True, exist_ok=True)
    DOCS_DATA.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    OUT_JSON_INTERNAL.write_text(json_text, encoding="utf-8")
    OUT_JSON_PUBLIC.write_text(json_text, encoding="utf-8")

    md = [
        "# UTE Truth Arithmetic Report v1",
        "",
        f"Generated by: {report['generated_by']}",
        f"Truth count: {report['truth_count']}",
        f"Active derivation candidates: {report['active_derivation_candidate_count']}",
        f"Already-present chains: {report['already_present_chain_count']}",
        "",
        "Truth arithmetic proposes next truths from derivation chains. It does not admit truths.",
        "",
        "## Active Derivation Candidates",
        ""
    ]

    if not report["active_derivation_candidates"]:
        md.append("No active derivation candidates detected.")
        md.append("")

    for item in report["active_derivation_candidates"]:
        md.extend([
            f"### {item['candidate_title']}",
            "",
            f"Chain ID: `{item['chain_id']}`",
            f"Pattern: `{item['derivation_pattern']}`",
            f"Confidence: `{item['confidence']}`",
            "",
            "Given truths:",
            ""
        ])
        for title in item["given_titles"]:
            md.append(f"- {title}")
        md.extend([
            "",
            "Proposed statement:",
            "",
            item["candidate_statement"],
            "",
            "Rationale:",
            "",
            item["rationale"],
            ""
        ])

    md.extend([
        "## Already-Present Derivation Chains",
        ""
    ])

    for item in report["already_present_chains"]:
        md.extend([
            f"### {item['candidate_title']}",
            "",
            f"Pattern: `{item['derivation_pattern']}`",
            f"Confidence: `{item['confidence']}`",
            "",
            "Status: already present in Fact Vault.",
            ""
        ])

    OUT_MD_INTERNAL.write_text("\n".join(md), encoding="utf-8")

    print("UTE Truth Arithmetic Engine v1 complete.")
    print("Graph source:", graph_path)
    print("Truths:", len(nodes))
    print("Active derivation candidates:", len(derivations))
    for item in report["active_derivation_candidates"]:
        print("-", item["candidate_title"], "(" + str(item["confidence"]) + ")")
    print("Already-present chains:", len(already_known))
    print("Wrote:", OUT_JSON_INTERNAL)
    print("Wrote:", OUT_MD_INTERNAL)
    print("Wrote:", OUT_JSON_PUBLIC)

if __name__ == "__main__":
    main()
