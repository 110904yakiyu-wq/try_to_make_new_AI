# Experiment 121 — Heldout response for equal edit budget and raw-Hamming matched nulls

## Method

- Reuse Experiment 120's *preoutcome* feasibility cohort: only **15** patch contexts across the same frozen 112 parent roster; widths 1/2/3: 3/5/7 patches, 2/4/5 parent clusters.
- Regenerate the exact fully matched alternative states from 120's one-for-one exchanged edit-site sets. Assert the state count per patch equals the precommitted 120 census; all must preserve equal window edit number, global G0 distance, first changed-site mask, popcount, ring adjacent AND and first autonomous bit-flip count. No material-response outcomes are involved in candidate selection.
- For comparison, regenerate 113's original fixed-site null pool and restrict its reporting to exactly the same 15 contexts.
- Select *one* alternative per null pool by nearest initial **6 train probes** (raw 1,7,15 × two boundaries; response-position-mask Hamming at ticks 1 and 3), lexicographic microstate tie rule. Test on the 24 other raw-value probes (12 values × 2 sides), at ticks 6,12,24, evaluating response-mask Jaccard and equality relative to the original G0 parent. Equal weighting: patch within parent, parent within eligible cohort. No cycle outcome test in this experiment.

## Results: tick24 Jaccard, donor minus null

| Width | Parent clusters | Patch contexts | Donor − equal-budget null | Donor − old fixed-patch null on same contexts | Wins/losses/ties vs equal-budget |
|---|---:|---:|---:|---:|---|
| 1 | 2 | 3 | −0.04530 | +0.08870 | 0 / 1 / 1 |
| 2 | 4 | 5 | +0.04481 | +0.12874 | 3 / 1 / 0 |
| 3 | 5 | 7 | +0.08090 | +0.10300 | 1 / 2 / 2 |

There is no persuasive consistent G0 advantage: even in width 3 the parent sign test is 1 positive, 2 negative, 2 ties. Small matched support and different edited positions preclude an organization-specific causal claim. The old-control row is computed on identical eligible contexts to separate selection loss from comparator design; it is not a randomized counterfactual comparison.

## Run

```sh
python experiments/121_equal_budget_heldout/run.py --output experiments/121_equal_budget_heldout/results/default.json > experiments/121_equal_budget_heldout/results/default.txt
python experiments/121_equal_budget_heldout/test_smoke.py
```

Full per-patch nearest training distances, candidate inventories, and per-parent aggregates are preserved in JSON. No new physical or cognitive primitive.
