# 011 — Experiment 111 conditional bit-transplant audit

Experiment 111 tests whether G0 local raw-bit transfer has an excess effect relative to random bit assignments under a fixed first-tick changed-position mask.

Of 130 G0 parents, 55 retained exact Experiment 108 matches. Only 20 of those also shared the first-tick changed-position mask. Among these 20 pairs, 35, 16, and 20 donor patches of widths 1, 2, and 3 preserved that mask. Every retained patch obtained four random assignments with the same edited sites and mask.

The six preselected boundary probes distinguished the original parent from the matched control in only **two** of the 20 pairs (one resolved disagreement per pair). Parent-mean confirmed response matches for donor versus random patch controls were 0 vs 0 (width 1), 0.5 vs 0 (width 2), and 0 vs 0.125 (width 3). These comparisons are statistically and mechanistically inconclusive.

The outcome is a negative or underpowered test of a specific causal transfer mechanism, **not** evidence that persistent organization is absent. Timeout means unresolved by 500 ticks, not negative survival. A matching one-tick changed-position mask leaves raw bit values and later state transitions uncontrolled.

Next test: fix a more discriminating probe panel in advance, retain parent-level sampling, and measure unresolved trajectories separately. Do not modify the physical update rule to force a positive observation.

Reproducibility: see `experiments/111_conditional_local_bit_swap/` for code, test, summary, and full JSON records.
