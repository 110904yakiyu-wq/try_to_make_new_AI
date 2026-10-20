# Experiment 152 — Pretest physical state overlap after external experience

Experiment151 observed higher heldout causal susceptibility after one earlier external pulse. To distinguish that from a claim of abstract acquired knowledge, check whether the *post-pulse physical state* can be balanced on two simple low-level observables **without using heldout outcomes**:

1. Total set 4-bit count across all 60 windows;
2. Total number of occupied (nonzero) windows.

Restrict first to contexts where the heldout target site is empty for sham/raw7/raw11. Study exact equality on either feature or both, by arm pair. Do **not** interpret conditioning on a downstream-of-training feature as an unbiased causal mediation estimate.

## Main finding

| Pretest delay | Eligible site contexts | Sham vs raw7: both physical counts equal | Sham vs raw11: both equal | raw7 vs raw11: both equal |
|---|---:|---:|---:|---:|
| 24 | 228 | **2** | 3 | 76 |
| 96 | 219 | **2** | 2 | 78 |

The severe 2/228 and 2/219 support for sham/raw7 identifies a **positivity/overlap failure** for this particular attempted low-level match. Means restricted to these tiny subcohorts are not evidence for or against learning. Matching on both scalar features does not match the full raw microstate or its exact future.

Source is the frozen Exp151 lossless CSV archive; no additional simulation or learner is added. Rerun:

```sh
python experiments/152_pretest_physical_overlap_audit/run.py > experiments/152_pretest_physical_overlap_audit/results/default.txt
python experiments/152_pretest_physical_overlap_audit/test_smoke.py
```
