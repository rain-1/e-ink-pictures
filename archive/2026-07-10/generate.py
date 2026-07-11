#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-10 (Tesla's 170th birthday).

Five 400x300 images in exactly three colors (white, black, red).
July 10 turns out to be an electric date: Nikola Tesla born 1856 (at midnight,
in a lightning storm), Telstar 1 launched 1962 (first live TV across an ocean),
and the hottest air temperature ever recorded on Earth (Death Valley, 1913).
Tonight the old crescent moon slips past the Pleiades with Mars nearby.
"""

import math
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
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


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


# ------------------------------------------------- 1. Tesla, constructivist
def image1_tesla_constructivist():
    """The Lissitzky piece from the backlog, finally. A red lightning wedge
    strikes a white circle across a diagonally split field. Hard edges,
    pure palette, no dithering."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # diagonal split: black field above the line (0,190)-(400,30)
    dr.polygon([(0, 0), (W * s, 0), (W * s, 30 * s), (0, 190 * s)], fill=BLACK)

    # white circle sitting mostly in the black field
    cx, cy, r = 258 * s, 108 * s, 78 * s
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)

    # the red lightning wedge: broad at lower-left, striking to the circle center
    bolt = [
        (6, 296), (60, 268),      # broad base
        (128, 212), (108, 208),   # first kink (backstep makes the zigzag)
        (172, 152), (150, 146),   # second kink
        (258, 108),               # tip: dead center of the circle
        (128, 232),               # return edge
        (148, 238),
        (84, 288),
    ]
    dr.polygon([(x * s, y * s) for x, y in bolt], fill=RED)

    # small counterweight: red square in the far black corner
    dr.rectangle([368 * s, 12 * s, 388 * s, 32 * s], fill=RED)

    # typography, constructivist: big name, stacked figure
    f_name = font(FONT_SANS_B, 44 * s)
    f_num = font(FONT_SANS_B, 30 * s)
    f_sm = font(FONT_SANS_B, 10 * s)
    f_xs = font(FONT_SANS, 9 * s)
    dr.text((14 * s, 8 * s), "TESLA", font=f_name, fill=WHITE)
    dr.text((14 * s, 56 * s), "170", font=f_num, fill=RED)
    # right column, in the white lower field
    dr.text((W * s - 14 * s, 218 * s), "BORN AT MIDNIGHT", font=f_sm,
            fill=BLACK, anchor="ra")
    dr.text((W * s - 14 * s, 232 * s), "IN A LIGHTNING STORM", font=f_sm,
            fill=RED, anchor="ra")
    dr.text((W * s - 14 * s, 248 * s), "SMILJAN · 10 VII 1856", font=f_xs,
            fill=BLACK, anchor="ra")
    dr.text((W * s - 14 * s, 262 * s),
            "the midwife called him a child of the storm;", font=f_xs, fill=BLACK,
            anchor="ra")
    dr.text((W * s - 14 * s, 275 * s),
            "his mother said: no — a child of the light", font=f_xs, fill=BLACK,
            anchor="ra")
    return finalize(img, dither=False)


