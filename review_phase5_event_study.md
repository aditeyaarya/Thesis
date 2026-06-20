# Phase 5 Review: Event Study, TWFE & Stacked DiD
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 12 / 12

---

### HEADLINE: The most important structural change (t=−1 retained in-sample) is CORRECTLY implemented and reproduces the thesis numbers.

> ⚠️ **Note on the review brief's own verification code:** The reproduction snippets in §5.1 / §6.3 of the review prompt contain `w = w[w.et != -1].copy()`, which **drops** t=−1. Running *that* code gives the wrong, under-identified values (t+1 −0.265, t+2 −0.157) and a **spurious significant t=−2 (+0.324, p<0.001)**. The **actual notebook** (cell 53) does **not** drop t=−1 — it retains it as the reference. Always verify against the notebook spec, not the brief's snippet. This matters directly for Phase 6 (the wild bootstrap must be run on the t=−1-retained design).

---

### CRITICAL ISSUES (must fix before submission)
None found.

### IMPORTANT ISSUES (should fix)

**1. "Flat pre-trend" is true for the headline specs but NOT for GFC main-shows-only — keep the caveat in the abstract.**
- *Problem:* In the pooled stacked DiD and the full-panel per-shock event studies, t=−2 is flat (stacked +0.179 p=0.146; per-shock GFC +0.226 p=0.153, COVID +0.156 p=0.346). But in the **main-shows-only** robustness (Spring/Fall), **GFC t=−2 = +0.307, p=0.027 (significant)**; COVID t=−2 stays flat (p=0.746). The notebook *itself* discloses this ("a residual positive GFC t−2 persists in main shows, p~0.03").
- *Why it matters:* If the abstract/H1 prose says "pre-trends are flat" without qualification, Juror 1 will run the main-shows spec and find a significant GFC pre-trend. The notebook is honest internally; the summary prose must inherit that honesty.
- *Fix:* State "pre-trends are flat in the pooled DiD and full-panel event studies; a small positive GFC t−2 appears in the main-shows-only subset (p≈0.03) but does not overturn the post-shock dip." One clause.

### MINOR ISSUES (nice to fix)

**1. Per-shock event study uses HC3 (cell 49) while Stage 18 uses brand-clustering (cell 53).** Two SE versions of the per-shock event study exist. The pooled/headline inference is brand-clustered (correct). Make sure any per-shock event p-value quoted in the thesis is the brand-clustered (cell 53) one, and label cell 49 as the descriptive/plot version.

**2. TWFE on `recession` is not separately identified.** A `recession + EntityEffects + TimeEffects` PanelOLS is degenerate because `recession` is year-level and fully absorbed by year FEs (collinearity). This is *expected* and is exactly why the within-brand event study is used. If the thesis shows a TWFE table, ensure the recession coefficient there is not interpreted (or use it only to demonstrate year-FE joint significance).

### CHECKS PASSED

**5.1 t=−1 reference retained in-sample — VERIFIED**
- Cell 49: `window_sub = window.copy()` keeps all 7 years; only the dummy set excludes t=−1 (t=−1 rows have all 6 dummies = 0 → baseline). ✓
- Cell 53 stacked DiD: `w = rb[...between(yr−3,yr+3)]...` with **no** `et!=-1` drop; comment "keep t=−1 as reference." t=−1 rows retained = 139. ✓
- **Stacked DiD (notebook spec, brand-clustered), N=981:**
  - t=−3 −0.059 (p=0.49), **t=−2 +0.179 (p=0.146, flat)**, t=0 −0.217 (p=0.007), **t+1 −0.411 (p=0.0013)**, **t+2 −0.305 (p=0.0102)**, t+3 −0.229 (p=0.060). Mean post (t1–3) = −0.315.
  - Matches thesis claims **t+1 ≈ −0.41, t+2 ≈ −0.30** exactly. Not the old −0.27/−0.16. ✓
- **Per-shock event study (full panel, t=−1 reference):** COVID **t+1 −0.487 (p<0.001)** [claim −0.49 ✓], GFC **t+2 −0.347 (p=0.020)** [claim −0.35 ✓]. Pre-trends t=−2 flat for both (p=0.153, p=0.346). ✓

**5.2 TWFE**
- PanelOLS with `EntityEffects` (brand) + `TimeEffects` (year), `cov_type='clustered', cluster_entity=True`. Brand-only within-R² = 0.0046; year-level treatment is absorbed by TimeEffects (collinear), confirming year FEs carry the macro variation and motivating the event-study design.

**5.3 Stacked DiD**
- Brand-by-cohort FE: `C(be)` with `be = brand + '_' + shock` → **50 groups** (25 brands × 2 shocks). ✓
- SEs clustered by **brand (25 clusters)**, not `be` (50) — more conservative. ✓
- t=−1 retained as reference for both cohorts (see 5.1). ✓
- Mean post-shock t+1..t+3 = −0.315; t+1/t+2 = −0.41/−0.30 as claimed. ✓
- *FWL partialling note (for Phase 6):* The Part IV prose says the wild bootstrap on the stacked DiD was run "after FWL partialling of the brand×cohort FEs." Whether the bootstrap code actually partials (vs. running the raw `C(be)` formula) is verified in Phase 6 — flagged there.

**5.4 Main-shows-only robustness**
- `season ∈ {Spring, Fall}` restriction: 1,645 → **1,139** cells. ✓
- COVID t+1 drop persists strongly; t=−2 flat for COVID (p=0.75) but **GFC t=−2 significant (p=0.027)** — see Important #1.

### CROSS-PHASE FLAGS
- **Phase 6 (critical):** Run the wild bootstrap on the **t=−1-retained** stacked design (cell 53 spec). Do NOT use the brief's `et!=-1` reproduction — it under-identifies and will return misleading bootstrap p-values.
- **Phase 6:** Confirm whether the stacked-DiD wild bootstrap actually FWL-partials the `C(be)` FEs or runs the raw formula (prose claims partialling).
- **Phase 10/11:** The GFC main-shows t=−2 nuance feeds the "did the t=−2 framing really change?" jury question (Q9) — answer: yes for full panel/pooled, with an honest GFC main-shows exception.
