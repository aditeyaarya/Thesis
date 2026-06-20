# Phase 7 Review: Presentation & Thesis-Readiness
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 7.1 numbers (15) + 7.2 jury (7) + 7.3 export (2) = all run

---

### 7.1 NUMBERS VERIFICATION TABLE (thesis-claimed → actual on fixed data)

| Quantity | Thesis claim | Actual now | Verdict |
|---|---|---|---|
| Total images in panel | 48,246 / 48,245 | sampled **48,101** / extracted **47,738** / CLIP **48,056** | ✗ none match — pick one denominator |
| Total cells | 1,657 | **1,645** | ✗ (12 sparse cells dropped) |
| Brands | 25 | 25 | ✓ |
| Year range | 2000–2024 | **2000–2023** | ✗ (24 years) |
| **Model 6 recession coef** | **−0.319, p=0.001** | **−0.08, p=0.49** | ✗✗ **headline gone** |
| Model 1-ARI recession | −0.223, p=0.009 | −0.224, **p=0.053** | coef ✓ / sig ✗ |
| ARI R² | 0.278 | 0.274 (M1-ARI) / 0.285 (M6) | ✓ |
| PC1 explained variance | 44.8% | 44.7% | ✓ |
| r(ARI, aesthetic) | 0.370 | 0.365 | ✓ |
| Bayesian max R-hat | 1.0021 | 1.0028 | ✓ (both <1.01) |
| **P(Luxury < Avant-garde)** | **0.834** | **0.465** | ✗✗ **tier story reversed** |
| **CLIP within-sim recession** | **+0.016, p=0.000** | **−0.009, p=0.047** | ✗ **sign flipped** |
| Bootstrap CI (Lux×rec interaction) | [−0.192, +0.363] | [−0.10, +0.39] | ✓ (interaction; incl. 0) |
| Event study GFC t=−2 | +0.363, p=0.000 | +0.351, p<0.001 | ✓ |
| Event study COVID t=+1 | −0.378, p=0.000 | −0.380, p<0.001 | ✓ |

**Pattern:** descriptive, PCA, event-study, and Bayesian-convergence numbers reproduce; the *headline inferential* claims (Model 6 lagged recession, P(Lux<AG), CLIP coherence sign, Model 1-ARI significance) and the basic counts (cells, years, images) do **not**. Every "2000–2024 / 1,657 cells / 48,246 images / Model 6 p=0.001 / P=0.834 / CLIP +0.016" statement in the draft must be corrected.

---

### CRITICAL ISSUES (must fix before submission)

(Carried from Phases 4–5 — restated here because they will appear as *written numbers*.)
- **Model 6 lagged-recession (−0.319/p0.001) is now −0.08/p0.49** — do not write the old figure.
- **P(Luxury < Avant-garde) is 0.465, not 0.834** — do not write the tier-heterogeneity claim.

---

### IMPORTANT ISSUES (should fix)

**I7.1 — The results workbook `vogue_runway_results.xlsx` is incomplete and likely stale.** It contains Model 1–5 (dispersion, Stage 9), Coherence, Granger, LeadingIndicator, etc., but **omits the now-central analyses**: Model 6, the ARI models, the event study, the TWFE, and the Bayesian model. It was also exported from an earlier cell (39), so its Model 1–5 numbers may predate the Phase-1 fixes. **Fix:** regenerate the workbook after re-running, and add sheets for Model 6, event study, and Bayesian posteriors.

**I7.2 — Basic-count and headline numbers in the draft will be wrong** (cells 1,657→1,645; years →2023; images denominator; Model 6; P(Lux<AG); CLIP sign; Model 1-ARI p). See table. These are "presentation" only in that they're already-known data facts, but a jury cross-checking the notebook against the text will find mismatches. Reconcile the entire numbers section against a fresh run.

---

### MINOR ISSUES (nice to fix)

