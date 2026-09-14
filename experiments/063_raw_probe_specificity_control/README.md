# Experiment 063 — raw-probe specificity control

## Question

Does repeated exposure to raw input pattern A selectively reduce the K8 scan cost of a later A probe, compared with a matched B-trained history, and vice versa for B?

This is a deliberately strict control against over-interpreting the access-cost effects from Experiments 059–062 as learning.

## Setup

Two histories start from the same background and receive equal work budgets:

- A-trained: `A,A,A,A,A`
- B-trained: `B,B,B,B,B`

where B is the width-3 complement of A.

Training occurs at position 0. Testing occurs at the antipodal aligned position, separated from the training site.

Each saved trained state is tested with both an A probe and a B probe. The assay measures the self-delimiting closure depth from the test position.

A true raw-pattern specificity effect would require a cross-over:

- A-trained cheaper than B-trained on A probe;
- B-trained cheaper than A-trained on B probe.

## Result

Using 256 deterministic backgrounds, both stateless scheduler orientations, and all four A/B complement representatives:

### key width 3

- trials: 2048
- A-probe comparable: 506
  - matched cheaper: 207
  - equal: 82
  - matched costlier: 217
- B-probe comparable: 522
  - matched cheaper: 202
  - equal: 86
  - matched costlier: 234
- all four probe costs available: 127
- strict two-sided cross-over: **14/127**
- reverse two-sided effect: **34/127**
- mean cross-over score `(Btrain(A)-Atrain(A)) + (Atrain(B)-Btrain(B))`: **-0.7874**

### key width 4

- trials: 2048
- A-probe comparable: 223
  - matched cheaper: 88
  - equal: 50
  - matched costlier: 85
- B-probe comparable: 228
  - matched cheaper: 84
  - equal: 56
  - matched costlier: 88
- all four probe costs available: 21
- strict two-sided cross-over: **1/21**
- reverse two-sided effect: **6/21**
- mean cross-over score: **-1.6667**

### key width 5

- trials: 2048
- A-probe comparable: 71
  - matched cheaper: 28
  - equal: 18
  - matched costlier: 25
- B-probe comparable: 76
  - matched cheaper: 28
  - equal: 15
  - matched costlier: 33
- all four probe costs available: 1
- strict two-sided cross-over: **0/1**

## Interpretation

There is no evidence here that K8 compiles the literal raw training symbol itself into a cheaper later probe.

In the denser width-3 and width-4 conditions, the aggregate direction is if anything slightly opposite to the desired cross-over.

This is a useful negative result. It blocks the easy story:

> repeated A exposure -> A becomes cheaper -> learning.

The more plausible target is not the externally supplied raw symbol A, but the **transformation roles that the substrate actually executes during the experience**.

## Next question

Define an experienced role from the first actual K8 event caused during an A exposure, then ask whether additional A exposures reduce access cost to that same role relative to an equal-budget B-trained control.

That moves the learning target from an observer-provided input label to an endogenous operational event.