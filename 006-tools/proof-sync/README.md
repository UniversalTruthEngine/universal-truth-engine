# UTE Browser Proof Sync v1

## Purpose

This tool copies Fact Vault proof files into the browser-served GitHub Pages proof folder.

## Why This Exists

The live UTE cosmos map is served from:

```text
docs/
```

The browser cannot reliably fetch proof files from outside the served site context.

Therefore proof copies are required here:

```text
docs/data/proofs/
```

## Usage

Run from repository root:

```bash
python 006-tools/proof-sync/sync-browser-proofs-v1.py
```

## Reads

```text
001-fact-vault/UTE-FV-XXXX/proof.md
```

## Writes

```text
docs/data/proofs/UTE-FV-XXXX-proof.md
003-machine-readable/browser-proof-sync-report-v1.json
```

## Principle

The Fact Vault remains the source of truth.

The browser proof folder is a serving layer only.
