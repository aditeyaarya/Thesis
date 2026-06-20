"""Stage W1D — Wild cluster bootstrap for H1 (stacked DiD event study).

Stacked GFC(2008)+COVID(2020) DiD on the Palette Boldness Index, brand*cohort
(be) FE + season FE, clustered on brand (25 clusters). Headline event-time
coefficients: pooled post-shock dip at t+1 and t+2.

TWO METHODOLOGICAL FIXES vs the brief's reconstruction:

1. Reference period. The brief (and the notebook's event-study cell) DROP the
   t=-1 rows from the window. With no in-sample reference, the six event dummies
   sum to 1 and are collinear with the constant, so the model is only identified
   up to a min-norm (pinv) normalisation and cluster/bootstrap inference on the
   individual coefficients is ill-posed. We KEEP t=-1 as the reference (its
   dummies are all zero), which is the standard event-study setup and yields a
   well-conditioned design (residualised-dummy Gram condition number ~8).

2. Nested FE + few clusters. The 50 brand*cohort FE are nested within the 25
   brand clusters and there are 59 parameters, so the cluster-robust variance on
   the full design is rank-deficient and a naive wild bootstrap is unstable. We
   use Frisch-Waugh-Lovell: partial the FE out of the outcome and the event
   dummies, then wild-bootstrap the low-dimensional residualised regression
   (6 params << 25 clusters), clustered on brand.

Consequence: coefficients are measured against t=-1 and are therefore larger in
magnitude than the headline min-norm numbers (t+1 -0.27 / t+2 -0.16); the
qualitative story (significant post-shock dip, flat pre-trend) is unchanged and
in fact cleaner.
"""
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from patsy import dmatrix
from wildboottest.wildboottest import wildboottest

warnings.filterwarnings('ignore')
B_PKG = 9999
B_MANUAL = 4999

pf = pd.read_csv('panel_full.csv')

_ET = {-3: 'etm3', -2: 'etm2', 0: 'etp0', 1: 'etp1', 2: 'etp2', 3: 'etp3'}  # t=-1 = reference
EVENT = list(_ET.values())
stk = []
for sh, yr in [('GFC', 2008), ('COVID', 2020)]:
    w = pf[pf['year'].between(yr - 3, yr + 3)].dropna(subset=['ARI']).copy()
    w['et'] = w['year'] - yr
    w['be'] = w['brand'] + '_' + sh
    stk.append(w)                       # keep t=-1 rows as the reference
S = pd.concat(stk).reset_index(drop=True)
for t, n in _ET.items():
    S[n] = (S['et'] == t).astype(int)   # t=-1 -> all event dummies = 0

ET_FORMULA = 'ARI ~ ' + ' + '.join(EVENT) + ' + C(season) + C(be)'
m_full = smf.ols(ET_FORMULA, data=S).fit(
    cov_type='cluster', cov_kwds={'groups': S['brand']})
n_brand_clusters = S['brand'].nunique()
print(f"Stacked DiD: {int(m_full.nobs)} obs (incl t=-1 ref), {n_brand_clusters} brand "
      f"clusters, {S['be'].nunique()} brand×cohort units, {len(m_full.params)} full params")
print("=== Full model — brand-clustered SEs (reference t=-1) ===")
for t, n in _ET.items():
    print(f"  t={t:+d} ({n}): coef={m_full.params[n]:+.4f}  p={m_full.pvalues[n]:.4f}")
print()

# ---- FWL: partial out nested FE (C(be)+C(season)) ----------------------------
FE = np.asarray(dmatrix('C(be) + C(season)', data=S, return_type='dataframe'))
P = np.eye(len(S)) - FE @ np.linalg.pinv(FE)
X_df = pd.DataFrame({n: P @ S[n].values.astype(float) for n in EVENT})
X_df['__y__'] = P @ S['ARI'].values.astype(float)
print("Residualised-dummy Gram condition number:",
      round(np.linalg.cond(X_df[EVENT].T @ X_df[EVENT]), 2))

m_fwl = smf.ols('__y__ ~ ' + ' + '.join(EVENT) + ' - 1', data=X_df).fit(
    cov_type='cluster', cov_kwds={'groups': S['brand'].values})
print("=== FWL residualised model (coefs identical to full) — brand-clustered ===")
for n in EVENT:
    print(f"  {n}: coef={m_fwl.params[n]:+.4f}  p={m_fwl.pvalues[n]:.4f}")
print()


def pkg_wild(model_results, brand, param, B=B_PKG):
    cl = pd.factorize(brand)[0].astype(np.int64)
    r = wildboottest(model=model_results.model, param=param, cluster=cl, B=B,
                     weights_type='rademacher', impose_null=True,
                     bootstrap_type='11', seed=42, show=False)
    return float(r.loc[param, 'p-value']), float(r.loc[param, 'statistic'])


