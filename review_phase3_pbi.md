# Phase 3 Review: PBI/ARI Construction & Naming
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 13 / 13

---

### CRITICAL ISSUES (must fix before submission)
None found.

### IMPORTANT ISSUES (should fix)

**1. PC3 carries a significant contemporaneous recession signal (p = 0.010).**
- *Problem:* The single-component (PC1 = PBI) summary is justified partly on the premise that the recession signal lives only in PC1. Independent recomputation of `PCk ~ recession + C(brand) + C(season)` (year-clustered SE) gives: **PC1 p=0.212, PC2 p=0.946, PC3 coef=−0.242 p=0.010**. PC3 is significant; PC1 contemporaneously is **not**.
- *Why it matters to a jury:* If the thesis states "PC2 and PC3 show no recession signal, so PBI/PC1 is a sufficient summary," that claim is false for PC3. A methods juror (Juror 1/3) will ask what PC3 represents and why a significant macro-responsive axis was discarded. (Note PC1's contemporaneous null is itself consistent with the thesis's position that the *contemporaneous* OLS is not the H1 headline — the event study is — but PC3's significance still needs an answer.)
- *Fix:* (a) Report the per-component recession regression honestly in the PCA section, (b) inspect PC3's loadings and name the construct it captures, and (c) either justify focusing on PC1 on interpretability/variance grounds (PC1 = 44.7% vs PC3 = 18.7%) while acknowledging PC3's macro sensitivity, or add a PC3 robustness appendix. Do not assert "only PC1 responds."

### MINOR ISSUES (nice to fix)

**1. 22 output-facing lines still say "ARI" with no "PBI" qualifier.**
- *Problem:* Prose/abstract use "Palette Boldness Index (PBI)" but 22 `print`/`label`/axis lines emit raw "ARI" (vs 22 lines that do say PBI). Most are internal test prints (`T3 PASS — ARI column present`) that won't reach the PDF, but figure-facing ones will — e.g. cell 28 (the tier ARI-trend plot, `label=tier`, axis), cell 25 summary prints.
- *Why it matters:* A juror reading the appendix figures will see axes/titles labelled "ARI" while the body calls it PBI, and ask why two names. Pure cosmetics, but it reads as unfinished.
- *Fix:* Relabel all figure titles/axes and any printed summary headers to "PBI" (or "PBI (ARI)" once, then PBI). The internal `T#` test prints can stay as-is or be globally renamed; lowest priority.

### CHECKS PASSED

**3.1 PCA validity**
- StandardScaler + PCA fit on **`cell_metrics.csv` (1,645 rows)**, not panel_full — confirmed in cell 25 (`X = cell_metrics[METRICS].values`). ✓
- 7 input metrics correct; **`mean_hue` excluded** (circular variable). ✓
- **PC1 explained variance = 44.74%** (≥40%; matches "~44–45%" claim). EVR: [44.7, 22.6, 18.7, 6.3, 4.0, 3.6, 0.06].
- Sign flip correct: `mean_L` loading **before flip = +0.483 (positive)** → flip applied. After flip: `mean_L −0.483` (lightness=conservative), `saturation_mean +0.397` (bold), `hue_conc_mean −0.220` (monochromatic=conservative), `dispersion_mean +0.219` (spread=bold). All four directions correct → PBI interpretation is **not** inverted. ✓
- ARI z-scored: cell-level mean=−0.0000, std=1.0000; panel_full mean=−0.0000, std=1.0000. ✓ at both levels.
- **Horn parallel analysis (1000 sims): exactly 3 components retained** (real EV > random EV for PC1–3, fails at PC4). Matches notebook's claim. ✓

**3.2 Naming**
- Quantified: 22 output-facing ARI-without-PBI vs 22 PBI lines (see Minor Issue 1).

**3.3 Tier-level face validity** — all match thesis claims within tolerance:
- Accessible Luxury **−0.230** (claim −0.23 ✓), Avant-garde **−0.024** (claim −0.02 ✓), Luxury **+0.141** (claim +0.14 ✓).
- Top 5 by mean ARI: **Dolce & Gabbana (0.673), Prada (0.655), Jean Paul Gaultier (0.599)**, Miu Miu, Gucci — D&G and JPG present as claimed. ✓
- Bottom 8: Rick Owens, Chanel, Stella McCartney, Alexander McQueen, **Balenciaga (−0.320)**, Max Mara, Marni, Ralph Lauren — Rick Owens and Balenciaga present as claimed. ✓

**Sample window note (cross-ref Phase 1):** Notebook cell 0 (abstract) states "2000–2023", matching the panel. The "2000–2024" only appears in the external review brief, so the notebook is internally consistent — downgrade the Phase 1 wording concern to a check-other-prose item.

### CROSS-PHASE FLAGS
- PC3's contemporaneous recession significance (p=0.010) interacts with Phase 4 (contemporaneous null framing) and Phase 9 (multiple testing) — if PC3 is reported as a DV anywhere, it must enter the testing family.
- The CLIP semantic axis is a *second* DV (Phase 6/8); naming consistency should also cover its labels.
