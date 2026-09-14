# Experiment 062 — global access-cost landscape

## Question

Experiment 059–061 showed that a history-generated local context can reduce the scan cost needed to reach a particular K8 transformation role.

Does history reorganize the **global access-cost landscape** of the medium, rather than only isolated local contexts?

For a trained state `h`, define the observer-side transformation identity

`E = (first window value, shared field T)`

and its access cost

`C_h(E) = minimum self-delimiting closure depth over all starts that realize E`.

No cost is optimized internally by the substrate. This is an external assay.

## Setup

- K8 self-delimiting substrate from Experiment 057
- six key-width windows of ring capacity
- equal-budget histories `A,A,A,B,B` and `B,B,A,A,A`
- fixed event budget `3`
- `128` deterministic random backgrounds
- both `min` and `max` stateless event policies
- all training positions aligned to key width
- all four width-3 complement-pair representatives

For each history pair, compare:

1. which transformation identities `E` are reachable;
2. the minimum access cost for identities reachable in both histories;
3. whether the reachable identity sets are exactly equal but the cost map differs.

## Result

Each key width produced **6144 equal-budget history comparisons**.

### key width 3

- same reachable identity set: **123/6144**
- identical full cost map: **112/6144**
- at least one common identity with a different cost: **2933/6144**
- common reachable identities: **8477**
- common identities whose minimum cost differs: **5046/8477 = 59.52%**
- same identity set but reorganized cost map: **11**
  - seq1 cost-dominates: **7**
  - seq2 cost-dominates: **4**
  - incomparable pure cost reorganization: **0**

### key width 4

- same reachable identity set: **134/6144**
- identical full cost map: **133/6144**
- at least one common identity with a different cost: **831/6144**
- common reachable identities: **3500**
- common identities whose minimum cost differs: **1084/3500 = 30.97%**
- same identity set but reorganized cost map: **1**
  - seq1 cost-dominates: **1**

## Interpretation boundary

K8 does not usually preserve the complete set of available transformation identities while changing only their costs.

Instead, equal-budget history tends to change both:

- **what transformations are currently reachable**, and
- **how expensive shared transformations are to reach**.

Thus the strongest supported statement is not “learning only changes cost.” It is:

> history reorganizes a coupled possibility/cost landscape under a fixed physical kernel and fixed CPU budget.

The rare cost-only cases show that a pure access-cost deformation is possible, but it is not the dominant regime in this substrate.

## Next question

Does repeated exposure to a particular experience selectively reduce access cost for transformation roles associated with that experience, relative to matched control experiences?

That would be stronger than generic history dependence and closer to experience-specific compilation.