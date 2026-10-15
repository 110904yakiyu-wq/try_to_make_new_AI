# Experiment 130 — Monotone physical-spread threshold robustness

## Motivation

Experiment 129 finds lower eventual `ever spread to all 60 ring positions` for G0 than exact autonomous-cycle-matched controls in the frozen 55 matched parents, with the sign already bounded negative by 500 ticks. As the 60/60 event was proposed following examination of the Experiment128 right-censored trajectories, it could reflect **observer threshold selection**. We therefore compute a declared family of cumulative nonzero-window union targets: **10, 20, 30, 40, 50, and 60** positions, without reselecting the parents or changing any physics.

## Measurement contract

- Unchanged 104/108 kernel: 60 circular 4-bit windows, left rotation, `CENTER=30`, three-phase local updates and phase-0 initial state.
- Frozen Experiment126–129 accepted 55 pairs out of 130 G0 parents, same 30 boundary raw-material probes on each arm, no material-outcome-based selection.
- Threshold event `E_K`: during the deterministic response trajectory, at least K **distinct physical window positions** have held a nonzero raw value at some point. The positions need not be active simultaneously. This is a monotone historical event and does not imply eventual recurrence or autonomous persistence.
- **Yes** is certified by first hitting K, **No** by an exact full physical microstate+next scheduler-phase recurrence before ever reaching K, and **unknown** otherwise. Every certified no remains a permanent no for the unchanged deterministic continuation. No unresolved recurrent-cycle outcome is treated as nonviable.
- Examine the fixed horizons 500, 2,000, 50,000 ticks. A single trace produces the nested threshold family. Aggregate rates over 1,650 probes per arm, with **55 parent clusters**; thresholds and probes are dependent repeated views, not independent replications.

## Results

| Threshold K | G0 proven spread by tick50k | Control proven spread by tick50k | G0−control eventual event-rate difference (sharp bounds) |
|---|---:|---:|---:|
| 10 | 173/1650 | 453/1650 | −16.97 pp, identified |
| 20 | 147/1650 | 400/1650 | [−15.39,−15.33] pp |
| 30 | 145/1650 | 396/1650 | [−15.27,−15.21] pp |
| 40 | 143/1650 | 395/1650 | [−15.33,−15.27] pp |
| 50 | 143/1650 | 395/1650 | [−15.33,−15.27] pp |
| 60 | 143/1650 | 395/1650 | [−15.33,−15.27] pp |

All six worst-case identification intervals exclude zero in the **same direction**, on exactly the same frozen matched population. Even at 500 ticks, all six rates' identification intervals exclude zero negatively. Thus the observed lower physical spread propensity for G0 is not produced solely by choosing the endpoint threshold at 60/60.

This does **not** establish a G0-specific causal stability mechanism. The raw bit contents differ, controls were selected from 55/130 parents only, and the whole threshold family is exploratory and based on the same deterministic sample. No learning, organism identity, reproduction, survival goals or SELF follows from this result.

## Reproduction

```bash
cd experiments/127_censor_resolution_work_budget
python build_states.py
c++ -std=c++17 -O3 sweep.cpp -o sweep
./sweep states.bin results/probes.csv 50000
cd ../130_spread_threshold_robustness
c++ -std=c++17 -O3 trace.cpp -o trace
./trace ../127_censor_resolution_work_budget/states.bin ../127_censor_resolution_work_budget/results/probes.csv results/probes.csv
python analyze.py > results/default.txt
python test_smoke.py
```

The CSV archives all 3,300 first-hit times at the six cumulative thresholds. The summary JSON contains cohort-level sharp bounds and parent-level robust direction counts. `test_smoke.py` verifies **all 3,300** full-ring hit times against Experiment129 and checks the nesting of first-hit times across thresholds.

## Next boundary

The reliable result is **differential global propagation propensity** on matched but raw-content-unequal cycles. To test whether this follows entirely from simple physical-feature differences, stratify by existing post-injection bit density or initial local AND interactions using preoutcome matching, and be prepared for severe overlap restrictions. The tail endpoint should not be relabeled as organizational self-maintenance or adaptation.
