#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-23.

Theme of the day: small departures. Things that began, or left, on 23 October.
  1. Nightfall, 4004 BC — Ussher's beginning of time, drawn as a halftone dusk
  2. 6.02214076 × 10²³ — Mole Day, via Perrin's tracings of a jostled grain
  3. 60 m — Santos-Dumont's 14-bis at Bagatelle, 1906, everything at one scale
  4. Capistrano — the swallows leave on St John's day (so the legend goes)
  5. Crackle — a tea bowl's glaze, one break mended in red (no words)

Run: python3 generate.py <outdir>
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
INTER = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FREESERIF = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
SERIF_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


_pal = Image.new("P", (1, 1))
_pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)


def snap(img):
    """Any RGB image -> RGB containing only the three palette colours (no dither)."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img.convert("RGB").quantize(palette=_pal, dither=Image.Dither.NONE).convert("RGB")


def crisp(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return d


def finalize(img):
    return img.convert("RGB").quantize(palette=_pal, dither=Image.Dither.NONE)


def text_w(d, t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0]


def ctext(d, cx, y, t, f, fill):
    d.text((cx - text_w(d, t, f) / 2, y), t, font=f, fill=fill)


def dashed_poly(d, pts, dash, gap, fill, width=1):
    """Dashed polyline; dash/gap in pixels along the path."""
    on, run, seg = True, 0.0, [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        t = 0.0
        while t < L:
            step = min(L - t, (dash if on else gap) - run)
            t += step
            run += step
            p = (x0 + (x1 - x0) * t / L, y0 + (y1 - y0) * t / L)
            if on:
                seg.append(p)
            if run >= (dash if on else gap) - 1e-9:
                if on and len(seg) > 1:
                    d.line(seg, fill=fill, width=width)
                on, run, seg = not on, 0.0, [p]
    if on and len(seg) > 1:
        d.line(seg, fill=fill, width=width)


# ------------------------------------------------------ 1. England expects
# Numeral flags redrawn in the screen's three colours (the 1805 originals were


def wtext(d, x, y, t, f, fill):
    """Right-aligned text ending at x."""
    d.text((x - text_w(d, t, f), y), t, font=f, fill=fill)



def noise(shape, seed, scales=(64, 32, 16, 8), weights=(1, .5, .25, .12)):
    """Fractal value noise in [0,1] (bicubic-upsampled random grids)."""
    rng = np.random.default_rng(seed)
    h, w = shape
    acc = np.zeros(shape, np.float32)
    for s, wt in zip(scales, weights):
        g = rng.random((h // s + 3, w // s + 3)).astype(np.float32)
        im = Image.fromarray(g, "F").resize(((w // s + 3) * s, (h // s + 3) * s), Image.BICUBIC)
        acc += wt * np.asarray(im)[s:s + h, s:s + w]
    acc -= acc.min()
    return acc / acc.max()


def halftone(dark, cell, angle):
    """Classic AM screen: boolean ink mask; dot area follows `dark` in [0,1]."""
    h, w = dark.shape
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    c, s = math.cos(angle), math.sin(angle)
    u, v = (x * c + y * s) / cell, (-x * s + y * c) / cell
    du, dv = u - np.round(u), v - np.round(v)
    # spot function that grows from round dots into a chequer and back out to holes
    spot = (np.cos(math.pi * 2 * du) + np.cos(math.pi * 2 * dv)) / 4 + .5
    return spot > 1 - dark


def to_img(mask_rgb):
    return Image.fromarray(mask_rgb.astype(np.uint8))


# ------------------------------------------------------ 1. Ussher's nightfall
# Annales Veteris Testamenti (1650): time began "in noctis initium quae xxiii
# diem Octobris praecessit", Julian Period 710 = 4004 BC. Stars only on day four.

def image1_ussher():
    S = 3
    h, w = H * S, W * S
    hor = 222 * S
    y = np.mgrid[0:h, 0:w][0].astype(np.float32)
    t = np.clip((hor - y) / (hor - 46 * S), 0, 1)
    dark = np.clip(0.04 + 0.96 * t ** 1.15, 0, 1)
    ink = halftone(dark, 7.5 * S, math.radians(45))
    rgb = np.where(ink[..., None], np.uint8(0), np.uint8(255)) * np.ones(3, np.uint8)
    # the sun, just gone: a red cap above the line
    yy, xx = np.mgrid[0:h, 0:w]
    sun = ((xx - 268 * S) ** 2 + (yy - (hor + 6 * S)) ** 2 < (15 * S) ** 2)
    rgb[sun] = RED
    # land: a long low ridge
    xs = np.arange(w)
    ridge = hor + (2.5 * S * np.sin(xs / (61 * S)) + 4 * S * np.sin(xs / (23 * S) + 1)
                   - 10 * S * np.exp(-((xs - 90 * S) / (60 * S)) ** 2)
                   + 5 * S * np.exp(-((xs - 268 * S) / (40 * S)) ** 2))
    rgb[yy >= ridge[None, :].astype(int)] = BLACK
    rgb[sun & (yy < hor + 2 * S)] = RED
    img = snap(to_img(rgb))
    d = crisp(img)
    ctext(d, W / 2, 13, "in noctis initium quæ xxiii diem Octobris præcessit", font(SERIF_I, 16), WHITE)
    ctext(d, W / 2, 246, "No stars yet. Those came on the fourth day.", font(SERIF_I, 17), WHITE)
    ctext(d, W / 2, 274, "TIME BEGINS: NIGHTFALL BEFORE 23 OCT 4004 BC · USSHER 1650", font(MONO, 9), WHITE)
    return finalize(img)


# ------------------------------------------------------ 2. Perrin, for Mole Day
# Mole Day = 10/23, 6:02. Perrin's 1909 tracings of resin grains in water:
# positions every 30 s, joined by straight lines; he noted that sampling every
# second would turn each segment into a polygon of 30 sides. 3.2 µm grid.

def walk(rng, n, start, sig, box):
    x0, y0, x1, y1 = box
    p = [start]
    for _ in range(n):
        x, y = p[-1]
        x, y = x + rng.normal(0, sig), y + rng.normal(0, sig)
        x = x0 + abs(x - x0) if x < x0 else (x1 - abs(x - x1) if x > x1 else x)
        y = y0 + abs(y - y0) if y < y0 else (y1 - abs(y - y1) if y > y1 else y)
        p.append((x, y))
    return p


def image2_perrin(seed=6022):
    rng = np.random.default_rng(seed)
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    big = font(INTER, 30)
    d.text((14, 6), "6.02214076 × 10", font=big, fill=BLACK)
    d.text((14 + text_w(d, "6.02214076 × 10", big) + 2, 4), "23", font=font(INTER, 15), fill=BLACK)
    d.text((16, 44), "MOLE DAY · 10/23 · 6:02 · EXACT SINCE 20 MAY 2019", font=font(MONO, 9), fill=BLACK)
    gx0, gy0, n, g = 16, 64, 13, 16          # 13 × 13 squares of 3.2 µm
    for i in range(n + 1):
        for j in range(0, n * g + 1, 2):
            d.point((gx0 + i * g, gy0 + j), fill=BLACK)
            d.point((gx0 + j, gy0 + i * g), fill=BLACK)
    box = (gx0 + 4, gy0 + 4, gx0 + n * g - 4, gy0 + n * g - 4)
    tracks = [walk(rng, 30, (60, 100), 11, (gx0 + 4, gy0 + 4, gx0 + 100, gy0 + 110)),
              walk(rng, 30, (170, 110), 11, (gx0 + 110, gy0 + 4, gx0 + n * g - 4, gy0 + 120)),
              walk(rng, 30, (110, 230), 11, (gx0 + 30, gy0 + 120, gx0 + n * g - 4, gy0 + n * g - 4))]
    for tr in tracks:
        d.line(tr, fill=BLACK, width=1)
        for x, y in tr:
            d.rectangle((x - 1, y - 1, x + 1, y + 1), fill=BLACK)
    # the longest segment of the first track is the one we open up
    k = max(range(len(tracks[0]) - 1),
            key=lambda i: math.dist(tracks[0][i], tracks[0][i + 1]))
    a, b = tracks[0][k], tracks[0][k + 1]
    d.line((a, b), fill=RED, width=3)
    for x, y in (a, b):
        d.rectangle((x - 2, y - 2, x + 2, y + 2), fill=RED)
    # inset: the same 30 s at one-second resolution (Brownian bridge, 30 steps)
    ix0, iy0, iw = 248, 70, 140
    d.rectangle((ix0, iy0, ix0 + iw, iy0 + iw), outline=BLACK)
    steps = rng.normal(0, 1, (30, 2))
    path = np.vstack([[0, 0], np.cumsum(steps, 0)])
    path -= np.linspace(0, 1, 31)[:, None] * path[-1]
    path += np.linspace(0, 1, 31)[:, None] * np.array([1.0, 0.0]) * 6.0
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    c, s = math.cos(ang), math.sin(ang)
    path = path @ np.array([[c, s], [-s, c]])
    path -= (path.max(0) + path.min(0)) / 2
    sc = (iw - 24) / max(np.ptp(path[:, 0]), np.ptp(path[:, 1]))
    pts = [(ix0 + iw / 2 + px * sc, iy0 + iw / 2 + py * sc) for px, py in path]
    dashed_poly(d, [pts[0], pts[-1]], 3, 3, BLACK)
    d.line(pts, fill=RED, width=1)
    for x, y in pts:
        d.point((x, y), fill=RED)
    for x, y in (pts[0], pts[-1]):
        d.rectangle((x - 2, y - 2, x + 2, y + 2), fill=RED)
    si = font(SERIF_I, 16)
    d.text((ix0, iy0 + iw + 8), "Each straight line", font=si, fill=BLACK)
    d.text((ix0, iy0 + iw + 26), "hides thirty more.", font=si, fill=BLACK)
    d.text((ix0, iy0 + iw + 48), "RED SEGMENT, EVERY 1 S", font=font(MONO, 9), fill=BLACK)
    d.text((16, gy0 + n * g + 8), "AFTER J. PERRIN 1909 · A GRAIN EVERY 30 S · GRID 3.2 µm",
           font=font(MONO, 9), fill=BLACK)
    return finalize(img)


# ------------------------------------------------------ 3. Capistrano
# Legend (in print from 1924): the swallows leave the mission on St John's day,
# 23 October, for Goya, Argentina, ~6,000 miles south; back on 19 March.

SWALLOW = [(6, 0), (1, 1.4), (-3, 9), (-1.2, 1.4), (-5, 1), (-10.5, 3.8), (-7, 0),
           (-10.5, -3.8), (-5, -1), (-1.2, -1.4), (-3, -9), (1, -1.4)]


def swallow(d, x, y, head, s, fill, flap=1.0):
    c, sn = math.cos(head), math.sin(head)
    pts = []
    for px, py in SWALLOW:
        py = py * (flap if abs(py) > 5 else 1)
        pts.append((x + (px * c - py * sn) * s, y + (px * sn + py * c) * s))
    d.polygon(pts, fill=fill)


def bezier(t, P):
    u = 1 - t
    return (u ** 3 * P[0] + 3 * u * u * t * P[1] + 3 * u * t * t * P[2] + t ** 3 * P[3])


def image4_capistrano(seed=1023):
    rng = np.random.default_rng(seed)
    S = 3
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)
    # campanario: wall, stepped gable, four openings with bells
    k = lambda pts: [(x * S, y * S) for x, y in pts]
    d.rectangle(k([(22, 196), (142, 300)]), fill=BLACK)
    d.polygon(k([(40, 196), (40, 150), (54, 150), (60, 138), (104, 138), (110, 150),
                 (124, 150), (124, 196)]), fill=BLACK)
    d.rectangle(k([(79, 124), (85, 138)]), fill=BLACK)
    d.rectangle(k([(74, 128), (90, 132)]), fill=BLACK)

    def arch(x0, x1, y0, y1, bell):
        r = (x1 - x0) / 2
        d.rectangle(k([(x0, y0 + r), (x1, y1)]), fill=WHITE)
        d.ellipse(k([(x0, y0), (x1, y0 + 2 * r)]), fill=WHITE)
        cx = (x0 + x1) / 2
        d.line(k([(cx, y0 + 2), (cx, y0 + r + 2)]), fill=BLACK, width=S)
        bw, bh = bell, bell * 1.1
        by = y0 + r + 2
        d.polygon(k([(cx - bw * .3, by), (cx + bw * .3, by), (cx + bw * .45, by + bh * .7),
                     (cx + bw * .6, by + bh), (cx - bw * .6, by + bh), (cx - bw * .45, by + bh * .7)]),
                  fill=BLACK)
    arch(32, 72, 206, 262, 22)
    arch(92, 132, 206, 262, 22)
    arch(50, 76, 154, 190, 13)
    arch(88, 114, 154, 190, 13)
    # the flock, streaming off the top-right (south, on a map that faces it)
    P = [np.array(p, float) for p in [(118, 128), (175, 40), (300, 210), (420, 18)]]
    birds = []
    for _ in range(300):
        t = rng.beta(1.15, 1.25)
        c = bezier(t, P)
        tan = bezier(min(t + .01, 1), P) - bezier(max(t - .01, 0), P)
        head = math.atan2(tan[1], tan[0])
        nrm = np.array([-math.sin(head), math.cos(head)])
        spread = 6 + 46 * math.sin(math.pi * t) ** 1.4
        off = rng.normal(0, spread)
        q = c + nrm * off + rng.normal(0, 4, 2)
        sc = (0.95 - 0.55 * t) * rng.uniform(.75, 1.15)
        birds.append((q[0], q[1], head + rng.normal(0, .35), sc))
    birds.sort(key=lambda b: b[3])
    for x, y, hd, sc in birds:
        if x < 150 and y > 120 or not (0 < x < W and 0 < y < 236):
            continue
        swallow(d, x * S, y * S, hd, sc * S, BLACK, flap=rng.uniform(.55, 1.1))
    # one has not gone yet: perched on the cross-arm
    swallow(d, 92 * S, 123 * S, math.radians(-160), 1.15 * S, RED, flap=.35)
    img = snap(img)
    dd = crisp(img)
    wtext(dd, 390, 240, "They leave on St John's day,", font(SERIF_I, 16), BLACK)
    wtext(dd, 390, 258, "or so the mission says.", font(SERIF_I, 16), BLACK)
    wtext(dd, 390, 280, "23 OCT → GOYA, ARGENTINA · ~6,000 MI", font(MONO, 9), BLACK)
    return finalize(img)


# ------------------------------------------------------ 4. 14-bis, to scale
# Bagatelle, 23 Oct 1906: ~60 m at 2–3 m, about 7 s, took off unassisted; the
# Archdeacon cup asked for 25 m. ~9.7 m long, ~11.2 m span. Tail-first canard,
# pusher prop. Everything here is at one scale, vertical included.

def plane(d, x, ground, hm, ppm, S, fill, hatch=False):
    """14-bis side elevation, flying to the right; x = rear of the aircraft (px, 1x).
    Metres: rear 0 → nose 9.7, up from the wheel bottoms."""
    m = lambda X, Y: ((x + X * ppm) * S, (ground - (hm + Y) * ppm) * S)
    lw = max(1, round(S * ppm / 9))

    def panel(x0, x1, y0, y1, y0b=None, y1b=None):
        y0b = y0 if y0b is None else y0b
        y1b = y1 if y1b is None else y1b
        quad = [m(x0, y0), m(x1, y0b), m(x1, y1b), m(x0, y1)]
        if hatch:
            d.polygon(quad, outline=fill, width=lw * 2)
            for k in np.arange(x0 + .25, x1, .3):
                f = (k - x0) / (x1 - x0)
                d.line([m(k, y0 + (y0b - y0) * f), m(k, y1 + (y1b - y1) * f)], fill=fill, width=lw)
        else:
            d.polygon(quad, fill=fill)
    # boom: two longerons from the wing cells forward to the canard, a few struts
    top = [(1.0, 3.25), (8.0, 3.0)]
    bot = [(1.0, 2.25), (8.0, 2.75)]
    d.line([m(*top[0]), m(*top[1])], fill=fill, width=lw)
    d.line([m(*bot[0]), m(*bot[1])], fill=fill, width=lw)
    if hatch:
        for k in np.linspace(3.5, 7.5, 6):
            f = (k - 1) / 7
            yt, yb = 3.25 - .25 * f, 2.25 + .5 * f
            d.line([m(k, yt), m(k + .6, yb + .04)], fill=fill, width=lw)
    # main Hargrave cells (outer side panel faces us), biplane, at the rear
    panel(0.9, 3.4, 2.0, 3.65)
    # canard box cell at the nose, tilted up a touch
    panel(7.8, 9.7, 2.3, 3.5, 2.45, 3.65)
    # pusher propeller and engine behind the cells
    d.line([m(0.3, 1.55), m(0.3, 4.05)], fill=fill, width=lw * 2)
    d.rectangle([m(0.45, 3.05), m(0.9, 2.55)], fill=fill)
    # pilot standing in his basket just ahead of the cells
    d.rectangle([m(3.75, 3.05), m(4.35, 2.3)], fill=fill if not hatch else None,
                outline=fill, width=lw)
    d.line([m(4.05, 3.05), m(4.05, 3.55)], fill=fill, width=lw * 2)
    r = 0.17 * ppm * S
    hx, hy = m(4.05, 3.72)
    d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=fill)
    # undercarriage
    for xx in (1.9, 2.7):
        d.line([m(xx, 2.0), m(xx, 0.4)], fill=fill, width=lw)
        r = 0.4 * ppm * S
        cx, cy = m(xx, 0.4)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=fill, width=lw)


def image3_14bis():
    S = 3
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)
    x0, ppm, gy = 34, 5.5, 214

    def wheels(s):  # wheel-bottom height (m) at distance s along the ground
        if s <= 0 or s >= 60:
            return 0.0
        return 2.7 * math.sin(math.pi * s / 60) ** .55
    # red: all the air there ever was under the wheels
    poly = [(x0 + s * ppm, gy - wheels(s) * ppm) for s in np.linspace(0, 60, 121)]
    d.polygon([(x * S, y * S) for x, y in poly], fill=RED)
    d.line([(8 * S, gy * S), (392 * S, gy * S)], fill=BLACK, width=2 * S)
    sm, rear_off = 30, 2.3
    plane(d, x0 + (sm - rear_off) * ppm, gy, wheels(sm), ppm, S, BLACK)
    # the same machine, enlarged, directly above
    big = 18.0
    bx = x0 + sm * ppm - rear_off * big
    plane(d, bx, 166, 0, big, S, BLACK, hatch=True)
    img = snap(img)
    dd = crisp(img)
    m9 = font(MONO, 9)
    dd.text((bx - 4 - text_w(dd, "×3.3", m9), 158), "×3.3", font=m9, fill=BLACK)
    for s in range(0, 61, 10):
        x = x0 + s * ppm
        dd.line((x, gy + 2, x, gy + 6), fill=BLACK)
        ctext(dd, x, gy + 8, f"{s}", m9, BLACK)
    for s in range(0, 61, 2):
        dd.point((x0 + s * ppm, gy + 3), fill=BLACK)
    xa = x0 + 25 * ppm
    dd.line((xa, gy + 20, xa, gy + 26), fill=BLACK)
    dd.text((xa + 4, gy + 19), "ARCHDEACON CUP ASKED FOR 25 M", font=m9, fill=BLACK)
    dd.text((x0 + 60 * ppm + 5, gy + 8), "m", font=m9, fill=BLACK)
    dd.text((14, 6), "60 m", font=font(INTER, 64), fill=BLACK)
    lines = ["BAGATELLE, PARIS", "23 OCTOBER 1906", "SANTOS-DUMONT, 14-BIS", "≈7 S · 2–3 M UP",
             "ONE SCALE, BOTH WAYS"]
    for i, t in enumerate(lines):
        wtext(dd, 388, 12 + i * 12, t, m9, BLACK)
    ctext(dd, W / 2, 256, "About seven seconds. The red is all the air he used.",
          font(SERIF_I, 16), BLACK)
    ctext(dd, W / 2, 278, "First powered flight officially witnessed in Europe.", font(SERIF_I, 13), BLACK)
    return finalize(img)


# ------------------------------------------------------ 5. Crackle (no words)
# A tea bowl's crackle glaze, two generations of cracks, and one break mended
# in red lacquer the way kintsugi mends with gold.

def voronoi_edges(px, py, sites, width):
    d1 = np.full(px.shape, 1e9, np.float32)
    d2 = np.full(px.shape, 1e9, np.float32)
    for sx, sy in sites:
        dd = np.hypot(px - sx, py - sy)
        d2 = np.where(dd < d1, d1, np.minimum(d2, dd))
        d1 = np.minimum(d1, dd)
    return (d2 - d1) < width


def image5_crackle(seed=4004):
    rng = random.Random(seed)
    S = 3
    h, w = H * S, W * S
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # bowl silhouette (chawan): rim y=58, body to y=236, foot ring below
    rim, base, cx = 58 * S, 236 * S, 200 * S
    tt = np.clip((yy - rim) / (base - rim), 0, 1)
    half = (118 - 10 * tt ** 1.6 - 46 * tt ** 4.0) * S
    body = (yy >= rim) & (yy <= base) & (np.abs(xx - cx) <= half)
    foot = (yy > base - 6 * S) & (yy <= 250 * S) & (np.abs(xx - cx) <= (44 - (yy - base) / S * .25) * S)
    bowl = body | foot
    # domain warp so the cracks wander
    n1 = noise((h, w), seed, (96, 48, 24), (1, .5, .25)) - .5
    n2 = noise((h, w), seed + 1, (96, 48, 24), (1, .5, .25)) - .5
    px, py = xx + n1 * 16 * S, yy + n2 * 16 * S
    big = [(rng.uniform(60, 340) * S, rng.uniform(40, 270) * S) for _ in range(34)]
    small = [(rng.uniform(60, 340) * S, rng.uniform(40, 270) * S) for _ in range(190)]
    c1 = voronoi_edges(px, py, big, 1.6 * S)
    n3 = noise((h, w), seed + 2, (24, 12), (1, .5)) - .5
    c2 = voronoi_edges(px + n3 * 6 * S, py + n3 * 6 * S, small, 0.75 * S)
    # glaze thins toward the foot: fewer fine cracks lower down
    fade = noise((h, w), seed + 3, (32, 16), (1, .5))
    c2 &= fade > (tt * 0.9 + 0.15)
    rgb = np.full((h, w, 3), 0, np.uint8)               # black ground
    rgb[bowl] = WHITE
    rgb[bowl & (c1 | c2) & (yy > rim + 6 * S)] = BLACK
    rgb[foot & (yy > base)] = WHITE
    # the mended break: a jagged seam from rim down, with one branch
    img = Image.fromarray(rgb)
    d = ImageDraw.Draw(img)
    pts, x, y = [], 236.0, 58.0
    while y < 196:
        pts.append((x * S, y * S))
        y += rng.uniform(6, 13)
        x += rng.uniform(-9, 6)
    br, x, y = [pts[7]], pts[7][0] / S, pts[7][1] / S
    while x < 292:
        x += rng.uniform(6, 12)
        y += rng.uniform(-2, 7)
        br.append((x * S, y * S))
    d.line(pts, fill=RED, width=int(3.2 * S), joint="curve")
    d.line(br, fill=RED, width=int(2.4 * S), joint="curve")
    rgb = np.asarray(img).copy()
    rgb[~bowl] = BLACK
    img = Image.fromarray(rgb)
    d = ImageDraw.Draw(img)
    # rim lip: a thin black line inside the white so the top edge reads
    d.line([(84 * S, 64 * S), (316 * S, 64 * S)], fill=BLACK, width=S)
    d.line([(150 * S, 238 * S), (250 * S, 238 * S)], fill=BLACK, width=S)
    return finalize(snap(img))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    ims = [image1_ussher(), image2_perrin(), image3_14bis(), image4_capistrano(), image5_crackle()]
    for i, im in enumerate(ims, 1):
        assert im.size == (W, H)
        im.save(os.path.join(out, f"{i}.png"))


if __name__ == "__main__":
    main()
