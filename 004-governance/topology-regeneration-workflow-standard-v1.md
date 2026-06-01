# Topology Regeneration Workflow Standard v1

## Purpose

Defines the proper workflow order for UTE automated assurance.

## Core Principle

The Fact Vault is the source of truth.

Before assurance runs, derived topology files should be regenerated from Fact Vault metadata.

## Required Workflow Order

```text
1. Check out repository
2. Set up Python
3. Regenerate truth index and graph
4. Run UTE Assurance
5. Upload generated topology and assurance report artifacts
```

## Generated Files

```text
003-machine-readable/truth-index-v1.json
003-machine-readable/truth-graph.json
```

## Why This Matters

Manual updates to registry files do not scale.

As UTE expands, stale topology files should not block assurance when the Fact Vault metadata is valid and the generator can rebuild the topology.

## Important Note

This workflow regenerates topology files inside the GitHub Actions run.

A later enhancement may commit regenerated files back to the repository or integrate generation into the GitHub Pages build process.
