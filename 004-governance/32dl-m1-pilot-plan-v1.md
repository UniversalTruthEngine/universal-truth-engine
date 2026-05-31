# 32DL M1 Pilot Plan v1

## Purpose

Test whether 32DL can usefully annotate the M1 stabilised Core Truths.

## Scope

Pilot truths:

- UTE-FV-0015 — Law of Identity
- UTE-FV-0002 — Equality of Quantity
- UTE-FV-0003 — Counting and Natural Numbers
- UTE-FV-0026 — Measurement
- UTE-FV-0029 — Coordinate System
- UTE-FV-0031 — Position

## Pilot Questions

For each truth, test whether 32DL can express:

- identity,
- dependencies,
- uncertainty,
- review state,
- proof sequence,
- and consensus status.

## Example Candidate Notation

```text
I:UTE-FV-0015 → I:UTE-FV-0002
```

Possible meaning:

```text
Law of Identity maps into / supports Equality of Quantity.
```

```text
I:UTE-FV-0002 ; I:UTE-FV-0003
```

Possible meaning:

```text
Equality of Quantity composes into Counting and Natural Numbers.
```

```text
I:reviewer_A | I:reviewer_B → 1/π
```

Possible meaning:

```text
Independent reviewers converge on shared ground.
```

## Success Criteria

32DL is useful if it improves:

- compactness,
- semantic precision,
- dependency representation,
- review comparison,
- or machine parsing.

32DL is not useful if it increases opacity without improving verification.

## Decision Outcomes

- Reject for UTE
- Use only in review notation
- Use as optional semantic annotation
- Use as machine-readable semantic layer
- Reconsider after further development
