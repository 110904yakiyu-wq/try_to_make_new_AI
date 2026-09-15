# Experiment 090 — parallel K8 churn audit

## Question

Experiment 089 removed the period-2 / period-3 observer ontology but did not reveal strong environment-conditioned selection among K8 operational roles.

A natural next step is to let many self-delimiting K8 contexts coexist in the same medium and execute from the same pre-sweep state.

The first implementation used a symmetric parallel update: every start position proposes its K8 rewrite from the same old state and all rewrite deltas are XOR-composed.

This produced persistent activity but very low role-set recurrence, especially for larger key widths.

Why?

This audit separates three candidate causes:

1. overlapping event supports;
2. long self-delimited closure arity / effective propagation range;
3. conflict-resolution policy for simultaneous rewrite demands.

No learning, reward, SELF, organization label, or fitness scalar is added.

## Full parallel K8

A 12-window ring was sampled for widths 3, 4, and 5 over 16 random seeds and 100 sweeps.

Under XOR composition:

- width 3: event-support overlap = **0.810**, role-set Jaccard = **0.082**;
- width 4: overlap = **0.855**, Jaccard = **0.022**;
- width 5: overlap = **0.882**, Jaccard = **0.006**.

A single-bit difference in the initial state affected, after one sweep, approximately half the whole ring and reached nearly the maximum circular distance:

- width 3: 17.94 / 36 bits differ, max distance 17.56;
- width 4: 24.06 / 48 bits differ, max distance 23.25;
- width 5: 30.88 / 60 bits differ, max distance 28.88.

So nominally parallel execution is not operationally local. The K8 scan allows a local start position to recruit a long closure, and many such closures heavily overlap.

## Arity-cap decomposition

For width 4, the same experiment was repeated while allowing closures only up to a maximum arity.

- max arity 2: Jaccard **0.903**, but only 4/16 seeds remain active at the end;
- max arity 3: Jaccard **0.942**, 0/16 remain active;
- max arity 4: Jaccard **0.698**, 3/16 remain active;
- max arity 6: Jaccard **0.080**, 16/16 remain active;
- max arity 8: Jaccard **0.027**, 16/16 remain active;
- full arity 12: Jaccard **0.022**, 16/16 remain active.

This exposes a sharp boundary rather than a smooth improvement:

- strong locality tends toward extinction or near-freezing;
- enough interaction reach to sustain all seeds also produces strong churn.

Locality alone therefore does not solve the problem.

## Conflict-resolution control

With full width-4 K8 closures:

- XOR-composing all rewrite deltas gives mean 23.89 changed bits per 48-bit sweep and Jaccard 0.022;
- rejecting every event whose support overlaps another event gives **zero state change** and Jaccard 1.0;
- allowing only bit positions touched by exactly one event support also freezes completely.

A weaker bit-level control that allows a bit to change only when exactly one event actually proposes a delta on that bit leaves tiny residual motion: mean **0.025** changed bits per sweep and Jaccard **0.994**.

Increasing the allowed number of simultaneous delta proposals gradually restores motion, but that simply introduces an arbitrary arbitration threshold.

## Interpretation

The present failure is not well described as merely "too global" or "too much activity".

The deeper boundary is:

> multiple self-delimited causal processes can demand incompatible changes to the same finite substrate, but K8 has no endogenous notion of who gets temporary use of that substrate.

Two symmetric extremes are both bad:

- compose every demand -> high-churn soup;
- reject contested demands -> frozen medium.

Therefore a metastable ecology appears to require some form of **finite causal occupancy / arbitration**.

This is not yet permission to add priorities, agents, territories, or scheduler-owned identities. Those would reintroduce ontology by hand.

The next question is narrower:

> Can temporary execution rights emerge from the same local interaction history, without persistent owner labels and without a fixed priority order?

A useful next experiment should therefore make conflict itself consume a finite local resource, so an event can proceed only by creating the conditions for its own temporary causal occupancy. The occupancy state must live in the same medium and be erasable/reusable, rather than being an external scheduler table.
