#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-19 (Planck's law, 126 years old today).

Five 400x300 images in exactly three colors (white, black, red).
Theme of the day: notation as art — the diagrams people draw to describe
the world (a spectrum, a weaving draft, a star chart, a Turing pattern),
made into pictures.
"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
DJ = "/usr/share/fonts/truetype/dejavu/"
SANS, SANS_B = DJ + "DejaVuSans.ttf", DJ + "DejaVuSans-Bold.ttf"
COND_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF = DJ + "DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
MONO = DJ + "DejaVuSansMono.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


_pal = Image.new("P", (1, 1))
_pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)


def down(img):
    """Supersampled RGB -> clean 1x RGB in palette colors, ready for crisp text."""
    img = img.resize((W, H), Image.LANCZOS).convert("RGB")
    return img.quantize(palette=_pal, dither=Image.Dither.NONE).convert("RGB")


def crisp(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return d


def finalize(img, dither=False):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=_pal, dither=d)


# ------------------------------------------------- 1. Planck, 19 October 1900
def image1_planck():
    s = 3
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)
    # left black column with the date
    d.rectangle([0, 0, 92 * s, H * s], fill=BLACK)
    f = font(COND_B, 46 * s)
    for i, t in enumerate(["19", "X", "1900"]):
        ff = f if t != "1900" else font(COND_B, 34 * s)
        bb = d.textbbox((0, 0), t, font=ff)
        d.text(((92 * s - (bb[2] - bb[0])) // 2 - bb[0], (18 + i * 58) * s), t,
               font=ff, fill=RED if t == "X" else WHITE)

    # plot area
    x0, x1, y0, y1 = 112, 388, 46, 244
    def X(lam):  # lam in micrometres, 0..3
        return (x0 + (x1 - x0) * lam / 3.0) * s
    def B(lam, T):
        l = lam * 1e-6
        return 1.0 / (l ** 5 * (math.exp(0.014388 / (l * T)) - 1))
    Bmax = B(2.8978e-3 / 6000 * 1e6, 6000)
    def Y(v):
        return (y1 - (y1 - y0) * min(v, 1.15) / 1.0) * s
    # axes
    d.line([X(0), y1 * s, X(3), y1 * s], fill=BLACK, width=2 * s)
    d.line([X(0), y1 * s, X(0), (y0 - 14) * s], fill=BLACK, width=2 * s)
    for k in range(4):
        d.line([X(k), y1 * s, X(k), (y1 + 4) * s], fill=BLACK, width=s)
    # visible band hatch
    for xx in range(int(X(0.38)), int(X(0.75)), 4 * s):
        d.line([xx, y1 * s, xx + 12 * s, (y1 - 12) * s], fill=BLACK, width=1)
    # Rayleigh-Jeans for 6000K (dashed) — the ultraviolet catastrophe
    T = 6000
    pts = []
    for i in range(1, 400):
        lam = 0.05 + i * 0.0075
        v = 2 * 2.998e8 * 1.381e-23 * T / (lam * 1e-6) ** 4
        v /= 2 * 6.626e-34 * 2.998e8 ** 2
        pts.append((X(lam), Y(v / Bmax)))
    for i in range(0, len(pts) - 1, 4):
        d.line([pts[i], pts[i + 1]], fill=BLACK, width=s)
    # family of curves
    for T in [3000, 3500, 4000, 4500, 5000, 5500]:
        pts = [(X(l), Y(B(l, T) / Bmax)) for l in np.linspace(0.06, 3, 500)]
        d.line(pts, fill=BLACK, width=s, joint="curve")
    pts = [(X(l), Y(B(l, 6000) / Bmax)) for l in np.linspace(0.06, 3, 500)]
    d.line(pts, fill=RED, width=4 * s, joint="curve")
    lp = 2.8978e-3 / 6000 * 1e6
    d.ellipse([X(lp) - 4 * s, Y(1) - 4 * s, X(lp) + 4 * s, Y(1) + 4 * s], fill=RED)
    img = down(img)
    d = crisp(img)
    fs = font(SANS, 10)
    d.text((10, 214), "Berlin.\nDeutsche\nPhysikalische\nGesellschaft", font=fs, fill=WHITE, spacing=2)
    for k in range(4):
        d.text((X(k) / s - 3, y1 + 6), str(k), font=fs, fill=BLACK)
    d.text((X(3) / s - 34, y1 + 6), "λ/μm", font=fs, fill=BLACK)
    d.text((X(lp) / s + 8, Y(1) / s - 7), "6000 K", font=font(SANS_B, 11), fill=RED)
    d.text((X(0.95) / s, Y(0.66) / s), "Rayleigh–Jeans: → ∞", font=fs, fill=BLACK)
    d.text((X(2.25) / s, Y(0.17) / s), "3000 K", font=fs, fill=BLACK)
    xx = x0 + 10
    for txt, sup in [("E = Cλ", 0), ("−5", 1), (" / (e", 0), ("c/λT", 1), (" − 1)", 0)]:
        f = font(SANS, 10 if sup else 16)
        d.text((xx, 8 if sup else 12), txt, font=f, fill=BLACK)
        xx += d.textlength(txt, font=f) + (1 if sup else 0)
    d.text((x0, 266), "„Über eine Verbesserung der Wienschen", font=font(SERIF_I, 11), fill=BLACK)
    d.text((x0, 279), "Spektralgleichung“ — Max Planck", font=font(SERIF_I, 11), fill=BLACK)
    d.text((300, 279), "→ quanta", font=font(SANS_B, 11), fill=RED)
    return finalize(img)


# ------------------------------------------------- 2. Weaving draft (Albers)
def image2_draft():
    rng = random.Random(20261019)
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    c = 5  # cell
    nwarp, nweft, nsh = 54, 40, 4
    # threading: point/rosepath variations, random but structured
    motifs = [[0, 1, 2, 3], [3, 2, 1, 0], [0, 1, 0, 3, 2, 3], [0, 1, 2, 3, 2, 1], [1, 0, 3, 2]]
    thread = []
    while len(thread) < nwarp:
        thread += rng.choice(motifs)
    thread = thread[:nwarp]
    # tie-up: twill-ish
    tie = [[0] * nsh for _ in range(nsh)]  # tie[treadle][shaft]
    base = rng.choice([[1, 1, 0, 0], [1, 0, 1, 1], [1, 1, 1, 0]])
    for t in range(nsh):
        for sh in range(nsh):
            tie[t][sh] = base[(sh - t) % nsh]
    tread = []
    while len(tread) < nweft:
        tread += rng.choice(motifs)
    tread = tread[:nweft]

    ox, oy = 22, 56  # drawdown origin
    # threading strip above
    ty = oy - 6 - nsh * c
    tx = ox + nwarp * c + 6
    def grid(x, y, cols, rows):
        for i in range(cols + 1):
            d.line([x + i * c, y, x + i * c, y + rows * c], fill=BLACK)
        for j in range(rows + 1):
            d.line([x, y + j * c, x + cols * c, y + j * c], fill=BLACK)
    grid(ox, ty, nwarp, nsh)
    for i, sh in enumerate(thread):
        d.rectangle([ox + i * c, ty + (nsh - 1 - sh) * c, ox + i * c + c, ty + (nsh - sh) * c], fill=BLACK)
    grid(tx, ty, nsh, nsh)
    for t in range(nsh):
        for sh in range(nsh):
            if tie[t][sh]:
                d.rectangle([tx + t * c + 1, ty + (nsh - 1 - sh) * c + 1,
                             tx + t * c + c - 1, ty + (nsh - sh) * c - 1], fill=RED)
    grid(tx, oy, nsh, nweft)
    for j, t in enumerate(tread):
        d.rectangle([tx + t * c, oy + j * c, tx + t * c + c, oy + j * c + c], fill=BLACK)
    # drawdown: warp up = black, weft up = red
    for j, t in enumerate(tread):
        for i, sh in enumerate(thread):
            col = BLACK if tie[t][sh] else RED
            d.rectangle([ox + i * c, oy + j * c, ox + i * c + c - 1, oy + j * c + c - 1], fill=col)
    d.rectangle([ox - 1, oy - 1, ox + nwarp * c, oy + nweft * c], outline=BLACK)
    # labels
    fs = font(MONO, 8)
    d.text((ox, ty - 12), "THREADING", font=fs, fill=BLACK)
    d.text((tx - 6, ty - 12), "TIE-UP", font=fs, fill=BLACK)
    d.text((ox, oy + nweft * c + 5), "DRAWDOWN", font=fs, fill=BLACK)
    lbl = Image.new("RGB", (60, 10), WHITE)
    ImageDraw.Draw(lbl).text((0, 0), "TREADLING", font=fs, fill=BLACK)
    img.paste(lbl.rotate(-90, expand=True), (tx + nsh * c + 3, oy))
    # right column text
    d.fontmode = "1"
    rx = 344
    d.text((rx, 52), "draft\nfor a\ncloth\nthat\nnever\nexisted", font=font(SERIF_I, 13), fill=BLACK, spacing=3)
    d.line([rx, 160, rx + 46, 160], fill=RED, width=2)
    d.text((rx, 168), "after\nAnni\nAlbers", font=font(SANS, 10), fill=BLACK, spacing=2)
    d.text((rx, 236), "19·X", font=font(SANS_B, 12), fill=RED)
    d.text((ox + 60, oy + nweft * c + 4), "a draft is a score; the cloth is its performance",
           font=font(SERIF_I, 11), fill=BLACK)
    d.text((ox, 6), "warp ▮ black · weft ▮ red · 4 shafts · 4 treadles", font=font(SANS, 9), fill=BLACK)
    return img.quantize(palette=_pal, dither=Image.Dither.NONE)


# ------------------------------------------------- 3. Constructivist poster
def image3_wedge():
    s = 4
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)
    S = lambda pts: [(x * s, y * s) for x, y in pts]
    # black field, white disk cut into it
    d.polygon(S([(0, 0), (250, 0), (175, 300), (0, 300)]), fill=BLACK)
    cx, cy, r = 150, 150, 78
    d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=WHITE)
    d.pieslice([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], 255, 75, fill=BLACK)
    d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], outline=BLACK, width=3 * s)
    # the red wedge comes from the right and pierces the circle
    d.polygon(S([(400, 92), (400, 172), (128, 148)]), fill=RED)
    # flying shards
    rng = random.Random(1019)
    for _ in range(9):
        x, y = rng.uniform(250, 390), rng.uniform(190, 285)
        w, h = rng.uniform(6, 26), rng.uniform(3, 8)
        a = math.radians(rng.uniform(-35, 35) - 6)
        pts = [(-w, -h), (w, -h), (w, h), (-w, h)]
        pts = [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts]
        d.polygon(S(pts), fill=rng.choice([BLACK, BLACK, RED]))
    for _ in range(6):
        x, y = rng.uniform(20, 140), rng.uniform(240, 290)
        d.rectangle([x * s, y * s, (x + rng.uniform(4, 20)) * s, (y + 3) * s], fill=WHITE)
    # typography, rotated
    def rot_text(text, fnt, fill, ang, pos, bg=(0, 0, 0, 0)):
        bb = d.textbbox((0, 0), text, font=fnt)
        t = Image.new("RGBA", (bb[2] + 4, bb[3] + 4), bg)
        ImageDraw.Draw(t).text((2 - bb[0], 2), text, font=fnt, fill=fill)
        t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
        img.paste(t, (int(pos[0] * s), int(pos[1] * s)), t)
    rot_text("ONE RED LINE", font(COND_B, 19 * s), BLACK, 6, (250, 14))
    rot_text("CUTS THE DAY", font(COND_B, 19 * s), RED, 6, (262, 42))
    rot_text("OPEN", font(COND_B, 42 * s), WHITE, 90, (10, 14))
    img = down(img)
    crisp(img).text((268, 284), "after El Lissitzky, 1919", font=font(SANS, 10), fill=BLACK)
    return finalize(img)


