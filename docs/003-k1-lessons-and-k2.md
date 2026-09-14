# K1 lessons and K2 candidate

Date: 2026-09-14

## K1 conclusion

K1 changed K0's synchronous ECA into a queue-free/event-driven physical substrate while keeping the same binary ring and local truth table.

What survived strict audits:

- equal-budget history changes the set of currently enabled physical events;
- this remains true with stateless scheduling, so it is not merely queue memory;
- small naturally generated local contexts can causally transfer later event cascades;
- the same contexts recur across different histories and strongly predict the same later cascade.

What failed:

- strong compositionality is rare;
- distributed causal control is rare;
- among donor cascades reproducible from four candidate regions, almost every case is reproduced by one local region alone.

So K1 is best understood as a history-sensitive local execution medium, not yet as fluid distributed organization.

## Why not add a learner

The failure is structural, not an optimization failure.

Adding a reward, learned gate, SELF state, explicit memory, or neural controller would answer a different question and would reintroduce cognitive assumptions that this project is deliberately trying to avoid.

The next substrate should instead change the physical interaction topology.

## K2 requirement

K2 should allow **who can interact with whom** to arise from the current medium and to disappear again after interaction.

Constraints:

- no persistent graph / edge table;
- no semantic node type;
- no external reward or objective;
- no dedicated memory;
- no learned scheduler;
- finite CPU-native execution;
- interaction eligibility must be recomputed from current physical content.

## Candidate: unsegmented rendezvous ring

Use one circular bit medium.

At any instant, every fixed-width local window is only a physical substring, not a cognitive object.

Two non-overlapping locations are temporarily related when their current key windows satisfy the same minimal physical matching rule. The relation is not stored. It exists only because the current bits make the pair eligible.

An interaction rewrites small neighborhoods around both matched locations. Therefore the interaction can:

- destroy the relation that enabled it;
- create a new matching relation elsewhere;
- change which future nonlocal interactions are executable.

A stateless scheduler selects one currently eligible rendezvous under a fixed finite event budget.

## Why this is different from K1

K1 has a fixed one-dimensional neighborhood graph. History can gate local execution, but the possible interaction partners are always the same immediate spatial neighbors.

K2 keeps the physical bit ring but makes executable nonlocal relations content-dependent.

The target phenomenon is therefore no longer only:

`history -> local state -> enabled local update`

but:

`history -> medium content -> temporary relation topology -> execution -> new relation topology`

## First falsification test

Do not test intelligence.

Test whether equal-budget histories with the same intervention multiset but different order produce different recurrent rendezvous repertoires and whether transplanting the small physical neighborhoods that support one rendezvous can causally transfer part of the later nonlocal interaction cascade.

If K2 immediately collapses again to one dominant local patch, the rendezvous rule is too weak and should be discarded.
