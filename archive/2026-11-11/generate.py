#!/usr/bin/env python3
"""2026-11-11 — theme: signs.  Run from the repo root: python3 archive/2026-11-11/generate.py"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
K, WH, R = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = ["images", "archive/2026-11-11"]
F = "/usr/share/fonts/truetype/"
def font(name, size):
    paths = {"mono": F + "dejavu/DejaVuSansMono.ttf", "monob": F + "dejavu/DejaVuSansMono-Bold.ttf",
             "ital": F + "liberation/LiberationSerif-Italic.ttf", "serif": F + "liberation/LiberationSerif-Regular.ttf",
             "serifb": F + "liberation/LiberationSerif-Bold.ttf", "bital": F + "liberation/LiberationSerif-BoldItalic.ttf",
             "fsi": F + "freefont/FreeSerifItalic.ttf", "fs": F + "freefont/FreeSerif.ttf",
             "black": "/usr/share/fonts/opentype/inter/Inter-Black.otf"}
    return ImageFont.truetype(paths[name], size)
def canvas(bg=WH):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im); d.fontmode = "1"; return im, d
def save(im, n):
    pal = Image.new("P", (1, 1)); pal.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0, 0, 0] * 253)
    q = im.quantize(palette=pal, dither=Image.Dither.NONE)
    for o in OUT:
        os.makedirs(o, exist_ok=True); q.save(f"{o}/{n}.png")
def ctext(d, cx, y, s, f, fill):
    d.text((cx - d.textlength(s, font=f) / 2, y), s, font=f, fill=fill)

# ---------------------------------------------------------------- 1. Nova stella
def nova():
    im, d = canvas()
    stars = {  # name: (RA h, Dec deg, mag)
        "b": (0.153, 59.15, 2.3), "a": (0.675, 56.54, 2.2), "g": (0.945, 60.72, 2.4),
        "d": (1.430, 60.24, 2.7), "e": (1.907, 63.67, 3.4), "k": (0.550, 62.93, 4.2),
        "h": (0.818, 57.82, 3.4), "z": (0.617, 53.90, 3.7), "t": (1.185, 55.15, 4.3),
        "i": (2.485, 67.40, 4.5), "nova": (0.422, 64.15, -4)}
    ra0, de0, sc = 1.05, 60.3, 12.0
    def proj(ra, de):
        x = -(ra - ra0) * 15 * math.cos(math.radians(de)) * sc + 168
        y = -(de - de0) * sc + 132
        return x, y
    P = {k: proj(v[0], v[1]) for k, v in stars.items()}
    def star(x, y, r, n, fill, inner=0.38):
        pts = []
        for i in range(2 * n):
            rr = r if i % 2 == 0 else r * inner
            a = math.pi * i / n - math.pi / 2
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        d.polygon(pts, fill=fill)
    # border, woodcut style
    d.rectangle((5, 5, W - 6, H - 6), outline=K, width=2); d.rectangle((10, 10, W - 11, H - 11), outline=K)
    # dotted W
    order = ["b", "a", "g", "d", "e"]
    for a, b in zip(order, order[1:]):
        (x0, y0), (x1, y1) = P[a], P[b]; L = math.hypot(x1 - x0, y1 - y0)
        for s in np.arange(12, L - 10, 5):
            x, y = x0 + (x1 - x0) * s / L, y0 + (y1 - y0) * s / L
            d.rectangle((x, y, x + 1, y + 1), fill=K)
    for k, (ra, de, m) in stars.items():
        if k == "nova": continue
        x, y = P[k]; r = 15 - 2.6 * m
        star(x, y, r, 6 if m < 3 else 5, K)
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=WH)
    # rays + the new star
    x, y = P["nova"]
    for i in range(24):
        a = math.pi * i / 12; r0, r1 = 21, (34 if i % 2 == 0 else 27)
        d.line((x + r0 * math.cos(a), y + r0 * math.sin(a), x + r1 * math.cos(a), y + r1 * math.sin(a)), fill=R)
    star(x, y, 17, 8, R, 0.45)
    d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=WH)
    d.text((x + 40, y - 12), "I", font=font("serifb", 22), fill=K)
    d.text((x + 54, y - 7), "Nova stella", font=font("ital", 17), fill=K)
    d.text((24, 206), "CASSIOPEIA", font=font("serif", 14), fill=K)
    f = font("mono", 10)
    d.line((18, 232, W - 19, 232), fill=K)
    d.text((18, 238), "11 NOV 1572", font=f, fill=R)
    d.text((90, 238), "Tycho Brahe, walking home from the laboratory", font=f, fill=K)
    d.text((18, 251), "at Herrevad, counts one star too many. Brighter than Venus,", font=f, fill=K)
    d.text((18, 264), "then gone. Tonight Cassiopeia is overhead at nine; look for", font=f, fill=K)
    d.text((18, 277), "the gap.", font=f, fill=K)
    save(im, 1)

# ---------------------------------------------------------------- 2. 11:00
def armistice():
    im, d = canvas()
    rnd = random.Random(1918); rs = np.random.RandomState(1111)
    ctext(d, 200, 20, "THE END OF THE WAR", font("serif", 15), K)
    ctext(d, 200, 40, "a graphic record", font("ital", 13), K)
    xa0, xa1, xb0, xb1 = 14, 186, 214, 386
    ys = [84 + i * 25 for i in range(6)]
    n = xa1 - xa0
    events = [(rnd.uniform(0, n - 10), rnd.uniform(3, 11), rnd.uniform(0.5, 1.1), rnd.uniform(-4, 4)) for _ in range(34)]
    for i, y in enumerate(ys):
        sig = np.zeros(n * 2)
        t = np.arange(n * 2) / 2.0
        for (t0, amp, fr, slope) in events:
            tt = t - (t0 + slope * i + rnd.uniform(-1, 1))
            sig += np.where(tt > 0, amp * np.exp(-tt / 5.0) * np.sin(tt * fr * 2.2), 0)
        sig += rs.normal(0, 0.5, n * 2)
        sig = np.clip(sig, -11, 11)
        pts = [(xa0 + j / 2.0, y - sig[j]) for j in range(n * 2)]
        d.line(pts, fill=K)
        d.line((xb0, y, xb1, y), fill=K)
    for x0, x1 in ((xa0, xa1), (xb0, xb1)):
        for x in range(x0, x1 + 1, 43):
            d.line((x, 66, x, 70), fill=K); d.line((x, 222, x, 226), fill=K)
    d.line((200, 62, 200, 230), fill=R, width=1)
    ctext(d, 200, 236, "11:00", font("monob", 12), R)
    f = font("mono", 10)
    ctext(d, (xa0 + xa1) / 2, 236, "ONE MINUTE BEFORE", f, K)
    ctext(d, (xb0 + xb1) / 2, 236, "ONE MINUTE AFTER", f, K)
    ctext(d, 200, 264, "Six microphones of a U.S. sound-ranging set near the", f, K)
    ctext(d, 200, 277, "Moselle, 11 November 1918. Each line is one of them.", f, K)
    save(im, 2)

# ---------------------------------------------------------------- 3. summa
def summa():
    im, d = canvas(R)
    big = font("fsi", 290)
    d.text((30, -6), "∫", font=big, fill=WH)
    d.text((150, 62), "umma", font=font("fsi", 92), fill=K)
    d.text((188, 160), "y dx", font=font("fsi", 60), fill=WH)
    f = font("mono", 10)
    for i, s in enumerate(["PARIS, 11 NOVEMBER 1675", "Leibniz finds the area", "under a curve, and writes", "a tall s for the sum.", "Printed 1686. Never replaced."]):
        d.text((190, 228 + i * 13), s, font=f, fill=WH)
    save(im, 3)

# ---------------------------------------------------------------- 4. Man in hole
def vonnegut():
    im, d = canvas(K)
    rs = np.random.RandomState(1922)
    lay = Image.new("L", (W, H), 0); ld = ImageDraw.Draw(lay)
    red = Image.new("L", (W, H), 0); rd = ImageDraw.Draw(red)
    x0, x1, ym, amp = 46, 372, 142, 100
    ld.line((x0, 24, x0, 262), fill=255, width=2); ld.line((x0, ym, x1 + 10, ym), fill=255, width=2)
    def curve(dr, fn, width=3, t0=0.0, t1=1.0):
        pts = [(x0 + 6 + (x1 - x0 - 6) * t, ym - amp * fn(t)) for t in np.linspace(t0, t1, 300)]
        dr.line(pts, fill=255, width=width, joint="curve")
        return pts
    man = lambda t: 0.12 - 0.65 * math.sin(math.pi * t) ** 1.3 + 0.45 * t
    curve(ld, man)
    CP = [(0, -.86), (.07, -.86), (.09, -.5), (.19, -.5), (.21, -.14), (.31, -.14), (.33, .22), (.43, .22),
          (.45, .58), (.57, .58), (.60, -.62), (.78, -.62)]
    def cind(t):
        if t >= .78: return -0.62 + ((t - 0.78) / 0.22) ** 1.6 * 1.78
        return float(np.interp(t, [c[0] for c in CP], [c[1] for c in CP]))
    curve(rd, cind)
    # chalk texture: knock out specks
    spe = rs.rand(H, W)
    la = np.array(lay) * (spe > 0.16); ra = np.array(red) * (spe > 0.10)
    a = np.array(im); a[la > 0] = WH; a[ra > 0] = R
    im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = "1"
    fi = font("bital", 17); fs = font("ital", 14)
    d.text((22, 22), "G", font=fi, fill=WH); d.text((26, 244), "I", font=fi, fill=WH)
    d.text((30, ym - 10), "B", font=fi, fill=WH); d.text((x1 + 14, ym - 10), "E", font=fi, fill=WH)
    d.text((150, 184), "man in hole", font=fi, fill=WH)
    d.text((236, 210), "Cinderella", font=fi, fill=R)
    d.text((228, 62), "midnight", font=fs, fill=WH); 
    d.text((382, 16), "∞", font=font("fs", 20), fill=R)
    d.text((56, 20), "good fortune", font=fs, fill=WH); d.text((56, 250), "ill fortune", font=fs, fill=WH)
    f = font("mono", 10)
    d.text((14, 272), "Kurt Vonnegut, born 11 Nov 1922, on Armistice Day.", font=f, fill=WH)
    d.text((14, 285), "\"B for beginning, E for entropy.\"", font=f, fill=WH)
    return im

# ---------------------------------------------------------------- 5. Signac
def signac():
    HH = 264
    rs = np.random.RandomState(1863)
    yy, xx = np.mgrid[0:HH, 0:W].astype(float)
    hz = 150; sx, sy = 282, 84
    D = np.zeros((HH, W)); Rr = np.zeros((HH, W))
    sky = yy < hz
    ds = np.hypot(xx - sx, yy - sy)
    D = np.where(sky, 0.30 * np.clip(1 - yy / hz, 0, 1) ** 1.2 * np.clip(ds / 160, 0, 1), D)
    Rr = np.where(sky, 0.6 * np.exp(-np.maximum(ds - 26, 0) / 30), Rr)
    Rr[(ds < 26) & sky] = 1.0; D[(ds < 26) & sky] = 0
    sea = ~sky
    dep = (yy - hz) / (HH - hz)
    wave = 0.5 + 0.5 * np.sin(yy * 1.9 + np.sin(xx / 23.0) * 2)
    refl = np.exp(-((xx - sx) / (10 + 40 * dep)) ** 2)
    D = np.where(sea, (0.50 + 0.30 * dep + 0.18 * wave) * (1 - 0.9 * refl), D)
    Rr = np.where(sea, 0.9 * refl * (0.6 + 0.4 * wave), Rr)
    # headland and bell tower, far left
    hill = hz - 34 * np.exp(-((xx - 10) / 70) ** 2)
    hm = (yy > hill) & sky & (xx < 135)
    D[hm] = 1.0; Rr[hm] = 0.0
    tower = (np.abs(xx - 84) < 6) & (yy > hz - 52) & sky
    D[tower] = 1.0; Rr[tower] = 0.0
    cap = (np.hypot(xx - 84, yy - (hz - 52)) < 8) & (yy <= hz - 51)
    Rr[cap] = 1.0; D[cap] = 0
    def tri(p, q, r):
        def s(a, b): return (xx - b[0]) * (a[1] - b[1]) - (a[0] - b[0]) * (yy - b[1])
        d1, d2, d3 = s(p, q), s(q, r), s(r, p)
        return ~(((d1 < 0) | (d2 < 0) | (d3 < 0)) & ((d1 > 0) | (d2 > 0) | (d3 > 0)))
    def boat(bx, by, s, redsail):
        s1 = tri((bx + 3, by - 62 * s), (bx + 3, by - 5), (bx + 30 * s, by - 5))
        s2 = tri((bx - 4, by - 50 * s), (bx - 4, by - 5), (bx - 22 * s, by - 5))
        halo = tri((bx + 3, by - 62 * s - 8), (bx - 22 * s - 8, by), (bx + 30 * s + 8, by))
        D[halo] *= 0.0; Rr[halo] *= 0.0
        for m in (s1, s2):
            if redsail: Rr[m] = 1.0; D[m] = 0
            else: Rr[m] = 0.0; D[m] = 1.0
        hull = (np.abs(xx - bx) < 26 * s - (yy - by) * 1.2) & (yy >= by - 2) & (yy < by + 8 * s)
        D[hull] = 1.0; Rr[hull] = 0
        mast = (np.abs(xx - bx) < 1.5) & (yy > by - 66 * s) & (yy < by); D[mast] = 1; Rr[mast] = 0
        rf = (np.abs(xx - bx - 3 * np.sin(yy / 2.0)) < 14 * s) & (yy > by + 7 * s) & (yy < by + 7 * s + 46 * s)
        if redsail: Rr[rf] = 0.55; D[rf] = 0.5
        else: D[rf] = 0.95
    boat(165, 196, 1.5, True); boat(346, 184, 1.1, False)
    im, d = canvas()
    n = 0
    for row, y in enumerate(np.arange(2, hz - 1, 4)):
        for x in np.arange(2 + (row % 2) * 2, W - 1, 4):
            xi, yi = int(x), int(y); u, v = rs.rand(), rs.rand()
            c = R if u < Rr[yi, xi] else (K if v < D[yi, xi] else None)
            if c:
                d.rectangle((xi - 1, yi - 1, xi + 1, yi + 1), fill=c); n += 1
    for row, y in enumerate(np.arange(hz + 1, HH - 1, 3)):
        for x in np.arange(2 + (row % 2) * 3, W - 2, 6):
            xi, yi = int(x), int(y); u, v = rs.rand(), rs.rand()
            c = R if u < Rr[yi, xi] else (K if v < D[yi, xi] else None)
            if c:
                d.rectangle((xi - 2, yi, xi + 2, yi + 1), fill=c); n += 1
    d.rectangle((0, HH, W, H), fill=WH); d.line((0, HH, W, HH), fill=K)
    f = font("mono", 10)
    d.text((8, HH + 6), "Paul Signac, born Paris, 11 Nov 1863.", font=f, fill=K)
    d.text((8, HH + 19), f"After his Saint-Tropez harbours: {n:,} touches, two inks.", font=f, fill=K)
    save(im, 5)

if __name__ == "__main__":
    nova(); armistice(); summa(); save(vonnegut(), 4); signac()
    print("ok")
