# Automated Truth Index and Graph Generation v1

## Purpose

Generates UTE truth registry files directly from the Fact Vault.

## Run

```bash
python 006-tools/topology/generate-truth-index-and-graph-v1.py
```

## Reads

```text
001-fact-vault/UTE-FV-*/metadata.json
```

## Writes

```text
003-machine-readable/truth-index-v1.json
003-machine-readable/truth-graph.json
```

## Why This Exists

Manual maintenance of the truth index and graph does not scale.

Whenever new truths are added to the Fact Vault, the index and graph should be regenerated from metadata.
