# Experiment 089 — operational-role environmental filtering audit

## Question

Experiments 083–087 used explicit period-2 / period-3 observer categories. Even though the kernel did not contain semantic labels, the experiment family still revolved around a privileged periodicity ontology.

Can environment-conditioned filtering be seen instead in K8's own self-delimiting operational roles?

## Operational role

For every K8 closure available at a state, define the observer-side role

`R = (first window value, shared field T, closure depth)`.

This is the same finite-resource operational family used in the K8 access-cost experiments. It is not stored in the substrate.

## Assay

- binary ring: 24 bits
- K8 window width: 4 bits
- 32 random initial backgrounds
- min and max K8 event-selection policies
- settle each background for three K8 events
- create every single-bit variant
- retain only variants that create at least one new operational role relative to the settled parent
- compare the same variant for six K8/environment steps under two value-blind environments:
  - `L3`: rotate every 3-bit block left by one bit
  - `R3`: rotate every 3-bit block right by one bit

L3 and R3 have the same block size and differ only in orientation. This avoids the large gross persistence difference seen when comparing different block sizes.

Total variant cases with at least one novel role: **1312**.

## Gross survival

Mean fraction of variant-created roles still present after six steps:

- L3: **0.027614**
- R3: **0.032834**

Variant-level comparison:

- L3 preserves more: **91**
- R3 preserves more: **100**
- tie: **1121**

There is no strong global environmental preference.

## Role-specific audit

Across the assay there are **383** distinct operational roles. Restricting to roles observed in at least 20 independent variant cases leaves **84** roles.

Observed role-specific statistics:

- maximum absolute L3-vs-R3 survival difference: **0.192308**
- occurrence-weighted RMS role difference: **0.049982**

A structure-preserving null independently swaps L3/R3 labels at the whole-variant-case level, preserving correlations among all roles created by the same micro-variant.

Using 1000 null permutations:

- max-difference empirical p: **0.065**
- weighted-RMS empirical p: **0.407**

The strongest individual-looking role is therefore only borderline under the multiple-role search, and the aggregate role structure is fully compatible with the null.

## Interpretation

This is a negative result.

Removing the p2/p3 ontology does not automatically reveal a robust environment-specific operational selection law in single K8 variants.

The environment certainly changes trajectories, but under this assay we do not have strong evidence that recurring operational role classes are being differentially retained in a reproducible way.

Therefore:

`environmental perturbation of K8 trajectories != operational-role ecology`

## Next

A single variant followed by one global K8 event stream is probably the wrong level for ecological selection.

The next substrate should let many self-delimiting K8 contexts coexist and update in parallel within the same medium. Then we can measure birth, death, recurrence, invasion, and environmental filtering of operational roles without predefining organism boundaries.