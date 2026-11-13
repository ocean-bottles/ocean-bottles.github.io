"""Combine the int8 HYCOM exports (codes of 0.015 m/s, land -128, last band water) into cur_MM.png."""
import sys, glob, json, base64, numpy as np, rasterio
from PIL import Image
months = {}
water = None
for f in sorted(glob.glob('raw/hycom_i8_m*.tif')):
    r = rasterio.open(f); a = r.read().astype(np.int16); m0 = int(f.split('_m')[-1].split('.')[0])
    top = r.transform.f; r0 = int(round((90 - top) / 0.25))
    full = np.full((a.shape[0], 720, 1440), -128, np.int16); full[-1] = 0
    full[:, r0:r0 + a.shape[1]] = a
    for k in range(4): months[m0 + k] = (full[2 * k], full[2 * k + 1])
    water = full[-1] > 0 if water is None else water
print('have months', sorted(months))
for m in range(1, 13):
    src = m if m in months else min(months, key=lambda k: min(abs(k - m), 12 - abs(k - m)))
    u, v = months[src]
    land = (u == -128) | (v == -128) | ~water
    cu = np.where(land, 0, u) + 128; cv = np.where(land, 0, v) + 128
    rgba = np.dstack([cu, cv, np.where(land, 0, 255), np.full_like(cu, 255)]).astype(np.uint8)
    Image.fromarray(rgba, 'RGBA').save(f'web/data/cur_{m:02d}.png', optimize=True)
    sp = np.hypot(u[~land], v[~land]) * 0.015
    print(m, 'from', src, 'max', sp.max().round(2), 'p99', np.percentile(sp, 99).round(2))
