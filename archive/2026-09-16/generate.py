#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-16.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

Today: Mexican Independence Day (Grito de Dolores, 1810); the Mayflower left
Plymouth on this day in 1620; the Moon is a 25% waxing crescent; Venus peaks in
brilliancy on the 18th; the equinox lands in six days.

1. Papel picado   — cut-tissue-paper banners, ¡VIVA MÉXICO!         (hard edge)
2. Red wedge      — a Lissitzky-style constructivist calendar poster (hard edge)
3. Kamon          — six procedurally drawn Japanese family crests    (hard edge)
4. Equinox        — terminator globe + the rest of September's moons (dithered)
5. Mayflower      — woodcut ship on a generative sea, red sun        (dithered)

Hard-edged pieces are drawn at 3x and thresholded (no dither) so curves stay
crisp; tonal pieces are drawn at 3x and Floyd–Steinberg dithered.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_LIB_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED)
    palette += [0, 0, 0] * (256 - 3)
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


class Ink:
    """Crisp text for tonal pieces: text is drawn on 3x masks, downscaled and
    thresholded, then stamped onto the already-dithered image so letters are
    never speckled by the dither."""

    def __init__(self):
        self.masks = {WHITE: None, BLACK: None, RED: None}

    def text(self, xy, txt, fnt, fill):
        if self.masks[fill] is None:
            self.masks[fill] = Image.new("L", (W * SS, H * SS), 0)
        ImageDraw.Draw(self.masks[fill]).text(xy, txt, font=fnt, fill=255)

    def textbbox(self, txt, fnt):
        return ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), txt, font=fnt)

    def apply(self, out):
        for color, idx in ((WHITE, 0), (BLACK, 1), (RED, 2)):
            m = self.masks[color]
            if m is None:
                continue
            m = m.resize((W, H), Image.LANCZOS).point(lambda v: 255 if v >= 96 else 0)
            out.paste(idx, (0, 0), m)


def finalize(img, dither=True, ink=None):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    out = img.convert("RGB").quantize(palette=PAL, dither=d)
    if ink is not None:
        ink.apply(out)
    # my mark: a 6px red square, 6px in from the bottom-right corner
    px = out.load()
    for y in range(H - 12, H - 6):
        for x in range(W - 12, W - 6):
            px[x, y] = 2
    return out


def font(path, size):
    return ImageFont.truetype(path, size)


def new_canvas(bg):
    img = Image.new("RGB", (W * SS, H * SS), bg)
    return img, ImageDraw.Draw(img)


