"""Stage W2A — Fast-fashion / mid-market brand availability check."""
import json
import pandas as pd

df = pd.read_parquet('VogueRunway.parquet')

FAST_FASHION_CANDIDATES = [
    'Zara', 'H&M', 'COS', 'Cos', 'Sandro', 'Maje', 'Iro', 'Ba&sh',
    'Isabel Marant', 'A.P.C.', 'Carven', 'Claudie Pierlot', 'The Kooples',
    'Zadig & Voltaire', 'Vanessa Bruno', 'Paul & Joe', 'Comptoir des Cotonniers',
    'Rouje', 'Rouje Paris', 'See by Chloé', 'See By Chloe', 'DKNY',
    'Calvin Klein', 'Tommy Hilfiger', 'Lacoste', 'Pinko', 'Liu Jo',
    'Tory Burch', 'Kate Spade', 'Kate Spade New York', 'Coach',
    'Michael Kors', 'Michael Michael Kors',
]

print(f"Total designers in dataset: {df['designer'].nunique()}")
print(f"Sections present: {sorted(df['section'].dropna().unique())[:15]}")
print()

available = []
for cand in FAST_FASHION_CANDIDATES:
    matches = df[df['designer'].str.lower() == cand.lower()]
    if len(matches) == 0:
        continue
    cm = matches[(matches['section'] == 'Collection') & (matches['year'].between(2000, 2024))]
    if len(cm) == 0:
        continue
    cell_count = cm.groupby(['year', 'season']).size()
    available.append({
        'candidate': cand,
        'exact_name': matches['designer'].iloc[0],
        'total_images': int(len(cm)),
        'cells_min15': int((cell_count >= 15).sum()),
        'n_cells': int(len(cell_count)),
        'year_range': f"{int(cm['year'].min())}-{int(cm['year'].max())}",
        'has_gfc_coverage': bool(cm['year'].between(2005, 2011).any()),
        'has_covid_coverage': bool(cm['year'].between(2017, 2023).any()),
    })

avail_df = pd.DataFrame(available).sort_values('cells_min15', ascending=False)
print("Available candidates:")
print(avail_df.to_string(index=False) if len(avail_df) else "  (none matched exact names)")
print()

found_names = {a['candidate'].lower() for a in available}
not_found = [c for c in FAST_FASHION_CANDIDATES if c.lower() not in found_names]

qualified = avail_df[(avail_df['cells_min15'] >= 10) &
                     (avail_df['has_gfc_coverage']) &
                     (avail_df['has_covid_coverage'])] if len(avail_df) else avail_df
print(f"Qualified (>=10 cells min15, both shock windows): {len(qualified)}")
if len(qualified):
    print(qualified[['exact_name', 'total_images', 'cells_min15', 'year_range']].to_string(index=False))

# Broader fallback search (always run for the report; informs selection if <3 qualify).
luxury_brands = ['Prada', 'Chanel', 'Christian Dior', 'Louis Vuitton', 'Gucci', 'Fendi',
                 'Versace', 'Valentino', 'Saint Laurent', 'Giorgio Armani', 'Dolce & Gabbana',
                 'Givenchy', 'Burberry', 'Stella McCartney', 'Max Mara', 'Missoni',
                 'Ralph Lauren', 'Miu Miu', 'Marni', 'Maison Margiela', 'Alexander McQueen',
                 'Balenciaga', 'Rick Owens', 'Dries Van Noten', 'Jean Paul Gaultier']
non_lux = df[~df['designer'].isin(luxury_brands) & (df['section'] == 'Collection')]
broad = (non_lux.groupby('designer')
         .agg(total_images=('key', 'count'), year_min=('year', 'min'), year_max=('year', 'max'))
         .query('total_images >= 300 and year_min <= 2008 and year_max >= 2020')
         .sort_values('total_images', ascending=False).head(40))
# add cells_min15 for the broad set
broad_cells = {}
for name in broad.index:
    sub = df[(df['designer'] == name) & (df['section'] == 'Collection') & df['year'].between(2000, 2024)]
    cc = sub.groupby(['year', 'season']).size()
    broad_cells[name] = int((cc >= 15).sum())
broad['cells_min15'] = pd.Series(broad_cells)
print("\nBroader non-luxury candidates (>=300 imgs, span 2008-2020):")
print(broad.to_string())

out = {
    'available': available,
    'not_found': not_found,
    'qualified': qualified.to_dict(orient='records') if len(qualified) else [],
    'broad': broad.reset_index().rename(columns={'index': 'designer'}).to_dict(orient='records'),
    'n_designers': int(df['designer'].nunique()),
}
with open('week12_scripts/_w2a.json', 'w') as f:
    json.dump(out, f, indent=2, default=str)
print("\nSaved _w2a.json")
