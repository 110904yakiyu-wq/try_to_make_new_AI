# K0 lessons and the next substrate step

Date: 2026-09-14

This is a hobby-project checkpoint, not a formal claim of a new theory.

## What K0 was

K0 used ordinary one-dimensional binary elementary cellular automata as a deliberately austere null substrate.

Hard physical assumptions:

- finite binary ring
- fixed local ECA truth table
- synchronous global update
- finite observation/intervention budget

Intentionally absent as cognitive primitives:

- learner
- reward
- SELF
- memory module
- neural network
- explicit representation language
- meta-level controller
- plastic local rule

## What survived falsification so far

The experiments do **not** establish intelligence, learning, or metacognition.

They do establish several weaker substrate facts under the observer assays used here.

### 1. History can change operational identity under a fixed local law

The same fixed probe family can induce different quotient structures after different histories.

The change can refine, coarsen, or non-monotonically reorganize the quotient.

### 2. Small endogenous local patterns often carry the history effect

A local patch transplanted between histories usually transfers the donor history's operational quotient (Experiment 022).

### 3. The same patch naturally recurs across different histories

A recurrent radius-2 patch predicts the current operational quotient across distinct histories with high accuracy (Experiment 023).

### 4. Recurrent patches also predict future operational dynamics

The same small patch predicts a substantial fraction of the future autonomous quotient trajectory (Experiment 024).

### 5. Some earlier apparent 'new test generation' was only hidden state

When two histories have the same current quotient but diverge later, the divergence is usually already encoded in local microstate inside the current probe light cone (Experiment 025).

This explicitly weakens the earlier interpretation of Experiments 020/021.

### 6. Equal physical interaction budgets can leave different endogenous context repertoires

With the same five interventions, at the same times, using the same pattern multiset, changing only temporal order changes the later recurrent local-context repertoire in a majority of tested cases (Experiment 026).

### 7. The operational repertoire changes too

A substantial subset of those equal-budget histories instantiate different recurrent operational quotient types (Experiment 027).

## What K0 has not shown

The largest missing item is **endogenous selection/use**.

In a synchronous ECA every cell is updated every tick. The substrate does not have to decide, compete, or gate which local interaction receives computational work. Observer-side probes can show that contexts matter, but the physical update schedule itself is independent of those contexts.

Therefore it would be an overclaim to interpret K0 as a system that selects or deliberately uses its emergent contexts.

## K1: minimal change

Do not add a learner, objective, symbolic rule language, SELF, or plastic ECA truth table.

Change only the time/execution semantics.

Candidate K1:

> an asynchronous, event-driven binary ring using the same fixed local ECA truth table.

A site is physically **enabled** when applying the local ECA rule would change its current bit.

Only enabled sites become update events.

After an event changes one bit, only that location and nearby locations need to be reconsidered, so computation can be sparse and CPU-native.

History now changes not only the medium state but also the set of physically enabled future interactions.

This is the first substrate in the project where an analogue of an interaction repertoire exists at the execution layer rather than only in the observer assay.

## K1 falsification question

Before building anything more elaborate, test:

> Can this minimal asynchronous substrate preserve history-dependent recurrent/operational context effects while also producing a history-dependent enabled-event repertoire under equal physical work budgets?

If not, do not add high-level cognition machinery. First determine which additional **physical** degree of freedom is actually necessary.

If yes, only then test whether recurrent contexts causally gate event creation, suppression, and routing.
