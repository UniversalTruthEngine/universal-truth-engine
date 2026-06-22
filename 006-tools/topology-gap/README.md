# Topology Gap Tools

## Purpose

Future home of UTE tools for detecting incomplete regions of the truth topology.

## Planned Tool

```bash
python 006-tools/topology-gap/detect-topology-gaps-v1.py
```

## Intended Input

```text
003-machine-readable/truth-graph.json
docs/data/truth-map-v1.json
```

## Intended Output

```text
003-machine-readable/topology-gap-report-v1.json
```

## Principle

Gap detection identifies possible missing regions.

It does not create truths.
