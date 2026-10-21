#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-21.

Theme of the day: messages in code. Things that only mean something once
you know how to read them; the red is the part that changes the reading.
  1. England Expects — Nelson's Trafalgar signal as twelve flag hoists (21 Oct 1805)
  2. XI M V — St Ursula's feast; one letter read as a thousand
  3. Guggenheim — Wright's spiral, opened 21 Oct 1959; the red is the walk down
  4. Halley — the comet is out past Neptune, its dust arrives tonight (Orionids)
  5. Hooke's anagram — as hangs the chain, so stands the arch (inverted, in red)

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
# red/white/blue/yellow; their exact set is still argued over).
def draw_flag(d, x, y, digit, w=26, h=17):
    x1, y1 = x + w, y + h
    mx, my = x + w // 2, y + h // 2
    d.rectangle([x, y, x1, y1], fill=WHITE)
    if digit == 1:
        d.rectangle([x, y, x1, y1], fill=RED)
    elif digit == 2:
        d.rectangle([mx, y, x1, y1], fill=BLACK)
    elif digit == 3:
        t = w // 3
        d.rectangle([x, y, x + t, y1], fill=BLACK)
        d.rectangle([x1 - t, y, x1, y1], fill=RED)
    elif digit == 4:
        d.rectangle([mx - 2, y, mx + 2, y1], fill=RED)
        d.rectangle([x, my - 2, x1, my + 2], fill=RED)
    elif digit == 5:
        d.rectangle([x, y, x1, my], fill=RED)
    elif digit == 6:
        d.rectangle([mx - 5, my - 4, mx + 5, my + 4], fill=BLACK)
    elif digit == 7:
        d.polygon([(x, y), (x1, y), (x, y1)], fill=BLACK)
    elif digit == 8:
        d.rectangle([x, y, mx, my], fill=BLACK)
        d.rectangle([mx, my, x1, y1], fill=BLACK)
    elif digit == 9:
        d.rectangle([x, y, x1, y1], fill=RED)
        d.rectangle([x, my - 2, x1, my + 2], fill=WHITE)
    elif digit == 0:
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=RED)
    elif digit == "T":  # telegraph flag: red over white, split on the diagonal
        d.polygon([(x, y), (x1, y), (x1, y1)], fill=RED)
    d.rectangle([x, y, x1, y1], outline=BLACK)


def image1_flags():
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    hoists = [("253", "England"), ("269", "expects"), ("863", "that"),
              ("261", "every"), ("471", "man"), ("958", "will"),
              ("220", "do"), ("370", "his"), ("4", "D"), ("21", "U"),
              ("19", "T"), ("24", "Y")]
    d.text((14, 8), "ENGLAND EXPECTS", font=font(INTER, 27), fill=BLACK)
    d.text((16, 40), "TRAFALGAR · 21 X 1805 · POPHAM'S TELEGRAPHIC CODE",
           font=font(MONO, 10), fill=BLACK)
    # telegraph flag, flown first, at the right of the title
    draw_flag(d, 356, 12, "T", 26, 17)
    d.line([(355, 6), (355, 34)], fill=BLACK)
    d.text((351, 32), "TELEG.", font=font(MONO, 8) if False else font(MONO, 10), fill=BLACK)

    fw, fh, gap = 26, 17, 3
    colw = 64
    rows = [hoists[:6], hoists[6:]]
    fword = font(INTER_B, 11)
    fnum = font(MONO, 10)
    for r, row in enumerate(rows):
        top = 66 + r * 92
        d.line([(10, top - 6), (390, top - 6)], fill=BLACK)  # the halyard yard
        for c, (num, word) in enumerate(row):
            cx = 10 + colw * c + colw // 2 + 2
            spelled = r == 1 and c >= 2
            x = cx - fw // 2
            d.line([(x - 2, top - 6), (x - 2, top + 3 * (fh + gap))], fill=BLACK)
            for k, ch in enumerate(num):
                draw_flag(d, x, top + k * (fh + gap), int(ch), fw, fh)
            ly = top + 3 * (fh + gap) + 2
            col = RED if spelled else BLACK
            ctext(d, cx, ly, num, fnum, col)
            ctext(d, cx, ly + 12, word, fword, col)
        if r == 1:
            # bracket under the spelled-out word
            bx0 = 10 + colw * 2 + 8
            bx1 = 10 + colw * 6 - 4
            by = top + 3 * (fh + gap) + 31
            d.line([(bx0, by), (bx1, by)], fill=RED)
            d.line([(bx0, by - 3), (bx0, by)], fill=RED)
            d.line([(bx1, by - 3), (bx1, by)], fill=RED)
    f = font(SERIF_I, 14)
    d.text((14, 258), "‘Confides’ was not in the book, so it became ‘expects’.",
           font=f, fill=BLACK)
    d.text((14, 276), "‘Duty’ was not in the book either. It had to be spelled.",
           font=f, fill=BLACK)
    return finalize(img)


