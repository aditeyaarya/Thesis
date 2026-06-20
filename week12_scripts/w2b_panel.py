"""Stage W2B — Fast-fashion panel construction (identical filtering to luxury)."""
import json
import pandas as pd

sel = json.load(open('week12_scripts/_ff_selection.json'))
FF_BRAND_MAP = {name: [exact] for name, exact in sel['exact_names'].items()}
assert FF_BRAND_MAP, "FF_BRAND_MAP empty — run W2A first."

df = pd.read_parquet('VogueRunway.parquet')
ff_name_to_canon = {raw: canon for canon, raws in FF_BRAND_MAP.items() for raw in raws}

ff = df[df['designer'].isin(ff_name_to_canon)].copy()
ff['brand'] = ff['designer'].map(ff_name_to_canon)
ff['tier'] = 'Fast Fashion'
ff = ff[(ff['section'] == 'Collection') & ff['year'].between(2000, 2024)]

print(f"FF panel before density filter: {len(ff)} images, {ff['brand'].nunique()} brands, "
      f"{int(ff['year'].min())}-{int(ff['year'].max())}")

density = ff.groupby(['brand', 'year', 'season']).size().reset_index(name='n_images')
print("\nDensity per brand:")
print(density.groupby('brand').agg(n_cells=('n_images', 'count'),
                                   min_images=('n_images', 'min'),
                                   median_images=('n_images', 'median')).to_string())

ff = ff.merge(density, on=['brand', 'year', 'season'])
ff = ff[ff['n_images'] >= 15].drop(columns='n_images')
print(f"\nAfter ≥15 filter: {len(ff)} images, "
      f"{ff.groupby(['brand','year','season']).ngroups} cells")

# Stratified ≤30 images/cell — identical to luxury cell 10.
ff_sample = (
    ff.assign(rand=lambda x: x.groupby(['brand', 'tier', 'year', 'season']).cumcount())
    .pipe(lambda x: x[x['rand'] < 30])
    .sample(frac=1, random_state=42)
    .drop(columns='rand')
    .reset_index(drop=True)
)
cols = ['brand', 'tier', 'year', 'season', 'url', 'key']
ff_sample[cols].to_csv('fast_fashion_panel_urls.csv', index=False)
print(f"\nSaved fast_fashion_panel_urls.csv: {len(ff_sample)} images")
print(ff_sample.groupby('brand').size().rename('n_sampled').to_string())
