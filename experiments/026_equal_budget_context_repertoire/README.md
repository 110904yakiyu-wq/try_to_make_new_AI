# Experiment 026 — equal-budget endogenous context repertoire

## Question

Does history change the set of naturally available local contexts only because one history receives more external interventions, or can the repertoire differ even when the physical intervention budget is held fixed?

## Method

Use the same five injection times: `0,4,8,12,16`.

For each ECA rule and each complementary width-3 pair `A/B`, compare two histories with exactly the same multiset of injected patterns:

- sequence 1: `A,A,A,B,B`
- sequence 2: `B,B,A,A,A`

Thus both histories receive:

- the same number of interventions,
- at the same times,
- with the same counts of A and B,
- under the same local update law.

Only temporal order differs.

After training ends at time 48, let the CA evolve autonomously for eight more steps. At every time slice and every ring position, record the naturally occurring radius-2 patch (7 bits).

A patch belongs to the endogenous context repertoire only if it appears in at least two different time slices of that autonomous window. This excludes one-frame transients.

The two recurrent-patch sets are then compared as sets: same, strict superset/subset, or non-nested reorganization.

## Default result

To avoid counting complementary A/B pairs twice, use `A=000..011`, giving **1024** rule/history-pair cases.

- same repertoire: **371**
- non-nested reorganization: **373**
- sequence 1 strict superset: **140**
- sequence 2 strict superset: **140**

Thus **653 / 1024 = 63.7695%** of cases have a different recurrent local-context repertoire despite identical intervention count, timing, and pattern multiset.

Average recurrent repertoire sizes:

- sequence 1: **24.1982** patch types
- sequence 2: **23.7588** patch types

Average history-exclusive patch types:

- sequence-1-only: **4.2900**
- sequence-2-only: **3.8506**

## Interpretation

This removes the main confound in the earlier one-shot/repeated comparison.

The available recurrent local context set is not determined only by how much external input was supplied. Under a fixed interaction budget, temporal ordering alone can leave the substrate with a different autonomous repertoire afterward.

At the observer level, this is a direct finite-budget example of

`C_B(history_1) != C_B(history_2)`

without changing hardware, local rule, interaction count, or input multiset.

The change is frequently non-monotone: histories often replace some recurrent contexts while creating others rather than simply adding more.

## Important boundary

A naturally recurring bit patch is still an observer-defined context candidate. The CA does not label it as a context.

This experiment also does not yet prove that the history-exclusive patches provide genuinely new operational capabilities. Experiments 022–024 establish that recurrent patches often carry operational and dynamical meaning globally, but the next step should test the **history-exclusive repertoire itself** for operational novelty.
