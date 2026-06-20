# Stage W2F — Luxury vs Fast-Fashion: Lagged Monetary Channel (Placebo Test)

**Date:** 2026-06-02. **Figures:** `fast_fashion_comparison.png` (coefficients), `fast_fashion_pbi_trends.png` (PBI over time). **Underlying:** `_w2f.json`.

## Headline: the placebo does NOT confirm the production-calendar mechanism

> **This is an honest null/contradictory result.** The pre-registered prediction was that luxury brands (9–12-month design calendars) respond to the *prior-year* ECB rate while short-cycle fast-fashion/accessible brands (4–8-week cycles) do not. The data do **not** support that contrast. On a common scale the fast-fashion brands respond to lagged ECB at least as strongly as luxury, and the two slopes are statistically indistinguishable.

## Fast-fashion sample

5 accessible/contemporary brands, 191 usable cells, 20 year clusters: Isabel Marant (41 cells), Lacoste (33 cells), Tommy Hilfiger (38 cells), Tory Burch (60 cells), Vanessa Bruno (23 cells).

## 1. Per-panel models (each macro variable z-scored within its own panel)

| Regressor | Luxury coef | Luxury p (clustered) | Luxury p (wild) | FF coef | FF p (clustered) | FF p (wild) |
|---|---|---|---|---|---|---|
| Lagged ECB rate | -0.1034 | 0.0020 | 0.0475 | -0.0811 | 0.0493 | 0.3927 |
| Lagged EU GDP | +0.0767 | 0.0320 | 0.4958 | +0.0103 | 0.7822 | 0.8170 |
| Lagged EU recession | -0.1041 | 0.1365 | — | -0.0195 | 0.6781 | — |

Luxury N=1603 (23 yr-clusters, R²=0.285); FF N=191 (20 yr-clusters, R²=0.277).

At face value this *looks* like the predicted contrast: luxury lagged-ECB survives the wild bootstrap (p=0.047) while fast-fashion does not (p=0.39). **But this is misleading** — the FF coefficient (−0.081) is similar to luxury's (−0.103), and its non-significance is a small-sample power problem (5 brands, 191 cells), not a smaller effect. The per-panel z-scoring also puts the two coefficients on slightly different ECB scales, so they are not directly comparable.

## 2. The correct test: pooled interaction on a common scale

Pooling both panels and z-scoring the ECB rate once over the combined sample makes the slopes directly comparable. Model: `PBI ~ lagged_ECB_z * fast_fashion + brand FE + season FE`, year-clustered (N=1,796, 23 year clusters).

| Term | Estimate | p (clustered) | p (wild) |
|---|---|---|---|
| Lagged ECB (luxury slope) | −0.0801 | 0.014 | — |
| Lagged ECB × fast-fashion (difference) | **−0.0432** | **0.361** | **0.838** |
| ⇒ implied fast-fashion slope | **−0.1233** | — | — |

**The interaction is nowhere near significant** (clustered p=0.36; wild bootstrap p=0.84). On a common scale the fast-fashion slope (−0.123) is in fact *steeper* than the luxury slope (−0.080). We cannot reject that the two segments respond identically; the data lean, if anything, toward fast-fashion responding slightly more.

## 3. Interpretation (honest)

Following the pre-specified protocol for a failed placebo: *document the actual findings honestly and do not overstate the mechanism.* Concretely:

- **The lagged-ECB → palette-boldness association is NOT specific to long-cycle luxury production.** It appears, at comparable magnitude, in short-cycle accessible brands. The production-calendar story (collections planned 9–12 months out, so prior-year credit conditions constrain fabric/dyeing budgets) is therefore **not validated** by this placebo, and arguably undercut by it.
- **What the lagged-ECB effect more likely reflects** is a broad, industry-wide co-movement of palette boldness with the monetary/credit cycle that operates through channels common to all fashion segments — e.g. consumer-sentiment and retail-buying conditions, trend diffusion, or shared textile/colour-forecasting suppliers (Pantone/WGSN cycles) — rather than a luxury-specific budgeting mechanism. This is consistent with H3 (the response is industry-wide, not segment-specific).
- **Caveat — the placebo is underpowered.** With only 5 brands and 191 cells the fast-fashion panel cannot decisively confirm *or* rule out a difference. A back-of-envelope power calculation puts the **minimum detectable interaction at ≈0.11 PBI units** — roughly the size of the luxury main effect itself — so the test could only have caught a luxury/fast-fashion gap as large as the entire main effect. The correct statement is therefore that there is **no evidence of a differential response**, not that the responses are proven equal.

## 4. Recommended thesis language

> "To probe whether the lagged-ECB effect reflects the luxury production calendar specifically, we replicated the analysis on five accessible/short-cycle brands drawn from the same data and projected onto the identical PBI basis. The fast-fashion brands show a lagged-ECB response of comparable magnitude (pooled, common-scale slope −0.12 vs −0.08 for luxury), and a formal interaction test cannot distinguish the two segments (p=0.36; wild bootstrap p=0.84). We therefore do **not** interpret the lagged-ECB channel as evidence of a luxury-specific production-calendar mechanism. It is better read as an industry-wide co-movement of aesthetic boldness with monetary/credit conditions — consistent with our finding that the macro response is broadly shared rather than segmented."

## 5. What this does and does not change

- **H2 itself is unchanged and still holds:** prior-year ECB conditions predict palette boldness (luxury p_wild=0.047; CLIP semantic axis p_wild=0.0002). The *existence* of the lagged monetary channel is robust.
- **What changes is the mechanism narrative:** drop the production-calendar framing as a validated claim; present it at most as one candidate explanation among several, explicitly noting the fast-fashion placebo did not support it.
- This is a cleaner, more defensible position than asserting a mechanism the data contradict.
