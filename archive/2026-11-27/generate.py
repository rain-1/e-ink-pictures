#!/usr/bin/env python3
"""2026-11-27 (Fri) — theme: upside down / the other way up.
Run from the repo root: python3 archive/2026-11-27/generate.py
Needs numpy + pillow. Writes images/1..5.png and archive/2026-11-27/1..5.png."""
import math, os, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
K, WH, R = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = "archive/2026-11-27"
F = "/usr/share/fonts/"
MONO = F + "truetype/dejavu/DejaVuSansMono.ttf"
MONOB = F + "truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANSB = F + "truetype/dejavu/DejaVuSans-Bold.ttf"
INTERB = F + "opentype/inter/Inter-Black.otf"
S = 3


def font(p, s):
    return ImageFont.truetype(p, s)


def snap(img):
    a = np.asarray(img.convert("RGB")).astype(int)
    pal = np.array([K, WH, R])
    d = ((a[:, :, None, :] - pal[None, None]) ** 2).sum(-1)
    return Image.fromarray(pal[d.argmin(-1)].astype(np.uint8), "RGB")


def down(img3):
    return snap(img3.resize((W, H), Image.LANCZOS))


def save(img, n):
    img = snap(img)
    p = Image.new("P", (1, 1))
    p.putpalette(list(K) + list(WH) + list(R) + [0] * 753)
    q = img.quantize(palette=p, dither=Image.NONE)
    q.save(f"{OUT}/{n}.png")
    os.makedirs("images", exist_ok=True)
    shutil.copy(f"{OUT}/{n}.png", f"images/{n}.png")


