#!/usr/bin/env python3
"""Five plates for 2026-10-05 — a black/white/red 400x300 e-ink panel.

Style rules (see memory-fable-5-1.md): no dithering, ever. Everything is
line, hatch, dot or flat fill. Drawn at 4x, downscaled, then snapped to the
nearest of the three inks. Red is reserved for the one thing that happens.
"""

import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 4
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
DATE = "2026·10·05"
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_pal = Image.new("P", (1, 1))
_pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)


LATE = []   # small text, drawn at 1x without antialiasing so it stays crisp


class Small:
    def __init__(self, path, px):
        self.font = ImageFont.truetype(path, px)


def F(path, px):
    return Small(path, px) if px < 12 else ImageFont.truetype(path, px * S)


class Draw(ImageDraw.ImageDraw):
    def text(self, xy, t, font=None, fill=None, **kw):
        if isinstance(font, Small):
            LATE.append(((round(xy[0] / S), round(xy[1] / S)), t, font.font, fill))
        else:
            super().text(xy, t, font=font, fill=fill, **kw)

    def textlength(self, t, font=None, **kw):
        if isinstance(font, Small):
            return font.font.getlength(t) * S
        return super().textlength(t, font=font, **kw)


ImageDraw.Draw = lambda im, mode=None: Draw(im, mode)


def canvas(bg):
    img = Image.new("RGB", (W * S, H * S), bg)
    return img, ImageDraw.Draw(img)


def finish(img, name):
    small = img.resize((W, H), Image.LANCZOS)
    small = small.quantize(palette=_pal, dither=Image.Dither.NONE).convert("RGB")
    d = ImageDraw.ImageDraw(small)
    d.fontmode = "1"
    for xy, t, f, fill in LATE:
        d.text(xy, t, font=f, fill=fill)
    LATE.clear()
    out = small.quantize(palette=_pal, dither=Image.Dither.NONE)
    out.save(os.path.join(OUT, name), optimize=True)


def plate_mark(d, n, ink):
    """Signature: tiny plate number, bottom-right."""
    f = F(MONO, 7)
    t = f"F·{n}  {DATE}"
    w = d.textlength(t, font=f)
    d.text((W * S - w - 6 * S, H * S - 12 * S), t, font=f, fill=ink)


def P(*xy):
    return [v * S for v in xy]