# ---------------------------------------------------------------- 2. XI M V
def stick(d, x, y, col):
    """A 9 x 17 px Isotype figure, head at (x, y)."""
    d.ellipse([x - 3, y, x + 3, y + 6], fill=col)
    d.polygon([(x - 4, y + 8), (x + 4, y + 8), (x + 5, y + 18), (x - 5, y + 18)], fill=col)


def image2_ursula():
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    big = font(INTER, 92)
    parts = [("XI", BLACK), ("·", BLACK), ("M", RED), ("·", BLACK), ("V", BLACK)]
    sp = 10
    total = sum(text_w(d, t, big) for t, _ in parts) + sp * (len(parts) - 1)
    x = (W - total) / 2
    for t, col in parts:
        bb = d.textbbox((0, 0), t, font=big)
        d.text((x - bb[0], -8), t, font=big, fill=col)
        x += text_w(d, t, big) + sp
    d.line([(14, 104), (386, 104)], fill=BLACK)

    fm = font(MONO, 10)
    fi = font(SERIF_I, 13)
    # left reading: eleven
    d.text((14, 112), "M = martyres", font=fm, fill=BLACK)
    d.text((14, 126), "eleven virgin martyrs", font=fi, fill=BLACK)
    for k in range(11):
        stick(d, 20 + k * 13 + (6 if k >= 5 else 0), 182, BLACK)
    d.text((14, 210), "11", font=font(INTER, 24), fill=BLACK)

    # right reading: eleven thousand, one pixel each
    d.text((186, 112), "M = milia", font=fm, fill=RED)
    d.text((186, 126), "eleven thousand virgins", font=fi, fill=RED)
    gx, gy = 186, 144
    a = np.asarray(img).copy()
    n = 0
    for j in range(110):
        for i in range(100):
            a[gy + j, gx + 2 * i + (j % 2)] = RED
            n += 1
    assert n == 11000
    img = Image.fromarray(a)
    d = crisp(img)
    f13 = font(INTER, 15)
    d.text((gx + 200 - text_w(d, "11 000", f13), gy + 112), "11 000", font=f13, fill=RED)
    d.text((gx, gy + 114), "one red pixel each", font=fm, fill=RED)

    d.line([(14, 272), (386, 272)], fill=BLACK)
    d.text((14, 277), "St Ursula, 21 October. One letter, read as a thousand — so one theory goes.",
           font=font(SERIF_I, 12), fill=BLACK)
    return finalize(img)


