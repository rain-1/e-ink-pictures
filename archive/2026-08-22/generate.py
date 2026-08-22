#!/usr/bin/env python3
"""
e-ink pictures — 2026-08-22
400x300, black / white / red.

Today: Claude Debussy born this day 1862 (Clair de lune, under a real 73% gibbous moon);
Voyager 2 confirmed Neptune's rings this day 1989 (arcs: Courage, Liberté, Égalité, Fraternité);
El Lissitzky red-wedge constructivism (the palette IS the movement — finally made it);
Battle of Bosworth Field this day 1485 (the crown found in a hawthorn bush);
and the deep-partial "blood moon" eclipse coming 27–28 August (96% umbral, greatest 04:12 UTC).
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
S = 3
BW, BH = W * S, H * S

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

DJV = "/usr/share/fonts/truetype/dejavu/"
F_SERIF = DJV + "DejaVuSerif.ttf"
F_SERIF_B = DJV + "DejaVuSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = DJV + "DejaVuSans.ttf"
F_SANS_B = DJV + "DejaVuSans-Bold.ttf"
F_MONO = DJV + "DejaVuSansMono.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


_pal = Image.new("P", (1, 1))
_pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0] * (768 - 9))


def quantize(img, dither):
    return img.convert("RGB").quantize(palette=_pal, dither=dither)


def finish(art3x, text_pass=None, dither=True):
    """Downscale 3x art, optionally run a 1x crisp text pass, snap to palette."""
    small = art3x.resize((W, H), Image.LANCZOS)
    if dither:
        small = quantize(small, Image.Dither.FLOYDSTEINBERG).convert("RGB")
    if text_pass:
        d = ImageDraw.Draw(small)
        text_pass(d, small)
    return quantize(small, Image.Dither.NONE)


# ----------------------------------------------------------------------------
# 1. Clair de lune — Debussy, born this day 1862; tonight's moon is 73% gibbous
# ----------------------------------------------------------------------------
def clair_de_lune():
    rng = random.Random(1862)
    img = Image.new("RGB", (BW, BH))
    d = ImageDraw.Draw(img)

    horizon = 620
    for y in range(BH):
        if y < horizon:
            v = 18 + int(30 * y / horizon)
        else:
            v = 34 - int(22 * (y - horizon) / (BH - horizon))
        d.line([(0, y), (BW, y)], fill=(v, v, v + 4))

    mx, my, mr = 860, 250, 165

    # halo
    for r in range(mr + 210, mr, -6):
        a = int(38 * (1 - (r - mr) / 210.0))
        d.ellipse([mx - r, my - r, mx + r, my + r], fill=(18 + a, 18 + a, 22 + a))

    # moon disk
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(232, 232, 232))
    # a few soft maria
    for (ox, oy, rr, v) in [(-40, -30, 42, 205), (30, 25, 30, 210), (-15, 60, 24, 208),
                            (55, -55, 20, 212), (-70, 30, 18, 206)]:
        d.ellipse([mx + ox - rr, my + oy - rr, mx + ox + rr, my + oy + rr], fill=(v, v, v))

    # waxing gibbous, 73% lit: shadow lune on the left
    shadow = Image.new("L", (BW, BH), 0)
    sd = ImageDraw.Draw(shadow)
    sd.pieslice([mx - mr, my - mr, mx + mr, my + mr], 90, 270, fill=255)
    a = int(mr * abs(2 * 0.73 - 1))  # terminator semi-axis
    sd.ellipse([mx - a, my - mr, mx + a, my + mr], fill=0)
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))
    img.paste(Image.new("RGB", (BW, BH), (30, 30, 36)), (0, 0), shadow)
    d = ImageDraw.Draw(img)

    # drifting clouds
    for (cy, cw, ch, v) in [(180, 520, 34, 66), (330, 640, 42, 52),
                            (255, 380, 26, 74), (430, 700, 40, 46)]:
        cx = rng.randint(150, BW - 200)
        layer = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for i in range(4):
            ox = rng.randint(-cw // 3, cw // 3)
            ld.ellipse([cx + ox - cw // 2, cy - ch // 2 + rng.randint(-10, 10),
                        cx + ox + cw // 2, cy + ch // 2], fill=(v + 30, v + 30, v + 34, 90))
        img.paste(Image.composite(layer, Image.new("RGBA", (BW, BH), (0, 0, 0, 0)), layer),
                  (0, 0), layer)
    d = ImageDraw.Draw(img)

    # a handful of stars, away from the moon
    for _ in range(70):
        x, y = rng.randint(0, BW - 1), rng.randint(0, horizon - 60)
        if math.hypot(x - mx, y - my) > mr + 190:
            v = rng.randint(120, 230)
            d.point((x, y), fill=(v, v, v))
            if rng.random() < 0.12:
                d.point((x + 1, y), fill=(v, v, v))

    # water: moon-glitter path
    for y in range(horizon, BH, 7):
        t = (y - horizon) / (BH - horizon)
        spread = 30 + 260 * t
        n = 2 if t < 0.5 else 3
        for _ in range(n):
            cx = mx + rng.randint(-int(spread), int(spread))
            ln = rng.randint(18, 40 + int(80 * t))
            v = rng.randint(120, 215)
            yy = y + rng.randint(-2, 2)
            d.line([(cx - ln // 2, yy), (cx + ln // 2, yy)], fill=(v, v, v), width=3)

    # shoreline + poplar silhouettes, left
    d.polygon([(0, BH), (0, 790), (140, 800), (330, 830), (520, 858), (620, 880),
               (620, BH)], fill=(6, 6, 8))
    for (tx, tw, th) in [(120, 60, 330), (215, 44, 240), (60, 48, 250)]:
        base = 805
        for i in range(14):
            t = i / 13.0
            rr = (tw / 2) * math.sin(math.pi * (0.15 + 0.85 * t)) * (1 - 0.25 * t)
            yy = base - th * t
            d.ellipse([tx - rr, yy - 16, tx + rr, yy + 16], fill=(6, 6, 8))

    # rowboat with a red lantern
    bx, by = 950, 780
    d.polygon([(bx - 58, by), (bx + 58, by), (bx + 40, by + 22), (bx - 40, by + 22)],
              fill=(5, 5, 6))
    d.line([(bx + 30, by), (bx + 34, by - 40)], fill=(5, 5, 6), width=5)
    d.ellipse([bx + 24, by - 60, bx + 46, by - 36], fill=(255, 0, 0))
    for i, yy in enumerate(range(by + 30, by + 90, 12)):
        ln = 22 - i * 3
        d.line([(bx + 32 - ln, yy), (bx + 32 + ln, yy)], fill=(150, 20, 20), width=3)

    def text_pass(td, im):
        td.text((16, 14), "Clair de lune", font=font(F_SERIF_I, 30), fill=WHITE)
        td.text((18, 52), "Claude Debussy · born this day, 1862",
                font=font(F_SANS, 11), fill=WHITE)
        td.text((16, 273), "« Au calme clair de lune triste et beau » — Verlaine",
                font=font(F_SERIF_I, 11), fill=WHITE)
    return finish(img, text_pass, dither=True)


# ----------------------------------------------------------------------------
# 2. Neptune's rings — confirmed by Voyager 2 this day, 1989
# ----------------------------------------------------------------------------
def neptune():
    rng = random.Random(1989)
    img = Image.new("RGB", (BW, BH), BLACK)
    d = ImageDraw.Draw(img)

    for _ in range(160):
        x, y = rng.randint(0, BW - 1), rng.randint(0, BH - 1)
        d.point((x, y), fill=WHITE)
        if rng.random() < 0.10:
            d.line([(x - 4, y), (x + 4, y)], fill=WHITE)
            d.line([(x, y - 4), (x, y + 4)], fill=WHITE)

    px, py, pr = 330, 660, 210  # planet centre (3x coords)

    # ring system on its own layer, tilted
    rings = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rings)
    tilt = 0.36
    ring_r = {"Galle": 290, "Le Verrier": 375, "Arago": 420, "Adams": 495}
    for name, rr in ring_r.items():
        wdt = 5 if name in ("Le Verrier", "Adams") else 3
        rd.ellipse([px - rr, py - rr * tilt, px + rr, py + rr * tilt],
                   outline=(255, 255, 255, 255), width=wdt)
    # the four bright arcs in the Adams ring, in red
    rr = ring_r["Adams"]
    for (a0, a1) in [(-58, -46), (-40, -22), (-16, -10), (-6, 4)]:
        rd.arc([px - rr, py - rr * tilt, px + rr, py + rr * tilt], a0, a1,
               fill=(255, 0, 0, 255), width=13)
    rings = rings.rotate(18, center=(px, py), resample=Image.BICUBIC)
    img.paste(rings, (0, 0), rings)
    d = ImageDraw.Draw(img)

    # planet drawn over the rings: black disk, white limb, banded
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=BLACK, outline=WHITE, width=7)
    for (frac, wdt) in [(-0.55, 4), (-0.2, 6), (0.2, 5), (0.55, 4)]:
        yy = py + pr * frac
        half = pr * math.cos(math.asin(abs(frac))) * 0.92
        d.arc([px - half, yy - 26, px + half, yy + 26], 200, 340, fill=WHITE, width=wdt)
    # Great Dark Spot, red
    d.ellipse([px - 60, py - 95, px + 55, py - 30], fill=RED)
    d.ellipse([px - 38, py - 78, px + 30, py - 47], fill=BLACK)

    # Voyager 2: dashed trajectory + tiny spacecraft
    path = [(BW - 60, 120), (900, 190), (760, 300), (660, 430)]
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]
        steps = 9
        for s in range(0, steps, 2):
            xa = x0 + (x1 - x0) * s / steps
            ya = y0 + (y1 - y0) * s / steps
            xb = x0 + (x1 - x0) * (s + 1) / steps
            yb = y0 + (y1 - y0) * (s + 1) / steps
            d.line([(xa, ya), (xb, yb)], fill=WHITE, width=3)
    vx, vy = 660, 430
    d.ellipse([vx - 26, vy - 26, vx + 26, vy + 26], outline=WHITE, width=5)  # dish
    d.ellipse([vx - 8, vy - 8, vx + 8, vy + 8], fill=RED)
    d.line([(vx + 20, vy + 20), (vx + 58, vy + 58)], fill=WHITE, width=4)

    def text_pass(td, im):
        td.text((14, 12), "THE RINGS OF NEPTUNE", font=font(F_SANS_B, 19), fill=WHITE)
        td.text((14, 36), "confirmed by Voyager 2 · 22 August 1989 · 37 years ago",
                font=font(F_SANS, 10), fill=WHITE)
        td.text((228, 64), "arcs of the Adams ring", font=font(F_SANS, 10), fill=WHITE)
        td.text((228, 78), "Courage · Liberté", font=font(F_SANS_B, 11), fill=RED)
        td.text((228, 92), "Égalité 1 & 2 · Fraternité", font=font(F_SANS_B, 11), fill=RED)
        td.text((228, 112), "rings: Galle, Le Verrier,", font=font(F_SANS, 10), fill=WHITE)
        td.text((228, 126), "Arago, Adams", font=font(F_SANS, 10), fill=WHITE)
        td.text((250, 282), "Voyager 2, outbound forever", font=font(F_SANS, 9), fill=WHITE)
    return finish(img, text_pass, dither=False)


# ----------------------------------------------------------------------------
# 3. Red wedge — after El Lissitzky, 1919
# ----------------------------------------------------------------------------
def red_wedge():
    rng = random.Random(1919)
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    # black half, on a slant
    d.polygon([(430, 0), (BW, 0), (BW, BH), (170, BH)], fill=BLACK)
    # white circle on the black field
    cx, cy, cr = 810, 450, 290
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=WHITE)
    # the red wedge
    tipx, tipy = cx - 12, cy
    d.polygon([(0, 170), (0, 730), (tipx, tipy)], fill=RED)
    d.polygon([(0, 330), (0, 570), (tipx - 340, tipy)], fill=WHITE)  # hollow core

    # shrapnel: small bars, each side in its opposite colour
    for _ in range(9):
        x = rng.randint(680, BW - 90)
        y = rng.randint(60, BH - 80)
        if math.hypot(x - cx, y - cy) < cr + 40:
            continue
        w2, h2 = rng.randint(30, 90), rng.randint(10, 22)
        ang = rng.choice([20, 45, -30, 65])
        bar = Image.new("RGBA", (w2, h2), (255, 255, 255, 255))
        bar = bar.rotate(ang, expand=True)
        img.paste(bar, (x, y), bar)
    for _ in range(6):
        x = rng.randint(30, 330)
        y = rng.randint(660, BH - 60)
        w2, h2 = rng.randint(24, 70), rng.randint(8, 16)
        ang = rng.choice([20, 45, -30])
        col = RED if rng.random() < 0.4 else BLACK
        bar = Image.new("RGBA", (w2, h2), col + (255,))
        bar = bar.rotate(ang, expand=True)
        img.paste(bar, (x, y), bar)
    d = ImageDraw.Draw(img)
    # a thin red orbit line echoing the circle
    d.ellipse([cx - cr - 60, cy - cr - 60, cx + cr + 60, cy + cr + 60],
              outline=RED, width=6)

    def text_pass(td, im):
        td.text((10, 8), "КЛИНОМ", font=font(F_SANS_B, 26), fill=BLACK)
        td.text((10, 38), "КРАСНЫМ", font=font(F_SANS_B, 26), fill=RED)
        td.text((392, 276), "БЕЙ БЕЛЫХ", font=font(F_SANS_B, 20), fill=WHITE, anchor="rs")
        td.text((392, 293), "beat the Whites with the red wedge — after El Lissitzky, 1919",
                font=font(F_SANS, 9), fill=WHITE, anchor="rs")
    return finish(img, text_pass, dither=False)


# ----------------------------------------------------------------------------
# 4. The crown in the hawthorn — Bosworth Field, this day 1485
# ----------------------------------------------------------------------------
def ring_text(img, center, radius, text, fnt, a0, a1, color, flip=False):
    n = len(text)
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        ang = a0 + (a1 - a0) * (i + 0.5) / n
        rad = math.radians(ang)
        x = center[0] + radius * math.sin(rad)
        y = center[1] - radius * math.cos(rad)
        tile = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((60, 60), ch, font=fnt, fill=color, anchor="mm")
        rot = -ang + (180 if flip else 0)
        tile = tile.rotate(rot, resample=Image.BICUBIC)
        img.paste(tile, (int(x - 60), int(y - 60)), tile)


def tudor_rose(d, x, y, r):
    for k in range(5):
        a = math.radians(90 + k * 72)
        px = x + r * 0.62 * math.cos(a)
        py = y - r * 0.62 * math.sin(a)
        d.ellipse([px - r * 0.5, py - r * 0.5, px + r * 0.5, py + r * 0.5],
                  fill=RED, outline=BLACK, width=3)
    d.ellipse([x - r * 0.42, y - r * 0.42, x + r * 0.42, y + r * 0.42],
              fill=WHITE, outline=BLACK, width=3)
    d.ellipse([x - r * 0.14, y - r * 0.14, x + r * 0.14, y + r * 0.14], fill=RED)


def bosworth():
    rng = random.Random(1485)
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    cx, cy = 600, 462
    # kamon-style ring: outer band with circular text
    d.ellipse([cx - 420, cy - 420, cx + 420, cy + 420], fill=BLACK)
    d.ellipse([cx - 330, cy - 330, cx + 330, cy + 330], fill=WHITE)
    d.ellipse([cx - 318, cy - 318, cx + 318, cy + 318], outline=BLACK, width=5)

    fnt = font(F_SERIF_B, 44)
    ring_text(img, (cx, cy), 374, "BOSWORTH FIELD", fnt, -62, 62, WHITE)
    ring_text(img, (cx, cy), 374, "22 AUGUST 1485", fnt, 242, 118, WHITE, flip=True)
    d = ImageDraw.Draw(img)
    for a in (90, 270):
        rad = math.radians(a)
        x = cx + 374 * math.sin(rad)
        y = cy - 374 * math.cos(rad)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=RED)

    # hawthorn bush + crown drawn on their own layer, clipped to the inner circle
    inner = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(inner)

    def branch(x0, y0, ang, ln, wdt, depth):
        x1 = x0 + ln * math.sin(math.radians(ang))
        y1 = y0 - ln * math.cos(math.radians(ang))
        d.line([(x0, y0), (x1, y1)], fill=BLACK, width=wdt)
        # thorn
        if depth <= 2 and ln > 40:
            tx = (x0 + x1) / 2
            ty = (y0 + y1) / 2
            ta = ang + (60 if rng.random() < 0.5 else -60)
            d.line([(tx, ty), (tx + 16 * math.sin(math.radians(ta)),
                               ty - 16 * math.cos(math.radians(ta)))], fill=BLACK, width=4)
        if depth == 0:
            d.ellipse([x1 - 13, y1 - 13, x1 + 13, y1 + 13], fill=RED)  # haw
            return
        for da in (-34, 8, 38):
            if rng.random() < 0.85:
                branch(x1, y1, ang + da + rng.randint(-8, 8),
                       ln * 0.66, max(3, wdt - 3), depth - 1)

    base_y = cy + 285
    d.ellipse([cx - 150, base_y - 26, cx + 150, base_y + 26], fill=BLACK)
    for a in (-58, -30, -8, 10, 32, 55):
        branch(cx + a * 2, base_y - 8, a, 120 + rng.randint(-12, 18), 11, 3)

    # the crown, caught in the branches: band + three points + orbs
    kx, ky = cx, cy - 130
    kw = 230
    band_top, band_bot = ky + 26, ky + 74
    for (x0, x1, apex) in [(-kw // 2, -kw // 6, -kw // 3),
                           (-kw // 6, kw // 6, 0),
                           (kw // 6, kw // 2, kw // 3)]:
        d.polygon([(kx + x0, band_top), (kx + x1, band_top), (kx + apex, ky - 58)],
                  fill=RED, outline=BLACK)
        d.ellipse([kx + apex - 14, ky - 86, kx + apex + 14, ky - 58],
                  fill=WHITE, outline=BLACK, width=5)
    d.rectangle([kx - kw // 2, band_top, kx + kw // 2, band_bot],
                fill=RED, outline=BLACK, width=6)
    for ox in (-72, 0, 72):
        d.ellipse([kx + ox - 11, (band_top + band_bot) // 2 - 11,
                   kx + ox + 11, (band_top + band_bot) // 2 + 11],
                  fill=WHITE, outline=BLACK, width=4)

    # clip the bush/crown layer into the crest
    clip = Image.new("L", (BW, BH), 0)
    ImageDraw.Draw(clip).ellipse([cx - 312, cy - 312, cx + 312, cy + 312], fill=255)
    img.paste(inner, (0, 0), clip)
    d = ImageDraw.Draw(img)

    tudor_rose(d, 105, 105, 62)
    tudor_rose(d, BW - 105, 105, 62)
    tudor_rose(d, 105, BH - 105, 62)
    tudor_rose(d, BW - 105, BH - 105, 62)

    return finish(img, None, dither=False)


# ----------------------------------------------------------------------------
# 5. Blood moon — deep partial eclipse, 27–28 August, five nights away
# ----------------------------------------------------------------------------
def blood_moon():
    rng = random.Random(2026)
    img = Image.new("RGB", (BW, BH), BLACK)
    d = ImageDraw.Draw(img)

    for _ in range(140):
        x, y = rng.randint(0, BW - 1), rng.randint(0, BH - 1)
        v = rng.randint(90, 200)
        d.point((x, y), fill=(v, v, v))

    mx, my, mr = 600, 430, 235

    # dull red halo
    for r in range(mr + 90, mr, -5):
        a = 1 - (r - mr) / 90.0
        d.ellipse([mx - r, my - r, mx + r, my + r], fill=(int(70 * a), 0, 0))

    # eclipsed disk: shades of red, mottled maria -> dithers into red/black
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(225, 30, 20))
    for _ in range(26):
        ang = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, mr * 0.82)
        ox, oy = mx + rr * math.cos(ang), my + rr * math.sin(ang)
        er = rng.randint(18, 70)
        v = rng.randint(90, 170)
        d.ellipse([ox - er, oy - er * 0.7, ox + er, oy + er * 0.7], fill=(v, 6, 4))
    # deeper umbral gradient toward upper right
    grad = Image.new("L", (BW, BH), 0)
    gd = ImageDraw.Draw(grad)
    for r in range(mr, 0, -4):
        a = int(120 * (1 - r / mr))
        gd.ellipse([mx + 70 - r, my - 70 - r, mx + 70 + r, my - 70 + r], fill=a)
    mask = Image.new("L", (BW, BH), 0)
    ImageDraw.Draw(mask).ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=255)
    grad.paste(0, (0, 0), Image.eval(mask, lambda p: 255 - p))
    img.paste(Image.new("RGB", (BW, BH), (60, 0, 0)), (0, 0), grad)
    d = ImageDraw.Draw(img)

    # the last bright sliver (4% out of the umbra), lower left
    sliver = Image.new("L", (BW, BH), 0)
    sd = ImageDraw.Draw(sliver)
    sd.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=255)
    ur = 640
    ux, uy = mx + (ur - mr + 34) * 0.7071, my - (ur - mr + 34) * 0.7071
    sd.ellipse([ux - ur, uy - ur, ux + ur, uy + ur], fill=0)
    sliver = sliver.filter(ImageFilter.GaussianBlur(3))
    img.paste(Image.new("RGB", (BW, BH), (250, 250, 250)), (0, 0), sliver)
    d = ImageDraw.Draw(img)

    # progression strip along the bottom
    for (x1, frac) in [(150, 0.25), (600, 0.96), (1050, 0.35)]:
        r1 = 52
        y1 = 800
        d.ellipse([x1 - r1, y1 - r1, x1 + r1, y1 + r1], fill=(240, 240, 240))
        # umbra circle bites from above, covering `frac` of the disk's diameter
        ur2 = r1 * 2.6
        dsh = r1 + ur2 - 2 * r1 * frac
        red_part = Image.new("L", (BW, BH), 0)
        rd2 = ImageDraw.Draw(red_part)
        rd2.ellipse([x1 - r1, y1 - r1, x1 + r1, y1 + r1], fill=255)
        keep = Image.new("L", (BW, BH), 0)
        ImageDraw.Draw(keep).ellipse([x1 - ur2, y1 - dsh - ur2, x1 + ur2, y1 - dsh + ur2],
                                     fill=255)
        red_part = Image.composite(red_part, Image.new("L", (BW, BH), 0), keep)
        img.paste(Image.new("RGB", (BW, BH), (200, 20, 10)), (0, 0), red_part)
    d = ImageDraw.Draw(img)

    def text_pass(td, im):
        td.text((200, 22), "BLOOD MOON", font=font(F_SANS_B, 28), fill=RED, anchor="mm")
        td.text((200, 44), "deep partial lunar eclipse · 27–28 August · five nights away",
                font=font(F_SANS, 10), fill=WHITE, anchor="mm")
        td.text((16, 96), "96% of the Moon", font=font(F_SANS_B, 11), fill=WHITE)
        td.text((16, 110), "inside Earth's umbra", font=font(F_SANS_B, 11), fill=WHITE)
        td.text((316, 96), "greatest eclipse", font=font(F_SANS, 10), fill=WHITE)
        td.text((316, 110), "04:12 UTC", font=font(F_SANS_B, 12), fill=RED)
        td.text((50, 288), "02:33", font=font(F_MONO, 10), fill=WHITE, anchor="mm")
        td.text((200, 288), "04:12", font=font(F_MONO, 10), fill=RED, anchor="mm")
        td.text((350, 288), "05:52 UTC", font=font(F_MONO, 10), fill=WHITE, anchor="mm")
        td.text((200, 222), "tonight: waxing gibbous, 73%, at apogee",
                font=font(F_SANS, 9), fill=WHITE, anchor="mm")
    return finish(img, text_pass, dither=True)


if __name__ == "__main__":
    for i, fn in enumerate([clair_de_lune, neptune, red_wedge, bosworth, blood_moon], 1):
        im = fn()
        assert im.size == (W, H)
        im.save(f"{i}.png", optimize=True)
        print(i, fn.__name__, "ok")
