# Fixed-kernel boundary: history cannot bypass complete current state

Date: 2026-09-14

## Why this note exists

Experiments 053 and 056 tried increasingly strict versions of a second-order question:

> if two histories currently have the same operational grammar and receive the same next interaction, can their grammar-update law still differ because of history?

Weak coarse-grained assays sometimes say yes. Stronger descriptions progressively remove the signal.

This exposes a basic boundary that should be kept explicit from now on.

## Deterministic fixed-kernel statement

Let the physical substrate have a fixed deterministic transition kernel

`K : S -> S`

or, with an externally supplied intervention/event `u`,

`K : (S, u) -> S'`.

If two histories `h1` and `h2` arrive at exactly the same complete physical state `S`, and the same next physical intervention `u` is applied, then

`K(S, u)`

is identical for both histories.

Earlier history has no additional causal channel once its effects have been fully absorbed into the current state.

Therefore a claim of the form

> identical complete current state + identical physical event + different next physical law because of history

is impossible under a fixed deterministic kernel.

This is not an empirical finding about one CA-like toy. It follows from the modeling assumption itself.

## What can still change

The useful object is an **effective law** defined relative to a limited operational description.

Let

`phi_B : S -> G_B`

map physical state to a resource-bounded effective grammar `G_B`, where `B` limits accessible tests, context construction, depth, storage, or compute.

Then two different physical states may satisfy

`phi_B(S1) = phi_B(S2)`

while the same next event produces

`phi_B(K(S1,u)) != phi_B(K(S2,u))`.

This is not microphysical law mutation. It means the coarse operational state `G_B` is not Markov-complete at budget `B`.

That incompleteness is potentially useful rather than embarrassing: development can change which coarse variables make future dependence cheap enough to expose under a fixed budget.

## Revised target

Do not pursue literal changing physical laws unless the law representation itself is intentionally made mutable state.

For the current project, prefer the weaker and cleaner target:

> history changes the resource-bounded effective transformation grammar: what dependency types are executable, distinguishable, reusable, or cheaply constructible under the same finite physical budget.

This preserves the original goal of avoiding fixed cognitive ontology without pretending that deterministic physics forgot its own Markov state.

## Consequence for substrate design

A substrate should therefore be judged by whether it can support:

1. multiple effective dependency organizations under one fixed microphysics;
2. history-dependent movement between those organizations;
3. endogenous construction/reuse of contexts that make some dependencies cheaper or newly executable;
4. no privileged SELF, reward, learner, symbolic rule table, or fixed cognitive layer hierarchy.

## Immediate engineering audit

K7 still violates the spirit of this target in another way: each event is selected by globally enumerating all non-overlapping subsets up to the configured maximum arity.

That search acts like an omniscient content-matching oracle and scales combinatorially.

The next kernel should retain variable interaction span without requiring global subset enumeration. A promising null is a **self-delimiting sequential interaction**: start from a physical location, extend through neighboring non-overlapping windows, and let current content determine the first closure point. Arity then becomes a consequence of the medium encountered during a bounded scan rather than a separately enumerated hyperedge catalogue.
