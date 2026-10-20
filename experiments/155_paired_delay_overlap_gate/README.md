# Experiment 155 — Fixed-cohort delay overlap for apparent experience effects

Experiment151 reported pulse7−sham affected-window union difference of +1.3913 at t24 and +1.0728 at t96. **The evaluated parent/side population was not the same at both delays**, because the no-overwrite eligibility test is state-dependent.

## Procedure

Reuse only frozen Experiment151 eligibility and heldout-response CSV, with zero extra simulation or fitting. Restrict to the **same original parent and the same training-side context** whose opposite-side heldout test site is empty for all three arms at both 24 and 96 ticks. Score the parent-equal-weight pulse-sham union-position difference (and >=10/30 binary measures) at both delays, plus paired 96-minus-24 change. Do not treat dependent directions or timepoints as independent experiments.

## Outcome

- Eligible contexts separately: 228/260 at t24 and 219/260 at t96.
- **Shared eligible contexts: 215/260**, representing **127 parents**.
- On this fixed cohort, pulse7−sham mean affected-window difference: **+0.9478 (t24)** and **+0.8976 (t96)**; paired change **−0.0502 positions** (16 parents shrink, 8 increase, 103 tied).
- For equal-initial-popcount raw11, pulse11−sham: +0.5177 (t24), +0.5335 (t96), paired change +0.0157 (10 shrink, 10 increase, 107 tied).

**Inference boundary:** It is not valid to label the raw full-cohort reduction of +1.3913→+1.0728 as direct forgetting or diminishing physical learning. Much of it reflects the changing set of evaluable contexts. The fixed-cohort result is still ordinary physical susceptibility, not semantic memory, adaptation or retained functional skill; it does not remove raw-state imbalance.

Reproduce:

```sh
python experiments/155_paired_delay_overlap_gate/run.py > experiments/155_paired_delay_overlap_gate/results/default.txt
python experiments/155_paired_delay_overlap_gate/test_smoke.py
```
