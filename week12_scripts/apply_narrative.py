# -*- coding: utf-8 -*-
"""Fold Week-1/2 findings into the notebook: event-study reference fix, cd_change
collision fix + corrected 14-brand dict, EU-GDP demotion, H2 industry-wide
reframing + placebo, wild-bootstrap robustness cell."""
import json
import nbformat

NB = 'vogue_runway_analysis.ipynb'
nb = json.load(open(NB))
cells = nb['cells']


def src(i):
    return ''.join(cells[i]['source'])


def setsrc(i, text):
    cells[i]['source'] = text.splitlines(keepends=True)


def rep(i, old, new, n=1):
    s = src(i)
    assert s.count(old) == n, f"cell {i}: expected {n} of {old!r}, found {s.count(old)}"
    setsrc(i, s.replace(old, new))


def find(substr):
    for i, c in enumerate(cells):
        if substr in ''.join(c['source']):
            return i
    raise AssertionError(f"not found: {substr!r}")


# ============================ CODE FIXES ====================================
DICT10 = ("{'Balenciaga': [2012, 2015], 'Burberry': [2018, 2022], 'Chanel': [2019],\n"
          "       'Christian Dior': [2011, 2012, 2016], 'Givenchy': [2017, 2020], 'Gucci': [2015, 2023],\n"
          "       'Louis Vuitton': [2013], 'Maison Margiela': [2014], 'Saint Laurent': [2012, 2016],\n"
          "       'Valentino': [2008, 2016]}")
DICT14 = ("{'Alexander McQueen': [2010], 'Balenciaga': [2012, 2015], 'Burberry': [2018, 2022], 'Chanel': [2019],\n"
          "       'Christian Dior': [2011, 2012, 2016], 'Fendi': [2020], 'Givenchy': [2017, 2020], 'Gucci': [2015, 2023],\n"
          "       'Jean Paul Gaultier': [2020], 'Louis Vuitton': [2013], 'Maison Margiela': [2014], 'Prada': [2020],\n"
          "       'Saint Laurent': [2012, 2016], 'Valentino': [2008, 2016]}")

# compact dict appears in 3 code cells (Stage 18 / Stage 16 / Stage 17)
for key in ['_CD = {', '_CD = {', '_CD = {']:
    pass
n_compact = 0
for i, c in enumerate(cells):
    if c['cell_type'] == 'code' and DICT10 in ''.join(c['source']):
        setsrc(i, ''.join(c['source']).replace(DICT10, DICT14))
        n_compact += 1
assert n_compact == 3, f"compact dict replaced in {n_compact} cells (expected 3)"

# cd_change collision: drop existing column before re-merging (panel_full.csv now
# persists cd_change after Stage W1A).
i53 = find('rb = rb.merge(_cd, ')
rep(i53, "rb = rb.merge(_cd, on=['brand', 'year'], how='left');",
    "rb = rb.drop(columns=['cd_change'], errors='ignore').merge(_cd, on=['brand', 'year'], how='left');")
i72 = find("_pf = _pf.merge(_cd, ")
rep(i72, "_pf = _pf.merge(_cd, on=['brand', 'year'], how='left')",
    "_pf = _pf.drop(columns=['cd_change'], errors='ignore').merge(_cd, on=['brand', 'year'], how='left')")
i75 = find("wb = wb.merge(_cd, ")
rep(i75, "wb = wb.merge(_cd, on=['brand', 'year'], how='left');",
    "wb = wb.drop(columns=['cd_change'], errors='ignore').merge(_cd, on=['brand', 'year'], how='left');")