- **M7.1 — Jury Q3 (segmentation efficacy) is not verifiable from saved artifacts.** `rembg`/U2Net is not installed and `color_metrics_raw.csv` stores no foreground/garment pixel counts or alpha fraction, so the ">30% of pixels removed" claim cannot be confirmed without re-running Stage 5. Log `n_foreground`, `n_garment`, `alpha_fraction` on the next extraction (ties to Phase 2 M2.1).

---

### CHECKS PASSED (clean results)

- **Excel export:** all prompt-listed sheets present and populated — Model1_MainEffects, Model2_TierInteractions, Model3_Lagged, Model4_LaggedTier, Model5_MixedEffects, ModelComparison, Coherence (×2), Granger, LeadingIndicator, BrandDispersionRanking, CellMetrics, MacroIndicators.
- **All 10 figures exist, are non-trivial (57–329 KB), and open without corruption** (e.g. event_study.png 2400×750, bayesian_forest_plot.png 2700×1500). All saved at dpi=150 per code.

---

### 7.2 JURY-PREP ANALYSES

**Q1 — Sample sensitivity (random 20 brands ×5).** Model 1-ARI recession coef stays **directionally stable** (−0.17 to −0.29) but **significance is fragile** (p significant in 2/5, marginal/insig in 3/5). Honest framing: the contemporaneous recession→lower-ARI effect is a *consistent direction, modest and not always significant* — matches the full-sample p=0.053.

**Q2 — Why LAB?** LAB `dispersion_mean` correlates only **moderately** with HSV-side metrics (saturation_std r=0.52, entropy 0.28, hue_conc −0.22), so colour-space choice is **not** innocuous (not r>0.9). The thesis should justify LAB perceptual uniformity explicitly; the full HSV-DV robustness lives in Phase 8 Extension 7.

**Q3 — Is segmentation removing backgrounds?** **Not verifiable from saved artifacts** (M7.1). Needs a Stage-5 re-run logging alpha fraction. Combined with Phase 2 I2.1 (skin barely excluded), segmentation quality is the weakest-evidenced part of the pipeline.

**Q4 — t=−2 pre-trend robustness (drop t=−2; t=−3 as sole pre-period).** **COVID is robust** — t=+1 = −0.342, p=0.001 holds; t=−3 insignificant (p=0.58). **GFC weakens** — t=+2 drops to −0.148, p=0.077 (from −0.201, p=0.014) and t=+1 insignificant. So the parallel-trends concern bites mainly the **GFC** result; the **COVID** post-shock drop is the robust event-study finding.

**Q5 — ARI = brand identity or year-to-year change?** **Within-brand variance = 88.1%** of total (ICC = 0.119). ARI overwhelmingly captures within-brand year-to-year change, not a static fingerprint — easily clears the 30% bar. Strong, favourable answer. (Caveat: some of that 88% is the cell-level noise flagged in Phase 3 I3.3.)

**Q6 — Photography vs colour (CLIP ⟂ dispersion)?** r(`clip_within_sim`, `dispersion_mean`) = **−0.03**, r(CLIP, ARI) = −0.07 — essentially orthogonal. CLIP is **not** just re-measuring colour (good for independence), but it therefore does not corroborate the colour findings (and now points the other way — Phase 5 I5.3).

**Q7 — Bootstrap symmetric/positive while main finding negative?** Confirmed: the bootstrap (and LOO) extract the **Luxury×recession interaction**, whose positive mean (+0.14) means Luxury is *less* conservative than the baseline tier in recessions — consistent with the insignificant tier interaction, **not** a contradiction of the (separate) negative main recession effect. (Phase 4 I4.3.)

---

### CROSS-PHASE FLAGS

1. All ✗/✗✗ rows feed the **Phase 9** verdict and the **Final report** numbers table.
2. **I7.1 (stale/incomplete workbook)** and **M7.1 (segmentation logging)** are quick fixes for the Final prioritised list.