# ------------------------------------------------------------ 1. Papel picado
def image1_papel_picado():
    rng = random.Random(20260916)
    s = SS
    img, dr = new_canvas(BLACK)

    def scalloped_pennant(x0, y0, w, h, color, notch_r):
        # rectangle with a row of semicircular notches along the bottom edge
        dr.rectangle([x0, y0, x0 + w, y0 + h], fill=color)
        n = max(2, int(w / (notch_r * 2)))
        pitch = w / n
        for i in range(n):
            cx = x0 + pitch * (i + 0.5)
            dr.ellipse([cx - notch_r, y0 + h - notch_r, cx + notch_r, y0 + h + notch_r], fill=BLACK)
        # tiny cut triangles along the top under the string
        for i in range(n):
            cx = x0 + pitch * (i + 0.5)
            dr.polygon([(cx - notch_r * 0.5, y0), (cx + notch_r * 0.5, y0), (cx, y0 + notch_r * 0.9)], fill=BLACK)

    def cut_flower(cx, cy, r, petals=8):
        for k in range(petals):
            a = 2 * math.pi * k / petals
            px, py = cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62
            pr = r * 0.30
            dr.ellipse([px - pr, py - pr, px + pr, py + pr], fill=BLACK)
        dr.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22], fill=BLACK)

    def cut_star(cx, cy, r, points=5):
        pts = []
        for k in range(points * 2):
            a = -math.pi / 2 + math.pi * k / points
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        dr.polygon(pts, fill=BLACK)

    def cut_dove(cx, cy, r, flip=False):
        f = -1 if flip else 1
        # body
        dr.ellipse([cx - r * 0.75, cy - r * 0.32, cx + r * 0.75, cy + r * 0.32], fill=BLACK)
        # head
        hx = cx + f * r * 0.75
        dr.ellipse([hx - r * 0.24, cy - r * 0.42, hx + r * 0.24, cy + r * 0.06], fill=BLACK)
        # beak
        dr.polygon([(hx + f * r * 0.2, cy - r * 0.22), (hx + f * r * 0.48, cy - r * 0.14), (hx + f * r * 0.2, cy - r * 0.08)], fill=BLACK)
        # wing (up)
        dr.polygon([(cx - f * r * 0.1, cy - r * 0.2), (cx - f * r * 0.55, cy - r * 0.95), (cx + f * r * 0.35, cy - r * 0.25)], fill=BLACK)
        # tail
        dr.polygon([(cx - f * r * 0.6, cy - r * 0.1), (cx - f * r * 1.05, cy + r * 0.05), (cx - f * r * 1.0, cy + r * 0.35), (cx - f * r * 0.6, cy + r * 0.25)], fill=BLACK)

    def cut_diamond_border(x0, y0, w, h, d):
        # diamonds around the inside edge
        nx = int(w / (d * 2.2))
        for i in range(nx):
            cx = x0 + w * (i + 0.5) / nx
            for cy in (y0 + d * 1.6, y0 + h - d * 2.6):
                dr.polygon([(cx, cy - d), (cx + d * 0.6, cy), (cx, cy + d), (cx - d * 0.6, cy)], fill=BLACK)
        ny = int(h / (d * 2.4))
        for j in range(1, ny - 1):
            cy = y0 + h * (j + 0.5) / ny
            for cx in (x0 + d * 1.2, x0 + w - d * 1.2):
                dr.polygon([(cx, cy - d), (cx + d * 0.6, cy), (cx, cy + d), (cx - d * 0.6, cy)], fill=BLACK)

    def cut_lace(x0, y0, w, h, cell):
        # folded-paper lattice: mirror-symmetric grid of small holes
        cols = int(w / cell)
        rows = int(h / cell)
        holes = set()
        for j in range(rows):
            for i in range((cols + 1) // 2):
                if rng.random() < 0.55:
                    holes.add((i, j))
                    holes.add((cols - 1 - i, j))
        for (i, j) in holes:
            cx = x0 + cell * (i + 0.5)
            cy = y0 + cell * (j + 0.5)
            rr = cell * 0.28
            if (i + j) % 2:
                dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=BLACK)
            else:
                dr.polygon([(cx, cy - rr * 1.2), (cx + rr * 1.2, cy), (cx, cy + rr * 1.2), (cx - rr * 1.2, cy)], fill=BLACK)

    def string(y, sag):
        pts = [(x, y + sag * math.sin(math.pi * x / (W * s))) for x in range(0, W * s + 1, 6)]
        dr.line(pts, fill=WHITE, width=max(1, s))
        return pts

    def y_on_string(pts, x):
        i = min(len(pts) - 1, max(0, int(x / 6)))
        return pts[i][1]

    # --- row 1 & 3: motif pennants ---
    def motif_row(y_str, sag, n, motifs, red_idx):
        pts = string(y_str * s, sag * s)
        pw = (W * s) / n
        for i in range(n):
            x0 = pw * i + pw * 0.06
            w = pw * 0.88
            y0 = y_on_string(pts, x0 + w / 2) + 2 * s
            h = 66 * s
            color = RED if i in red_idx else WHITE
            scalloped_pennant(x0, y0, w, h, color, 4.5 * s)
            cx, cy = x0 + w / 2, y0 + h * 0.46
            m = motifs[i % len(motifs)]
            cut_diamond_border(x0, y0, w, h, 2.6 * s)
            if m == "flower":
                cut_flower(cx, cy, 16 * s, petals=rng.choice([6, 8]))
            elif m == "star":
                cut_star(cx, cy, 15 * s)
            elif m == "dove":
                cut_dove(cx, cy + 3 * s, 13 * s, flip=(i % 2 == 1))
            elif m == "lace":
                cut_lace(x0 + 7 * s, y0 + 9 * s, w - 14 * s, h - 22 * s, 5.5 * s)

    motif_row(22, 9, 6, ["flower", "dove", "lace", "star", "dove", "flower"], {1, 4})
    # --- row 2: lettered pennants VIVA MÉXICO ---
    letters = list("VIVA·MÉXICO")
    pts = string(120 * s, 7 * s)
    n = len(letters)
    pw = (W * s) / n
    fnt = font(FONT_LIB_B, int(30 * s))
    for i, ch in enumerate(letters):
        x0 = pw * i + pw * 0.07
        w = pw * 0.86
        y0 = y_on_string(pts, x0 + w / 2) + 2 * s
        h = 60 * s
        color = RED if ch in "M" or i in (0, 3, 10) else WHITE
        if ch == "·":
            color = RED
        scalloped_pennant(x0, y0, w, h, color, 3.8 * s)
        if ch == "·":
            cut_star(x0 + w / 2, y0 + h * 0.45, 11 * s)
        else:
            bbox = dr.textbbox((0, 0), ch, font=fnt)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            dr.text((x0 + w / 2 - tw / 2 - bbox[0], y0 + h * 0.44 - th / 2 - bbox[1]), ch, font=fnt, fill=BLACK)
    motif_row(212, 8, 7, ["star", "lace", "flower", "dove", "flower", "lace", "star"], {2, 4})

    # caption
    f2 = font(FONT_MONO, int(8.5 * s))
    dr.text((6 * s, 289 * s), "16 SEP · GRITO DE DOLORES 1810 · PAPEL PICADO", font=f2, fill=WHITE)
    return finalize(img, dither=False)


