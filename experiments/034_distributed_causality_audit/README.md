# Experiment 034 — distributed causality audit

## Question

K1 supports recurrent, causally effective local execution contexts, but Experiment 033 found very little strict two-patch synergy.

Is the donor execution cascade nevertheless controlled by a distributed set of local regions, or does one region usually dominate?

## Setup

Use the same queue-free K1 substrate and equal-budget history family as Experiments 031–033.

For each eligible donor/recipient pair with different future execution traces, consider four non-overlapping radius-2 / 7-bit donor patches at positions:

`0, 8, 16, 24`

Enumerate every non-empty subset of those regions. For each subset, transplant the donor patches into the recipient and run the same 32-slot future event budget.

Record the smallest number of transplanted regions needed to exactly reproduce the donor execution trace.

## Result

- eligible donor/recipient trace differences: **1312**
- minimum one region: **1179**
- minimum two regions: **2**
- minimum three regions: **0**
- minimum four regions: **0**
- not reproduced even by all four candidate regions: **131**

Among the **1181** cases reproduced by this candidate region set, **99.83%** required only one region.

## Interpretation

This is strong evidence that the current K1 dynamics are predominantly **locally dominated**, not distributed in the sense sought here.

The result does not say that the global ring state is irrelevant. Rather, for the specific history-dependent execution differences studied here, a small local context near the interaction site is usually enough to transfer the entire future event cascade.

This explains why Experiment 033 found almost no strict compositional synergy: there is usually no need for multiple independent local contexts to jointly determine the execution outcome.

## Consequence for the substrate search

K1 has been useful:

- history changes which events are executable;
- this remains true with stateless scheduling;
- naturally generated local contexts are causal and reusable;
- those contexts can act as execution macros.

But K1 now shows a structural limitation:

> its history-dependent execution organization is usually compressible into a single small local region.

That is too close to a context-sensitive local automaton and too weak for the original goal of fluid, relational, distributed organization.

The next substrate should therefore change **interaction topology**, not add a reward, learner, SELF, or symbolic layer. The minimal next candidate should let executable relations themselves form and disappear, while keeping the underlying physical operations small and CPU-native.
