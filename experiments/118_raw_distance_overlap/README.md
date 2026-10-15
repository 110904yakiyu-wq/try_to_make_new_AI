# Experiment 118 — Raw-source proximity confounding and one-extra-site overlap

## Motivation

Experiment 117 retained width-3 favorable held-out response similarity across five train/test raw-material splits. However, every real donor patch in Experiments 109–117 is copied **directly from the original G0 reference**, while every distinct-null patch must differ from that original copied patch. As all states outside the patch are exactly the same recipient microstate, any legal fixed-patch null has strictly larger raw-bit Hamming distance to G0. Under this asymmetry, higher donor-to-G0 future-response similarity is expected even in wholly ordinary nonlinear physics.

## Formal support failure

For original source `G`, recipient `C`, selected patch `P`, donor transplant `T`, and any distinct fixed-patch alternative `N` with `N_i = C_i = T_i` for all `i` outside `P`, and `T_i = G_i` for all `i` in `P`,

\[
 d_H(N,G)-d_H(T,G)=\sum_{i\in P}\operatorname{popcount}(N_i\oplus G_i)>0.
\]

Therefore no distinct fixed-patch alternative has **equal raw-bit Hamming distance** to G0, irrespective of matching popcount/AND/first-tick mask. For the full-feature-matched 113 nulls, all extra distance gaps are **even** due to equal popcount, and the 506 candidate gaps are: 2 (151), 4 (147), 6 (135), 8 (64), 10 (9).

This is a causal identification limit of the chosen *donor-relative-to-source* outcome contrast, not absence of physical dynamics or a refutation of the 108 persistence association.

## Feasibility repair: one additional external edited site

To see if raw-distance-equivalent comparison is possible with **one extra physical edit**, for each 113 strongest-tier null patch, enumerate every originally G0/recipient-different occupied site outside the patch, and assign every alternative nonzero 4-bit value. No injected-material response is inspected. Count candidates satisfying nested filters:

1. Exact raw-bit distance to G0 equal to the G0 transplant's distance.
2. Plus same first unperturbed tick's changed-site mask.
3. Plus exact total popcount.
4. Plus exact adjacent-neighbor bitwise AND popcount.
5. Plus exact first-tick bit-flip count.

A compensated state necessarily edits one extra occupied window beyond the original selected patch; **the support/number-of-edited-windows is no longer identical between donor and control**. This compensates one confound but introduces another. Only 113 full-feature-matched *base patch* nulls are considered before the extra edit, so this is a **conditional census**, not all globally possible controls.

## Results

| Width | Original eligible patches | Original exact-feature null microstates | Compensated full-feature patches | Distinct states, summed per patch |
|---|---:|---:|---:|---:|
| 1 | 23 | 33 | 10 | 17 |
| 2 | 14 | 59 | 9 | 21 |
| 3 | 20 | 414 | 9 | 35 |

Across the 57 patch contexts, **28** contain at least one distance-compensated fully feature-matched alternative (17 + 21 + 35 = 73 distinct *patch-conditional* candidate states). Counting unique states over different patch contexts would require global deduplication and is not claimed.

## Interpretation

This demonstrates that source-proximity support was impossible under the old fixed edit-site constraint but can be partially restored by allowing one additional compensatory edit. It does **not** imply causal equivalence: changed-site budgets differ. No outcome claim is made in 118. The next experiment should freeze exactly these candidate sets and evaluate held-out responses (training response selection separated), comparing on the **identical 28 patches** against the original 113 nearest physical alternative and against the donor. Report all losses of eligibility by patch and parent.

## Reproduction

```sh
python experiments/118_raw_distance_overlap/run.py --output experiments/118_raw_distance_overlap/results/default.json > experiments/118_raw_distance_overlap/results/default.txt
python experiments/118_raw_distance_overlap/test_smoke.py
```

Python standard library. Complete per-patch candidate counts and raw-gap histograms are archived in JSON. Neither the 104 physical kernel nor the previous results have been modified.