# ------------------------------------------------------------ 1. Occultation
def plate1_occultation():
    """Jupiter slips behind a 20% waning crescent, 6 Oct 2026."""
    img, d = canvas(BLACK)
    cx, cy, R = 232, 150, 112
    # sun direction: lit limb faces east (left), slightly down (dawn sky)
    phase_k = 0.20                      # illuminated fraction
    ang = math.radians(200)
    sx, sy = math.cos(ang), -math.sin(ang)
    # terminator: sun elevation such that lit fraction = k  -> cos(i) = 2k-1
    cosi = 2 * phase_k - 1
    sini = math.sqrt(1 - cosi * cosi)
    # light vector in (x right, y down, z toward viewer)
    L = np.array([sx * sini, sy * sini, cosi])
    # engraving: horizontal-ish hatch lines, spacing 3 px at 1x; line kept
    # wherever the surface is lit enough; thickness grows with brightness
    gap = 3.0
    yy = np.arange((cy - R) * S, (cy + R) * S)
    xx = np.arange((cx - R) * S, (cx + R) * S)
    X, Y = np.meshgrid(xx, yy)
    nx = (X / S - cx) / R
    ny = (Y / S - cy) / R
    rr = nx * nx + ny * ny
    inside = rr <= 1
    nz = np.sqrt(np.clip(1 - rr, 0, 1))
    b = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    # curve the hatch with the sphere (lines follow latitude-ish bulge)
    v = (Y / S + 6 * nz * np.sign(ny + 1e-9) * 0) / gap + 0.9 * nz * 3
    frac = np.abs((v % 1) - 0.5)        # 0 at line centre .. 0.5 between
    width = 0.08 + 0.42 * b ** 0.6
    hatch = (frac < width) & (b > 0.02) & inside
    # earthshine: sparse stipple on the dark side
    rng = np.random.default_rng(20261006)
    stip = (rng.random(X.shape) < 0.004) & inside & (b <= 0.02)
    arr = np.array(img)
    sub = arr[(cy - R) * S:(cy + R) * S, (cx - R) * S:(cx + R) * S]
    sub[hatch] = WHITE
    sub[stip] = (150, 150, 150)
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img)
    # thin limb circle on the dark side, dotted
    for t in range(0, 360, 4):
        a = math.radians(t)
        px, py = cx + R * math.cos(a), cy + R * math.sin(a)
        nxl, nyl = math.cos(a), math.sin(a)
        if nxl * L[0] + nyl * L[1] < 0.05:
            d.ellipse(P(px - .7, py - .7, px + .7, py + .7), fill=WHITE)

    # Jupiter's track relative to the moon: enters bright limb (left), exits dark limb
    jy = 128
    xs_in = [22, 52, 82, 112]
    for i, jx in enumerate(xs_in):
        r = 7
        d.ellipse(P(jx - r, jy - r, jx + r, jy + r), fill=RED)
        for by in (-3, 2):
            d.line(P(jx - r + 1.5, jy + by, jx + r - 1.5, jy + by), fill=BLACK, width=int(1.1 * S))
    # path behind the disc
    x_enter = cx - math.sqrt(R * R - (jy - cy) ** 2)
    x_exit = cx + math.sqrt(R * R - (jy - cy) ** 2)
    x = x_enter + 4
    while x < x_exit - 4:
        d.line(P(x, jy, x + 3, jy), fill=RED, width=S)
        x += 8
    # reappearance: ghost outline at dark limb
    gx = x_exit + 14
    d.ellipse(P(gx - 7, jy - 7, gx + 7, jy + 7), outline=RED, width=int(1.3 * S))
    # tiny moons of Jupiter trailing along
    for jx in xs_in:
        for off in (-17, 13):
            d.ellipse(P(jx + off - .9, jy - .9, jx + off + .9, jy + .9), fill=WHITE)

    f = F(MONO_B, 11)
    d.text(P(14, 14), "OCCULTATION", font=f, fill=WHITE)
    fs = F(MONO, 8)
    d.text(P(14, 30), "the Moon swallows Jupiter", font=fs, fill=WHITE)
    d.text(P(14, 160), "in at the", font=fs, fill=WHITE)
    d.text(P(14, 170), "bright limb", font=fs, fill=WHITE)
    d.text(P(14, 242), "6 OCT 2026", font=F(MONO_B, 9), fill=RED)
    d.text(P(14, 254), "08:13–12:17 GMT", font=fs, fill=WHITE)
    d.text(P(14, 264), "moon 20% lit, waning", font=fs, fill=WHITE)
    d.text(P(14, 274), "Americas · Africa", font=fs, fill=WHITE)
    d.text(P(gx - 6, jy + 12), "out", font=fs, fill=RED)
    plate_mark(d, 1, WHITE)
    finish(img, "1.png")


