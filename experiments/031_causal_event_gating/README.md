# Experiment 031 — causal transfer of event gating

## Question

Does a naturally generated local K1 context merely correlate with later execution, or can it causally transfer the future event cascade between equal-budget histories?

## Setup

Use the queue-free K1 substrate with a stateless event selector.

Two histories receive the same five width-3 interventions with the same multiset and physical work budget, changing only order:

- `A,A,A,B,B`
- `B,B,A,A,A`

where `B` is the width-3 complement of `A`.

For each rule, training position, and scheduler policy (`min` or `max` enabled index):

1. run both histories;
2. observe the next 32 event slots with no further intervention;
3. retain cases where the two future event traces differ;
4. copy only the donor history's 7-bit local patch (3-bit core plus radius-2 flanks) into the recipient history at the training location;
5. measure whether the recipient's future event trace moves toward the donor trace;
6. as a spatial control, copy the same-width donor patch at the antipodal location (`+32` cells) instead.

The event selector itself stores no history.

## Result

Across 8 training positions, two stateless scheduler orientations, all 256 ECA rules, and all four complement-pair representatives:

- eligible cases with different future traces: **1529**
- local patch transplant reduced donor/recipient trace distance: **1023/1529 = 66.91%**
- local patch transplant produced an exact 32-slot donor trace: **998/1529 = 65.27%**
- antipodal same-width control improved the trace: **59/1529 = 3.86%**

The effect is therefore strongly localized to the history-generated context near the interaction site rather than being reproduced by an arbitrary same-size transplant elsewhere on the ring.

## Interpretation boundary

This is not evidence of intelligent choice or a learned symbolic representation.

It is a narrower causal statement:

> equal-budget history can be condensed into a small naturally generated local context that determines which later physical events receive execution, and transplanting that context often transfers the resulting event cascade.

This is stronger than the observer-only quotient effects in K0 because the transferred object changes the actual execution trace of K1.

## Next question

Does the same local context act as a reusable execution macro when it reappears naturally in a different history, or is its causal effect specific to the state from which it was transplanted?