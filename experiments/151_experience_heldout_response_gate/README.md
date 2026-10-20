# Experiment 151 — Single-pulse experience and heldout susceptibility gate

## Question
Can a spontaneously arising G0 physical organization acquire a measurable improvement on **novel, heldout material inputs** following one previous material encounter, with no learner or reward encoded into the physics?

## Frozen preoutcome protocol

- Same original Exp104/139 kernel, 60 circular 4-bit windows, CENTER=30, left rotation, 3-phase scheduler. All **130** G0 catalog parents, not the null-eligible 113.
- At tick0, introduce exactly one boundary pulse **raw7** or **raw11** on the left or right of each parent's original autonomous union support. Sham state receives no pulse. raw7 and raw11 both have 3 set bits, but are not necessarily physically matched after evolution.
- Evolve every arm for **24 or 96 ticks**; they are multiples of the scheduler period. At equal phase0, test the **opposite** original boundary using raw values **1, 5, 9, 14**, never used as training raw values.
- A test is admissible only if its target site remains zero in **all three arms before evaluation**. Excluded cases are reported, not counted as failures. This is a pretest conditioning restriction, and the hypothetical overwrite intervention at occupied sites is not defined.
- For each arm, evolve both the heldout-injected state and **its own no-heldout baseline** for 60 ticks. Let `R(t) = {window position | injected(t) != baseline(t)}`. Define time-integrated affected-location count as `|union_{t=1..60} R(t)|`; also record thresholds >=10 and >=30 affected locations, and t6/24/60 differences.
- Unit of independence is **parent**; directions, delays and test raw values are dependent repeated observations. Equal-weight eligible parents are the primary aggregation, not a pooled-binomial inference. Observer-designed containment is not an internally learned goal.

## Results

| Pretest state delay | Eligible parent-side contexts / 260 | Eligible parent clusters | Mean union affected positions sham | Pulse7 | Pulse11 | Parent-mean pulse7 − sham |
|---|---:|---:|---:|---:|---:|---:|
| 24 | 228 | 130 | 5.9933 | 7.3846 | 7.2346 | **+1.3913** |
| 96 | 219 | 127 | 6.1939 | 7.2667 | 6.8996 | **+1.0728** |

The >=10-location response fraction at delay24 is sham 13.46%, raw7 18.56%, raw11 19.33%. At delay96, sham 14.67%, raw7 17.32%, raw11 17.22%. Larger effect footprint is **worse** under the stipulated observer-defined containment target. The training signal neither improves that objective nor establishes any internally represented objective.

## Interpretation boundary

This *single exposure* is not evidence of training, a change in prediction capability, reinforcement learning, semantic memory or endogenous goal. More spread is straightforwardly compatible with ordinary nonlinear microstate sensitivity. Before the novel test, sham and pulsed states have different physical bit budgets and occupancy distributions; exact physical overlap is rare (Experiment152). Pretest site eligibility conditions on the post-experience state and excludes 73 of 520 contexts. Results are conditional on that eligibility and cannot be generalized to forbidden overwrite tests.

## Reproduce

From repo root:

```sh
python experiments/151_experience_heldout_response_gate/run.py > experiments/151_experience_heldout_response_gate/results/default.txt
python experiments/151_experience_heldout_response_gate/test_smoke.py
```

`results/default.json` stores full protocol, inventory and parent-mean summaries; `results/probes.csv` holds every 5,364 per-arm physical response; `results/eligibility.csv` keeps all 520 pretest context-eligibility and bit-density records. All are deterministic. No new physical primitive added.
