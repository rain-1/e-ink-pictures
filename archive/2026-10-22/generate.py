#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-22.

Theme of the day: against the fall. Garnerin cut his rope over Parc Monceau
on 22 Oct 1797; everything today is about coming down, or refusing to.
  1. 1 Brumaire VI — the first parachute descent; the red is the trapped air
  2. PARA- — parasol, parapluie, paravent, parachute: one shield, four weathers
  3. 0.6 % — Venus at inferior conjunction (24 Oct 04 UTC) shows us its night
  4. 4 + 4 + 4 — Liszt (b. 22 Oct 1811) and the chord with nowhere to land
  5. Suminagashi — ink dropped on water, combed (pure generative, no words)

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


# ------------------------------------------------------ 1. Garnerin, 22 Oct 1797
# ≈1000 m (sources say 2,000–3,000 ft), canopy ≈7 m, no apex vent; it swung so
# hard he was airsick. Lalande's fix: a hole in the top for the air to leave by.

def canopy(d, cx, cy, ang, s, spill=True):
    """Canopy centred at (cx, cy), tilted by ang (radians), scale s px = radius."""
    ca, sa = math.cos(ang), math.sin(ang)

    def rot(x, y):
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)
    dome = [rot(s * math.cos(t), -0.62 * s * math.sin(t))
            for t in np.linspace(0, math.pi, 30)]
    rim = [rot(-s, 0), rot(s, 0)]
    # scalloped hem
    hem = []
    for i in range(7):
        x0 = -s + 2 * s * i / 6
        hem.append(rot(x0, 0))
        if i < 6:
            hem.append(rot(x0 + s / 6, 0.12 * s))
    d.polygon(dome, fill=WHITE)
    d.line(dome + [dome[0]], fill=BLACK, width=2)
    for k in (-0.5, 0, 0.5):
        rib = [rot(k * s * math.cos(t) * 1.0 if False else k * s, 0)]
        d.line([rot(k * s, 0), rot(k * s * 0.4, -0.6 * s * math.sqrt(1 - k * k))], fill=BLACK, width=1)
    d.line(hem, fill=BLACK, width=1)
    basket = rot(0, 1.25 * s)
    for k in (-1, -0.45, 0.45, 1):
        d.line([rot(k * s, 0), rot(k * 0.18 * s, 1.18 * s)], fill=BLACK, width=1)
    bx, by = basket
    q = [rot(-0.2 * s, 1.15 * s), rot(0.2 * s, 1.15 * s), rot(0.16 * s, 1.42 * s), rot(-0.16 * s, 1.42 * s)]
    d.polygon(q, fill=BLACK)
    # figure's head above basket rim
    hx, hy = rot(0, 1.07 * s)
    d.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=BLACK)
    if spill:
        # air spilling out from the lifted side of the rim
        side = -1 if ang > 0 else 1
        x0, y0 = rot(side * s, 0)
        out = (side * ca, side * sa)
        up = (sa, -ca)
        for j, k in enumerate((0.0, 0.35, 0.7)):
            px = x0 + out[0] * (3 + 4 * j) + up[0] * (-2 + 5 * j)
            py = y0 + out[1] * (3 + 4 * j) + up[1] * (-2 + 5 * j)
            pts = [(px + out[0] * t + up[0] * 2.5 * math.sin(t / 2.2),
                    py + out[1] * t + up[1] * 2.5 * math.sin(t / 2.2)) for t in np.linspace(0, 10, 8)]
            d.line(pts, fill=RED, width=2)
    return basket


