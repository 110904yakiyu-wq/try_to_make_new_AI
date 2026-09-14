# Experiment 043 — isolated mediator causality

## Question

Does mediator content causally control an A/B relation when the A/B endpoint contents themselves are held fixed?

## Isolation criterion

Start from the K3 equal-budget donor/recipient history pairs.

Keep only cases where the donor's first selected event has endpoints `(A,B,M)` such that:

- recipient endpoint A has the same key as donor A;
- recipient endpoint B has the same key as donor B;
- recipient mediator window at donor M does **not** have the donor mediator key.

Then transplant only the donor mediator key into the recipient. A and B are left untouched.

## Result

Only **7** cases satisfy the strict isolation criterion under the default small K3 setup.

After mediator-only transplant:

- the same donor A/B endpoint pair becomes the selected relation: **7/7**
- the selected relation has the same A key, B key, and mediator value as donor: **7/7**
- the exact donor triple including mediator position is recovered: **4/7**
- future 8-event trace moves closer to donor: **4/7**
- future 8-event trace exactly matches donor: **2/7**

## Interpretation

This is a much cleaner causal statement than Experiment 042.

When the A/B candidate structures are already physically identical across histories, changing only the third mediator structure can switch which A/B relation is executable.

So under this K3 kernel:

> current third-party medium content can causally determine the effective pairwise relation between otherwise unchanged endpoint structures.

At the same time, mediator transfer is not sufficient to reconstruct the whole future trajectory in most cases. The effective relation grammar is locally mediated, but global execution remains distributed over the rest of the medium.

## Claim boundary

The XOR compatibility law is still fixed by the designer. This is not spontaneous invention of relation semantics.

The useful result is narrower:

- K2: current content changed which fixed relation instances existed;
- K3: current content can change **which relation criterion applies to a fixed endpoint pair**, via a third structure.

That is closer to a soft effective relation grammar, but the physical compatibility language itself remains hard-coded.

## Next question

Can the compatibility operation itself become soft without embedding a general interpreter or explicit rule object?

A candidate next step is to let the mediator determine **which bitwise comparison is physically applied** (for example by supplying a mask), while keeping that mask as ordinary rewritable medium rather than typed metadata. The audit must distinguish genuine history-dependent grammar from merely adding more designer-specified relation options.
