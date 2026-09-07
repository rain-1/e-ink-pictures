#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-08-25 (Voyager Day).

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

Today: Aug 25 is a double space anniversary — Voyager 2 skimmed Neptune's
clouds in 1989 and Voyager 1 crossed into interstellar space in 2012, exactly
23 years apart on the same calendar date. Also: a 96% "blood moon" partial
lunar eclipse arrives in three nights (Aug 27-28), Matthew Webb finished the
first swim of the English Channel on this day in 1875, and Momofuku Ando
invented instant ramen on this day in 1958.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3  # supersample factor
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED)
    palette += [0, 0, 0] * (256 - 3)
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=True):
    """Downscale (if supersampled) and quantize to the exact 3-color palette."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def save(img, n):
    for path in (os.path.join(ROOT, "images", f"{n}.png"),
                 os.path.join(HERE, f"{n}.png")):
        img.save(path, optimize=True)
    print(f"saved {n}.png")


# ------------------------------------------------------- 1. Neptune, 1989
def image1_neptune():
    """Voyager 2's Neptune flyby: banded planet, dark spot, tiny spacecraft."""
    rng = random.Random(19890825)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # star field
    for _ in range(180):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s)
        r = rng.uniform(0.4, 1.4) * s
        v = rng.randint(120, 255)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # planet disc, chord by chord, with sinusoidal latitude banding
    cx, cy, R = 268 * s, 148 * s, 118 * s
    for dy in range(-R, R + 1):
        half = math.sqrt(R * R - dy * dy)
        lat = dy / R  # -1..1
        base = 168 - 38 * abs(lat)  # limb-ish darkening toward poles
        band = (18 * math.sin(lat * 9.0) + 10 * math.sin(lat * 17.0 + 1.3)
                + 6 * math.sin(lat * 29.0 + 4.0))
        v = max(30, min(225, int(base + band)))
        dr.line([cx - half, cy + dy, cx + half, cy + dy], fill=(v, v, v), width=1)

    # terminator: soft shadow creeping in from the right limb
    shade = Image.new("L", img.size, 0)
    sd = ImageDraw.Draw(shade)
    sd.ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
    mask = shade.copy()
    grad = Image.new("L", img.size, 0)
    gd = ImageDraw.Draw(grad)
    for i in range(40):
        off = int(R * (0.55 + 0.02 * i))
        gd.ellipse([cx - R + off, cy - R, cx + R + off, cy + R], fill=min(255, 10 + i * 7))
    img.paste(Image.new("RGB", img.size, BLACK), (0, 0),
              Image.composite(grad, Image.new("L", img.size, 0), mask))

    # Great Dark Spot — in red, the panel's one loud color
    sx, sy = cx - 0.34 * R, cy + 0.10 * R
    dr.ellipse([sx - 34 * s, sy - 19 * s, sx + 34 * s, sy + 19 * s], fill=(210, 0, 0))
    dr.ellipse([sx - 22 * s, sy - 11 * s, sx + 22 * s, sy + 11 * s], fill=(150, 0, 0))
    # "Scooter" companion cloud
    dr.ellipse([sx - 6 * s, sy + 34 * s, sx + 26 * s, sy + 44 * s], fill=(235, 235, 235))

    # trajectory: dotted red arc sweeping over the pole
    pts = []
    for t in range(0, 101):
        u = t / 100
        x = (20 + 400 * u) * s
        y = (250 - 240 * u + 190 * u * u) * s
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        if i % 4 < 2:
            dr.ellipse([x - 1.6 * s, y - 1.6 * s, x + 1.6 * s, y + 1.6 * s],
                       fill=(255, 60, 60))

    # Voyager silhouette (dish + bus + booms), lower left, in white
    vx, vy = 88 * s, 208 * s

    def L(a, b, w=2):
        dr.line([vx + a[0] * s, vy + a[1] * s, vx + b[0] * s, vy + b[1] * s],
                fill=WHITE, width=int(w * s))

    dr.ellipse([vx - 22 * s, vy - 16 * s, vx + 10 * s, vy + 8 * s], outline=WHITE,
               width=int(1.4 * s))  # dish rim
    dr.ellipse([vx - 15 * s, vy - 11 * s, vx + 3 * s, vy + 3 * s], fill=WHITE)  # dish
    L((-6, -4), (2, 10), 2)                      # feed strut
    dr.rectangle([vx + 2 * s, vy + 8 * s, vx + 16 * s, vy + 18 * s], fill=WHITE)  # bus
    L((16, 12), (46, 2), 1.6)                    # magnetometer boom
    L((8, 18), (-4, 40), 1.6)                    # RTG boom
    dr.rectangle([vx - 10 * s, vy + 38 * s, vx - 1 * s, vy + 46 * s], fill=WHITE)

    img = finalize(img)
    dr = ImageDraw.Draw(img)
    dr.text((16, 12), "NEPTUNE", font=font(FONT_SERIF_B, 34), fill=0)
    dr.text((15, 11), "NEPTUNE", font=font(FONT_SERIF_B, 34), fill=2)
    dr.text((17, 52), "25 AUG 1989 · VOYAGER 2", font=font(FONT_MONO, 12), fill=0)
    dr.text((17, 268), "4,800 km above the clouds — still our only visit.",
            font=font(FONT_SANS, 12), fill=0)
    return img


