# 048 — Response-mask matching on disjoint probe panels further reduces spread differences

**Experiment 148** selects one control per parent from the same 970 eligible autonomous period/support/phase0-matched controls (113/130 G0 catalogue parents). Original 60×4-bit / three-phase / bit-rotate-left kernel is unchanged.

Selection only uses *six* training probes: raw bit values 1,7,15 at the left and right sides of the original union support. For each physically available state, evolve the injected and its own noninjected phase-aligned trajectories; compute 60-position difference masks at ticks 1,3,6. Select controls with minimum G0/control symmetric response-mask distance on 1 / (1,3) / (1,3,6), tie by raw-bit distance, differing window count, accepted proposal attempt. Exactly **24 other side/raw combinations per parent remain held out**. None of their 50,000-tick eventual spread events or recurrence statuses is consulted when selecting the comparator.

On 113 parents, 24 heldout probes per arm (2712 each): the frozen first-choice control has G0−control ever10 spread −12.28 pp and censor-aware ever60 difference [−10.62,−10.58] pp. Matching all three time slices on the training probes reduces the contrasts to **−3.72 pp** (ever10) and **−3.13 pp** (ever60). This is consistent with an important explanatory role for low-level physical response geometry but not a causal mediation proof. All results are correlated evaluations of the same 113 parent microstates and all 970 alternatives; probe splits do not create independent parent groups. Training response is an experimentally induced physical measurement rather than a new learner or memory primitive.

**Do not infer** a novel abstract self-preservation code, history-only dependence beyond deterministic microstate+phase, reward learning, reproduction, heredity, or cognition. Prior Exp142 result that arbitrary eligible control choice can cross zero remains authoritative. Extrapolation to all 130 parents is unsupported while 17 have no eligible control.

Authority: `experiments/148_train_probe_matched_spread_holdout/`, and frozen 139/140/142 (plus 145/147 selection benchmarks).
