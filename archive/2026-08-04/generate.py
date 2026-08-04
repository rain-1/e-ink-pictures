#!/usr/bin/env python3
"""
e-ink pictures — 2026-08-04
Five images for a 400x300 black/white/red e-ink panel.

Today: Louis Armstrong's 125th birthday (b. New Orleans, 1901-08-04),
and eight days before the 2026-08-12 total solar eclipse + Perseid peak
under a new moon.

1. totality-minus-8  — almanac card for the Aug 12 eclipse + Perseids
2. satchmo-125       — jazz poster, trumpet silhouette in a red sunburst
3. red-wedge         — constructivist composition (Lissitzky homage, finally)
4. kamon             — procedural Japanese crest, seeded by the date
5. truchet           — multiscale Truchet arc tiling, seeded by the date
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3                      # supersample factor
W3, H3 = W * S, H * S
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SEED = 20260804

DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEJAVU_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def palette_image():
    p = Image.new("P", (1, 1))
    p.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0] * 249 * 3)
    return p


PAL = palette_image()


def finish(img3, name, dither=False):
    """Downscale 3x -> 1x, snap to the 3-color palette, save as mode-P PNG."""
    img = img3.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    q = img.convert("RGB").quantize(palette=PAL, dither=d)
    q.save(name)
    print("wrote", name)


def ctext(draw, xy, text, fnt, fill, anchor="mm"):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- 1: eclipse
def img1():
    im = Image.new("RGB", (W3, H3), WHITE)
    d = ImageDraw.Draw(im)

    cx, cy, r = 330, 430, 185

    # soft gray glow around the eclipsed sun (dithers into speckle)
    for rr in range(r + 150, r, -3):
        t = (rr - r) / 150.0
        g = int(255 - (1 - t) ** 2 * 110)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(g, g, g))

    # red corona rays
    for i in range(16):
        a = math.radians(i * 22.5 + 11)
        ln = r + 95 + (55 if i % 2 == 0 else 0)
        spread = math.radians(3.2)
        pts = [
            (cx + r * 0.9 * math.cos(a - spread * 3), cy + r * 0.9 * math.sin(a - spread * 3)),
            (cx + ln * math.cos(a), cy + ln * math.sin(a)),
            (cx + r * 0.9 * math.cos(a + spread * 3), cy + r * 0.9 * math.sin(a + spread * 3)),
        ]
        d.polygon(pts, fill=RED)

    # the moon covering the sun
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=7)

    # title
    ctext(d, (W3 // 2, 62), "TOTAL SOLAR ECLIPSE", font(DEJAVU, 72), BLACK)

    # right column
    rx = 880
    ctext(d, (rx, 210), "12 AUG", font(DEJAVU, 105), BLACK)
    ctext(d, (rx, 310), "IN 8 DAYS", font(DEJAVU, 62), RED)
    f = font(DEJAVU_REG, 44)
    for i, place in enumerate(["GREENLAND", "ICELAND", "SPAIN"]):
        y = 420 + i * 72
        d.ellipse([rx - 190 - 12, y - 12, rx - 190 + 12, y + 12], fill=RED)
        d.text((rx - 150, y), place, font=f, fill=BLACK, anchor="lm")
    ctext(d, (rx, 665), "path of totality", font(DEJAVU_REG, 34), BLACK)

    # bottom band: the Perseids, same night
    d.rectangle([0, 720, W3, H3], fill=BLACK)
    for k, (x0, y0) in enumerate([(24, 748), (52, 810), (1062, 760), (1094, 826)]):
        d.line([x0, y0, x0 + 72, y0 + 24], fill=(RED if k % 2 else WHITE), width=5)
        d.ellipse([x0 + 66, y0 + 18, x0 + 78, y0 + 30], fill=(RED if k % 2 else WHITE))
    ctext(d, (W3 // 2, 775), "THAT SAME NIGHT: PERSEIDS PEAK", font(DEJAVU, 52), WHITE)
    ctext(d, (W3 // 2, 845), "50–100 meteors/hr · new moon · darkest skies", font(DEJAVU_REG, 40), WHITE)

    finish(im, "1.png", dither=True)


# ---------------------------------------------------------------- 2: satchmo
def img2():
    im = Image.new("RGB", (W3, H3), WHITE)
    d = ImageDraw.Draw(im)

    # sunburst from the trumpet bell
    bx, by = 900, 330
    for i in range(24):
        if i % 2:
            continue
        a0 = math.radians(i * 15 + 4)
        a1 = math.radians(i * 15 + 11)
        L = 1500
        d.polygon(
            [(bx, by),
             (bx + L * math.cos(a0), by + L * math.sin(a0)),
             (bx + L * math.cos(a1), by + L * math.sin(a1))],
            fill=RED)

    # trumpet silhouette, pointing right, bell at (bx, by)
    ty = by
    # lead pipe
    d.rectangle([175, ty - 9, 700, ty + 9], fill=BLACK)
    # mouthpiece
    d.ellipse([128, ty - 20, 178, ty + 20], fill=BLACK)
    d.rectangle([100, ty - 26, 132, ty + 26], fill=BLACK)
    # bell flare (concave)
    top, bot = [], []
    for x in range(700, 901, 10):
        h = 9 + 96 * ((x - 700) / 200.0) ** 2.4
        top.append((x, ty - h))
        bot.append((x, ty + h))
    d.polygon(top + bot[::-1], fill=BLACK)
    d.ellipse([884, ty - 108, 916, ty + 108], fill=BLACK)
    # valves: pistons above, casings below
    for i, vx in enumerate((430, 495, 560)):
        d.rectangle([vx - 8, ty - 62, vx + 8, ty], fill=BLACK)          # piston stem
        d.rectangle([vx - 17, ty - 78, vx + 17, ty - 60], fill=BLACK)   # finger button
        d.rectangle([vx - 13, ty, vx + 13, ty + 78], fill=BLACK)        # casing
        d.ellipse([vx - 13, ty + 66, vx + 13, ty + 92], fill=BLACK)
    # tuning slide loop below
    d.rectangle([292, ty + 6, 310, ty + 66], fill=BLACK)
    d.rectangle([604, ty + 6, 622, ty + 66], fill=BLACK)
    d.rectangle([292, ty + 50, 622, ty + 66], fill=BLACK)

    # title block
    d.rectangle([0, 600, W3, H3], fill=BLACK)
    ctext(d, (W3 // 2, 700), "SATCHMO", font(DEJAVU, 175), WHITE)
    ctext(d, (W3 // 2, 822), "LOUIS ARMSTRONG · 125 YEARS", font(DEJAVU, 48), RED)
    ctext(d, (W3 // 2, 872), "New Orleans · August 4, 1901", font(DEJAVU_REG, 34), WHITE)

    finish(im, "2.png", dither=False)


# --------------------------------------------------------------- 3: red wedge
def img3():
    im = Image.new("RGB", (W3, H3), WHITE)
    d = ImageDraw.Draw(im)

    # black circle, upper right
    ccx, ccy, cr = 840, 300, 250
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=BLACK)

    # thin diagonal bars echoing the wedge
    ang = math.radians(-20)
    ux, uy = math.cos(ang), math.sin(ang)
    for off, wdt, ln in ((150, 10, 1500), (205, 22, 1250), (-90, 8, 1350)):
        px, py = -100 + (-uy) * off, 780 + (ux) * off
        d.polygon(
            [(px - uy * wdt, py + ux * wdt),
             (px + ux * ln - uy * wdt, py + uy * ln + ux * wdt),
             (px + ux * ln + uy * wdt, py + uy * ln - ux * wdt),
             (px + uy * wdt, py - ux * wdt)],
            fill=BLACK)

    # the red wedge, piercing the circle
    base = (-60, 860)
    tipx, tipy = ccx - 30, ccy + 20
    half = 130
    d.polygon(
        [(base[0] - uy * half, base[1] + ux * half),
         (tipx, tipy),
         (base[0] + uy * half, base[1] - ux * half)],
        fill=RED)
    # white notch where the wedge bites the circle
    d.polygon([(tipx, tipy), (tipx + 130, tipy - 45), (tipx + 100, tipy + 85)], fill=WHITE)

    # small satellites on the same axis
    d.ellipse([150, 130, 210, 190], fill=RED)
    d.rectangle([250, 145, 420, 175], fill=BLACK)
    d.ellipse([1035, 640, 1085, 690], fill=BLACK)
    d.rectangle([880, 700, 1150, 715], fill=RED)

    # rotated caption
    txt = Image.new("RGBA", (700, 90), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt)
    td.text((0, 0), "IV · VIII · MMXXVI", font=font(DEJAVU, 60), fill=BLACK + (255,))
    txt = txt.rotate(20, expand=True, resample=Image.BICUBIC)
    im.paste(txt, (95, 555), txt)

    finish(im, "3.png", dither=False)


# ------------------------------------------------------------------- 4: kamon
def img4():
    rng = random.Random(SEED)
    im = Image.new("RGB", (W3, H3), BLACK)
    d = ImageDraw.Draw(im)
    cx, cy = W3 // 2, H3 // 2
    R = 385

    # double enclosing ring
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=WHITE, width=16)
    r2 = R - 34
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=WHITE, width=5)

    k = rng.choice([5, 6, 8])
    motif = rng.choice(["teardrop", "crescent", "diamond"])
    rot0 = rng.uniform(0, 2 * math.pi)
    Rm = r2 - 40

    for i in range(k):
        a = rot0 + 2 * math.pi * i / k
        ca, sa = math.cos(a), math.sin(a)
        ex, ey = cx + Rm * 0.62 * ca, cy + Rm * 0.62 * sa
        col = RED if (k % 2 == 0 and i % 2 == 0) else WHITE
        if motif == "teardrop":
            rr = Rm * 0.30
            tip = (cx + Rm * ca * 0.98, cy + Rm * sa * 0.98)
            side = rr * 0.92
            d.polygon(
                [tip,
                 (ex - sa * side, ey + ca * side),
                 (ex + sa * side, ey - ca * side)],
                fill=col)
            d.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=col)
            d.ellipse([ex - rr * 0.45, ey - rr * 0.45, ex + rr * 0.45, ey + rr * 0.45], fill=BLACK)
        elif motif == "crescent":
            rr = Rm * 0.30
            d.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=col)
            off = rr * 0.42
            d.ellipse([ex - rr * 0.8 - ca * off, ey - rr * 0.8 - sa * off,
                       ex + rr * 0.8 - ca * off, ey + rr * 0.8 - sa * off], fill=BLACK)
        else:  # diamond
            rr = Rm * 0.34
            d.polygon(
                [(cx + Rm * ca, cy + Rm * sa),
                 (ex - sa * rr * 0.6, ey + ca * rr * 0.6),
                 (cx + Rm * 0.24 * ca, cy + Rm * 0.24 * sa),
                 (ex + sa * rr * 0.6, ey - ca * rr * 0.6)],
                fill=col)

    # center
    rc = Rm * 0.22
    d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=RED)
    d.ellipse([cx - rc * 0.45, cy - rc * 0.45, cx + rc * 0.45, cy + rc * 0.45], fill=WHITE)

    d.text((W3 - 30, H3 - 20), f"KAMON № {SEED} · {k}×{motif}", font=font(MONO, 30),
           fill=WHITE, anchor="rs")

    finish(im, "4.png", dither=False)


# ----------------------------------------------------------------- 5: truchet
def img5():
    rng = random.Random(SEED + 5)
    im = Image.new("RGB", (W3, H3), WHITE)
    d = ImageDraw.Draw(im)
    T = 100  # tile at 3x  -> ~33px tiles, 12 x 9 grid

    def qarc(px, py, r, a0, a1, color, w):
        # stroke centered on radius r (PIL draws width inward, so pad the bbox)
        rr = r + w // 2
        d.arc([px - rr, py - rr, px + rr, py + rr], a0, a1, fill=color, width=w)

    def arcs(x, y, t, orient, color, width):
        # two quarter arcs joining edge midpoints, centered at opposite corners
        if orient == 0:
            qarc(x, y, t // 2, 0, 90, color, width)
            qarc(x + t, y + t, t // 2, 180, 270, color, width)
        else:
            qarc(x + t, y, t // 2, 90, 180, color, width)
            qarc(x, y + t, t // 2, 270, 360, color, width)

    cols, rows = W3 // T, H3 // T
    tiles = [[(rng.randint(0, 1), RED if rng.random() < 0.13 else BLACK)
              for _ in range(cols)] for _ in range(rows)]
    # pass 1: thick colored strokes; pass 2: thinner white core -> outlined pipes
    for j in range(rows):
        for i in range(cols):
            o, c = tiles[j][i]
            arcs(i * T, j * T, T, o, c, 30)
    for j in range(rows):
        for i in range(cols):
            o, _ = tiles[j][i]
            arcs(i * T, j * T, T, o, WHITE, 12)

    finish(im, "5.png", dither=False)


if __name__ == "__main__":
    img1()
    img2()
    img3()
    img4()
    img5()
