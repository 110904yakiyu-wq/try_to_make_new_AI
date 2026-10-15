# Experiment 106 — on-cycle control for daughter outcomes

## Question

Experiment 105 random compact states usually did not start on an attractor.
Does the G0 connected-activity persistence advantage remain when controls
also start at a phase-0 frame on a pre-existing autonomous localized cycle?

## Control construction

For each G0 parent, randomize the nonzero values at the SAME occupied sites
up to 12 times (fixed deterministic seeds). Accept the first candidate
whose UNPERTURBED trajectory reaches an active localized cycle by tick 500.
Then, unlike Experiment 105, **take a phase-0 maximum-support frame from
that control's actual cycle**. This resolves the gross on-cycle confound.

Perturb the actual and control frame with one raw 4-bit value 1..15 at either
side of EACH organization's own cycle-union boundary. No candidate is selected
based on its daughter outcomes. Parent is the statistical comparison unit.

## Results

Eligible pairs: 116/130; 30 interventions per paired organization.

| Outcome | Original G0 | Independent on-cycle control |
|---|---:|---:|
| Strict fission | 12 | 167 |
| Fragmented / nonviable | 71 | 304 |
| Connected active | 3088 | 2376 |
| Static | 56 | 11 |
| Censored at tick 500 | 253 | 622 |

Parent-level connected-active advantage: original higher in 78, control higher
in 24, tied in 14 of the 116 pairs. However, only **4 of 116** controls
match their G0 parent in both cycle period AND union-support size.

## Claim boundary

The persistence difference is not explained ONLY by the random controls
starting off attractor. But this is not a fully matched organization
comparison: cycle period, support geometry and material positions may differ.
The 12-vs-167 fission difference is therefore not evidence of an intrinsic
reproduction-suppression objective or of learned adaptation.

Next: match period and support size, and ideally occupied positions at
phase zero. Preserve the resulting small eligible sample and report the
control-selection constraint explicitly.

## Run

python experiments/106_on_cycle_control/run.py
