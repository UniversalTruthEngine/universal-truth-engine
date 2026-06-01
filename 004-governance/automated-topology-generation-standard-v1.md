# Automated Topology Generation Standard v1

## Purpose

Define the rule that UTE topology registry files should be generated from the Fact Vault wherever possible.

## Core Principle

The Fact Vault is the source of truth.

Derived files such as truth indexes and truth graphs should be generated from Fact Vault metadata.

## Required Generated Files

```text
003-machine-readable/truth-index-v1.json
003-machine-readable/truth-graph.json
```

## Governance Rule

After adding, removing, or editing Core Truth metadata, the topology generator should be run before Assurance.

## Strategic Importance

This prevents drift between:

- Fact Vault,
- truth index,
- truth graph,
- Cosmos map,
- and assurance reports.
