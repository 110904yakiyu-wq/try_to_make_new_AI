# Experiment 036 — relation-break control

## Question

Experiment 035 found cases where both endpoints of a temporary rendezvous relation had to be transplanted together to recover the donor execution cascade.

Was that effect caused by the relation itself, or merely by copying two local pieces of donor state?

## Control

Take the cases where a raw 4-bit joint endpoint transplant exactly reproduces the donor trace.

Immediately after the successful joint transplant, flip only one bit in the second endpoint key. This leaves almost all copied local state unchanged but destroys equality between the two rendezvous keys.

Then run the same future event budget.

## Result

- eligible donor/recipient differences: **83**
- successful joint endpoint transplants: **26**
- relation-broken controls that still reproduced donor trace: **0/26**
- relation-broken controls identical to the successful joint trace: **0/26**

## Interpretation

The joint transfer effect depends on the two separated regions continuing to satisfy the rendezvous relation.

This is stronger than saying that two donor patches jointly contain useful information.

Within this toy physical law:

> a nonlocally defined relation can itself be causally necessary for which future execution cascade occurs.

This does not imply representation, symbols, goals, or intelligence. It is a substrate-level result about relational causality.

## Next audit

The current matching and rotate rewrite are deliberately arbitrary. The next step is robustness:

- vary key width;
- vary scheduler orientation;
- vary endpoint separation;
- replace the rotate rewrite with other equally minimal rewrites.

If joint causal dependence disappears under small changes to these physical choices, K2 is only a toy-rule artifact rather than a useful substrate family.