# --------------------------------------------- 2. The red wedge, 2012
def image2_interstellar():
    """Constructivist: Voyager 1 as a red wedge piercing the heliosphere."""
    img = Image.new("RGB", (W * SS, H * SS), WHITE)
    dr = ImageDraw.Draw(img)
    s = SS

    # the heliosphere: a great black circle, low left
    cx, cy, R = 148 * s, 178 * s, 118 * s
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)

    # planetary orbits inside, thin white rings around a white sun
    for rr in (14, 26, 38, 50, 66, 84, 100):
        dr.ellipse([cx - rr * s, cy - rr * s, cx + rr * s, cy + rr * s],
                   outline=WHITE, width=max(1, int(0.8 * s)))
    dr.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], fill=WHITE)

    # sparse black stars outside
    rng = random.Random(20120825)
    for _ in range(90):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s)
        if (x - cx) ** 2 + (y - cy) ** 2 > (R + 8 * s) ** 2:
            r = rng.uniform(0.7, 1.8) * s
            dr.ellipse([x - r, y - r, x + r, y + r], fill=BLACK)

    # the red wedge: from the sun, out through the boundary, into the white
    ang = math.radians(-28)
    tipx = cx + 258 * s * math.cos(ang)
    tipy = cy + 258 * s * math.sin(ang)
    perp = (math.cos(ang + math.pi / 2), math.sin(ang + math.pi / 2))
    base_w = 26 * s
    p1 = (cx + perp[0] * base_w, cy + perp[1] * base_w)
    p2 = (cx - perp[0] * base_w, cy - perp[1] * base_w)
    dr.polygon([p1, p2, (tipx, tipy)], fill=RED)

    # tiny spacecraft at the wedge tip, already in interstellar space
    vx = tipx + 16 * s * math.cos(ang)
    vy = tipy + 16 * s * math.sin(ang)
    dr.ellipse([vx - 7 * s, vy - 7 * s, vx + 7 * s, vy + 7 * s],
               outline=BLACK, width=int(1.2 * s))
    dr.ellipse([vx - 2.6 * s, vy - 2.6 * s, vx + 2.6 * s, vy + 2.6 * s], fill=BLACK)
    dr.line([vx + 6 * s * math.cos(ang), vy + 6 * s * math.sin(ang),
             vx + 20 * s * math.cos(ang), vy + 20 * s * math.sin(ang)],
            fill=BLACK, width=int(1.2 * s))

    img = finalize(img, dither=False)

    dr = ImageDraw.Draw(img)
    dr.text((16, 8), "INTERSTELLAR", font=font(FONT_SANS_B, 29), fill=1)
    dr.text((16, 44), "VOYAGER 1 LEAVES THE HELIOSPHERE", font=font(FONT_MONO, 11), fill=1)
    dr.text((16, 60), "25 · VIII · 2012 — 122 AU FROM THE SUN", font=font(FONT_MONO, 11), fill=2)
    dr.text((290, 232), "one object,", font=font(FONT_SANS, 11), fill=1)
    dr.text((290, 246), "made by hands,", font=font(FONT_SANS, 11), fill=1)
    dr.text((290, 260), "outside the", font=font(FONT_SANS, 11), fill=1)
    dr.text((290, 274), "bubble.", font=font(FONT_SANS, 11), fill=1)
    return img


