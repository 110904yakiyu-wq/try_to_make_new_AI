# Experiment 025 — hidden local-state audit

## Question

Experiments 020 and 021 found histories that have the same current operational quotient but later diverge autonomously.

A tempting interpretation was that a new, history-generated context from outside the current assay region later enters the probe's causal cone and creates a new distinction.

This experiment tests that interpretation directly.

## Method

Keep only cases where:

1. one-shot and repeated histories have the same quotient at the current time,
2. their quotients first diverge within the next 8 autonomous steps.

At the current time, transplant different regions between the two history states:

- **center**: the region already inside the current probe light cone,
- **annulus**: only the additional shell that can enter the probe light cone by the future distinguishing depth,
- **expanded**: center plus annulus, i.e. the full future causal region,
- **distant annulus**: the same annulus shifted half a ring away as a causal control.

Then allow the CA to evolve autonomously to the original distinguishing depth and recompute the quotient.

If the future divergence is genuinely caused mainly by newly arriving outer context, annulus transplant should transfer the future quotient. If hidden microstate already inside the current observational region is responsible, center transplant should dominate.

## Default result

Eligible same-now / later-diverge cases through depth 8: **247**

### Center transplant

- repeated -> single future quotient: **240 / 247**
- single -> repeated future quotient: **240 / 247**
- bidirectional exact switch: **235 / 247**

### Incoming annulus only

- repeated -> single: **4 / 247**
- single -> repeated: **3 / 247**
- bidirectional: **1 / 247**

### Full expanded future causal region

- repeated -> single: **243 / 247**
- single -> repeated: **245 / 247**
- bidirectional: **242 / 247**

### Distant-annulus control

- repeated -> single: **0 / 247**
- single -> repeated: **0 / 247**

## Interpretation

The earlier interpretation was mostly wrong.

The delayed quotient divergence is usually **not** produced by a newly arriving external shell that functions as a newly available test context.

Instead, one-shot and repeated histories already contain different local microstates inside the present probe light cone, even when the current operational quotient treats those histories as equivalent. The fixed assay is simply too coarse to expose those local differences immediately.

Future autonomous evolution then amplifies or rotates that already-present hidden local structure until the same assay can see a difference.

So the result is better described as:

> current operational equivalence can hide locally present dynamical state that later becomes operationally visible.

This is much closer to ordinary finite-depth behavioral equivalence than to endogenous metacognitive test generation.

## Consequence for the project

This negative result tightens the target.

To claim that the substrate makes a genuinely new test available to itself, it is not enough for a currently hidden microstate difference to become visible later under the same fixed probe family.

We need a stronger phenomenon in which an endogenous pattern changes the **effective interaction repertoire or cost**, rather than merely carrying hidden state through time.

Experiments 022–024 still matter: they show that compact local patterns are causally transferable, recurrent across histories, and predictive of future operational trajectories. The next step is to ask whether those patterns actually mediate a new interaction that could not be reproduced by merely waiting for hidden microstate to unfold.
