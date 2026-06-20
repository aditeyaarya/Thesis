# Phase 9 Review: Robustness Checks & Multiple Testing
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 12 / 12

---

### CRITICAL ISSUES (must fix before submission)
None found.

### IMPORTANT ISSUES (should fix)

**1. EU-GDP survives Bonferroni in the actual Stage 16 table (HC3) — must be reconciled with its wild-bootstrap demotion.**
- *Confirmed by running Stage 16:* family of **8** hypotheses, Bonferroni α/m = 0.0063. `Lagged EU-GDP → ARI`: raw HC3 p = **0.0024**, bonferroni_p = **0.0194**, `survives_bonferroni = True`. So the multiple-testing table *prints EU-GDP as a Bonferroni survivor*, while Part IV demotes it as a wild-bootstrap false positive (p≈0.50). A juror reading both will see a direct contradiction.
- *Fix (same as Phase 6 #1):* Recompute the Stage 16 family on **year-clustered or wild-bootstrap** p-values (the regressors are year-level), OR add an explicit note in the table: "EU-GDP's HC3 significance is a few-cluster artefact; under valid inference (wild bootstrap) it is null and is not claimed as a channel." Best: regenerate the table so EU-GDP no longer appears as a survivor — that removes the contradiction entirely.

**2. The headline must rest on the event study, not the contemporaneous main coefficient (Check 6b).**
- *Finding:* Check 6a (leave-one-brand-out on the **main** recession coefficient) is **25/25 negative**, range [−0.254, −0.172] — extremely stable. But Check 6b (brand-stratified bootstrap of the *contemporaneous* main coefficient) gives 95% CI **[−0.48, +0.06]** — it **includes 0** (barely). This is consistent with Phase 4: the contemporaneous recession→ARI effect is weak under valid (cluster/bootstrap) inference.
- *Why it matters:* If the thesis cites the contemporaneous main coefficient bootstrap as headline support, the CI crossing 0 undercuts it. The robust H1 evidence is the **stacked DiD wild bootstrap** (t+1 p=0.002, t+2 p=0.013, Phase 6) — which excludes 0 comfortably.
- *Fix:* Frame Check 6a (25/25 sign-stable) + the event-study wild bootstrap as the H1 robustness story; present the contemporaneous-coefficient bootstrap as descriptive, noting its CI includes 0 because year-level treatment with ~24 clusters is imprecise contemporaneously.

### MINOR ISSUES (nice to fix)

**1. GFC t+2 survives FDR but not Bonferroni — state which correction the thesis uses.** In Stage 16, `Event GFC t+2`: bonferroni_p = 0.1132 (fails), bh_fdr_p = 0.0226 (survives). The review brief expected GFC t+2 among Bonferroni survivors; it is actually an FDR survivor. Either lead with BH-FDR (defensible for a discovery-oriented family) or note GFC t+2 is FDR-robust, Bonferroni-borderline (and the *pooled* stacked t+2 is wild-bootstrap-robust at p=0.013, which is the stronger statement).

**2. Stage 16 event-study p-values use the t=−1-dropped spec.** Cell 72 computes the event family with `_w = _w[_w.et != -1]` (the under-identified version). It still flags COVID t+1 as a survivor, but for consistency with cells 49/53 the family should use the t=−1-retained spec. Low impact on conclusions; tidy for reproducibility.

**3. Placebo main-effect is significant but in the corroborating direction.** Check 4's *tier-interaction* placebo passes (Luxury×recession p=0.807, null ✓), and recession=0 is confirmed in 2003/2006/2015. A placebo on the *main* coefficient is significant (+0.19, p=0.003) — but **positive**: 2003/2006/2015 are expansion years, so "bolder palettes in good years" is the same directional story, not a spurious recession effect. Worth one sentence so a reader doesn't misread a significant placebo as a red flag.

### CHECKS PASSED

**9.1 Scope** — Cell 70 explicitly labels Checks 1–5 as the **Luxury×recession tier interaction** (secondary/fragile) and Check 6 as the **main recession coefficient** (headline). The distinction is in the code and prints. ✓

**9.2 Leave-one-brand-out**
- Check 1 (tier interaction): **0/25 negative, 0/25 significant**, coef range [+0.020, +0.130]. *Investigated (review asked to if 0/25 negative):* the Luxury×recession interaction is genuinely **null-to-slightly-positive**, never significant — fully consistent with H3 rejection and the Bayesian P(Lux<AG)=0.46. Not a bug; it is the honest tier null. Present Checks 1–5 as confirming the tier interaction is *not* robust (expected), not as a failed headline.
- Check 6a (main coefficient): **25/25 negative**, range [−0.254, −0.172] → far exceeds the ≥22/25 bar. Headline sign is rock-solid. ✓

**9.3 Bootstrap**
- Check 3 (tier interaction): 95% CI [−0.239, +0.372] **includes 0** → expected for a weak/null interaction, framed honestly. ✓
- Check 6b (main): CI [−0.48, +0.06] (see Important #2).

**9.4 Placebo (Check 4)** — `recession == 0` confirmed for 2003/2006/2015; tier-interaction placebo p=0.807 (null) ✓. (Main-effect placebo nuance: Minor #3.)

**9.5 Multiple testing (Stage 16)**
- Primary family = **8** hypotheses (in the 7–8 expected range). ✓
- **CLIP semantic-axis ECB result is NOT in the family** — only the contemporaneous `Recession → CLIP coherence` (clip_within_sim) appears. The lagged ECB→CLIP semantic (p=0.0002) is correctly treated as independent validation, keeping the Bonferroni threshold from tightening. ✓
- Bonferroni survivors: **Contemp recession→dispersion (0.031), Lagged ECB→ARI (0.0001), Lagged EU-GDP→ARI (0.019), Event COVID t+1 (0.0018)**. BH-FDR additionally passes GFC t+2 (0.023). The lagged ECB rate is the strongest survivor — the core H2 result clears even Bonferroni. ✓ (EU-GDP survival = Important #1.)

### CROSS-PHASE FLAGS
- EU-GDP reconciliation is the recurring #1 issue (Phases 4, 6, 9) — one prose+table fix resolves all.
- Check 6b CI-includes-0 reinforces Phase 4/Phase 5: H1 headline = event study, not contemporaneous OLS.
- All Stage 16 survivor p-values feed the Phase 10 numbers table.
