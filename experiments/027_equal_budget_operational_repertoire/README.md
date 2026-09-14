# Experiment 027 — equal-budget operational repertoire

## Question

Experiment 026 showed that equal-budget histories with the same intervention multiset can leave different recurrent local patch repertoires.

This experiment asks whether those physical repertoire differences are merely different bit patterns, or whether they also correspond to different **operational quotient types**.

## Method

Use the same equal-budget history pair as Experiment 026:

- sequence 1: `A,A,A,B,B`
- sequence 2: `B,B,A,A,A`

with identical injection times `0,4,8,12,16` and `B` equal to the width-3 complement of `A`.

After training ends at time 48:

1. identify radius-2 patches that recur in at least two time slices of the next eight autonomous steps,
2. take each recurrent patch's first natural occurrence,
3. at that location compute the operational quotient induced by all eight width-3 probes over an eight-step response horizon,
4. compare the set of quotient types available through recurrent contexts in the two histories.

The experiment also asks a stricter question: when a physical patch exists only in one history, does its operational quotient type also fail to appear anywhere in the other history's recurrent context repertoire?

## Default result

Cases: **1024**

Operational repertoire relation:

- same: **602**
- non-nested reorganization: **209**
- sequence 1 strict superset: **104**
- sequence 2 strict superset: **109**

Thus **422 / 1024 = 41.2109%** of equal-budget history pairs differ in recurrent operational quotient repertoire.

Cross-tab with the physical patch repertoire:

- physical same / operational same: **342**
- physical same / operational changed: **29**
- physical changed / operational same: **260**
- physical changed / operational changed: **393**

History-exclusive physical patches produce at least one quotient type absent from the other history in **366 / 1024** cases.

Across those cases, the total counts of history-exclusive operational types are:

- sequence 1 only: **622**
- sequence 2 only: **601**

## Interpretation

The equal-budget result survives at the operational level.

Temporal order can change not only which local patterns recur but which probe-equivalence structures are naturally instantiated afterward, while keeping hardware, rule, intervention count, injection times, and input multiset fixed.

The most relevant cases are the strict supersets: under the same physical interaction budget, one history ends with recurrent operational context types that the other history never realizes during the same autonomous observation window.

This is a concrete toy example of a history-relative operational repertoire rather than a fixed, globally available test vocabulary.

## Important boundary

The quotient assigned to a recurrent patch is measured at its first occurrence. Experiment 023 shows that radius-2 patches predict current quotient across distinct histories with high accuracy, but the mapping is not mathematically exact because larger context can matter.

Therefore this result should be read as observer-side evidence of operational repertoire drift, not as a claim that a 7-bit patch is a self-contained symbolic operator.

The substrate also still does not deliberately choose among these contexts. The next unresolved boundary is endogenous **selection/use**: whether naturally generated contexts can bias which later interactions actually occur, rather than merely being available to an external assay.
