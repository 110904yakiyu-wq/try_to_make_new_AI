# Experiment 055 — K7 arity causal support audit

## Question

Experiment 054 showed that equal-budget history can change which interaction arities are currently executable under one arity-generic content relation.

Does a selected k-way event actually require its k distributed members to reproduce the donor's near-future execution, or is the apparent higher arity mostly redundant?

## Assay

Use K7 with:

- ring size 20
- key width 5
- permitted search arities 2..4
- equal-budget `A,A,A,B,B` vs `B,B,A,A,A` histories
- eight backgrounds
- both stateless scheduler orientations
- two future events as the causal target

For every directed donor->recipient history pair with different future traces:

1. select the donor's next enabled event;
2. exhaustively transplant proper subsets of that event's member windows into the recipient;
3. find the minimum number of donor members needed for the recipient's two-event trace to equal the donor trace exactly.

`minimum=0` in the output means that even transplanting all members of the selected event is insufficient.

## Result

Directed history cases with different future traces: **508**.

Forty donor states have no enabled event under the current finite search, leaving **468 selected-event cases**.

### donor arity 2

- cases: 300
- selected event insufficient: 238
- one endpoint sufficient: 7
- **both endpoints required: 55**

Among locally reproducible pair events, 55/62 = **88.7%** require the full pair.

### donor arity 3

- cases: 159
- selected event insufficient: 150
- one/two members sufficient: 0
- **all three required: 9/9 locally reproducible cases**

### donor arity 4

- cases: 9
- two members sufficient: 1
- three members sufficient: 1
- **all four required: 7**

Thus, when a higher-order selected event is locally sufficient to transfer the near-future execution class, the complete current event support is usually necessary.

## Interpretation boundary

This is deliberately not called emergent compositionality or emergent hypergraph structure.

The kernel already defines an enabled event as a finite set of windows satisfying one joint XOR relation. Therefore some dependence on all members is structurally expected.

The useful result is narrower:

> allowing variable arity did not immediately collapse back to effectively pairwise causal support; genuinely full-support triple and four-way cases survive the transplant audit.

## Next audit

The next step must avoid the tautology "a k-way event depends on k members because the event was defined over k members".

A stronger test is to hold the same observable current event repertoire fixed and ask whether history changes **which arity becomes selected after the same next perturbation**, or whether all apparent arity plasticity is already completely encoded in the current detailed medium state.
