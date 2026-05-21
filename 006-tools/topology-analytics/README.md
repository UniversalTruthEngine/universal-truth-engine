# UTE Topology Analytics v1

## Purpose

Analyses the UTE truth topology and produces machine-readable analytics.

## Usage

Run from repository root:

```bash
python 006-tools/topology-analytics/analyze-topology-v1.py
```

## Reads

```text
docs/data/truth-map-v1.json
docs/data/truth-index-v1.json
```

## Writes

```text
003-machine-readable/topology-analytics-v1.json
docs/data/topology-analytics-preview.json
```

## Metrics

The tool calculates:

- highest centrality truths,
- root truths,
- isolated truths,
- leaf truths with dependencies,
- deepest dependency chains,
- domain summary,
- bridge truths,
- dependency density.

## Why This Matters

Topology analytics helps UTE identify:

- foundational bottlenecks,
- weak proof areas,
- conceptual bridges,
- orphaned regions,
- and future expansion priorities.
