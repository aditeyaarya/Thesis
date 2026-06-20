"""Stage W2C — Fast-fashion colour extraction (RESUMABLE + checkpointed).

Identical extraction method to the luxury pipeline (cell 12): U2Net background
removal (rembg, single shared session) + HSV skin exclusion, 500 garment
pixels/image, LAB dispersion/entropy + HSV saturation/value/hue.

Robustness changes vs the first attempt (which was killed at 46% losing all
results because it only saved at the end):
  * one shared rembg session (no 60-thread model-download race);
  * MODERATE worker count (avoids the memory/thread thrash that stalled & killed
    the 60-worker run);
  * a PARTIAL checkpoint file written every CHECKPOINT images, and resume-on-
    restart by skipping keys already done. A kill now costs <CHECKPOINT images.
"""
import os
import colorsys
from io import BytesIO

import numpy as np
import pandas as pd
import requests
from PIL import Image
from skimage.color import rgb2lab
from scipy.stats import entropy as scipy_entropy
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

FF_CACHE = 'fast_fashion_color_metrics_raw.csv'
PARTIAL = 'week12_scripts/_w2c_partial.csv'
N_WORKERS = 16
CHECKPOINT = 250

if os.path.exists(FF_CACHE):
    print(f"{FF_CACHE} found — loading from cache.")
    print(pd.read_csv(FF_CACHE).describe().round(3))
    raise SystemExit(0)

from rembg import remove as rembg_remove
from rembg import new_session
print("rembg loaded. Preparing shared U2Net session (model already cached)...")
SESSION = new_session('u2net')
print("U2Net session ready.")


def extract_garment_pixels(content, n=500):
    img_rgba = Image.open(BytesIO(content)).convert('RGBA')
    img_no_bg = rembg_remove(img_rgba, session=SESSION)
    arr = np.array(img_no_bg)
    alpha_mask = arr[:, :, 3] > 128
    fg_rgb = arr[:, :, :3][alpha_mask]
    hsv_fg = np.array([colorsys.rgb_to_hsv(p[0] / 255, p[1] / 255, p[2] / 255)
                       for p in fg_rgb])
    h, s, v = hsv_fg[:, 0], hsv_fg[:, 1], hsv_fg[:, 2]
    skin = (h <= 0.07) & (s >= 0.08) & (s <= 0.70) & (v >= 0.30)
    garment_rgb = fg_rgb[~skin]
    if len(garment_rgb) < 50:
        garment_rgb = fg_rgb
    idx = np.random.choice(len(garment_rgb), min(n, len(garment_rgb)), replace=False)
    return garment_rgb[idx].astype(np.float32) / 255.0


def extract_color_features(row):
    try:
        r = requests.get(row['url'], timeout=10)
        if r.status_code != 200:
            return None
        pixels = extract_garment_pixels(r.content)
        if len(pixels) < 30:
            return None
        lab = rgb2lab(pixels.reshape(-1, 1, 3)).reshape(-1, 3)
        L, a, b_ch = lab[:, 0], lab[:, 1], lab[:, 2]
        dispersion = float(np.sqrt(np.var(L) + np.var(a) + np.var(b_ch)))
        hue_angle = np.arctan2(b_ch, a)
        bins = np.histogram(hue_angle, bins=36, range=(-np.pi, np.pi))[0].astype(float) + 1e-9
        lab_entropy = float(scipy_entropy(bins))
        hsv = np.array([colorsys.rgb_to_hsv(p[0], p[1], p[2]) for p in pixels])
        H, S, V = hsv[:, 0], hsv[:, 1], hsv[:, 2]
        hue_rad = H * 2 * np.pi
        hue_concentration = float(
            np.sqrt(np.mean(np.cos(hue_rad)) ** 2 + np.mean(np.sin(hue_rad)) ** 2))
        return {
            'key': row['key'], 'brand': row['brand'], 'tier': row['tier'],
            'year': row['year'], 'season': row['season'], 'segmented': True,
            'dispersion': dispersion, 'lab_entropy': lab_entropy,
            'mean_L': float(np.mean(L)),
            'mean_saturation': float(np.mean(S)), 'std_saturation': float(np.std(S)),
            'mean_value': float(np.mean(V)),
            'hue_concentration': hue_concentration, 'mean_hue': float(np.mean(H)),
        }
    except Exception:
        return None


ff_urls = pd.read_csv('fast_fashion_panel_urls.csv')

# Resume: load any partial results, skip their keys.
done_keys = set()
results = []
if os.path.exists(PARTIAL):
    prev = pd.read_csv(PARTIAL)
    results = prev.to_dict('records')
    done_keys = set(prev['key'])
    print(f"Resuming: {len(done_keys)} images already done; skipping them.")

todo = ff_urls[~ff_urls['key'].isin(done_keys)]
print(f"Extracting {len(todo)} of {len(ff_urls)} images ({N_WORKERS} workers, "
      f"checkpoint every {CHECKPOINT})...")

failed = []
since_ckpt = 0
with ThreadPoolExecutor(max_workers=N_WORKERS) as ex:
    futures = {ex.submit(extract_color_features, row): row for _, row in todo.iterrows()}
    for fut in tqdm(as_completed(futures), total=len(futures)):
        res = fut.result()
        if res:
            results.append(res)
        else:
            failed.append(futures[fut]['key'])
        since_ckpt += 1
        if since_ckpt >= CHECKPOINT:
            pd.DataFrame(results).to_csv(PARTIAL, index=False)
            since_ckpt = 0

ff_results_df = pd.DataFrame(results)
ff_results_df.to_csv(FF_CACHE, index=False)
if os.path.exists(PARTIAL):
    os.remove(PARTIAL)
print(f"\nSuccessful: {len(results)}  Failed this run: {len(failed)} "
      f"({len(failed)/max(len(todo),1)*100:.1f}% of attempted)")
print(ff_results_df.describe().round(3))
