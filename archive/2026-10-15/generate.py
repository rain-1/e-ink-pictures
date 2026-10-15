#!/usr/bin/env python3
"""Daily e-ink pictures - 2026-10-15.  Style: "almanac press".

Today's hooks: 444 years since the Gregorian calendar deleted 5-14 October
1582; Anni Albers' 'Black-White-Red' weaving; Mars closing on Jupiter in the
predawn sky (conjunction 16 Nov); Pilatre de Rozier's first human ascent
(15 Oct 1783); and a Turing reaction-diffusion study.

Pipeline: draw at 3x in pure palette colours, LANCZOS down, then a custom
quantizer (hue test for red, luminance threshold for black/white) so
antialiased black edges never turn red.
"""
import math
import random
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S = 400, 300, 3
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
FD = "/usr/share/fonts/truetype/"
SERIF = FD + "liberation/LiberationSerif-Regular.ttf"
SERIF_B = FD + "liberation/LiberationSerif-Bold.ttf"
SERIF_I = FD + "liberation/LiberationSerif-Italic.ttf"
SANS_B = FD + "dejavu/DejaVuSans-Bold.ttf"
SANS = FD + "dejavu/DejaVuSans.ttf"
MONO = FD + "dejavu/DejaVuSansMono.ttf"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."


def F(path, px):  # font sized in final pixels, for a 3x canvas
    return ImageFont.truetype(path, int(px * S))


def canvas(bg=WHITE):
    im = Image.new("RGB", (W * S, H * S), bg)
    return im, ImageDraw.Draw(im)


def quantize(im, thresh=175):
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (r + g + b) / 3
    red = (r - np.maximum(g, b)) > 90
    idx = np.where(red, 2, np.where(lum < thresh, 1, 0)).astype(np.uint8)
    out = Image.fromarray(idx, "P")
    out.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0] * 759)
    return out


def S_(*v):
    return [x * S for x in v]


def text(d, xy, s, font, fill=BLACK, anchor="la"):
    d.text((xy[0] * S, xy[1] * S), s, font=font, fill=fill, anchor=anchor)


def mark(d, label):
    """Signature: tiny red square + date, bottom-right corner."""
    f = F(FD + "dejavu/DejaVuSansMono-Bold.ttf", 7)
    text(d, (391, 293), label, f, anchor="rs")
    w = d.textlength(label, font=f) / S
    d.rectangle(S_(391 - w - 8, 288, 391 - w - 4, 292), fill=RED)


# ------------------------------------------------- 1. The ten missing days
def img_missing_days():
    im, d = canvas()
    text(d, (200, 14), "OCTOBER", F(SERIF_B, 30), anchor="mt")
    text(d, (200, 46), "·  M D L X X X I I  ·", F(SERIF, 11), anchor="mt")
    cols = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    x0, cw, y0, rh = 46, 44, 82, 34
    for i, c in enumerate(cols):
        text(d, (x0 + i * cw + cw / 2, y0 - 12), c, F(SERIF_I, 10), anchor="mm")
    d.line(S_(x0, y0 - 3, x0 + 7 * cw, y0 - 3), fill=BLACK, width=S)
    days = [1, 2, 3, 4, 15, 16, 17] + list(range(18, 32))
    fnum = F(SERIF, 20)
    for k, n in enumerate(days):
        r, c = divmod(k, 7)
        cx, cy = x0 + c * cw + cw / 2, y0 + r * rh + rh / 2
        fill = RED if n == 15 else BLACK
        text(d, (cx, cy), str(n), F(SERIF_B, 20) if n in (4, 15) else fnum, fill, "mm")
    # the seam between Thursday 4 and Friday 15
    sx = x0 + 4 * cw
    for yy in range(int(y0 + 2), int(y0 + rh - 2), 4):
        d.line(S_(sx, yy, sx, yy + 2), fill=RED, width=2 * S)
    # tiny 'ten days' bracket hanging off the seam
    d.line(S_(sx, y0 + rh - 2, sx, y0 + rh + 4), fill=RED, width=S)
    # ghost days below the grid
    gy = y0 + 3 * rh + 26
    gx0 = 62
    fg = F(SERIF, 13)
    for i, n in enumerate(range(5, 15)):
        gx = gx0 + i * 29
        text(d, (gx, gy), str(n), fg, anchor="mm")
        d.line(S_(gx - 10, gy + 1, gx + 10, gy - 1), fill=RED, width=int(1.5 * S))
    d.line(S_(46, gy - 14, 354, gy - 14), fill=BLACK, width=S)
    text(d, (200, gy + 18), "Thursday the 4th was followed by Friday the 15th.",
         F(SERIF_I, 12), anchor="mt")
    text(d, (200, gy + 34), "Ten days deleted by papal bull — 444 years ago today.",
         F(SERIF, 10), anchor="mt")
    mark(d, "15·X·26  i")
    return quantize(im)


