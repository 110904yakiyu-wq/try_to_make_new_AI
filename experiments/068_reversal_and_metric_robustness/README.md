# Experiment 068 — reversal and metric robustness

## Question

The high-repeat K8 perturbation assay showed a possible experience-specific operational recovery bias. Is that bias tied to the **most recently repeated experience**, and is it robust to the observer-side missing-transform penalty?

## Reversal design

Use the same two same-Hamming-weight perturbations `P` and `Q`, with exactly the same total counts in both histories:

- state 1: `Q x 8 -> P x 8`
- state 2: `P x 8 -> Q x 8`

Thus the experience multiset is identical. Only order differs.

After six autonomous washout events, challenge both states with `P` and `Q` separately and compare operational recovery using the K8 access-cost landscape.

A positive recent-experience score means:

- the `P`-recent state recovers better from `P`, and/or
- the `Q`-recent state recovers better from `Q`.

## Result

With 16 deterministic backgrounds:

- comparisons: **1152**
- recent-experience advantage: **621**
- older-experience advantage: **485**
- ties: **46**
- strict two-sided reversal: **184**

All six same-weight perturbation pairs individually had more recent than older advantages.

## Metric robustness

Repeating the assay over 8 backgrounds while changing the penalty for lost/gained transformation identities:

- penalty 1: `291 recent / 235 old`
- penalty 2: `309 / 232`
- penalty 4: `315 / 233`
- penalty 7: `315 / 238`
- penalty 10: `317 / 237`
- penalty 20: `317 / 237`

The direction never flips.

## Interpretation boundary

This is stronger than a simple frequency comparison because the two histories contain exactly the same perturbations in exactly the same counts.

However, it is **not yet evidence of generic learning**. The history has a highly structured block form (`8 + 8`). A deterministic dynamical system can carry strong order/phase hysteresis under block forcing.

The next audit therefore destroys block periodicity while preserving the same `8P + 8Q` multiset.
