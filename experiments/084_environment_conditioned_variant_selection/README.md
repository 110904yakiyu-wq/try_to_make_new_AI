# Experiment 084 — environment-conditioned variant filtering

## Question

Experiment 083 showed that pre-existing period-2 and period-3 organizations have different consequences under E2 and E3 environments.

But that could still be dismissed as an initialization artifact: the experimenter supplied both organization types in advance.

Can a new relational type arise from generic turnover and persist only in the environment where its structure is consequentially compatible?

## Setup

Start from a ring that is entirely period-2.

The only variant source is one unbiased symbol replacement per sweep.

Compare three regimes:

- no positional environment;
- E2: rotate every 2-cell block;
- E3: rotate every 3-cell block.

Raw symbol labels are randomized across seeds. The repetition-extension substrate remains symbol-permutation symmetric.

Observer classification uses **minimal** persistent period:

- a location is counted as p2 first if it has period 2;
- only locations that are not p2 but do have period 3 are counted as p3.

This prevents homogeneous or period-2 structure from being double-counted as period-3.

## Variant-emergence result

Over 600 sweeps and 16 seeds:

### No environment + turnover

- late p2 coverage: **114.0**
- late p3 coverage: **0.0**
- p3 births: **0**

### E2 + turnover

- late p2 coverage: **114.0**
- late p3 coverage: **0.0**
- p3 births: **0**

### E3 + turnover

- late p2 coverage: **108.32**
- late p3 coverage: **2.45**
- maximum observed p3 coverage: **25.63**
- p3 birth episodes: **6.56** per run
- mean p3 episode lifetime: **19.57** sweeps
- mean maximum p3 lifetime: **69.38** sweeps
- first p3 appearance: about **42.4** sweeps

## Generation-vs-filtering control

E3 without turnover produces:

- p3 coverage: **0**
- p3 births: **0**

Therefore E3 does not directly write a period-3 organization into the medium.

The combination matters:

- turnover supplies structural variation;
- E3 changes which variants can persist and expand long enough to become an observer-detectable p3 organization.

## Environment-switch result

Using 32 seeds and switching at sweep 300:

### E2 -> E3

Before switch:

- p2: **114.0**
- p3: **0.0**

Late after switch:

- p2: **102.20**
- p3: **4.58**

### E3 -> E2

Before switch:

- p2: **99.74**
- p3: **5.67**

Late after switch:

- p2: **112.91**
- p3: **0.0**

### E3 -> no environment

Before removal:

- p3: **5.67**

Late after removal:

- p3: **0.0**

## Interpretation

This is the first experiment in this line where all of the following hold simultaneously:

1. the starting medium contains only one relational organization type;
2. raw symbols remain exchangeable;
3. variation is supplied by generic turnover, not a p3-specific mutation rule;
4. a new relational type appears only under a compatible environmental consequence;
5. changing the environment reverses which type persists.

The conservative description is **environment-conditioned ecological filtering of structural variants**.

It is still not learning in the strong sense.

The p3 organization disappears when E3 is removed, so the medium has not internalized the environmental regularity into a new self-maintaining organization. The environment remains part of the closure supporting that variant.

## Next question

Can an environment-selected structural variant become sufficiently self-maintaining that it survives after the environmental support is removed?

That is the next boundary between:

- externally scaffolded ecological filtering, and
- internally retained adaptation.

The next experiment should therefore allow locally selected organization to modify its own regeneration context, then test **post-environment persistence** without adding a reward scalar or explicit fitness memory.
