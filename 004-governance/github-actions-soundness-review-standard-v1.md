# GitHub Actions Soundness Review Standard v1

## Purpose

This document defines GitHub-native automated soundness review for UTE.

## Workflow File

```text
.github/workflows/ute-soundness-review.yml
```

## Trigger Events

The workflow runs on:

- pushes to `main`,
- pull requests to `main`,
- manual workflow dispatch.

## Review Command

The workflow runs:

```bash
python 006-tools/soundness-review/run-soundness-review-v1.py
```

## Where Results Appear

Results appear under:

```text
GitHub → Actions → UTE Soundness Review
```

The generated report is uploaded as a workflow artifact:

```text
ute-soundness-review-report
```

## Relationship to Structural Assurance

UTE now separates:

```text
UTE Assurance
    structural repository integrity

UTE Soundness Review
    conceptual/proof-quality review risk
```

## Final Principle

Structural correctness and conceptual soundness are related but distinct review layers.