def manual_wcr(Xdf, event, param, brand, B=B_MANUAL, seed=42):
    rng = np.random.default_rng(seed)
    full = smf.ols('__y__ ~ ' + ' + '.join(event) + ' - 1', data=Xdf).fit(
        cov_type='cluster', cov_kwds={'groups': brand})
    t_obs = full.params[param] / full.bse[param]
    others = [e for e in event if e != param]
    restr = smf.ols('__y__ ~ ' + ' + '.join(others) + ' - 1', data=Xdf).fit()
    fit_r, res_r = restr.fittedvalues.values, restr.resid.values
    clusters = np.asarray(brand)
    uniq = np.unique(clusters)
    db = Xdf.copy()
    tb = []
    for _ in range(B):
        wts = rng.choice([-1.0, 1.0], size=len(uniq))
        wmap = dict(zip(uniq, wts))
        ow = np.array([wmap[c] for c in clusters])
        db['__y__'] = fit_r + res_r * ow
        try:
            mb = smf.ols('__y__ ~ ' + ' + '.join(event) + ' - 1', data=db).fit(
                cov_type='cluster', cov_kwds={'groups': brand})
            tb.append(mb.params[param] / mb.bse[param])
        except Exception:
            continue
    tb = np.asarray(tb)
    return float(np.mean(np.abs(tb) >= np.abs(t_obs))), float(t_obs)


brand_arr = S['brand'].values
rows = []
for label, param in [('COVID/GFC pooled t+1', 'etp1'),
                     ('COVID/GFC pooled t+2', 'etp2')]:
    p_pkg, _ = pkg_wild(m_fwl, brand_arr, param)
    p_man, t_obs = manual_wcr(X_df, EVENT, param, brand_arr)
    coef = m_fwl.params[param]
    p_std = m_fwl.pvalues[param]
    verdict = 'SURVIVES@5%' if p_man < 0.05 else ('MARGINAL@10%' if p_man < 0.10 else 'FAILS')
    print(f"  {label} ({param}): coef={coef:+.4f}  p_std={p_std:.4f}  "
          f"p_wild(WCR-t)={p_man:.4f}  p_wild(pkg)={p_pkg:.4f}  {verdict}")
    rows.append({
        'model': 'H1_stackedDiD_PBI', 'parameter': param,
        'coefficient': round(coef, 4),
        'p_standard_clustered': round(p_std, 4),
        'p_wild_bootstrap': round(p_man, 4),
        'wild_statistic': round(t_obs, 4),
        'n_clusters': int(n_brand_clusters),
        'survives_wild_5pct': bool(p_man < 0.05),
        'survives_wild_10pct': bool(p_man < 0.10),
        'engine': f'FWL+WCR-t rademacher B={B_MANUAL} (pkg ref={round(p_pkg,4)})',
    })

pretrend = []
for param in ['etm3', 'etm2']:
    p_man, t_obs = manual_wcr(X_df, EVENT, param, brand_arr)
    pretrend.append({'parameter': param, 'coefficient': round(m_fwl.params[param], 4),
                     'p_standard_clustered': round(m_fwl.pvalues[param], 4),
                     'p_wild_bootstrap': round(p_man, 4)})
    print(f"  pre-trend {param}: coef={m_fwl.params[param]:+.4f}  p_wild={p_man:.4f}")

# ---- Rebuild the full CSV cleanly from W1C json + these H1 rows --------------
w1c = json.load(open('week12_scripts/_w1c_results.json'))
all_rows = w1c['h2'] + w1c['clip'] + rows
cols = ['model', 'parameter', 'coefficient', 'p_standard_clustered', 'p_wild_bootstrap',
        'wild_statistic', 'n_clusters', 'survives_wild_5pct', 'survives_wild_10pct', 'engine']
pd.DataFrame(all_rows)[cols].to_csv('wild_bootstrap_results.csv', index=False)
print("\nRewrote wild_bootstrap_results.csv (W1C + W1D, clean).")

with open('week12_scripts/_w1d_results.json', 'w') as f:
    json.dump({'h1': rows, 'pretrend': pretrend,
               'n_obs': int(m_full.nobs), 'n_brand_clusters': int(n_brand_clusters),
               'n_full_params': int(len(m_full.params)),
               'headline_minnorm_note': 't+1 -0.27 / t+2 -0.16 are the min-norm (drop-t=-1) numbers',
               'all_event_coefs': {n: [round(m_full.params[n], 4),
                                       round(m_full.pvalues[n], 4)] for n in EVENT}}, f, indent=2)
print("Saved _w1d_results.json")
