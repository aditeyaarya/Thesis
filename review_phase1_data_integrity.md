# Phase 1 Review: Data Integrity & Panel Construction
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 18 / 18

---

### CRITICAL ISSUES (must fix before submission)
None found.

### IMPORTANT ISSUES (should fix)

**1. Panel ends in 2023, but the thesis claims a 2000–2024 sample.**
- *Problem:* `panel_full.csv` year range is **2000–2023**. `macro_indicators.csv` correctly spans 2000–2024 (25 rows), but no runway cells exist for 2024. The abstract/intro states "2000–2024."
- *Why it matters to a jury:* A reviewer who counts years or looks for 2024 collections will find them absent. A one-year overstatement of the sample window is the kind of small factual slip that erodes trust in the larger numbers.
- *Fix:* Either (a) change all prose to "2000–2023" (image data) while noting macro covers 2000–2024 to support the 2023 lag, or (b) explicitly state "runway data 2000–2023; 2024 macro retained only to construct lagged regressors." One sentence in the data section resolves it.

### MINOR ISSUES (nice to fix)

**1. `cd_change` covers a 2-year window (change year + following year).**
- *Observation, not a defect:* The review's `EXPECTED_CD` lists only change years, but the notebook (Cell 55) deliberately codes `cd_change=1` for "the year of CD change **and the year after (transition effects)**." Every brand therefore shows `[Y, Y+1]`. This is documented in the code comment and is a defensible modeling choice (a new creative director's first full season).
- *Fix (optional):* Add one sentence in the methods prose stating the 2-year transition window so a jury does not read the wider flag set as an error. Total flagged = 141 cells (8.6% of 1,645) — slightly below the 10–15% the review anticipated, fully explained by the design.

### CHECKS PASSED

**1.1 Panel construction**
- Rows = **1,645** (exact match).
- All **25 brands** present; tier assignments match exactly (Luxury 12, Accessible Luxury 7, Avant-garde 6). No missing/extra brands.
- Year range 2000–2023 (no out-of-range values). Seasons = {Fall, Pre-Fall, Resort, Spring}. (`section` filter applied upstream; no `section` column in panel.)
- Three dropped sparse cells confirmed **absent**: JPG 2008 Resort, Burberry 2000 Fall, Burberry 2019 Resort.
- Duplicate `(brand, year, season)` = **0**.
- `n_images` minimum = **15**; zero cells below 15.
- `bw_collection` = exactly **3** cells, all Saint Laurent: 2013 Pre-Fall (lab_entropy 0.284), 2014 Resort (0.051), 2021 Resort (0.043) — all anomalously low vs SL range 0.043–2.968. Matches spec.

**1.2 Macro indicators**
- `macro_indicators.csv` = 25 rows, 2000–2024, **no NaN**.
- EU recession dummy = 1 for **2011, 2012, 2013 only**; 2010 = 0. ✓
- US/NBER recession = 1 for **2001, 2008, 2009, 2020**; 2021 = 0. ✓
- `ecb_rate` is **negative for 2014–2021** (min −0.50 in 2020/21). The FRED pull is correct (ECB Deposit Facility Rate). ✓
- Lag construction verified: `eu_recession_lag1[T]` = `eu_recession[T−1]` for Chanel, Gucci, Prada. Year-2000 lags all NaN. All 4 season-rows of a brand-year share one `ecb_z_lag1` value (year-level lag). ✓

**1.3 CD change controls**
- `cd_change` present; 141 cells flagged (8.6%). Construction matches the documented 14-brand `CD_CHANGES` dict + 1-year transition window.
- Brands not in the dict (Rick Owens, Missoni, Ralph Lauren, etc.) have **zero** flagged cells. ✓

**1.4 External files**
- All four present: `wild_bootstrap_results.md`, `fast_fashion_comparison_results.md`, `fast_fashion_panel_full.csv`, `fast_fashion_cell_metrics.csv`. ✓

### CROSS-PHASE FLAGS
- The 2-year `cd_change` window feeds Models 6/7 (Phase 4) — confirm the coefficient interpretation prose reflects a transition *window*, not a single-year shock.
- 2023 vs 2024 sample-window wording recurs in Phase 10 numbers/framing checks — fix once, propagate.
