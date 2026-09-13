# Experiment 013 — cross-rule low-dimensional response modes

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

## Result

All eleven tested rules have observed top-two explained variance above the maximum of 500 row-shuffle null trials.

Examples:

- Rule 98: top-two = ~0.9884
- Rule 113: ~0.9582
- Rule 142: ~0.9582
- Rule 226: ~0.9506
- Rule 14: ~0.9504
- Rule 129: ~0.8251
- Rule 110: ~0.8096

Thus the low-dimensional structure first noticed in Rule 129 is not unique to Rule 129, and it is not explained solely by the magnitude distribution within individual training histories.

## Interpretation boundary

This still does not imply learning, representation, or latent variables inside the CA.

The observer sees that many different histories alter later intervention responses along a small number of shared directions. Those directions may be consequences of domain propagation, phase structure, symmetries, or other fixed-law dynamics.

The next task is therefore explanatory rather than celebratory: determine which properties of the local rule make this structured history dependence possible, and whether the low-dimensional modes remain fixed or reorganize across conditions.
