"""3. H-ALPHA — Niels Bohr born 7 Oct 1885, the year Balmer published his formula.

Top: Bohr orbits (radius ∝ n²) with the n=3→2 jump. Middle: energy ladder.
Bottom: hydrogen's visible emission spectrum on a true nm scale, computed from
1/λ = R(1/2² − 1/n²). The one red line on this screen is the one red line in hydrogen.
"""
import math
import numpy as np
from PIL import Image
from common import *

RH = 1.0967758e7  # m^-1, Rydberg constant for hydrogen


def balmer(n):
    return 1e9 / (RH * (0.25 - 1 / n ** 2)) / 1.000277   # in air, as spectroscopists quote it


def make(path):
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    fT = F("InterDisplay-Black", 26)
    fm = F("Inter-Medium", 9)
    fr = F("Inter-Regular", 9)

    # ---- spectrum strip (bottom band) ------------------------------------
    sx0, sx1, sy0, sy1 = 14, 386, 206, 246
    lam0, lam1 = 360.0, 680.0

    def X(l):
        return sx0 + (l - lam0) / (lam1 - lam0) * (sx1 - sx0)

    d.rectangle([sx0, sy0, sx1, sy1], fill=BLACK)
    lines = [(n, balmer(n)) for n in range(3, 41)]
    for n, l in lines:
        x = round(X(l))
        if n == 3:
            d.rectangle([x - 1, sy0, x + 1, sy1], fill=RED)
        elif n <= 6:
            d.rectangle([x, sy0, x + (1 if n < 5 else 0), sy1], fill=WHITE)
        else:
            # the series crowds toward its limit; draw shorter, sparser strokes
            h = max(4, int((sy1 - sy0) * 6 / n))
            d.line([x, sy1 - h, x, sy1], fill=WHITE)
    lim = balmer(1e9)
    xl = round(X(lim))
    d.line([xl, sy0 - 6, xl, sy0 - 1], fill=BLACK)
    d.text((xl - 2, sy0 - 17), f"limit {lim:.1f}", font=fr, fill=BLACK)
    # nm ruler
    for l in range(360, 681, 10):
        x = round(X(l))
        t = 4 if l % 50 == 0 else 2
        d.line([x, sy1 + 1, x, sy1 + t], fill=BLACK)
        if l % 50 == 0 and l < 680:
            s = f"{l}"
            d.text((x - tw(d, s, fr) / 2, sy1 + 5), s, font=fr, fill=BLACK)
    d.text((sx1 - tw(d, "nm", fr), sy1 + 5), "nm", font=fr, fill=BLACK)
    # line labels above the strip
    names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ"}
    for n in range(3, 7):
        l = balmer(n)
        x = round(X(l))
        s = f"{names[n]} {l:.1f}"
        col = RED if n == 3 else BLACK
        d.line([x, sy0 - 5, x, sy0 - 1], fill=col)
        tx = x - tw(d, s, fm) / 2
        if n == 6:
            tx = x - 4
        d.text((tx, sy0 - 17 - (0 if n != 6 else 11)), s, font=fm, fill=col)
    # move the limit label so it doesn't collide with Hδ
    # (Hδ label sits one row higher)

    # ---- Bohr atom (left) -------------------------------------------------
    cx, cy = 92, 102
    k = 7.2                                   # r = k n² ... n=1..3 fully, 4 clipped by frame
    for n in range(1, 4):
        r = k * n * n
        if n == 4:
            # n=4 orbit as dotted arc
            for a in range(0, 360, 6):
                t = math.radians(a)
                px, py = cx + r * math.cos(t), cy + r * math.sin(t)
                if 8 < py < 196 and 4 < px < 196:
                    d.point((px, py), fill=BLACK)
        else:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=BLACK)  # proton
    # electron jumps 3 -> 2 at angle -35°, photon wiggles away
    a = math.radians(-35)
    p3 = (cx + 9 * k * math.cos(a), cy + 9 * k * math.sin(a))
    p2 = (cx + 4 * k * math.cos(a), cy + 4 * k * math.sin(a))
    d.ellipse([p3[0] - 2, p3[1] - 2, p3[0] + 2, p3[1] + 2], outline=BLACK, fill=WHITE)
    d.line([p3, p2], fill=BLACK)
    d.ellipse([p2[0] - 3, p2[1] - 3, p2[0] + 3, p2[1] + 3], fill=BLACK)
    # the photon: a red sine leaving from the landing point
    pts = []
    for i in range(0, 90):
        t = i / 89
        bx = p2[0] + 6 + t * 62
        by = p2[1] - 14 - t * 36
        nx, ny = 0.5, 0.86
        w = 3 * math.sin(t * 2 * math.pi * 5)
        pts.append((bx + nx * w, by + ny * w))
    d.line(pts, fill=RED)
    for n in (2, 3):
        r = k * n * n
        d.text((cx + r + 3, cy - 5), str(n), font=fr, fill=BLACK)

    # ---- energy ladder (middle-right) ------------------------------------
    lx0, lx1 = 214, 300
    ey = lambda n: 38 + 150 * (1 - (1 / n ** 2 - 1 / 4) / (1 - 1 / 4)) if n >= 2 else 0
    # use only n>=2 (the Balmer floor) mapped between y=188 (n=2) and y=38 (n=∞)
    def Y(n):
        e = 1 / n ** 2  # 0..0.25
        return 188 - (0.25 - e) / 0.25 * 150
    for n in list(range(2, 9)) + [1e9]:
        y = round(Y(n))
        d.line([lx0, y, lx1, y], fill=BLACK)
        lab = "∞" if n > 100 else str(n)
        if n in (2, 3, 4, 5) or n > 100:
            d.text((lx1 + 4, y - 5), lab, font=fr, fill=BLACK)
    for i, n in enumerate(range(3, 8)):
        x = lx0 + 10 + i * 15
        y1, y2 = round(Y(n)), round(Y(2))
        col = RED if n == 3 else BLACK
        d.line([x, y1, x, y2 - 4], fill=col)
        d.polygon([(x - 2, y2 - 5), (x + 2, y2 - 5), (x, y2 - 1)], fill=col)
    d.text((lx0, 192), "n = 2, the floor", font=fr, fill=BLACK)

    # ---- title & text (right) --------------------------------------------
    d.text((318, 12), "Hα", font=fT, fill=RED)
    tx = 318
    for i, t in enumerate(["Niels Bohr,", "born 7 Oct", "1885 — the", "year Balmer", "found the", "formula.",
                           "In 1913 Bohr", "told him why."]):
        d.text((tx, 46 + i * 11), t, font=fr, fill=BLACK)
    d.text((10, 8), "1/λ = R (1/2² − 1/n²)", font=F("Inter-Medium", 11), fill=BLACK)
    d.text((14, 266), "Every hydrogen atom in the universe plays this same chord. Only the first note is red.", font=fr, fill=BLACK)
    footer(d, 3, "Hydrogen, visible series, to scale")
    finish(img, path)


if __name__ == "__main__":
    make("3.png")
