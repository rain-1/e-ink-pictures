#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-26.

Today is Esperanto Day (Unua Libro, 1887) and the anniversary of Syncom 2
(1963), the first geosynchronous satellite. Moon is a waxing gibbous, full
on the 29th, and August 12 is shaping up huge: Perseids + new moon + total
solar eclipse.

Five 400x300 images in exactly three colors (white, black, red).
Tonal scenes render at 3x, LANCZOS downscale, Floyd-Steinberg dither.
Hard-edged posters render at 3x and quantize with no dither (nearest color).
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
    return ImageFont.truetype(path, size)


def ctext(dr, xy, s, f, fill, anchor="mm"):
    dr.text(xy, s, font=f, fill=fill, anchor=anchor)


# ------------------------------------------------------------- 1. Esperanto Day
def star_points(cx, cy, r_out, k=5, rot=-math.pi / 2):
    """Classic 5-pointed star polygon."""
    r_in = r_out * math.sin(math.radians(18)) / math.sin(math.radians(54))
    pts = []
    for i in range(k * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / k
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def image1_esperanto():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # The verda stelo — rendered red, the only bright color this screen owns.
    cx, cy, r = 200 * s, 96 * s, 62 * s
    dr.polygon(star_points(cx, cy, r + 7 * s), fill=BLACK)
    dr.polygon(star_points(cx, cy, r), fill=RED)

    ctext(dr, (200 * s, 22 * s), "1887 · la 26-a de julio · 2026",
          font(FONT_MONO, 11 * s), BLACK)

    ctext(dr, (200 * s, 190 * s), "ESPERANTO",
          font(FONT_SANS_B, 40 * s), BLACK)

    ctext(dr, (200 * s, 226 * s), "«Saluton, mondo!»",
          font(FONT_SERIF, 19 * s), BLACK)

    dr.line([(60 * s, 250 * s), (340 * s, 250 * s)], fill=BLACK, width=s)
    ctext(dr, (200 * s, 268 * s),
          "Esperanto-Tago — Unua Libro, L. L. Zamenhof",
          font(FONT_SANS, 11 * s), BLACK)
    ctext(dr, (200 * s, 284 * s), "139 jaroj da espero",
          font(FONT_SANS, 11 * s), RED)
    return finalize(img, dither=False)


# ---------------------------------------------------------------- 2. Syncom 2
def rot2(x, y, a):
    return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)


