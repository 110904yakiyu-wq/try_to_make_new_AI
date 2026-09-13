# Experiment 017 — operational quotient drift

## Question

Can a fixed local law, with no learner or mutable rule, induce different finite operational equivalence classes when the observer changes only when/where the same bounded interaction assay is applied?

This experiment moves back toward the original theoretical question: not whether a state variable changes, but whether **what counts as operationally indistinguishable** can change.

## Signature

For each of the eight width-3 exposure patterns:

1. run one-shot exposure,
2. run repeated exposure,
3. at every sampled exposure position, apply all eight width-3 probes at a remote site,
4. record `repeated impact - one-shot impact` for every position × probe pair.

No averaging is used when deciding exact equivalence. The complete finite vector is the exposure pattern's history-effect signature under the current observer condition.

Two exposure patterns are placed in the same operational class only when these complete signatures are identical (within numerical tolerance).

## Conditions

The physical ECA rule is unchanged. The assay budget is unchanged. Only probe offset/time are varied:

- baseline: offset 20, time 48
- offset12_t48
- offset20_t40
- offset20_t56

## Result

Some rules show exact quotient drift.

Examples:

- Rule 98: `7 -> 2 -> 2 -> 7` classes
- Rule 226: `7 -> 4 -> 4 -> 7`
- Rule 143: `7 -> 4 -> 4 -> 6`
- Rule 110: `8 -> 8 -> 7 -> 8`
- Rule 151: `7 -> 7 -> 8 -> 7`

Other rules are stable under these conditions:

- Rule 14: 5 classes throughout
- Rule 113: 5 throughout
- Rule 142: 5 throughout
- Rule 126: 8 throughout
- Rule 129: 8 throughout

## Interpretation

The result is modest but conceptually useful.

No explicit category labels or mutable ontology are present in the substrate. Nevertheless, under a finite operational assay, the same exposure patterns can merge into or split out of exact equivalence classes as the interaction condition changes.

This is **not** endogenous metacognition: the observer is still changing probe time/position from outside. It is only a substrate-level demonstration that operational identity need not be globally fixed even when the physical law is fixed.

A later experiment must make the context change arise from the substrate's own history rather than from an external experimenter. That is the important next boundary.
