# Generated Map Integration v1

## Purpose

This document defines the first integration stage between the live UTE map and metadata-generated topology data.

The goal is to transition gradually from a handcrafted map to a map generated from Core Truth metadata.

---

## Strategy

Use dual-mode operation.

The map should support:

1. curated map mode,
2. generated preview mode.

This allows comparison before fully replacing the live map.

---

## Why Dual Mode

A generated graph may initially have:

- imperfect positioning,
- incomplete metadata,
- missing coordinates,
- rough clustering,
- or unexpected topology shape.

Dual mode allows the system to improve safely.

---

## Generated Data Source

Generated topology should eventually come from:

```text
003-machine-readable/truth-graph-generated.json
```

and optionally be copied into:

```text
docs/data/truth-map-generated-preview.json
```

for browser loading.

---

## Required Generated Fields

Each node should include:

- id,
- title,
- domain,
- confidence_level,
- dependencies,
- proof_file,
- entry_file,
- dependency_centrality,
- recursive_dependency_centrality,
- bridge_score.

---

## UI Requirements

Generated Map Integration v1 should expose:

- mode selector,
- generated topology preview,
- topology health summary,
- fallback if generated data is missing,
- and explanation that generated mode is experimental.

---

## Final Principle

The live UTE cosmos should eventually emerge from truth metadata rather than manual map definitions.
