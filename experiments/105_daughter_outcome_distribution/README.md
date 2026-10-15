# Experiment 105 — daughter outcome distribution audit

## Question

Experiment 104 found 36 strict fissions in 3900 phase-aligned conditions.
Do the full daughter outcomes, rather than only a binary fission score, differ
from matched random compact patterns? Does any difference survive controls
for basic pre-intervention dynamical viability?

## Crucial phase contract

Experiment 104 uses CENTER=30, divisible by the three-phase scheduler period.
Changing CENTER to 20 changes the physical experiment. Reconstructing at
CENTER=20 misleadingly gives 100 instead of 36 strict fissions. Both the
130-parent catalog period distribution and the 36/3900 result are reproduced
when the phase contract is respected.

## Parent-clustered design

For each of the 130 G0 parents take a maximal-support phase-0 cycle frame.
Add exactly one raw 4-bit window at either union-support boundary, testing
all values 1..15: 30 conditions per parent.

Random control frames preserve the occupied positions but randomize nonzero
values. Each parent-level null replicate is held fixed across all 30
intervention conditions, preserving dependence within the parent cluster.
Outcomes: strict fission, fragmented/nonviable, connected active, static,
and censored/nonconverged.

Run: python experiments/105_daughter_outcome_distribution/run.py --nulls 2 --max-ticks 500

| Outcome (3900 trials per arm) | G0 | Null 1 | Null 2 |
|---|---:|---:|---:|
| Strict fission | 36 | 37 | 45 |
| Fragmented/nonviable | 144 | 109 | 119 |
| Connected active | 3396 | 737 | 714 |
| Static | 56 | 8 | 18 |
| Censored at 500 ticks | 268 | 3009 | 3004 |

The pooled-category total variation is 0.703462. This is overwhelmingly
driven by the huge difference in cycle convergence; the null compact states
are generally NOT already sitting on attractor cycles.

Therefore this does not demonstrate organization-specific reproductive
control. It does show strong persistence of connected activity in actual
G0 cycle frames compared with a support-only compact random control.
One cannot count censored null cases as confirmed reproduction failures.

## Horizon sensitivity

With the first control replicate and 1000 instead of 500 ticks:
G0 stays (36,144,3396,56,268), and null becomes
(38,111,748,8,2995) in the above category order.
The censoring imbalance remains.

## Viability-selected support-matched control

Run: python experiments/105_daughter_outcome_distribution/viability_control.py

For each G0 parent, independently randomize occupied bit values up to 12 times
and accept the first compact state that, BEFORE intervention, is observed to
enter an active compact cycle by tick 500. Never choose controls based on
their later offspring outcome. 116/130 parents have an accepted control.

| Outcome (3480 trials per arm) | Actual G0 subset | Viability-selected null |
|---|---:|---:|
| Strict fission | 12 | 60 |
| Fragmented/nonviable | 71 | 119 |
| Connected active | 3088 | 1065 |
| Static | 56 | 15 |
| Censored | 253 | 2221 |

Parent-level strict-fission differences: actual higher in 3 parents,
null higher in 34, tie in 79.

But this is NOT a phase-matched on-cycle control: eventual viability does
not imply that the random compact input was on its eventual attractor at
the time of material injection. Nor are period and full cycle geometry
matched. Thus these figures do not prove reduced fertility in G0.

## Claim boundary

- The strict 36/3900 fragmentation effect is reproducible.
- G0 organizations are more stable as connected active cycles than
  raw support-matched random compact frames.
- This is not reproduction or heredity.
- Strict fission alone is too weak a measure; censoring and attractor
  membership are dominant confounds.
- The next assay should compare on-cycle G0 organizations to independently
  generated on-cycle control organizations, documenting period/support
  mismatch and placing material at each organization's live boundary.

Files: run.py; viability_control.py; results/default.txt;
results/horizon1000.txt; results/viability_control.txt.
