# Experiment 150 — Parent-deletion bounds on fivefold heldout spread residual

## Motivation

Experiment149 found that raw training-probe response matching reduces G0−control heldout spread-rate contrasts consistently across five disjoint train-raw panels, but leaves negative differences. Does that residual rely entirely on a few extreme parents, or is its observed sign insensitive to deleting some matched parent clusters?

## Protocol

- **No new simulation, physical update, control fitting or training.** Source = Experiment149's immutable 5-fold × 113-parent selected-control and G0 heldout counts.
- For every fold, rule (first, raw-nearest, training-response nearest), and event (ever reaching >=10 or >=60 union window positions), define parent-specific censor-aware eventual difference interval:
  - Lower = G0-confirmed-event − control-confirmed-event − control-unknown;
  - Upper = G0-confirmed-event + G0-unknown − control-confirmed-event.
- For a hypothetical deletion of exactly `k` parent clusters, the largest possible remaining upper event difference is obtained by **deleting the k most negative parent upper differences**. This is a deterministic finite-population adversarial sensitivity calculation, *not a permissible data-dependent sample selection policy*.
- Determine the smallest k for which this worst-case remaining upper difference becomes >=0; any fewer deletions provably preserve the negative sign for that fold. Report repeated-fold results, but folds are not independent parents.

## Main result

| Comparator | All-five-fold guaranteed sign after ANY parent deletions up to k (ever10) | Ever60 |
|---|---:|---:|
| First accepted | 37 parents | 40 parents |
| Nearest raw bits | 25 parents | 24 parents |
| Matched t1,t3,t6 response | **9 parents** | **9 parents** |

The smallest deletion set that can yield a nonnegative sum for **response-matched** controls is 10 parents (fold 5) for ever10 and for ever60; per-fold minimum required deletions: ever10 `[14,11,18,14,10]`, ever60 `[15,12,19,15,10]`. These choices depend on post-outcome per-parent effects and constitute a mathematical bound, not the user's prospective selection mechanism.

This audit confirms that a single extreme parent is insufficient to reverse the sign in the frozen 113-parent population. However the residual is much less deletion-robust than the original first-control association. This does not identify cognition or prove a causal low-level mediator. All 113 parents are from the selected 1000-proposal eligible group; 17 original catalog parents remain unmatched.

## Reproduce

```sh
python experiments/150_heldout_parent_deletion_envelope/run.py \
  > experiments/150_heldout_parent_deletion_envelope/results/default.txt
python experiments/150_heldout_parent_deletion_envelope/test_smoke.py
```

Standard library; full 1695 fold/rule/threshold parent delta records are saved to `results/default.json`. All observations refer to the same Exp149 heldout 24 per arm/parent and unchanged Exp104 local dynamics. No inference about independent fivefold replications, adaptation, SELF, learning, goals, heredity or reproduction.
