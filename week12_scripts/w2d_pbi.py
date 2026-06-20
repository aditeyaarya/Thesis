"""Stage W2D — Fast-fashion PBI via the LUXURY PCA basis (no refit)."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

METRICS = ['dispersion_mean', 'lab_entropy_mean', 'mean_L',
           'saturation_mean', 'saturation_std', 'value_mean', 'hue_conc_mean']

# Luxury reference basis — identical to notebook cell 25.
lux = pd.read_csv('cell_metrics.csv')
scaler = StandardScaler()
X_lux = scaler.fit_transform(lux[METRICS].values)
pca = PCA(n_components=7, random_state=42)
pca.fit(X_lux)
print(f"Luxury PC1 explains {pca.explained_variance_ratio_[0]*100:.1f}% of variance")
print("PC1 loadings (after sign flip; +ve = bold):")
print(pd.Series(-pca.components_[0], index=METRICS).round(4).sort_values().to_string())

lux_ari_raw = -pca.transform(X_lux)[:, 0]
ari_mean_lux, ari_std_lux = lux_ari_raw.mean(), lux_ari_raw.std()

# Sanity: reconstructed luxury PBI must match panel_full['ARI'].
pf = pd.read_csv('panel_full.csv')
lux_chk = lux[['brand', 'year', 'season']].copy()
lux_chk['ARI_recon'] = (lux_ari_raw - ari_mean_lux) / ari_std_lux
chk = pf.dropna(subset=['ARI']).merge(lux_chk, on=['brand', 'year', 'season'])
corr = chk['ARI'].corr(chk['ARI_recon'])
print(f"\nSanity: corr(reconstructed luxury PBI, panel_full ARI) = {corr:.4f} "
      f"(should be ~1.000)")

# Aggregate FF image metrics to cells.
ff = pd.read_csv('fast_fashion_color_metrics_raw.csv')
ff_cell = (ff.groupby(['brand', 'tier', 'year', 'season'])
           .agg(dispersion_mean=('dispersion', 'mean'),
                dispersion_std=('dispersion', 'std'),
                lab_entropy_mean=('lab_entropy', 'mean'),
                mean_L=('mean_L', 'mean'),
                saturation_mean=('mean_saturation', 'mean'),
                saturation_std=('std_saturation', 'mean'),
                value_mean=('mean_value', 'mean'),
                hue_conc_mean=('hue_concentration', 'mean'),
                hue_mean=('mean_hue', 'mean'),
                n_images=('key', 'count'))
           .reset_index())
ff_cell = ff_cell[ff_cell['n_images'] >= 15].reset_index(drop=True)
print(f"\nFast-fashion cells (≥15 images): {len(ff_cell)}")

# Project onto luxury basis — DO NOT refit.
X_ff = scaler.transform(ff_cell[METRICS].values)
ff_comp = pca.transform(X_ff)
ff_cell['ARI_raw'] = -ff_comp[:, 0]
ff_cell['ARI'] = (ff_cell['ARI_raw'] - ari_mean_lux) / ari_std_lux  # luxury-scaled

print(f"\nFF PBI (z-scored to luxury distribution): mean={ff_cell['ARI'].mean():.3f} "
      f"std={ff_cell['ARI'].std():.3f} min={ff_cell['ARI'].min():.3f} "
      f"max={ff_cell['ARI'].max():.3f}")
print("\nBrand-level mean PBI (fast-fashion):")
print(ff_cell.groupby('brand')['ARI'].mean().sort_values().round(3).to_string())
print(f"\nFor reference, luxury panel mean PBI = {pf['ARI'].mean():.3f}")

ff_cell.to_csv('fast_fashion_cell_metrics.csv', index=False)
print("\nSaved fast_fashion_cell_metrics.csv")
