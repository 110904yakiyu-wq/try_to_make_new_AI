# 012 — Probe discrimination and immediate-mask conditional transfer boundary

## Status

Experiment 112 completed using Experiment 104/108's **unchanged**
three-phase, 60-window, 4-bit finite-speed kernel. All control selection
was performed before material perturbation and without checking its
outcome. A 500-tick absence of cycle convergence is censored.

## Distinguishing reference responses

Exact geometry/phase matching retained 55/130 parents, of which 20
also matched the exact first autonomous tick changed-position mask.
The predeclared boundary material panel expanded from values {1,7,15}
per boundary (6 total) to all {1,..,15} per boundary (30 total).

In the 20 pairs, both arms resolved on 71/120 old conditions and 420/600
expanded conditions. Coarse response classes disagreed only 2 times
from 2 parents with the old panel, and 10 times from 8 parents with the
larger panel. 180 of the 600 expanded paired conditions had at least
one censored reference result. Among resolved pairs, differences of
postperturbation cycle period (283) and exact union-support set (263)
were much more frequent than coarse-class disagreement (10).
These physical details should **not** be mistaken for emergent goals,
learning or autonomous self-maintenance.

## Fixed-constraint secondary transplant

The 111 protocol was repeated unchanged on the newly informative
reference panel: widths 1/2/3 contiguous donor patches, four site-
matched random raw-value replacements per patch, and an exact first-
tick changed-position mask constraint on every accepted candidate.
Patch/null eligibility did not depend on perturbation response.

- Width 1: 35 eligible patches, 8 informative parent units; parent-mean
  G0 confirmed response fraction 0.4375 versus null 0.234375, difference
  +0.203125; wins/losses/ties 4/1/3.
- Width 2: 16 patches, 5 informative parent units; G0 0.400 versus null
  0.225, difference +0.175; wins/losses/ties 1/1/3.
- Width 3: 20 patches, 6 informative parent units; G0 0.333333 versus null
  0.229167, difference +0.104167; wins/losses/ties 3/2/1.

The donor-positive directions are exploratory **associations**, not
proof of transferred multi-time organization. Every informative parent
has only one or two resolved, discordant reference probes, parent
eligibility was restrictive, and the null is not popcount- or local-
interaction-statistic matched. The 71 patches and their four random
replicates are **not** independent samples for inferential purposes.
Patch/null censoring remains a distinct, nonnegative interpretation.

## Next strict boundary

Test whether the small residual conditional donor advantage survives
more demanding physical matching (raw popcount, local pairwise overlap,
first-tick bit-flip count and multi-tick phase-consistent trace). Design
null construction and sampling quotas before looking at material
response. Include a no-eligible-match outcome and a parent-clustered
summary. A failure of stronger controls should be recorded as a
negative result; it must not trigger ad hoc insertion of a reward,
learner, goal, SELF, reproduction primitive or new physical rule.

Reproducible authority: `experiments/112_probe_discrimination_audit/`
contains `run.py`, `transplant.py`, `test_smoke.py`, the full packed
reference results `results/default.json`, and the independent local
patch-control archive `results/transplant.json`.