# ------------------------------------------------------- 2. Draft notation
def plate2_draft():
    """A weaving draft (threading x tie-up x treadling = drawdown), after Anni Albers."""
    img, d = canvas(WHITE)
    rng = random.Random(1899 + 1005)   # Albers b. 1899
    shafts = 8
    cols, rows, c = 52, 33, 5
    # threading: a wandering point-twill (walk up and down the shafts)
    thr, s, step = [], 0, 1
    for _ in range(cols):
        thr.append(s)
        if rng.random() < 0.18:
            step = -step
        s = (s + step) % shafts
    # treadling: a different walk, with occasional repeats
    trd, s, step = [], 3, 1
    for _ in range(rows):
        trd.append(s)
        if rng.random() < 0.25:
            step = -step
        if rng.random() > 0.12:
            s = (s + step) % shafts
    # tie-up: broken 3/1/1/3 twill
    base = [1, 1, 1, 0, 1, 0, 0, 0]
    tie = [[base[(sh - tr) % shafts] for tr in range(shafts)] for sh in range(shafts)]

    x0, y0 = 14, 80           # drawdown origin
    tx0, ty0 = x0, y0 - 6 - shafts * c       # threading
    rx0 = x0 + cols * c + 6                  # treadling / tie-up column
    ink = BLACK

    def cell(x, y, fill, outline=BLACK):
        d.rectangle(P(x, y, x + c, y + c), fill=fill, outline=outline, width=1)

    # threading grid
    for i in range(cols):
        for sh in range(shafts):
            cell(tx0 + i * c, ty0 + (shafts - 1 - sh) * c, BLACK if thr[i] == sh else WHITE)
    # tie-up
    for tr in range(shafts):
        for sh in range(shafts):
            cell(rx0 + tr * c, ty0 + (shafts - 1 - sh) * c, RED if tie[sh][tr] else WHITE)
    # treadling
    for j in range(rows):
        for tr in range(shafts):
            cell(rx0 + tr * c, y0 + j * c, BLACK if trd[j] == tr else WHITE)
    # drawdown: warp (red) shows where its shaft is lifted by the pressed treadle
    for j in range(rows):
        for i in range(cols):
            up = tie[thr[i]][trd[j]]
            x, y = x0 + i * c, y0 + j * c
            if up:
                d.rectangle(P(x, y, x + c, y + c), fill=RED)
            else:
                d.rectangle(P(x, y, x + c, y + c), fill=BLACK)
    d.rectangle(P(x0, y0, x0 + cols * c, y0 + rows * c), outline=BLACK, width=S)

    f = F(SERIF_I, 13)
    d.text(P(rx0, y0 + rows * c + 6), "draft", font=f, fill=BLACK)
    d.text(P(rx0, y0 + rows * c + 20), "notation", font=f, fill=BLACK)
    fs = F(MONO, 7)
    d.text(P(14, 12), "THREADING x TIE-UP x TREADLING = CLOTH", font=F(MONO_B, 8), fill=BLACK)
    d.text(P(14, 23), "a score for cloth — after Anni Albers, On Weaving, 1965", font=fs, fill=BLACK)
    yb = y0 + rows * c + 8
    d.text(P(14, yb), "8 shafts · 8 treadles · red = warp lifted", font=fs, fill=BLACK)
    d.text(P(14, yb + 10), "seed 1899 (her birth year) + today", font=fs, fill=BLACK)
    plate_mark(d, 2, BLACK)
    finish(img, "2.png")


# --------------------------------------------------------------- 3. Draconids
DRACO = {
    "beta": (17.507, 52.30), "gamma": (17.943, 51.49), "xi": (17.892, 56.87),
    "nu": (17.537, 55.18), "delta": (19.209, 67.66), "eps": (19.803, 70.27),
    "chi": (18.351, 72.73), "phi": (18.346, 71.34), "zeta": (17.146, 65.71),
    "eta": (16.400, 61.51), "theta": (16.031, 58.56), "iota": (15.415, 58.97),
    "alpha": (14.073, 64.38), "kappa": (12.558, 69.79), "lambda": (11.523, 69.33),
}
DRACO_MAG = {"gamma": 2.2, "beta": 2.8, "eta": 2.7, "delta": 3.1, "zeta": 3.2,
             "iota": 3.3, "chi": 3.6, "alpha": 3.7, "xi": 3.8, "kappa": 3.9,
             "lambda": 3.8, "eps": 3.8, "theta": 4.0, "phi": 4.2, "nu": 4.9}
OTHERS = {"Vega": ((18.615, 38.78), 0.0), "Polaris": ((2.53, 89.26), 2.0),
          "Kochab": ((14.845, 74.16), 2.1), "Deneb": ((20.69, 45.28), 1.25)}


