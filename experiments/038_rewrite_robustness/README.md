# Experiment 038 — K2 rewrite robustness

## Question

Experiments 035–037 showed joint causal dependence across several rendezvous key widths, but all used the same opposite-rotation rewrite.

Is the effect caused by transient matching relations in general, or only by that particular rewrite?

## Method

Keep fixed:

- one circular bit medium;
- content-defined equality rendezvous;
- non-overlapping endpoints;
- stateless min/max pair scheduling;
- equal-budget history family.

Change only what happens after a matched pair is selected.

Test four small rewrites for a key `x`:

1. `rotate`: first endpoint `rotl(x)`, second `rotr(x)`;
2. `edgeflip`: flip opposite edge bits at the two endpoints;
3. `flip_first`: flip one bit only at the first endpoint, leave the second unchanged;
4. `complement_first`: complement the first endpoint key, leave the second unchanged.

Use a shorter common event/cascade budget for this cross-law audit.

## Result

| rewrite | causal eligible | endpoint 1 exact | endpoint 2 exact | both exact | strict both-only |
| --- | ---: | ---: | ---: | ---: | ---: |
| rotate | 94 | 7 | 0 | 22 | **15** |
| edgeflip | 88 | 1 | 1 | 2 | **0** |
| flip_first | 52 | 10 | 0 | 12 | **2** |
| complement_first | 66 | 2 | 0 | 19 | **17** |

## Interpretation

The K2 joint-causality effect is **not** guaranteed by matching topology alone.

It survives a major change of rewrite law: `complement_first` produces a strict joint-only effect comparable to, and under this shorter budget slightly stronger than, the rotate law.

But `edgeflip` produces essentially no strict joint-only recovery, and `flip_first` is weak.

Therefore the current evidence supports a more specific hypothesis:

> transient nonlocal relations can support distributed causal organization when the relation-triggered rewrite preserves or regenerates dependence on both endpoints strongly enough.

The topology matters, but so does the physical transformation performed through that topology.

This is useful because it prevents treating “dynamic graph” as a magic ingredient.

## Next question

What property separates the strong rewrites (`rotate`, `complement_first`) from the weak ones?

The next audit should compare whether an interaction:

- destroys the enabling relation immediately;
- creates new matches involving both former endpoints;
- propagates endpoint information into different windows;
- changes the number and spatial span of future rendezvous relations.

The aim is to find a dynamical property, not another hand-picked rewrite catalogue.
