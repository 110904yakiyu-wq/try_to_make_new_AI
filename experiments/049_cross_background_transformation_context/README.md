# Experiment 049 — cross-background transformation context

## Question

Experiment 046 found perfect recurrence of `(A,B,M)` transformation contexts under the original single-bit background.

Does that recurrence survive when the same context is required to generalize across **different initial media**?

## Assay

Reuse the ten deterministic backgrounds from Experiment 048 and the full ten-order equal-budget history family.

For every valid trained state:

- record the naturally selected first `(A,B,M)` content triple;
- record the next eight content-level event signatures;
- predict the trajectory using only peers with the same `(scheduler,A,B,M)` but from a **different initial background**.

Controls:

- `(scheduler,A,B)` only;
- shuffle M labels within each fixed `(scheduler,A,B)` group.

## Result

Total valid histories: **3199**.

For the strict cross-background prediction subset:

- covered histories: **1648**
- `(A,B,M)` exact eight-event trajectory accuracy: **96.4806%**
- pair-only `(A,B)` accuracy on the same covered histories: **80.9466%**

Across 100 within-pair M-shuffle trials:

- null mean accuracy: **~64.25%**
- null maximum accuracy: **~68.68%**

For reference, when same-background peers are also allowed:

- covered histories: **3080**
- `(A,B,M)` accuracy: **97.8247%**
- pair-only accuracy: **83.2143%**

## Interpretation

The perfect 100% recurrence in Experiment 046 was partly a special property of the original background, but the effect remains strong after forcing generalization across different initial media.

Thus M is not merely identifying one whole-state attractor reached from the single-bit initialization. The same local `(A,B,M)` content relation carries substantial information about the future transformation trajectory across substantially different global states.

## Boundary

This is still a deterministic physical macro under a fixed K5 algebra. It does not establish an emergent rule language.

The next hidden assumption is now clearer: K5 gives M a permanently privileged mediator role. A cleaner substrate should remove fixed A/B/M semantic roles and let all interacting regions participate under the same physical law.