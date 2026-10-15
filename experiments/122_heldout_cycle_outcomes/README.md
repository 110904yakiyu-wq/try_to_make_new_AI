# Experiment 122 — Direct heldout orbit-class outcomes under equal edit budget

## Question and frozen protocol

Does a residual response-similarity advantage imply better exact-cycle persistence? Experiment 122 evaluates the **identical 15 eligible patch contexts** from Experiment 121. No candidate is chosen based on these downstream outcomes.

- Unchanged 104 physical kernel (SIZE60/CENTER30/phase0, 3-phase left-rotation step).
- Same 120 one-for-one exchanged edited-window null with equal number of edited windows and equal global raw Hamming to original G0; first-tick mask/popcount/adjacent AND/flip counts also match.
- Same null assignment selected in 121: the nearest initial-response signature on train raw inputs 1,7,15 at ticks 1 and 3.
- Exact orbit recurrence detection at **500 ticks** on all other 12 nonzero raw input values per side. Four mutually exclusive categories: `connected` (active connected recurrent cycle), `fragmented` (active multicomponent recurrent cycle), `static` (recurrent nonactive microstate), `censored` (no recurrence identified yet). A censored orbit is **not** a failed organization, death, or proof of no cycle.
- Additional arms are G0/reference source, 108 matched recipient, transplant, and original fixed-patch null; each arm is tested on the same 24 material probes. Parent is the unit of aggregation; patches/probes remain repeated measures.

## Results

| Width | Independent parent clusters | Transplant connected by 500 | Equal-budget null connected by 500 | Donor − null | Transplant censored | Equal-budget null censored |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 83.33% | 89.58% | −6.25pt | 16.67% | 8.33% |
| 2 | 4 | 87.50% | 93.75% | −6.25pt | 10.42% | 6.25% |
| 3 | 5 | 53.75% | 42.92% | +10.83pt | 44.17% | 53.33% |

Width-3 parent-level connected-rate differences are 2 positive, 1 negative, 2 tied. Most of its visible 'connected by 500' contrast covaries with unresolved trajectories. The ratio must **not** be promoted to a claim of eventual viability, learning or organization-specific persistence. The recurrence horizon is a finite observer budget.

## Conclusion

Even after equal raw G0 distance, edit count, initial changed-position mask and aggregate initial physical-feature matching, the 15 qualified patch contexts are extremely scarce and not exchangeable in edit *location*. The experiment does not establish an independent temporal organization causal mechanism. It reinforces distinguishing transient observation censoring and actual recurrent class.

## Run

```sh
python experiments/122_heldout_cycle_outcomes/run.py --output experiments/122_heldout_cycle_outcomes/results/default.json > experiments/122_heldout_cycle_outcomes/results/default.txt
python experiments/122_heldout_cycle_outcomes/test_smoke.py
```

Python standard library only. The historical G0/control 500-tick labels are not used for null selection, and no kernel physics is edited.
