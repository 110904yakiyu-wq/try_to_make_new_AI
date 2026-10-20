# Experiment 139 — 100 → 1000 autonomous control proposals

**Question.** Were Experiment 133's 75/130 unmatchable parents truly structurally without controls, or did the finite 100-proposal budget censor control availability?

## Frozen physics and eligibility

- Original Experiment 104/108 kernel: 60 × 4-bit ring windows; center 30; phase0; three-phase simultaneous triple update; bit rotate **left**.
- The 130 original G0 on-cycle catalog entries; retain each parent's autonomously established period, exact cycle-union support locations, and phase0 occupied positions.
- For candidate attempt index `a` from zero, use **CPython `random.Random(3_000_000 + pid*300_000 + a)`** and nonzero values 1..15 at precisely the original frame's occupied windows.
- Test each candidate autonomously for at most **500 ticks**; check period, exact cycle support, phase0 occupied positions. No perturbation outcome is consulted.
- Change only the **proposal count** from 100 to 1000. Do not change autonomous cycle censor budget or physical update rule.

## Results

At 100: exactly 55 parents eligible, 87 accepted candidates; the full per-parent acceptance-count histogram is exactly Experiment 133's 0:75, 1:33, 2:16, 3:3, 4:2, 5:1. The original 55 first-acceptance attempt IDs exactly match Experiment 126's immutable manifest. Independent Python/C++ classification checks pass.

At 1000: **113/130 eligible**; 970 accepted candidates in total; **58 additional parents** acquire controls. Among the 17 still unmatched, two have cycle period 3, four period 12, four period 18, three period 24, four period 168. Zero acceptances by 1000 is **not evidence of mathematical nonexistence**.

## Reproduce

From repository root, Python standard library and C++17 compiler:

```sh
python experiments/139_extended_control_budget/build_proposals.py
c++ -O3 -std=c++17 experiments/139_extended_control_budget/sweep.cpp -o /tmp/exp139_sweep
/tmp/exp139_sweep experiments/139_extended_control_budget/results/proposals.bin experiments/139_extended_control_budget/results/accepted.csv
python experiments/139_extended_control_budget/analyze.py
python experiments/139_extended_control_budget/test_smoke.py
```

`results/proposals.bin` is generated (23 MB) and deliberately not committed. The committed `accepted.csv` lists all accepted attempts and reconstructed 60-byte control microstates. `results/default.json` includes all 130 parent-level acceptance metadata and first-acceptance attempts. The stand-alone `core.py` copies the published physical semantics to make the Python/C++ agreement independently auditable. Tests verify the exact historical 100-proposal identities and 96 proposed controls directly in Python.

**Inference boundary:** This improves *eligibility coverage*, not evidence of learning, organization-specific causality, or universal generalization. All 113 eligible parents remain a selected subset of the 130 G0 catalog. The 500-tick candidate convergence horizon also matters.
