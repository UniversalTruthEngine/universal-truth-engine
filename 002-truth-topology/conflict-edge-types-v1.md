# Conflict & Contradiction Topology v1

## Purpose

Extend the Universal Truth Engine topology beyond positive dependency relationships.

UTE must be able to represent not only:

- depends_on
- supports

but also relationships such as:

- contradicts
- undermines
- supersedes
- competes_with

## Rationale

A truth engine that cannot represent conflict is incomplete.

Scientific and mathematical development often proceeds by discovering contradictions, replacing models, refining assumptions, or identifying incompatible frameworks.

## Conflict Edge Types

### contradicts

Use when one truth directly conflicts with another under the same assumptions.

Example:

```text
A contradicts B
```

### undermines

Use when one truth weakens the justification, proof, confidence, or applicability of another truth without fully contradicting it.

### supersedes

Use when a later truth or model replaces an earlier truth or model in a defined scope.

This is especially relevant in empirical science.

### competes_with

Use when two truths or models are alternative explanations or formulations but no final resolution has been established.

## Governance Rules

Conflict edges must include:

- source truth
- target truth
- edge type
- explanation
- scope of conflict
- review status

## Important Distinction

Contradiction does not always mean deletion.

A contradicted truth may remain historically useful, domain-limited, or valid under specific assumptions.

## Example

```json
{
  "source": "UTE-FV-XXXX",
  "target": "UTE-FV-YYYY",
  "type": "contradicts",
  "scope": "under shared assumptions",
  "status": "requires review"
}
```

## Final Principle

Disagreement is not noise.

In a mature truth architecture, contradiction is part of the topology.
