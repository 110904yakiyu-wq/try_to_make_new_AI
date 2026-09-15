# Experiment 079 — parallel relational ecology

## Motivation

Experiment 078 removed absolute symbol privilege, but the sequential update schedule caused one relational organization to spread until it nearly monopolized the whole ring.

The next question is whether that monopoly is intrinsic to the `A-B-A` catalyst or partly an artifact of allowing a rewrite to trigger another rewrite later in the **same** sweep.

## Change from Experiment 078

The relational rule is unchanged:

`A B A D -> A B A B`

for `A != B` and `D != B`.

Only the timing semantics changes.

### Sequential mode

Each rewrite is immediately visible to later start positions in the same sweep.

### Parallel mode

All eligible events are detected from the pre-sweep state and then written simultaneously.

This bounds causal propagation to one local step per sweep. It introduces no symbol value, fitness score, resource label, or species identity.

## Result

Parallel timing strongly suppresses relation monopoly.

With no turnover:

- sequential active pairs: **1.00**
- parallel active pairs: **5.84**
- sequential dominant-pair fraction: **1.00**
- parallel dominant-pair fraction: **0.385**

Under one unbiased symbol mutation per sweep:

- sequential active pairs: **1.86**
- parallel active pairs: **9.34**
- sequential dominant-pair fraction: **0.991**
- parallel dominant-pair fraction: **0.331**
- parallel pair-repertoire Jaccard between adjacent sweeps: **0.903**

The same pattern persists under stronger turnover. Parallel timing keeps more simultaneously active relational pairs and prevents any one pair from accounting for nearly all motifs.

## Two-domain control

A ring initialized as two equal-size alternating domains,

- left half: `0,1,0,1,...`
- right half: `2,3,2,3,...`

contains 46 active motifs of each pair.

After 100 parallel sweeps with no noise the counts are still exactly:

- `(0,1): 46`
- `(2,3): 46`

Thus multiple relational organizations can coexist stably without assigning either pair a privileged symbol value or explicit niche label.

## Interpretation boundary

This experiment supports a narrower claim than "ecology emerged."

Supported:

> finite propagation speed can convert a permutation-symmetric relational autocatalyst from global monopoly into persistent coexistence of several relational organizations.

Still not established:

- invasion and replacement dynamics under finite space competition;
- spontaneous birth of new organizations from interactions among existing ones;
- history-dependent selection among organizations;
- adaptation;
- open-ended novelty.

The important design lesson is that **time semantics is part of the physical substrate**. Allowing unlimited within-sweep cascades effectively granted one organization a nonlocal replication advantage even though the symbolic rule itself was local and symmetric.

## Next question

Do the coexisting relational organizations actually compete and replace one another when space is scarce, or are they merely frozen domains separated by inert boundaries?

The next experiment should perturb domain boundaries and introduce small local competing seeds, then measure invasion probability, boundary motion, extinction, and reformation while preserving permutation symmetry and parallel updates.
