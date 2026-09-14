# Experiment 024 — recurrent dynamical macro

## Question

Experiment 023 showed that a small local pattern predicts the **current** operational quotient when it reappears naturally in a different history.

This experiment asks a stronger question:

> does the same local pattern also predict how the operational quotient will evolve autonomously afterward?

If yes, the pattern behaves less like a static context label and more like a local dynamical macro: a compact physical configuration associated with a reproducible family of future operational reorganizations.

## Method

For all 256 ECA rules, all eight width-3 training patterns, both one-shot and repeated histories, and every sampled training position:

1. run to time 48,
2. read the naturally occurring radius-2 local patch at the remote assay site,
3. without further training interventions, evaluate the local probe quotient at delays `0,1,2,4,8`,
4. concatenate those five quotients into a trajectory label,
5. predict that trajectory from occurrences of the same `(rule, 7-bit patch)` found only in **other training histories**.

A rule-only cross-history majority predictor is the baseline.

A within-rule patch-shuffle null preserves rule identity, trajectory frequencies, and patch-frequency distributions while destroying the relationship between the local patch and the future trajectory.

## Default result

Samples: **32,768**

Radius 2, delays `0,1,2,4,8`:

- cross-history coverage: **0.918426514**
- trajectory accuracy from the recurring local patch: **0.898288752**
- rule-only trajectory accuracy: **0.684967041**

100 within-rule patch-shuffle trials:

- mean trajectory accuracy: **0.666415116**
- minimum: **0.662229980**
- maximum: **0.670427276**
- mean coverage: **0.978911133**

Thus an endogenous 7-bit patch often predicts not only the present operational quotient but the later autonomous quotient trajectory across distinct histories.

## Interpretation

Together with Experiment 022, the current evidence is:

1. local endogenous patches can causally transfer a history-specific quotient,
2. the same patch naturally reappears in other histories and usually reproduces the same current quotient,
3. the recurring patch also predicts a substantial portion of the future operational reorganization trajectory.

At the observer level, this is consistent with a **reusable local dynamical context** emerging from a fixed, semantically empty local law.

The patch is not a built-in node, symbol, memory object, or rule. Its apparent role is produced by the dynamics.

## Important boundary

The CA still does not explicitly recognize the patch as a macro, deliberately recreate it, or choose it because it is useful.

Prediction from the patch is observer-side analysis.

The next boundary is therefore sharper: determine whether histories that generate one of these recurrent dynamical contexts make some later operational distinction available with **less additional physical work** than histories that do not. That would connect the endogenous context directly to the working notion of resource-bounded cognitive growth.