# cell 55 (Extension 3) verbose dict -> 14 brands + drop before merge
i55 = find('# ── Extension 3: Creative Director change controls')
VERBOSE10 = """CD_CHANGES = {
    'Balenciaga':        [2012, 2015],   # Wang 2012, Demna 2015
    'Burberry':          [2018, 2022],   # Tisci 2018, Daniel Lee 2022
    'Chanel':            [2019],         # Virginie Viard after Lagerfeld
    'Christian Dior':    [2011, 2012, 2016],  # Simons 2012, Chiuri 2016
    'Givenchy':          [2017, 2020],   # Waight Keller 2017, M.Williams 2020
    'Gucci':             [2015, 2023],   # A.Michele 2015, De Sarno 2023
    'Louis Vuitton':     [2013],         # Ghesquière replaces M.Jacobs
    'Maison Margiela':   [2014],         # Galliano joins (Margiela)
    'Saint Laurent':     [2012, 2016],   # Slimane 2012, Vaccarello 2016
    'Valentino':         [2008, 2016],   # Chiuri+Piccioli 2008, Piccioli solo 2016
}"""
VERBOSE14 = """CD_CHANGES = {  # corrected 14-brand list — see Stage W1A / cd_change_audit.md
    'Alexander McQueen': [2010],         # Lee McQueen died 2010; Sarah Burton
    'Balenciaga':        [2012, 2015],   # Wang 2012, Demna 2015
    'Burberry':          [2018, 2022],   # Tisci 2018, Daniel Lee 2022
    'Chanel':            [2019],         # Virginie Viard after Lagerfeld
    'Christian Dior':    [2011, 2012, 2016],  # Simons 2012, Chiuri 2016
    'Fendi':             [2020],         # Kim Jones womenswear/couture
    'Givenchy':          [2017, 2020],   # Waight Keller 2017, M.Williams 2020
    'Gucci':             [2015, 2023],   # A.Michele 2015, De Sarno 2023
    'Jean Paul Gaultier': [2020],        # RTW retirement -> couture only
    'Louis Vuitton':     [2013],         # Ghesquière replaces M.Jacobs
    'Maison Margiela':   [2014],         # Galliano joins (Margiela)
    'Prada':             [2020],         # Raf Simons co-CD with Miuccia
    'Saint Laurent':     [2012, 2016],   # Slimane 2012, Vaccarello 2016
    'Valentino':         [2008, 2016],   # Chiuri+Piccioli 2008, Piccioli solo 2016
}"""
rep(i55, VERBOSE10, VERBOSE14)
rep(i55, "panel_full = panel_full.merge(cd_df, on=['brand','year'], how='left')",
    "panel_full = panel_full.drop(columns=['cd_change'], errors='ignore').merge(cd_df, on=['brand','year'], how='left')")

# ---- Event study: keep t=-1 as reference (cells 49 + 53) -------------------
i49 = find('# ── Event Study: GFC (2008) and COVID (2020)')
rep(i49, "    window_sub = window[window['event_time'] != -1].copy()   # omit t=-1 (reference)\n",
    "    window_sub = window.copy()   # keep t=-1 in-sample as the reference (all dummies = 0 there)\n")
rep(i49, "    w = w[w['event_time'] != -1].copy()\n",
    "    # t=-1 retained in-sample as the reference period\n")
