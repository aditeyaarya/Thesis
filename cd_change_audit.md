# Stage W1A — Creative Director Change Audit & Correction

**Date:** 2026-06-02  
**Output:** updated `panel_full.csv` (now includes a `cd_change` column) + this report.

## 1. Summary

| | Cells flagged `cd_change=1` | % of 1,645-cell panel | Brands |
|---|---|---|---|
| **Old** (notebook dict, 10 brands) | 121 | 7.4% | 10 |
| **New** (corrected, 14 brands) | 141 | 8.6% | 14 |

**Important context.** `panel_full.csv` did **not** previously store a `cd_change` column on disk; the control was rebuilt inline inside the notebook (cells 53/55/72) from a 10-brand dictionary every time it ran. That 10-brand dictionary is treated as the *old/current* state here. This stage now writes a persisted, corrected `cd_change` column to `panel_full.csv` so every downstream cell reads an identical, auditable control.

## 2. What changed

Four brands were **added** (previously missing CD transitions inside the 2000–2024 window):

- **Alexander McQueen — 2010.** Lee McQueen died February 2010; Sarah Burton took over. A major creative discontinuity that was entirely absent from the old list.
- **Fendi — 2020.** Kim Jones became artistic director of womenswear/couture in 2020.
- **Jean Paul Gaultier — 2020.** Retired from ready-to-wear; the house went couture-only — a major format/palette shift.
- **Prada — 2020.** Raf Simons joined Miuccia Prada as co-creative director.

No previously-included brand/year was removed; the 10 original brands are unchanged.

## 3. Old vs new, by brand

`cd_change=1` is applied to the change year **and** the following (transition) year.

| Brand | Old change years | New change years | Status | In panel |
|---|---|---|---|---|
| Alexander McQueen | — | 2010 | ADDED (brand) | yes |
| Balenciaga | 2012, 2015 | 2012, 2015 | unchanged | yes |
| Burberry | 2018, 2022 | 2018, 2022 | unchanged | yes |
| Chanel | 2019 | 2019 | unchanged | yes |
| Christian Dior | 2011, 2012, 2016 | 2011, 2012, 2016 | unchanged | yes |
| Fendi | — | 2020 | ADDED (brand) | yes |
| Givenchy | 2017, 2020 | 2017, 2020 | unchanged | yes |
| Gucci | 2015, 2023 | 2015, 2023 | unchanged | yes |
| Jean Paul Gaultier | — | 2020 | ADDED (brand) | yes |
| Louis Vuitton | 2013 | 2013 | unchanged | yes |
| Maison Margiela | 2014 | 2014 | unchanged | yes |
| Prada | — | 2020 | ADDED (brand) | yes |
| Saint Laurent | 2012, 2016 | 2012, 2016 | unchanged | yes |
| Valentino | 2008, 2016 | 2008, 2016 | unchanged | yes |

### Cells actually flagged in the panel (new version)

(Distinct flagged years that intersect the brand's panel coverage; a year appears as a cell for each season present.)

| Brand | Flagged years present in panel |
|---|---|
| Alexander McQueen | 2010, 2011 |
| Balenciaga | 2012, 2013, 2015, 2016 |
| Burberry | 2018, 2019, 2022, 2023 |
| Chanel | 2019, 2020 |
| Christian Dior | 2011, 2012, 2013, 2016, 2017 |
| Fendi | 2020, 2021 |
| Givenchy | 2017, 2018, 2020, 2021 |
| Gucci | 2015, 2016, 2023 |
| Jean Paul Gaultier | 2020, 2021 |
| Louis Vuitton | 2013, 2014 |
| Maison Margiela | 2014, 2015 |
| Prada | 2020, 2021 |
| Saint Laurent | 2012, 2013, 2016, 2017 |
| Valentino | 2008, 2009, 2016, 2017 |

## 4. Brands deliberately left at `cd_change=0` throughout

These houses had the **same** creative leadership across 2000–2024 (or transitions outside the window) and are intentionally never flagged:

- **Versace** — Donatella Versace continuously since 1997.
- **Stella McCartney** — sole creative director throughout.
- **Giorgio Armani, Ralph Lauren, Rick Owens, Dolce & Gabbana** — founder-led throughout.
- **Missoni** — family-run (Angela Missoni) across the window.
- **Max Mara** — house style, no single named CD.
- **Dries Van Noten** — founder-led; retirement (2024) falls outside the analysis window, so no change is coded.

## 5. Uncertain / judgement calls

- **Prada 2020 (Raf Simons).** Coded as a change because it was a genuine co-creative-director appointment with public creative impact, even though Miuccia Prada remained. A stricter rule ("only full handovers") would exclude it; we include it to be conservative about controlling for palette discontinuities.
- **Jean Paul Gaultier 2020.** Coded as a change: the RTW line ended and the house pivoted to couture-only, which is a format/palette discontinuity rather than a personnel swap.
- **Maison Margiela 2014.** Martin Margiela left in 2009 but the house continued without a named CD until John Galliano in 2014; only the 2014 Galliano arrival is coded.
- **Balenciaga 2012.** Ghesquière's 2012 departure is retained from the old list even though Alexander Wang's tenure (2012–2015) is short; both 2012 and the 2015 Demna arrival are flagged.

_Panel after correction: 1645 rows × 42 columns._