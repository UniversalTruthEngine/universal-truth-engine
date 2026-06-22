# Automated Frontier Detection Architecture v1

## Purpose

Describe the first self-building loop in UTE.

## Loop

```text
Truth Vault
    ↓
Generated Truth Index
    ↓
Automated Frontier Detection
    ↓
Candidate Truth Report
    ↓
Human + LLM Review
    ↓
Fact Vault Admission
```

## Current Limitation

Version 1 uses controlled derivation rules.

Future versions should infer candidates from richer topology patterns, enables links, contradiction structure, and proof gaps.
