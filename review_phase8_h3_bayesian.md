# Phase 8 Review: H3, Bayesian Model & Heterogeneity
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 12 / 12

---

### CRITICAL ISSUES (must fix before submission)
None found.

### IMPORTANT ISSUES (should fix)

**1. The brand-level forest plot displays tier posteriors copied across brands — disclose it in the figure caption (prep Q8).**
- *Problem:* The model has **one** recession effect per *tier* (`beta_recession_tier`, shape = n_tiers). Cell 65 builds the "brand-level" panel by giving every brand its tier's distribution (code comment: "each brand inherits its tier"). So the right-hand panel shows 25 bars that are really 3 distributions repeated (12 identical Luxury, 7 identical Accessible, 6 identical Avant-garde). The code discloses this; the **figure title** ("brand-specific recession effects") does not.
- *Why it matters:* Juror 1/3 (Q8) will spot 25 bars with identical within-tier error bars and ask whether these are brand estimates or 3 tier estimates copied. If the caption doesn't pre-empt it, it looks like overclaiming brand-level resolution the model can't deliver.
- *Fix:* Retitle/caption: "Brand-level view of *tier* recession posteriors — all brands within a tier share one distribution by design (tier-varying, not brand-varying, slopes)." Or add a brand-varying slope if true brand-level estimates are wanted (heavier model). Caption fix is sufficient.

**2. LOO-CV is reported without a comparison model — I ran the missing comparison; add it.**
- *Problem:* Cell 66 prints `elpd_loo`, `p_loo`, Pareto-k but only *notes* "compare against a simpler model" — it never runs one. A lone `elpd_loo` is uninterpretable as fit.
- *I ran it for you:* Full model **elpd_loo = −2102.8** vs a brand-FE-only null **−2254.7** → **Δelpd = 152 (dse ≈ 18.8, ~8 SE)**. The macro/tier structure adds substantial out-of-sample predictive value. Pareto-k > 0.7 = **0 obs** (LOO reliable).
- *Fix:* Add the null model + `az.compare` and report Δelpd ≈ 152 ± 19. This turns an uninterpretable number into evidence that the macro model genuinely predicts better.

### MINOR ISSUES (nice to fix)

**1. The "Avant-garde × recession = +0.57 (p=0.09)" figure is from a looser spec.** Under year-clustered SEs with brand+season FE, the AG×recession interaction is **+0.19, p=0.36** — firmly null. The cited +0.57/p=0.09 (Model 2-ARI, HC3-style) overstates a non-result. The notebook *does* contextualise it correctly (consistent with P(Lux<AG)=0.47), but quoting the +0.57 invites a question. Prefer reporting the clustered +0.19/p=0.36, or label the +0.57 as the (less conservative) HC3 value.

### CHECKS PASSED

**8.1 H3 result framing**
- **P(Luxury < Avant-garde) = 0.462** (re-run from a fresh MCMC trace; claim 0.47 ✓ — ≈0.5 = no tier divergence).
- All three tiers carry negative recession posteriors (Accessible −0.30 [P<0=0.99], Avant-garde −0.20 [0.93], Luxury −0.19 [0.95]) → shared response, no Luxury-specific extra conservatism.
- Ownership interaction **p = 0.775** (>0.7 ✓); size interaction **p = 0.781** (>0.7 ✓). Both null.
- **DVN sensitivity:** excluding Dries Van Noten (independent until 2023, coded `conglom=1`), the ownership interaction is **−0.030, p = 0.69** — essentially unchanged. The known DVN mis-coding is **immaterial** to the null. ✓

**8.2 Bayesian diagnostics** (4 chains × 1,000 draws, non-centered, seed=42)
- **Max R-hat = 1.006 (< 1.01)** ✓
- **Min ESS = 576 (> 400)** ✓
- **Divergences = 1** (< 10 threshold; non-centered parameterisation working) ✓
- **95% HDI = `np.percentile(vals, [2.5, 97.5])`** — confirmed 95%, not the previous version's 94%. ✓
- Tier-level design caveat: the forest plot is tier-posteriors-by-brand (Important #1).

**8.3 LOO-CV**
- elpd_loo = −2102.8, p_loo = 31.2, **Pareto-k > 0.7 = 0** (no influential-point problems; LOO trustworthy). Comparison model now supplied (Important #2).

### CROSS-PHASE FLAGS
- H3 "industry-wide / no heterogeneity" rests on three independent nulls (tier Bayesian P=0.46, ownership p=0.77, size p=0.78) plus the fast-fashion placebo (Phase 7) — collectively a strong, honest null. Feeds Phase 11 grade on Results Validity.
- Forest-plot caption fix (Q8) and the AG-interaction wording feed Phase 10 framing checks.
