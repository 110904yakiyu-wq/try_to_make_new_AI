# Experiment 073 — autonomous attractor explanation

## Question

Experiment 072 showed that the K8 block-reversal bias persists for hundreds of autonomous events. Is the apparent memory simply history-dependent selection of different autonomous attractors?

## Assay

Use the standard `Q^8 -> P^8` versus `P^8 -> Q^8` histories with 8 backgrounds, both stateless min/max policies, all six aligned training positions, and all six same-Hamming-weight perturbation pairs.

For each trained state, follow deterministic autonomous K8 dynamics until a state repeats. Record:

- transient length `mu`;
- cycle period;
- a canonical cycle identifier.

Then classify each history pair as entering the same or different eventual cycles.

## Result

Across 576 trained history pairs:

- different eventual cycles: **568/576**
- same eventual cycle: **8/576**
- unresolved: **0**

After 192 autonomous events, recovery bias conditioned on attractor relation was:

### Different-cycle group

- cases: **568**
- recent advantage: **320**
- older advantage: **237**
- ties: **11**
- strict two-sided reversal: **91**

### Same-cycle group

- cases: **8**
- ties: **8/8**
- recent advantage: **0**
- older advantage: **0**

The most common cycle periods are very short (1–3 events), although longer periods also occur.

## Interpretation

This largely explains the extraordinary washout persistence.

The conservative mechanism is:

`experience order -> basin selection -> different limit cycle -> persistent operational hysteresis`

Thus K8 does not need a hidden learning rule to produce the long-lived reversal signal. The finite deterministic substrate simply lands in different attractors.

This is an important negative boundary:

> persistent experience-specific behavior is not sufficient evidence of learning when deterministic basin selection explains it.

K8 remains useful because it demonstrated history-dependent operational contexts and access-cost compression. But its block-reversal effect should not be promoted as adaptive learning.

The next substrate should add a minimal form of **precarious continuation** or turnover so useful organization must be continually regenerated rather than merely frozen into a stable attractor.
