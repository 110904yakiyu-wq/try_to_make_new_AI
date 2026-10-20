# Experiment 146 — Orbit identity and within-distance response variation

## Question

Does the eligible control archive accidentally contain the same autonomous cycle as its G0 comparator? Is scalar XOR Hamming distance sufficient to account for material response, and do different tie-break rules matter?

## Assay

For all 970 controls of 113 eligible G0 parents, reproduce autonomous phase0 cycles with the original finite 60-window / 4-bit / 3-phase kernel. Compare the canonical lexicographically minimal phase0 state on each confirmed exact recurrent cycle against the G0's canonical phase0 state. The full physical microstate and next scheduler phase define recurrence. Contrast the preoutcome raw-bit distance to G0 against each control's frozen Exp142 material outcomes. Hold G0, eligible controls, and 30 material inputs per candidate fixed; no resampling.

Raw-distance ties are resolved in two separate ways: minimal accepted attempt; and (as in Exp145) minimal differing 4-bit window count followed by attempt. This is an **important explicit selection convention**.

## Findings

- 970 eligible control states. **One control (parent 22, attempt 15) is exactly G0's full phase0 microstate** and therefore has the same autonomous cycle; the remaining 969 are distinct G0 cycles. This literal identity is *not* independent evidence and must not be counted as a nontrivial physical null.
- 111/113 parent pools have >1 distinct raw-bit distance among controls.
- Within a parent and a fixed raw-bit distance, 231 groups have at least 2 candidate controls. Of these, **198/231 differ** in counts of 10-position spread responses, **199/231 differ** for 60-position spread. A single scalar distance is not sufficient to determine response.
- Tie-break convention changes the nearest control in **6 parents**, farthest in **2 parents**. Selecting nearest by bit distance then attempt yields control-ever10=663, while tie-breaking by distinct window count (Exp145 rule) yields **615**. The corresponding ever60 counts are 518 vs 476. Only 6 parents account for this sizeable descriptive shift.
- When raw distance alone breaks ties by attempt, comparing furthest vs nearest control counts per parent: for ever10, far higher 45 / near higher 45 / tied 23; for ever60, far higher 49 / near higher 43 / tied 21. Mean far-minus-near spread rates are +3.13 pp and +2.63 pp. It is **not** a consistent parent-level monotone rule.
- 65/111 measurable within-parent slopes of ever10 response count vs raw distance are positive and 46 negative; 68/111 vs 43 for ever60. These observational slopes are not causal effects.

## Reproduce

```sh
python experiments/146_autonomous_orbit_and_distance_gradient/run.py \
  > experiments/146_autonomous_orbit_and_distance_gradient/results/default.txt
python experiments/146_autonomous_orbit_and_distance_gradient/test_smoke.py
```

`run.py` writes detailed `results/default.json`. Python stdlib only, importing the exact phase-aware physical step and autonomous orbit helper from Experiment139. The same 970 control states and outcomes are already committed from 140/142.

**Limits:** Counting distinct physical cycles is not showing reproduction, learning or emergent autonomy. Same-distance dispersion is expected in an anisotropic nonlinear local kernel. Control selection is outcome-blind but not randomized assignment; only 113/130 matched parents are eligible.
