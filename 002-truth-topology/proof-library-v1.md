# Proof Library v1

## Purpose

UTE truths should expose inspectable proof layers.

A truth node should not merely summarize a proof. It should link to a full proof object or proof file.

## Required Proof Layers

1. Plain-language explanation
2. Step-by-step derivation
3. Formal or structural proof
4. Reconstruction method
5. Conditions of validity
6. Failure cases

## Current Implementation

Map Engine v7 loads markdown proof files from:

```text
docs/data/proofs/
```

and displays them in the Truth Inspector Proof tab.