def plate3_draconids():
    img, d = canvas(WHITE)
    ra0, de0 = math.radians(17.0 * 15), math.radians(62)

    def proj(ra_h, dec):
        a, dd = math.radians(ra_h * 15), math.radians(dec)
        k = 2 / (1 + math.sin(de0) * math.sin(dd) + math.cos(de0) * math.cos(dd) * math.cos(a - ra0))
        x = k * math.cos(dd) * math.sin(a - ra0)
        y = k * (math.cos(de0) * math.sin(dd) - math.sin(de0) * math.cos(dd) * math.cos(a - ra0))
        return 205 - x * 330, 160 - y * 330    # east to the left

    # chart frame with RA/Dec graticule (light dashed)
    grat = [[proj(h / 20, dec) for h in range(0, 481)] for dec in (40, 50, 60, 70, 80)]
    grat += [[proj(h, dec / 4) for dec in range(120, 360)] for h in range(0, 24, 2)]
    for line in grat:
        acc, last = 0.0, None
        for p in line:
            if last is not None:
                acc += math.dist(p, last)
            last = p
            if acc >= 5 and 0 < p[0] < W and 0 < p[1] < H:
                acc = 0
                d.ellipse(P(p[0] - .55, p[1] - .55, p[0] + .55, p[1] + .55), fill=BLACK)

    # radiant
    rx, ry = proj(17.47, 54.0)
    # meteors: streaks radially outward, beginning well away from radiant
    rng = random.Random(21)  # 21P/Giacobini-Zinner
    for k in range(44):
        th = rng.uniform(0, 2 * math.pi)
        r1 = rng.uniform(22, 170)
        L = rng.uniform(18, 52) * (0.6 + r1 / 150)
        x1, y1 = rx + r1 * math.cos(th), ry + r1 * math.sin(th)
        x2, y2 = rx + (r1 + L) * math.cos(th), ry + (r1 + L) * math.sin(th)
        red = k == 9
        # taper: draw as thin polygon, fat at the far end (where it burns brightest)
        wmax = 2.6 if red else rng.uniform(1.3, 2.4)
        nxp, nyp = -math.sin(th), math.cos(th)
        poly = [(x1, y1), (x2 + nxp * wmax / 2, y2 + nyp * wmax / 2),
                (x2 + math.cos(th) * wmax, y2 + math.sin(th) * wmax),
                (x2 - nxp * wmax / 2, y2 - nyp * wmax / 2)]
        if red:
            th = math.radians(-20)
            nxp, nyp = -math.sin(th), math.cos(th)
            x1, y1 = rx + 40 * math.cos(th), ry + 40 * math.sin(th)
            L = 105
            x2, y2 = rx + (40 + L) * math.cos(th), ry + (40 + L) * math.sin(th)
            poly = [(x1, y1), (x2 + nxp * 2, y2 + nyp * 2), (x2 + math.cos(th) * 4, y2 + math.sin(th) * 4),
                    (x2 - nxp * 2, y2 - nyp * 2)]
        d.polygon([v * S for p in poly for v in p], fill=RED if red else BLACK)

    # radiant marker
    for r in (5, 9):
        d.ellipse(P(rx - r, ry - r, rx + r, ry + r), outline=RED, width=int(1.2 * S))
    # constellation figure
    path = ["lambda", "kappa", "alpha", "iota", "theta", "eta", "zeta", "phi", "chi", "eps", "delta", "xi"]
    head = ["xi", "nu", "beta", "gamma", "xi"]
    for seq in (path, head):
        pts = [proj(*DRACO[s]) for s in seq]
        for p, q in zip(pts, pts[1:]):
            d.line(P(*p, *q), fill=BLACK, width=int(0.8 * S))
    for name, (ra, de) in DRACO.items():
        x, y = proj(ra, de)
        r = 4.2 - 0.7 * DRACO_MAG[name]
        r = max(r, 1.2)
        d.ellipse(P(x - r - 1.4, y - r - 1.4, x + r + 1.4, y + r + 1.4), fill=WHITE)
        d.ellipse(P(x - r, y - r, x + r, y + r), fill=BLACK)
    fs = F(MONO, 7)
    for name, ((ra, de), mag) in OTHERS.items():
        x, y = proj(ra, de)
        in_box = (x < 175 and y > 245) or (x < 155 and y < 70)
        if 6 < x < W - 6 and 6 < y < H - 6 and not in_box:
            r = 4.2 - 0.7 * mag
            d.ellipse(P(x - r, y - r, x + r, y + r), fill=BLACK)
            d.text(P(x + r + 2, y - 4), name, font=fs, fill=BLACK)
    x, y = proj(*DRACO["gamma"])
    d.text(P(x + 4, y + 2), "Eltanin", font=fs, fill=BLACK)
    x, y = proj(*DRACO["alpha"])
    d.text(P(x + 4, y + 2), "Thuban", font=fs, fill=BLACK)

    # cartouche
    d.rectangle(P(10, 10, 150, 64), fill=WHITE, outline=BLACK, width=S)
    d.text(P(16, 13), "Draconids", font=F(SERIF_B, 20), fill=BLACK)
    d.text(P(16, 37), "peak 8–9 Oct · look at dusk", font=fs, fill=BLACK)
    d.text(P(16, 47), "dust of comet 21P/G–Z", font=fs, fill=RED)
    d.rectangle(P(10, 254, 168, 290), fill=WHITE, outline=BLACK, width=S)
    d.text(P(16, 258), "storms: 1933 · 1946", font=fs, fill=BLACK)
    d.text(P(16, 268), "new moon 10 Oct: dark skies", font=fs, fill=BLACK)
    d.text(P(16, 278), "◎ radiant  RA 17h28 +54°", font=fs, fill=RED)
    plate_mark(d, 3, BLACK)
    finish(img, "3.png")


