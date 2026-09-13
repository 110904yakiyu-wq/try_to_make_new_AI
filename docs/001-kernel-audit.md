# Kernel audit 001

Date: 2026-09-14

This note records the last abstraction pass before the first executable toy experiment.

## Goal

Use the smallest practical computational substrate that does **not** hard-code cognitive entities such as agents, nodes, memories, goals, self models, or meta-layers.

The substrate may still have physical primitives. The rule is:

> physical primitive != cognitive primitive

## Candidates considered

### A. Self-interpreting instruction machine

Pros:
- easy to make code self-modifying
- easy to run on a CPU

Rejected for experiment 000 because it hard-codes too much structure too early:
- program counter
- instruction boundaries
- operand roles
- opcode semantics

### B. Reflective rewrite / artificial chemistry

Pros:
- program/data distinctions can be softened
- rewrite rules can become data
- good route toward self-reference

Not selected for experiment 000 because most practical versions still predefine entities, molecules, terms, ports, or explicit rewrite objects.

### C. Fixed local cellular medium

Selected as the null substrate.

Use a finite one-dimensional binary cellular automaton with a fixed local transition law. Cells, adjacency, time, and the transition law are treated as physical implementation primitives only. They are not interpreted as neurons, concepts, agents, or cognitive nodes.

Rule 110 is useful here because an elementary 1-D binary local rule is known to be computationally universal (Matthew Cook, 2004), while universality by itself is clearly not sufficient for open-ended evolution or intelligence.

References:
- Matthew Cook, "Universality in Elementary Cellular Automata", Complex Systems 15(1), 2004.
- Hiroki Sayama et al., "Self-Reproduction and Evolution in Cellular Automata: 25 Years After Evoloops", Artificial Life 31(1), 2025.

## Kernel K0

Let the physical medium be

`M_t in {0,1}^N`

with circular boundary conditions.

Each position is updated synchronously from radius-1 neighbors using Rule 110:

- 111 -> 0
- 110 -> 1
- 101 -> 1
- 100 -> 0
- 011 -> 1
- 010 -> 1
- 001 -> 1
- 000 -> 0

No other semantics are supplied.

There is no built-in:

- object boundary
- program/data boundary
- SELF
- agent/environment boundary
- reward
- memory module
- learning rule
- representation layer
- meta-controller

## Why this is deliberately too weak

Experiment 000 is not an attempt to create intelligence.

It asks a smaller question:

> Can a fixed, unsegmented, finite local medium generate newly available interaction contexts that refine an observer-defined operational equivalence relation over time?

If even this minimal effect cannot be demonstrated cleanly, richer claims should not be built on top of the substrate.

## Observer versus system

The system itself has no objective and does not compute operational equivalence.

The observer is allowed to measure:

- naturally encountered local contexts
- bounded interventions
- future consequences under those contexts
- quotient classes induced by indistinguishability under the currently available context repertoire

Observer metrics are not internal objectives.

## Experiment 000 criterion

At checkpoint `t1`, two candidate local patterns may be operationally equivalent under every naturally encountered context currently available to the assay.

At a later checkpoint `t2`, a context that first becomes available through the medium's own history may distinguish them.

The minimal observation is therefore:

`a ~_t1 b` but `a !~_t2 b`

This is not evidence of cognition. It only validates that the measurement language can track history-dependent refinement of operational identity without changing the physical rule.

## Decision

Kernel audit 001 passes for a falsification prototype.

The next step is implementation, but only as `experiment-000`: a null-substrate assay. The CA is not being proposed as the final AI architecture.