# --------------------------------------------------------------- 2. Red wedge
def image2_red_wedge():
    s = SS
    img, dr = new_canvas(WHITE)

    # black half-field on the right, cut by a diagonal
    dr.polygon([(W * s * 0.52, 0), (W * s, 0), (W * s, H * s), (W * s * 0.72, H * s)], fill=BLACK)
    # the white circle (the target), sitting mostly on black
    cx, cy, r = W * s * 0.70, H * s * 0.42, 84 * s
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    # the red wedge from lower-left piercing into the circle
    tip = (cx + 8 * s, cy - 2 * s)
    dr.polygon([(-10 * s, H * s * 0.98), (-10 * s, H * s * 0.60), tip], fill=RED)
    # black wedge ghost (thin) echoing the diagonal
    dr.line([(0, H * s * 0.30), (W * s * 0.50, H * s * 0.02)], fill=BLACK, width=int(2.5 * s))
    # small satellites: constructivist debris
    for (px, py, pr, col) in [(0.84, 0.16, 7, RED), (0.90, 0.80, 11, WHITE), (0.60, 0.86, 5, BLACK), (0.30, 0.18, 4, RED)]:
        px, py, pr = px * W * s, py * H * s, pr * s
        dr.ellipse([px - pr, py - pr, px + pr, py + pr], fill=col)
    # red bar under the circle
    dr.rectangle([W * s * 0.585, H * s * 0.78, W * s * 0.98, H * s * 0.80], fill=RED)
    # a scattering of thin black rules (rhythm)
    for k, (x0, y0, x1, y1) in enumerate([(0.02, 0.44, 0.19, 0.44), (0.02, 0.48, 0.13, 0.48), (0.02, 0.52, 0.16, 0.52)]):
        dr.line([(x0 * W * s, y0 * H * s), (x1 * W * s, y1 * H * s)], fill=BLACK, width=int(1.5 * s))

    # diagonal typography (rotated text pasted with alpha)
    def diag_text(txt, fpath, size, fill, angle, pos):
        f = font(fpath, int(size * s))
        bbox = dr.textbbox((0, 0), txt, font=f)
        tw, th = bbox[2] - bbox[0] + 8 * s, bbox[3] - bbox[1] + 8 * s
        layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((4 * s - bbox[0], 4 * s - bbox[1]), txt, font=f, fill=fill + (255,))
        layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
        img.paste(layer, (int(pos[0] * s), int(pos[1] * s)), layer)

    ang = math.degrees(math.atan2(H * 0.38, W * 0.70))  # slope of the wedge
    diag_text("SEPTEMBER 16", FONT_SANS_B, 22, BLACK, ang, (30, 138))
    diag_text("day 259 of 365", FONT_SANS, 11, BLACK, ang, (118, 176))
    ang2 = math.degrees(math.atan2(H * 0.28, W * 0.50))  # slope of the thin black rule
    diag_text("6 DAYS TO EQUINOX", FONT_SANS_B, 13, BLACK, ang2, (34, 62))
    fw = font(FONT_SANS_B, int(8 * s))
    dr.text((296 * s, 246 * s), "VENUS BRIGHTEST", font=fw, fill=WHITE)
    dr.text((296 * s, 257 * s), "THU 18 · MAG −4.8", font=fw, fill=WHITE)
    # top-left tag block
    fm = font(FONT_MONO_B, int(9 * s))
    dr.rectangle([0, 0, 64 * s, 15 * s], fill=BLACK)
    dr.text((4 * s, 3 * s), "2026·IX·16", font=fm, fill=WHITE)
    fm2 = font(FONT_MONO_B, int(7.5 * s))
    dr.text((4 * s, 20 * s), "after Lissitzky, 1919", font=fm2, fill=BLACK)
    return finalize(img, dither=False)