# --------------------------------------------------------- 3. Guggenheim
def image3_guggenheim():
    S = 3
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    cx = 128 * S
    ground = 262 * S
    levels = 6
    band = 30 * S
    r_bot = 62 * S
    r_top = 108 * S
    # bands of the inverted ziggurat, each one wider and set slightly back
    rs = [r_bot + (r_top - r_bot) * k / (levels - 1) for k in range(levels)]
    for k in range(levels):
        y1 = ground - k * band
        y0 = y1 - band
        r = rs[k]
        # parapet band leaning out: bottom narrower than top
        rb = r - 4 * S
        d.polygon([(cx - rb, y1), (cx + rb, y1), (cx + r, y0 + 8 * S), (cx - r, y0 + 8 * S)],
                  fill=WHITE, outline=BLACK, width=S * 2)
        d.rectangle([cx - r, y0 + 2 * S, cx + r, y0 + 8 * S], fill=BLACK)
        # thin window slot under each parapet
    top_y = ground - levels * band
    # glass dome: shallow, with radial ribs
    dome_r = rs[-1] * 0.62
    d.chord([cx - dome_r, top_y - 26 * S, cx + dome_r, top_y + 22 * S], 180, 360,
            fill=WHITE, outline=BLACK, width=S * 2)
    for k in range(1, 12):
        a = math.pi + math.pi * k / 12
        d.line([(cx, top_y - 2 * S),
                (cx + dome_r * math.cos(a), top_y - 2 * S + 24 * S * math.sin(a))],
               fill=BLACK, width=S)
    d.line([(10 * S, ground), (246 * S, ground)], fill=BLACK, width=S * 2)

    # the walk down: a red helix inside the drum, front strokes solid, back dashed
    turns = levels - 0.5
    N = 2000
    front, back = [], []
    for i in range(N + 1):
        u = i / N
        t = 2 * math.pi * turns * u
        z = ground - 6 * S - u * (levels * band - 18 * S)
        rr = (r_bot + (r_top - r_bot) * u) * 0.72
        x = cx + rr * math.sin(t)
        y = z - 10 * S * math.cos(t)
        (front if math.cos(t) < 0 else back).append((i, x, y))
    img = snap(big)
    d1 = crisp(img)

    def runs(pts):
        out, cur, last = [], [], None
        for i, x, y in pts:
            if last is not None and i != last + 1:
                out.append(cur)
                cur = []
            cur.append((x / S, y / S))
            last = i
        if cur:
            out.append(cur)
        return out

    for seg in runs(back):
        if len(seg) > 1:
            dashed_poly(d1, seg, 3, 3, RED, 1)
    for seg in runs(front):
        if len(seg) > 1:
            d1.line(seg, fill=RED, width=3)
    # arrow at the bottom end, pointing down the slope
    path = sorted(front + back)
    (_, x0, y0), (_, x1, y1) = path[12], path[0]
    ex, ey = x1 / S, y1 / S
    ang = math.atan2(y1 - y0, x1 - x0)
    tip = (ex + 7 * math.cos(ang), ey + 7 * math.sin(ang))
    l = (ex + 5 * math.cos(ang + 2.2), ey + 5 * math.sin(ang + 2.2))
    r_ = (ex + 5 * math.cos(ang - 2.2), ey + 5 * math.sin(ang - 2.2))
    d1.polygon([tip, l, r_], fill=RED)

    d1.text((256, 18), "THE", font=font(INTER, 15), fill=BLACK)
    d1.text((256, 32), "LONG", font=font(INTER, 30), fill=BLACK)
    d1.text((256, 62), "WAY", font=font(INTER, 30), fill=BLACK)
    d1.text((256, 92), "DOWN", font=font(INTER, 30), fill=RED)
    fm = font(MONO, 10)
    for k, line in enumerate(["Solomon R. Guggenheim", "Museum, Fifth Avenue",
                              "opened 21 X 1959", "Wright d. 9 IV 1959",
                              "ramp ≈ ¼ mile"]):
        d1.text((257, 134 + k * 13), line, font=fm, fill=BLACK)
    fi = font(SERIF_I, 13)
    for k, line in enumerate(["Wright meant you to", "ride to the top and", "let the floor carry",
                              "you down. He died six", "months before anyone", "could."]):
        d1.text((257, 206 + k * 15), line, font=fi, fill=BLACK)
    return finalize(img)


# ---------------------------------------------------------------- 4. Halley
def halley_orbit():
    a, e = 17.834, 0.96714
    i, node, w = map(math.radians, (162.26, 58.42, 111.33))
    T_peri = 1986.109

    def xyz(nu):
        r = a * (1 - e * e) / (1 + e * math.cos(nu))
        u = w + nu
        x = r * (math.cos(node) * math.cos(u) - math.sin(node) * math.sin(u) * math.cos(i))
        y = r * (math.sin(node) * math.cos(u) + math.cos(node) * math.sin(u) * math.cos(i))
        z = r * math.sin(u) * math.sin(i)
        return x, y, z, r

    # where is it now? (2026-10-21)
    t = 2026 + (294 - 0.5) / 365.25
    P = a ** 1.5
    M = 2 * math.pi * ((t - T_peri) / P % 1.0)
    E = M if e < 0.8 else math.pi
    for _ in range(100):
        E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    nu = 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2), math.sqrt(1 - e) * math.cos(E / 2))
    return xyz, nu


