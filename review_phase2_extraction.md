# Phase 2 Review: Feature Extraction Audit
## Status: COMPLETE
## Date: 2026-06-02
## Checks Run: 11 / 11

---

### CRITICAL ISSUES (must fix before submission)
None found.

### IMPORTANT ISSUES (should fix)
None found.

### MINOR ISSUES (nice to fix)

**1. Very fair skin escapes the HSV skin filter (h ≤ 0.07 cutoff).**
- *Problem:* In the calibration table, a fair-skin swatch (255,224,196) lands at **H = 0.08, S = 0.23**, just above the `h ≤ 0.07` ceiling, so it is **kept as garment**. Medium, tan, and dark skin (H 0.06–0.07) are correctly excluded. Light, low-saturation skin pixels therefore leak into the garment set and nudge `mean_L` upward and `saturation_mean` downward for pale-model collections.
- *Why it matters to a jury (mild):* A vision-savvy juror (Juror 3) may ask how robust the palette metrics are to skin-tone leakage. The leakage is small (only the lightest skin, and only the fraction the model leaves un-segmented), but it is asymmetric across collections.
- *Fix:* Either widen the hue ceiling slightly (`h <= 0.10`) with a brightness guard, or simply disclose in the methods that the filter is tuned to exclude medium-to-dark skin and that residual fair-skin leakage is a known, bounded limitation. A one-line robustness note suffices; no re-extraction required.

**2. Pixel-level extraction is non-reproducible (no per-image seed).**
- *Observation:* `np.random.choice(len(garment_rgb), min(n, ...), replace=False)` has no per-image seed, so the 500-pixel sample differs run-to-run. This is fine **as long as the thesis claims cell-level reproducibility** (the cached `color_metrics_raw.csv` / `cell_metrics.csv` freeze the values). Confirm the thesis does not claim bit-exact pixel reproducibility.
- *Fix:* State explicitly that reproducibility is guaranteed at the cell level via the cached CSVs, not at the pixel-sampling level.

### CHECKS PASSED

**2.1 Segmentation & pixel extraction**
- HSV skin bounds exactly match spec: `h <= 0.07 & s >= 0.08 & s <= 0.70 & v >= 0.30`.
- Calibration table confirms the **critical** behaviour: warm/saturated garments are **kept**, not mistaken for skin — terracotta (H0.04,**S0.80**), bright red (H0.00,**S0.91**), navy (H0.64) all kept because their saturation exceeds the 0.70 skin ceiling. Medium/tan/dark skin correctly excluded.
- Fallback confirmed: `if len(garment_rgb) < 50: garment_rgb = fg_rgb` — falls back to **foreground pixels**, not the full image. ✓

**2.2 LAB metrics**
- `rgb2lab` is called on pixels already in [0,1] (`garment_rgb[idx]/255.0`). ✓
- `dispersion = sqrt(var(L)+var(a)+var(b))` verified **mathematically identical** to the RMS of per-pixel Euclidean distances from the colour centroid (66.6352 = 66.6352). The notebook's description "RMS distance of pixels from their colour centroid" is **exact**. It is *not* the mean pairwise distance (84.64 in the test) — prose is correct as long as it does not say "pairwise." No jury exposure.
- `scipy_entropy` on raw bin counts `+ 1e-9` before scipy's internal normalisation — correct.
- Hue angle via `arctan2(b,a)`, 36 bins over `(-π, π)` = full circle, no gap. ✓

**2.3 B&W collection handling**
- `bw_collection` present in **both** `cell_metrics.csv` and `panel_full.csv`.
- All 3 B&W cells retain **non-null ARI** (3/3) — not excluded from PBI/ARI models. Flag is advisory only. ✓

**2.4 CLIP embeddings**
- `clip_embeddings.npz` shape = **(48056, 512)** (≈48k, matches thesis). Unit-normalised: all norms = 1.0000 (±0.01). ✓
- `mean_off_diagonal_sim = (sim.sum() − trace(sim)) / (n*(n−1))` — exactly the spec; prose says "off-diagonal pairwise cosine similarity (diagonal excluded)" — consistent. ✓
- Same checkpoint **`ViT-B-32` + `pretrained='openai'`** for image encoding (cell 40) and text/tokenizer (cell 57). Image–text dot products are valid. ✓

### CROSS-PHASE FLAGS
- CLIP semantic axis (`semantic_boldness`) validity and its use as a second DV is examined in Phase 6 (wild bootstrap p=0.0002) and Phase 8/11 (Juror 3: is it the primary DV?). Extraction side is clean.
