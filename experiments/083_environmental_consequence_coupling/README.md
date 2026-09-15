# Experiment 083 — environmental consequence coupling

## Motivation

Experiments 081–082 showed that period-2 organization has a strong intrinsic nucleation advantage under the repetition-extension substrate.

The next question is whether an environment can change the persistence of different relational organization types **without inspecting raw symbol values and without assigning fitness scores**.

## Environment

Two symbol-blind positional perturbations are used:

- `E2`: rotate every aligned 2-cell block by one position (equivalent to pair swap);
- `E3`: rotate every aligned 3-cell block by one position.

Both operators act only on position. They are equivariant under any permutation of symbol labels.

A period-2 organization is structurally compatible with E2, while a period-3 organization is structurally compatible with E3.

## Fixed-domain consequence assay

The ring begins half period-2 and half period-3.

With environment applied every 5 sweeps and no turnover, late mean coverage is:

| environment | p2 coverage | p3 coverage |
| --- | ---: | ---: |
| E2 | **54.80** | 26.00 |
| E3 | 18.15 | **51.54** |

Thus the same substrate supports a clear reversal in relative maintenance when only the external positional dynamics changes.

No organization label or fitness value is provided to the medium.

## Turnover ecology

Add one unbiased symbol mutation per sweep and randomize symbol labels, phases, and spatial rotation across 16 seeds.

At environmental interval 2:

- E2: p2 **79.71**, p3 8.69;
- E3: p2 57.76, p3 **47.17**.

At interval 1:

- E2: p2 **91.49**, p3 5.23;
- E3: p2 56.43, p3 **41.65**.

So E3 substantially increases period-3 persistence and suppresses period-2 relative to E2.

However, the period-2 type still usually remains numerically dominant once turnover allows continual renucleation.

## Interpretation

This separates two effects that had previously been mixed together:

1. **substrate prior** — short relational organizations nucleate and repair more cheaply;
2. **environmental consequence** — different positional disturbance regimes preserve different relational structures.

The environment can strongly reshape persistence, but it does not automatically erase the substrate's intrinsic complexity prior.

The supported statement is therefore:

> a fixed, symbol-symmetric substrate can exhibit environment-dependent persistence of relational organization types without an explicit fitness score.

This is still weaker than adaptive evolution or learning. The initial types were supplied by the experimenter, and turnover plus environmental filtering does not yet demonstrate generation of new structural types followed by selective amplification.

## Next question

Can the medium itself generate structural variants near an existing organization, and can an environment amplify variants whose **relational structure** is more compatible with current disturbances?

The next experiment should therefore stop initializing exactly one p2 and one p3 domain. Start from mostly one type, inject only generic symbol turnover, and measure whether new period types arise and persist differentially under E2 versus E3.