# ------------------------------------------------------------------- 3. Kamon
def image3_kamon():
    s = SS
    img, dr = new_canvas(WHITE)
    R = 40 * s
    ring_w = 3 * s

    def clip_circle(draw_fn, cx, cy, r, color):
        """Draw with draw_fn onto a mask, then paste color through mask ∩ circle."""
        layer = Image.new("L", img.size, 0)
        ld = ImageDraw.Draw(layer)
        draw_fn(ld)
        circ = Image.new("L", img.size, 0)
        ImageDraw.Draw(circ).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
        from PIL import ImageChops
        mask = ImageChops.multiply(layer, circ)
        img.paste(Image.new("RGB", img.size, color), (0, 0), mask)

    def maru(cx, cy, color):
        dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=color)
        dr.ellipse([cx - R + ring_w, cy - R + ring_w, cx + R - ring_w, cy + R - ring_w], fill=WHITE)

    def mon_tsuki(cx, cy, color):  # 月 crescent moon with a star
        maru(cx, cy, color)
        r = R * 0.62
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
        r2 = R * 0.56
        dr.ellipse([cx - r2 + R * 0.28, cy - r2 - R * 0.10, cx + r2 + R * 0.28, cy + r2 - R * 0.10], fill=WHITE)
        sr = R * 0.10
        dr.ellipse([cx + R * 0.30 - sr, cy + R * 0.22 - sr, cx + R * 0.30 + sr, cy + R * 0.22 + sr], fill=color)

    def mon_nami(cx, cy, color):  # 波 stacked wave crests (seigaiha inside the ring)
        maru(cx, cy, color)

        def waves(ld):
            rows = [(-0.42, -0.5), (0.05, 0.0), (0.52, -0.5)]
            for (oy, ox) in rows:
                for k in range(-1, 3):
                    wx = cx + (k + ox) * R * 0.9
                    wy = cy + oy * R + R * 0.45
                    for i, rr in enumerate([0.45, 0.34, 0.23, 0.12]):
                        rr *= R
                        col = 255 if i % 2 == 0 else 0
                        ld.pieslice([wx - rr, wy - rr, wx + rr, wy + rr], 180, 360, fill=col)
        clip_circle(waves, cx, cy, R - ring_w * 1.8, color)

    def mon_kikyo(cx, cy, color):  # 桔梗 bellflower: five pointed petals
        maru(cx, cy, color)
        for k in range(5):
            a = -math.pi / 2 + 2 * math.pi * k / 5
            tip = (cx + math.cos(a) * R * 0.72, cy + math.sin(a) * R * 0.72)
            l = (cx + math.cos(a - 0.55) * R * 0.36, cy + math.sin(a - 0.55) * R * 0.36)
            rgt = (cx + math.cos(a + 0.55) * R * 0.36, cy + math.sin(a + 0.55) * R * 0.36)
            dr.polygon([tip, l, (cx, cy), rgt], fill=color)
            # petal vein
            dr.line([(cx, cy), tip], fill=WHITE, width=int(1.2 * s))
        pr = R * 0.14
        dr.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=color)
        pr2 = R * 0.07
        dr.ellipse([cx - pr2, cy - pr2, cx + pr2, cy + pr2], fill=WHITE)

    def mon_hoshi(cx, cy, color):  # 三つ星 three stars (Mōri-style, with the 'one' bar)
        maru(cx, cy, color)
        dr.rectangle([cx - R * 0.55, cy - R * 0.62, cx + R * 0.55, cy - R * 0.44], fill=color)
        sr = R * 0.19
        for (ox, oy) in [(0, -0.12), (-0.33, 0.36), (0.33, 0.36)]:
            px, py = cx + ox * R, cy + oy * R
            dr.ellipse([px - sr, py - sr, px + sr, py + sr], fill=color)

    def mon_hishi(cx, cy, color):  # 四つ割菱 four split diamonds
        maru(cx, cy, color)
        d = R * 0.33
        g = R * 0.05
        for (ox, oy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            px, py = cx + ox * (d + g) * 0.95, cy + oy * (d + g) * 0.72
            dr.polygon([(px, py - d * 0.72), (px + d * 0.95, py), (px, py + d * 0.72), (px - d * 0.95, py)], fill=color)
            dr.polygon([(px, py - d * 0.36), (px + d * 0.48, py), (px, py + d * 0.36), (px - d * 0.48, py)], fill=WHITE)

    def mon_igeta(cx, cy, color):  # 井桁 well-frame lattice
        maru(cx, cy, color)
        t = R * 0.13
        L = R * 0.66
        o = R * 0.22
        for (x0, y0, x1, y1) in [(-o - t / 2, -L, -o + t / 2, L), (o - t / 2, -L, o + t / 2, L)]:
            dr.polygon([(cx + x0, cy + y0 - t * 0.6), (cx + x1, cy + y0 + t * 0.6), (cx + x1, cy + y1 + t * 0.6), (cx + x0, cy + y1 - t * 0.6)], fill=color)
        for (x0, y0, x1, y1) in [(-L, -o - t / 2, L, -o + t / 2), (-L, o - t / 2, L, o + t / 2)]:
            dr.polygon([(cx + x0, cy + y0 + t * 0.6), (cx + x1, cy + y0 - t * 0.6), (cx + x1, cy + y1 - t * 0.6), (cx + x0, cy + y1 + t * 0.6)], fill=color)

    crests = [
        (mon_tsuki, "月", "tsuki · moon", RED),
        (mon_nami, "波", "nami · wave", BLACK),
        (mon_kikyo, "桔梗", "kikyō · bellflower", BLACK),
        (mon_hoshi, "三つ星", "mitsuboshi · 3 stars", BLACK),
        (mon_hishi, "菱", "hishi · diamonds", BLACK),
        (mon_igeta, "井桁", "igeta · well-frame", BLACK),
    ]
    ink = Ink()
    fj = font(FONT_JP, int(13 * s))
    fr = font(FONT_SANS_B, int(8 * s))
    cols, rows = 3, 2
    for i, (fn, kanji, roman, col) in enumerate(crests):
        c, r_ = i % cols, i // cols
        cx = (c + 0.5) * (W * s / cols)
        cy = 20 * s + R + r_ * 128 * s
        fn(cx, cy, col)
        bb = ink.textbbox(kanji, fj)
        ink.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy + R + 4 * s), kanji, fj, col)
        bb = ink.textbbox(roman, fr)
        ink.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy + R + 21 * s), roman, fr, BLACK)
    fm = font(FONT_MONO_B, int(8 * s))
    ink.text((6 * s, 287 * s), "家紋 KAMON · six crests drawn with compass rules · 2026-09-16", font(FONT_JP, int(8.5 * s)), BLACK)
    return finalize(img, dither=False, ink=ink)


