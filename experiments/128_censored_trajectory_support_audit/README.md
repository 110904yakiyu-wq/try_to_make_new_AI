# Experiment 128 — Physical support of the right-censored trajectories

## Question and control

Experiment 127 leaves 537 paired-probe records (G0 143, matched control 394) with no exact full-state-plus-phase recurrence by tick 50,000. Do these trajectories remain spatially localized while undergoing long transients, or do they spread physically over the 60-window ring? This is a purely descriptive **preexisting-physics observation**, not a new definition of persistence or a new matching rule.

- Use the *unchanged* Experiment 104/108 60-window 4-bit, CENTER30, phase-0 three-phase local mutual-modulation kernel.
- Reconstruct **exactly the same 55 matched parent pairs** from the frozen Experiment126 control attempt roster via Experiment127's `build_states.py`.
- Filter probes **only by** Experiment127's recorded 50,000-tick right-censor status (this is a retrospective observational subgroup, not a new outcome-blind causal comparison).
- For each censored full injected state, execute all ticks through 50,000 and record the **union of all positions with nonzero window contents**, including the initial state, at ticks 500, 2,000, 10,000, and 50,000. Also observe the maximum *instantaneously* occupied window count, first full-union hitting time, and mean occupancy over the trace.
- Memoize identical initial states; the 537 condition records correspond to 528 distinct physical inputs. Repeated probes are dependent within the matched parent, and the subgroup is selected for being censored, so this is **not** an unbiased matched G0/control superiority estimate.

## Results

| Right-censored at tick 50,000 | G0 | Control | Total |
|---|---:|---:|---:|
| Probe records | 143 | 394 | 537 |
| Historical nonzero union covers 60/60 windows by tick 500 | 129 | 367 | 496 |
| Historical nonzero union covers 60/60 by tick 50,000 | **143** | **393** | **536** |
| At some tick ≥30 windows nonzero simultaneously | 143 | 393 | 536 |

The sole 50,000-censored record not reaching full-ring union is in the control arm; its historical nonzero support union is 12 windows over this horizon. The majority of right-censored trials have thus become **spatially global at some point during the observation**. The union indicator does **not** mean all 60 windows are nonzero simultaneously, nor does it prove that an orbit can never return to a localized recurrent state later.

In particular, the original Experiment108 500-tick `connected` classification is a **recurrent-cycle union-support category** and must not be conflated with *any-time historical spread*, which is an alternative monotone event history. Full-ring spread often precedes all available recurrence detection and may explain why a finite-state cycle detector remains computationally expensive; this is plausible but not a proven cause.

## Reproduce

From the repository root, after building the reproducible 127 reference:

```bash
cd experiments/127_censor_resolution_work_budget
python build_states.py
c++ -O3 -std=c++17 sweep.cpp -o sweep
./sweep states.bin results/probes.csv 50000
python analyze.py
cd ../128_censored_trajectory_support_audit
c++ -O3 -std=c++17 trace.cpp -o trace
./trace ../127_censor_resolution_work_budget/states.bin ../127_censor_resolution_work_budget/results/probes.csv results/censored_trace.csv
python analyze.py > results/default.txt
python test_smoke.py
```

All 537 per-condition physical geometry measurements are in `results/censored_trace.csv`; `results/default.json` contains the summary, without duplicating the CSV rows. Python smoke independently checks 500/2,000 historical-union counts for 10 traces against the raw physical update.

## Boundaries / next hypothesis test

This does not sharpen the *eventual connected recurrence* rate bounds from Experiment127: a deterministic trajectory can visit the whole ring and later enter any of the finite recurrent-cycle classes. It suggests a different, operationally meaningful and **monotone** observable, namely `ever visits every window` rather than `eventually reaches a connected recurrent cycle`. A follow-up can exhaustively classify *all 3,300 injected states* for the monotone full-ring-spread event, and use recurrence to certify permanent negative results when full-ring spread never occurred during the entire preperiod and cycle. The scientific interpretations of those two outcomes must remain separate.
