# Wild Cluster Bootstrap Results (Stages W1C + W1D)

**Date:** 2026-06-02. **Engine:** `wildboottest` (MacKinnon–Roodman WCR score bootstrap, **null imposed**, Rademacher weights, B=9999, **`seed=42`** for reproducibility), with a correct manual WCR-t bootstrap as cross-check. Companion data: `wild_bootstrap_results.csv`.

## Why this matters

The H2 monetary-channel models vary their key regressors at the **year** level, giving only **23 clusters**. Standard cluster-robust SEs rely on a large-cluster asymptotic approximation that is unreliable below ~30–50 clusters and tends to *understate* p-values. The wild cluster bootstrap (Cameron, Gelbach & Miller 2008) is valid with few clusters. We re-test every headline coefficient with it; what survives here is genuinely defensible.

---

## Stage W1C — H2 (monetary channel)

**Model 6** (PBI ~ lagged EU recession + lag×tier + lagged EU-GDP + **lagged ECB rate** + CD-change + brand FE + season FE), N=1603, 23 year clusters, R²=0.285. SEs clustered on year.

| Parameter | Coef | p (std clustered) | p (wild WCR) | Verdict |
|---|---|---|---|---|
| ecb_z_lag1 | -0.1034 | 0.0019 | 0.0474 | ✅ survives |
| eu_gdp_z_lag1 | +0.0767 | 0.0320 | 0.4958 | ❌ fails |
| eu_recession_lag1 | -0.0852 | 0.4212 | 0.5709 | ❌ fails |

**Manual WCR-t cross-check** (independent implementation, null imposed on the restricted model, B=1999): `ecb_z_lag1` t=-3.098, p=0.0485 — agrees with the package's 0.0474. The headline number is stable across two independent bootstrap engines.

### Independent validation on the CLIP semantic boldness axis

`semantic_boldness` is a CLIP zero-shot "restrained↔bold" axis — a measurement-independent proxy for the same construct. Same Model-6-style specification, year-clustered.

| Parameter | Coef | p (std clustered) | p (wild WCR) | Verdict |
|---|---|---|---|---|
| ecb_z_lag1 | -0.4571 | 0.0000 | 0.0002 | ✅ survives |
| eu_gdp_z_lag1 | +0.0653 | 0.0841 | 0.1361 | ❌ fails |

### Interpretation (H2)

- **Lagged ECB rate → PBI survives the wild bootstrap.** On the colour-based PBI the p-value moves from 0.0019 (standard) to **0.0474** under the wild bootstrap — still significant at the 5% level, but only just. On the **independent CLIP semantic axis the same effect is far stronger and unambiguous (p_wild=0.0002)**. The monetary-policy→palette channel is the one headline result that is *doubly confirmed*: it holds under valid few-cluster inference **and** reproduces on a measurement that shares none of the colour pipeline.
- **Lagged EU-GDP → PBI does NOT survive.** Despite a standard clustered p of 0.032, the wild bootstrap returns p=0.496 (colour) and 0.136 (CLIP). This was a textbook few-cluster false positive; it should be **demoted from a 'channel' to, at most, a directionally-consistent but non-significant association**, and reported honestly.
- **Lagged EU-recession dummy** remains null (p_wild≈0.57), consistent with the Phase-1 finding that its earlier significance was a lag-leakage artefact.

**Recommended thesis language for H2:** "The lagged ECB-rate effect on palette boldness survives the wild cluster bootstrap (Cameron–Gelbach–Miller) at the 5% level on the colour PBI (p=0.047) and is highly significant on an independent CLIP semantic axis (p<0.001), so the monetary-policy channel is robust to valid few-cluster inference. The weaker lagged-GDP association does not survive the bootstrap and is not claimed as a separate channel."

---

## Stage W1D — H1 (stacked GFC + COVID event study)

Stacked difference-in-differences on the PBI, brand×cohort + season fixed effects, N=981, **25 brand clusters**. Headline coefficients: the pooled post-shock dip at t+1 and t+2, measured against the t−1 reference.

### Two methodological corrections (required for valid inference)

