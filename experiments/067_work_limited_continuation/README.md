# Experiment 067 — work-limited continuation audit

## Question

Experiment 065 coupled K8 to real CPU work but still evaluated access cost from outside. Does repeated perturbation training make a familiar perturbation support **more actual interaction events** under the same finite work budget?

This uses the sequential work-accounting scheduler from Experiment 065:

- prefix reads consume budget;
- rewrites consume budget;
- the number of events that physically execute before budget exhaustion is the readout.

No Hamming recovery metric or observer cost-map distance is used here.

## Assay

Train matched states with repeated same-strength XOR perturbations `P` or `Q`. Then challenge both states with P and Q separately.

A matching advantage means the state trained under a perturbation executes more K8 interactions after that same perturbation than the mismatched state.

## Result

16 backgrounds, key width 3, 1152 matched perturbation-pair comparisons:

### work budget 24

- net matching advantage: **256**
- net mismatching advantage: **531**
- ties: **365**
- strict P/Q cross-over: **73**

### work budget 48

- net matching advantage: **365**
- net mismatching advantage: **516**
- ties: **271**
- strict cross-over: **94**

### work budget 96

- net matching advantage: **425**
- net mismatching advantage: **435**
- ties: **292**
- strict cross-over: **118**

## Interpretation

This is another negative result for learning.

Even when computational access cost directly controls how much physical execution occurs, repeated exposure to a perturbation does not reliably make the substrate better able to continue executing under that perturbation.

At low and medium work budgets the direction is actually more often opposite to familiarity; at the largest tested budget it is approximately balanced.

Therefore K8 has no supported mechanism for consequence-driven retention. It can generate history-dependent contexts and costs, but successful interaction does not feed back strongly enough to preserve or amplify the structures that enabled it.

## Next substrate requirement

The next kernel should add **precariousness** rather than another observer metric:

> inability to sustain interaction under finite resource should physically destabilize the current medium, while successful interaction prevents or repairs that destabilization.

This still need not be a reward scalar. It is a continuation condition built into the substrate physics.
