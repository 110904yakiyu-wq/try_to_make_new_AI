# Experiment 144 — Direction/raw robustness in the *new* 58 parents

Use only the **58 additional** G0 parent pairs that were not eligible within the first 100 autonomous proposals but became eligible within the original unchanged 1000-proposal control-selection experiment. No new physics, baseline or input conditions; simply stratify the independent newly covered set of 1740 paired raw-material probes into left/right and raw values 1..15, separately for ever-reaching 10 and 60 cumulative active positions.

For every left/right group, and for **every** raw input value 1..15, the G0–control spread difference is negative, including the censor-aware upper bound. The complete parent-level data and exact crossing times are in the frozen Experiment140 `results/probes.csv`. This stratification is a repeated-measures sensitivity test, **not** 30 independent replications, and the first-choice control comparator still carries raw-state confounds and selection bias.

## Reproduce

```sh
python experiments/144_new_cohort_input_robustness/run.py
python experiments/144_new_cohort_input_robustness/test_smoke.py
```

Requires the Experiment140 per-probe result file; results JSON contains the total, direction and 15 raw-input stratum bounds. This result does not demonstrate intelligence, experience-specific learning or self-maintenance goals.
