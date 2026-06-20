"""Stage W1B — PBI/ARI naming fix.

Replaces user-visible 'ARI' strings (figure titles, axis labels, DV print
statements) with 'PBI (Palette Boldness Index)' wording. The Python variable /
column / dict-key / sheet-name 'ARI' is deliberately retained as a code alias.

Operates on the notebook JSON per source line (guarantees valid JSON output) and
applies replacements in a collision-safe order (specific strings before the
generic substrings they contain).
"""
import json

NB = 'vogue_runway_analysis.ipynb'

# Ordered (specific -> generic) so longer patterns fire before substrings.
REPLACEMENTS = [
    # Event-study suptitle (must precede the generic 'Aesthetic Risk' handling)
    ('DiD Event Study — Macro Shocks & Aesthetic Risk (ARI)',
     'DiD Event Study — Macro Shocks & Palette Boldness Index (PBI)'),
    # Axis label that already carried the (ARI) tag -> clean single label
    ('Aesthetic Risk Index (ARI)', 'Palette Boldness Index (PBI)'),
    # DV print statements
    ('DV = Aesthetic Risk Index', 'DV = Palette Boldness Index (PBI)'),
    ('DV = ARI', 'DV = PBI (Palette Boldness Index)'),
    # Generic full-name (covers any remaining 'Aesthetic Risk Index')
    ('Aesthetic Risk Index', 'Palette Boldness Index (PBI)'),
    # Event-study delta labels
    ('ΔARI', 'ΔPBI'),
    # z-scored axis labels (specific 'Mean ...' before bare)
    ('Mean ARI (z-scored)', 'Mean PBI (z-scored)'),
    ('ARI (z-scored)', 'PBI (z-scored)'),
    # Other figure labels / titles
    ('Within-Brand ARI', 'Within-Brand PBI'),
    ('ARI direction', 'PBI direction'),
    ('ARI vs Aesthetic Quality', 'PBI vs Aesthetic Quality'),
    ('Recession effect on ARI', 'Recession effect on PBI'),
    ('Brand ARI ranking', 'Brand PBI ranking'),
]

with open(NB) as f:
    nb = json.load(f)

# Count occurrences first (over the joined source, for reporting), then apply
# per-line with the same ordered logic.
def count_all(nb, patterns):
    counts = {p: 0 for p, _ in patterns}
    for cell in nb['cells']:
        # work on a mutable copy of joined text using same order to mimic apply
        text = ''.join(cell['source'])
        for old, new in patterns:
            c = text.count(old)
            counts[old] += c
            text = text.replace(old, new)  # so nested substrings counted post-parent
    return counts

counts = count_all(nb, REPLACEMENTS)

# Apply, line by line, same order.
total_applied = {p: 0 for p, _ in REPLACEMENTS}
for cell in nb['cells']:
    new_src = []
    for line in cell['source']:
        for old, new in REPLACEMENTS:
            if old in line:
                total_applied[old] += line.count(old)
                line = line.replace(old, new)
        new_src.append(line)
    cell['source'] = new_src

with open(NB, 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write('\n')

print("Naming fixes applied (count = post-parent-substitution occurrences):")
for old, new in REPLACEMENTS:
    if total_applied[old] > 0:
        print(f"  {total_applied[old]:>2}x  '{old}'  ->  '{new}'")

# Validate JSON / nbformat integrity.
import nbformat
nbformat.read(NB, as_version=4)
print("\nNotebook re-parsed by nbformat — valid.")

# Persist change log for the report.
with open('week12_scripts/_w1b_changes.json', 'w') as f:
    json.dump([{'old': o, 'new': n, 'count': total_applied[o]}
               for o, n in REPLACEMENTS], f, indent=2)
