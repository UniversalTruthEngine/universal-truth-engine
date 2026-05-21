# Core Truth Soundness Review Standard v1

## Purpose

Defines the conceptual soundness review layer for UTE Core Truths.

## Core Principle

Structural validity is not enough.

A Core Truth should also be reviewed for:

- conceptual clarity,
- dependency soundness,
- proof adequacy,
- reconstruction usefulness,
- domain fit,
- and overclaiming risk.

## Review Classification

Recommended review levels:

| Level | Meaning |
|---|---|
| low | no immediate issue detected |
| medium | review recommended |
| high | review required before major expansion |

## Important Limitation

This review is not an automated proof engine.

It is a triage layer for identifying where human or AI review should focus.

## Output

```text
003-machine-readable/core-truth-soundness-review-v1.json
```

## Final Principle

UTE should evaluate not only whether files exist, but whether truths are clear, bounded, and reconstructable.
