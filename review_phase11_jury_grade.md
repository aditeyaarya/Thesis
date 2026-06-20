# Phase 11 Review: Jury Simulation & Grade
## Status: COMPLETE
## Date: 2026-06-02

This evaluation is grounded in the Phase 1–10 audit, in which **every cited statistic (25/25) reproduced** and the headline wild-bootstrap p-values matched to ~4 decimals.

---

## Juror 1 — Quantitative Methods & Econometrics

**Strengths**
- The t=−1 reference is correctly retained in-sample (cells 49, 53); stacked DiD reproduces t+1 −0.411 / t+2 −0.305 with flat pre-trends — verified from scratch.
- The wild cluster bootstrap is textbook: WCR (null imposed), Rademacher, B=9999, two independent engines, and **genuine FWL partialling** of the nested brand×cohort FE (my from-scratch FWL reproduced the file's exact p-values). 23-cluster limitation is explicitly acknowledged and is the stated reason for the bootstrap.
- Few-cluster honesty: the contemporaneous composite effect is reported as failing year-clustering; EU-GDP and EU-recession are demoted.

**Concerns**
- **EU-GDP survives Bonferroni (HC3 p=0.0024) in the Stage 16 table but fails the bootstrap.** The thesis prints both without reconciling — the single biggest methodological loose end.
- Stage 16's event-study p-values use the *t=−1-dropped* spec (inconsistent with the corrected cells).
- Check 6b bootstrap CI for the contemporaneous main coefficient includes 0 — fine if H1 rests on the event study, but the text must say so.

**Score: 16/20.** *Rigorous and honest few-cluster inference; held back only by the unreconciled Bonferroni/bootstrap conflict.*
**Question:** "Your EU-GDP effect survives Bonferroni but you demote it on the bootstrap — why does the bootstrap win, and why isn't the Bonferroni family computed on clustered p-values?"

---

## Juror 2 — Marketing & Luxury Management

**Strengths**
- The reframing from "luxury production-calendar" to "industry-wide co-movement" is intellectually honest and follows the failed placebo rather than burying it.
- Brand coverage (25 houses, 3 tiers) and the CD-change controls (14 brands, transition windows) show real domain care.
- The H3 null is triangulated (tier Bayesian, ownership, size, fast-fashion) — a credible "no segmentation" story.

**Concerns**
- **No mechanism** for an industry-wide 1-year lag. Without the production-calendar story the lag is unmotivated — the thesis's central intellectual debt.
- **"Fast-fashion" mislabels Tommy Hilfiger / Tory Burch** (structured seasonal collections, not weekly cycles); the placebo's lead-time contrast is weaker than claimed.
- The contribution is now a robust *correlation* with an unknown channel — interesting but not yet a managerial story.

**Score: 14/20.** *Honest and well-scoped, but the mechanism void and the fast-fashion labelling weaken the managerial payoff.*
**Question:** "If the monetary channel is industry-wide, what is the mechanism, and are Tommy Hilfiger and Tory Burch really 'fast fashion'?"

---

## Juror 3 — Data Science & Machine Learning

**Strengths**
- CLIP pipeline is clean: (48,056×512), unit-normalised, **same ViT-B-32/openai checkpoint for image and text** (valid dot products).
- The independent CLIP semantic axis replicates the ECB result decisively (p=0.0002) — a genuine multimodal confirmation that shares none of the colour pipeline.
- Fast-fashion PBI is projected onto the **luxury PCA basis exactly** (corr = 1.000000) — no leakage from a refit. PCA validity (44.7% PC1, correct sign flip, Horn = 3) is solid.

**Concerns**
- The CLIP axis (p=0.0002) is far stronger than colour PBI (p=0.047) — is colour PBI really the primary DV, or should CLIP lead? The choice should be argued, not assumed.
- CLIP zero-shot "restrained↔bold" prompts are used as ground truth without prompt validation against human ratings.
- **PC3 carries a significant contemporaneous recession signal (p=0.010)** that the single-PC1 summary doesn't address.

**Score: 16/20.** *Strong, careful multimodal work; the DV hierarchy and prompt validation are the open ML questions.*
**Question:** "Your CLIP result is an order of magnitude stronger than colour PBI — why is the weaker measure your headline DV, and how do you know the CLIP prompts measure boldness?"

---

## Grading Rubric (HEC Paris MSc, /20)

| Dimension | Weight | Score /20 | Key Strengths | Key Concerns |
|---|---|---|---|---|
| Research Question & Novelty | 15% | 16 | Macro→aesthetics with multimodal measurement; novel ECB-lead finding | Mechanism unidentified |
| Literature Positioning & Theory | 10% | 13 | Clear hypotheses, honest revision | Thin theory for the industry-wide lag |
| Data Quality & Methodology Rigor | 25% | 17 | 1,645 clean cells; correct DiD; valid few-cluster inference; FWL bootstrap | EU-GDP Bonferroni conflict; stale t−2 cell |
| Results Validity & Robustness | 20% | 17 | 25/25 numbers reproduce; bootstrap + CLIP double-confirmation; honest nulls | Borderline ECB-PBI; underpowered placebo |
| Technical Execution | 15% | 18 | Reproducible pipeline; diagnostics; everything runs and matches | Two SE versions coexist; minor naming |
| Discussion & Managerial Implications | 10% | 13 | Honest reframing | Mechanism void limits implications |
| Presentation & Academic Writing | 5% | 14 | Clear abstract/structure | ARI/PBI labels; contradictory t−2 cells |

**Weighted: 0.15·16 + 0.10·13 + 0.25·17 + 0.20·17 + 0.15·18 + 0.10·13 + 0.05·14**
= 2.40 + 1.30 + 4.25 + 3.40 + 2.70 + 1.30 + 0.70 = **16.05 / 20**

**Weighted Final Grade: 16.0 / 20 — Mention: Très Bien**

---

## Ten Critical Jury Questions — answers from the current pipeline

1. **t=−1 change (−0.27/−0.16 → −0.41/−0.30):** Dropping t−1 left six dummies collinear with the constant → min-norm (pinv) estimates and ill-posed inference. Retaining t−1 as the zero-baseline is the standard event-study setup; the larger estimates are the correctly-referenced ones. *Verified; notebook ready.*
2. **ECB p=0.047 borderline:** Borderline on colour PBI alone; decisive on the independent CLIP axis (0.0002). Two-modality confirmation is the argument. *Ready (Q4).*
3. **TH/Tory Burch as fast fashion:** They are accessible/shorter-cycle, not weekly — the contrast is a lead-time gradient, not a dichotomy. *Needs relabelling + lead-time disclosure (Phase 7 #2).*
4. **Industry-wide mechanism:** Not identified by the design; candidate channels = credit→creative/marketing budgets, consumer sentiment, shared colour-forecasting cycles. *Needs the paragraph (Phase 4 #1).*
5. **EU-GDP Bonferroni vs bootstrap:** HC3 on cell-rows overstates precision for a year-level regressor; the bootstrap is valid for 23 clusters and overrides. *Needs explicit reconciliation / table regen (Phase 6 #1, Phase 9 #1).*
6. **CLIP stronger than PBI — which is primary?** Defensible either way, but the choice must be argued; colour PBI is the pre-registered construct, CLIP the independent validator. *Add one sentence.*
7. **5-brand placebo power:** MDE ≈ 0.11 PBI units ≈ the luxury effect → "no evidence of difference," not "proven equal." *Add the MDE number (Phase 7 #1).*
8. **Forest plot:** Shows tier posteriors copied across brands (model has tier-varying, not brand-varying, slopes). *Needs caption disclosure (Phase 8 #1).*
9. **t−2 framing change:** Flat in headline specs (verified); the old "late-boom exuberance" was a missing-reference artefact — **but cell 47 still asserts it**. *Must fix the contradiction (Phase 10 #1).*
10. **Which claim most/least robust:** Most robust = **H1 acute-shock dip** (25/25 LOO-negative, wild bootstrap p=0.002/0.013). Most fragile = **H2 colour-PBI ECB** (p=0.047), rescued by the CLIP replication. H3 is a well-supported null.

---

## Final Jury Verdict

**Overall Assessment.** This is a strong, unusually honest empirical thesis. Its scientific contribution is a robust, doubly-confirmed finding that aesthetic boldness on the runway falls after acute macro shocks (H1) and tracks the prior-year ECB policy rate (H2) — the latter validated both under valid few-cluster inference and on an independent CLIP semantic axis. The student's willingness to demote EU-GDP, reject the production-calendar mechanism after a failed placebo, and report an honest H3 null reflects real scientific maturity, and the Phase-level audit confirms the work is reproducible to the decimal. Its remaining weaknesses are conceptual rather than computational: there is no theoretical mechanism for the industry-wide lag, the fast-fashion placebo is underpowered and mislabelled, and a stale "late-boom exuberance" passage contradicts the corrected pre-trend analysis. None of these threatens the core results; all are addressable in prose. The thesis merits distinction.

**Grade before final fixes: 16.0 / 20 — Très Bien.**

**Grade after fixing the three most important issues** — (1) supply a candidate mechanism for the industry-wide ECB lag, (2) reconcile the EU-GDP Bonferroni-vs-bootstrap conflict (ideally regenerate the Stage 16 table on clustered p-values), (3) disclose the Bayesian forest plot's tier-level design — **plus the stale cell-47 fix: 17.0–17.5 / 20 — solid Très Bien, approaching Excellent.**

**One-sentence verdict:** Before the oral defence, the student must give the industry-wide lagged-ECB effect a stated (even if unproven) mechanism and resolve the EU-GDP Bonferroni/bootstrap contradiction — the results are sound and reproducible; what's missing is the *story* that turns a robust correlation into a defensible thesis.
