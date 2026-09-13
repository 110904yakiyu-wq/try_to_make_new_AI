# Experiment 005 — spatial transfer

Experiment 004 found several fixed ECA rules with large repeat-count-dependent effects.

The obvious failure mode is trivial local residue: repeated overwriting may simply leave a local phase/state that makes the familiar probe cheaper at the exact training site.

## Question

Does the **repetition gain** transfer away from the training location?

For each candidate rule and offset `d`:

1. Train A or B repeatedly at position `p`.
2. Also run the one-shot A/B controls at the same `p`.
3. Probe at `q = p + d` instead of at the training position.
4. Compute the cross-over score for repeated exposure and one-shot exposure.
5. Report `transfer_gain(d) = repeated_score(d) - single_score(d)`.
6. Average across many training positions.

The physical medium remains fixed-rule and has no internal objective.

## Interpretation

- Gain only at `d = 0`: likely local residue / local phase memory.
- Gain over a finite causal region: the history-dependent effect has become distributed through the medium.
- Gain outside the causal light cone would indicate a bug in the assay.

Distributed transfer is still not learning. It is merely a stronger prerequisite than local residue.
