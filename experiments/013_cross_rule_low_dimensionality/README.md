# Experiment 013 — cross-rule low-dimensional response modes

> **Audit note:** the null used here was later found to be too weak because the 28 pairwise rows are generated from only eight underlying pattern-specific vectors. See Experiment 016 for the structure-preserving re-test. The original result is intentionally kept as part of the experiment history.

## Question

Do the strongest remote-history effects from Experiment 012 merely produce large, unstructured residuals, or do different fixed ECA rules also organize those effects into a small number of shared response modes?

## Method

For each selected rule, construct a 28 × 8 matrix:

- 28 rows: every unordered pair of width-3 exposure patterns
- 8 columns: every width-3 probe pattern
- entry: repeated-exposure response minus one-shot response at a remote probe site

Center the columns and compute the variance spectrum of the resulting response geometry.

A row-wise probe-label shuffle is used as an observer-side null. Each row keeps exactly the same values, but its eight probe labels are independently permuted. This destroys shared cross-history probe geometry while preserving each history's marginal response magnitudes.

## Default rules

The list contains the strongest rules from Experiment 012 plus Rule 129 and two useful controls/relatives:

`98,159,151,143,142,14,113,226,129,110,126`

## Original result

All eleven tested rules had observed top-two explained variance above the maximum of 500 row-shuffle null trials.

Examples:

- Rule 98: top-two = ~0.9884
- Rule 113: ~0.9582
- Rule 142: ~0.9582
- Rule 226: ~0.9506
- Rule 14: ~0.9504
- Rule 129: ~0.8251
- Rule 110: ~0.8096

## Why the interpretation was revised

Every pairwise row can be written exactly as `G_ab = H_a - H_b`, where only eight `H_a` vectors exist. Shuffling probe coordinates independently in all 28 pairwise rows destroys this algebraic consistency and therefore understates the low-dimensional structure expected under a suitable null.

Experiment 016 repeats the test directly on the 8 × 8 `H` matrix and preserves that construction. Under the corrected null, strong structure survives for a subset of rules, but Rules 110 and 151 no longer support the broad claim made here.

## Interpretation boundary

Even the original observation never implied learning, representation, or latent variables inside the CA. Experiment 016 further narrows the claim to rules whose history-effect geometry remains unusually low-dimensional after preserving the eight-vector construction.