# ------------------------------------------------- 4. Orionids radiant chart
def image4_orionids():
    s = 3
    img = Image.new("RGB", (W * s, H * s), BLACK)
    d = ImageDraw.Draw(img)
    ra0, de0, scale = 6.2, 6.0, 5.6  # center (hours, deg), px per degree
    def P(ra, de):
        # gnomonic-ish local projection
        a, b = math.radians((ra - ra0) * 15), math.radians(de)
        c0 = math.radians(de0)
        cosc = math.sin(c0) * math.sin(b) + math.cos(c0) * math.cos(b) * math.cos(a)
        x = math.cos(b) * math.sin(a) / cosc
        y = (math.cos(c0) * math.sin(b) - math.sin(c0) * math.cos(b) * math.cos(a)) / cosc
        return ((200 - math.degrees(x) * scale) * s, (150 - math.degrees(y) * scale) * s)
    rng = random.Random(1022)
    # faint field stars
    for _ in range(260):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s)
        r = rng.choice([1, 1, 1, 2]) * s * 0.5
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    stars = {
        "Betelgeuse": (5.919, 7.41, 1.0), "Rigel": (5.242, -8.20, 1.0), "Bellatrix": (5.418, 6.35, 0.7),
        "Saiph": (5.796, -9.67, 0.6), "Alnitak": (5.679, -1.94, 0.6), "Alnilam": (5.603, -1.20, 0.65),
        "Mintaka": (5.533, -0.30, 0.6), "Meissa": (5.585, 9.93, 0.45),
        "Castor": (7.577, 31.89, 0.75), "Pollux": (7.755, 28.03, 0.85), "Alhena": (6.629, 16.40, 0.65),
        "Mebsuta": (6.732, 25.13, 0.45), "Tejat": (6.383, 22.51, 0.45), "Propus": (6.248, 22.51, 0.4),
        "Aldebaran": (4.599, 16.51, 0.95), "Elnath": (5.438, 28.61, 0.7), "Procyon": (7.655, 5.22, 0.9),
        "Sirius": (6.752, -16.72, 1.2), "Mirzam": (6.378, -17.96, 0.55),
    }
    lines = [("Betelgeuse", "Bellatrix"), ("Betelgeuse", "Alnitak"), ("Bellatrix", "Mintaka"),
             ("Alnitak", "Alnilam"), ("Alnilam", "Mintaka"), ("Alnitak", "Saiph"), ("Mintaka", "Rigel"),
             ("Betelgeuse", "Meissa"), ("Bellatrix", "Meissa"),
             ("Castor", "Mebsuta"), ("Mebsuta", "Tejat"), ("Tejat", "Propus"), ("Pollux", "Alhena"),
             ("Castor", "Pollux"), ("Sirius", "Mirzam"), ("Aldebaran", "Elnath")]
    for a, b in lines:
        (x1, y1), (x2, y2) = P(*stars[a][:2]), P(*stars[b][:2])
        n = int(math.hypot(x2 - x1, y2 - y1) / (5 * s))
        for k in range(0, n, 2):
            t0, t1 = k / n, (k + 1) / n
            d.line([x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0, x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1],
                   fill=WHITE, width=s)
    # meteors radiating from radiant (RA 6h20m, Dec +16)
    rx, ry = P(6.33, 15.8)
    for k in range(17):
        ang = rng.uniform(0, 2 * math.pi)
        r0 = rng.uniform(30, 120) * s
        L = rng.uniform(25, 70) * s
        red = k % 4 == 0
        for j in range(24):
            t0, t1 = j / 24, (j + 1) / 24
            w = max(1, int((1 + 3.5 * t1) * s * (1.2 if red else 0.8)))
            p0 = (rx + math.cos(ang) * (r0 + L * t0), ry + math.sin(ang) * (r0 + L * t0))
            p1 = (rx + math.cos(ang) * (r0 + L * t1), ry + math.sin(ang) * (r0 + L * t1))
            d.line([p0, p1], fill=RED if red else WHITE, width=w)
    d.ellipse([rx - 5 * s, ry - 5 * s, rx + 5 * s, ry + 5 * s], outline=RED, width=2 * s)
    for name, (ra, de, m) in stars.items():
        x, y = P(ra, de)
        r = (1.5 + 3.2 * m) * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED if name == "Betelgeuse" else WHITE)
    d.rectangle([0, 0, W * s, 34 * s], fill=BLACK)
    d.line([0, 34 * s, W * s, 34 * s], fill=RED, width=2 * s)
    d.rectangle([0, 282 * s, W * s, H * s], fill=BLACK)
    img = down(img)
    d = crisp(img)
    fs = font(SANS, 10)
    for name in ["Betelgeuse", "Rigel", "Aldebaran", "Sirius", "Pollux", "Procyon"]:
        x, y = P(*stars[name][:2])
        if 44 < y / s < 270:
            d.text((x / s + 7, y / s - 5), name, font=fs, fill=WHITE)
    d.text((8, 5), "ORIONIDS", font=font(COND_B, 22), fill=WHITE)
    d.text((126, 4), "peak before dawn · 21–22 Oct · ~20/hr", font=fs, fill=WHITE)
    d.text((126, 18), "dust of comet Halley, arriving at 66 km/s", font=fs, fill=RED)
    d.text((8, 286), "after moonset, look east · trails point back to ○ the radiant", font=fs, fill=WHITE)
    return finalize(img)