def image1_garnerin():
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    fm, fm9 = font(MONO, 10), font(MONO, 9)
    top, ground = 34, 268
    # height ruler: 0..1000 m
    rx = 22
    d.line([(rx, top), (rx, ground)], fill=BLACK)
    for m in range(0, 1001, 100):
        y = ground - (ground - top) * m / 1000
        L = 6 if m % 500 == 0 else 3
        d.line([(rx, y), (rx + L, y)], fill=BLACK)
    d.text((rx - 4, top - 13), "1000 m", font=fm9, fill=BLACK)
    d.text((rx + 8, ground - 12), "0", font=fm9, fill=BLACK)
    # balloon, released, rising out of frame
    bxc = 150
    d.ellipse([bxc - 13, 2, bxc + 13, 28], outline=BLACK, width=2)
    for k in (-8, 0, 8):
        d.line([(bxc + k * 0.4, 2), (bxc + k, 27)], fill=BLACK)
    d.line([(bxc - 6, 28), (bxc, 36), (bxc + 6, 28)], fill=BLACK)
    dashed_poly(d, [(bxc, 36), (bxc - 2, 44)], 2, 2, BLACK)
    # descent: snapshots of a pendulum swing
    n = 6
    cx0 = 112
    sw = lambda u: math.cos(u * math.pi)
    path = []
    snaps = []
    for i in range(n):
        t = i / (n - 1)
        y = 62 + t * (ground - 52 - 62)
        ang = 0.42 * sw(i) * (1 - 0.2 * t)
        x = cx0 + 40 * sw(i) * (1 - 0.2 * t)
        snaps.append((x, y, ang))
    # basket path (dense)
    for k in range(200):
        u = k / 199 * (n - 1)
        t = u / (n - 1)
        y = 62 + t * (ground - 52 - 62)
        ang = 0.42 * sw(u) * (1 - 0.2 * t)
        x = cx0 + 40 * sw(u) * (1 - 0.2 * t)
        s = 16
        path.append((x - math.sin(ang) * 1.3 * s, y + math.cos(ang) * 1.3 * s))
    dashed_poly(d, path, 1, 3, BLACK)
    for x, y, ang in snaps:
        canopy(d, x, y, ang, 16)
    # ground: Parc Monceau, the crowd
    d.line([(10, ground), (232, ground)], fill=BLACK, width=2)
    rnd = random.Random(1797)
    for grp in (52, 150, 196):
        for k in range(rnd.randint(4, 7)):
            x = grp + k * 5 + rnd.randint(-1, 1)
            h = rnd.choice((6, 7, 8))
            d.line([(x, ground), (x, ground - h + 2)], fill=BLACK, width=2)
            d.ellipse([x - 1.5, ground - h - 2, x + 1.5, ground - h + 1], fill=BLACK)
    # text column
    X = 246
    d.text((X, 10), "22 OCT 1797", font=font(INTER, 24), fill=BLACK)
    d.text((X, 38), "1 BRUMAIRE AN VI", font=fm, fill=BLACK)
    rows = ["PARC MONCEAU, PARIS", "A.-J. GARNERIN", "CUT AWAY AT ≈1000 m", "CANOPY ≈7 m", "VENT: NONE"]
    for i, r in enumerate(rows):
        d.text((X, 62 + i * 13), r, font=fm9, fill=BLACK)
    si = font(SERIF_I, 13)
    lines = ["The air under the silk", "had no way out but", "round the edge, so it", "tipped him to one side,", "then the other,", "all the way down."]
    for i, l in enumerate(lines):
        d.text((X, 136 + i * 15), l, font=si, fill=BLACK)
    # inset: Lalande's vent
    ix, iy = 300, 250
    canopy(d, ix, iy, 0, 15, spill=False)
    d.rectangle([ix - 3, iy - 11, ix + 3, iy - 8], fill=WHITE)
    for k, j in ((-1, 0), (0, 1), (1, 0)):
        pts = [(ix + k * 2 + 1.6 * math.sin(t / 1.8 + j), iy - 7 - t) for t in np.linspace(0, 16, 9)]
        d.line(pts, fill=RED, width=2)
    d.text((ix + 22, iy - 20), "LALANDE:", font=fm9, fill=BLACK)
    d.text((ix + 22, iy - 9), "cut a hole", font=font(SERIF_I, 12), fill=BLACK)
    d.text((ix + 22, iy + 3), "in the top.", font=font(SERIF_I, 12), fill=BLACK)
    return finalize(img)


# ------------------------------------------------------ 2. PARA-
# para- from Italian parare, to ward off; parasol & paravent via Italian
# (parasole, paravento), parapluie coined in French on that model, parachute
# coined by Lenormand (1785).