# ------------------------------------------------ 3. Blood moon almanac
def image3_eclipse():
    """Almanac card: the deep partial lunar eclipse three nights from now."""
    rng = random.Random(20260828)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # header band
    dr.rectangle([0, 0, W * s, 34 * s], fill=BLACK)

    # the moon, 96% swallowed by the umbra
    cx, cy, R = 133 * s, 168 * s, 88 * s
    # red eclipsed disc with darker mottling
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(196, 20, 10))
    for _ in range(260):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(2, 9) * s
        d = (R - r) * math.sqrt(rng.random()) * 0.98
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        shade = rng.choice([(150, 10, 5), (120, 8, 4), (220, 40, 20)])
        dr.ellipse([x - r, y - r, x + r, y + r], fill=shade)
    # craters
    for _ in range(26):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(3, 10) * s
        d = (R - r) * math.sqrt(rng.random()) * 0.95
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        dr.ellipse([x - r, y - r, x + r, y + r], outline=(120, 8, 4),
                   width=max(1, int(0.8 * s)))

    # the bright sliver that stays outside the umbra (bottom-left lune):
    # umbra circle centered up-right of the moon, big enough to cover all
    # but ~15% of the moon's radius on the far limb
    ua = math.radians(-50)
    ur = R * 2.6
    d = ur - 0.85 * R
    ux = cx + d * math.cos(ua)
    uy = cy + d * math.sin(ua)
    sliver = Image.new("L", img.size, 0)
    sd = ImageDraw.Draw(sliver)
    sd.ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
    sd.ellipse([ux - ur, uy - ur, ux + ur, uy + ur], fill=0)
    img.paste(Image.new("RGB", img.size, (250, 250, 245)), (0, 0), sliver)

    img = finalize(img)
    dr = ImageDraw.Draw(img)
    dr.text((14, 7), "ALMANAC", font=font(FONT_SERIF_B, 17), fill=0)
    dr.text((300, 10), "25 AUG 2026", font=font(FONT_MONO, 11), fill=0)

    x = 242
    dr.text((x, 52), "IN THREE NIGHTS", font=font(FONT_SANS_B, 14), fill=2)
    dr.text((x, 76), "Partial lunar eclipse", font=font(FONT_SANS_B, 13), fill=1)
    dr.text((x, 94), "night of 27–28 Aug", font=font(FONT_SANS, 12), fill=1)
    for i, line in enumerate([
            "96% of the Moon slides",
            "into Earth's umbra —",
            "all but a bright sliver",
            "turns eclipse-red.",
            "",
            "Greatest: 04:13 UT"]):
        dr.text((x, 122 + i * 15), line, font=font(FONT_SANS, 11), fill=1)
    dr.line([x, 218, 388, 218], fill=1, width=1)
    dr.text((x, 226), "then:", font=font(FONT_SANS_B, 10), fill=1)
    for i, line in enumerate(["Sep 11  new moon",
                              "Sep 23  equinox",
                              "Sep 25  Neptune at",
                              "        opposition"]):
        dr.text((x, 240 + i * 13), line, font=font(FONT_MONO, 9), fill=1)
    return img


