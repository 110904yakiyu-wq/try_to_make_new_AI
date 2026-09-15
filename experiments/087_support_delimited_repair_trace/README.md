# Experiment 087 — support-delimited repair trace

## Question

Experiment 086 found post-E3 p3 persistence only when a fixed repair-trace length of 6 symbols was used. Because 6 is exactly two period-3 blocks, that result is contaminated by target-compatible geometry.

Can the trace span instead be derived from the repair event itself?

## Setup

The disturbance and repetition-repair dynamics are unchanged.

For the mutated site, collect every period hypothesis `p in [2,8]` that:

1. observes two equal preceding p-blocks;
2. proposes changing the disturbed site;
3. proposes the exact pre-disturbance symbol;
4. agrees with all other successful repair proposals.

No observer-specified trace length is used.

Three derived retention spans are audited:

- `union`: retain the full contiguous span covering all successful causal supports, equivalent to `2 * max(p)` symbols;
- `intersection`: retain only the common shortest support span, `2 * min(p)` symbols;
- `one_block`: retain one block at the largest successful period, `max(p)` symbols. This last version is less causally complete and is included only as a control.

E3 is present for 300 sweeps and then removed for 300 sweeps.

## Result

Using 32 seeds:

- `union`: pre-removal p3 = **0.000000**, post-removal p3 = **0.000000**
- `intersection`: pre-removal p3 = **0.000000**, post-removal p3 = **0.000000**
- `one_block`: pre-removal p3 = **7.313125**, post-removal p3 = **0.760000**

The two natural causal-support spans do not reproduce the L=6 persistence of Experiment 086.

The one-block control can retain some p3, but it requires an additional abstraction choice: collapse a two-block causal witness into one block and use the largest successful period. That is already another structural prior.

## Interpretation

This strengthens the negative reading of Experiment 086.

The fixed-L positive result was not a generic consequence of retaining the causal support of successful repair. It depended strongly on **how the support was geometrically encoded**.

Therefore:

`repair consequence + self-derived causal support != robust internalization`

The next step should not keep tuning period-trace encodings. The period ontology itself is now part of the problem.

## Next

Return to the self-delimiting K8 substrate, where context boundaries come from the medium's own closure event rather than from an externally enumerated period family. Test consequence-coupled retention using the exact self-delimited event context, with no fixed trace length and no p2/p3 target label in the kernel.