def image4_halley():
    xyz, nu_now = halley_orbit()
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    cxn, cyn, rnow = xyz(nu_now)[0], xyz(nu_now)[1], xyz(nu_now)[3]
    # earth today: heliocentric longitude = sun's longitude + 180
    lam_e = math.radians((208.0 + 180.0) % 360)
    ex, ey = math.cos(lam_e), math.sin(lam_e)

    # orient so the aphelion points left: rotate by angle of aphelion
    ap = xyz(math.pi)
    rot = math.pi - math.atan2(ap[1], ap[0])
    def R(x, y):
        return (x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot))

    sc = 9.6
    sx, sy = 352, 150

    def P(x, y):
        X, Y = R(x, y)
        return sx + X * sc, sy - Y * sc

    # planets, faint dashes
    for au, name in [(5.20, "J"), (9.54, "S"), (19.19, "U"), (30.07, "N")]:
        pts = [P(au * math.cos(k / 200 * 2 * math.pi), au * math.sin(k / 200 * 2 * math.pi))
               for k in range(201)]
        pts = [(x, y) for x, y in pts]
        dashed_poly(d, pts, 2, 4, BLACK, 1)
    for au, name in [(19.19, "URANUS"), (30.07, "NEPTUNE")]:
        x, y = P(-au * math.cos(rot) * 0 + 0, 0)
    # orbit of Halley
    orb = [P(*xyz(-math.pi + 2 * math.pi * k / 2000)[:2]) for k in range(2001)]
    d.line(orb, fill=BLACK, width=1)
    # comet now
    qx, qy = P(cxn, cyn)
    d.ellipse([qx - 4, qy - 4, qx + 4, qy + 4], fill=BLACK)
    d.rectangle([qx - 6, qy - 34, qx + 70, qy - 8], fill=WHITE)
    d.text((qx - 4, qy - 33), f"HALLEY, NOW\n{rnow:.1f} AU", font=font(MONO, 10), fill=BLACK)
    # sun
    d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=BLACK)

    # inset: the inner system magnified around the sun
    ix, iy, ir = 300, 228, 62
    zoom = ir / 1.35
    d.line([(sx, sy), (ix - ir * 0.2, iy - ir * 0.98)], fill=BLACK)
    d.ellipse([sx - 15, sy - 15, sx + 15, sy + 15], outline=BLACK)
    d.ellipse([ix - ir, iy - ir, ix + ir, iy + ir], fill=WHITE, outline=BLACK, width=2)

    def Pi(x, y):
        X, Y = R(x, y)
        return ix + X * zoom, iy - Y * zoom

    def inside(p):
        return (p[0] - ix) ** 2 + (p[1] - iy) ** 2 < (ir - 2) ** 2

    # earth orbit
    eo = [Pi(math.cos(k / 200 * 2 * math.pi), math.sin(k / 200 * 2 * math.pi)) for k in range(201)]
    d.line(eo, fill=BLACK, width=1)
    # halley orbit near sun; dust stream thickened in red
    seg = []
    near = None
    rng = random.Random(1021)
    for k in range(4001):
        nu = -math.pi + 2 * math.pi * k / 4000
        x, y, z, r = xyz(nu)
        p = Pi(x, y)
        if inside(p):
            seg.append(p)
            dd = math.hypot(x - ex, y - ey)
            if near is None or dd < near[0]:
                near = (dd, p)
            # dust: scattered red grains along the orbit
            for _ in range(3):
                gx = p[0] + rng.gauss(0, 2.4)
                gy = p[1] + rng.gauss(0, 2.4)
                if inside((gx, gy)):
                    d.point((gx, gy), fill=RED)
        elif len(seg) > 1:
            d.line(seg, fill=BLACK)
            seg = []
    if len(seg) > 1:
        d.line(seg, fill=BLACK)
    # sun and earth in inset
    d.ellipse([ix - 3, iy - 3, ix + 3, iy + 3], fill=BLACK)
    epx, epy = Pi(ex, ey)
    d.ellipse([epx - 4, epy - 4, epx + 4, epy + 4], fill=WHITE, outline=BLACK, width=2)
    d.text((epx - 46, epy + 6), "EARTH", font=font(MONO, 10), fill=BLACK)
    d.text((ix - 12, iy + 28), "1 AU", font=font(MONO, 10), fill=BLACK)

    d.rectangle([8, 6, 220, 100], fill=WHITE)
    d.text((12, 10), "THE COMET IS", font=font(INTER, 20), fill=BLACK)
    d.text((12, 32), "OUT PAST NEPTUNE.", font=font(INTER, 20), fill=BLACK)
    d.text((12, 54), "ITS DUST ARRIVES", font=font(INTER, 20), fill=RED)
    d.text((12, 76), "TONIGHT.", font=font(INTER, 20), fill=RED)
    fm = font(MONO, 10)
    d.rectangle([8, 192, 186, 298], fill=WHITE)
    for k, line in enumerate(["ORIONIDS PEAK 21 X 2026", "~20 meteors an hour",
                              "1P/Halley: e 0.967, P 75 yr", "next perihelion 28 VII 2061"]):
        d.text((12, 196 + k * 13), line, font=fm, fill=BLACK)
    d.text((12, 262), "Earth passes through the old", font=font(SERIF_I, 13), fill=BLACK)
    d.text((12, 278), "tail. The comet will not notice.", font=font(SERIF_I, 13), fill=BLACK)
    return finalize(img), rnow, near


