#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-21.

The sky and the calendar rhyme today: first-quarter moon at 11:07 UTC (terminator
on the central meridian — sharpest crater relief of the month) on the 57th anniversary
of the first Moonwalk (21 Jul 1969 UTC, Tranquility Base). Five 400x300 images in
exactly three colors (white, black, red) for a black/white/red e-ink panel.

  1. First Quarter    — procedural Lambert-sphere moon, real maria, grazing craters
  2. To the Moon      — Constructivist / El Lissitzky, red thrust wedge
  3. Abelian sandpile — 50k grains toppled at the origin; values 0..3 -> B/W/R
  4. Seigaiha         — traditional wave-scale pattern, an occasional red scale
  5. Sky this week    — almanac card, first quarter -> Full Buck Moon
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
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
IMAGES = os.path.join(REPO, "images")


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


def ctext(dr, xy, text, fnt, fill, anchor="la"):
    dr.text(xy, text, font=fnt, fill=fill, anchor=anchor)


# ----------------------------------------------------------- 1. First Quarter
def image1_first_quarter():
    """Physically-motivated first-quarter moon.

    Lambert sphere lit from due east: for an orthographic disc, the surface
    brightness of a point equals its horizontal coordinate u = (x-cx)/R, so the
    terminator falls exactly on the central meridian. Maria lower the albedo;
    craters add grazing-light rims and shadows, exaggerated near the terminator.
    """
    s = SS
    R = int(H * 0.44) * s
    cx, cy = int(W * 0.40) * s, int(H * 0.50) * s
    ww, hh = W * s, H * s

    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float64)
    u = (xx - cx) / R
    v = -(yy - cy) / R
    rr2 = u * u + v * v
    disc = rr2 <= 1.0

    lam = np.clip(u, 0.0, 1.0)          # Lambert brightness == horizontal coord
    z = np.sqrt(np.clip(1.0 - rr2, 0, 1))  # toward-viewer component (for limb)

    # selenographic coords of every disc pixel
    lat = np.arcsin(np.clip(v, -1, 1))
    coslat = np.clip(np.cos(lat), 1e-6, 1)
    sinlon = np.clip(u / coslat, -1, 1)
    lon = np.arcsin(sinlon)             # front hemisphere, degrees below
    latd = np.degrees(lat)
    lond = np.degrees(lon)

    # base regolith albedo with gentle mottling
    rng = np.random.default_rng(20260721)
    albedo = np.full((hh, ww), 0.74)
    mott = rng.normal(0, 1, (hh // (3 * s), ww // (3 * s)))
    mott = np.array(Image.fromarray(mott).resize((ww, hh), Image.BILINEAR))
    albedo += 0.03 * mott

    # maria (lower albedo) at real selenographic coordinates: (lonE, latN, radius_deg, depth)
    maria = [
        (59, 17, 12, 0.30),   # Crisium
        (31, 8, 17, 0.34),    # Tranquillitatis
        (18, 28, 15, 0.32),   # Serenitatis
        (51, -8, 14, 0.30),   # Fecunditatis
        (34, -15, 12, 0.30),  # Nectaris
        (5, 13, 9, 0.26),     # Vaporum
        (2, 55, 20, 0.22),    # Frigoris (northern arc)
        (23, 43, 10, 0.20),   # (northern mare edge)
    ]
    for lo, la, rad, depth in maria:
        d2 = ((lond - lo) / rad) ** 2 + ((latd - la) / (rad * 0.9)) ** 2
        albedo -= depth * np.exp(-d2 * 1.4)
    albedo = np.clip(albedo, 0.18, 0.95)

    shade = lam * albedo

    # limb darkening near the edge
    shade *= 0.55 + 0.45 * np.clip(z * 1.4, 0, 1)

    # craters: grazing-light rim (bright east side, dark west side) + shadow,
    # amplified near the terminator where the sun is low.
    def add_crater(lon0, lat0, rad_deg, amp=1.0):
        cxc = cx + R * math.cos(math.radians(lat0)) * math.sin(math.radians(lon0))
        cyc = cy - R * math.sin(math.radians(lat0))
        pr = R * math.sin(math.radians(rad_deg)) * math.cos(math.radians(lat0)) + 2
        if pr < 2:
            return
        x0 = max(0, int(cxc - pr - 2)); x1 = min(ww, int(cxc + pr + 2))
        y0 = max(0, int(cyc - pr - 2)); y1 = min(hh, int(cyc + pr + 2))
        if x0 >= x1 or y0 >= y1:
            return
        sub_u = (xx[y0:y1, x0:x1] - cxc)
        sub_v = (yy[y0:y1, x0:x1] - cyc)
        dist = np.sqrt(sub_u * sub_u + sub_v * sub_v) / pr
        inside = dist <= 1.15
        # grazing factor: crater at horizontal fraction ufrac; small -> near terminator
        ufrac = max(0.02, (cxc - cx) / R)
        graz = min(3.2, 0.6 / (ufrac + 0.12) + 0.5)
        ring = np.exp(-((dist - 0.92) ** 2) / 0.05)     # rim ring weight
        bowl = np.clip(1 - (dist / 0.8) ** 2, 0, 1)     # bowl floor weight
        cosang = np.divide(sub_u, np.hypot(sub_u, sub_v) + 1e-6)  # +1 east, -1 west
        delta = amp * graz * 0.32 * cosang * ring        # bright E rim, dark W rim
        delta -= amp * 0.10 * bowl                        # floor a touch darker
        sub = shade[y0:y1, x0:x1]
        sub[inside] += delta[inside]

    # named showpieces strung along the first-quarter terminator + a random field
    named = [
        (-2, -9, 8), (-4, -14, 6), (-1.5, -18, 5),   # Ptolemaeus / Alphonsus / Arzachel chain
        (26, -11, 5), (24, -14, 4), (23, -18, 4),    # Theophilus / Cyrillus / Catharina
        (2, 24, 5), (7, 40, 5), (-3, 9, 3),
        (38, 5, 4), (44, -2, 3), (14, 18, 3),
    ]
    for lo, la, rad in named:
        add_crater(lo, la, rad, amp=1.15)
    cr = random.Random(7)
    for _ in range(46):
        lo = cr.uniform(-6, 78)
        la = cr.uniform(-62, 62)
        if lo * lo + la * la < 30:
            continue
        add_crater(lo, la, cr.uniform(1.6, 4.2), amp=cr.uniform(0.6, 1.0))

    img = np.zeros((hh, ww, 3), dtype=np.uint8)      # black sky
    g = np.clip(shade, 0, 1)
    gg = (g * 255).astype(np.uint8)
    for c in range(3):
        img[:, :, c] = np.where(disc, gg, 0)

    pim = Image.fromarray(img, "RGB")
    dr = ImageDraw.Draw(pim)

    # a scatter of stars in the sky
    for _ in range(120):
        sx, sy = cr.randint(0, ww - 1), cr.randint(0, hh - 1)
        if (sx - cx) ** 2 + (sy - cy) ** 2 > (R + 6 * s) ** 2:
            dr.ellipse([sx, sy, sx + s, sy + s], fill=(150, 150, 150))

    # Tranquility Base marker (red) — Mare Tranquillitatis, 0.67N 23.47E.
    # Route the leader down-left into the night side, where red + light text pop.
    tlo, tla = 23.47, 0.67
    tx = cx + R * math.cos(math.radians(tla)) * math.sin(math.radians(tlo))
    ty = cy - R * math.sin(math.radians(tla))
    lx, ly = 18 * s, cy + R * 0.16
    dr.line([tx, ty, lx + 2 * s, ly - 2 * s], fill=RED, width=max(1, s))
    rr = 5 * s
    dr.ellipse([tx - rr, ty - rr, tx + rr, ty + rr], outline=RED, width=max(1, s))
    dr.ellipse([tx - s, ty - s, tx + s, ty + s], fill=RED)

    f_lab = font(FONT_SANS_B, 15 * s)
    f_lab2 = font(FONT_SANS, 12 * s)
    ctext(dr, (lx, ly), "TRANQUILITY BASE", f_lab, RED)
    ctext(dr, (lx, ly + 18 * s), "Apollo 11 · 21 Jul 1969", f_lab2, (215, 215, 215))

    # titles
    f_title = font(FONT_SERIF_B, 26 * s)
    f_sub = font(FONT_SANS, 13 * s)
    ctext(dr, (16 * s, 12 * s), "FIRST QUARTER", f_title, WHITE)
    ctext(dr, (17 * s, 40 * s), "21 July 2026 · 11:07 UTC", f_sub, (200, 200, 200))
    ctext(dr, (16 * s, hh - 26 * s), "the sharpest crater relief of the month",
          font(FONT_SANS, 12 * s), (185, 185, 185))

    return finalize(pim, dither=True)


# ------------------------------------------------------------- 2. To the Moon
def image2_constructivist():
    """El Lissitzky / Constructivist: a red thrust wedge driving toward the moon."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # thin diagonal scaffolding
    for i in range(-3, 9):
        x = i * 52
        dr.line([x, H, x + 150, 0], fill=BLACK, width=1)
    # a couple of bold black bars
    dr.polygon([(0, 250), (400, 120), (400, 138), (0, 268)], fill=BLACK)
    dr.polygon([(0, 300), (0, 282), (400, 150), (400, 168)], fill=BLACK)

    # the moon: a solid black disc, upper right, on a white halo so it reads clean
    mcx, mcy, mr = 316, 82, 60
    dr.ellipse([mcx - mr - 7, mcy - mr - 7, mcx + mr + 7, mcy + mr + 7], fill=WHITE)
    dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=BLACK)

    # orbit arc (thin red) sweeping around the moon
    dr.arc([mcx - 90, mcy - 90, mcx + 90, mcy + 90], start=40, end=310, fill=RED, width=4)

    # THE RED WEDGE — thrust vector from lower-left driving up into the moon
    dr.polygon([(20, 292), (250, 150), (206, 96), (14, 262)], fill=RED)
    dr.polygon([(206, 96), (250, 150), (300, 118), (238, 74)], fill=RED)  # spearhead

    # small constructivist detail circles
    dr.ellipse([54, 44, 92, 82], outline=BLACK, width=4)
    dr.ellipse([66, 56, 80, 70], fill=RED)
    for gx in range(0, 5):
        for gy in range(0, 2):
            cx = 30 + gx * 15
            cy = 210 + gy * 15
            dr.ellipse([cx, cy, cx + 4, cy + 4], fill=BLACK)

    # typography
    f_big = font(FONT_SANS_B, 46)
    f_med = font(FONT_SANS_B, 20)
    f_small = font(FONT_MONO_B, 15)
    ctext(dr, (24, 12), "К ЛУНЕ", f_big, BLACK)
    ctext(dr, (26, 62), "TO  THE  MOON", f_med, RED)
    ctext(dr, (398, 292), "1969 · 2026", f_small, BLACK, anchor="rs")

    return finalize(img, dither=False)


# ---------------------------------------------------------- 3. Abelian sandpile
def image3_sandpile():
    """Drop 50,000 grains on one cell of an infinite grid; topple until stable.
    Stable cell values are 0..3 — a natural three-colour image, no dithering."""
    n = 301
    c = n // 2
    grid = np.zeros((n, n), dtype=np.int64)
    grid[c, c] = 50000
    while True:
        topple = grid // 4
        if not topple.any():
            break
        grid -= topple * 4
        grid[1:, :] += topple[:-1, :]
        grid[:-1, :] += topple[1:, :]
        grid[:, 1:] += topple[:, :-1]
        grid[:, :-1] += topple[:, 1:]

    # crop to content
    nz = np.argwhere(grid > 0)
    (y0, x0), (y1, x1) = nz.min(0), nz.max(0) + 1
    g = grid[y0:y1, x0:x1]

    # values 0,1,2,3 -> colours (chosen for punch on the panel)
    lut = np.array([WHITE, RED, WHITE, BLACK], dtype=np.uint8)  # 0/2 white, 1 red accent, 3 black
    rgb = lut[g]
    tile = Image.fromarray(rgb, "RGB")

    # place centred on a white canvas, nearest-neighbour to keep cells crisp
    side = 268
    tile = tile.resize((side, side), Image.NEAREST)
    canvas = Image.new("RGB", (W, H), WHITE)
    canvas.paste(tile, ((W - side) // 2, (H - side) // 2 - 6))
    dr = ImageDraw.Draw(canvas)
    dr.rectangle([0, 0, W - 1, H - 1], outline=BLACK, width=2)
    f = font(FONT_MONO, 13)
    ctext(dr, (W // 2, H - 15), "ABELIAN SANDPILE  ·  50 000 GRAINS", f, BLACK, anchor="mm")
    return finalize(canvas, dither=False)


# --------------------------------------------------------------- 4. Seigaiha
def image4_seigaiha():
    """Seigaiha — 'blue-sea-wave' scales. Concentric arcs, an occasional red scale.
    A quiet nod to the Sea of Tranquility. Rendered 4x + dither for clean arcs."""
    s = 4
    ww, hh = W * s, H * s
    img = Image.new("RGB", (ww, hh), WHITE)
    dr = ImageDraw.Draw(img)

    R = 46 * s            # scale radius
    rings = 6
    dx = R                # horizontal centre spacing
    dy = int(R * 0.52)    # vertical row spacing (rows overlap heavily)
    rng = random.Random(721)

    row = 0
    y = -R
    while y < hh + R:
        offset = (R // 2) if (row % 2) else 0
        x = -R + offset
        while x < ww + R:
            red_scale = rng.random() < 0.07
            for k in range(rings):
                rr = R - k * (R // rings)
                if rr <= 2:
                    continue
                if red_scale and (k % 2 == 0):
                    col = RED
                else:
                    col = BLACK if (k % 2 == 0) else WHITE
                # filled disc, largest first -> concentric rings; upper part shows as a fan
                dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col)
            x += dx
        y += dy
        row += 1

    # mask to only show the classic upper-fan overlap: redraw is unnecessary — the
    # heavy vertical overlap already hides the lower halves of each scale.
    out = finalize(img, dither=True)
    return out


# ------------------------------------------------------------ 5. Sky this week
def image5_almanac():
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)
    dr.rectangle([0, 0, W - 1, H - 1], outline=BLACK, width=3)
    dr.rectangle([8, 8, W - 9, H - 9], outline=BLACK, width=1)

    f_h = font(FONT_SERIF_B, 27)
    f_dr = font(FONT_SANS, 13)
    ctext(dr, (22, 18), "SKY THIS WEEK", f_h, BLACK)
    ctext(dr, (23, 48), "21 – 28 July 2026", f_dr, RED)
    dr.line([22, 68, W - 22, 68], fill=BLACK, width=2)

    def half_moon(cx, cy, r, fill_right=True):
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK, width=2)
        if fill_right:
            dr.pieslice([cx - r, cy - r, cx + r, cy + r], -90, 90, fill=BLACK)
        else:
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK)

    f_b = font(FONT_SANS_B, 14)
    f_t = font(FONT_SANS, 13)
    y = 84
    # first quarter row
    half_moon(40, y + 8, 12, fill_right=True)
    ctext(dr, (62, y), "First Quarter tonight", f_b, BLACK)
    ctext(dr, (62, y + 18), "11:07 UTC — best crater relief", f_t, (60, 60, 60))

    y += 48
    # red full disc icon for the Buck Moon
    dr.ellipse([28, y - 4, 52, y + 20], fill=RED, outline=BLACK, width=2)
    ctext(dr, (62, y), "Full Buck Moon · Jul 28", f_b, RED)
    ctext(dr, (62, y + 18), "the month's bright full moon", f_t, (60, 60, 60))

    y += 48
    # planets split
    dr.ellipse([32, y + 2, 44, y + 14], fill=BLACK)
    dr.ellipse([36, y - 4, 40, y], fill=BLACK)
    ctext(dr, (62, y), "Planets split the horizons", f_b, BLACK)
    ctext(dr, (62, y + 18), "Venus + Jupiter W · Mars + Saturn E", f_t, (60, 60, 60))

    y += 48
    # meteors icon
    for i in range(3):
        dr.line([30 + i * 6, y + 2 + i * 4, 46 + i * 6, y - 6 + i * 4], fill=RED, width=2)
    ctext(dr, (62, y), "δ-Aquariid + α-Capricornid", f_b, BLACK)
    ctext(dr, (62, y + 18), "peak Jul 30 — full moon washes them out", f_t, (60, 60, 60))

    return finalize(img, dither=False)


# ---------------------------------------------------------------------- main
def main():
    os.makedirs(IMAGES, exist_ok=True)
    os.makedirs(HERE, exist_ok=True)
    builders = [
        image1_first_quarter,
        image2_constructivist,
        image3_sandpile,
        image4_seigaiha,
        image5_almanac,
    ]
    for i, b in enumerate(builders, 1):
        img = b()
        img.save(os.path.join(IMAGES, f"{i}.png"))
        img.save(os.path.join(HERE, f"{i}.png"))
        print("wrote", i)


if __name__ == "__main__":
    main()
