# Experiment 114 — Phase-consistent response trace and censoring audit

## Question

Experiment 113 showed that bit-density and other immediate physical-feature matching substantially changes a tiny-sample response-transfer contrast. Does the remaining apparent persistence difference reflect (a) delayed cycle identification beyond 500 ticks, or (b) divergent phase-consistent raw response trajectories hidden by the observer's `connected` class?

**Scope:** This is a measurement audit of the **frozen 112 20-parent cohort**, not a new matched-null causal intervention on the 113 transplanted patches. It cannot establish temporal organizational autonomy.

## Fixed physical and sample contracts

- Historical `104` kernel: 60 ring windows of 4 bits, `CENTER=30`, phase 0, **left** bit rotation, simultaneous triplet updates, 3-phase scheduler. No change to physics or cognitive primitives.
- Same `108` controls selected from preintervention autonomous cycles, period + exact union-support positions + phase-zero occupancy matched; `112` fixed first autonomous changed-position mask equality. Frozen 20 pairs from `experiments/112_probe_discrimination_audit/results/default.json`.
- Same fixed 30 material probes per pair: 15 nonzero 4-bit raw values, each injected immediately outside left/right union support. There are 600 paired probes but **20 independent parent clusters**.
- At horizons **100, 250, 500, 1000, 2000 ticks**, determine whether each orbit has already exhibited an exact recurrence in the key `(full 60-window physical microstate, next scheduler phase)`. `first_recurrence` is the first recurrence time, not an estimated relaxation constant.
- An unresolved trajectory is **right censored**, not static, inactive, dead, or an absence of reproduction. Activity classes refer to resolved cycles only; no isolated daughter viability tested.
- Compare at absolute ticks **1, 3, 6, 12, 24**, always starting the autonomous baseline and raw-injected trajectories at identical scheduler phase 0. At each tick, form `R(t) = {i | injected_state_i(t) != no_injection_state_i(t)}` for each individual arm, and compare the response *position masks* across G0 and matched control. Also record Jaccard similarity and relative Hamming bit-response counts.
- These observer differences are purely deterministic perturbation-response diagnostics. Distinct 4-bit contents can give distinct response masks under the same fixed law, even when an eventual coarse class is equal.

## Results

The 500-tick outcome audit **exactly reproduces** Experiment 112 on the same 20 parent pairs: 81 G0 and 112 control censored, 420 jointly resolved, 410 jointly connected, 10 jointly resolved class disagreements. This is an integrity check, not independent evidence.

| Horizon | G0 censored | Control censored | Both resolved | Both connected | Resolved class differences |
|---|---:|---:|---:|---:|---:|
| 100 | 93 | 127 | 398 | 391 | 7 |
| 250 | 81 | 112 | 420 | 410 | 10 |
| 500 | 81 | 112 | 420 | 410 | 10 |
| 1000 | 81 | 111 | 421 | 411 | 10 |
| 2000 | 81 | 111 | 421 | 411 | 10 |

Only **one** previously censored control response reaches a cycle in ticks 501–2000 (in fact by 1000); no new G0 response converges. Thus at horizon 2000, **179 of 600 pairs** still have at least one censored arm. Horizon-extension sensitivity is highly limited over this range; later resolution cannot be ruled out.

| Tick | G0/control equal causal-response position mask | Count of 600 | Parent-mean Jaccard |
|---|---:|---:|---:|
| 1 | 76.33% | 458 | 0.8822 |
| 3 | 18.00% | 108 | 0.5669 |
| 6 | 11.83% | 71 | 0.4499 |
| 12 | 37.33% | 224 | 0.5633 |
| 24 | 42.00% | 252 | 0.5773 |

Since all parents receive exactly 30 probes, these are both probe-frequency fractions and parent-weighted averages; they are not 600 independent replicates.

Of the **410** paired probes resolved as connected in *both* arms at tick 500, only **67** share the same causal-response location mask at tick 6 (**16.34%**). There is no paradox: class equivalence is much coarser than equality of short-time physical responses, and different baseline microstates need not evolve the same way. Mask agreement is also weaker than exact bit-response agreement.

## Inference boundary

1. **No support for a new physical primitive** or an inserted learning/goal/reproduction mechanism.
2. Neither a 500-tick `connected` class nor its 2000-tick extension identifies a unique short-time trajectory or organizational cause.
3. G0 and control differ in raw 4-bit content, and the matching was selected from only 20/130 parents. The observed response-mask divergence **does not imply organization-specific distributed causality**. It could be entirely ordinary nonlinear bit-level dynamics.
4. This 114 assay does **not** retest 113's exhaustive feature-matched transplanted-patch contrasts; the causal bit-content mechanism remains unproven.
5. The censored group cannot be treated as failed persistence. Long periods and transients past 2000 ticks may exist.
6. All probes within a parent remain dependent. Report parent-level metrics; avoid naive binomial confidence intervals over 600 observations.

## Reproduce

From the repository root (Python standard library only):

```bash
python experiments/114_phase_response_censoring_audit/run.py \
  --output experiments/114_phase_response_censoring_audit/results/default.json \
  --csv experiments/114_phase_response_censoring_audit/results/probes.csv \
  > experiments/114_phase_response_censoring_audit/results/default.txt
python experiments/114_phase_response_censoring_audit/test_smoke.py
```

`default.json` is the complete deterministic parent-level summary; `probes.csv` retains the full 600 paired probe observations (censor status at 500/2000, recurrence times, period, support hash, and time-slice response indicators). The script checks the historical 112 outcome totals, and, when the full historical archive is available as in the repository, checks each 500-tick class/period/support record against that source.

Execution for this commit was performed using a faithful local copy of the published `104`/`108` core step/orbit/matching functions and the frozen `112` 20-entry eligibility metadata; historical 112 aggregate outcomes were recovered exactly, and three selected 108 controls were independently confirmed to be the first accepted candidates. The checked-in runner imports the existing repository source files directly.

## Follow-on recommendation

First establish whether low-level physical baselines (raw bit density/AND and matching short-time bit-response features) already account for this mask divergence. A useful next *causal* study would condition on those features **before** evaluating probe outcomes, with explicit eligibility and censoring, rather than reifying a temporal observer quotient as a new physical variable.
