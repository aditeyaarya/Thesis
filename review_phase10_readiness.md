# Phase 10 Review: Numbers Verification & Thesis Readiness
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 10 / 10 (+ 25-row numbers table)

---

### 10.1 Numbers Verification Table (all independently recomputed)

| Statistic | Thesis Claim | Verified Value | Match? |
|---|---|---|---|
| Total cells in panel | 1,645 | 1,645 | ✅ |
| Total brands | 25 | 25 | ✅ |
| PC1 explained variance | ~44–45% | 44.74% | ✅ |
| PBI/ARI mean (cell level) | ≈ 0.000 | −0.0000 | ✅ |
| PBI/ARI std (cell level) | ≈ 1.000 | 1.0000 | ✅ |
| Luxury mean ARI | +0.14 | +0.141 | ✅ |
| Stacked DiD t+1 coef | −0.41 | −0.411 | ✅ |
| Stacked DiD t+2 coef | −0.30 | −0.305 | ✅ |
| Stacked DiD t+1 brand-clustered p | <0.01 | 0.0013 | ✅ |
| Stacked DiD t+1 wild bootstrap p | 0.002 | 0.0020 | ✅ |
| Stacked DiD t+2 wild bootstrap p | 0.013 | 0.0126 | ✅ |
| COVID event t+1 coef | −0.49 | −0.487 | ✅ |
| GFC event t+2 coef | −0.35 | −0.347 | ✅ |
| Lagged ECB → PBI coef | −0.10 | −0.1034 | ✅ |
| Lagged ECB → PBI year-clustered p | 0.002 | 0.0019 | ✅ |
| Lagged ECB → PBI wild bootstrap p | 0.047 | 0.0474 (re-run 0.0485) | ✅ |
| Lagged ECB → CLIP semantic coef | −0.45 | −0.4571 | ✅ |
| Lagged ECB → CLIP wild bootstrap p | 0.0002 | 0.0002 (re-run ≈0.000) | ✅ |
| EU-GDP → PBI wild bootstrap p | ~0.50 | 0.4958 (re-run 0.484) | ✅ |
| FF × luxury interaction p (year-clustered) | 0.36 | 0.3610 | ✅ |
| FF × luxury wild bootstrap p | 0.84 | 0.838 (file) | ✅ |
| P(Luxury < Avant-garde), Bayesian | 0.47 | 0.462 | ✅ |
| Bayesian R-hat max | <1.01 | 1.006 | ✅ |
| t=−2 pre-trend p (GFC, full panel) | >0.05 | 0.153 | ✅ |
| t=−2 pre-trend p (COVID, full panel) | >0.05 | 0.346 | ✅ |

**Every cited number reproduces.** This is an unusually clean numbers audit — 25/25 match.

---

### CRITICAL ISSUES (must fix before submission)
None found.

### IMPORTANT ISSUES (should fix)

**1. Stale "late-boom exuberance" text in cell 47 contradicts the corrected result and cell 46 (prep Q9).**
- *Problem:* Cell 46 (correct) states the "positive t−2 / late-boom exuberance" reading *disappears* once t−1 is retained and pre-trends are flat. **Cell 47 still says the opposite:** "t−2 is *positive* in both shocks — palettes were unusually bold two years before each downturn (late-boom exuberance), so parallel trends are imperfect at the 2-year horizon." Two markdown cells make **opposite** claims about t−2.
- *Why it matters:* This is exactly the version-change a juror will probe (Q9: "you dropped late-boom exuberance — which is it?"). An internal contradiction in the thesis is worse than either framing alone.
- *Fix:* Rewrite cell 47 to match cell 46 and the data (t−2 flat: stacked +0.18 p=0.15, GFC +0.23 p=0.15, COVID +0.16 p=0.35). Keep only the honest caveat that GFC t−2 turns mildly positive in the main-shows-only subset (p≈0.03). Delete the "late-boom exuberance / parallel trends imperfect" sentence.

**2. (Carried from Phases 6/9) EU-GDP Bonferroni-vs-bootstrap contradiction** — reconcile in prose or regenerate the Stage 16 table on clustered p-values.

**3. (Carried from Phases 4/7) Mechanism for the industry-wide lagged ECB effect** — add a candidate-channels paragraph.

### MINOR ISSUES (nice to fix)
- **ARI vs PBI labels** (Phase 3): 22 output-facing "ARI" lines remain; relabel figure axes/titles to PBI.
- **Bayesian forest-plot caption** (Phase 8): disclose tier-level design.
- **Sample window**: notebook is internally consistent at "2000–2023"; ensure no stray "2000–2024" survives in the final write-up prose.

### CHECKS PASSED

**10.2 Framing consistency (markdown grep)**
- Industry-wide: 8 ✓ | Production-calendar: 3 (all explicit rejections, Phase 4) ✓ | Wild bootstrap: 18 ✓ | Fast-fashion: 8 ✓ | Flat/parallel pre-trend: 6 ✓ | PBI naming: 24 ✓.
- **Late-boom exuberance: 4** — 2 are the *corrective* mention in cell 46 (good); 2 are the **stale assertion in cell 47** (Important #1). Not yet fully purged.

**10.3 Output files** — all 15 required artifacts present (panel/cell/macro/color/urls CSVs; density/scree/ari/event/forest/robustness PNGs; results xlsx; wild_bootstrap + fast_fashion md; fast_fashion panel). ✓

**10.4 Jury-question readiness** (answers the data supports):
- **Q1 (EU-GDP in Model 6):** Retained as a control; HC3/clustered significance is a 23-cluster false positive (wild p≈0.50). *Notebook needs the explicit control sentence (Phase 4 #2).*
- **Q2 (5-brand placebo):** Cannot rule out a luxury-specific effect; shows no evidence of difference, MDE≈0.11 ≈ effect size. *Add the MDE number (Phase 7 #1).*
- **Q3 (t−2 framing):** Flat in headline specs (verified); cell 47 stale text must go (Important #1).
- **Q4 (ECB p=0.047 borderline):** Borderline on colour PBI, decisive on CLIP (p=0.0002); two-modality confirmation. *Well supported.*
- **Q5 (mechanism):** Unknown; candidate industry-wide channels. *Needs the paragraph (Important #3).*
- **Q6 (B precision):** B=9999 gives 95% band [0.043, 0.051] for p=0.047 — adequate. *Well supported (Phase 6).*
- **Q7 (forest plot):** Tier posteriors by brand — *needs caption (Phase 8 #1).*

### CROSS-PHASE FLAGS
- The three "carry" issues (EU-GDP reconciliation, mechanism, late-boom text) are the core of the Phase 11 "fix before defence" list.
- Numbers table is 25/25 — Technical Execution and Results Validity scores in Phase 11 should reflect this.
