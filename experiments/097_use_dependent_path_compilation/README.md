# Experiment 097 — use-dependent path compilation audit

## Question

The finite-speed mutual-modulation kernel has metastable coarse activity and history-dependent propagation cost.

Does repeatedly exercising a source path make later perturbations from that same source propagate more cheaply than perturbations from an equally trained alternative source?

A positive result would be a weak form of use-dependent compilation. It must survive timing controls; otherwise it is only phase entrainment.

## Cross-over setup

For each random background choose two source windows separated by three windows on the ring.

Create two equal-budget training histories:

- repeatedly flip one bit at source A, with autonomous evolution between flips;
- repeatedly flip the same bit at source B, with the same timing schedule.

After training, measure distance-6 propagation cost for probes at both A and B.

A matching advantage means:

- A-trained is cheaper than B-trained when probing A;
- B-trained is cheaper than A-trained when probing B.

No reward, target feedback, retention counter, or path label is present.

## Fixed-gap sweep

64 backgrounds, two rotation orientations, 12 source positions, 12 repetitions:

| ticks between repeated probes | matching cheaper | mismatching cheaper | ties |
| ---: | ---: | ---: | ---: |
| 1 | 1283 | 1283 | 506 |
| 2 | 1337 | 1298 | 437 |
| 3 | 1377 | 1228 | 467 |
| 4 | 1243 | 1352 | 477 |
| 5 | 1311 | 1280 | 481 |
| 6 | 1332 | 1291 | 449 |

The sign changes with timing. In particular, gap 3 favors the matching source while gap 4 favors the mismatching source.

## Irregular timing control

Using the same 12 repetitions but irregular gap schedules:

### Schedule A

`1,4,2,5,3,6,1,4,2,5,3,6`

- matching cheaper: **1339**
- mismatching cheaper: **1279**
- ties: **454**

### Schedule B

`2,5,1,6,3,4,2,5,1,6,3,4`

- matching cheaper: **1285**
- mismatching cheaper: **1309**
- ties: **478**

The direction reverses between two equally valid irregular schedules.

## Interpretation

The current kernel does not show robust use-dependent path compilation.

Repeated local use certainly changes the later propagation landscape, but whether that change benefits the exercised path depends strongly on temporal schedule and phase.

Therefore the positive fixed-gap cases should be interpreted as schedule/phase-dependent hysteresis, not learning.

This extends the earlier boundary:

> history-dependent causal cost is not sufficient for adaptive cost reduction.

## Next question

The missing ingredient may be a generic physical trace of **actual local interaction**, not merely the state changes produced by the interaction.

A minimal next substrate should remain local and finite-speed, but allow an interaction to leave a short-lived raw trace in the same medium that can alter later neighboring interactions.

The trace must not encode success, reward, source identity, or an explicit path label. The first falsification target is whether this generic local trace produces timing-robust use-dependent propagation without hard-coding the exercised path.
