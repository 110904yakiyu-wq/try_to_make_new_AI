# Experiment 070 — spacing and spatial transfer audit

## Question

Experiment 069 showed that the strong K8 recovery bias depends on block-like experience order. Is it merely a fixed-period forcing artifact, and is it confined to the exact training location?

## Irregular temporal spacing

Keep the block order `Q^8 -> P^8` versus `P^8 -> Q^8`, but vary the number of autonomous K8 events after each perturbation.

Using 8 backgrounds:

- constant 3 events: `315 recent / 238 old`
- jitter A `[1,5,2,4,6,1,3,5,2,6,4,1,5,3,2,4]`: `324 / 229`
- jitter B `[6,1,4,2,5,3,1,6,2,4,1,5,3,6,2,4]`: `326 / 230`
- alternating `1,5`: `285 / 238`

Thus the block effect survives strong timing irregularity. It is not explained by a narrow periodic resonance with a fixed 3-event training interval.

## Spatial test shift

Train at one width-3 location, then test at offsets around the 18-bit ring after six washout events.

With 16 backgrounds:

- shift 0: `621 recent / 485 old`
- shift 3: `568 / 545`
- shift 6: `589 / 528`
- shift 9: `572 / 536`
- shift 12: `546 / 557`
- shift 15: `582 / 516`

The bias weakens and can reverse at some offsets, but it does not decay monotonically with distance.

## Interpretation

K8 interactions already scan self-delimiting contexts across the ring, so a simple local-memory interpretation is not appropriate.

The conservative description is:

> block-ordered perturbation history produces a global, position-dependent hysteresis in the operational recovery landscape.

The effect survives irregular temporal spacing but is not schedule-independent and is not spatially uniform.

The next audit should map block length against washout to determine whether there is a genuine dose/persistence regime rather than a single tuned `8+8` condition.
