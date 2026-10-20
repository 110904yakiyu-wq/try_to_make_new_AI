# Experiment 143 — First-choice spread across matching proposal budgets

Keep the original phase0 three-phase physical kernel and the deterministic 1000-attempt control generator of Experiment139. At each budget B ∈ {1,2,5,10,25,50,75,100,150,200,300,400,500,750,1000}, retain each G0 parent iff its **first** autonomous control qualifies within B attempts. Because the first-choice control itself is unchanged, the Experiment140 precomputed 30-probe outcomes are reused verbatim. No new physics or perturbation evaluation is required.

## Observed trend

| Candidate budget B | Matched G0 parents | G0−control ever-10-position spread |
|---|---:|---:|
| 1 | 1 | −33.33 pp |
| 25 | 19 | −19.12 pp |
| 100 | 55 | −16.97 pp |
| 200 | 83 | −14.10 pp |
| 500 | 107 | −13.43 pp |
| 1000 | 113 | **−12.95 pp** |

The comparison is negative at all 15 audited budgets for both 10-position and 60-position spread endpoints. The parent cohort expands in a *nested, selective* manner; this is a budget/selection sensitivity curve, not independent replication or a convergence proof. The first eight budgets reproduce Experiment137's previously frozen per-probe bounds exactly.

## Reproduce

```sh
python experiments/143_extended_budget_curve/run.py
python experiments/143_extended_budget_curve/test_smoke.py
```

Reads `experiments/139_extended_control_budget/results/default.json`, `experiments/140_extended_matched_spread/results/probes.csv` and the existing Experiment137 results. Does not introduce memory/learning/SELF/reward.
