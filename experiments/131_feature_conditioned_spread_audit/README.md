# Experiment 131 — Initial physical-feature conditioning of monotone spread

## Question and frozen contract

The Experiment 129–130 exact-cycle-matched cohort (55/130 G0 parent pairs, 30 material probes per arm) has lower G0 propensity to ever occupy at least 10–60 distinct windows. Does the difference remain when comparing **only paired G0 and control perturbations sharing elementary physical features of the injected microstates**?

Reuse **unchanged** 60-window/4-bit finite-speed left-rotation kernel, phase 0, CENTER=30, same parent matches and all 1,650 paired material probes. The source is Experiment 130 `results/probes.csv` (3,300 arm records), and initial states are reconstructed from the frozen Experiment 127 matching manifest using `build_states.py`. No new simulation, physical primitive, reward, feedback, or outcome-based null selection.

For each paired material intervention, measure exactly on the **post-injection initial microstate**:

1. `popcount` — sum of all 60 raw 4-bit popcounts.
2. `neighbor_and` — sum of pairwise ring-neighbor bitwise-AND popcounts.
3. `first_flips` — global bit Hamming difference after one autonomous phase-0 update.
4. `first_changed_mask` — exact physical positions with changed 4-bit values after that update.

Nested eligibility requires equality of the first k features between G0 and control, preserving same seed parent, material side and raw value. The physical-feature eligibility does **not** examine subsequent spread events; these are retrospective physical matched *subsets*, **not** randomized counterfactual interventions. For eventual event `E_K` (union support reaches at least K distinct positions), a first hit is a certified yes, exact phase-aware state recurrence without a hit is certified no, and an unrecurring orbit at tick 50,000 is right censored/unknown. Bounds are worst-case eventual yes-rate differences, computed both by pooled paired probes and by parent-equal averaging. Probes in one parent are dependent.

## Results

| Nested physical equality | Eligible parents | Eligible paired probes | `E_10` G0−control (pp) | `E_60` G0−control bound (pp) |
|---|---:|---:|---:|---:|
| None | 55 | 1,650 | −16.97 | [−15.33,−15.27] |
| Popcount | 15 | 450 | −13.78 | [−12.00,−11.78] |
| + adjacent AND | 14 | 168 | +2.38 | [+2.38,+2.98] |
| + first-tick flips | 10 | 126 | +2.38 | [+2.38,+3.17] |
| + exact first-tick changed mask | 6 | 102 | +12.75 | +9.80 |

**Critical distinction:** for the 126-probe `pop_and_flips` subset, the `E_10` pooled contrast is +2.38 pp while the parent-equal contrast is −4.90 pp, because the retained probe count varies across the ten eligible parents. These are **different estimands**; neither can be treated as independent 126-sample significance.

A special property of the popcount stratum is that all 30 probes are retained or all 30 are excluded **per parent**, because G0/control occupancy and the injected value/position are the same. Subsequent tiers also select within-parent *particular* raw values/sides. Experiment 132 explicitly decomposes these selection shifts.

### Interpretation boundary

The original negative spread contrast holds for the full matched cohort. It does **not** remain invariant under conditional sample selection. A reversed observational association is **not** evidence that AND interactions or one-tick response masks *cause* lower spread, mediate organization, or add a new temporal/cognitive primitive. The small matched subset and conditioning on post-injection physical variables preclude a population causal statement. Selected strata may have different parent composition and unequal within-parent probe counts; compare at both levels. No reproduction, learning, goals or SELF implied.

## Reproduce

From repository root:

```sh
python experiments/127_censor_resolution_work_budget/build_states.py
python experiments/131_feature_conditioned_spread_audit/run.py \
  --output experiments/131_feature_conditioned_spread_audit/results/default.json \
  --csv experiments/131_feature_conditioned_spread_audit/results/paired_features.csv \
  > experiments/131_feature_conditioned_spread_audit/results/default.txt
python experiments/131_feature_conditioned_spread_audit/test_smoke.py
```

`results/default.json` is the bounded parent/stratum/endpoint summary. `results/paired_features.csv` preserves all 1,650 corresponding paired feature values and individual event statuses for reanalysis. No repacking of the Experiment 130 physical trace is required; provenance remains its checked-in 3,300-row raw CSV.
