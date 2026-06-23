# Truth Arithmetic Engine Protocol v1

## Purpose

Define how UTE may infer possible next truths from existing truth chains.

## Core Idea

Some truths naturally enable later truths.

Examples:

```text
Addition -> Multiplication
Multiplication -> Exponents
Multiplication -> Division
Division + Fractions -> Ratio
Ratio + Equality -> Proportion
```

## Governance Rule

Truth Arithmetic may propose derivation candidates.

It may not admit them.

## Review Requirements

Each proposed candidate must be reviewed for:

- dependency validity,
- minimality,
- truthfulness,
- reconstructability,
- counterexample resistance,
- duplicate avoidance,
- domain fit.

## Strategic Role

This is the first explicit UTE component that attempts to move from existing truths toward possible next truths using controlled derivation logic.
