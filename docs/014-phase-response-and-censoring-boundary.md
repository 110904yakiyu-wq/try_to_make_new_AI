# 014 — Persistence audit: cycle censoring vs phase-consistent response geometry

**Audited through Experiment 114.** Frozen Experiment 112 cohort: 130 catalog G0 parents, 55 exact autonomous on-cycle geometry matches, 20 pairs with equal first-tick changed-position mask. Experiment 114 reuses the 20 pairs and the same two-boundary × 15-value material probes, but changes the *observer*, not the physical kernel or intervention.

## Observations

1. Horizon 500 reproduces the 112 outcome panel: 81/600 G0 and 112/600 controls unresolved, 420 jointly resolved, 410 jointly connected, and 10 resolved-class differences.
2. Extending to 2000 ticks resolves only one additional control; 81 G0, 111 controls remain right censored. Of 600 paired conditions, 179 still have at least one unresolved arm. This does not imply eventual nonconvergence, failure, or physical death.
3. For each arm, define a phase-consistent perturbation-response mask by subtracting the arm's *own* no-injection trajectory at the same tick. The two arms' response-position sets coincide in 458/600 at tick 1, 108/600 at tick 3, 71/600 at tick 6, 224/600 at tick 12, and 252/600 at tick 24.
4. Among the 410 conditions that have the same `connected` class at 500 ticks, the tick-6 response mask is equal in only 67. Class equivalence is therefore not a sufficient statistic for detailed causal response geometry, **not** evidence of a special high-level causal primitive.

## Strict interpretation

- The physical evolution is deterministic Markovian when conditioned on complete microstate and scheduler phase. Unequal raw bits are a sufficient *possible* explanation of unequal short-time responses.
- 114 does **not** estimate a causal effect of an emergent organization. Its established contrast is between previously selected G0 and matched controls, not exhaustive physics-feature-matched alternative donors from 113.
- The first-recurrence detector distinguishes a proven finite cycle from unresolved censoring. It cannot certify an infinite nonperiodic future in a finite state space.
- Do not relabel delayed or unresolved trajectories as no survival, no reproduction, adaptation, learning, goals, or SELF.
- The 600 paired probes are repeated measures of 20 parent pairs. Independence at probe level would be a false confidence claim.
- The nonmonotonic mask-similarity fractions at ticks 1–24 reflect phase-consistent dynamics; do not interpret as monotonic degradation or recovery without a causal intervention.

## Next decision boundary

If testing the causal relevance of time-dependent organizations, construct a **preoutcome-matched low-level physical alternative** (e.g., immediate raw bit density/AND/flip and matched early response-mask trajectories) and compare *held-out* later consequences. Report null existence rate, per-parent effects, and separate right-censor fractions. If matching destroys support or yields no differential result, retain the negative result instead of adding a cognitive rule.

**Authority:** `experiments/114_phase_response_censoring_audit/{run.py,test_smoke.py,README.md,results/default.json,results/probes.csv}`. Frozen reference: `experiments/112_probe_discrimination_audit/results/default.json`. No historical science-spec revision and no new physical primitive.
