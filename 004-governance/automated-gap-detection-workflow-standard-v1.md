# Automated Gap Detection Workflow Standard v1

## Purpose

Defines the GitHub Actions workflow order for automatic topology gap detection.

## Workflow Order

```text
1. Check out repository
2. Set up Python
3. Regenerate truth index and truth graph
4. Run UTE Assurance
5. Detect topology gaps
6. Upload generated topology files
7. Upload topology gap report
8. Upload assurance report
```

## Generated Gap Report

```text
003-machine-readable/topology-gap-report-v1.json
docs/data/topology-gap-report-v1.json
```

## Governance Principle

Topology gap detection is diagnostic.

A detected gap is not a truth and is not automatically admitted to the Fact Vault.
