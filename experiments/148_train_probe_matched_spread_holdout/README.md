# Experiment 148 — Train-probe-matched controls versus heldout spread

## Question

Experiment147 matched **unperturbed** early autonomous orbit snapshots and reduced, but did not eliminate, the spread contrast. Can predeclared **short-time perturbation response geometry** select closer physical controls while preserving an unobserved raw-material evaluation panel?

## Exact intervention and separation

- Frozen 104/139 physics: a 60-window ring of 4-bit values, CENTER30, left bit rotation, scheduler phase0/1/2. No learner, reward, SELF, special memory register, or new rule.
- Frozen 139 pool: 970 pre-material eligible controls over 113 parents, with equal autonomous cycle period, exact union-support locations, phase0 occupancy and scheduler phase.
- **Train side/raw conditions:** left/right x {1,7,15}, exactly **6**. At raw injection time 0, compare each organism's material-injected trajectory to its *own no-injection trajectory* at ticks 1,3,6 (phase-aligned physical times). Form a 60-position response bitset for each. Match the G0 responses to each control's responses by minimizing summed position-mask symmetric difference over the six training conditions at predeclared tick sets {1}, {1,3}, {1,3,6}. Tie-break by raw-bit XOR Hamming distance, differing 4-bit windows, then acceptance attempt.
- **Heldout side/raw conditions:** left/right x the 12 raw values other than {1,7,15}: exactly **24** per parent. None is used by the control selector. Evaluate frozen Exp140 G0 and Exp142 control histories only on those heldout conditions. Report ever-10 and ever-60 cumulative reached ring positions by 50,000 ticks, with exact recurrence certificates and separate censoring.
- Compare with first-accepted and tick0 raw-bit-nearest baselines, *on the identical heldout 24 probes*; don't compare percentages to prior 30-probe denominators without disclosing this change.

## Results: matched 113-parent cohort (24 heldout probes per arm)

| Pre-material control choice | G0−control ever10 | G0−control ever60 |
|---|---:|---:|
| First accepted autonomous control | −12.28 pp | [−10.62,−10.58] pp |
| Minimum tick0 raw-bit distance | −7.30 pp | −5.57 pp |
| Training response mask tick1 | −8.41 pp | −6.71 pp |
| Training response mask ticks1,3 | −7.37 pp | −5.94 pp |
| Training response mask ticks1,3,6 | **−3.72 pp** | **−3.13 pp** |

The most constrained training response selection differs from first-choice in **95/113 parents**, although only five selected parent-control pairs have exactly equal response masks on both training ticks 1 and 3. Effects remain negative in both separately monitored groups (original 55 and new 58) but do **not** identify a new causal mechanism. Train/test probes are disjoint but measured on the same correlated parent material and related physical state. A negative spread difference can be entirely ordinary nonlinear bit-level physics.

## Reproduce

```sh
python experiments/148_train_probe_matched_spread_holdout/run.py \
  > experiments/148_train_probe_matched_spread_holdout/results/default.txt
python experiments/148_train_probe_matched_spread_holdout/test_smoke.py
```

Standard library only. `results/default.json` retains all selected attempts and every parent-cluster heldout count. Inputs are committed Exp140 and Exp142 prequalified control states and material response traces. No new 50,000-tick experiment is run: the **new experimental act is constructing a predeclared selection rule and evaluating its disjoint heldout inputs** on frozen source observations.

## Limits

Selection compares perturbation response shapes, not merely raw physical state; near-zero response difference is much stronger conditioning than autonomous phase0 matching. No evidence this residual represents self-maintenance, learning, adapted behavior, goals, a special dynamical code, or intelligence. The 113/130 match eligibility and previous Exp142 unconstrained eligible-choice envelope crossing zero still limit inference.
