# Experiment 124 — Read-only material outcome stratification by prior autonomous dynamics

## Question

Does the small positive width-3 `connected active cycle by tick 500` difference observed in 122 persist if both the original G0 patch transplant and its equal-edit-budget null have proven autonomous **connected active recurrence by tick 500**, without an additional boundary material input?

## Procedure

- No simulations, no new matching and no physical changes. Join frozen Experiment 122 material-response outcome data with Experiment 123 autonomous no-material recurrence records on `(parent_id,width,patch)`.
- Report mutually exclusive strata: **both connected** autonomous at 500; **both censored** at 500; **mixed resolved** classes at 500; other. No censored state is categorized as static or dead.
- Within each stratum, compute downstream held-out-24-probe connected fraction and censor fraction (both by 500), averaging patches within parent then equally over eligible parent clusters. These are *conditioned descriptive estimands*, not population treatment effects.

## Results

| Width | Pre-material autonomous stratum | Eligible patches | Parent clusters | Downstream G0 transplant minus equal-budget control: connected fraction | Difference in censored fraction |
|---|---|---:|---:|---:|---:|
| 1 | both connected | 3 | 2 | −0.06250 | +0.08333 |
| 2 | both connected | 5 | 4 | −0.06250 | +0.04167 |
| 3 | both connected | **3** | **2** | **+0.02083** | −0.02083 |
| 3 | both censored | 3 | 2 | −0.04167 | +0.06250 |
| 3 | different resolved classes | 1 | 1 | +0.58333 | −0.54167 |

The last row corresponds to a G0 transplant that was autonomously connected vs a static control even **before** the boundary perturbation. It contributes a large difference but cannot support a perturbation-induced persistence advantage.

Width-3 both-connected parent sign counts: **1 positive, 0 negative, 1 tie** over only two parents. Stronger restrictions therefore remove much of the apparent difference but simultaneously remove almost all evaluation support.

## Strict interpretation

This is not a causal mediation analysis. Conditioning on a microstate-derived autonomous outcome after the raw bit transplant can induce selection bias. The analysis is an audit of the **nonexchangeable starting states** rather than a randomized causal experiment. It cannot establish absence of a mechanism, only that these data do not identify one. No reproduction, heredity, learning, SELF or goal is inferred.

## Run

```sh
python experiments/124_autonomous_cohort_conditioning/run.py --output experiments/124_autonomous_cohort_conditioning/results/default.json > experiments/124_autonomous_cohort_conditioning/results/default.txt
python experiments/124_autonomous_cohort_conditioning/test_smoke.py
```

Standard-library read-only reaggregation of the committed 122 and 123 JSON archives.
