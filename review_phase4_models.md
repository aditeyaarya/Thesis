# Phase 4 Review: Regression Models — H1, H2, H3
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 17 / 17

---

### CRITICAL ISSUES (must fix before submission)
None found.

### IMPORTANT ISSUES (should fix)

**1. Mechanism void for the industry-wide 1-year lagged ECB effect (theoretical, not statistical).**
- *Problem:* H2 is now correctly framed as "industry-wide monetary/credit co-movement," and the production-calendar story is explicitly rejected (good). But removing the production-calendar mechanism removes the *reason* a 1-year lag is the right horizon. No markdown cell yet supplies an alternative theory for why palette boldness tracks *last year's* ECB rate across the whole industry.
- *Why it matters to a jury:* This is the single hardest question in the thesis (Juror 2/3, prep Q5). A significant, replicated lag with no mechanism reads as a correlation in search of a story.
- *Fix:* Add a short "Mechanism" paragraph offering candidate channels — credit availability → creative/marketing budgets set a season ahead; consumer-sentiment transmission; advertising-spend interest-rate sensitivity — and explicitly state the mechanism is not identified by this design. Honest acknowledgment + 2–3 candidate channels is sufficient at MSc level.

**2. EU-GDP "control vs channel" language is implied but not stated precisely (prep for Q1).**
- *Problem:* Markdown demotes lagged EU-GDP ("+0.08, p=0.03 under standard clustering; does not survive the wild bootstrap, p≈0.50") — good. But it does not explicitly say *eu_gdp_z_lag1 is retained in Model 6 as a control to avoid omitted-variable bias, not interpreted as an independent channel.* A juror will ask why it is still in the formula.
- *Fix:* One sentence in the H2 section: "We retain lagged EU-GDP as a macro control; its HC3/clustered significance is a low-cluster false positive (fails the wild bootstrap, p≈0.50) and we do not interpret it as a channel."

### MINOR ISSUES (nice to fix)

**1. Reference tier not stated explicitly.** Patsy orders tiers alphabetically → reference = **Accessible Luxury** (confirmed). No markdown cell says so (0 matches). Add one line so the `eu_recession_lag1:C(tier)[T.Luxury]` / `[T.Avant-garde]` coefficients are unambiguously read as *relative to Accessible Luxury*.

**2. Two SE versions of Model 6 coexist.** Cell 55 fits an HC3 version of the H2 formula; cells 57/58/68 (Stage 18) fit the **year-clustered** version that the thesis cites (prints literally say "year-clustered SEs"). The cited headline reproduces only under clustering. Label cell 55 clearly as exploratory/superseded so a reader who runs it does not quote the HC3 p-value.

### CHECKS PASSED

**4.1 SE strategy**
- Macro/H2 models (Model 6, monetary deep-dive, heterogeneity) use **`cov_type='cluster', groups=year`** (`g='year'` in cells 57/58/68). ✓ Correct for year-level regressors.
- Model 7 / robustness use HAC `maxlags=2` as an additional conservative check (6 HAC uses found). ✓
- Event-study brand-clustering verified in Phase 5.

**4.2 Model 6** (`ARI ~ eu_recession_lag1 + eu_recession_lag1:C(tier) + eu_gdp_z_lag1 + ecb_z_lag1 + cd_change + C(brand) + C(season)`), N=1,603, 23 year clusters:
- **`ecb_z_lag1` = −0.1034, year-clustered p = 0.0019** → matches thesis claim (coef −0.10, p=0.002). ✓
- `eu_gdp_z_lag1` = +0.0767, p=0.0320 (significant under clustering — the value the wild bootstrap later demotes). ✓
- `eu_recession_lag1` = −0.085 (p=0.42); tier interactions null (Avant-garde −0.046 p=0.63, Luxury −0.018 p=0.89) → H3 tier-null supported.
- Reference tier = **Accessible Luxury** (patsy alpha order). ✓
- `corr(ecb_z_lag1, eu_gdp_z_lag1) = +0.127` → not collinear. ✓
- VIF (non-FE): all low — max 3.60 (eu_recession_lag1), ECB 1.05, EU-GDP 1.03. Panel-structure inflation concern did **not** materialise. ✓
- `cd_change` = −0.051, p=0.36 (not significant) → CD transitions do **not** confound the recession/ECB finding. ✓

**4.3 Model 7** (`ARI ~ rec_x_lux + rec_x_al + cd_change + C(brand) + C(season_year)`, HAC maxlags=2), N=1,603, 77 season-year dummies, within-R²=0.351:
- `rec_x_lux` = +0.052 (p=0.72), `rec_x_al` = +0.065 (p=0.70) → both null → confirms the tier null (H3), not a primary H2 test. ✓

**4.4 H2 framing consistency**
- Abstract (cell 0) states H2 is **industry-wide**, H3 rejected. ✓ (8 "industry-wide" mentions.)
- All 3 "production-calendar" mentions are explicit **rejections** ("tested whether... it is NOT... so H2 is industry-wide"; "we do not read the lagged-ECB effect as a luxury production-calendar mechanism"). No stale luxury-mechanism framing remains. ✓
- Fast-fashion result (interaction p=0.36) cited **in the H2 body**, not buried. ✓ (8 fast-fashion mentions, 24 wild-bootstrap mentions.)

**4.5 Contemporaneous null framing**
- Contemporaneous recession → **ARI**: coef −0.224, HC3 p=0.053 (borderline, *not* <0.05), year-clustered **p=0.141 (null)**. The thesis correctly treats the composite contemporaneous effect as failing clustering.
- Contemporaneous recession → **dispersion**: coef −1.77, HC3 p=0.004, clustered p=0.006 (significant both ways) — the contemporaneous signal lives in raw spread, not the composite.
- Headline H1 therefore correctly rests on the event study / stacked DiD, not contemporaneous OLS. ✓

### CROSS-PHASE FLAGS
- Mechanism-void (Important #1) is re-examined in Phase 7 (fast-fashion) and Phase 11 (Q5) — fix once.
- EU-GDP Bonferroni-vs-wild-bootstrap tension is the Phase 6/9 reconciliation; the control-language fix here is its prose counterpart.
- PC3 contemporaneous recession significance (Phase 3) is an additional contemporaneous result not in any model's DV — decide whether to mention.
