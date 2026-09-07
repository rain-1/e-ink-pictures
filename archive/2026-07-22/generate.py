#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-22 (Pi Approximation Day, 22/7).

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Tonal scenes render at 3x then Floyd-Steinberg
dither into the exact palette; hard-edged geometric pieces render at 1x in
pure palette colors.

July 22 written 22/7 is Archimedes' fraction for pi (3.142857..., good to
~0.04%). Three of today's five lean into that; one is a Lissitzky homage
(the black/white/red palette IS constructivism); one is the late-July sky.
"""

import math
import random
from datetime import date
from PIL import Image, ImageDraw, ImageFont
import numpy as np

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
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"

TODAY = date(2026, 7, 22)


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


# --------------------------------------------------------------- 1. 22 / 7
def image1_twentytwo_sevenths():
    """Typographic hero: the fraction, a rolling wheel, the repeating decimal."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # header band
    dr.rectangle([0, 0, W * s, 30 * s], fill=RED)
    f_hd = font(FONT_SANS_B, 13 * s)
    dr.text((14 * s, 15 * s), "PI APPROXIMATION DAY", font=f_hd, fill=WHITE,
            anchor="lm")
    f_hdr = font(FONT_SANS, 11 * s)
    dr.text((W * s - 14 * s, 15 * s),
            TODAY.strftime("%A, %-d %B %Y"), font=f_hdr, fill=WHITE, anchor="rm")

    # giant fraction 22 / 7 on the left
    f_num = font(FONT_SERIF_B, 82 * s)
    fx = 96 * s
    dr.text((fx, 96 * s), "22", font=f_num, fill=BLACK, anchor="mm")
    dr.text((fx, 178 * s), "7", font=f_num, fill=BLACK, anchor="mm")
    # fraction bar
    dr.line([fx - 52 * s, 137 * s, fx + 52 * s, 137 * s], fill=RED,
            width=int(4.5 * s))

    # the rolling wheel on the right: diameter 7 -> circumference ~ 22
    wx, wy, wr = 300 * s, 118 * s, 62 * s
    dr.ellipse([wx - wr, wy - wr, wx + wr, wy + wr], outline=BLACK,
               width=int(2.5 * s))
    # hub + a few spokes
    dr.ellipse([wx - 4 * s, wy - 4 * s, wx + 4 * s, wy + 4 * s], fill=BLACK)
    for k in range(6):
        a = math.radians(60 * k + 12)
        dr.line([wx, wy, wx + wr * math.cos(a), wy + wr * math.sin(a)],
                fill=BLACK, width=s)
    # diameter marker "= 7"
    dr.line([wx - wr, wy, wx + wr, wy], fill=RED, width=int(2 * s))
    dr.text((wx, wy - 10 * s), "diameter 7", font=font(FONT_SANS, 9 * s),
            fill=BLACK, anchor="mb")
    # a red mark on the rim + ground line: "roll once -> ~22 across"
    gy = wy + wr + 12 * s
    dr.line([wx - wr - 6 * s, gy, wx + wr + 34 * s, gy], fill=BLACK, width=s)
    dr.ellipse([wx - wr - 3 * s, wy - 3 * s, wx - wr + 3 * s, wy + 3 * s],
               fill=RED)
    dr.text((wx, gy + 4 * s),
            "one turn ≈ 22 along the ground", font=font(FONT_SANS, 9 * s),
            fill=BLACK, anchor="mt")

    # repeating decimal with overline, near the bottom
    f_dec = font(FONT_MONO_B, 20 * s)
    base_x, base_y = 20 * s, 250 * s
    pre = "22 ÷ 7 = 3.142857"
    rep = "142857"
    dr.text((base_x, base_y), pre, font=f_dec, fill=BLACK, anchor="lm")
    # overline just above the repeating block "142857"
    x_pre = base_x + dr.textlength("22 ÷ 7 = 3.", font=f_dec)
    x_rep_end = x_pre + dr.textlength(rep, font=f_dec)
    dr.text((x_rep_end, base_y), "…", font=f_dec, fill=BLACK, anchor="lm")
    ay = base_y - 12 * s
    dr.line([x_pre, ay, x_rep_end, ay], fill=RED, width=int(2 * s))

    f_sm = font(FONT_SANS, 10 * s)
    dr.text((20 * s, 276 * s),
            "true π = 3.141592653…   —   22/7 overshoots by only 0.04%",
            font=f_sm, fill=BLACK, anchor="lm")
    return finalize(img)