# ------------------------------------------- 4. The Channel swim, 1875
def image4_channel():
    """Map of the Dover Strait: straight course vs. Webb's tide-bent path,
    the sea filled with seigaiha wave-scales."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # seigaiha: overlapping rows of concentric arcs across the whole sheet
    pr = 26 * s  # scale radius
    for row in range(-1, int(H * s / (pr * 0.55)) + 2):
        y = row * pr * 0.55
        off = 0 if row % 2 == 0 else pr
        for col in range(-1, int(W * s / (pr * 2)) + 2):
            x = col * pr * 2 + off
            for k in range(3):
                rr = pr - k * 7 * s
                if rr > 0:
                    dr.arc([x - rr, y - rr, x + rr, y + rr], 180, 360,
                           fill=(120, 120, 120), width=max(1, int(0.7 * s)))

    # England (top-left) and France (bottom-right), solid black coasts
    england = [(-10, -10), (150, -10), (132, 14), (118, 30), (96, 44),
               (88, 62), (72, 70), (52, 88), (30, 96), (10, 118), (-10, 124)]
    france = [(410, 310), (240, 310), (252, 286), (270, 272), (286, 252),
              (302, 246), (308, 228), (326, 218), (338, 198), (356, 192),
              (366, 172), (386, 162), (410, 148)]
    dr.polygon([(x * s, y * s) for x, y in england], fill=BLACK)
    dr.polygon([(x * s, y * s) for x, y in france], fill=BLACK)

    # ports
    dover = (92, 56)
    calais = (300, 240)
    for px, py in (dover, calais):
        dr.ellipse([(px - 4) * s, (py - 4) * s, (px + 4) * s, (py + 4) * s],
                   fill=WHITE, outline=BLACK, width=int(1.2 * s))

    # straight course: dashed black, 21 miles
    dx, dy = calais[0] - dover[0], calais[1] - dover[1]
    dist = math.hypot(dx, dy)
    steps = int(dist / 7)
    for i in range(steps):
        if i % 2 == 0:
            t0, t1 = i / steps, (i + 0.6) / steps
            dr.line([(dover[0] + dx * t0) * s, (dover[1] + dy * t0) * s,
                     (dover[0] + dx * t1) * s, (dover[1] + dy * t1) * s],
                    fill=BLACK, width=int(2.0 * s))

    # Webb's actual path: tides swept him along the channel axis, an S of S's
    path = []
    for i in range(201):
        t = i / 200
        px = dover[0] + dx * t
        py = dover[1] + dy * t
        # perpendicular tidal displacement: two big swings + small chop
        amp = (34 * math.sin(t * math.pi * 2.2 + 0.4) * math.sin(t * math.pi)
               + 5 * math.sin(t * math.pi * 9))
        nx, ny = -dy / dist, dx / dist
        path.append(((px + nx * amp) * s, (py + ny * amp) * s))
    dr.line(path, fill=RED, width=int(2.6 * s), joint="curve")

    img = finalize(img)
    dr = ImageDraw.Draw(img)
    dr.text((12, 6), "ENGLAND", font=font(FONT_SERIF_B, 15), fill=0)
    dr.text((316, 279), "FRANCE", font=font(FONT_SERIF_B, 15), fill=0)
    dr.text((104, 50), "Dover", font=font(FONT_SANS_B, 11), fill=1)
    dr.text((246, 232), "Calais", font=font(FONT_SANS_B, 11), fill=1)

    # title card, lower left, clear of the route
    dr.rectangle([12, 194, 238, 248], fill=1)
    dr.rectangle([14, 196, 236, 246], fill=0)
    dr.rectangle([15, 197, 235, 245], fill=1)
    dr.text((23, 201), "THE FIRST CHANNEL SWIM", font=font(FONT_SANS_B, 12), fill=0)
    dr.text((23, 218), "Matthew Webb · 24–25 Aug 1875", font=font(FONT_SANS, 10), fill=0)
    dr.text((23, 231), "21 mi across — 39 mi swum · 21h 45m", font=font(FONT_SANS, 10), fill=2)
    return img


# --------------------------------------------------- 5. Instant ramen, 1958
def image5_ramen():
    """Japanese poster: hinomaru sun, black bowl with a meander band,
    chopsticks lifting noodles. Momofuku Ando, 25 Aug 1958."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # hinomaru sun
    scx, scy, sr = 208 * s, 108 * s, 86 * s
    dr.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=RED)

    # steam: two S-curls rising from the bowl area, white over red / black over white
    for k, x0 in enumerate((150, 250)):
        pts = []
        for i in range(60):
            t = i / 59
            x = x0 * s + 14 * s * math.sin(t * math.pi * 2.4 + k * 1.7)
            y = (176 - 108 * t) * s
            pts.append((x, y))
        col = WHITE if k == 0 else (20, 20, 20)
        dr.line(pts, fill=col, width=int(3.2 * s), joint="curve")

    # chopsticks from upper right into the bowl
    tip1 = (196 * s, 132 * s)
    tip2 = (216 * s, 136 * s)
    dr.line([tip1, (356 * s, 30 * s)], fill=BLACK, width=int(3.4 * s))
    dr.line([tip2, (372 * s, 44 * s)], fill=BLACK, width=int(3.4 * s))

    # noodles: a bundle of wavy strands from chopstick tips into the bowl
    for j in range(7):
        pts = []
        x0 = 176 + j * 9
        for i in range(50):
            t = i / 49
            x = (x0 + 10 * math.sin(t * 6.28 * 1.6 + j)) * s
            y = (134 + 78 * t) * s
            pts.append((x, y))
        dr.line(pts, fill=(20, 20, 20), width=int(2.2 * s), joint="curve")

    # bowl: wide silhouette with a foot
    bowl = [(66, 196), (334, 196), (322, 232), (296, 258), (252, 270),
            (148, 270), (104, 258), (78, 232)]
    dr.polygon([(x * s, y * s) for x, y in bowl], fill=BLACK)
    dr.rectangle([164 * s, 270 * s, 236 * s, 282 * s], fill=BLACK)

    # meander (raimon) band on the bowl in white
    def meander(x, y, u):
        # one greek-key unit drawn with lines, u = unit size
        w = int(1.6 * s)
        seq = [(0, 0), (4, 0), (4, 3), (2, 3), (2, 2), (3, 2), (3, 1), (1, 1),
               (1, 4), (4, 4)]
        pts = [(x + px * u, y + py * u) for px, py in seq]
        dr.line(pts, fill=WHITE, width=w)

    u = 5.4 * s
    for k in range(9):
        meander((92 + k * 26) * s, 206 * s, u)

    img = finalize(img, dither=False)
    dr = ImageDraw.Draw(img)

    # vertical kanji: 即席ラーメン ("instant ramen") down the left edge
    jp = font(FONT_JP, 30)
    for i, ch in enumerate("即席ラーメン"):
        if ch == "ー":
            # vertical writing: the long-vowel bar runs vertically
            tile = Image.new("P", (34, 34), 0)
            tile.putpalette(PAL.getpalette())
            ImageDraw.Draw(tile).text((1, -2), ch, font=jp, fill=1)
            img.paste(tile.transpose(Image.Transpose.ROTATE_270), (14, 12 + i * 33))
        else:
            dr.text((14, 12 + i * 33), ch, font=jp, fill=1)

    dr.text((58, 284), "25 AUG 1958 · MOMOFUKU ANDO INVENTS INSTANT RAMEN",
            font=font(FONT_SANS_B, 10), fill=1)
    return img


if __name__ == "__main__":
    save(image1_neptune(), 1)
    save(image2_interstellar(), 2)
    save(image3_eclipse(), 3)
    save(image4_channel(), 4)
    save(image5_ramen(), 5)
    print("done")
