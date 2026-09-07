#!/usr/bin/env python3
"""2026-08-03 — day 2: Under the ice / red wedge day.

Five 400x300 pictures for a black/white/red e-ink screen.
1. Nautilus 90 North   — USS Nautilus crossed the North Pole submerged, Aug 3 1958
2. The Red Wedge       — constructivist composition (Lissitzky homage)
3. TRS-80 READY>_      — the TRS-80 was unveiled Aug 3 1977
4. Eclipse + Perseids  — almanac poster for Aug 12 2026
5. Seigaiha sea        — wave-scale pattern; Columbus sailed Aug 3 1492
"""
import math
import random
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3  # supersample factor
BW, BH = W * S, H * S
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = os.path.dirname(os.path.abspath(__file__))

PALETTE_IMG = Image.new("P", (1, 1))
PALETTE_IMG.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0, 0, 0] * 253)

FONTDIR = "/usr/share/fonts/truetype"


def font(name, size):
    return ImageFont.truetype(f"{FONTDIR}/{name}", size)


def finish(img, path, dither=True):
    """Downscale from 3x, snap to the 3-color palette, save mode-P PNG."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    img = img.convert("RGB").quantize(palette=PALETTE_IMG, dither=d)
    img.save(path, optimize=True)
    print("wrote", path)


def ctext(d, xy, s, f, fill, anchor="mm"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- 1. Nautilus
def nautilus():
    rng = random.Random(19580803)
    img = Image.new("RGB", (BW, BH), BLACK)
    d = ImageDraw.Draw(img)

    # Depth gradient: dark grey-blue-ish water fading to black (greys dither nicely)
    for y in range(BH):
        t = y / BH
        v = max(0, int(55 - 90 * t))
        d.line([(0, y), (BW, y)], fill=(v, v, v))

    # Ice sheet with pressure ridges (jagged underside)
    ice_base = int(BH * 0.18)
    pts = [(0, 0), (BW, 0)]
    xs = list(range(BW, -1, -S * 4))
    for x in xs:
        ridge = ice_base + rng.randint(-14, 10) * S
        if rng.random() < 0.06:  # occasional deep keel
            ridge += rng.randint(15, 40) * S
        pts.append((x, ridge))
    d.polygon(pts, fill=WHITE)
    # faint ice cracks
    for _ in range(26):
        x0 = rng.randint(0, BW)
        y0 = rng.randint(0, ice_base)
        d.line([(x0, y0), (x0 + rng.randint(-40, 40), y0 + rng.randint(20, 70))],
               fill=(180, 180, 180), width=S)

    # 90N meridian: dashed white vertical line at pole
    px = int(BW * 0.62)
    y = ice_base + 30
    while y < BH - 40 * S:
        d.line([(px, y), (px, y + 8 * S)], fill=(200, 200, 200), width=S)
        y += 16 * S

    # Sonar rings from the sub
    cx, cy = int(BW * 0.40), int(BH * 0.55)
    for r in (60, 110, 170, 240):
        d.arc([cx - r * S // 2, cy - r * S // 2, cx + r * S // 2, cy + r * S // 2],
              -65, 65, fill=(210, 210, 210), width=S)

    # The submarine (red), heading right: hull + sail + planes + screw wake
    hw, hh = 95 * S, 13 * S  # half-width, half-height of hull
    d.ellipse([cx - hw, cy - hh, cx + hw, cy + hh], fill=RED)
    # sail (conning tower)
    sw = 14 * S
    d.polygon([(cx + 6 * S, cy - hh - 22 * S), (cx + 6 * S + sw, cy - hh - 22 * S),
               (cx + 10 * S + sw, cy - hh + 2 * S), (cx + 2 * S, cy - hh + 2 * S)],
              fill=RED)
    # tail planes
    d.polygon([(cx - hw + 6 * S, cy), (cx - hw - 14 * S, cy - 16 * S),
               (cx - hw - 8 * S, cy), (cx - hw - 14 * S, cy + 16 * S)], fill=RED)
    # bubble wake
    for i in range(28):
        bx = cx - hw - (10 + i * 4 + rng.randint(0, 8)) * S
        by = cy + rng.randint(-6 - i, 6 + i) * S
        r = rng.randint(1, 2) * S
        d.ellipse([bx - r, by - r, bx + r, by + r], outline=WHITE, width=S)

    # Text
    fb = font("dejavu/DejaVuSans-Bold.ttf", 22 * S)
    fs = font("dejavu/DejaVuSansMono.ttf", 11 * S)
    ctext(d, (BW * 0.5, BH * 0.88), "NAUTILUS 90 NORTH", fb, WHITE)
    ctext(d, (BW * 0.5, BH * 0.955),
          "FIRST SHIP AT THE NORTH POLE · SUBMERGED · 3 AUG 1958 23:15", fs,
          (200, 200, 200))
    ctext(d, (px, ice_base + 16 * S), "90°N", font("dejavu/DejaVuSans-Bold.ttf", 13 * S),
          WHITE, anchor="ma")
    finish(img, f"{OUT}/1.png", dither=True)


# ---------------------------------------------------------------- 2. Red wedge
def red_wedge():
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    # Black disc, upper right
    cx, cy, r = int(BW * 0.64), int(BH * 0.42), int(BH * 0.335)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK)

    # Red wedge piercing from lower-left into the disc
    tip = (int(BW * 0.66), int(BH * 0.44))
    d.polygon([(0, int(BH * 0.98)), (int(BW * 0.16), int(BH * 0.60)), tip], fill=RED)
    # thin white slit inside the disc continuing the wedge line (the "cut")
    d.line([tip, (int(BW * 0.80), int(BH * 0.30))], fill=WHITE, width=2 * S)

    # Diagonal black bars, lower right
    for i, (w_, l_) in enumerate([(7, 300), (4, 210), (10, 150)]):
        x0 = int(BW * 0.55) + i * 26 * S
        y0 = int(BH * 0.97)
        ang = math.radians(-52)
        x1 = x0 + int(l_ * S * math.cos(ang))
        y1 = y0 + int(l_ * S * math.sin(ang))
        d.line([(x0, y0), (x1, y1)], fill=BLACK, width=w_ * S)

    # Small red circle outline + black square, upper left (counterweight)
    d.ellipse([int(BW * 0.07), int(BH * 0.10), int(BW * 0.16), int(BH * 0.22)],
              outline=RED, width=3 * S)
    d.rectangle([int(BW * 0.115), int(BH * 0.155), int(BW * 0.165), int(BH * 0.225)],
                fill=BLACK)

    # Typography, constructivist: rotated caption strip
    fb = font("dejavu/DejaVuSans-Bold.ttf", 15 * S)
    strip = Image.new("RGB", (int(BW * 0.5), 22 * S), WHITE)
    sd = ImageDraw.Draw(strip)
    sd.text((0, 0), "AUGUST · АВГУСТ · 3", font=fb, fill=BLACK)
    strip = strip.rotate(38, expand=True, fillcolor=WHITE)
    mask = strip.convert("L").point(lambda v: 255 - v)
    img.paste(BLACK, (int(BW * 0.045), int(BH * 0.47)), mask)

    fs = font("dejavu/DejaVuSansMono.ttf", 10 * S)
    d.text((BW - 8 * S, 6 * S), "after El Lissitzky, 1919", font=fs, fill=BLACK,
           anchor="ra")
    finish(img, f"{OUT}/2.png", dither=False)


# ---------------------------------------------------------------- 3. TRS-80
def trs80():
    # Render at 200x150 for chunk, then nearest x2 to 400x300.
    w2, h2 = 200, 150
    img = Image.new("RGB", (w2, h2), WHITE)
    d = ImageDraw.Draw(img)

    # Bezel: white case, rounded dark screen
    d.rectangle([0, 0, w2, h2], fill=WHITE)
    d.rounded_rectangle([10, 8, w2 - 11, h2 - 20], radius=6, fill=BLACK)

    fm = font("dejavu/DejaVuSansMono-Bold.ttf", 8)
    lines = [
        ("READY", WHITE),
        (">10 PRINT \"HAPPY 49TH\"", WHITE),
        (">20 PRINT \"TRS-80\"", WHITE),
        (">30 GOTO 10", WHITE),
        (">RUN", WHITE),
        ("HAPPY 49TH", RED),
        ("TRS-80", WHITE),
        ("HAPPY 49TH", RED),
        ("TRS-80", WHITE),
        ("HAPPY 49TH", RED),
        ("BREAK AT 10", WHITE),
        (">█", WHITE),
    ]
    y = 13
    for s, c in lines:
        d.text((16, y), s, font=fm, fill=c)
        y += 9

    # Label on the case bottom
    fl = font("dejavu/DejaVuSans-Bold.ttf", 9)
    d.text((14, h2 - 14), "TRS-80", font=fl, fill=BLACK)
    d.text((58, h2 - 12), "UNVEILED 3 AUG 1977", font=font("dejavu/DejaVuSans.ttf", 7),
           fill=BLACK)
    d.rectangle([w2 - 42, h2 - 14, w2 - 14, h2 - 4], fill=RED)
    d.text((w2 - 28, h2 - 13), "49", font=fl, fill=WHITE, anchor="ma")

    img = img.resize((W, H), Image.NEAREST)
    # scanlines over the screen area only
    d2 = ImageDraw.Draw(img)
    for y in range(20, H - 42, 4):
        d2.line([(24, y), (W - 26, y)], fill=BLACK, width=1)
    finish(img, f"{OUT}/3.png", dither=False)


# ---------------------------------------------------------------- 4. Eclipse
def eclipse():
    rng = random.Random(20260812)
    img = Image.new("RGB", (BW, BH), BLACK)
    d = ImageDraw.Draw(img)

    # Star field
    for _ in range(240):
        x, y = rng.randint(0, BW), rng.randint(0, BH)
        r = rng.choice([1, 1, 1, 2]) * S // 2 + 1
        v = rng.randint(120, 255)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # Corona: radial streamers around the eclipsed sun
    cx, cy = int(BW * 0.32), int(BH * 0.42)
    R = int(BH * 0.19)
    for i in range(160):
        a = rng.uniform(0, 2 * math.pi)
        ln = R * rng.uniform(0.25, 1.45) * (1.5 if rng.random() < 0.12 else 1.0)
        x0 = cx + R * 1.02 * math.cos(a)
        y0 = cy + R * 1.02 * math.sin(a)
        x1 = cx + (R + ln) * math.cos(a)
        y1 = cy + (R + ln) * math.sin(a)
        v = rng.randint(120, 230)
        d.line([(x0, y0), (x1, y1)], fill=(v, v, v), width=S)
    # glow ring then black moon disc
    d.ellipse([cx - R - 3 * S, cy - R - 3 * S, cx + R + 3 * S, cy + R + 3 * S], fill=WHITE)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)

    # Perseid meteors: red streaks radiating from a point upper-right
    rx, ry = int(BW * 0.86), int(BH * 0.14)
    for _ in range(14):
        a = rng.uniform(math.radians(100), math.radians(240))
        d0 = rng.uniform(40, 120) * S
        d1 = d0 + rng.uniform(35, 110) * S
        x0, y0 = rx + d0 * math.cos(a), ry + d0 * math.sin(a)
        x1, y1 = rx + d1 * math.cos(a), ry + d1 * math.sin(a)
        d.line([(x0, y0), (x1, y1)], fill=RED, width=2 * S)
        d.ellipse([x1 - 2 * S, y1 - 2 * S, x1 + 2 * S, y1 + 2 * S], fill=RED)
    d.ellipse([rx - 2 * S, ry - 2 * S, rx + 2 * S, ry + 2 * S], fill=RED)

    # Text block lower area
    fb = font("dejavu/DejaVuSans-Bold.ttf", 21 * S)
    fs = font("dejavu/DejaVuSansMono.ttf", 11 * S)
    ctext(d, (BW * 0.5, BH * 0.78), "TOTAL SOLAR ECLIPSE", fb, WHITE)
    ctext(d, (BW * 0.5, BH * 0.865), "12 AUGUST 2026 · IN NINE DAYS", fs, RED)
    ctext(d, (BW * 0.5, BH * 0.935),
          "ICELAND · SPAIN · THAT NIGHT: PERSEIDS, NEW MOON, 100/hr", fs,
          (200, 200, 200))
    finish(img, f"{OUT}/4.png", dither=True)


# ---------------------------------------------------------------- 5. Seigaiha
def seigaiha():
    rng = random.Random(14920803)
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    horizon = int(BH * 0.30)
    # Sky: white, with a red sun
    scx, scy, sr = int(BW * 0.76), int(BH * 0.15), int(BH * 0.085)
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=RED)

    # Sea: rows of overlapping scale-waves, growing toward the viewer
    y = horizon
    row = 0
    while y < BH + 100 * S:
        t = (y - horizon) / (BH - horizon)  # 0 near horizon, 1 at bottom
        rad = int((14 + 34 * t) * S)  # scale radius grows with nearness
        step = int(rad * 1.9)
        offset = (row % 2) * step // 2
        for x in range(-step, BW + step, step):
            cx = x + offset
            red_scale = rng.random() < 0.05
            # base disc
            d.ellipse([cx - rad, y - rad, cx + rad, y + rad],
                      fill=RED if red_scale else WHITE,
                      outline=BLACK, width=max(S, int(S * (0.8 + t))))
            # concentric rings
            nrings = 4
            for i in range(1, nrings):
                rr = rad * (nrings - i) / nrings
                col = WHITE if red_scale else BLACK
                d.arc([cx - rr, y - rr, cx + rr, y + rr], 180, 360, fill=col,
                      width=max(S, int(S * (0.8 + t))))
        y += int(rad * 0.62)
        row += 1

    # clean band at horizon + caravel silhouette
    d.rectangle([0, horizon - int(3 * S), BW, horizon], fill=WHITE)
    bx, by = int(BW * 0.22), horizon
    # hull
    d.polygon([(bx - 22 * S, by - 2 * S), (bx + 22 * S, by - 2 * S),
               (bx + 14 * S, by + 8 * S), (bx - 14 * S, by + 8 * S)], fill=BLACK)
    # masts and sails
    d.line([(bx, by - 2 * S), (bx, by - 34 * S)], fill=BLACK, width=2 * S)
    d.polygon([(bx - 1 * S, by - 32 * S), (bx - 1 * S, by - 8 * S),
               (bx - 16 * S, by - 8 * S)], fill=BLACK)
    d.polygon([(bx + 1 * S, by - 28 * S), (bx + 1 * S, by - 8 * S),
               (bx + 13 * S, by - 8 * S)], fill=RED)
    d.line([(bx - 10 * S, by - 2 * S), (bx - 10 * S, by - 20 * S)], fill=BLACK, width=2 * S)
    d.polygon([(bx - 11 * S, by - 19 * S), (bx - 11 * S, by - 6 * S),
               (bx - 20 * S, by - 6 * S)], fill=BLACK)

    fs = font("dejavu/DejaVuSerif.ttf", 11 * S)
    d.text((int(BW * 0.03), int(BH * 0.035)), "3 · VIII · 1492", font=fs, fill=BLACK)
    d.text((int(BW * 0.03), int(BH * 0.095)), "out of Palos, before dawn", font=fs,
           fill=BLACK)
    finish(img, f"{OUT}/5.png", dither=False)


if __name__ == "__main__":
    nautilus()
    red_wedge()
    trs80()
    eclipse()
    seigaiha()
