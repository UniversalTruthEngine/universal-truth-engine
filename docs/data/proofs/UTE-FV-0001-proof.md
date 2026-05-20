# UTE-FV-0001 — Pythagorean Theorem Proof

## Claim

For a right triangle on a flat Euclidean plane:

```text
a² + b² = c²
```

where `a` and `b` are the perpendicular side lengths, and `c` is the hypotenuse.

## Plain-Language Explanation

A right triangle has one angle of 90 degrees.

If a square is built on each side of the triangle:

- the square on side `a` has area `a²`,
- the square on side `b` has area `b²`,
- the square on side `c` has area `c²`.

The theorem says the two smaller square areas together equal the largest square area.

## Step-by-Step Area Proof

Construct a large square with side length:

```text
a + b
```

Its area is:

```text
(a + b)² = a² + 2ab + b²
```

Now place four identical right triangles inside the large square.

Each triangle has area:

```text
ab / 2
```

Four such triangles have total area:

```text
4 × (ab / 2) = 2ab
```

The remaining central region is a square with side length `c`, so its area is:

```text
c²
```

Therefore:

```text
large square area = four triangle areas + central square area
```

So:

```text
a² + 2ab + b² = 2ab + c²
```

Subtract `2ab` from both sides:

```text
a² + b² = c²
```

## Conditions of Validity

This theorem assumes Euclidean geometry, flat space, straight line segments, a true right angle, consistent units, and ordinary area arithmetic.

## Failure Cases

The theorem does not apply unchanged on curved surfaces, in non-Euclidean geometry, if the angle is not a right angle, or if units are inconsistent.
