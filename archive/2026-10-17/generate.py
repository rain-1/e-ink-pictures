#!/usr/bin/env python3
"""Plates 001-005 · 2026-10-17 · 400x300 black/white/red e-ink.

Run from anywhere:  python3 generate.py [outdir]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
DATE = "17·X·2026"
SEED = 20261017

F = "/usr/share/fonts/truetype/"
MONO = F + "dejavu/DejaVuSansMono.ttf"
MONO_B = F + "dejavu/DejaVuSansMono-Bold.ttf"
SERIF = F + "liberation/LiberationSerif-Regular.ttf"
SERIF_I = F + "liberation/LiberationSerif-Italic.ttf"
SERIF_B = F + "liberation/LiberationSerif-Bold.ttf"
INTER_B = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
INTER = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"


def font(p, s):
    return ImageFont.truetype(p, s)


PALETTE = np.array([WHITE, BLACK, RED], dtype=np.int32)


def to_palette(img):
    """Nearest-colour snap (no dithering) to the exact 3-colour palette."""
    a = np.asarray(img.convert("RGB"), dtype=np.int32)
    d = ((a[:, :, None, :] - PALETTE[None, None]) ** 2).sum(-1)
    idx = d.argmin(-1).astype(np.uint8)
    out = Image.fromarray(idx, "P")
    pal = [255, 255, 255, 0, 0, 0, 255, 0, 0] + [0] * (253 * 3)
    out.putpalette(pal)
    return out


def hard(img):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return to_palette(img)


def colophon(d, n, fg=BLACK, bg=None, x=None, y=None):
    """My mark: a small red lozenge and a running plate number."""
    f = font(MONO, 9)
    t = f"№{n:03d}"
    tw = d.textlength(t, font=f)
    x = W - tw - 6 if x is None else x
    y = H - 13 if y is None else y
    if bg is not None:
        d.rectangle([x - 12, y - 1, x + tw + 2, y + 11], fill=bg)
    d.polygon([(x - 8, y + 5), (x - 5, y + 2), (x - 2, y + 5), (x - 5, y + 8)], fill=RED)
    d.text((x, y), t, font=f, fill=fg)


# ------------------------------------------------------------- 1 helicorder
def plate_helicorder():
    """Loma Prieta, 17 Oct 1989 17:04 PDT, as a drum seismogram."""
    S = 2
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)
    rng = np.random.default_rng(1989)
    top, bot, left, right = 58, 286, 34, 392
    nlines = 20
    gap = (bot - top) / (nlines - 1)
    # each line = 30 minutes, starting 08:00 local
    quake_line, quake_x = 18, 0.14  # 17:00 line, 4 min in
    f_small = font(MONO, 8 * S)
    for i in range(nlines):
        y0 = top + i * gap
        hh = 8 + i // 2
        mm = "00" if i % 2 == 0 else "30"
        if i % 2 == 0:
            d.text((4 * S, (y0 - 4) * S), f"{hh:02d}:{mm}", font=f_small, fill=BLACK)
        n = (right - left) * 3
        xs = np.linspace(left, right, n)
        t = np.linspace(0, 1, n)
        noise = rng.normal(0, 0.45, n)
        noise = np.convolve(noise, np.ones(3) / 3, "same")
        micro = 0.6 * np.sin(t * 2 * math.pi * 55 + i) * (0.5 + 0.5 * np.sin(t * 7 + i))
        ys = y0 + noise + micro * 0.5
        col = BLACK
        if i == quake_line:
            env = np.where(t > quake_x, np.exp(-(t - quake_x) * 9) * (1 - np.exp(-(t - quake_x) * 300)), 0)
            burst = env * 70 * rng.normal(0, 1, n)
            burst = np.convolve(burst, np.ones(2) / 2, "same")
            ys = ys + burst
            col = RED
        if i == quake_line + 1:
            env = 0.10 + 0.35 * np.exp(-t * 4)
            ys = ys + env * 22 * rng.normal(0, 1, n) * (rng.random(n) < 0.6)
            for k in range(3):  # aftershocks
                c = rng.uniform(0.3, 0.95)
                ys = ys + np.exp(-((t - c) / 0.01) ** 2) * 8 * rng.normal(0, 1, n)
            col = RED
        if i < quake_line:  # foreshock-free calm; faint pen tremor only
            pass
        pts = [(float(x) * S, float(y) * S) for x, y in zip(xs, ys)]
        d.line(pts, fill=col, width=1 * S if col == BLACK else max(1, S))
        # minute ticks
        for m in range(1, 30):
            mx = left + (right - left) * m / 30
            if m % 5 == 0:
                d.line([(mx * S, (y0 - 1) * S), (mx * S, (y0 + 1) * S)], fill=BLACK, width=1)
    img = img.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    # header (on top of trace chaos, with white knockout)
    d.rectangle([0, 0, W, 46], fill=WHITE)
    d.text((8, 6), "LOMA PRIETA", font=font(INTER_B, 24), fill=BLACK)
    d.text((10, 33), "17 OCT 1989 · 17:04:15 PDT · Mw 6.9", font=font(MONO, 9), fill=BLACK)
    d.text((W - 8, 8), "37", font=font(INTER_B, 26), fill=RED, anchor="ra")
    d.text((W - 8, 36), "years ago today", font=font(SERIF_I, 11), fill=BLACK, anchor="ra")
    d.line([(8, 49), (W - 8, 49)], fill=BLACK, width=1)
    # note box bottom-left within calm lines
    f = font(SERIF_I, 11)
    note = ["Fifteen seconds of shaking, minutes before", "Game 3 of the Bay Bridge World Series."]
    bx, by = 170, 64
    d.rectangle([bx - 4, by - 3, bx + 222, by + 29], fill=WHITE, outline=BLACK)
    for k, s in enumerate(note):
        d.text((bx, by + k * 13), s, font=f, fill=BLACK)
    out = hard(img)
    colophon(ImageDraw.Draw(out), 1, bg=WHITE)
    return out


# ------------------------------------------------------------- 2 lunar X
def plate_lunar_x():
    """First quarter tomorrow: terminator relief, Lunar X marked in red."""
    S = 3
    w, h = W * S, H * S
    cx, cy, R = 138 * S, 152 * S, 124 * S
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    X = (xx - cx) / R
    Y = (yy - cy) / R
    r2 = X * X + Y * Y
    inside = r2 < 1
    Z = np.sqrt(np.clip(1 - r2, 0, 1))
    lat = np.degrees(np.arcsin(np.clip(-Y, -1, 1)))
    lon = np.degrees(np.arctan2(X, Z))
    rng = np.random.default_rng(SEED)

    # albedo: maria as soft blobs at (lat, lon, radius_deg)
    maria = [(33, -16, 17), (28, 17, 10), (8.5, 31, 13), (17, 59, 8), (-8, 51, 10),
             (-15, 35, 7), (-21, -17, 11), (18, -57, 25), (56, 1, 6), (13, 4, 5),
             (-24, -39, 6), (2, -16, 6), (44, 15, 6)]
    alb = np.ones_like(X)
    for la, lo, rad in maria:
        dlat = lat - la
        dlon = (lon - lo) * np.cos(np.radians(la))
        dd = np.sqrt(dlat ** 2 + dlon ** 2)
        alb -= 0.42 * np.clip(1.2 - dd / rad, 0, 1) ** 0.7 / 1.2
    alb = np.clip(alb, 0.45, 1)

    # height field of craters in (lon, lat) degrees -> relief shading
    hgt = np.zeros_like(X)
    craters = [(rng.uniform(-80, 80), rng.uniform(-80, 80), r) for r in
               np.concatenate([rng.uniform(1.2, 3, 260), rng.uniform(3, 8, 45), rng.uniform(8, 14, 6)])]
    # the Lunar X trio: Blanchinus, La Caille, Purbach (+ Werner)
    craters += [(2.5, -25.3, 3.4), (1.1, -23.8, 3.5), (-1.9, -25.5, 4.5), (3.3, -28, 3.3)]
    cosl = np.cos(np.radians(lat))
    for lo, la, r in craters:
        dlon = (lon - lo) * cosl
        dd = np.sqrt((lat - la) ** 2 + dlon ** 2) / r
        m = dd < 1.6
        if not m.any():
            continue
        prof = np.where(dd < 1, dd ** 2 - 1, 0.25 * np.exp(-((dd - 1) / 0.25) ** 2))
        hgt[m] += (prof[m] + 0.25 * (dd[m] < 1)) * r * 0.25
    hgt += 0.6 * np.cumsum(rng.normal(0, 0.02, X.shape), axis=1) * 0  # keep deterministic, flat
    gx = np.gradient(hgt, axis=1) * (R / 90)  # slope towards +x (sun side)
    # sun from +x, a touch past 90° (≈ first quarter)
    sun = np.radians(91)
    L = np.array([math.sin(sun), 0, math.cos(sun)])
    nx, ny, nz = X, -Y, Z
    mu0 = nx * L[0] + nz * L[2]
    mu = np.clip(Z, 1e-3, 1)
    base = np.where(mu0 > 0, mu0 / (mu0 + mu), 0) * 2
    graz = np.exp(-np.clip(mu0, 0, 1) * 5)  # relief strongest near terminator
    relief = gx * (0.6 + 2.5 * graz)
    lit = base * alb + relief * (mu0 > -0.04)
    lit = np.where(mu0 > -0.04, lit, 0)
    lit = np.clip(lit, 0, 1.15)
    lit[~inside] = 0
    g = (np.clip(lit, 0, 1) * 255).astype(np.uint8)
    moon = Image.fromarray(g, "L").resize((W, H), Image.LANCZOS)
    moon = moon.convert("1", dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    d = ImageDraw.Draw(moon)
    # Lunar X marker
    la, lo = -25.0, 0.9
    px = cx / S + R / S * math.cos(math.radians(la)) * math.sin(math.radians(lo))
    py = cy / S - R / S * math.sin(math.radians(la))
    d.ellipse([px - 11, py - 11, px + 11, py + 11], outline=RED, width=2)
    k = 4
    d.line([(px - k, py - k), (px + k, py + k)], fill=RED, width=2)
    d.line([(px - k, py + k), (px + k, py - k)], fill=RED, width=2)
    d.line([(px - 11, py + 3), (px - 40, py + 40), (14, py + 40)], fill=RED, width=1)
    # text column
    tx = 276
    d.text((tx, 22), "FIRST", font=font(INTER_B, 23), fill=WHITE)
    d.text((tx, 48), "QUARTER", font=font(INTER_B, 23), fill=WHITE)
    d.text((tx + 1, 80), "SUN 18 OCT 2026", font=font(MONO, 9), fill=RED)
    body = ["For an hour or two the", "sun grazes the rims of", "Blanchinus, La Caille", "and Purbach before it",
            "reaches their floors —", "a glowing X floats in", "the dark."]
    f = font(SERIF_I, 12)
    for i, s in enumerate(body):
        d.text((tx, 102 + i * 14), s, font=f, fill=WHITE)
    d.text((14, py + 37), "LUNAR X", font=font(MONO_B, 11), fill=RED, anchor="ls")
    out = to_palette(moon)
    colophon(ImageDraw.Draw(out), 2, fg=WHITE)
    return out


# ------------------------------------------------------------- 3 weave draft
def plate_weave():
    """An 8-shaft weave draft: threading × tie-up × treadling = cloth."""
    rng = np.random.default_rng(SEED)
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    c = 4  # cell px
    ends, picks, shafts = 62, 58, 8
    # threading: broken point twill
    seq = list(range(8)) + list(range(6, 0, -1))
    threading = [seq[j % len(seq)] for j in range(ends)]
    # tie-up: 8x8 twill 3/1/1/3 rotated
    base = [1, 1, 1, 0, 1, 0, 0, 0]
    tie = np.array([[base[(s - t) % 8] for t in range(8)] for s in range(8)])
    # treadling: point treadling in blocks with date-seeded jumps
    tread, t, step = [], 0, 1
    for i in range(picks):
        tread.append(t)
        if rng.random() < 0.18:
            step = -step
        t = (t + step) % 8
    weft_red = np.zeros(picks, bool)
    for a, b in [(10, 14), (28, 30), (44, 50)]:
        weft_red[a:b] = True
    x0, y0 = 8, 8 + shafts * c + 6  # drawdown origin
    tx0 = x0 + ends * c + 6  # treadling/tie-up column
    # threading grid
    for j in range(ends):
        for s in range(shafts):
            x, y = x0 + j * c, 8 + (shafts - 1 - s) * c
            d.rectangle([x, y, x + c, y + c], outline=BLACK)
            if threading[j] == s:
                d.rectangle([x + 1, y + 1, x + c - 1, y + c - 1], fill=BLACK)
    # tie-up
    for t_ in range(8):
        for s in range(shafts):
            x, y = tx0 + t_ * c, 8 + (shafts - 1 - s) * c
            d.rectangle([x, y, x + c, y + c], outline=BLACK)
            if tie[s, t_]:
                d.rectangle([x + 1, y + 1, x + c - 1, y + c - 1], fill=RED)
    # treadling
    for i in range(picks):
        for t_ in range(8):
            x, y = tx0 + t_ * c, y0 + i * c
            d.rectangle([x, y, x + c, y + c], outline=BLACK)
            if tread[i] == t_:
                d.rectangle([x + 1, y + 1, x + c - 1, y + c - 1], fill=RED if weft_red[i] else BLACK)
    # drawdown / cloth
    for i in range(picks):
        for j in range(ends):
            up = tie[threading[j], tread[i]]
            col = BLACK if up else (RED if weft_red[i] else WHITE)
            x, y = x0 + j * c, y0 + i * c
            d.rectangle([x, y, x + c - 1, y + c - 1], fill=col)
    d.rectangle([x0 - 1, y0 - 1, x0 + ends * c, y0 + picks * c], outline=BLACK)
    # text
    rx = tx0 + 8 * c + 10
    d.text((rx, 8), "DRAFT", font=font(INTER_B, 19), fill=BLACK)
    d.text((rx, 30), "8 shafts", font=font(MONO, 8), fill=BLACK)
    f = font(SERIF_I, 11)
    lines = ["A weave draft is a", "tiny program. Top:", "which shaft lifts", "each warp. Corner:",
             "the tie-up. Right:", "the foot's order.", "Below: what the", "loom computes.", "",
             "Anni Albers made", "pictures from this", "logic rather than", "drawing onto cloth."]
    for i, s in enumerate(lines):
        d.text((rx, 50 + i * 13), s, font=f, fill=BLACK)
    out = to_palette(img)
    colophon(ImageDraw.Draw(out), 3)
    return out


# ------------------------------------------------------------- 4 Halley
def plate_halley():
    """Orionids peak Wed 21 Oct: Earth runs through Halley's old dust."""
    S = 3
    img = Image.new("RGB", (W * S, H * S), BLACK)
    d = ImageDraw.Draw(img)
    rng = np.random.default_rng(1986)
    sx, sy, au = 112, 168, 62  # sun position, px per AU (1x)

    def P(x, y):
        return (x * S, y * S)

    # Earth orbit (dotted white)
    for k in range(180):
        a = 2 * math.pi * k / 180
        x, y = sx + au * math.cos(a), sy + au * math.sin(a)
        d.ellipse([*P(x - .6, y - .6), *P(x + .6, y + .6)], fill=WHITE)
    # Halley: a=17.83, e=0.967, perihelion pointing left, tilted a little
    a_, e = 17.83, 0.967
    p = a_ * (1 - e * e)
    tilt = math.radians(200)

    def orb(nu, off=0.0):
        r = p / (1 + e * math.cos(nu)) * (1 + off)
        ang = nu + tilt
        return sx + au * r * math.cos(ang), sy - au * r * math.sin(ang)

    pts = []
    for nu in np.linspace(-2.95, 2.95, 1500):
        x, y = orb(nu)
        if -50 < x < W + 50 and -50 < y < H + 50:
            pts.append(P(x, y))
    d.line(pts, fill=WHITE, width=2)
    # Sun
    d.ellipse([*P(sx - 6, sy - 6), *P(sx + 6, sy + 6)], fill=WHITE)
    for k in range(12):
        a = k * math.pi / 6
        d.line([P(sx + 8 * math.cos(a), sy + 8 * math.sin(a)),
                P(sx + 12 * math.cos(a), sy + 12 * math.sin(a))], fill=WHITE, width=S)
    # crossings with r = 1 AU
    nu1 = math.acos((p - 1) / e)
    img = img.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    # dust stream: scattered grains along the orbit, drawn at 1x so they survive
    for _ in range(2600):
        nu = rng.uniform(-2.9, 2.9)
        x, y = orb(nu, rng.normal(0, 0.03))
        x += rng.normal(0, 2.2)
        y += rng.normal(0, 2.2)
        if 0 <= x < W and 0 <= y < H and img.getpixel((int(x), int(y)))[0] < 100:
            d.point((int(x), int(y)), fill=RED)
    cross = {}
    for nu, name in [(nu1, "oct"), (-nu1, "may")]:
        cross[name] = orb(nu)
    ox, oy = cross["oct"]
    mx, my = cross["may"]
    # Earth on the October crossing
    d.ellipse([ox - 6, oy - 6, ox + 6, oy + 6], fill=RED, outline=WHITE, width=2)
    d.ellipse([mx - 3, my - 3, mx + 3, my + 3], outline=WHITE, width=1)
    fm = font(MONO, 9)
    d.text((ox + 9, oy - 2), "EARTH · 21 OCT", font=font(MONO_B, 9), fill=RED, anchor="lm" if ox < 300 else "rm")
    d.text((mx + 8, my + 2), "η Aquariids · May", font=fm, fill=WHITE, anchor="lm")
    d.text((sx - 9, sy + 14), "SUN", font=fm, fill=WHITE)
    # title
    d.text((W - 10, 12), "ORIONIDS", font=font(INTER_B, 30), fill=WHITE, anchor="ra")
    d.text((W - 10, 46), "peak before dawn · Wed 21 Oct", font=font(MONO, 9), fill=RED, anchor="ra")
    f = font(SERIF_I, 12)
    body = ["Every streak is a crumb of", "Halley's Comet, shed on some",
            "pass centuries ago, now hitting", "the air at 66 km/s."]
    for i, s in enumerate(body):
        d.text((W - 10, 68 + i * 14), s, font=f, fill=WHITE, anchor="ra")
    d.text((W - 10, H - 30), "Halley itself: ~33 AU out, falling back.", font=fm, fill=WHITE, anchor="ra")
    d.text((W - 10, H - 18), "Next perihelion 2061.", font=fm, fill=WHITE, anchor="ra")
    out = to_palette(img)
    colophon(ImageDraw.Draw(out), 4, fg=WHITE, x=8, y=8)
    return out


