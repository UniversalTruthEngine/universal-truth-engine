# Dependency Weighting System v1

## Purpose

This document defines an initial weighting system for links in the UTE truth topology.

Weights are provisional and may evolve, but the early system should remain simple.

---

## Weight Scale

| Weight | Meaning |
|---|---|
| 1.00 | Essential dependency |
| 0.75 | Strong dependency |
| 0.50 | Moderate relationship |
| 0.25 | Weak relationship |
| 0.10 | Loose analogy or contextual relevance |

---

## Example

```json
{
  "source": "UTE-FV-0004",
  "target": "UTE-FV-0003",
  "type": "depends_on",
  "weight": 1.0
}
```

Addition depends essentially on counting.

---

## Weighting Guidance

Use high weights when:

- the source truth cannot be understood without the target,
- the source truth cannot be derived without the target,
- or the target is a direct prerequisite.

Use lower weights when:

- the relationship is helpful but not required,
- the link is analogical,
- or the relationship is cross-domain but indirect.

---

## Future Cosmological Interpretation

In the eventual UTE knowledge cosmos:

- high dependency weight may behave like stronger gravity,
- highly connected truths may appear near the core,
- dense clusters may form domains,
- and weak analogical links may behave like long-range bridges.

This is metaphorical, but computationally useful.
