#!/usr/bin/env python3
"""
UTE Browser Proof Sync v1

Purpose:
    Copy Fact Vault proof files into the browser-served docs/data/proofs folder.

Run from repository root:

    python 006-tools/proof-sync/sync-browser-proofs-v1.py

Reads:
    001-fact-vault/UTE-FV-XXXX/proof.md

Writes:
    docs/data/proofs/UTE-FV-XXXX-proof.md

Important:
    The Fact Vault proof.md files remain the source of truth.
    docs/data/proofs/ contains browser-serving copies for GitHub Pages.
"""

from pathlib import Path
import json

ROOT = Path.cwd()
VAULT = ROOT / "001-fact-vault"
PROOFS_OUT = ROOT / "docs" / "data" / "proofs"
MACHINE = ROOT / "003-machine-readable"

def main():
    if not VAULT.exists():
        raise SystemExit("ERROR: 001-fact-vault does not exist. Run from repository root.")

    PROOFS_OUT.mkdir(parents=True, exist_ok=True)
    MACHINE.mkdir(parents=True, exist_ok=True)

    synced = []
    missing = []

    for folder in sorted(VAULT.glob("UTE-FV-*")):
        if not folder.is_dir():
            continue

        truth_id = folder.name
        proof = folder / "proof.md"

        if not proof.exists():
            missing.append(truth_id)
            continue

        target = PROOFS_OUT / f"{truth_id}-proof.md"
        text = proof.read_text(encoding="utf-8", errors="replace")
        target.write_text(text, encoding="utf-8")
        synced.append(truth_id)

    report = {
        "report_id": "UTE-BROWSER-PROOF-SYNC-V1",
        "synced_count": len(synced),
        "synced_truths": synced,
        "missing_proofs": missing,
        "output_folder": "docs/data/proofs"
    }

    report_path = MACHINE / "browser-proof-sync-report-v1.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"Synced {len(synced)} browser proof files.")
    if missing:
        print("Missing proof.md files:")
        for item in missing:
            print("-", item)
    print("Wrote 003-machine-readable/browser-proof-sync-report-v1.json")

if __name__ == "__main__":
    main()
