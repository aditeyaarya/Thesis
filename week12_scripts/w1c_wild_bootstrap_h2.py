"""Stage W1C — Wild cluster bootstrap for H2 (monetary channel).

Headline robustness check: does the lagged-ECB-rate effect survive valid
few-cluster inference (23 year clusters)?

Primary engine: the `wildboottest` package (Roodman/MacKinnon WCR score bootstrap,
null imposed = WCR, Rademacher weights, B=9999).

Cross-check: a correct manual WCR-t bootstrap (refit the RESTRICTED model that
imposes H0: beta_param = 0, perturb its residuals by cluster-level Rademacher
weights, refit the UNRESTRICTED model, compare cluster-robust t-stats). This
imposes the null properly, unlike the brief's fallback which perturbed
unrestricted fitted values.
"""
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from wildboottest.wildboottest import wildboottest

warnings.filterwarnings('ignore')
RNG_SEED = 42
B_PKG = 9999
B_MANUAL = 1999

# ---------------------------------------------------------------------------
# Data prep (z-scores recomputed fresh, never trust saved).
# ---------------------------------------------------------------------------
pf = pd.read_csv('panel_full.csv')
for col, z in [('vix_annual_mean', 'vix_z'), ('gdp_growth_world', 'gdp_z'),
               ('ecb_rate', 'ecb_z'), ('eu_gdp_growth', 'eu_gdp_z')]:
    if col in pf.columns:
        pf[z] = (pf[col] - pf[col].mean()) / pf[col].std()

data_h2 = pf.dropna(subset=['ARI', 'eu_recession_lag1', 'ecb_z_lag1',
                            'eu_gdp_z_lag1', 'cd_change']).copy()
print(f"H2 dataset: {len(data_h2)} obs, {data_h2['year'].nunique()} year clusters, "
      f"{data_h2['brand'].nunique()} brands, years "
      f"{data_h2['year'].min()}-{data_h2['year'].max()}")
csz = data_h2.groupby('year').size()
print(f"Cluster sizes: min={csz.min()} median={int(csz.median())} max={csz.max()}")
print()

FORMULA_H2 = ('ARI ~ eu_recession_lag1 + eu_recession_lag1:C(tier) '
              '+ eu_gdp_z_lag1 + ecb_z_lag1 + cd_change + C(brand) + C(season)')
KEYS = ['ecb_z_lag1', 'eu_gdp_z_lag1', 'eu_recession_lag1']

m_clustered = smf.ols(FORMULA_H2, data=data_h2).fit(
    cov_type='cluster', cov_kwds={'groups': data_h2['year']})
m_plain = smf.ols(FORMULA_H2, data=data_h2).fit()  # for the package

print("=== Model 6 — standard year-clustered SEs ===")
for k in KEYS:
    print(f"  {k}: coef={m_clustered.params[k]:+.4f}  p_clustered={m_clustered.pvalues[k]:.4f}")
print()


def pkg_wild(model_results, data, param, cluster_col, B=B_PKG):
    r = wildboottest(model=model_results.model, param=param,
                     cluster=data[cluster_col].values, B=B,
                     weights_type='rademacher', impose_null=True,
                     bootstrap_type='11', seed=RNG_SEED, show=False)
    return float(r.loc[param, 'p-value']), float(r.loc[param, 'statistic'])


def manual_wcr(formula, data, param, cluster_col, B=B_MANUAL, seed=RNG_SEED):
    """Correct WCR-t bootstrap: impose the null in the bootstrap DGP."""
    rng = np.random.default_rng(seed)
    full = smf.ols(formula, data=data).fit(
        cov_type='cluster', cov_kwds={'groups': data[cluster_col]})
    t_obs = full.params[param] / full.bse[param]

    # Restricted model: drop the tested term, impose beta_param = 0.
    terms = [t.strip() for t in formula.split('~', 1)[1].split('+')]
    terms_r = [t for t in terms if t != param]
    formula_r = formula.split('~', 1)[0].strip() + ' ~ ' + ' + '.join(terms_r)
    restr = smf.ols(formula_r, data=data).fit()
    fitted_r = restr.fittedvalues.values
    resid_r = restr.resid.values

    clusters = data[cluster_col].values
    uniq = np.unique(clusters)
    dv = formula.split('~', 1)[0].strip()
    grp = data[cluster_col]

    t_boot = []
    db = data.copy()
    for _ in range(B):
        w = rng.choice([-1.0, 1.0], size=len(uniq))
        wmap = dict(zip(uniq, w))
        ow = np.array([wmap[c] for c in clusters])
        db[dv] = fitted_r + resid_r * ow
        try:
            mb = smf.ols(formula, data=db).fit(
                cov_type='cluster', cov_kwds={'groups': grp})
            t_boot.append(mb.params[param] / mb.bse[param])
        except Exception:
            continue
    t_boot = np.asarray(t_boot)
    p = float(np.mean(np.abs(t_boot) >= np.abs(t_obs)))
    return p, float(t_obs)


