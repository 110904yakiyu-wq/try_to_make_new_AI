# Experiment 071 — block hysteresis specificity controls

## Question

Is the Experiment 068 block-reversal signal just the last perturbation bits lingering at the training site, or does it reflect a broader history-dependent state? And is one trained state simply globally easier to recover from any perturbation?

## Local erase control

After `Q^8 -> P^8` versus `P^8 -> Q^8` training, restore selected width-3 windows in **both** states to the corresponding bits from the common initial background before the six-event washout.

With 8 backgrounds:

- no erase: `315 recent / 238 old`
- restore training window only (3 bits): `307 / 247`
- restore 3 adjacent windows (9 bits): `290 / 268`
- restore 5 adjacent windows (15 of the 18 ring bits): `219 / 271`

Restoring a single width-3 window at different offsets also changes the bias strongly and can flip its sign. Thus the effect is not a simple copy of the last P/Q value at the training site. It is also not robust to large state resets.

Because K8 interactions scan around the whole small ring, the best description remains **global dynamical hysteresis**, not localized memory.

## Held-out perturbation specificity

For each trained pair `(P,Q)`, test the third same-Hamming-weight perturbation `R` that was never used during training.

With 16 backgrounds and 1152 comparisons:

Experienced perturbations:

- P test favors P-recent history: **567**
- P test favors Q-recent history: **524**
- P ties: **61**
- Q test favors Q-recent history: **579**
- Q test favors P-recent history: **514**
- Q ties: **59**
- strict two-sided P/Q specificity: **184**

Held-out R:

- R favors P-recent history: **531**
- R favors Q-recent history: **551**
- ties: **70**

The held-out perturbation is approximately balanced, while trained P/Q tests show a modest expected-direction asymmetry.

## Interpretation boundary

The block effect has some experience specificity and is not simply a globally better state. But it is schedule-sensitive, spatially nonuniform, and fragile under large resets.

Therefore K8 should still not be called a learning system. The supported statement is:

> structured experience can bias later operational recovery in an experience-related way through distributed dynamical hysteresis.

The next question is whether this bias scales smoothly with experience dose and persists across washout, or whether it is an irregular property of selected block lengths.
