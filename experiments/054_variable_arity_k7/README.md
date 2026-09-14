# Experiment 054 — variable-arity K7

## Question

K6b fixed interaction arity at three windows. Can one fixed content relation support pair, triple, and higher-order interactions without selecting an arity in the kernel, and can equal-budget history change which arities are currently executable?

## K7 rule

Use one circular bit medium and one relation over any non-overlapping finite window set `S`:

`XOR(values in S) == 0`

The experiment only searches arities 2 through 4 as a finite observer/compute budget. There is no separate pair rule, triple rule, or four-way rule.

For an enabled set, compute one symmetric raw field:

`T = rotl(sum(values) mod 2^w, 1)`

and rewrite every member identically:

`x' = (x + T) mod 2^w`.

Events that would be no-ops are ignored. The stateless min/max schedulers do not explicitly prioritize arity.

## Equal-budget history assay

As before, compare two histories with exactly the same five width-3 writes and the same physical event budget, changing only order:

- `A,A,A,B,B`
- `B,B,A,A,A`

with `B` the 3-bit complement of `A`.

Sweep eight deterministic backgrounds, both stateless scheduler orientations, four injection positions, and four complement-pair representatives: **256 comparisons per key width**.

## Result

### key width 3

- same full relation repertoire: 4
- seq1 strict superset: 24
- seq2 strict superset: 19
- incomparable reorganization: **209**
- different executable arity set: **9/256**
- different future event trace: 252/256

### key width 4

- same: 3
- seq1 strict superset: 9
- seq2 strict superset: 6
- incomparable reorganization: **238**
- different executable arity set: **51/256**
- different future event trace: 255/256

### key width 5

- same: 2
- seq1 strict superset: 33
- seq2 strict superset: 10
- incomparable reorganization: **211**
- different executable arity set: **109/256 = 42.58%**
- different future event trace: 254/256

At width 3 the medium is dense enough that arities 2/3/4 are usually all available simultaneously. As relation matching becomes less dense, history increasingly changes the arity repertoire itself.

## Interpretation boundary

This does **not** show that the substrate invented the concept of arity. The physical kernel permits arbitrary finite-set interactions and the implementation truncates search at arity four.

The narrower result is:

> with one arity-generic content relation and a fixed finite compute budget, equal-budget history can change whether pairwise, ternary, or four-way dependencies are currently executable.

This is stronger than K6b only in one specific sense: the dependency cardinality is no longer fixed by a separate hard-coded event type.

## Next audit

A repertoire difference is not yet causal evidence that arity itself matters. The next test should hold as much endpoint content as possible fixed and ask whether transferring the minimal members required for a higher-order event transfers a future execution class, while proper subsets fail.
