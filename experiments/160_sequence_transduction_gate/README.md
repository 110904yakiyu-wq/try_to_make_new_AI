# Experiment 160 — Heldout symbolic sequence transduction gate

## Question

Can an **external**, fixed-method linear readout of the frozen physical terminal microstate recover a prespecified two-input Boolean relationship for previously unseen 4-bit input masks, beyond reading the raw input bits alone? This tests **observer-decodable transduction**, not learning by the physics.

## Frozen protocol

- Physics: unchanged `139_extended_control_budget/core.py` / 104 kernel, 60 windows × 4 bits, period-3 scheduler, phase0 start and evaluation.
- Initial conditions: original 130 G0 parents, **no outcome-based parent selection**.
- Original cycle-union left and right support boundaries, respectively. At tick0 apply XOR mask `a` to the left window; at tick24 apply XOR mask `b` to the right window; evolve through tick96. XOR is an **external experiment input operator** and does not alter the kernel, even if the window has become occupied. Both input masks are nonzero.
- Binary observer target: `popcount(a) % 2 XOR popcount(b) % 2`.
- External decoder training raw values: `[1,2,3,5,6,7,9,11]`, 8²=64 pairs. Strict heldout raw values: `[4,8,10,12,13,14,15]`, 7²=49 pairs. No heldout raw value appears in either training position; each set includes both parity classes. Training labels balanced 32:32; heldout labels 25:24.
- Parent-specific external **dual ridge regression** classifier (α=1, training-only feature centering, prediction threshold 0.5), no validation-based hyperparameter optimization. Features: full tick96 terminal microstate represented by 240 raw bits, direct concatenated 8 input bits (no physical evolution), or terminal total bit count and occupied-window count. Baseline also includes five deterministic shuffled training-label decoders per parent.
- Inference unit: **parent**, not 49 dependent heldout sequences; equal-parent aggregation. Descriptive 10,000-resample parent-cluster bootstrap percentile 95% intervals, added after the initial exploratory run and **not** prospectively preregistered.

## Result: no demonstrated functional generalization

130 parents, 14,690 complete tick96 physical trajectories (130 × [64 + 49]); deterministic re-execution and smoke test pass.

| Readout | Mean parent heldout balanced accuracy | Exploratory parent-bootstrap 95% interval |
|---|---:|---:|
| Terminal 240-bit microstate | **50.0776%** | 49.2608–50.8962% |
| Direct 8-bit input (no evolution) | 45.1667% | 45.1667–45.1667% |
| Terminal bit count + occupied windows | 49.1865% | 48.3115–50.0590% |
| Terminal readout with shuffled training labels | 49.8246% | 49.4312–50.1994% |

The terminal-minus-input difference is **+4.9109 percentage points** (95% interval **+4.0942 to +5.7295**), with 101 parents positive, 19 negative, 10 tied. **Crucially, terminal readout itself does not exceed balanced-chance 50% with supported uncertainty.** The direct-input baseline performing *below* chance is insufficient to infer a useful computation. The primary functional-generalization gate therefore **fails**. One parent has heldout exact terminal-state collisions across opposite labels.

## Scope and limitations

This is exploratory task/readout design, not preregistered confirmation. The relationship is defined by the researcher, the labels and supervised decoder are external, and the original kernel receives no labels/reward/feedback and does not train. No self-derived task, internal goal, adaptation or learned representation is identified. An input-only linear baseline is deliberately limited and is **not** an information-theoretic bound: a nonlinear observer computing input parity has perfect accuracy trivially. A finding of high downstream readout accuracy would likewise not prove intrinsic learning. The same raw-value split is reused for all parents; parent-bootstrap intervals describe variation across this G0 catalogue, not generalization to arbitrary initial states.

## Reproduce

From repository root, with Python and NumPy:

```bash
python experiments/160_sequence_transduction_gate/test_smoke.py
python experiments/160_sequence_transduction_gate/run.py \
  --output experiments/160_sequence_transduction_gate/results/default.json \
  > experiments/160_sequence_transduction_gate/results/default.txt
```

`results/default.json.gz` contains the lossless complete `default.json`, including 130 parent records. Decode with `gzip -dk default.json.gz` in a copy or use Python `gzip.open`. The reproducible text summary is also committed. All physical trajectories are regenerable from the frozen parent catalogue; individual 60-window trajectories are not stored in the archive.
