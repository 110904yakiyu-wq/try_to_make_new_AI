# Experiment 109 — minimum causal window transplant

## Motivation

Experiment 108 matched period, exact cycle-union support positions and
phase-0 occupied positions, leaving G0 and control with different raw
4-bit values at several sites. Does G0's distinctive future-response
profile require **multiple** internal windows to be transplanted, and
is that multi-window requirement stronger than a synthetic null?

## Assay

Use the 55 G0/control parent pairs accepted under Experiment 108.
For each, record six boolean outcome probes:

- inject raw value 1, 7 or 15 just outside the left cycle-union boundary;
- apply the same three probes just outside the right boundary;
- output whether an active, spatially connected cycle is detected
  by tick 500, with all other outcomes classified false **only for
  this fixed six-probe signature**.

For each pair, exhaustively transplant every subset of internal windows
whose raw value differs from G0 to control. Report the minimum number
required to reproduce the complete G0 six-probe response signature.

If the original response signature already matches, the minimum is zero.

Null: for each parent, create TWO randomized synthetic donors that
differ from the same recipient at exactly the same physical sites as
G0. Each changed value is a random nonzero 4-bit value different from
the recipient at that site. Count the corresponding minimum transfers.

These randomized donors are NOT preconditioned to be on-cycle. The null
is a diagnostic for ordinary nonlinear bit-site combinatorics, not a
fully dynamics-matched organization control.

## Results

55 actual donor/recipient pairs; 110 null donors.

| Minimum transferred internal windows | G0 donor | randomized donors |
|---|---:|---:|
| 0 | 8 | 0 |
| 1 | 6 | 28 |
| 2 | 11 | 26 |
| 3 | 13 | 24 |
| 4 | 13 | 29 |
| 5 | 4 | 3 |

Mean minimum number (including already-matching profiles):
- G0: **2.5273**;
- synthetic null: **2.5727**.

Compare the actual requirement against each parent's average of its
two randomized-donor requirements:
- actual needs more: **22** parents;
- randomized donors need more: **24** parents;
- equal: **9** parents.

## Claim boundary

Several internal windows often have to be combined to reproduce a
response signature. But the required cardinality is not meaningfully
larger than the matched-sites randomized donor baseline here.

Therefore the transfer test supplies NO evidence for organization-
specific distributed causal composition. Multi-site dependence alone
is expected in a locally interacting nonlinear finite-state medium.

This audit does not erase Experiment 108's persistence association.
It prevents the much stronger interpretation that G0 internal windows
are an emergent compositional language or self-model.

The six-probe signature is a resource-bounded, retrospective observer
measurement, not an internal objective and not the entire future.

## Run

python experiments/109_causal_window_transplant/run.py

Further controls should test which physical attributes (local
AND-overlap, instantaneous activity pattern, bit density) coincide
with the remaining connected-cycle persistence differences.
