#!/usr/bin/env python3
"""Daily e-ink pictures - 2026-10-04.  Theme: "Signals".

Saturn at opposition (12 UTC today), Sputnik's 69th launch anniversary,
World Animal Day / St Francis, Chladni sound figures, and a LeWitt-style
instruction drawing. Five 400x300 PNGs in exactly white/black/red.
"""

import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_pal = Image.new("P", (1, 1))
_pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)


def finalize(img, dither=False):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=_pal, dither=d)


def F(path, size):
    return ImageFont.truetype(path, size)


def crisp(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"  # no antialiasing: text stays pure palette colours
    return d


def label(d, x, y, text, fill=BLACK, size=10, path=MONO):
    d.text((x, y), text, font=F(path, size), fill=fill)


# ------------------------------------------------------------ 1. Saturn
def saturn():
    S = 3
    w, h = W * S, H * S
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    cx, cy = w * 0.5, h * 0.47
    R = 62 * S                      # equatorial radius in px
    flat = 0.902                    # polar / equatorial
    B = math.radians(7.5)           # ring opening, south face toward us
    x = (xx - cx) / R
    y = (yy - cy) / R               # y down
    img = np.zeros((h, w, 3))

    # stars
    rng = random.Random(1004)
    for _ in range(90):
        sx, sy = rng.randrange(w), rng.randrange(h)
        r = rng.choice([1, 1, 2, 3])
        img[max(0, sy - r):sy + r, max(0, sx - r):sx + r] = 255

    # planet: oblate disc, tipped so the south pole is toward us (south = down)
    yp = y / flat
    rho2 = x * x + yp * yp
    disc = rho2 < 1
    mu = np.sqrt(np.clip(1 - rho2, 0, 1))
    # latitude-ish coordinate for bands: rotate by B about x axis
    lat = np.arcsin(np.clip(yp * math.cos(B) - mu * math.sin(B), -1, 1))
    band = 0.78 + 0.12 * np.cos(lat * 9.0) + 0.06 * np.cos(lat * 23 + 1.3)
    band -= 0.25 * np.clip((np.abs(lat) - 1.05) * 2.5, 0, 1)  # dark polar caps
    shade = band * (0.35 + 0.65 * mu ** 0.6)
    gray = np.clip(shade * 255, 0, 255)
    for c in range(3):
        img[..., c] = np.where(disc, gray, img[..., c])

    # rings: radius in the ring plane; near side is UP (north) for a south-facing view
    rr = np.sqrt(x * x + (y / math.sin(B)) ** 2)
    near = y < 0
    zones = [  # (inner, outer, density) in Saturn radii
        (1.24, 1.53, 0.30), (1.53, 1.95, 1.00), (1.95, 2.03, 0.0),
        (2.03, 2.21, 0.70), (2.21, 2.22, 0.0), (2.22, 2.27, 0.60)]
    dens = np.zeros_like(rr)
    for a, b, dd in zones:
        dens = np.where((rr >= a) & (rr < b), dd, dens)
    ringvis = (dens > 0) & (near | ~disc)
    # red ring dithered with black: mix colour = red * density
    img[..., 0] = np.where(ringvis, 255 * (0.25 + 0.75 * dens), img[..., 0])
    img[..., 1] = np.where(ringvis, 0, img[..., 1])
    img[..., 2] = np.where(ringvis, 0, img[..., 2])
    # where the near ring crosses the disc, a thin black edge keeps them apart
    im = Image.fromarray(img.astype(np.uint8))
    out = finalize(im, dither=True).convert("RGB")

    d = crisp(out)
    d.rectangle([0, 262, W, H], fill=BLACK)
    label(d, 10, 266, "SATURN AT OPPOSITION", WHITE, 13, MONO_B)
    label(d, 10, 283, "04 OCT 2026 12:00 UTC · in Cetus", WHITE, 10)
    label(d, 268, 268, "rings open 7.5° S", RED, 10)
    label(d, 268, 283, "mag +0.3 · 1.26 Gm", WHITE, 10)
    label(d, 10, 8, "the Sun is directly behind you tonight", WHITE, 10)
    label(d, 10, 21, "— so Saturn swallows its own shadow,", WHITE, 10)
    label(d, 10, 34, "  and the rings flare (Seeliger effect)", RED, 10)
    return finalize(out)


# ------------------------------------------------------------ 2. Sputnik
def sputnik():
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    # equirectangular ground-track panel
    px0, py0, pw, ph = 10, 40, 380, 190
    d.rectangle([px0, py0, px0 + pw, py0 + ph], outline=BLACK)
    for lat in (-60, -30, 0, 30, 60):
        yv = py0 + ph / 2 - lat / 90 * ph / 2
        for xv in range(px0, px0 + pw, 4):
            d.point((xv, yv), fill=BLACK)
    for lon in range(-150, 180, 30):
        xv = px0 + (lon + 180) / 360 * pw
        for yv in range(py0, py0 + ph, 4):
            d.point((xv, yv), fill=BLACK)
    inc = math.radians(65.1)
    P = 96.2 * 60
    we = 2 * math.pi / 86164
    lam0 = math.radians(63.3)  # Baikonur longitude, launch site
    lat0 = math.radians(45.9)
    u0 = math.asin(math.sin(lat0) / math.sin(inc))
    node = lam0 - math.atan2(math.cos(inc) * math.sin(u0), math.cos(u0))

    def track(t0, t1, col, wid):
        prev = None
        t = t0
        while t <= t1:
            u = u0 + 2 * math.pi * t / P
            la = math.asin(math.sin(inc) * math.sin(u))
            lo = node + math.atan2(math.cos(inc) * math.sin(u), math.cos(u)) - we * t
            lo = (lo + math.pi) % (2 * math.pi) - math.pi
            X = px0 + (lo + math.pi) / (2 * math.pi) * pw
            Y = py0 + ph / 2 - la / (math.pi / 2) * ph / 2
            if prev and abs(prev[0] - X) < pw / 2:
                d.line([prev, (X, Y)], fill=col, width=wid)
            prev = (X, Y)
            t += 20
    track(P, 15 * P, BLACK, 1)          # the rest of the first day
    track(0, P, RED, 2)                 # orbit one, in red
    # launch site
    bx = px0 + (lam0 + math.pi) / (2 * math.pi) * pw
    by = py0 + ph / 2 - lat0 / (math.pi / 2) * ph / 2
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=RED, outline=BLACK)
    label(d, bx + 6, by - 14, "Байконур", BLACK, 10)

    # the satellite itself, top right
    sx, sy = 372, 18
    for ang, ln in ((160, 30), (168, 34), (192, 34), (200, 30)):
        a = math.radians(ang)
        d.line([(sx, sy), (sx + ln * math.cos(a), sy - ln * math.sin(a) * 0.4 + 4)], fill=BLACK)
    d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=BLACK)
    d.ellipse([sx - 5, sy - 5, sx - 2, sy - 2], fill=WHITE)
    label(d, 10, 6, "ПС-1 · 4 X 1957 · 69 years ago", BLACK, 13, MONO_B)
    label(d, 10, 23, "one day of ground track · orbit one in red", BLACK, 10)

    # the beep: two carriers alternating 0.3 s on / 0.3 s off
    y1, y2 = 248, 272
    label(d, 10, y1 - 4, "20.005", BLACK, 10)
    label(d, 10, y2 - 4, "40.002", RED, 10)
    x = 62
    on = True
    while x < 390:
        seg = 22
        for (yy, col, active) in ((y1, BLACK, on), (y2, RED, not on)):
            if active:
                for k in range(0, seg, 2):
                    amp = 7
                    d.line([(x + k, yy - amp), (x + k, yy + amp)], fill=col)
            else:
                d.line([(x, yy), (x + seg, yy)], fill=col)
        on = not on
        x += seg + 2
    label(d, 62, 284, "beep — beep — beep   (MHz, 0.3 s each, 22 days until silence)", BLACK, 9)
    return finalize(img)


