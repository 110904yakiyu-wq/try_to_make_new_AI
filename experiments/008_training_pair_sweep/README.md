# Experiment 008 — training-pair sweep

Experiment 007 used one exposure pair, A=`011` versus B=`101`.

The broad response-geometry change may be special to that pair.

## Question

Does Rule 129 show a repetition-induced remote geometry change for many different training distinctions, or only for one specially aligned pair?

## Sweep

For all 28 unordered pairs of 3-bit patterns:

1. run one-shot A/B histories;
2. run repeated A/B histories;
3. probe all 8 possible 3-bit patterns at offset 20;
4. compute the geometry-change vector `G(p)` as in experiment 007;
5. report its L1/L2 magnitude and how many probes not used in training have `|G| > 0.01`.

## Interpretation

Broad effects across many training pairs would make the phenomenon less likely to be a literal residue of one privileged bit pattern.

It would still be fully compatible with deterministic distributed phase/domain dynamics. No learning objective is present.
