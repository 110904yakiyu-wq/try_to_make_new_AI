# Experiment 147 — Autonomous temporal proximity selection, held-out material response

## Design

Select one of the original 970 qualified controls per matched parent using the **no-injection**, phase-aligned physical evolution at ticks 0/1/3/6/12. Predeclared distances sum per-window 4-bit XOR bitcounts against the G0 autonomous state at equal absolute tick and scheduler phase. No material probe outcomes enter the candidate selection. Ties use tick-0 bit distance, then window mismatch count, then accepted proposal index. Evaluate the exact **same** 30 held-out material probes already archived in Experiment 140/142. The physical kernel is unchanged; these are deterministic observational comparisons.

Five predeclared selection rules: raw0, [0,3], [0,3,6], [0,1,3,6,12], [3,6,12]. `raw0` reproduces Experiment145's minimum raw bit distance convention *exactly*. Include all 113 parents and separately examine old55/new58; results are not independent sample replications.

## Result: 113 parent groups

| Autonomous states used to rank eligible controls | G0−control ever10 | G0−control ever60 |
|---|---:|---:|
| Tick0 alone | −8.53 pp | −6.96 pp |
| 0,3 | −8.11 pp | −6.84 pp |
| 0,3,6 | **−7.67 pp** | **−6.55 pp** |
| 0,1,3,6,12 | −8.32 pp | −6.99 pp |
| 3,6,12 | −7.67 pp | −6.55 pp |

At all five preoutcome selection rules, the finite time ever10 sign is negative and the censor-aware eventual ever60 contrast upper bound is also negative. No additional long-horizon simulation was needed; Exp140/142 stored all held-out probes. The near-time selection choice changes 17–21 controls relative to tick0-only ranking. No monotonic gain in response matching with more autonomous time slices is established.

## Reproduce

```sh
python experiments/147_phase_aligned_autonomous_proximity/run.py \
 > experiments/147_phase_aligned_autonomous_proximity/results/default.txt
python experiments/147_phase_aligned_autonomous_proximity/test_smoke.py
```

Standard library only; `run.py` imports the original phase0 three-phase 60x4-bit step exposed in Experiment139. Default JSON contains per-parent selected candidate attempts, selection distances, spread response outcomes and full cluster summaries.

## Interpretation

Distance between finite no-injection trajectories does not identify a unique organization-level temporal causal code. Full physical microstates differ (except the one exact G0 duplicate from Exp146). Outcome-blind selection does not eliminate residual raw-bit motifs, spatial interactions, proposal-selection bias, or the 17 unmatched parents. No learning, goals, reproduction or SELF demonstrated.
