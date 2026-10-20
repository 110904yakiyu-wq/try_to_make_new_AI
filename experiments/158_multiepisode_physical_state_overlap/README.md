# Experiment 158 — Physical overlap and time-resolved susceptibility under repeated external inputs

## Question

Can the 157 observation be separated from unbalanced physical state features at the time of testing, and is the effect instantaneous or amplified by nonlinear evolution?

## Method

Read **frozen** Exp157 results. On its 111-parent all-eight-arm common cohort, calculate bit-popcount and occupied-window differences for each history against sham at tick96, and compare full physical microstates separately. Read the 7,104 frozen heldout XOR probe responses, aggregate instantaneous positional difference at tick1/3/6/24/60 and 60-tick causal union by parent. No control or intervention is chosen using response outcomes. The frozen 139 kernel is invoked only to reconstruct phase-consistent pretest states and test exact Markov state identity.

## Result

- Left-then-right two-pulse state minus sham: mean **+9.0901 4-bit one-bits**, **+3.7387 occupied windows**. Right-then-left: **+9.4775 bits** and **+4.1441 windows**.
- Among 111 parents, **zero** have both popcount and occupied-window count equal to sham for either two-pulse history. **Zero** have completely identical 60-window physical microstates to sham across all non-sham histories. There is no complete support for an equal-physical-state interpretation.
- Left-then-right minus sham causal instantaneously affected positions, measured from independent identical bit-flip probes: tick1 +0.1475, tick3 +0.7331, tick6 +1.6441, tick24 +3.9392, tick60 +4.7714. Union over 60 ticks: +5.8097 positions.
- Full-state identity checks use `(state, phase0)`; a deterministic Markov update can never produce different futures from the same full state and phase.

## Interpretation

The larger response after prior external stimulation is a real, predeclared finite-time *physical susceptibility contrast*, but not identified as adaptive learning. It may be completely explained by different raw input bit configurations and ordinary local nonlinear propagation. The factorial interaction is similarly not an organism-internal objective or function. The common 111-parent cohort is selected by externally scripted pulse feasibility.

## Reproduce

```bash
python experiments/158_multiepisode_physical_state_overlap/run.py > experiments/158_multiepisode_physical_state_overlap/results/default.txt
python experiments/158_multiepisode_physical_state_overlap/test_smoke.py
```

`results/default.json` includes all 111 × 8 parent-arm physical feature rows and parent-level time-resolved summaries.
