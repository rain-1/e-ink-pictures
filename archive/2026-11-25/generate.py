#!/usr/bin/env python3
"""2026-11-25 — "Instruments": five pictures about machines that draw.

1. Chladni plate, mode (11,25)      — sand knows where to sit
2. Weaving draft, 8 shafts          — threading / tie-up / treadling / drawdown
3. PROUN 25.XI                      — constructivist hard-edge composition
4. Benz Patent-Motorwagen           — blueprint; Karl Benz born 25 Nov 1844
5. De Jong attractor                — one equation, three million points

Usage: python3 generate.py [outdir]
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
K, WH, R = (0, 0, 0), (255, 255, 255), (255, 0, 0)
PAL = np.array([K, WH, R], dtype=np.int32)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

FD = "/usr/share/fonts/"
INTER = FD + "opentype/inter/Inter-%s.otf"
MONO = FD + "truetype/jetbrains-mono/JetBrainsMono-%s.ttf"
SERIF = FD + "truetype/crosextra/Caladea-%s.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def snap(img, gain=1.0):
    """Nearest-palette snap (no dither) -> mode P image at 400x300.
    gain > 1 keeps thin light lines alive on a black ground."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    a = np.asarray(img.convert("RGB"), dtype=np.int32)
    a = np.clip(a * gain, 0, 255).astype(np.int32)
    d = ((a[:, :, None, :] - PAL[None, None, :, :]) ** 2).sum(-1)
    return to_p(d.argmin(-1).astype(np.uint8))


def to_p(idx):
    im = Image.fromarray(idx, "P")
    im.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0] * (253 * 3))
    return im


def save(im, n):
    im.save(os.path.join(OUT, "%d.png" % n), optimize=True)


def spaced(d, xy, text, f, fill, track=0.0, anchor="l"):
    """Draw letter-spaced text. anchor l/r/m."""
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    x, y = xy
    if anchor == "r":
        x -= total
    elif anchor == "m":
        x -= total / 2
    for c, w in zip(text, widths):
        d.text((x, y), c, font=f, fill=fill)
        x += w + track
    return total


