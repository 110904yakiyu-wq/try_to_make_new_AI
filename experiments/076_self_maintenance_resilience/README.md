# Experiment 076 — self-maintenance resilience audit

## Question

K10 did not create robust experience-specific operational recovery. Did its interaction-catalyzed regeneration nevertheless create a stronger form of self-maintaining organization?

## Assay

For K8, K9, and K10:

1. start from deterministic random states under min/max stateless policies;
2. follow autonomous dynamics until the eventual limit cycle is identified;
3. choose a state on that cycle;
4. perturb bits;
5. follow the perturbed state to its eventual cycle;
6. ask whether it returns to exactly the original cycle.

No learning or reward metric is involved. This is a direct attractor-restoration test.

## One-bit result

Across 64 sampled cycles and all 18 one-bit perturbations per cycle:

- K8: **8/1152 = 0.69%** return to the same cycle
- K9: **87/1152 = 7.55%**
- K10: **244/1152 = 21.18%**

## Two-bit result

Across 32 sampled cycles and all `C(18,2)=153` two-bit perturbations per cycle:

- K8: **55/4896 = 1.12%**
- K9: **351/4896 = 7.17%**
- K10: **470/4896 = 9.60%**

K10 remains the most resilient, although its advantage over K9 shrinks for two-bit damage.

## Interpretation

Interaction-catalyzed regeneration has a real dynamical effect: it creates organizations that are substantially more likely to restore the same autonomous attractor after local damage.

But Experiment 075 showed that K10 still lacks robust schedule-independent experience-specific operational adaptation.

Therefore this toy sequence now demonstrates a useful separation:

> **self-maintenance / resilience is not sufficient for learning.**

This is consistent with the broader theoretical warning that autopoiesis-like closure alone should not be equated with intelligence.

## Next question

Without changing K10's physics, does repeated exposure to perturbation `P` preferentially move the medium into attractors that are more resilient to `P` than attractors reached after repeated `Q` exposure?

That would test consequence-sensitive attractor selection rather than observer-defined access-cost learning.
