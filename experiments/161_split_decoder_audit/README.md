# Experiment 161 — Input-mask split × readout-capacity audit

## Question

Exp160 observed +4.91 percentage points of heldout balanced accuracy (BA) for the **linear** readout of 240 physical terminal bits vs eight literal input bits, but terminal accuracy itself was approximately chance. Is this contrast robust to different heldout raw-value partitions and matched nonlinear external readouts?

## Frozen physics and task

- Uses the exact `139_extended_control_budget/core.py` kernel via Exp160: 60 windows × 4 bits, phase0, deterministic three-phase local updates, no training or reward.
- Uses original 130 G0 parents. At tick0 left **original** support boundary XOR mask `a`; at tick24 right **original** support boundary XOR mask `b`; end at tick96, phase0.
- Observer label: `popcount(a)%2 XOR popcount(b)%2`. The raw input alone fully determines the label. This is an intentionally **externally assigned** Boolean task, not an organism's purpose or an intrinsic learning objective.
- 12 fixed raw-mask partitions, the first **identical to Exp160**, 11 more obtained with `random.Random(1612026)` without inspecting results. Each split trains on 4 odd-popcount and 4 even-popcount nonzero masks (64 ordered pairs); the complementary 7 masks (49 pairs) are held out and **never** used for fit or bandwidth. All 225 ordered pairs are physically evolved **once per parent** and cached, then assigned to fixed split indices.
- Compare the **same external family** trained separately on physical terminal state (240 bits) and unchanged literal input (8 bits): dual linear Ridge (`alpha=1`, train-only mean centering), and Gaussian RBF kernel Ridge (`alpha=1`, squared-Hamming bandwidth = median of positive training pair distances). Fixed threshold 0.5, no heldout tuning.
- Algebraic direct-input parity oracle = **100% by definition**, not a trained baseline.

## Results

130 parents × 225 physical trajectories = **29,250** trajectories; 12 folds × 130 parents = **1,560** parent-fold comparisons, **14,040** decoder fits including permutations. All BA means use equal weight per original G0 parent and split.

| Fixed external readout | Physical terminal BA | Input-only BA | Physical − input, percentage points |
|---|---:|---:|---:|
| Linear ridge | **51.30%** | 51.53% | **−0.23** |
| Gaussian RBF ridge | **56.42%** | 75.79% | **−19.37** |

Parent-cluster bootstrap 95% descriptive interval (conditional on these 12 folds): linear physical-minus-input −0.59 to +0.14 points; RBF physical-minus-input −20.15 to −18.58 points. The original Exp160 split (fold0) reproduces +4.91 points linear; over all folds, linear paired advantage spans **−6.95 to +11.40** points. Thus the Exp160 linear *relative* advantage is strongly split-dependent and not robust.

RBF terminal readout is above 50% (parent-only interval 55.64–57.21%; 12 fixed fold means 50.62–69.14%), **but never justifies learning by the physics**. With five post-first-run seeded train-label permutations per parent/fold, physical RBF BA is 50.01%, paired true-minus-shuffled is +6.40 points (parent-only interval +5.60 to +7.20). The RBF input-only representation performs much better; it attains 100% on four of the 12 splits (fold IDs 1, 5, 10, 11), but only 48.83% on fold2. The heldout task depends strongly on the external decoder's inductive bias and raw-mask partition.

A **post-first-run** joint parent/split resampling stress test produces descriptive 95% ranges of 53.81–59.56% for terminal RBF BA, −2.99 to +2.78 points for terminal-minus-input linear, and −28.05 to −10.68 points for terminal-minus-input RBF. Splits share raw values and are correlated; this is **not** a confidence interval based on 12 independent experiments, nor a claim covering all possible splits. Label permutations and joint-axis intervals were added as exploratory diagnostics **after initial Exp161 outcomes**, and must not be misrepresented as preregistered tests.

Exact equal-terminal-state, opposite-label collisions appear in 12 of 1,560 parent-fold comparisons (four original parents). Such collisions impose a decoding constraint but do not explain the complete performance pattern.

## Interpretation and limits

The fixed kernel has a nontrivial, externally decodable, task-correlated nonlinear transformation of the stimulus sequence under the selected probe. However the physical-state readout is **inferior to using the original inputs** with the matched RBF family, and the alleged linear advantage from Exp160 disappears over folds. No learner, labels, feedback, decoder, memory variable, reward or goal were inserted into the physical system. A trained *observer decoder* cannot be counted as acquired internal computation or adaptive learning. Lower performance of these two decoder families is **not** an information-theoretic proof that the physical dynamics destroyed input information.

## Reproduction

From repository root with Python + NumPy, preferably `OPENBLAS_NUM_THREADS=1` for predictable runtime:

```bash
python experiments/161_split_decoder_audit/test_smoke.py
python experiments/161_split_decoder_audit/run.py \
  --output experiments/161_split_decoder_audit/results/default.json \
  > experiments/161_split_decoder_audit/results/default.txt
```

`results/default.txt.gz` is the committed reproducible summary including all 12 per-fold means, parent bootstrap intervals, joint sensitivity intervals, and predeclared split metadata as generated by `run.py`. `results/sha256.txt` records the exact SHA-256 digests of the separately preserved lossless full JSON (1,560 parent-fold observations) and text summary distributed in the experiment ZIP. The full JSON can also be regenerated directly using the command above. The Git repository stores the executable source and negative results; the full JSON is in the downloadable experiment archive rather than committed as a Git blob. Individual physical trajectories can be regenerated from the frozen kernel and original G0 catalogue.
