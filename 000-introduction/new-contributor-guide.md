# New Contributor Guide

## Purpose

This guide explains how to safely contribute to the Universal Truth Engine (UTE).

UTE is not intended to become an unstructured collection of facts.

Every contribution should preserve:
- clarity,
- reconstructability,
- dependency integrity,
- proof quality,
- and long-term epistemic stability.

---

# Core Principle

UTE stores:

- Core Truths,
- dependency relationships,
- proof structures,
- and reconstructable knowledge pathways.

Contributors should prioritise:
- precision over speed,
- structure over volume,
- and clarity over complexity.

---

# Required Structure for a Core Truth

Each Core Truth should contain:

```text
entry.md
proof.md
metadata.json
```

inside a dedicated folder:

```text
001-fact-vault/UTE-FV-XXXX/
```

---

# Required Components

## 1. Identifier

Example:

```text
UTE-FV-0042
```

Identifiers must:
- be unique,
- remain stable,
- and never be reused.

---

## 2. Title

Titles should be:
- concise,
- descriptive,
- and domain-appropriate.

Avoid vague or promotional language.

---

## 3. Statement

The statement should express the Core Truth clearly and directly.

Good example:

```text
Distance describes measurable separation between positions.
```

Avoid:
- unnecessary jargon,
- unsupported claims,
- or ambiguous wording.

---

# Proof Requirements

Every Core Truth should include a human-readable proof or reasoning structure.

Proofs should aim to provide:
- step-by-step reasoning,
- assumptions,
- conditions of validity,
- dependencies,
- and failure conditions where relevant.

UTE prioritises:
- interpretability,
- transparency,
- and reconstructability.

---

# Dependency Rules

Dependencies should identify which prior truths are required before a truth can exist coherently.

Dependencies must:
- reference valid truth IDs,
- avoid circular dependency chains,
- and remain logically necessary.

---

# Metadata Standards

Each metadata.json file should include:

```json
{
  "id": "UTE-FV-XXXX",
  "title": "Example Title",
  "domain": "Example Domain",
  "statement": "Example statement.",
  "dependencies": [],
  "confidence": 5,
  "status": "core-truth"
}
```

---

# Confidence Guidance

Confidence values should reflect:
- proof maturity,
- empirical reliability,
- and conceptual stability.

Current scale:

| Value | Meaning |
|---|---|
| 1 | speculative |
| 2 | weak |
| 3 | moderate |
| 4 | strong |
| 5 | foundational / highly reliable |

---

# Governance Expectations

Contributors should:
- preserve repository structure,
- avoid unnecessary file duplication,
- avoid overwriting root governance files unintentionally,
- and document major changes in the `updates/` folder.

---

# Assurance Expectations

Before submitting changes:

- verify IDs are unique,
- verify dependencies resolve correctly,
- verify proof files load,
- verify JSON validity,
- and verify map/topology alignment where relevant.

Large changes should undergo:
- Level 1 Assurance,
- and potentially Level 2 Assurance.

---

# Recommended Contribution Philosophy

UTE should expand:
- slowly,
- carefully,
- and structurally.

A smaller coherent topology is more valuable than rapid uncontrolled expansion.

---

# Final Principle

Contributors are not merely adding information.

They are helping construct a long-term navigable topology of reconstructable knowledge for both humans and machine reasoning systems.
