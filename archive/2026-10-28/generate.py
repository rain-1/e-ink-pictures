#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-28 (Wednesday).

Theme: "thin things that held".
  1. In hoc signo   — Milvian Bridge, 28 Oct 312: the sign seen above the sun.
  2. 3/32 inch      — Statue of Liberty dedicated 28 Oct 1886; her copper skin,
                      drawn at actual size on this 4.2" screen (≈4.72 px/mm).
  3. 14:04 GMT      — 28 Oct 1962: Radio Moscow reads Khrushchev's letter on air.
  4. Tabula rasa    — John Locke d. 28 Oct 1704: "white paper, void of all characters".
  5. (untitled)     — first frost: diffusion-limited aggregation from the sill.

Run from the repo root:  python3 archive/2026-10-28/generate.py
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F = "/usr/share/fonts/truetype/"
MONO = F + "jetbrains-mono/JetBrainsMono-Regular.ttf"
MONO_B = F + "jetbrains-mono/JetBrainsMono-Bold.ttf"
MONO_XB = F + "jetbrains-mono/JetBrainsMono-ExtraBold.ttf"
SERIF = F + "freefont/FreeSerif.ttf"
SERIF_B = F + "freefont/FreeSerifBold.ttf"
SERIF_I = F + "liberation/LiberationSerif-Italic.ttf"
SERIF_BI = F + "freefont/FreeSerifBoldItalic.ttf"
INTER_XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"

OUT_DIRS = ["images", "archive/2026-10-28"]


def font(path, size):
    return ImageFont.truetype(path, size)


def _pal(colors):
    p = Image.new("P", (1, 1))
    flat = []
    for c in colors:
        flat += list(c)
    p.putpalette(flat + [0, 0, 0] * (256 - len(colors)))
    return p


PAL3 = _pal([WHITE, BLACK, RED])
PAL2 = _pal([WHITE, BLACK])


