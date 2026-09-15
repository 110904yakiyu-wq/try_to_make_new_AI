# Experiment 074 — minimal precarious-turnover K9

## Question

K8 stores long-lived history largely through deterministic basin selection. Does adding the weakest possible form of structural precariousness improve schedule-independent operational adaptation?

## K9 physical change

K9 keeps K8's self-delimiting interaction unchanged and adds one rule:

- after each event, deterministically flip one currently nonparticipating bit;
- if no event exists, flip one deterministic bit so no state is perfectly absorbing;
- store no age, reward, fitness, lifetime, or activity counter.

The intent is simply that unused structure cannot remain perfectly frozen forever.

## Result

With 16 deterministic backgrounds and six washout events:

### Block reversal

- cases: **1152**
- recent advantage: **575**
- older advantage: **564**
- ties: **13**
- strict two-sided reversal: **222**

### Irregular equal-count schedule

- cases: **1152**
- recent advantage: **582**
- older advantage: **554**
- ties: **16**
- strict two-sided reversal: **226**

These are close to balanced.

## Autonomous dynamics

In a 4-background cycle audit, all 576 sampled trained states still entered deterministic cycles. The period distribution broadened relative to K8:

- period 2: 261
- period 4: 196
- period 8: 52
- period 24: 42
- period 6: 20
- period 89: 3

So one-bit turnover disrupts K8's very short attractors but does not eliminate attractor dynamics.

## Interpretation

Minimal precariousness alone is insufficient.

It weakens K8's strong block hysteresis but does not produce robust schedule-independent experience-specific operational recovery.

Therefore do **not** tune the turnover rate to search for a favorable parameter.

The next justified addition, if any, must create a mechanism by which organization that actively participates in ongoing interaction can be **regenerated**, not merely protected by passive decay. This moves toward selection/replicator dynamics and must be treated as such rather than advertised as spontaneous intelligence.
