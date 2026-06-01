# 2026-06-01 — M2-A.2 Topology Regeneration Workflow v1

## Purpose

Updates the UTE Assurance workflow so truth index and graph files are regenerated before assurance runs.

## Updated File

```text
.github/workflows/ute-assurance.yml
```

## Strategic Importance

This fixes the M2-A expansion failure where the Fact Vault contained more truths than the truth index and graph.

The workflow now follows:

```text
Fact Vault
    ↓
Generate truth index and graph
    ↓
Run assurance
```
