# Experiment 107 — match period, support and physical phase

## Rationale

Experiment 106 showed strong persistent-connected-activity differences
between G0 and independently formed active cycles. However only 4/116 pairs
shared both period and union-support size. This audit tightens control
matching, without selecting on any material-injection outcomes.

## Protocol

For each of 130 phase-0 G0 parent cycle frames, randomize the occupied values
up to 100 times. Accept the FIRST candidate whose unperturbed trajectory
enters a nonstatic bounded cycle with exactly the same:
- cycle period;
- number of positions in cycle-union support.

Take the accepted control's own maximum-support phase-0 frame and inject
the same 15 raw values at both edges of its own union-support region.
All outcome comparisons are paired by original parent.

An optional --exact-phase0-occupancy filter also requires identical
nonzero positions in the compared phase-0 frames. This leaves a smaller
pre-intervention-selected subset. The full union-support *positions*, raw
bit contents and response geometry are not necessarily identical.
Cycle detection is censored at 500 ticks.

## Results

|  | Period+support (69 pairs) | Also exact phase-0 occupancy (54 pairs) |
|---|---:|---:|
| G0 strict fission | 2 | 2 |
| Control strict fission | 3 | 3 |
| G0 connected active | 1866 | 1455 |
| Control connected active | 1519 | 1192 |
| G0 censored | 157 | 143 |
| Control censored | 488 | 390 |

Each paired organization is tested with 30 perturbations.

In the 54-pair stronger subset, G0 has more connected-active outcomes
than its control in 37 parents, fewer in 11, and ties in 6.
Strict fission is negligible and essentially indistinguishable: 2 vs 3.

## Interpretation boundary

Matching the coarse physical organization variables removes the dramatic
fission differential seen in Experiment 106. It does NOT remove the
connected-activity persistence difference.

This supports an OBSERVER-LEVEL association between the particular naturally
formed G0 cycles and continued connected execution after raw perturbation,
under these selected geometries. It is not learning, reproduction, an
objective to persist, or proof of organizational causation independent of
all remaining microstate and union-support differences.

Only 54 of 130 parents satisfy the strongest filter among 100 random
candidate controls each. This selection is severe and results must not be
generalized to all G0. Censored trials are not failures.

## Commands

python experiments/107_period_support_matched_control/run.py
python experiments/107_period_support_matched_control/run.py --exact-phase0-occupancy

Next: explicitly match the cycle-union occupied positions and test whether
the extra persistence is merely a local bit-density/motif effect, or is
associated with relationally organized temporal dynamics.
