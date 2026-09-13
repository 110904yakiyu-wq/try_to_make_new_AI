# Experiment 011 — cross-condition mode transfer

Experiment 010 found strong low dimensionality under several probe conditions, while the covariance geometry drifted.

This experiment asks a stricter question:

> If the observer extracts the best two response directions in condition A, how much of condition B can those same directions explain without refitting them?

## Metric

For each condition, let `C` be the centered `8 x 8` probe covariance matrix and let `U_A` contain the top two eigenvectors from source condition A.

Cross-condition captured variance is:

`capture(A -> B) = trace(U_A^T C_B U_A) / trace(C_B)`

Also report:

`relative_capture(A -> B) = capture(A -> B) / own_top2(B)`

where `own_top2(B)` is the variance B can explain using its own best two directions.

## Interpretation

- relative capture near 1: approximately reusable/fixed two-dimensional axes;
- much lower relative capture while B remains strongly two-dimensional: low-dimensionality survives but the axes are reconstructed with context.

The response modes remain observer-only descriptions. Nothing resembling a latent-vector module is added to the CA.
