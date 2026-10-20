# Experiment 157 — Two externally scheduled experiences and nontrivial boundary-XOR probe

## Question

Does delivering two externally scripted experiences yield a heldout *functional locality improvement*, compared against no pulse, each constituent single pulse, opposite order and simultaneous delivery? Use the same original G0 130-parent catalogue and physical law as 156; **do not make a learning claim from history-dependent physical change**.

## Protocol

- Same frozen 60 × 4-bit, CENTER30, left-rotation phase0/1/2 104/139 kernel.
- Exactly the eight histories defined in 156; raw7 at original left boundary, raw11 at original right boundary; time 0 or 24, with all tests at absolute time96, phase0. Physical injection into an already occupied training site is forbidden. Histories are predeclared and not selected by downstream outcome.
- **New measurement operator, not a physical rule:** at each original nearest support boundary `(min(support)-1) % 60` or `(max(support)+1) % 60`, flip one physical bit by XOR mask1/2/4/8 at test time. This test is *defined* even if the cell is occupied, and it does not add a cognition primitive.
- Track the union of locations where the perturbed trajectory differs from its own arm-specific unperturbed trajectory across 60 ticks, plus instantaneous differences at tick1/3/6/24/60. Lower union is a **designated observer locality objective**, not a reward used by the physics.
- Factorial contrasts: `LR - L0 - R24 + sham` and `RL - R0 - L24 + sham`, each calculated on parents where all four corresponding physical histories are feasible. A separate **common eight-arm** cohort is used for fair order/simultaneous comparisons. Parent-weighted means prevent pseudoreplication of raw masks/sides.

## Complete result

Across all 130 original parents and 260 parent-side contexts, 8,168 test records, 6,432 distinct `(full pretest physical state, test position, XOR mask)` combinations. The two four-arm cohorts contain LR 119 parents/238 contexts and RL 122 parents/244 contexts. The strict eight-arm common cohort contains **111 parents/222 contexts** and 7,104 response records.

Within the common cohort (average of the two test sides and four XOR masks, then across parents), the 60-tick causal affected-site union is:

| Experience history | Mean affected locations |
|---|---:|
| No external experience (sham) | 3.4685 |
| Left raw7 at tick0 | 5.5901 |
| Right raw11 at tick24 | 5.8266 |
| Left then right | **9.2782** |
| Right then left | **9.1453** |
| Both simultaneously | 9.7072 |

The parent-weighted two-pulse minus sham contrasts are +5.8097 (106 positive/3 negative/2 tied parents) for left-right and +5.6768 (102/8/1) for right-left. A positive contrast is *worse* under the declared objective of localized response.

Factorial interactions relative to individual pulses, on the common cohort, are +1.3300 and +1.2264 affected locations. These are not internal synergy/learning operators; they measure external forcing and nonlinear physical trajectories.

Original boundary XOR corrects Exp156's trivial distant-site sham score: the 1,040 sham test records span many affected-site union values; their parent-weighted average is 3.4685 in the common cohort.

## Scientific boundary

No internal task, no reward, no feedback, no goal, no population optimization, no adaptive exposure schedule, no online learning. Extra pulses change state/popcount/support, which can alone create response differences. The strict alternative arm eligibility depends on prior physical evolution, so comparisons apply only to those 111 eligible parents. Exp158 measures this baseline-state overlap limitation.

## Reproduce

```bash
python experiments/157_boundary_xor_multiepisode_gain_gate/run.py \
  --output experiments/157_boundary_xor_multiepisode_gain_gate/results/default.json \
  --csv experiments/157_boundary_xor_multiepisode_gain_gate/results/probes.csv \
  > experiments/157_boundary_xor_multiepisode_gain_gate/results/default.txt
python experiments/157_boundary_xor_multiepisode_gain_gate/test_smoke.py
```
