# Experiment 078 — permutation-symmetric relational catalysis

## Why this experiment

The uncommitted K11 scratch work showed a dangerous confound: some absolute 3-bit values could maintain activity much better than others when deposited into the medium. That means apparent ecological persistence could be caused by a privileged raw symbol rather than by relations among structures.

This experiment removes that confound completely.

## Kernel

The medium is a circular sequence of eight possible raw symbols. The only interaction rule is

`A B A D -> A B A B`

when

- `A != B`, and
- `D != B`.

The rule depends only on equality and inequality relations. It does not inspect the numeric value of A or B.

Therefore, for any permutation `pi` of the symbol alphabet,

`F(pi(x)) = pi(F(x))`.

No raw symbol is physically privileged by the rule.

## Observer assays

Three things are measured.

1. **Permutation equivariance** — random relabelings of all eight symbols must commute exactly with one update sweep.
2. **Relational self-repair** — begin from an alternating `A B A B ...` organization, replace one site by any third symbol, and ask whether one sweep restores maximal `A-B-A` motif density.
3. **Maintenance under unbiased turnover** — after every sweep, replace 0, 1, 2, or 4 random sites with uniformly chosen different symbols. Compare the relational catalyst against a no-rule control.

The observer records:

- number of active `A-B-A` motifs;
- number of distinct unordered symbol pairs participating in those motifs;
- executed repair events.

## Default result

The rule is exactly permutation-equivariant in **512/512** random relabeling trials.

Every tested single-site third-symbol defect in every alternating symbol pair was repaired at the motif level after one sweep:

- **16128/16128** cases.

Under continual unbiased turnover, active motif density remains very high:

| mutations / sweep | no-rule active motifs | relational rule active motifs |
| ---: | ---: | ---: |
| 0 | 10.34 | 96.00 |
| 1 | 10.56 | 93.86 |
| 2 | 10.58 | 91.76 |
| 4 | 10.42 | 87.75 |

So self-maintenance does not require an absolute catalytic symbol value.

However, the same experiment exposes a new failure mode. The number of distinct active symbol pairs collapses strongly:

| mutations / sweep | no-rule active pairs | relational rule active pairs |
| ---: | ---: | ---: |
| 0 | 7.66 | 1.00 |
| 1 | 7.93 | 1.86 |
| 2 | 7.85 | 2.60 |
| 4 | 7.79 | 3.87 |

With no turnover the medium converges to a single globally alternating pair. With turnover, a small number of pairs dominate.

## Interpretation boundary

This is a useful positive and negative result at the same time.

Supported:

> relation-dependent regeneration can produce robust self-maintenance even when every raw symbol is exactly exchangeable.

Not supported:

> a diverse ecology of independently maintained organizations emerges.

Removing **absolute-symbol monopoly** merely reveals **relation monopoly**: one simple relational organization expands until it occupies almost the whole medium.

This is not intelligence and not open-ended ecology. It is a permutation-symmetric autocatalytic toy.

## Next question

Can multiple relational organizations coexist without introducing a privileged species, explicit resource label, fitness score, or externally assigned niche?

The next assay should preserve symbol-permutation symmetry while adding only **local competition for finite space / interaction opportunity**. The target is persistent coexistence, invasion, replacement, and reformation of several relational motifs rather than collapse to one globally dominant alternating pair.
