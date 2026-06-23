# Topology Gap Detector Operational Protocol v1

## Purpose

Define how to interpret output from the first topology gap detector.

## What Version 1 Detects

Version 1 detects frontier boundary nodes:

```text
truths that currently have no downstream dependants
```

## Review Flow

```text
Gap detected
    ↓
Human + LLM review
    ↓
Possible candidate generation
    ↓
Candidate review
    ↓
Fact Vault admission or dismissal
```
