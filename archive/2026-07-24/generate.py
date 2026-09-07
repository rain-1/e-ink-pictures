#!/usr/bin/env python3
"""
2026-07-24 — five pictures for a 400x300 black/white/red e-ink screen.

Today: the waxing gibbous Moon passes 0.6 deg south of Antares ("rival of Mars"),
Apollo 11 splashed down on this day in 1969, and Hiram Bingham reached
Machu Picchu on this day in 1911. Plus two from the backlog: the Lissitzky
red-wedge homage and a date-seeded kamon crest generator.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
S = 3                     # supersample factor for antialiased pieces
BW, BH = W * S, H * S
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

PALETTE = [0, 0, 0, 255, 255, 255, 255, 0, 0]

DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def pal_image():
    p = Image.new("P", (1, 1))
    p.putpalette(PALETTE + [0, 0, 0] * 253)
    return p


def quantize_dither(img):
    """LANCZOS downscale then Floyd-Steinberg into the 3-color palette."""
    img = img.resize((W, H), Image.LANCZOS)
    return img.quantize(palette=pal_image(), dither=Image.FLOYDSTEINBERG)


def quantize_hard(img):
    """Downscale then snap each pixel to the nearest palette color (no dither)."""
    img = img.resize((W, H), Image.LANCZOS)
    return img.quantize(palette=pal_image(), dither=Image.NONE)


def font(path, size):
    return ImageFont.truetype(path, size)


def ctext(d, cx, y, txt, f, fill, anchor="mm"):
    d.text((cx, y), txt, font=f, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- 1. antares

def antares():
    """Tonight the 75% waxing gibbous Moon sits 0.6 deg south of Antares,
    the red heart of Scorpius. Antares = 'anti-Ares', the rival of Mars."""
    img = Image.new("RGB", (BW, BH), BLACK)
    d = ImageDraw.Draw(img)
    rng = random.Random(20260724)

    # faint background starfield
    for _ in range(420):
        x, y = rng.uniform(0, BW), rng.uniform(0, BH * 0.88)
        r = rng.choice([1, 1, 1, 2, 2, 3])
        g = rng.randint(70, 150)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(g, g, g))

    # Scorpius principal stars: (RA hours, Dec deg, mag, name)
    stars = {
        "beta":    (16.09, -19.8, 2.6, "Acrab"),
        "delta":   (16.01, -22.6, 2.3, "Dschubba"),
        "pi":      (15.98, -26.1, 2.9, ""),
        "sigma":   (16.35, -25.6, 2.9, ""),
        "antares": (16.49, -26.43, 1.0, "ANTARES"),
        "tau":     (16.60, -28.2, 2.8, ""),
        "epsilon": (16.84, -34.3, 2.3, ""),
        "mu":      (16.87, -38.0, 3.0, ""),
        "zeta":    (16.91, -42.4, 3.6, ""),
        "eta":     (17.20, -43.2, 3.3, ""),
        "theta":   (17.62, -43.0, 1.9, "Sargas"),
        "iota":    (17.79, -40.1, 3.0, ""),
        "kappa":   (17.71, -39.0, 2.4, ""),
        "lambda":  (17.56, -37.1, 1.6, "Shaula"),
        "upsilon": (17.51, -37.3, 2.7, ""),
    }
    chain = ["beta", "delta", "pi"]
    body = ["delta", "sigma", "antares", "tau", "epsilon", "mu", "zeta",
            "eta", "theta", "iota", "kappa", "lambda", "upsilon"]

    ra0, dec0 = 16.85, -31.5
    sy = 8.0 * S                      # px per degree
    sx = 15.0 * sy                    # px per RA-hour (15 deg/hour), equal scale

    def pos(key):
        ra, dec, _, _ = stars[key]
        x = BW * 0.44 - (ra - ra0) * sx * math.cos(math.radians(dec))
        y = BH * 0.50 + (dec0 - dec) * sy
        return x, y

    # constellation lines
    for seq in (chain, body):
        pts = [pos(k) for k in seq]
        d.line(pts, fill=(120, 120, 120), width=2 * S)

    # stars on top of lines
    for key, (ra, dec, mag, name) in stars.items():
        x, y = pos(key)
        r = (5.2 - mag) * 1.55 * S
        if key == "antares":
            r = 8.5 * S
            for gr in range(int(r * 2.2), int(r), -S):
                a = int(60 * (1 - (gr - r) / (r * 1.2)))
                d.ellipse([x - gr, y - gr, x + gr, y + gr],
                          outline=(a, 0, 0))
            d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
            # star spikes
            for ang in range(0, 360, 90):
                dx = math.cos(math.radians(ang + 45)) * r * 2.1
                dy = math.sin(math.radians(ang + 45)) * r * 2.1
                d.line([x, y, x + dx, y + dy], fill=RED, width=S)
        else:
            d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

    # the Moon, 0.6 deg south of Antares (drawn oversized for legibility)
    ax, ay = pos("antares")
    mx, my = ax + 34 * S, ay + 38 * S
    mr = 21 * S
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=WHITE)
    # a few craters on the lit part
    for cx_, cy_, cr_ in [(-0.35, -0.3, 0.16), (0.1, 0.25, 0.12),
                          (-0.1, 0.55, 0.09), (-0.45, 0.15, 0.08)]:
        d.ellipse([mx + cx_ * mr - cr_ * mr, my + cy_ * mr - cr_ * mr,
                   mx + cx_ * mr + cr_ * mr, my + cy_ * mr + cr_ * mr],
                  fill=(185, 185, 185))
    # waxing gibbous: dark sliver on the eastern limb (disc AND offset ellipse)
    disc = Image.new("L", (BW, BH), 0)
    ImageDraw.Draw(disc).ellipse([mx - mr, my - mr, mx + mr, my + mr],
                                 fill=255)
    sliver = Image.new("L", (BW, BH), 0)
    ImageDraw.Draw(sliver).ellipse(
        [mx - mr * 2.35, my - mr * 1.45, mx - mr * 0.42, my + mr * 1.45],
        fill=255)
    from PIL import ImageChops
    dark = ImageChops.multiply(disc, sliver)
    img.paste((12, 12, 12), (0, 0), dark)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=(160, 160, 160),
              width=S)

    # labels
    lf = font(DEJAVU_B, 13 * S)
    sf = font(DEJAVU, 11 * S)
    d.text((ax + 16 * S, ay - 34 * S), "ANTARES", font=lf, fill=RED)
    d.text((mx + mr + 6 * S, my - 6 * S), "MOON 75%", font=sf,
           fill=(200, 200, 200))
    d.text((pos("lambda")[0] - 8 * S, pos("lambda")[1] + 10 * S), "Shaula",
           font=sf, fill=(170, 170, 170))
    d.text((pos("delta")[0] - 30 * S, pos("delta")[1] - 22 * S), "Dschubba",
           font=sf, fill=(170, 170, 170))

    # title block
    tf = font(SERIF_B, 22 * S)
    d.text((14 * S, 10 * S), "Tonight the Moon grazes", font=tf, fill=WHITE)
    d.text((14 * S, 34 * S), "the rival of Mars", font=tf, fill=RED)
    bf = font(MONO, 11 * S)
    d.rectangle([0, BH - 26 * S, BW, BH], fill=(15, 15, 15))
    d.text((BW / 2, BH - 13 * S),
           "SCORPIUS · MOON 0.6° S OF ANTARES · 24 JUL 2026",
           font=bf, fill=(210, 210, 210), anchor="mm")
    return quantize_dither(img)


# -------------------------------------------------------------- 2. splashdown

def splashdown():
    """Apollo 11 came home on this day in 1969: three red/white ringsail
    parachutes over a seigaiha sea."""
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    horizon = int(BH * 0.62)

    # pale sky gradient
    for y in range(horizon):
        g = 255 - int(18 * (y / horizon))
        d.line([0, y, BW, y], fill=(g, g, g))

    def parachute(cx, cy, r, tilt=0.0):
        # canopy: half-disc of alternating red/white gores
        n = 8
        for i in range(n):
            a0 = 180 + i * (180 / n) + tilt
            a1 = 180 + (i + 1) * (180 / n) + tilt
            col = RED if i % 2 == 0 else WHITE
            d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a1,
                       fill=col, outline=BLACK, width=S)
        d.arc([cx - r, cy - r, cx + r, cy + r], 180 + tilt, 360 + tilt,
              fill=BLACK, width=2 * S)
        d.line([cx - r, cy, cx + r, cy], fill=BLACK, width=2 * S)
        return cx, cy

    # capsule position
    capx, capy = BW * 0.5, BH * 0.40
    chutes = [(BW * 0.30, BH * 0.17, 34 * S),
              (BW * 0.52, BH * 0.13, 38 * S),
              (BW * 0.72, BH * 0.18, 34 * S)]
    # shroud lines first
    for cx, cy, r in chutes:
        for fx in (-0.92, -0.45, 0.0, 0.45, 0.92):
            d.line([cx + fx * r, cy + 1 * S, capx, capy], fill=BLACK, width=S)
    for cx, cy, r in chutes:
        parachute(cx, cy, r)

    # command module: truncated cone with blunt heat shield
    cw, ch = 17 * S, 15 * S
    d.polygon([(capx - cw * 0.35, capy - ch), (capx + cw * 0.35, capy - ch),
               (capx + cw, capy + ch * 0.7), (capx - cw, capy + ch * 0.7)],
              fill=(40, 40, 40), outline=BLACK)
    d.chord([capx - cw, capy + ch * 0.15, capx + cw, capy + ch * 1.25],
            0, 180, fill=BLACK)
    d.ellipse([capx - 4 * S, capy - 4 * S, capx + 4 * S, capy + 4 * S],
              fill=WHITE, outline=BLACK, width=S)

    # seigaiha sea: rows of overlapping scallop fans
    rad = 26 * S
    row_h = int(rad * 0.42)
    rowi = 0
    y = horizon
    d.rectangle([0, horizon, BW, BH], fill=WHITE)
    while y < BH + rad:
        off = 0 if rowi % 2 == 0 else rad
        x = -rad + off - rad
        while x < BW + rad:
            red_wave = (rowi * 7 + int(x / (2 * rad))) % 9 == 3
            base = RED if red_wave else BLACK
            for k in range(4):
                rr = rad - k * (rad // 4)
                fill = WHITE if k % 2 == 1 else base
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=fill,
                          outline=base, width=S)
            x += 2 * rad
        y += row_h
        rowi += 1
    # crop sea to below horizon by repainting sky band
    # (fans poke above horizon: that's the chop of the Pacific — keep a clean line)
    d.line([0, horizon, BW, horizon], fill=BLACK, width=S)

    # caption band
    bandh = 34 * S
    d.rectangle([0, BH - bandh, BW, BH], fill=BLACK)
    f1 = font(DEJAVU_B, 15 * S)
    f2 = font(MONO, 10 * S)
    d.text((BW / 2, BH - bandh + 10 * S), "SPLASHDOWN — APOLLO 11 CAME HOME",
           font=f1, fill=WHITE, anchor="mm")
    d.text((BW / 2, BH - 9 * S),
           "24 JULY 1969 · PACIFIC OCEAN · 13 NM FROM USS HORNET",
           font=f2, fill=RED, anchor="mm")
    return quantize_dither(img)


# ------------------------------------------------------------ 3. machu picchu

def machu():
    """115 years since Hiram Bingham, led by a local boy, first saw the
    terraces of Machu Picchu through the mist."""
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)
    rng = random.Random(19110724)

    # big red sun, high right
    sunx, suny, sunr = BW * 0.78, BH * 0.20, 36 * S
    d.ellipse([sunx - sunr, suny - sunr, sunx + sunr, suny + sunr], fill=RED)

    # far ridge (light gray -> dithers to a sparse tone)
    far = [(0, BH * 0.60)]
    x, yy = 0, BH * 0.60
    while x < BW:
        x += rng.uniform(28, 60) * S
        yy = BH * (0.46 + rng.uniform(-0.05, 0.07))
        far.append((x, yy))
    far += [(BW, BH * 0.55), (BW, BH * 0.80), (0, BH * 0.80)]
    d.polygon(far, fill=(190, 190, 190))

    # Huayna Picchu: the steep sugarloaf that towers behind the ruins
    hp = [(BW * 0.02, BH * 0.80),
          (BW * 0.10, BH * 0.52), (BW * 0.155, BH * 0.34),
          (BW * 0.21, BH * 0.155), (BW * 0.255, BH * 0.075),
          (BW * 0.295, BH * 0.10), (BW * 0.345, BH * 0.20),
          (BW * 0.41, BH * 0.30), (BW * 0.47, BH * 0.44),
          (BW * 0.545, BH * 0.60), (BW * 0.62, BH * 0.80)]
    d.polygon(hp + [(BW * 0.02, BH * 0.80)], fill=(55, 55, 55))
    d.line(hp, fill=BLACK, width=2 * S)
    # rocky texture strokes down the face
    for _ in range(60):
        t = rng.uniform(0.1, 0.95)
        px = BW * (0.06 + t * 0.52)
        top = BH * 0.80 - (BH * 0.80 - BH * 0.09) * max(
            0.0, 1 - abs((px / BW - 0.265) / 0.30) ** 1.4)
        py = rng.uniform(top + 6 * S, BH * 0.78)
        ln = rng.uniform(4, 14) * S
        d.line([px, py, px + rng.uniform(-3, 3) * S, py + ln],
               fill=(20, 20, 20), width=S)

    # two thin mist ribbons across the peak's waist
    for my_, mh_ in [(0.40, 8), (0.52, 6)]:
        y0 = BH * my_
        d.ellipse([-BW * 0.05, y0 - mh_ * S, BW * 0.58, y0 + mh_ * S],
                  fill=WHITE)

    # foreground: fine agricultural terraces climbing out of the frame
    ty = int(BH * 0.80)
    step = int(9 * S)
    while ty < BH - 26 * S:
        d.rectangle([0, ty, BW, ty + step], fill=WHITE)
        d.line([0, ty, BW, ty], fill=BLACK, width=2 * S)
        xx = rng.uniform(0, 10) * S
        while xx < BW:
            d.line([xx, ty + 2 * S, xx, ty + step - S], fill=(90, 90, 90),
                   width=S)
            xx += rng.uniform(7, 16) * S
        ty += step
    d.line([0, ty, BW, ty], fill=BLACK, width=2 * S)

    # title in the sky
    f1 = font(SERIF_B, 27 * S)
    f2 = font(SERIF, 12 * S)
    d.text((BW - 12 * S, BH * 0.40), "MACHU", font=f1, fill=BLACK, anchor="rs")
    d.text((BW - 12 * S, BH * 0.52), "PICCHU", font=f1, fill=BLACK, anchor="rs")
    d.text((BW - 12 * S, BH * 0.585), "found in the clouds", font=f2,
           fill=BLACK, anchor="rs")
    fb = font(MONO, 10 * S)
    d.rectangle([0, BH - 26 * S, BW, BH], fill=BLACK)
    d.text((BW / 2, BH - 13 * S),
           "HIRAM BINGHAM REACHES THE LOST CITY · 24 JULY 1911",
           font=fb, fill=WHITE, anchor="mm")
    return quantize_dither(img)


# ---------------------------------------------------------------- 4. lissitzky

def wedge():
    """El Lissitzky, 1919, adapted for a screen that owns exactly these three
    colors: beat the grays with the red wedge."""
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    # diagonal field split: lower-right black
    d.polygon([(BW, 0), (BW, BH), (0, BH)], fill=BLACK)

    # white circle sitting mostly in the black half
    ccx, ccy, cr = BW * 0.60, BH * 0.48, BH * 0.34
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=WHITE,
              outline=BLACK, width=2 * S)

    # the red wedge, piercing from upper-left into the circle's heart
    tipx, tipy = ccx + cr * 0.18, ccy + cr * 0.10
    d.polygon([(0, BH * 0.06), (0, BH * 0.34), (tipx, tipy)], fill=RED)

    # supporting cast: small bars and discs
    d.rectangle([BW * 0.70, BH * 0.76, BW * 0.78, BH * 0.92], fill=RED)
    d.rectangle([BW * 0.81, BH * 0.80, BW * 0.85, BH * 0.92], fill=WHITE)
    d.rectangle([BW * 0.88, BH * 0.72, BW * 0.91, BH * 0.92], fill=WHITE)
    d.ellipse([BW * 0.16 - 8 * S, BH * 0.70 - 8 * S,
               BW * 0.16 + 8 * S, BH * 0.70 + 8 * S], fill=BLACK)
    d.ellipse([BW * 0.24 - 5 * S, BH * 0.78 - 5 * S,
               BW * 0.24 + 5 * S, BH * 0.78 + 5 * S], fill=RED)
    d.rectangle([BW * 0.05, BH * 0.86, BW * 0.30, BH * 0.885], fill=BLACK)
    # thin rays from the wedge
    d.line([BW * 0.10, BH * 0.04, BW * 0.56, BH * 0.16], fill=BLACK,
           width=S)

    # typography, stacked constructivist-style
    f_big = font(DEJAVU_B, 24 * S)
    f_sm = font(DEJAVU_B, 13 * S)
    d.text((BW * 0.035, BH * 0.40), "BEAT THE GRAYS", font=f_big, fill=BLACK)
    d.text((BW * 0.035, BH * 0.50), "WITH THE RED WEDGE", font=f_sm, fill=RED)
    f_tiny = font(MONO, 9 * S)
    d.text((BW - 8 * S, BH - 14 * S),
           "after El Lissitzky, 1919 — this screen has no grays to beat",
           font=f_tiny, fill=WHITE, anchor="rm")
    return quantize_hard(img)


# -------------------------------------------------------------------- 5. kamon

def kamon():
    """A family crest for the day, generated from the date. Kamon are bold,
    circular, and radially symmetric — born for 400x300 in three colors."""
    seed = 20260724
    rng = random.Random(seed)
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    cx, cy = BW * 0.40, BH * 0.50
    R = BH * 0.40

    # enclosure: double ring
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)
    r2 = R * 0.90
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=WHITE)
    r3 = R * 0.86
    d.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], fill=BLACK)

    n = rng.choice([5, 6, 8])          # fold symmetry
    motif = rng.choice(["petal", "blade", "diamond"])
    base_rot = rng.uniform(0, 360 / n)

    def rot(px, py, ang, ox, oy):
        a = math.radians(ang)
        qx = ox + (px - ox) * math.cos(a) - (py - oy) * math.sin(a)
        qy = oy + (px - ox) * math.sin(a) + (py - oy) * math.cos(a)
        return qx, qy

    def draw_motif(ang, fill):
        if motif == "petal":
            # pointed petal: two arcs approximated by a polygon
            pts = []
            L, Wd = r3 * 0.78, r3 * 0.34
            for t in [i / 24 for i in range(25)]:
                pts.append((cx + L * t, cy - Wd * math.sin(math.pi * t) * 0.5))
            for t in [i / 24 for i in range(24, -1, -1)]:
                pts.append((cx + L * t, cy + Wd * math.sin(math.pi * t) * 0.5))
        elif motif == "blade":
            L, Wd = r3 * 0.80, r3 * 0.26
            pts = [(cx + r3 * 0.10, cy),
                   (cx + L * 0.55, cy - Wd * 0.5),
                   (cx + L, cy - Wd * 0.12),
                   (cx + L * 0.9, cy + Wd * 0.28),
                   (cx + L * 0.4, cy + Wd * 0.42)]
        else:  # diamond
            L, Wd = r3 * 0.80, r3 * 0.30
            pts = [(cx + r3 * 0.12, cy), (cx + L * 0.56, cy - Wd * 0.5),
                   (cx + L, cy), (cx + L * 0.56, cy + Wd * 0.5)]
        pts = [rot(px, py, ang, cx, cy) for px, py in pts]
        d.polygon(pts, fill=fill)

    for i in range(n):
        draw_motif(base_rot + i * 360 / n, WHITE)
    # inner core: red dot ringed with white
    rc = r3 * 0.16
    d.ellipse([cx - rc * 1.6, cy - rc * 1.6, cx + rc * 1.6, cy + rc * 1.6],
              fill=WHITE)
    d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=RED)

    # side column: vertical Japanese caption, like a hanging label
    colx = BW * 0.845
    d.rectangle([colx - 22 * S, BH * 0.08, colx + 22 * S, BH * 0.92],
                outline=BLACK, width=2 * S)
    jf = font(JP, 26 * S)
    label = "文月紋"      # "crest of Fumizuki", the old name for July
    for i, ch in enumerate(label):
        d.text((colx, BH * 0.17 + i * 34 * S), ch, font=jf, fill=BLACK,
               anchor="mm")
    d.ellipse([colx - 8 * S, BH * 0.80 - 8 * S, colx + 8 * S, BH * 0.80 + 8 * S],
              fill=RED)
    f_tiny = font(MONO, 9 * S)
    d.text((BW * 0.40, BH - 12 * S),
           f"a crest for 24 july · {n}-fold {motif} · seed {seed}",
           font=f_tiny, fill=BLACK, anchor="mm")
    return quantize_hard(img)


# ----------------------------------------------------------------------- main

def main():
    import os
    outdirs = ["images", "archive/2026-07-24"]
    for o in outdirs:
        os.makedirs(o, exist_ok=True)
    pieces = [antares, splashdown, machu, wedge, kamon]
    for i, fn in enumerate(pieces, 1):
        im = fn()
        assert im.size == (W, H)
        for o in outdirs:
            im.save(f"{o}/{i}.png", optimize=True)
        print(f"{i}.png <- {fn.__name__}")


if __name__ == "__main__":
    main()
