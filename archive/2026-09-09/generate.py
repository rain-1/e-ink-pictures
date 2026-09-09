#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-09 (Chōyō no Sekku · the moth · kuku · new moon).

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

Three render modes are used today:
  * TONAL  — render at 3x in grayscale+red, LANCZOS downscale, Floyd–Steinberg
             dither into the palette (photographic / painterly pieces).
  * CLEAN  — render at 3x with antialiasing, LANCZOS downscale, quantize with
             NO dither: smooth curves, hard edges, no speckle (crests, posters).
  * PIXEL  — render at 1x in pure palette colors (grids, dot arrays).
"""

import math
import os
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
FONT_HAND = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED)
    palette += [0, 0, 0] * (256 - 3)
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=True):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, int(size))


def rot_ellipse(cx, cy, a, b, ang, n=48):
    """Polygon points of an ellipse (semi-axes a along `ang`, b across)."""
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        x, y = a * math.cos(t), b * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def petal_poly(cx, cy, r0, r1, ang, width, n=24):
    """A kamon-style petal: narrow at the centre, rounded at the tip."""
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    L = r1 - r0
    # one side out, tip, other side back
    for k in range(n + 1):
        t = k / n
        rr = r0 + L * t
        w = width * (0.25 + 0.75 * math.sin(math.pi * min(t, 0.85) / 1.7)) if t < 0.85 else width
        if t >= 0.85:
            w = width * math.sqrt(max(0.0, 1 - ((t - 0.85) / 0.15) ** 2))
        pts.append((rr, w))
    side1 = [(cx + rr * ca - w * sa, cy + rr * sa + w * ca) for rr, w in pts]
    side2 = [(cx + rr * ca + w * sa, cy + rr * sa - w * ca) for rr, w in reversed(pts)]
    return side1 + side2


# ================================================================ 1. KAMON
def draw_omote_kiku(dr, cx, cy, R, n=16, double=True, core=RED, s=SS):
    """Front-facing chrysanthemum crest, `n` petals, optional back layer."""
    lw = max(1, int(1.2 * s))
    if double:
        for k in range(n):
            ang = 2 * math.pi * (k + 0.5) / n - math.pi / 2
            poly = petal_poly(cx, cy, 0.15 * R, 1.0 * R, ang, math.pi * R / n * 0.70)
            dr.polygon(poly, fill=BLACK, outline=WHITE, width=lw)
    for k in range(n):
        ang = 2 * math.pi * k / n - math.pi / 2
        poly = petal_poly(cx, cy, 0.05 * R, 0.88 * R, ang, math.pi * R / n * 0.72)
        dr.polygon(poly, fill=BLACK, outline=WHITE, width=lw)
    rc = 0.22 * R
    dr.ellipse([cx - rc - lw * 1.5, cy - rc - lw * 1.5, cx + rc + lw * 1.5, cy + rc + lw * 1.5], fill=WHITE)
    dr.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=core)


def draw_ura_kiku(dr, cx, cy, R, n=16, s=SS):
    """Back-facing chrysanthemum: petals with a five-lobed calyx in front."""
    lw = max(1, int(1.2 * s))
    for k in range(n):
        ang = 2 * math.pi * k / n - math.pi / 2
        poly = petal_poly(cx, cy, 0.05 * R, 1.0 * R, ang, math.pi * R / n * 0.72)
        dr.polygon(poly, fill=BLACK, outline=WHITE, width=lw)
    # calyx lobes
    for k in range(5):
        ang = 2 * math.pi * k / 5 - math.pi / 2
        poly = petal_poly(cx, cy, 0.0, 0.55 * R, ang, 0.19 * R)
        dr.polygon(poly, fill=WHITE)
        inner = petal_poly(cx, cy, 0.02 * R, 0.48 * R, ang, 0.14 * R)
        dr.polygon(inner, fill=BLACK)
    rc = 0.08 * R
    dr.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=WHITE)


def draw_kikusui(dr, cx, cy, R, s=SS):
    """Chrysanthemum floating on flowing water (kikusui)."""
    lw = max(1, int(1.2 * s))
    # water: three bands of curved strokes under the flower
    for i, (dy, thick) in enumerate([(0.30, 0.10), (0.55, 0.09), (0.78, 0.08)]):
        pts = []
        for k in range(0, 41):
            t = k / 40
            x = cx - R * 1.05 + 2.1 * R * t
            y = cy + dy * R + 0.13 * R * math.sin(2 * math.pi * (t * 1.5 + 0.3 * i))
            pts.append((x, y))
        dr.line(pts, fill=BLACK, width=int(thick * R), joint="curve")
    # flower: half crest peeking above the water
    n = 16
    mask = Image.new("L", dr._image.size, 0)
    md = ImageDraw.Draw(mask)
    md.rectangle([cx - 2 * R, cy - 2 * R, cx + 2 * R, cy + 0.18 * R], fill=255)
    layer = Image.new("RGB", dr._image.size, WHITE)
    ld = ImageDraw.Draw(layer)
    draw_omote_kiku(ld, cx, cy - 0.15 * R, 0.78 * R, n=n, double=True, core=BLACK, s=s)
    dr._image.paste(layer, (0, 0), mask)


def draw_kikubishi(dr, cx, cy, R, s=SS):
    """Diamond chrysanthemum (kiku-bishi): four petals in a lozenge."""
    lw = max(1, int(1.2 * s))
    for k in range(4):
        ang = math.pi / 2 * k
        poly = petal_poly(cx, cy, 0.0, R, ang, 0.5 * R)
        dr.polygon(poly, fill=BLACK, outline=WHITE, width=lw)
    for k in range(4):
        ang = math.pi / 2 * k
        for sign in (-1, 1):
            a2 = ang + sign * 0.30
            poly = petal_poly(cx, cy, 0.0, 0.62 * R, a2, 0.10 * R)
            dr.polygon(poly, fill=WHITE)
    rc = 0.1 * R
    dr.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=WHITE)


def image1_kamon():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # the big imperial-style crest: 16 petals, double layer, front
    draw_omote_kiku(dr, 150 * s, 150 * s, 118 * s, n=16, double=True, core=RED)

    # four smaller variants down the right-hand side
    variants = [
        ("hitoe · single", lambda x, y: draw_omote_kiku(dr, x, y, 26 * s, n=12, double=False, core=BLACK)),
        ("ura · from behind", lambda x, y: draw_ura_kiku(dr, x, y, 26 * s, n=16)),
        ("kikusui · on water", lambda x, y: draw_kikusui(dr, x, y, 27 * s)),
        ("kikubishi · diamond", lambda x, y: draw_kikubishi(dr, x, y, 27 * s)),
    ]
    f_lab = font(FONT_SANS, 8 * s)
    xs = 312
    for i, (label, fn) in enumerate(variants):
        y = 38 + i * 66
        fn(xs * s, y * s)
        dr.text((xs * s, (y + 31) * s), label, font=f_lab, fill=BLACK, anchor="ma")

    # vertical title 重陽 in red, far right
    f_jp = font(FONT_JP, 24 * s)
    for i, ch in enumerate("重陽"):
        dr.text((380 * s, (36 + i * 28) * s), ch, font=f_jp, fill=RED, anchor="mm")
    f_t = font(FONT_SANS_B, 9 * s)
    f_c = font(FONT_SANS, 8 * s)
    dr.text((14 * s, (H - 20) * s), "CHŌYŌ NO SEKKU", font=f_t, fill=RED)
    dr.text((14 * s, (H - 10) * s), "the ninth of the ninth · the chrysanthemum festival · 16 petals for the sun",
            font=f_c, fill=BLACK)
    dr.text((14 * s, 10 * s), "KIKU-MON", font=f_t, fill=BLACK)
    dr.text((14 * s, 20 * s), "jūroku-yae-omote-kiku", font=f_c, fill=BLACK)
    return finalize(img, dither=False)


# ============================================================== 2. KISEWATA
def image2_kisewata():
    rng = random.Random(20260909)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # faint dawn: a gradient band low on the right, dithers into mist
    for y in range(int(150 * s), H * s):
        t = (y - 150 * s) / (H * s - 150 * s)
        v = int(28 * t)
        dr.line([0, y, W * s, y], fill=(v, v, v))

    # the bloom, built by phyllotaxis (Vogel): petal i at angle i*137.5°, r ~ sqrt(i)
    cx, cy = 272 * s, 176 * s
    N = 130
    golden = math.radians(137.50776)
    c = 7.4 * s
    petals = []
    for i in range(N):
        ang = i * golden
        r = c * math.sqrt(i + 1)
        petals.append((i, ang, r))
    # draw outer petals first so inner ones sit on top
    for i, ang, r in reversed(petals):
        L = 18 * s + 0.55 * r
        r0 = max(0, r - 0.55 * L)
        r1 = r + 0.45 * L
        wdt = 3.1 * s + 0.055 * r
        # curl the petal slightly
        ang2 = ang + 0.04 * math.sin(i)
        poly = petal_poly(cx, cy, r0, r1, ang2, wdt, n=18)
        t = i / N
        v = int(235 - 90 * (1 - t))  # inner petals darker (in shadow), outer lighter
        dr.polygon(poly, fill=(v, v, v), outline=(20, 20, 20), width=max(1, int(0.9 * s)))
    # centre: tight dark whorl
    dr.ellipse([cx - 5 * s, cy - 5 * s, cx + 5 * s, cy + 5 * s], fill=(90, 90, 90))

    # the cotton floss (kisewata) laid over the top of the bloom: fluffy white
    for _ in range(420):
        ang = rng.uniform(math.pi * 1.05, math.pi * 1.95)
        rad = rng.uniform(0, 1) ** 0.6 * 96 * s
        x = cx + rad * math.cos(ang)
        y = cy + rad * math.sin(ang) * 0.75 - 18 * s
        rr = rng.uniform(3, 11) * s
        v = rng.choice([255, 255, 245, 235, 225])
        dr.ellipse([x - rr, y - rr * 0.8, x + rr, y + rr * 0.8], fill=(v, v, v))
    # loose wisps at the edges
    for _ in range(60):
        ang = rng.uniform(math.pi * 1.0, math.pi * 2.0)
        rad = rng.uniform(90, 110) * s
        x = cx + rad * math.cos(ang)
        y = cy + rad * math.sin(ang) * 0.75 - 18 * s
        rr = rng.uniform(1.5, 4) * s
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(200, 200, 200))

    # dew: bright beads sitting on the cotton, each with a dark rim
    for _ in range(26):
        ang = rng.uniform(math.pi * 1.1, math.pi * 1.9)
        rad = rng.uniform(0.2, 0.95) * 86 * s
        x = cx + rad * math.cos(ang)
        y = cy + rad * math.sin(ang) * 0.75 - 18 * s
        rr = rng.uniform(1.6, 3.4) * s
        dr.ellipse([x - rr - s, y - rr - s, x + rr + s, y + rr + s], fill=(40, 40, 40))
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=WHITE)

    # stem, leaving the frame at the bottom
    dr.line([(cx, cy + 40 * s), (cx - 30 * s, H * s + 10 * s)], fill=(60, 60, 60), width=int(3 * s))

    # text, left column
    f_h = font(FONT_SERIF_B, 17 * s)
    f_b = font(FONT_SERIF, 9 * s)
    f_jp = font(FONT_JP, 13 * s)
    x0 = 16 * s
    dr.text((x0, 18 * s), "kisewata", font=f_h, fill=WHITE)
    dr.text((x0, 40 * s), "菊の被綿", font=f_jp, fill=RED)
    lines = [
        "On the eve of the ninth",
        "the Heian court laid",
        "floss cotton over the",
        "chrysanthemums.",
        "",
        "All night it drank",
        "the dew and the scent",
        "of the flower.",
        "",
        "At dawn you wiped",
        "your face with it, and",
        "were promised long life.",
    ]
    y = 64
    for ln in lines:
        dr.text((x0, y * s), ln, font=f_b, fill=WHITE)
        y += 12.5
    dr.text((x0, (H - 28) * s), "Chōyō no Sekku · 9 IX", font=font(FONT_SANS, 8 * s), fill=WHITE)
    dr.text((x0, (H - 16) * s), "petals set by the golden angle, 137.5°",
            font=font(FONT_SANS, 8 * s), fill=(170, 170, 170))
    # red seal
    sx, sy = 368 * s, 22 * s
    dr.rectangle([sx - 13 * s, sy - 13 * s, sx + 13 * s, sy + 13 * s], fill=RED)
    dr.text((sx, sy + s), "菊", font=font(FONT_JP, 19 * s), fill=WHITE, anchor="mm")
    return finalize(img, dither=True)


# ================================================================ 3. THE MOTH
def moth_polygon_wing(cx, cy, scale, side, fore=True):
    """Points for a moth wing, side=+1 right, -1 left. Hand-placed control shape."""
    if fore:
        shape = [(0.05, -0.10), (0.35, -0.55), (0.80, -0.75), (1.20, -0.72), (1.42, -0.55),
                 (1.45, -0.30), (1.30, -0.05), (1.00, 0.08), (0.60, 0.12), (0.25, 0.10), (0.05, 0.05)]
    else:
        shape = [(0.05, 0.05), (0.40, 0.08), (0.80, 0.18), (1.05, 0.38), (1.02, 0.62),
                 (0.82, 0.78), (0.52, 0.80), (0.25, 0.66), (0.08, 0.40)]
    return [(cx + side * x * scale, cy + y * scale) for x, y in shape]


def draw_moth(dr, cx, cy, scale, s):
    rng = random.Random(1947)
    for side in (-1, 1):
        hind = moth_polygon_wing(cx, cy, scale, side, fore=False)
        dr.polygon(hind, fill=RED, outline=BLACK, width=int(1.2 * s))
    for side in (-1, 1):
        fore = moth_polygon_wing(cx, cy, scale, side, fore=True)
        dr.polygon(fore, fill=RED, outline=BLACK, width=int(1.2 * s))
        # veins
        for (ex, ey) in [(1.40, -0.50), (1.38, -0.28), (1.20, -0.08), (0.95, -0.70), (0.60, -0.62)]:
            dr.line([(cx + side * 0.08 * scale, cy - 0.05 * scale),
                     (cx + side * ex * scale, cy + ey * scale)], fill=BLACK, width=max(1, int(0.6 * s)))
        # eyespot
        ex, ey = cx + side * 0.95 * scale, cy - 0.42 * scale
        rr = 0.07 * scale
        dr.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=BLACK)
        # scalloped wing edge: little black notches
        for (ex2, ey2) in [(1.44, -0.42), (1.38, -0.17)]:
            dr.ellipse([cx + side * ex2 * scale - 0.03 * scale, cy + ey2 * scale - 0.03 * scale,
                        cx + side * ex2 * scale + 0.03 * scale, cy + ey2 * scale + 0.03 * scale], fill=WHITE)
    # body
    bw, bh = 0.09 * scale, 0.72 * scale
    dr.ellipse([cx - bw, cy - 0.30 * scale, cx + bw, cy - 0.30 * scale + bh], fill=BLACK)
    for k in range(5):
        yy = cy - 0.05 * scale + k * 0.09 * scale
        dr.line([(cx - bw * 0.9, yy), (cx + bw * 0.9, yy)], fill=WHITE, width=max(1, int(0.5 * s)))
    # head + feathery antennae
    hr = 0.08 * scale
    hy = cy - 0.34 * scale
    dr.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=BLACK)
    for side in (-1, 1):
        pts = []
        for k in range(12):
            t = k / 11
            x = cx + side * (0.05 + 0.55 * t) * scale
            y = hy - (0.15 + 0.55 * t - 0.25 * t * t) * scale
            pts.append((x, y))
        dr.line(pts, fill=BLACK, width=max(1, int(0.8 * s)))
        for k in range(1, 12, 1):
            x, y = pts[k]
            ln = (0.05 + 0.03 * math.sin(k)) * scale
            dr.line([(x, y), (x + side * 0.4 * ln, y - ln)], fill=BLACK, width=max(1, int(0.5 * s)))
            dr.line([(x, y), (x - side * 0.1 * ln, y + ln)], fill=BLACK, width=max(1, int(0.5 * s)))


def image3_moth():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # ruled paper: faint lines (dither to dotted), red margin rule
    for y in range(52, H - 8, 16):
        dr.line([0, y * s, W * s, y * s], fill=(160, 160, 160), width=s)
    dr.line([40 * s, 0, 40 * s, H * s], fill=RED, width=s)
    # binder holes
    for hy in (60, 150, 240):
        dr.ellipse([12 * s, hy * s - 5 * s, 22 * s, hy * s + 5 * s], fill=(200, 200, 200), outline=(90, 90, 90), width=s)

    f_head = font(FONT_MONO_B, 9 * s)
    f_hand = font(FONT_HAND, 13 * s)
    f_hand_b = font(FONT_HAND, 15 * s)
    f_sm = font(FONT_SANS, 7.5 * s)

    dr.text((48 * s, 12 * s), "HARVARD MARK II  ·  RELAY CALCULATOR  ·  LOG", font=f_head, fill=BLACK)
    # rules are at y = 52 + 16k; handwriting sits on the rule (baseline 3px above it)
    def hand(x, rule_y, txt, fnt=f_hand):
        dr.text((x * s, (rule_y - 3) * s), txt, font=fnt, fill=BLACK, anchor="ls")

    hand(48, 52, "Tuesday, 9 September 1947")

    entries = [
        (68, "1100", "Started Cosine Tape (Sine check)"),
        (84, "1525", "Started Mult + Adder Test."),
        (100, "1545", "Relay #70  Panel F"),
    ]
    for y, t, txt in entries:
        hand(48, y, t)
        hand(92, y, txt)
    hand(92, 116, "(moth) in relay.")

    # the moth, taped in below
    mx, my = 205 * s, 168 * s
    draw_moth(dr, mx, my, 42 * s, s)
    # two strips of cellophane tape
    for (tx, ty, ang) in [(mx - 46 * s, my - 18 * s, 22), (mx + 46 * s, my + 12 * s, -18)]:
        tw, th = 44 * s, 11 * s
        a = math.radians(ang)
        ca, sa = math.cos(a), math.sin(a)
        pts = [(tx + x * ca - y * sa, ty + x * sa + y * ca)
               for x, y in [(-tw / 2, -th / 2), (tw / 2, -th / 2), (tw / 2, th / 2), (-tw / 2, th / 2)]]
        dr.polygon(pts, fill=(215, 215, 215), outline=(120, 120, 120), width=s)

    hand(92, 228, "First actual case of bug being found.", f_hand_b)
    # underline the famous sentence, slightly wobbly like pen
    ux0, ux1 = 92 * s, 330 * s
    pts = [(ux0 + (ux1 - ux0) * k / 30, 230 * s + 1.2 * s * math.sin(k * 0.9)) for k in range(31)]
    dr.line(pts, fill=BLACK, width=s)

    hand(48, 260, "1700")
    hand(92, 260, "closed down.")

    dr.text((48 * s, (H - 22) * s),
            "79 years ago today. The moth is still taped in the book, at the Smithsonian.",
            font=f_sm, fill=BLACK)
    dr.text((48 * s, (H - 12) * s),
            "we have been debugging ever since", font=f_sm, fill=RED)
    return finalize(img, dither=True)


# ================================================================== 4. KUKU
def image4_kuku():
    # Geometry is pixel-aligned at 1x and scaled by s so the dots stay crisp
    # after the LANCZOS downscale; text gets the benefit of antialiasing.
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    cell = 27
    ox, oy = 26, 24
    f_jp = font(FONT_JP, 12 * s)
    kanji = "一二三四五六七八九"
    # axis labels
    for k in range(9):
        dr.text(((ox + k * cell + cell // 2) * s, (oy - 8) * s), kanji[k], font=f_jp, fill=BLACK, anchor="mm")
        dr.text(((ox - 9) * s, (oy + k * cell + cell // 2) * s), kanji[k], font=f_jp, fill=BLACK, anchor="mm")
    # grid
    for k in range(10):
        dr.line([(ox + k * cell) * s, oy * s, (ox + k * cell) * s, (oy + 9 * cell) * s], fill=BLACK, width=s)
        dr.line([ox * s, (oy + k * cell) * s, (ox + 9 * cell) * s, (oy + k * cell) * s], fill=BLACK, width=s)
    # dots: cell (i, j) holds an i-by-j array of 2px dots => i*j dots
    pitch = 2.75
    for j in range(1, 10):        # row = j
        for i in range(1, 10):    # column = i
            x0 = ox + (i - 1) * cell + 2
            y0 = oy + (j - 1) * cell + 2
            colr = RED if (i * j) % 9 == 0 else BLACK
            for a in range(i):
                for b in range(j):
                    x = int(x0 + a * pitch)
                    y = int(y0 + b * pitch)
                    dr.rectangle([x * s, y * s, (x + 2) * s - 1, (y + 2) * s - 1], fill=colr)

    # right column text
    xr = 292
    f_big = font(FONT_JP, 46 * s)
    dr.text(((xr + 48) * s, 22 * s), "九", font=f_big, fill=RED, anchor="ma")
    dr.text(((xr + 48) * s, 70 * s), "九", font=f_big, fill=RED, anchor="ma")
    f_b = font(FONT_SANS_B, 10 * s)
    f_s = font(FONT_SANS, 8 * s)
    dr.text((xr * s, 132 * s), "KUKU", font=f_b, fill=BLACK)
    for k, ln in enumerate([
        "the times table,",
        "named 9×9 and",
        "chanted by every",
        "Japanese child.",
        "",
        "Each cell holds",
        "its product as dots.",
        "",
        "Red: multiples of 9.",
        "Their digits always",
        "sum to nine.",
        "",
        "9 · 9 · 2026",
    ]):
        dr.text((xr * s, (146 + k * 10.5) * s), ln, font=f_s, fill=RED if ln.startswith("Red") else BLACK)
    dr.text((ox * s, (oy + 9 * cell + 8) * s), "in-in ga ichi … ku-ku hachijū-ichi", font=f_s, fill=BLACK)
    dr.text((ox * s, (oy + 9 * cell + 19) * s),
            "a 1,300-year-old wooden kuku tablet was dug up at Fujiwara-kyō", font=f_s, fill=BLACK)
    return finalize(img, dither=False)


# ========================================================== 5. CONSTRUCTIVIST
def rotated_text(txt, fnt, fill, angle, bg=WHITE):
    """Render text to its own image and rotate it (expanded, transparent)."""
    x0, y0, x1, y1 = fnt.getbbox(txt)
    im = Image.new("RGBA", (x1 - x0 + 8, y1 - y0 + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((4 - x0, 4 - y0), txt, font=fnt, fill=fill + (255,))
    return im.rotate(angle, expand=True, resample=Image.BICUBIC)


def image5_constructivist():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # the new moon: a black disc, hanging upper-left
    mx, my, mr = 150 * s, 118 * s, 84 * s
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=BLACK)
    # thin white ring just inside the edge — the moon's limb, barely lit
    dr.ellipse([mx - mr + 6 * s, my - mr + 6 * s, mx + mr - 6 * s, my + mr - 6 * s],
               outline=WHITE, width=s)

    # the red wedge: a meteor driving in from lower-right into the disc
    wedge = [(W * s + 4 * s, (H - 10) * s), (W * s + 4 * s, (H - 62) * s), (mx + 10 * s, my + 22 * s)]
    dr.polygon(wedge, fill=RED)
    # thin black bars: the radiant lines
    for (x0, y0, x1, y1, wd) in [(392, 252, 250, 60, 1.5), (398, 290, 300, 30, 1.0), (330, 296, 290, 150, 1.0)]:
        dr.line([x0 * s, y0 * s, x1 * s, y1 * s], fill=BLACK, width=int(wd * s))
    # horizontal black bar, page structure
    dr.rectangle([0, 214 * s, 244 * s, 226 * s], fill=BLACK)
    # small red squares, the shower's other meteors
    for (x, y, sz) in [(272, 46, 8), (318, 30, 5), (338, 78, 6), (58, 236, 6)]:
        dr.rectangle([x * s, y * s, (x + sz) * s, (y + sz) * s], fill=RED)

    # typography
    f_huge = font(FONT_SANS_B, 33 * s)
    f_big = font(FONT_SANS_B, 22 * s)
    f_med = font(FONT_SANS_B, 11 * s)
    f_sm = font(FONT_SANS, 8.5 * s)
    # vertical NEW MOON along the left edge
    rt = rotated_text("NEW MOON", f_huge, BLACK, 90)
    img.paste(rt, (10 * s, 214 * s - rt.size[1]), rt)
    dr.text((14 * s, 234 * s), "10 · IX", font=f_big, fill=BLACK)
    dr.text((14 * s, 262 * s), "the darkest sky of the month", font=f_sm, fill=BLACK)
    dr.text((14 * s, 274 * s), "no moon from dusk to dawn", font=f_sm, fill=BLACK)
    dr.text((250 * s, 140 * s), "ε-PERSEIDS", font=f_med, fill=RED)
    dr.text((250 * s, 153 * s), "peak tonight, 18h UTC", font=f_sm, fill=BLACK)
    dr.text((250 * s, 164 * s), "radiant in Perseus, NE", font=f_sm, fill=BLACK)
    dr.text((250 * s, 175 * s), "~8 an hour, if you are patient", font=f_sm, fill=BLACK)
    # tiny credit line
    dr.text(((W - 12) * s, 10 * s), "after El Lissitzky, 1919", font=font(FONT_SANS, 7.5 * s), fill=BLACK, anchor="ra")
    return finalize(img, dither=False)


if __name__ == "__main__":
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_kamon, image2_kisewata, image3_moth, image4_kuku, image5_constructivist]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        assert im.size == (W, H)
        print(path, "colors:", cols)
