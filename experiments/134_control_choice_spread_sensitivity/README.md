# Experiment 134 — Propagation outcome sensitivity to choice among valid controls

## Motivation

Experiment 133 identified **87** preoutcome exact-geometry-matched on-cycle controls for the original **55 G0 parents**, including 32 additional distinct controls at 22 parents. The earlier Experiments 129–132 use only the *first eligible control*. Could the observed negative G0−control physical spread contrast be an artifact of this arbitrary first-choice convention?

## Assay

- Original 104/108 physical kernel, 60 circular 4-bit windows, left rotation, CENTER30, phase0 three-phase scheduler. No physics changes, learning/SELF/reproduction/reward primitives.
- Candidate eligibility is fixed by Experiment 133's **pre-injection, autonomous** criterion; the exact accepted candidate attempt indices and microstate SHA256 are frozen in `133/results/default.json`.
- Reconstruct the **32 additional accepted phase0 controls** from the original RNG and autonomously certify their phase0 cycle. Save their 60-byte raw microstates as hex strings with SHA256 in `results/alternative_controls.csv`.
- For each of these 32 physical controls, test the complete original **30-probe** panel: raw 1..15 at the same two support boundaries. C++ implementation of the original local 4-bit kernel tests whether cumulative historical support ever reaches 10 or 60 distinct positions, up to tick 50,000. An exact `(microstate, next scheduler phase)` recurrence before the threshold is a **permanent no**; an unresolved trajectory is censored. The C++ physical step and event certificates are spot-checked by Python.
- The **55 original first-choice** controls and all 55 G0 arms retain the authoritative Experiment 130 raw CSV. Combine only after all additional controls are measured. No choice is made based on injected response outcomes.
- Report three contrasts for each K: historical first eligible; uniform averaging over **all accepted eligible controls per parent**, then equal weight over 55 parents; and a *retrospectively selected* min/max across each parent's eligible controls as a **mathematical sensitivity envelope**. The envelope is NOT a deployable outcome-aware null selector.

## Results

| Endpoint (eventual yes-rate G0−control) | Historical first choice | Parent-weighted mean over eligible candidates | Any eligible control choice envelope |
|---|---:|---:|---:|
| At least 10 reached positions | −16.97 pp | −15.68 pp | **[−20.18,−11.45] pp** |
| At least 60 reached positions | [−15.33,−15.27] pp | [−14.07,−14.01] pp | **[−17.94,−10.42] pp** |

At both endpoints, **20 of 22** multi-control parents exhibit some control outcome variation. At K=10, **six** parents admit both strict positive and negative individual parent G0−control contrasts depending on which eligible control is chosen. At K=60, **five** admit both directions.

The **population-conditional 55-parent aggregate sign remains negative** even if one retrospectively picks independently, for every parent, whichever pre-qualified control would have produced the most favorable G0−control difference. This provides a strong robustness check of the *descriptive physical-spread association* against the original first-match-control convention. It does not establish a G0-specific autonomous mechanism, nor does it validate the selected 55 parents as representative of all 130 G0 organizations.

Additional controls: 32 × 30 = 960 probes, with all K10 and K60 labels certified by tick50,000 (no censored additional controls at either endpoint). The historical 55 control arms include one unresolved K60 record. The interval calculus retains this right-censoring uncertainty.

## Reproduce

```sh
python experiments/134_control_choice_spread_sensitivity/build_alternatives.py
c++ -O3 -std=c++17 experiments/134_control_choice_spread_sensitivity/assay.cpp -o /tmp/exp134_assay
/tmp/exp134_assay experiments/134_control_choice_spread_sensitivity/results/alternative_controls.csv experiments/134_control_choice_spread_sensitivity/results/probes.csv 50000
python experiments/134_control_choice_spread_sensitivity/analyze.py > experiments/134_control_choice_spread_sensitivity/results/default.txt
python experiments/134_control_choice_spread_sensitivity/test_smoke.py
```

All source paths are defined relative to their experiment directories or supplied explicitly. No network/GPU required. Source and result JSON/CSV are committed; the compiled executable is not.

## Inference restrictions

87 controls are correlated within 55 parents. The 100-attempt finite candidate pool is not an unbiased sample of the space of all on-cycle organizations. The retrospective choice envelope is a **sensitivity range**, not a confidence interval or randomized causal identification. Raw 4-bit microstates still differ. No inference about reproduction, learning, heredity, goals, SELF, or causally irreducible organization is justified.
