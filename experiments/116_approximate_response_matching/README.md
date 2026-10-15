# Experiment 116 — Approximate early-response matching

## Question

Experiment 115 found zero distinct fully physics-matched controls reproducing the donor transplant's complete train-probe response-position masks at both ticks 1 and 3. Does a *bounded* mismatch permit nontrivial controls, and do early-response-nearest controls explain held-out responses without invoking an emergent temporal mechanism?

## Frozen conditions

- Unchanged local 4-bit 60-window, CENTER=30, 3-phase, left-rotation kernel from 104. No new physical/cognitive primitive.
- Same 112's 20 parent pairs selected without injected outcomes using exact cycle/support/phase and first-tick changed-site matching. Same 113's strongest exact null conditions: original changed positions, nonzero raw bits, same first unperturbed changed mask, total popcount, neighbor AND sum and first-tick Hamming flips, excluding exact G0 donor-patch assignment.
- Enumerate **all 506** alternate microstates in 57 mask-and-feature-qualified patches (width 1/2/3: 33/59/414 controls in 23/14/20 patches). No random sampling error in null pool.
- Train only on **6 probes** (raw 1,7,15 on each of left/right) at ticks 1 and 3. For each probe/tick, compare response-position mask of candidate against the actual transplanted G0-patch organization. Sum the integer Hamming bit counts across all 12 snapshots. These are spatial window *position* differences, not raw 4-bit Hamming distance.
- Before looking at heldout metrics, take nearest 1 (lexicographic deterministic tie), nearest 3, or all alternatives within predeclared distances <=4/8/16/32/64; separately analyze exact tick-1 train mask equality and the unrestricted physical pool. **Do not compare summary rows with unequal eligible parent populations as if a single causal contrast.**
- Test **24 distinct probes** (12 untrained raw values × two boundaries) at ticks 6,12,24; evaluate Jaccard and exact response-position mask similarity to the original G0 parent. Aggregate patch scores within parent, then mean equally over eligible parents. Only 20 parent-pair clusters; patches/null candidates/probes are repeated measures.

## Results

| Width | Qualified patches | Full-physics null states | min train distance, median across patches | patches with distance <=4 | <=8 |
|---|---:|---:|---:|---:|---:|
| 1 | 23 | 33 | 5 | 10 | 22 |
| 2 | 14 | 59 | 4 | 10 | 13 |
| 3 | 20 | 414 | 2.5 | 16 | 20 |

No control has train-t1,t3 distance **zero**, confirming the Experiment 115 empty-exact-match boundary. Yet all 57 patches have alternatives with at most 16 position disagreements across 12 early response snapshots. This mismatch should not be interpreted as a physical law of increasing complexity.

The main diagnostic held-out tick-24 Jaccard **donor minus physical control** result:

| Width | All qualified controls, parent mean | Nearest-1 control, parent mean | Parent wins / losses (nearest) |
|---|---:|---:|---:|
| 1 | +0.02007 | +0.00980 | 9 / 6 |
| 2 | +0.07849 | **−0.01112** | 4 / 6 |
| 3 | +0.15671 | **+0.13116** | 11 / 5 |

Nearest-1 comparisons reuse the exact same physical-eligible patches as the all-null row, so the change is due to early-trace conditioning rather than lost patch eligibility. The effect is non-monotonic across width and not evidence of an independent temporal organization variable. The nearest-1 null is a *minimum-score candidate*, not an independent random sample and not a matched population with balanced propensity.

Additional threshold tables, parent details, and exact similarity metrics live in the canonical result JSON. Multiple thresholds are a sensitivity analysis; no threshold was optimized on held-out outcomes.

## Reproduction

From repository root:

```sh
python experiments/116_approximate_response_matching/run.py --output experiments/116_approximate_response_matching/results/default.json > experiments/116_approximate_response_matching/results/default.txt
python experiments/116_approximate_response_matching/test_smoke.py
```

Python standard library only. The full default JSON includes all 57 patch-level inventories, distance distributions and parent-level contrasts; the text file is the readable summary. No retrospective mutation of experiments 104–115.

## Interpretation

The observed small-early-distance pool demonstrates approximate physical null support where complete early equality was infeasible. That alone cannot distinguish *ordinary microstate-dependent nonlinear propagation* from a temporally organized effective quotient. A sensible next falsification is to rotate the held-out raw-probe split rather than promote a single train-set result.
