# Experiment 012 — full ECA remote-geometry sweep

## Question

Is the remote response-geometry effect seen in Rule 129 specific to that rule, or does it occur across other fixed elementary cellular automata under the same finite observer budget?

## Hard-coded assumptions

- one-dimensional binary ECA substrate
- periodic ring
- fixed local update rule during each run
- width-3 injected patterns
- one-shot schedule `0`
- repeated schedule `0,4,8,12,16`
- probe offset 20 cells from the exposure site
- fixed probe horizon and fixed spatial sampling budget

No learner, reward, SELF variable, memory module, trainable rule, or internal objective is added.

## Observer metric

For a fixed training pair (`011`, `101`), measure the response of all eight width-3 probes after one-shot and repeated exposure. The vector difference is the response-geometry change.

The main ranking metric is the L2 norm restricted to the six probes that were **not** used for exposure. This deliberately asks whether repeated history changes the later response to interventions that were never trained.

## Default finite budget

- ring size: 64
- sampled exposure positions: every 8 cells
- remote probe offset: 20
- probe time: 48
- probe horizon: 8

## Result

The effect is not Rule-129-specific.

The strongest rules under the default budget include 98, 159, 151, 143, 142, 14, 113, and 226. Rule 129 remains non-zero but is only around rank 17 by untrained-probe L2.

At the same time, many of the 256 rules give exactly or nearly zero effect. Therefore the observation is neither unique to Rule 129 nor a trivial property of every ECA.

Rules with completely homogeneous truth tables (0 or 8 one-outputs) give zero. Intermediate truth-table densities contain most of the strong cases, but rule-table density alone clearly does not explain the ranking.

## Interpretation boundary

This is **not** evidence of learning. It only establishes that a fixed, extremely small local law can map repeated history into a distributed change of later intervention geometry, including interventions absent from the exposure history.

The next question is whether the strongest rules also show the low-dimensional shared response modes previously observed for Rule 129, or whether they merely produce large unstructured residuals.