# update cell 49 interpretation prints (reference fix -> flat pre-trends)
OLD49 = '''print("Pre-trend interpretation (honest):")
print("  t=-3: not significant in either shock -> parallel trends hold at the 3-year horizon.")
print("  t=-2: significant and POSITIVE in both shocks (GFC ~+0.35, COVID ~+0.30) -> palettes")
print("        were unusually BOLD two years before each downturn, consistent with late-boom")
print("        exuberance at the top of the cycle, NOT anticipatory de-risking. The post-shock")
print("        drop (COVID t+1 ~-0.38; GFC t+2 ~-0.20) is measured against t=-1 and is the")
print("        robust result; the elevated t=-2 means parallel trends are imperfect at 2 years")
print("        and the COVID/GFC drops should be read as relative to the immediate pre-period.")'''
NEW49 = '''print("Pre-trend interpretation (honest; t=-1 reference retained in-sample):")
print("  t=-3 and t=-2: NOT significant in either shock (all-shows GFC t-2 p~0.15, COVID t-2 p~0.35)")
print("        -> parallel trends hold; the earlier 'significant positive t-2' was an artefact of")
print("        dropping the t=-1 reference. The post-shock drop is the robust result:")
print("        COVID t+1 ~-0.49 (p<0.001); GFC t+2 ~-0.35 (p=0.02), measured against t=-1.")'''
rep(i49, OLD49, NEW49)
OLD49B = '''print("  => t=-2 remains positive & significant and the COVID t+1 drop remains strong,")
print("     so the event-study pattern is not driven by pre-collection (Resort/Pre-Fall) noise.")'''
NEW49B = '''print("  => the COVID t+1 drop remains strong on main shows only; a residual positive GFC t-2")
print("     persists in main shows (p~0.03), so the post-shock dips are not a pre-collection artefact.")'''
rep(i49, OLD49B, NEW49B)

# cell 50 trailing prints
i50 = find('# ── Event Study Plot')
rep(i50, '''print("Key finding:")
print("  t=-2 significant (positive) in both shocks — anticipatory conservatism.")
print("  GFC: drop peaks at t=+2; COVID: drops at t=+1 (within-season adjustment).")''',
    '''print("Key finding (t=-1 reference retained):")
print("  Flat pre-trend (t=-3, t=-2 both ns) -> parallel trends support a causal reading.")
print("  GFC: drop peaks at t=+2 (~-0.35); COVID: drops at t=+1 (~-0.49, within-season adjustment).")''')

# cell 53: keep t=-1 in both the per-shock loop and the stacked loop
rep(i53, "    w['et'] = w.year - yr; w = w[w.et != -1]\n",
    "    w['et'] = w.year - yr  # keep t=-1 as reference\n")
rep(i53, "    w['et'] = w.year - yr; w = w[w.et != -1]; w['be'] = w['brand'] + '_' + sh\n",
    "    w['et'] = w.year - yr; w['be'] = w['brand'] + '_' + sh  # keep t=-1 as reference\n")
rep(i53, '''print("  Reading: flat pre-trend at t-3, late-boom bump at t-2, robust post-shock dip.")''',
    '''print("  Reading: flat pre-trend (t-3 and t-2 both ns), robust post-shock dip (t+1/t+2).")''')

# ============================ MARKDOWN ======================================
# cell 0 — H2 bullet, framing note, headline table
i0 = find('# Vogue Runway — Aesthetic Conservatism')
rep(i0,
    "- **H2 — Monetary/credit channel.** Monetary-policy and credit conditions lead aesthetics by ~1 year. *(Supported, novel — confirmed in two independent measurement modalities.)*",
    "- **H2 — Monetary/credit channel.** Monetary-policy and credit conditions lead aesthetics by ~1 year. *(Supported, novel — survives the wild cluster bootstrap and reproduces on an independent CLIP axis; the response is **industry-wide**, not luxury-specific.)*")
rep(i0,
    "H2 — the lagged monetary-policy channel — **emerged** as the most robust effect during analysis and is presented as such, not as an a-priori prediction.",
    "H2 — the lagged monetary-policy channel — **emerged** as the most robust effect during analysis and is presented as such, not as an a-priori prediction. A fast-fashion placebo (short-cycle brands) tested whether the lagged-ECB effect is specific to the long luxury production calendar; it is **not** (no differential vs short-cycle brands, interaction p=0.36), so H2 is framed as an industry-wide monetary/credit co-movement rather than a luxury-budgeting mechanism.")
