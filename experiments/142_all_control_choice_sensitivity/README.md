# Experiment 142 — Exhaustive 1000-budget control-choice sensitivity

**Question.** Experiment 134 found an aggregate negative spread contrast against **any** of 87 controls from the first 100 autonomous proposals. Is that uniformly robust after 1000 candidates per parent? This assay tests **all 970** eligible controls over 113 matched parents and 30 boundary-material probes each, using exactly the same deterministic phase-aware physical kernel and 50,000-tick crossing/certification rule.

No control selection depends on injected outcomes for the *predeclared first-control* or *uniform-over-eligible-controls* estimands. The separate 'any eligible control' envelope takes mathematical extrema **after outcomes** and is a sensitivity bound, NOT a permissible operational control selection policy.

## Result

| Contrast (G0 − control spread) | 10-window event | 60-window event |
|---|---:|---:|
| First eligible control within 1000, 113 parents | −12.95 pp | [−11.68,−11.62] pp |
| Equal weight per parent, uniform average over that parent's 1000-budget eligible controls | **−12.73 pp** | confirmed −10.66 pp; eventual range approximately [−10.69,−10.66] pp |
| Worst-to-best over *arbitrary* one eligible control per parent | **[−40.09,+6.64] pp** | **[−33.42,+5.10] pp** |

The arbitrary-choice envelopes **include zero**. Thus Experiment 134's strong finite-choice negative sign is **not preserved across the larger eligible control pool**. However two natural, pre-outcome comparison rules, first-choice and uniform-per-parent, still show a negative association. Parent-level control choice is high variance; 111/113 parents show outcome variation across controls. This cannot be credited to or against a higher-level organization-specific mechanism.

**Integrity check:** Restrict to the 87 controls admitted within the first 100 proposals on the original 55 parents. Worst-case 10-position difference is exactly [−333,−189]/1650, i.e. [−20.18,−11.45] pp; 60-position range exactly [−296,−172]/1650, i.e. [−17.94,−10.42] pp, reproducing Experiment 134.

## Reproduce

```sh
python experiments/142_all_control_choice_sensitivity/build_controls.py
c++ -std=c++17 -O3 experiments/142_all_control_choice_sensitivity/trace.cpp -o /tmp/exp142_trace
/tmp/exp142_trace experiments/142_all_control_choice_sensitivity/results/eligible_states.csv experiments/142_all_control_choice_sensitivity/results/probes.csv 50000
python experiments/142_all_control_choice_sensitivity/analyze.py
python experiments/142_all_control_choice_sensitivity/test_smoke.py
```

`results/default.json` retains per-parent, per-control response-class summaries including censor counts; `results/probes.csv` (29,100 rows) can be reproduced using committed input states and physics. This is a **control-choice sensitivity audit**, not a statistical confidence interval or evidence of learning, goals or a SELF.
