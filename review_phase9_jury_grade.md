# Phase 9 Review: Jury Simulation & Grade (as of now)
## Status: COMPLETE
## Date: 2026-06-02

This simulation grades the thesis **as it currently stands** — i.e. with the Phase-1 data fixes applied
(which is the true state of the files) but with the *draft narrative still claiming the pre-fix
results*. The central tension the jury will exploit: the pipeline is technically excellent, but its
stated headline findings no longer reproduce.

---

### GRADING RUBRIC (HEC Paris MSc, /20)

| Dimension | Weight | Score /20 | One-line basis |
|---|---|---|---|
| Research Question & Novelty | 15% | **16** | Genuinely original, cross-disciplinary, well-motivated |
| Literature Positioning & Theory | 10% | **13** | Trickle-down/retrenchment framing present but thin; not fully assessable from notebook |
| Data Quality & Methodology Rigor | 25% | **13** | Large dataset, fixes applied, but weak skin segmentation, narrow ARI construct, residual bugs |
| Results Validity & Robustness | 20% | **11** | Headline findings collapsed post-fix; surviving results modest; extensive but partly-broken robustness |
| Technical Execution (code/pipeline) | 15% | **15** | Sophisticated, mostly-correct stack (PCA, TWFE, event study, Bayesian, CLIP); a few brand-name bugs |
| Discussion & Managerial Implications | 10% | **12** | Needs rewrite — the tier/managerial story no longer holds |
| Presentation & Academic Writing | 5% | **12** | Numbers in draft will mismatch the notebook until reconciled |

**Weighted final grade (now): 13.2 / 20**
**Letter equivalent: B− / B**
**Mention: Assez Bien** (borderline Bien)

Weighted calc: 16·.15 + 13·.10 + 13·.25 + 11·.20 + 15·.15 + 12·.10 + 12·.05 = 2.40+1.30+3.25+2.20+2.25+1.20+0.60 = **13.20**.

---

### JURY EVALUATION BY DIMENSION

**Research Question & Novelty — 16/20.**
- *Does well:* "Do brands de-risk aesthetics during macro shocks, and does it differ by tier?" is novel, testable, and bridges computer vision, finance, and luxury strategy. 1.28M-image scale is impressive.
- *Concerns:* the question presupposes a measurable "aesthetic risk"; the operationalisation (colour boldness) is narrower than the framing.
- *Juror 2 question:* "Is reducing colour saturation really 'aesthetic risk reduction,' or just seasonal palette drift?"

**Literature Positioning & Theory — 13/20.**
- *Does well:* invokes Pesendorfer trickle-down and creative-retrenchment logic; ECB/credit-channel reasoning is economically literate.
- *Concerns:* not visible/strong in the notebook; the trickle-down (Granger) test is null and underpowered, so the theory is asserted more than evidenced.
- *Juror 2 question:* "Which prior literature predicts a *monetary-policy lag* effect on creative output specifically?"

**Data Quality & Methodology Rigor — 13/20.**
- *Does well:* the Phase-1 fixes are real and honest (correct year-based lag, COVID in the recession dummy, sparse cells dropped, revenue series corrected); season-aware normalisation; B&W-collection handling; HC3/HAC/clustering used appropriately.
- *Concerns:* the **skin-exclusion mask barely works** (most skin tones survive, terracotta wrongly removed — Phase 2 I2.1); the **ARI is a colour-boldness index, not "aesthetic risk"** (Phase 3 I3.2); segmentation efficacy is unlogged/unverifiable; data is **2000–2023, not 2000–2024**.
- *Juror 3 question:* "Your skin filter keeps fair/medium/dark skin — how much of your 'palette' is model skin, and could exposed-skin trends correlate with your macro variable?"