# ------------------------------------------------- 5. Turing pattern
def image5_turing():
    rng = np.random.default_rng(20261019)
    h, w = H, W
    U = np.ones((h, w))
    V = np.zeros((h, w))
    for _ in range(30):
        y, x = rng.integers(0, h - 8), rng.integers(0, w - 8)
        U[y:y + 6, x:x + 6] = 0.5
        V[y:y + 6, x:x + 6] = 0.25
    V += rng.random((h, w)) * 0.02
    Du, Dv, F, k = 0.16, 0.08, 0.037, 0.06
    def lap(Z):
        return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)
    yy, xx = np.mgrid[0:h, 0:w]
    # feed rate drifts across the image: spots on the left, labyrinth on the right
    Fm = 0.024 + 0.013 * (xx / w)
    km = 0.057 + 0.004 * (yy / h)
    for _ in range(9000):
        uvv = U * V * V
        U += Du * lap(U) - uvv + Fm * (1 - U)
        V += Dv * lap(V) + uvv - (Fm + km) * V
    on = V > 0.2
    out = np.zeros((h, w, 3), np.uint8) + 255
    cx, cy, r = 292, 118, 72
    disk = (xx - cx) ** 2 + (yy - cy) ** 2 < r * r
    out[on & ~disk] = BLACK
    out[on & disk] = RED
    img = Image.fromarray(out)
    d = crisp(img)
    d.rectangle([0, 268, 246, 300], fill=WHITE)
    d.line([0, 268, 246, 268], fill=BLACK)
    d.line([246, 268, 246, 300], fill=BLACK)
    d.text((6, 271), "∂v/∂t = D∇²v + uv² − (F+k)v", font=font(SANS, 11), fill=BLACK)
    d.text((6, 286), "Turing pattern · 9000 steps from 30 seeds", font=font(SANS, 10), fill=RED)
    return img.quantize(palette=_pal, dither=Image.Dither.NONE)


if __name__ == "__main__":
    import os, sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    for i, fn in enumerate([image1_planck, image2_draft, image3_wedge, image4_orionids, image5_turing], 1):
        fn().save(os.path.join(out, f"{i}.png"))
        print("wrote", i)
