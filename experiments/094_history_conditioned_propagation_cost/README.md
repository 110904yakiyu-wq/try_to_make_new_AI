# Experiment 094 — history-conditioned propagation cost

## Question

Experiment 093 produced a finite-speed local substrate with metastable activity support. Can equal-budget history change the **cost of propagating a causal distinction** through that substrate?

This is the finite-speed analogue of the K8 access-cost question, but no atomic global scan is available.

## History construction

Use the width-4 left-rotation mutual-modulation kernel from Experiment 093 on a 12-window ring.

For one intervention position and complementary raw patterns `A` and `B`, compare two histories:

- sequence 1: `A,A,B,B,A`
- sequence 2: `B,B,A,A,A`

Both contain exactly three A and two B interventions and receive exactly the same execution budget.

After each of the first four interventions, run three local ticks. The fifth and final intervention is A in **both** histories, and the probe is applied immediately afterward.

Therefore the raw probe window is exactly identical between the two histories by construction. Only the earlier order differs.

## Probe cost

Flip the same single bit in the common final probe window.

For each trained state, run perturbed and unperturbed copies under the same local dynamics and record the first tick at which the perturbation reaches circular window distance at least `d`.

This first-arrival time is an observer-side finite-speed propagation cost.

The horizon is 18 ticks.

## Main result

Sweep:

- 64 random backgrounds;
- all 12 intervention positions;
- all 16 width-4 values for A, with B its bitwise complement.

Total comparisons: **12288**.

Number of cases in which the two history orders give different propagation cost:

- distance 1: **4932 / 12288**
- distance 2: **6901 / 12288**
- distance 3: **8945 / 12288**
- distance 4: **8308 / 12288**
- distance 5: **8685 / 12288**
- distance 6: **10270 / 12288**

At distance 6 the direction is almost perfectly balanced:

- sequence 1 faster: **5187**
- sequence 2 faster: **5083**
- tie: **2018**

So this is not evidence that one particular schedule is intrinsically better. History reorganizes the propagation-cost landscape in both directions.

## Strong controls

### Same immediate activity support

The two trained states have exactly the same next-tick active-window support in **6979** cases.

Even inside that subset, distance-6 propagation cost differs in **5767 / 6979** cases.

Thus the coarse activity mask alone does not determine later causal accessibility.

### Same local raw neighborhood

Because the final probe window is overwritten with the same A, it is identical in all 12288 cases.

A stricter condition requiring the probe window and its immediate left/right neighbors to be exactly identical occurs in **64** cases.

Distance-6 propagation cost still differs in **53 / 64** of them.

### Same local neighborhood and same immediate support

Both controls hold simultaneously in **42** cases.

Distance-6 propagation cost differs in **34 / 42**.

Therefore the difference cannot generally be reduced to the last local patch or to the immediately visible activity support. More distant history-dependent organization changes what the same local probe can reach under the same future budget.

## Handedness control

Using right rotation on 32 backgrounds gives the same qualitative result at distance 6:

- sequence 1 faster: 2570
- sequence 2 faster: 2533
- tie: 1041

So the effect is not tied to the left-rotation orientation.

## Interpretation boundary

This is **not learning** and not an improvement claim.

The supported statement is narrower:

> under a fixed finite-speed local law, equal-budget order history can reorganize the future resource cost of propagating the same local distinction, even when the probe location itself is identical and, in strict subsets, its immediate raw neighborhood and coarse activity support are also identical.

This is a stronger form of distributed operational history dependence than K1 showed, because the relevant causal difference is not usually compressible into the immediate local probe context.

## Next question

Which distributed parts of the trained medium are causally necessary for the changed propagation cost?

The next experiment should transplant separated regions between the two trained histories and ask for the minimum subset needed to transfer the donor's propagation-cost profile. That will distinguish genuinely distributed organization from one hidden remote control patch.
