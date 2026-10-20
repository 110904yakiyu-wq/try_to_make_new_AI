# Experiment 153 — Material-input order and heldout response

Does the **order** of two externally scripted pulses change the downstream response when both histories deliver the **same two raw values at the same two sites**? This measures ordinary phase-dependent physical path sensitivity, not learning.

## Contract

- All original 130 G0 parents; original left and right **cycle-union boundary** sites are zero before the first pulse.
- Two chronological histories: left raw7 at tick0, right raw11 at tick24 (**left-first**), and the opposite order (**right-first**); each value remains attached to its specific spatial site. Reference: apply both pulses simultaneously at tick0. The simultaneous reference uses the same contents but not the same timing schedule.
- The second pulse is allowed only when the target site is still zero in both ordered histories. No overwriting or silent skip.
- Evolve every history to common **absolute tick72**, phase0. Then use heldout raw values `{1,5,9,14}` at either outside-original-boundary position `left-2` or `right+2`, only if it is zero across all three histories.
- The heldout response is the union of positions with a physical bit difference from that history's own phase-identical untested future during the next **60 ticks**. Prespecified observer criteria are union size and reach>=10/30. Parent-level repeated-measures summaries, no claim of three independent cohorts.

## Results

- Both chronological 2-pulse histories were physically admissible for **111/130 parents**.
- **110 eligible test-site contexts** from **70 distinct parents**, four heldout raw values = **440 heldout probes per arm**.
- Parent-mean cumulative causal-response union size: left-first **14.6446**, right-first **15.2304**, simultaneous **15.1179**. Left-minus-right = **−0.5857 sites**, with 18/26/26 parents positive/negative/tied.
- Parent-mean response union >=10: left-first **67.86%**, right-first **68.57%**, simultaneous **68.39%**.
- **46/110 eligible contexts have exactly identical complete microstates** at tick72 for the ordered histories; see Experiment154 for strict future equality.

Input order changes some physical states and observed heldout responses but does not establish a training algorithm, memory register, information use, goal or adaptation. The equal-material schedules differ in timing and consequently their evolved bit distributions. Severe eligibility attrition and input order are explicit.

```sh
python experiments/153_input_order_history_gate/run.py > experiments/153_input_order_history_gate/results/default.txt
python experiments/153_input_order_history_gate/test_smoke.py
```

`results/default.json` contains protocol, all pretest context states' feature counts and outcome summaries; `results/probes.csv` records every 1,320 heldout response.
