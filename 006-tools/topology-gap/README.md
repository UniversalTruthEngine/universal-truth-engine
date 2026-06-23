# Topology Gap Detector v1

## Purpose

Detects simple topology gaps in the UTE truth graph.

Version 1 detects frontier boundary nodes:

```text
truths with no downstream dependants
```

## Run

```bash
python 006-tools/topology-gap/detect-topology-gaps-v1.py
```

## Output

```text
003-machine-readable/topology-gap-report-v1.json
docs/data/topology-gap-report-v1.json
```

A topology gap is not a truth. It is a review signal.