# ---------------------------------------------------------------- 1. Chladni
def chladni():
    rng = np.random.default_rng(1125)
    idx = np.zeros((H, W), dtype=np.uint8)  # black plate
    P0, PS = 10, 280  # square plate origin / size
    m, n = 11, 25

    def u(x, y):
        return (np.cos(n * np.pi * x) * np.cos(m * np.pi * y)
                - np.cos(m * np.pi * x) * np.cos(n * np.pi * y))

    # sand: rejection-sample grains that settle where the plate is still
    N = 900000
    x, y = rng.random(N), rng.random(N)
    amp = np.abs(u(x, y))
    keep = rng.random(N) < np.exp(-(amp / 0.11) ** 2) * 0.55
    px = (P0 + x[keep] * PS).astype(int)
    py = (P0 + y[keep] * PS).astype(int)
    idx[py, px] = 1
    # a few stray grains still bouncing on the loud parts
    stray = rng.random(N) < 0.0025
    idx[(P0 + y[stray] * PS).astype(int), (P0 + x[stray] * PS).astype(int)] = 1

    im = to_p(idx)
    d = ImageDraw.Draw(im)
    # plate edge + the bow
    d.rectangle([P0 - 3, P0 - 3, P0 + PS + 2, P0 + PS + 2], outline=1)
    d.line([P0 + PS + 3, 150, 399, 108], fill=2, width=2)   # violin bow, red
    d.ellipse([P0 + PS // 2 - 3, P0 + PS // 2 - 3, P0 + PS // 2 + 3, P0 + PS // 2 + 3], fill=2)

    tx = 304
    d.text((tx, 12), "25", font=font(INTER % "Black", 54), fill=1)
    d.text((tx + 2, 70), "11", font=font(INTER % "Black", 54), fill=2)
    f = font(MONO % "Medium", 9)
    for i, s in enumerate(["cos 25πx cos 11πy", " − cos 11πx cos 25πy", "   = 0"]):
        d.text((tx - 4, 170 + i * 12, ), s, font=font(MONO % "Regular", 8), fill=1)
    d.text((tx, 222), "CHLADNI", font=font(INTER % "Bold", 13), fill=1)
    for i, s in enumerate(["sand settles", "where the plate", "stands still", "Klangfigur, 1787"]):
        d.text((tx, 240 + i * 12), s, font=f, fill=2 if i == 3 else 1)
    save(im, 1)


# ---------------------------------------------------------------- 2. Weaving draft
def weave():
    C = 5                       # cell px
    NW, NP, NS = 62, 42, 8      # warp ends, picks, shafts
    # threading: an advancing point twill whose reversal points are the date digits 2,0,2,6,1,1,2,5
    digits = [2, 0, 2, 6, 1, 1, 2, 5]
    thread, s, direction, k = [], 0, 1, 0
    run = 0
    while len(thread) < NW:
        thread.append(s % NS)
        run += 1
        if run >= 4 + digits[k % 8]:
            direction, run, k = -direction, 0, k + 1
        s += direction
    # tie-up: 3/1/1/3 twill
    base = [1, 1, 1, 0, 1, 0, 0, 0]
    tie = [[base[(sh - t) % NS] for t in range(NS)] for sh in range(NS)]  # tie[shaft][treadle]
    # treadling: "tromp as writ" — treadle in the order the warp is threaded
    tread = [thread[(i * 1) % NW] for i in range(NP)]

    im = Image.new("P", (W, H), 1)
    im.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0] * (253 * 3))
    d = ImageDraw.Draw(im)
    gap = 7
    tw, th = NW * C, NS * C
    X0 = (W - (tw + gap + th)) // 2
    Y0 = 12
    DX, DY = X0, Y0 + th + gap          # drawdown origin
    TX = X0 + tw + gap                  # tie-up / treadling x

    def grid(x0, y0, nx, ny):
        for i in range(nx + 1):
            for j in range(ny + 1):
                d.point((x0 + i * C, y0 + j * C), fill=0)
        d.rectangle([x0, y0, x0 + nx * C, y0 + ny * C], outline=0)

    grid(X0, Y0, NW, NS)
    grid(TX, Y0, NS, NS)
    grid(TX, DY, NS, NP)
    for i, sh in enumerate(thread):     # shaft 1 at the bottom
        y = Y0 + (NS - 1 - sh) * C
        d.rectangle([X0 + i * C + 1, y + 1, X0 + i * C + C - 1, y + C - 1], fill=0)
    for sh in range(NS):
        for t in range(NS):
            if tie[sh][t]:
                y = Y0 + (NS - 1 - sh) * C
                d.rectangle([TX + t * C + 1, y + 1, TX + t * C + C - 1, y + C - 1], fill=2)
    for p, t in enumerate(tread):
        d.rectangle([TX + t * C + 1, DY + p * C + 1, TX + t * C + C - 1, DY + p * C + C - 1], fill=0)

    # drawdown: black warp; weft is white with a red band woven through the middle third
    for p, t in enumerate(tread):
        weft = 2 if (NP // 3 <= p < 2 * NP // 3) else 1
        for i, sh in enumerate(thread):
            col = 0 if tie[sh][t] else weft
            d.rectangle([DX + i * C, DY + p * C, DX + i * C + C - 1, DY + p * C + C - 1], fill=col)
    d.rectangle([DX - 1, DY - 1, DX + tw, DY + NP * C], outline=0)

    f = font(MONO % "Medium", 8)
    d.text((X0, 1), "THREADING  2·0·2·6·1·1·2·5", font=f, fill=0)
    d.text((TX, 1), "TIE-UP", font=f, fill=2)
    lab = Image.new("L", (120, 10), 0)
    ImageDraw.Draw(lab).text((0, 0), "TREADLING — tromp as writ", font=f, fill=255)
    lab = lab.rotate(-90, expand=True).point(lambda v: 255 if v > 110 else 0)
    im.paste(0, (TX + th + 3, DY), lab)
    d.text((X0, DY + NP * C + 3), "DRAWDOWN · 8 SHAFTS · cloth = treadling ∘ tie-up⁻¹ ∘ threading",
           font=font(MONO % "Medium", 8), fill=0)
    save(im, 2)


# ---------------------------------------------------------------- 3. Proun
def proun():
    S = 4
    im = Image.new("RGB", (W * S, H * S), WH)
    d = ImageDraw.Draw(im)

    def P(pts):
        return [(x * S, y * S) for x, y in pts]

    def rot(pts, ang, cx, cy):
        a = math.radians(ang)
        return [(cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a),
                 cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a)) for x, y in pts]

    def bar(cx, cy, w, h, ang, fill):
        pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
        d.polygon(P(rot(pts, ang, cx, cy)), fill=fill)

    A = -24
    # great black disc, cut by the frame
    d.ellipse(P([(175, 20), (455, 300)]), fill=K)
    # white ring inside it
    d.ellipse(P([(262, 107), (368, 213)]), outline=WH, width=3 * S)
    # the red wedge drives in from the left
    d.polygon(P([(-10, 205), (8, 78), (292, 152)]), fill=R)
    # planks
    bar(118, 232, 250, 16, A, K)
    bar(150, 262, 150, 5, A, K)
    bar(60, 40, 120, 5, A, K)
    bar(252, 66, 190, 9, A, WH)
    bar(232, 84, 110, 3, A, WH)
    bar(330, 245, 120, 22, A, R)
    bar(352, 268, 60, 5, A, WH)
    # hatched plank
    for i in range(14):
        bar(40 + i * 7 * math.cos(math.radians(A)), 270 + i * 7 * math.sin(math.radians(A)), 2.5, 34, A, K)
    # small squares & orbiting dots
    bar(128, 48, 26, 26, A, R)
    bar(162, 30, 11, 11, A, K)
    d.ellipse(P([(18, 232), (36, 250)]), fill=K)
    d.ellipse(P([(374, 20), (386, 32)]), fill=R)
    d.line(P([(0, 300), (190, 0)]), fill=K, width=S)
    d.line(P([(30, 300), (212, 12)]), fill=K, width=S // 2)

    # type, set on the diagonal
    def rtext(s, f, fill, cx, cy, ang, track=0):
        tmp = Image.new("L", (1400, 500), 0)
        td = ImageDraw.Draw(tmp)
        w = spaced(td, (10, 10), s, f, 255, track)
        bb = tmp.getbbox()
        tmp = tmp.crop(bb).rotate(-ang, expand=True, resample=Image.BICUBIC)
        im.paste(fill, (int(cx * S - tmp.width / 2), int(cy * S - tmp.height / 2)), tmp)

    rtext("25", font(INTER % "Black", 96 * S), WH, 318, 152, A)
    rtext("XI", font(INTER % "Black", 40 * S), WH, 100, 148, 14.6)
    rtext("ПРОУН", font(INTER % "Bold", 12 * S), K, 240, 250, A, track=5 * S)
    rtext("MMXXVI", font(INTER % "Medium", 8 * S), K, 70, 20, A, track=3 * S)
    save(snap(im), 3)


# ---------------------------------------------------------------- 4. Benz Patent-Motorwagen
def benz():
    S = 4
    im = Image.new("RGB", (W * S, H * S), K)
    d = ImageDraw.Draw(im)

    def L(pts, fill=WH, w=1.0):
        d.line([(x * S, y * S) for x, y in pts], fill=fill, width=max(S - 1, int(w * S)), joint="curve")

    def C(cx, cy, r, fill=None, outline=WH, w=1.0):
        d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill, outline=outline,
                  width=max(1, int(w * S)))

    # faint drafting grid: dotted
    for gx in range(0, W, 20):
        for gy in range(0, H, 20):
            d.rectangle([gx * S, gy * S, gx * S + S - 1, gy * S + S - 1], fill=WH)

    GY = 222                      # ground line
    RW, FW = 74, 40               # wheel radii (px): rear, front
    RX, FX = 262, 92
    RYc, FYc = GY - RW, GY - FW

    def wheel(cx, cy, r, spokes):
        C(cx, cy, r, w=2.2)
        C(cx, cy, r - 4, w=0.6)
        for i in range(spokes):
            a = 2 * math.pi * i / spokes + 0.13
            # wire spokes, laced slightly tangentially like a bicycle wheel
            off = 0.22 if i % 2 else -0.22
            L([(cx + 5 * math.cos(a + off * 4), cy + 5 * math.sin(a + off * 4)),
               (cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a))], w=0.5)
        C(cx, cy, 6, fill=K, w=1.2)
        C(cx, cy, 2, fill=WH)

    # frame tubes (drawn before wheels so wheels overlay)
    L([(FX + 6, FYc - 34), (150, 150), (300, 150)], w=2.0)          # main tube
    L([(150, 150), (178, RYc + 30), (RX, RYc)], w=1.4)              # lower stay to axle
    L([(300, 150), (RX, RYc)], w=1.4)
    # front fork & tiller
    L([(FX, FYc), (FX + 6, FYc - 34), (FX + 10, FYc - 62)], w=2.0)
    L([(FX + 10, FYc - 62), (FX + 10, 96), (136, 90)], w=1.2)       # steering column to tiller
    C(140, 89, 3, fill=WH)
    # elliptic leaf spring + bench seat
    for k in (0, 1):
        pts = [(168 + t * 92 / 20, 136 + (1 if k else -1) * 9 * math.sin(math.pi * t / 20)) for t in range(21)]
        L(pts, w=0.9)
    L([(160, 124), (268, 124)], w=3.0)                               # seat board
    L([(268, 124), (276, 92), (272, 90)], w=1.6)                     # backrest
    L([(160, 124), (156, 110)], w=1.6)
    L([(196, 124), (196, 112), (252, 112), (252, 124)], w=0.8)       # cushion
    # engine: horizontal single cylinder behind the seat, big horizontal flywheel
    d.rectangle([286 * S, 128 * S, 330 * S, 146 * S], outline=WH, width=int(1.2 * S))
    for fx in range(290, 330, 5):                                   # cooling ribs
        L([(fx, 129), (fx, 145)], w=0.5)
    L([(330, 137), (348, 137)], w=1.4)                               # connecting rod
    L([(308, 128), (308, 108)], w=1.0)                               # evaporative cooler pipe
    d.rectangle([298 * S, 92 * S, 320 * S, 108 * S], outline=WH, width=int(1.0 * S))
    d.ellipse([292 * S, 166 * S, 372 * S, 180 * S], outline=WH, width=int(1.8 * S))   # flywheel, edge-on ellipse
    d.ellipse([324 * S, 170 * S, 340 * S, 176 * S], outline=WH, width=int(0.8 * S))
    L([(332, 146), (332, 170)], w=1.6)                               # crank shaft (vertical)
    # belt to countershaft, chain to wheel
    C(226, 164, 9, w=1.0)
    L([(226, 155), (330, 131)], w=0.5)
    L([(226, 173), (300, 172)], w=0.5)
    for a, b in (((226, 157), (RX, RYc - 14)), ((226, 171), (RX, RYc + 14))):
        n = 22
        for i in range(n):                                           # chain = dashes
            if i % 2 == 0:
                x0 = a[0] + (b[0] - a[0]) * i / n; y0 = a[1] + (b[1] - a[1]) * i / n
                x1 = a[0] + (b[0] - a[0]) * (i + 1) / n; y1 = a[1] + (b[1] - a[1]) * (i + 1) / n
                L([(x0, y0), (x1, y1)], w=0.8)
    C(RX, RYc, 14, w=0.8)                                            # sprocket
    wheel(RX, RYc, RW, 20)
    wheel(FX, FYc, FW, 14)
    # brake lever
    L([(170, 124), (150, 84)], w=1.0)
    C(150, 83, 2.5, fill=WH)

    # ground
    L([(14, GY + 1), (386, GY + 1)], w=1.0)
    for gx in range(18, 386, 8):
        L([(gx, GY + 8), (gx + 5, GY + 2)], w=0.4)

    # red dimensions
    def dim_h(x0, x1, y, label):
        L([(x0, y), (x1, y)], fill=R, w=0.7)
        for x, sgn in ((x0, 1), (x1, -1)):
            d.polygon([(x * S, y * S), ((x + 6 * sgn) * S, (y - 2.2) * S), ((x + 6 * sgn) * S, (y + 2.2) * S)], fill=R)
            L([(x, y - 5), (x, y + 5)], fill=R, w=0.5)
        f = font(MONO % "Bold", 10 * S)
        tw = d.textlength(label, font=f)
        cx = (x0 + x1) / 2 * S
        d.rectangle([cx - tw / 2 - 3 * S, (y - 6) * S, cx + tw / 2 + 3 * S, (y + 6) * S], fill=K)
        d.text((cx - tw / 2, (y - 7) * S), label, font=f, fill=R)

    dim_h(FX, RX, GY + 20, "1450")
    L([(FX, FYc), (FX, GY + 24)], fill=R, w=0.4)
    L([(RX, RYc), (RX, GY + 24)], fill=R, w=0.4)
    # rear wheel diameter, vertical
    xr = 352
    L([(xr, GY - 2 * RW), (xr, GY)], fill=R, w=0.7)
    L([(xr - 5, GY - 2 * RW), (xr + 5, GY - 2 * RW)], fill=R, w=0.5)
    L([(RX, GY - 2 * RW), (xr + 5, GY - 2 * RW)], fill=R, w=0.3)
    lab = Image.new("L", (60 * S, 13 * S), 0)
    ImageDraw.Draw(lab).text((2 * S, 0), "Ø 1125", font=font(MONO % "Bold", 10 * S), fill=255)
    lab = lab.rotate(90, expand=True)
    im.paste(R, ((xr + 4) * S, (GY - RW - 26) * S), lab)

    # title block
    f1 = font(INTER % "ExtraBold", 17 * S)
    spaced(d, (16 * S, 12 * S), "PATENT-MOTORWAGEN", f1, WH, track=1.5 * S)
    d.text((16 * S, 34 * S), "DRP 37435 · MANNHEIM 1886 · 954 cc · 16 km/h",
           font=font(MONO % "Medium", 9 * S), fill=WH)
    d.rectangle([14 * S, 262 * S, 386 * S, 288 * S], outline=WH, width=S)
    L([(250, 262), (250, 288)], w=1)
    L([(310, 262), (310, 288)], w=1)
    d.text((20 * S, 268 * S), "KARL BENZ   * 25. XI. 1844", font=font(MONO % "Bold", 10 * S), fill=WH)
    d.text((257 * S, 263 * S), "Bl. 4/5", font=font(MONO % "Medium", 9 * S), fill=WH)
    d.text((257 * S, 275 * S), "M 1:20", font=font(MONO % "Bold", 9 * S), fill=R)
    d.text((316 * S, 263 * S), "25.11.2026", font=font(MONO % "Medium", 9 * S), fill=WH)
    d.text((316 * S, 275 * S), "182 years", font=font(MONO % "Medium", 9 * S), fill=WH)
    save(snap(im, gain=1.7), 4)


