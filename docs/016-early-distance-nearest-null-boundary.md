# 016 — Early-distance physical-null boundary (Experiment 116)

**Status:** audited full 20-parent cohort using unchanged physical kernel and exact strongest-tier Experiment 113 physical alternatives.

## Result

There are 57 feature-eligible patches: widths 1, 2, 3 yield respectively 23, 14, 20 patches and 33, 59, 414 distinct full-physics-matched alternative raw states. The 6 training raw probes (1,7,15 × two support boundaries), using early response-mask samples at ticks 1 and 3, have strictly positive minimal aggregate response Hamming distance against each donor transplant. Yet every patch has at least one null at distance <=16. The smallest mismatch ranges from 1 to 11 position bits; medians by width are 5, 4, 2.5.

On held-out 24 probes, tick-24 response-position-mask Jaccard donor−null, averaged within 15/10/16 eligible parents by width, is +0.02007/+0.07849/+0.15671 for complete physical null pools. Taking the single nearest training response null (with lexicographic tie rule and no outcome evaluation) yields +0.00980/−0.01112/+0.13116, with parent wins/losses 9/6, 4/6, 11/5.

No result here identifies a novel physical primitive, organizational independence, learning, reproduction, goals, SELF, or history dependence at equal full microstates. Parent cohorts are selected and share patches/probes; alternatives are state-space support within that limited cohort, not iid population samples. Jaccard agreement at tick 24 measures coarse response geometry, not long-run viability or physical work. The matched physical features do not exhaust later local microstate trajectories. Several predeclared thresholds create multiple descriptive comparisons, not inferentially corrected discoveries.

**Next:** Rotate the train/test value subsets (fixed folds) to test whether nearest-physical-null performance persists across previously unused perturbation values. Keep held-out outcomes completely excluded from null selection; preserve matched parent weights and control eligibility reporting.

**Authority:** `experiments/116_approximate_response_matching/{run.py,README.md,test_smoke.py,results/default.json}`. Exact physical nulls inherit from 115/113; parent reference from 112. No previous results or physics revised.
