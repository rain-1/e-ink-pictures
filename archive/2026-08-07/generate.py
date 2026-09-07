#!/usr/bin/env python3
"""
e-ink pictures — 2026-08-07
Five images, 400x300, palette {black, white, red}.

1. Man on Wire       — Philippe Petit's WTC walk, 52 years ago today
2. T-5: Eclipse      — countdown to Aug 12: total solar eclipse + Perseids at new moon
3. Red Wedge         — Lissitzky constructivist homage (from the backlog, finally)
4. Kamon             — date-seeded Japanese crest generator
5. Seigaiha          — wave-pattern sea with red sun
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3  # supersample factor
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.normpath(os.path.join(HERE, "..", "..", "images"))

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * S)


def canvas(bg=WHITE):
    img = Image.new("RGB", (W * S, H * S), bg)
    return img, ImageDraw.Draw(img)


def palettize(img, dither=False):
    pal = Image.new("P", (1, 1))
    pal.putpalette(list(BLACK) + list(WHITE) + list(RED) + [0, 0, 0] * 253)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=pal, dither=d)


def finish(img, name, dither=False):
    small = img.resize((W, H), Image.LANCZOS)
    palettize(small, dither).save(os.path.join(IMAGES, name))
    print("wrote", name)


def sx(*pts):
    """scale a flat list/tuple of 1x coords to supersampled coords"""
    return [p * S for p in pts]


def text_c(d, cx, y, s, f, fill):
    """centered text (1x coords)"""
    bb = d.textbbox((0, 0), s, font=f)
    d.text((cx * S - (bb[2] - bb[0]) / 2, y * S), s, font=f, fill=fill)


def text_r(d, rx, y, s, f, fill):
    """right-aligned text (1x coords)"""
    bb = d.textbbox((0, 0), s, font=f)
    d.text((rx * S - (bb[2] - bb[0]), y * S), s, font=f, fill=fill)


# ----------------------------------------------------------------------------
# 1. Man on Wire
# ----------------------------------------------------------------------------
def man_on_wire():
    img, d = canvas(WHITE)
    wire_y = 95

    # red sun in the gap between the towers
    d.ellipse(sx(200 - 46, 68 - 46, 200 + 46, 68 + 46), fill=RED)

    # towers with WTC pinstripe facades
    for x0, x1 in [(22, 150), (250, 378)]:
        d.rectangle(sx(x0, wire_y, x1, 258), fill=BLACK)
        for x in range(x0 + 4, x1 - 2, 4):
            d.line(sx(x, wire_y + 5, x, 254), fill=WHITE, width=S)

    # the wire
    d.line(sx(150, wire_y, 250, wire_y), fill=BLACK, width=5)

    # Petit: stick figure with balance pole, mid-crossing
    fx = 187
    d.ellipse(sx(fx - 3, 73, fx + 3, 79), fill=BLACK)          # head
    d.line(sx(fx, 79, fx, 88), fill=BLACK, width=4)            # body
    d.line(sx(fx, 88, fx - 4, wire_y), fill=BLACK, width=3)    # legs
    d.line(sx(fx, 88, fx + 4, wire_y), fill=BLACK, width=3)
    d.line(sx(fx - 22, 86, fx + 22, 83), fill=BLACK, width=2)  # balance pole

    # birds
    for bx, by in [(60, 40), (78, 50), (330, 32)]:
        d.line(sx(bx - 5, by, bx, by - 3), fill=BLACK, width=2)
        d.line(sx(bx, by - 3, bx + 5, by), fill=BLACK, width=2)

    # caption
    d.line(sx(22, 266, 378, 266), fill=RED, width=2)
    text_c(d, 200, 268, "MAN ON WIRE", font(F_SERIF_B, 17), BLACK)
    text_c(d, 200, 288, "PHILIPPE PETIT · WORLD TRADE CENTER · 7 AUGUST 1974",
           font(F_MONO, 8), BLACK)
    finish(img, "1.png")


# ----------------------------------------------------------------------------
# 2. T-5: total solar eclipse + Perseids
# ----------------------------------------------------------------------------
def eclipse():
    rng = random.Random(20260812)
    img, d = canvas(WHITE)
    sky_h = 205
    d.rectangle(sx(0, 0, W, sky_h), fill=BLACK)

    cx, cy, r = 135, 100, 50

    # stars
    for _ in range(70):
        x, y = rng.uniform(4, W - 4), rng.uniform(4, sky_h - 8)
        if math.hypot(x - cx, y - cy) < r + 65:
            continue
        d.ellipse(sx(x - 1.1, y - 1.1, x + 1.1, y + 1.1), fill=WHITE)

    # Perseid streaks: radiant off the top-right
    for _ in range(9):
        x, y = rng.uniform(150, W - 10), rng.uniform(5, sky_h - 30)
        if math.hypot(x - cx, y - cy) < r + 70:
            continue
        L = rng.uniform(18, 42)
        ang = math.atan2(y - 10, x - 390) # away from radiant at (390,10)
        x2, y2 = x + L * math.cos(ang), y + L * math.sin(ang)
        if math.hypot(x2 - cx, y2 - cy) < r + 60 or y2 > sky_h - 6:
            continue
        d.line(sx(x, y, x2, y2), fill=WHITE, width=S)
        d.ellipse(sx(x2 - 1.8, y2 - 1.8, x2 + 1.8, y2 + 1.8), fill=RED)

    # corona: radial streamers
    for i in range(90):
        ang = i * math.tau / 90 + rng.uniform(-0.02, 0.02)
        equat = abs(math.cos(ang))  # longer streamers near the "equator"
        L = rng.uniform(8, 20) + 34 * equat ** 2 * rng.uniform(0.5, 1.0)
        r0 = r + 4
        x1, y1 = cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)
        x2, y2 = cx + (r0 + L) * math.cos(ang), cy + (r0 + L) * math.sin(ang)
        d.line(sx(x1, y1, x2, y2), fill=WHITE,
               width=2 * S if rng.random() < 0.3 else S)
    d.ellipse(sx(cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4),
              outline=WHITE, width=int(1.5 * S))

    # chromosphere ring + moon disc
    d.ellipse(sx(cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2), fill=RED)
    d.ellipse(sx(cx - r, cy - r, cx + r, cy + r), fill=BLACK)

    # info panel
    d.rectangle(sx(0, sky_h, W, sky_h + 6), fill=RED)
    d.text(sx(16, 220), "TOTAL SOLAR ECLIPSE", font=font(F_SANS_B, 19), fill=BLACK)
    text_r(d, 384, 220, "T−5", font(F_SANS_B, 19), RED)
    lines = [
        "WED 12 AUG · totality over Greenland, Iceland, Spain",
        "same night: PERSEIDS peak on a new-moon sky, ~100/hr",
        "the darkest Perseid night until 2045 — go somewhere dark",
    ]
    for i, ln in enumerate(lines):
        d.text(sx(16, 251 + i * 15), ln, font=font(F_MONO, 9), fill=BLACK)
    finish(img, "2.png")


# ----------------------------------------------------------------------------
# 3. Red Wedge (after El Lissitzky, 1919)
# ----------------------------------------------------------------------------
def red_wedge():
    img, d = canvas(WHITE)

    # diagonal field: white upper-left, black lower-right
    d.rectangle(sx(0, 0, W, H), fill=BLACK)
    d.polygon(sx(0, 0, 240, 0, 0, 290), fill=WHITE)
    # white circle sitting in the black field
    ccx, ccy, cr = 272, 128, 82
    d.ellipse(sx(ccx - cr, ccy - cr, ccx + cr, ccy + cr), fill=WHITE)

    # the red wedge, launched from the white field, piercing the circle
    d.polygon(sx(6, 210, 6, 258, ccx + 6, ccy), fill=RED)

    # supporting cast: small hard shapes
    d.polygon(sx(60, 274, 92, 274, 76, 250), fill=RED)            # small triangle
    d.polygon(sx(112, 282, 136, 282, 124, 263), fill=WHITE)       # white triangle
    d.rectangle(sx(330, 226, 344, 288), fill=RED)                  # red bar
    d.rectangle(sx(352, 250, 362, 288), fill=WHITE)                # white bar
    d.ellipse(sx(100, 26, 120, 46), fill=BLACK)                    # black dot, white field
    d.rectangle(sx(130, 32, 178, 40), fill=BLACK)                  # black bar
    d.rectangle(sx(130, 48, 156, 54), fill=RED)                    # red bar
    for i in range(5):                                             # hatching, white field
        d.line(sx(30, 104 + i * 8, 88, 104 + i * 8), fill=BLACK, width=S)
    # crack lines radiating where the wedge hits
    for ang in (-42, -12, 18, 46):
        a = math.radians(ang)
        x2 = ccx + 6 + 32 * math.cos(a)
        y2 = ccy + 32 * math.sin(a)
        d.line(sx(ccx + 6, ccy, x2, y2), fill=BLACK, width=2 * S)

    d.text(sx(16, 2), "7", font=font(F_SANS_B, 46), fill=RED)
    d.text(sx(18, 64), "АВГУСТА", font=font(F_SANS_B, 13), fill=BLACK)
    d.text(sx(176, 282), "ПОСЛЕ ЛИСИЦКОГО · 1919", font=font(F_MONO, 8), fill=WHITE)
    finish(img, "3.png")


# ----------------------------------------------------------------------------
# 4. Kamon — date-seeded crest generator
# ----------------------------------------------------------------------------
def kamon():
    rng = random.Random(20260807)
    img, d = canvas(WHITE)
    cx, cy = 186, 150

    # enclosing rings
    d.ellipse(sx(cx - 122, cy - 122, cx + 122, cy + 122), outline=BLACK, width=6 * S)
    d.ellipse(sx(cx - 110, cy - 110, cx + 110, cy + 110), outline=BLACK, width=1 * S)

    k = rng.choice([6, 8, 12])
    base = rng.uniform(0, math.tau)
    r0, r1 = 24, 98
    pinch = rng.uniform(0.55, 0.9)
    wmax = (math.pi * r1 / k) * rng.uniform(0.55, 0.75)

    def petal(theta, rin, rout, wscale, fill):
        pts = []
        n = 26
        fwd, back = [], []
        for i in range(n + 1):
            t = i / n
            rr = rin + (rout - rin) * t
            w = wscale * math.sin(math.pi * t) ** pinch
            fwd.append((rr, w))
            back.append((rr, -w))
        for rr, w in fwd + back[::-1]:
            x = cx + rr * math.cos(theta) - w * math.sin(theta)
            y = cy + rr * math.sin(theta) + w * math.cos(theta)
            pts.extend([x, y])
        d.polygon(sx(*pts), fill=fill)

    # petals: black, with a white inner petal, red on a chosen few
    reds = set(rng.sample(range(k), rng.choice([1, 2])))
    for i in range(k):
        th = base + i * math.tau / k
        petal(th, r0, r1, wmax, RED if i in reds else BLACK)
        petal(th, r0 + 10, r1 - 12, wmax * 0.45, WHITE)

    # gap dots
    if rng.random() < 0.8:
        for i in range(k):
            th = base + (i + 0.5) * math.tau / k
            gx, gy = cx + 88 * math.cos(th), cy + 88 * math.sin(th)
            d.ellipse(sx(gx - 3.5, gy - 3.5, gx + 3.5, gy + 3.5), fill=BLACK)

    # core
    d.ellipse(sx(cx - 27, cy - 27, cx + 27, cy + 27), fill=BLACK)
    d.ellipse(sx(cx - 22, cy - 22, cx + 22, cy + 22), fill=WHITE)
    d.ellipse(sx(cx - 15, cy - 15, cx + 15, cy + 15), fill=RED)

    # vertical date, right margin + red seal
    jp = font(F_JP, 20)
    for i, ch in enumerate("八月七日"):
        text_c(d, 368, 34 + i * 26, ch, jp, BLACK)
    d.rectangle(sx(357, 148, 379, 170), fill=RED)
    text_c(d, 368, 149, "紋", font(F_JP, 15), WHITE)
    finish(img, "4.png")


# ----------------------------------------------------------------------------
# 5. Seigaiha — wave sea with red sun
# ----------------------------------------------------------------------------
def seigaiha():
    rng = random.Random(2026 * 807)
    img, d = canvas(WHITE)
    horizon = 112

    # red sun
    d.ellipse(sx(318 - 30, 52 - 30, 318 + 30, 52 + 30), fill=RED)
    # birds
    for bx, by in [(70, 38), (95, 48), (120, 34), (245, 60)]:
        d.line(sx(bx - 6, by, bx, by - 4), fill=BLACK, width=2)
        d.line(sx(bx, by - 4, bx + 6, by), fill=BLACK, width=2)

    # seigaiha fans, back to front, growing toward the viewer
    y = horizon + 2
    j = 0
    while y < H + 60:
        s = 1.0 + 0.32 * j
        cw = 46 * s          # fan spacing
        fr = 30 * s          # fan radius
        rh = 13 * s          # row step
        off = (j % 2) * cw / 2
        x = -off - cw
        lw = max(S, int(2 * s * S / 3))
        while x < W + cw:
            red_fan = rng.random() < 0.09
            ring_col = RED if red_fan else BLACK
            d.ellipse(sx(x - fr, y - fr, x + fr, y + fr),
                      fill=WHITE, outline=ring_col, width=lw)
            for q in (0.72, 0.44, 0.16):
                rr = fr * q
                d.ellipse(sx(x - rr, y - rr, x + rr, y + rr),
                          outline=ring_col, width=lw)
            if red_fan:
                rr = fr * 0.16
                d.ellipse(sx(x - rr, y - rr, x + rr, y + rr), fill=RED)
            x += cw
        y += rh
        j += 1

    # sailboat riding a back-row crest, silhouetted against the sky
    bx, by = 138, 86
    d.polygon(sx(bx - 15, by, bx + 15, by, bx + 10, by + 7, bx - 10, by + 7), fill=BLACK)
    d.polygon(sx(bx - 1, by - 3, bx - 1, by - 26, bx - 16, by - 3), fill=BLACK)
    d.polygon(sx(bx + 2, by - 3, bx + 2, by - 20, bx + 13, by - 3), fill=BLACK)

    finish(img, "5.png")


if __name__ == "__main__":
    os.makedirs(IMAGES, exist_ok=True)
    man_on_wire()
    eclipse()
    red_wedge()
    kamon()
    seigaiha()
