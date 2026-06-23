# Truth Derivation Audit Engine Protocol v1

## Purpose

Define how UTE explains candidate derivation reasoning.

## Core Rule

No candidate should proceed without an auditable derivation path.

## Audit Questions

For each candidate:

1. Which source truths caused this proposal?
2. What reasoning steps connect the source truths to the candidate?
3. Does the candidate already exist?
4. Is the candidate a duplicate, bridge, abstraction, or extension?
5. Should it proceed to candidate review?

## Safety Rule

Derivation audit is explanatory only.

It does not admit, merge, delete, or supersede truths.
