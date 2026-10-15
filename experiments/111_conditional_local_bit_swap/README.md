# Experiment 111 — Immediate-mask-conditional local bit transplantation

## Question

Experiment 108 found a connected-active persistence association after
matching cycle period, exact union-support positions, phase-zero occupancy,
scheduler phase and material input. Experiment 110 found a small subset
(20/55 matched pairs) with identical *first autonomous tick* changed-site
masks. Does copying genuine G0 local 4-bit contents into its matched
control produce an excess transfer of the G0 material-response signature
relative to random values satisfying **the same initial execution mask**?

This is an exploratory falsification test, not evidence for an endogenous
organization, memory, SELF, learning, reproduction or temporal mediation.

## Frozen assay / selection

- Reuse the **unchanged** `104` finite-speed left-rotation kernel, size=60,
  CENTER=30, phase=0, three-phase scheduler and `108` 100-attempt
  preintervention matching (500-tick horizon).
- Retain a `108` pair only if the parent and control have the same **exact
  first-tick changed physical position set**. This filter uses *no injected
  raw-material response*.
- For contiguous patch widths 1, 2 and 3, enumerate patches fully inside
  positions where donor G0 and control raw 4-bit values differ. Copy the
  original donor values into the control. Retain a transplant only if the
  control's first-tick changed-position mask is exactly conserved. Patch
  selection does not inspect the future-response signature.
- For each retained patch, make 4 independently proposed synthetic
  replacements at **the same sites**, always nonzero and different from
  the recipient values, and retain proposals with exactly the same
  first-tick mask. Fix the RNG formula in `run.py`. Up to 256 proposals
  per patch. If fewer than 4 controls are eligible, exclude that patch
  *before* testing outcomes and report the shortage. Sampling is with
  replacement; equal values across null replicates are possible.
- Six fixed material probes: 1, 7, 15 just beyond the left and right
  cycle-union boundaries of the matched pair. The observed outcomes are:
  `connected`, `fragmented`, `static`, or `censored` (no cycle by tick 500).
  No isolated-daughter viability or reproduction classification is done.
- Informative probes are those for which the G0 and matched control
  **both resolve** and have different outcome classes. This is a fixed
  parent-level comparison denominator shared by the transplanted and
  random arms. A censored transplant counts as **no confirmed G0 match**,
  never as death or failure of reproduction; censored counts are also
  reported separately. If the two reference signatures coincide on the
  fixed probes, the test has **zero transfer-identification power**.
- Aggregate **within parents first** (across eligible patches), then
  across parents with at least one informative probe. Patch/trial counts
  are not independent sample sizes. Widths 2 and 3 are exploratory.

## Results (complete default run)

| Quantity | Result |
|---|---:|
| G0 catalog parents inspected | 130 |
| Exact geometry-matched pairs (108) | 55 |
| Also equal first-tick changed-site mask | 20 |
| Mask-preserving donor patches, widths 1 / 2 / 3 | 35 / 16 / 20 |
| Donor patches with four matching synthetic nulls | 35 / 16 / 20 |
| Parents represented by patches, widths 1 / 2 / 3 | 20 / 11 / 16 |
| Parents with **informative resolved reference probes**, each width | **2 / 2 / 2** |

Per-parent means of *confirmed G0 response match fractions* over
informative probes:

| Width | Donor | Mask-conditioned null | Donor−null | Parent win/loss/tie |
|---|---:|---:|---:|---:|
| 1 | 0.000 | 0.000 | 0.000 | 0 / 0 / 2 |
| 2 | 0.500 | 0.000 | +0.500 | 1 / 0 / 1 |
| 3 | 0.000 | 0.125 | −0.125 | 0 / 1 / 1 |

The six-probe reference signature distinguishes G0 from the control in
**only two of the 20 first-mask-matched pairs**, with **one informative
resolved probe in each pair**. The majority of matched pairs therefore
provide no transfer-specific evidence under this restricted probe budget.

**Interpretation:** no reliable positive support for G0-specific local
content transfer beyond simple execution-mask-matched bit assignments.
The opposing width-2 and width-3 directions are each driven by only two
informative parents and are *not* comparative evidence for a multi-window
organization mechanism. This result does **not** demonstrate equivalence
of the mechanisms, nor does it erase Experiment 108's persistence
association. Replacing a few values does not retain the full autonomous
on-cycle trajectory or its multi-tick temporal structure.

The separate `censored` category remains important: for informative
probe/patch applications the donor has censored counts 1 / 0 / 2
and the random controls 8 / 4 / 6 (widths 1 / 2 / 3). Those are
counts over applications, **not independent parents**.

## Reproduction

```sh
python experiments/111_conditional_local_bit_swap/run.py \
  --output experiments/111_conditional_local_bit_swap/results/default.json
python experiments/111_conditional_local_bit_swap/test_smoke.py
```

The script uses only the Python standard library. The committed
`results/default.json` is the full patch- and parent-level archive;
`results/default.txt` prints parameters, inventory and summary.
The result was executed with the same frozen 104/108 step/orbit/
matching functions reproduced locally for execution, with a 500-tick
limit, and 55 matched/20 exact-first-mask pairs recovered as invariants.

## Boundary / next falsification

The remaining hard problem is measurement informativeness. No conclusion
about temporal interaction structure can be identified from only two
informative parents, and conditioning on a shared first-tick mask can
change the population under study. A follow-up needs a pre-registered
higher-discrimination probe set and/or a more powerful intervention on
phase-consistent multi-tick traces, with explicit censoring and
parent-level replication. Do not invent an additional physics primitive
solely to obtain a positive effect.
