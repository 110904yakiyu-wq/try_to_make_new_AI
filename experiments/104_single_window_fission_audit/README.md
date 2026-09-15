# Experiment 104 — single-window fission audit

## Question

Experiment 103 showed externally fed bounded accretion but not autonomous reproduction.

Can one existing bounded organization plus **generic raw material** generate two spatially separated bounded organizations without the experimenter inserting another valid seed?

## Strong fission criterion

Use the 130 G0 localized organizations from Experiment 099.

For each organization:

1. choose a scheduler-phase-0 cycle frame with maximal active support;
2. place exactly one additional non-zero 4-bit window immediately outside the left or right union-support boundary;
3. sweep all raw values `1..15`.

The added one-window material is deliberately weak: Experiment 099 showed that every one-window non-zero seed is static when placed alone in a zero background.

A trial counts as a **strict fission candidate** only when:

1. the eventual cycle has at least two spatially separated non-zero support components;
2. there exists one common phase-0 frame in which both components are present;
3. each component is cut out from that same frame and placed alone in an otherwise-zero ring;
4. at least two extracted components independently converge to active localized cycles.

Thus visual splitting of one pattern is not enough.

## Exhaustive result

Trial count:

- 130 parent organizations
- 2 boundary sides
- 15 raw material values
- **3900 total conditions**

Strict fission candidates:

- **36 / 3900 = 0.923%**

Every successful case produces exactly two independently active daughters, giving **72 daughter organizations**.

## Daughter audit

Across the 72 daughters:

- ring-size-invariant period/support on rings 60, 90, 120: **72 / 72**
- exact match to the original parent microcycle: **0 / 72**
- match to any G0 isolated two-window-seed catalog cycle: **4 / 72**
- absent from the G0 catalog: **68 / 72**

Daughter support sizes:

- 4 windows: **16**
- 5 windows: **16**
- 8 windows: **4**
- 9 windows: **32**
- 10 windows: **4**

Daughter periods:

- 6: **16**
- 9: **4**
- 12: **20**
- 24: **32**

So the strict positive cases really do create two separately viable bounded activity organizations, usually with microcycles not present in the original G0 catalog.

## Matched compact-pattern control

The existence of strict fission cases is not yet evidence that the **organization** caused the fission.

As a control, preserve the same occupied positions as the parent phase frame but replace every occupied window value by an independently sampled non-zero 4-bit value. Keep the same added material position and value.

To keep the control tractable, sample every tenth condition from the 3900-condition sweep, giving **390 matched compact-state trials**.

Strict fission in the matched control:

- **3 / 390 = 0.769%**

Compare with actual:

- actual: 36 / 3900 = 0.923%
- matched compact null: 3 / 390 = 0.769%
- Fisher exact two-sided: **p = 1.0**

There is no evidence in this assay that the pre-existing G0 organization makes strict fission more likely than a compact random non-zero pattern with the same support geometry.

## Interpretation boundary

This experiment therefore gives both a useful positive and a stronger negative.

Positive:

> the local kernel can transform one compact pattern plus one raw non-zero window into two spatially separated, independently persistent bounded activity organizations.

Negative:

> the effect is not detectably specific to the metastable G0 organization class under the present matched control.

The daughters are also not copies of the parent.

Therefore this is **not reproduction, heredity, or organization-driven fission**.

A safer description is **rare nonlinear fragmentation into multiple viable activity organizations**.

## Next question

The missing feature is not the ability to produce multiple viable pieces; the kernel can already do that.

The missing feature is **organization-specific causal control over that production**.

The next assay should therefore avoid inventing a reproduction rule and instead ask whether some naturally generated organization changes the probability or type of daughter outcome under a broad, support-matched perturbation ensemble compared with compact random controls.

If no such organization-conditioned daughter distribution exists, fission should be treated as a generic substrate property rather than a property of the organizations themselves.
