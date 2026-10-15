# Experiment 117 — Disjoint train raw-probe split robustness

## Goal

Experiment 116 saw a width-3 donor-transplant response-similarity advantage over its early-response-nearest physical null (within a retrospectively chosen 20-G0-parent cohort). Does changing **which raw material probes are allowed for null selection** destroy this association? More importantly, can persistent differences still be explained by copying exact source raw-bit contents into the donor while prohibiting donor identity in null controls?

## Fixed protocol

- Same 104 local three-phase finite-speed physical kernel (left rotation, SIZE60, CENTER30), 112 matched 20-parent cohort and 113 fully feature-matched alternative bit-pool.
- At most 57 eligible transplant patches (23/14/20 for widths 1/2/3) and 506 distinct admissible physical-null microstates, enumerated before *any* train-response selection.
- **Five predetermined disjoint raw-value train folds:** `(1,7,15)`, `(2,8,14)`, `(3,9,13)`, `(4,10,12)`, `(5,6,11)`. Each fold uses these three nonzero values on *both* left/right union-support boundary sites. The 12 remaining raw values on both sides are held out. No train or test input value appears in both sets for any fold.
- For each fold and patch, select exactly one available physical alternative minimizing summed integer Hamming differences in the six train-probe response *position masks* at ticks 1 and 3 relative to the G0-patch transplant. Deterministically break distance ties by microstate bytes, without consulting the heldout values.
- Evaluate response-position-mask Jaccard/exact similarity of both G0-patch transplant and selected null against the original on-cycle G0 parent, at ticks 6,12,24 on **24 held-out probes**. Mean over patches in each parent, then equally over parents. The five folds share the same 20 parent-pairs and candidate pool: **not five independent validations**.
- Outcome does **not** test survival or learning. 'G0 response' here is observer-defined local dynamics relative to each frame's own unperturbed baseline.

## Results

### Parent mean held-out tick-24 Jaccard donor-minus-nearest-null

| Width | Fold 0 `(1,7,15)` | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Mean over parent-folds |
|---|---:|---:|---:|---:|---:|---:|
| 1 | +0.00980 | +0.01421 | +0.04336 | +0.03108 | +0.04161 | +0.02801 |
| 2 | −0.01112 | +0.09374 | +0.07444 | +0.04906 | +0.06583 | +0.05439 |
| 3 | +0.13116 | +0.15854 | +0.15417 | +0.12965 | +0.13114 | +0.14093 |

Width-3's positive *parent mean* persists across these train splits: each fold has 16 eligible parents, with 11–13 positive parent differences and 3–5 negative. Among the 16 parents, eight are positive for all five folds, two negative for all five folds. The remaining six change signs across folds.

Fold 0 exactly reproduces the Experiment 116 `nearest1` parent-mean for every width, an independent implementation-path consistency assertion, **not** independent validation.

## Critical interpretation / next audit

These are not separate data sets; all folds reuse the same substrate, parent selection, donor, null pool and response dynamics. Selecting a null by training-response similarity can also induce ordinary matching biases. Crucially, every G0 transplant copies exactly the G0 reference's raw bit values at the target patch sites, while all physical nulls expressly exclude that same patch assignment. Hence donor microstate is *necessarily closer to G0 at the edited sites* than every legal alternative, regardless of any emergent temporal structure. Future similarity to the G0 may therefore reflect a built-in **identity/proximity advantage**, not a special organizational causal role.

The correct next experiment is an identifiability/overlap census at the bit-level: test whether a nonidentical null with the same global raw-bit distance to G0 exists under fixed intervention support. If no, the current donor-to-G0 outcome comparison cannot be interpreted as isolated organization-specific causation. Do not add new physics merely to retain a positive effect.

## Run

```sh
python experiments/117_probe_split_robustness/run.py --output experiments/117_probe_split_robustness/results/default.json > experiments/117_probe_split_robustness/results/default.txt
python experiments/117_probe_split_robustness/test_smoke.py
```

All code is Python standard library; full 57-patch-by-5-fold data and parent summaries are archived in `results/default.json`.