**Results Validity & Robustness — 11/20.** *(the decisive weakness)*
- *Does well:* the **event study is a genuine quasi-experimental design** with parallel trends checked; the COVID post-shock ARI drop is robust (survives dropping t=−2 and Bonferroni); lagged ECB/EU-GDP effects are robust (HAC, balanced panel). Robustness suite is broad (LOO, bootstrap, placebo).
- *Concerns:* the **stated primary result is dead** — Model 6 `eu_recession_lag1` is −0.08, p=0.49 (was −0.319, p=0.001); **tier heterogeneity reversed** — P(Lux<AG)=0.465 (was 0.834), and Stage 15's own test T5 now fails; **CLIP coherence flipped sign** (−0.009, was +0.016); Model 1-ARI is borderline (p=0.053); the balanced-panel and CD-control checks have brand-name bugs.
- *Juror 1 question:* "Reproduce Model 6 live. Why does your text say p=0.001 when the notebook gives p=0.49?"

**Technical Execution — 15/20.**
- *Does well:* clean PCA→ARI, `linearmodels` TWFE, event-study with explicit dummies, non-centered hierarchical Bayesian (R-hat 1.003, ESS 5260), CLIP with correct off-diagonal similarity. Validation-test cells throughout.
- *Concerns:* three brand-name mismatches (CD control, balanced-panel list, Stage 13B map) silently drop brands; a hardcoded validation assertion (T5) no longer holds; results workbook omits the key models.
- *Juror 3 question:* "Your balanced-panel check lists 'Jacquemus' and 'Toteme' — brands not in your sample. What is that check actually testing?"

**Discussion & Managerial Implications — 12/20.**
- *Does well:* sensible economic intuition (credit tightening → conservative creative investment).
- *Concerns:* the managerial punchline ("luxury de-risks most") is no longer supported; the discussion must be rewritten around a more modest finding.
- *Juror 2 question:* "If there's no robust tier difference, what's the actionable takeaway for a brand strategist?"

**Presentation & Academic Writing — 12/20.**
- *Concerns:* every headline number in the draft (cells, years, image count, Model 6, P(Lux<AG), CLIP) will mismatch the corrected notebook until reconciled; the workbook is stale/incomplete.

---

### THE 10 ORAL-DEFENCE QUESTIONS

1. **Why PC1 and not PC2/PC3?** *(a)* PC1 (44.7%) is the dominant colour-boldness axis; *but* parallel analysis retains 3 components — PC2 ("vivid-monochrome", 22.6%) and PC3 ("contrast", 18.7%) are signal, not noise. *(b)* Currently under-prepared — the draft implies a clean 1-component solution. *(c)* Add the parallel-analysis result and a multi-component robustness run; justify PC1 on face validity.

2. **0/25 significant in leave-one-brand-out — defend the finding.** *(a)* That LOO tests the *Luxury×recession interaction* (stably positive, insignificant), not the main effect; it is *consistent* with "no tier difference," not a refutation of the main recession effect (−0.34, p=0.016). *(b)* Under-prepared — the notebook's WARN framing is misleading. *(c)* Relabel the check and add a LOO on the *main* coefficient.

3. **t=−2 positive — parallel-trends violation?** *(a)* Yes, a significant t=−2 weakens strict parallel trends; the "anticipation" story is plausible (fashion booked 6–12 months ahead) but not proven. Dropping t=−2, **COVID survives (t+1=−0.34, p=0.001) but GFC weakens (t+2 p=0.077)**. *(b)* Partially prepared. *(c)* Lead with COVID; present GFC as suggestive.

4. **Balenciaga ranks "conservative" — reconcile.** *(a)* ARI measures *colour* boldness; Balenciaga's avant-garde reputation is about silhouette/concept, which the colour pipeline can't see (same for Margiela ranking mid, Missoni below average). *(b)* Under-prepared — these face-validity cases aren't addressed. *(c)* Re-scope the construct to "palette boldness" and add this reconciliation explicitly.

5. **U2Net consistency across 48k images / eras; could segmentation correlate with macro?** *(a)* Plausible risk and currently **unverifiable** — segmentation efficacy and skin-pixel survival are unlogged. *(b)* Poorly prepared (Phase 2 I2.1, Phase 7 M7.1). *(c)* Log alpha-fraction; test whether removal rate or image resolution correlates with recession years (note: resolution *does* differ by era — already found in Stage 13).

