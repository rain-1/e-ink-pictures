#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-15.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

Today's set:
  1. Luna-16          — constructivist poster (the red wedge and the black moon)
  2. Wall Drawing     — an instruction, executed (after Sol LeWitt)
  3. Multi-scale Truchet — Carlson's winged tiles, one river dyed red
  4. Analemma         — the sun's figure-eight, with today marked
  5. Carapace         — a tortoise shell grown from a Voronoi field
                        (HMS Beagle reached the Galápagos on 15 IX 1835)

Rendering rules that work on this panel: geometric pieces are drawn at 3x
and snapped to the palette WITHOUT dithering (clean edges, no speckle);
only genuinely tonal passages get Floyd-Steinberg.
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
FONT_SERIF_I = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED)
    palette += [0, 0, 0] * (256 - 3)
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=False):
    """Downscale (if supersampled) and quantize to the exact 3-color palette."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def down(img):
    """Supersampled RGB -> 1x RGB, snapped to the palette (no dither)."""
    return finalize(img).convert("RGB")


def label(img, xy, text, fnt, fill, anchor="la", thresh=120):
    """Crisp small text drawn at 1x: render antialiased, threshold, stamp in one colour.
    Small type survives the 3-colour panel much better this way than via downscaling."""
    layer = Image.new("L", img.size, 0)
    ImageDraw.Draw(layer).text(xy, text, font=fnt, fill=255, anchor=anchor)
    mask = layer.point(lambda v: 255 if v >= thresh else 0)
    img.paste(fill, mask=mask)


def rotated_text(base, xy, text, fnt, fill, angle, anchor="mm"):
    """Draw text rotated by `angle` degrees (CCW) centred at xy on an RGB image."""
    bbox = fnt.getbbox(text)
    tw, th = bbox[2] - bbox[0] + 8, bbox[3] - bbox[1] + 8
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((4 - bbox[0], 4 - bbox[1]), text, font=fnt, fill=fill)
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.paste(layer, (int(xy[0] - layer.width / 2), int(xy[1] - layer.height / 2)), layer)


# ------------------------------------------------------------------ 1. Luna-16
def image1_luna16():
    """Red wedge, black moon. Luna-16 launched 12 IX 1970; on 15 IX it was three
    days out, falling toward Mare Fecunditatis (landed 20 IX, home 24 IX with
    101 g of the Moon — the first robotic sample return)."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    def P(x, y):
        return (x * s, y * s)

    # the black moon
    mx, my, mr = 278, 160, 96
    dr.ellipse([P(mx - mr, my - mr), P(mx + mr, my + mr)], fill=BLACK)

    # thin black construction lines (orbit geometry)
    dr.line([P(-10, 290), P(410, 40)], fill=BLACK, width=s)          # trajectory axis
    dr.line([P(120, -10), P(330, 310)], fill=BLACK, width=s)          # crossing rule
    dr.ellipse([P(mx - 150, my - 150), P(mx + 150, my + 150)], outline=BLACK, width=s)

    # the red wedge: from off-canvas lower-left to the landing site
    apex = (293, 160)
    wedge = [P(-40, 230), P(-40, 330), P(*apex)]
    dr.polygon(wedge, fill=RED)

    # landing site: Mare Fecunditatis, a white disc the wedge just touches
    lx, ly, lr = 302, 160, 10
    dr.ellipse([P(lx - lr, ly - lr), P(lx + lr, ly + lr)], fill=WHITE)
    dr.ellipse([P(lx - 3, ly - 3), P(lx + 3, ly + 3)], fill=RED)

    # projectiles: small floating rectangles
    for (x, y, w, h, c) in [(352, 22, 14, 14, BLACK), (372, 30, 6, 6, RED),
                            (60, 178, 22, 5, BLACK), (100, 196, 5, 5, RED),
                            (20, 150, 4, 4, RED), (130, 150, 3, 20, BLACK)]:
        dr.rectangle([P(x, y), P(x + w, y + h)], fill=c)

    # typography
    f_big = font(FONT_SANS_B, 46 * s)
    f_num = font(FONT_SANS_B, 46 * s)
    dr.text(P(14, 10), "ЛУНА", font=f_big, fill=BLACK)
    tw = dr.textlength("ЛУНА", font=f_big) / s
    dr.text(P(14 + tw + 8, 10), "16", font=f_num, fill=RED)
    dr.rectangle([P(16, 66), P(150, 69)], fill=BLACK)

    rotated_text(img, P(150, 212), "К ЛУНЕ", font(FONT_SANS_B, 13 * s), WHITE, 16.4)
    # white panels behind the text blocks (the orbit passes behind them)
    dr.rectangle([P(12, 74), P(178, 152)], fill=WHITE)
    dr.rectangle([P(120, 270), P(392, 296)], fill=WHITE)

    out = down(img)
    f_sm = font(FONT_SANS, 9)
    f_smb = font(FONT_SANS_B, 9)
    lines = [("12 IX", "launched from Baikonur"),
             ("15 IX", "three days out — today"),
             ("20 IX", "landed, Mare Fecunditatis"),
             ("24 IX", "home with 101 g of Moon")]
    y = 78
    for d, t in lines:
        label(out, (16, y), d, f_smb, RED if "15" in d else BLACK)
        label(out, (52, y), t, f_sm, BLACK)
        y += 14
    label(out, (16, 138), "1970", f_smb, BLACK)

    f_cap = font(FONT_SANS, 9)
    label(out, (W - 12, H - 26), "the first machine to bring a piece of another world home",
          f_cap, BLACK, anchor="ra")
    label(out, (W - 12, H - 13), "tonight the young crescent hangs between Venus and Antares, low in the west",
          f_cap, BLACK, anchor="ra")
    return finalize(out)


