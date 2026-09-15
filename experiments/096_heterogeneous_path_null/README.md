# Experiment 096 — heterogeneous-path null

## Question

Experiment 095 found that, even after the three-window probe neighborhood is made identical, reproducing a donor's propagation cost often requires transplanting multiple separated remote regions.

Is that distributed support specific to the trained history, or is it a generic property of propagating through a heterogeneous finite-speed medium?

## Null construction

For every trained donor/recipient pair used in Experiment 095:

1. keep the donor state fixed;
2. keep the local three-window probe neighborhood identical;
3. preserve, at every remote position, the exact Hamming distance between donor and recipient window values;
4. replace the recipient's concrete remote value by a randomly sampled value at that same Hamming distance from the donor value.

Thus the null preserves:

- where the two states differ;
- how many bits differ at each position;
- the same local probe state;
- the same finite-speed physical kernel.

It destroys the particular content produced by the shared training histories.

The same three-region donor-transplant assay is then repeated.

## Result

Using 16 backgrounds:

### Distance-6 scalar cost

Trained-history cases: **2468**

- min 1 region: **1010**
- min 2 regions: **697**
- min 3 regions: **761**

Hamming-matched null cases whose cost differs from the donor: **2037**

- min 1 region: **784**
- min 2 regions: **545**
- min 3 regions: **708**

For the 2037 directly paired cases:

- trained required fewer regions than null: **536**
- equal: **983**
- trained required more regions than null: **518**
- mean `trained - null`: **-0.0157 regions**

### Full distance-1..6 profile

Trained-history cases: **3006**

- min 1 region: **306**
- min 2 regions: **645**
- min 3 regions: **2055**

Hamming-matched null cases: **2954**

- min 1 region: **265**
- min 2 regions: **608**
- min 3 regions: **2081**

Paired comparison:

- trained fewer: **471**
- equal: **2058**
- trained more: **425**
- mean `trained - null`: **-0.0227 regions**

## Interpretation

This is an important correction to Experiment 095.

The distributed causal support is real in the narrow physical sense: multiple separated regions can be jointly required to reproduce long-range propagation cost.

But the same phenomenon appears almost unchanged in a control that preserves only distributed raw heterogeneity and removes the trained content.

Therefore the stronger reading is rejected:

> Experiment 095 does **not** yet show that training history created a distinctive distributed operational organization.

The conservative explanation is simpler:

> finite-speed propagation through a heterogeneous medium generically depends on multiple path segments.

This is still useful because it separates two questions that had been conflated:

1. is causality spatially distributed? — yes;
2. is the distributed structure a reusable/history-specific organization? — not shown.

## Next question

A stronger target is use-dependent restructuring rather than mere distributed transmission.

If a path is repeatedly exercised, does the same medium later make that path cheaper to traverse than a matched alternative path, under irregular timing controls that rule out simple phase entrainment?