def crisp(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return d


def vnoise(rng, gw, gh, w=W, h=H):
    g = (rng.random((gh, gw)) * 255).astype(np.uint8)
    return np.asarray(Image.fromarray(g, "L").resize((w, h), Image.BICUBIC)).astype(float) / 255


# ------------------------------------------------- 1. Venus, one apparition
def p1():
    # (label, % lit, diameter in arcsec) — PyEphem, geocentric
    data = [("6 NOV", 5.7, 57.8), ("27 NOV", 24.6, 42.1), ("20 DEC", 41.7, 30.1),
            ("1 FEB", 63.1, 19.1), ("1 APR", 81.8, 13.1), ("12 AUG", 100.0, 9.8)]
    sc = 1.8
    gap = 15
    a = np.zeros((H, W, 3), np.uint8)
    x = 4
    cy = 122
    rot = math.radians(-28)
    cents = []
    for i, (lab, k, dia) in enumerate(data):
        r = dia * sc / 2
        cx = x + r
        cents.append((cx, r))
        n = int(r) + 3
        ys, xs = np.mgrid[-n * 3:n * 3 + 1, -n * 3:n * 3 + 1] / 3.0
        xr = xs * math.cos(rot) - ys * math.sin(rot)
        yr = xs * math.sin(rot) + ys * math.cos(rot)
        rho2 = xs ** 2 + ys ** 2
        t = 1 - 2 * k / 100
        lit = (rho2 < r * r) & (xr < -t * np.sqrt(np.clip(r * r - yr ** 2, 0, None)))
        m = lit[:lit.shape[0] // 3 * 3, :lit.shape[1] // 3 * 3]
        m = m.reshape(m.shape[0] // 3, 3, m.shape[1] // 3, 3).mean((1, 3)) > 0.5
        oy, ox = int(round(cy)) - n, int(round(cx)) - n
        col = R if i == 1 else WH
        for j in range(m.shape[0]):
            for q in range(m.shape[1]):
                X, Y = ox + q, oy + j
                if not (0 <= X < W and 0 <= Y < H):
                    continue
                if m[j, q]:
                    a[Y, X] = col
                else:
                    d = math.hypot(X - cx, Y - cy)
                    if abs(d - r + 0.5) < 0.6 and (X + Y) % 2 == 0:
                        a[Y, X] = WH
        x += 2 * r + gap
    img = Image.fromarray(a, "RGB")
    d = crisp(img)
    d.text((8, 8), "VENUS", font=font(INTERB, 26), fill=WH)
    d.text((104, 12), "the morning star, one apparition", font=font(MONO, 10), fill=WH)
    d.text((104, 24), "discs to one scale", font=font(MONO, 10), fill=WH)
    f = font(MONO, 10)
    fb = font(MONOB, 10)
    for i, ((lab, k, dia), (cx, r)) in enumerate(zip(data, cents)):
        y = 190
        d.text((cx, y), lab, font=f, fill=WH, anchor="ma")
        d.text((cx, y + 13), f"{k:.0f}%", font=f, fill=WH, anchor="ma")
        d.text((cx, y + 26), f'{dia:.0f}"', font=f, fill=WH, anchor="ma")
    cx = cents[1][0]
    d.line([(cx, 232), (cx, 246)], fill=R)
    d.rectangle([cx - 46, 247, cx + 46, 263], fill=R)
    d.text((cx, 249), "THIS MORNING", font=fb, fill=WH, anchor="ma")
    d.text((8, 276), "It shrinks as it fills; brightest a quarter lit, mag -4.5.",
           font=f, fill=WH)
    save(img, 1)


# ------------------------------------------------- 2. Mars 2 (silent)
def p2():
    rng = np.random.default_rng(19711127)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    cx, cy, Rp = 262.0, 246.0, 212.0
    nx, ny = (xx - cx) / Rp, (yy - cy) / Rp
    r2 = nx ** 2 + ny ** 2
    inside = r2 < 1
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    L = np.array([-0.62, -0.48, 0.62])
    L /= np.linalg.norm(L)
    lam = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    # dust: long streaks following latitude, a storm with no features
    streak = vnoise(rng, 5, 46) * 0.6 + vnoise(rng, 14, 90) * 0.4
    billow = vnoise(rng, 9, 7)
    T = lam ** 0.75 * (0.55 + 1.15 * (streak - 0.5) + 0.35 * (billow - 0.5))
    T += 0.10 * np.exp(-(1 - np.sqrt(np.clip(r2, 0, 1))) / 0.03) * (lam > 0.02)  # limb haze
    T = np.clip(T, 0, 0.93)
    ink = (rng.random((H, W)) < T ** 1.15) & inside
    a = np.zeros((H, W, 3), np.uint8)
    a[ink] = WH
    # a few stars
    for _ in range(26):
        X, Y = int(rng.integers(0, W)), int(rng.integers(0, H))
        if (X - cx) ** 2 + (Y - cy) ** 2 > (Rp + 8) ** 2:
            a[Y, X] = WH
    img = Image.fromarray(a, "RGB")
    d = ImageDraw.Draw(img)
    # the way down: dotted arc ending in one red cross
    ix, iy = 150, 132
    p0, p1_, p2_ = (4, 14), (96, 40), (ix, iy)
    n = 30
    for i in range(n):
        t = i / n
        X = (1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1_[0] + t * t * p2_[0]
        Y = (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1_[1] + t * t * p2_[1]
        over = (X - cx) ** 2 + (Y - cy) ** 2 < Rp ** 2
        if over:
            d.ellipse([X - 5, Y - 5, X + 4, Y + 4], fill=K)
            d.rectangle([X - 1, Y - 1, X, Y], fill=WH)
        else:
            d.rectangle([X - 1, Y - 1, X, Y], fill=WH)
    d.ellipse([ix - 11, iy - 11, ix + 11, iy + 11], fill=K)
    for w_, c in ((0, R),):
        d.line([(ix - 6, iy - 6), (ix + 6, iy + 6)], fill=c, width=3)
        d.line([(ix - 6, iy + 6), (ix + 6, iy - 6)], fill=c, width=3)
    save(img, 2)


# ------------------------------------------------- 3. Celsius, the other way up
def p3():
    img = Image.new("RGB", (W, H), WH)
    d = crisp(img)
    tx = 52
    y0, y100 = 40, 220
    # glass
    d.rounded_rectangle([tx - 8, 22, tx + 8, 250], radius=8, outline=K, width=2)
    d.ellipse([tx - 21, 232, tx + 21, 274], fill=K)
    d.ellipse([tx - 18, 235, tx + 18, 271], fill=R)
    yv = y0 + (y100 - y0) * 0.80
    d.rectangle([tx - 3, yv, tx + 3, 240], fill=R)
    d.rectangle([tx - 6, 24, tx - 5, 30], fill=WH)
    f = font(MONO, 10)
    fb = font(MONOB, 10)
    for v in range(0, 101, 5):
        y = y0 + (y100 - y0) * v / 100
        if v % 10 == 0:
            d.line([(tx + 12, y), (tx + 24, y)], fill=K, width=1)
            d.text((tx + 28, y), str(v), font=fb if v in (0, 100) else f, fill=K, anchor="lm")
        else:
            d.line([(tx + 12, y), (tx + 18, y)], fill=K)
    big = font(INTERB, 92)
    lab = font(SANSB, 13)
    X = 148
    d.text((X, 6), "0°", font=big, fill=K)
    d.text((X, 172), "100°", font=big, fill=R)
    bb0 = d.textbbox((X, 6), "0°", font=big)
    bb1 = d.textbbox((X, 172), "100°", font=big)
    d.text((bb0[2] + 12, bb0[3] - 14), "WATER BOILS", font=lab, fill=K)
    d.text((X + 3, bb1[3] + 6), "WATER FREEZES", font=lab, fill=K)
    # leaders
    for y, bb in ((y0, bb0), (y100, bb1)):
        for x in range(tx + 50, X - 6, 3):
            d.point((x, y), fill=K)
    ty = 118
    for i, s in enumerate(["Anders Celsius, born 27 November 1701,",
                           "numbered his thermometer downward.",
                           "It was turned over after his death."]):
        d.text((X + 3, ty + i * 13), s, font=f, fill=K)
    save(img, 3)


# ------------------------------------------------- 4. Note G
def p4():
    ops = "x-+//--+/x+--+/x-+/xx+-++"
    assert len(ops) == 25
    img3 = Image.new("RGB", (W * S, H * S), R)
    d = ImageDraw.Draw(img3)
    c, g, m = 52, 4, 12
    cells = []
    for i, o in enumerate(ops):
        cx_, cy_ = i % 5, i // 5
        x0, y0 = m + cx_ * (c + g), m + cy_ * (c + g)
        loop = 12 <= i <= 22
        bg, fg = (WH, K) if loop else (K, WH)
        cells.append((x0, y0, bg, fg, i + 1))
        d.rectangle([x0 * S, y0 * S, (x0 + c) * S - 1, (y0 + c) * S - 1], fill=bg)
        mx, my = (x0 + c / 2 + 3) * S, (y0 + c / 2 + 3) * S
        l, t = 15 * S, 4 * S
        if o in "-+/":
            d.rectangle([mx - l, my - t, mx + l, my + t], fill=fg)
        if o == "+":
            d.rectangle([mx - t, my - l, mx + t, my + l], fill=fg)
        if o == "/":
            for s_ in (-1, 1):
                q = my + s_ * 11 * S
                d.ellipse([mx - 4.5 * S, q - 4.5 * S, mx + 4.5 * S, q + 4.5 * S], fill=fg)
        if o == "x":
            k = l * 0.74
            d.line([(mx - k, my - k), (mx + k, my + k)], fill=fg, width=2 * t)
            d.line([(mx - k, my + k), (mx + k, my - k)], fill=fg, width=2 * t)
    img = down(img3)
    d = crisp(img)
    f = font(MONO, 10)
    fb = font(MONOB, 10)
    for x0, y0, bg, fg, n in cells:
        d.text((x0 + 3, y0 + 1), str(n), font=fb, fill=fg)
    X = 298
    d.text((X, 10), "NOTE", font=font(INTERB, 30), fill=WH)
    d.text((X, 42), "G", font=font(INTERB, 78), fill=WH)
    lines = ["25 operations", "for an engine", "never built:", "a Bernoulli", "number, 1843.", "",
             "White cards,", "13 to 23, are", "run twice."]
    for i, s in enumerate(lines):
        d.text((X, 134 + i * 12), s, font=fb, fill=WH)
    d.text((X, 262), "A. A. L.", font=font(SANSB, 13), fill=K)
    d.text((X, 278), "d. 27 XI 1852", font=fb, fill=K)
    save(img, 4)


# ------------------------------------------------- 5. The parade (silent)
def p5():
    rng = np.random.default_rng(19241127)
    img3 = Image.new("RGB", (W * S, H * S), WH)
    d = ImageDraw.Draw(img3)

    def P(pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(pts, fill=K):
        d.polygon(P(pts), fill=fill)

    def ell(x0, y0, x1, y1, fill=K):
        d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill)

    def line(pts, w=2, fill=K):
        d.line(P(pts), fill=fill, width=int(w * S), joint="curve")
        for x, y in pts:
            ell(x - w / 2, y - w / 2, x + w / 2, y + w / 2, fill)

    G = 190  # street level

    def person(x, h=50, stride=7, arm="swing", hat="cap", col=K):
        top = G - h
        hr = h * 0.095
        hy = top + hr + 2
        sh, hip = hy + hr + 2, G - h * 0.45
        ell(x - hr, hy - hr, x + hr, hy + hr, col)
        poly([(x - 7, sh), (x + 7, sh), (x + 4.5, hip), (x - 4.5, hip)], col)
        kn = (hip + G) / 2
        line([(x + 1, hip), (x + stride * 0.7, kn), (x + stride, G - 1), (x + stride + 4, G - 1)], 3.4, col)
        line([(x - 1, hip), (x - stride * 0.2, kn), (x - stride, G - 1), (x - stride + 4, G - 1)], 3.4, col)
        if arm == "swing":
            line([(x + 6, sh + 2), (x + 9, sh + 11), (x + 12, sh + 16)], 2.6, col)
            line([(x - 6, sh + 2), (x - 9, sh + 11), (x - 8, sh + 18)], 2.6, col)
        if hat == "shako":
            poly([(x - hr, hy - hr + 1), (x + hr, hy - hr + 1), (x + hr + 1, hy - hr - 11), (x - hr - 1, hy - hr - 11)], col)
            line([(x, hy - hr - 11), (x + 1, hy - hr - 19)], 2.6, col)
        if hat == "cap":
            poly([(x - hr - 1, hy - hr + 2), (x + hr + 5, hy - hr + 2), (x + hr, hy - hr - 3), (x - hr, hy - hr - 3)], col)
        return sh, hip, hy, hr

    # -- drum major, baton high
    x = 378
    sh, hip, hy, hr = person(x, 54, 8, arm=None, hat="shako")
    line([(x + 6, sh + 2), (x + 13, sh - 6), (x + 12, sh - 18)], 2.6)
    line([(x + 12, sh - 6), (x + 12, sh - 40)], 1.6)
    ell(x + 9, sh - 46, x + 15, sh - 40)
    line([(x - 6, sh + 2), (x - 10, sh + 12), (x - 5, sh + 17)], 2.6)
    # -- bass drum
    x = 349
    sh, hip, hy, hr = person(x, 50, 7, arm=None)
    ell(x + 2, sh + 1, x + 24, sh + 23)
    ell(x + 5, sh + 4, x + 21, sh + 20, WH)
    ell(x + 7, sh + 6, x + 19, sh + 18)
    line([(x + 5, sh + 2), (x + 10, sh - 4), (x + 15, sh - 9)], 2.2)
    ell(x + 13, sh - 13, x + 19, sh - 7)
    # -- horns
    for x in (322, 297):
        sh, hip, hy, hr = person(x, 50, 7, arm=None)
        line([(x + 5, sh + 3), (x + 11, sh + 3), (x + 9, hy + 1)], 2.6)
        line([(x + 5, hy + 1), (x + 20, hy - 3)], 2.2)
        poly([(x + 19, hy - 9), (x + 27, hy - 12), (x + 27, hy + 5), (x + 19, hy)])
    # -- elephant, facing right
    ex, ey = 156, G - 78

    def E(pts):
        return [(ex + px * 1.08, ey + py * 1.08) for px, py in pts]

    def eell(x0, y0, x1, y1, fill=K):
        (a, b), (c_, e_) = E([(x0, y0), (x1, y1)])
        ell(a, b, c_, e_, fill)
    eell(8, 10, 78, 54)
    eell(60, 6, 94, 42)
    for x0, x1, yt in ((14, 27, 40), (30, 41, 44), (56, 67, 44), (68, 81, 40)):
        poly(E([(x0, yt), (x1, yt), (x1 - 0.5, 72), (x0 + 0.5, 72)]))
    line(E([(89, 26), (95, 40), (96, 54), (99, 63), (105, 62)]), 7)
    line(E([(104, 62), (107, 58)]), 4)
    line(E([(11, 22), (5, 34), (5, 46)]), 2)
    eell(56, 10, 76, 42, WH)
    eell(58, 12, 74, 40)
    line(E([(86, 37), (93, 44)]), 1.6, WH)
    eell(83, 18, 86, 21, WH)
    # blanket on its back
    poly(E([(30, 9), (56, 9), (58, 34), (28, 34)]), WH)
    poly(E([(32, 11), (54, 11), (56, 32), (30, 32)]))
    for i in range(4):
        eell(33 + i * 6, 15, 36 + i * 6, 18, WH)
        eell(33 + i * 6, 24, 36 + i * 6, 27, WH)
    # keeper walking at its shoulder
    x = 280
    # -- camel, facing right
    kx, ky = 70, G - 82

    def C(pts):
        return [(kx + px, ky + py) for px, py in pts]
    (a, b), (c_, e_) = C([(10, 30), (62, 54)])
    ell(a, b, c_, e_)
    (a, b), (c_, e_) = C([(24, 14), (50, 44)])
    ell(a, b, c_, e_)
    poly(C([(54, 36), (68, 8), (77, 10), (68, 46)]))
    (a, b), (c_, e_) = C([(68, 2), (90, 15)])
    ell(a, b, c_, e_)
    poly(C([(70, 4), (72, -2), (75, 4)]))
    for xa, xk, xb in ((18, 15, 17), (27, 29, 26), (50, 48, 52), (58, 61, 58)):
        line(C([(xa, 50), (xa, 66), (xb, 81), (xb + 4, 81)]), 3.4)
    line(C([(11, 38), (6, 50)]), 2)
    # -- Santa's float, last in line
    fx = 6
    poly([(fx, G - 30), (fx + 62, G - 30), (fx + 62, G - 9), (fx, G - 9)])
    for i in range(6):
        ell(fx + 1 + i * 10.2, G - 15, fx + 11 + i * 10.2, G - 4)
    for wx in (fx + 14, fx + 48):
        ell(wx - 8, G - 15, wx + 8, G + 1)
        ell(wx - 4, G - 11, wx + 4, G - 3, WH)
    # sleigh
    poly([(fx + 8, G - 30), (fx + 8, G - 52), (fx + 16, G - 56), (fx + 18, G - 40), (fx + 50, G - 40),
          (fx + 56, G - 50), (fx + 60, G - 48), (fx + 54, G - 30)])
    # Santa (red)
    sx, sy = fx + 31, G - 40
    poly([(sx - 10, sy), (sx + 10, sy), (sx + 8, sy - 22), (sx - 8, sy - 22)], R)
    ell(sx - 7, sy - 36, sx + 7, sy - 22, R)
    poly([(sx - 7, sy - 31), (sx + 7, sy - 31), (sx - 3, sy - 48)], R)
    ell(sx - 7, sy - 51, sx - 1, sy - 45, R)
    line([(sx + 7, sy - 18), (sx + 17, sy - 30), (sx + 19, sy - 40)], 3.4, R)   # waving
    ell(sx - 3, sy - 30, sx + 8, sy - 19, WH)   # beard
    poly([(sx - 1, sy - 23), (sx + 9, sy - 23), (sx + 5, sy - 13)], WH)
    line([(sx - 9, sy - 10), (sx + 9, sy - 10)], 2.4, K)   # belt
    # street
    d.line(P([(0, G + 2), (W, G + 2)]), fill=K, width=S)
    # tram rails further forward
    for yy_ in (206, 211):
        for x in range(0, W, 6):
            d.rectangle([x * S, yy_ * S, (x + 3) * S - 1, (yy_ + 1) * S - 1], fill=K)

    # bunting strung across the street
    for (xa, ya, xb, yb, sag) in ((-10, 20, 284, 34, 30), (284, 34, 410, 16, 22)):
        pts = []
        for i in range(41):
            t = i / 40
            pts.append((xa + (xb - xa) * t, ya + (yb - ya) * t + sag * 4 * t * (1 - t)))
        d.line(P(pts), fill=K, width=S)
        for i in range(2, 40, 3):
            (x0, y0), (x1, y1) = pts[i - 1], pts[i + 1]
            poly([(x0, y0 + 1), (x1, y1 + 1), ((x0 + x1) / 2, (y0 + y1) / 2 + 13)])
    line([(284, 34), (284, G)], 1.2)
    ell(278, 28, 290, 40)
    ell(280, 30, 288, 38, WH)
    # -- the crowd, seen from behind
    def head(x, y, r, hat):
        # white moat
        ell(x - r - 2, y - r - 6, x + r + 2, y + r + 2, WH)
        d.rounded_rectangle([(x - r * 2.1 - 2) * S, (y + r * 0.7 - 2) * S, (x + r * 2.1 + 2) * S, (H + 20) * S],
                            radius=int(r * 1.1 * S), fill=WH)
        d.rounded_rectangle([(x - r * 2.1) * S, (y + r * 0.7) * S, (x + r * 2.1) * S, (H + 20) * S],
                            radius=int(r * 1.0 * S), fill=K)
        ell(x - r, y - r, x + r, y + r)
        if hat == 0:      # fedora
            ell(x - r * 1.75 - 1.5, y - r * 0.75 - 1.5, x + r * 1.75 + 1.5, y - r * 0.1 + 1.5, WH)
            ell(x - r * 1.75, y - r * 0.75, x + r * 1.75, y - r * 0.1)
            d.rounded_rectangle([(x - r * 0.95) * S, (y - r * 1.5) * S, (x + r * 0.95) * S, (y - r * 0.3) * S],
                                radius=int(r * 0.4 * S), fill=K)
            line([(x - r * 0.9, y - r * 0.62), (x + r * 0.9, y - r * 0.62)], 1.2, WH)
        elif hat == 1:    # cloche
            ell(x - r * 1.18, y - r * 1.3, x + r * 1.18, y + r * 0.7)
            line([(x - r * 1.0, y + r * 0.05), (x + r * 1.0, y + r * 0.05)], 1.2, WH)
        elif hat == 2:    # flat cap
            ell(x - r * 1.25, y - r * 1.2, x + r * 1.25, y - r * 0.1)
        # hat 3: bare head

    back = []
    x = -6.0
    while x < W + 10:
        back.append((x, 240 + rng.uniform(-4, 4), rng.uniform(8.5, 10), int(rng.integers(0, 4))))
        x += rng.uniform(27, 33)
    front = []
    x = 8.0
    while x < W + 10:
        front.append((x, 270 + rng.uniform(-4, 4), rng.uniform(11, 13), int(rng.integers(0, 3))))
        x += rng.uniform(36, 43)
    # a child on someone's shoulders, arm up
    bx, by, br, _ = back[5]
    cy_ = by - br - 22
    ell(bx - 9, cy_ - 2, bx + 9, by - br + 6, WH)
    poly([(bx - 6, cy_ + 6), (bx + 6, cy_ + 6), (bx + 5, by - br + 2), (bx - 5, by - br + 2)])
    ell(bx - 6, cy_ - 6, bx + 6, cy_ + 6)
    line([(bx + 5, cy_ + 8), (bx + 12, cy_ + 1), (bx + 14, cy_ - 9)], 2.6)
    for h_ in back:
        head(*h_)
    for h_ in front:
        head(*h_)
    img = down(img3)
    save(img, 5)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    p1(); p2(); p3(); p4(); p5()
