# Experiment 066 — perturbation recovery audit

## Question

Does repeated exposure to a perturbation make K8 selectively better at recovering from that perturbation, without adding reward or a learner?

Two same-Hamming-weight width-3 XOR perturbations `P` and `Q` are used. One state receives repeated P exposure, the matched state repeated Q exposure. Each exposure is followed by the same K8 event budget.

At test time both states are challenged with P and Q separately.

A strict adaptation cross-over would mean:

- P-trained recovers better from P than Q-trained;
- Q-trained recovers better from Q than P-trained.

## Raw-state result

Using Hamming distance from each state's own pre-test bit state after three recovery events, 16 backgrounds and five training exposures produced:

- comparisons: **1152**
- net matching-training advantage: **627**
- net mismatching-training advantage: **437**
- ties: **88**
- strict cross-over: **236**

The raw-state signal survives long autonomous washout periods. With 24 washout events it is still about **607 matching vs 429 mismatching**.

It also weakly transfers spatially, but decays: at a shift of two key windows the raw net advantage is approximately **541 vs 535**, close to null.

## Stronger operational readout at one dose

The same assay was repeated using an observer-side operational distance between the pre- and post-test K8 access-cost landscapes:

`E = (first window value, shared field T)`

with penalties for both lost/gained transformation identities and changed minimum closure depths.

At the original **five-exposure, six-washout** condition and 8 backgrounds:

- same-position test: **281 matching vs 282 mismatching**
- one-window shift: **286 vs 277**
- two-window shift: **293 vs 282**

So the raw-state signal does **not** imply operational adaptation at this particular dose/washout condition.

## Important correction

A later dose sweep showed that this null is **condition-specific**, not a global negative result.

At higher repeated-exposure counts (especially 8–12), the same operational metric develops a clear matching-experience advantage that survives several washout events. That phenomenon is separated into Experiment 068 rather than retrofitted into this experiment.

Therefore Experiment 066 supports only the narrower statement:

> apparent raw-state adaptation can be misleading, and operational adaptation must be assayed directly; five exposures are insufficient under the tested six-event washout condition.

It does **not** support the stronger statement that K8 can never develop perturbation-specific operational adaptation.