def image2_syncom():
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)
    rng = random.Random(19630726)

    # star field
    for _ in range(90):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s)
        r = rng.choice([1, 1, 1, 2]) * s // 2 + 1
        dr.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

    # wireframe Earth
    ex, ey, er = 128 * s, 168 * s, 58 * s
    dr.ellipse([ex - er, ey - er, ex + er, ey + er], outline=WHITE, width=s)
    for lat in (-60, -30, 0, 30, 60):
        y = er * math.sin(math.radians(lat))
        a = er * math.cos(math.radians(lat))
        b = a * 0.30
        wdt = 2 * s if lat == 0 else s
        dr.ellipse([ex - a, ey - y - b, ex + a, ey - y + b],
                   outline=WHITE, width=wdt)
    for k in (0.35, 0.75):
        a = er * k
        dr.ellipse([ex - a, ey - er, ex + a, ey + er], outline=WHITE, width=s)
    dr.line([(ex, ey - er), (ex, ey + er)], fill=WHITE, width=s)

    # inclined geosynchronous orbit (dashed ellipse, rotated)
    tilt = math.radians(-18)
    A, B = 118 * s, 34 * s
    pts = []
    for i in range(241):
        t = 2 * math.pi * i / 240
        x, y = rot2(A * math.cos(t), B * math.sin(t), tilt)
        pts.append((ex + x, ey + y))
    for i in range(0, 240, 8):  # dashes
        dr.line([pts[i], pts[i + 4]], fill=WHITE, width=s)

    # the satellite, in red
    sx, sy = pts[210]
    dr.rectangle([sx - 4 * s, sy - 4 * s, sx + 4 * s, sy + 4 * s], fill=RED)
    dr.line([(sx - 10 * s, sy), (sx - 16 * s, sy)], fill=RED, width=s)
    dr.line([(sx + 10 * s, sy), (sx + 16 * s, sy)], fill=RED, width=s)
    ctext(dr, (sx + 4 * s, sy - 14 * s), "SYNCOM 2",
          font(FONT_MONO_B, 11 * s), RED, anchor="lm")

    # ground-track panel: the figure-eight (analemma over 55°W)
    px0, py0, px1, py1 = 268 * s, 108 * s, 388 * s, 228 * s
    dr.rectangle([px0, py0, px1, py1], fill=BLACK, outline=WHITE, width=s)
    pcx, pcy = (px0 + px1) / 2, (py0 + py1) / 2
    for fy in (-1 / 3, 0, 1 / 3):
        yy = pcy + fy * (py1 - py0)
        dr.line([(px0, yy), (px1, yy)], fill=(90, 90, 90), width=1)
    dr.line([(pcx, py0), (pcx, py1)], fill=(90, 90, 90), width=1)
    f8 = []
    for i in range(201):
        t = 2 * math.pi * i / 200
        lon = 22 * math.sin(2 * t)   # exaggerated for legibility
        lat = 52 * math.sin(t)
        f8.append((pcx + lon * s, pcy - lat * s))
    dr.line(f8, fill=RED, width=2 * s, joint="curve")
    ctext(dr, ((px0 + px1) / 2, py1 + 10 * s), "ground track · 55°W",
          font(FONT_MONO, 9 * s), WHITE)

    # titles
    ctext(dr, (16 * s, 22 * s), "SYNCOM 2", font(FONT_SANS_B, 26 * s),
          WHITE, anchor="lm")
    ctext(dr, (16 * s, 46 * s), "THE FIRST GEOSYNCHRONOUS SATELLITE",
          font(FONT_MONO, 11 * s), RED, anchor="lm")
    ctext(dr, (16 * s, 64 * s), "launched 26 July 1963 · Cape Canaveral",
          font(FONT_MONO, 10 * s), WHITE, anchor="lm")
    ctext(dr, (16 * s, 286 * s),
          "alt 35 786 km · period 23h 56m 04s · incl 33°",
          font(FONT_MONO, 10 * s), WHITE, anchor="lm")
    return finalize(img, dither=False)


# ------------------------------------------------------------------- 3. Kamon
def petal(cx, cy, angle, r0, r1, width):
    """Pointed-oval petal from radius r0 to r1 along `angle`."""
    ca, sa = math.cos(angle), math.sin(angle)
    pts = []
    n = 40
    for i in range(n + 1):
        t = i / n
        d = r0 + (r1 - r0) * t
        w = width * math.sin(math.pi * t) ** 0.85
        pts.append((cx + d * ca - w * sa, cy + d * sa + w * ca))
    for i in range(n + 1):
        t = 1 - i / n
        d = r0 + (r1 - r0) * t
        w = width * math.sin(math.pi * t) ** 0.85
        pts.append((cx + d * ca + w * sa, cy + d * sa - w * ca))
    return pts


