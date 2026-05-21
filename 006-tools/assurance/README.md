# UTE Automated Assurance Tool v1

## Purpose

Runs automated structural checks across the Universal Truth Engine repository.

## Usage

Run from repository root:

```bash
python 006-tools/assurance/run-assurance-v1.py
```

## Checks

- Fact Vault truth folders exist
- each truth has `entry.md`, `proof.md`, and `metadata.json`
- metadata IDs match folder names
- dependencies resolve to known truth IDs
- `docs/data/truth-index-v1.json` matches the Fact Vault
- `docs/data/truth-map-v1.json` matches the Fact Vault
- browser proof files exist under `docs/data/proofs/`
- no deprecated `PACKAGE-README.md` files exist

## Output

```text
003-machine-readable/assurance-report-generated-v1.json
```