# ------------------------------------------------------------- 4. Goddard
def plate4_goddard():
    """Robert H. Goddard, b. 5 Oct 1882. First liquid-fuel flight: 41 ft, 184 ft, 2.5 s."""
    img, d = canvas(WHITE)
    ground = 262
    x_launch, ft = 74, 1.45         # px per foot
    x_land = x_launch + 184 * ft
    apex_h = 41 * ft
    lw = int(0.9 * S)

    # ground hatching
    d.line(P(8, ground, W - 8, ground), fill=BLACK, width=int(1.4 * S))
    for x in range(10, W - 8, 6):
        d.line(P(x, ground + 1, x - 5, ground + 6), fill=BLACK, width=lw)

    # trajectory: rises, arcs over, dives into the cabbages (asymmetric)
    pts = []
    for i in range(121):
        t = i / 120
        x = x_launch + (x_land - x_launch) * t
        # skewed hump peaking at t~0.35
        h = apex_h * (math.sin(math.pi * t ** 0.72)) ** 1.0
        pts.append((x, ground - h))
    for i in range(0, 120, 3):
        d.line(P(*pts[i], *pts[i + 2]), fill=RED, width=int(1.6 * S))
    # time ticks every 0.5 s along the path (approx even in t)
    fs = F(MONO, 7)
    for k in range(1, 5):
        i = int(k / 5 * 120)
        x, y = pts[i]
        d.ellipse(P(x - 2, y - 2, x + 2, y + 2), fill=BLACK)
        d.text(P(x - 6, y - 13), f"{k * 0.5:.1f}s", font=fs, fill=BLACK)
    # apex dimension
    ia = max(range(121), key=lambda i: -pts[i][1])
    ax, ay = pts[ia]
    d.line(P(ax, ay, ax, ground), fill=BLACK, width=lw)
    for yy, s_ in ((ay, 1), (ground, -1)):
        d.polygon(P(ax, yy, ax - 2.5, yy + 6 * s_, ax + 2.5, yy + 6 * s_), fill=BLACK)
    d.text(P(ax + 4, (ay + ground) / 2 - 5), "41 ft", font=F(MONO_B, 8), fill=BLACK)
    # range dimension
    yd = ground + 14
    d.line(P(x_launch, yd, x_land, yd), fill=BLACK, width=lw)
    for xx, s_ in ((x_launch, 1), (x_land, -1)):
        d.polygon(P(xx, yd, xx + 6 * s_, yd - 2.5, xx + 6 * s_, yd + 2.5), fill=BLACK)
        d.line(P(xx, ground + 8, xx, yd + 4), fill=BLACK, width=lw)
    tw = d.textlength("184 ft", font=F(MONO_B, 8)) / S
    mid = (x_launch + x_land) / 2
    d.rectangle(P(mid - tw / 2 - 3, yd - 5, mid + tw / 2 + 3, yd + 6), fill=WHITE)
    d.text(P(mid - tw / 2, yd - 5), "184 ft", font=F(MONO_B, 8), fill=BLACK)

    # launch frame (A-frame of pipe) at x_launch
    fx = x_launch
    d.line(P(fx - 9, ground, fx - 2, ground - 40), fill=BLACK, width=lw)
    d.line(P(fx + 9, ground, fx + 2, ground - 40), fill=BLACK, width=lw)
    d.line(P(fx - 6, ground - 18, fx + 6, ground - 18), fill=BLACK, width=lw)

    # cabbages at landing
    rng = random.Random(1926)
    for k in range(9):
        cxp = x_land - 30 + k * 7 + rng.uniform(-1, 1)
        r = rng.uniform(3, 4.2)
        d.ellipse(P(cxp - r, ground - 2 * r, cxp + r, ground), outline=BLACK, width=lw, fill=WHITE)
        d.arc(P(cxp - r * .6, ground - 1.6 * r, cxp + r * .6, ground - .3 * r), 200, 340, fill=BLACK, width=lw)
    d.text(P(x_land - 4, ground - 20), "cabbages", font=fs, fill=BLACK)

    # 'Nell' detail, top-left: motor ON TOP, tanks below, fed by two long pipes
    ox, oy, k = 36, 34, 1.0
    # nozzle + chamber
    d.ellipse(P(ox - 5, oy, ox + 5, oy + 10), outline=BLACK, width=lw)
    d.polygon(P(ox - 2, oy + 10, ox + 2, oy + 10, ox + 5, oy + 22, ox - 5, oy + 22), outline=BLACK, width=lw)
    # flame (red), pointing down toward the tanks
    d.polygon(P(ox - 4, oy + 22, ox + 4, oy + 22, ox + 1.5, oy + 44, ox, oy + 52, ox - 1.5, oy + 44), fill=RED)
    # pipes
    d.line(P(ox - 5, oy + 5, ox - 10, oy + 14), fill=BLACK, width=lw)
    d.line(P(ox + 5, oy + 5, ox + 10, oy + 14), fill=BLACK, width=lw)
    d.line(P(ox - 10, oy + 14, ox - 10, oy + 96), fill=BLACK, width=lw)
    d.line(P(ox + 10, oy + 14, ox + 10, oy + 96), fill=BLACK, width=lw)
    # conical shield over the tanks
    d.polygon(P(ox, oy + 58, ox - 8, oy + 70, ox + 8, oy + 70), outline=BLACK, width=lw)
    # tanks
    d.rounded_rectangle(P(ox - 6, oy + 70, ox + 6, oy + 92), radius=3 * S, outline=BLACK, width=lw)
    d.rounded_rectangle(P(ox - 6, oy + 94, ox + 6, oy + 116), radius=3 * S, outline=BLACK, width=lw)
    d.text(P(ox + 14, oy + 2), "motor", font=fs, fill=BLACK)
    d.text(P(ox + 14, oy + 76), "LOX", font=fs, fill=BLACK)
    d.text(P(ox + 14, oy + 100), "gasoline", font=fs, fill=BLACK)
    d.text(P(ox - 22, oy + 122), "'Nell', 10 ft", font=fs, fill=BLACK)

    # title block
    d.text(P(150, 18), "2.5 seconds", font=F(SERIF_B, 26), fill=BLACK)
    d.text(P(152, 50), "first liquid-fuelled rocket flight", font=fs, fill=BLACK)
    d.text(P(152, 60), "Auburn, Mass. · 16 March 1926 · ~60 mph", font=fs, fill=BLACK)
    d.text(P(152, 74), "R. H. GODDARD  b. 5 OCT 1882", font=F(MONO_B, 8), fill=RED)
    plate_mark(d, 4, BLACK)
    finish(img, "4.png")


