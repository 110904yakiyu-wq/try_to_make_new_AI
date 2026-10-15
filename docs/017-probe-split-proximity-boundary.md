# 017 — Five-fold raw-probe rotation does not eliminate source-patch proximity confounding

**Experiment 117 (completed)** evaluates exactly the Experiment 116 fully physically matched null repertoire of 57 G0 transplant patches and 506 alternative bit assignments. In five predeclared disjoint three-value training splits covering raw values 1..15, the selected nearest early-response controls are evaluated on the other 12 values per support boundary. Fold 0 is identical to 116 and passes a direct regression assertion.

Parent-averaged tick-24 heldout-response Jaccard donor-minus-nearest-null varies by train fold: width 1 +0.00980 .. +0.04336 (15 parents); width 2 −0.01112 .. +0.09374 (10 parents); width 3 +0.12965 .. +0.15854 (16 parents). Eight width-3 parents show positive differences across all five folds, two show negative differences across all folds and six change signs. This is not five independent replications; entire parent cohort and physical null sets are reused.

**Identification warning:** Donor transplant copies **exact source G0 bits at patch locations**, whereas null construction **explicitly excludes** that exact patch assignment. Outside the patch donor and alternative are identical to recipient. Thus every alternate microstate must differ in at least one of the G0 patch bits, creating a deterministic raw-Hamming proximity advantage for donor in the very state used as the heldout target. This alone can affect response similarity and cannot be controlled by varying train probe values. The persistent width-3 effect is compatible with ordinary deterministic Markovian microstate sensitivity. It is not evidence for a distributed 'code', self-maintenance, cognitive causality, reproduction, or learning.

**Next:** Quantify this structural overlap failure and separately test whether raw-distance compensated replacements are possible with a broader edit budget; preselect eligibility before examining response outcomes. Negative/empty support must be preserved.

Authorities: `experiments/117_probe_split_robustness/`, with 104/108/112/113 matching and 116 nearest-control semantics. No physics revision.
