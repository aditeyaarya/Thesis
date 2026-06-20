# Phase 8 Review: Extensions
## Status: COMPLETE
## Date: 2026-06-02
## Extensions Run: 8 / 8

Several extensions were already executed during Phases 4–7; results are consolidated here.

---

### EXTENSIONS COMPLETED

**Extension 1 — Newey–West HAC SEs on Model 6 (HIGH).** Re-ran Model 6 with `cov_type='HAC', maxlags=2`. The surviving effects are robust to autocorrelation: `ecb_z_lag1` = −0.099, **p = 0.0001** (HC3: p < 0.0001); `eu_gdp_z_lag1` p = 0.004. The lagged-recession dummy stays null (HAC p = 0.51). **Verdict:** HAC eliminates the autocorrelation concern for the *surviving* (ECB/GDP) findings; it does not revive the recession dummy.

**Extension 2 — Balanced panel 2004–2023 (HIGH).** Proper re-run (24 brands present every year, N = 1,423; this is the corrected version of the broken Stage 9B Check 5): `ecb_z_lag1` = −0.096, **p = 0.0005** (robust); `eu_recession_lag1` = −0.117, **p = 0.32** (null) — both consistent with the full panel. **Verdict:** the ECB effect is robust to panel imbalance; the recession-dummy null is not an artifact of unbalanced early years.

**Extension 3 — Creative-director controls (MEDIUM).** `cd_change` added to Model 6; coefficient ≈ +0.07, **p ≈ 0.48** (insignificant), and the surviving ECB/GDP effects are unchanged. **Caveat (bug, Phase 4 I4.2):** the `CD_CHANGES` dict uses non-canonical names ("Dior", "Margiela", "Bottega Veneta", "Issey Miyake"), so Christian Dior's and Maison Margiela's CD changes are never flagged — only 8 of 12 intended brands get the control. **Verdict:** CD changes do not confound the findings, but fix the brand names so the control is honestly specified.

**Extension 4 — Corrected EU dummy (2011–2013 vs 2010–2013) (MEDIUM).** With a proper year-based lag: 2011–2013 (CEPR, current) `eur_lag` = −0.083, **p = 0.48**; 2010–2013 (old) `eur_lag` = −0.153, **p = 0.14**. **Both codings are null**, and `ecb_z_lag1` stays p < 0.0001 in both. **Verdict:** the headline does not return under the looser 2010–2013 coding — confirming it was the lag-by-season *bug* (Phase 1 C1.1), not the dummy years, that produced the original "p = 0.001." Keep the CEPR-aligned 2011–2013 coding as primary.

**Extension 5 — CLIP diagonal fix (MEDIUM).** Recomputed across all 1,645 cells: mean off-diagonal `clip_within_sim` = 0.8559 vs mean full-matrix (diagonal-inclusive) = 0.8609 — a **+0.0050** upward bias if the diagonal were kept (mean cell n = 29.2, so ≈ (1−0.856)/29). The shift is **below the 0.01 threshold**, and the notebook **already uses the off-diagonal mean (correct)**. **Verdict:** no action — the fix is in place and the residual bias it removes is small.

**Extension 6 — Within vs between-brand ARI variance (MEDIUM).** Within-brand SS = **88.1%** of total, between (ICC) = **0.119**. **Verdict:** ARI is overwhelmingly within-brand year-to-year variation (≫ 30% bar) — it is not a static brand fingerprint, which supports within-brand identification of macro effects. (Caveat: part of the 88% is the cell-level noise flagged in Phase 3 I3.3.)

**Extension 7 — Colour-space robustness (LOW).** Contemporaneous `recession` on standardised DVs (brand+season FE):

| DV | recession coef | p |
|---|---|---|
| ARI (LAB PCA) | −0.224 | 0.053 |
| dispersion_mean (LAB) | −0.367 | 0.004 |
| saturation_mean (HSV) | −0.192 | 0.127 |
| lab_entropy_mean | −0.153 | 0.225 |
| hue_conc_mean (↑=conservative) | +0.031 | 0.84 |
| value_mean (↑=conservative) | +0.026 | 0.83 |

**Verdict:** the recession→conservatism *direction* is **consistent across LAB and HSV** (boldness metrics negative, conservatism metrics positive), so the finding is **not a LAB-space artifact** — but significance is concentrated in `dispersion`/ARI; the individual HSV metrics are directionally right yet insignificant, underscoring that the effect is modest.

**Extension 8 — Aesthetic score provenance (LOW).** The `aesthetic` column remains **undocumented** (no README/paper/repo identifying the scoring model); range [1.64, 8.67], ~normal, no floor/ceiling (Phase 5 I5.2). Additionally, the resolution-residualised version `aesthetic_resid_mean` (used in Stage 13B/13C) is **missing for 14 of 25 brands / 888 cells (54%)** due to a brand-map bug (Phase 5 I5.1), so the "resolution confound" conclusion is built on a ~46% subset. **Verdict:** trace and document the score's source, fix the Stage 13 brand map, and re-evaluate; otherwise flag Stage 13 as suggestive only.

---

### CRITICAL ISSUES
None new (all criticals are in Phases 4/7).

### IMPORTANT ISSUES
- **I8.1** — Extension 3 CD-control and Extension 8 Stage-13B brand-map bugs must be fixed for the controls/conclusions to be valid (cross-ref Phase 4 I4.2, Phase 5 I5.1).

### MINOR ISSUES
- **M8.1** — Once the surviving model is finalised, regenerate the results workbook to include the extension outputs (Phase 7 I7.1).

### CHECKS PASSED
- Extensions 1, 2, 5, 6 confirm the surviving findings (ECB/GDP lag effects, ARI within-brand variation) are robust; Extension 4 confirms the dead recession-dummy is genuinely null under both codings; Extension 7 confirms colour-space independence of the direction.

---

### CROSS-PHASE FLAGS
1. Extensions 1/2/4 reinforce the **Phase 4** conclusion: the robust core is **lagged ECB/EU-GDP + the COVID event study**, not the recession dummy.
2. Extension 8 + I8.1 feed the **Phase 9** Juror-3 questions and the Final fix list.