# ---------------------------------------------------------------- 5. De Jong attractor
def attractor():
    a, b, c, dd = 1.641, 1.902, 0.316, 1.525      # Peter de Jong map
    rng = np.random.default_rng(25)
    x = rng.uniform(-1, 1, 60000)
    y = rng.uniform(-1, 1, 60000)
    SS = 2
    hist = np.zeros((H * SS, W * SS))
    for i in range(160):
        x, y = np.sin(a * y) - np.cos(b * x), np.sin(c * x) - np.cos(dd * y)
        if i < 20:
            continue
        # rotate 90deg-ish fit: map [-2,2]^2 into frame with margins
        if i == 20:
            x0, x1, y0, y1 = x.min(), x.max(), y.min(), y.max()
        px = ((x - x0) / (x1 - x0) * (W - 24) + 11) * SS
        py = ((y - y0) / (y1 - y0) * (H - 62) + 10) * SS
        np.add.at(hist, (py.astype(int), px.astype(int)), 1)
    hist = hist.reshape(H, SS, W, SS).sum((1, 3))
    t = np.log1p(hist)
    t = t / t.max()
    ink = np.clip(t ** 0.9 * 1.25, 0, 1)             # 0 = paper, 1 = full ink
    hot = t > 0.70                                    # densest folds glow red

    # Floyd–Steinberg on the ink channel (serpentine)
    g = ink.copy()
    out = np.zeros((H, W), dtype=np.uint8)
    for yy in range(H):
        rng_x = range(W) if yy % 2 == 0 else range(W - 1, -1, -1)
        sgn = 1 if yy % 2 == 0 else -1
        for xx in rng_x:
            old = g[yy, xx]
            new = 1.0 if old >= 0.5 else 0.0
            out[yy, xx] = 1 if new else 0
            e = old - new
            if 0 <= xx + sgn < W:
                g[yy, xx + sgn] += e * 7 / 16
            if yy + 1 < H:
                if 0 <= xx - sgn < W:
                    g[yy + 1, xx - sgn] += e * 3 / 16
                g[yy + 1, xx] += e * 5 / 16
                if 0 <= xx + sgn < W:
                    g[yy + 1, xx + sgn] += e * 1 / 16
    idx = np.where(out == 1, np.where(hot, 2, 0), 1).astype(np.uint8)
    im = to_p(idx)
    d = ImageDraw.Draw(im)
    f = font(SERIF % "Italic", 11)
    d.text((10, 270), "x′ = sin(ay) − cos(bx)", font=f, fill=0)
    d.text((10, 283), "y′ = sin(cx) − cos(dy)", font=f, fill=0)
    d.text((390, 284), "a 1.641  b 1.902  c 0.316  d 1.525", font=font(MONO % "Medium", 8), fill=2, anchor="ra")
    save(im, 5)


if __name__ == "__main__":
    random.seed(20261125)
    chladni()
    weave()
    proun()
    benz()
    attractor()
    print("done ->", OUT)