6. **Bootstrap CI includes zero — is the finding robust?** *(a)* The CI is for the *tier interaction* (mean +0.14, includes 0) → no robust tier difference; the main recession effect is separately negative and the COVID event-study effect survives Bonferroni. *(b)* Prepared if reframed. *(c)* Distinguish "interaction CI" from "main-effect/event-study evidence."

7. **Is t=−2 a fashion-calendar artifact?** *(a)* Possibly — Pre-Fall/Resort pre-collections are booked far ahead and add ARI noise (Phase 3 I3.3); the anticipation could be mechanical. *(b)* Under-prepared. *(c)* Re-run the event study on main Spring/Fall shows only.

8. **Why these 25 brands / representativeness?** *(a)* European luxury+accessible+avant-garde, cross-referenced to Brand Finance; excludes fast fashion/mid-market/non-European. *(b)* Adequately prepared; subsample stability shows direction-stable, significance-fragile results (Phase 7 Q1). *(c)* State scope limits explicitly.

9. **Is CLIP (internet-trained) appropriate for runway photography?** *(a)* It encodes runway images coherently (within-sim 0.66–0.94) and is *orthogonal* to colour (r=−0.03), so it adds an independent view — but the corrected recession effect is now *negative* and weak, so it no longer supports retrenchment. *(b)* Under-prepared given the sign flip. *(c)* Report the corrected result; frame CLIP as exploratory.

10. **Predict which brands de-risk in the next recession.** *(a)* Honestly: the model gives *no robust brand- or tier-level* prediction — the tier effects are statistically indistinguishable; the most defensible statement is a modest *average* colour-conservatism around shocks, clearest for COVID. *(b)* Under-prepared if overclaiming. *(c)* Answer with calibrated humility.

---

### FINAL JURY VERDICT

**Overall assessment (jury chair):** This is an ambitious, technically accomplished thesis that assembles a genuinely impressive pipeline — 1.28M images, U2Net segmentation, a PCA-based aesthetic index, two-way fixed effects, a DiD event study, a hierarchical Bayesian model, and CLIP embeddings — around an original and engaging question. The student also deserves credit for intellectual honesty: the very data-integrity fixes that improve the work (correct lag, COVID coding, sparse-cell removal) are what dissolve the headline results. As it currently reads, however, the thesis advertises findings that no longer reproduce: the primary lagged-EU-recession effect is insignificant (p=0.49), the luxury-tier heterogeneity reverses (P=0.47), and the CLIP corroboration flips sign. What *survives* is real but more modest — a robust lagged monetary-policy (ECB) effect, a clean COVID event-study drop, and a weak average colour-conservatism around shocks — and the central construct (ARI) measures colour palette rather than "aesthetic risk" in the conceptual sense, producing face-validity puzzles (Balenciaga, Margiela, Missoni). The methodology is now sound where it counts, but a handful of brand-name bugs and an unverified segmentation step remain. This meets the standard for the MSc, but not yet for distinction.

**Grade as of now (before fixes): 13.2 / 20 — Assez Bien** (borderline Bien).

**Projected grade after all Critical/Important fixes and high-priority extensions: 14.5–15 / 20 — Bien.** Pivoting the narrative to the surviving, well-identified evidence (event study + ECB lag + honest nulls), re-scoping ARI as a palette index, fixing the brand-name bugs, correcting all numbers, and pre-empting the face-validity and pre-trend questions would produce a coherent, defensible, honest empirical thesis. It is unlikely to reach Très Bien (16+) because there is no single robust, novel headline causal result once the bug is fixed — the contribution is a careful null-and-modest-effects story, not a strong positive finding.

**One-sentence verdict:** Rewrite the thesis around what survives — the COVID event-study drop and the lagged-ECB effect — because the stated primary results (lagged EU recession, luxury-tier heterogeneity, CLIP coherence) do not reproduce on the corrected data and will not survive a methods juror reproducing them live.
