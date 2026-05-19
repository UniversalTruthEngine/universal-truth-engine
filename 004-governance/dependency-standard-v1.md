# Dependency Standard v1

## Purpose

This document defines how dependencies between Core Truths should be represented within the Universal Truth Engine.

Dependencies form the structural topology of UTE. They determine how truths connect, how reconstruction paths are found, and how the knowledge cosmos takes shape.

---

## 1. Definition of a Dependency

A dependency exists when one truth requires another truth, concept, operation, or assumption to be understood, derived, validated, or reconstructed.

Example:

```text
Addition depends on Counting.
Counting depends on Equality / Identity of Quantity.
```

---

## 2. Direct vs Recursive Dependencies

### Direct Dependency

A truth directly depends on another truth when it cannot be understood or derived without that prior truth.

### Recursive Dependency

A recursive dependency includes the full chain of prerequisites.

Example:

```text
Division → Multiplication → Addition → Counting → Equality
```

UTE should preserve both.

---

## 3. Minimal Dependency Rule

Dependencies should be as minimal as possible.

A Core Truth should not list every indirectly related truth as a direct dependency.

Direct dependencies should be the nearest necessary prerequisites.

---

## 4. Dependency Weights

Dependencies may be weighted.

Suggested scale:

| Weight | Meaning |
|---|---|
| 1.00 | Essential dependency |
| 0.75 | Strong dependency |
| 0.50 | Moderate relationship |
| 0.25 | Weak relationship |
| 0.10 | Loose analogy or contextual relevance |

---

## 5. Cycles

Dependency cycles should generally be avoided.

If two truths appear to depend on each other, the entries may need to be decomposed into simpler truths.

Cycles may be allowed only after explicit topology review.

---

## 6. Bridge Truths

A bridge truth connects two or more domains.

Example:

```text
Ratio
```

may bridge arithmetic, geometry, measurement, physics, and chemistry.

Bridge truths should be identified because they are important for navigation and reconstruction.

---

## 7. Dependency Direction

Dependency direction matters.

```text
Addition depends on Counting
```

does not mean:

```text
Counting depends on Addition
```

---

## 8. AI Traversal

Machine-readable dependency data should allow AI systems to:

- trace prerequisites,
- identify missing nodes,
- find shortest reconstruction paths,
- detect circular dependencies,
- and estimate foundational centrality.

---

## 9. Final Principle

The dependency graph is not decoration.

It is the structural skeleton of the UTE knowledge universe.
