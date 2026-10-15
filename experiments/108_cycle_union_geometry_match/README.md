# Experiment 108 — exact cycle-union support matching

## Question

Experiment 107 matched period, union-support SIZE and snapshot occupancy,
but not the exact set of positions occupied during the entire cycle.
Does the G0 connected-activity persistence advantage remain after exact
cycle-union geometry matching?

## Method

Keep the unchanged width-4, three-phase finite-speed kernel and 130
G0 organizations. For each, generate up to 100 random nonzero
value assignments preserving its observed phase-0 occupied positions.
Evolve each random candidate autonomously *before the perturbation*.
Accept the first candidate whose on-cycle state has:

- identical cycle period;
- identical complete cycle-union support POSITION SET;
- identical phase-0 instantaneous occupied POSITION SET.

All comparisons use the same scheduler phase and 30 one-window
material perturbations (15 raw values on either side of the common
cycle-union support). Treat parents, not individual perturbations,
as independent comparison units. Nonconvergence at tick 500 is censored.

## Result

55/130 parents have an eligible on-cycle control within 100 attempts.

| Outcome (1650 trials per arm) | G0 | matched control |
|---|---:|---:|
| Strict fission | 2 | 2 |
| Fragmented, daughter criterion not met | 15 | 28 |
| Connected active cycle | **1486** | **1215** |
| Static | 4 | 7 |
| Nonconverged by tick 500 | 143 | 398 |

Across the 55 paired parents, connected-active is higher in 37
G0s and 11 controls; 7 ties. Accepted attempt median is 32.

## Interpretation boundary

The connected-persistence difference is not solely attributable to
period, cycle-union support positions, instantaneous active positions
or scheduler phase. However the **raw 4-bit values** are different and
the groups remain selectively sampled (55/130).

In a deterministic Markov kernel, exactly matching the full physical
microstate AND scheduler phase makes futures identical. This assay
cannot establish an irreducible history variable or intrinsic drive
to reproduce. It is conditional persistence associated with a
particular dynamically reachable organization.

Censored runs are NOT inactivity, death or failed reproduction.

## Run

python experiments/108_cycle_union_geometry_match/run.py

Next: causal internal-window transplantation, with a matched
synthetic-donor null, to test whether the persistence signature
is carried by one or by several raw local windows.
