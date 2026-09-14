# Experiment 066 — perturbation recovery audit

## Question

Does repeated exposure to a perturbation make K8 selectively better at recovering from that perturbation, without adding reward or a learner?

Two same-Hamming-weight width-3 XOR perturbations `P` and `Q` are used. One state receives repeated P exposure, the matched state repeated Q exposure. Each exposure is followed by the same K8 event budget.

At test time both states are challenged with P and Q separately.

A strict adaptation cross-over would mean:

- P-trained recovers better from P than Q-trained;
- Q-trained recovers better from Q than P-trained.

## Raw-state result

Using Hamming distance from each state's own pre-test bit state after three recovery events, 16 backgrounds produced:

- comparisons: **1152**
- net matching-training advantage: **627**
- net mismatching-training advantage: **437**
- ties: **88**
- strict cross-over: **236**

The raw-state signal survives long autonomous washout periods. With 24 washout events it is still about **607 matching vs 429 mismatching**.

It also weakly transfers spatially, but decays: at a shift of two key windows the raw net advantage is approximately **541 vs 535**, close to null.

At first sight this looks adaptation-like.

## Stronger operational readout

The same assay was repeated using an observer-side operational distance between the pre- and post-test K8 access-cost landscapes:

`E = (first window value, shared field T)`

with penalties for both lost/gained transformation identities and changed minimum closure depths.

Using 8 backgrounds and six autonomous washout events:

- same-position test: **281 matching vs 282 mismatching**
- one-window shift: **286 vs 277**
- two-window shift: **293 vs 282**

These are approximately balanced. The apparent raw-state adaptation disappears under the stronger operational readout.

## Interpretation

This is a corrective negative result.

Repeated perturbation can place deterministic K8 dynamics on trajectories that return closer to their own prior **bit state** after a familiar disturbance. But that does not robustly imply recovery of the same operational capability/cost structure.

Therefore the raw Hamming recovery signal should be treated as attractor/orbit hysteresis, not as evidence of learning.

## Boundary reached

K8 now has strong evidence for:

- history dependence;
- reusable operational context;
- operational coarse-graining across different micro-contexts;
- history-dependent possibility/cost landscapes.

It still lacks robust evidence for:

- selective learning from repetition;
- consequence-driven operational adaptation;
- stable experience-specific compilation.

The next substrate should couple continuation or persistence to **operational consequences**, not merely to repetition, raw trace deposition, or bit-state return.
