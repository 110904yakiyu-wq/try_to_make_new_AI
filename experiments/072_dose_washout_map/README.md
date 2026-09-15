# Experiment 072 — block dose and washout map

## Question

Does the K8 block-reversal bias show a clean experience-dose threshold or decay with autonomous washout?

The assay compares `Q^n -> P^n` against `P^n -> Q^n`, with identical perturbation counts and operational recovery tests.

## Dose result

At 16 backgrounds and six autonomous washout events:

- `n=1`: `554 recent / 524 old / 74 ties`
- `n=3`: `615 / 508 / 29`
- `n=5`: `608 / 505 / 39`
- `n=8`: `621 / 485 / 46`
- `n=12`: `635 / 460 / 57`

Longer blocks often strengthen the bias, but the relation is not a clean monotone learning curve and there is no sharp threshold.

## Washout persistence

For 16 backgrounds:

### n = 1

- washout 0: `568 / 514`
- 6: `554 / 524`
- 12: `561 / 518`
- 24: `556 / 515`

### n = 8

- washout 0: `622 / 476`
- 6: `621 / 485`
- 12: `621 / 485`
- 24: `619 / 487`

### n = 12

- washout 0: `626 / 478`
- 6: `635 / 460`
- 12: `639 / 457`
- 24: `642 / 453`

For n=8 with 8 backgrounds, extending washout to 48, 96, and 192 events still leaves approximately `320–322 recent / 234–237 old`.

## Interpretation

The effect does not behave like a decaying short-term memory. It is extremely persistent under deterministic autonomous dynamics.

That persistence motivates a stronger alternative explanation: the two history orders may place the finite K8 medium into different autonomous attractors or limit cycles.

Experiment 073 tests that explanation directly.
