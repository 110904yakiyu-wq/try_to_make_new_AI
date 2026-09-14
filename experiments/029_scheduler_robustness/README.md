# Experiment 029 — scheduler robustness of K1

## Question

Experiment 028 introduced an asynchronous event-driven K1 substrate and found history-dependent enabled-event repertoires.

The obvious audit is whether that phenomenon is merely an artifact of the FIFO queue order.

## Method

Keep every other physical assumption and resource budget unchanged, but replace the event scheduler with three deterministic policies:

- FIFO
- LIFO
- minimum-index first

For each scheduler, repeat the same 1024 equal-budget history comparisons from Experiment 028 and measure whether the recurrent repertoire of radius-2 patches centered on **enabled** sites differs between the two histories.

Also record whether the number of successful bit-changing updates differs despite identical queue-processing slot budgets.

## Default result

### FIFO

- same: 503
- reorganize: 351
- sequence 1 strict superset: 93
- sequence 2 strict superset: 77
- changed: **521 / 1024**
- successful-update count differs: **682 / 1024**

### LIFO

- same: 429
- reorganize: 337
- sequence 1 strict superset: 201
- sequence 2 strict superset: 57
- changed: **595 / 1024**
- successful-update count differs: **773 / 1024**

### Minimum-index first

- same: 566
- reorganize: 144
- sequence 1 strict superset: 260
- sequence 2 strict superset: 54
- changed: **458 / 1024**
- successful-update count differs: **231 / 1024**

Cross-scheduler persistence:

- changed under all three schedulers: **290** cases
- changed under at least one scheduler: **727** cases

Changed-case overlap:

- FIFO / LIFO: 414 cases, Jaccard ~0.5897
- FIFO / min-index: 351 cases, Jaccard ~0.5589
- LIFO / min-index: 372 cases, Jaccard ~0.5463

## Interpretation

The existence of history-dependent enabled-event repertoires is **not FIFO-specific**. It survives substantial changes in deterministic event ordering.

However, scheduler choice strongly affects **which** histories preserve the effect and the detailed superset/reorganization relation.

That is a useful correction rather than a failure:

> execution order is part of the physical substrate, not a semantically neutral implementation detail.

K1 therefore has two coupled physical ingredients:

1. local enabledness determined by the current medium,
2. a timing/scheduling law that decides which enabled interaction is realized first.

The project should not silently treat the latter as invisible infrastructure.

## Important boundary

The scheduler is still external to the binary medium. The substrate has history-dependent enabled interactions, but it does not yet generate its own scheduling law.

Before adding a self-modifying scheduler, the next safer test is causal: determine whether a naturally recurring local context can **create or suppress enabled events nearby**, and whether transplanting that context transfers the event-gating effect.