# ---------------------------------------------------------- 5. Hooke's chain
def hanging_chain(xa, xb, y_top, loads, n=120, sag=None):
    """Funicular polygon of a chain with uniform weight plus point loads.

    loads: list of (fraction along span, weight relative to the chain's total).
    Returns points (x, y) with y increasing downward, scaled to hit `sag`.
    """
    xs = np.linspace(xa, xb, n + 1)
    w = np.full(n + 1, 1.0 / n)
    for f, m in loads:
        w[int(round(f * n))] += m
    # vertical shear from equilibrium: moments about the left support
    # y(x) is proportional to the bending moment of a simple beam with these loads
    L = xb - xa
    Ra = sum(wi * (xb - xi) for wi, xi in zip(w, xs)) / L
    M = np.zeros(n + 1)
    for k, x in enumerate(xs):
        M[k] = Ra * (x - xa) - sum(wi * (x - xj) for wi, xj in zip(w[:k], xs[:k]))
    M = M / M.max() * sag
    return list(zip(xs, y_top + M))


def image5_hooke():
    S = 3
    mid = 150
    chains = [
        (40, 360, [(0.5, 0.0)], 112),
        (70, 330, [(0.3, 0.25), (0.7, 0.25)], 92),
        (112, 288, [(0.5, 0.45)], 72),
        (150, 250, [], 48),
    ]
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    top = 34
    # the ceiling beam the chains hang from
    d.rectangle([24 * S, (top - 4) * S, 376 * S, top * S], fill=BLACK)
    for xa, xb, loads, sag in chains:
        pts = hanging_chain(xa, xb, top, loads, sag=sag)
        # chain: small links
        d.line([(x * S, y * S) for x, y in pts], fill=BLACK, width=S)
        for k in range(0, len(pts), 4):
            x, y = pts[k]
            d.ellipse([(x - 1.2) * S, (y - 1.2) * S, (x + 1.2) * S, (y + 1.2) * S], fill=BLACK)
        for f, m in loads:
            if m > 0:
                x, y = pts[int(round(f * 120))]
                d.line([(x * S, y * S), (x * S, (y + 7) * S)], fill=BLACK, width=S)
                d.ellipse([(x - 4) * S, (y + 6) * S, (x + 4) * S, (y + 14) * S], fill=BLACK)
        # the inverted arch: voussoirs along the mirrored curve
        arch = [(x, 2 * mid - y + 2 * (top - mid) + 2 * (mid - top) + (2 * mid - 2 * top) * 0)
                for x, y in pts]
        arch = [(x, 2 * mid - y) for x, y in pts]
        thick = 9
        for k in range(0, len(arch) - 1, 5):
            k2 = min(k + 5, len(arch) - 1)
            (x0, y0), (x1, y1) = arch[k], arch[k2]
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            nx, ny = -dy / L * thick / 2, dx / L * thick / 2
            poly = [(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)]
            d.polygon([(px * S, py * S) for px, py in poly], fill=RED, outline=WHITE, width=S)
    ground = 2 * mid - top
    d.rectangle([24 * S, ground * S, 376 * S, (ground + 4) * S], fill=BLACK)
    img = snap(big)
    d = crisp(img)
    # the mirror line
    dashed_poly(d, [(14, mid), (386, mid)], 2, 5, BLACK)
    fm = font(MONO, 10)
    s = "ut pendet continuum flexile sic stabit contiguum rigidum inuersum".replace(" ", "")
    ana = "".join(sorted(s))
    ctext(d, W / 2, 6, ana, fm, BLACK)
    ctext(d, W / 2, 274, "Ut pendet continuum flexile, sic stabit contiguum rigidum inversum.",
          font(SERIF_I, 12), BLACK)
    ctext(d, W / 2, 287, "As hangs the flexible line, so, inverted, stands the rigid arch.",
          font(SERIF_I, 11), RED)
    d.text((14, mid - 13), "R. HOOKE, 1676", font=fm, fill=BLACK)
    d.text((386 - text_w(d, "(ANAGRAM, ABOVE)", fm), mid + 3), "(ANAGRAM, ABOVE)", font=fm, fill=BLACK)
    return finalize(img)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    ims = [image1_flags(), image2_ursula(), image3_guggenheim()]
    h, rnow, near = image4_halley()
    print("halley r now", rnow, "min dist to earth-today in inset", near[0])
    ims += [h, image5_hooke()]
    for i, im in enumerate(ims, 1):
        assert im.size == (W, H)
        im.save(os.path.join(out, f"{i}.png"))


if __name__ == "__main__":
    main()