# ----------------------------------------------------------------- 4. Equinox
# --- low-precision Sun/Moon ephemeris (Meeus, truncated) for real phases ---
def jd_utc(y, m, d, h=0.0):
    if m <= 2: y -= 1; m += 12
    A = y // 100; B = 2 - A + A // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + h / 24 + B - 1524.5
def sun_lon(T):
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    M = math.radians(357.52911 + 35999.05029 * T - 0.0001537 * T * T)
    C = (1.914602 - 0.004817 * T) * math.sin(M) + 0.019993 * math.sin(2 * M) + 0.000289 * math.sin(3 * M)
    return (L0 + C) % 360
def moon_lon_lat(T):
    Lp = 218.3164477 + 481267.88123421 * T
    D = math.radians(297.8501921 + 445267.1114034 * T)
    M = math.radians(357.5291092 + 35999.0502909 * T)
    Mp = math.radians(134.9633964 + 477198.8675055 * T)
    F = math.radians(93.2720950 + 483202.0175233 * T)
    lon = Lp + 6.288774 * math.sin(Mp) + 1.274027 * math.sin(2 * D - Mp) + 0.658314 * math.sin(2 * D) \
        + 0.213618 * math.sin(2 * Mp) - 0.185116 * math.sin(M) - 0.114332 * math.sin(2 * F) \
        + 0.058793 * math.sin(2 * D - 2 * Mp) + 0.057066 * math.sin(2 * D - M - Mp) + 0.053322 * math.sin(2 * D + Mp) \
        + 0.045758 * math.sin(2 * D - M) - 0.040923 * math.sin(M - Mp) - 0.034720 * math.sin(D) - 0.030383 * math.sin(M + Mp)
    lat = 5.128122 * math.sin(F) + 0.280602 * math.sin(Mp + F) + 0.277693 * math.sin(Mp - F) + 0.173237 * math.sin(2 * D - F)
    return lon % 360, lat
def illum(jd):
    T = (jd - 2451545.0) / 36525
    ls = sun_lon(T); lm, bm = moon_lon_lat(T)
    psi = math.acos(math.cos(math.radians(bm)) * math.cos(math.radians(lm - ls)))
    # elongation sign (waxing if moon east of sun)
    d = (lm - ls) % 360
    k = (1 - math.cos(psi)) / 2
    return k, d


def moon_disc(dr, cx, cy, r, jd, fill_lit, fill_dark, outline=None):
    """Draw the Moon as it is at Julian date jd (correct illuminated fraction
    and terminator). Waxing lights the right limb (northern-hemisphere view)."""
    k, elong = illum(jd)
    waxing = elong < 180
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill_dark, outline=outline)
    if waxing:
        dr.pieslice([cx - r, cy - r, cx + r, cy + r], -90, 90, fill=fill_lit)
    else:
        dr.pieslice([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=fill_lit)
    ex = abs(2 * k - 1) * r
    color = fill_lit if k > 0.5 else fill_dark
    if ex > 0.5:
        dr.ellipse([cx - ex, cy - r, cx + ex, cy + r], fill=color)
    if outline:
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=outline, width=1)
    return k


