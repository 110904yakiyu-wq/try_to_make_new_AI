# Experiment 077 — attractor resilience selection audit

## Question

K10 creates substantially more self-restoring attractors than K8/K9. Does repeated exposure to perturbation `P` preferentially move the medium into an attractor that is more resilient to `P` than attractors reached after repeated `Q` exposure?

This tests adaptation using **self-maintenance consequence** rather than access-cost distance.

## Assay

For each same-Hamming-weight pair `(P,Q)`:

1. train one K10 state with repeated `P`, another with repeated `Q`;
2. identify each state's eventual autonomous limit cycle;
3. for every phase on that cycle, apply `P` or `Q`;
4. measure the fraction of phases that return to exactly the same attractor;
5. compare whether P-training raises P-resilience and Q-training raises Q-resilience.

## Result

Using 8 backgrounds:

- repeat 1: `116 match / 106 mismatch / 354 ties`, strict 9
- repeat 3: `112 / 132 / 332`, strict 15
- repeat 5: `132 / 129 / 315`, strict 14
- repeat 8: `130 / 123 / 323`, strict 15
- repeat 12: `125 / 125 / 326`, strict 13

There is no monotone or robust experience-specific resilience selection.

## Interpretation

K10 demonstrates that interaction-catalyzed regeneration can create self-maintaining attractors, but repeated perturbation does not systematically select attractors specialized for that perturbation.

This gives a stronger boundary than Experiment 075:

> **self-maintenance and resilience are still not enough for adaptive learning.**

The missing ingredient is not simply persistence. Some consequence of organization must feed back into which organizations occupy future computational opportunity.

Rather than adding a scalar reward or a bespoke reinforcement rule, the next direction is ecological:

- multiple local organizations coexist in one medium;
- organization must continually regenerate under turnover;
- computational opportunity is finite;
- recurrently viable organizations can occupy more of the medium only through the same substrate interactions;
- no externally labelled winner is selected.

This moves toward artificial chemistry / autocatalytic ecology, so any positive result must be interpreted against that prior-art boundary.
