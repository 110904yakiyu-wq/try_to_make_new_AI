# Experiment 111 — secondary censor-aware distance audit

## Relation to the primary Experiment 111

The existing `run.py` and `README.md` in this directory are the **primary**
Experiment 111 assay. They test contiguous patch widths 1–3 and count only
**resolved, discordant reference material probes** as informative, leaving
only **two informative parent pairs** under that definition. Do not conflate
those primary denominators with this *secondary* audit.

This additional script tests only **single-window** substitutions and uses a
**three-category Hamming response distance** that explicitly treats
`censored` as a distinct finite-horizon observer label. It counts donor vs
recipient censoring differences toward a distance, so it produces a larger
`informative` cohort (16 parents), but these extra differences **do not
constitute confirmed transfer of persistence**. No inferential claim takes
priority over the primary resolved-probe analysis.

## Question

Experiment 108 found an association between G0 origin and connected-active
cycle detection after material injection despite exact matching of phase-0
nonzero sites, cycle period and all positions visited during the autonomous
cycle. Experiment 110 reduced the parent-level advantage after matching the
first autonomous tick's changed-site set. Is a *specific G0 raw window value*
causally transferable, beyond the effect of inserting another value that
preserves the same immediate physical execution mask?

This experiment does **not** add cognition, reproduction, learning, reward,
SELF, history variables, or a new kernel. It uses the Experiment-104/108
60-window, 4-bit, `left`-rotation, three-phase local update law, `CENTER=30`
and phase 0. The tested units are 4-bit physical windows, not learned symbols.

## Prespecified comparison

1. Reconstruct Experiment-108's first eligible on-cycle control for each of
   130 G0 parents using up to 100 fixed-seed attempts **without inspecting
   material-probe outcomes**. Match autonomous cycle period, exact full-cycle
   union-support position set and phase-0 instantaneous nonzero position set.
2. Retain pairs with the **same exact set** of positions changed by the
   unperturbed autonomous first tick. This yields 20 of the 55 pairs in 108.
3. For each physical site where G0 donor and control recipient contain
   different nonzero values, insert the donor's *single* raw value into the
   recipient. Retain an intervention only if the entire unperturbed first-tick
   changed-site set is unchanged. This changes no position/occupancy at t=0.
4. At that **same site in that same recipient**, identify all alternative
   nonzero raw values that preserve that first-tick mask, excluding donor and
   recipient values. The primary null is a fixed-seed sample of at most two
   alternatives. A tighter null also matches the number of bit flips from
   the recipient value. Both samples are selected using only the physical
   masks and fixed seeds, before running any material-probe outcomes.
5. Measure six material probes: left/right adjacent sites just outside the
   shared cycle-union support, with raw values 1, 7, 15; same 500-tick
   horizon. Record one of `connected_active`, `other_cycle`, `censored`.
   Unlike a Boolean collapse, **censored is its own category**, not failure.
6. Let `gap` be the six-category Hamming distance between the original G0
   donor and the recipient response signatures. For a local replacement,
   `gain = gap - Hamming(replacement_signature, donor_signature)`.
   Positive gain means closer to G0, negative means farther away. Report
   means of interventions **within each parent, then means across parents**
   (never treat material probes or window replacements as independent units).
   `gap=0` sites are non-informative for directional response transfer.

Optional secondary audit: `--require-probe-mask` also requires the exact
first-update changed-site set after **each of the six injected materials**
to coincide across G0, recipient, transplant and each null. This is a much
tighter low-level physical constraint, not a temporal-organization test by
itself. The two arms have different eligibility and should not be pooled.

## Results — primary, full 130-parent scan

| Quantity | Observation |
|---|---:|
| G0 parents examined | 130 |
| Exact Experiment-108 matched pairs | 55 |
| Same first-tick changed-site mask | 20 |
| Admissible physical sites with null alternatives | 34 across 20 parents |
| Informative sites (donor/recipient signature differs) | 27 across 16 parents |
| Exact transfer of all six labels | 2 of 27 informative sites |
| Mean G0-directed gain, averaging parent means | 0.000 |
| Mean same-mask null gain, averaging parent means | -0.448 |
| Mean G0-minus-null gain | +0.448 (10 positive, 5 negative, 1 tie parents) |
| Mean stricter same-mask/same-bitflip null gain | -0.781 |
| Mean G0-minus-stricter-null gain | +0.781 (11 positive, 2 negative, 3 tie parents) |
| Donor/recipient/transplant also share injected first-update masks on all six probes | 10 of 34 sites |

