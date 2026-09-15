# Experiment 082 — period proposal agreement

## Question

Experiment 081 showed strong period-2 dominance, but its update rule explicitly chose the shortest eligible repeated block.

Was that dominance merely caused by the shortest-period tie break?

## Control

Keep the same symbol-permutation-symmetric repetition extension idea, but remove period priority completely.

For each target position:

1. every eligible period `p=2..8` proposes the symbol required to continue its own local repetition;
2. if all nontrivial proposals agree, apply that symbol;
3. if proposals disagree, do nothing.

No shortest or longest period is selected.

## Result

The period-2 monopoly remains.

With one unbiased mutation per sweep:

- period 2 mean late coverage: **110.47 / 120**;
- periods 3–8: **0**.

With noise=2:

- period 2: **102.87**;
- period 3: **0.009**;
- period 4: **0.147**.

Even at noise=4, period 2 still dominates at **82.55**, while period 3 and 4 each remain below 1 on average.

Proposal conflict is essentially absent:

- noise 0–2: **0** mean conflicts;
- noise 4: **0.00156** conflicts per sweep.

So removing the explicit priority convention barely changes the qualitative result.

## Interpretation

The hidden fitness prior is deeper than scheduler tie breaking.

A short relational organization has a combinatorial nucleation advantage:

- a short repeated block is much more likely to occur accidentally;
- after perturbation it is cheaper to reconstruct;
- once present it supplies more local continuation opportunities.

Thus finite local dynamics itself creates an implicit complexity prior even when raw symbols are exchangeable and execution priority is neutralized.

The strongest supported statement is:

> organization types with different description / closure lengths are not automatically fitness-neutral under finite resources.

This matters for the larger project. A substrate can secretly prefer some representations even without an explicit reward, learner, or semantic label.

## Next question

Do not artificially normalize period frequencies; that would simply hand-design equal fitness.

Instead, introduce an environment in which relational organizations with different structural costs also have different **consequences**. Then test whether the ecology shifts between organization types when the disturbance regime changes.

The relevant target is not “all types are equally common.” It is:

> can a fixed, symbol-symmetric substrate support heritable structural variation whose persistence changes with environmental consequences, without an explicit fitness score?
