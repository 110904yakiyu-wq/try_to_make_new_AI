# Experiment 119 — Heldout response of raw-distance-compensated physical controls

## Question

The previous G0-patch transfer vs distinct alternative construction had deterministic source proximity advantage. Experiment 118 showed one additional compensating edit often permits a null state with the **same raw-Hamming distance to G0** while preserving the first-tick changed-position mask, global popcount, adjacent AND and first-tick flip count. Does the apparent G0-patch heldout response advantage remain in this restricted, partially repaired counterfactual population?

## Frozen protocol

- No new physics. Same 104 kernel, 112 20-parent cohort, 113 original strongest physics alternatives and 118 one-additional-site compensation constraints.
- Select candidate states using only unperturbed physical features; no injected-material outcomes. 118 produced 28 qualifying patch contexts (width 1/2/3: 10/9/9) and 73 candidate microstates summed by patch.
- Original null: strictly at the original edited patch positions, matching the physical feature tier. Compensated null: additionally edits **one other originally G0/recipient-different occupied window** outside the patch, and matches donor-to-G0 raw-Hamming distance exactly, plus all immediate physical features. Both are selected only from the same 28 eligible patch contexts.
- Preselected train (Exp116 fold0): raw values 1,7,15 on both union-support boundaries, causal response-position masks at ticks 1 and 3; select nearest original null and nearest compensated null by integer Hamming, lexicographic tie break. No heldout outcomes used.
- Evaluate 24 disjoint raw-value inputs (all remaining 12 values × 2 sides) at ticks 6,12,24 by response-mask Jaccard and exact equality relative to original G0. Aggregate patches within parent, then equal-weight parent mean. No class/survival effect is inferred.

## Results

| Width | Eligible patches | Parents | Distinct compensated states (summed per patch) | G0 minus compensated nearest, tick24 Jaccard | G0 minus original nearest, same patches | G0 win / loss vs compensated |
|---|---:|---:|---:|---:|---:|---|
| 1 | 10 | 9 | 17 | +0.00134 | −0.02337 | 5 / 4 |
| 2 | 9 | 9 | 21 | −0.00224 | −0.05784 | 4 / 5 |
| 3 | 9 | 6 | 35 | +0.03068 | +0.02207 | 2 / 4 |

The previously substantial positive width-3 pooled contrast from Experiment 117 **does not translate to strong discrimination** on the 6 parent pairs having distance-compensated controls. The width-3 difference is small and the parent sign comparison is 2 vs 4. This cannot be directly compared to the full 16-parent prior result without accounting for support loss: the table includes an old-control benchmark restricted to the **same** 9 patch contexts.

## Strict interpretation

Distance compensation repairs only one serious asymmetry. The control receives an additional site edit (width+1 vs width), and the null pool is conditioned on previously valid 113 patch values, not a uniform physical ensemble. Thus even a nonzero difference would not establish a privileged temporal interaction mechanism or autonomous organization. Unequal edit budgets remain a potential physical confound.

Neither this result nor the 118 proximity theorem rejects the 108 persistence association. All comparisons target **G0 response similarity** under deterministic local physics, not reproduction, learning, survival goals, SELF, or emergent information selection.

## Run

```sh
python experiments/119_compensated_heldout_audit/run.py --output experiments/119_compensated_heldout_audit/results/default.json > experiments/119_compensated_heldout_audit/results/default.txt
python experiments/119_compensated_heldout_audit/test_smoke.py
```

Full patch-level fixed train selections and parent-weighted results are preserved in the JSON. Results were regenerated and tested with the existing source kernel.