def image4_equinox():
    s = SS
    img, dr = new_canvas(WHITE)
    ink = Ink()

    # --- terminator globe, axis upright, lit from the right (equinox: day/night split exactly pole to pole)
    gx, gy, gr = 108 * s, 118 * s, 88 * s
    # soft shading: darker toward the terminator on the lit side, black on the night side
    for i in range(int(gr), 0, -1):
        pass
    dr.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=WHITE, outline=BLACK, width=int(1.5 * s))
    # night half (left) with a dusky gradient into the terminator
    night = Image.new("L", img.size, 0)
    nd = ImageDraw.Draw(night)
    for x in range(int(gx - gr), int(gx + gr)):
        t = (x - (gx - gr)) / (2 * gr)  # 0 left .. 1 right
        # brightness: night 0 until 0.5, ramp near the terminator, then bright
        if t < 0.46:
            v = 0
        elif t < 0.54:
            v = int(255 * (t - 0.46) / 0.08)
        else:
            v = 255
        v = 255 - v  # mask darkness
        nd.line([(x, gy - gr), (x, gy + gr)], fill=v)
    circ = Image.new("L", img.size, 0)
    ImageDraw.Draw(circ).ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=255)
    from PIL import ImageChops
    mask = ImageChops.multiply(night, circ)
    img.paste(Image.new("RGB", img.size, BLACK), (0, 0), mask)
    # graticule: latitude ellipses & meridians
    for lat in (-60, -30, 0, 30, 60):
        y = gy - gr * math.sin(math.radians(lat))
        rx = gr * math.cos(math.radians(lat))
        col = RED if lat == 0 else (120, 120, 120)
        dr.line([(gx - rx, y), (gx + rx, y)], fill=col, width=int((2.2 if lat == 0 else 1.0) * s))
    for lon in (-60, -30, 0, 30, 60):
        rx = gr * math.sin(math.radians(lon))
        if abs(rx) < 1:
            dr.line([(gx, gy - gr), (gx, gy + gr)], fill=(120, 120, 120), width=int(1.0 * s))
        else:
            dr.ellipse([gx - abs(rx), gy - gr, gx + abs(rx), gy + gr], outline=(120, 120, 120), width=int(1.0 * s))
    # axis ticks (poles)
    dr.line([(gx, gy - gr - 8 * s), (gx, gy - gr + 4 * s)], fill=BLACK, width=int(1.5 * s))
    dr.line([(gx, gy + gr - 4 * s), (gx, gy + gr + 8 * s)], fill=BLACK, width=int(1.5 * s))
    # sun rays from the right
    for k in range(-3, 4):
        y = gy + k * 22 * s
        dr.line([(gx + gr + 10 * s, y), (gx + gr + 26 * s, y)], fill=RED, width=int(2 * s))

    # --- text block
    fh = font(FONT_SERIF_B, int(24 * s))
    ink.text((228 * s, 26 * s), "EQUINOX", fh, BLACK)
    fs = font(FONT_SERIF, int(10.5 * s))
    lines = [
        "in 6 days",
        "Tue 22 Sep · 00:05 UTC",
        "",
        "The terminator runs pole to",
        "pole; every latitude gets",
        "twelve hours of sun.",
        "",
        "Today the Sun stands",
        "2.3° north of the equator",
        "and drops 0.4° a day.",
    ]
    y = 58 * s
    for ln in lines:
        if ln == "in 6 days":
            ink.text((228 * s, y), ln, font(FONT_SERIF_B, int(13 * s)), RED)
        else:
            ink.text((228 * s, y), ln, fs, BLACK)
        y += 14.5 * s

    # --- moon strip: Sep 16..30 at 12h UTC, phases from the ephemeris above
    strip_y = 246 * s
    fm = font(FONT_MONO_B, int(7.5 * s))
    dr.line([(8 * s, strip_y - 20 * s), (392 * s, strip_y - 20 * s)], fill=BLACK, width=int(1 * s))
    ink.text((8 * s, strip_y - 32 * s), "MOON, REST OF SEPTEMBER", font(FONT_MONO_B, int(8 * s)), BLACK)
    ink.text((296 * s, strip_y - 32 * s), "26th: HARVEST MOON", font(FONT_MONO_B, int(8 * s)), RED)
    days = list(range(16, 31))
    pitch = (W * s - 30 * s) / (len(days) - 1)
    mr = 9 * s
    for i, d in enumerate(days):
        cx = 15 * s + pitch * i
        k = moon_disc(dr, cx, strip_y, mr, jd_utc(2026, 9, d, 12), WHITE, BLACK, outline=BLACK)
        lbl = str(d)
        bb = ink.textbbox(lbl, fm)
        col = RED if d == 16 else BLACK
        ink.text((cx - (bb[2] - bb[0]) / 2 - bb[0], strip_y + 13 * s), lbl, fm, col)
        if d == 16:
            dr.ellipse([cx - mr - 3 * s, strip_y - mr - 3 * s, cx + mr + 3 * s, strip_y + mr + 3 * s], outline=RED, width=int(2 * s))
        if d == 26:
            dr.ellipse([cx - mr - 3 * s, strip_y - mr - 3 * s, cx + mr + 3 * s, strip_y + mr + 3 * s], outline=RED, width=int(2 * s))
    # today's fraction
    k, _ = illum(jd_utc(2026, 9, 16, 12))
    age_today = jd_utc(2026, 9, 16, 12) - jd_utc(2026, 9, 11, 0)  # new moon ~2026-09-11 00h UTC
    fc = font(FONT_MONO_B, int(7.5 * s))
    ink.text((8 * s, strip_y + 26 * s), f"TODAY: waxing crescent, {int(round(k * 100))}% lit, age {age_today:.1f} days", fc, BLACK)
    ink.text((8 * s, strip_y + 36 * s), "VENUS at greatest brilliancy Thu 18th, mag -4.8, low in the west after sunset", fc, BLACK)
    return finalize(img, dither=True, ink=ink)


