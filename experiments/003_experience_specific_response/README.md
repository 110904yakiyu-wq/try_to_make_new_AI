# Experiment 003 — experience-specific response

Experiments 000–002 show that a fixed Rule 110 medium has rich, history-dependent operational structure.

That is still compatible with an ordinary reservoir: history changes the current state, but the substrate does not necessarily become specifically better adapted to what it repeatedly experienced.

## Question

Does repeated exposure to a local pattern produce a persistent, pattern-specific change in how the same medium later responds to that pattern?

## Cross-over design

Use two equal-width patterns:

- A = `011`
- B = `101`

For each possible training position on the ring:

1. Start from the same single-1 initial condition.
2. A-trained run: inject A repeatedly at fixed training times.
3. B-trained run: inject B on the same schedule.
4. Allow a washout period after the last exposure.
5. At probe time, clone each trained medium and inject either A or B once.
6. Evolve the probed and unprobed clones for the same fixed number of steps.
7. Define probe impact as normalized Hamming distance between probed and unprobed future states.

For each position compute the cross-over familiarity score:

`S = ((impact_Atrained(B) - impact_Atrained(A)) + (impact_Btrained(A) - impact_Btrained(B))) / 2`

A consistently positive score would look like habituation to the familiar pattern. A consistently negative score would look like familiar-pattern sensitization. Either robust sign would indicate experience-specific modulation.

A mean near zero with large position-to-position variation is evidence that the fixed substrate is merely carrying history, not exhibiting this simple form of plasticity.

## Important

The score is an observer assay only. The CA is not rewarded for habituation, novelty, or any other behavior.

A negative result is useful: it would motivate adding the smallest possible form of endogenous plasticity rather than adding an AI architecture wholesale.
