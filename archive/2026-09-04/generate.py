#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-04.

Five 400x300 images in exactly three colours (white, black, red).
Run from the repo root:  python3 archive/2026-09-04/generate.py
Writes images/1.png … images/5.png and dated copies next to this script.

Today: last-quarter moon; 1550 years since the last western Roman emperor was
deposed (4 Sept 476). Themes: a September moon calendar, an asanoha shoji
lattice, an abelian sandpile, a Roman inscription, a constructivist poster.
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

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATE = "2026-09-04"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=False):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def colophon(dr, s, dark=False):
    """Signature: tiny date + red square, bottom-right. Same on every picture."""
    f = font(FONT_MONO, 8 * s)
    txt = "2026·09·04"
    tw = dr.textlength(txt, font=f)
    x = W * s - tw - 14 * s
    y = H * s - 13 * s
    dr.text((x, y), txt, font=f, fill=WHITE if dark else BLACK)
    dr.rectangle([W * s - 10 * s, y + 1 * s, W * s - 5 * s, y + 6 * s], fill=RED)


def spaced_text(dr, xy, text, f, fill, tracking, anchor_center=False):
    """Draw text with letter-spacing. Returns total width."""
    widths = [dr.textlength(c, font=f) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor_center:
        x = x - total / 2
    for c, w in zip(text, widths):
        dr.text((x, y), c, font=f, fill=fill)
        x += w + tracking
    return total


def save(img, n):
    img.save(os.path.join(ROOT, "images", f"{n}.png"), optimize=True)
    img.save(os.path.join(HERE, f"{n}.png"), optimize=True)


# ------------------------------------------------------------ 1. September moons
SYNODIC = 29.530588853
NEW_MOON_REF = 2451550.1  # JD of 2000-01-06 18:14 UTC


def julian_day(y, m, d, hour=12.0):
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5 + hour / 24


def moon_phase_angle(jd):
    age = (jd - NEW_MOON_REF) % SYNODIC
    return 2 * math.pi * age / SYNODIC  # 0 new, pi full


def draw_moon(dr, cx, cy, r, phi, lit=WHITE, dark=BLACK, ring=WHITE, ring_w=1):
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=dark, outline=ring, width=ring_w)
    c = math.cos(phi)
    for yy in range(-int(r), int(r) + 1):
        w = math.sqrt(max(r * r - yy * yy, 0))
        if phi <= math.pi:  # waxing: right side lit
            x0, x1 = w * c, w
        else:  # waning: left side lit
            x0, x1 = -w, -w * c
        if x1 - x0 > 0.5:
            dr.line([(cx + x0, cy + yy), (cx + x1, cy + yy)], fill=lit, width=1)