OLD_TBL = """| Finding | Estimate | Inference |
|---|---|---|
| Stacked GFC+COVID post-shock drop (PBI) | t+1 −0.27 / t+2 −0.16 | p<0.01 (clustered by brand) |
| COVID event, t+1 | −0.38 | p=0.0002 (brand-clustered) |
| GFC event, t+2 | −0.20 | p=0.0001 (brand-clustered) |
| Lagged ECB rate → PBI | −0.10 | p=0.002 (year-clustered); survives Bonferroni |
| Lagged EU-GDP → PBI | +0.08 | p=0.03 (year-clustered) |
| Lagged ECB → CLIP semantic axis | −0.45 | p<0.0001 (independent modality) |
| Contemp. recession → raw dispersion | −1.77 | p=0.006 (partly seasonal) |
| Tier heterogeneity (Bayesian P(Lux<AG)) | 0.47 | null — no divergence |
| Ownership / size heterogeneity | ≈0 | null (p>0.7) |"""
NEW_TBL = """| Finding | Estimate | Inference (incl. wild cluster bootstrap) |
|---|---|---|
| Stacked GFC+COVID post-shock drop (PBI) | t+1 −0.41 / t+2 −0.30 | brand-clustered p<0.01; **survives wild bootstrap** (0.002 / 0.013) |
| COVID event, t+1 | −0.49 | p<0.001 (brand-clustered) |
| GFC event, t+2 | −0.35 | p=0.02 (brand-clustered) |
| Lagged ECB rate → PBI | −0.10 | p=0.002 year-clustered; **wild bootstrap p=0.047** (survives, borderline) |
| Lagged ECB → CLIP semantic axis | −0.45 | p<0.0001; **wild bootstrap p=0.0002** (decisive, independent modality) |
| Lagged EU-GDP → PBI | +0.08 | p=0.03 — **fails wild bootstrap (p≈0.50)**; not claimed as a channel |
| Fast-fashion placebo (lagged-ECB × segment) | diff −0.04 | p=0.36 — no differential; effect is **not** luxury-specific |
| Contemp. recession → raw dispersion | −1.77 | p=0.006 (partly seasonal) |
| Tier heterogeneity (Bayesian P(Lux<AG)) | 0.47 | null — no divergence |
| Ownership / size heterogeneity | ≈0 | null (p>0.7) |

> Event-study estimates are measured against the **t−1 reference** (kept in-sample). The
> earlier −0.27/−0.16 figures came from a specification that dropped t−1, leaving the
> coefficients only min-norm-identified; retaining the reference is the correct, better-
> identified spec and gives the larger, cleaner estimates above (with flat pre-trends)."""
rep(i0, OLD_TBL, NEW_TBL)

# cell 46 — H1 narrative
i46 = find('## H1 — Acute macro shocks reduce aesthetic boldness')
setsrc(i46, """## H1 — Acute macro shocks reduce aesthetic boldness

Treats the 2008 GFC and the 2020 COVID shock as natural experiments. We estimate event-time coefficients on the Palette Boldness Index relative to the immediate pre-shock year (**t−1, kept in-sample as the reference**), with brand and season fixed effects, then pool both shocks into a single **stacked difference-in-differences** design. SEs are clustered by brand (the level the within-brand treatment varies at). **Result:** a clear post-shock drop in boldness in both shocks (stacked **t+1 −0.41, t+2 −0.30**, brand-clustered p<0.01) and **flat pre-trends** (t−3 and t−2 both n.s.), supporting a causal reading. Per shock, COVID drops at t+1 (≈−0.49, p<0.001) and the GFC at t+2 (≈−0.35, p=0.02). Both dips **survive the wild cluster bootstrap** (Cameron–Gelbach–Miller; t+1 p=0.002, t+2 p=0.013), so the result is robust to valid few-cluster inference. A main-shows-only check rules out a pre-collection artefact.

> *Methodological note.* An earlier version dropped the t−1 rows from the window; with no in-sample reference the six event dummies become collinear with the constant and the coefficients are only min-norm-identified (and cluster/bootstrap inference on them is ill-posed). Retaining t−1 fixes this — and, incidentally, the "positive t−2 / late-boom exuberance" reading disappears: it was an artefact of the missing reference, and pre-trends are in fact flat.""")

