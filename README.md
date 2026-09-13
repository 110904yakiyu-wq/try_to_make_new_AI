# try_to_make_new_AI

A public hobby repository for experimenting with alternative computational foundations for AI.

This is intentionally **not** being treated as a formal research repository. Failed ideas, discarded abstractions, toy implementations, and negative results are welcome here. Git history is part of the experiment log.

## Current direction

The working idea is to avoid assuming standard cognitive primitives such as:

- neural networks, neurons, nodes, edges, or layers
- a fixed agent/environment boundary
- an explicit SELF variable
- a fixed reward or objective function
- a dedicated memory module
- a dedicated meta-cognitive layer

Instead, we are exploring whether such notions can emerge as observer-level descriptions of a finite, history-dependent computational process.

Current theoretical focus:

1. Start from finite executable histories rather than predefined cognitive entities.
2. Treat operational equivalence as capability-relative: two processes are effectively identical when the current system has no affordable interaction that distinguishes them.
3. Let the repertoire of constructible interactions change with history.
4. Treat memory, learning, selfhood, and meta-level behavior as possible derived phenomena rather than built-in modules.
5. Keep semantic assumptions soft; only the physical computational substrate is allowed to be hard.
6. Prefer sparse, event-driven, CPU-native computation if that falls out naturally from the model.

## Working style

- Keep commits small and hypothesis-oriented.
- Preserve failed experiments when they teach us something.
- Do not optimize for a polished architecture too early.
- Distinguish observer metrics from internal objectives.
- Before adding a primitive, ask whether it is computationally necessary or merely a cognitive assumption smuggled in by the designer.

## Status

Pre-v0 substrate design / falsification stage.

The next milestone is to specify the smallest executable substrate that can test whether history can change the set of operational distinctions available under a fixed finite resource budget.