# ------------------------------------------------------- 2. Polyphase (3φ)
def image2_polyphase():
    """Three-phase alternating current: three sine waves a third of a turn
    apart. Tesla's polyphase system (1888) is still the shape of every
    power grid on Earth — and at every instant the three sum to zero."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    x0, x1 = 18, 382
    ymid, amp = 148, 74
    cycles = 2.0

    # faint horizontal axis + vertical grid every quarter cycle
    dr.line([x0 * s, ymid * s, x1 * s, ymid * s], fill=(90, 90, 90), width=s)
    for k in range(int(cycles * 4) + 1):
        gx = (x0 + (x1 - x0) * k / (cycles * 4)) * s
        for gy in range(int((ymid - amp) * s), int((ymid + amp) * s), 7 * s):
            dr.line([gx, gy, gx, gy + 2 * s], fill=(70, 70, 70), width=s)

    def wave(phase_deg, fill, width, dash=None):
        pts = []
        for px in range(x0 * s, x1 * s + 1, s):
            t = (px / s - x0) / (x1 - x0)
            y = ymid - amp * math.sin(2 * math.pi * (cycles * t) -
                                      math.radians(phase_deg))
            pts.append((px, y * s))
        if dash is None:
            dr.line(pts, fill=fill, width=width, joint="curve")
        else:
            on, off = dash
            run = 0.0
            for i in range(len(pts) - 1):
                seg = math.hypot(pts[i + 1][0] - pts[i][0],
                                 pts[i + 1][1] - pts[i][1])
                if (run % (on + off)) < on:
                    dr.line([pts[i], pts[i + 1]], fill=fill, width=width)
                run += seg

    wave(0, WHITE, 3 * s)                              # phase A
    wave(120, (150, 150, 150), 2 * s)                  # phase B (gray → dither)
    wave(240, RED, 3 * s)                              # phase C

    # phase labels riding their crests
    f_lbl = font(FONT_MONO_B, 12 * s)
    crest = lambda ph: (x0 + (x1 - x0) * ((90 + ph) / 360) / cycles)
    dr.text((crest(0) * s, (ymid - amp - 16) * s), "A", font=f_lbl, fill=WHITE,
            anchor="ma")
    dr.text((crest(120) * s, (ymid - amp - 16) * s), "B", font=f_lbl,
            fill=(150, 150, 150), anchor="ma")
    dr.text((crest(240) * s, (ymid - amp - 16) * s), "C", font=f_lbl, fill=RED,
            anchor="ma")

    # header
    f_big = font(FONT_SANS_B, 26 * s)
    f_sm = font(FONT_SANS, 10 * s)
    dr.text((16 * s, 10 * s), "3φ", font=f_big, fill=RED)
    dr.text((58 * s, 16 * s), "POLYPHASE — Tesla, 1888", font=font(FONT_SANS_B, 12 * s),
            fill=WHITE)
    # footer
    dr.line([16 * s, 258 * s, (W - 16) * s, 258 * s], fill=(120, 120, 120),
            width=s)
    dr.text((16 * s, 266 * s),
            "three currents, a third of a turn apart — the shape of every grid",
            font=f_sm, fill=WHITE)
    dr.text((16 * s, 281 * s),
            "at every instant the three sum exactly to zero",
            font=f_sm, fill=RED)
    return finalize(img)


# ----------------------------------------------------------- 3. Telstar 1
def image3_telstar():
    """Telstar 1, launched 10 July 1962: a faceted 88 cm sphere that relayed
    the first live television picture across an ocean."""
    rng = random.Random(19620710)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # stars
    for _ in range(150):
        x, y = rng.uniform(0, W * s), rng.uniform(0, 218 * s)
        v = rng.randint(110, 230)
        r = rng.uniform(0.4, 1.1) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # Earth limb: big circle far below, only the top arc visible
    ec_x, ec_y, ec_r = 200 * s, (300 + 560) * s, 640 * s
    dr.ellipse([ec_x - ec_r, ec_y - ec_r, ec_x + ec_r, ec_y + ec_r],
               fill=(215, 215, 215))
    # thin bright atmosphere line on the limb
    dr.arc([ec_x - ec_r, ec_y - ec_r, ec_x + ec_r, ec_y + ec_r],
           255, 285, fill=WHITE, width=2 * s)
    # ground station marks on the limb
    def limb_point(deg):
        a = math.radians(deg)
        return ec_x + ec_r * math.cos(a), ec_y + ec_r * math.sin(a)
    gs1 = limb_point(258.5)   # Andover, Maine (left)
    gs2 = limb_point(282.5)   # Goonhilly Downs (right)

    # the satellite: faceted sphere
    sx, sy, sr = 200 * s, 108 * s, 52 * s
    dr.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(60, 60, 60))
    # solar-cell facets: lat/lon grid of small tiles, shaded by a light from
    # upper left
    for lat in range(-75, 90, 15):
        for lon in range(0, 360, 15):
            la, lo = math.radians(lat), math.radians(lon)
            nx = math.cos(la) * math.sin(lo)
            ny = -math.sin(la)
            nz = math.cos(la) * math.cos(lo)
            if nz <= 0.05:
                continue
            px, py = sx + sr * nx * 0.96, sy + sr * ny * 0.96
            shade = max(0.0, min(1.0, 0.55 * nz + 0.45 * (-nx * 0.5 - ny * 0.7)))
            v = int(60 + 180 * shade)
            fs = (3.4 * math.sqrt(nz)) * s
            dr.rectangle([px - fs, py - fs, px + fs, py + fs], fill=(v, v, v))
    # equatorial antenna band (the ring of little ports)
    for lon in range(0, 360, 10):
        lo = math.radians(lon)
        nx, nz = math.sin(lo), math.cos(lo)
        if nz <= 0.1:
            continue
        px, py = sx + sr * nx * 0.99, sy
        fs = 2.2 * math.sqrt(nz) * s
        dr.rectangle([px - fs, py - fs * 1.6, px + fs, py + fs * 1.6], fill=BLACK)
    # helical antenna spike on top
    dr.line([sx, sy - sr, sx, sy - sr - 12 * s], fill=WHITE, width=s)
    dr.ellipse([sx - 2 * s, sy - sr - 15 * s, sx + 2 * s, sy - sr - 11 * s],
               fill=WHITE)

    # signal beams: dashed red, up from Maine, down to Cornwall
    def dashed(p1, p2, dash=8 * s, gapf=0.45, width=2 * s, fill=RED):
        d = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        n = max(1, int(d / dash))
        for k in range(n):
            t0, t1 = k / n, (k + (1 - gapf)) / n
            dr.line([p1[0] + (p2[0] - p1[0]) * t0, p1[1] + (p2[1] - p1[1]) * t0,
                     p1[0] + (p2[0] - p1[0]) * t1, p1[1] + (p2[1] - p1[1]) * t1],
                    fill=fill, width=width)
    dashed(gs1, (sx - sr * 0.55, sy + sr * 0.65))
    dashed((sx + sr * 0.55, sy + sr * 0.65), gs2)
    # little red dots at the ground stations
    for gx, gy in (gs1, gs2):
        dr.ellipse([gx - 3 * s, gy - 3 * s, gx + 3 * s, gy + 3 * s], fill=RED)

    f_sm = font(FONT_SANS_B, 9 * s)
    dr.text((gs1[0] + 4 * s, gs1[1] + 8 * s), "ANDOVER,\nMAINE", font=f_sm,
            fill=BLACK, anchor="ma", align="center")
    dr.text((gs2[0] - 4 * s, gs2[1] + 8 * s), "GOONHILLY,\nCORNWALL", font=f_sm,
            fill=BLACK, anchor="ma", align="center")

    # title block
    f_t = font(FONT_SANS_B, 17 * s)
    f_c = font(FONT_SANS, 10 * s)
    dr.text((14 * s, 12 * s), "TELSTAR 1", font=f_t, fill=RED)
    dr.text((14 * s, 34 * s), "launched 10 July 1962", font=f_c, fill=WHITE)
    dr.text((W * s - 12 * s, 14 * s), "64\nyears\nago\ntoday", font=f_c,
            fill=WHITE, anchor="ra", align="right")
    dr.text((200 * s, 174 * s),
            "an 88 cm sphere that carried the first live TV picture across an ocean",
            font=f_c, fill=WHITE, anchor="ma")
    return finalize(img)


# --------------------------------------- 4. Before dawn: Moon, Pleiades, Mars
def image4_dawn_sky():
    """Tomorrow before dawn (Jul 11) the waning crescent moon slips past the
    Pleiades, with Mars and Aldebaran below — look east."""
    rng = random.Random(20260711)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # faint background stars
    for _ in range(170):
        x, y = rng.uniform(0, W * s), rng.uniform(0, 250 * s)
        v = rng.randint(90, 200)
        r = rng.uniform(0.4, 1.2) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    def star(x, y, r, v=255):
        x, y, r = x * s, y * s, r * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # Pleiades — the little dipper shape, upper middle
    plx, ply, sc = 218, 74, 34
    cluster = [("Alcyone", 0.00, 0.00, 2.6), ("Atlas", 0.30, 0.06, 2.2),
               ("Pleione", 0.33, -0.06, 1.6), ("Merope", -0.10, 0.16, 2.0),
               ("Electra", -0.30, 0.06, 2.0), ("Maia", -0.22, -0.14, 2.0),
               ("Taygeta", -0.36, -0.18, 1.7), ("Celaeno", -0.30, -0.06, 1.3)]
    for _, dx, dy, r in cluster:
        star(plx + dx * sc, ply + dy * sc, r)
    # faint nebulosity haze
    for _ in range(90):
        x = rng.gauss(plx, 0.24 * sc) * s
        y = rng.gauss(ply, 0.16 * sc) * s
        rr = rng.uniform(0.8, 2.0) * s
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(70, 70, 70))

    # the waning crescent moon, just past the cluster (28-day-old moon,
    # lit on the lower-left toward the coming sun)
    mx, my, mr = 128 * s, 96 * s, 30 * s
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(38, 38, 38))
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=(90, 90, 90),
               width=s)
    # crescent: difference of two discs, offset toward upper-right
    crescent = Image.new("L", (2 * mr + 2 * s, 2 * mr + 2 * s), 0)
    cd = ImageDraw.Draw(crescent)
    cd.ellipse([s, s, 2 * mr + s, 2 * mr + s], fill=255)
    off = 0.62 * mr
    cd.ellipse([s + off * 0.707, s - off * 0.707,
                2 * mr + s + off * 0.707, 2 * mr + s - off * 0.707], fill=0)
    img.paste((232, 232, 232), (int(mx - mr - s), int(my - mr - s)), crescent)

    # Hyades V with Aldebaran, lower right; Mars nearby in red
    hyx, hyy, hsc = 300, 176, 52
    hyades = [(0.00, 0.00), (-0.30, -0.18), (-0.52, -0.30),  # lower arm
              (-0.28, 0.10), (-0.55, 0.16), (-0.72, 0.22)]   # upper arm
    pts = [(hyx + dx * hsc, hyy + dy * hsc) for dx, dy in hyades]
    for i, j in [(0, 1), (1, 2), (0, 3), (3, 4), (4, 5)]:
        dr.line([pts[i][0] * s, pts[i][1] * s, pts[j][0] * s, pts[j][1] * s],
                fill=(80, 80, 80), width=s)
    for k, (px, py) in enumerate(pts):
        star(px, py, 2.0 if k else 3.4)
    # Mars — red wanderer between the clusters
    mrx, mry = 252, 140
    dr.ellipse([(mrx - 3.2) * s, (mry - 3.2) * s, (mrx + 3.2) * s,
                (mry + 3.2) * s], fill=RED)

    # labels
    f_l = font(FONT_SANS_B, 10 * s)
    f_s = font(FONT_SANS, 9 * s)
    dr.text((plx * s, (ply - 22) * s), "PLEIADES", font=f_l, fill=WHITE,
            anchor="mb")
    dr.text((mx, my + mr + 8 * s), "old moon, 14%", font=f_s, fill=WHITE,
            anchor="ma")
    dr.text(((mrx + 10) * s, (mry - 4) * s), "MARS", font=f_l, fill=RED)
    dr.text(((hyx + 10) * s, (hyy + 2) * s), "Aldebaran", font=f_s, fill=WHITE)

    # horizon: black treeline over a faint twilight glow band
    glow_top = 252
    for yy in range(glow_top, 272):
        t = (yy - glow_top) / 20
        v = int(30 + 120 * t)
        dr.line([0, yy * s, W * s, yy * s], fill=(v, v, v), width=s)
    ground = []
    for px in range(0, W + 1, 4):
        yv = 268 + 6 * math.sin(px / 31.0) + 3 * math.sin(px / 7.3)
        ground.append((px * s, yv * s))
    dr.polygon(ground + [(W * s, H * s), (0, H * s)], fill=BLACK)
    for tx, th in [(46, 26), (58, 18), (330, 30), (344, 20), (360, 12)]:
        base = 268 + 6 * math.sin(tx / 31.0)
        dr.line([tx * s, base * s, tx * s, (base - th) * s], fill=BLACK,
                width=2 * s)
        for fy in range(3):
            wdt = (th * 0.55) * (1 - fy / 3)
            yy = base - th * (0.45 + 0.55 * fy / 3)
            dr.line([(tx - wdt) * s, (yy + wdt * 0.7) * s, tx * s, yy * s],
                    fill=BLACK, width=2 * s)
            dr.line([tx * s, yy * s, (tx + wdt) * s, (yy + wdt * 0.7) * s],
                    fill=BLACK, width=2 * s)

    # title
    f_t = font(FONT_SERIF_B, 15 * s)
    dr.text((14 * s, 10 * s), "BEFORE DAWN", font=f_t, fill=RED)
    dr.text((14 * s, 30 * s), "July 11 — look east around 4 am", font=f_s,
            fill=WHITE)
    dr.text((W * s - 12 * s, (H - 16) * s),
            "the old moon slips past the Pleiades; Mars waits below", font=f_s,
            fill=WHITE, anchor="rs")
    return finalize(img)


# ------------------------------------------------------------ 5. 134 °F
def image5_furnace_creek():
    """10 July 1913, Furnace Creek, Death Valley: 134 °F — still the hottest
    air temperature ever measured on Earth."""
    rng = random.Random(1913)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # huge red sun, slightly off-center, with heat-ripple arcs beneath it
    sunx, suny, sunr = 312 * s, 76 * s, 46 * s
    dr.ellipse([sunx - sunr, suny - sunr, sunx + sunr, suny + sunr], fill=RED)
    for k in range(1, 4):
        rr = sunr + k * 10 * s
        dr.arc([sunx - rr, suny - rr, sunx + rr, suny + rr], 35, 145,
               fill=RED, width=s)

    # heat shimmer: thin wavy vertical strands rising over the dunes
    # (kept clear of the thermometer and the big number)
    for wx in range(66, 400, 24):
        if 96 < wx < 262:
            continue
        pts = []
        for wy in range(150, 208, 3):
            xx = wx + 2.6 * math.sin(wy / 6.5 + wx)
            pts.append((xx * s, wy * s))
        dr.line(pts, fill=(170, 170, 170), width=s)

    # dunes: layered crescents, light with black shadow crests
    def dune(cx, base, wdt, hgt, v):
        pts = []
        for px in range(int(cx - wdt), int(cx + wdt) + 1, 2):
            t = (px - cx) / wdt
            yy = base - hgt * (1 - t * t) ** 1.5 if abs(t) <= 1 else base
            pts.append((px * s, yy * s))
        dr.polygon(pts + [((cx + wdt) * s, H * s), ((cx - wdt) * s, H * s)],
                   fill=(v, v, v))
        # slip-face shadow on the right flank
        shadow = [(px, yy) for px, yy in pts if px >= cx * s]
        dr.polygon(shadow + [((cx + wdt) * s, base * s)], fill=(v - 55,) * 3)
        dr.line(pts, fill=(max(0, v - 90),) * 3, width=s)

    dune(90, 262, 150, 46, 235)
    dune(320, 268, 170, 54, 220)
    dune(190, 292, 200, 60, 200)
    dr.rectangle([0, 288 * s, W * s, H * s], fill=(200, 200, 200))

    # thermometer, left side, red column pinned at the very top of its scale
    tx, ty0, ty1 = 40, 42, 218
    dr.rounded_rectangle([(tx - 7) * s, ty0 * s, (tx + 7) * s, ty1 * s],
                         radius=7 * s, fill=WHITE, outline=BLACK, width=2 * s)
    dr.ellipse([(tx - 13) * s, (ty1 - 4) * s, (tx + 13) * s, (ty1 + 22) * s],
               fill=RED, outline=BLACK, width=2 * s)
    dr.rectangle([(tx - 3.5) * s, (ty0 + 8) * s, (tx + 3.5) * s, (ty1 + 2) * s],
                 fill=RED)
    f_tick = font(FONT_SANS, 8 * s)
    for i, deg in enumerate(range(130, 80, -10)):
        yy = ty0 + 14 + i * (ty1 - ty0 - 40) / 4
        dr.line([(tx + 7) * s, yy * s, (tx + 13) * s, yy * s], fill=BLACK,
                width=s)
        dr.text(((tx + 17) * s, yy * s), str(deg), font=f_tick, fill=BLACK,
                anchor="lm")

    # the number
    f_huge = font(FONT_SANS_B, 58 * s)
    f_deg = font(FONT_SANS_B, 22 * s)
    f_sm = font(FONT_SANS, 10 * s)
    f_smb = font(FONT_SANS_B, 11 * s)
    dr.text((104 * s, 112 * s), "134", font=f_huge, fill=BLACK)
    dr.text((236 * s, 122 * s), "°F", font=f_deg, fill=RED)
    dr.text((108 * s, 178 * s), "56.7 °C in the shade", font=f_smb, fill=BLACK)

    # caption
    dr.text((14 * s, 12 * s), "FURNACE CREEK, DEATH VALLEY", font=f_smb,
            fill=BLACK)
    dr.text((14 * s, 27 * s), "10 July 1913", font=f_sm, fill=RED)
    # white plate behind the caption so it reads over the dithered sand
    cap = "still the hottest air ever measured on Earth — 113 years today"
    bb = dr.textbbox((W * s - 10 * s, (H - 12) * s), cap, font=f_sm, anchor="rs")
    dr.rectangle([bb[0] - 6 * s, bb[1] - 4 * s, bb[2] + 6 * s, bb[3] + 4 * s],
                 fill=WHITE)
    dr.text((W * s - 10 * s, (H - 12) * s), cap, font=f_sm, fill=BLACK,
            anchor="rs")
    return finalize(img)


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_tesla_constructivist, image2_polyphase, image3_telstar,
              image4_dawn_sky, image5_furnace_creek]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", cols)