# ------------------------------------------------- 2. Weaving draft
def img_draft():
    rng = random.Random(1582_1015)
    shafts, c = 8, 5
    ends, picks = 52, 40
    # threading: an extended point (rosepath-like) run, seeded
    seq, s, dirn = [], 0, 1
    while len(seq) < ends:
        run = rng.choice([3, 4, 5, 7, 8])
        for _ in range(run):
            seq.append(s)
            s += dirn
            if s in (shafts, -1):
                dirn = -dirn
                s += 2 * dirn
        if rng.random() < 0.6:
            dirn = -dirn
            s += 2 * dirn
            s = max(0, min(shafts - 1, s))
    thread = seq[:ends]
    # tie-up: a broken 8-shaft twill, 3/1/1/3 base rotated per treadle
    base = [1, 1, 1, 0, 1, 0, 0, 0]
    tie = [[base[(sh - t) % shafts] for t in range(shafts)] for sh in range(shafts)]
    # treadling: point run then reversed ("tromp as writ"-ish, mirrored)
    half = [thread[i % ends] for i in range(picks // 2)]
    tread = half + half[::-1]
    weft_red = [1 if (p // 4) % 5 == 2 or p in (19, 20) else 0 for p in range(picks)]

    im, d = canvas()
    gx, gy = 18, 66               # drawdown origin
    tx = gx + ends * c + 6        # treadling column x
    ty = 16                       # threading top y
    def cell(x, y, col):
        d.rectangle(S_(x, y, x + c - 1, y + c - 1), fill=col)
    # threading
    for i, sh in enumerate(thread):
        cell(gx + i * c, ty + (shafts - 1 - sh) * c, BLACK)
    d.rectangle(S_(gx - 1, ty - 1, gx + ends * c, ty + shafts * c), outline=BLACK, width=S)
    # tie-up
    for sh in range(shafts):
        for t in range(shafts):
            if tie[sh][t]:
                cell(tx + t * c, ty + (shafts - 1 - sh) * c, BLACK)
    d.rectangle(S_(tx - 1, ty - 1, tx + shafts * c, ty + shafts * c), outline=BLACK, width=S)
    # treadling
    for p, t in enumerate(tread):
        cell(tx + t * c, gy + p * c, RED if weft_red[p] else BLACK)
    d.rectangle(S_(tx - 1, gy - 1, tx + shafts * c, gy + picks * c), outline=BLACK, width=S)
    # drawdown: warp up = black; else weft colour
    for p, t in enumerate(tread):
        for i, sh in enumerate(thread):
            up = tie[sh][t]
            col = BLACK if up else (RED if weft_red[p] else WHITE)
            if col != WHITE:
                cell(gx + i * c, gy + p * c, col)
    d.rectangle(S_(gx - 1, gy - 1, gx + ends * c, gy + picks * c), outline=BLACK, width=S)
    # labels
    lx = tx + shafts * c + 6
    fs = F(SERIF_I, 9)
    text(d, (lx, ty + 1), "threading", fs)
    text(d, (lx, ty + 13), "& tie-up", fs)
    text(d, (lx, gy + 2), "treadling", fs)
    text(d, (lx, gy + 70), "after", F(SERIF, 9))
    text(d, (lx, gy + 82), "Anni", F(SERIF_B, 11))
    text(d, (lx, gy + 95), "Albers,", F(SERIF_B, 11))
    text(d, (lx, gy + 110), "Black-", F(SERIF, 10))
    text(d, (lx, gy + 122), "White-", F(SERIF, 10))
    text(d, (lx, gy + 134), "Red", F(SERIF, 10), RED)
    text(d, (lx, gy + 148), "1926/27", F(SERIF_I, 9))
    text(d, (gx, gy + picks * c + 8), "DRAFT No. 1015  ·  8 shafts, 52 ends, 40 picks",
         F(MONO, 8))
    mark(d, "15·X·26  ii")
    return quantize(im)


# ------------------------------------------------- 3. Mars chasing Jupiter
def img_chase():
    im, d = canvas()
    text(d, (16, 12), "MARS IS CATCHING JUPITER", F(SANS_B, 15))
    text(d, (16, 32), "Look east before dawn. Each red dot is one morning.", F(SERIF_I, 11))
    # Jupiter-centred frame: Mars closes from ~12 deg (today) to 1.2 deg on 16 Nov
    jx, jy = 352, 132
    px_deg = 25.0
    ang = math.radians(-12)  # slight tilt of the ecliptic
    def pos(sep):
        return jx - sep * px_deg * math.cos(ang), jy - sep * px_deg * math.sin(ang)
    # ecliptic
    a, b = pos(13.2), pos(-1.4)
    for t in np.linspace(0, 1, 90):
        if int(t * 89) % 2 == 0:
            x1 = a[0] + (b[0] - a[0]) * t; y1 = a[1] + (b[1] - a[1]) * t
            x2 = x1 + (b[0] - a[0]) / 180; y2 = y1 + (b[1] - a[1]) / 180
            d.line(S_(x1, y1, x2, y2), fill=BLACK, width=S)
    ex, ey = pos(6.0)
    text(d, (ex, ey - 10), "ecliptic", F(SERIF_I, 10), anchor="mb")
    days = 32
    labels = {0: "today · 15 Oct", 7: "22", 14: "29", 21: "5 Nov", 28: "12"}
    for k in range(days + 1):
        sep = 12.0 - (12.0 - 1.2) * k / days
        x, y = pos(sep)
        r = 4.5 if k == 0 else (2.2 if k % 7 else 3.2)
        if k < days:
            d.ellipse(S_(x - r, y - r, x + r, y + r), fill=RED)
        if k in labels:
            d.line(S_(x, y + 7, x, y + 16), fill=BLACK, width=S)
            text(d, (x, y + 18), labels[k], F(SERIF, 11), anchor="mt")
    # Jupiter with belts
    R = 14
    d.ellipse(S_(jx - R, jy - R, jx + R, jy + R), fill=BLACK)
    for off, h in ((-5, 2), (3, 3)):
        d.rectangle(S_(jx - R, jy + off, jx + R, jy + off + h), fill=WHITE)
    d.ellipse(S_(jx - R - 1, jy - R - 1, jx + R + 1, jy + R + 1), outline=BLACK, width=2 * S)
    text(d, (jx, jy - R - 6), "JUPITER", F(SANS_B, 9), anchor="mb")
    mx, my = pos(12.0)
    text(d, (mx, my - 9), "MARS", F(SANS_B, 9), RED, anchor="mb")
    # meeting point
    cx, cy = pos(1.2)
    d.ellipse(S_(cx - 5, cy - 5, cx + 5, cy + 5), outline=RED, width=2 * S)
    text(d, (cx + 4, cy + 24), "16 Nov:", F(SERIF_B, 11), anchor="lt")
    text(d, (cx + 4, cy + 37), "1.2\u00b0 apart", F(SERIF, 11), anchor="lt")
    # horizon: a low town silhouette
    rng = random.Random(1611)
    hy = 238
    pts = [(0, H)]
    x = 0
    while x < W:
        w = rng.randint(8, 30); h = rng.choice([4, 7, 10, 14, 18, 24])
        pts += [(x, hy - h), (x + w, hy - h)]
        if rng.random() < 0.15:  # a spire
            pts += [(x + w, hy - h), (x + w + 3, hy - h - 22), (x + w + 6, hy - h)]
            w += 6
        x += w
    pts += [(W, hy), (W, H)]
    d.polygon([(p[0] * S, p[1] * S) for p in pts], fill=BLACK)
    text(d, (16, 262), "E A S T", F(SANS_B, 12), WHITE)
    text(d, (16, 278), "32 mornings to go", F(SANS_B, 10), WHITE)
    f = F(MONO, 7)
    text(d, (391, 293), "15·X·26  iii", f, WHITE, "rs")
    w = d.textlength("15·X·26  iii", font=f) / S
    d.rectangle(S_(391 - w - 8, 288, 391 - w - 4, 292), fill=RED)
    return quantize(im, 140)


# ------------------------------------------------- 4. First ascent (line-screen engraving)
def img_balloon():
    SW, SH = W * S, H * S
    yy, xx = np.mgrid[0:SH, 0:SW].astype(float)
    cx, top, neck = 250 * S, 22 * S, 205 * S
    Rm = 70 * S
    # envelope profile: sphere-ish crown, cone to neck
    def radius(y):
        t = (y - top) / (neck - top)
        r = np.where(t < 0.42, Rm * np.sqrt(np.clip(1 - ((0.42 - t) / 0.42) ** 2, 0, 1)),
                     Rm * (1 - (t - 0.42) / 0.58 * 0.70))
        return np.where((t >= 0) & (t <= 1), r, 0)
    r = radius(yy)
    u = np.where(r > 0, (xx - cx) / np.maximum(r, 1), 9)
    inside = np.abs(u) <= 1
    nz = np.sqrt(np.clip(1 - u ** 2, 0, 1))
    t = (yy - top) / (neck - top)
    ny = np.where(t < 0.42, -(0.42 - t) / 0.42, 0.35)
    nrm = np.sqrt(u ** 2 + ny ** 2 + nz ** 2) + 1e-9
    L = np.array([-0.55, -0.45, 0.70]); L /= np.linalg.norm(L)
    lit = np.clip((u * L[0] + ny * L[1] + nz * L[2]) / nrm, 0, 1)
    dark = np.clip(1 - lit, 0, 1) ** 1.2 * 0.85 + 0.06
    # latitude-following lines (bowed by the curvature)
    period = 4.0 * S
    v = (yy + 9 * S * nz) / period
    fr = np.abs((v % 1) - 0.5) * 2  # 0 at line centre .. 1
    ink = inside & (fr > 1 - dark)
    # cross hatch in the deep shadow along gores
    lon = np.arcsin(np.clip(u, -1, 1))
    w2 = (lon * 40 / math.pi)
    fr2 = np.abs((w2 % 1) - 0.5) * 2
    ink |= inside & (dark > 0.62) & (fr2 > 0.82)
    # gore seams
    seam = inside & (np.abs(((lon / (math.pi / 12)) % 1) - 0.5) > 0.47)
    ink |= seam
    # red ornamental band of suns
    band = inside & (np.abs(t - 0.40) < 0.045)
    red = band & ~(np.abs(((lon / (math.pi / 8)) % 1) - 0.5) < 0.08)
    ink &= ~band
    ink |= inside & (np.abs(np.abs(t - 0.40) - 0.045) < 0.004)
    # outline
    edge = (np.abs(np.abs(u) - 1) < 2.2 * S / np.maximum(r, 1)) & (r > 0)
    ink |= edge
    a = np.full((SH, SW, 3), 255, np.uint8)
    a[ink] = 0
    a[red] = (255, 0, 0)
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    # suns on the band
    for k in range(-3, 4):
        lo = k * math.pi / 8 + math.pi / 16
        if abs(lo) > 1.35:
            continue
        yb = top + 0.40 * (neck - top)
        sx = cx + math.sin(lo) * Rm * 0.995
        rs = 3.6 * S * math.cos(lo)
        d.ellipse((sx - rs, yb - rs, sx + rs, yb + rs), fill=WHITE)
    # gallery + brazier
    gy = neck
    rn = Rm * 0.30
    d.rectangle((cx - rn - 6 * S, gy, cx + rn + 6 * S, gy + 6 * S), fill=BLACK)
    for i in range(9):
        x = cx - rn - 4 * S + i * (2 * rn + 8 * S) / 8
        d.line((x, gy + 6 * S, x, gy + 12 * S), fill=BLACK, width=S)
    d.rectangle((cx - rn - 6 * S, gy + 12 * S, cx + rn + 6 * S, gy + 14 * S), fill=BLACK)
    # tiny aeronaut
    px = cx + rn - 2 * S
    d.ellipse((px - 2 * S, gy - 5 * S, px + 2 * S, gy - 1 * S), fill=BLACK)
    # fire
    d.polygon([(cx - 6 * S, gy + 14 * S), (cx, gy + 30 * S), (cx + 6 * S, gy + 14 * S)], fill=RED)
    # tethers to the ground
    gl = 270 * S
    for ax in (-1, 1):
        d.line((cx + ax * (rn + 6 * S), gy + 14 * S, cx + ax * 70 * S, gl), fill=BLACK, width=S)
    d.line((150 * S, gl, 390 * S, gl), fill=BLACK, width=2 * S)
    for i in range(40):  # ground hatching
        x = 150 * S + i * 6 * S
        d.line((x, gl + 2 * S, x - 6 * S, gl + 8 * S), fill=BLACK, width=S)
    # crowd
    rng = random.Random(1783)
    for i in range(22):
        x = rng.uniform(158, 385) * S
        if abs(x - cx) < 40 * S:
            continue
        h = rng.uniform(7, 10) * S
        d.line((x, gl, x, gl - h), fill=BLACK, width=2 * S)
        d.ellipse((x - 1.6 * S, gl - h - 3.2 * S, x + 1.6 * S, gl - h), fill=BLACK)
    # text column
    text(d, (14, 26), "15 · X · 1783", F(SERIF_B, 15))
    d.line(S_(14, 48, 140, 48), fill=RED, width=2 * S)
    lines = ["Faubourg Saint-", "Antoine, Paris.", "", "Jean-François", "Pilâtre de Rozier",
             "steps into a gallery", "beneath a paper-and-", "silk Montgolfier and", "rises on a tether.",
             "", "Four minutes aloft.", "No human had", "ever flown before."]
    y = 56
    for ln in lines:
        fnt = F(SERIF_I, 11) if ln.startswith(("Four", "No", "ever")) else F(SERIF, 11)
        text(d, (14, y), ln, fnt, RED if ln.startswith("ever") else BLACK)
        y += 14
    text(d, (14, 262), "FIRST ASCENT", F(SANS_B, 12))
    mark(d, "15·X·26  iv")
    return quantize(im)


# ------------------------------------------------- 5. Morphogenesis (Gray-Scott)
def img_turing():
    rng = np.random.default_rng(20261015)
    h, w = 150, 200  # simulate at half res, upsample smoothly
    U = np.ones((h, w)); V = np.zeros((h, w))
    yy, xx = np.mgrid[0:h, 0:w]
    seeds = [(75, 100, 6)] + [(rng.integers(20, 130), rng.integers(20, 180), 3) for _ in range(5)]
    for sy, sx, r in seeds:
        m = (yy - sy) ** 2 + (xx - sx) ** 2 < r * r
        U[m] = 0.5; V[m] = 0.25
    V += rng.random((h, w)) * 0.01
    Du, Dv, f, k = 0.16, 0.08, 0.037, 0.060   # labyrinth / fingerprint regime
    def lap(Z):
        return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)
    # spatially varying feed: a slow gradient so the pattern changes across the card
    fmap = f + 0.012 * (xx / w - 0.5)
    for i in range(9000):
        uvv = U * V * V
        U += Du * lap(U) - uvv + fmap * (1 - U)
        V += Dv * lap(V) + uvv - (fmap + k) * V
    Vi = np.asarray(Image.fromarray((V * 255 / max(V.max(), 1e-6)).astype(np.uint8))
                    .resize((W, H), Image.BICUBIC)).astype(float) / 255
    a = np.full((H, W, 3), 255, np.uint8)
    # a red 'cell' where the same pattern is printed in red ink
    yy, xx = np.mgrid[0:H, 0:W]
    disc = (xx - 290) ** 2 + (yy - 105) ** 2 < 72 ** 2
    ring = np.abs(np.sqrt((xx - 290) ** 2 + (yy - 105) ** 2) - 72) < 1.5
    ink = Vi > 0.36
    a[ink & ~disc] = 0
    a[ink & disc] = (255, 0, 0)
    a[ring] = 0
    im = Image.fromarray(a)
    # caption plate
    big = im.resize((W * S, H * S), Image.NEAREST)
    d = ImageDraw.Draw(big)
    d.rectangle(S_(14, 248, 214, 286), fill=WHITE, outline=BLACK, width=2 * S)
    text(d, (22, 252), "MORPHOGENESIS", F(SANS_B, 12))
    text(d, (22, 270), "two chemicals, one rule, no plan", F(SERIF_I, 10))
    d.rectangle(S_(300, 284, 396, 298), fill=WHITE)
    mark(d, "15·X·26  v")
    return quantize(big)


if __name__ == "__main__":
    makers = [img_missing_days, img_draft, img_chase, img_balloon, img_turing]
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    for i, fn in enumerate(makers, 1):
        if only and str(i) not in only:
            continue
        fn().save(f"{OUT}/{i}.png")
        print("wrote", i, fn.__name__)
