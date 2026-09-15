# Experiment 092 — read-many / write-local audit

## Question

Parallel K8 has two kinds of nonlocality coupled together:

1. an event may read many width-bit windows before self-delimiting closure;
2. the same event rewrites every participating window.

Experiment 090 showed strong overlap and churn, but did not tell which nonlocality matters more.

This experiment leaves K8 closure discovery unchanged but applies the derived field only to one local output window (the first window of the closure).

No occupancy, token, reward, memory, or priority mechanism is added.

## Full-range result

With 12-window rings, 32 seeds, and 200 sweeps, localizing the write greatly reduces direct write-support overlap, but barely improves operational-role recurrence.

### width 3

- events/sweep: 24.19
- changed bits/sweep: 16.68 / 36
- local write-support overlap: 0.123
- role-set Jaccard: **0.085**
- 32/32 seeds remain active

### width 4

- events/sweep: 22.32
- changed bits/sweep: 19.71 / 48
- local write-support overlap: 0.157
- role-set Jaccard: **0.023**
- 32/32 remain active

### width 5

- events/sweep: 16.55
- changed bits/sweep: 18.38 / 60
- local write-support overlap: 0.205
- role-set Jaccard: **0.007**
- 32/32 remain active

A one-bit initial difference still propagates nearly to the opposite side of the ring in one sweep, because closure detection itself reads distant windows.

## Read-range cap

For width 4, local writes were kept while the maximum closure arity was varied.

Using 64 seeds and 500 sweeps around the transition:

- arity <= 5: role Jaccard **0.880**, but only 17/64 remain active;
- arity <= 6: Jaccard **0.540**, 28/64 active;
- arity <= 7: Jaccard **0.125**, 54/64 active;
- arity <= 8: Jaccard **0.039**, 61/64 active.

There is again a sharp activity/stability tradeoff rather than a clean metastable middle.

## Interpretation

The dominant source of churn is not the physical extent of the write.

It is the fact that one atomic K8 event can make its execution depend on a context spanning a large fraction of the ring.

This means K8's `scan until closure` is doing hidden computational work outside the medium. A distant dependency can become causally relevant in one kernel step without any intermediate structure carrying that dependency through space and time.

That is inconsistent with the stronger finite-resource thesis of this project:

> expensive context should have to be constructed through reusable intermediate process, not granted as an atomic substrate operation.

## Next boundary

Do not tune the arity cap.

Replace atomic prefix scan with **finite-speed local construction of context**. Long-range closure should exist only if local interactions have physically propagated and composed the required information over multiple steps.

This is a kernel-level correction, not a learning mechanism.
