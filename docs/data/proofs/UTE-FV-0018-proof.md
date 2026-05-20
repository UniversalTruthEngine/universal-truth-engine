# UTE-FV-0018 — Modus Ponens Proof

## Claim

If P implies Q, and P is true, then Q is true.

```text
P → Q
P
Therefore Q
```

## Plain-Language Explanation

Modus Ponens is a basic valid inference rule.

If a condition is enough to guarantee a result, and that condition is present, then the result follows.

Example:

```text
If it is raining, the ground becomes wet.
It is raining.
Therefore, the ground becomes wet.
```

## Logical Structure

Let:

```text
P = condition
Q = consequence
```

The implication states:

```text
P → Q
```

This means:

```text
Whenever P is true, Q must also be true.
```

If P is true, Q follows.

## Truth Table Demonstration

| P | Q | P → Q | Both premises true? | Conclusion |
|---|---|---|---|---|
| True | True | True | Yes | Q true |
| True | False | False | No | Invalid case |
| False | True | True | No | Not applicable |
| False | False | True | No | Not applicable |

The only case where both premises are true requires Q to be true.

## Conditions of Validity

The implication must be valid.  
The premise P must actually be true.  
The meanings of P and Q must remain stable.

## Failure Cases

Modus Ponens is misused when:

- the implication is false,
- P is not actually true,
- Q is only probable rather than guaranteed,
- terms change meaning,
- or a causal assumption is mistaken for logical implication.