# ---------------------------------------------------- 2. Archimedes' squeeze
def image2_archimedes():
    """Inscribed & circumscribed polygons trapping a circle: 223/71 < pi < 22/7."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    cx, cy, r = 150 * s, 158 * s, 104 * s
    n = 12  # polygon sides — few enough that the squeeze is visible

    def poly(radius, rot):
        return [(cx + radius * math.cos(2 * math.pi * k / n + rot),
                 cy + radius * math.sin(2 * math.pi * k / n + rot))
                for k in range(n)]

    # circumscribed polygon (outside the circle): vertices at r / cos(pi/n)
    out_r = r / math.cos(math.pi / n)
    dr.polygon(poly(out_r, math.pi / n), outline=BLACK, width=int(2 * s))
    # the circle itself, in red, sitting snugly between the two polygons
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=int(3 * s))
    # inscribed polygon (inside the circle): vertices on the circle
    dr.polygon(poly(r, 0), outline=BLACK, width=int(2 * s))
    # emphasise the vertices where inscribed polygon touches the circle
    for vx, vy in poly(r, 0):
        dr.ellipse([vx - 2.5 * s, vy - 2.5 * s, vx + 2.5 * s, vy + 2.5 * s],
                   fill=BLACK)

    # radius line + center dot
    dr.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s], fill=BLACK)
    ang = math.radians(-58)
    dr.line([cx, cy, cx + r * math.cos(ang), cy + r * math.sin(ang)],
            fill=BLACK, width=s)
    dr.text((cx + 0.5 * r * math.cos(ang) + 4 * s,
             cy + 0.5 * r * math.sin(ang) - 4 * s), "r",
            font=font(FONT_SERIF, 12 * s), fill=BLACK, anchor="lb")

    # right-hand text column
    tx = 288 * s
    dr.text((tx, 40 * s), "ARCHIMEDES’", font=font(FONT_SERIF_B, 15 * s),
            fill=RED, anchor="mm")
    dr.text((tx, 60 * s), "SQUEEZE", font=font(FONT_SERIF_B, 15 * s),
            fill=BLACK, anchor="mm")
    lines = [
        "Trap a circle between",
        "two polygons. The",
        "perimeters bound its",
        "circumference — so",
        "they bound π.",
        "",
        "With 96-gons, c.250 BCE,",
        "he proved:",
    ]
    y = 84 * s
    for ln in lines:
        dr.text((tx, y), ln, font=font(FONT_SANS, 10 * s), fill=BLACK,
                anchor="mm")
        y += 15 * s
    # the famous bound
    dr.text((tx, y + 6 * s), "223       22", font=font(FONT_MONO_B, 13 * s),
            fill=BLACK, anchor="mm")
    dr.text((tx, y + 22 * s), "─── < π < ──",
            font=font(FONT_MONO_B, 13 * s), fill=RED, anchor="mm")
    dr.text((tx, y + 38 * s), " 71        7", font=font(FONT_MONO_B, 13 * s),
            fill=BLACK, anchor="mm")
    dr.text((tx, y + 58 * s), "3.1408 <π< 3.1429",
            font=font(FONT_SANS, 9 * s), fill=BLACK, anchor="mm")

    dr.text((16 * s, 20 * s), "inscribed ≤ circle ≤ circumscribed",
            font=font(FONT_SANS, 10 * s), fill=BLACK, anchor="lm")
    return finalize(img)


# ------------------------------------------------------- 3. Monte Carlo pi
def image3_montecarlo():
    """Random darts in a square; those under the quarter circle -> pi/4."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # square plot on the left
    m = 26
    x0, y0 = m * s, 42 * s
    side = 226 * s
    x1, y1 = x0 + side, y0 + side
    dr.rectangle([x0, y0, x1, y1], outline=BLACK, width=int(1.5 * s))
    # quarter circle centred at bottom-left corner (x0, y1), radius = side
    dr.arc([x0 - side, y1 - side, x0 + side, y1 + side], -90, 0, fill=RED,
           width=int(2.5 * s))

    rng = random.Random(20260722)
    N = 3000
    inside = 0
    dots = []
    for _ in range(N):
        u, v = rng.random(), rng.random()
        in_circle = (u * u + v * v) <= 1.0
        if in_circle:
            inside += 1
        px = x0 + u * side
        py = y1 - v * side
        dots.append((px, py, in_circle))
    # draw outside dots first (black), then inside (red) so red reads on top
    for px, py, ic in dots:
        if not ic:
            dr.ellipse([px - 1.4 * s, py - 1.4 * s, px + 1.4 * s, py + 1.4 * s],
                       fill=BLACK)
    for px, py, ic in dots:
        if ic:
            dr.ellipse([px - 1.4 * s, py - 1.4 * s, px + 1.4 * s, py + 1.4 * s],
                       fill=RED)

    est = 4.0 * inside / N

    # header
    dr.text((m * s, 24 * s), "MONTE CARLO π", font=font(FONT_SANS_B, 14 * s),
            fill=BLACK, anchor="lm")

    # right column
    tx = 300 * s
    dr.text((tx, 60 * s), "Throw darts at a", font=font(FONT_SANS, 10 * s),
            fill=BLACK, anchor="mm")
    dr.text((tx, 74 * s), "square. Count how", font=font(FONT_SANS, 10 * s),
            fill=BLACK, anchor="mm")
    dr.text((tx, 88 * s), "many land under", font=font(FONT_SANS, 10 * s),
            fill=BLACK, anchor="mm")
    dr.text((tx, 102 * s), "the arc.", font=font(FONT_SANS, 10 * s),
            fill=BLACK, anchor="mm")

    dr.text((tx, 132 * s), "inside", font=font(FONT_SANS, 10 * s), fill=RED,
            anchor="mm")
    dr.text((tx, 148 * s), "π ≈ 4 × ─────",
            font=font(FONT_MONO, 12 * s), fill=BLACK, anchor="mm")
    dr.text((tx, 164 * s), "total", font=font(FONT_SANS, 10 * s), fill=BLACK,
            anchor="mm")

    dr.text((tx, 196 * s), f"{inside} / {N}", font=font(FONT_MONO_B, 13 * s),
            fill=BLACK, anchor="mm")
    dr.text((tx, 224 * s), "π ≈", font=font(FONT_SANS, 13 * s),
            fill=BLACK, anchor="mm")
    dr.text((tx, 246 * s), f"{est:.4f}", font=font(FONT_MONO_B, 22 * s),
            fill=RED, anchor="mm")
    dr.text((tx, 272 * s), f"{N} random darts", font=font(FONT_SANS, 9 * s),
            fill=BLACK, anchor="mm")
    return finalize(img)


