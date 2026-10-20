# Experiment 156 — Multi-episode, distant-site heldout probe (negative design audit)

## Question and immutable substrate

Can two externally supplied raw inputs improve the locality of the physical response to a previously unused input? Frozen 104/139 60-position 4-bit left-rotation three-phase kernel, CENTER30. Nothing resembling reward, memory, an organism identifier, a learner or an internal target is introduced.

Eight externally controlled histories: sham, left raw7 at tick0 (L0), right raw11 at tick24 (R24), both as L0→R24 (LR), right raw11 at tick0 (R0), left raw7 at tick24 (L24), both R0→L24 (RL), and simultaneous left raw7/right raw11 at tick0. All start from original G0 phase0 recurrent frame; comparison after tick96 (scheduler phase0). Every event requires an empty site; an occupied site is **never overwritten**.

Heldout physical test: deposit raw1,5,9,14 at either original support boundary moved **one further position outwards** (left-2 or right+2 from support). Eligibility requires an empty evaluation site in the compared histories. For each arm, the response is the 60-tick union of locations where the arm-with-test differs from that arm's own no-test future. Smaller union is an *observer-designated* locality goal, not an internal preference.

## Findings and experimental-design failure

- All 130 parents, 260 parent × test-side contexts; 6,128 eligible arm × raw response records; 4,528 unique test-state/site/raw combinations.
- Ordered four-arm comparison: LR 81 parents / 128 contexts; RL 81 parents / 129 contexts. Distant-site common eight-arm subset: **69 parents / 102 contexts**.
- At the distant-site test location, **every one of 1,040 sham response records has exactly one affected site**. This is nearly tautological: a single fresh perturbation outside the original supported domain can remain uncoupled. Apparent negative utility for externally pulsed histories is therefore not a meaningful functional-learning evaluation.
- It is not legitimate to replace the probe with a boundary *material deposit* while keeping the strict common-arm vacancy contract: zero of the 260 original-boundary contexts satisfy all four arms of either ordered comparison at tick96.

**Disposition:** preserve as a failed measurement design. Correct the evaluation operator, without changing the physical kernel, in Experiment 157. Never cite the large positive exposure–sham affected-site difference from 156 as evidence for or against learning.

## Reproduce

```bash
python experiments/156_multiepisode_heldout_gain_gate/run.py \
  --output experiments/156_multiepisode_heldout_gain_gate/results/default.json \
  --csv experiments/156_multiepisode_heldout_gain_gate/results/probes.csv \
  > experiments/156_multiepisode_heldout_gain_gate/results/default.txt
python experiments/156_multiepisode_heldout_gain_gate/test_smoke.py
```

All 260 eligibility records and parent-level descriptions are in JSON; raw probe observations in CSV. Cluster unit is the original parent, not each side or heldout raw value.
