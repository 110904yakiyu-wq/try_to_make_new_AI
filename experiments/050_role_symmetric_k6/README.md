# Experiment 050 — role-symmetric ternary K6

## Motivation

K5 removed explicit opcodes but still assigned a permanent semantic role to the third window M.

K6 removes that hard role. Three ordinary non-overlapping windows participate under one permutation-symmetric physical law.

## Physical law

For width-4 windows `(X,Y,Z)`, a triple is enabled when

`(popcount(X) + popcount(Y) + popcount(Z)) mod 3 == 0`.

The rewrite treats all three windows identically:

- `X' = rotl(Y XOR Z, 1)`
- `Y' = rotl(X XOR Z, 1)`
- `Z' = rotl(X XOR Y, 1)`

There is no mediator, source, target, rule object, reward, learner, or persistent edge.

A stateless scheduler ranks enabled triples by a permutation-invariant content score `(X+Y+Z, X XOR Y XOR Z, sorted(X,Y,Z))`, then uses physical positions only as a tie-break. Both minimum and maximum orientations are tested.

## Initialization

The sparse single-bit background strongly favors all-zero windows. Following Experiment 048, this K6 null uses eight deterministic dense random backgrounds (`seed=0..7`).

## Equal-budget result

Across 8 backgrounds × 32 equal-budget history conditions = **256** comparisons:

- same effective ternary repertoire: **122**
- seq1 strict superset: **8**
- seq2 strict superset: **1**
- incomparable reorganization: **125**
- future eight-event trace differs: **205/256**

Thus order alone can substantially reorganize which ternary content relations are physically executable under a fixed role-symmetric kernel.

## Locking audit

For both members of every comparison, inspect the first and second autonomous events after training (512 trajectories total).

Number of physical endpoint positions shared between event 1 and event 2:

- all 3 positions reused: **493**
- 2 positions reused: **0**
- 1 position reused: **9**
- 0 positions reused: **10**

So K6 removes hard semantic roles, but the first implementation still has strong **local triple locking**: once a content-selected triple wins the scheduler, it usually remains the next winner.

## Interpretation boundary

The useful result is not that a ternary relation exists; the kernel explicitly defines one.

The useful step is narrower:

> no endpoint has a permanently privileged transformation role, while equal-budget history can still reorganize the currently executable relation repertoire.

The major remaining weakness is local triple locking and strong dependence on the rest of the global medium.