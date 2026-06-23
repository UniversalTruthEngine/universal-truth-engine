# Arithmetic Duplicate / Continuity Review v1

## Purpose

Review duplicate or overlapping arithmetic truths introduced during the transition from the original arithmetic cluster to the M2-A arithmetic expansion.

This is a governance continuity issue, not an Assurance failure.

---

## Current Issue

The UTE currently contains overlapping arithmetic entries:

```text
UTE-FV-0004 — Addition
UTE-FV-0102 — Addition

UTE-FV-0005 — Subtraction
UTE-FV-0103 — Subtraction
```

The repository remains structurally valid because:

```text
UTE Assurance: PASS
Truth Index: synchronised
Truth Graph: synchronised
Missing dependencies: none
```

However, duplicate concepts can weaken future candidate generation and topology reasoning.

---

## Why This Matters

The Truth Frontier and Candidate Generation systems rely on:

- clean identity of concepts,
- stable dependency chains,
- non-duplicated topology,
- unambiguous enablement relationships.

If two truths represent the same concept, the engine may incorrectly treat them as separate nodes.

---

## Review Questions

For each duplicate pair:

1. Are the statements meaningfully different?
2. Are the dependency sets different?
3. Is one entry more mature or better integrated?
4. Should one truth supersede the other?
5. Should one become a historical alias?
6. Should the newer M2-A entry replace the earlier arithmetic entry?
7. Should both remain but be distinguished by scope?

---

## Preliminary Assessment

### Addition

```text
UTE-FV-0004 — Addition
UTE-FV-0102 — Addition
```

Likely resolution:

```text
Retain one authoritative Addition truth.
Mark the other as superseded, alias, or historical.
```

### Subtraction

```text
UTE-FV-0005 — Subtraction
UTE-FV-0103 — Subtraction
```

Likely resolution:

```text
Retain one authoritative Subtraction truth.
Mark the other as superseded, alias, or historical.
```

---

## Recommended Governance Direction

UTE should not delete historical truths casually.

Instead, use a controlled status such as:

```text
superseded_by
historical_alias
merged_into
```

This preserves auditability while preventing topology confusion.

---

## Proposed Resolution Strategy

1. Compare old and new entries.
2. Select authoritative versions.
3. Add supersession metadata.
4. Update topology if needed.
5. Regenerate truth index and graph.
6. Run Assurance and Soundness Review.

---

## Governance Principle

A concept should have one authoritative active Core Truth unless there is a clear scope distinction.
