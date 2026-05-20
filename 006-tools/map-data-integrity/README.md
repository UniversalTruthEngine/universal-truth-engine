# UTE Map Data Integrity Checker v1

This tool checks whether the Fact Vault and map data are aligned.

## Usage

From repository root:

```bash
python 006-tools/map-data-integrity/check_map_integrity.py
```

## Output

```text
003-machine-readable/map-data-integrity-generated-v1.json
```

## Checks

- Core Truths missing from curated map
- Core Truths missing from generated preview
- map nodes not found in Fact Vault
- missing proof files
- missing entry files
- missing dependency references
