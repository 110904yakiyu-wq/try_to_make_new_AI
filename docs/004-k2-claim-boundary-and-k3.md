# K2 claim boundary and K3 target

Date: 2026-09-14

## What K2 actually established

K2 replaced K1's fixed nearest-neighbor interaction topology with temporary content-defined nonlocal rendezvous.

This produced:

- equal-budget history-dependent relation repertoires;
- history-dependent execution traces;
- causal dependence on two separated rendezvous endpoints;
- robustness across several key widths;
- survival under more than one rewrite law.

Those are valid substrate observations.

## What K2 did **not** establish

The relation grammar was fixed by the designer:

> two separated windows may interact when their keys are equal.

Because the physical law explicitly requires a joint condition on two endpoints, observing joint endpoint causality is partly expected by construction.

Therefore K2 is not evidence that a substrate spontaneously invented relational organization.

It only shows that removing persistent edges while retaining a fixed relation predicate is computationally workable.

## The next hidden hard assumption

K0 hard-coded spatial adjacency.

K1 hard-coded spatial adjacency but made execution event-driven.

K2 made topology transient, but still hard-coded **what relation means**.

The next target is therefore:

`fixed physical interaction law`

while allowing

`effective relation grammar`

to become history-dependent.

## K3 candidate: mediated relation grammar

Do not make the kernel rewrite its own interpreter yet.

Instead use one minimal fixed physical primitive in which a third local structure acts as a transient mediator for whether two other structures interact.

Conceptually:

- `A` and `B` are two current physical windows;
- `M` is another current window;
- the fixed kernel computes a minimal compatibility relation from the raw bits of `(A, B, M)`;
- changing `M` changes which pairs `(A,B)` are executable;
- `M` itself is rewritten by interactions and is not typed as a rule, controller, or metadata object.

Thus the physical law remains fixed, but the effective pairwise relation induced by the current medium can vary with history.

A simple first implementation may interpret `M` as a bit mask only at the **physical** level, for example allowing interaction when selected bits of `A` and `B` agree. The project must not promote the mask to a cognitive rule object.

## Required falsification

K3 is only interesting if:

1. equal-budget histories produce different effective relation partitions over the same candidate `A/B` windows;
2. transplanting only the mediator region can transfer that effective relation partition;
3. the same mediator pattern recurrently induces similar relation behavior in different histories;
4. different mediator histories can cause refine, coarsen, or incomparable reorganization of which `A/B` pairs may interact;
5. no dedicated learner, reward, SELF, relation table, or explicit meta-layer is introduced.

If these fail, the mediated grammar is another decorative encoding and should be discarded.

## Current conceptual progression

`K0: fixed local topology`

`K1: history-dependent local event gating`

`K2: history-dependent transient topology under fixed relation grammar`

`K3 target: history-dependent effective relation grammar under fixed physics`

This is closer to the original meta objective: not merely changing state or topology, but changing **which dependencies can exist**.
