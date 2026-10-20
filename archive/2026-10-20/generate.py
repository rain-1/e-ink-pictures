#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-20.

Theme of the day: the hidden figure. Each picture is a true diagram of
something that cannot be seen directly, and the hidden thing is the one
thing drawn in red:
  1. the sphere inside the Sydney Opera House (opened 20 Oct 1973)
  2. Rømer's light-delay figure, burning (Copenhagen fire, 20 Oct 1728)
  3. the light path inside Tolkowsky's ideal brilliant (1919; Tracy Hall b. 20 Oct 1919)
  4. the neutron, which leaves no track (Chadwick b. 20 Oct 1891)
  5. a page of graphic score, where the red line is the sound

Run: python3 generate.py <outdir>
"""

import math
import random
import sys
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
INTER = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
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


def dashed_arc(d, cx, cy, r, a0, a1, dash, gap, fill, width):
    """Dashed circle arc (angles in radians), dash/gap measured in pixels."""
    step = 1.0 / r
    a, on, run = a0, True, 0.0
    pts = []
    while a < a1:
        p = (cx + r * math.cos(a), cy + r * math.sin(a))
        if on:
            pts.append(p)
        run += 1
        if on and run >= dash:
            if len(pts) > 1:
                d.line(pts, fill=fill, width=width)
            pts, on, run = [], False, 0
        elif not on and run >= gap:
            on, run = True, 0
        a += step
    if on and len(pts) > 1:
        d.line(pts, fill=fill, width=width)


def value_noise(shape, scales, seed):
    rng = np.random.default_rng(seed)
    h, w = shape
    out = np.zeros(shape)
    amp, tot = 1.0, 0.0
    for sc in scales:
        g = rng.random((max(2, h // sc + 2), max(2, w // sc + 2)))
        im = Image.fromarray((g * 255).astype(np.uint8)).resize(
            (w + sc * 2, h + sc * 2), Image.BICUBIC)
        out += amp * np.asarray(im, dtype=float)[:h, :w] / 255.0
        tot += amp
        amp *= 0.55
    return out / tot


# ---------------------------------------------- 1. The spherical solution
def arc_points(p1, p2, R, interior, n=80):
    """Points on the arc of radius R from p1 to p2, centre on the `interior` side."""
    (x1, y1), (x2, y2) = p1, p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    dd = math.hypot(dx, dy)
    nx, ny = -dy / dd, dx / dd
    if (interior[0] - mx) * nx + (interior[1] - my) * ny < 0:
        nx, ny = -nx, -ny
    h = math.sqrt(R * R - (dd / 2) ** 2)
    cx, cy = mx + nx * h, my + ny * h
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    da = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    pts = [(cx + R * math.cos(a1 + da * i / n), cy + R * math.sin(a1 + da * i / n))
           for i in range(n + 1)]
    return pts, (cx, cy)


def image1_opera():
    s = 3
    G = 204  # podium top / base of shells
    WL = 216  # water line
    R = 172  # one radius for every shell ridge: the sphere
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)

    # (base_left, pedestal, apex_x, apex_y, facing) ; facing -1 = mouth to the left
    shells = [
        (172, 240, 186, 100, -1),   # rear of the series
        (112, 206, 124, 58, -1),    # tallest
        (66, 152, 76, 92, -1),      # front
        (226, 284, 270, 140, 1),    # small reversed shell at the back
        (300, 352, 310, 150, -1),   # restaurant pair
        (322, 380, 334, 132, -1),
    ]
    hero = 1
    centres = {}
    geo = []
    for i, (bl, pd, ax, ay, f) in enumerate(shells):
        interior = (bl, G)
        back, c = arc_points((ax, ay), (pd, G), R, interior)
        centres[i] = c
        # front edge: gentle concave curve from base-left up to the apex
        front = []
        for k in range(31):
            t = k / 30
            x = bl + (ax - bl) * t - f * 8 * math.sin(math.pi * t) * (-1)
            y = G + (ay - G) * t
            front.append((x, y))
        geo.append((back, front, (pd, G)))

    # the sphere, behind everything
    cx, cy = centres[hero]
    S = lambda p: (p[0] * s, p[1] * s)
    dashed_arc(d, cx * s, cy * s, R * s, 0, 2 * math.pi, 7 * s, 5 * s, RED, 2 * s)

    # podium
    d.rectangle([40 * s, G * s, 392 * s, WL * s], fill=BLACK)
    for k in range(6):  # the grand stair on the south side
        x0 = 380 - k * 5
        d.line([x0 * s, (G + 2 + k * 2) * s, 400 * s, (G + 2 + k * 2) * s], fill=WHITE, width=s)

    order = [0, 1, 2, 3, 4, 5]
    order = [0, 1, 2, 5, 4, 3]
    for i in order:
        back, front, ped = geo[i]
        poly = front + back[1:] + [front[0]]
        # glass wall under the mouth
        bl, pd, ax, ay, f = shells[i]
        d.polygon([S(p) for p in poly], fill=WHITE)
        # ribs: great-circle arcs fanning from the pedestal, seen edge-on as lines
        for k in range(2, 30, 3):
            d.line([S(ped), S(front[k])], fill=BLACK, width=s)
        # glass wall: the mouth, a dark triangle under the lowest part of the front edge
        d.polygon([S(p) for p in front[:9]] + [S((front[8][0], G))], fill=BLACK)
        d.line([S(p) for p in front], fill=BLACK, width=2 * s)
        d.line([S(p) for p in back], fill=RED if i == hero else BLACK, width=(3 if i == hero else 2) * s)

    # radius from the hidden centre to the ridge
    mid = geo[hero][0][34]
    d.line([S((cx, cy)), S(mid)], fill=RED, width=s)
    d.ellipse([(cx - 3) * s, (cy - 3) * s, (cx + 3) * s, (cy + 3) * s], fill=RED)

    img = snap(img)

    # water: hatch lines, denser where the shells reflect
    a = np.array(img)
    shellmask = np.zeros((H, W), bool)
    region = a[:G, :, :]
    shellmask[:G] = ~((region[..., 0] == 255) & (region[..., 1] == 255) & (region[..., 2] == 255))
    rng = random.Random(1973)
    for y in range(WL + 4, H, 3):
        depth = (y - WL) / (H - WL)
        src = WL - (y - WL) * 1.1 - 12
        for x in range(0, W):
            refl = 0 <= src < G and shellmask[int(src), x] and abs(x - cx) > 2
            p = 0.03 + 0.22 * depth
            if refl:
                p = 0.9
            if rng.random() < p:
                a[y, x] = BLACK
    # break the hatching into dashes
    for y in range(WL + 3, H, 3):
        x = 0
        while x < W:
            ln = rng.randint(4, 30)
            gap = rng.randint(1, 4)
            a[y, x + ln:x + ln + gap] = WHITE
            x += ln + gap
    img = Image.fromarray(a)
    d = crisp(img)
    # text: sky, top right
    f1 = font(INTER, 17)
    d.text((228, 10), "THE SPHERICAL", font=f1, fill=BLACK)
    d.text((228, 28), "SOLUTION", font=f1, fill=BLACK)
    fm = font(MONO, 10)
    d.text((228, 52), "Bennelong Point", font=fm, fill=BLACK)
    d.text((228, 64), "opened 20·X·1973", font=fm, fill=BLACK)
    d.text((228, 76), "R = 75.2 m  (246 ft)", font=fm, fill=RED)
    fi = font(SERIF_I, 12)
    d.text((228, 92), "Every shell is cut from", font=fi, fill=BLACK)
    d.text((228, 105), "the same ball. — Utzon, 1961", font=fi, fill=BLACK)
    return finalize(img)


# ---------------------------------------------- 2. Rømer's figure, burning
def image2_romer():
    s = 3
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)
    S = lambda x, y: (x * s, y * s)
    A = (128, 176)            # the Sun
    r_e = 62                  # Earth's orbit
    B = (322, 146)            # Jupiter
    r_io = 16
    # Earth's orbit
    d.ellipse([S(A[0] - r_e, A[1] - r_e), S(A[0] + r_e, A[1] + r_e)], outline=BLACK, width=2 * s)
    # Sun
    d.ellipse([S(A[0] - 7, A[1] - 7), S(A[0] + 7, A[1] + 7)], fill=BLACK)
    for k in range(12):
        an = k * math.pi / 6
        d.line([S(A[0] + 10 * math.cos(an), A[1] + 10 * math.sin(an)),
                S(A[0] + 14 * math.cos(an), A[1] + 14 * math.sin(an))], fill=BLACK, width=s)
    # Jupiter, Io's orbit, shadow
    ang = math.atan2(B[1] - A[1], B[0] - A[0])
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    rj = 7
    shadow_len = 70
    poly = [S(B[0] + px * rj, B[1] + py * rj), S(B[0] - px * rj, B[1] - py * rj),
            S(B[0] - px * (rj - 1.5) + ux * shadow_len, B[1] - py * (rj - 1.5) + uy * shadow_len),
            S(B[0] + px * (rj - 1.5) + ux * shadow_len, B[1] + py * (rj - 1.5) + uy * shadow_len)]
    d.polygon(poly, fill=BLACK)
    d.ellipse([S(B[0] - r_io, B[1] - r_io), S(B[0] + r_io, B[1] + r_io)], outline=BLACK, width=s)
    d.ellipse([S(B[0] - rj, B[1] - rj), S(B[0] + rj, B[1] + rj)], fill=WHITE, outline=BLACK, width=2 * s)
    # C and D: Io entering and leaving the shadow
    C = (B[0] + ux * r_io + px * rj * 0.9, B[1] + uy * r_io + py * rj * 0.9)
    D = (B[0] + ux * r_io - px * rj * 0.9, B[1] + uy * r_io - py * rj * 0.9)
    for P in (C, D):
        d.ellipse([S(P[0] - 2.5, P[1] - 2.5), S(P[0] + 2.5, P[1] + 2.5)], fill=WHITE, outline=BLACK, width=s)
    # Earth stations (Rømer's letters), angle measured from the Sun-Jupiter line
    stations = {"L": 62, "K": 98, "F": 262, "G": 298, "H": 180, "E": 0}
    pos = {}
    for name, deg in stations.items():
        a = ang + math.radians(deg) * -1
        P = (A[0] + r_e * math.cos(a), A[1] + r_e * math.sin(a))
        pos[name] = P
        d.ellipse([S(P[0] - 3, P[1] - 3), S(P[0] + 3, P[1] + 3)], fill=BLACK)
    # light from Io (at D) to Earth at L (near) and at G (far)
    for nm in ("L", "F"):
        d.line([S(*D), S(*pos[nm])], fill=RED, width=2 * s)
    # the extra path: across the orbit
    img = img.resize((W, H), Image.LANCZOS)
    img = snap(img)

    # ---- the fire, coming in from the lower right
    yy, xx = np.mgrid[0:H, 0:W]
    n = value_noise((H, W), [48, 24, 12, 5, 2], 1728)
    g = (xx / W) * 0.62 + (yy / H) * 0.55
    field = g + (n - 0.5) * 0.45
    thr = 0.93
    a = np.array(img)
    rng = np.random.default_rng(20)
    burnt = field > thr
    ember = (field > thr - 0.022) & ~burnt
    scorch = (field > thr - 0.09) & ~burnt & ~ember
    sp = rng.random((H, W))
    a[scorch & (sp < ((field - (thr - 0.09)) / 0.07) ** 3 * 0.5)] = BLACK
    a[ember] = RED
    a[burnt] = BLACK
    sparks = burnt & (field > thr + 0.04) & (sp < 0.012)
    a[sparks] = RED
    # a few sparks escaping above the edge
    for _ in range(40):
        y, x = rng.integers(0, H), rng.integers(0, W)
        if thr - 0.2 < field[y, x] < thr - 0.09:
            a[y, x] = RED
    img = Image.fromarray(a)
    d = crisp(img)
    fl = font(SERIF_I, 13)
    keep = lambda x, y: field[min(H - 1, int(y)), min(W - 1, int(x))] < thr - 0.1
    labels = {"L": (-12, -14), "K": (-4, -16), "F": (4, 2), "G": (4, 0), "H": (-14, -6), "E": (4, -14)}
    for nm, (ox, oy) in labels.items():
        P = pos[nm]
        if keep(P[0] + ox, P[1] + oy):
            d.text((P[0] + ox, P[1] + oy), nm, font=fl, fill=BLACK)
    d.text((A[0] - 4, A[1] + 15), "A", font=fl, fill=BLACK)
    for nm, P, off in (("B", B, (-6, -30)), ("C", C, (6, 2)), ("D", D, (2, -18))):
        if keep(P[0] + off[0], P[1] + off[1]):
            d.text((P[0] + off[0], P[1] + off[1]), nm, font=fl, fill=BLACK)

    f1 = font(INTER, 40)
    d.text((10, 4), "1728", font=f1, fill=BLACK)
    fm = font(MONO, 10)
    d.text((12, 50), "COPENHAGEN · 20 OCTOBER", font=fm, fill=BLACK)
    d.text((12, 62), "Rømer's notebooks burn.", font=fm, fill=BLACK)
    fi = font(SERIF_I, 12)
    d.text((168, 8), "In 1676 he showed that Io's eclipses", font=fi, fill=BLACK)
    d.text((168, 21), "run late when Earth is far from Jupiter:", font=fi, fill=BLACK)
    d.text((168, 34), "light takes time. About 22 minutes,", font=fi, fill=BLACK)
    d.text((168, 47), "he said, to cross our orbit.", font=fi, fill=BLACK)
    d.text((12, 272), "The fire took the paper.", font=font(SERIF_BI, 13), fill=BLACK)
    d.text((12, 285), "The light had already left.", font=font(SERIF_BI, 13), fill=RED)
    return finalize(img)


# ---------------------------------------------- 3. Tolkowsky's brilliant
def trace_brilliant(x0, n_d=2.417):
    t, ch, pd = 0.53, 0.47 * math.tan(math.radians(34.5)), math.tan(math.radians(40.75))
    poly = [(-t, ch), (t, ch), (1, 0), (0, -pd), (-1, 0)]
    edges = [(poly[i], poly[(i + 1) % 5]) for i in range(5)]
    p = (x0, ch)  # just inside the table
    v = (0.0, -1.0)
    path = [(x0, ch + 0.9), p]
    crit = math.asin(1 / n_d)
    for _ in range(8):
        best = None
        for (a, b) in edges:
            ex, ey = b[0] - a[0], b[1] - a[1]
            den = v[0] * ey - v[1] * ex
            if abs(den) < 1e-12:
                continue
            tt = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
            u = ((a[0] - p[0]) * v[1] - (a[1] - p[1]) * v[0]) / den
            if tt > 1e-7 and -1e-9 <= u <= 1 + 1e-9 and (best is None or tt < best[0]):
                best = (tt, a, b)
        tt, a, b = best
        q = (p[0] + v[0] * tt, p[1] + v[1] * tt)
        path.append(q)
        ex, ey = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ex, ey)
        nx, ny = ey / L, -ex / L  # outward normal (polygon is clockwise in y-up)
        if nx * (q[0]) + ny * (q[1]) < 0:
            nx, ny = -nx, -ny
        cosi = v[0] * nx + v[1] * ny
        inc = math.acos(max(-1, min(1, cosi)))
        if inc > crit:
            v = (v[0] - 2 * cosi * nx, v[1] - 2 * cosi * ny)
            p = q
            continue
        # refract out
        eta = n_d
        k = 1 - eta * eta * (1 - cosi * cosi)
        tx = eta * v[0] + (math.sqrt(k) - eta * cosi) * nx
        ty = eta * v[1] + (math.sqrt(k) - eta * cosi) * ny
        return path, q, (tx, ty), poly
    return path, None, None, poly


def image3_diamond():
    s = 3
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)

    # plan view
    pcx, pcy, pr = 92, 168, 78
    P = lambda r, a: ((pcx + r * pr * math.cos(a)) * s, (pcy + r * pr * math.sin(a)) * s)
    t, st = 0.53, 0.53 + 0.5 * 0.47
    off = math.pi / 8
    d.ellipse([(pcx - pr) * s, (pcy - pr) * s, (pcx + pr) * s, (pcy + pr) * s], outline=BLACK, width=2 * s)
    for k in range(8):
        a0 = off + k * math.pi / 4
        a1 = a0 + math.pi / 4
        am = a0 + math.pi / 8
        d.line([P(t, a0), P(t, a1)], fill=BLACK, width=2 * s)              # table
        d.line([P(t, a0), P(st, am)], fill=BLACK, width=s)                 # star
        d.line([P(t, a1), P(st, am)], fill=BLACK, width=s)
        d.line([P(st, am), P(1, a0)], fill=BLACK, width=s)                 # kite
        d.line([P(st, am), P(1, a1)], fill=BLACK, width=s)
        d.line([P(t, a0), P(1, a0)], fill=BLACK, width=s)
        d.line([P(st, am), P(1, am)], fill=BLACK, width=s)                 # upper girdle split
    # pavilion mains seen through the table: faint arrows
    for k in range(8):
        a = off + k * math.pi / 4
        for r in np.linspace(0.05, 0.5, 9):
            x, y = P(r, a)
            d.ellipse([x - s, y - s, x + s, y + s], fill=BLACK)

    # profile
    cx, gy, R = 270, 158, 88
    T = lambda x, y: ((cx + x * R) * s, (gy - y * R) * s)
    path, q, vout, poly = trace_brilliant(-0.27)
    d.polygon([T(*p) for p in poly], outline=BLACK, width=2 * s)
    # facet junction lines on the crown and pavilion (as seen in profile)
    tt, ch = 0.53, 0.47 * math.tan(math.radians(34.5))
    d.line([T(-tt, ch), T(-0.77, 0.16 * 0 + ch * 0.5)], fill=BLACK, width=s)
    d.line([T(tt, ch), T(0.77, ch * 0.5)], fill=BLACK, width=s)
    d.line([T(-0.77, ch * 0.5), T(-1, 0)], fill=BLACK, width=s)
    d.line([T(0.77, ch * 0.5), T(1, 0)], fill=BLACK, width=s)
    pdp = math.tan(math.radians(40.75))
    d.line([T(-0.55, 0), T(0, -pdp)], fill=BLACK, width=s)
    d.line([T(0.55, 0), T(0, -pdp)], fill=BLACK, width=s)
    d.line([T(-1, 0), T(1, 0)], fill=BLACK, width=s)
    # the ray, red
    d.line([T(*p) for p in path], fill=RED, width=3 * s, joint="curve")
    if q is not None:
        for k, da in enumerate((-0.05, 0.0, 0.05)):
            ang = math.atan2(vout[1], vout[0]) + da
            d.line([T(*q), T(q[0] + 0.85 * math.cos(ang), q[1] + 0.85 * math.sin(ang))],
                   fill=RED, width=(2 if da == 0 else 1) * s)
    img = snap(img)
    d = crisp(img)

    # dimension: table 53%
    y = int(gy - (ch + 0.95) * R) - 2
    x0, x1 = int(cx - 0.53 * R), int(cx + 0.53 * R)
    fm = font(MONO, 10)
    # angle labels
    d.text((cx + R + 3, gy - 18), "34.5°", font=fm, fill=BLACK)
    d.text((cx + int(0.42 * R) + 6, gy + 34), "40.75°", font=fm, fill=BLACK)
    d.text((cx - 18, gy - int(ch * R) - 14), "table 53%", font=fm, fill=BLACK)
    d.text((cx - 18, gy + int(pdp * R) + 4), "culet", font=fm, fill=BLACK)

    f1 = font(INTER, 22)
    d.text((10, 8), "DIAMOND DESIGN", font=f1, fill=BLACK)
    d.text((12, 36), "Marcel Tolkowsky, London, 1919", font=fm, fill=BLACK)
    d.text((12, 48), "n = 2.417 · critical angle 24.4°", font=fm, fill=BLACK)
    fi = font(SERIF_I, 12)
    d.text((10, 256), "He drew the cut that bends light back out of the", font=fi, fill=BLACK)
    d.text((10, 270), "stone. That autumn, on 20 October, Tracy Hall was", font=fi, fill=BLACK)
    d.text((10, 284), "born — the man who in 1954 first made a diamond.", font=fi, fill=BLACK)
    return finalize(img)


# ---------------------------------------------- 4. The particle that leaves no track
def image4_neutron():
    img = Image.new("RGB", (W, H), WHITE)
    a = np.array(img)
    ccx, ccy, cr = 262, 150, 134
    yy, xx = np.mgrid[0:H, 0:W]
    inside = (xx - ccx) ** 2 + (yy - ccy) ** 2 < cr ** 2
    rim = ((xx - ccx) ** 2 + (yy - ccy) ** 2 < (cr + 5) ** 2) & ~inside
    rng = np.random.default_rng(1891)
    a[inside] = BLACK
    a[rim] = BLACK
    mist = inside & (rng.random((H, W)) < 0.018)
    a[mist] = WHITE
    pyr = random.Random(1932)

    def trail(pts, colour, density, jitter, thick=1):
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) * 2))
            for k in range(n):
                if pyr.random() > density:
                    continue
                x = x0 + (x1 - x0) * k / n + pyr.gauss(0, jitter)
                y = y0 + (y1 - y0) * k / n + pyr.gauss(0, jitter)
                for ox in range(thick):
                    for oy in range(thick):
                        xi, yi = int(x) + ox, int(y) + oy
                        if 0 <= xi < W and 0 <= yi < H and inside[yi, xi]:
                            a[yi, xi] = colour

    # cosmic rays: long, faint, straight, crossing the chamber
    for _ in range(3):
        y0 = pyr.uniform(30, 270)
        y1 = y0 + pyr.uniform(-120, 120)
        trail([(120, y0), (400, y1)], WHITE, 0.35, 0.4)
    # electrons: curling spirals in the magnetic field
    for _ in range(5):
        x, y = pyr.uniform(170, 360), pyr.uniform(50, 250)
        r, th, sgn = pyr.uniform(14, 34), pyr.uniform(0, 6.28), pyr.choice((-1, 1))
        pts = []
        for k in range(160):
            pts.append((x + r * math.cos(th), y + r * math.sin(th)))
            th += sgn * 0.08
            r *= 0.985
        trail(pts, WHITE, 0.8, 0.3)
    # alpha stubs from the walls
    for _ in range(4):
        th = pyr.uniform(0, 6.28)
        x0, y0 = ccx + (cr - 2) * math.cos(th), ccy + (cr - 2) * math.sin(th)
        L = pyr.uniform(14, 26)
        trail([(x0, y0), (x0 - L * math.cos(th), y0 - L * math.sin(th))], WHITE, 1.0, 0.6, 2)

    # the neutrons: never seen; only the protons they knock out of the gas
    src = (100, 150)
    for _ in range(11):
        dist = pyr.uniform(50, 250)
        spread = pyr.gauss(0, 0.13)
        ox = src[0] + dist * math.cos(spread)
        oy = src[1] + dist * math.sin(spread)
        if (ox - ccx) ** 2 + (oy - ccy) ** 2 > (cr - 15) ** 2:
            continue
        th = spread + pyr.choice((-1, 1)) * pyr.uniform(0.2, 1.1)
        L = 40 * math.cos(th - spread) ** 2 + pyr.uniform(6, 16)
        trail([(ox, oy), (ox + L * math.cos(th), oy + L * math.sin(th))], RED, 1.0, 0.5, 2)
        a[int(oy) - 1:int(oy) + 2, int(ox) - 1:int(ox) + 2] = RED

    img = Image.fromarray(a)
    d = crisp(img)
    # source: polonium + beryllium at the chamber wall
    d.rectangle([92, 140, 106, 160], fill=WHITE, outline=BLACK, width=2)
    d.text((95, 143), "Be", font=font(MONO, 10), fill=BLACK)
    d.rectangle([80, 144, 90, 156], fill=BLACK)
    fh = font(INTER, 16)
    y = 12
    for line in ("THE", "PARTICLE", "THAT", "LEAVES", "NO", "TRACK"):
        d.text((8, y), line, font=fh, fill=RED if line == "NO" else BLACK)
        y += 18
    fm = font(MONO, 10)
    d.text((8, 168), "Po", font=fm, fill=BLACK)
    d.text((8, 180), "→ Be", font=fm, fill=BLACK)
    d.text((8, 192), "→ n  (unseen)", font=fm, fill=BLACK)
    d.text((8, 204), "→ p", font=fm, fill=RED)
    fi = font(SERIF_I, 12)
    d.text((8, 230), "James Chadwick,", font=fi, fill=BLACK)
    d.text((8, 243), "born 20 Oct 1891.", font=fi, fill=BLACK)
    d.text((8, 262), "Nature 129, 312", font=fm, fill=BLACK)
    d.text((8, 274), "(27 Feb 1932)", font=fm, fill=BLACK)
    return finalize(img)


# ---------------------------------------------- 5. Score for a small room
def image5_score():
    s = 3
    rng = random.Random(20261020)
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)
    S = lambda x, y: (x * s, y * s)
    LY = 158  # the life line, which runs through every page
    d.line([S(0, LY), S(400, LY)], fill=BLACK, width=2 * s)

    # 1. a staff that loses its nerve and bends away
    for k in range(5):
        pts = []
        for i in range(61):
            x = 10 + i * 1.6
            bend = max(0, (x - 52)) ** 2 / 55
            pts.append(S(x, 92 + k * 6 + bend * (1 + k * 0.18)))
        d.line(pts, fill=BLACK, width=s)
    for x, k in ((22, 1.5), (34, 3), (46, 0.5)):
        y = 92 + k * 6
        d.ellipse([S(x - 3.5, y - 2.6), S(x + 3.5, y + 2.6)], fill=BLACK)
        d.line([S(x + 3, y), S(x + 3, y - 18)], fill=BLACK, width=s)

    # 2. circles sitting on the line
    x = 118
    for r, filled in ((13, False), (6, True), (9, False), (3, True), (17, False)):
        d.ellipse([S(x, LY - 2 * r), S(x + 2 * r, LY)], outline=BLACK, fill=BLACK if filled else None, width=2 * s)
        x += 2 * r + 3

    # 3. a black wedge under the line
    d.polygon([S(150, LY + 4), S(232, LY + 4), S(232, LY + 46)], fill=BLACK)
    # numbers hanging from it
    fN = font(INTER_B, 11 * s)
    for i, n in enumerate("3 5 2 8".split()):
        d.text(S(160 + i * 17, LY + 52), n, font=fN, fill=BLACK)

    # 4. tick rhythm above the line
    x = 200
    while x < 266:
        h = rng.choice((6, 6, 10, 18, 3, 26))
        d.line([S(x, LY - 4), S(x, LY - 4 - h)], fill=BLACK, width=s)
        x += rng.choice((2, 3, 3, 5, 8))

    # 5. a perspective block
    d.polygon([S(300, 70), S(360, 58), S(360, 112), S(300, 122)], outline=BLACK, width=2 * s)
    d.polygon([S(360, 58), S(384, 66), S(384, 118), S(360, 112)], fill=BLACK)
    for k in range(1, 6):
        yv = 70 + k * 9
        d.line([S(300, yv), S(360, yv - 12 + k * 0.4)], fill=BLACK, width=s)

    # 6. a fan of lines from below
    for k in range(9):
        a = math.radians(200 + k * 9)
        d.line([S(300, 270), S(300 + 80 * math.cos(a), 270 + 80 * math.sin(a))], fill=BLACK, width=s)
    # dotted descent
    for k in range(14):
        d.ellipse([S(330 + k * 4.5 - 1.2, LY + 10 + k * k * 0.42 - 1.2),
                   S(330 + k * 4.5 + 1.2, LY + 10 + k * k * 0.42 + 1.2)], fill=BLACK)
    # small square cluster
    for (qx, qy, qs) in ((40, 214, 10), (54, 220, 6), (64, 206, 14), (82, 224, 4)):
        d.rectangle([S(qx, qy), S(qx + qs, qy + qs)], outline=BLACK, width=s)

    # the sound: one red line, held
    pts = []
    for i in range(201):
        t = i / 200
        x = 96 + t * 250
        y = LY - 2 - 70 * math.sin(math.pi * t) ** 1.4 + 10 * math.sin(t * 9) * t
        pts.append(S(x, y))
    d.line(pts, fill=RED, width=4 * s, joint="curve")
    img = snap(img)
    d = crisp(img)
    fm = font(MONO, 10)
    d.text((10, 10), "SCORE FOR A SMALL ROOM", font=font(INTER, 14), fill=BLACK)
    d.text((10, 28), "page 1 of 1 · any number of players", font=fm, fill=BLACK)
    d.text((10, 282), "20·X·2026", font=fm, fill=BLACK)
    d.text((246, 282), "after Cardew, Treatise", font=font(SERIF_I, 12), fill=BLACK)
    return finalize(img)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    makers = [image1_opera, image2_romer, image3_diamond, image4_neutron, image5_score]
    for i, fn in enumerate(makers, 1):
        im = fn()
        assert im.size == (W, H)
        im.save(os.path.join(out, f"{i}.png"))
        print(i, fn.__name__)


if __name__ == "__main__":
    main()
