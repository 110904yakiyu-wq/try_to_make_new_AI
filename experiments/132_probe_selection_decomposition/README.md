# Experiment 132 — Parent and probe selection decomposition

## Question

Experiment 131 revealed sign reversals when the fixed G0/control pairs were filtered for equality of early post-injection raw physical features. Is the change entirely attributable to shifting *which parents* are measured, or does selecting *which raw probes within those same parents* matter?

## Frozen design

This is a **read-only deterministic reanalysis** of the 1,650 paired feature/outcome records produced by Experiment 131. It introduces no kernel modifications, no new physical rule, no model, no reinjection or new control construction, and no outcome-guided eligibility. Five nested physical feature conditions are retained from 131. For each eligible set:

1. `full_55_parent_cohort`: all 1,650 G0/control probe pairs.
2. `same_eligible_parents_all_30`: for parents with at least one eligible probe, include *all* 30 raw material inputs per parent.
3. `feature_eligible_probes`: only those probes satisfying the physical feature equality filter.
4. `same_parents_feature_ineligible_probes`: other probes within **exactly the same parents**.

Recompute the sharp eventual hit/no-hit bounds for thresholds 10/20/30/40/50/60 at the same 50,000-tick observational budget. The pooled contrast on the same-parent population must equal the eligibility-count-weighted average of eligible and excluded probe contrasts (asserted for both bound endpoints). Parent-equal contrasts are reported separately.

## Results — threshold 10

| Eligibility filter | Selected parents | All 30 probes in those parents | Eligible probes | Excluded probes |
|---|---:|---:|---:|---:|
| None | 55 | −16.97 pp (1,650) | −16.97 pp (1,650) | — |
| Popcount | 15 | −13.78 pp (450) | −13.78 pp (450) | — |
| + AND | 14 | **−11.90 pp (420)** | **+2.38 pp (168)** | **−21.43 pp (252)** |
| + first flips | 10 | **−14.00 pp (300)** | **+2.38 pp (126)** | **−25.86 pp (174)** |
| + changed-site mask | 6 | **−2.78 pp (180)** | **+12.75 pp (102)** | **−23.08 pp (78)** |

Numbers in parentheses are **paired probes**, not independent parents. For threshold 60, the same sign-separation appears in the fully certified or partial-identification contrasts:

- 14 AND-eligible parents, all probes: [−10.48, −10.24] pp; AND-equal 168 probes: [+2.38, +2.98] pp; 252 ineligible probes: −19.05 pp.
- Six changed-mask-eligible parents, all probes: −2.22 pp; mask-equal 102 probes: +9.80 pp; 78 ineligible probes: −17.95 pp.

## Interpretation

**The reversal is not solely a parent-composition shift.** For a fixed set of 14 or six parents, selecting probes on early physical feature equality changes the descriptive spread association's sign. The selection is deterministic and performed without consulting subsequent spread outcomes, yet the selected early physical response may already be related to future propagation. Thus this is **selection and observation-granularity sensitivity**, not evidence for causal mediation or a distinct emergent mechanism.

Experiment 131's parent-equal vs pooled difference additionally shows that unequal numbers of eligible probes per parent can change even the sign of the estimand. None of these subgroup averages is an independent replication or an estimate for all 130 initial G0 parents; the 55 were preselected by viable exact geometry-matched on-cycle controls.

## Reproduce

```sh
python experiments/132_probe_selection_decomposition/run.py > experiments/132_probe_selection_decomposition/results/default.txt
python experiments/132_probe_selection_decomposition/test_smoke.py
```

Read-only input: `experiments/131_feature_conditioned_spread_audit/results/paired_features.csv`; output: `results/default.json` and readable `results/default.txt`. Standard-library Python only.
