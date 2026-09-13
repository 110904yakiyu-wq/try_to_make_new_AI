# Theory snapshot 000

Date: 2026-09-14

This note captures the current reasoning before the first implementation. It is deliberately provisional.

## 1. What we are trying not to assume

The current design exercise removes, as cognitive primitives:

- node / edge / graph
- neuron / layer / weight
- explicit state vector
- SELF
- agent/environment partition
- reward / utility
- memory object
- fixed representation language
- fixed meta-level

These may later appear as useful observer descriptions, but they should not be required by the substrate.

## 2. Operational viewpoint

Let `h` denote an executable history. Under finite resource budget `B`, only some continuations/interactions are constructible.

Two candidate processes or effects are provisionally equivalent at history `h` when the currently reachable interactions cannot expose a consequential difference between them within the budget.

This equivalence is not claimed to be absolute. It is capability-relative and history-relative.

A later history may make a previously unavailable distinguishing interaction cheap or constructible, causing a former equivalence class to split.

This gives a possible interpretation of development:

> growth can occur when the same finite hardware becomes capable of constructing interactions that expose distinctions which were previously computationally inaccessible.

## 3. Derived notions under investigation

These are observer-level hypotheses, not substrate primitives.

### Memory

Historical dependence that changes future operational accessibility or equivalence.

### Learning

Persistent, non-trivial change in the operational structure induced by history.

### Understanding

A reduction in the resource cost required to expose consequential distinctions, potentially freeing budget for more complex interactions.

### Selfhood

Not a membership bit. A possible temporary coherence among several operational factorizations, such as ownership-like, agency-like, memory-like, or threat-like relations.

Rubber-hand-style phenomena motivate treating self-attribution as context-local rather than globally binary.

### Metacognition

Not a separate layer. A possible endogenous change in the interactions that determine what the process can operationally distinguish or treat as equivalent.

## 4. Current strongest constraint

Semantic structures should remain soft.

The physical substrate may be fixed because computation requires a floor. However, byte patterns, addresses, opcodes, regions, or other implementation details must not automatically be promoted to cognitive entities.

Physical primitive != cognitive primitive.

## 5. Current implementation question

The candidate substrate is an unsegmented executable medium rather than a pre-partitioned population of agents, nodes, or molecules.

Before implementing it, the remaining design question is:

> What is the minimal execution semantics required for an initially untyped finite medium to produce new operationally distinguishable interactions without predefining program/data/entity boundaries?

The first implementation should be a falsification prototype, not an attempt at general intelligence.
