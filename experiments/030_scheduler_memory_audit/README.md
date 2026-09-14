# Experiment 030 — scheduler-memory audit

## Question

Could the K1 history effect from Experiments 028/029 be an artifact of hidden state in the event queue rather than the binary ring itself?

## Setup

The physical substrate remains a binary ring with a fixed ECA truth table. A site is enabled when its current bit differs from the local rule target.

Two equal-budget histories use the same five interventions and the same multiset of width-3 patterns, changing only order:

- `A,A,A,B,B`
- `B,B,A,A,A`

where `B` is the width-3 complement of `A`.

Two scheduler variants remove persistent queue state:

1. `ResetFIFO`: rebuild the FIFO from the current ring at every physical-work block. No queue survives between blocks.
2. `StatelessMin`: keep no queue at all. At every work slot, recompute the enabled sites directly from the current ring and execute the minimum-index enabled site.

The observer records the recurrent repertoire of local patches centered on enabled sites during a fixed post-history budget.

## Result

Across all `256 × 4 = 1024` equal-budget rule/pattern cases:

- `ResetFIFO`: enabled-context repertoire changed in **525/1024** cases.
- `StatelessMin`: enabled-context repertoire changed in **483/1024** cases.

Thus the execution-level history dependence survives even when scheduler memory is removed completely.

## Interpretation boundary

This does **not** imply agency, learning, or intelligent selection.

It establishes a narrower point: the binary ring state itself can carry enough history to alter which local interactions are currently executable under a stateless event-selection rule. The queue used in earlier K1 experiments is therefore not necessary to obtain the effect.

This motivates a causal test of whether a naturally generated local context can transfer a later event cascade when transplanted between histories.