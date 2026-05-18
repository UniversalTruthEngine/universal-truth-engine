# Truth Link Types

## Purpose

This document defines the first reference set of relationship types used in the Universal Truth Engine truth topology.

Truths are not isolated statements. They form a dependency-aware structure that future humans, artificial intelligences, and other intelligences may navigate.

---

## Core Link Types

| Link Type | Meaning |
|---|---|
| `depends_on` | Truth A requires Truth B to be understood, derived, or validated |
| `supports` | Truth A provides evidence, reasoning, or reinforcement for Truth B |
| `derived_from` | Truth A is logically, mathematically, or experimentally derived from Truth B |
| `enables` | Truth A makes Truth B practically possible |
| `contrasts_with` | Truth A is clarified by comparison with Truth B |
| `limits` | Truth A defines the boundary or failure domain of Truth B |
| `analogous_to` | Truth A has structural similarity to Truth B |
| `generalises` | Truth A is a broader form of Truth B |
| `specialises` | Truth A is a narrower case of Truth B |
| `corrects` | Truth A revises, improves, or corrects Truth B |

---

## Direction Matters

Most links are directed.

Example:

```text
Equality depends_on Identity
Counting depends_on Equality
Addition depends_on Counting
```

This does not mean Identity depends on Counting.

---

## AI Interpretation

AI systems should treat link types as semantic edges in a graph.

A link should contain:

```json
{
  "source": "UTE-FV-0003",
  "target": "UTE-FV-0002",
  "type": "depends_on",
  "weight": 0.95
}
```

---

## Future Expansion

Additional link types may be added after review, but existing link meanings should remain stable where possible.
