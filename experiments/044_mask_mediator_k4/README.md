# Experiment 044 — masked-mediator K4

## Question

Can the mediator soften not only which relation instances exist, but which bits of two endpoints are physically compared?

## Candidate physical law

Use three non-overlapping current windows `A`, `B`, and `M`.

`M` is an ordinary rewritable physical window. A triple is eligible when:

`M != 0` and `(A XOR B) AND M == 0`

Thus `M` selects which bit positions of A/B must agree. No persistent rule object or relation table is stored.

The event rewrite is kept simple:

- rotate A left;
- rotate B right;
- complement M.

## Small equal-budget test

Default small setup:

- ring size: 24
- key width: 4
- 4 events after each intervention
- same five-intervention multiset, changing only order
- stateless min/max triple schedulers

Observer-side effective pair grammar contains `(a,b)` when at least one currently present nonzero mask `m` satisfies `(a XOR b) AND m == 0`.

## Result

Across 24 equal-budget conditions:

- same grammar: **12**
- sequence 1 strict superset: **6**
- sequence 2 strict superset: **6**
- incomparable grammar reorganization: **0**
- future 6-event trace differs: **16/24**

## Interpretation

The mask mediator does make relation permissiveness history-dependent, but this first implementation is weaker than K3 for the project's purpose.

The effective grammar behaves mostly like a union of currently available masks: histories tend to make the relation set broader or narrower rather than reorganizing it in qualitatively incomparable ways.

This is not the desired notion of a soft ontology. It looks too much like a designer-provided menu of comparison dimensions.

Therefore do **not** promote this K4 candidate.

## Lesson

Making a parameter of a fixed relation predicate endogenous is not automatically the same as making the effective relation grammar genuinely plastic.

K3's mediator-value construction, despite being simpler, produced more genuine refine/coarsen/incomparable changes because mediator values selected distinct XOR relation classes rather than only relaxing a common masked-equality predicate.

The next step should not add more mask parameters. It should ask whether a mediator can change the **transformation applied after relation formation**, so that the same endpoint pair can enter different future dependency structures depending on a third current structure.
