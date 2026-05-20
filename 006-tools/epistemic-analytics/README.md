# UTE Epistemic Analytics v1

This tool analyses the structure of the Universal Truth Engine truth graph.

## Usage

From the repository root:

```bash
python 006-tools/epistemic-analytics/analyze_epistemic_structure.py
```

## Output

```text
003-machine-readable/epistemic-analytics-generated-v1.json
```

## Current Metrics

- dependency centrality
- recursive dependency centrality
- proof completeness score
- missing dependencies
- high-centrality weak-proof risk
- orphan/root candidates
