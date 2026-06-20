# Phase 3 Review: PCA and ARI Construction
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 13 / 13

PCA re-fit from `cell_metrics.csv` (1,645 cells) exactly as the notebook does; ARI re-derived and
compared to the saved `panel_full.ARI`.

---

### CRITICAL ISSUES (must fix before submission)

**None found.** The PCA mechanics are all correct. The issues below are about *interpretation and construct validity*, which a jury will press hard on.

---

### IMPORTANT ISSUES (should fix)

**I3.1 — Parallel analysis and Kaiser's rule both say retain 3 components, not 1; PC1 is only 44.7% of variance.** Horn's parallel analysis (200 random permutations) gives real vs random eigenvalues: PC1 3.13 vs 1.11, **PC2 1.58 vs 1.06, PC3 1.31 vs 1.03** (all three real > random → retain), PC4 0.44 vs 1.00 (drop). Kaiser (eigenvalue > 1) agrees: PC1–PC3 all > 1. PC2 (22.6%) and PC3 (18.7%) together carry **41%** of the color-metric variance and are *interpretable*, not noise:
  - **PC2** loads + on `hue_conc_mean` (0.62) and `saturation_mean` (0.35), − on `lab_entropy_mean` (−0.50)/`dispersion_mean` (−0.33): a **"vivid-but-monochromatic vs muted-multicolour" axis** (palette focus).
  - **PC3** loads + on `dispersion_mean` (0.61), `saturation_std` (0.44), `value_mean` (0.38): a **"high-contrast / variegated" axis**.
- **Why it matters:** The thesis uses PC1 alone as the ARI, discarding two statistically- and substantively-meaningful dimensions. Jury question 1 ("why is PC1 the right component? could PC2/PC3 be more relevant to aesthetic risk?") is directly on point — and the data answers "PC1 is the largest but not the only signal." This is defensible *if* framed as "PC1 = an overall colour-boldness index," but the thesis must (a) report that 3 components are retainable, (b) justify PC1 on theoretical/face-validity grounds rather than implying a scree elbow at 1, and ideally (c) show the main result is robust to using PC2/PC3 or a multi-component score.
- **Fix:** add the parallel-analysis result to the methodology; reframe ARI as "PC1, the dominant colour-boldness axis (44.7%)"; optionally re-run Model 6 with PC2 and PC3 as additional DVs/controls to show the recession effect is specific to PC1.

**I3.2 — ARI has real face-validity gaps; it is a *colour-boldness* index, not "aesthetic risk" in the conceptual sense.** Brand ranking (mean ARI, low = conservative):
  - **Missoni ranks 11/25 (ARI −0.04), below average** — yet Missoni is the archetypal vivid/maximalist knitwear house. Expected near the top; it isn't. **Face-validity failure.**
  - **Maison Margiela ranks 16/25 (ARI +0.05), above average** — yet Margiela is conceptually avant-garde with a famously muted/deconstructed palette. Expected near the bottom; it isn't. **Face-validity failure.**
  - **Balenciaga ranks 4/25 (most conservative quartile)** — colour-wise defensible, but this is precisely Jury question 4: a house widely read as avant-garde scores "conservative." Must be pre-empted.
  - Structurally, the **Avant-garde tier sits in the middle**, while **Luxury is the *boldest* tier and Accessible Luxury the most conservative** (tier × quartile: Luxury 29.4% in Q4 / 19.0% in Q1; Accessible Luxury 35.8% in Q1). The intuitive "avant-garde = boldest" ordering does not hold because ARI captures colour saturation/lightness, whereas avant-garde risk is largely about *silhouette, deconstruction and concept* — which the colour pipeline cannot see.
- **Why it matters:** Juror 2 (luxury management) will argue ARI measures palette, not "aesthetic risk." The construct claim must be narrowed to "colour boldness / palette conservatism," and the Balenciaga/Margiela/Missoni cases addressed explicitly. The well-behaved extremes (Dolce & Gabbana 25/25, JPG 23/25, Ralph Lauren 1/25, Marni 2/25) support the colour interpretation.
- **Fix:** rename/re-scope the construct ("Palette Boldness Index" or explicitly "colour-based aesthetic risk"), and add a paragraph reconciling the avant-garde-but-muted houses.

