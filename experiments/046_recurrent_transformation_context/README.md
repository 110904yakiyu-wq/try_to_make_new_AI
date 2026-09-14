# Experiment 046 — recurrent transformation context

## Question

Experiment 045 showed that transplanting M can causally transfer a mediator-conditioned transformation when A/B are held fixed.

Does the same `(A,B,M)` context also behave reproducibly when it arises **naturally from different histories**?

The immediate rewrite is not used as the target because it is fixed by the K5 equation and would be tautological. Instead, the target is the next eight **content-level event signatures**, ignoring physical positions.

## History family

For each of four 3-bit complement pairs, each training position, and both stateless scheduler orientations, enumerate all ten distinct orderings of the same multiset:

`{A,A,A,B,B}`

This gives 320 equal-budget trained states.

For each state:

1. record the naturally selected first event's `(A,B,M)` contents;
2. run eight autonomous events;
3. record each event only by its before/after window contents, not its positions;
4. predict the complete eight-event trajectory from *other histories* with the same `(scheduler,A,B,M)` context.

Controls:

- use `(scheduler,A,B)` only;
- shuffle M labels within each fixed `(scheduler,A,B)` group for 200 trials.

## Result

Total histories: **320**.

Every history has at least one different-history peer with the same `(scheduler,A,B,M)` context:

- coverage: **320/320 = 100%**
- exact eight-event trajectory accuracy from `(A,B,M)`: **320/320 = 100%**
- pair-only `(A,B)` accuracy on the same histories: **93.125%**
- within-pair M-shuffle null mean: **~94.20%**
- maximum over 200 M-shuffle trials: **96.25%**

By scheduler:

- `min`: `(A,B,M)` accuracy **100%**, pair-only **88.75%**
- `max`: `(A,B,M)` accuracy **100%**, pair-only **97.50%**

The recurrence groups are not all trivial pairs: some `(A,B,M)` contexts recur in well over one hundred distinct histories.

## Interpretation boundary

K5 still has a designer-fixed compatibility predicate and designer-fixed bitwise rewrite equation. This is not an emergent instruction language.

The narrower observation is:

> an ordinary third window, used without opcode decoding, forms a reusable transformation context: when the same `(A,B,M)` content relation reappears naturally across different histories, it fixes not only the immediate rewrite but the subsequent content-level execution trajectory under this toy substrate.

This is stronger than a one-off transplant effect, but it is still compatible with a small deterministic dynamical macro.

## Next question

Can the same M participate in *different* A/B contexts and transfer a common transformation relation across them, or is every useful context really the full triple `(A,B,M)`? That distinguishes a reusable mediator role from mere whole-event state recurrence.