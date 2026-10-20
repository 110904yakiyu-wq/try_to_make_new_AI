# Experiment 140 — Spread outcomes on 113 newly covered G0 parents

**Design.** Reuse Experiment 139's *first autonomous eligible candidate* by attempt index <=1000 for each of 113 G0 parents. Keep the pre-response period, exact support, phase0 occupancy and scheduler equality. For each parent, inject all nonzero 4-bit values (1..15) at both external support boundaries into both G0 and control, with no further search. Measure cumulative **ever-reached 10 or 60 distinct ring-window positions** until recurrence or 50,000 ticks, exactly as in Experiment 130. A proven recurrence without threshold crossing certifies negative; non-arrival without recurrence is **unknown**, not negative.

## New results (G0 minus control spread event rates)

| Group | Parents | 10-position event contrast | 60-position censor-aware interval |
|---|---:|---:|---:|
| Historical first-100 eligible | 55 | −16.97 percentage points | [−15.33, −15.27] pp |
| Newly eligible by 1000 | 58 | −9.14 pp | [−8.22, −8.16] pp |
| Combined | 113 | **−12.95 pp** | **[−11.68, −11.62] pp** |

The old 55-parent cohort's complete **3,300 per-probe** first-threshold crossing times agree exactly with frozen Experiment 130. For non-full-ring trials, the recurrence times agree too. Independently run the original Python kernel on **64 new injected states**; all crossing and recurrence observations agree within 500 ticks. The same physical rules apply to the newly eligible parents. Repeated probes are clustered within the 113 parents.

**Interpretation:** The negative association persists in the newly available cohort but is weaker in magnitude. This is not a bound over **all possible** eligible control states, only an *explicit, pre-outcome, first-accepted* rule. Experiment 142 audits control-choice multiplicity at the larger budget. No causal attribution to a special temporal organization is established.

## Reproduce

```sh
python experiments/139_extended_control_budget/build_proposals.py
# Run 139/sweep.cpp to regenerate accepted.csv before the following commands.
python experiments/140_extended_matched_spread/build_states.py
c++ -std=c++17 -O3 experiments/140_extended_matched_spread/trace.cpp -o /tmp/exp140_trace
/tmp/exp140_trace experiments/140_extended_matched_spread/results/selected_states.csv experiments/140_extended_matched_spread/results/probes.csv 50000
python experiments/140_extended_matched_spread/analyze.py
python experiments/140_extended_matched_spread/test_smoke.py
```

`test_smoke.py` uses the committed Experiment 130 `results/probes.csv` for the historical 3,300-row regression. `selected_states.csv` contains exactly 226 original/selected states; generated from the 139 acceptance results. `probes.csv` records 6,780 trajectory observations. No physical primitives or new cognitive variables are added.
