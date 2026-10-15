# Experiment 123 — Autonomous pre-material orbit outcomes of frozen edited controls

## Purpose

Experiments 120–122 built a small restricted set of bit-distance/edited-window-count/first-step-feature matched controls. Even before raw-material perturbation, do G0-patch transplants and those controls have different autonomous recurrence classes? If so, subsequent material-probe `connected` rates cannot be attributed solely to the subsequent perturbation.

## Method

- Same frozen 15 patch contexts of 121 and 122, containing 2/4/5 independent parent clusters for widths 1/2/3. Repeat the exact selected controls from 121 using only six prechosen train probes (raw 1,7,15 on each side, response masks ticks 1/3), with an assertion on the frozen training distances.
- Remove external material injection entirely. Starting each state at scheduler phase 0, evolve the *unchanged* 104 local kernel and record first exact `(microstate, next scheduler phase)` recurrence, preperiod, period, coarse recurrent class, and right censor at tick 500 and 2000.
- The previous raw bit edits are still part of the **candidate microstate**; 'no material' only means no later boundary raw-material probe. Candidate states need **not** lie on a cycle at time 0.
- Classify G0 reference, on-cycle matched recipient reference, G0 transplant, equal-edit budget control, and old fixed-patch null; parent means aggregate dependent patch records.

## Findings

| Width | Parent clusters | Transplant connected cycle identified by 500 | Equal-budget null connected cycle identified by 500 | Transplant censored by 500 | Null censored by 500 |
|---|---:|---:|---:|---:|---:|
| 1 | 2 | 100% | 100% | 0% | 0% |
| 2 | 4 | 100% | 100% | 0% | 0% |
| 3 | 5 | 60% | 40% | 40% | 40% |

For width 3, the same 40% of patch-weighted parent observations remain censored even at 2000 ticks in *each arm*. The connected class may differ despite equal aggregate immediate features; this says nothing about a special causal role without conditioning on the full physical state and micro-orbit.

## Interpretation and next step

One width-3 patch has transplant connected and equal-edit null static before any material injection, while two parent groups have censored initial trajectories. Evaluating subsequent material outcomes on this full subset confounds immediate perturbation response with initial autonomous viability/censor differences.

The next read-only comparison should condition on whether **both arms have proven connected autonomous cycles** by 500 ticks, and explicitly report resulting loss of support, then show any remaining downstream connected/censor contrasts. Such retrospective stratification is a *selection diagnostic*, not mediation identification.

## Reproduce

```sh
python experiments/123_autonomous_viability_control/run.py --output experiments/123_autonomous_viability_control/results/default.json > experiments/123_autonomous_viability_control/results/default.txt
python experiments/123_autonomous_viability_control/test_smoke.py
```

All numerical data remain based on the same 104 kernel, no new physics, no cognitive assumptions; `censored` means no recurrence identified at the requested finite horizon, not death or permanent failure.
