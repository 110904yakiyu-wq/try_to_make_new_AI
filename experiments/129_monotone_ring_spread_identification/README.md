# Experiment 129 — Sign-identified monotone full-ring spread

## Question

In Experiments 125–127 the conditional G0 vs exact autonomous-cycle matched-control difference in **eventual recurrent connected class** remained non-sign-identifiable because of unequal right censoring. Experiment 128 showed that nearly all unresolved orbits had reached the whole ring at least once by tick 50,000. Can a *different, precisely defined observable* — **ever touches all 60 physical window positions at any time** — be sign-identified without pretending that the recurrent connected class has been identified?

## Frozen protocol and sound certificates

- Reuse exactly the 55 preintervention matched G0/control parent pairs (of 130 G0 catalog parents), and the 30 left/right × raw 1..15 material probes, from Exp126/127.
- Unchanged kernel: 60 cyclic 4-bit windows, CENTER 30, phase 0, three-phase local mutual modulation with bit rotation left.
- An **ever-full-ring positive certificate** occurs when the historical union of nonzero window positions first reaches 60. This is a monotone history event; simultaneous occupancy of 60 windows is not required.
- A **permanent ever-full-ring negative certificate** occurs when the complete `(full physical microstate, next scheduler phase)` has recurred, and the historical union has remained below 60 throughout the preperiod and one complete cycle. No later trajectory can add a previously unseen window because the future repeats this same cycle forever.
- Otherwise, at horizon `h`, the event remains right censored. This is a different outcome from `connected`, `fragmented`, `static`, or `censored` in previous recurrent-cycle audits; it is never substituted for them.
- For each arm, the true ever-full rate is bounded by `[observed positive, observed positive + unresolved]`. For the G0–control rate difference, the sharp interval is `[G0_yes − (CTRL_yes + CTRL_unknown), G0_yes + G0_unknown − CTRL_yes] / 1,650`. Pair/parent clustering is retained and no binomial IID claim is made.

## Observed results

| Evaluation horizon | G0 yes/no/unknown | Control yes/no/unknown | Ever-full rate difference G0−control, bounds |
|---|---|---|---|
| 100 | 0 / 1,454 / 196 | 5 / 1,214 / 431 | [−26.42, +11.58] percentage points |
| 250 | 12 / 1,507 / 131 | 24 / 1,248 / 378 | [−23.64, +7.21] pp |
| **500** | **129 / 1,507 / 14** | **369 / 1,251 / 30** | **[−16.36, −13.70] pp** |
| 1,000 | 143 / 1,507 / 0 | 395 / 1,252 / 3 | [−15.45, −15.27] pp |
| 2,000 | 143 / 1,507 / 0 | 395 / 1,254 / 1 | [−15.33, −15.27] pp |
| 50,000 | 143 / 1,507 / 0 | 395 / 1,254 / 1 | [−15.33, −15.27] pp |

At 50k, **the G0 group has definitively lower ever-full-ring spread rate** in the same 55 parent pairs, regardless of the one remaining censored control condition. Ten matched parent pairs are guaranteed G0-higher, 37 control-higher, and eight remain parentwise sign-ambiguous/tied (these are conservative signs, not statistical confidence levels).

This is **not** proof that any distinct G0-specific survival mechanism exists. The G0s and controls have differing raw 4-bit values, source catalog selection and preintervention matching on 55/130. The alternative metric was motivated by inspecting censored outputs and is exploratory. A robust next study should predeclare a *family of spread thresholds* rather than choosing one after viewing outcomes.

## Exact reproduction

```bash
cd experiments/127_censor_resolution_work_budget
python build_states.py
c++ -O3 -std=c++17 sweep.cpp -o sweep
./sweep states.bin results/probes.csv 50000
cd ../129_monotone_ring_spread_identification
c++ -O3 -std=c++17 trace.cpp -o trace
./trace ../127_censor_resolution_work_budget/states.bin ../127_censor_resolution_work_budget/results/probes.csv results/probes.csv
python analyze.py > results/default.txt
python test_smoke.py
```

`results/probes.csv` archives all 3,300 recorded first-full-ring times, recurrence certificates, and observational work. `results/default.json` contains the per-horizon and parent-cluster count bounds; all decisions are computed from physical trajectories, and no new rule is injected. `test_smoke.py` confirms all 537 late-censored full-ring times against the independent Exp128 simulator and 72 sample 500-tick traces against the Python 104 kernel.
