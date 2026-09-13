# Experiment 009 — low-dimensional response modes

Experiment 008 showed broad response-geometry changes for all 28 possible 3-bit training pairs under Rule 129.

The next question is whether those changes are merely 28 unrelated high-dimensional residues, or whether different histories act through a small set of shared response modes.

## Matrix

Build a `28 x 8` matrix:

- one row per unordered 3-bit training pair;
- one column per possible 3-bit probe;
- each value is the repetition-induced geometry change from experiment 007.

Center each probe column across training pairs.

Compute the eigenvalues of `X^T X`; these are proportional to squared singular values, so they give explained variance by response mode.

## Null

For each null trial, independently shuffle the 8 probe labels within every training-pair row.

This preserves each row's values and magnitude but destroys any shared cross-history alignment between probe dimensions.

Compare the observed variance explained by the first two modes with this shuffle null.

## Why this matters

If many distinct histories reshape future responses along a few shared directions, then the medium has an observer-visible low-dimensional context structure.

That would be more interesting than literal high-dimensional residue, but it is still not a claim of concept formation, learning, or metacognition.