# ------------------------------------------------------------ 3. Chladni
def chladni():
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    n, m = 10, 4                     # October 4th
    x0, y0, s = 16, 16, 268
    rng = np.random.default_rng(20261004)
    pts = rng.random((260000, 2))
    X, Y = pts[:, 0], pts[:, 1]
    f = (np.cos(n * np.pi * X) * np.cos(m * np.pi * Y)
         - np.cos(m * np.pi * X) * np.cos(n * np.pi * Y))
    keep = np.abs(f) < 0.055 + 0.04 * rng.random(len(f))
    # a scatter of stray grains still travelling
    stray = rng.random(len(f)) < 0.012
    arr = np.array(img)
    for sel, col in ((keep | stray, 0),):
        xs = (x0 + X[sel] * s).astype(int)
        ys = (y0 + Y[sel] * s).astype(int)
        arr[ys, xs] = col
    img = Image.fromarray(arr)
    d = crisp(img)
    d.rectangle([x0 - 1, y0 - 1, x0 + s, y0 + s], outline=BLACK)
    c = (x0 + s / 2, y0 + s / 2)
    d.ellipse([c[0] - 4, c[1] - 4, c[0] + 4, c[1] + 4], fill=RED)
    # right column
    rx = 298
    label(d, rx, 16, "CHLADNI", BLACK, 16, SERIF_B)
    label(d, rx, 36, "FIGURE", BLACK, 16, SERIF_B)
    label(d, rx, 66, "mode", BLACK, 10)
    label(d, rx, 78, "(10, 4)", RED, 20, SERIF_B)
    label(d, rx, 104, "for 10/04", BLACK, 10)
    txt = ["Sand on a brass", "plate, bowed until", "it sings. Grains", "flee the moving",
           "parts and gather", "where the plate", "stands still.", "", "Chladni, 1787.",
           "Napoleon paid", "3,000 francs for", "the maths of it.", "", "red: the bolt"]
    for i, t in enumerate(txt):
        label(d, rx, 132 + i * 11, t, RED if t.startswith("red") else BLACK, 9)
    return finalize(img)


