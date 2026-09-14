# Experiment 042 — mediator-only transfer limit

## Question

Experiment 041 showed that equal-budget history changes the observer-side effective pair grammar because different mediator-width patterns exist in the medium.

Can transplanting one history-exclusive mediator pattern by itself transfer the donor's effective grammar and future execution?

## Method

For each donor/recipient equal-budget pair:

1. find a mediator-width value present in the donor but absent in the recipient;
2. choose the first such value deterministically;
3. transplant one donor window carrying that value into the recipient;
4. compare grammar distance to the donor;
5. compare the next 8-event trace distance to the donor.

A shared mediator-value transplant is used as a weak control for generic local rewriting.

## Result

Eligible donor/recipient cases with at least one history-exclusive mediator value: **49**.

- mediator-only transplant reduced abstract grammar distance to donor: **34/49**
- mediator-only transplant reduced future execution-trace distance: **1/49**
- mediator-only transplant exactly reproduced donor trace: **0/49**
- shared-value control improved donor trace distance: **0/49**

## Interpretation

A single mediator pattern can readily alter the observer-side effective pair grammar, but that does **not** normally transfer the global future execution trajectory.

This is an important boundary.

The medium does not behave as if one mediator window were a portable global meta-rule. Global execution still depends on the surrounding physical organization.

Therefore K3 should not identify:

`mediator pattern == rule object`

The next test isolates mediator causality more carefully: retain donor and recipient cases in which the candidate A/B endpoint contents are already identical, while only the mediator needed for the donor's first relation differs. Then transplant only that mediator and ask whether the same A/B relation becomes executable.
