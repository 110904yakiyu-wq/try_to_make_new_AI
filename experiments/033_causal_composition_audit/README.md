# Experiment 033 — causal composition audit

## Question

Experiments 031–032 showed that a small naturally generated local K1 context can causally transfer and recurrently predict a later execution cascade.

Do two such local contexts compose into a joint execution effect that cannot be reduced to either context alone?

## Setup

Use the queue-free K1 substrate and the same equal-budget history family as Experiments 031–032.

For each eligible donor/recipient pair whose future execution traces differ:

1. transplant donor patch `P` at the training site;
2. transplant donor patch `Q` at a second site;
3. transplant both `P+Q`;
4. run the same 32-slot future event budget;
5. compare each trace to the donor trace.

The default patches are radius-2 / 7-bit local contexts and the default second offset is 6 cells, which keeps the two patch windows non-overlapping.

A strict compositional-synergy case requires:

- `P` alone does not reproduce the donor trace;
- `Q` alone does not reproduce the donor trace;
- `P+Q` does reproduce it.

## Result

Default offset 6:

- eligible donor/recipient trace differences: **1312**
- `P` alone exactly reproduced the donor trace: **1156/1312**
- `Q` alone exactly reproduced the donor trace: **11/1312**
- `P+Q` exactly reproduced the donor trace: **1172/1312**
- joint transplant was closer to the donor than both singles: **6/1312**
- strict `P+Q`-only exact synergy: **5/1312**

Additional offsets showed the same qualitative result. For example, strict synergy was 2/1312 at offset 12, 2/1312 at offset 16, and zero at several larger offsets.

## Interpretation

This is a negative/limiting result.

The K1 local execution macro is usually **dominant rather than compositional**: the patch near the interaction site already determines most of the future cascade, and adding a second naturally generated patch rarely creates an execution effect that neither patch can produce alone.

Therefore the project should not claim that K1 has emergent symbolic or program-like composition.

A better reading is:

> K1 supports recurrent, causally effective local execution contexts, but its current dynamics do not provide strong evidence that multiple contexts can combine into qualitatively new executable organization.

## Next question

Can a substrate acquire **distributed causal organization** without hard-coding nodes or symbols?

The next experiment should stop asking whether two preselected patches compose. Instead, perturb several separated regions one at a time and jointly, then search for histories where no single region controls the execution outcome but a distributed set is jointly necessary. If such cases remain rare, K1 should be considered exhausted and the next substrate should permit genuinely relational interactions rather than one-bit local updates.
