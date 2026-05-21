# UTE-FV-0001 — Pythagorean Theorem Proof

## Claim

For a right triangle on a flat Euclidean plane:

```text
a² + b² = c²
```

## Plain-Language Explanation

A right triangle has one angle of 90 degrees. If a square is built on each side of the triangle, the two smaller square areas together equal the largest square area.

## Step-by-Step Area Proof

Construct a large square with side length `a + b`.

Its area is:

```text
(a + b)² = a² + 2ab + b²
```

Place four identical right triangles inside the square. Each triangle has area `ab / 2`, so four have area `2ab`.

The remaining central region is a square of side `c`, so its area is `c²`.

Therefore:

```text
a² + 2ab + b² = 2ab + c²
```

Subtract `2ab` from both sides:

```text
a² + b² = c²
```

## Conditions of Validity

Euclidean geometry, flat space, straight line segments, a true right angle, consistent units, and ordinary area arithmetic.

## Failure Cases

Curved surfaces, non-Euclidean geometry, non-right angles, or inconsistent units.
