# Experiment 056 — strict K7 second-order arity audit

## Question

Does K7 show evidence that history changes the **law by which the current variable-arity grammar responds to the same next physical interaction**, or is the apparent second-order effect only a consequence of using a coarse grammar description?

## Two observation levels

The assay is run twice.

### 1. Coarse arity repertoire

Observe only the set of currently executable arities, e.g. `{2,3}`.

### 2. Full relation repertoire

Observe every currently executable abstract relation type `(arity, sorted content multiset)`.

For each observation level:

1. retain equal-budget history pairs with equal current repertoire;
2. write the same width-3 bridge at the same position;
3. require the repertoires to remain equal immediately after the bridge;
4. require the next selected physical event to have exactly the same positions and window contents;
5. execute exactly one event;
6. test whether the repertoires diverge.

## Result

### Coarse arity-only observation

- initial equal-repertoire history pairs: **147**
- bridge trials: **1176**
- repertoire still equal after bridge: **793**
- exact same next physical event: **8**
- post-event arity-repertoire divergence: **2/8**

So a weak second-order-looking signal exists if grammar is represented only by the currently available arity set.

### Full relation repertoire

- initial equal-repertoire history pairs: **2**
- bridge trials: **16**
- repertoire still equal after bridge: **1**
- exact same next physical event: **1**
- post-event repertoire divergence: **0/1**

The signal disappears under the stronger current-grammar description in this default sweep.

## Interpretation

The 2/8 coarse result should **not** be read as a history-conditioned change of microphysical law.

A more economical explanation is that the arity-only observable discards current microstate/relation information. Two states can look identical under that coarse grammar while still containing different latent physical structure that becomes visible after the same event.

This reproduces the lesson from Experiment 053 in a variable-arity substrate:

> second-order effective-law change is representation- and resource-relative; it is not evidence that the deterministic kernel itself changed.

## No-go boundary exposed by this experiment

For a fixed deterministic kernel, once the complete current physical state is specified, earlier history has no independent causal channel into the next state. Any history effect must be encoded in the current state.

Therefore the project's target cannot literally be "microphysical law changes while the complete state is fixed" unless the kernel itself becomes part of the mutable state.

The useful target is instead a **resource-bounded effective transformation grammar** whose coarse operational transition structure changes with history even though the underlying physical law remains fixed.

## Next move

Before inventing another substrate, audit a separate hidden assumption in K7: every event currently relies on a global combinatorial search over all non-overlapping subsets. That search is an oracle-like scheduler primitive and is poorly aligned with the CPU-first motivation.

The next substrate should make interaction span/arity self-delimiting from local sequential content rather than found by global subset enumeration.
