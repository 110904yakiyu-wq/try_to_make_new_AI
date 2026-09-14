# Experiment 035 — dynamic rendezvous K2

## Question

K1 allowed history-dependent event gating, but its execution differences were usually controlled by one small local patch.

Can a substrate with **content-dependent temporary nonlocal relations** produce genuinely joint causal control without adding nodes, persistent edges, reward, memory, or a learner?

## K2 physical rule

The medium is still one circular bit ring.

Every position exposes a fixed-width physical key window. Two non-overlapping locations are temporarily eligible to interact when their current key windows are identical.

No edge is stored.

For an eligible pair with key `x`:

- the first window is rewritten as `rotl(x, 1)`;
- the second window is rewritten as `rotr(x, 1)`.

After every event, all currently eligible rendezvous relations are recomputed from the ring. A stateless `min` or `max` ordering chooses one current pair.

The rule is deliberately arbitrary and minimal. It is not a cognitive model. It only adds one capability missing from K1: current content determines temporary interaction topology.

## Equal-budget order result

Histories receive the same five width-3 interventions and the same physical event budget. Only order differs:

- `A,A,A,B,B`
- `B,B,A,A,A`

with `B` the bitwise complement of `A`.

Across both stateless scheduler orientations, eight intervention positions, and four complement-pair representatives:

- equal-budget history cases: **64**
- final rendezvous relation repertoire differed: **52/64**
- next 32-event execution trace differed: **46/64**

Thus order alone can change both temporary nonlocal relation topology and later execution.

## Causal endpoint test

For each donor/recipient history pair whose future traces differ, take the donor's first enabled rendezvous relation `(i,j)`.

Transplant into the recipient:

1. only the donor key window at endpoint `i`;
2. only endpoint `j`;
3. both endpoints.

Then run the same future event budget.

With raw 4-bit endpoint windows (`radius=0`):

- eligible donor/recipient cases: **83**
- first endpoint alone exactly reproduced donor trace: **4/83**
- second endpoint alone: **5/83**
- both endpoints: **26/83**
- both endpoints succeeded while neither single endpoint did: **17/83**
- joint transplant was closer to donor than both singles: **47/83**

Using radius-2 neighborhoods makes the absolute transfer rate larger, but the same qualitative result remains: **25/83** cases require the joint endpoint transplant for exact donor-trace recovery.

## Interpretation boundary

This is not emergent symbolic composition and not evidence of intelligence.

The narrow result is stronger and more physical:

> when an executable relation itself is defined by two separated pieces of current medium, the two endpoints can become jointly causally necessary for the future execution cascade.

This behavior was almost absent in K1, where one local region usually dominated.

K2 therefore passes the first reason for introducing dynamic interaction topology.

## Next audits

Before treating this as progress, test whether the result survives:

- separation-distance changes;
- alternative stateless pair schedulers;
- different key widths;
- different minimal rewrite rules;
- controls that preserve local endpoint contents but break endpoint matching.

The central question is whether **relational causality**, rather than this particular rotate-and-match toy rule, is what creates the joint effect.
