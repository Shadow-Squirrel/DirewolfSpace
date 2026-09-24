#!/usr/bin/env python3
"""Procedurally render the hero background: Earth's night-side limb seen from orbit,
with city lights, an atmospheric rim, a star field, a faint nebula and sun glare.

Requires: pip install numpy pillow
Usage:    python3 tools/render_hero_background.py
Outputs:  assets/img/hero-space.webp (landscape) and assets/img/hero-space-portrait.webp
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img')


def value_noise(shape, scale, rng):
    h, w = shape
    small = rng.random((h // scale + 2, w // scale + 2)).astype(np.float32)
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(im).astype(np.float32) / 255.0


def fbm(shape, rng, scales=(420, 210, 105, 52, 26), weights=(1, .55, .3, .16, .08)):
    acc = np.zeros(shape, np.float32)
    for s, wgt in zip(scales, weights):
        acc += wgt * value_noise(shape, s, rng)
    return acc / sum(weights)


def blur(arr, radius):
    if radius <= 0:
        return arr
    im = Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(radius))).astype(np.float32) / 255.0


def render(W, H, seed, sun_x_frac, limb_apex_frac, nebula_center, out_name, quality=82):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    img = np.zeros((H, W, 3), np.float32)

    # ---- deep-space base gradient
    t = (yy / H)[..., None]
    img += (np.array([3, 5, 10], np.float32) / 255) * (1 - t) + (np.array([6, 9, 17], np.float32) / 255) * t

    # ---- nebula / galactic haze (top-right by default)
    neb = fbm((H, W), rng)
    neb = np.clip((neb - 0.47) * 3.2, 0, 1) ** 1.7
    ncx, ncy = nebula_center[0] * W, nebula_center[1] * H
    nmask = np.exp(-(((xx - ncx) / (0.33 * W)) ** 2 + ((yy - ncy) / (0.30 * H)) ** 2))
    img += (neb * nmask * 0.62)[..., None] * (np.array([95, 140, 215], np.float32) / 255)
    haze = fbm((H, W), rng, scales=(700, 350, 175), weights=(1, .5, .25))
    img += (haze * nmask * 0.11)[..., None] * (np.array([130, 160, 210], np.float32) / 255)
    # a denser bright core of the nebula
    core = np.exp(-(((xx - ncx) / (0.09 * W)) ** 2 + ((yy - ncy) / (0.08 * H)) ** 2))
    img += (core * neb * 0.9)[..., None] * (np.array([200, 215, 240], np.float32) / 255)

    # ---- stars
    n = int(W * H / 260)
    sx = rng.integers(0, W, n)
    sy = rng.integers(0, H, n)
    bright = rng.random(n) ** 3.4
    cool = np.zeros((H, W), np.float32)
    warm = np.zeros((H, W), np.float32)
    tint = rng.random(n)
    np.maximum.at(cool, (sy, sx), bright * (tint > 0.25))
    np.maximum.at(warm, (sy, sx), bright * (tint <= 0.25))
    cool = blur(cool, 0.55)
    warm = blur(warm, 0.55)
    # dense faint dust of stars inside the nebula region
    n2 = int(W * H / 60)
    sx2 = rng.integers(0, W, n2)
    sy2 = rng.integers(0, H, n2)
    dust = np.zeros((H, W), np.float32)
    np.maximum.at(dust, (sy2, sx2), rng.random(n2) ** 2 * 0.45)
    dust = blur(dust, 0.4) * nmask
    img += (cool + dust)[..., None] * (np.array([225, 235, 255], np.float32) / 255)
    img += warm[..., None] * (np.array([255, 235, 205], np.float32) / 255)
    # bright stars with soft halo and 4-point glint
    # medium stars: soft 1-2px blobs, no rays
    nm = int(W * H / 9000)
    mx = rng.integers(0, W, nm)
    my = rng.integers(0, int(H * 0.75), nm)
    mb = 0.25 + rng.random(nm) ** 2 * 0.5
    med = np.zeros((H, W), np.float32)
    np.maximum.at(med, (my, mx), mb)
    img += (blur(med, 1.0) * 1.6)[..., None] * (np.array([230, 238, 255], np.float32) / 255)
    # a handful of bright stars with a small halo and short 4-point glint
    nb = 22
    bx = rng.integers(0, W, nb)
    by = rng.integers(0, int(H * 0.7), nb)
    bb = 0.45 + rng.random(nb) * 0.55
    glint = np.zeros((H, W), np.float32)
    for x, y, b in zip(bx, by, bb):
        r = 1.1 + b * 1.3
        x0, x1 = max(0, int(x - 30)), min(W, int(x + 31))
        y0, y1 = max(0, int(y - 30)), min(H, int(y + 31))
        gx, gy = xx[y0:y1, x0:x1] - x, yy[y0:y1, x0:x1] - y
        dd2 = gx * gx + gy * gy
        blob = np.exp(-dd2 / (2 * r * r)) * b + np.exp(-dd2 / (2 * (r * 4) ** 2)) * b * 0.12
        rays = (np.exp(-np.abs(gy) * 1.8) * np.exp(-np.abs(gx) / (3 + 7 * b)) + np.exp(-np.abs(gx) * 1.8) * np.exp(-np.abs(gy) / (3 + 7 * b))) * b * 0.3
        glint[y0:y1, x0:x1] = np.maximum(glint[y0:y1, x0:x1], blob + rays)
    img += glint[..., None] * (np.array([235, 242, 255], np.float32) / 255)

    # ---- planet limb
    R = 2.7 * W
    pcx = 0.44 * W
    pcy = limb_apex_frac * H + R
    d = np.sqrt((xx - pcx) ** 2 + (yy - pcy) ** 2) - R  # >0 space, <0 planet
    inside = np.clip(-d, 0, 1)[..., None]
    planet_base = np.array([5, 9, 18], np.float32) / 255
    terrain = fbm((H, W), rng, scales=(300, 150, 75, 38), weights=(1, .5, .3, .2))
    depth = np.clip(-d / (0.3 * H), 0, 1)
    planet = planet_base[None, None, :] * (0.55 + 0.95 * terrain[..., None]) * (1 - 0.3 * depth[..., None])
    img = img * (1 - inside) + planet * inside

    # ---- city lights: clusters near the limb, foreshortened
    lights = np.zeros((H, W), np.float32)
    net = Image.new('L', (W, H), 0)
    draw = ImageDraw.Draw(net)
    K = int(46 * W / 2400)
    centers = []
    for _ in range(K):
        cx = rng.uniform(0.02 * W, 0.98 * W)
        limb_y = pcy - np.sqrt(max(R * R - (cx - pcx) ** 2, 1))
        dep = rng.uniform(6, 0.24 * H) ** 1.0
        cy = limb_y + dep
        if cy >= H - 2:
            continue
        persp = 0.25 + 0.75 * (dep / (0.24 * H))
        sig = rng.uniform(10, 46) * persp
        npts = int(rng.integers(60, 420) * persp + 30)
        px = rng.normal(cx, sig, npts)
        py = rng.normal(cy, sig * 0.32, npts)
        pb = rng.random(npts) ** 1.8 * (0.5 + 0.5 * persp)
        ok = (px >= 0) & (px < W) & (py >= 0) & (py < H)
        pxi, pyi = px[ok].astype(int), py[ok].astype(int)
        np.maximum.at(lights, (pyi, pxi), pb[ok])
        centers.append((cx, cy, persp))
    # network lines between nearby clusters
    for i, (x1, y1, p1) in enumerate(centers):
        dists = sorted(((x2 - x1) ** 2 + (y2 - y1) ** 2, j) for j, (x2, y2, _) in enumerate(centers) if j != i)
        for _, j in dists[:2]:
            x2, y2, _ = centers[j]
            if abs(x2 - x1) < 0.28 * W:
                mx_, my_ = (x1 + x2) / 2, (y1 + y2) / 2 - abs(x2 - x1) * 0.06
                pts = [((1 - u) ** 2 * x1 + 2 * (1 - u) * u * mx_ + u * u * x2, (1 - u) ** 2 * y1 + 2 * (1 - u) * u * my_ + u * u * y2) for u in np.linspace(0, 1, 24)]
                draw.line(pts, fill=int(60 + 50 * p1), width=1)
    netl = np.asarray(net.filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255.0 * 0.16
    lights_glow = blur(lights, 7) * 0.9 + blur(lights, 22) * 0.5
    lmask = (d < -2).astype(np.float32)
    lights_all = (blur(lights, 0.6) * 1.0 + lights_glow + netl) * lmask
    img += lights_all[..., None] * (np.array([255, 196, 120], np.float32) / 255)
    img += (blur(lights, 1.2) * lmask * 0.7)[..., None] * (np.array([255, 240, 215], np.float32) / 255)

    # ---- atmosphere rim + glow, brighter toward the sun
    sun_side = 0.55 + 0.45 * np.clip((xx - 0.15 * W) / (0.8 * W), 0, 1) if sun_x_frac > 0.5 else 0.55 + 0.45 * np.clip((0.85 * W - xx) / (0.8 * W), 0, 1)
    rim = np.exp(-(d / 2.6) ** 2)
    outer = np.where(d > 0, np.exp(-d / (0.045 * H)), 0)
    outer2 = np.where(d > 0, np.exp(-d / (0.16 * H)), 0)
    inner = np.where(d < 0, np.exp(d / (0.03 * H)), 0)
    atm = np.array([110, 175, 255], np.float32) / 255
    rimc = np.array([215, 232, 255], np.float32) / 255
    img += (rim * sun_side * 1.15)[..., None] * rimc
    img += ((outer * 0.62 + outer2 * 0.22) * sun_side)[..., None] * atm
    img += (inner * sun_side * 0.55)[..., None] * (np.array([120, 170, 240], np.float32) / 255)

    # ---- sun glare at the limb
    sxp = sun_x_frac * W
    syp = pcy - np.sqrt(max(R * R - (sxp - pcx) ** 2, 1)) + 0.006 * H
    dd = np.sqrt(((xx - sxp) / 1.7) ** 2 + (yy - syp) ** 2)
    corex = np.exp(-(dd / (0.014 * H)) ** 2)
    halo = np.exp(-dd / (0.09 * H)) * 0.5
    wide = np.exp(-dd / (0.34 * H)) * 0.16
    streak = np.exp(-((yy - syp) / (0.004 * H)) ** 2) * np.exp(-np.abs(xx - sxp) / (0.2 * W)) * 0.4
    img += corex[..., None] * (np.array([255, 250, 240], np.float32) / 255)
    img += halo[..., None] * (np.array([255, 226, 180], np.float32) / 255)
    img += wide[..., None] * (np.array([255, 215, 160], np.float32) / 255)
    img += streak[..., None] * (np.array([255, 225, 185], np.float32) / 255)
    # warm the atmosphere near the sun
    warmatm = (rim * 0.8 + outer * 0.5) * np.exp(-np.abs(xx - sxp) / (0.18 * W))
    img += warmatm[..., None] * (np.array([255, 205, 150], np.float32) / 255)

    # ---- vignette and tone
    vx = (xx / W - 0.5) * 2
    vy = (yy / H - 0.5) * 2
    vig = 1 - 0.28 * np.clip(vx * vx * 0.9 + vy * vy * 0.5, 0, 1)
    img *= vig[..., None]
    img = np.clip(img, 0, 1) ** 0.96

    out = Image.fromarray((img * 255).astype(np.uint8), 'RGB')
    path = os.path.join(OUT, out_name)
    out.save(path, 'WEBP', quality=quality, method=6)
    print(out_name, out.size, os.path.getsize(path) // 1024, 'KB')


if __name__ == '__main__':
    render(2400, 1350, seed=11, sun_x_frac=0.9, limb_apex_frac=0.78, nebula_center=(0.76, 0.2), out_name='hero-space.webp')
    render(1080, 1620, seed=23, sun_x_frac=0.86, limb_apex_frac=0.84, nebula_center=(0.62, 0.22), out_name='hero-space-portrait.webp', quality=80)
