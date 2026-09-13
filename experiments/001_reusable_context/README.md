# Experiment 001 — reusable context

Experiment 000 only showed that newly encountered contexts can refine an observer-defined operational quotient.

That is too weak. A one-off context is not interesting enough.

## Question

Can a context that did not exist in the initial repertoire:

1. appear later through the substrate's own dynamics,
2. distinguish patterns that were initially operationally equivalent, and
3. reappear at multiple later times so that the distinction is reusable?

## Observer-only definition

Take the operational equivalence relation induced by contexts available at `t = 0`.

For every later naturally encountered context `c`, measure:

- `split_gain(c)`: how many initially equivalent core pairs are distinguished by `c`;
- `occurrences(c)`: how many times `c` appears in the run;
- `distinct_times(c)`: how many different timesteps contain `c`;
- `first_seen(c)`: when it first appeared.

A provisional **reusable discriminator** is a later context with:

- `split_gain > 0`
- `distinct_times >= 2`

This name is purely an observer description. The CA does not know the score and does not optimize it.

## Why this is still weak

Even a positive result can be caused by ordinary recurring Rule 110 structures. It does not imply learning.

The next stronger question is whether a reusable structure makes a distinction **cheaper under a fixed resource budget**, rather than merely recurring.
