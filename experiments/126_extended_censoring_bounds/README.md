# Experiment 126 — Full 55-parent 2000-tick censor audit

## Objective

Experiment 125 reconstructed all 55 exact-geometry-matched G0/control parent pairs from 108 and found that eventual connected persistence is not sign-identified with 500-tick right censoring. Experiment 114 had extended a narrower 20-pair subset to 2000 ticks, finding one additional resolved control trial. Does extending **all 55 parents**, not just the 20 first-tick-mask-equal subset, materially improve the bounds?

## Frozen kernel, cohorts and computation

- Unchanged 104/108 60-window 4-bit circle, CENTER=30, scheduler phase0 with three-phase synchronous local updates, left rotation. Each of the 130 original G0 parents is offered up to 100 autonomous control candidates; retain the **same 55 exact period/cycle union support/phase0 occupancy matches** documented by Experiment 125.
- Same 30 raw material probes per parent and arm, 1650 per arm.
- Compare exact full-microstate+next-scheduler-phase cycle detection at 500 and 2000 ticks. Every state proved recurrent by 500 retains the same class at 2000; **only 500-censored orbits are recomputed at 2000**. Identical full injected microstates are memoized, but remain repeated parent/probe records (not independent observations).
- For eventual connected outcome, bound each arm's count by `[proven connected, proven connected+censored]`. Aggregate paired lower and upper differences; do not treat censored as failure. Parent-level sign bound is calculated from each parent's 30 paired trials.

## Result

| Metric, 1650 conditions per arm | 500 tick | 2000 tick |
|---|---:|---:|
| G0 confirmed connected | 1486 | 1486 |
| Control confirmed connected | 1215 | **1218** |
| G0 censored | 143 | 143 |
| Control censored | 398 | **395** |
| Observed confirmed connected difference | +271 | **+268** |
| Lower possible eventual connected-rate difference | −7.697% | **−7.697%** |
| Upper possible eventual connected-rate difference | +25.091% | **+24.909%** |
| Parent sign: guaranteed G0/control/undecided | 11 / 1 / 43 | **11 / 1 / 43** |

There are **three newly resolved control orbits** across the full cohort; no newly resolved G0 orbits. Original 125 500-tick counts are exactly reproduced. There were 3270 unique 500-tick injected microstates and 532 unique 2000-tick follow-ups on 500-censored microstates; repeated probes explain the difference from the 541 total censored per-arm record counts.

## Scientific boundary

Even quadrupling the horizon does not sign-identify the eventual rate contrast. This does **not** show censored orbits never converge: deterministic finite-state dynamics guarantees eventual recurrence, but onset times can greatly exceed this observer budget. The 2000-tick population is 55 preselected matched parents; 75 G0 parents without a qualifying control are outside the estimand. Continued horizon extension is allowed but should weigh physical work cost against extremely low recent censor resolution rate.

No learning, SELF, goals, reproduction, heredity or organization-specific autonomous mechanism is demonstrated.

## Reproduce

```sh
python experiments/126_extended_censoring_bounds/run.py --output experiments/126_extended_censoring_bounds/results/default.json > experiments/126_extended_censoring_bounds/results/default.txt
python experiments/126_extended_censoring_bounds/test_smoke.py
```

Entire parent-by-arm 500/2000 category table is committed in JSON; Python standard library. Uses source Experiment125 parent roster and exact matching attempts, with no new selection based on material outcomes.
