# Experiment 041 — mediated relation grammar K3

## Question

K2 made interaction topology transient, but the criterion for relation was still fixed equality matching.

Can a fixed physical kernel support a **history-dependent effective relation grammar** by requiring a third current structure to mediate whether two other structures may interact?

## K3 physical rule

The medium remains one circular bit ring.

For three non-overlapping key windows `A`, `B`, and `M`, an event is physically eligible when:

`M = A XOR B`

No window is permanently typed as a rule, mediator, program, or data object. The roles exist only for the current event.

When a triple fires:

- `A` is rotated left;
- `B` is rotated right;
- `M` is complemented.

All eligible triples are recomputed from current ring content after every event. A stateless `min` or `max` tuple ordering selects one event.

This is still an arbitrary toy physical law. Its purpose is only to make the **effective A/B relation criterion depend on which M values currently exist in the medium**.

## Equal-budget history test

Use the same five interventions with identical multiset and event budget, changing only order:

- `A,A,A,B,B`
- `B,B,A,A,A`

where `B` is the width-3 complement of `A`.

Default substrate:

- ring size: 32
- key width: 4
- event budget after each intervention: 8
- future trace budget: 8

Define the observer-side effective pair grammar as all abstract key pairs `(x,y)` for which `x XOR y` is currently present somewhere as a mediator-width window.

## Result

Across 32 equal-budget conditions:

- same effective grammar: **1**
- sequence 1 grammar strict superset: **7**
- sequence 2 grammar strict superset: **9**
- incomparable grammar reorganization: **15**
- future event trace differs: **32/32**

So **31/32** equal-budget history pairs produce a different effective pair-relation grammar.

The result is not only monotone growth. Nearly half of the cases are incomparable reorganizations: each history permits abstract pair relations that the other does not.

## Interpretation boundary

The XOR mediation rule is still hard-coded physics. K3 therefore does not "invent relation logic" from nothing.

What changed from K2 is narrower but important:

> the fixed kernel no longer directly determines one pairwise relation predicate. Instead, current third-party medium content determines which pairwise dependencies are physically realizable.

Under equal physical budget, history changes that mediator content and therefore changes the effective relation grammar.

This is close to the project's earlier target:

`history changes what kinds of dependencies can exist`

but only at the level of a toy substrate.

## Next falsification

The next step must be causal, not descriptive.

Identify a mediator value present in one history but absent in the other. Transplant only that mediator-bearing physical window into the recipient while leaving candidate A/B structures untouched. Test whether this changes the recipient's executable relation repertoire and later event cascade in the predicted direction.

If mediator-only transfer fails, the grammar interpretation is merely an observer description of global state rather than a causal mechanism.
