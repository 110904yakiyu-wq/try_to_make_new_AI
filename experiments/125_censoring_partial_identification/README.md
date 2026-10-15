# Experiment 125 — Partial identification under finite-time censoring (Exp108)

## Question

Does Experiment 108 establish eventual G0 organizational connected-cycle superiority, or only more rapid confirmed connected-cycle detection by tick 500? Can a sign be identified without treating an unresolved microstate as nonconnected or dead?

## Fixed cohort and procedure

- Recompute **all 130** G0 catalogue parents from the original 104/108 60-window/CENTER30/phase0 three-phase left-rotation kernel. Select controls *without any material injection*, using the same exact period, cycle union-support positions, phase0 occupied sites and scheduler phase, up to 100 candidate attempts per parent. **55** accepted; other 75 do not enter the comparison.
- On each accepted parent/control pair, inject raw 1..15 on each of the two union-support boundaries, **30 paired probes per parent, 1650 per arm**, horizon 500. Track the mutually exclusive observer classes: connected recurrent active, fragmented recurrent active, static recurrent, and unresolved/censored.
- For eventual connected-class outcome, confirmed connected recurrences are known connected forever under the unchanged deterministic phase-coupled kernel. Confirmed static/fragmented recurrence cannot later become connected without new interventions. *Only the right-censored trials remain unresolved.* Therefore per-arm lower bound = confirmed connected, upper bound = confirmed connected + censored.
- The overall paired difference bound is exactly `[G0_connected − (CTRL_connected + CTRL_censored), (G0_connected + G0_censored) − CTRL_connected]`. Report conditional averages across parent clusters and analogous parent-specific bounds, not binomial significance over 1650 correlated probes.

## Results

| Outcome (1650 trials per arm) | G0 | On-cycle, exact geometry-matched control |
|---|---:|---:|
| Confirmed connected active by 500 | **1486** | **1215** |
| Confirmed other recurrence | 21 | 37 |
| Censored (still no proven cycle by 500) | **143** | **398** |

Observed finite-horizon connected difference: **+271/1650 = +16.42 percentage points**.

Worst-case eventual connected count difference, allowing censored outcomes to resolve either way:

\[
 \Delta_{\mathrm{eventual}} \in [1486-(1215+398),\,(1486+143)-1215] / 1650
 = [-127,414]/1650 = [-7.70,25.09]\text{ percentage points}.
\]

**The interval includes zero**. Thus the eventual-persistence contrast is *not sign-identified* under this minimal censor assumption; treating censored controls as failed persistence falsely strengthens the evidence.

Parent-level bound classification (55 paired parents):

- Strictly positive lower bound: **11 parents** (robust G0 advantage even if all censored controls later connected).
- Strictly negative upper bound: **1 parent** (robust control advantage).
- Overlapping zero or not sign-resolved: **43 parents**.

The result is conditional on 55/130 accepted matches, not a claim about all G0 starting organizations. Finite observed superiority at tick500 and eventual superiority are different estimands. The long-horizon 114 audit on a narrower 20-pair subset did not resolve most censored cases by tick2000, but it does not close the 108 whole-cohort bound.

## Code reproducibility

```sh
python experiments/125_censoring_partial_identification/run.py --output experiments/125_censoring_partial_identification/results/default.json > experiments/125_censoring_partial_identification/results/default.txt
python experiments/125_censoring_partial_identification/test_smoke.py
```

Includes all 55 parent-pair class counts and individual lower/upper bounds. The original 108 exact connected/fragmented/censored distribution is reproduced (its fission and other fragmented cases are both folded under `fragmented` here; no new reproduction assay). Python standard library, no physical changes.

## Interpretation boundary

Not evidence for a SELF, learning, goals, heredity, or even unconditional stronger persistence. The proven observable is *higher fraction of connected recurrence identified by tick500* in this selected population, with substantial unequal right censoring. Next work should optimize observational power and parent support without freezing a desired direction.
