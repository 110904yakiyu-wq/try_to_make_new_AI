# Experiment 113 — Physical-feature-conditioned local replacement null

## Question

Experiment 112's exploratory 30-probe assay found positive **confirmed G0-class response transfer** from an internal G0 patch into a support/phase/cycle-matched control relative to four *first-tick execution-mask*-matched random bit assignments. Is that association robust to matching elementary physical characteristics of the unperturbed transplanted microstate — notably raw bit density, adjacent AND overlap, and immediate one-tick bit flips — without changing the physical kernel?

## Frozen environment and causal contrast

- Unchanged Experiment 104 kernel: 60 circular 4-bit windows, center 30, left rotation, phase-0 initial frame and three-phase scheduler. Horizon: **500 ticks**. A `censored` orbit is unresolved, **not** inactivity, death, or failed reproduction.
- The **frozen Experiment 112 reference archive** defines the cohort: 130 G0 parents, 55 exact Experiment 108 matches, and 20 pairs sharing identical unperturbed first-tick changed-*position* masks. Only eight of those 20 have any reference **class** disagreement in the fixed 30 material probes (15 raw values per left/right support boundary), both arms resolved. Reference outcome disagreements define the common scoring keys *before* comparing transplant and null arms. This remains an observer-defined exploratory outcome contrast.
- For each 1-, 2-, or 3-window contiguous patch where the G0 values differ from the matched control, place G0's values into the control. Retain it if its **unperturbed** first-tick changed-position mask equals the original common mask (71 G0 patches: 35/16/20).
- **Enumerate** every nonzero 4-bit assignment at exactly those patch positions that differs from the recipient at each edited position (at most `14 ** width` candidates). Exclude the entire **G0 patch value assignment**, even when it would satisfy the feature constraints. Require the same full first-tick changed-position mask. This prevents trivial donor-identity controls.
- Compute on each **unperturbed** state the global total popcount, ring-adjacent bitwise AND popcount, and total Hamming flips in the first autonomous tick. Compare an increasing hierarchy of *exact donor-patch feature matches*: `mask`; `mask + popcount`; `mask + popcount + neighbor AND`; `mask + popcount + neighbor AND + first-tick flips`.
- **All admissible alternative microstates** are scored for their response to the *same fixed informative reference probes*. Null probabilities here are **exact uniform expectations across enumerated legal assignments** for each patch, not four sampled nulls. When no distinct matching null exists, the patch is **not evaluable** for that feature tier. These eligibility decisions do **not** inspect injected-material outcomes.
- First aggregate over the eligible patches for each parent, and then equally across informative parents. Compare donor against a mask-only alternative **restricted to exactly the same tier-eligible patches** as a selection diagnostic. Patch counts and enumerable microstates do not increase the number of independent parent pairs.

## Reproduced primary result

### Support and null existence

| Width | G0 mask-pass patches | distinct mask null exists | +popcount | +neighbor AND | +first-tick flips |
|---|---:|---:|---:|---:|---:|
| 1 | 35 | 34 | 31 | 23 | 23 |
| 2 | 16 | 16 | 16 | 14 | 14 |
| 3 | 20 | 20 | 20 | 20 | 20 |

The number of **informative parents** changes as the null constraints become stronger, so naive across-row trend comparisons are *not* causal mediation estimates.

### Parent-weighted confirmed G0-class match fractions (all eligible nulls enumerated)

