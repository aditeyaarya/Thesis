# Phase 7 Review: Fast-Fashion Placebo Audit
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 9 / 9

---

### HEADLINE: The placebo is technically clean and intellectually honest. The PBI basis projection is exact, and the interaction p-values reproduce to the decimal. The weaknesses are conceptual (power + brand labelling), and the writeup already concedes them.

---

### CRITICAL ISSUES (must fix before submission)
None found.

### IMPORTANT ISSUES (should fix)

**1. The placebo is underpowered to the point where its "minimum detectable difference" ≈ the entire luxury effect.**
- *Problem (quantified):* With 5 fast-fashion brands the interaction SE = 0.0396, so the ~80%-power minimum detectable interaction is **≈ 0.11 PBI units**. The luxury lagged-ECB slope is only **≈ 0.08–0.10**. A *fully* luxury-specific effect (FF slope ≈ 0, luxury ≈ −0.10) would be a difference of ~0.10 — **right at the edge of what the test can detect.** So the placebo cannot rule out even a practically-large luxury-specific mechanism.
- *Why it matters:* Juror 1/2 (prep Q7) will ask for the MDE. The honest answer is "≈0.11, comparable to the effect we're trying to attribute" — which means "no evidence of a difference" is the *only* defensible claim, not "the effect is industry-wide" stated as established fact.
- *Fix:* Report the MDE (~0.11) explicitly and soften "industry-wide" to "no evidence of a luxury-specific differential; the test is underpowered (MDE ≈ 0.11 ≈ the luxury effect size), so industry-wide co-movement is the most parsimonious reading, not a proven one." The md already says "no evidence of a difference, not proven equality" — add the number.

**2. "Fast-fashion" is a misnomer for Tommy Hilfiger / Tory Burch (brand-labelling, prep Q3).**
- *Problem:* Tommy Hilfiger and Tory Burch run structured seasonal collections, not Zara/H&M weekly drops. The placebo's logic depends on these brands having a *materially shorter design lead time* than luxury; that contrast is weak if they too plan 6–9 months out. The md's own term "accessible/contemporary, short-cycle" is more accurate than "fast-fashion."
- *Why it matters:* Juror 2 will say the placebo never created the production-calendar contrast it claims to test, so a null interaction is unsurprising and uninformative about the mechanism.
- *Fix:* Rename throughout to "accessible/short(er)-cycle brands," state their approximate design lead times vs luxury, and acknowledge the contrast is in lead-time *gradient*, not a true fast-fashion vs luxury dichotomy. This strengthens, not weakens, the honest framing.

**3. Mechanism void (shared with Phase 4).** The placebo rejects the production-calendar story but supplies no replacement for why a 1-year lag fits short-cycle brands. Same fix as Phase 4 Important #1 — name candidate industry-wide channels (consumer sentiment, retail-buying conditions, shared colour-forecasting/Pantone-WGSN cycles, which the md already gestures at) and concede the mechanism is not identified.

### MINOR ISSUES (nice to fix)

**1. Cell-count wording.** The md says "191 usable cells"; `fast_fashion_panel_full.csv` has **195** rows (Isabel Marant 41, Lacoste 33, Tommy Hilfiger 38, Tory Burch 60, Vanessa Bruno 23). The 4-cell gap is the 2000/NaN-lag rows dropped when `ecb_z_lag1` is required. State "195 cells, 191 with a valid lagged regressor."

**2. Asymmetry consistency not shown for FF.** The monetary deep-dive finds tightening (not easing) drives the luxury effect. The writeup does not check whether the same asymmetry holds in the fast-fashion panel. If it does, that *strengthens* the industry-wide reading; if it doesn't, that's worth knowing. Add the FF tightening/easing split or note it as future work.

### CHECKS PASSED

**7.1 File existence** — `fast_fashion_panel_full.csv`, `fast_fashion_cell_metrics.csv`, `fast_fashion_comparison_results.md` all present (Phase 1). ✓

**7.2 Brand coverage** — all 5 brands present; cell counts 23–60, **none below 5**. Coverage spans both GFC (≤2011) and COVID (≥2017) windows. FF ARI mean 0.226. ✓

**7.3 PBI basis consistency — EXACT PASS (the critical Juror-3 check).**
- Recomputing FF PBI by projecting `fast_fashion_cell_metrics.csv` onto the **luxury** StandardScaler + PCA basis and z-scoring against the **luxury** distribution reproduces the saved FF ARI with **corr = 1.000000, max|diff| = 0.000000**. The PCA was **not** refit on the combined dataset; luxury PBI values are unchanged. ✓

**7.4 Interaction test — EXACT reproduction.**
- Common-scale pooled spec (`PBI ~ ECB_lag * fast_fashion + brand FE + season FE`, year-clustered, N=1,796, 23 clusters): **interaction = −0.0432, p = 0.3610** (thesis: −0.043, 0.36 ✓). Luxury slope **−0.0801**, FF slope **−0.1233** (thesis −0.08/−0.12 ✓). FF slope is *steeper* than luxury → no luxury-specificity.
- The review-brief's per-panel-z spec gives interaction +0.018, p=0.65 — also null. Conclusion (no differential) is robust to either scaling. (Wild bootstrap p=0.84 reported in the md; the standard p alone already settles it.)

**7.5 Logical validity of the reframing** — see Important #1 (power), #2 (labelling), #3 (mechanism). The writeup's core claims ("not luxury-specific," "no evidence of difference, not proven equality," "drop production-calendar as validated") are individually defensible and honestly stated.

### CROSS-PHASE FLAGS
- Mechanism void recurs (Phase 4, Phase 11 Q5) — one fix covers all three.
- Power/MDE limitation is the substance of Phase 11 Q7.
- The fast-fashion result is the empirical driver of H3's "industry-wide" framing → feeds Phase 8 heterogeneity and the Phase 11 grade on Results Validity.
