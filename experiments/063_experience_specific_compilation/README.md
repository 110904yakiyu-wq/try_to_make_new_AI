# Experiment 063 — experience-specific cost compilation audit

## Question

Experiments 059–062 showed that K8 can form reusable contexts that reduce access cost to an operational transformation identity.

Does repeating experience `A` selectively make an `A`-probe cheaper than repeating its complement `B`, and vice versa?

That would be stronger than generic history dependence and would justify language such as experience-specific compilation.

## Strict assay

For each initial background, scheduler policy, aligned position, and complement pair `A/B`:

1. train one state with five copies of `A`;
2. train a matched state with five copies of `B`;
3. write the **same query probe** into both states;
4. require both queried states to expose the same operational transformation identity
   `E = (first window value, shared field T)`;
5. compare only the closure depth needed to reach that same `E`.

The `A` query counts as experience-specific only if the A-trained state is cheaper. The B query is symmetric.

A strict cross-over requires both effects simultaneously in the same history pair.

## Result

### Default check: 16 backgrounds

Key width 3:

- cases: **768**
- A-comparable: **49**
  - A-trained cheaper: **11**
  - equal: **14**
  - B-trained cheaper: **24**
- B-comparable: **43**
  - B-trained cheaper: **14**
  - equal: **16**
  - A-trained cheaper: **13**
- strict cross-over: **0**

Key width 4:

- cases: **768**
- comparable cases are much rarer;
- strict cross-over: **0**.

### Width-3 confirmation: 32 backgrounds

- cases: **1536**
- A-comparable: **108**
  - matching A experience cheaper: **34**
  - equal: **36**
  - mismatching B experience cheaper: **38**
- B-comparable: **107**
  - matching B experience cheaper: **42**
  - equal: **34**
  - mismatching A experience cheaper: **31**
- both A and B queries comparable in the same pair: **2**
- strict cross-over: **0**

Across the separate A/B comparable queries, matching experience is cheaper in **76** observations and mismatching experience is cheaper in **69**. There is no clear selective direction, and there is no strict pairwise cross-over.

## Interpretation

This is a negative result.

K8 supports:

- history-dependent operational repertoires;
- history-dependent access costs;
- reusable causal context patterns;
- multiple micro-contexts implementing the same operational accelerator role.

But **mere repeated exposure does not automatically privilege transformations associated with the repeated experience**.

Therefore the project should not call K8 learning, frequency compilation, or understanding on the basis of Experiments 059–062 alone.

## Consequence

The missing ingredient is no longer memory or history dependence. It is **differential retention / selection of useful history-generated context**.

The next substrate change should therefore be minimal and explicit: add a physical retention asymmetry without adding reward labels, task semantics, SELF, or a hand-written learner.
