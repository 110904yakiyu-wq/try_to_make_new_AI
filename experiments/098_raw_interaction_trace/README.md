# Experiment 098 — raw interaction trace

## Question

Experiment 097 found no timing-robust use-dependent path compilation in the finite-speed mutual-modulation kernel.

Can the smallest possible physical trace of actual interaction create such an effect without adding reward, success labels, path identity, counters, or a separate memory store?

## Trace rule

Keep the Experiment 093 local three-window update.

For every active triple, compute the raw change masks:

`dx = X XOR X'`

`dy = Y XOR Y'`

`dz = Z XOR Z'`

and define one trace value

`T = dx XOR dy XOR dz`.

After the parallel triple updates, XOR `T` into the first window of the immediately adjacent next triple.

The deposited value is ordinary medium content. It is not tagged as memory and is processed by the same physical update law on later ticks.

This is deliberately only one predeclared trace formula; no trace-function search is used to find a favorable result.

## Assay

Repeat the source-path cross-over test from Experiment 097 with 12 source uses and irregular timing schedules.

64 backgrounds, two rotation orientations, 12 source positions.

### Jitter schedule A

`1,4,2,5,3,6,1,4,2,5,3,6`

- matching cheaper: **850**
- mismatching cheaper: **865**
- tie: **1357**
- strict two-sided cross-over: **111**

### Jitter schedule B

`2,5,1,6,3,4,2,5,1,6,3,4`

- matching cheaper: **846**
- mismatching cheaper: **817**
- tie: **1409**
- strict two-sided cross-over: **108**

For comparison, the trace-free kernel in Experiment 097 produced schedule-sensitive signs rather than a consistent matching advantage.

## Interpretation

The generic raw interaction trace does not create robust use-dependent path compilation.

It greatly increases ties and changes the propagation dynamics, but it does not make the exercised source consistently cheaper across timing schedules.

Therefore:

> leaving an unlabelled physical residue of interaction is not, by itself, sufficient to turn history-dependent causal cost into adaptive cost reduction.

This is another negative against the idea that generic memory/retention alone is the missing primitive.

## Consequence

The next useful direction should not search over trace formulas.

The unresolved issue is **consequence**: a trace can persist, but nothing makes traces that preserve ongoing organization physically different from traces that do not.

A minimal next audit should therefore introduce precariousness without a reward scalar: inactive local material should be subject to unbiased turnover while currently participating material is temporarily protected. Then test whether self-maintaining activity organizations emerge and whether environmental perturbations reshape them.
