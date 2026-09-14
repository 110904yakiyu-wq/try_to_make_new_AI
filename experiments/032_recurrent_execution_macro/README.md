# Experiment 032 — naturally recurrent execution macros

## Question

Experiment 031 showed that a 7-bit local context can causally transfer a later event cascade when transplanted between histories.

Does the same context also carry the same execution role when it **reappears naturally** in a different equal-budget history?

## Setup

Use the queue-free K1 substrate at a fixed interaction location (`train_pos=0`). For both stateless scheduler orientations (`min` and `max`):

- sweep all 256 ECA rules;
- use the same equal-budget `A,A,A,B,B` and `B,B,A,A,A` history family;
- record the naturally produced radius-2 / 7-bit patch at the interaction site;
- record the next 32 event slots with no further intervention.

For each sample, predict its future event trace from **other histories with the same rule, scheduler, and naturally recurring 7-bit patch**. The target sample itself is excluded.

Controls:

1. rule-only leave-one-history-out majority trace;
2. 200 within-rule patch-label shuffles, preserving the patch-frequency distribution and prediction coverage.

## Result

Total samples: **4096**.

A same-patch peer existed for **2071/4096 = 50.56%** of samples.

Within those covered samples:

- same-patch future-trace accuracy: **2001/2071 = 96.62%**
- rule-only baseline accuracy: **1755/2071 = 84.74%**
- shuffled-patch null mean accuracy: **87.38%**
- maximum over 200 shuffled null trials: **89.04%**

The effect is similar for both stateless scheduler orientations:

- `min`: 96.63% accuracy on 1394 covered samples
- `max`: 96.60% accuracy on 677 covered samples

## Interpretation boundary

The local patch is not declared to be a symbol, representation, program, or learned concept.

The narrow result is:

> when the same small local pattern emerges naturally from different histories under the same physical law, it usually predicts the same subsequent execution cascade much better than the rule alone.

Together with Experiment 031, this makes the patch look like a reusable **operational execution macro** from the observer's perspective: it is both causally transferable and naturally recurrent.

## Next question

The remaining problem is compositionality. Can two such recurrent contexts interact so that their joint execution effect is not reducible to either context alone, while no explicit symbol boundary or composition operator is introduced?