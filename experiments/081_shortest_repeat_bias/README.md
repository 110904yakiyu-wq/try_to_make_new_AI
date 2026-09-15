# Experiment 081 — shortest-repeat bias

## Motivation

Experiment 080 produced a genuinely dynamic but neutral ecology. Different raw symbol pairs were exchangeable, so there was no heritable operational variation for selection to act on.

A natural next idea is to let different **relational organization types** coexist: period-2, period-3, period-4, and so on, while keeping raw symbol identities fully exchangeable.

## Candidate rule

For every target position, search backward for a repeated block:

- find a period `p` such that the two immediately preceding length-`p` blocks are identical;
- extend that repetition by copying the symbol expected at the target;
- use the smallest eligible `p`.

The rule is invariant under arbitrary permutation of symbol labels. It therefore removes absolute-value preference.

However, it contains a new hidden preference: **shortest closure wins**.

## Result

The hidden preference dominates the ecology.

With one unbiased symbol mutation per sweep, late-trajectory mean coverage on a 120-symbol ring is approximately:

- period 2: **110.51**
- period 3: **0.00**
- period 4: **0.00**
- period 5–8: **0.00**

With noise=2, period 2 still covers about **102.33/120** positions. Even with noise=4 it remains dominant at **84.49/120**, while all longer periods together are negligible.

Without noise, some period-3 and period-4 structure survives, but the active type count remains below one on average in the late trajectory because many seeds settle into states with no observer-detected persistent repetition.

## Interpretation

This is a useful negative result.

Removing raw-symbol privilege is not enough. The scheduler / closure convention can privilege an **organization description** instead.

Here the substrate effectively contains an Occam-like fitness prior:

> shorter repeating explanations are always given causal priority over longer ones.

That makes period-2 organization a built-in winner. Calling the resulting dominance “selection” would therefore be misleading.

## Broader lesson

The same problem appeared earlier in different forms:

- absolute bit pattern could be catalytic;
- sequential timing could give one organization nonlocal replication speed;
- now shortest-description priority gives one relational type a structural fitness advantage.

So the audit target should be strengthened:

> not only raw values, but also representation length, interaction arity, closure depth, and scheduler order must be checked for hidden fitness priors.

## Next move

Do not tune the shortest-repeat rule.

Instead, compare candidate relational organizations under a **common causal budget** without giving shorter periods earlier execution priority. A useful next control is to let every eligible period propose a continuation in parallel and only apply a write when all currently eligible proposals agree; conflicts remain unresolved rather than being broken by period length.

If this removes period-2 monopoly while retaining multiple relational organization types, then the hidden fitness prior was indeed the priority convention rather than periodic organization itself.
