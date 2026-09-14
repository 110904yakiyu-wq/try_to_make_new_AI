# Experiment 058 — K7 subset oracle vs K8 prefix-scan scaling

## Question

Did K8 merely replace one arbitrary interaction rule with another, or did it also remove the combinatorial search oracle hidden in K7?

## Comparison

Let the ring contain `m` windows' worth of physical capacity, each window width `w`.

### K7

K7 globally enumerates every pairwise-disjoint subset of physical window starts for arities 2 through `m`.

For a circular ring of `N=m*w` bit positions, the number of size-`k` non-overlapping width-`w` window sets is

`N / (N-(w-1)k) * C(N-(w-1)k, k)`.

The total candidate catalogue is the sum over `k=2..m`.

### K8

K8 examines each physical start and extends one sequential prefix at most across the ring capacity. The worst-case number of closure checks is

`N * (m-1) = w*m*(m-1)`.

This is still not a fully local event queue, but it removes arbitrary subset enumeration.

## Default result, width 5

| window capacity m | K7 subset candidates | K8 prefix checks | ratio |
|---:|---:|---:|---:|
| 4 | 255 | 60 | 4.25x |
| 5 | 1,105 | 100 | 11.05x |
| 6 | 4,581 | 150 | 30.54x |
| 7 | 18,772 | 210 | 89.39x |
| 8 | 76,683 | 280 | 273.87x |
| 9 | 312,959 | 360 | 869.33x |
| 10 | 1,276,890 | 450 | 2,837.53x |
| 11 | 5,209,352 | 550 | 9,471.55x |
| 12 | 21,252,215 | 660 | 32,200.33x |

## Interpretation

K8's variable arity is not free, but its search frontier grows with a bounded sequential scan instead of an explicit combinatorial hyperedge catalogue.

This matters for the original CPU-first motivation: higher-order interaction should not require a hidden exponential matching oracle.

## Remaining issue

K8 still scans every possible start position to choose the globally preferred event. A later implementation should replace that full rescan with a reconstructible event frontier updated only near changed bits, while auditing that the frontier itself does not become a second hidden memory.

## Next experiment

Use K8's self-delimiting span as a resource measure. Test whether equal-budget history changes the number of windows that must be scanned before a consequential closure appears under the same physical start and same scan budget.
