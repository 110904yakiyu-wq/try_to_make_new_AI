# Experiment 045 — mediator-conditioned rewrite K5

## Question

Can an ordinary third current structure change not only whether A/B may interact, but also the transformation that follows, without decoding that structure as an opcode or rule identifier?

## K5 substrate

The medium is still one circular bit ring. Every candidate event uses three non-overlapping width-4 windows `(A,B,M)`.

A triple is enabled when the parity of `A XOR B XOR M` is even. This deliberately leaves multiple possible mediator values for the same A/B pair.

The fixed rewrite is one algebraic equation family:

- `A' = A XOR M`
- `B' = B XOR rotl(M,1)`
- `M' = M XOR (A AND B)`

No M value is decoded as an instruction number. M is ordinary rewritable medium content.

A stateless scheduler chooses the lexicographically minimum or maximum enabled triple.

## Equal-budget history assay

As before, compare two histories that receive the same five width-3 interventions with the same multiset, differing only in order:

- `A,A,A,B,B`
- `B,B,A,A,A`

where B is the 3-bit complement of A.

Defaults: ring size 32, key width 4, eight event slots after each intervention, eight future event slots.

The observer-side transformation grammar is the set of `(A,B,A',B')` transformations currently realizable using mediator values present in the ring.

## Result

Across 32 equal-budget conditions:

- same transformation grammar: **6**
- seq1 strict superset: **17**
- seq2 strict superset: **4**
- incomparable reorganization: **5**
- future event traces differ: **16/32**

The important causal subset holds endpoint position and endpoint contents fixed while the selected mediator value differs.

There are three such history pairs, or six directed donor->recipient transfers.

After transplanting only the donor mediator window:

- the same A/B endpoint pair with the donor M becomes selected in **6/6** directed cases;
- the exact first donor event is reproduced in **4/6**;
- the full next eight-event donor trace is reproduced in **4/6**.

## Interpretation boundary

This does **not** show that a transformation language has emerged from nothing. The parity compatibility predicate and bitwise rewrite algebra remain fixed physical law.

The narrower result is stronger than K3:

> while A/B are held fixed, ordinary third-medium content can causally select a different physical transformation and, in some cases, transfer the complete subsequent execution trajectory.

So the current medium can carry transformation context without an explicit rule object, opcode table, learner, reward, SELF, or persistent graph.

## Next question

Is the M-conditioned transformation reusable across unrelated histories, or is it only a local causal transplant effect? The next assay should test natural recurrence of the same `(A,B,M)` transformation context and whether it predicts the same post-event transformation class across histories.