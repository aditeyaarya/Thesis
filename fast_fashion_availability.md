# Stage W2A — Fast-Fashion / Short-Cycle Brand Availability

**Date:** 2026-06-02. **Source:** `VogueRunway.parquet` (1788 distinct designers). **Filters:** `section=='Collection'`, years 2000–2024, cell = brand×year×season, ≥15 images/cell, must cover both the GFC (2005–2011) and COVID (2017–2023) windows.

## Important framing

Pure fast-fashion labels (Zara, H&M, COS, Mango…) **do not stage Vogue Runway shows** and are absent from the dataset. The valid short-production-cycle comparison group is therefore **accessible / contemporary / mid-market** houses that *do* show on the runway but operate on much shorter design-to-shelf cycles (≈2–4 months, with reactive pre-collections) than the 9–12-month luxury planning calendar that underlies H2. These brands are the placebo: the production-calendar mechanism predicts **no** lagged-ECB effect for them.

## Candidates found (exact-name matches)

| Brand | Images (Collection) | Cells ≥15 imgs | Year range | GFC cov | COVID cov |
|---|---|---|---|---|---|
| Tory Burch | 1867 | 60 | 2006-2023 | ✓ | ✓ |
| DKNY | 2556 | 42 | 2000-2016 | ✓ | — |
| Isabel Marant | 1840 | 41 | 2009-2023 | ✓ | ✓ |
| Tommy Hilfiger | 2322 | 38 | 2000-2023 | ✓ | ✓ |
| Lacoste | 1907 | 33 | 2006-2022 | ✓ | ✓ |
| See by Chloé | 945 | 30 | 2012-2021 | — | ✓ |
| Paul & Joe | 1399 | 28 | 2011-2019 | ✓ | ✓ |
| Coach | 1496 | 28 | 2014-2023 | — | ✓ |
| Carven | 1314 | 27 | 2011-2018 | ✓ | ✓ |
| Vanessa Bruno | 796 | 23 | 2009-2020 | ✓ | ✓ |
| Kate Spade New York | 699 | 23 | 2013-2023 | — | ✓ |
| A.P.C. | 794 | 19 | 2012-2023 | — | ✓ |
| Zadig & Voltaire | 633 | 15 | 2013-2022 | — | ✓ |
| Sandro | 546 | 13 | 2015-2022 | — | ✓ |
| Maje | 302 | 9 | 2017-2021 | — | ✓ |
| Iro | 294 | 8 | 2015-2019 | — | ✓ |
| The Kooples | 101 | 4 | 2016-2019 | — | ✓ |
| Comptoir des Cotonniers | 42 | 2 | 2015-2016 | — | — |

## Not found in the dataset

These searched names returned no Collection rows: Zara, H&M, COS, Cos, Ba&sh, Claudie Pierlot, Rouje, Rouje Paris, See By Chloe, Calvin Klein, Pinko, Liu Jo, Kate Spade, Michael Kors, Michael Michael Kors. (Zara, H&M, COS etc. as expected — no runway presence.)

## Qualified (≥10 cells, both shock windows)

Seven brands qualify: Tory Burch, Isabel Marant, Tommy Hilfiger, Lacoste, Paul & Joe, Carven, Vanessa Bruno.

## Final selection (5 brands)

Chosen to maximise (a) short-cycle/accessible identity and (b) coverage across the full 2001–2023 span so the year-level lagged-ECB regressor is well-identified:

| Selected brand | `designer` string in parquet | Cells ≥15 | Span |
|---|---|---|---|
| Tommy Hilfiger | `Tommy Hilfiger` | 38 | 2000-2023 |
| Tory Burch | `Tory Burch` | 60 | 2006-2023 |
| Isabel Marant | `Isabel Marant` | 41 | 2009-2023 |
| Lacoste | `Lacoste` | 33 | 2006-2022 |
| Vanessa Bruno | `Vanessa Bruno` | 23 | 2009-2020 |

**Total: 195 brand-season-year cells (≥15 images each).** All five are accessible/contemporary houses with shorter production cycles than the luxury panel; Tommy Hilfiger, Tory Burch and Lacoste anchor the GFC window, all five cover COVID.

Brands considered but not selected: **DKNY** (strong GFC coverage but ends 2016 — no COVID), **Coach / Kate Spade / See by Chloé / A.P.C.** (no GFC coverage), **Paul & Joe / Carven** (qualify but only marginal GFC coverage; held as reserves).

If a larger placebo is later wanted, the broader non-luxury pool (Emporio Armani, Moschino, Balmain, Michael Kors Collection, etc., all with 49–77 cells and full 2000–2023 spans) is available in `_w2a.json` — though those skew back toward designer/luxury cycles and are less clean as a short-cycle placebo.
