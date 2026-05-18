# Reference Truth Schema v1

## Purpose

This schema defines the standard structure for UTE Core Truth entries.

Every Core Truth should be understandable by:

- humans,
- future artificial intelligences,
- future low-technology societies,
- and other possible intelligent systems.

---

## Required Fields

Each Core Truth entry should contain:

1. Stable ID
2. Title
3. Category
4. Claim
5. Confidence Level
6. Conditions of Validity
7. Failure Cases
8. Proof / Evidence
9. Dependency Chain
10. Applications
11. Reconstruction Protocol
12. Human Reconstruction Difficulty
13. Compression Risk
14. Common Misconceptions
15. Civilisational Leverage
16. Ethical Hazard Level
17. Validation Assessment
18. Admission Decision
19. Last Review Date
20. Machine-readable Metadata

---

## Recommended Folder Structure

```text
UTE-FV-000X-entry-title/
  entry.md
  validation.md
  derivation.md
  reconstruction.md
  dependencies.md
  machine-readable.json
  review-history.md
  diagrams/
```

---

## Stable ID Rule

Stable IDs must not be changed after assignment.

Example:

```text
UTE-FV-0001
```

The folder title may evolve, but the stable ID should remain permanent.

---

## Review Rule

Substantive changes should be recorded in `review-history.md`.

UTE should avoid silent rewriting of truth entries.
