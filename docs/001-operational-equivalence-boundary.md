# Operational equivalence — prior-art boundary

Date: 2026-09-14

This note is an audit, not a novelty claim.

## 1. The recent experiments rediscovered a classical shape

Experiments 018–020 showed that two histories can be indistinguishable under a finite observer assay yet become distinguishable after a later event or after additional autonomous evolution.

That general mathematical shape is not new.

### Testing equivalence

Process-algebra testing semantics identifies two processes when no allowed test distinguishes their observable behavior. A modern discussion of contextual/testing equivalence is:

- Bernardo & De Nicola et al., *Processes against tests: On defining contextual equivalences*, Journal of Logical and Algebraic Methods in Programming 129 (2022), 100799.
  https://doi.org/10.1016/j.jlamp.2022.100799

Probabilistic testing theory similarly identifies processes when they pass every test with the same probability:

- Bernardo, De Nicola & Loreti, *Algebraic theory of probabilistic processes*, Journal of Logic and Algebraic Programming 56 (2003), 117–177.
  https://doi.org/10.1016/S1567-8326(02)00069-3

### Bounded / k-bisimulation

Finite approximants to bisimulation formalize the fact that two states can agree for all observations up to depth `k` yet differ at a greater depth. For finitely branching settings, full bisimilarity is the limit of these finite-depth approximants.

A useful modern reference is:

- Abramsky, Dawar & Wang, *Relating Structure and Power: Comonadic Semantics for Computational Resources*, Journal of Logic and Computation 31(6) (2021), 1390–1429.
  https://doi.org/10.1093/logcom/exab048

The modal-logic viewpoint explicitly relates `k`-bisimilarity to indistinguishability by formulas/tests of modal depth at most `k`.

### Computational mechanics / causal states

Computational mechanics groups two past histories into the same causal state only when they induce the same conditional distribution over the entire future. In that idealized equivalence, two histories that later exhibit different future distributions were never the same causal state in the first place.

Recent overview/reference:

- *What Is a Pattern in Statistical Mechanics? Formalizing Structure and Patterns in One-Dimensional Spin Lattice Models with Computational Mechanics* (2026).
  https://pmc.ncbi.nlm.nih.gov/articles/PMC12839616/

The causal-equivalence principle is therefore stronger than the finite resource-bounded quotients used in this repository.

## 2. What Experiment 020 does and does not mean

Experiment 020 should **not** be described as discovering a new hierarchy of equivalence.

Its modest result is:

> under a deliberately bounded intervention assay, two different ECA histories can have the same current quotient while autonomous continuation later makes the same fixed assay separate them.

An omniscient observer of the complete microstate already distinguishes those histories. The apparent identity is resource-/test-relative by construction.

This is conceptually compatible with bounded testing and finite-depth bisimulation.

## 3. Where this hobby project is still trying something different

The interesting target is not the existence of bounded behavioral equivalences. Those are classical.

The target is to minimize the amount of **semantic testing machinery supplied by the designer**.

The long-term question is whether a finite fixed computational substrate can, through its own history:

1. create or make affordable new interactions that function as distinguishing tests,
2. thereby change its effective finite operational quotient,
3. retain second-order historical differences in how that quotient can later reorganize,
4. and eventually make such distinctions consequential to its own subsequent dynamics without an external observer selecting the relevant test language.

The present ECA experiments have only reached items 1–3 in a weak observer-relative sense. Item 4 has not been demonstrated.

## 4. Terminology discipline

Use these terms conservatively:

- **operational quotient**: equivalence classes induced by the explicitly stated finite assay;
- **operational depth / test cost**: resources needed by our assay to expose a difference;
- **history-induced quotient change**: same external assay, different prior substrate histories, different quotient;
- **second-order operational memory**: same current first-order quotient but different response of that quotient to a later common event;
- **autonomous quotient divergence**: same current quotient, no later intervention, different quotient after autonomous continuation.

Do not call these:

- metacognition,
- self-awareness,
- learning,
- causal states,
- or novel forms of bisimulation

without substantially stronger evidence.

## 5. Current boundary

The current experiments suggest a substrate can contain historical differences that are invisible to one finite quotient but visible to deeper/composed tests.

Classical theory already tells us that this is possible in principle.

The remaining hobby question is more architectural:

> can the substrate itself make deeper/composed tests operationally available and use the distinctions they reveal, while keeping the cognitive ontology out of the fixed kernel?
