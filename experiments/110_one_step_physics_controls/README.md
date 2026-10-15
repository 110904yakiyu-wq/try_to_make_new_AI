# Experiment 110 — one-step physical feature controls

## Question

Experiment 108 preserves the active cycle period, exact positions visited
throughout the cycle, phase-0 occupied positions and perturbation protocol.
Experiment 109 found no special excess multi-window causality relative to
a matched-sites randomized donor.

Could the residual connected-cycle persistence association be explained
by simpler physical features of the phase-0 microstate, such as raw bit
density, pairwise bit overlaps or the immediate execution footprint?

## Assay

Reuse the EXACT same 55 G0/control pairs accepted in Experiment 108
(with no re-optimization, no outcome-based selection and no new physics).
Measure each pair's connected-active trial count over 30 injected raw
material conditions. Then filter the matched parents separately by
equality of one observable physical feature:

- total popcount of the phase-0 snapshot;
- sum of bitwise AND popcounts of neighboring windows;
- total bit flips during the first autonomous tick;
- count of changed non-overlapping triples during the first tick;
- EXACT set of changed physical window positions on the first tick.

For each matched-feature stratum, count how many parent pairs favor the
G0 organization, the control, or neither.

## Result

| Equal physical feature | Matched parent pairs | G0 advantage | Control advantage | Ties |
|---|---:|---:|---:|---:|
| Snapshot popcount | 15 | 9 | 2 | 4 |
| Neighboring AND popcount | 20 | 8 | 7 | 5 |
| First-tick bit-flip count | 29 | 16 | 9 | 4 |
| Changed-triple count | 51 | 36 | 10 | 5 |
| Exact first-tick changed-position set | 20 | 9 | 7 | 4 |

The particularly interesting conditional observation is that among
the 20 pairs with exactly the same first-tick changed-position mask,
there is no strong directional persistence advantage (9 vs 7).
But the sample is small and postselected by an intermediate variable.

## Interpretation boundary

This is NOT evidence that first-tick execution masks causally mediate
the persistence effect. Conditioning on a mediator or on a feature
derived from the same microstate can induce selection bias, and the
features are measured retrospectively.

What it does show is that the strong headline 37-vs-11 parent advantage
from Experiment 108 should NOT yet be promoted to a claim about deep
temporal organization: a much simpler immediate physical-response
feature could be implicated, and tighter matching markedly reduces
the apparent directionality.

Window-level contents and full multi-tick phase trajectories still
differ. A complete microstate+phase match would trivially force identical
futures under this deterministic Markov law.

## Reproduce

python experiments/110_one_step_physics_controls/run.py

## Next falsification test

Use a **conditional replacement** of a short causal neighborhood while
holding the initial one-step changed-position mask fixed. Record how
often the perturbation response transfers. Compare against replacements
sampled from the same physical-mask stratum, not against unrestricted
random bit strings.

This might distinguish temporal persistence of coupled activity
from accidental physical microstate regularities without adding a
learner, reward, SELF, reproduction primitive or any new kernel physics.
