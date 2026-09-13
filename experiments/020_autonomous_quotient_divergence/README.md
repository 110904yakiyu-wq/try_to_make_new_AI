# Experiment 020 — autonomous quotient divergence

## Question

Can two histories have the same current first-order operational quotient, receive **no further intervention at all**, and nevertheless develop different future quotients under the same fixed physical law?

This removes the external bridge used in Experiment 019.

## Method

At training time 48, compare one-shot and repeated exposure histories for all 256 ECA rules and all eight width-3 training patterns.

Keep only cases where the complete fixed probe assay yields exactly the same current quotient under both histories.

Then apply no new pattern, no bridge, and no parameter change. Let both states evolve autonomously under the same ECA rule.

Re-run the identical probe assay after future offsets `1,2,4,8,12,16` and record the earliest offset at which the two quotients differ.

## Result

Under the default finite assay:

- 1846 rule × training-pattern cases have the same current quotient at time 48.
- 230 of those cases autonomously diverge within the tested future offsets.
- 64 of the 256 ECA rules contain at least one such case.

Many divergences occur quickly, but delayed cases also exist.

A useful example is Rule 129 with training pattern `111`:

At time 48, both one-shot and repeated histories have the same fully separated eight-class quotient.

After eight autonomous steps:

- one-shot history remains fully separated;
- repeated history merges probes `001` and `011`.

No bridge or external context change occurs between those measurements.

## Interpretation

The current first-order quotient is therefore not, in general, sufficient to determine the future quotient trajectory.

Past history can remain hidden from the current quotient yet reappear in how operational identity reorganizes later under autonomous dynamics.

This is stronger than simple state-memory language in one precise sense: the hidden historical difference is detected at the level of **future changes in the operational equivalence relation**, not merely by reading a stored bit pattern.

However, the underlying CA microstates are already different and an omniscient observer could distinguish them directly. The result is therefore resource-/assay-relative, exactly as intended by the working theory.

This still does not constitute metacognition. The probe quotient remains an observer construction. What it demonstrates is that a fixed substrate can support a hierarchy of operational distinctions:

- two histories can look identical at one assay order,
- yet differ when tested by their future autonomous reorganization.

The next step is to formalize this hierarchy without inventing explicit meta-level objects in the substrate.
