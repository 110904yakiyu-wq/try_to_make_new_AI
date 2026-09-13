# Experiment 000 — CA null substrate

This is the first executable falsification toy.

It does **not** try to build intelligence.

## Question

Can a fixed minimal local medium produce new naturally encountered contexts that refine an observer-defined operational equivalence relation, without changing the underlying physical rule?

## Substrate

- 1-D binary circular cellular automaton
- Rule 110
- no agent boundary
- no reward
- no memory object
- no learning rule
- no program/data distinction

## Observer assay

The observer considers all 3-bit core patterns as candidate local patterns.

A context is a pair of left/right flanks actually encountered in the CA history around some location. Contexts are collected in order of first appearance, up to a fixed repertoire budget.

For a candidate core and a context:

1. Insert the core between the encountered left/right flanks.
2. Evolve the resulting finite local field with Rule 110 for a short horizon.
3. Observe only the center bit at the horizon.

Two cores are provisionally operationally equivalent when every currently available context gives the same observed outcome.

This equivalence belongs to the **observer assay**, not to the CA itself.

## Default seed

A single `1` in a ring of `0`s.

This intentionally starts with a restricted context repertoire. As the CA evolves, new local arrangements may appear.

## What counts as the minimum positive result

At an earlier checkpoint, at least one pair of core patterns belongs to the same equivalence class.

At a later checkpoint, a newly encountered context splits that class.

Expected form:

`a ~_early b`

but later

`a !~_late b`

## What this does NOT show

A positive result is not evidence for:

- intelligence
- learning in the ordinary ML sense
- selfhood
- open-ended evolution
- autonomous concept formation

It only verifies that a fixed low-level rule can support a history-dependent expansion of the observer's operational discrimination repertoire.

## Next question if this works

Can previously expensive distinctions become cheap because reusable structures have formed, under the **same fixed resource budget**?

That is the more important experiment.