**I3.3 — ARI is volatile at the cell level; ~14% of cells show year-over-year jumps > 1.5σ, concentrated in pre-collections.** Within brand-season, **239 cells** jump > 1.5 ARI units vs the previous year, several enormous (Givenchy Spring 2022 +4.27, Saint Laurent Pre-Fall 2016 +4.04, Stella McCartney Resort 2019 −3.82). Many of the largest sit in **Resort/Pre-Fall** pre-collections (smaller, lookbook-style, different photography) and around known CD changes (Saint Laurent 2016 Vaccarello, Gucci 2015 Michele). This volatility cuts both ways: it gives the within-brand identification power the thesis relies on (Extension 6), but it also signals measurement noise/heterogeneity from mixing main runway shows with pre-collections.
- **Fix / check:** verify the largest jumps against CD changes vs artifacts; consider a robustness run excluding Pre-Fall/Resort (main Spring/Fall only) to confirm the macro results survive. **CROSS-PHASE FLAG → Phase 4 / Phase 8.**

---

### MINOR ISSUES (nice to fix)

- **M3.1 — `mean_L` (−0.48) and `value_mean` (−0.46) are near-duplicate loadings** (recall cell-level r = 0.984 from Phase 1). They jointly dominate the negative side of PC1, effectively double-weighting "lightness/paleness." Consider dropping one or combining them, and note the redundancy.

---

### CHECKS PASSED (clean results)

- **No data leakage in scaling:** `StandardScaler` is fit on `cell_metrics[METRICS]` only (cell 41); no macro/panel_full variables enter the scaler.
- **7 input metrics correct:** `dispersion_mean, lab_entropy_mean, mean_L, saturation_mean, saturation_std, value_mean, hue_conc_mean`. **`hue_mean` (circular) is correctly excluded.**
- **PC1 explained variance = 44.74%** (matches reported 44.8%, ≥ 40%). **PC2 = 22.56%, PC3 = 18.73%** (match reported 22.5% / 18.7%).
- **PC1 loadings all in the theoretically expected direction after sign flip:** positive — `saturation_std` (0.43), `saturation_mean` (0.40), `lab_entropy_mean` (0.35), `dispersion_mean` (0.22); negative — `mean_L` (−0.48), `value_mean` (−0.46), `hue_conc_mean` (−0.22). (Higher hue concentration = more monochrome = conservative → correctly loads negative on bold ARI.)
- **Sign flip correct and consistent:** `ARI_raw = −PC1`, so paleness/lightness load negative and saturation positive, as intended.
- **ARI z-scored after flip:** mean = −0.0000, std = 1.0000 (3 dp). `panel_full.ARI` identical (mean −0.0000, std 1.0000).
- **No NaN in ARI** across all 1,645 cells (panel and cell_metrics agree, n = 1,645).
- **Tier–ARI multicollinearity check:** only **19.0%** of Luxury cells fall in Q1 (not the >70% the prompt warned about); the tier–ARI relationship is real but moderate and runs *opposite* to intuition (Luxury boldest) — no degenerate collinearity, and within-brand FEs identify the recession effect regardless.

---

### CROSS-PHASE FLAGS

1. **I3.1 (1 vs 3 components)** → **Phase 9** Jury question 1; consider a multi-component robustness run.
2. **I3.2 (ARI = colour boldness, not conceptual risk; Balenciaga/Margiela/Missoni)** → **Phase 9** Juror 2 + Jury question 4.
3. **I3.3 (cell-level ARI volatility, pre-collections)** → **Phase 4** (identification / Extension 6) and **Phase 8** (robustness excluding pre-collections).
4. **M3.1 (mean_L ≈ value_mean)** continues the Phase 1 M1.1 collinearity note.
