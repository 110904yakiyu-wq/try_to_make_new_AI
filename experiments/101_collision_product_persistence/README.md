# Experiment 101 — collision-product persistence

## Question

Experiment 100 showed that collisions between naturally generated localized organizations can produce new localized microcycles absent from the complete isolated two-window-seed catalog.

Are those collision products themselves metastable organizations, or merely fragile one-off collision residues?

## Setup

Use the 102 novel localized products created by identical-parent collisions at separation 3 under the left-rotation width-4 kernel.

For each product, choose a phase of its eventual cycle with maximal non-zero support.

Apply the same two damage classes used in Experiment 099:

1. flip one bit inside an active window;
2. add one bit to an immediately adjacent zero boundary window.

Then evolve autonomously and classify the resulting long-run behavior.

Two observables are kept separate:

- return to the exact original collision-product microcycle;
- persistence of the broader `localized active` organization class.

## Matched null

For each damaged state, preserve:

- exactly the same occupied window positions;
- exactly the same number of non-zero windows.

Replace the contents of every occupied window by independently sampled non-zero 4-bit values.

Run ten deterministic matched-null realizations per product and damage class.

This asks whether persistence is explained merely by retaining a small occupied patch.

## Result

### Actual collision products

Across 102 products:

- internal one-bit damage remains localized active: **73 / 102 = 71.6%**
- boundary one-bit addition remains localized active: **98 / 102 = 96.1%**

Exact return to the original product microcycle:

- internal damage: **0 / 102**
- boundary damage: **0 / 102**

The aggregate actual-damage counts are exactly the same under the right-rotation kernel.

### Matched local-pattern null

Across 1020 null realizations per damage class:

- internal-support null remains localized active: **99 / 1020 = 9.7%**
- boundary-support null remains localized active: **77 / 1020 = 7.5%**

## Interpretation

The collision products behave much more like the metastable organizations of Experiment 099 than like brittle transient residues.

The important feature is again **organization-class persistence without microstate restoration**:

> after local damage, the exact collision-generated cycle is typically lost, but a bounded persistent activity organization often remains.

This is especially strong for boundary perturbations.

The matched-null control makes it unlikely that the result is explained only by the damaged state remaining spatially compact.

## Comparison with first-generation organizations

Experiment 099 first-generation organizations showed:

- internal-damage localized persistence: 80.0%
- boundary-damage localized persistence: 95.4%

The collision products show:

- internal: 71.6%
- boundary: 96.1%

So second-generation collision products retain broadly comparable coarse persistence even though their exact microcycles are absent from the first-generation isolated-seed catalog.

## Claim boundary

This is still not reproduction or heredity.

The collision product is not shown to make a copy of itself, and the coarse `localized active` class is observer-defined.

The useful narrow result is:

> organization-changing collisions can create new bounded persistent activity organizations that themselves survive local perturbation far above matched compact-pattern controls.

## Next question

Can a collision-generated organization participate in another collision and create yet another persistent organization?

If so, the relevant state space is no longer just a fixed first-generation catalog. The next experiment should therefore test **second-generation interaction chains** and classify whether localized products can recursively participate in further organization-changing collisions.
