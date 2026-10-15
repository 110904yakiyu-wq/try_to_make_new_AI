# Experiment 115 — Early-response-equivalent physical controls on held-out probes

## Question

Experiment 114 found that the 20 exact-geometry/first-mask-matched G0-parent pairs often have different short-time physical perturbation responses despite arriving at the same coarse cycle class. Does a G0-patch response-transfer advantage survive after constructing *distinct physically matched bit controls* whose early response on a **fixed six-probe training panel** agrees with that patch?

This is a test of an observer-defined response organization, not a test for a learning rule, SELF, reproduction or independent cognitive causation.

## Frozen contract

- Same `104` local three-phase mutual-modulation kernel (`SIZE=60`, 4-bit windows, left rotation, `CENTER=30`, phase 0), same **112** frozen roster of 20 parent/control pairs. Controls are reconstructed from the historical accepted attempt number and verified against frozen seed, support and first-tick mask. Do not reselect on outcomes.
- Same 1-, 2- and 3-window G0-to-control transplants as 113; keep only those with the original exact first-autonomous-tick changed-position mask.
- Exhaustive **strongest 113 physical null**: all nonzero changed-site bit assignments different from the recipient at each changed site, excluding the identical transplanted G0 patch, subject to the same first-tick mask, total popcount, adjacent AND popcount and first-tick Hamming flip count. Null existence is decided before material outcomes.
- **Training inputs**: left/right boundary raw values `{1,7,15}` (six probes). A causal response at tick `t` is the set of window positions whose 4-bit values differ from the same arm's own no-injection trajectory at equal scheduler phase. Two non-adaptive training gates are evaluated: all six causal-position masks equal donor-transplant at tick **1**; and equal donor-transplant at ticks **1 and 3**. The unrestricted physically matched tier is the baseline.
- **Held-out inputs**: the 12 remaining raw values `{2,3,4,5,6,8,9,10,11,12,13,14}` at each boundary (**24 probes**). These are never used for null eligibility. Report mask Jaccard and exact-mask agreement with the original G0 parent at ticks **6, 12, 24**. Compare transplanted G0 patch to the exact uniform expectation over eligible alternative nulls; average patches **within parent**, then average eligible parents equally. All outputs are deterministic and finite-horizon.
- A separate **secondary** 500-tick class outcome uses only held-out reference keys where frozen 112 G0 and control are both resolved but differ. Those reference discrepancies were measured in **prior** experiments; this is retrospective selection and not prospective validation. Censored interventions are unconfirmed and reported separately; no timeouts are treated as deaths or negative persistence.
- Neither full microstate nor bit-level response trajectory is matched across the controls. The training masks are a low-dimensional coarse quotient; a residual difference can be ordinary unmodeled nonlinear bit physics.

## Reproduced main result

| Transplant width | Full physical matching: patches / parents / alternatives | Same train tick-1 masks: patches / parents / alternatives | Same train tick-1 and tick-3 masks |
|---:|---:|---:|---:|
| 1 | 23 / 15 / 33 | 12 / 10 / 16 | **0** |
| 2 | 14 / 10 / 59 | 9 / 8 / 32 | **0** |
| 3 | 20 / 16 / 414 | 20 / 16 / 392 | **0** |

The donor mask-conserving inventory is unchanged from 113: **35 / 16 / 20** patches. Full physical null eligibility is also unchanged (**23 / 14 / 20**). **No distinct null** satisfies all six response position masks at **both** ticks 1 and 3 while retaining those physical constraints. This is a measured positivity/support failure, not a zero treatment effect. In particular, it does *not* establish a special temporal mechanism.

Held-out tick-24 mask Jaccard with the *original* G0 parent (parent-weighted; donor and null compared on identical tier-eligible patches):

| Width | Null gate | Parents | G0-transplant | Physical-null expectation | Donor minus null | Parent wins/losses/ties |
|---:|---|---:|---:|---:|---:|---|
| 1 | physical | 15 | 0.52125 | 0.50117 | +0.02007 | 9 / 6 / 0 |
| 1 | train tick 1 | 10 | 0.52096 | 0.55417 | **-0.03321** | 4 / 6 / 0 |
| 2 | physical | 10 | 0.50308 | 0.42459 | +0.07849 | 5 / 5 / 0 |
| 2 | train tick 1 | 8 | 0.45491 | 0.46213 | **-0.00722** | 4 / 4 / 0 |
| 3 | physical | 16 | 0.49206 | 0.33535 | +0.15671 | 9 / 7 / 0 |
| 3 | train tick 1 | 16 | 0.49206 | 0.33361 | **+0.15845** | 9 / 7 / 0 |

The positive width-3 difference persists after the tick-1 gate, but the 9-to-7 parent win/loss count and unequal bit-level residuals provide **no reliable evidence** for organization-specific temporal causal structure. The original G0 parent is naturally closer in raw contents to its exact transplanted patch than to most alternative patches, a basic possible explanation. Width-1 and width-2 show no donor advantage under the tick-1 gate. Estimates across gates have different eligible parent/patch populations; naive row subtraction is not mediation analysis.

### Secondary class and censoring (retrospective)

The held-out 500-tick resolved reference-class-disagreement keys are exceptionally few (8 across 6 parents, excluding the two historical `{1,7,15}` training-panel disagreements). In the tick-1 gate, evaluable **parents** are 3 / 2 / 4 for widths 1 / 2 / 3. Parent-weighted confirmed class-match contrasts are **+0.08333 / -0.08333 / +0.01452** respectively, and are not decisive. The null censored-application counts refer to enumerated microstate×probe applications, while donor counts refer to donor patch×probe applications; do **not** compare their raw magnitudes as though the denominators match.

The tick-1+tick-3 gate has no admissible controls and hence no held-out comparison. Neither physical match nor same response positions at tick 1 means exact response values, phase trajectory or future dynamics are equal.

## Reproduce

From repo root, Python standard library only:

```sh
python experiments/115_heldout_temporal_response_audit/run.py \
  --reference experiments/112_probe_discrimination_audit/results/default.json \
  --output experiments/115_heldout_temporal_response_audit/results/default.json \
  > experiments/115_heldout_temporal_response_audit/results/default.txt
python experiments/115_heldout_temporal_response_audit/test_smoke.py
```

The locally executed verification used a reduced copy containing only the exact 20 verified 112 cohort entries and the ten published resolved class-disagreement keys; `run.py` uses the *full frozen 112 archive* on GitHub and verifies its pairing metadata. The reduced local test source is not committed. No fabricated physical measurements or unexecuted result numbers appear in the archived files.

The checked-in `default.json` includes all 57 feature-qualified patch records, tier-specific null cardinalities, parent-weighted summaries and censoring counts; `default.txt` is the summary extract. Compare source code and results using `test_smoke.py`. Provenance references: `104`, `108`, `112`, `113` and `114` published main-branch files.

## Interpretation and next falsification

The strongest early-response gate is **not evaluable** due to zero distinct nulls. The tick-1 gate leaves enough nulls for a descriptive, lower-resolution held-out study but no stable width-independent donor advantage. Do not call this autonomous behavior, learning, or a temporal grammar. A useful next control is to measure exact *minimum early-response distance* in the 113 physical null sets, rather than requiring strict 6-probe equality at both ticks, and then compare later held-out predictive performance at fixed common-support strata. This would investigate a graded approximation without adding physics or covertly using held-out outcomes for matching.