# ------------------------------------------------------------- 5 Gray-Scott
def plate_reaction():
    """Gray–Scott reaction–diffusion: black worms with red skin."""
    n, m = 150, 200
    rng = np.random.default_rng(SEED)
    U = np.ones((n, m))
    V = np.zeros((n, m))
    for _ in range(26):
        y, x = rng.integers(5, n - 5), rng.integers(5, m - 5)
        r = rng.integers(2, 5)
        V[y - r:y + r, x - r:x + r] = 0.5 + rng.random() * 0.2
        U[y - r:y + r, x - r:x + r] = 0.25
    Du, Dv, Fk, kk = 0.16, 0.08, 0.035, 0.0625

    def lap(Z):
        return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)

    for _ in range(9000):
        uvv = U * V * V
        U += Du * lap(U) - uvv + Fk * (1 - U)
        V += Dv * lap(V) + uvv - (Fk + kk) * V
    im = Image.fromarray((np.clip(V / V.max(), 0, 1) * 255).astype(np.uint8), "L")
    v = np.asarray(im.resize((W, H), Image.BICUBIC), dtype=np.float64) / 255
    out = np.zeros((H, W, 3), np.uint8) + 255
    out[v > 0.30] = RED
    out[v > 0.48] = BLACK
    img = Image.fromarray(out, "RGB")
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 18, W, H], fill=WHITE)
    d.line([(0, H - 18), (W, H - 18)], fill=BLACK)
    d.text((8, H - 14), f"GRAY–SCOTT  F .035  k .0625  ·  9000 steps  ·  seed {SEED}",
           font=font(MONO, 8), fill=BLACK)
    out = to_palette(img)
    colophon(ImageDraw.Draw(out), 5, y=H - 14)
    return out


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    plates = [plate_helicorder, plate_lunar_x, plate_weave, plate_halley, plate_reaction]
    for i, fn in enumerate(plates, 1):
        im = fn()
        assert im.size == (W, H)
        im.save(os.path.join(outdir, f"{i}.png"), optimize=True)
        print("wrote", i, fn.__name__)


if __name__ == "__main__":
    main()
