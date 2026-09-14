# Experiment 051 — K6 distributed causality audit

## Question

K6 removes fixed endpoint roles, but is the subsequent execution still usually controlled by one local window, as in K1, or do multiple members of the selected ternary interaction become jointly necessary?

## Assay

Use the same eight deterministic dense backgrounds and equal-budget history pairs as Experiment 050.

For every directed donor->recipient case whose next eight-event traces differ:

1. take the donor's naturally selected first ternary event;
2. copy donor window contents at the three event positions into the recipient;
3. test every non-empty subset of the three donor windows;
4. record the smallest subset that exactly reproduces the donor's next eight-event trace.

## Result

Directed cases with different future traces: **410**.

The donor future trace can be reproduced using only the three local event windows in **48** cases:

- minimum 1 endpoint: **30**
- minimum 2 endpoints: **10**
- all 3 endpoints required: **8**
- no subset of the three is sufficient: **362**

Among locally reproducible cases, **18/48 = 37.5%** require more than one endpoint.

## Interpretation

K6 is less locally one-window-dominated than K1, but the global state still matters strongly: most donor trajectories cannot be recreated by copying the selected ternary event alone.

The multi-endpoint cases are consistent with distributed causal organization, but some joint necessity is expected because the physical interaction itself is ternary. The result is therefore a substrate diagnostic, not an emergence claim.

The more serious remaining weakness is Experiment 050's local triple locking: event 1 and event 2 usually reuse all three physical positions.