def to3(img, dither=False):
    """Quantize an RGB image (any size) into the exact 3-colour palette."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL3, dither=d)


def dither_bw(gray):
    """Floyd–Steinberg a float array (0 black .. 1 white) to pure black/white RGB."""
    g = Image.fromarray(np.clip(gray * 255, 0, 255).astype(np.uint8), "L").convert("RGB")
    q = g.quantize(palette=PAL2, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    return q


def mask_layer(draw_fn):
    """Draw at 3x into an L mask, return a 1x boolean mask (crisp edges)."""
    m = Image.new("L", (W * SS, H * SS), 0)
    draw_fn(ImageDraw.Draw(m), SS)
    m = m.resize((W, H), Image.LANCZOS)
    return np.array(m) > 110


def paint(img, mask, color):
    a = np.array(img.convert("RGB"))
    a[mask] = color
    return Image.fromarray(a, "RGB")


def save(img, n):
    img = to3(img)
    assert img.size == (W, H)
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        img.save(os.path.join(d, f"{n}.png"))


def value_noise(h, w, rng, octaves=((4, 1.0), (8, 0.5), (16, 0.25), (32, 0.12))):
    out = np.zeros((h, w))
    for cells, amp in octaves:
        g = rng.random((cells + 1, int(cells * w / h) + 2))
        im = Image.fromarray((g * 255).astype(np.uint8), "L").resize((w, h), Image.BICUBIC)
        out += amp * (np.array(im) / 255.0 - 0.5)
    return out


# ---------------------------------------------------------------- 1. In hoc signo
def in_hoc_signo():
    rng = np.random.default_rng(312)
    horizon = 214  # waterline at 1x
    deck = 170
    sx, sy = 236, 150  # sun, just above the parapet
    y, x = np.mgrid[0:H, 0:W].astype(float)

    # sky: dark at the zenith, pale toward the horizon, a glow around the sun
    t = np.clip(y / horizon, 0, 1)
    sky = 0.0 + 0.62 * t ** 1.8
    r = np.hypot(x - sx, (y - sy) * 1.25)
    sky += 0.5 * np.exp(-(r / 45) ** 2) + 0.18 * np.exp(-(r / 150) ** 2)
    # long horizontal cloud bars
    n = value_noise(H, W, rng)
    bars = np.sin(y * 0.33 + 6 * n) * 0.5 + 0.5
    sky -= 0.28 * (bars > 0.82) * np.clip(t * 1.4, 0, 1)
    sky = np.where(r < 13, 1.0, sky)

    # water: the sky mirrored, darker, broken into horizontal ripples
    yy = np.clip(2 * horizon - y, 0, H - 1).astype(int)
    shift = (np.sin(y * 1.7) * 3 + np.sin(y * 0.6 + 1) * 4).astype(int)
    xs = np.clip(x.astype(int) + shift, 0, W - 1)
    water = sky[yy, xs] * 0.55
    # the sun's glitter path
    glitter = (np.abs(x - sx) < 6 + (y - horizon) * 0.35) & (rng.random((H, W)) < 0.45)
    water = np.where(glitter & (y > horizon), 1.0, water)
    tone = np.where(y < horizon, sky, water)
    img = dither_bw(tone)

    # the bridge: deck, parapet, piers and five arches (Ponte Milvio has odd spans)
    arches = [(14, 24), (82, 30), (158, 34), (238, 30), (300, 24), (382, 26)]  # (centre x, radius)
    spring = horizon + 4

    def bridge(d, s):
        d.rectangle([0, deck * s, W * s, (horizon) * s], fill=255)
        d.rectangle([0, (deck - 8) * s, W * s, deck * s], fill=255)
        for i in range(0, W, 9):  # parapet crenels
            d.rectangle([i * s, (deck - 12) * s, (i + 5) * s, (deck - 7) * s], fill=255)
        # a small tower at the north end
        d.rectangle([318 * s, (deck - 46) * s, 352 * s, deck * s], fill=255)
        d.polygon([(314 * s, (deck - 46) * s), (356 * s, (deck - 46) * s), (335 * s, (deck - 62) * s)], fill=255)
        for cx, rr in arches:
            d.ellipse([(cx - rr) * s, (spring - rr) * s, (cx + rr) * s, (spring + rr) * s], fill=0)

    bmask = mask_layer(bridge)
    tower_window = mask_layer(lambda d, s: d.rectangle([332 * s, (deck - 34) * s, 338 * s, (deck - 22) * s], fill=255))
    img = paint(img, bmask, BLACK)
    img = paint(img, tower_window, RED)

    # reflection of the bridge, rippled
    ref = np.zeros((H, W), bool)
    for yy_ in range(horizon, H):
        src = 2 * horizon - yy_
        if 0 <= src < H:
            row = bmask[src]
            k = int(math.sin(yy_ * 1.7) * 3 + math.sin(yy_ * 0.6 + 1) * 4)
            ref[yy_] = np.roll(row, k) & (rng.random(W) < 0.92 - 0.004 * (yy_ - horizon))
    img = paint(img, ref, BLACK)

    # the sign above the sun: ☧ drawn as strokes
    cx, cy, L = sx, 64, 36

    def chirho(d, s):
        w = 7 * s
        d.line([((cx - L * 0.7) * s, (cy - L * 0.55) * s), ((cx + L * 0.7) * s, (cy + L * 0.55) * s)], fill=255, width=w)
        d.line([((cx + L * 0.7) * s, (cy - L * 0.55) * s), ((cx - L * 0.7) * s, (cy + L * 0.55) * s)], fill=255, width=w)
        d.line([(cx * s, (cy - L) * s), (cx * s, (cy + L) * s)], fill=255, width=w)
        # the loop of the rho
        d.ellipse([(cx - 1) * s, (cy - L - 1) * s, (cx + 21) * s, (cy - L + 21) * s], outline=255, width=w)
        # rays
        for k in range(24):
            a = k * math.tau / 24
            r0, r1 = 50, 56 + (5 if k % 2 == 0 else 0)
            d.line([((cx + r0 * math.cos(a)) * s, (cy + r0 * math.sin(a)) * s),
                    ((cx + r1 * math.cos(a)) * s, (cy + r1 * math.sin(a)) * s)], fill=255, width=2 * s)

    halo = mask_layer(lambda d, s: d.ellipse([(cx - 45) * s, (cy - 45) * s, (cx + 45) * s, (cy + 45) * s], fill=255))
    img = paint(img, halo & ~mask_layer(chirho), BLACK)
    img = paint(img, mask_layer(chirho), RED)

    # type
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    f = font(SERIF_B, 15)
    txt = "I N   H O C   S I G N O   V I N C E S"
    dr.rectangle([0, 0, 118, 116], fill=BLACK)
    dr.text((14, 12), "IN HOC", font=font(SERIF_B, 20), fill=WHITE)
    dr.text((14, 33), "SIGNO", font=font(SERIF_B, 20), fill=WHITE)
    dr.text((14, 54), "VINCES", font=font(SERIF_B, 20), fill=WHITE)
    dr.text((14, 82), "in this sign,", font=font(SERIF_I, 13), fill=WHITE)
    dr.text((14, 96), "conquer", font=font(SERIF_I, 13), fill=WHITE)
    m = font(MONO, 9)
    dr.rectangle([0, 287, W, H], fill=BLACK)
    dr.text((6, 288), "PONS MILVIUS · TIBER · 28·X·312", font=m, fill=WHITE)
    dr.text((W - 6, 288), "1714 years", font=m, fill=RED, anchor="ra")
    return img


# ---------------------------------------------------------------- 2. 3/32 inch
PX_PER_MM = 400 / 84.8  # Waveshare 4.2" active area is 84.8 x 63.6 mm


def three_32():
    img = Image.new("RGB", (W, H), WHITE)
    skin_mm = 3 / 32 * 25.4  # 2.38 mm
    t = skin_mm * PX_PER_MM  # ~11.2 px

    # the skin: a gently curving band across the screen at true thickness
    def curve(xx):
        return 150 + 26 * math.sin((xx - 40) / 120) - 0.00025 * (xx - 200) ** 2

    def skin(d, s):
        pts_top = [(xx * s, curve(xx) * s) for xx in range(-5, W + 6, 2)]
        pts_bot = [(xx * s, (curve(xx) + t) * s) for xx in range(W + 5, -6, -2)]
        d.polygon(pts_top + pts_bot, fill=255)

    smask = mask_layer(skin)

    # outer face hatching (patina side, above): fine engraved lines
    def hatch(d, s):
        for k in range(-300, 500, 7):
            d.line([(k * s, 0), ((k + 160) * s, 160 * s)], fill=255, width=1 * s)

    above = np.zeros((H, W), bool)
    for xx in range(W):
        above[: int(curve(xx)) - 1, xx] = True
    # fade the hatching out toward the top
    yy = np.arange(H)[:, None]
    hm = mask_layer(hatch) & above & ((curve(200) - yy) < 46)
    img = paint(img, hm, BLACK)
    img = paint(img, smask, RED)

    # saddle: a U-strap riveted to the inner face, wrapping a flat armature bar
    bx = 236  # bar centre x
    by = curve(bx) + t + 30
    def saddle(d, s):
        y0 = curve(bx) + t
        # the feet
        d.rectangle([(bx - 44) * s, y0 * s, (bx - 14) * s, (y0 + 5) * s], fill=255)
        d.rectangle([(bx + 14) * s, y0 * s, (bx + 44) * s, (y0 + 5) * s], fill=255)
        # the U
        d.rounded_rectangle([(bx - 19) * s, y0 * s, (bx + 19) * s, (y0 + 48) * s], radius=12 * s, fill=255)
        d.rounded_rectangle([(bx - 14) * s, (y0 - 2) * s, (bx + 14) * s, (y0 + 43) * s], radius=9 * s, fill=0)

    def bar(d, s):
        y0 = curve(bx) + t
        d.rectangle([(bx - 10) * s, (y0 + 10) * s, (bx + 10) * s, (y0 + 42) * s], fill=255)

    img = paint(img, mask_layer(saddle), BLACK)
    # the bar in section, cross-hatched (iron)
    barm = mask_layer(bar)
    a = np.array(img)
    ys, xs = np.nonzero(barm)
    ch = ((xs + ys) % 4 == 0) | ((xs - ys) % 4 == 0)
    edge = barm & ~np.roll(barm, 1, 0) | barm & ~np.roll(barm, -1, 0) | barm & ~np.roll(barm, 1, 1) | barm & ~np.roll(barm, -1, 1)
    a[ys[ch], xs[ch]] = BLACK
    a[edge] = BLACK
    img = Image.fromarray(a)

    # rivets through the feet into the skin (round heads on the outside)
    def rivets(d, s):
        for rx in (bx - 30, bx + 30):
            yt = curve(rx)
            d.rectangle([(rx - 2) * s, (yt - 1) * s, (rx + 2) * s, (curve(bx) + t + 6) * s], fill=255)
            d.pieslice([(rx - 5) * s, (yt - 5) * s, (rx + 5) * s, (yt + 5) * s], 180, 360, fill=255)
    img = paint(img, mask_layer(rivets), BLACK)

    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    # the leader to the skin + dimension
    xl = 92
    yt = curve(xl)
    dr.line([(xl, yt - 30), (xl, yt - 2)], fill=BLACK)
    dr.polygon([(xl - 3, yt - 7), (xl + 3, yt - 7), (xl, yt - 1)], fill=BLACK)
    dr.line([(xl, yt + t + 2), (xl, yt + t + 30)], fill=BLACK)
    dr.polygon([(xl - 3, yt + t + 7), (xl + 3, yt + t + 7), (xl, yt + t + 1)], fill=BLACK)
    dr.text((14, 14), "3⁄32″", font=font(INTER_XB, 62), fill=BLACK)
    dr.text((178, 22), "Liberty's skin,", font=font(SERIF_I, 15), fill=BLACK)
    dr.text((178, 40), "drawn at actual size.", font=font(SERIF_I, 15), fill=BLACK)
    dr.text((178, 62), "2.38 millimetres, about two pennies", font=font(MONO, 9), fill=BLACK)
    dr.text((xl - 8, yt + t + 12), "copper sheet,", font=font(MONO, 9), fill=BLACK, anchor="ra")
    dr.text((xl - 8, yt + t + 24), "hand-hammered", font=font(MONO, 9), fill=BLACK, anchor="ra")
    dr.text((bx + 50, by - 4), "saddle", font=font(MONO, 9), fill=BLACK)
    dr.text((bx + 50, by + 8), "iron armature bar", font=font(MONO, 9), fill=BLACK)
    dr.text((bx + 50, by + 20), "(Eiffel)", font=font(MONO, 9), fill=BLACK)
    # footer
    fy = 248
    dr.line([(14, fy), (W - 14, fy)], fill=BLACK)
    m = font(MONO, 9)
    dr.text((14, fy + 6), "300,000 rivets · 1,500 saddles · 1,350 bars · 46 m tall", font=m, fill=BLACK)
    dr.text((14, fy + 19), "Dedicated in the rain, 28 October 1886.", font=m, fill=BLACK)
    dr.text((14, fy + 32), "4.72 px/mm: true scale on this 4.2″ panel", font=m, fill=BLACK)
    dr.text((W - 14, fy + 32), "140 years", font=font(MONO_B, 9), fill=RED, anchor="ra")
    return img


# ---------------------------------------------------------------- 3. 14:04 GMT
def radio_moscow():
    img = Image.new("RGB", (W, H), BLACK)
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    # the glass dial
    x0, y0, x1, y1 = 16, 52, W - 16, 226
    dr.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=WHITE)
    dr.rounded_rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], radius=7, outline=BLACK)
    bands = [("49 m", 5.90, 6.20), ("41 m", 7.20, 7.45), ("31 m", 9.40, 9.90),
             ("25 m", 11.60, 12.10), ("19 m", 15.10, 15.80)]
    ax0, ax1 = x0 + 40, x1 - 14
    fsm = font(MONO, 8)
    fb = font(MONO_B, 9)
    for i, (name, lo, hi) in enumerate(bands):
        yb = y0 + 26 + i * 24
        dr.text((x0 + 12, yb - 9), name, font=fb, fill=BLACK)
        dr.line([(ax0, yb), (ax1, yb)], fill=BLACK)
        n = 30
        for k in range(n + 1):
            xx = ax0 + (ax1 - ax0) * k / n
            hgt = 5 if k % 5 == 0 else 2
            dr.line([(xx, yb - hgt), (xx, yb)], fill=BLACK)
            if k % 10 == 0:
                anc = "la" if k == 0 else ("ra" if k == n else "ma")
                dr.text((xx, yb + 2), f"{lo + (hi - lo) * k / n:.2f}", font=fsm, fill=BLACK, anchor=anc)
    # stations along the bottom of the glass, two staggered rows
    cities = [("LONDON", 0.04), ("PARIS", 0.17), ("ROMA", 0.30), ("BERLIN", 0.43), ("PRAHA", 0.74),
              ("HAVANA", 0.86), ("WIEN", 0.97)]
    fc = font(MONO, 8)
    for j, (nm, fx) in enumerate(cities):
        xx = ax0 + (ax1 - ax0) * fx
        yy = y1 - 30 + (j % 2) * 11
        dr.text((xx, yy), nm, font=fc, fill=BLACK, anchor="ma")
    # MOSKVA in red where the needle sits
    fxm = 0.585
    xn = int(ax0 + (ax1 - ax0) * fxm)
    dr.text((xn, y1 - 26), "МОСКВА", font=font(MONO_XB, 11), fill=RED, anchor="ma")
    # the needle
    dr.rectangle([xn - 1, y0 + 6, xn + 1, y1 - 30], fill=RED)
    # tuning knobs / magic eye
    ex, ey = 64, 262
    dr.ellipse([ex - 22, ey - 22, ex + 22, ey + 22], fill=WHITE)
    dr.ellipse([ex - 18, ey - 18, ex + 18, ey + 18], fill=BLACK)
    dr.pieslice([ex - 18, ey - 18, ex + 18, ey + 18], 250, 290, fill=WHITE)
    dr.pieslice([ex - 18, ey - 18, ex + 18, ey + 18], 70, 110, fill=WHITE)
    dr.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=WHITE)
    for kx in (W - 64, W - 116):
        dr.ellipse([kx - 18, ey - 18, kx + 18, ey + 18], fill=WHITE)
        for a in range(0, 360, 20):
            r1 = 18
            dr.line([(kx + 14 * math.cos(math.radians(a)), ey + 14 * math.sin(math.radians(a))),
                     (kx + r1 * math.cos(math.radians(a)), ey + r1 * math.sin(math.radians(a)))], fill=BLACK)
        dr.ellipse([kx - 3, ey - 3, kx + 3, ey + 3], fill=BLACK)
    dr.line([(W - 64, ey), (W - 64 + 12, ey - 8)], fill=BLACK, width=2)
    # headline
    dr.text((16, 10), "14:04", font=font(INTER_XB, 32), fill=WHITE)
    dr.text((122, 13), "GMT · Sunday 28 October 1962", font=font(MONO_B, 10), fill=WHITE)
    dr.text((122, 28), "the letter is read on air before it is", font=font(MONO, 9), fill=WHITE)
    dr.text((122, 39), "finished being typed. The missiles go home.", font=font(MONO, 9), fill=WHITE)
    dr.text((W // 2 - 20, 255), "radio beat", font=font(SERIF_I, 13), fill=WHITE, anchor="ma")
    dr.text((W // 2 - 20, 270), "the cable", font=font(SERIF_I, 13), fill=WHITE, anchor="ma")
    return img


# ---------------------------------------------------------------- 4. Tabula rasa
def tabula_rasa():
    rng = np.random.default_rng(1704)
    img = Image.new("RGB", (W, H), WHITE)
    # two leaves of a diptych, frames of wood rendered as engraved grain
    leaves = [(22, 34, 194, 246), (206, 34, 378, 246)]
    fw = 12
    frame = np.zeros((H, W), bool)
    inner = np.zeros((H, W), bool)
    for (a, b, c, d) in leaves:
        frame[b:d, a:c] = True
        inner[b + fw:d - fw, a + fw:c - fw] = True
    wood = frame & ~inner
    y, x = np.mgrid[0:H, 0:W]
    n = value_noise(H, W, rng, ((3, 1.0), (9, 0.4)))
    grain = (np.sin((y + 18 * n + 0.02 * x) * 1.25) > 0.55)
    a = np.array(img)
    a[wood] = BLACK
    a[wood & grain] = WHITE
    # edge lines of the frames
    for (l, t, r_, b_) in leaves:
        for (xa, ya, xb, yb) in [(l, t, r_, b_), (l + fw, t + fw, r_ - fw, b_ - fw)]:
            a[ya, xa:xb] = BLACK
            a[yb - 1, xa:xb] = BLACK
            a[ya:yb, xa] = BLACK
            a[ya:yb, xb - 1] = BLACK
    img = Image.fromarray(a)
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    # binding cords between the leaves
    for cy in (88, 192):
        dr.ellipse([190, cy - 5, 210, cy + 5], outline=BLACK, width=2)
    # the stylus, lying across the right leaf, red
    def stylus(d, s):
        p0, p1 = (262, 212), (340, 196)
        d.line([(p0[0] * s, p0[1] * s), (p1[0] * s, p1[1] * s)], fill=255, width=3 * s)
        # the spatula end
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        px, py = -math.sin(ang), math.cos(ang)
        c = math.cos(ang); sn = math.sin(ang)
        e = [(p1[0] + 5 * px, p1[1] + 5 * py), (p1[0] + 12 * c + 5 * px, p1[1] + 12 * sn + 5 * py),
             (p1[0] + 12 * c - 5 * px, p1[1] + 12 * sn - 5 * py), (p1[0] - 5 * px, p1[1] - 5 * py)]
        d.polygon([(u * s, v * s) for u, v in e], fill=255)
        # the point
        tip = (p0[0] - 12 * math.cos(ang), p0[1] - 12 * math.sin(ang))
        d.polygon([((p0[0] + 2 * px) * s, (p0[1] + 2 * py) * s), ((p0[0] - 2 * px) * s, (p0[1] - 2 * py) * s),
                   (tip[0] * s, tip[1] * s)], fill=255)
    img = paint(img, mask_layer(stylus), RED)
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    # its shadow? no — instead the first, tiny mark it has made
    dr.line([(244, 218), (248, 214)], fill=RED, width=1)
    # text
    dr.text((W // 2, 8), "TABVLA  RASA", font=font(SERIF_B, 17), fill=BLACK, anchor="ma")
    fi = font(SERIF_I, 12)
    dr.text((W // 2, 254), "“Let us then suppose the mind to be, as we say, white paper,",
            font=fi, fill=BLACK, anchor="ma")
    dr.text((W // 2, 268), "void of all characters, without any ideas: how comes it to be furnished?”",
            font=fi, fill=BLACK, anchor="ma")
    m = font(MONO, 8)
    dr.text((22, 288), "JOHN LOCKE · ESSAY II.i.2", font=m, fill=BLACK)
    dr.text((378, 288), "d. Oates, Essex, 28·X·1704", font=m, fill=BLACK, anchor="ra")
    return img


# ---------------------------------------------------------------- 5. (untitled) first frost
def first_frost():
    rng = np.random.default_rng(20261028)
    occ = np.full((H, W), -1, np.int32)  # owner id of each crystal pixel
    occ[H - 1, :] = np.arange(W)  # the sill: every pixel a seed
    # a few nucleation points stuck to the glass (dust, a scratch)
    for k, (sx, sy) in enumerate([(70, 120), (300, 70), (180, 200)]):
        occ[sy, sx] = W + k
    top = H - 1
    N = 4000

    def spawn(n):
        lo = max(0, top - 30)
        return rng.integers(0, W, n), rng.integers(lo, max(lo + 1, min(H - 2, top + 10)), n)

    wx, wy = spawn(N)
    dirs = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
    stuck_total = 0
    target = 26000
    it = 0
    while stuck_total < target and it < 200000:
        it += 1
        d = dirs[rng.integers(0, 4, N)]
        wx = (wx + d[:, 0]) % W
        wy = np.clip(wy + d[:, 1], 0, H - 2)
        # walkers that wandered far above get re-dropped
        far = wy < top - 45
        if far.any():
            nx, ny = spawn(far.sum())
            wx[far], wy[far] = nx, ny
        onc = occ[wy, wx] >= 0
        if onc.any():
            nx, ny = spawn(onc.sum())
            wx[onc], wy[onc] = nx, ny
        # neighbour check
        best = np.full(N, -1)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            o = occ[np.clip(wy + dy, 0, H - 1), (wx + dx) % W]
            best = np.where((best < 0) & (o >= 0), o, best)
        hit = (best >= 0) & (rng.random(N) < 0.6)
        if hit.any():
            hx, hy, ho = wx[hit], wy[hit], best[hit]
            # resolve duplicates by letting the first win
            keyidx = np.unique(hy * W + hx, return_index=True)[1]
            hx, hy, ho = hx[keyidx], hy[keyidx], ho[keyidx]
            free = occ[hy, hx] < 0
            occ[hy[free], hx[free]] = ho[free]
            stuck_total += int(free.sum())
            top = min(top, int(hy.min()))
            nx, ny = spawn(hit.sum())
            wx[hit], wy[hit] = nx, ny
        if top <= 2:
            break
    # choose the red tree: the largest single-seed tree from the sill
    ids, counts = np.unique(occ[occ >= 0], return_counts=True)
    sill = ids < W
    red_id = ids[sill][np.argmax(counts[sill])]
    a = np.full((H, W, 3), 255, np.uint8)
    a[occ >= 0] = BLACK
    a[occ == red_id] = RED
    return Image.fromarray(a), it, stuck_total, red_id


if __name__ == "__main__":
    save(in_hoc_signo(), 1)
    save(three_32(), 2)
    save(radio_moscow(), 3)
    save(tabula_rasa(), 4)
    img, it, n, rid = first_frost()
    print("frost:", it, "steps,", n, "crystals, red seed x =", rid)
    save(img, 5)
