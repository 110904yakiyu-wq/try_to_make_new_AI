# Experiment 162 — Orbit-class-blocked cross-parent readout transfer

## Research question

In Experiment 161, external readout models were trained anew on 64 input pairs for **each evaluated parent**. Here we test whether a **single external model trained on other physical parents** can decode an unseen Boolean relation on (i) a never-trained parent and (ii) raw input masks that were not used for the decoder fit.

This is **observer-readable response transfer**, **not physical learning**. The frozen 60 × 4-bit, phase-0, three-scheduler local kernel is unchanged: it contains no labels, reward, task, external model, internal goal, or online adaptation.

## Fixed assay

- Use the 130 original G0 catalogue parents and the twelve train/heldout mask partitions frozen by Exp161. On each parent, the 225 nonzero `(a,b)` mask pairs are applied at the original left support boundary as XOR at tick0 and original right boundary at tick24; evaluate the 240 terminal physical bits at tick96, common phase0.
- Heldout observer label: `(popcount(a) & 1) XOR (popcount(b) & 1)`. Each split uses 8 train masks for both positions (64 ordered train pairs) and 7 disjoint evaluation masks (49 pairs).
- **Class-blocked parent groups.** Exactly 126 distinct phase-aware autonomous cycle classes exist among 130 nominal parents. Four pairs of different initial seeds fall in exactly the same phase-aware orbit: `[7,31]`, `[15,68]`, `[124,126]`, `[125,128]`. Assign entire equivalence classes to one of five **26-parent** groups via a deterministic, label-blind, greedy size-balanced allocation. Each group is the evaluation cohort in one cross-parent fold; the other **104 parents** are the entire decoder source pool. No identical phase-aware parent orbit is split across training and evaluation.
- **Shared readout training:** for each of the 64 input pairs, average the representation over the 104 source parents, yielding a 64-row prototype matrix. Train exactly the same Exp161 dual linear ridge or Gaussian RBF kernel ridge (`alpha=1`, threshold 0.5, bandwidth based exclusively on train-prototype pair distances). Evaluate the one source-model on 26 heldout parents. The source pool uses external labels; no evaluation-parent labels are used.
- Representations: (A) raw 240 terminal bits; (B) terminal bits minus **that parent's unlabeled no-input counterfactual** at tick96. (B) is label-free, target-parent-specific calibration and is **not pure no-touch zero-shot**.
- Within-parent reference: same external decoder family and same masks, but fitted to the evaluation parent's 64 labeled train pairs, exactly reproducing Exp161. Five prespecified seeded shuffled-label replicas per (mask split, parent group, representation, decoder) are observer-side negative controls.
- Unit: original parent, nested within 126 phase-aware orbit classes, with 12 dependent mask splits. The 5,000-parent bootstrap in `run.py` is only a descriptive conditional sensitivity analysis; `audit.py` additionally resamples the **126 physical orbit classes**. Neither refits source models in each bootstrap replicate, and neither supports population-level confidence claims or independent-split inference.

## Valid findings (after correcting orbit-class splitting)

29,250 non-sham physical trajectories plus 130 sham trajectories. Five heldout parent groups × twelve mask splits × 26 target parents × four readout settings = **6,240 parent/split/readout records**. The 60 fitted source-prototype models per setting use all 104 source parents without target-parent labels.

| Representation/readout | Shared decoder: unseen-parent heldout BA | Within-parent BA | Shared − within | Shuffled shared BA |
|---|---:|---:|---:|---:|
| Raw terminal / linear | 50.1910% | 51.2989% | −1.1079 pt | 50.0457% |
| Raw terminal / RBF | 53.1751% | 56.4187% | −3.2436 pt | 50.0295% |
| Sham-difference / linear | 50.1923% | 51.2989% | −1.1066 pt | 50.1621% |
| **Sham-difference / RBF** | **55.1704%** | 56.4187% | **−1.2483 pt** | 50.1104% |

Orbit-class cluster bootstrap descriptive 95% range (126 classes), **conditional on source-model fits and the fixed partitions**: raw-linear 49.924–50.461%, raw-RBF 52.702–53.653%, sham-linear 49.901–50.460%, sham-RBF **54.551–55.822%**.

For the sham-difference RBF, shared-minus-shuffled is +5.0600 pt; all 12 fixed mask-split mean accuracies exceed 50%, ranging 50.66–61.88%. **The observer can decode above-chance task-correlated information from heldout physical parents under this specified setup.** It does **not** mean the physics has acquired a task or learned a general skill. Sham-difference RBF remains below the parent-specialized decoder (−1.2483 pt, conditional parent bootstrap interval −2.16 to −0.33 pt). The Exp161 input-only RBF baseline is 75.79%, much higher than the transferred physical representation; direct parity calculation is exactly 100% by definition.

The sham-difference RBF outperforms raw-terminal RBF by +1.9953 pt, orbit-class-resampling descriptive 95% range +1.64 to +2.35 pt. This comparison and its additional interval were calculated **after the original preliminary run** and are exploratory.

### Invalid first split preserved as a design failure

The initial, outcome-blind `parent_id % 5` split failed a **previously omitted physics-level leakage check**: four pairs of distinct parent seeds were actually members of the same phase-aware autonomous orbit, and all four pairs spanned the split. The invalid initial results, which had sham-difference RBF at 55.5906% (not 55.1704%), **must not be used as evidence of independent-parent transfer**. The class-blocked split repaired the leakage, followed by full simulation/reexecution. This is a post-first-run experimental design amendment; Experiment 162 inference is **exploratory**, not an independently preregistered confirmatory result.

## Audits and reproduction

- Smoke test PASS, including algebraic equivalence of vectorized six-label kernel prediction to Exp161 one-label fitting, input mask disjointness, and five-fold orbit-blocked assignment.
- Full `default.json` and `default.txt` independently regenerated twice with exact SHA-256 matches.
- Frozen 104/139 `core.py` Git blob hash: `0b55b6bfdf0320784356f50096f8101a0e7108ae`.
- All 6,240 within-parent Exp162 entries matched Exp161 per-parent/per-mask-fold results **exactly** (source ZIP containing Exp161 full JSON), including both representations (sham centering is invariant within a parent for these decoders).
- `audit.py` reproduces orbit-class grouping checks and posthoc class bootstrap; the optional `--exp161` argument allows full prior-result row-level comparison.

From repo root with Python + NumPy:

```bash
export OPENBLAS_NUM_THREADS=1  # Linux/macOS; for Windows set this environment variable as appropriate
python experiments/162_cross_parent_readout_transfer/test_smoke.py
python experiments/162_cross_parent_readout_transfer/run.py \
  --output experiments/162_cross_parent_readout_transfer/results/default.json \
  > experiments/162_cross_parent_readout_transfer/results/default.txt
python experiments/162_cross_parent_readout_transfer/audit.py \
  --input experiments/162_cross_parent_readout_transfer/results/default.json \
  --output experiments/162_cross_parent_readout_transfer/results/audit.json
```

`results/sha256.txt` tracks the exact full JSON, full stdout and audit JSON. The downloadable experiment ZIP contains full per-parent split observations (lossless gzip), the verified initial invalid design record, and reproducibility files. Git stores executable code, scientific interpretation, summary, failure/audit record, and hashes. No new physics primitives were introduced.
