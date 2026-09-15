# Experiment 103 — bounded accretion audit

## Why this audit exists

Experiment 102 used the Experiment-099 convenience threshold `cycle union support <= 13 windows` as the label `localized`.

That threshold was safe for the original two-window-seed catalog because the observed classes separated cleanly there, but it is **not** a physical definition of localization.

Collision products can be larger than every G0 organization while still remaining spatially bounded.

This experiment therefore re-audits the apparent `expansive_cycle` outcomes using ring-size scaling instead of the fixed 13-window threshold.

## Corrected boundedness test

Take a cycle frame at scheduler phase 0 and embed the same finite non-zero pattern into rings of:

- 60 windows;
- 90 windows;
- 120 windows.

A collision product is treated as bounded for this audit when cycle period and cycle-union support remain unchanged across all three ring sizes.

### Result

The 70 `G2 + parent` collision outcomes that Experiment 102 split into:

- 38 `localized` cases;
- 32 `expansive_cycle` cases;

are in fact **70 / 70 ring-size-invariant bounded cycles**.

They form two families:

- 38 cycles: period **6**, support **13** windows;
- 32 cycles: period **12**, support **14** windows.

The 38 next-stage cycles previously labelled `expansive_cycle` are also bounded:

- period **6**;
- support **16** windows;
- exactly the same period/support on rings 60, 90, and 120.

Therefore Experiment 102's statement that the bounded chain necessarily terminates at that step was too strong.

## Continued accretion

Follow the 38 period-6 branch.

After another adjacent parent collision the bounded cycle has support **19** windows.

Re-center that finite pattern in a 120-window quiescent ring and continue adding the same G0 parent at the nearest phase-compatible side, alternating sides.

Across all 38 chains the support sequence is exactly:

`19 -> 22 -> 25 -> 28 -> 31 -> 34`

for the six audited stages.

The period remains **6** throughout.

A representative chain was extended further to support **49** windows with the same period-6 behavior.

So collision products can support repeated bounded **accretion** rather than terminating after a few generations.

## Is that open-ended novelty?

No.

Measure the number of distinct local motifs occurring anywhere in one full cycle.

Across all 38 period-6 chains from support 19 through support 34:

- distinct 3-window motifs: **12 at every stage**;
- distinct 5-window motifs: **28 at every stage**;
- distinct 7-window motifs: **48 at support 19, then 50 from support 22 onward**.

For every one of the 38 chains, the 3-window and 5-window repertoires are already completely saturated before the audited growth sequence. The 7-window repertoire changes once and then saturates as well.

Thus the collision chain adds spatial extent without continuing to add local organizational grammar.

The conservative description is:

> the local kernel supports persistent, externally fed growth by repeated accretion, but the tested growth becomes structurally repetitive rather than open-ended.

## Important correction to Experiment 102

The raw label `expansive_cycle` in Experiment 102 should be read as:

> cycle support exceeded the old 13-window convenience threshold.

It should **not** be read as evidence that the organization spread through the ring.

Experiment 103 supersedes that interpretation.

## Claim boundary

This is not autonomous growth.

The experimenter repeatedly supplies another parent organization at a neighboring site. No substrate process seeks material, copies itself, or chooses when to accrete.

It is also not open-ended evolution: local motif diversity saturates quickly while size continues increasing.

The useful result is narrower:

- localized collision products remain causally usable;
- repeated interactions can enlarge one persistent organization;
- boundedness survives larger physical domains;
- but size growth and organizational novelty are distinct, and the present kernel mainly provides the former.

## Next question

The next useful target is **endogenous fission / reproduction**, not longer externally fed chains.

Can one bounded organization, after receiving generic material or perturbation, generate two spatially separated bounded organizations without an experimenter placing a second valid seed?

That would test whether organizational persistence can begin to create its own future interaction partners rather than merely absorb externally supplied ones.
