# FINAL CONSOLIDATED REVIEW — Vogue Runway Analysis (Thesis v3)
## Date: 2026-06-02
## Reviewer: Claude Code (11-phase audit, all checks executed against the live notebook & data)

---

## Bottom line

A **strong, reproducible, intellectually honest** MSc thesis. Across 11 phases, **every cited statistic (25/25) reproduced**, and the headline wild-bootstrap p-values matched the saved results to ~4 decimal places — including a from-scratch reconstruction of the FWL-partialled stacked-DiD bootstrap. The remaining work is **prose, not computation**: one logical reconciliation, one missing mechanism, one stale paragraph, and a few labelling fixes.

**Simulated grade: 16.0 / 20 (Très Bien) → 17.0–17.5 after the three priority fixes.**

> ⚠️ **Methodological note for the supervisor:** The review brief's *own* verification snippets for the stacked DiD / wild bootstrap (`w = w[w.et != -1]`) **drop the t−1 reference**, which under-identifies the model and produces the wrong −0.27/−0.16 estimates and a spurious significant t−2. The **actual notebook is correct** (it retains t−1). Anyone re-checking these results must use the notebook spec, not the brief's snippet.

---

## What is verified correct (the spine of the thesis holds)

| Result | Verified |
|---|---|
| Panel: 1,645 cells, 25 brands, correct tiers, no dupes, n_images≥15 | ✅ |
| Macro: negative ECB 2014–21, correct recession dummies, lags | ✅ |
| PCA/PBI: PC1 44.7%, sign flip correct (not inverted), Horn=3, ARI z(0,1) | ✅ |
| CLIP: (48,056×512), unit-norm, same ViT-B-32/openai for image+text | ✅ |
| Model 6 ECB lag: −0.103, year-clustered p=0.0019 | ✅ |
| Stacked DiD (t−1 retained): t+1 −0.411/p=0.001, t+2 −0.305/p=0.010, t−2 flat | ✅ |
| Wild bootstrap: t+1 0.002, t+2 0.013, ECB-PBI 0.047, ECB-CLIP 0.0002, EU-GDP ≈0.50 | ✅ all re-run |
| FWL partialling of nested FE | ✅ genuinely implemented |
| Fast-fashion on luxury PCA basis (corr=1.000000); interaction −0.043/p=0.361 | ✅ |
| Bayesian: R-hat 1.006, ESS 576, 1 divergence, P(Lux<AG)=0.46, 95% HDI | ✅ |
| H3 nulls: ownership p=0.77, size p=0.78, DVN immaterial | ✅ |
| Main recession LOO: 25/25 negative | ✅ |

---

## CRITICAL ISSUES
**None.** No result is wrong; nothing must be re-run.

---

## THE THREE PRIORITY FIXES (do these before defence)

1. **Mechanism for the industry-wide lagged-ECB effect** *(Phases 4, 7, 11 Q4/Q5).*
   Add a short paragraph naming candidate channels (credit→creative/marketing budgets set a season ahead; consumer sentiment; shared colour-forecasting/Pantone-WGSN cycles) and explicitly conceding the mechanism is not identified by the design. This is the single most important gap.

2. **Reconcile EU-GDP: Bonferroni-survivor vs bootstrap-failure** *(Phases 6, 9, 11 Q5).*
   Confirmed: Stage 16 prints `Lagged EU-GDP survives_bonferroni = True` (HC3 p=0.0024) while Part IV demotes it (wild p≈0.50). Either regenerate the Stage 16 family on **year-clustered / wild-bootstrap** p-values (best — removes the contradiction), or add an explicit note that HC3 overstates precision for a year-level regressor and the bootstrap governs at 23 clusters.

3. **Disclose the Bayesian forest plot's tier-level design** *(Phase 8, 11 Q8).*
   The "brand-level" panel shows each tier's posterior copied across its brands (the model has tier-varying, not brand-varying, slopes). Caption it so the 25 identical-within-tier bars aren't read as brand-specific estimates.

**Plus a near-free 4th:** delete/rewrite the **stale cell-47 "late-boom exuberance"** passage, which contradicts cell 46 and the verified flat pre-trends (Phase 10 #1).

---

## IMPORTANT ISSUES (should fix)

- **Fast-fashion power + label** (Phase 7): report MDE ≈ 0.11 PBI units (≈ the luxury effect) and rename "fast-fashion" → "accessible/short-cycle"; state "no evidence of a difference, not proven equality."
- **EU-GDP control language** (Phase 4): say in the H2 text that it is a retained control, not a channel.
- **H1 headline = event study, not contemporaneous OLS** (Phases 4, 9): the contemporaneous main-coefficient bootstrap CI includes 0; lead with the event-study/bootstrap evidence.
- **GFC main-shows t−2** (Phase 5): keep the honest caveat that t−2 is mildly positive (p≈0.03) in the Spring/Fall subset, even though flat in the pooled/full-panel specs.

---

## MINOR ISSUES (nice to fix)

- **ARI vs PBI labels** (Phase 3): 22 output-facing "ARI" lines; relabel figure axes/titles to PBI.
- **PC3 recession signal** (Phase 3): PC3 is significantly recession-associated (p=0.010); don't claim "only PC1 responds" — name what PC3 captures or add a PC3 robustness note.
- **CLIP as primary DV?** (Phase 8/11 Q6): argue the colour-PBI-primary / CLIP-validator choice in one sentence; consider validating the CLIP prompts.
- **Two SE versions of Model 6 / event study** (Phases 4, 5): label HC3 cells as exploratory so the clustered Stage-18 values are unambiguously the cited ones.
- **Stage 16 event family** uses the t−1-dropped spec (Phase 9): tidy for consistency.
- **Bootstrap seed** not documented in `wild_bootstrap_results.md` (Phase 6): it's 42; state it.
- **Sample window**: notebook says 2000–2023 (consistent); purge any stray "2000–2024."
- **Fair-skin HSV leakage** (Phase 2): disclose the filter targets medium-to-dark skin; fair-skin residual is bounded.

---

## Phase-by-phase status

| Phase | Topic | Verdict | File |
|---|---|---|---|
| 1 | Data integrity | Clean | review_phase1_data_integrity.md |
| 2 | Feature extraction | Clean | review_phase2_extraction.md |
| 3 | PBI/ARI & naming | 2 flags (PC3, labels) | review_phase3_pbi.md |
| 4 | Models H1/H2/H3 | Reproduce; mechanism + EU-GDP prose | review_phase4_models.md |
| 5 | Event study/DiD | **Correctly implemented**; numbers match | review_phase5_event_study.md |
| 6 | Wild bootstrap | **Exact reproduction**; EU-GDP tension | review_phase6_wild_bootstrap.md |
| 7 | Fast-fashion placebo | Clean basis; underpowered + label | review_phase7_fast_fashion.md |
| 8 | H3/Bayesian | Converges; forest caption + LOO compare | review_phase8_h3_bayesian.md |
| 9 | Robustness/MT | H1 25/25; EU-GDP Bonferroni confirmed | review_phase9_robustness.md |
| 10 | Numbers/readiness | **25/25 numbers match**; cell-47 stale | review_phase10_readiness.md |
| 11 | Jury & grade | 16.0→17.5/20, Très Bien | review_phase11_jury_grade.md |

---

## One-sentence verdict
The empirics are sound and reproducible to the decimal; before the oral defence the student must give the industry-wide lagged-ECB effect a stated (even if unproven) mechanism and resolve the EU-GDP Bonferroni/bootstrap contradiction — everything else is labelling and prose.
