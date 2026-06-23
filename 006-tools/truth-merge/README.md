# Truth Merge Review Engine v1

## Purpose

Detects duplicate and near-duplicate truth concepts in the UTE truth index.

## Run

```bash
python 006-tools/truth-merge/truth-merge-review-engine-v1.py
```

## Input

```text
003-machine-readable/truth-index-v1.json
```

## Outputs

```text
003-machine-readable/truth-merge-review-report-v1.json
003-machine-readable/truth-merge-review-report-v1.md
docs/data/truth-merge-review-report-v1.json
```

## Principle

The merge engine does not merge, delete, or supersede truths.

It only produces a review report.
