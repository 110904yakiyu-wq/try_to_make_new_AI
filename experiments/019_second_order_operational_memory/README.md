# Experiment 019 — second-order operational memory

## Question

Can two histories that are **indistinguishable at the current first-order operational quotient** nevertheless differ in how the *same later intervention* changes that quotient?

If yes, then current operational identity is not a sufficient state description for future operational reorganization. Past history remains latent in the system's future plasticity.

## Three-stage assay

1. **Prior history** — one-shot or repeated exposure to the same width-3 pattern.
2. **Bridge event** — inject exactly the same later width-3 pattern under both prior histories.
3. **Fixed final assay** — measure exact future-effect signatures for all eight candidate probes and construct the operational quotient.

All observer geometry is fixed: locations, times, horizons, sampling positions, and candidate probes.

Crucially, cases are retained only when the quotient immediately before the bridge event is identical under one-shot and repeated prior history.

## Second-order case

A case is counted when:

- pre-bridge first-order quotient is identical under both prior histories, but
- the bridge induces different quotient-transition types (`same`, `refine`, `coarsen`, `reorganize`).

This asks whether past history changes not merely the present quotient, but the **response law of that quotient to a later common event**.

## Result

Second-order cases occur for several fixed ECA rules.

Default counts:

- Rule 14: 8 cases across training patterns `001,010,011,101`
- Rule 113: 9 cases across `001,010,011,101,111`
- Rule 142: 9 cases across `001,010,011,101,111`
- Rule 143: 3 cases across `010,100,110`
- Rule 159: 5 cases across `010,101`
- Rule 226: 1 case across `011`
- Rule 126: 2 cases across `010,011`
- Rule 129: 2 cases across `010,011`
- Rules 98, 110, and 151: none under this particular second-stage geometry

Two qualitatively different effects appear.

### Prior repetition creates sensitivity

Example: Rule 14, train `001`, bridge `010`.

Before the bridge, one-shot and repeated histories have the same quotient. The bridge leaves the one-shot quotient unchanged but strongly coarsens the repeated-history quotient.

### Prior repetition creates resistance

Example: Rule 126, train `010`, bridge `010`.

Before the bridge, both histories have the same fully separated quotient. The bridge coarsens the one-shot history but leaves the repeated-history quotient unchanged.

Rule 129 shows an analogous stabilization effect for a different bridge pattern.

## Interpretation

This is stronger than Experiment 018.

The prior histories can be first-order operationally indistinguishable under the current assay while remaining distinguishable by a **test of how they change under a future intervention**.

In that precise observer-level sense, history is stored not only in present response classes but in the system's future capacity to reorganize those classes.

This resembles "plasticity of plasticity" or a meta-state, but those terms are deliberately not promoted to substrate primitives. There is still no mutable learning rule, meta-layer, reward, SELF variable, or explicit state abstraction in the CA.

This is also not yet metacognition: the bridge and final assay are externally supplied. The next boundary is to ask whether the substrate can generate the bridge-like operation from its own ongoing dynamics and thereby expose or exploit these second-order distinctions without an external experimenter selecting the intervention.
