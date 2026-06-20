# Stage W1B — PBI / ARI Naming Fix

**Date:** 2026-06-02  
**File modified:** `vogue_runway_analysis.ipynb` (validated with `nbformat` after edit).  
**Backup:** `vogue_runway_analysis.ipynb.bak_w1b_*`.

## Rationale

The thesis presents PC1 as the **Palette Boldness Index (PBI)**, but the codebase used the legacy label **ARI** ("Aesthetic Risk Index") in some figure titles, axis labels and model-output print statements. A jury reading the thesis text and then the figures/appendix would see two names for one construct. This stage harmonises every *user-visible* string to PBI wording while keeping the Python identifier `ARI` unchanged as a code alias.

## Substitutions applied

Applied in a collision-safe order (specific strings before the substrings they contain), operating per source line so the notebook JSON stays valid.

| # | Old (user-visible) | New | Count |
|---|---|---|---|
| 1 | `DiD Event Study — Macro Shocks & Aesthetic Risk (ARI)` | `DiD Event Study — Macro Shocks & Palette Boldness Index (PBI)` | 1 |
| 2 | `Aesthetic Risk Index (ARI)` | `Palette Boldness Index (PBI)` | 1 |
| 3 | `DV = Aesthetic Risk Index` | `DV = Palette Boldness Index (PBI)` | 1 |
| 4 | `DV = ARI` | `DV = PBI (Palette Boldness Index)` | 1 |
| 5 | `Aesthetic Risk Index` | `Palette Boldness Index (PBI)` | 4 |
| 6 | `ΔARI` | `ΔPBI` | 2 |
| 7 | `Mean ARI (z-scored)` | `Mean PBI (z-scored)` | 2 |
| 9 | `Within-Brand ARI` | `Within-Brand PBI` | 2 |
| 10 | `ARI direction` | `PBI direction` | 1 |
| 11 | `ARI vs Aesthetic Quality` | `PBI vs Aesthetic Quality` | 1 |
| 12 | `Recession effect on ARI` | `Recession effect on PBI` | 2 |
| 13 | `Brand ARI ranking` | `Brand PBI ranking` | 1 |

**Total replacements: 19** across figure titles, axis labels, legend labels and DV print statements (cells 27, 28, 29, 31, 34, 50, 65).

## Deliberately NOT changed — `ARI` retained as a code alias

The following remain `ARI` on purpose, because they are code identifiers, not jury-facing text:

- The pandas column / variable **`ARI`** in `panel_full.csv` and throughout the pipeline.
- Dictionary keys, model object names (`model1_ari`, `model2_ari`), and workbook sheet names (`Model1_ARI`, `Model2_ARI_tier`).
- Internal code comments (e.g. `# Model 1-ARI: ...`).
- Console *diagnostic* prints that explain the construct in passing (e.g. "Sign is flipped so ARI > 0 = bold"), which document the variable rather than label a deliverable.
- Output PNG filenames (`ari_trends.png`, `ari_within_brand_variance.png`): internal artefacts, not embedded labels.

The construct-validity markdown (cell 24) already states explicitly: *"We label PC1 the **Palette Boldness Index (PBI)** — in code it remains the variable `ARI` for backward compatibility."* This documents the alias for any reader.

## Note on the original instruction

The brief's mechanical `nb_content.replace('Aesthetic Risk Index', ...)` would have produced the artefact `Palette Boldness Index (PBI) (ARI)` from the existing xlabel `Aesthetic Risk Index (ARI)`. We instead used a curated, ordered map that yields clean labels (that xlabel becomes simply `Palette Boldness Index (PBI)`). All of the brief's intended substitutions (DV print, z-scored axis labels, ΔARI→ΔPBI, the DiD suptitle) are included.