def image2_para():
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    fm, fm9 = font(MONO, 10), font(MONO, 9)
    d.text((18, 12), "para-  < It. parare, to ward off", font=fm, fill=BLACK)
    big = font(INTER, 40)
    words = [("SOL", "the sun"), ("PLUIE", "the rain"), ("VENT", "the wind"), ("CHUTE", "the fall")]
    pw = text_w(d, "PARA", big)
    x0 = 18
    y = 38
    for i, (w, g) in enumerate(words):
        b = d.textbbox((0, 0), "PARA", font=big)
        d.text((x0, y - b[1]), "PARA", font=big, fill=RED)
        d.text((x0 + pw + 3, y - b[1]), w, font=big, fill=BLACK)
        wtext(d, 382, y + 16, "against " + g, font(SERIF_I, 14), BLACK)
        y += 52
        if i < 3:
            dashed_poly(d, [(x0, y - 8), (382, y - 8)], 1, 3, BLACK)
    d.line([(18, 252), (382, 252)], fill=BLACK)
    d.text((18, 259), "Lenormand named it in 1785, after the Italian.", font=font(SERIF_I, 13), fill=BLACK)
    d.text((18, 276), "Garnerin trusted his life to it on 22 October 1797.", font=font(SERIF_I, 13), fill=BLACK)
    return finalize(img)


# ------------------------------------------------------ 3. Venus from behind
# Computed from JPL mean elements: conjunction 24 Oct 2026 ≈04 UTC, distance
# 0.273 AU, 6.5° south of the Sun, phase angle 171°, 0.6 % of the disc lit,
# 61″ across. The Sun is therefore "up" (north) from the disc.

def image3_venus():
    img = Image.new("RGB", (W, H), WHITE)
    R = 92
    cx, cy = 118, 172
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    u = (cy - yy)  # toward the sun (up)
    v = xx - cx
    r2 = u * u + v * v
    disc = r2 <= R * R
    k = abs(math.cos(math.radians(171.04)))
    lit = disc & (u > k * np.sqrt(np.maximum(R * R - v * v, 0)) - 1.3)
    a = np.full((H, W, 3), 255, np.uint8)
    a[disc] = BLACK
    a[lit] = RED
    img = Image.fromarray(a)
    d = crisp(img)
    fm, fm9 = font(MONO, 10), font(MONO, 9)
    d.text((14, 10), "VENUS · INFERIOR CONJUNCTION · 24 OCT 2026 ≈04 UTC", font=fm, fill=BLACK)
    # arrow to the sun
    d.line([(cx, 60), (cx, 36)], fill=BLACK)
    d.polygon([(cx - 4, 40), (cx + 4, 40), (cx, 32)], fill=BLACK)
    d.text((cx + 8, 34), "SUN: 6.5° THIS WAY", font=fm9, fill=BLACK)
    d.text((cx + 8, 45), "= 383 OF THESE DISCS", font=fm9, fill=BLACK)
    X = 236
    d.text((X, 70), "0.6 %", font=font(INTER, 44), fill=RED)
    rows = ["OF THE DISC IS LIT", "", "0.273 AU AWAY", "61″ ACROSS", "PHASE ANGLE 171°"]
    for i, r in enumerate(rows):
        d.text((X, 124 + i * 13), r, font=fm9, fill=BLACK)
    si = font(SERIF_I, 13)
    for i, l in enumerate(["The closest it comes", "all year, and it turns", "its night toward us."]):
        d.text((X, 200 + i * 15), l, font=si, fill=BLACK)
    d.text((X, 256), "Evening star in September;", font=font(SERIF_I, 11), fill=BLACK)
    d.text((X, 270), "morning star by November.", font=font(SERIF_I, 11), fill=BLACK)
    return finalize(img)


# ------------------------------------------------------ 4. Liszt's augmented triad

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]


def note(d, x, y, fill):
    d.ellipse([x - 5, y - 3.6, x + 5, y + 3.6], fill=fill)


def sharp(d, x, y, fill):
    d.line([(x - 1.5, y - 7), (x - 1.5, y + 6)], fill=fill)
    d.line([(x + 1.5, y - 6), (x + 1.5, y + 7)], fill=fill)
    d.line([(x - 4, y - 1), (x + 4, y - 3)], fill=fill, width=2)
    d.line([(x - 4, y + 3), (x + 4, y + 1)], fill=fill, width=2)


