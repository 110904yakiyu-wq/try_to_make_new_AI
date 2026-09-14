# K3/K4 lessons and next substrate target

Date: 2026-09-14

## K3 lesson

K3 replaced K2's fixed pairwise equality predicate with a mediated ternary compatibility:

`M = A XOR B`

The physical rule stayed fixed, while the currently available mediator values changed which abstract A/B relations were executable.

Equal-budget histories produced:

- strict grammar supersets in either direction;
- many incomparable grammar reorganizations;
- isolated cases where changing only M, while holding A and B fixed, changed which A/B relation was selected.

This is the strongest toy result so far for the statement:

> history can change which dependencies are executable without changing the physical kernel.

But the XOR compatibility language is still designer-fixed.

## K4 lesson

K4 let M behave like an endogenous comparison mask:

`(A XOR B) AND M == 0`

This made permissiveness history-dependent but mostly produced broader/narrower versions of one common relation family.

It did not produce the same quality of incomparable grammar reorganization as K3 under the first small test.

So merely endogenizing parameters of a fixed relation predicate is not enough.

## Next hidden assumption

So far the mediator changes **whether** an interaction can occur.

The transformation performed after an interaction is still selected entirely by the fixed kernel.

That leaves another hard layer:

`relation established -> one designer-fixed rewrite`

If the project is serious about soft dependency grammar, history should eventually influence not only which regions interact, but what kinds of future dependencies that interaction creates.

## Next candidate

Keep one fixed physical equation rather than an opcode table.

Use an untyped third window M directly inside the rewrite algebra, for example a family conceptually like:

- compatibility depends jointly on A, B, and M;
- `A'` is a simple bitwise function of A and M;
- `B'` is a different simple bitwise function of B and M;
- M is itself rewritten;
- no bit pattern is decoded as an instruction number or semantic rule identifier.

The important criterion is not the exact formula. It is whether **the same endpoint pair can enter different subsequent operational relation structures because a different current third structure participated**.

## Required falsification

A useful next substrate must show all of the following under fixed finite budget:

1. hold A/B endpoint contents fixed;
2. vary only an ordinary third current structure M;
3. observe different future operational relation repertoires or event-cascade classes;
4. causally transplant M and transfer that future class;
5. show recurrence of the same M-conditioned transformation across different histories;
6. avoid an explicit opcode decoder, rule table, reward, learner, SELF, or persistent graph.

If this requires a large catalogue of hand-designed bitwise operations, stop. That would only move the architecture into the substrate.
