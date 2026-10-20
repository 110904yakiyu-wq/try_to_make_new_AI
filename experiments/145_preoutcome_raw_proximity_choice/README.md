# Experiment 145 — Preoutcome raw-bit proximity and spread contrast

## Purpose

Experiment 142 showed that the negative spread association survives two natural pre-outcome selection conventions (first accepted, equal candidate average) but NOT arbitrary post-outcome control choice over 970 eligible states. Here we select one of the same 970 controls per G0 parent on strictly **pre-material physical-state features**: Hamming bit distance, differing 4-bit window count, or popcount discrepancy.

## Frozen contract

- Same original 104/108 kernel, 60 4-bit windows, CENTER30, three-phase left rotation. No new physics, memory, reward or cognitive label.
- Source states: Experiment 140 phase0 G0 frames, Experiment 142 phase0 autonomous eligible controls; 113 of 130 G0 parents have >=1 eligible control under 1000 proposed raw frames/parent.
- Eligibility (period, exact cycle-union support positions, phase0 instantaneous occupancy, phase) is frozen from 139.
- Rank candidates before consulting the material response outcomes: (1) first accepted, (2) minimum XOR bitcount; tie minimum distinct 4-bit windows; tie attempt, (3) maximum bitcount, analogous ties, (4) median bitcount rank, (5) minimum global popcount difference; tie adjacent-AND difference, raw bit distance and attempt.
- Evaluate previously frozen 140 G0 and 142 per-control **all 30 held-out raw boundary-material probes**. Event: cumulative nonzero support visits >=10 or >=60 positions, 50,000-tick observation or certificate by exact recurrence. Censored nonarrivals retain unknown status.
- Aggregate equally across 113 parent clusters; old55 and new58 separately. Controls/probes are repeated dependent measures.

## Observed all-113 result

| Pre-material control choice | Mean G0/control bit distance | G0−control ever-10 difference | Ever-60 difference, censor range |
|---|---:|---:|---:|
| First qualifying candidate | 8.2655 | −12.9499 pp | [−11.6814,−11.6224] pp |
| Minimum bit distance | 4.3717 | −8.5251 pp | −6.9617 pp |
| Minimum popcount difference | 7.0088 | −8.3481 pp | [−7.2566,−7.2271] pp |
| Maximum bit distance | 11.8496 | −12.2124 pp | [−10.2065,−10.1180] pp |

Nearest-bit choice differs from first-choice on **91/113 parents**. All these predeclared selection rules retain negative aggregate event differences, but magnitudes vary. Exactly copying the G0 bit pattern is allowed by the preexisting autonomous matching contract; it is not automatically a nonidentical null. Experiment146 audits identity and tie-break sensitivity.

## Reproduce

```sh
python experiments/145_preoutcome_raw_proximity_choice/run.py \
  --output experiments/145_preoutcome_raw_proximity_choice/results/default.json \
  > experiments/145_preoutcome_raw_proximity_choice/results/default.txt
python experiments/145_preoutcome_raw_proximity_choice/test_smoke.py
```

Python stdlib only. All inputs are committed 139/140/142 records. `results/default.json` retains per-parent choices and all summarized strata. **No unreported simulation is necessary**.

## Interpretation boundary

Raw closeness is observational and not a causal intervention. This is a sensitivity analysis over a highly selected 113-parent population; 17 parents have no eligible control within this proposal budget. Controlling one global distance does not equal controlling all physical spatiotemporal variables. No claim of learned adaptation, SELF, purpose or organization-specific mechanism.