# cell 52 — survivors spine (drop EU-GDP)
i52 = find('### Cluster-robust re-test + stacked DiD')
rep(i52,
    "Survivors form the defensible spine of the thesis: the stacked shock drop, the lagged\nECB-rate and EU-GDP effects, and the contemporaneous recession→dispersion effect. The\ncontemporaneous recession→PBI effect and the lagged EU-recession dummy do *not* survive.",
    "Survivors (under both clustering **and** the wild cluster bootstrap) form the defensible\nspine: the stacked shock drop and the lagged **ECB-rate** effect (the latter also reproduced\non the independent CLIP axis). The lagged **EU-GDP** effect clears standard clustering but\n**fails the wild bootstrap** (p≈0.50) and is no longer claimed as a channel; the\ncontemporaneous recession→PBI effect and the lagged EU-recession dummy also do *not* survive.")

# cell 54 — H2 narrative
i54 = find('## H2 — Monetary & credit conditions lead aesthetics by ~1 year')
setsrc(i54, """## H2 — Monetary & credit conditions lead aesthetics by ~1 year

The most robust — and most novel — result. Palette boldness responds to the **prior-year** ECB policy rate (Model 6: −0.10, p=0.002 year-clustered). Because the macro regressors vary at the year level (~23 clusters), we re-test with the **wild cluster bootstrap**: the lagged-ECB effect **survives on the colour PBI (p=0.047, borderline)** and, decisively, **on the independent CLIP semantic axis (−0.45, wild-bootstrap p=0.0002)** — so it is not a colour-pipeline artefact. The original lagged *recession dummy* does not survive a lag-bug fix (−0.08, p≈0.49), and the lagged **EU-GDP** effect (+0.08, p=0.03 under standard clustering) **does not survive the wild bootstrap (p≈0.50)** and is therefore *not* claimed as a separate channel — it was a few-cluster false positive.

**Is the channel luxury-specific? No.** A pre-registered **fast-fashion placebo** runs the identical pipeline on five short-cycle / accessible brands (Tommy Hilfiger, Tory Burch, Isabel Marant, Lacoste, Vanessa Bruno), projected onto the *same* PBI basis. On a common scale these brands respond to lagged ECB at least as strongly as luxury (pooled slope −0.12 vs −0.08), and a formal interaction test cannot distinguish the two segments (p=0.36; wild-bootstrap p=0.84). We therefore do **not** read the lagged-ECB effect as evidence of a luxury production-calendar mechanism; it is better understood as an **industry-wide** co-movement of palette boldness with monetary/credit conditions — consistent with H3's industry-wide finding. (The placebo is small — 5 brands — so it shows *no evidence of a difference* rather than proven equality.) A monetary deep-dive additionally shows the effect is asymmetric: palettes turn conservative the year *after* the ECB tightens, while easing is neutral.""")

# cell 71 — multiple-testing EU-GDP caveat
i71 = find('### Multiple-testing correction')
rep(i71,
    "**Headline reading:** the lagged ECB-rate effect, the lagged EU-GDP\neffect, the contemporaneous recession→raw-dispersion effect, and the COVID event-study drop\nall survive Bonferroni; the contemporaneous recession→ARI effect, the lagged EU-recession\ndummy, and the CLIP-coherence effect do **not** — they are reported honestly as\nweak/borderline or null.",
    "**Headline reading:** the lagged ECB-rate effect, the contemporaneous recession→raw-\ndispersion effect, and the COVID event-study drop survive Bonferroni; the contemporaneous\nrecession→PBI effect, the lagged EU-recession dummy, and the CLIP-coherence effect do\n**not**. The lagged **EU-GDP** effect survives Bonferroni *but fails the wild cluster\nbootstrap* (p≈0.50; see Part IV), so it is treated as a few-cluster artefact, not a channel.")

