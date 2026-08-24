#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-08-24.

Today: Vesuvius erupted 1,947 years ago (24 Aug 79 AD); Pluto was reclassified
a dwarf planet exactly 20 years ago (24 Aug 2006); the Perseids end tonight;
and a deep partial lunar eclipse (96% umbral) arrives Friday 28 Aug.

Five 400x300 images in exactly three colors (white, black, red).
Tonal scenes render at 3x, LANCZOS downscale, Floyd-Steinberg dither into the
palette; hard-edged pieces quantize without dithering.
"""

import math
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
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
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


# ---------------------------------------------------------------- 1. Vesuvius
def image1_vesuvius():
    """24 Aug 79 AD, around noon: the Plinian column over the Bay of Naples."""
    rng = random.Random(79)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    horizon = int(0.78 * H * s)
    vent_x, vent_y = int(0.60 * W * s), int(0.46 * H * s)

    # Faint ash veil high in the sky
    for i in range(1400):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, 0.30 * H * s) * rng.random()
        r = rng.uniform(1, 5) * s
        g = rng.randint(190, 235)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(g, g, g))

    # The Plinian column: a rising trunk that spreads into Pliny's umbrella pine
    def blob(x, y, r, g):
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(g, g, g))

    canopy_y = int(0.13 * H * s)
    for i in range(5200):
        t = rng.random()  # 0 at vent, 1 at canopy
        y = vent_y + (canopy_y - vent_y) * t
        trunk_w = (0.030 + 0.075 * t**1.6) * W * s
        x = vent_x + rng.gauss(0, trunk_w)
        r = rng.uniform(2, 9) * s * (0.6 + 0.8 * t)
        core = abs(x - vent_x) / (trunk_w + 1)
        g = int(20 + 150 * min(1.0, core) + rng.uniform(-15, 40))
        blob(x, y, r, max(0, min(230, g)))
    # canopy spreading sideways, drifting east (right)
    for i in range(5200):
        u = rng.gauss(0.22, 0.38)  # spread, biased rightward
        if u < -0.55:  # keep the north-west corner clear for the caption
            u = -0.55 - (u + 0.55) * 0.2
        x = vent_x + u * 0.46 * W * s
        y = canopy_y + rng.gauss(0, 0.05 * H * s) - 0.02 * H * s * math.cos(u * 2)
        r = rng.uniform(3, 12) * s
        g = int(30 + 120 * abs(u) + rng.uniform(-20, 50))
        blob(x, y, r, max(0, min(235, g)))
    # ash fall streaks under the right canopy
    for i in range(260):
        x0 = vent_x + rng.uniform(0.10, 0.48) * W * s
        y0 = canopy_y + rng.uniform(0.02, 0.06) * H * s
        ln = rng.uniform(0.05, 0.30) * H * s
        g = rng.randint(120, 200)
        dr.line([x0, y0, x0 + ln * 0.18, y0 + ln], fill=(g, g, g), width=s)

    # Volcanic lightning inside the column (red)
    def bolt(x, y, length, ang, width):
        pts = [(x, y)]
        for _ in range(7):
            ang += rng.uniform(-0.7, 0.7)
            step = length / 7
            x += step * math.sin(ang)
            y += step * math.cos(ang)
            pts.append((x, y))
        dr.line(pts, fill=RED, width=width)

    for i in range(3):
        bx = vent_x + rng.uniform(-0.03, 0.05) * W * s
        by = canopy_y + rng.uniform(0.10, 0.20) * H * s
        bolt(bx, by, rng.uniform(0.10, 0.16) * H * s, rng.uniform(-0.3, 0.3), 3 * s)

    # The mountain: black silhouette up to the vent
    ridge = []
    left_base, right_base = int(0.30 * W * s), int(0.92 * W * s)
    npts = 60
    for i in range(npts + 1):
        t = i / npts
        x = left_base + (right_base - left_base) * t
        peak = 1 - abs(t - (vent_x - left_base) / (right_base - left_base)) ** 1.1 * 2.2
        y = horizon - max(0.0, peak) * (horizon - vent_y)
        y += rng.uniform(-2, 2) * s
        ridge.append((x, min(y, horizon)))
    poly = [(left_base, horizon)] + ridge + [(right_base, horizon)]
    dr.polygon(poly, fill=(10, 10, 10))

    # Crater glow + lava rivulets (red over black flank)
    for i in range(50):
        r = rng.uniform(2, 7) * s
        x = vent_x + rng.gauss(0, 6) * s
        y = vent_y + rng.uniform(0, 8) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    for i in range(3):
        x, y = vent_x + rng.uniform(-8, 8) * s, vent_y + 4 * s
        drift = rng.uniform(-0.16, 0.2)
        stop = vent_y + (horizon - vent_y) * rng.uniform(0.45, 0.7)
        pts = [(x, y)]
        while y < stop:
            y += rng.uniform(6, 14) * s
            x += rng.uniform(-1.5, 1.5) * s + drift * 8 * s
            pts.append((x, y))
        dr.line(pts, fill=RED, width=max(s, int(rng.uniform(0.8, 2.2) * s)))

    # The bay: dark water, wave scratches, a fleeing galley
    dr.rectangle([0, horizon, W * s, H * s], fill=(25, 25, 25))
    for i in range(220):
        x = rng.uniform(0, W * s)
        y = rng.uniform(horizon + 4 * s, H * s - 2 * s)
        ln = rng.uniform(4, 26) * s
        g = rng.randint(120, 255)
        dr.line([x, y, x + ln, y], fill=(g, g, g), width=s)
    # galley silhouette, lower left, rowing away
    gx, gy = int(0.16 * W * s), horizon + int(0.10 * (H * s - horizon))
    hull = [(gx - 26 * s, gy), (gx + 26 * s, gy), (gx + 18 * s, gy + 8 * s), (gx - 20 * s, gy + 8 * s)]
    dr.polygon(hull, fill=(0, 0, 0))
    dr.line([gx - 24 * s, gy, gx - 30 * s, gy - 10 * s], fill=(0, 0, 0), width=2 * s)  # prow
    dr.line([gx + 2 * s, gy, gx + 2 * s, gy - 22 * s], fill=(0, 0, 0), width=2 * s)  # mast
    dr.polygon([(gx + 2 * s, gy - 22 * s), (gx + 20 * s, gy - 14 * s), (gx + 2 * s, gy - 8 * s)], fill=(0, 0, 0))
    for i in range(6):  # oars
        ox = gx - 18 * s + i * 7 * s
        dr.line([ox, gy + 6 * s, ox - 4 * s, gy + 12 * s], fill=(0, 0, 0), width=s)

    # Caption on a clean plaque so the ash can't bury it
    f1 = font(FONT_SERIF_B, 25 * s)
    f2 = font(FONT_SERIF, 11 * s)
    plaque_w = max(
        dr.textlength("VESVVIVS", font=f1),
        dr.textlength("XXIV · AVG · ANNO LXXIX", font=f2),
        dr.textlength("1,947 years ago today", font=f2),
    ) + 20 * s
    dr.rectangle([8 * s, 8 * s, 8 * s + plaque_w, 82 * s], fill=WHITE, outline=BLACK, width=s)
    dr.text((18 * s, 12 * s), "VESVVIVS", font=f1, fill=(0, 0, 0))
    dr.text((19 * s, 46 * s), "XXIV · AVG · ANNO LXXIX", font=f2, fill=(0, 0, 0))
    dr.text((19 * s, 62 * s), "1,947 years ago today", font=f2, fill=RED)

    return finalize(img)


# ------------------------------------------------------------------- 2. Pluto
def image2_pluto():
    """24 Aug 2006: the IAU votes in Prague. Twenty years a dwarf planet."""
    rng = random.Random(134340)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # Starfield
    for i in range(240):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s)
        r = rng.choice([1, 1, 1, 2]) * s * 0.6
        dr.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

    cx, cy, R = 128 * s, 152 * s, 92 * s

    # Pluto: pale mottled disc
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(215, 215, 215))
    for i in range(900):  # mottling
        a = rng.uniform(0, 2 * math.pi)
        d = R * math.sqrt(rng.random()) * 0.97
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        r = rng.uniform(2, 10) * s
        g = rng.choice([160, 175, 190, 200, 235, 245])
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(g, g, g))
    # Cthulhu Macula: the dark whale along the equator, west of the heart
    for i in range(320):
        t = rng.random()
        x = cx - R * 0.92 + t * R * 0.95
        y = cy + R * 0.10 + math.sin(t * 3.1) * R * 0.10 + rng.gauss(0, R * 0.07)
        if (x - cx) ** 2 + (y - cy) ** 2 > (R * 0.95) ** 2:
            continue
        r = rng.uniform(3, 9) * s
        g = rng.randint(30, 90)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(g, g, g))

    # Tombaugh Regio: the heart, in red
    hx, hy = cx + R * 0.30, cy + R * 0.28
    hs = R * 0.0345  # heart scale
    pts = []
    for i in range(120):
        t = i / 120 * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        ang = -0.35  # slight tilt, like the real one
        xr = x * math.cos(ang) - y * math.sin(ang)
        yr = x * math.sin(ang) + y * math.cos(ang)
        pts.append((hx + xr * hs, hy + yr * hs))
    dr.polygon(pts, fill=RED)

    # Text block, right side
    tx = 248 * s
    dr.text((tx, 52 * s), "134340", font=font(FONT_MONO, 12 * s), fill=RED)
    dr.text((tx, 68 * s), "PLUTO", font=font(FONT_SERIF_B, 34 * s), fill=WHITE)
    lines = [
        ("planet", "1930 – 2006"),
        ("dwarf planet", "2006 –"),
    ]
    y = 120 * s
    fk = font(FONT_SANS, 11 * s)
    fv = font(FONT_MONO, 11 * s)
    for k, v in lines:
        dr.text((tx, y), k, font=fk, fill=WHITE)
        dr.text((tx + 78 * s, y), v, font=fv, fill=WHITE)
        y += 17 * s
    dr.line([tx, y + 4 * s, tx + 120 * s, y + 4 * s], fill=RED, width=s)
    dr.text((tx, y + 12 * s), "reclassified by the IAU", font=fk, fill=WHITE)
    dr.text((tx, y + 27 * s), "in Prague, 24 Aug 2006 —", font=fk, fill=WHITE)
    dr.text((tx, y + 42 * s), "twenty years ago today.", font=fk, fill=WHITE)
    dr.text((tx, y + 66 * s), "Still a world.", font=font(FONT_SERIF, 13 * s), fill=RED)
    dr.text((tx, y + 82 * s), "Still has a heart.", font=font(FONT_SERIF, 13 * s), fill=RED)

    return finalize(img)


# ------------------------------------------------------------------- 3. Kamon
def image3_kamon():
    """A generated family crest (kamon), seeded by the date. From the backlog."""
    rng = random.Random(20260824)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    cx, cy = W * s // 2, 140 * s
    R = 108 * s

    # enclosing ring (maru)
    ring_w = int(R * 0.085)
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLACK, width=ring_w)
    inner = R - ring_w * 2.2

    k = rng.choice([5, 6, 8])  # fold symmetry
    petal_len = inner * rng.uniform(0.86, 0.97)
    petal_half = rng.uniform(0.24, 0.40) * math.pi / k * 2  # angular half-width
    cut = rng.uniform(0.45, 0.62)  # white cutout ratio
    tip_r = inner * rng.uniform(0.06, 0.10)
    base_r = inner * rng.uniform(0.16, 0.24)
    rot0 = rng.uniform(0, 2 * math.pi)

    def petal(angle, length, half, color):
        """Teardrop petal from center along `angle`."""
        pts = []
        n = 48
        for i in range(n + 1):  # one side out
            t = i / n
            rr = length * math.sin(t * math.pi / 2) ** 0.8
            aa = angle - half * math.sin((1 - t) * math.pi) * (1 - t * 0.35)
            pts.append((cx + rr * math.cos(aa), cy + rr * math.sin(aa)))
        for i in range(n + 1):  # other side back
            t = 1 - i / n
            rr = length * math.sin(t * math.pi / 2) ** 0.8
            aa = angle + half * math.sin((1 - t) * math.pi) * (1 - t * 0.35)
            pts.append((cx + rr * math.cos(aa), cy + rr * math.sin(aa)))
        dr.polygon(pts, fill=color)

    for i in range(k):
        a = rot0 + i * 2 * math.pi / k
        petal(a, petal_len, petal_half, BLACK)
    for i in range(k):
        a = rot0 + i * 2 * math.pi / k
        petal(a, petal_len * cut + base_r * 0.4, petal_half * cut, WHITE)
    # tip dots
    if rng.random() < 0.8:
        for i in range(k):
            a = rot0 + i * 2 * math.pi / k
            x, y = cx + petal_len * 1.02 * math.cos(a), cy + petal_len * 1.02 * math.sin(a)
            dr.ellipse([x - tip_r, y - tip_r, x + tip_r, y + tip_r], fill=BLACK)
    # interstitial accents
    if rng.random() < 0.7:
        rr = petal_len * rng.uniform(0.55, 0.75)
        dot = inner * 0.045
        for i in range(k):
            a = rot0 + (i + 0.5) * 2 * math.pi / k
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
            dr.ellipse([x - dot, y - dot, x + dot, y + dot], fill=BLACK)
    # red center
    dr.ellipse([cx - base_r, cy - base_r, cx + base_r, cy + base_r], fill=RED)
    ir = base_r * 0.45
    if rng.random() < 0.5:
        dr.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=WHITE)

    # caption
    cap = "二〇二六年八月二十四日 · 日々の紋"
    fj = font(FONT_JP, 13 * s)
    tw = dr.textlength(cap, font=fj)
    dr.text(((W * s - tw) / 2, 268 * s), cap, font=fj, fill=BLACK)

    return finalize(img, dither=False)


# ---------------------------------------------------------------- 4. Sandpile
def image4_sandpile():
    """Abelian sandpile: 2^17 grains dropped on one cell, toppled to rest."""
    N = 2**17
    h = np.zeros((H, W), dtype=np.int64)
    h[H // 2, W // 2] = N
    while True:
        t = h >> 2
        if not t.any():
            break
        h -= t << 2
        h[1:, :] += t[:-1, :]
        h[:-1, :] += t[1:, :]
        h[:, 1:] += t[:, :-1]
        h[:, :-1] += t[:, 1:]

    # heights 0..3 -> palette indices (0=white, 1=black, 2=red)
    lut = np.array([0, 2, 1, 0], dtype=np.uint8)  # 0->white, 1->red, 2->black, 3->white
    idx = lut[h]

    img = Image.new("P", (W, H))
    img.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)
    img.putdata(idx.flatten().tolist())

    # caption drawn in palette space
    dr = ImageDraw.Draw(img)
    fm = font(FONT_MONO, 10)
    dr.text((6, H - 16), "abelian sandpile", font=fm, fill=1)
    label = "2^17 grains"
    tw = dr.textlength(label, font=fm)
    dr.text((W - tw - 6, H - 16), label, font=fm, fill=1)
    return img


# ----------------------------------------------------- 5. Lunar eclipse almanac
def image5_eclipse():
    """Friday's deep partial lunar eclipse: 96% of the Moon in Earth's umbra."""
    rng = random.Random(20260828)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # header band
    dr.rectangle([0, 0, W * s, 40 * s], fill=BLACK)
    dr.rectangle([0, 40 * s, W * s, 43 * s], fill=RED)
    dr.text((14 * s, 8 * s), "SKY ALMANAC", font=font(FONT_SERIF_B, 18 * s), fill=WHITE)
    sub = "week of 24 Aug 2026"
    fsub = font(FONT_MONO, 11 * s)
    dr.text((W * s - dr.textlength(sub, font=fsub) - 14 * s, 14 * s), sub, font=fsub, fill=WHITE)

    # left panel: night sky with the eclipsed moon
    px0, py0, px1, py1 = 14 * s, 56 * s, 196 * s, 252 * s
    dr.rectangle([px0, py0, px1, py1], fill=BLACK)
    for i in range(90):
        x, y = rng.uniform(px0 + 2 * s, px1 - 2 * s), rng.uniform(py0 + 2 * s, py1 - 2 * s)
        dr.ellipse([x - s * 0.7, y - s * 0.7, x + s * 0.7, y + s * 0.7], fill=WHITE)

    mcx, mcy, mR = (px0 + px1) // 2, (py0 + py1) // 2 - 6 * s, 58 * s
    # umbral red disc
    dr.ellipse([mcx - mR, mcy - mR, mcx + mR, mcy + mR], fill=RED)
    # faint maria in black on the red disc
    for i in range(60):
        a = rng.uniform(0, 2 * math.pi)
        d = mR * math.sqrt(rng.random()) * 0.9
        x, y = mcx + d * math.cos(a), mcy + d * math.sin(a)
        r = rng.uniform(2, 7) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(120, 0, 0))
    # the surviving bright sliver (4%), lower-left limb
    moon_mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(moon_mask)
    md.ellipse([mcx - mR, mcy - mR, mcx + mR, mcy + mR], fill=255)
    off = mR * 0.055
    md.ellipse(
        [mcx - mR + off, mcy - mR - off, mcx + mR + off, mcy + mR - off], fill=0
    )
    img.paste(Image.new("RGB", img.size, WHITE), (0, 0), moon_mask)
    dr.text((px0 + 8 * s, py1 - 20 * s), "96% in umbra", font=font(FONT_MONO, 10 * s), fill=WHITE)

    # right column: the facts
    tx = 210 * s
    dr.text((tx, 58 * s), "DEEP PARTIAL", font=font(FONT_SERIF_B, 17 * s), fill=BLACK)
    dr.text((tx, 79 * s), "LUNAR ECLIPSE", font=font(FONT_SERIF_B, 17 * s), fill=RED)
    dr.line([tx, 104 * s, tx + 176 * s, 104 * s], fill=BLACK, width=s)
    fk = font(FONT_SANS, 10 * s)
    fb = font(FONT_SANS_B, 10 * s)
    rows = [
        ("Fri 28 Aug", "04:12 UTC", fb),
        ("", "", fk),
        ("magnitude", "0.93 — near-total:", fk),
        ("", "a blood moon, one", fk),
        ("", "bright sliver left", fk),
        ("partiality", "3 h 18 m", fk),
        ("visible", "Americas, Europe,", fk),
        ("", "Africa", fk),
    ]
    y = 114 * s
    for kx, v, f in rows:
        if kx == "" and v == "":
            y += 4 * s
            continue
        if kx:
            dr.text((tx, y), kx, font=fb, fill=BLACK)
        dr.text((tx + 78 * s, y), v, font=f, fill=BLACK)
        y += 15 * s
    # footer
    dr.line([14 * s, 264 * s, W * s - 14 * s, 264 * s], fill=BLACK, width=s)
    foot = "tonight: the Perseids end · Friday: full Corn Moon"
    ff = font(FONT_MONO, 10 * s)
    dr.text(((W * s - dr.textlength(foot, font=ff)) / 2, 274 * s), foot, font=ff, fill=BLACK)

    return finalize(img)


def main():
    import os

    out_today = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "images")
    out_arch = os.path.dirname(os.path.abspath(__file__))
    makers = [
        image1_vesuvius,
        image2_pluto,
        image3_kamon,
        image4_sandpile,
        image5_eclipse,
    ]
    for i, make in enumerate(makers, 1):
        im = make()
        assert im.size == (W, H), (i, im.size)
        for d in (out_today, out_arch):
            im.save(os.path.join(d, f"{i}.png"), optimize=True)
        print(f"image {i}: {make.__doc__.strip().splitlines()[0]}")


if __name__ == "__main__":
    main()
