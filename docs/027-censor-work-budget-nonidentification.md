# 027 — Extended work-budget audit: persistence sign still not identified (Exp127)

**Scope:** Frozen 55 matched G0/control parent pairs from Experiments 108, 125, and 126. Identical 30 boundary raw-material probes per parent and arm. Physical law (60×4-bit ring, three-phase finite-speed mutual modulation) is untouched. No additional cognitive primitive or adaptive mechanism.

Experiment 127 calculates exact full-microstate-plus-scheduler-phase first recurrence out to **50,000 ticks**, and records computational cost in unique state-transition steps. Its C++ kernel was checked on 192 Python-recomputed probes/horizons; historical whole-cohort class tallies at 500 and 2,000 are also recovered exactly.

### Empirical limits

- At 500 ticks: G0 connected 1,486, control connected 1,215; G0 censored 143, control censored 398. Worst-case eventual connected-rate difference: **[-7.70, +25.09] percentage points**.
- At 2,000 ticks: confirmed connected = 1,486 versus 1,218; censored = 143 versus 395. Worst-case difference: **[-7.70, +24.91] pp**.
- Between 2,000 and 32,000 ticks, no new proof of cycle recurrence; at 50,000 ticks just **one additional control fragmented cycle** is resolved. Censored = 143 versus 394, and the eventual difference bound becomes **[-7.64, +24.91] pp**, still overlapping zero.
- Parent-level signs at 50,000: 12 definitely G0-positive, one definitely control-positive, **42 indeterminate** of 55. This is a finite-population descriptive bound; repeated probes do not represent independent parent units.
- Updating all distinct states until 50,000 required **26,519,585 state transitions**, against 1,128,913 for 2,000. Observational gain after 2,000 was one resolved case.

### Causal and epistemic boundary

The finite-time **observed** connected recurrence difference is positive, but the sign of the **eventual** connected-cycle difference remains unidentified without unsupported assumptions about the censored trajectories. Finite deterministic phase-aware systems must eventually recur, but the recurrence class is not certified by a 50,000-tick timeout. No autonomous survival drive, self-model, heredity, learning, adaptation, special organizational cause, or intrinsic reproduction is established.

Simply increasing simulation horizon is currently a poor research priority compared with proofs of restrictive physical invariants, exact state-space reduction under verified isolation assumptions, or other rigorously sound certificates. New recognizers may change the observer, but should not modify the kernel merely to produce a positive outcome.

**Authority:** `experiments/127_censor_resolution_work_budget/{build_states.py,sweep.cpp,analyze.py,test_smoke.py,results/}`; historical `experiments/125_censoring_partial_identification/` and `experiments/126_extended_censoring_bounds/`.