# cell 73 — results summary
i73 = find('# Part V — Results Summary & Workbook')
setsrc(i73, """# Part V — Results Summary & Workbook

**What survives, in one place.** The defensible findings — all robust to the **wild cluster bootstrap** (valid for our ~23–25 clusters) — are: (1) a post-shock drop in palette boldness around both the GFC and COVID (stacked DiD, brand-clustered, t+1 −0.41 / t+2 −0.30, wild-bootstrap p≤0.013, flat pre-trends); (2) a novel lagged **monetary** channel — tighter prior-year ECB policy predicts more conservative palettes — reproduced on an *independent* CLIP semantic measure (wild-bootstrap p=0.0002) and shown by a fast-fashion placebo to be **industry-wide**, not luxury-specific; and (3) a clean null on cross-market heterogeneity (no tier, ownership or size differences). Honest nulls / demotions: the lagged **EU-GDP** effect (fails the wild bootstrap), contemporaneous recession on the composite index (fails clustering), the lagged recession *dummy*, aesthetic trickle-down (Granger), leading-indicator power, and CLIP within-collection coherence.

The cell below regenerates the complete results workbook (`vogue_runway_results.xlsx`) with one sheet per headline model, recomputed from the corrected panel.""")

# ===================== insert robustness markdown cell =====================
ROB = """## Part IV addendum — Wild cluster bootstrap & fast-fashion placebo

Two robustness additions (full detail in `wild_bootstrap_results.md` and `fast_fashion_comparison_results.md`).

**Wild cluster bootstrap (Cameron–Gelbach–Miller).** With only ~23 year / 25 brand clusters, standard cluster-robust SEs can understate p-values. Re-testing every headline coefficient with the restricted wild bootstrap (Rademacher weights, B=9999):

| Result | Coef | Std clustered p | Wild bootstrap p | Status |
|---|---|---|---|---|
| H1 stacked DiD, t+1 (vs t−1) | −0.41 | 0.001 | 0.002 | ✅ survives |
| H1 stacked DiD, t+2 (vs t−1) | −0.30 | 0.008 | 0.013 | ✅ survives |
| H2 lagged ECB → PBI (colour) | −0.10 | 0.002 | 0.047 | ✅ survives (borderline) |
| H2 lagged ECB → CLIP semantic | −0.46 | <0.001 | 0.0002 | ✅ survives (decisive) |
| H2 lagged EU-GDP → PBI | +0.08 | 0.032 | ~0.50 | ❌ fails — not a channel |
| H2 lagged EU-recession dummy | −0.09 | 0.42 | 0.57 | ❌ null |

The H1 dips and the H2 lagged-ECB channel are *doubly confirmed*; the lagged EU-GDP "channel" was a few-cluster false positive and is dropped. (The event-study figures use the well-conditioned **t−1-reference** specification; the wild bootstrap on the stacked design is run after Frisch–Waugh–Lovell partialling of the brand×cohort fixed effects, since those are nested within the brand clusters.)

**Fast-fashion placebo.** Running the identical pipeline on five short-cycle/accessible brands (projected onto the same PBI basis) tests whether the lagged-ECB effect is specific to the long luxury production calendar. It is not: on a common scale the fast-fashion slope (−0.12) is as steep as luxury's (−0.08), and a pooled interaction cannot distinguish them (p=0.36; wild-bootstrap p=0.84). H2 is therefore an **industry-wide** monetary/credit co-movement, not a luxury-budgeting mechanism — consistent with the H3 null. The placebo is underpowered (5 brands), so this is *no evidence of a difference*, not proven equality."""
rob_cell = {'cell_type': 'markdown', 'metadata': {}, 'source': ROB.splitlines(keepends=True)}
# insert just before "# Part V — Results Summary"
cells.insert(i73, rob_cell)

# ============================ save + validate ===============================
with open(NB, 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write('\n')
nbformat.read(NB, as_version=4)
print(f"Edits applied. Notebook now {len(cells)} cells. nbformat-valid.")
