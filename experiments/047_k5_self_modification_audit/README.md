# Experiment 047 — K5 self-modification audit

## Question

K5 lets M condition the A/B rewrite, but does the rewrite of M itself actually contribute to later transformation-grammar change?

The K5 equation is:

- `A' = A XOR M`
- `B' = B XOR rotl(M,1)`
- `M' = M XOR (A AND B)`

If selected events rarely have overlapping 1-bits in A and B, the nominal M rewrite may be physically inert.

## Assay

Reuse all 320 equal-budget histories from Experiment 046.

For the first naturally selected event in each history:

1. record whether `A AND B` is nonzero;
2. execute the normal K5 event and measure the new transformation grammar;
3. execute a counterfactual event with identical A/B rewrites but leave M unchanged;
4. compare both the post-event transformation grammar and the remaining future event trace.

## Result

Across all **320** histories:

- selected events with `A AND B != 0`: **0/320**
- therefore the nominal M update is `M' = M` in **320/320** first events
- transformation grammar changes after the first event in **45/320** histories
  - same: **275**
  - strict expansion: **38**
  - incomparable reorganization: **7**
- normal K5 versus frozen-M counterfactual grammar differs: **0/320**
- normal K5 versus frozen-M future trace differs: **0/320**

## Interpretation

This is a negative result and tightens the K5 claim.

Experiment 045/046 supports:

> current M content can condition which A/B transformation occurs and can form a recurrent transformation context.

It does **not** support:

> transformation contexts rewrite themselves and thereby modify the future transformation grammar.

Under the tested scheduler and histories, the M-update branch is completely inactive.

## Consequence

Do not patch this by adding an ad-hoc list of mediator-update cases. The cleaner next substrate should remove the privileged mediator role and use a role-symmetric ternary algebra in which all three ordinary windows necessarily participate in rewriting one another.