def dsharp(d, x, y, fill):
    d.line([(x - 3, y - 3), (x + 3, y + 3)], fill=fill, width=2)
    d.line([(x - 3, y + 3), (x + 3, y - 3)], fill=fill, width=2)
    for px, py in ((x - 3, y - 3), (x + 3, y + 3), (x - 3, y + 3), (x + 3, y - 3)):
        d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=fill)


def image4_liszt():
    img = Image.new("RGB", (W * 3, H * 3), WHITE)
    d = ImageDraw.Draw(img)
    cx, cy, r = 96 * 3, 162 * 3, 76 * 3

    def pc(i, rr=r):
        t = math.radians(-90 + 30 * i)
        return (cx + rr * math.cos(t), cy + rr * math.sin(t))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK, width=3)
    for i in range(12):
        x, y = pc(i)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=BLACK)
    # the other three augmented triads, faint
    for s in (1, 2, 3):
        pts = [pc(s + 4 * j, r - 2) for j in range(3)]
        for j in range(3):
            a, b = pts[j], pts[(j + 1) % 3]
            n = 22
            for q in range(n):
                if q % 2 == 0:
                    p0 = (a[0] + (b[0] - a[0]) * q / n, a[1] + (b[1] - a[1]) * q / n)
                    p1 = (a[0] + (b[0] - a[0]) * (q + 1) / n, a[1] + (b[1] - a[1]) * (q + 1) / n)
                    d.line([p0, p1], fill=BLACK, width=2)
    tri = [pc(0 + 4 * j) for j in range(3)]
    d.line(tri + [tri[0]], fill=RED, width=9, joint="curve")
    for x, y in tri:
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=RED)
    img = snap(img)
    d = crisp(img)
    fm, fm9 = font(MONO, 10), font(MONO, 9)
    for i in range(12):
        x, y = pc(i, r + 42)
        t = NAMES[i]
        f = fm9
        ctext(d, x / 3, y / 3 - 6, t, f, RED if i in (0, 4, 8) else BLACK)
    d.text((14, 10), "F. LISZT · b. 22 OCT 1811", font=fm, fill=BLACK)
    d.text((14, 26), "4 + 4 + 4 = 12", font=font(INTER, 22), fill=BLACK)
    # staff: one chord, spelled from each of its notes
    sx0, sx1, base, gap = 200, 388, 112, 8   # base = y of bottom line (E4)
    for k in range(5):
        y = base - k * gap
        d.line([(sx0, y), (sx1, y)], fill=BLACK)
    d.text((sx0 + 2, base - 4 * gap - 22), "\U0001D11E", font=font(FREESERIF, 50), fill=BLACK)

    def sy(step):  # diatonic steps above E4
        return base - step * gap / 2
    chords = [
        [(-2, None), (0, None), (2, "s")],     # C  E  G#
        [(0, None), (2, "s"), (4, "s")],       # E  G# B#
        [(2, "s"), (4, "s"), (6, "x")],        # G# B# D##
    ]
    labels = ["C E G#", "E G# B#", "G# B# Dx"]
    for c, ch in enumerate(chords):
        x = (258, 316, 372)[c]
        col = 0
        for j, (st, acc) in enumerate(ch):
            y = sy(st)
            if st <= -2:
                d.line([(x - 8, sy(-2)), (x + 8, sy(-2))], fill=BLACK)
            note(d, x, y, RED if j == 0 else BLACK)
        for j, (st, acc) in reversed(list(enumerate(ch))):
            # accidentals stack leftwards from the top note down
            y = sy(st)
            if acc == "s":
                sharp(d, x - 13 - 9 * col, y, BLACK)
                col += 1
            elif acc == "x":
                dsharp(d, x - 12 - 9 * col, y, BLACK)
                col += 1
        ctext(d, x - 6, base + 20, labels[c], fm9, BLACK)
    d.line([(sx1, base - 4 * gap), (sx1, base)], fill=BLACK)
    for i, l in enumerate(["One sound, three spellings:", "any of its notes may be the root,",
                           "so none of them is. A chord with", "no floor has nowhere to land."]):
        d.text((206, base + 48 + i * 16), l, font=font(SERIF_I, 13), fill=BLACK)
    wtext(d, 388, 280, "NUAGES GRIS, 1881 — IT HANGS THERE.", fm9, BLACK)
    return finalize(img)


