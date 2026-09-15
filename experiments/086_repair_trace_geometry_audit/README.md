# Experiment 086 — repair-trace geometry audit

## Question

Experiment 085 showed that generic replication reinforces the substrate's existing p2 prior rather than internalizing the E3-selected p3 organization.

A more consequence-coupled mechanism is to retain context only after a real disturbance is actually repaired.

One unbiased turnover mutation is applied, the repetition dynamics attempt to repair it, and only when the disturbed site is restored to its pre-mutation symbol is a local raw context copied forward.

Does this produce environment-selected retention without secretly encoding the target organization in the trace geometry?

## Setup

- 120-symbol ring, 8 exchangeable symbols
- initial state: pure p2
- one unbiased turnover mutation per sweep
- mutation occurs before the repair sweep
- if the mutated site is restored, copy a raw context of length `L` ending at the repaired site to the immediately following `L` sites
- E3 is present for 300 sweeps, then removed for 300 sweeps
- 16 seeds
- observer readout: minimal p3 coverage in the last 100 sweeps before and after E3 removal

No p2/p3 label is used by the trace rule. However, `L` is a physical geometry parameter and therefore must be audited.

## Trace-length sweep

| L | p3 before E3 removal | p3 after E3 removal |
|---:|---:|---:|
| 2 | 1.213750 | 0.008750 |
| 3 | 10.948750 | 0.186250 |
| 4 | 1.034375 | 0.001875 |
| 5 | 1.593125 | 0.000000 |
| 6 | 5.656250 | **2.628125** |
| 7 | 1.025000 | 0.000000 |
| 8 | 1.514375 | 0.000000 |
| 9 | 5.551875 | 0.000000 |
| 10 | 0.990000 | 0.042500 |

Only `L=6` produces substantial post-environment persistence.

## Environment controls for L=6

With the same repair-trace rule active for all 600 sweeps:

- no environment: late p3 = **0.000000**
- E2: late p3 = **0.000000**
- E3: late p3 = **3.865000**

So the trace rule does not simply manufacture p3 by itself. E3 still matters.

## Critical audit

`L=6` is exactly two period-3 blocks.

That means the positive retention result is geometrically resonant with the observer-defined p3 organization. The mechanism contains no explicit `p3` label, but the physical trace span supplies a hidden structural prior that is unusually well matched to p3.

Therefore the correct interpretation is not "the medium learned E3".

It is:

`environment-conditioned selection + target-compatible trace geometry -> post-environment persistence`

This is useful but still too engineered.

## Boundary

Consequence coupling alone is not enough if the retention channel has a privileged scale that matches the organization being tested.

The next kernel should avoid a fixed trace length. The size of what is retained must be derived from the actual repair event itself, or otherwise be scale-free / self-delimiting.
