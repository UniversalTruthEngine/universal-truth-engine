# UTE-FV-0001 — Pythagorean Theorem Proof

## Claim

For a right triangle on a flat Euclidean plane:

```text
a² + b² = c²
```

where `a` and `b` are the perpendicular side lengths, and `c` is the hypotenuse.

---

## 1. Plain-Language Explanation

A right triangle has two sides meeting at a right angle.

If we build a square on each side of the triangle:

- the square on side `a` has area `a²`,
- the square on side `b` has area `b²`,
- the square on side `c` has area `c²`.

The theorem says that the two smaller square areas together exactly equal the largest square area.

---

## 2. Area Rearrangement Proof

Construct a large square with side length:

```text
a + b
```

The area of this large square is:

```text
(a + b)²
```

Expanding:

```text
(a + b)² = a² + 2ab + b²
```

Now place four identical right triangles inside the large square.

Each right triangle has area:

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

Therefore, for a right triangle in Euclidean geometry:

```text
a² + b² = c²
```

---

## 3. Why This Proof Works

The proof depends on area conservation.

The same large square is being described in two ways:

1. by its outside side length,
2. by adding the areas of the shapes inside it.

Because both descriptions refer to the same total area, they must be equal.

---

## 4. Reconstruction Method

A low-technology society can rediscover the theorem by:

1. marking a rope into 12 equal segments,
2. forming a triangle with side lengths 3, 4, and 5,
3. observing that it forms a right angle,
4. checking:

```text
3² + 4² = 5²
9 + 16 = 25
```

This gives a concrete example.

The general proof comes from area rearrangement.

---

## 5. Conditions of Validity

This proof assumes:

- flat Euclidean geometry,
- straight line segments,
- a true right angle,
- consistent measurement units,
- ordinary area arithmetic.

It does not directly apply unchanged on curved surfaces.
