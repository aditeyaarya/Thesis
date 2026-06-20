# Phase 6 Review: Statistical Validity Checks
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 9 / 9

All on the fixed panel (1,645 cells). The "primary family" for multiple-testing uses the
*surviving* findings (Phase 4), since the thesis's stated primary (eu_recession_lag1) is now null.

---

### CRITICAL ISSUES (must fix before submission)

**None.**

---

### IMPORTANT ISSUES (should fix)

**I6.1 — No multiple-testing correction is reported, and it matters for the borderline results.** The pipeline runs 50+ hypothesis tests across Stages 9–15. Applying corrections to a pre-specified primary family (current p-values):

| Hypothesis | raw p | Bonferroni | BH (FDR) |
|---|---|---|---|
| `ecb_z_lag1` (Model 6) | <0.0001 | **0.000** ✓ | **0.000** ✓ |
| `eu_gdp_z_lag1` (Model 6) | 0.0029 | **0.014** ✓ | **0.005** ✓ |
| Event study COVID t=+1 | <0.001 | **0.000** ✓ | **0.000** ✓ |
| Event study GFC t=+2 | 0.014 | 0.070 ✗ | **0.017** ✓ |
| Contemp. recession→ARI (Model 1-ARI) | 0.053 | 0.264 ✗ | 0.053 ✗ |

- **Takeaway:** the **lagged ECB-rate, lagged EU-GDP, and COVID post-shock drop survive even Bonferroni**; GFC t=+2 survives BH but not Bonferroni; the contemporaneous recession→ARI effect (already only p=0.053) does **not** survive any correction. The thesis's *originally* claimed primary (eu_recession_lag1, "p=0.001") is moot — it is now p=0.49.
- **Fix:** declare 3–5 pre-specified primary hypotheses, report Bonferroni/BH-adjusted p-values, and frame the surviving family (ECB, EU-GDP, COVID event) as the robust core. Treat everything else as exploratory.

**I6.2 — The Avant-garde tier annual ARI series is borderline non-stationary (ADF p = 0.087).** The panel-stacked ARI is firmly stationary (ADF p < 0.0001), and Luxury (p < 0.0001) and Accessible Luxury (p = 0.013) tier-annual series are stationary — so the main brand+season-FE regressions are **not** spurious. But the Avant-garde tier-annual series has a possible unit root/trend, which — together with n = 24 — further undermines the **tier-level Granger (10A) and leading-indicator (10C)** time-series analyses (already null/exploratory). **Fix:** add a note; if any tier-level time-series claim is retained, difference or de-trend first.

---

### MINOR ISSUES (nice to fix)

- **M6.1 — Panel is mildly unbalanced.** Obs/brand: mean 65.8, min 42 (Rick Owens), max 78 (Christian Dior). **4 brands > 20% below the mean:** Rick Owens (42), Dries Van Noten (46), Dolce & Gabbana (48), Maison Margiela (48) — mostly Avant-garde, driven by fewer Pre-Fall/Resort pre-collections. Not extreme; note it and rely on the balanced-panel robustness (below).

---

### CHECKS PASSED (clean results)

**6.2 Autocorrelation**
- **Durbin–Watson = 1.701** on Model 6 residuals (ordered brand-year) — within the acceptable [1.5, 2.5] band, **not** flagged. Within-brand residual AR(1) is mild (r = 0.15). The notebook already reports **Newey–West HAC (maxlags = 2)** for Model 6, which appropriately handles the residual serial correlation, so HC3 is adequately backstopped. No HAC gap.

**6.3 Stationarity**
- Panel-stacked ARI **stationary** (ADF p < 0.0001); Luxury and Accessible Luxury tier-annual series stationary. The cell-level dependent variable used in all FE regressions is stationary → regression results are not spurious. (Only Avant-garde tier-annual is borderline — see I6.2.)

**6.4 Panel balance**
- **24 of 25 brands are present in every year 2004–2023** — the panel is well-balanced from 2004 onward.
- **Correct balanced-panel robustness re-run** (24 brands, 2004–2023, N = 1,423; this is the *fixed* version of the broken Stage 9B Check 5, Phase 4 I4.1): `ecb_z_lag1` = **−0.096, p = 0.0005** (robust) and `eu_recession_lag1` = −0.117, **p = 0.324** (null) — both **consistent with the full-panel result**. The surviving ECB finding is robust to panel balance; the dead recession-dummy finding stays dead. This doubles as Phase 8 Extension 2.

---

### CROSS-PHASE FLAGS

1. **I6.1 (multiple testing)** → **Phase 7** numbers and **Phase 9** Juror 1 ("p-hacking / 50+ tests"). The surviving primary family (ECB, EU-GDP, COVID event) clears Bonferroni — lead with it.
2. **Balanced-panel re-run** satisfies **Phase 8 Extension 2** (ECB effect robust; recession-dummy null in balanced panel).
3. **I6.2 (Avant-garde non-stationarity)** reinforces the null status of Stage 10A/10C (Phase 5).