def image3_kamon():
    s = SS
    rng = random.Random(20260726)
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    cx, cy = 200 * s, 150 * s

    R = 128 * s          # outer ring outer radius
    ring_w = 9 * s
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)
    dr.ellipse([cx - R + ring_w, cy - R + ring_w,
                cx + R - ring_w, cy + R - ring_w], fill=WHITE)

    k = rng.choice([6, 7, 8])                # fold symmetry for today: seeded
    rot = -math.pi / 2 + rng.uniform(0, math.pi / k)
    r_tip = R - ring_w - 8 * s
    r_base = 26 * s
    pw = (math.pi * (r_tip * 0.62) / k) * rng.uniform(0.62, 0.78)

    for j in range(k):
        a = rot + 2 * math.pi * j / k
        dr.polygon(petal(cx, cy, a, r_base, r_tip, pw), fill=BLACK)
        # white vein inside each petal
        dr.polygon(petal(cx, cy, a, r_base + 7 * s, r_tip - 9 * s,
                         pw * 0.45), fill=WHITE)
        # red seed inside the vein
        mid = r_base + (r_tip - r_base) * 0.42
        mx, my = cx + mid * math.cos(a), cy + mid * math.sin(a)
        rr = pw * 0.30
        dr.ellipse([mx - rr, my - rr, mx + rr, my + rr], fill=RED)
        # small circle between petals
        b = a + math.pi / k
        bd = r_tip * 0.80
        bx, by = cx + bd * math.cos(b), cy + bd * math.sin(b)
        br = 7 * s
        dr.ellipse([bx - br, by - br, bx + br, by + br], fill=BLACK)

    # center: black disc, white ring, red core
    for rr, col in ((r_base - 2 * s, BLACK), (r_base - 8 * s, WHITE),
                    (r_base - 12 * s, RED)):
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)

    ctext(dr, (388 * s, 268 * s), "家紋", font(FONT_JP, 20 * s),
          BLACK, anchor="rm")
    ctext(dr, (388 * s, 288 * s), "七月二十六日", font(FONT_JP, 11 * s),
          BLACK, anchor="rm")
    ctext(dr, (12 * s, 288 * s), f"mon {k}-fold · seed 20260726",
          font(FONT_MONO, 9 * s), BLACK, anchor="lm")
    return finalize(img, dither=False)


# ------------------------------------------------------------ 4. Moon almanac
def image4_moon():
    s = SS
    rng = random.Random(20260726)
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    mx, my, mr = 105 * s, 138 * s, 82 * s
    e = 0.80  # terminator: illuminated fraction (1+e)/2 = 90%, lit side right

    # maria blobs and craters on a light disc, then dither does the rest
    tex = Image.new("L", (2 * mr, 2 * mr), 228)
    td = ImageDraw.Draw(tex)
    for _ in range(9):  # maria
        bx, by = rng.uniform(0.15, 0.85) * 2 * mr, rng.uniform(0.1, 0.9) * 2 * mr
        br = rng.uniform(0.12, 0.30) * mr
        td.ellipse([bx - br, by - br * 0.8, bx + br, by + br * 0.8], fill=190)
    for _ in range(70):  # craters
        bx, by = rng.uniform(0, 2 * mr), rng.uniform(0, 2 * mr)
        br = rng.uniform(0.015, 0.06) * mr
        td.ellipse([bx - br, by - br, bx + br, by + br], fill=150)

    for yy in range(-mr, mr):
        half = math.sqrt(max(mr * mr - yy * yy, 0))
        xt = -e * half  # terminator x for this row
        for xx in range(int(-half), int(half)):
            if xx >= xt:
                g = tex.getpixel((xx + mr, yy + mr))
                # limb shading near the terminator
                fade = min(1.0, (xx - xt) / (0.35 * mr + 1))
                g = int(g * (0.55 + 0.45 * fade))
                img.putpixel((mx + xx, my + yy), (g, g, g))
            else:
                img.putpixel((mx + xx, my + yy), (25, 25, 25))
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=BLACK,
               width=2 * s)

    ctext(dr, (16 * s, 26 * s), "MOON ALMANAC", font(FONT_SANS_B, 21 * s),
          BLACK, anchor="lm")
    ctext(dr, (16 * s, 48 * s), "26 JUL 2026 · waxing gibbous · 90% lit",
          font(FONT_MONO, 11 * s), BLACK, anchor="lm")
    dr.line([(16 * s, 62 * s), (384 * s, 62 * s)], fill=BLACK, width=s)

    rows = [
        ("JUL 29", "Full Buck Moon", BLACK, 11),
        ("JUL 31", "double meteor shower", BLACK, 11),
        ("", "α-Capricornids · δ-Aquariids", BLACK, 10),
        ("AUG 12", "★ Perseids · new moon", RED, 11),
        ("", "best conditions since 2018", BLACK, 10),
        ("AUG 12", "★ total solar eclipse", RED, 11),
        ("", "Iceland → Spain", BLACK, 10),
    ]
    y = 92 * s
    for date, txt, col, sz in rows:
        if date:
            ctext(dr, (204 * s, y), date, font(FONT_MONO_B, 12 * s), RED,
                  anchor="lm")
        ctext(dr, (258 * s, y), txt, font(FONT_SANS, sz * s), col,
              anchor="lm")
        y += 24 * s
    dr.line([(204 * s, 262 * s), (384 * s, 262 * s)], fill=BLACK, width=s)
    ctext(dr, (204 * s, 280 * s), "mark the 12th of August.",
          font(FONT_SERIF, 12 * s), BLACK, anchor="lm")
    return finalize(img, dither=True)


