# Experiment 141 — Why do candidate controls fail to qualify?

Classify each of the **same 130,000** Experiment 139 *autonomous* candidates by its **first failing** gate, evaluated at a frozen 500-tick horizon. Gate order: no detected recurrence (right-censored), recurrent but static, wrong period, wrong exact cycle-union support, wrong phase0 occupancy, accepted. This is a partition by algorithmic decision path, **not** a causal decomposition of why candidate microstates behave differently.

| First gate outcome | Candidate count |
|---|---:|
| No recurrence by tick 500 (censored) | 89,999 |
| Autonomous static cycle | 1,185 |
| Wrong period | 28,226 |
| Wrong exact union support | 9,580 |
| Wrong phase0 occupancy | 40 |
| Accepted | 970 |

Among the 17 parents still without an accepted alternative at attempt 1000, many candidates are themselves right-censored by tick 500. In particular, this audit cannot distinguish a genuinely absent matching basin from insufficient candidate convergence time or a rare proposal probability. Testing longer autonomous horizons requires a separately frozen experiment and proper cost accounting.

## Reproduce

```sh
python experiments/139_extended_control_budget/build_proposals.py
c++ -std=c++17 -O3 experiments/141_control_eligibility_gates/gates.cpp -o /tmp/exp141_gates
/tmp/exp141_gates experiments/139_extended_control_budget/results/proposals.bin experiments/141_control_eligibility_gates/results/gates.csv
python experiments/141_control_eligibility_gates/analyze.py
python experiments/141_control_eligibility_gates/test_smoke.py
```

The exhaustive `gates.csv` is regenerable and may be omitted from Git to avoid redundant 130,000-row records; the committed JSON has the **full per-parent gate counts**. The accepted-candidate set is asserted to match Experiment 139 identically. Independent Python classifications on 96 proposals pass. Unresolved means **censored**, not a failed physical organization.
