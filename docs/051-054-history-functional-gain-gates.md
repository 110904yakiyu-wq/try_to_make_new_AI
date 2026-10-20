# 051–054 — Functional experience gates: susceptibility, physical overlap and history-state equality

**Experiments 151–154** target a sharper boundary than raw persistence: can an initially emergent local organization gain an externally defined useful response to novel inputs following previous exposure, without adding a cognitive primitive? All four assays preserve the original 60-window four-bit, phase0 three-phase left-rotation kernel, with no learner, reward, memory register, SELF, or scheduler change.

## 151: single prior pulse does not yield containment improvement

Original G0 130 parents. Pretest one external boundary raw7 or raw11 pulse (same initial popcount) vs sham; allow 24 or 96 ticks. Test opposite boundary with disjoint raw1/5/9/14, provided the site is vacant in all arms. Reference for the heldout test is each arm's **own contemporaneous no-test trajectory**, isolating the incremental consequence of the novel input instead of conflating it with spontaneous background activity. Score the union of impacted window positions in 60 ticks; lower is externally selected as more localized.

Of 520 parent/side/delay contexts, 447 eligible (228 at delay24, 219 at delay96); all 130 parents at delay24 and 127 at delay96. Parent-mean footprint sham vs raw7 vs raw11 at delay24: 5.9933, 7.3846, 7.2346. At delay96: 6.1939, 7.2667, 6.8996. There is **no demonstrated functional gain**; pulsed arms generally have more affected positions.

## 152: strong scalar-feature positivity failure

Immediately before the novel test, condition on equal total raw bitcount and equal occupied-window count. Same-site eligibility aside, only **2/228** (delay24) and **2/219** (delay96) contexts match both observables for sham vs raw7. This prevents using such a selected stratum as a reliable physical-controlled demonstration. Conditioning on post-treatment microstate descriptors is itself a change of estimand; any apparent difference within the tiny overlap is not a controlled direct effect.

## 153–154: order of external exposures versus physical state

Present raw7-left and raw11-right at times 0/24 in opposite orders, with simultaneous-input reference. Observe all arms at common tick72 phase0; select unoccupied outer sites for heldout raw1/5/9/14. Both chronological schedules exist in 111/130 parents, but only 110 test-site contexts (70 parents) satisfy all-arm non-overwrite requirements. Parent-mean location-footprint left-first/right-first/simultaneous: 14.6446/15.2304/15.1179; small order sensitivity is present and is not evidence of adaptive learning.

Critically, **46/110 test-site contexts have identical entire physical microstates** after the differently ordered histories. All **184 corresponding heldout probes** exhibit *exactly identical* future response signatures. The other 64 contexts differ in current physical state, so differing responses require no extraphysical history variable. This directly checks the Markov contract.

## Inference hierarchy and next gate

1. Observed: physical context and externally administered input history alter subsequent input susceptibility; equal complete microstate and scheduler phase have equal deterministic futures.
2. Not observed: a learned improvement on the stipulated novel-input containment criterion; experience-driven generalization across unseen tasks; an endogenous cost/goal signal or an internal state encoding functional success.
3. Not identified: specific causal mediation by a self-maintaining temporal organization versus ordinary raw-bit physics and post-experience state-selection.
4. Necessary next step: **predeclared functional target** and explicit trained-vs-equal-material control with more than one episode, while measuring both pretest physical overlap and heldout performance. Repeated injections must respect the no-overwrite physical contract and fixed scheduler phase. Do not claim successful learning merely because the state changes or input order matters.

Sources: `experiments/151_experience_heldout_response_gate/` through `154_history_state_equivalence_audit/`. No historical result revised, no new physical primitive, failed/null assays retained.
