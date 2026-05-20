# 2026-05-20 — Browser Proof Access Fix v1

## Purpose

This update addressed proof files not being accessible from the live GitHub Pages map.

## Issue

The live map attempted to load proof files from paths outside the browser-served `docs/` directory.

This caused messages such as:

```text
Proof file not available in browser path.
```

## Resolution

Browser-accessible proof copies were added under:

```text
docs/data/proofs/
```

and map node proof paths were updated to reference those browser-accessible files.

## Architectural Note

The Fact Vault remains the source of truth.

The browser proof files are serving copies for the live map and should eventually be generated automatically.