# ------------------------------------------------------ 5. Suminagashi
# Mathematical marbling (after Jaffer / Lu et al.): every operation is an
# invertible map of the water surface, so each pixel is traced backwards
# through the operations until it lands inside a drop.

def image5_marble(seed=20261022):
    rnd = np.random.default_rng(seed)
    S = 3
    Wb, Hb = W * S, H * S
    yy, xx = np.mgrid[0:Hb, 0:Wb].astype(np.float64)
    ops = []
    # suminagashi: drops are laid alternately at several centres, so every
    # new ring shoves its neighbours' rings out of round; one ring is red
    centres = [(0.27, 0.36), (0.70, 0.27), (0.55, 0.72), (0.10, 0.88), (0.93, 0.70), (0.40, 0.05)]
    seq = [int(rnd.choice(len(centres), p=[.24, .2, .2, .12, .12, .12])) for _ in range(96)]
    n0 = seq.count(0)
    red_at = (0, n0 - 4 if (n0 - 4) % 2 == 0 else n0 - 5)   # a late, still-thick ring
    counts = [0] * len(centres)
    for ci in seq:
        fx, fy = centres[ci]
        c = (fx * Wb + rnd.normal(0, 3), fy * Hb + rnd.normal(0, 3))
        k = counts[ci]
        counts[ci] += 1
        col = 2 if (ci, k) == red_at else (1 if k % 2 == 0 else 0)
        rad = 50 + rnd.random() * 16
        ops.append(("drop", c, rad, col))
    # then one slow stroke of a stylus across the water, and a gentle stir
    ops.append(("hline", Hb * 0.55, 260.0, 40.0))
    ops.append(("swirl", (Wb * 0.60, Hb * 0.45), 2.4, 200.0))

    out = np.zeros((Hb, Wb), np.int8) - 1
    px, py = xx.copy(), yy.copy()
    for op in reversed(ops):
        alive = out < 0
        if op[0] == "drop":
            _, (cx, cy), rad, col = op
            dx, dy = px - cx, py - cy
            r2 = dx * dx + dy * dy
            inside = alive & (r2 < rad * rad)
            out[inside] = col
            f = np.sqrt(np.maximum(1 - rad * rad / np.maximum(r2, 1e-9), 0))
            px = np.where(inside, px, cx + dx * f)
            py = np.where(inside, py, cy + dy * f)
        elif op[0] == "hline":
            _, yl, alpha, lam = op
            px = px - alpha * lam / (np.abs(py - yl) + lam)
        elif op[0] == "vcomb":
            _, lines, alpha, lam = op
            dist = np.min(np.abs(px[None] - np.array(lines)[:, None, None]), axis=0)
            py = py - alpha * lam / (dist + lam)
        elif op[0] == "hwave":
            _, amp, ph, wl, lam = op
            py = py - amp * np.sin(2 * math.pi * px / wl + ph) * 0.0
            px = px - amp * 0.5 * np.sin(2 * math.pi * py / wl)
        elif op[0] == "swirl":
            _, (cx, cy), turn, scale = op
            dx, dy = px - cx, py - cy
            rr = np.sqrt(dx * dx + dy * dy)
            th = -turn * np.exp(-rr / scale)
            c, s = np.cos(th), np.sin(th)
            px, py = cx + dx * c - dy * s, cy + dx * s + dy * c
    pal = np.array([WHITE, BLACK, RED, WHITE], np.uint8)
    a = pal[out]
    return finalize(snap(Image.fromarray(a)))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    ims = [image1_garnerin(), image2_para(), image3_venus(), image4_liszt(), image5_marble()]
    for i, im in enumerate(ims, 1):
        assert im.size == (W, H)
        im.save(os.path.join(out, f"{i}.png"))


if __name__ == "__main__":
    main()