# ---------------------------------------------------------- 4. Red Wedge
def image4_red_wedge():
    """Homage to El Lissitzky, 'Beat the Whites with the Red Wedge' (1919).
    Pure constructivist black/white/red geometry."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    def P(x, y):
        return (x * s, y * s)

    # a large black circle, right of centre, partly bled off the top
    ccx, ccy, cr = 250, 150, 118
    dr.ellipse([P(ccx - cr, ccy - cr)[0], P(ccx - cr, ccy - cr)[1],
                P(ccx + cr, ccy + cr)[0], P(ccx + cr, ccy + cr)[1]], fill=BLACK)
    # the white field itself is the "white" army the red wedge drives into;
    # leave the disk solid.

    # THE red wedge: a sharp triangle driving from the left into the circle
    wedge = [P(6, 74), P(292, 150), P(6, 226)]
    dr.polygon(wedge, fill=RED)

    # bold black bars (constructivist scaffolding)
    dr.rectangle([P(0, 262)[0], P(0, 262)[1], P(400, 276)[0], P(400, 276)[1]],
                 fill=BLACK)
    dr.line([P(70, 20), P(70, 262)], fill=BLACK, width=int(3 * s))
    # a red bar shooting off to the top-right
    dr.polygon([P(300, 8), P(392, 8), P(392, 22), P(300, 40)], fill=RED)

    # scatter of small hard shapes (black squares + a red dot) for rhythm
    for (bx, by, bs) in [(96, 250, 9), (120, 258, 6), (150, 252, 12),
                         (350, 250, 10)]:
        dr.rectangle([P(bx, by)[0], P(bx, by)[1],
                      P(bx + bs, by + bs)[0], P(bx + bs, by + bs)[1]],
                     fill=BLACK)
    dr.ellipse([P(44, 44)[0], P(44, 44)[1], P(60, 60)[0], P(60, 60)[1]],
               fill=RED)
    # a thin diagonal red line, dynamic
    dr.line([P(20, 250), P(240, 60)], fill=RED, width=int(2 * s))

    # tiny homage caption sitting inside the black bottom bar (white on black)
    dr.text(P(8, 269), "after El Lissitzky · Beat the Whites with the "
            "Red Wedge · 1919", font=font(FONT_SANS, 8 * s), fill=WHITE,
            anchor="lm")
    return finalize(img, dither=False)


# ------------------------------------------------------- 5. Late July sky
def moon_array(size, illum, waxing=True):
    """Return an (size,size,3) uint8 RGB array of a moon, lit fraction `illum`.
    Waxing -> lit on the right. Uses a row-scan terminator (numpy)."""
    n = size
    yy, xx = np.mgrid[0:n, 0:n]
    cx = cy = (n - 1) / 2.0
    r = n / 2.0 - 1
    x = (xx - cx) / r
    y = (yy - cy) / r
    disk = (x * x + y * y) <= 1.0
    halfw = np.sqrt(np.clip(1.0 - y * y, 0.0, 1.0))
    t = 1.0 - 2.0 * illum  # terminator position factor in [-1,1]
    if waxing:
        lit = disk & (x >= t * halfw)
    else:
        lit = disk & (x <= -t * halfw)

    arr = np.zeros((n, n, 3), dtype=np.uint8)
    arr[disk] = (18, 18, 18)          # dark side, near black
    arr[lit] = (232, 232, 232)        # lit side, light gray (will dither)
    # subtle maria: darker gray blotches only on the lit part
    rng = np.random.default_rng(722)
    for _ in range(40):
        mx = rng.uniform(0.15, 0.95)
        my = rng.uniform(-0.8, 0.8)
        mr = rng.uniform(0.05, 0.16)
        blob = ((x - mx) ** 2 + (y - my) ** 2) <= mr ** 2
        sel = blob & lit
        shade = int(rng.integers(150, 200))
        arr[sel] = (shade, shade, shade)
    return arr


def image5_sky():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # header
    dr.text((16 * s, 16 * s), "LATE JULY SKY", font=font(FONT_SERIF_B, 20 * s),
            fill=RED, anchor="lm")
    dr.text((16 * s, 38 * s), "Wed Jul 22, 2026 — waxing gibbous, ~57% lit",
            font=font(FONT_SANS, 11 * s), fill=BLACK, anchor="lm")
    dr.line([16 * s, 52 * s, (W - 16) * s, 52 * s], fill=BLACK, width=s)

    # moon: waxing gibbous ~57%, lit on the right
    msz = 150
    marr = moon_array(msz * s, illum=0.57, waxing=True)
    moon = Image.fromarray(marr, "RGB")
    mx, my = 96, 168  # centre in 1x coords
    img.paste(moon, ((mx - msz // 2) * s, (my - msz // 2) * s))
    # crisp rim
    mr = msz // 2 - 1
    dr.ellipse([(mx - mr) * s, (my - mr) * s, (mx + mr) * s, (my + mr) * s],
               outline=BLACK, width=s)
    dr.text((mx * s, (my + msz // 2 + 8) * s),
            "toward the Full Buck Moon, Jul 29", font=font(FONT_SANS, 9 * s),
            fill=BLACK, anchor="mt")

    # events column on the right
    cx0 = 196
    dr.text((cx0 * s, 74 * s), "COMING NIGHTS", font=font(FONT_SANS_B, 11 * s),
            fill=BLACK, anchor="lm")
    events = [
        ("JUL 28", "δ Aquariids peak"),
        ("", "(moonlight drowns most)"),
        ("JUL 29", "FULL BUCK MOON"),
        ("JUL 30", "α Capricornid"),
        ("", "fireballs — few but bright"),
        ("DAWN", "Mars, Saturn,"),
        ("E sky", "Neptune, Uranus lined up"),
    ]
    y = 96
    for tag, txt in events:
        if tag:
            dr.text((cx0 * s, y * s), tag, font=font(FONT_SANS_B, 10 * s),
                    fill=RED, anchor="lm")
        dr.text(((cx0 + 52) * s, y * s), txt, font=font(FONT_SANS, 10 * s),
                fill=BLACK, anchor="lm")
        y += 20
    dr.line([cx0 * s, (y + 2) * s, (W - 16) * s, (y + 2) * s], fill=BLACK,
            width=s)
    dr.text((cx0 * s, (y + 12) * s),
            "The Milky Way's core rides\nhighest around midnight now.",
            font=font(FONT_SANS, 9 * s), fill=BLACK, anchor="lm")
    dr.rectangle([8 * s, 6 * s, (W - 8) * s, (H - 6) * s], outline=BLACK,
                 width=s)
    return finalize(img)


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_twentytwo_sevenths, image2_archimedes, image3_montecarlo,
              image4_red_wedge, image5_sky]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", sorted(cols))
