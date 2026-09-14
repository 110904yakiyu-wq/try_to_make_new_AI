# Experiment 028 — minimal event-driven K1 substrate

## Motivation

K0 (synchronous ECA) showed that fixed local laws can produce history-dependent recurrent contexts and operational repertoires, but it did **not** provide endogenous execution-level selection. Every cell was updated every tick regardless of the current medium state.

K1 makes only one physical change:

> keep the binary ring and fixed ECA truth table, but execute local updates asynchronously through an enabled-event queue.

No learner, reward, SELF, symbolic rule language, plastic truth table, or explicit memory is added.

## Event semantics

A site is **enabled** when the ECA truth table would change its current bit.

The simulator keeps a FIFO queue of potentially enabled sites.

When one site actually changes, only that site and its immediate neighbors are re-enqueued, because only those local enabledness relations can have changed.

The external experiment allocates the same number of queue-processing slots to both compared histories. An empty queue consumes idle budget, so physical work-slot budget remains equal even when the number of successful state-changing events differs.

## Equal-budget history test

Use the same history pair as Experiments 026/027:

- sequence 1: `A,A,A,B,B`
- sequence 2: `B,B,A,A,A`

with complementary width-3 patterns A/B.

Each injected pattern is followed by 128 event-processing slots.

After the fifth injection, observe eight additional blocks of 64 processing slots.

Measure two recurrent repertoires across those post-training snapshots:

1. all naturally occurring radius-2 local patches,
2. only radius-2 patches centered on sites that are currently **physically enabled** to update.

A context must occur in at least two snapshots to enter either repertoire.

## Default result

Cases: **1024**

### Recurrent local-context repertoire

- same: **410**
- non-nested reorganization: **406**
- sequence 1 strict superset: **102**
- sequence 2 strict superset: **106**

Changed: **614 / 1024 = 59.9609%**

### Enabled-event context repertoire

- same: **503**
- non-nested reorganization: **351**
- sequence 1 strict superset: **93**
- sequence 2 strict superset: **77**

Changed: **521 / 1024 = 50.8789%**

### Actual computation performed

The two histories receive the same number of queue-processing slots, but successful bit-changing event counts differ in **682 / 1024 = 66.6016%** of cases.

- mean absolute update-count difference: **24.8623**
- mean successful updates, sequence 1: **483.3857**
- mean successful updates, sequence 2: **488.5762**

## Interpretation

This is the first project substrate where history changes a repertoire at the **execution layer**, not only under an observer-side probe assay.

The current medium determines which local interactions are enabled. Different equal-budget histories therefore leave different sets of contexts eligible to receive future computational work, and they often consume different amounts of actual state-changing work under the same external slot budget.

This is a weaker and safer claim than saying that the system 'chooses' or 'attends'.

What has emerged is only a primitive physical analogue of selection:

> history changes which interactions are currently executable.

That is enough to justify continuing with K1 rather than immediately adding higher-level learning machinery.

## Important boundary

The FIFO scheduler is still a fixed physical assumption and introduces an ordering convention external to the binary medium.

The enabled predicate is also derived from the fixed ECA truth table.

Therefore this is not yet an endogenous scheduler in the strongest sense. The next audits should test:

1. robustness to scheduler changes,
2. whether recurrent local contexts causally create/suppress enabled events,
3. whether the same context can route computation differently depending on history,
4. whether event sparsity yields a genuine CPU-work advantage rather than merely a different dynamics.
