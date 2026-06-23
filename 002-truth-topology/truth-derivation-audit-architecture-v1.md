# Truth Derivation Audit Architecture v1

## Purpose

Place derivation audit between candidate generation and candidate scoring.

## Flow

```text
Truth Graph
    ↓
Candidate Generation
    ↓
Derivation Audit
    ↓
Duplicate / Merge Review
    ↓
Candidate Scoring
    ↓
Human + LLM Review
    ↓
Fact Vault Admission
```

## Strategic Importance

The UTE should not merely say:

```text
I propose this truth.
```

It should say:

```text
I propose this truth because these prior truths imply this derivation path.
```
