# Experiment 004 — ECA rule sweep

Experiment 003 was negative for Rule 110 under one simple experience-specific response assay.

That does **not** justify adding a plasticity mechanism yet. Rule 110 may simply be a poor physical law for this phenomenon.

Elementary 1-D binary radius-1 cellular automata have only 256 possible rules, so sweep all of them first.

## Question

Can a completely fixed local rule show a persistent difference between:

- one exposure to a pattern, and
- repeated exposure to the same pattern,

when later tested using the symmetric A/B cross-over probe from experiment 003?

## Metric

For each rule compute:

- `single_score`: cross-over familiarity score after schedule `[0]`
- `repeat_score`: cross-over familiarity score after schedule `[0,4,8,12,16]`
- `repetition_gain = repeat_score - single_score`

The sweep ranks rules by `abs(repetition_gain)`.

This is an observer metric only. Rules are not trained or selected during a run.

## Interpretation

A large repetition gain does not prove learning. It can arise from persistent phase changes or other ordinary state dynamics.

The purpose is to answer a narrower design question:

> Do we need to add mutable transition laws just to obtain repeat-count-dependent persistent behavior?

If some fixed rules already do this, keep the physical kernel fixed and investigate the emergent mechanism before adding more substrate machinery.
