# Experiment 002 — fixed-budget quotient

Experiment 001 showed that recurrence + discriminating power is far too easy to satisfy.

This experiment fixes the observer's computational budget across time.

## Question

With the same physical substrate and the same observer budget, can the currently available organization expose a different operational quotient over the same candidate patterns?

## Fixed budget

At every checkpoint:

- same ring size `N`
- same core width
- same context radius
- same assay horizon
- exactly one assay context per ring position (`N` contexts, duplicates included)

No past context repertoire is accumulated.

The observer therefore performs the same number and shape of local assays at every timestep.

## Equivalence

For each 3-bit candidate core, insert it at every position using the left/right flanks present at that checkpoint and observe the center bit after the fixed horizon.

Two cores are operationally equivalent at time `t` if their `N` outcomes are identical.

The resulting quotient can refine or coarsen over time even though the observer budget does not change.

## Important limitation

A changing quotient is still not learning. The Rule 110 configuration itself changes, so different instantaneous contexts are available.

The point is narrower:

> operational identity can be history-dependent and reversible under a strictly fixed assay budget.

That is useful for later experiments on metastable self-like and concept-like factorizations without hard-coding them.