# --------------------------------------------------------------- 5. Red wedge
def image5_wedge():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    rng = random.Random(1919)

    # split field: white above the diagonal, black below
    dr.polygon([(0, H * s), (W * s, 0), (W * s, H * s)], fill=BLACK)

    # the circle, sitting on the black field, white
    ccx, ccy, cr = 268 * s, 128 * s, 92 * s
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=WHITE)

    # halftone dots inside lower part of the circle
    for gy in range(0, 2 * cr, 10 * s):
        for gx in range(0, 2 * cr, 10 * s):
            px, py = ccx - cr + gx, ccy - cr + gy
            d = math.hypot(px - ccx, py - ccy)
            if d < cr - 4 * s and py > ccy + 12 * s:
                rr = 2 * s
                dr.ellipse([px - rr, py - rr, px + rr, py + rr], fill=BLACK)

    # the red wedge, piercing from the lower left into the circle's heart
    tip = (ccx + 2 * s, ccy - 2 * s)
    base_a = (-8 * s, 236 * s)
    base_b = (44 * s, 292 * s)
    dr.polygon([base_a, tip, base_b], fill=RED)

    # supporting cast: black bars on the white field, white bars on black
    for (x0, y0, ln, ang, wd, col) in [
        (150, 95, 70, -48, 5, BLACK),
        (108, 145, 50, -48, 3, BLACK),
        (58, 85, 40, -48, 3, BLACK),
        (330, 250, 70, -48, 4, WHITE),
        (250, 262, 40, -48, 3, WHITE),
    ]:
        a = math.radians(ang)
        x1 = x0 + ln * math.cos(a)
        y1 = y0 + ln * math.sin(a)
        dr.line([(x0 * s, y0 * s), (x1 * s, y1 * s)], fill=col, width=wd * s)

    # small red satellites of the wedge
    for (x, y, r) in [(52, 150, 9), (170, 140, 5)]:
        dr.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s],
                   fill=RED)

    ctext(dr, (12 * s, 20 * s), "LA RUĜA KOJNO", font(FONT_SANS_B, 15 * s),
          BLACK, anchor="lm")
    ctext(dr, (388 * s, 286 * s), "post El Lissitzky, 1919",
          font(FONT_MONO, 9 * s), WHITE, anchor="rm")
    return finalize(img, dither=False)


# -------------------------------------------------------------------- main
def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(here))
    makers = [image1_esperanto, image2_syncom, image3_kamon,
              image4_moon, image5_wedge]
    for i, make in enumerate(makers, 1):
        im = make()
        for path in (os.path.join(root, "images", f"{i}.png"),
                     os.path.join(here, f"{i}.png")):
            im.save(path, optimize=True)
        print(f"wrote {i}.png")


if __name__ == "__main__":
    main()
