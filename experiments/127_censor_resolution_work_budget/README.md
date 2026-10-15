# Experiment 127 — Full-cohort censor-resolution work budget

## Purpose

Experiment 125 found that the eventual G0-minus-control connected-cycle difference was not sign-identified by 500-tick observations. Experiment 126 extended the same 55 exact autonomous support/period/phase-matched pairs to 2,000 ticks, with only three newly proven connected cycles in the control arm. Experiment 127 asks whether significantly longer observation intervals close the partial-identification interval, and what the exact additional kernel-update cost is.

## Frozen protocol

- **Physics unchanged:** Experiment 104/108, 60 circular 4-bit windows, CENTER=30, scheduler phase0, three-phase simultaneous local mutual modulation, left bit rotation. No added learning, reward or reproduction mechanism.
- **Population unchanged:** 55 accepted parent pairs out of the 130 G0 parents, using the same accepted random candidate attempt documented in Experiment 126. `build_states.py` reconstructs the exact phase0 G0/control frame. Control generation is prior to raw material injection and uses the original Python `random.Random(3_000_000 + parent_id * 300_000 + attempt - 1)` and `randrange(1,16)` contract. No reselection.
- **Probe panel unchanged:** both cycle-union support boundaries × nonzero raw values 1..15 = 30 per parent, 1,650 per arm. Unresolved trajectories are **right censored**, not failed persistence.
- **Observer:** exact recurrence of `(full 60-window microstate, next scheduler phase)`; a recurrent active cycle is called `connected` only if its union-support is one ring-connected component. Otherwise active cycles are `fragmented` and inactive cycles are `static`.
- **Horizon ladder (cumulative):** 500, 1,000, 2,000, 4,000, 8,000, 16,000, 32,000, 50,000 ticks. The single longest trace supports all shorter horizons, without altering their event definitions.
- **Runtime:** a C++17 kernel faithfully implementing the same physical step with exact state and phase keys. A memo of identical injected microstates reduces the number of orbits from 3,300 to 3,270. The measure of computational cost is the count of unique state transitions actually needed at each horizon, not wall-clock time.
- **Inference:** worst-case bounds on eventual connected cycle contrast under no assumption about right-censored outcomes. Within each parent the lower and upper count differences are `G0_connected - CONTROL_connected - CONTROL_censored` and `G0_connected + G0_censored - CONTROL_connected`. The estimand is conditional on matching; 75 nonmatched parents remain outside its domain. Probe rows are dependent within 55 parent clusters.

## Result

| Horizon | G0 censored | Control censored | Eventual rate-difference identification interval | Parent signs G0 / Control / Indeterminate | Unique kernel updates to this horizon |
|---|---:|---:|---:|---:|---:|
| 500 | 143 | 398 | [-7.70%, +25.09%] | 11 / 1 / 43 | 333,344 |
| 2,000 | 143 | 395 | [-7.70%, +24.91%] | 11 / 1 / 43 | 1,128,913 |
| 8,000 | 143 | 395 | [-7.70%, +24.91%] | 11 / 1 / 43 | 4,302,913 |
| 16,000 | 143 | 395 | [-7.70%, +24.91%] | 11 / 1 / 43 | 8,534,913 |
| 32,000 | 143 | 395 | [-7.70%, +24.91%] | 11 / 1 / 43 | 16,998,913 |
| 50,000 | 143 | 394 | [-7.64%, +24.91%] | 12 / 1 / 42 | 26,519,585 |

- All Experiment 125/126 aggregate class counts at horizons 500 and 2,000 are reproduced exactly. Parent/candidate assignment remains the 126 reference manifest.
- **No new recurrence between 2,000 and 32,000.** One control orbit previously right censored enters a proven **fragmented**, not connected, cycle by 50,000. Hence the lower eventual-difference bound increases from -127/1,650 to -126/1,650, while its upper bound stays at +411/1,650.
- At 50,000, G0 confirmed connected is 1,486, control confirmed connected 1,218; G0 censored 143, control censored 394.
- The sign of the overall eventual advantage is **still unidentified**. Additional computation cost is high relative to the small shrinkage of the interval. This observation does not prove that the remaining censored states never enter recurrent cycles.

## Reproduce

From repository root, with Python 3 standard library and a C++17 compiler:

```bash
cd experiments/127_censor_resolution_work_budget
python build_states.py
c++ -O3 -std=c++17 sweep.cpp -o sweep
./sweep states.bin results/probes.csv 50000
python analyze.py --csv results/probes.csv --output results/default.json > results/default.txt
python test_smoke.py
```

The `states.bin` and compiled executable are regenerable runtime intermediates, not intended for Git. All final probe classifications/recurrence times and tabulated bounds are in `results/probes.csv`, `results/default.json` and `results/default.txt`. The code and frozen parent manifest are committed.

`test_smoke.py` independently re-evaluates 192 injected states/horizon pairs in Python using the original update prescription and verifies numerical agreement with the C++ trace. It also checks historical 500/2,000 counts. This cross-language check is a regression test, not an independent validation of the underlying scientific interpretation.

## Interpretation

The important negative result is *poor observational returns from longer simulation of right-censored nonlinear local trajectories*, not no persistence, reproduction, or learning. The eventual finite-state recurrence is guaranteed; proving its class at an affordable computational horizon is not. A stronger next experiment should analyze **physical invariants or sound reachability certificates**, or reduce the class question to a bounded local subsystem *only when such a reduction is proved*. Do not condition on observed outcomes to choose a favorable control cohort, or treat a finite-horizon timeout as inactive.
