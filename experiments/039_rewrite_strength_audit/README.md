# Experiment 039 — rewrite strength audit

## Question

Experiment 038 showed that transient matching relations are not sufficient by themselves: some rewrites produce strong joint causal dependence while others do not.

Can the difference be explained simply by how much of one endpoint is rewritten?

## Controlled rewrite family

Use one common structure:

- matching rendezvous relation is unchanged;
- only the first endpoint is modified;
- the second endpoint is left untouched;
- the first endpoint flips its lowest `m` key bits.

Sweep:

`m = 1, 2, 3, 4`

with key width 4 and the same short common event/cascade budget used in the rewrite audit.

## Result

| flipped bits `m` | causal eligible | endpoint 1 exact | endpoint 2 exact | both exact | strict both-only |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 52 | 10 | 0 | 12 | **2** |
| 2 | 44 | 2 | 12 | 14 | **0** |
| 3 | 54 | 7 | 0 | 16 | **9** |
| 4 | 66 | 2 | 0 | 19 | **17** |

## Interpretation

Rewrite magnitude matters, but not monotonically by itself.

The 3-bit and 4-bit endpoint changes produce much more strict joint-only causal recovery than the 1-bit change, while the 2-bit change is a counterexample to any simple "more changed bits = more relational causality" rule.

Therefore the relevant property is likely a combination of:

- how far the post-interaction endpoint moves in local state space;
- which bit positions are changed;
- which new rendezvous matches become available afterward;
- whether one endpoint remains an anchor while the other creates new relational opportunities.

The strong `complement_first` result from Experiment 038 is therefore not explained merely by asymmetric rewriting. Its particular large transformation of one endpoint appears important.

## Current K2 hypothesis

A useful K2 interaction may require two ingredients simultaneously:

1. **relational enablement** — execution requires separated current structures to satisfy a joint condition;
2. **topology-generating rewrite** — executing that relation must alter the medium strongly enough to create a different future relation repertoire.

This remains a substrate hypothesis, not a cognitive claim.

## Next direction

Stop cataloguing arbitrary rewrites before this becomes parameter fishing.

The next useful experiment should measure the generated **relation repertoire itself** before and after an event and ask whether histories that exhibit strong joint causal transfer are also the histories in which one interaction creates access to previously absent relation types/spans under the same finite event budget.
