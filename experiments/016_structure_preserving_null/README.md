# Experiment 016 — structure-preserving null

## Why this experiment exists

Experiments 009 and 013 used a 28 × 8 matrix whose rows corresponded to unordered training-pattern pairs. A later audit found that these 28 rows are not independent objects.

For pattern-specific history-effect vectors `H_a`, every pair row is exactly

`G_ab = H_a - H_b`.

Therefore the pairwise matrix inherits algebraic structure from only eight underlying vectors. Independently shuffling the eight probe labels inside each of the 28 pairwise rows destroys that consistency and creates a null that is too permissive.

This experiment corrects that problem.

## Corrected observable

Construct the 8 × 8 matrix `H` directly:

- row: one of the eight width-3 exposure patterns
- column: one of the eight width-3 probe patterns
- value: remote probe impact after repeated exposure minus impact after one-shot exposure

Low-dimensionality is measured directly on the centered `H` matrix.

## Structure-preserving null

For each null trial, independently shuffle the eight probe labels **inside each of the eight rows of H**, then recompute the top-two explained variance.

This preserves:

- exactly eight underlying exposure-specific history-effect vectors
- each row's value multiset and magnitude distribution
- the fact that any later pairwise geometry would be generated from those same eight vectors

while destroying consistent probe-coordinate organization across exposure histories.

## Result

The stronger null materially changes the conclusion.

Rules 98, 226, 14, 113, 142, 143, and 126 remain very strongly above the null range. Rule 129 remains above the null but much less dramatically. Rule 159 is only modestly above the corrected null. Rules 110 and 151 are consistent with the null under this assay.

Thus the broad claim from Experiment 013 — that all tested rules exhibit unexpectedly strong shared low-dimensional modes — was too strong.

A narrower claim survives:

> some fixed local laws produce repeated-history effects whose exposure-by-probe geometry is substantially more low-dimensional than expected after preserving the eight-vector construction.

## Interpretation boundary

This remains an observer-level property of deterministic dynamics. It is not evidence that the CA internally stores two latent variables.

The correction itself is important for this repository: experiment history is allowed to invalidate earlier interpretations, and the invalidated result remains in Git rather than being rewritten away.
