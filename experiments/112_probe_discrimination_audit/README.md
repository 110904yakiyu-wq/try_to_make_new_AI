# Experiment 112 — Fixed 30-probe discrimination audit

## Question and frozen setting

Experiment 111's six probes distinguished the G0 parent from an exact-
geometry/on-cycle control in only 2 of 20 pairs sharing the same *first
unperturbed tick changed-position mask*. Does an entirely prespecified
panel of **all 15 nonzero 4-bit values at both cycle-union boundaries**
improve outcome-class identifiability before evaluating further local
transplant transfer?

The main assay is a **measurement diagnostic**, not proof of a causal
organization mechanism. Physics stays identical to Experiment 104/108:
60 four-bit windows in a ring, center 30, left rotation, three scheduler
phases, phase-zero frame, 500-tick censor horizon. 108's 100-attempt
preintervention cycle-period, exact union-support-positions, phase-zero
instantaneous-occupancy and scheduler-phase matching is reused unchanged.
Only pairs with exactly equal first-autonomous-tick changed physical sites
are included. The material-response outcome is never used to choose a
control or qualify a parent pair.

Probe order is fixed: left boundary values 1..15, then right boundary
values 1..15. There is no adaptive probe selection. Each individual
probe outcome is `connected`, `fragmented`, `static`, or `censored`.
`censored` means **no confirmed cycle by tick 500**, not a failed
organism or proof of eventual inactivity. A class difference is counted
as *informative* only when both reference arms resolve to different
classes. Postperturbation cycle-period and exact union-support discordance
are secondary physical observables even when both arms have the same
coarse response class.

## Completed reference diagnostic

| Quantity | Six frozen legacy probes | All 30 probes |
|---|---:|---:|
| Parent-by-probe comparisons | 120 | 600 |
| Both reference arms resolved | 71 | 420 |
| Reference class disagreements (both resolved) | 2 | 10 |
| Parents with at least one such disagreement | 2 | 8 |
| Resolved cycle-period disagreements | 46 | 283 |
| Resolved exact union-support disagreements | 32 | 263 |
| At least one arm censored | 49 | 180 |

The population remains **130 G0 parents -> 55 exact 108 controls ->
20 first-mask-matched pairs**. The larger fixed panel identifies six
additional parents, but the effective reference discrimination budget is
still **10 resolved class-discordant probes from 8 parents**. The 600
probe rows are repeated tests on 20 pairs, not 600 independent systems.

## Secondary conditional local transplant (exploratory)

Given the improved discrimination, we repeated the *unchanged* 111
patch and null protocol, now scoring the predeclared 30-probe reference
panel. The donor and recipient are the same preintervention G0/control
pair. A contiguous patch of width 1, 2 or 3 is eligible only if copying
the G0 bit values into the control keeps its first-unperturbed-tick
changed-position mask **identical**. At exactly those patch sites, four
random nonzero bit assignments different from the recipient's values
are sampled, also required to preserve that identical mask. No
perturbation response is inspected before patch/null eligibility is
frozen. The random seed and maximum 256 proposals per patch are exactly
the same as Experiment 111; duplicates are possible.

For each parent, transfer is the fraction of the parent's informative
reference probes for which the patched state confirms the G0 coarse
class, counting a patched `censored` response as **unconfirmed** but
tracking censoring separately. Fractions are averaged across patches
*within each parent*, then across informative parents. The null fraction
first averages across the four controls for each patch. This is
**conditional descriptive matching**, not a randomized independent-parent
causal effect estimate.

| Patch width | Eligible patches | Informative parents (among parents with patches) | G0 donor mean | Matched random mean | Difference | Parent win / loss / tie |
|---|---:|---:|---:|---:|---:|---|
| 1 | 35 | 8 | 0.4375 | 0.234375 | +0.203125 | 4 / 1 / 3 |
| 2 | 16 | 5 | 0.4000 | 0.225000 | +0.175000 | 1 / 1 / 3 |
| 3 | 20 | 6 | 0.3333 | 0.229167 | +0.104167 | 3 / 2 / 1 |

The donor's positive mean for each width is **not** established
organization-specific causation: only 8 / 5 / 6 parents are evaluable,
and each provides just one or two informative reference probes. For
width 1 the 4-to-1 non-tie directional count is weak and the 3 ties
matter. The null does not match all possible raw bit statistics,
subsequent scheduler-phase traces, or postperturbation convergence
rates. Distinct raw values and orbit basins remain alternatives.

Counts of censored **probe applications**, not independent parent
replicates, are donor 5/3/6 versus random 30/19/30 for widths 1/2/3.
Any confirmed-match fraction must be interpreted with this asymmetry.

## Reproduce

```sh
python experiments/112_probe_discrimination_audit/run.py \
  --output experiments/112_probe_discrimination_audit/results/default.json
python experiments/112_probe_discrimination_audit/transplant.py \
  --reference experiments/112_probe_discrimination_audit/results/default.json \
  --output experiments/112_probe_discrimination_audit/results/transplant.json
python experiments/112_probe_discrimination_audit/test_smoke.py
```

`default.json` is a lossless packed archive of all 30 paired responses per
parent: responses ordered left 1..15 then right 1..15; each response
contains G0 `[class, period, support_bitset_hex]` followed by control
triplet. `null` means censored period/support. `run.py` includes a
round-trip-tested decoder, and the `summary` data and all parent-level
records are retained. `transplant.json` stores the 71 patch-level records
and per-parent reference totals. `default.txt` and `transplant.txt`
are human-readable parameter/inventory/summary outputs. Both scripts
are Python standard-library only and reuse the existing GitHub kernel.

## Interpretation and next falsification

Exp108's persistence association is unchanged. Exp112 improves coarse
outcome identification, but does not prove temporally distributed
organizational persistence as a distinct causal mechanism, much less
learning, SELF, reproduction, adaptation or heredity.

A sensible next comparison must separate the effect of G0 bit values
from unmeasured low-level features, for example **matched raw popcount,
local AND-overlap, number of first-tick flips**, and later phase-consistent
execution trace. Freeze the contrast and matching constraints before
computing response transfer; preserve censoring and parent units. One
should not introduce any new cognitive primitive or physical kernel
solely to produce a positive experimental outcome.
