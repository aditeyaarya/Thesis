"""Stage W1A — Creative Director change audit and correction.

Rebuilds the cd_change control in panel_full.csv from a corrected, complete
CD_CHANGES dictionary and writes an audit report.

NOTE: panel_full.csv on disk does NOT contain a cd_change column — it is computed
inline in the notebook (cells 53/55/72) from a 10-brand dictionary. We treat that
10-brand dictionary as the CURRENT/OLD state for the audit comparison.
"""
import pandas as pd

PANEL = 'panel_full.csv'
panel_full = pd.read_csv(PANEL)
n_rows_before = len(panel_full)

# ---------------------------------------------------------------------------
# Step 1 — Current (OLD) cd_change coverage.
# The old dictionary is the one hard-coded in the notebook (10 brands).
# ---------------------------------------------------------------------------
CD_CHANGES_OLD = {
    'Balenciaga':        [2012, 2015],
    'Burberry':          [2018, 2022],
    'Chanel':            [2019],
    'Christian Dior':    [2011, 2012, 2016],
    'Givenchy':          [2017, 2020],
    'Gucci':             [2015, 2023],
    'Louis Vuitton':     [2013],
    'Maison Margiela':   [2014],
    'Saint Laurent':     [2012, 2016],
    'Valentino':         [2008, 2016],
}


def build_cd(panel, cd_dict):
    rows = []
    for brand, years in cd_dict.items():
        for yr in years:
            rows.append({'brand': brand, 'year': yr})
            rows.append({'brand': brand, 'year': yr + 1})
    if not rows:
        out = panel.copy()
        out['cd_change'] = 0
        return out['cd_change'].astype(int)
    cd_df = pd.DataFrame(rows).drop_duplicates()
    cd_df['cd_change'] = 1
    merged = panel[['brand', 'year']].merge(cd_df, on=['brand', 'year'], how='left')
    return merged['cd_change'].fillna(0).astype(int)


old_cd = build_cd(panel_full, CD_CHANGES_OLD)
print("Current (OLD) cd_change observations:")
print(f"  Total cells with cd_change=1: {old_cd.sum()}")
print(f"  As % of panel: {old_cd.mean()*100:.1f}%")
print()
_tmp = panel_full[['brand', 'year']].copy(); _tmp['cd_change'] = old_cd.values
print("Brands with cd_change=1 cells (OLD):")
print(_tmp[_tmp['cd_change'] == 1].groupby('brand')['year'].apply(sorted).to_string())
print()

# ---------------------------------------------------------------------------
# Step 2 — Corrected and complete dictionary (CD_CHANGES_FINAL).
# ---------------------------------------------------------------------------
CD_CHANGES_FINAL = {
    'Alexander McQueen': [2010],              # Lee McQueen died Feb 2010; Sarah Burton took over
    'Balenciaga':        [2012, 2015],        # Wang->Demna 2015; Ghesquiere left 2012
    'Burberry':          [2018, 2022],        # Tisci 2018; Daniel Lee 2022
    'Chanel':            [2019],              # Lagerfeld died Feb 2019; Viard took over
    'Christian Dior':    [2011, 2012, 2016],  # Galliano fired 2011; Simons 2012; Chiuri 2016
    'Fendi':             [2020],              # Kim Jones AD womenswear 2020
    'Givenchy':          [2017, 2020],        # Waight Keller 2017; M.Williams 2020
    'Gucci':             [2015, 2023],        # Michele 2015; De Sarno 2023
    'Jean Paul Gaultier': [2020],             # RTW retirement; brand went couture-only
    'Louis Vuitton':     [2013],             # Ghesquiere replaced Marc Jacobs 2013
    'Maison Margiela':   [2014],             # Galliano joined 2014
    'Prada':             [2020],             # Raf Simons co-CD with Miuccia 2020
    'Saint Laurent':     [2012, 2016],        # Slimane 2012; Vaccarello 2016
    'Valentino':         [2008, 2016],        # Chiuri+Piccioli 2008; Piccioli solo 2016
}

# ---------------------------------------------------------------------------
# Step 3 — Rebuild cd_change in panel_full.csv (from scratch).
# ---------------------------------------------------------------------------
panel_full = panel_full.drop(columns=['cd_change'], errors='ignore')

cd_rows = []
for brand, years in CD_CHANGES_FINAL.items():
    for yr in years:
        cd_rows.append({'brand': brand, 'year': yr})
        cd_rows.append({'brand': brand, 'year': yr + 1})
cd_df = pd.DataFrame(cd_rows).drop_duplicates()
cd_df['cd_change'] = 1

panel_full = panel_full.merge(cd_df, on=['brand', 'year'], how='left')
panel_full['cd_change'] = panel_full['cd_change'].fillna(0).astype(int)

assert len(panel_full) == n_rows_before, (
    f"Row count changed: {n_rows_before} -> {len(panel_full)}")

new_count = int(panel_full['cd_change'].sum())
print(f"New cd_change observations: {new_count} "
      f"({panel_full['cd_change'].mean()*100:.1f}% of panel)")
print()
print("Brands with cd_change=1 (NEW version, in-panel cells):")
new_str = panel_full[panel_full['cd_change'] == 1].groupby('brand')['year'].apply(sorted).to_string()
print(new_str)

panel_full.to_csv(PANEL, index=False)
print(f"\nSaved updated {PANEL} with corrected cd_change column "
      f"({len(panel_full)} rows, {panel_full.shape[1]} cols).")

# ---------------------------------------------------------------------------
# Step 4 — Audit report data (per-brand old vs new), written by the report block.
# ---------------------------------------------------------------------------
all_brands = sorted(set(CD_CHANGES_OLD) | set(CD_CHANGES_FINAL))
audit_rows = []
panel_years = panel_full.groupby('brand')['year'].apply(set).to_dict()
for b in all_brands:
    old_years = sorted(set(CD_CHANGES_OLD.get(b, [])))
    new_years = sorted(set(CD_CHANGES_FINAL.get(b, [])))
    status = 'unchanged'
    if b not in CD_CHANGES_OLD and b in CD_CHANGES_FINAL:
        status = 'ADDED (brand)'
    elif old_years != new_years:
        status = 'CHANGED'
    audit_rows.append({
        'brand': b,
        'old_change_years': old_years,
        'new_change_years': new_years,
        'status': status,
        'in_panel': b in panel_years,
    })
audit_df = pd.DataFrame(audit_rows)

# Cells actually flagged in panel, per brand (new)
flagged = (panel_full[panel_full['cd_change'] == 1]
           .groupby('brand')['year'].apply(lambda s: sorted(s.unique())).to_dict())

import json
with open('week12_scripts/_w1a_audit_data.json', 'w') as f:
    json.dump({
        'old_count': int(old_cd.sum()),
        'old_pct': float(old_cd.mean() * 100),
        'new_count': new_count,
        'new_pct': float(panel_full['cd_change'].mean() * 100),
        'audit_rows': audit_df.to_dict(orient='records'),
        'flagged_cells_new': {k: v for k, v in flagged.items()},
        'n_rows': len(panel_full),
        'n_cols': int(panel_full.shape[1]),
    }, f, indent=2, default=str)
print("\nWrote week12_scripts/_w1a_audit_data.json for report generation.")