# ---------------------------------------------------------------------------
# Wild bootstrap for the three H2 regressors (package).
# ---------------------------------------------------------------------------
results = []
for param in KEYS:
    print(f"wildboottest (WCR, B={B_PKG}) for {param} ...")
    p_wild, stat = pkg_wild(m_clustered, data_h2, param, 'year')
    coef = m_clustered.params[param]
    p_std = m_clustered.pvalues[param]
    verdict = 'SURVIVES@5%' if p_wild < 0.05 else ('MARGINAL@10%' if p_wild < 0.10 else 'FAILS')
    print(f"  coef={coef:+.4f}  p_std={p_std:.4f}  p_wild={p_wild:.4f}  {verdict}")
    results.append({
        'model': 'H2_Model6_PBI', 'parameter': param,
        'coefficient': round(coef, 4),
        'p_standard_clustered': round(p_std, 4),
        'p_wild_bootstrap': round(p_wild, 4),
        'wild_statistic': round(stat, 4),
        'n_clusters': int(data_h2['year'].nunique()),
        'survives_wild_5pct': bool(p_wild < 0.05),
        'survives_wild_10pct': bool(p_wild < 0.10),
        'engine': f'wildboottest WCR(11) rademacher B={B_PKG}',
    })

# Manual WCR cross-check on the headline ECB lag.
print(f"\nManual WCR-t cross-check (B={B_MANUAL}) for ecb_z_lag1 ...")
p_manual, t_obs = manual_wcr(FORMULA_H2, data_h2, 'ecb_z_lag1', 'year')
print(f"  t_obs={t_obs:+.4f}  p_manual_WCR={p_manual:.4f}  "
      f"(package p={results[0]['p_wild_bootstrap']:.4f})")
manual_check = {'param': 'ecb_z_lag1', 't_obs': round(t_obs, 4),
                'p_manual_wcr': round(p_manual, 4), 'B': B_MANUAL}

# ---------------------------------------------------------------------------
# Step 5 — CLIP semantic boldness axis (independent validation).
# ---------------------------------------------------------------------------
clip_results = []
data_clip = pf.dropna(subset=['semantic_boldness', 'ecb_z_lag1',
                              'eu_gdp_z_lag1', 'cd_change']).copy()
if len(data_clip) > 100:
    print(f"\nCLIP semantic axis: {len(data_clip)} obs, "
          f"{data_clip['year'].nunique()} year clusters")
    FORMULA_CLIP = ('semantic_boldness ~ ecb_z_lag1 + eu_gdp_z_lag1 '
                    '+ cd_change + C(brand) + C(season)')
    m_clip = smf.ols(FORMULA_CLIP, data=data_clip).fit(
        cov_type='cluster', cov_kwds={'groups': data_clip['year']})
    for param in ['ecb_z_lag1', 'eu_gdp_z_lag1']:
        p_wild, stat = pkg_wild(m_clip, data_clip, param, 'year')
        coef = m_clip.params[param]
        p_std = m_clip.pvalues[param]
        verdict = 'SURVIVES@5%' if p_wild < 0.05 else ('MARGINAL@10%' if p_wild < 0.10 else 'FAILS')
        print(f"  CLIP {param}: coef={coef:+.4f}  p_std={p_std:.4f}  "
              f"p_wild={p_wild:.4f}  {verdict}")
        clip_results.append({
            'model': 'H2_CLIP_semantic', 'parameter': param,
            'coefficient': round(coef, 4),
            'p_standard_clustered': round(p_std, 4),
            'p_wild_bootstrap': round(p_wild, 4),
            'wild_statistic': round(stat, 4),
            'n_clusters': int(data_clip['year'].nunique()),
            'survives_wild_5pct': bool(p_wild < 0.05),
            'survives_wild_10pct': bool(p_wild < 0.10),
            'engine': f'wildboottest WCR(11) rademacher B={B_PKG}',
        })
else:
    print("semantic_boldness unavailable — skipping CLIP wild bootstrap")

# ---------------------------------------------------------------------------
# Save CSV + JSON for report (W1D will append to the same MD + CSV).
# ---------------------------------------------------------------------------
all_rows = results + clip_results
pd.DataFrame(all_rows).to_csv('wild_bootstrap_results.csv', index=False)
print("\nSaved wild_bootstrap_results.csv")

with open('week12_scripts/_w1c_results.json', 'w') as f:
    json.dump({'h2': results, 'clip': clip_results, 'manual_check': manual_check,
               'n_obs': int(m_clustered.nobs),
               'n_year_clusters': int(data_h2['year'].nunique()),
               'rsquared': round(m_clustered.rsquared, 4)}, f, indent=2)
print("Saved _w1c_results.json")
