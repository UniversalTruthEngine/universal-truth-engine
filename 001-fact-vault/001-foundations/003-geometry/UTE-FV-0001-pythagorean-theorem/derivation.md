# Derivation — UTE-FV-0001

## Area Rearrangement Proof

Construct a large square with side length `a + b`.

Place four identical right triangles inside it. Each triangle has side lengths `a`, `b`, and `c`.

The total area of the large square is:

```text
(a + b)^2 = a^2 + 2ab + b^2
```

The four right triangles together have total area:

```text
4 * (ab / 2) = 2ab
```

The remaining central area is a square whose side length is `c`, so its area is:

```text
c^2
```

Therefore:

```text
a^2 + 2ab + b^2 = 2ab + c^2
```

Subtract `2ab` from both sides:

```text
a^2 + b^2 = c^2
```