def image1_september():
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    f_title = font(FONT_SANS_B, 26 * s)
    f_small = font(FONT_MONO, 8 * s)
    f_day = font(FONT_MONO_B, 8 * s)

    dr.text((16 * s, 12 * s), "SEPTEMBER", font=f_title, fill=WHITE)
    tw = dr.textlength("SEPTEMBER", font=f_title)
    dr.text((16 * s + tw + 10 * s, 24 * s), "2026", font=font(FONT_MONO, 12 * s), fill=RED)
    dr.text((W * s - 16 * s - dr.textlength("moon by night", font=f_small), 30 * s),
            "moon by night", font=f_small, fill=WHITE)

    events = {4: "last quarter", 6: "moon · mars", 8: "moon · jupiter", 11: "new moon",
              18: "first quarter", 22: "venus brightest", 23: "equinox", 26: "harvest moon"}
    today = 4

    cell = 25.6 * s
    r = 8.5 * s
    x0 = 16 * s
    rows_y = [70 * s, 130 * s]
    for day in range(1, 31):
        row = (day - 1) // 15
        col = (day - 1) % 15
        cx = x0 + col * cell + cell / 2
        cy = rows_y[row]
        phi = moon_phase_angle(julian_day(2026, 9, day, 21.0))
        draw_moon(dr, cx, cy, r, phi, ring_w=max(1, s // 2))
        label = str(day)
        lw = dr.textlength(label, font=f_day)
        col_txt = RED if day == today else WHITE
        dr.text((cx - lw / 2, cy + r + 4 * s), label, font=f_day, fill=col_txt)
        if day == today:
            dr.ellipse([cx - r - 4 * s, cy - r - 4 * s, cx + r + 4 * s, cy + r + 4 * s],
                       outline=RED, width=2 * s)
        elif day in events:
            dr.rectangle([cx - 1.5 * s, cy + r + 15 * s, cx + 1.5 * s, cy + r + 18 * s], fill=RED)

    # event list, two columns
    dr.line([(16 * s, 172 * s), (W * s - 16 * s, 172 * s)], fill=WHITE, width=s)
    items = sorted(events.items())
    colx = [16 * s, 210 * s]
    for i, (d, name) in enumerate(items):
        cx = colx[i // 4]
        cy = 182 * s + (i % 4) * 16 * s
        dr.text((cx, cy), f"{d:2d}", font=f_day, fill=RED if d == today else WHITE)
        dr.text((cx + 22 * s, cy), name, font=f_small, fill=WHITE)
    dr.text((16 * s, 250 * s), "tonight: last quarter rises near midnight, high at dawn",
            font=f_small, fill=WHITE)
    dr.text((16 * s, 262 * s), "sat 6: mars 3° south of the crescent before sunrise",
            font=f_small, fill=WHITE)
    colophon(dr, s, dark=True)
    return finalize(img)


# ------------------------------------------------------------ 2. Asanoha shoji
def image2_asanoha():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # red sun behind the screen
    sr = 96 * s
    scx, scy = 262 * s, 128 * s
    dr.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=RED)

    a = 38 * s  # triangle side
    h = a * math.sqrt(3) / 2
    lw = max(2, int(1.6 * s))

    # triangular lattice: rows of points
    pts_rows = []
    y = -h
    row = 0
    while y < H * s + h:
        off = a / 2 if row % 2 else 0
        xs = np.arange(-a, W * s + 2 * a, a) + off
        pts_rows.append([(float(x), float(y)) for x in xs])
        y += h
        row += 1

    def tri(p, q, r):
        cx = (p[0] + q[0] + r[0]) / 3
        cy = (p[1] + q[1] + r[1]) / 3
        for v in (p, q, r):
            dr.line([(cx, cy), v], fill=BLACK, width=lw)
        dr.line([p, q, r, p], fill=BLACK, width=lw)

    for i in range(len(pts_rows) - 1):
        A = pts_rows[i]
        B = pts_rows[i + 1]
        # up/down triangles between row i and i+1
        if i % 2 == 0:
            for j in range(len(A) - 1):
                tri(A[j], A[j + 1], B[j])
                if j + 1 < len(B):
                    tri(A[j + 1], B[j], B[j + 1])
        else:
            for j in range(len(A) - 1):
                if j + 1 < len(B):
                    tri(A[j], A[j + 1], B[j + 1])
                tri(A[j], B[j], B[j + 1])

    # frame + caption plate
    dr.rectangle([0, 0, W * s - 1, H * s - 1], outline=BLACK, width=3 * s)
    plate = [14 * s, 232 * s, 178 * s, 286 * s]
    dr.rectangle(plate, fill=WHITE, outline=BLACK, width=s)
    dr.text((22 * s, 236 * s), "麻の葉", font=font(FONT_JP, 22 * s), fill=BLACK)
    dr.text((22 * s, 262 * s), "asanoha · hemp leaf lattice", font=font(FONT_MONO, 8 * s), fill=BLACK)
    dr.text((22 * s, 273 * s), "a red sun behind the shoji", font=font(FONT_MONO, 8 * s), fill=RED)
    dr.rectangle([W * s - 74 * s, H * s - 17 * s, W * s - 3 * s, H * s - 3 * s], fill=WHITE)
    colophon(dr, s)
    return finalize(img)


# ------------------------------------------------------------ 3. Sandpile
def sandpile(n_grains, shape=(H, W)):
    a = np.zeros(shape, dtype=np.int64)
    a[shape[0] // 2, shape[1] // 2] = n_grains
    while True:
        q = a // 4
        if not q.any():
            break
        a -= 4 * q
        a[1:, :] += q[:-1, :]
        a[:-1, :] += q[1:, :]
        a[:, 1:] += q[:, :-1]
        a[:, :-1] += q[:, 1:]
    return a


def image3_sandpile():
    n = 2 ** 16
    a = sandpile(n)
    # untouched sand (0) -> red field; 1 and 2 grains -> white; 3 grains -> black
    lut = np.array([RED, WHITE, WHITE, BLACK], dtype=np.uint8)
    rgb = lut[np.clip(a, 0, 3)]
    img = Image.fromarray(rgb, "RGB")
    dr = ImageDraw.Draw(img)
    f = font(FONT_MONO_B, 9)
    dr.text((12, 10), "ABELIAN SANDPILE", font=f, fill=WHITE)
    dr.text((12, 22), "2^16 grains dropped on one cell", font=font(FONT_MONO, 8), fill=WHITE)
    dr.text((12, H - 30), "four grains topple, one to each side", font=font(FONT_MONO, 8), fill=WHITE)
    dr.text((12, H - 19), "black = 3 grains  white = 1 or 2", font=font(FONT_MONO, 8), fill=WHITE)
    colophon(dr, 1, dark=True)
    return finalize(img)


# ------------------------------------------------------------ 4. Roma CDLXXVI
def image4_roma():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    f_big = font(FONT_SERIF_B, 112 * s)
    f_cap = font(FONT_SERIF, 13 * s)
    f_capb = font(FONT_SERIF_B, 15 * s)
    f_small = font(FONT_SERIF, 10 * s)

    # rules like an inscription slab
    dr.line([(24 * s, 30 * s), (W * s - 24 * s, 30 * s)], fill=BLACK, width=s)
    dr.line([(24 * s, 34 * s), (W * s - 24 * s, 34 * s)], fill=BLACK, width=s)
    spaced_text(dr, (W * s / 2, 10 * s), "PRIDIE · NONAS · SEPTEMBRES", f_cap, BLACK, 2 * s, True)

    spaced_text(dr, (W * s / 2, 50 * s), "ROMA", f_big, BLACK, 6 * s, True)

    # the red bar: a rule struck through the name, ending in a wedge
    y = 122 * s
    dr.rectangle([24 * s, y - 5 * s, 310 * s, y + 5 * s], fill=RED)
    dr.polygon([(310 * s, y - 14 * s), (W * s - 24 * s, y), (310 * s, y + 14 * s)], fill=RED)

    spaced_text(dr, (W * s / 2, 176 * s), "ANNO · CDLXXVI", f_capb, RED, 3 * s, True)
    lines = [
        "The boy emperor Romulus Augustulus is deposed",
        "by Odoacer, who declines the purple and calls",
        "himself King of Italy. The West ends without a",
        "battle: the child is pensioned off to Campania.",
    ]
    for i, ln in enumerate(lines):
        tw = dr.textlength(ln, font=f_small)
        dr.text((W * s / 2 - tw / 2, 200 * s + i * 13 * s), ln, font=f_small, fill=BLACK)
    dr.line([(24 * s, 262 * s), (W * s - 24 * s, 262 * s)], fill=BLACK, width=s)
    spaced_text(dr, (W * s / 2, 268 * s), "MDL · YEARS · AGO · TODAY", f_cap, BLACK, 2 * s, True)
    colophon(dr, s)
    return finalize(img)


# ------------------------------------------------------------ 5. Constructivist last quarter
def image5_constructivist():
    s = SS
    rng = random.Random(20260904)
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # black diagonal field on the right; the moon sits wholly inside it
    dr.polygon([(150 * s, 0), (W * s, 0), (W * s, H * s), (50 * s, H * s)], fill=BLACK)

    # the moon: a circle exactly half lit (waning -> left half white)
    cx, cy, r = 262 * s, 132 * s, 82 * s
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK, outline=WHITE, width=2 * s)
    dr.pieslice([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=WHITE)

    # red wedge from lower-left, tip at the circle's centre
    dr.polygon([(0, H * s), (0, 210 * s), (cx, cy)], fill=RED)
    # thin white counter-wedge from the top right, aimed at the same point
    dr.polygon([(W * s, 12 * s), (W * s, 22 * s), (cx + 24 * s, cy - 14 * s)], fill=WHITE)

    # small bars: constructivist debris in the white field
    for _ in range(6):
        x = rng.randint(60, 110) * s
        y = rng.randint(24, 60) * s
        w = rng.randint(8, 44) * s
        hgt = rng.randint(3, 7) * s
        dr.rectangle([x, y, x + w, y + hgt], fill=BLACK if rng.random() < 0.6 else RED)

    # type, rotated to climb with the wedge
    f_big = font(FONT_SANS_B, 26 * s)
    f_small = font(FONT_SANS_B, 8 * s)
    txt = Image.new("L", (260 * s, 50 * s), 0)
    td = ImageDraw.Draw(txt)
    td.text((0, 0), "LAST QUARTER", font=f_big, fill=255)
    td.text((2 * s, 34 * s), "ПОСЛЕДНЯЯ ЧЕТВЕРТЬ · 4 · IX · 2026", font=f_small, fill=255)
    ang = math.degrees(math.atan2((H - 210 + 20) * s, cx))  # wedge slope
    txt = txt.rotate(ang, resample=Image.BICUBIC, expand=True)
    mask = Image.new("L", img.size, 0)
    mask.paste(txt, (10 * s, 28 * s))
    # the type inverts whatever it crosses: black on white, white on black/red
    arr = np.array(img)
    m = np.array(mask) > 128
    white_under = (arr[..., 0] > 128) & (arr[..., 1] > 128) & (arr[..., 2] > 128)
    arr[m & white_under] = BLACK
    arr[m & ~white_under] = WHITE
    img = Image.fromarray(arr, "RGB")
    dr = ImageDraw.Draw(img)

    # red block top-left, a counterweight
    dr.rectangle([14 * s, 10 * s, 50 * s, 18 * s], fill=RED)
    colophon(dr, s, dark=True)
    return finalize(img)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
    save(image1_september(), 1)
    save(image2_asanoha(), 2)
    save(image3_sandpile(), 3)
    save(image4_roma(), 4)
    save(image5_constructivist(), 5)
    print("done")
