# Experiment 007 — response geometry modulation

Rule 129 showed repetition-dependent effects that transfer away from the training site.

The next failure mode is simple pair-specific residue: perhaps the medium only changes how it reacts to the two patterns used during exposure.

## Question

Does repeated A/B history change the response to **probe patterns that were never used during exposure**?

## Setup

- physical rule: ECA Rule 129
- training patterns: A=`011`, B=`101`
- compare one-shot exposure with repeated exposure
- probe at offset 20 from the training position
- probe every possible 3-bit pattern `000..111`
- average across many training positions

For each probe `p`, define the A-vs-B history modulation:

`Delta(p) = impact_Atrained(p) - impact_Btrained(p)`

Then define the repetition-induced geometry change:

`G(p) = Delta_repeat(p) - Delta_single(p)`

If `G(p)` is nonzero only for A and B, the effect is pair-specific.

If many untrained probes also change, repeated history has modified a broader map from possible interventions to future consequences.

## Interpretation

This is still not learning. A deterministic propagated phase/domain pattern can alter the response geometry without any internal objective or adaptation mechanism.

The point is only to test whether history changes a broad operational relation rather than storing a literal familiar-pattern residue.
