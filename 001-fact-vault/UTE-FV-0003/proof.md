# UTE-FV-0003 — Counting and Natural Numbers Proof

## Claim

Discrete quantities can be represented consistently by assigning ordered count markers to distinguishable items.

## Plain-Language Explanation

Counting is the act of matching each distinguishable item in a collection with one marker in an ordered sequence.

Example:

```text
stone → 1
stone → 2
stone → 3
```

The final marker represents the number of items counted.

## Required Conditions

Counting requires:

- distinguishable items,
- a stable collection,
- an ordered count sequence,
- and one-to-one assignment between items and count markers.

## One-to-One Assignment

Each item must receive exactly one count marker.

If an item is skipped, the count is too low.

If an item is counted twice, the count is too high.

This links counting to equality of quantity because the counted collection and the assigned marker sequence must correspond one-to-one.

## Natural Number Sequence

Natural numbers arise through repeated successor steps:

```text
1, 2, 3, 4, ...
```

Each successor represents one additional counted unit.

The sequence must preserve order. Without ordered succession, the final count marker cannot reliably represent total quantity.

## Cardinal Role

Counting determines cardinal quantity: how many items are in a collection.

Example:

```text
object A → 1
object B → 2
object C → 3
```

The collection has cardinal quantity:

```text
3
```

## Step-by-Step Reasoning

1. Identify a finite collection of distinguishable items.
2. Establish an ordered count-marker sequence.
3. Assign the first count marker to one item.
4. Assign the next marker to another uncounted item.
5. Continue until no uncounted items remain.
6. The final marker represents the collection's quantity.

## Why Counting Is Stable

Counting is stable when:

- the collection does not change during counting,
- every item is counted once,
- no item is skipped,
- and the count-marker order remains stable.

The order in which the items are visited may vary, but the final quantity remains the same if the assignment is complete and one-to-one.

## Dependencies

- UTE-FV-0002 — Equality of Quantity

Counting depends on the ability to preserve quantitative correspondence between items and count markers.

It also presupposes stable reference, indirectly supported by the Law of Identity through UTE-FV-0002.

## Reconstruction Method

A future intelligence can rediscover counting by:

1. gathering distinguishable objects,
2. making one mark for each object,
3. ensuring no object receives more than one mark,
4. ensuring no object is missed,
5. preserving the mark sequence,
6. comparing collections by their final markers.

## Conditions of Validity

Counting applies most directly to discrete items.

It requires:

- distinguishability,
- stable identity during the count,
- a stable count sequence,
- and a finite or well-defined counting procedure.

## Failure Cases

Counting fails or becomes unreliable if:

- items cannot be distinguished,
- the collection changes during counting,
- items are skipped,
- items are counted more than once,
- the count sequence changes,
- or continuous quantities are treated as discrete without a defined partition.

## Boundary Distinctions

Counting should not be confused with:

```text
measurement
ordering
ranking
labelling
approximation
```

Counting answers:

```text
how many?
```

It does not by itself answer:

```text
how long?
how heavy?
which order?
how close?
```

## Stabilisation Note

During stabilisation review, this truth was assessed as:

```text
sound but expandable
```

Future UTE development may separate:
- counting,
- natural numbers,
- successor,
- zero,
- cardinality,
- and ordinal position.

## UTE Importance

Counting supports:

- natural numbers,
- arithmetic,
- addition,
- multiplication,
- measurement,
- indexing,
- enumeration,
- and machine-readable structure.
