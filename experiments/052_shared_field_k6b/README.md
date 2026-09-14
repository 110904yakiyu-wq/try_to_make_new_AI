# Experiment 052 — shared-field role-symmetric K6b

## Motivation

Experiment 050 removed hard endpoint roles but retained strong local triple locking: 493/512 first-to-second event transitions reused all three physical positions.

K6b keeps the same role-symmetric compatibility and stateless scheduler, changing only the symmetric rewrite equation.

## Rewrite

For an enabled triple `(X,Y,Z)` define one raw shared field

`T = rotl(X XOR Y XOR Z, 1)`.

Then apply exactly the same operation to all three windows:

- `X' = X XOR T`
- `Y' = Y XOR T`
- `Z' = Z XOR T`

T is not stored as a rule object or decoded as an opcode. It exists only as the instantaneous bitwise consequence of the current triple.

## Equal-budget repertoire result

Using the same eight dense deterministic backgrounds as Experiment 050, across **256** history comparisons:

- same repertoire: **19**
- seq1 strict superset: **14**
- seq2 strict superset: **20**
- incomparable reorganization: **203**
- future eight-event trace differs: **234/256**

## Partner-turnover result

Across the 512 trained states, physical endpoint overlap from event 1 to event 2 is:

- all 3 endpoints reused: **322**
- 2 endpoints reused: **20**
- 1 endpoint reused: **52**
- 0 endpoints reused: **118**

Thus the partner set changes in **190/512 = 37.1%** of trajectories, versus only 19/512 in the original K6.

## Distributed causal subset result

For the **468** directed donor->recipient cases with different future traces, exhaustively transplant subsets of the donor's first three event windows.

- minimum 1 endpoint: **20**
- minimum 2 endpoints: **5**
- all 3 endpoints required: **48**
- selected triple insufficient even when all 3 are copied: **395**

Among the 73 locally reproducible cases, **53/73** require multiple endpoints and **48/73** require the full ternary context.

## Interpretation

K6b is a better null substrate than K6 for the current goal:

- no hard A/B/M role;
- no rule object or persistent graph;
- history strongly reorganizes the currently executable relation repertoire;
- interaction partners turn over substantially more often;
- locally reproducible execution is more often genuinely multi-region.

This still does not constitute intelligence or an emergent language. The compatibility predicate and shared-field equation remain fixed physical law.

## Next question

Does one ternary interaction alter **how later interactions reorganize the repertoire**, even when the immediate observable repertoire is matched? That is the analogue of second-order operational memory for transformation grammar.