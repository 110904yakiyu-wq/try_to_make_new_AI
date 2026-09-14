# Experiment 059 — causal history-dependent closure-cost compression

## Question

Can equal-budget history make the **same local transformation consequence** reachable with a shorter self-delimiting context scan, without changing the fixed K8 microphysics?

This is the closest assay so far to the earlier working hypothesis:

> understanding may look like reducing the resource cost required to expose a consequential distinction or transformation.

## Strict case definition

Use K8 with:

- key width 4
- six-window ring capacity (`size=24`)
- equal-budget `A,A,A,B,B` vs `B,B,A,A,A` histories
- 64 deterministic backgrounds
- both stateless scheduler orientations

For every physical start position, compare the first nontrivial XOR closure in the two trained states.

A **strict comparable case** requires both histories to have:

1. the same first window value at that start;
2. the same generated shared field `T`;
3. different closure depth.

Because K8 rewrites each member as

`x' = (x + T) mod 2^w`,

the first local member undergoes the same transformation in both histories. The difference is how many additional context windows must be scanned before that transformation becomes enabled as a closed interaction.

## Causal transplant

For each strict case:

- choose the cheaper history as donor;
- keep the recipient's identical first window untouched;
- copy only the donor's additional prefix context windows needed before its earlier closure;
- recompute the first closure at the same physical start.

Then apply a one-bit break control to the last transplanted context window.

## Result

Across **73,728** same-start comparisons:

- equal closure cost: 43,372
- seq1 cheaper: 16,087
- seq2 cheaper: 14,269

So history changes raw first-closure scan cost frequently, with no strong directional bias between the two arbitrary sequence labels.

More importantly:

- same first window + same field `T`: **453** cases
- of these, same depth: 390
- **strict cost difference: 63 cases**

For all 63 strict cases:

- donor prefix-context transplant restores the donor's shorter exact closure: **63/63**
- flipping one bit in the final transplanted context destroys that exact restoration: **63/63**

Observed expensive -> cheap depth reductions include:

- 4 -> 3: 12
- 5 -> 4: 11
- 6 -> 2: 10
- 4 -> 2: 8
- 3 -> 2: 7
- 6 -> 5: 5
- 6 -> 4: 4
- 5 -> 3: 4
- 6 -> 3: 1
- 5 -> 2: 1

## Interpretation

This is not a claim of semantic understanding.

The narrow causal statement is:

> under fixed K8 microphysics, history can construct a local context that makes the same first-member transformation field available after a shorter bounded scan, and transferring that context transfers the resource reduction.

This is qualitatively different from merely changing which event happens. The first local value and the shared transformation field are held equal; the changed quantity is the amount of surrounding context needed to enable that transformation.

## Why this matters

Earlier experiments showed history-dependent state, grammar, and interaction arity. This experiment adds a resource dimension:

`history -> context construction -> lower operational access cost`

That is a plausible substrate-level precursor of learned expertise or compiled understanding, without a weight update rule or explicit cache object.

## Boundary

The effect is currently rare under the strict comparability filter: 63 cases out of 73,728 start comparisons. It should not be generalized beyond this toy substrate yet.

The next audit should test robustness across key width, ring capacity, and background distribution, and should compare against a context transplant drawn from an unrelated history rather than only a one-bit break control.
