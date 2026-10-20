# Experiment 159 — Is input-order history separately stored or embodied in the current physical state?

## Frozen contrast

Read Experiment 157's exact two-pulse and heldout XOR records. For each of 130 G0 catalogue parents, reconstruct physical states after left raw7 then right raw11 versus right raw11 then left raw7 (ticks0/24, evaluation tick96, common phase0), with the original no-overwrite training contract. Both schedules are feasible for 111 parents. Each schedule uses exactly the same two raw items and injection positions; only temporal order differs.

Compute full 60×4-bit current-state identity, 4-bit Hamming distance, changed-window count, and the eight **previously frozen** heldout XOR perturbation response results (left/right original nearest support boundary × masks1/2/4/8). The original physical law is unchanged; no supplementary memory or learner.

## Results

- **24/111 parents** reach precisely identical current physical microstates (with the same scheduler phase0) after the different sequences. In all 24 parents, all **192 heldout probes** have identical downstream responses (full 60-tick union and five instantaneous readouts).
- **87/111 parents** end in different raw microstates. All 87 have at least one changed heldout response. The mean physical Hamming distance among these is 11.87 bit positions.
- The order-contrast for parent-mean union affected locations, left-first minus right-first, is **+0.1329**, with 24 parents favoring the left-first larger response, 25 favoring the right-first larger response, and 62 ties. No stable preference across parent clusters.

The equality finding is a stringent internal regression for the phase-aware Markov kernel: different histories that converge to the same current microstate plus phase necessarily have identical futures, including heldout probes. **Different future responses when current physical state differs do not require independent history storage, learning, or another temporal state variable.**

## Reproduce

```bash
python experiments/159_order_state_response_equivalence/run.py \
  --output experiments/159_order_state_response_equivalence/results/default.json \
  > experiments/159_order_state_response_equivalence/results/default.txt
python experiments/159_order_state_response_equivalence/test_smoke.py
```

Result JSON contains one parent record per paired feasible parent and exact status of all eight probe comparisons. Unit of interpretation: original G0 parent, not 888 correlated heldout probes.
