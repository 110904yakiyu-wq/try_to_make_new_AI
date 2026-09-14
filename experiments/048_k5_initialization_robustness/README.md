# Experiment 048 — K5 initialization robustness

## Why this audit exists

Experiment 047 found that the K5 mediator update was inert on the default single-bit initial ring: every naturally selected first event had `A AND B == 0`, so `M' = M`.

That could be a substrate failure, or simply a consequence of a sparse zero-dominated initial condition.

## Assay

Keep K5 unchanged and vary only the fixed initial ring.

Use ten deterministic backgrounds:

- eight dense pseudo-random 32-bit states (`seed=0..7`);
- two alternating backgrounds (`0101...` and `1010...`).

For every background, run the full 320-history family from Experiment 046.

Compare the normal first K5 event against a counterfactual that performs the same A/B rewrites but leaves M unchanged.

## Result

Across **3199** valid trained states:

- selected first events with `A AND B != 0`: **104**
- normal versus frozen-M future trace differs: **104/3199**
- normal versus frozen-M post-event transformation grammar differs: **61/3199**

Per-background active M-update counts range from 5 to 24 out of ~320 states. All ten dense/alternating backgrounds contain at least some active M updates.

## Interpretation

Experiment 047 remains correct for the original single-bit initialization, but its negative conclusion does **not** generalize to K5 as a substrate.

The M self-rewrite path exists and can causally alter later execution and, in many cases, the effective transformation grammar. It is merely dormant under the sparse default background because the stateless scheduler repeatedly selects endpoint pairs with disjoint 1-bits.

This is also a warning for the project: a minimal physical substrate can look incapable simply because the chosen initial medium makes most of its physical law unreachable.

## Boundary

This does not rescue any strong intelligence claim. The K5 algebra is still designer-fixed. The result only establishes that current transformation context can sometimes modify future transformation context under non-degenerate initial conditions.