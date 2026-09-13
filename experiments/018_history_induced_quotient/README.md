# Experiment 018 — history-induced operational quotient

## Question

Can the substrate's own history change what later probes are operationally equivalent **without changing the observer condition**?

Experiment 017 still changed probe time/position externally. Here those are fixed. The only difference is whether the same training pattern was experienced once or repeatedly before the fixed probe assay.

## Fixed observer condition

For every run:

- same ring size
- same sampled training positions
- same remote probe offset
- same probe time
- same probe horizon
- same eight candidate probes
- same full future-difference signature

The observer never changes the assay between the one-shot and repeated-history conditions.

## Operational quotient

For a given history, each of the eight candidate probes is assigned its complete finite effect signature across all sampled positions. Two probes are equivalent only when those signatures are exactly identical.

Compare the partition after one-shot exposure with the partition after repeated exposure.

Partition changes are classified as:

- `same`: identical quotient
- `refine`: repeated history only splits old classes
- `coarsen`: repeated history only merges old classes
- `reorganize`: neither partition refines the other; some old identities are destroyed while new identities are formed

## Result

History alone is sufficient to change the operational quotient for several fixed ECA laws.

Across all eight possible width-3 training patterns:

- Rule 98: 6 same, 2 refine
- Rule 14: 5 same, 1 refine, 1 coarsen, 1 reorganize
- Rule 113: 6 same, 1 refine, 1 reorganize
- Rule 142: 6 same, 1 refine, 1 reorganize
- Rule 226: 7 same, 1 refine
- Rule 143: 1 same, 4 refine, 3 reorganize
- Rule 151: 7 same, 1 reorganize
- Rule 159: 3 same, 4 refine, 1 reorganize
- Rules 126, 129, and 110: unchanged for all eight training patterns under this assay

The most important cases are `reorganize`, because they cannot be described as monotonic acquisition of finer distinctions.

Example, Rule 151 after training pattern `011`:

`{000,100} {001} ... -> {000,001} {100} ...`

The old equivalence between `000` and `100` disappears, while a new equivalence between `000` and `001` appears.

## Interpretation

This is the first experiment in the repository where the observer condition is held fixed and **history alone changes the operational identity relation**.

There is still no learner, ontology object, SELF variable, reward, mutable rule, or explicit meta-level in the substrate.

The result does **not** mean the CA performs metacognition. The quotient is still an observer-defined finite assay. But it crosses an important boundary:

> operational identity can reorganize non-monotonically as a consequence of endogenous history, even when the physical update law and the later observer assay are fixed.

The next question is whether a later substrate interaction can *use* such history-induced quotient changes, rather than them existing only as something an external observer can measure.