# ------------------------------------------------------------ 2. Wall Drawing
def image2_wall_drawing():
    """After Sol LeWitt: the instruction is the work; the machine is the draughtsman."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    margin, gap = 12, 6
    cols, rows = 4, 3
    text_h = 62
    pw = (W - 2 * margin - (cols - 1) * gap) // cols
    ph = (H - margin - text_h - (rows - 1) * gap) // rows
    V, Hh, D1, D2 = "V", "H", "D1", "D2"
    combos = [(V,), (Hh,), (D1,), (D2,),
              (V, Hh), (V, D1), (V, D2), (Hh, D1), (Hh, D2), (D1, D2),
              (V, Hh, D1), (Hh, D1, D2)]
    spacing = 5

    def draw_part(part, dirs):
        d = ImageDraw.Draw(part)
        w, h = part.size
        for k in dirs:
            colr = RED if k in (D1, D2) else BLACK
            if k == V:
                for x in range(spacing // 2, w, spacing):
                    d.line([x, 0, x, h], fill=colr)
            elif k == Hh:
                for y in range(spacing // 2, h, spacing):
                    d.line([0, y, w, y], fill=colr)
            elif k == D1:  # rising to the right
                step = int(round(spacing * math.sqrt(2)))
                for c in range(-h, w + h, step):
                    d.line([c, h, c + h, 0], fill=colr)
            else:          # falling to the right
                step = int(round(spacing * math.sqrt(2)))
                for c in range(-h, w + h, step):
                    d.line([c, 0, c + h, h], fill=colr)

    idx = 0
    for r in range(rows):
        for c in range(cols):
            x0 = margin + c * (pw + gap)
            y0 = margin + r * (ph + gap)
            part = Image.new("RGB", (pw - 2, ph - 2), WHITE)
            draw_part(part, combos[idx])
            img.paste(part, (x0 + 1, y0 + 1))
            dr.rectangle([x0, y0, x0 + pw - 1, y0 + ph - 1], outline=BLACK)
            idx += 1

    f_t = font(FONT_SANS_B, 10)
    f_i = font(FONT_SERIF_I, 11)
    f_s = font(FONT_SANS, 9)
    ty = H - text_h + 8
    label(img, (margin, ty), "WALL DRAWING", f_t, BLACK)
    label(img, (margin + 92, ty), "A wall divided into twelve equal parts. In each part, one-, two- or",
          f_i, BLACK, thresh=110)
    label(img, (margin, ty + 14), "three-part combinations of straight lines in four directions, five pixels",
          f_i, BLACK, thresh=110)
    label(img, (margin, ty + 28), "apart: vertical and horizontal in black, diagonal in red.",
          f_i, BLACK, thresh=110)
    label(img, (W - margin, ty + 43), "after Sol LeWitt · executed by a machine · 15 IX 2026",
          f_s, RED, anchor="ra")
    return finalize(img)


# ------------------------------------------------------ 3. Multi-scale Truchet
def image3_truchet():
    """Christopher Carlson's multi-scale Truchet tiles (Bridges 2018). Winged tiles:
    arcs of radius 2/3 from two opposite corners, corner discs of radius 1/3 in the
    background colour, edge discs of radius 1/6 in the foreground; each halving
    inverts the colours. Afterwards one connected black domain is flood-filled red."""
    rng = random.Random(20260915)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    base = 100
    tiles = []  # (level, cx, cy, w, motif)

    def subdivide(level, cx, cy, w):
        p_split = [0.75, 0.6, 0.5, 0.0][level]
        if w > 25 and rng.random() < p_split:
            q = w / 4
            for dx in (-q, q):
                for dy in (-q, q):
                    subdivide(level + 1, cx + dx, cy + dy, w / 2)
        else:
            tiles.append((level, cx, cy, w, rng.randint(0, 1)))

    for i in range(4):
        for j in range(3):
            subdivide(0, base * i + base / 2, base * j + base / 2, base)
    tiles.sort(key=lambda t: t[0])

    def disc(cx, cy, r, fill):
        dr.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=fill)

    def pie(cx, cy, r, a0, a1, fill):
        dr.pieslice([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], a0, a1, fill=fill)

    for level, cx, cy, w, motif in tiles:
        fg, bg = (BLACK, WHITE) if level % 2 == 0 else (WHITE, BLACK)
        h = w / 2
        dr.rectangle([(cx - h) * s, (cy - h) * s, (cx + h) * s, (cy + h) * s], fill=bg)
        R = 2 * w / 3
        if motif == 0:   # "\"
            pie(cx + h, cy - h, R, 90, 180, fg)
            pie(cx - h, cy + h, R, 270, 360, fg)
        else:            # "/"
            pie(cx - h, cy - h, R, 0, 90, fg)
            pie(cx + h, cy + h, R, 180, 270, fg)
        for dx in (-h, h):
            for dy in (-h, h):
                disc(cx + dx, cy + dy, w / 3, bg)
        for dx, dy in ((0, -h), (h, 0), (0, h), (-h, 0)):
            disc(cx + dx, cy + dy, w / 6, fg)

    out = finalize(img).convert("RGB")
    # dye a few black domains red
    rng2 = random.Random(915)
    px = out.load()
    dyed = 0
    tries = 0
    while dyed < 3 and tries < 4000:
        tries += 1
        x, y = rng2.randrange(W), rng2.randrange(H)
        if px[x, y] != BLACK:
            continue
        before = np.array(out)
        ImageDraw.floodfill(out, (x, y), RED)
        after = np.array(out)
        changed = int(((before != after).any(axis=2)).sum())
        if changed < 1500 or changed > 30000:
            # undo: too small or too big
            out = Image.fromarray(before)
            px = out.load()
            continue
        px = out.load()
        dyed += 1

    dr2 = ImageDraw.Draw(out)
    f = font(FONT_SANS, 9)
    fb = font(FONT_SANS_B, 9)
    t1 = "MULTI-SCALE TRUCHET"
    t2 = "winged tiles halving into one another; three domains dyed red"
    bw = int(dr2.textlength(t2, font=f)) + 16
    dr2.rectangle([6, H - 34, 6 + bw, H - 6], fill=WHITE, outline=BLACK)
    label(out, (14, H - 30), t1, fb, BLACK)
    label(out, (14 + int(dr2.textlength(t1, font=fb)) + 8, H - 30), "15 · 09", fb, RED)
    label(out, (14, H - 18), t2, f, BLACK)
    return finalize(out)


# ------------------------------------------------------------- 4. Analemma
def sun_params(day_of_year, hour=12.0):
    """NOAA low-precision solar position: returns (equation of time [min], declination [deg])."""
    g = 2 * math.pi / 365 * (day_of_year - 1 + (hour - 12) / 24)
    eot = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                    - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    dec = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g)
           - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g)
           - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    return eot, math.degrees(dec)


def image4_analemma():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # chart frame: x = equation of time (min), y = declination (deg)
    x0, x1 = 150, 290        # px for -18 .. +18 min
    y0, y1 = 30, 262         # px for +25 .. -25 deg

    def P(eot, dec):
        return ((x0 + (eot + 18) / 36 * (x1 - x0)) * s,
                (y0 + (25 - dec) / 50 * (y1 - y0)) * s)

    # axes
    ax_x = P(0, 0)[0]
    ax_y = P(0, 0)[1]
    dr.line([ax_x, y0 * s, ax_x, y1 * s], fill=BLACK, width=s)
    dr.line([x0 * s - 20 * s, ax_y, x1 * s + 20 * s, ax_y], fill=BLACK, width=s)
    for m in (-15, -10, -5, 5, 10, 15):
        x = P(m, 0)[0]
        dr.line([x, ax_y - 3 * s, x, ax_y + 3 * s], fill=BLACK, width=s)
    for d in (-20, -10, 10, 20):
        y = P(0, d)[1]
        dr.line([ax_x - 3 * s, y, ax_x + 3 * s, y], fill=BLACK, width=s)
    # solstice guides
    for d in (23.44, -23.44):
        y = P(0, d)[1]
        for xx in range(x0 * s - 20 * s, x1 * s + 20 * s, 6 * s):
            dr.line([xx, y, xx + 3 * s, y], fill=BLACK, width=s)

    # the curve: one dot every third day
    pts = [sun_params(n) for n in range(1, 366)]
    for i in range(365):
        e, d = pts[i]
        e2, d2 = pts[(i + 1) % 365]
        dr.line([P(e, d), P(e2, d2)], fill=BLACK, width=s)
    for i in range(0, 365, 3):
        e, d = pts[i]
        x, y = P(e, d)
        dr.ellipse([x - 1.6 * s, y - 1.6 * s, x + 1.6 * s, y + 1.6 * s], fill=BLACK)

    months = [("JAN", 1), ("FEB", 32), ("MAR", 60), ("APR", 91), ("MAY", 121), ("JUN", 152),
              ("JUL", 182), ("AUG", 213), ("SEP", 244), ("OCT", 274), ("NOV", 305), ("DEC", 335)]
    for name, n in months:
        e, d = sun_params(n)
        x, y = P(e, d)
        dr.ellipse([x - 2.6 * s, y - 2.6 * s, x + 2.6 * s, y + 2.6 * s], fill=WHITE, outline=BLACK, width=s)

    # today, and the equinox a week away
    today_n = 258  # 15 September 2026
    e, d = sun_params(today_n)
    tx, ty = P(e, d)
    dr.ellipse([tx - 5 * s, ty - 5 * s, tx + 5 * s, ty + 5 * s], fill=RED)
    dr.line([tx + 6 * s, ty - 3 * s, tx + 44 * s, ty - 30 * s], fill=RED, width=s)
    e2, d2 = sun_params(265)
    ex, ey = P(e2, d2)
    dr.ellipse([ex - 3 * s, ey - 3 * s, ex + 3 * s, ey + 3 * s], fill=WHITE, outline=RED, width=s)

    out = down(img)
    f_tick = font(FONT_SANS, 8)
    f_m = font(FONT_SANS_B, 8)
    for m in (-15, -10):
        x = P(m, 0)[0] / s
        label(out, (x, ax_y / s + 5), f"{m:+d}", f_tick, BLACK, anchor="ma")
    for m in (10, 15):
        x = P(m, 0)[0] / s
        label(out, (x, ax_y / s - 5), f"{m:+d}", f_tick, BLACK, anchor="md")
    for dd in (-20, -10, 10, 20):
        y = P(0, dd)[1] / s
        label(out, (ax_x / s - 5, y), f"{dd:+d}°", f_tick, BLACK, anchor="rm")
    offsets = {"JAN": (-6, 9), "FEB": (-10, 0), "MAR": (-10, 0), "APR": (-11, -2), "MAY": (-11, 0),
               "JUN": (-11, -4), "JUL": (8, -4), "AUG": (9, 0), "SEP": (9, -1), "OCT": (11, 7),
               "NOV": (10, 2), "DEC": (9, -1)}
    for name, n in months:
        e_, d_ = sun_params(n)
        x, y = P(e_, d_)
        ox, oy = offsets[name]
        label(out, (x / s + ox, y / s + oy), name, f_m, BLACK, anchor="lm" if ox > 0 else "rm")
    label(out, (tx / s + 46, ty / s - 33), "TODAY, 15 Sep", font(FONT_SANS_B, 10), RED, anchor="lm")
    label(out, (tx / s + 46, ty / s - 22), "equinox (o) in a week", f_tick, RED, anchor="lm")

    # left column of text
    label(out, (14, 12), "ANALEMMA", font(FONT_SERIF_B, 17), BLACK)
    f_b = font(FONT_SANS, 9)
    body = [
        "Photograph the noon sun from",
        "the same window every few",
        "days for a year and it draws",
        "this figure of eight.",
        "",
        "Up and down: the Earth's tilt,",
        "±23.4° of declination.",
        "",
        "Side to side: the equation",
        "of time — an elliptical orbit",
        "puts a sundial up to 16 min",
        "fast or slow of the clock.",
        "",
        f"Today the sundial runs",
        f"{abs(e):.1f} min {'fast' if e > 0 else 'slow'}; the sun is {d:+.1f}°",
        "north and sinking 0.4° a day.",
    ]
    y = 40
    for i, line in enumerate(body):
        label(out, (14, y), line, f_b, RED if i >= len(body) - 3 else BLACK)
        y += 12 if line else 5
    label(out, (x0 - 20, y1 + 14), "sundial slow", f_tick, BLACK, anchor="la")
    label(out, (x1 + 20, y1 + 14), "sundial fast", f_tick, BLACK, anchor="ra")
    label(out, ((x0 + x1) / 2, y1 + 14), "minutes", f_tick, BLACK, anchor="ma")
    label(out, (x1 + 22, P(0, 23.44)[1] / s - 5), "June", f_tick, BLACK, anchor="lm")
    label(out, (x1 + 22, P(0, 23.44)[1] / s + 5), "solstice", f_tick, BLACK, anchor="lm")
    label(out, (x1 + 22, P(0, -23.44)[1] / s - 5), "December", f_tick, BLACK, anchor="lm")
    label(out, (x1 + 22, P(0, -23.44)[1] / s + 5), "solstice", f_tick, BLACK, anchor="lm")
    return finalize(out)


# ---------------------------------------------------------------- 5. Carapace
def image5_carapace():
    """A giant tortoise's shell from above, head to the left. Scutes are Voronoi cells;
    growth rings are level sets of the distance to the cell boundary, tighter
    toward the rim as growth slows. HMS Beagle reached the Galápagos 15 IX 1835."""
    rng = np.random.default_rng(1835)
    s = SS
    cx, cy = 190.0, 143.0     # shell centre (1x coords)
    a, b = 158.0, 112.0       # semi-axes

    centres = []
    # vertebral scutes along the spine
    for k in range(5):
        centres.append((cx + (k - 2) * 60.0, cy))
    # costal scutes, four each side
    for side in (-1, 1):
        for k in range(4):
            centres.append((cx + (k - 1.5) * 62.0, cy + side * 60.0))
    # marginal scutes around the rim
    n_m = 22
    for k in range(n_m):
        t = 2 * math.pi * (k + 0.5) / n_m
        centres.append((cx + 0.93 * a * math.cos(t), cy + 0.92 * b * math.sin(t)))
    # nuchal at the front, supracaudal at the back
    centres.append((cx - a * 0.86, cy))
    centres.append((cx + a * 0.86, cy))
    centres = np.array(centres) + rng.normal(0, 2.0, size=(len(centres), 2))

    ys, xs = np.mgrid[0:H * s, 0:W * s]
    X = xs / s
    Y = ys / s
    d = np.stack([np.hypot(X - px, Y - py) for px, py in centres])
    d.sort(axis=0)
    g = d[1] - d[0]          # 0 on cell borders, grows inward

    # gentle organic warp of the ring field
    warp = (np.sin(X / 9.0) * np.cos(Y / 7.0) + np.sin((X + Y) / 13.0)) * 0.9
    g = np.clip(g + warp, 0, None)
    # rings: tighter near the edge (small g), wider toward the areola
    f = np.sqrt(g / 22.0)
    ring = (f * 5.5) % 1.0 < 0.22
    border = g < 1.6
    inside = ((X - cx) / a) ** 2 + ((Y - cy) / b) ** 2 <= 1.0
    rim = (((X - cx) / a) ** 2 + ((Y - cy) / b) ** 2 > 0.965) & inside

    canvas = np.full((H * s, W * s, 3), 255, dtype=np.uint8)
    black = inside & (ring | border | rim)
    # areolae: the oldest, roughest centre of each scute, stippled
    areola = (g > 23.0) & ((X * 7919 + Y * 104729) % 3.0 < 0.3)
    black |= inside & areola
    canvas[black] = 0

    out = down(Image.fromarray(canvas))
    dr = ImageDraw.Draw(out)

    # specimen label
    lx, ly = 246, 256
    dr.rectangle([lx, ly, W - 10, H - 8], fill=WHITE, outline=RED)
    label(out, (lx + 6, ly + 5), "CHELONOIDIS", font(FONT_SANS_B, 10), RED)
    label(out, (lx + 6, ly + 19), "Galápagos  ·  15 IX 1835", font(FONT_SANS, 9), BLACK)
    label(out, (W - 15, ly + 6), "HMS Beagle", font(FONT_SERIF_I, 10), BLACK, anchor="ra", thresh=100)

    f_c = font(FONT_SANS, 9)
    label(out, (10, H - 38), "the day Darwin first met a tortoise", f_c, BLACK)
    label(out, (10, H - 26), "big enough to ride; its scutes grown", f_c, BLACK)
    label(out, (10, H - 14), "here as Voronoi cells with rings", f_c, BLACK)
    return finalize(out)


if __name__ == "__main__":
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_luna16, image2_wall_drawing, image3_truchet,
              image4_analemma, image5_carapace]
    only = os.environ.get("ONLY")
    for n, fn in enumerate(makers, 1):
        if only and str(n) not in only.split(","):
            continue
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        assert im.size == (W, H)
        print(path, "colors:", cols)
