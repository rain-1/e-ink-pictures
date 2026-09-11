#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-11 (Friday). New moon, Enkutatash, Patent 2,252.

Five 400x300 images in exactly three colors (white, black, red).
Run from the repo root:  python3 archive/2026-09-11/generate.py
Writes images/1.png … images/5.png and archive/2026-09-11/1.png … 5.png.

Today's five:
  1. Kamon        — a compass-and-ruler family crest generated from today's date
  2. Enkutatash   — Ethiopian New Year 2019, hills of adey abeba daisies
  3. Patent 2,252 — Rand's collapsible paint tube (issued 11 Sept 1841), as a patent sheet
  4. New Moon     — constructivist poster for tonight's moonless sky (new at 03:27 UTC)
  5. Sandpile     — Abelian sandpile, 2^15 grains dropped on one cell, toppled to rest
"""

import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT_DIR = "/usr/share/fonts/truetype"
SANS = f"{FONT_DIR}/dejavu/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf"
SERIF = f"{FONT_DIR}/dejavu/DejaVuSerif.ttf"
SERIF_B = f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf"
MONO = f"{FONT_DIR}/dejavu/DejaVuSansMono.ttf"
MONO_B = f"{FONT_DIR}/dejavu/DejaVuSansMono-Bold.ttf"
FREESERIF = f"{FONT_DIR}/freefont/FreeSerif.ttf"          # has Ethiopic
FREESERIF_I = f"{FONT_DIR}/freefont/FreeSerifItalic.ttf"
FREESANS_B = f"{FONT_DIR}/freefont/FreeSansBold.ttf"
JP = f"{FONT_DIR}/fonts-japanese-gothic.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATE = "2026-09-11"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=True):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def seal(img, n):
    """My signature: a small red hanko in the bottom-right with the picture number."""
    d = ImageDraw.Draw(img)
    s = 16
    x0, y0 = W - s - 6, H - s - 6
    d.rectangle([x0, y0, x0 + s, y0 + s], fill=RED)
    f = font(JP, 13)
    ch = "一二三四五"[n - 1]
    bb = d.textbbox((0, 0), ch, font=f)
    d.text((x0 + (s - (bb[2] - bb[0])) / 2 - bb[0], y0 + (s - (bb[3] - bb[1])) / 2 - bb[1]),
           ch, font=f, fill=WHITE)
    return img


# ------------------------------------------------------------------ 1. Kamon
def image1_kamon():
    """Compass-and-ruler crest. Kamon are drawn from circles and straight lines only;
    n-fold symmetric designs start from an inscribed n-gon, and 'tangential circle'
    crests come from dividing the diameter (7 equal circles ⇐ trisect the diameter)."""
    rng = random.Random(20260911)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)
    cx, cy = 150 * s, 150 * s
    R = 118 * s

    def circ(x, y, r, fill=None, outline=None, width=1):
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=outline, width=width)

    # outer ring (maru) with a thin inner ring — the classic "circle-enclosed" frame
    circ(cx, cy, R, outline=BLACK, width=int(5 * s))
    circ(cx, cy, R - 9 * s, outline=BLACK, width=int(1.2 * s))

    n = 5  # five-fold, for the five pictures
    # petal lobes: n circles tangent to each other and to the inner ring, sangaku-style
    r_in = R - 14 * s
    # radius of n mutually tangent circles arranged around the centre inside r_in:
    rp = r_in * math.sin(math.pi / n) / (1 + math.sin(math.pi / n))
    rc = r_in - rp
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        px, py = cx + rc * math.cos(a), cy + rc * math.sin(a)
        circ(px, py, rp, fill=BLACK)
    # carve each lobe with a white inner circle and a red seed
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        px, py = cx + rc * math.cos(a), cy + rc * math.sin(a)
        circ(px, py, rp * 0.62, fill=WHITE)
        circ(px, py, rp * 0.30, fill=RED)
    # central figure: a black disc pierced by a white n-gon star made of straight lines
    circ(cx, cy, rc - rp + 2 * s, fill=WHITE)
    circ(cx, cy, rc - rp - 4 * s, fill=BLACK)
    pts = []
    for k in range(2 * n):
        a = -math.pi / 2 + math.pi * k / n
        rr = (rc - rp - 10 * s) if k % 2 == 0 else (rc - rp - 10 * s) * 0.42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=WHITE)
    circ(cx, cy, 9 * s, fill=RED)
    # straight-line strokes between lobes (the "ruler" part of compass-and-ruler)
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * (k + 0.5) / n
        x1, y1 = cx + (rc - rp - 6 * s) * math.cos(a), cy + (rc - rp - 6 * s) * math.sin(a)
        x2, y2 = cx + (r_in - 2 * s) * math.cos(a), cy + (r_in - 2 * s) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=BLACK, width=int(3 * s))

    # right column: name and construction notes, vertical Japanese text
    fj = font(JP, 34 * s)
    name = "五曜梅"  # "five-star plum" — a crest I made up for today
    x = 350 * s
    y = 22 * s
    for ch in name:
        bb = d.textbbox((0, 0), ch, font=fj)
        d.text((x - (bb[2] - bb[0]) / 2 - bb[0], y), ch, font=fj, fill=BLACK)
        y += (bb[3] - bb[1]) + 10 * s
    fm = font(MONO, 9 * s)
    notes = ["KAMON", "circle & line", "only.", "", "5 tangent", "circles:",
             "r = R·sin(π/5)", "  /(1+sin(π/5))", "", "2026·09·11"]
    y = 172 * s
    for ln in notes:
        d.text((296 * s, y), ln, font=fm, fill=BLACK)
        y += 11.5 * s
    d.line([290 * s, 165 * s, 390 * s, 165 * s], fill=BLACK, width=int(1.5 * s))
    out = finalize(img, dither=False)
    return seal(out.convert("RGB"), 1)


# ------------------------------------------------------------- 2. Enkutatash
def image2_enkutatash():
    """Ethiopian New Year: 1 Meskerem 2019. The rains end and the hills go gold with
    adey abeba (Meskel daisies). No yellow on this screen, so the daisies are white
    with red hearts on rolling dithered hills, and the sun comes up behind them."""
    rng = random.Random(2019)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)

    # sky gradient (light) with a big rising sun
    d.ellipse([250 * s, 40 * s, 340 * s, 130 * s], fill=RED)

    # hills: three overlapping ridges, darker as they come forward
    def ridge(base, amp, freq, phase, tone):
        pts = [(0, H * s)]
        for x in range(0, W * s + 1, 2 * s):
            y = base + amp * math.sin(x / (W * s) * freq * math.pi + phase) \
                + amp * 0.35 * math.sin(x / (W * s) * freq * 2.7 * math.pi + phase * 1.7)
            pts.append((x, y * s))
        pts.append((W * s, H * s))
        d.polygon(pts, fill=tone)

    ridge(150, 12, 1.4, 0.8, (215, 215, 215))
    ridge(185, 16, 1.1, 2.6, (150, 150, 150))
    ridge(230, 12, 0.9, 4.4, BLACK)

    # daisies: smaller and denser toward the far ridge, bigger in front
    def daisy(x, y, r, petals=9):
        for k in range(petals):
            a = 2 * math.pi * k / petals + rng.uniform(-0.15, 0.15)
            px, py = x + r * 0.62 * math.cos(a), y + r * 0.62 * math.sin(a)
            pr = r * 0.42
            d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=WHITE, outline=BLACK, width=max(1, int(0.7 * s)))
        cr = r * 0.32
        d.ellipse([x - cr, y - cr, x + cr, y + cr], fill=RED, outline=BLACK, width=max(1, int(0.7 * s)))

    flowers = []
    for i in range(28):
        y = rng.uniform(150, 172)
        flowers.append((rng.uniform(0, W), y, rng.uniform(2.4, 3.4)))
    for i in range(44):
        y = rng.uniform(178, 215)
        flowers.append((rng.uniform(0, W), y, rng.uniform(3.5, 5.5)))
    for i in range(34):
        y = rng.uniform(225, 285)
        flowers.append((rng.uniform(0, W), y, rng.uniform(6.5, 11)))
    flowers.sort(key=lambda f: f[1])
    for x, y, r in flowers:
        if x > 0 and (y > 185 or x < 300):  # keep the title area on the right clear-ish
            daisy(x * s, y * s, r * s)

    # title block
    fe = font(FREESERIF, 30 * s)
    d.text((14 * s, 12 * s), "እንቁጣጣሽ", font=fe, fill=BLACK)
    fb = font(SERIF_B, 14 * s)
    d.text((16 * s, 52 * s), "ENKUTATASH", font=fb, fill=BLACK)
    fs = font(SERIF, 9 * s)
    d.text((16 * s, 72 * s), "Ethiopian New Year · 1 Meskerem", font=fs, fill=BLACK)
    fn = font(FREESERIF, 22 * s)
    d.text((16 * s, 86 * s), "፳፻፲፱", font=fn, fill=RED)  # 2019 in Ge'ez numerals
    d.text((78 * s, 96 * s), "= 2019, the rains are over", font=fs, fill=BLACK)
    out = finalize(img, dither=True)
    return seal(out.convert("RGB"), 2)


# ------------------------------------------------------------ 3. Patent 2,252
def image3_patent():
    """John Goffe Rand, portrait painter, U.S. Patent No. 2,252, issued 11 September 1841:
    'Improvement in the Construction of Vessels or Apparatus for Preserving Paint'.
    The collapsible tin tube. Renoir: 'without colours in tubes there would be no
    Cézanne, no Monet, no Pissarro, and no Impressionism.'"""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)
    thin = max(1, int(0.8 * s))
    mid = int(1.6 * s)

    # sheet border, double rule
    d.rectangle([6 * s, 6 * s, W * s - 6 * s, H * s - 6 * s], outline=BLACK, width=mid)
    d.rectangle([9 * s, 9 * s, W * s - 9 * s, H * s - 9 * s], outline=BLACK, width=thin)

    # header
    fh = font(SERIF_B, 13 * s)
    fi = font(FREESERIF_I, 9 * s)
    fs = font(SERIF, 8 * s)
    d.text((18 * s, 14 * s), "J. G. RAND.", font=fh, fill=BLACK)
    d.text((18 * s, 31 * s), "Vessel or Apparatus for Preserving Paint.", font=fi, fill=BLACK)
    d.text((252 * s, 14 * s), "No. 2,252.", font=fh, fill=BLACK)
    d.text((252 * s, 31 * s), "Patented Sept. 11, 1841.", font=fs, fill=BLACK)
    d.line([18 * s, 46 * s, W * s - 18 * s, 46 * s], fill=BLACK, width=thin)

    # Fig. 1 — the tube, drawn lying at a slight angle, with a squeeze of red paint
    def hatch(poly, spacing, angle_deg=45, color=BLACK):
        """Fill a polygon with engraved hatching by drawing lines clipped through a mask."""
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).polygon(poly, fill=255)
        layer = Image.new("RGB", img.size, WHITE)
        ld = ImageDraw.Draw(layer)
        L = W * s + H * s
        a = math.radians(angle_deg)
        dx, dy = math.cos(a), math.sin(a)
        nx, ny = -dy, dx
        for k in range(-L, L, int(spacing)):
            x0, y0 = k * nx, k * ny
            ld.line([x0 - L * dx, y0 - L * dy, x0 + L * dx, y0 + L * dy], fill=color, width=thin)
        img.paste(layer, (0, 0), mask)

    # tube body: a tapered rectangle from (60,150) to (250,150), crimped tail at the left
    tx0, tx1, ty = 62 * s, 246 * s, 158 * s
    r_body = 26 * s
    body = [(tx0, ty - r_body * 0.55), (tx1, ty - r_body), (tx1, ty + r_body), (tx0, ty + r_body * 0.55)]
    # shading: dense hatch along the lower half, light along the top (cylinder shading)
    hatch([(tx0, ty + r_body * 0.1), (tx1, ty + r_body * 0.15), (tx1, ty + r_body), (tx0, ty + r_body * 0.55)],
          2.6 * s, 0)
    hatch([(tx0, ty - r_body * 0.55), (tx1, ty - r_body), (tx1, ty - r_body * 0.55), (tx0, ty - r_body * 0.3)],
          4.5 * s, 0)
    d.polygon(body, outline=BLACK, width=mid)
    # crimped tail: folded end with short vertical strokes
    d.rectangle([tx0 - 8 * s, ty - r_body * 0.55, tx0, ty + r_body * 0.55], fill=WHITE, outline=BLACK, width=mid)
    for k in range(6):
        yy = ty - r_body * 0.55 + (k + 0.5) * (r_body * 1.1 / 6)
        d.line([tx0 - 8 * s, yy, tx0, yy], fill=BLACK, width=thin)
    # shoulder + neck + cap at the right
    d.polygon([(tx1, ty - r_body), (tx1 + 14 * s, ty - 9 * s), (tx1 + 14 * s, ty + 9 * s), (tx1, ty + r_body)],
              fill=WHITE, outline=BLACK, width=mid)
    hatch([(tx1, ty + r_body * 0.2), (tx1 + 14 * s, ty + 2 * s), (tx1 + 14 * s, ty + 9 * s), (tx1, ty + r_body)], 2.6 * s, 0)
    neck = [tx1 + 14 * s, ty - 9 * s, tx1 + 26 * s, ty + 9 * s]
    d.rectangle(neck, fill=WHITE, outline=BLACK, width=mid)
    for k in range(5):  # screw thread
        xx = tx1 + 15 * s + k * 2.4 * s
        d.line([xx, ty - 9 * s, xx, ty + 9 * s], fill=BLACK, width=thin)
    cap = [tx1 + 26 * s, ty - 13 * s, tx1 + 42 * s, ty + 13 * s]
    d.rectangle(cap, fill=WHITE, outline=BLACK, width=mid)
    for k in range(7):  # knurled cap
        yy = ty - 13 * s + (k + 0.5) * (26 * s / 7)
        d.line([tx1 + 26 * s, yy, tx1 + 42 * s, yy], fill=BLACK, width=thin)
    # the squeeze of paint (the only red thing on a black-ink sheet)
    d.ellipse([tx1 + 40 * s, ty - 8 * s, tx1 + 74 * s, ty + 14 * s], fill=RED)
    d.ellipse([tx1 + 56 * s, ty + 4 * s, tx1 + 88 * s, ty + 26 * s], fill=RED)
    d.rectangle([tx1 + 42 * s, ty - 5 * s, tx1 + 56 * s, ty + 6 * s], fill=RED)

    # reference letters, as on old patent drawings, with leader lines
    fl = font(FREESERIF_I, 15 * s)
    refs = [("a", (150 * s, 118 * s), (150 * s, ty - r_body * 0.8)),
            ("b", (56 * s, 205 * s), (tx0 - 4 * s, ty + r_body * 0.6)),
            ("c", (270 * s, 118 * s), (tx1 + 20 * s, ty - 10 * s)),
            ("d", (302 * s, 118 * s), (tx1 + 34 * s, ty - 14 * s)),
            ("e", (330 * s, 205 * s), (tx1 + 70 * s, ty + 20 * s))]
    for ch, (lx, ly), (px, py) in refs:
        d.line([lx + 4 * s, ly + 6 * s, px, py], fill=BLACK, width=thin)
        d.text((lx, ly - 4 * s), ch, font=fl, fill=BLACK)
    d.text((22 * s, 120 * s), "Fig. 1.", font=font(SERIF_B, 10 * s), fill=BLACK)

    # Fig. 2 — end-on cross-section (a circle with the tube wall hatched)
    fx, fy, fr = 345 * s, 232 * s, 28 * s
    d.text((fx - 60 * s, fy + 22 * s), "Fig. 2.", font=font(SERIF_B, 10 * s), fill=BLACK)
    d.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], outline=BLACK, width=mid)
    d.ellipse([fx - fr * 0.8, fy - fr * 0.8, fx + fr * 0.8, fy + fr * 0.8], outline=BLACK, width=mid)
    ring = Image.new("L", img.size, 0)
    rd = ImageDraw.Draw(ring)
    rd.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=255)
    rd.ellipse([fx - fr * 0.8, fy - fr * 0.8, fx + fr * 0.8, fy + fr * 0.8], fill=0)
    layer = Image.new("RGB", img.size, WHITE)
    ld = ImageDraw.Draw(layer)
    for k in range(-int(fr * 2), int(fr * 2), int(2.4 * s)):
        ld.line([fx + k - fr, fy - fr, fx + k + fr, fy + fr], fill=BLACK, width=thin)
    img.paste(layer, (0, 0), ring)
    d.ellipse([fx - fr * 0.55, fy - fr * 0.55, fx + fr * 0.55, fy + fr * 0.55], fill=RED)

    # description text
    ft = font(SERIF, 9 * s)
    lines = ["a: a tube of tin, closed at b by folding,",
             "with screw-neck c and cap d, so the colour e",
             "is pressed out and the rest kept from the air.",
             "",
             "\u201cWithout colours in tubes there would be",
             "no C\u00e9zanne, no Monet, no Pissarro, and",
             "no Impressionism.\u201d          \u2014 Renoir"]
    y = 200 * s
    for ln in lines:
        d.text((22 * s, y), ln, font=ft, fill=BLACK)
        y += 11.5 * s
    # a faint red office stamp, rotated
    st = Image.new("RGBA", (120 * s, 40 * s), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.rectangle([2 * s, 2 * s, 118 * s, 38 * s], outline=RED, width=mid)
    sd.text((10 * s, 8 * s), "U.S. PATENT OFFICE", font=font(SANS_B, 10 * s), fill=RED)
    sd.text((28 * s, 22 * s), "SEPT. 11 1841", font=font(SANS, 9 * s), fill=RED)
    st = st.rotate(12, resample=Image.BICUBIC, expand=True)
    img.paste(st, (262 * s, 50 * s), st)
    out = finalize(img, dither=False)
    return seal(out.convert("RGB"), 3)


# --------------------------------------------------------------- 4. New Moon
def image4_new_moon():
    """Tonight there is no moon at all (new at 03:27 UTC today). A poster in the
    Lissitzky/constructivist idiom this palette was practically invented for: a black
    disc, a red wedge, type on the diagonal. The wedge is the sliver that will grow."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)

    # big black disc — the moon you cannot see
    cx, cy, R = 232 * s, 150 * s, 118 * s
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)
    # the red wedge driving in from the lower-left
    d.polygon([(0, H * s), (cx - 6 * s, cy + 4 * s), (0, 200 * s)], fill=RED)
    d.polygon([(0, H * s), (cx - 6 * s, cy + 4 * s), (70 * s, H * s)], fill=RED)
    # a thin white crescent hint on the disc's right limb — tomorrow's moon
    r2 = R - 5 * s
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=WHITE)
    d.ellipse([cx - r2 - 7 * s, cy - r2, cx + r2 - 7 * s, cy + r2], fill=BLACK)
    # scatter of small squares and bars — the "secondary skirmishes"
    rng = random.Random(327)
    for i in range(9):
        w = rng.randint(3, 10) * s
        x, y = rng.randint(10, 150) * s, rng.randint(12, 110) * s
        d.rectangle([x, y, x + w, y + w], fill=rng.choice([BLACK, RED, BLACK]))
    d.line([0, 40 * s, 140 * s, 40 * s], fill=BLACK, width=int(2 * s))
    d.line([20 * s, 0, 20 * s, 120 * s], fill=BLACK, width=int(2 * s))

    # diagonal type
    def diag_text(text, xy, fnt, fill, angle):
        tw, th = d.textbbox((0, 0), text, font=fnt)[2:]
        layer = Image.new("RGBA", (tw + 4 * s, th + 4 * s), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((2 * s, 2 * s), text, font=fnt, fill=fill)
        layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
        img.paste(layer, (int(xy[0]), int(xy[1])), layer)

    diag_text("NEW MOON", (14 * s, 182 * s), font(FREESANS_B, 30 * s), WHITE, 30)
    fd = font(MONO_B, 9 * s)
    tw = d.textbbox((0, 0), "11\u00b7IX\u00b72026 \u00b7 new at 03:27 UTC", font=fd)[2]
    d.text((W * s - 14 * s - tw, 10 * s), "11\u00b7IX\u00b72026 \u00b7 new at 03:27 UTC", font=fd, fill=BLACK)
    # inside the disc, small white text: what to look for on a moonless night
    fm = font(MONO, 8 * s)
    lines = ["no moon tonight —", "darkest sky of the month", "", "look for:",
             "M31 Andromeda, naked eye", "Milky Way, Cygnus overhead", "Saturn low in the east",
             "", "first quarter Sep 18", "harvest moon Sep 26"]
    y = 96 * s
    for ln in lines:
        d.text((172 * s, y), ln, font=fm, fill=WHITE)
        y += 10.5 * s
    out = finalize(img, dither=False)
    return seal(out.convert("RGB"), 4)


# --------------------------------------------------------------- 5. Sandpile
def image5_sandpile():
    """Abelian sandpile: drop 2^15 grains on one cell of a grid; any cell with ≥4
    grains gives one to each neighbour; repeat until every cell holds 0–3. The order
    of toppling doesn't matter (hence 'abelian') and the result is this fractal."""
    gh, gw = 150, 200  # computed at half resolution, doubled to 400x300 — crisper on e-ink
    z = np.zeros((gh, gw), np.int64)
    z[gh // 2, gw // 2 + 25] = 2 ** 15
    touched = z > 0
    while True:
        t4 = z // 4
        if not t4.any():
            break
        z -= 4 * t4
        touched |= z > 0
        z[1:, :] += t4[:-1, :]
        z[:-1, :] += t4[1:, :]
        z[:, 1:] += t4[:, :-1]
        z[:, :-1] += t4[:, 1:]
    # inside the pile: 3 grains (commonest) white, 2 checker-grey, 1 black, 0 red.
    # cells the sand never reached stay white.
    z = np.where(touched, z, 3)
    rgb = np.zeros((gh * 2, gw * 2, 3), np.uint8)
    big = np.kron(z, np.ones((2, 2), np.int64))
    yy, xx = np.mgrid[0:gh * 2, 0:gw * 2]
    checker = ((yy + xx) % 2 == 0)
    rgb[big == 3] = WHITE
    rgb[(big == 2) & checker] = BLACK
    rgb[(big == 2) & ~checker] = WHITE
    rgb[big == 1] = BLACK
    rgb[big == 0] = RED
    img = Image.fromarray(rgb, "RGB")
    d = ImageDraw.Draw(img)
    fm = font(MONO, 9)
    d.text((8, 6), "ABELIAN SANDPILE", font=font(MONO_B, 10), fill=BLACK)
    d.text((8, 19), "2^15 grains on one cell;", font=fm, fill=BLACK)
    d.text((8, 30), "4 grains \u2192 1 to each side", font=fm, fill=BLACK)
    d.text((8, 270), "grains:  3    2    1    0", font=fm, fill=BLACK)
    d.rectangle([74, 271, 82, 279], fill=WHITE, outline=BLACK)
    for y in range(271, 280):
        for x in range(101, 110):
            d.point((x, y), fill=WHITE if (x + y) % 2 else BLACK)
    d.rectangle([128, 271, 136, 279], fill=BLACK)
    d.rectangle([155, 271, 163, 279], fill=RED)
    out = finalize(img, dither=False)
    return seal(out.convert("RGB"), 5)


def main():
    makers = [image1_kamon, image2_enkutatash, image3_patent, image4_new_moon, image5_sandpile]
    os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
    os.makedirs(HERE, exist_ok=True)
    for i, mk in enumerate(makers, 1):
        im = mk()
        im = im.convert("RGB").quantize(palette=PAL, dither=Image.Dither.NONE)
        assert im.size == (W, H)
        colors = set(c for _, c in im.convert("RGB").getcolors(1 << 20))
        assert colors <= {WHITE, BLACK, RED}, colors
        for path in (os.path.join(ROOT, "images", f"{i}.png"), os.path.join(HERE, f"{i}.png")):
            im.save(path, optimize=True)
        print("wrote", i, sorted(colors))


if __name__ == "__main__":
    main()
