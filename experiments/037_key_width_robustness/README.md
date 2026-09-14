# Experiment 037 — K2 key-width robustness

## Question

Is the joint causal endpoint effect from Experiment 035 specific to a 4-bit rendezvous key?

## Method

Keep the same K2 physical law, equal-budget histories, stateless min/max pair schedulers, intervention family, rotate rewrite, and future event budget.

Vary only rendezvous key width:

`3, 4, 5, 6`

For each width, measure:

- equal-budget histories whose final relation repertoire differs;
- histories whose future event trace differs;
- eligible donor/recipient causal-transfer cases;
- exact recovery by either endpoint alone;
- exact recovery by both endpoints together;
- strict joint-only recovery, where neither endpoint alone succeeds.

## Result

| key width | relation repertoire diff / 64 | future trace diff / 64 | causal eligible | endpoint 1 exact | endpoint 2 exact | both exact | strict both-only |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 56 | 39 | 76 | 0 | 3 | 34 | **31** |
| 4 | 52 | 46 | 83 | 4 | 5 | 26 | **17** |
| 5 | 42 | 42 | 75 | 2 | 0 | 11 | **9** |
| 6 | 33 | 33 | 59 | 0 | 0 | 3 | **3** |

## Interpretation

The relational joint-causality effect is not unique to a 4-bit key.

As key width increases, repeated matching windows become rarer under the same finite ring and event budget, so the absolute number of joint-transfer cases decreases. But strict joint endpoint necessity is present at every tested width.

The strongest result is actually at width 3, where endpoint 1 alone never exactly transfers the donor trace and endpoint 2 succeeds only three times, while the two endpoints together succeed in 34 cases, 31 of them strictly joint-only.

This supports a substrate-family interpretation:

> temporary content-defined relations can create jointly necessary separated causal support across several physical key granularities.

It does not yet show robustness to the rewrite law itself.

## Next audit

Change the minimal rewrite while keeping the same transient matching relation. This separates effects of **relational topology** from effects of the specific opposite-rotation rule.