The G0-directed single-window replacements did **not** improve mean
similarity to the G0 future-response signature. Other physically compatible
raw replacements often made the response signature less similar, so a
positive **relative** G0-vs-random-null difference does not constitute
positive absolute transfer or evidence of a special multi-tick mechanism.
The nulls are not guaranteed to be on-cycle; the comparison can reflect
ordinary microstate compatibility with an on-cycle background.

## Results — stricter probe-conditional changed-mask audit

When the immediate changed-position mask must also match for every material
probe (including matched null alternatives), **10 eligible sites across 7
parents** remain. Nine sites across six parents have non-identical donor and
recipient response signatures:

| Parent-weighted metric | Observation |
|---|---:|
| Mean actual G0-directed gain | +0.333 |
| Mean same-mask null gain | -0.375 |
| Mean excess actual over same-mask null | +0.708 (5 / 1 / 0 positive/negative/tie parents) |
| Mean actual gain on same-bitflip-null comparable subset | +0.167 |
| Mean same-bitflip null gain | -1.056 |
| Mean excess actual over same-bitflip null | +1.222 (6 / 0 / 0 parents) |
| Exact six-label transfer among informative sites | 2 of 9 |

This subset is small and strongly selected by physical masks. The weak
positive absolute mean cannot establish a distinct temporal interaction
mechanism. Observed label changes include changes in the 500-tick censoring
category; they are not automatically changes in long-term persistence.

## Interpretation and limitations

- This is a **single-window intervention on already selected parent pairs**;
  unlike a matched on-cycle organization, a partially transplanted frame need
  not itself lie on an autonomous cycle. Thus transferability of a multi-site
  organization is not identified.
- The only causal manipulation is a raw 4-bit value substitution. There is
  no demonstration of history-only effects at equal full microstate+phase;
  these are impossible in this deterministic Markov substrate.
- The paired parent is the analysis unit, but G0 parents belong to a finite,
  structured enumeration, not a random population; no population p-value or
  confidence claim is assigned to the small selected subsets.
- Two fixed-seed null samples per site were used to keep the finite CPU budget
  practical. Results may depend on null sampling. The categorical six-probe
  signature is not a full future trace. `other_cycle` combines several cycle
  categories and must not be interpreted as death or failure.
- Material probes at 500 ticks remain right-censored when periodicity is not
  identified. Absolute infinite-horizon persistence is not measured.

**Current conclusion:** persistence associations survive exact geometry
matching, but Experiment 111 does **not** establish that organization-specific
long-horizon temporal interaction is the cause. Simpler raw-bit configuration
and phase-aligned physical-mask explanations remain live.

## Reproduce

```sh
python experiments/111_conditional_local_bit_swap/secondary_censor_aware_distance.py
python experiments/111_conditional_local_bit_swap/secondary_censor_aware_distance.py --require-probe-mask \
  --output-csv experiments/111_conditional_local_bit_swap/results/probe_mask_strict_site_trials.csv
```

The first run writes `results/site_trials.csv` and stdout corresponding to
`results/censor_aware_default.txt`. The second writes
`results/probe_mask_strict_site_trials.csv` and stdout corresponding to
`results/censor_aware_probe_mask_strict.txt`. Both use `--attempts 100`,
`--max-ticks 500`, `--null-per-site 2`. Each CSV records the parent and
intervened site, raw values, Hamming gap, actual gain, alternative pool sizes,
selected null counts, null mean gains and injected first-mask agreement.

### Next falsification direction

Before adding physical primitives, test whether an **entire multi-window
phase-consistent intervention** transfers a future-response profile relative
to comparably conditioned replacement patterns. Avoid choosing the best site
using the evaluated probes. Match physical response masks and separate true
cycle convergence from finite-horizon censoring.
