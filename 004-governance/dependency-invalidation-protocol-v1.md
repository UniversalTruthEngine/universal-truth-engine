# Dependency Invalidation Protocol v1

## Core Principle

If a truth changes status, dependent truths must be flagged for review.

## Trigger Events

- revised
- downgraded
- superseded
- contradicted
- archived
- deprecated

## Propagation Rule

If A depends_on B and B changes status:

A -> review_required

This propagates recursively through dependency chains.

## Governance

Human review remains mandatory.
