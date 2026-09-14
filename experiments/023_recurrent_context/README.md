# Experiment 023 — recurrent endogenous context

## Question

Experiment 022 showed that a small naturally generated local patch can causally transfer the donor history's operational quotient when the observer transplants it.

The next question is stricter:

> when the same local patch reappears naturally in a different training history or at a different sampled location, does it carry the same operational effect without being moved by the observer?

## Method

For all 256 ECA rules, all eight width-3 training patterns, both one-shot and repeated exposure histories, and every sampled training position:

1. run the history to time 48,
2. read the naturally occurring local patch around the remote assay site,
3. compute the local operational quotient induced by all eight width-3 probes,
4. group samples by `(rule, local_patch)`,
5. predict a sample's quotient using only occurrences of the same patch from **other training histories**.

The default patch radius is 2, so the context key is only 7 bits wide.

A rule-only cross-history majority predictor is the baseline.

For a stronger null, patch labels are randomly permuted within each rule while preserving the patch-frequency distribution. The same cross-history prediction procedure is then repeated.

## Default result

Samples: **32,768**

For radius 2:

- cross-history coverage: **0.918426514**
- cross-history quotient accuracy from the recurring 7-bit patch: **0.963050341**
- rule-only cross-history accuracy: **0.758911133**

100 within-rule patch-shuffle null trials:

- mean accuracy: **0.752398648**
- minimum: **0.745565635**
- maximum: **0.757756228**
- mean coverage: **0.978911133**

Thus a small local pattern that emerges under one history usually predicts the same operational quotient when it independently reappears under a different history.

## Radius trend

The effect strengthens as more local context is retained, while recurrence coverage gradually falls:

- radius 0: coverage ~0.9707, accuracy ~0.8656
- radius 1: coverage ~0.9523, accuracy ~0.9096
- radius 2: coverage ~0.9184, accuracy ~0.9631
- radius 3: coverage ~0.8824, accuracy ~0.9754
- radius 4: coverage ~0.8380, accuracy ~0.9887

This is the expected trade-off for a context code: a larger patch is more operationally specific but less likely to recur exactly.

## Interpretation

Experiments 022 and 023 together establish two different properties:

1. **causal transferability** — moving the endogenous patch usually moves the operational quotient,
2. **natural recurrence** — when the same patch arises independently, it usually carries the same quotient.

That is enough to treat the patch, at the observer level, as a reusable operational context rather than merely as a history residue.

## Important boundary

The CA still does not identify the patch as a context, copy it intentionally, or select it for a task.

The grouping into local patches is observer-side.

The next useful test is stronger: ask whether the local patch predicts not only the current quotient but the **future autonomous quotient trajectory**. If so, the endogenous pattern behaves more like a reusable local operator or dynamical macro than a static context label.