# ------------------------------------------------------------ 4. Murmuration
def murmuration():
    img = Image.new("RGB", (W, H), WHITE)
    rng = random.Random(4102026)
    arr = np.full((H, W, 3), 255, np.uint8)

    def centre(t):  # spine of a twisting ribbon of birds, t in 0..1
        x = 45 + 300 * t + 22 * math.sin(t * 9.0)
        y = 135 - 70 * abs(math.sin(math.pi * t)) ** 1.5 + 30 * math.sin(t * 7.3 + 0.8)
        return x, y

    for _ in range(16000):
        t = rng.random()
        x, y = centre(t)
        x2, y2 = centre(t + 0.002)
        nx, ny = -(y2 - y), (x2 - x)
        ln = math.hypot(nx, ny) or 1
        # the ribbon twists: where it turns edge-on it pinches into a dark fold
        width = 3 + 34 * abs(math.cos(2.6 * math.pi * t + 0.4)) * math.sin(math.pi * t) ** 0.5
        g = rng.uniform(-1, 1) * width * (0.6 + 0.4 * rng.random())
        bx = int(x + nx / ln * g + rng.gauss(0, 2))
        by = int(y + ny / ln * g + rng.gauss(0, 2))
        if 0 <= bx < W and 0 <= by < 225:
            arr[by, bx] = 0
    img = Image.fromarray(arr)
    d = crisp(img)
    # a few stragglers as tiny wings
    for _ in range(40):
        bx, by = rng.uniform(20, 380), rng.uniform(20, 210)
        d.line([(bx - 2, by - 1), (bx, by), (bx + 2, by - 1)], fill=BLACK)
    # the one who turns first
    rx, ry = 338, 52
    d.line([(rx - 5, ry - 3), (rx, ry), (rx + 5, ry - 3)], fill=RED, width=2)
    # reed bed and water
    d.rectangle([0, 258, W, H], fill=BLACK)
    for i in range(700):
        xr = rng.uniform(0, W)
        top = 258 - rng.uniform(4, 34) * (0.6 + 0.4 * math.sin(xr / 37) ** 2)
        lean = rng.uniform(-3, 3)
        d.line([(xr, 258), (xr + lean, top)], fill=BLACK)
        if rng.random() < 0.08:
            d.ellipse([xr + lean - 1, top - 4, xr + lean + 2, top + 3], fill=BLACK)
    label(d, 10, 266, "MURMURATION", WHITE, 13, MONO_B)
    label(d, 10, 283, "4 Oct · World Animal Day · feast of St Francis", WHITE, 10)
    label(d, 300, 268, "each bird", RED, 10)
    label(d, 300, 283, "watches seven", RED, 10)
    return finalize(img)


# ------------------------------------------------------------ 5. Instruction drawing
def instruction():
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    top = 248
    # black arcs from the two lower corners, every 7 px -> moire
    for (ox, oy) in ((0, top), (W, top)):
        for r in range(7, 520, 7):
            d.arc([ox - r, oy - r, ox + r, oy + r], 180, 360, fill=BLACK)
    # 24 red lines from the centre of the top edge, stopping at the arcs' horizon
    cx, cy = W / 2, 0
    for k in range(24):
        a = math.radians(5 + k * (170 / 23))
        L = 600
        ex, ey = cx + L * math.cos(a), cy + L * math.sin(a)
        if ey > top:  # clip at the baseline
            t = (top - cy) / (ey - cy)
            ex, ey = cx + (ex - cx) * t, top
        d.line([(cx, cy), (ex, ey)], fill=RED)
    d.rectangle([0, top, W, H], fill=WHITE)
    d.line([(0, top), (W, top)], fill=BLACK)
    label(d, 10, top + 6, "WALL DRAWING FOR A SMALL SCREEN, NO. 1   (after Sol LeWitt)", BLACK, 9, MONO_B)
    label(d, 10, top + 19, "Black arcs from the two lower corners, 7 px apart.", BLACK, 9)
    label(d, 10, top + 30, "Twenty-four red lines from the midpoint of the top side.", RED, 9)
    label(d, 10, top + 41, "The drawing is the instruction; this is one performance of it.", BLACK, 9)
    return finalize(img)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    for i, fn in enumerate([saturn, sputnik, chladni, murmuration, instruction], 1):
        im = fn()
        assert im.size == (W, H)
        im.save(os.path.join(out, f"{i}.png"), optimize=True)


if __name__ == "__main__":
    main()
