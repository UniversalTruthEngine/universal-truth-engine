# UTE Topology Generator v1

This tool generates machine-readable topology data from Core Truth metadata.

## Usage

From the repository root:

```bash
python 006-tools/topology-generator/generate_topology.py
```

## Outputs

```text
003-machine-readable/truth-graph-generated.json
003-machine-readable/topology-health-report-generated.json
docs/data/truth-map-generated-preview.json
```

## Current Status

This is an architectural first step.

It does not yet replace the live map data automatically.
