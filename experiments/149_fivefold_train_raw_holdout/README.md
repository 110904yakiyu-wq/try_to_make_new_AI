# Experiment 149 — Fivefold raw-panel sensitivity of response-matched controls

## Question

Experiment148 matched controls on **six training side/raw probes** {left,right}×{1,7,15} and used a disjoint 24-condition test panel. Does the large attenuation of G0−control spread depend on that particular choice of raw input values?

## Fixed physical contract

- Exact 104/139 local 60×4-bit, CENTER30, three-phase left-rotate, phase0 physical kernel. No new memory, goals, reward or inference mechanism.
- The same 113 G0 parent states and 970 candidate controls autonomously qualified in Exp139 by period, exact cycle-union support and phase0 occupancy.
- Predeclare five **mutually disjoint 3-value train groups:** (1,6,11), (2,7,12), (3,8,13), (4,9,14), (5,10,15). For each group, train = left/right×3 = 6 probes; test = left/right×the other 12 raw values = 24 probes. No train condition is scored as a heldout condition within that fold.
- For every G0/control, construct injected-vs-own-baseline position-mask responses at fixed absolute scheduler-aligned ticks (1,3,6). Choose one control by minimum sum of response-position symmetric-difference sizes across the 6 train conditions and 3 ticks; ties resolved by original raw bit XOR distance, differing windows, and accepted attempt. This selector sees no heldout recurrence or spread outcome.
- Evaluate exactly the frozen Exp140/142 outcomes at 50,000 tick/certified recurrence for **the 24 heldout probes only**, compare first-accepted and raw-nearest selection *on the same heldout subset*. Preserve unknown right censoring and parent-cluster weighting.

## Results

| Training raw triple | First-choice ever10 G0−control | Response-matched ever10 | Response-matched ever60 |
|---|---:|---:|---:|
| 1,6,11 | −13.13 pp | −4.46 pp | −3.76 pp |
| 2,7,12 | −12.65 pp | −3.61 pp | −3.28 pp |
| 3,8,13 | −12.61 pp | −6.16 pp | −4.98 pp |
| 4,9,14 | −13.20 pp | −4.65 pp | −4.20 pp |
| 5,10,15 | −13.16 pp | −3.36 pp | −2.84 pp |

Across all five folds, the heldout **ever10** difference remains negative but attenuates substantially from first-choice; same for ever60. Parent/fold repeated observations are not five independent cohorts. Across folds, the mean response-matched ever10 is **−4.45 pp** (range −6.16 to −3.36 pp), ever60 **−3.81 pp** (range −4.98 to −2.84 pp). These are descriptive sensitivities, not confidence intervals.

## Reproduction

```sh
python experiments/149_fivefold_train_raw_holdout/run.py \
  > experiments/149_fivefold_train_raw_holdout/results/default.txt
python experiments/149_fivefold_train_raw_holdout/test_smoke.py
```

The full deterministic `results/default.json` includes all 565 parent-fold selected-control records, per-fold and per-cohort summaries. Uses only repository Python standard library and frozen Exp139/140/142 source records. No newly measured long-horizon trial or refitting of physical kernel.

## Interpretation boundary

The heldout evaluation is disjoint in **raw values** from the train panel, but shares the same physical parents, boundary sites and candidate controls. Matching short-time perturbation response is not proof of learning, adaptation, autonomous organization-specific mechanisms or a SELF. Some selected nulls may share G0's full state (Exp146 found one exact identity). The 17 unmatched G0 parents and Exp142 adversarial eligible-choice interval crossing zero remain material limitations. Do not treat repeated 5-fold observations as independent statistical replicates.
