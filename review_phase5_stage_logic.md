# Phase 5 Review: Stage-Specific Logic Checks
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 14 / 14

All re-run on the fixed panel (1,645 cells; sparse cells already dropped; corrected revenue series).

---

### CRITICAL ISSUES (must fix before submission)

**None** that aren't already captured as Critical in Phase 4. The items below are Important.

---

### IMPORTANT ISSUES (should fix)

**I5.1 — Stage 13B/13C run on only ~46% of the panel: `aesthetic_resid_mean` is NaN for 888/1,645 cells (14 of 25 brands entirely missing).** The Extension 8 residualisation (cell 56) builds its own `brand_map` that (a) renames "Christian Dior"→"Dior" and "Maison Margiela"→"Margiela" (which then fail to merge onto the panel's canonical names) and (b) **simply omits** Missoni, Alexander McQueen, Marni, Stella McCartney, Giorgio Armani, Fendi, Max Mara, Miu Miu, Ralph Lauren, Jean Paul Gaultier, Dolce & Gabbana, Dries Van Noten. Result: `aesthetic_resid_mean` is missing for those 14 brands.
- **Why it matters:** the resolution-correction conclusion — *"once image resolution is controlled, the recession effect on aesthetic quality disappears → the raw finding was a resolution confound"* — is estimated on a **non-random ~11-brand, 46%-of-cells subset**. That conclusion (which the thesis uses to *drop* the Stage 13 recession-on-quality result) is not established on the full panel. Stage 13 validation T8 only checks the column *exists*, not its coverage.
- **Fix:** use the canonical 25-brand map (reuse `name_to_canonical`/`tier_map`) so `aesthetic_resid_mean` covers all cells, then re-run 13B/13C and re-evaluate whether the resolution confound conclusion holds panel-wide.

**I5.2 — The `aesthetic` score's provenance is undocumented.** The column is a continuous score, range **[1.64, 8.67]**, mean 4.93, roughly symmetric (1/25/50/75/99 pct = 3.42/4.52/4.94/5.35/6.40), no floor/ceiling effect. But neither the notebook nor any companion file identifies **which model produced it** (Extension 8 was meant to establish provenance and does not). Using an undocumented third-party score as the *internal-validity instrument* for ARI is a soft spot a jury (Juror 3) will probe. **Fix:** trace the source (dataset README/paper/repo), name the model and its scale, or explicitly downgrade Stage 13 to "suggestive convergent evidence" and state the limitation.

**I5.3 — Stage 14's CLIP coherence result has FLIPPED SIGN and contradicts the thesis interpretation.** The thesis reports `recession` on `clip_within_sim` = **+0.016, p = 0.000** ("recession → more semantically coherent collections → creative retrenchment"). On the fixed data (COVID now in `recession`, sparse cells dropped, diagonal-corrected similarity) it is **−0.0093, p = 0.047** — recessions are associated with *lower* within-collection similarity (marginally significant), the **opposite** of the stated retrenchment story. `gdp_z` = −0.0057 (p = 0.0007) points the same (negative) way, so the two macro signals are also mutually inconsistent, suggesting a weak/noisy effect rather than a clean one.
- **Why it matters:** Stage 14 is presented as independent semantic confirmation of "creative retrenchment." It no longer confirms it. Also note `clip_within_sim` is **nearly orthogonal** to the colour metrics (r with `dispersion_mean` = −0.03, with `ARI` = −0.07) — good for independence (answers jury Q6: CLIP is *not* just measuring colour) but it means CLIP does **not** corroborate the colour-based findings; it is a separate, now-contradictory signal.
- **Fix:** either drop the "recession increases coherence" claim or report the corrected negative/insignificant result honestly. Update the Phase-7 number.

---

### MINOR ISSUES (nice to fix)

- **M5.1 — Stage 10C (leading indicator) is robustly null and entirely COVID-driven.** With the corrected revenue series, full-sample Pearson r = **−0.173, p = 0.42** (thesis: −0.287); **excluding the 2020–21 revenue targets, r = +0.031, p = 0.89** (essentially zero). The relationship vanishes without COVID and weakened further once the revenue figures were corrected. Keep it explicitly framed as null/exploratory; do not imply runway dispersion predicts luxury revenue.
- **M5.2 — Stage 10B (coherence) coefficient is unstable.** `recession` on `dispersion_std` moved from the reported +0.131 to **+0.346 (p = 0.111)** after dropping sparse cells and adding COVID — still insignificant, but a ~3× shift shows it's sensitive to specification. Report the current value and the null verdict.

---

### CHECKS PASSED (clean results)

**Stage 10A — Granger**
- Test direction is correctly labelled: `grangercausalitytests(tier_annual[['Luxury','Avant-garde']])` tests **Avant-garde → Luxury** (the 2nd column is the cause), matching the stated trickle-down hypothesis.
- **No time-series gaps:** `tier_annual` is complete (24 years 2000–2023, 0 NaN in all three tiers) — annual averaging produces no holes.
- All tests **null**: Avant-garde→Luxury p = {0.58, 0.77, 0.82}; Avant-garde→Accessible p = {0.87, 0.44, 0.32}; Luxury→Accessible p = {0.46, 0.51, 0.34}. The n = 24 underpowering is explicitly acknowledged. Correctly treated as exploratory.

**Stage 14 — CLIP mechanics** (cross-ref Phase 2)
- Model is **ViT-B-32, OpenAI pretrained** (cell 62), consistent throughout.
- `cosine_similarity` on unit-normalised vectors = dot product; **diagonal correctly excluded** in `clip_within_sim`; `clip_within_sim` has 0 NaN across 1,645 cells.

**Stage 13 — Aesthetic (raw)**
- `aesthetic` column present; range [1.64, 8.67] consistent with a ~1–9 quality scale; distribution ~normal, no ceiling/floor.
- `aesthetic_mean` has **0 NaN** across all 1,645 cells.
- **r(ARI, aesthetic_mean) = 0.365** (≈ reported 0.370); R² = 0.13 → *moderate* convergent validity (frame as moderate, not strong), confirming ARI tracks an independent quality score to a meaningful but partial degree.

---

### CROSS-PHASE FLAGS

1. **I5.3 (CLIP recession coef +0.016/p0.000 → −0.009/p0.047, sign flip)** → **Phase 7** numbers; **Phase 9** jury Q9 (CLIP appropriateness).
2. **I5.1 (Stage 13B/C 46% coverage)** and **I5.2 (aesthetic provenance)** → **Phase 8** Extension 8 and **Phase 9** Juror 3.
3. **M5.1 (leading indicator null)** → reinforces that Stage 10C is not a finding; relevant to Phase 1 I1.2 revenue note.