# --------------------------------------------------------------- 5. Azulejo
def plate5_azulejo():
    """Portugal became a republic on 5 Oct 1910. A padrão of 4x3 tiles; one missing."""
    N = 100 * S
    rng = random.Random(1910)
    yy, xx = np.mgrid[0:N, 0:N] / N           # tile coords 0..1
    u, v = np.abs(xx - 0.5), np.abs(yy - 0.5)  # fold to quadrant (centre at 0)
    a, b = np.maximum(u, v), np.minimum(u, v)  # fold to octant
    r = np.hypot(u, v)
    th = np.arctan2(v, u)
    # corner coordinates (distance from tile corner -> forms circles across 4 tiles)
    cu, cv = 0.5 - u, 0.5 - v
    rc = np.hypot(cu, cv)
    thc = np.arctan2(cv, cu)
    # edge midpoint coordinates
    em = np.hypot(0.5 - a, b)

    n_pet = rng.choice([8, 8, 12])
    rosette = r < 0.13 + 0.07 * np.abs(np.cos(n_pet / 2 * th))
    eye = r < 0.045
    corner_lobes = rc < 0.20 + 0.06 * np.cos(8 * thc)
    corner_hole = rc < 0.10
    corner_dot = rc < 0.045
    edge_leaf = em < 0.11
    edge_core = em < 0.05
    # diagonal tendrils: band along the diagonal between rosette and corner
    diag = (np.abs(u - v) < 0.035) & (r > 0.24) & (rc > 0.25)
    # ring
    ring = np.abs(r - 0.33) < 0.018

    red = (rosette & ~eye) | (corner_lobes & ~corner_hole) | corner_dot | (edge_leaf & ~edge_core) | diag
    black = ring | eye

    def outline(mask):
        m = mask
        e = np.zeros_like(m)
        k = 2 * S // 2
        for dx, dy in ((k, 0), (-k, 0), (0, k), (0, -k)):
            e |= np.roll(np.roll(m, dx, 1), dy, 0) != m
        return e

    tile = np.full((N, N, 3), 255, np.uint8)
    tile[red] = RED
    tile[outline(red)] = BLACK
    tile[black] = BLACK

    img = np.full((H * S, W * S, 3), 255, np.uint8)
    missing = (2, 1)
    for ty in range(3):
        for tx in range(4):
            y0, x0 = ty * N, tx * N
            if (tx, ty) == missing:
                img[y0:y0 + N, x0:x0 + N] = BLACK
                continue
            img[y0:y0 + N, x0:x0 + N] = tile
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    # grout lines
    for k in range(1, 4):
        d.line(P(k * 100, 0, k * 100, 300), fill=WHITE, width=int(1.5 * S))
    for k in range(1, 3):
        d.line(P(0, k * 100, 400, k * 100), fill=WHITE, width=int(1.5 * S))
    # inside the missing tile: the date, as if scratched into the mortar
    mx, my = missing[0] * 100, missing[1] * 100
    d.text(P(mx + 12, my + 18), "5·X·1910", font=F(MONO_B, 13), fill=WHITE)
    d.text(P(mx + 12, my + 42), "República", font=F(SERIF_I, 16), fill=RED)
    d.text(P(mx + 12, my + 64), "Portugal", font=F(MONO, 8), fill=WHITE)
    d.text(P(mx + 12, my + 76), "azulejo, in red", font=F(MONO, 7), fill=WHITE)
    d.rectangle(P(W - 86, H - 14, W, H), fill=WHITE)
    plate_mark(d, 5, BLACK)
    finish(im, "5.png")


if __name__ == "__main__":
    plate1_occultation()
    plate2_draft()
    plate3_draconids()
    plate4_goddard()
    plate5_azulejo()
