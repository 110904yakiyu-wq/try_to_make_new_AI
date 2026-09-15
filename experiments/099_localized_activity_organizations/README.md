# Experiment 099 — localized activity organizations

## Motivation

Experiments 094–098 showed that the finite-speed mutual-modulation kernel has metastable coarse activity and history-dependent causal cost, but not robust adaptive path compilation.

Before adding more retention machinery, ask a more basic question:

> can the unchanged local kernel generate a bounded, persistent activity organization from a small perturbation of an otherwise quiescent medium?

No object boundary, body variable, lifetime counter, replication rule, reward, or explicit organization type is supplied.

## Substrate

Use the Experiment 093 width-4 local symmetric kernel on a ring of 60 windows.

The all-zero medium is quiescent.

Embed only two adjacent non-zero windows in the center. Exhaust all ordered pairs from values `1..15`, giving **225** possible two-window seeds.

Run the deterministic local dynamics and classify the eventual behavior.

A localized organization is an active cycle whose non-zero support remains bounded to a small part of the 60-window ring. The observed localized cycles have union support at most 13 windows, so the class is separated cleanly from the expanding cases.

## Exhaustive result

For both left-rotation and right-rotation kernels, the aggregate classification is identical:

- localized active organization: **130 / 225**
- quiescent/static outcome: **63 / 225**
- expansive/global outcome: **32 / 225**

The exact seed-by-seed class agrees between left/right rotation for **193 / 225** seeds; the remaining cases exchange localized/quiescent/global behavior symmetrically.

Single-window control:

- all **15 / 15** non-zero one-window seeds become static one-window states;
- sustained localized activity therefore requires relational structure involving at least two adjacent windows in this assay.

## Localized-cycle geometry

Among the 130 left-rotation localized seeds:

Cycle periods:

- period 3: **2**
- period 6: **40**
- period 12: **76**
- period 18: **4**
- period 24: **4**
- period 168: **4**

Union of all non-zero positions visited during one cycle:

- 4 windows: **38**
- 5 windows: **76**
- 8 windows: **4**
- 10 windows: **4**
- 11 windows: **4**
- 13 windows: **4**

Thus most are stationary/breathing local structures rather than a localized pulse that simply travels around the entire ring.

The aggregate 130/63/32 classification is unchanged when ring size is increased from 60 to 90 windows. This rules out dependence on the 60-window circumference for the localized class.

## Perturbation audit

For each localized cycle, choose a phase with maximal non-zero support.

Two one-bit perturbations are tested:

1. flip one bit inside an active non-zero window;
2. add one bit in an immediately adjacent zero boundary window.

After perturbation, run again and classify the eventual organization.

### Exact microcycle return

Return to the exact original state/phase cycle within 1000 ticks is rare:

- internal perturbation: **8 / 130**
- boundary perturbation: **1 / 130**

So these are not rigid error-correcting objects.

### Organization-class persistence

Nevertheless the perturbed system remains in the localized-active class much more often:

- internal perturbation: **104 / 130 = 80.0%**
- boundary perturbation: **124 / 130 = 95.4%**

### Matched local-pattern null

For each perturbed state, preserve the same occupied window positions and the same number of non-zero windows, but replace each occupied window by an independently sampled non-zero 4-bit value.

With one deterministic matched null per organization:

- internal-support null localized: **35 / 130 = 26.9%**
- boundary-support null localized: **31 / 130 = 23.8%**

Therefore the high post-perturbation localization rate is not explained merely by having a small occupied support.

## Interpretation boundary

This is the strongest self-maintenance-like phenomenon in the project so far, but it should be described narrowly.

The useful observation is:

> a purely local finite-speed physical law can generate small bounded activity organizations whose exact microstate is replaceable, yet whose coarse localized-active organization often survives local damage.

That is closer to **metastable organizational persistence** than to memory of an exact state.

It is not yet autopoiesis in a strong theoretical sense, and it is not learning or intelligence.

There is no evidence yet that the organization reconstructs a boundary, reproduces itself, adapts to consequences, or selects its own perturbations.

## Next question

Can two naturally generated localized organizations interact without an externally supplied object boundary?

The next assay should place two independently valid localized seeds in the same quiescent ring at controlled separations and classify collision outcomes:

- independent coexistence;
- mutual extinction;
- merger into one localized organization;
- expansion/globalization;
- generation of a third persistent organization.

If interactions generate new stable organizations that are not reducible to either isolated seed, this provides a much more natural route toward an ecology than the earlier period-labelled constructions.