# --------------------------------------------------------------- 5. Mayflower
def image5_mayflower():
    rng = random.Random(1620_0916)
    s = SS
    img, dr = new_canvas(WHITE)
    ink = Ink()
    horizon = 168 * s

    # sky: light gray gradient toward horizon (dither will turn it into fine grain)
    for y in range(0, int(horizon)):
        t = y / horizon
        v = int(255 - 60 * t ** 2.2)
        dr.line([(0, y), (W * s, y)], fill=(v, v, v))
    # the red sun, low, big
    sr = 46 * s
    sx, sy = 262 * s, horizon - 14 * s
    dr.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=RED)
    # a few streak clouds cutting the sun (woodcut bands)
    for (y, x0, x1, hgt) in [(0.34, 0.50, 0.96, 3), (0.40, 0.42, 0.90, 2), (0.47, 0.55, 0.99, 4)]:
        dr.rectangle([x0 * W * s, y * H * s, x1 * W * s, y * H * s + hgt * s], fill=(235, 235, 235))

    # sea: layered wave bands, front ones darker, with white crests
    bands = 9
    for b in range(bands):
        t = b / (bands - 1)  # 0 far .. 1 near
        y0 = horizon + t ** 1.4 * (H * s - horizon) * 0.92
        amp = (2 + 9 * t) * s
        wl = (34 + 60 * t) * s
        phase = rng.uniform(0, 2 * math.pi)
        shade = int(150 - 150 * t)  # far bands gray, near bands black
        pts = []
        for x in range(-10, W * s + 11, 4):
            yy = y0 + amp * math.sin(2 * math.pi * x / wl + phase) + amp * 0.35 * math.sin(2 * math.pi * x / (wl * 0.37) + phase * 2)
            pts.append((x, yy))
        poly = pts + [(W * s + 10, H * s + 10), (-10, H * s + 10)]
        dr.polygon(poly, fill=(shade, shade, shade))
        # white crest line along the top of the band
        dr.line(pts, fill=WHITE, width=int((1 + 1.6 * t) * s))
        # hokusai claws: little foam curls on wave tops for the near bands
        if t > 0.45:
            for x in range(int(-10 + rng.uniform(0, wl)), W * s, int(wl)):
                # find a crest: use the derivative sign change approx — sample max in window
                seg = [p for p in pts if x <= p[0] < x + wl]
                if not seg:
                    continue
                px, py = min(seg, key=lambda p: p[1])
                for j in range(4):
                    fr = (2.5 + j * 2.2) * s * (0.6 + t)
                    ox = px - 6 * s * j
                    oy = py - 2 * s * j
                    dr.ellipse([ox - fr * 0.4, oy - fr * 0.4, ox + fr * 0.4, oy + fr * 0.4], fill=WHITE)

    # the ship: black silhouette hull, white sails with black outlines, red pennants
    bx, by = 150 * s, horizon + 30 * s  # waterline center
    hull = [
        (bx - 62 * s, by - 8 * s), (bx + 58 * s, by - 8 * s), (bx + 70 * s, by - 26 * s),
        (bx + 50 * s, by - 24 * s), (bx + 46 * s, by - 12 * s), (bx - 40 * s, by - 12 * s),
        (bx - 56 * s, by - 30 * s), (bx - 72 * s, by - 24 * s),
    ]
    dr.polygon(hull, fill=BLACK)
    # sterncastle block
    dr.rectangle([bx + 30 * s, by - 40 * s, bx + 62 * s, by - 24 * s], fill=BLACK)
    dr.rectangle([bx + 36 * s, by - 36 * s, bx + 40 * s, by - 30 * s], fill=WHITE)
    dr.rectangle([bx + 46 * s, by - 36 * s, bx + 50 * s, by - 30 * s], fill=WHITE)
    # bowsprit
    dr.line([(bx - 62 * s, by - 26 * s), (bx - 98 * s, by - 46 * s)], fill=BLACK, width=int(2.5 * s))
    # masts
    masts = [(bx - 30 * s, 92), (bx + 6 * s, 112), (bx + 44 * s, 70)]
    for (mx, mh) in masts:
        dr.line([(mx, by - 10 * s), (mx, by - mh * s)], fill=BLACK, width=int(2.5 * s))

    def sail(mx, ytop, wtop, hgt, belly):
        # curved square sail: belly bulges to the left (wind from the right/astern)
        pts = [(mx - wtop / 2, ytop), (mx + wtop / 2, ytop)]
        for i in range(1, 12):
            u = i / 12
            pts.append((mx + wtop / 2 + belly * math.sin(math.pi * u) * 0.3, ytop + hgt * u))
        pts.append((mx + wtop / 2, ytop + hgt))
        pts.append((mx - wtop / 2, ytop + hgt))
        for i in range(11, 0, -1):
            u = i / 12
            pts.append((mx - wtop / 2 - belly * math.sin(math.pi * u), ytop + hgt * u))
        dr.polygon(pts, fill=WHITE, outline=BLACK, width=int(1.6 * s))
        # yard
        dr.line([(mx - wtop / 2 - 4 * s, ytop), (mx + wtop / 2 + 4 * s, ytop)], fill=BLACK, width=int(2 * s))
        # woodcut hatching lines on the sail
        for j in range(1, 4):
            dr.line([(mx - wtop / 2 + 2 * s, ytop + hgt * j / 4), (mx + wtop / 2 - 2 * s, ytop + hgt * j / 4)], fill=(130, 130, 130), width=int(1 * s))

    # foremast
    sail(bx - 30 * s, by - 84 * s, 34 * s, 26 * s, 8 * s)
    sail(bx - 30 * s, by - 54 * s, 44 * s, 34 * s, 10 * s)
    # mainmast
    sail(bx + 6 * s, by - 104 * s, 36 * s, 26 * s, 9 * s)
    sail(bx + 6 * s, by - 72 * s, 50 * s, 40 * s, 12 * s)
    # mizzen: lateen triangle
    dr.polygon([(bx + 44 * s, by - 66 * s), (bx + 72 * s, by - 30 * s), (bx + 40 * s, by - 32 * s)], fill=WHITE, outline=BLACK, width=int(1.6 * s))
    # spritsail under the bowsprit
    dr.polygon([(bx - 70 * s, by - 32 * s), (bx - 92 * s, by - 44 * s), (bx - 90 * s, by - 24 * s), (bx - 70 * s, by - 16 * s)], fill=WHITE, outline=BLACK, width=int(1.6 * s))
    # rigging
    for (mx, mh) in masts:
        dr.line([(mx, by - mh * s), (bx + 74 * s, by - 26 * s)], fill=BLACK, width=int(1 * s))
        dr.line([(mx, by - mh * s), (bx - 80 * s, by - 24 * s)], fill=BLACK, width=int(1 * s))
    # red pennants at mastheads
    for (mx, mh) in masts:
        top = by - mh * s
        dr.polygon([(mx, top), (mx - 18 * s, top + 3 * s), (mx, top + 7 * s)], fill=RED)

    # re-draw the nearest wave band over the hull so the ship sits IN the sea
    t = 0.62
    y0 = horizon + t ** 1.4 * (H * s - horizon) * 0.92
    amp, wl, phase = (2 + 9 * t) * s, (34 + 60 * t) * s, 1.3
    pts = [(x, y0 + amp * math.sin(2 * math.pi * x / wl + phase)) for x in range(-10, W * s + 11, 4)]
    dr.polygon(pts + [(W * s + 10, y0 + 30 * s), (-10, y0 + 30 * s)], fill=(int(150 - 150 * t),) * 3)
    dr.line(pts, fill=WHITE, width=int(2.5 * s))

    # text
    ft = font(FONT_SERIF_B, int(26 * s))
    ink.text((12 * s, 10 * s), "MAYFLOWER", ft, BLACK)
    fs = font(FONT_SERIF_B, int(9.5 * s))
    ink.text((13 * s, 40 * s), "left Plymouth on this day, 1620", fs, BLACK)
    ink.text((13 * s, 53 * s), "102 souls · 66 days · Cape Cod 9 Nov", fs, BLACK)
    fm = font(FONT_MONO_B, int(8 * s))
    ink.text((13 * s, 70 * s), "406 years ago", fm, RED)
    return finalize(img, dither=True, ink=ink)


if __name__ == "__main__":
    import os, sys
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    for i, fn in enumerate([image1_papel_picado, image2_red_wedge, image3_kamon, image4_equinox, image5_mayflower], 1):
        im = fn()
        assert im.size == (W, H)
        im.save(os.path.join(outdir, f"{i}.png"), optimize=True)
        print("wrote", i, fn.__name__)
