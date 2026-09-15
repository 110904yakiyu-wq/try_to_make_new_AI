# Experiment 080 — neutral relational ecology

## Question

Experiment 079 produced stable coexistence of multiple relational organizations, but without turnover the domain boundaries were completely frozen.

Can the same permutation-symmetric substrate support actual birth, extinction, replacement, and reformation dynamics if we add only unbiased local turnover?

## Setup

- same parallel `A-B-A` relational catalyst as Experiment 079;
- 8 exchangeable raw symbols;
- ring size 96;
- no symbol-specific rule;
- after each parallel sweep, replace 0, 1, 2, or 4 randomly chosen sites by a uniformly chosen different symbol;
- 32 deterministic seeds for ecology statistics;
- 64 seeds for pair-occupancy symmetry audit.

The turnover is external physical noise, not reward or fitness.

## Static-domain control

Without turnover, two initialized alternating domains remain exactly frozen for 100 sweeps:

- `(0,1): 46 -> 46` active motifs;
- `(2,3): 46 -> 46` active motifs.

So coexistence by itself is not yet ecology.

## Dynamic result

With one unbiased mutation per sweep, averaged over 32 seeds:

- pair births per sweep: **0.475**;
- pair deaths per sweep: **0.474**;
- pair reappearances per sweep: **0.462**;
- dominant-pair switches per sweep: **0.088**;
- mean active pairs in the late trajectory: **9.39**;
- mean dominant-pair motif fraction: **0.336**;
- adjacent-sweep pair-set Jaccard: **0.905**.

All **28/28** unordered symbol pairs appear during every 1500-sweep run at noise levels 1, 2, and 4 in the default 32-seed sweep.

Increasing turnover increases birth/death/reappearance and dominant-pair switching while retaining substantial pair-repertoire continuity.

## Absolute-value neutrality audit

At noise=1, aggregate occupancy over 64 seeds and 1500 sweeps gives pair-presence fractions:

- minimum: **0.3178**;
- maximum: **0.3508**;
- mean: **0.3353**;
- coefficient of variation: **2.41%**.

Thus no particular raw pair is systematically privileged in the observed ecology. The dynamics are approximately neutral with respect to symbol identity, as required by the permutation-symmetric rule.

## Interpretation boundary

Supported:

> permutation-symmetric relational organizations can undergo persistent birth, extinction, reappearance, and dominance turnover under finite local disturbance.

But this is a **neutral ecology**. All pair organizations are related by symbol permutation and therefore have the same operational type under this kernel.

That gives a useful no-go boundary:

> if all persistent organizations are operationally isomorphic and the environment is also symbol-symmetric, there is nothing for selection to prefer except finite-size drift.

So adding more turnover will not create meaningful adaptation by itself.

## Next move

The substrate needs **heritable relational variation**, not merely different symbol labels.

The next experiment should permit more than one relational organization type while keeping raw symbol values exchangeable. A minimal candidate is a generic repetition-extension rule that can support different spatial periods / relational grammars (for example period-2 and period-3 organizations) under one common physical rule.

Then perturbations can test whether organizations with genuinely different operational consequences are differentially maintained, without assigning fitness scores or privileged symbol identities.
