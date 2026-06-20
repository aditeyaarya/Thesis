"""Stage W2F — Comparative analysis: luxury vs fast-fashion H2 (placebo test)."""
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wildboottest.wildboottest import wildboottest

warnings.filterwarnings('ignore')

lux = pd.read_csv('panel_full.csv')
ff = pd.read_csv('fast_fashion_panel_full.csv')

for col, z in [('vix_annual_mean', 'vix_z'), ('gdp_growth_world', 'gdp_z'),
               ('ecb_rate', 'ecb_z'), ('eu_gdp_growth', 'eu_gdp_z')]:
    if col in lux.columns:
        lux[z] = (lux[col] - lux[col].mean()) / lux[col].std()
    if col in ff.columns:
        ff[z] = (ff[col] - ff[col].mean()) / ff[col].std()

LUX_FORMULA = ('ARI ~ ecb_z_lag1 + eu_gdp_z_lag1 + eu_recession_lag1 '
               '+ cd_change + C(brand) + C(season)')
FF_FORMULA = ('ARI ~ ecb_z_lag1 + eu_gdp_z_lag1 + eu_recession_lag1 '
              '+ C(brand) + C(season)')
KEYS = ['ecb_z_lag1', 'eu_gdp_z_lag1', 'eu_recession_lag1']

lux_d = lux.dropna(subset=['ARI', 'ecb_z_lag1', 'eu_gdp_z_lag1'])
ff_d = ff.dropna(subset=['ARI', 'ecb_z_lag1', 'eu_gdp_z_lag1'])

m_lux = smf.ols(LUX_FORMULA, data=lux_d).fit(
    cov_type='cluster', cov_kwds={'groups': lux_d['year']})
m_ff = smf.ols(FF_FORMULA, data=ff_d).fit(
    cov_type='cluster', cov_kwds={'groups': ff_d['year']})


def stars(p):
    return '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.10 else 'ns'


print(f"=== LUXURY (year-clustered) N={int(m_lux.nobs)} "
      f"{lux_d['year'].nunique()} yr-clusters R²={m_lux.rsquared:.3f} ===")
for k in KEYS:
    print(f"  {k}: coef={m_lux.params[k]:+.4f} p={m_lux.pvalues[k]:.4f} {stars(m_lux.pvalues[k])}")
print(f"\n=== FAST-FASHION (year-clustered) N={int(m_ff.nobs)} "
      f"{ff_d['year'].nunique()} yr-clusters {ff_d['brand'].nunique()} brands "
      f"R²={m_ff.rsquared:.3f} ===")
for k in KEYS:
    print(f"  {k}: coef={m_ff.params[k]:+.4f} p={m_ff.pvalues[k]:.4f} {stars(m_ff.pvalues[k])}")


def pkg_wild(res, data, param, B=9999):
    cl = pd.factorize(data['year'])[0].astype(np.int64)
    r = wildboottest(model=res.model, param=param, cluster=cl, B=B,
                     weights_type='rademacher', impose_null=True,
                     bootstrap_type='11', seed=42, show=False)
    return float(r.loc[param, 'p-value'])


def manual_wcr(formula, data, param, B=4999, seed=42):
    rng = np.random.default_rng(seed)
    full = smf.ols(formula, data=data).fit(
        cov_type='cluster', cov_kwds={'groups': data['year']})
    t_obs = full.params[param] / full.bse[param]
    terms = [t.strip() for t in formula.split('~', 1)[1].split('+')]
    fr = formula.split('~', 1)[0].strip() + ' ~ ' + ' + '.join([t for t in terms if t != param])
    restr = smf.ols(fr, data=data).fit()
    fit_r, res_r = restr.fittedvalues.values, restr.resid.values
    clusters = data['year'].values
    uniq = np.unique(clusters)
    dv = formula.split('~', 1)[0].strip()
    grp = data['year']
    db = data.copy()
    tb = []
    for _ in range(B):
        wts = rng.choice([-1.0, 1.0], size=len(uniq))
        wmap = dict(zip(uniq, wts))
        ow = np.array([wmap[c] for c in clusters])
        db[dv] = fit_r + res_r * ow
        try:
            mb = smf.ols(formula, data=db).fit(
                cov_type='cluster', cov_kwds={'groups': grp})
            tb.append(mb.params[param] / mb.bse[param])
        except Exception:
            continue
    tb = np.asarray(tb)
    return float(np.mean(np.abs(tb) >= np.abs(t_obs)))


print("\n=== Wild bootstrap ===")
wild = {'lux': {}, 'ff': {}}
for param in ['ecb_z_lag1', 'eu_gdp_z_lag1']:
    try:
        pl = pkg_wild(m_lux, lux_d, param)
    except Exception:
        pl = manual_wcr(LUX_FORMULA, lux_d, param)
    try:
        pf_ = pkg_wild(m_ff, ff_d, param)
    except Exception as e:
        print(f"  (ff package failed for {param}: {e}; using manual)")
        pf_ = manual_wcr(FF_FORMULA, ff_d, param)
    wild['lux'][param] = pl
    wild['ff'][param] = pf_
    print(f"  {param}: luxury p_wild={pl:.4f} | fast-fashion p_wild={pf_:.4f} "
          f"{'(FF UNEXPECTED SIG)' if pf_ < 0.05 else '(FF null as predicted)'}")

