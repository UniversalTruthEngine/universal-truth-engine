# Map Data Standard v1

## Purpose

This document defines how Core Truth data should connect to the UTE interactive map.

The map should remain aligned with the Fact Vault. Every visible node should correspond to a real Core Truth entry, and every Core Truth intended for display should have valid metadata, proof links, and dependency data.

---

## Core Rule

The map is not the source of truth.

The Fact Vault and machine-readable metadata are the source of truth.

The map is a navigational interface.

---

## Required Map Node Fields

Each map node should include:

- `id`
- `title`
- `domain`
- `confidence_level`
- `dependencies`
- `dependency_centrality`
- `summary`
- `entry_file`
- `proof_file`
- `metadata_file`

---

## Required Map Edge Fields

Each map edge should include:

- `source`
- `target`
- `type`
- `weight`

The default edge type is:

```text
depends_on
```

---

## Integrity Requirements

A valid map node should satisfy:

1. The node ID exists in the Fact Vault.
2. The node has metadata.
3. The node has a proof file.
4. The node has an entry file.
5. All dependencies point to existing Core Truth IDs.
6. The node's domain is defined.
7. The node's confidence level is defined.

---

## Curated and Generated Map Alignment

UTE may maintain both:

- curated map data,
- generated map preview data.

These should be periodically compared.

If a truth appears in the Fact Vault but not in the map, it should be flagged.

If a map node does not exist in the Fact Vault, it should be flagged.

---

## Final Principle

The visual universe should remain faithful to the underlying archive.
