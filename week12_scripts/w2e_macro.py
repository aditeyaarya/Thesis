"""Stage W2E — Fast-fashion macro merge (same macro_indicators + 1-year lags)."""
import pandas as pd

ff_cell = pd.read_csv('fast_fashion_cell_metrics.csv')
macro = pd.read_csv('macro_indicators.csv')

ff = ff_cell.merge(macro, on='year', how='left')

# Contemporaneous z-scores from the FF panel's own distribution.
for col, z in [('vix_annual_mean', 'vix_z'), ('gdp_growth_world', 'gdp_z'),
               ('ecb_rate', 'ecb_z'), ('eu_gdp_growth', 'eu_gdp_z')]:
    if col in ff.columns:
        ff[z] = (ff[col] - ff[col].mean()) / ff[col].std()

ff = ff.sort_values(['brand', 'year']).reset_index(drop=True)

# 1-year lags via a year-indexed macro table merged on year+1 (same as luxury fix).
year_macro = (ff[['year', 'vix_z', 'gdp_z', 'recession', 'ecb_z', 'eu_gdp_z',
                  'eu_recession']]
              .drop_duplicates('year').sort_values('year').reset_index(drop=True))
lag_map = {'vix_z': 'vix_z_lag1', 'gdp_z': 'gdp_z_lag1', 'recession': 'recession_lag1',
           'ecb_z': 'ecb_z_lag1', 'eu_gdp_z': 'eu_gdp_z_lag1',
           'eu_recession': 'eu_recession_lag1'}
year_lag = year_macro.rename(columns=lag_map)
year_lag['year'] = year_lag['year'] + 1
ff = ff.merge(year_lag[['year', *lag_map.values()]], on='year', how='left')

ff['cd_change'] = 0  # not applicable to fast-fashion brands

ff.to_csv('fast_fashion_panel_full.csv', index=False)
print(f"Saved fast_fashion_panel_full.csv: {len(ff)} cells, "
      f"years {int(ff['year'].min())}-{int(ff['year'].max())}, "
      f"{ff['brand'].nunique()} brands")
print(f"NaN in ecb_z_lag1: {ff['ecb_z_lag1'].isna().sum()} "
      f"(expected: first-year cells with no prior year)")
print(f"Usable for H2 (non-NaN ARI & ecb_z_lag1): "
      f"{ff.dropna(subset=['ARI','ecb_z_lag1']).shape[0]} cells, "
      f"{ff.dropna(subset=['ARI','ecb_z_lag1'])['year'].nunique()} year clusters")
