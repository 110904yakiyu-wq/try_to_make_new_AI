# Experiment 069 — schedule geometry audit

## Question

Experiment 068 found a robust operational recovery bias toward the most recent block in `8 + 8` reversal histories. Is that a generic recency effect, or does it depend on the temporal geometry of the experience schedule?

All comparisons keep the same `8P + 8Q` multiset and compare a schedule ending in `P` against its exact P/Q-swapped counterpart ending in `Q`.

## Irregular equal-count schedule

For the fixed irregular schedule

`PQPQQPPQPQPQQPQP`

and its P/Q swap, with 16 backgrounds:

- recent advantage: **568**
- older advantage: **551**
- ties: **33**
- strict two-sided reversal: **150**

The strong block reversal signal from Experiment 068 is almost gone.

## Random equal-count schedules

Sixteen deterministic random `8P + 8Q` schedules were tested with four backgrounds each.

- schedules with positive recent-minus-old score: **8/16**
- schedules with negative score: **8/16**
- aggregate recent: **2287**
- aggregate old: **2172**

Thus the sign itself depends on schedule structure.

## Training interval mismatch

The block schedule was repeated while changing the number of autonomous K8 events after each training perturbation, while keeping the test recovery horizon fixed at 3 events.

Recent vs old:

- train budget 1: `286 / 267`
- 2: `290 / 265`
- 3: `315 / 238`
- 4: `293 / 257`
- 5: `341 / 205`
- 6: `306 / 235`

The block effect is not a narrow resonance with the 3-event test horizon.

## Final contiguous run length

A deterministic family with exactly `8P + 8Q` was constructed while varying only the final contiguous `P` run from 1 to 8 as much as possible while keeping the prefix alternating.

Recent-minus-old values were:

- run 1: `+13`
- run 2: `-3`
- run 3: `+50`
- run 4: `+69`
- run 5: `+82`
- run 6: `+31`
- run 7: `+98`
- run 8: `+77`

The relation is not monotonic, but longer terminal blocks often strengthen the bias.

## Interpretation

The strongest supported claim is now weaker and cleaner:

> K8 has strong temporal-order hysteresis in its operational recovery landscape, and block-structured histories can produce a recent-experience bias.

What is **not** supported:

- a schedule-independent recency rule;
- generic frequency learning;
- a simple periodic resonance explanation.

The next audit should ask whether the block effect survives when the exact temporal spacing is jittered but a long recent run is retained, and whether it transfers to a different spatial location. If not, the phenomenon is best treated as local dynamical hysteresis rather than learning.
