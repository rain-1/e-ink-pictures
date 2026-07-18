#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-18.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Tonal scenes render at 3x, LANCZOS downscale,
then Floyd-Steinberg dither into the exact palette; hard-edged geometric
pieces render at 1x in pure palette colors.

Today's set:
  1. PROUN         — a constructivist composition, after El Lissitzky's
                     "Beat the Whites with the Red Wedge" (1919). The panel's
                     black/white/red palette *is* that movement.
  2. Waxing Moon   — tonight's actual sky: a 20% waxing crescent, 4 days old,
                     low in the west after sunset, plus the week's events.
  3. Seigaiha      — the Japanese "blue ocean wave" scale pattern, generated
                     from overlapping concentric arcs, recolored for 3 inks.
  4. One Point Oh  — 50 years ago today (18 Jul 1976) Nadia Comaneci scored
                     the first perfect 10; the scoreboard couldn't show it and
                     read "1.00". A seven-segment homage.
  5. Truchet       — a multiscale Truchet tiling: one of two arc tiles per
                     cell, recursively subdivided, weaving an endless labyrinth.
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
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


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


# --------------------------------------------------------------------- 1. PROUN
def image1_proun():
    """Constructivist composition after Lissitzky — hard edges, pure palette."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # A black angular ground thrusting up from the lower right — the field the
    # red wedge drives across. Dynamic diagonal, not a horizon.
    dr.polygon([(400, 300), (400, 96), (150, 300)], fill=BLACK)

    # The white circle (the thing to be pierced), sitting on the black ground.
    ccx, ccy, cr = 292, 150, 62
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=WHITE)
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=BLACK, width=2)

    # Thin black construction lines with node dots — Lissitzky's draughtsman lines.
    nodes = [(20, 120), (392, 40), (60, 260), (360, 250), (150, 20)]
    lines = [(0, 1), (2, 3), (4, 3), (0, 3)]
    for a, b in lines:
        dr.line([nodes[a], nodes[b]], fill=BLACK, width=1)
    for (nx, ny) in nodes:
        dr.ellipse([nx - 3, ny - 3, nx + 3, ny + 3], fill=BLACK)

    # THE red wedge: a long triangle driving from the left, apex inside the circle.
    apex = (ccx + 6, ccy)
    dr.polygon([(36, 78), (36, 244), apex], fill=RED)
    # a small counter-wedge (black) balancing the pull, top right
    dr.polygon([(300, 8), (392, 8), (392, 58)], fill=RED)

    # Floating solid squares — the constructivist confetti of pure form.
    dr.rectangle([250, 250, 274, 274], fill=RED)
    dr.rectangle([196, 40, 214, 58], fill=BLACK)
    r2 = 10
    dr.ellipse([120, 214, 120 + 2 * r2, 214 + 2 * r2], fill=RED)

    # Typography: the title of Lissitzky's abstract works.
    f_title = font(FONT_SANS_B, 40)
    dr.text((16, 8), "PROUN", font=f_title, fill=BLACK)
    f_sm = font(FONT_SANS, 10)
    dr.text((17, 52), "project for the affirmation of the new", font=f_sm, fill=BLACK)
    f_cap = font(FONT_SANS, 9)
    dr.text((392, 292), "after El Lissitzky · the red wedge · 1919",
            font=f_cap, fill=WHITE, anchor="rs")
    return finalize(img, dither=False)


# ------------------------------------------------------------- 2. Waxing crescent
def _lit_crescent(dr, cx, cy, r, frac, waxing=True, fill=(232, 232, 232)):
    """Fill the sunlit crescent of a moon. frac in 0..1; waxing lights the right."""
    # illuminated fraction f = (1+cos e)/2 -> terminator ellipse scale k = 1-2f
    k = 1.0 - 2.0 * frac                       # +right..-left; sign set by 'waxing'
    step = 1
    y = -r
    while y <= r:
        hw = math.sqrt(max(0.0, r * r - y * y))
        xr = cx + hw            # right limb
        xl = cx - hw            # left limb
        xt = cx + k * hw        # terminator crossing this row
        if waxing:              # lit lies to the RIGHT of the terminator
            x0, x1 = xt, xr
        else:                   # lit lies to the LEFT
            x0, x1 = xl, xt
        if x1 - x0 > 0.5:
            dr.rectangle([x0, cy + y, x1, cy + y + step], fill=fill)
        y += step


def image2_moon():
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # a wash of faint stars on the night ground
    rng = random.Random(20260718)
    for _ in range(140):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, H * s)
        v = rng.randint(70, 200)
        rr = rng.uniform(0.4, 1.2) * s
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(v, v, v))

    # header
    f_h = font(FONT_SERIF_B, 19 * s)
    f_d = font(FONT_SANS, 10 * s)
    dr.text((16 * s, 12 * s), "WAXING CRESCENT", font=f_h, fill=RED)
    dr.text((16 * s, 36 * s),
            "Saturday July 18, 2026  —  20% lit  ·  4 days old",
            font=f_d, fill=WHITE)
    dr.line([16 * s, 54 * s, (W - 16) * s, 54 * s], fill=(150, 150, 150), width=s)

    # the moon itself: dark disk with earthshine, thin lit crescent on the right
    mx, my, mr = 108, 170, 74
    mx, my, mr = mx * s, my * s, mr * s
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(26, 26, 26))  # earthshine
    _lit_crescent(dr, mx, my, mr - s, 0.20, waxing=True, fill=(236, 236, 236))
    # a couple of maria on the lit sliver, near the right limb
    for _ in range(30):
        ang = rng.uniform(-1.0, 1.0)
        rad = rng.uniform(0.55, 0.95) * mr
        cx = mx + rad * math.cos(ang)
        cy = my + rad * math.sin(ang) * 1.0
        if cx < mx + 0.35 * mr:
            continue
        cr = rng.uniform(1.5, 5) * s
        v = rng.choice([150, 175, 200])
        dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(v, v, v))
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=(120, 120, 120), width=s)
    dr.text((mx, (my // s + mr // s + 16) * s), "low in the W after sunset",
            font=font(FONT_SANS, 9 * s), fill=(190, 190, 190), anchor="ma")

    # week-ahead column
    cx0 = 216
    f_wk = font(FONT_SANS_B, 11 * s)
    f_it = font(FONT_SANS, 10 * s)
    dr.text((cx0 * s, 74 * s), "THE WEEK AHEAD", font=f_wk, fill=WHITE)
    events = [
        ("JUL 21", "First-quarter moon"),
        ("", "best crater relief at dusk"),
        ("JUL 28", "Twin meteor showers"),
        ("", "faint — best after midnight"),
        ("JUL 29", "Full Buck Moon"),
    ]
    y = 96
    for tag, txt in events:
        if tag:
            dr.text((cx0 * s, y * s), tag, font=f_wk, fill=RED)
        dr.text(((cx0 + 52) * s, y * s), txt, font=f_it, fill=WHITE)
        y += 22
    dr.line([cx0 * s, (y + 2) * s, (W - 16) * s, (y + 2) * s],
            fill=(150, 150, 150), width=s)
    dr.text((cx0 * s, (y + 10) * s),
            "the crescent fattens toward\nfirst quarter — catch it early,\nit sets soon after the sun",
            font=font(FONT_SANS, 9 * s), fill=(200, 200, 200))
    return finalize(img)


# ------------------------------------------------------------------ 3. Seigaiha
def image3_seigaiha():
    """Overlapping concentric arcs — the seigaiha 'blue ocean wave' pattern."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)
    rng = random.Random(718)

    R = 33                       # scale radius
    fracs = [1.0, 0.72, 0.44]    # concentric arc radii, as fractions of R
    dx = R                       # horizontal spacing between centers
    dy = int(R * 0.60)           # vertical spacing (rows overlap)

    row = 0
    y = -R
    while y < H + R:
        offset = (R // 2) if (row % 2) else 0
        x = -R + offset
        while x < W + R:
            # erase whatever lies beneath this scale's upper half — this is what
            # crops the arcs above into crisp scallops as rows march downward.
            dr.pieslice([x - R, y - R, x + R, y + R], 180, 360, fill=WHITE)
            red_scale = rng.random() < 0.14
            red_idx = rng.randint(0, len(fracs) - 1)
            for i, fr in enumerate(fracs):
                rr = R * fr
                c = RED if (red_scale and i == red_idx) else BLACK
                dr.arc([x - rr, y - rr, x + rr, y + rr], 180, 360, fill=c, width=2)
            # a small solid node at the base of the scale
            dr.ellipse([x - 2, y - 2, x + 2, y + 2],
                       fill=(RED if red_scale else BLACK))
            x += dx
        y += dy
        row += 1

    # a clean caption plate along the bottom
    dr.rectangle([0, H - 22, W, H], fill=WHITE)
    dr.line([0, H - 22, W, H - 22], fill=BLACK, width=1)
    f_capb = font(FONT_SANS_B, 10)
    f_cap = font(FONT_SANS, 10)
    f_jp = font(FONT_JP, 15)
    dr.text((10, H - 17), "青海波", font=f_jp, fill=RED)
    dr.text((62, H - 16), "SEIGAIHA", font=f_capb, fill=BLACK)
    dr.text((128, H - 16), "waves of the blue sea, drawn as overlapping arcs",
            font=f_cap, fill=BLACK)
    return finalize(img, dither=False)


# ---------------------------------------------------------------- 4. One Point Oh
def _seven_seg(dr, x, y, w, h, t, segs, color):
    """Draw a seven-segment digit in box (x,y,w,h) with thickness t."""
    m = h / 2
    S = {
        "a": [x + t, y, x + w - t, y + t],
        "g": [x + t, y + m - t / 2, x + w - t, y + m + t / 2],
        "d": [x + t, y + h - t, x + w - t, y + h],
        "f": [x, y + t, x + t, y + m],
        "b": [x + w - t, y + t, x + w, y + m],
        "e": [x, y + m, x + t, y + h - t],
        "c": [x + w - t, y + m, x + w, y + h - t],
    }
    for seg in segs:
        dr.rectangle(S[seg], fill=color)


def image4_perfect_ten():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # top titles
    f_t = font(FONT_SANS_B, 15 * s)
    f_r = font(FONT_SANS_B, 11 * s)
    dr.text((W * s // 2, 16 * s), "A PERFECT TEN", font=f_t, fill=BLACK, anchor="ma")
    dr.text((W * s // 2, 36 * s), "JULY 18, 1976  ·  50 YEARS AGO TODAY",
            font=f_r, fill=RED, anchor="ma")

    # the scoreboard: black panel with a thin red frame
    px0, py0, px1, py1 = 44, 66, 356, 168
    dr.rectangle([px0 * s, py0 * s, px1 * s, py1 * s], fill=BLACK)
    dr.rectangle([px0 * s, py0 * s, px1 * s, py1 * s], outline=RED, width=2 * s)

    # seven-segment "1.00" in red on the panel
    dw, dh, dt = 46 * s, 74 * s, 9 * s
    gap = 10 * s
    dpw = 12 * s  # decimal point width
    total = dw + dpw + gap + dw + gap + dw
    startx = (px0 + px1) * s / 2 - total / 2
    dy_ = (py0 + py1) * s / 2 - dh / 2
    xcur = startx
    # ghost of all segments (very dark) so the panel reads as a real display
    ghost = (60, 0, 0)
    for gx in (xcur, xcur + dw + dpw + gap, xcur + dw + dpw + gap + dw + gap):
        _seven_seg(dr, gx, dy_, dw, dh, dt, "abcdefg", ghost)
    # lit digits: 1 . 0 0
    _seven_seg(dr, xcur, dy_, dw, dh, dt, "bc", RED)               # 1
    xcur += dw
    dr.rectangle([xcur + 2 * s, dy_ + dh - dpw, xcur + 2 * s + dt, dy_ + dh],
                 fill=RED)                                          # decimal point
    xcur += dpw + gap
    _seven_seg(dr, xcur, dy_, dw, dh, dt, "abcdef", RED)           # 0
    xcur += dw + gap
    _seven_seg(dr, xcur, dy_, dw, dh, dt, "abcdef", RED)           # 0

    # explanation
    f_b = font(FONT_SERIF, 12 * s)
    lines = [
        "The board was never built to show a ten.",
        "So Nadia Comăneci's 10.0 came up as 1.00.",
    ]
    yy = 182
    for ln in lines:
        dr.text((W * s // 2, yy * s), ln, font=f_b, fill=BLACK, anchor="ma")
        yy += 17

    # credit line
    f_c = font(FONT_SANS_B, 10 * s)
    dr.text((W * s // 2, 232 * s),
            "NADIA COMĂNECI  —  MONTREAL 1976  —  UNEVEN BARS",
            font=f_c, fill=BLACK, anchor="ma")
    f_c2 = font(FONT_SANS, 10 * s)
    dr.text((W * s // 2, 250 * s),
            "the first perfect 10 in Olympic gymnastics",
            font=f_c2, fill=RED, anchor="ma")

    # a thin rule and small stars either side
    dr.line([60 * s, 270 * s, 340 * s, 270 * s], fill=BLACK, width=s)
    for cx in (46, 354):
        cxx, cyy, rr = cx * s, 270 * s, 5 * s
        pts = []
        for k in range(10):
            ang = -math.pi / 2 + k * math.pi / 5
            rad = rr if k % 2 == 0 else rr * 0.42
            pts.append((cxx + rad * math.cos(ang), cyy + rad * math.sin(ang)))
        dr.polygon(pts, fill=RED)
    return finalize(img)


# ------------------------------------------------------------------- 5. Truchet
def image5_truchet():
    """Multiscale Truchet arc tiling — smooth arcs via supersample + dither."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    rng = random.Random(20260718 + 5)

    def tile(x, y, size, color):
        """One Truchet cell: two quarter-circle arcs, orientation from rng."""
        lw = max(s, int(size * 0.16))
        r = size / 2
        if rng.random() < 0.5:
            # arcs centered on top-left and bottom-right corners
            dr.arc([x - r, y - r, x + r, y + r], 0, 90, fill=color, width=lw)
            dr.arc([x + r, y + r, x + size + r, y + size + r], 180, 270,
                   fill=color, width=lw)
        else:
            # arcs centered on top-right and bottom-left corners
            dr.arc([x + r, y - r, x + size + r, y + r], 90, 180, fill=color, width=lw)
            dr.arc([x - r, y + r, x + r, y + size + r], 270, 360, fill=color, width=lw)

    def cell(x, y, size, depth):
        # recursively subdivide some cells for multiscale density
        if depth < 2 and size > 40 * s and rng.random() < 0.42:
            h = size / 2
            for (ox, oy) in ((0, 0), (h, 0), (0, h), (h, h)):
                cell(x + ox, y + oy, h, depth + 1)
        else:
            color = RED if rng.random() < 0.14 else BLACK
            tile(x, y, size, color)

    base = 50 * s
    cols = (W * s) // base + 1
    rows = (H * s) // base + 1
    for j in range(rows):
        for i in range(cols):
            cell(i * base, j * base, base, 0)

    im = finalize(img)
    # small caption plate, drawn after dithering to stay crisp
    im = im.convert("RGB")
    d2 = ImageDraw.Draw(im)
    d2.rectangle([0, H - 18, 214, H], fill=WHITE)
    d2.rectangle([0, H - 18, 214, H], outline=BLACK, width=1)
    d2.text((6, H - 15), "TRUCHET", font=font(FONT_SANS_B, 10), fill=BLACK)
    d2.text((62, H - 15), "two arcs per tile, one labyrinth",
            font=font(FONT_SANS, 10), fill=BLACK)
    return finalize(im, dither=False)


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_proun, image2_moon, image3_seigaiha,
              image4_perfect_ten, image5_truchet]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", cols)
