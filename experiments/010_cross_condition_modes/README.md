# Experiment 010 — cross-condition response modes

Experiment 009 found that 28 different training histories reshape the 8-probe response geometry through a small number of shared observer-visible modes under one assay condition.

That low dimensionality may be an artifact of one probe location/time.

## Question

Does low-dimensional organization persist when the observer changes *where* and *when* the later interaction is tested?

## Conditions

Keep Rule 129, training schedules, ring size, training-pair sweep, and probe family fixed.

Compare four observer conditions:

- baseline: offset 20, probe time 48
- nearer probe: offset 12, probe time 48
- earlier probe: offset 20, probe time 40
- later probe: offset 20, probe time 56

For each condition construct the same `28 x 8` repetition-induced response-geometry matrix used in experiment 009.

Measure:

1. variance explained by the first two centered response modes;
2. Frobenius cosine similarity between the `8 x 8` centered probe covariance matrices.

The covariance similarity is invariant to the names/order of training histories, but still depends on the observer's chosen probe family. It is not treated as an internal representation.

## Interpretation

- High top-two variance across conditions: low dimensionality is not tied to one precise probe time/location.
- Covariance similarity near 1: approximately fixed response axes.
- Moderate similarity with persistent low dimensionality: a lower-dimensional organization persists, but its orientation changes with context.

The latter is closer to the working metaphor of a metastable organization than to a fixed latent representation.

No mode variable is added to the substrate. All modes remain observer descriptions of the fixed local dynamics.
