# UTE-FV-0001 — Pythagorean Theorem Proof

## Claim

For a right triangle on a flat Euclidean plane:

```text
a² + b² = c²
```

where:

- `a` and `b` are the perpendicular side lengths,
- `c` is the hypotenuse.

---

## 1. Plain-Language Explanation

A right triangle has one angle of 90 degrees.

If a square is built on each side of the triangle:

- the square on side `a` has area `a²`,
- the square on side `b` has area `b²`,
- the square on side `c` has area `c²`.

The theorem says:

```text
area on side a + area on side b = area on side c
```

---

## 2. Area Rearrangement Proof

Construct a large square with side length:

```text
a + b
```

Its area is:

```text
(a + b)²
```

Expanding:

```text
(a + b)² = a² + 2ab + b²
```

Now place four identical right triangles inside the square.

Each triangle has area:

```text
ab / 2
```

Four such triangles have total area:

```text
4 × (ab / 2) = 2ab
```

The remaining central shape is a square whose side is `c`.

So the central square has area:

```text
c²
```

Thus:

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

---

## 3. Why This Proof Works

The same total area is described in two valid ways:

1. using the outer square,
2. using the internal pieces.

Because area is preserved under rearrangement, both descriptions must match.

---

## 4. Reconstruction Method

A future society can rediscover this theorem by:

1. drawing right triangles on a flat surface,
2. constructing squares on their sides,
3. measuring or comparing areas,
4. noticing the invariant relationship,
5. proving it through area rearrangement.

A practical example:

```text
3² + 4² = 5²
9 + 16 = 25
```

The 3-4-5 triangle forms a right angle.

---

## 5. Conditions of Validity

The theorem assumes:

- Euclidean geometry,
- flat space,
- straight line segments,
- a true right angle,
- consistent measurement units,
- ordinary area arithmetic.

---

## 6. Failure Cases

The theorem does not apply unchanged:

- on curved surfaces,
- in non-Euclidean geometry,
- if the angle is not a right angle,
- or if measurement units are inconsistent.

---

## 7. UTE Assessment

- Confidence Level: 5
- Proof Type: Geometric / algebraic
- Reconstruction Difficulty: Low
- Core Importance: Extremely high
