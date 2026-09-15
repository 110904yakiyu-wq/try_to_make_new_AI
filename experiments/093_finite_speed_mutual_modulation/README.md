# Experiment 093 — finite-speed mutual modulation

## Motivation

Experiments 090–092 identified a structural problem in K8: one atomic event can make its execution depend on a context spanning a large fraction of the ring. Localizing only the write does not fix the churn because the read itself is still effectively nonlocal.

The next substrate should therefore satisfy a stricter physical condition:

> long-range dependence must be constructed by repeated local interactions over time.

This experiment is a null for that condition. It does not test learning yet.

## Physical rule

The medium is a circular sequence of ordinary fixed-width raw windows.

Only three adjacent windows interact at once. A three-phase Margolus-like partition shifts the local triple grouping by one window each tick, so causal influence can move only through neighboring interactions.

For a local triple `(X,Y,Z)`, apply one permutation-symmetric nonlinear law:

```text
X' = X XOR rot(Y AND Z)
Y' = Y XOR rot(Z AND X)
Z' = Z XOR rot(X AND Y)
```

Every endpoint obeys the same equation. There is no mediator window, source/target role, reward, learner, SELF, persistent edge, global scan, or external relation table.

`rot` is a one-bit circular rotation within the physical window. Both left and right rotation are audited. The no-rotation variant is also tested as a control.

## Finite-speed causal cone

For width 4 and left rotation, flipping one raw bit before execution gives the following mean perturbation spread across 64 seeds:

- after 1 tick: 2.13 windows differ, maximum distance 1.22;
- after 2 ticks: 3.56 windows differ, maximum distance 2.23;
- after 3 ticks: 4.81 windows differ, maximum distance 3.14;
- after 6 ticks: 8.61 windows differ, maximum distance 5.05;
- after 12 ticks: 10.91 / 12 windows differ, maximum distance 5.84.

Unlike K8, a one-bit perturbation cannot influence the opposite side of the ring in one kernel step.

## Autonomous activity

Using 12 windows, 64 dense random initial states, and 2000 ticks:

### width 4, left rotation

- mean active triples/tick: **3.04 / 4**;
- mean changed windows/tick: **5.17 / 12**;
- 63/64 seeds remain active in the final 100 ticks;
- an exact state+phase cycle is detected in 52/64 seeds;
- detected cycle median: **48** ticks;
- detected maximum: **876** ticks;
- 12/64 seeds do not repeat within 2000 ticks.

### width 4, right rotation

- mean active triples/tick: **2.85 / 4**;
- mean changed windows/tick: **5.03 / 12**;
- 64/64 remain active;
- 51/64 cycles detected;
- detected cycle median: **36**;
- maximum: **1284**.

### no rotation control

The same endpoint-symmetric AND coupling without rotation collapses:

- active triples/tick: **0.016**;
- 0/64 remain active;
- all 64 settle to content-fixed states (state+phase period 3).

Thus sustained dynamics depends on a physical mixing operation, but not on the handedness of that operation.

## Coarse support persistence

Exact raw operational roles still change quickly. For width 4 / left rotation their adjacent-tick role-set Jaccard is only about **0.043**.

However, the spatial set of windows participating in active triples is much more persistent.

With 128 seeds and 1000 ticks:

- observed adjacent-tick support Jaccard: **0.762**;
- count- and phase-matched random-activity null: **0.716**;
- observed same-phase (lag 3) Jaccard: **0.821**;
- matched null: **0.722**.

Observed lag-3 persistence exceeds the matched null in **127/128** seeds.

Right rotation gives the same qualitative result.

## Perturbation audit

After 100 warmup ticks, flip one raw bit and compare the perturbed trajectory with the unperturbed control.

The raw states rapidly diverge: during ticks 25–48 after perturbation the mean raw Hamming distance is **22.40 / 48 bits**.

Yet over the same window:

- control-vs-perturbed activity-support Jaccard: **0.805**;
- control-vs-independent-trajectory null: **0.754**.

The per-seed paired difference is positive in 88 seeds and negative in 38 (2 ties), two-sided sign-test p about `9.8e-6`.

So the microstate is already substantially different while the coarse spatial organization of execution remains more similar than expected from independent trajectories.

## Interpretation boundary

This is the first post-K8 substrate in this line that simultaneously has:

1. finite-speed causal propagation;
2. no fixed semantic endpoint roles;
3. persistent autonomous activity for most random starts;
4. rapidly changing exact micro-roles;
5. statistically detectable persistence of a coarser execution-support organization under perturbation.

The conservative phrase is **metastable activity support**.

It is not learning, memory in the strong sense, selfhood, or evidence of intelligence.

The hard rotation/mixing law is also doing essential work and must remain explicit as a substrate assumption.

## Next question

Can history change the metastable support organization in a way that changes future finite-budget computation, while the raw microstate is controlled for as much as possible?

That is the appropriate place to reintroduce the operational-cost question from K8, now without atomic nonlocal scanning.
