# Experiment 120 — Equal edited-window-budget and source-distance positivity census

## Question

Experiment 119 repaired raw-Hamming distance to G0 by editing one additional occupied window in a physical control. Can a *different selection of exactly the same number of edited windows as the G0 transplant* match raw-Hamming distance **and** all previously matched immediate physical features?

## Frozen census (no evaluation responses)

- Unchanged 104 60-window, three-phase left-rotation kernel, CENTER30, phase 0; frozen 112 20 pairs and 113 57 eligible patches.
- For each donor patch `P` of width k (k=1,2,3), construct alternative edit-site sets `Q` by **removing one position from P and replacing it with one different G0/recipient-value position outside P**. This preserves exactly k edited occupied windows (although edit locations change), not necessarily a contiguous patch.
- At every site in Q, enumerate all 14 nonzero values different from the recipient. Exactly 14**k assignments per Q. Before any material-response test, filter by donor-to-source G0 **global 4-bit Hamming equality**, donor's exact first-tick changed-site mask, global popcount, ring adjacent-AND popcount, and total autonomous first-tick bit flips. The requested features are computed on the unperturbed microstate.
- There is no outcome-based selection and no modification of the physical kernel. The census is limited to **one-for-one site exchanges**, not arbitrary k-site edit arrangements.

## Reproduced results

| Width k | Original 113 eligible patches | Candidate assignments enumerated | Exact raw-distance eligible patches | Full-feature eligible patches | Full-feature alternative states (sum per patch) | Informative parents with any full-feature alternative |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 23 | 910 | 19 | **3** | **3** | 2 |
| 2 | 14 | 11,760 | 13 | **5** | **10** | 4 |
| 3 | 20 | 181,104 | 17 | **7** | **15** | 5 |

The full-feature alternative is nonidentical to the donor and has equal edited-window budget and global raw-Hamming to original G0. **But** its edited *locations* differ, so the spatial causal intervention remains unmatched. Equal aggregate popcount/neighbor AND/flip features do not fix detailed local bit patterns or future trajectories.

## Next

Proceed only within the 3/5/7 eligible patch contexts. Train null selection on the old six raw values/ticks 1 and 3, and evaluate held-out 24 distinct material inputs at t6,12,24. Compare to the original old fixed-site physical null **on exactly the same patch contexts**. This does not estimate whole-population persistent organization or reproduction.

## Run

```sh
python experiments/120_equal_edit_budget_overlap/run.py --output experiments/120_equal_edit_budget_overlap/results/default.json > experiments/120_equal_edit_budget_overlap/results/default.txt
python experiments/120_equal_edit_budget_overlap/test_smoke.py
```

Python standard library; no response probes in candidate selection. Save all positive and empty results.
