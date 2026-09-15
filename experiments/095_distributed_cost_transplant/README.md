# Experiment 095 — distributed propagation-cost transplant

## Question

Experiment 094 showed that equal-budget history can change the finite-speed cost for the same local probe to reach distant locations.

Is that cost difference controlled by one small local patch, as in K1, or by a distributed organization spread through the medium?

## Strong local control

After training two histories with the same intervention multiset but different order:

- `A,A,B,B,A`
- `B,B,A,A,A`

force the three windows around the probe site to be **identical in both histories** before testing:

- left neighbor = the original background value;
- probe window = the same final `A` value;
- right neighbor = the original background value.

Therefore any remaining propagation-cost difference must be carried outside the immediate three-window neighborhood.

## Remote regions

The other nine windows are divided into three non-overlapping three-window regions at relative offsets:

- `R1 = {+2,+3,+4}`
- `R2 = {+5,+6,+7}`
- `R3 = {+8,+9,+10}`

For every donor/recipient pair with a different probe response, exhaustively transplant all non-empty subsets of donor remote regions into the recipient.

Record the minimum number of remote regions required to reproduce either:

1. the donor's scalar arrival cost at maximum ring distance 6;
2. the full arrival-cost profile for distances 1 through 6.

No local probe-region information is transplanted because it has already been made identical.

## Result

32 deterministic backgrounds × two rotation orientations × 12 probe locations × eight complement-pair representatives were tested.

### Distance-6 scalar cost

Cases where donor and recipient costs differ after local canonicalization: **4951**.

Minimum remote support required to reproduce the donor cost:

- one region: **2074** (41.89%)
- two regions: **1374** (27.75%)
- all three regions: **1503** (30.36%)

Thus **2877/4951 = 58.11%** cannot be reduced to one remote region.

### Full propagation-cost profile

Cases with a different distance-1..6 cost profile: **6022**.

Minimum remote support required:

- one region: **594** (9.86%)
- two regions: **1284** (21.32%)
- all three regions: **4144** (68.81%)

Thus **5428/6022 = 90.14%** require more than one remote region.

## Interpretation boundary

This is substantially different from the K1 distributed-causality audit, where 1179 of 1181 reproducible execution differences were transferable with one local region.

The conservative claim here is:

> after the local probe neighborhood has been made physically identical, history-dependent finite-speed propagation cost is often jointly controlled by multiple separated remote regions.

This is evidence for **distributed causal support** under this assay.

It is not yet evidence for a persistent object, representation, self, or learned distributed code.

A remaining objection is important: any finite-speed path through a heterogeneous medium can require several segments to reproduce. The next experiment should therefore compare these trained-history pairs against controls with similarly distributed raw differences but no shared training history. The question is whether training creates a distinctive causal organization, rather than merely a generic heterogeneous transmission path.