1. **Reference period kept in-sample.** The brief's reconstruction (and the notebook's event-study cell) *drop* the t−1 rows. With no in-sample reference the six event dummies sum to 1 and are collinear with the constant, so the individual coefficients are only identified up to a min-norm (`pinv`) normalisation and cluster/bootstrap inference on them is ill-posed. We **keep t−1 as the reference** (its dummies are all zero), the standard event-study setup, giving a well-conditioned design (residualised-dummy Gram condition number ≈ 8).
2. **Frisch–Waugh–Lovell partialling.** The 50 brand×cohort fixed effects are *nested within* the 25 brand clusters and the full design has 59 parameters, so the cluster-robust variance is rank-deficient and a naive wild bootstrap is unstable (the score bootstrap collapses to p≈0; the studentised WCR-t blows up to p≈0.5). We partial the FE out of the outcome and the event dummies and bootstrap the low-dimensional residualised regression (6 params ≪ 25 clusters).

> **Note on magnitudes.** Because coefficients are now measured against t−1, they are larger than the headline min-norm numbers (t+1 −0.27 / t+2 −0.16 in the current results table). The qualitative conclusion is unchanged and in fact cleaner — see the pre-trend below. The thesis headline table may optionally be updated to these properly-referenced estimates.

### Results

| Parameter | Coef (vs t−1) | p (std clustered) | p (wild WCR-t) | p (wild, package) | Verdict |
|---|---|---|---|---|---|
| etp1 (t+1) | -0.4110 | 0.0009 | 0.0020 | 0.0023 | ✅ survives |
| etp2 (t+2) | -0.3046 | 0.0083 | 0.0126 | 0.0126 | ✅ survives |

**Pre-trend placebo (parallel-trends check):**

| Parameter | Coef (vs t−1) | p (wild WCR-t) | |
|---|---|---|---|
| etm3 (t−3) | -0.0587 | 0.4867 | null ✓ (no pre-trend) |
| etm2 (t−2) | +0.1794 | 0.1448 | null ✓ (no pre-trend) |

The two bootstrap engines (independent manual WCR-t and the `wildboottest` package) agree to within 0.001–0.003 once the design is well-conditioned, confirming the result is real and the earlier instability was purely the nested-FE / dropped-reference artefact.

### Interpretation (H1)

Both post-shock coefficients survive the wild cluster bootstrap comfortably: the pooled t+1 drop (-0.411) at p_wild=0.0020 and the t+2 drop (-0.305) at p_wild=0.0126 — both significant at the 5% (indeed ~1%) level. Pre-shock coefficients (t−3, t−2) are insignificant under the wild bootstrap, supporting parallel trends. H1 is robust to valid few-cluster inference.

---

## Combined summary — what is now defensible

| Result | Coef | Std clustered p | Wild bootstrap p | Status |
|---|---|---|---|---|
| H1 stacked DiD, t+1 (vs t−1) | -0.4110 | 0.0009 | 0.0020 | ✅ survives |
| H1 stacked DiD, t+2 (vs t−1) | -0.3046 | 0.0083 | 0.0126 | ✅ survives |
| H2 lagged ECB rate → PBI (colour) | -0.1034 | 0.0019 | 0.0474 | ✅ survives |
| H2 lagged ECB rate → CLIP semantic | -0.4571 | 0.0000 | 0.0002 | ✅ survives |
| H2 lagged EU-GDP → PBI (colour) | +0.0767 | 0.0320 | 0.4958 | ❌ fails |
| H2 lagged EU-recession dummy | -0.0852 | 0.4212 | 0.5709 | ❌ fails |

**Doubly confirmed (survive both standard clustering and the wild bootstrap):** the H1 post-shock dips at t+1 and t+2, and the H2 lagged-ECB-rate channel — the latter on *both* the colour PBI (p=0.047, borderline) and, decisively, the independent CLIP semantic axis (p<0.001).

**Borderline:** H2 lagged ECB on the colour PBI clears 5% but only just (0.047). The CLIP replication is what makes the channel convincing.

**Do not survive (few-cluster false positives to drop/caveat):** the lagged EU-GDP association (std p=0.032 → wild p≈0.50) and the lagged EU-recession dummy (already null). Neither should be presented as an independent channel.

_This summary is intended to be cited directly in the thesis robustness section. Underlying numbers: `wild_bootstrap_results.csv`._