# ---- Figure 1: coefficient comparison ---------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
labels = {'ecb_z_lag1': 'Lagged ECB Rate', 'eu_gdp_z_lag1': 'Lagged EU GDP Growth',
          'eu_recession_lag1': 'Lagged EU Recession'}
for ax, (pname, model, color) in zip(axes, [
        (f'Luxury (25 brands)', m_lux, '#1a1a2e'),
        (f'Fast-Fashion ({ff_d["brand"].nunique()} brands)', m_ff, '#e94560')]):
    coefs, lo, hi, pv, plab = [], [], [], [], []
    ci = model.conf_int()
    for k in KEYS:
        if k in model.params.index:
            coefs.append(model.params[k]); lo.append(ci[0][k]); hi.append(ci[1][k])
            pv.append(model.pvalues[k]); plab.append(labels[k])
    y = range(len(plab))
    ax.barh(y, coefs, xerr=[[c - l for c, l in zip(coefs, lo)],
                            [h - c for c, h in zip(coefs, hi)]],
            color=color, alpha=0.75, height=0.5, capsize=5)
    for i, (c, p) in enumerate(zip(coefs, pv)):
        ax.text(hi[i] + 0.01 if c > 0 else lo[i] - 0.01, i, f'{c:+.3f} {stars(p)}',
                va='center', ha='left' if c > 0 else 'right', fontsize=9)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_yticks(list(y)); ax.set_yticklabels(plab)
    ax.set_xlabel('Coefficient (year-clustered SEs, 95% CI)')
    ax.set_title(f'{pname}\nN={int(model.nobs)} cells  R²={model.rsquared:.3f}')
plt.suptitle('Lagged Monetary Channel: Luxury vs Fast-Fashion\n'
             'Prediction: ECB lag significant for luxury (long production cycles), '
             'null for fast-fashion (short cycles)', fontsize=12)
plt.tight_layout()
plt.savefig('fast_fashion_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nSaved fast_fashion_comparison.png")

# ---- Figure 2: PBI trends ----------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 6))
shocks = {2001: '9/11', 2008: 'GFC', 2020: 'COVID'}
lux_annual = lux.groupby('year')['ARI'].mean().reset_index()
ax.plot(lux_annual['year'], lux_annual['ARI'], color='#1a1a2e', linewidth=2.5,
        marker='o', markersize=4, label='Luxury (25-brand avg)', zorder=3)
ff_annual = ff.groupby(['brand', 'year'])['ARI'].mean().reset_index()
for brand, g in ff_annual.groupby('brand'):
    ax.plot(g['year'], g['ARI'], linewidth=1.4, marker='s', markersize=3, alpha=0.7,
            label=f'FF: {brand}')
ymin, ymax = ax.get_ylim()
for yr, lbl in shocks.items():
    ax.axvline(yr, color='grey', linestyle='--', alpha=0.5, linewidth=1.2)
    ax.text(yr + 0.1, ymax * 0.95, lbl, color='grey', fontsize=8, va='top')
ax.axhline(0, color='black', linewidth=0.5, linestyle=':')
ax.set_xlabel('Year')
ax.set_ylabel('Palette Boldness Index (PBI, z-scored to luxury distribution)')
ax.set_title('PBI Over Time: Luxury vs Fast-Fashion (2000–2023)')
ax.legend(fontsize=8, ncol=2)
plt.tight_layout()
plt.savefig('fast_fashion_pbi_trends.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fast_fashion_pbi_trends.png")

# ---- persist for report ------------------------------------------------------
def coefrow(m, k):
    return {'coef': round(m.params[k], 4), 'p': round(m.pvalues[k], 4)} if k in m.params.index else None

out = {
    'lux': {'n': int(m_lux.nobs), 'yr_clusters': int(lux_d['year'].nunique()),
            'r2': round(m_lux.rsquared, 3), 'coefs': {k: coefrow(m_lux, k) for k in KEYS}},
    'ff': {'n': int(m_ff.nobs), 'yr_clusters': int(ff_d['year'].nunique()),
           'brands': int(ff_d['brand'].nunique()), 'r2': round(m_ff.rsquared, 3),
           'brand_list': sorted(ff_d['brand'].unique().tolist()),
           'cells_per_brand': ff.groupby('brand').size().to_dict(),
           'coefs': {k: coefrow(m_ff, k) for k in KEYS}},
    'wild': wild,
}
json.dump(out, open('week12_scripts/_w2f.json', 'w'), indent=2, default=str)
print("Saved _w2f.json")