| Width | Physical null tier | Informative parents | G0 donor | feature-matched null | donor−null | parent wins / losses / ties |
|---|---|---:|---:|---:|---:|---|
| 1 | mask | 8 | 0.43750 | 0.26250 | +0.17500 | 4 / 3 / 1 |
| 1 | +popcount | 7 | 0.35714 | 0.39762 | **−0.04048** | 2 / 2 / 3 |
| 1 | +AND | 5 | 0.50000 | 0.40000 | +0.10000 | 2 / 1 / 2 |
| 1 | +flips | 5 | 0.50000 | 0.40000 | +0.10000 | 2 / 1 / 2 |
| 2 | mask | 5 | 0.40000 | 0.25418 | +0.14582 | 2 / 2 / 1 |
| 2 | +popcount | 5 | 0.40000 | 0.32652 | +0.07348 | 1 / 2 / 2 |
| 2 | +AND | 4 | 0.50000 | 0.40000 | +0.10000 | 1 / 1 / 2 |
| 2 | +flips | 4 | 0.50000 | 0.40000 | +0.10000 | 1 / 1 / 2 |
| 3 | mask | 6 | 0.33333 | 0.28939 | +0.04394 | 3 / 3 / 0 |
| 3 | +popcount | 6 | 0.33333 | 0.32494 | +0.00839 | 3 / 3 / 0 |
| 3 | +AND | 6 | 0.33333 | 0.30100 | +0.03233 | 3 / 2 / 1 |
| 3 | +flips | 6 | 0.33333 | 0.30882 | +0.02451 | 3 / 2 / 1 |

The original Experiment 112 mask-null mean differs because that experiment used **four random draws, including the possibility of exactly reproducing the donor's patch**. Experiment 113 uses full finite enumeration **excluding** exact donor-patch identity. The cohorts and estimands are therefore not numerically interchangeable.

### Same-eligible-patch comparison

When analyzing the **seven** informative width-1 parents with a distinct popcount-matched null, the donor−**mask-only** null difference, using those same patches, is **+0.05714**; the donor−**popcount-matched** null difference is **−0.04048**. Thus **+0.09762** of the change in this descriptive contrast comes from replacing the mask-only null by the popcount-conditioned null *within the same selected patch cohort*. It does not prove popcount is a causal mediator.

Null convergence varies strongly across physical conditions. For width 1, mask-only alternatives on informative patches show **67 censored probe applications / 113 exhaustive candidate-probe applications**, while popcount-matched alternatives show **12 / 29**; these are microstate/probe counts, not independent parents. Confirmation rates treat censoring as **unconfirmed** and report it separately, so they are not identified long-horizon survival rates.

## Interpretation boundary

**No reliable evidence that G0's local patch carries a unique multi-tick organizational causal code.** The positive mask-only width-1 transfer contrast is *not stable* under even exact popcount control; the direction reverses in the selected 7-parent subset. Stronger tiers retain weak positive differences but lose eligible pairs and patch alternatives. Neither observation establishes that popcount, AND, or flips *cause* persistence. Exact first-tick mask and three aggregate features still permit different spatial bit arrangements, second-tick updates, future orbit basins, and phase-consistent temporal trajectories.

This experiment does **not** invalidate the conditional Experiment 108 500-tick persistence association. It does not establish learning, reproduction, endogenous aims, a SELF, an irreducible history variable, or organizational autonomy.

## Reproduce

Run from repository root with Python standard library only:

```sh
python experiments/113_raw_physics_matched_transplant/run.py --census-only \
  --output experiments/113_raw_physics_matched_transplant/results/census.json
python experiments/113_raw_physics_matched_transplant/run.py \
  --output experiments/113_raw_physics_matched_transplant/results/default.json \
  > experiments/113_raw_physics_matched_transplant/results/default.txt
python experiments/113_raw_physics_matched_transplant/test_smoke.py
```

`results/census.json` documents pre-outcome eligibility counts with no transfer-response scoring; `results/default.json` contains **all patch-level and parent-level** results and complete constraint-pool counts; `default.txt` is the condensed readable summary. Exact logical and numerical regression assertions are in `test_smoke.py`. The 104 and 108 local reconstruction used in initial execution implements the same published `step`, `orbit`, `parents` and `matched_control` algorithms; the original 111/112 modules and the reference archive are Git-blob identical to GitHub authorities. No local physics additions are needed.

## Next falsification

Move from a fixed 500-tick confirmed-class indicator to a **resolution-aware** assay and, separately, phase-indexed two-/three-tick physical transition measurements. Freeze measurements and controls before examining further transplant outcomes. Continue treating parent-pair units, constrained support, nonconvergence, and negative results explicitly. Do not add a new learner, reward, reproduction instruction, or symbolic role to obtain a positive result.
