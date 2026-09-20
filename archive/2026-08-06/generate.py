#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-08-06.

Five 400x300 images in exactly three colors (white, black, red).
Today: 35 years of the World Wide Web (first website, 6 Aug 1991),
Andy Warhol's birthday (6 Aug 1928), the total solar eclipse six days
away (12 Aug 2026), the Perseids peaking under a new moon, and a
multi-scale Truchet tiling from the ideas backlog.

Hard-edged pieces render at 3x with AA and quantize with dither=NONE
(edge pixels snap to the nearest palette color — crisp). Tonal skies
render at 3x and Floyd-Steinberg dither.
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
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


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


def finalize_hard(img):
    """Crisp mapping for hard-edged art. Naive nearest-color quantization sends
    anti-aliased mid-grays to RED (it is nearest in RGB distance), which
    speckles every black/white edge — so classify explicitly: a pixel is red
    only if it is saturated toward red, otherwise black/white by luminance."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    a = np.asarray(img.convert("RGB"), dtype=np.int32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (r * 299 + g * 587 + b * 114) // 1000
    is_red = (r - g > 70) & (r - b > 70) & (r > 120)
    out = np.zeros(a.shape, dtype=np.uint8)
    out[lum > 127] = WHITE
    out[is_red] = RED
    return Image.fromarray(out).quantize(palette=PAL, dither=Image.Dither.NONE)


def font(path, size):
    return ImageFont.truetype(path, size)


def ctext(dr, xy, text, f, fill, anchor="mm"):
    dr.text(xy, text, font=f, fill=fill, anchor=anchor)


# ------------------------------------------------------------- 1. WWW at 35
def image1_www35():
    """The first website, rendered like the original NeXT-era hypertext page."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # window chrome: thin black frame with a title bar
    dr.rectangle([6 * s, 6 * s, (W - 6) * s, (H - 6) * s], outline=BLACK, width=s)
    dr.rectangle([6 * s, 6 * s, (W - 6) * s, 26 * s], fill=BLACK)
    ctext(dr, (14 * s, 16 * s), "WorldWideWeb.app", font(FONT_MONO_B, 11 * s), WHITE,
          anchor="lm")
    ctext(dr, ((W - 14) * s, 16 * s), "http://info.cern.ch", font(FONT_MONO, 10 * s),
          RED, anchor="rm")

    # document
    x0 = 22
    ctext(dr, (x0 * s, 47 * s), "World Wide Web", font(FONT_SERIF_B, 25 * s), BLACK,
          anchor="lm")
    dr.line([x0 * s, 62 * s, (W - 22) * s, 62 * s], fill=BLACK, width=s)

    body = [
        "The WorldWideWeb (W3) is a wide-area",
        "hypermedia information retrieval initiative",
        "aiming to give universal access to a large",
        "universe of documents.",
    ]
    fb = font(FONT_SERIF, 13 * s)
    y = 76
    for line in body:
        ctext(dr, (x0 * s, y * s), line, fb, BLACK, anchor="lm")
        y += 17

    # hyperlinks: red, underlined — the whole point of the thing
    links = [
        ("What's out there?", "Help"),
        ("Software Products", "Technical"),
        ("Bibliography", "People"),
        ("History", "How can I help?"),
    ]
    fl = font(FONT_SERIF, 13 * s)
    y = 152
    for left, right in links:
        for text, lx in ((left, x0), (right, 210)):
            ctext(dr, (lx * s, y * s), text, fl, RED, anchor="lm")
            wpx = dr.textlength(text, font=fl)
            dr.line([lx * s, (y + 8) * s, lx * s + wpx, (y + 8) * s], fill=RED,
                    width=s)
        y += 22

    # footer band
    dr.rectangle([6 * s, (H - 46) * s, (W - 6) * s, (H - 6) * s], fill=BLACK)
    ctext(dr, (W // 2 * s, (H - 33) * s), "THE FIRST WEBSITE WENT ONLINE",
          font(FONT_SANS_B, 12 * s), WHITE)
    ctext(dr, (W // 2 * s, (H - 17) * s), "6 AUGUST 1991 — 35 YEARS AGO TODAY",
          font(FONT_SANS_B, 12 * s), RED)
    return finalize_hard(img)


# ------------------------------------------------------ 2. Eclipse countdown
def image2_eclipse():
    """Total solar eclipse of 12 Aug 2026 — six days out."""
    rng = random.Random(20260812)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # eclipsed sun, left: black disk, red corona streamers
    cx, cy, r = 108 * s, 128 * s, 62 * s
    for i in range(120):
        a = rng.uniform(0, 2 * math.pi)
        ln = r * rng.uniform(0.18, 0.75) * (1.35 if i % 9 == 0 else 1.0)
        x1 = cx + math.cos(a) * (r + 2 * s)
        y1 = cy + math.sin(a) * (r + 2 * s)
        x2 = cx + math.cos(a) * (r + 2 * s + ln)
        y2 = cy + math.sin(a) * (r + 2 * s + ln)
        dr.line([x1, y1, x2, y2], fill=RED, width=max(s, int(s * 1.2)))
    dr.ellipse([cx - r - 4 * s, cy - r - 4 * s, cx + r + 4 * s, cy + r + 4 * s],
               outline=RED, width=2 * s)
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK)

    # title block, right
    tx = 218
    ctext(dr, (tx * s, 62 * s), "TOTAL", font(FONT_SANS_B, 34 * s), BLACK, "lm")
    ctext(dr, (tx * s, 98 * s), "SOLAR", font(FONT_SANS_B, 34 * s), BLACK, "lm")
    ctext(dr, (tx * s, 134 * s), "ECLIPSE", font(FONT_SANS_B, 34 * s), RED, "lm")
    ctext(dr, (tx * s, 166 * s), "12 AUGUST 2026", font(FONT_SANS_B, 15 * s),
          BLACK, "lm")
    dr.rectangle([tx * s, 182 * s, (tx + 118) * s, 210 * s], fill=RED)
    ctext(dr, ((tx + 59) * s, 196 * s), "IN 6 DAYS", font(FONT_SANS_B, 16 * s),
          WHITE)

    # phase strip along the bottom
    dr.line([20 * s, 228 * s, 380 * s, 228 * s], fill=BLACK, width=s)
    phases = [-1.0, -0.55, -0.2, 0.0, 0.2, 0.55, 1.0]  # moon offset in sun radii
    pr = 14 * s
    for i, off in enumerate(phases):
        px = (48 + i * 51) * s
        py = 252 * s
        dr.ellipse([px - pr, py - pr, px + pr, py + pr], fill=BLACK)
        if off != 0.0:
            # white moon disk sliding across a black sun silhouette
            mx = px + off * 2 * pr
            dr.ellipse([mx - pr, py - pr, mx + pr, py + pr], fill=WHITE)
            # re-crop stray white outside the sun by redrawing ring
            dr.ellipse([px - pr, py - pr, px + pr, py + pr], outline=BLACK,
                       width=s)
        else:
            dr.ellipse([px - pr - 3 * s, py - pr - 3 * s, px + pr + 3 * s,
                        py + pr + 3 * s], outline=RED, width=2 * s)
    ctext(dr, (200 * s, 285 * s),
          "GREENLAND · ICELAND · SPAIN — TOTALITY 2m 18s",
          font(FONT_SANS_B, 11 * s), BLACK)
    return finalize_hard(img)


# ------------------------------------------------------------- 3. Perseids
def image3_perseids():
    """Meteor shower chart: radiant in Perseus, Cassiopeia for bearings."""
    rng = random.Random(20260813)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # faint Milky Way wash through Cassiopeia/Perseus
    for i in range(1500):
        t = rng.random()
        cx = (0.05 + 0.9 * t) * W * s
        cy = (0.42 - 0.30 * t) * H * s
        x = rng.gauss(cx, 30 * s)
        y = rng.gauss(cy, 22 * s)
        v = rng.randint(30, 85)
        rr = rng.uniform(0.5, 1.8) * s
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(v, v, v))

    # background stars
    for i in range(240):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s * 0.82)
        v = rng.randint(110, 235)
        rr = rng.uniform(0.4, 1.2) * s
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(v, v, v))

    def star(x, y, r):
        x, y, r = x * s, y * s, r * s
        for rr, v in [(1.9, 70), (1.35, 160), (1.0, 255)]:
            dr.ellipse([x - r * rr, y - r * rr, x + r * rr, y + r * rr],
                       fill=(v, v, v))

    # radiant
    rx, ry = 208, 96

    # meteors: streaks pointing away from the radiant
    for i in range(26):
        a = rng.uniform(0, 2 * math.pi)
        d0 = rng.uniform(38, 150)
        ln = rng.uniform(18, 70)
        x1 = rx + math.cos(a) * d0
        y1 = ry + math.sin(a) * d0
        x2 = rx + math.cos(a) * (d0 + ln)
        y2 = ry + math.sin(a) * (d0 + ln)
        if not (0 <= x2 <= W and -10 <= y2 <= H * 0.8):
            continue
        col = RED if i % 7 == 0 else WHITE
        # taper: brighter head, thin tail
        dr.line([x1 * s, y1 * s, x2 * s, y2 * s], fill=col, width=s)
        hx, hy = (x1 + (x2 - x1) * 0.8), (y1 + (y2 - y1) * 0.8)
        dr.line([hx * s, hy * s, x2 * s, y2 * s], fill=col, width=2 * s)

    # radiant mark
    dr.ellipse([(rx - 5) * s, (ry - 5) * s, (rx + 5) * s, (ry + 5) * s],
               outline=RED, width=2 * s)
    ctext(dr, (rx * s, (ry - 18) * s), "RADIANT",
          font(FONT_SANS_B, 10 * s), RED)

    # Cassiopeia (the W), upper left, for orientation
    cas = [(38, 66), (66, 44), (95, 60), (120, 36), (152, 50)]
    for i in range(len(cas) - 1):
        dr.line([cas[i][0] * s, cas[i][1] * s, cas[i + 1][0] * s,
                 cas[i + 1][1] * s], fill=(150, 150, 150), width=s)
    for x, y in cas:
        star(x, y, 2.4)
    ctext(dr, (92 * s, 22 * s), "CASSIOPEIA", font(FONT_SANS, 10 * s),
          (170, 170, 170))

    # Perseus figure below the radiant
    per = [(208, 96), (222, 130), (218, 168), (196, 196), (246, 158),
           (268, 186)]
    seg = [(0, 1), (1, 2), (2, 3), (2, 4), (4, 5)]
    for a, b in seg:
        dr.line([per[a][0] * s, per[a][1] * s, per[b][0] * s, per[b][1] * s],
                fill=(150, 150, 150), width=s)
    star(222, 130, 3.2)  # Mirfak
    star(246, 158, 2.6)  # Algol
    for x, y in [(218, 168), (196, 196), (268, 186)]:
        star(x, y, 2.0)
    ctext(dr, (242 * s, 120 * s), "Mirfak", font(FONT_SANS, 10 * s),
          (190, 190, 190), "lm")
    ctext(dr, (258 * s, 168 * s), "Algol", font(FONT_SANS, 10 * s),
          (190, 190, 190), "lm")
    ctext(dr, (232 * s, 210 * s), "PERSEUS", font(FONT_SANS, 11 * s),
          (170, 170, 170))

    # info panel
    dr.rectangle([0, (H - 52) * s, W * s, H * s], fill=WHITE)
    dr.rectangle([0, (H - 52) * s, W * s, (H - 49) * s], fill=RED)
    ctext(dr, (200 * s, (H - 37) * s), "PERSEID METEOR SHOWER — PEAK AUG 12–13",
          font(FONT_SANS_B, 13 * s), BLACK)
    ctext(dr, (200 * s, (H - 17) * s),
          "new moon · no moonlight · up to 100 meteors/hr · look NE after 22h",
          font(FONT_SANS, 11 * s), BLACK)
    return finalize(img, dither=True)


# ------------------------------------------------------- 4. Warhol pop cans
def image4_warhol():
    """Six soup cans, colorways swapped — b. 6 Aug 1928."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    strip_h = 28
    cols, rows = 3, 2
    pw = W / cols
    ph = (H - strip_h) / rows

    # (panel bg, top label, bottom label, outline, SOUP color, small-text color)
    ways = [
        (WHITE, RED, WHITE, BLACK, WHITE, BLACK),
        (BLACK, WHITE, BLACK, WHITE, RED, WHITE),
        (RED, BLACK, WHITE, BLACK, RED, BLACK),
        (BLACK, RED, WHITE, WHITE, WHITE, BLACK),
        (RED, WHITE, RED, WHITE, BLACK, WHITE),
        (WHITE, BLACK, RED, BLACK, WHITE, WHITE),
    ]

    def can(cx, cy, cw, ch, top, bottom, line, t_top, t_bot):
        x0, y0 = cx - cw / 2, cy - ch / 2
        x1, y1 = cx + cw / 2, cy + ch / 2
        eh = cw * 0.22  # lid ellipse height
        mid = y0 + ch * 0.52
        # body halves
        dr.rectangle([x0, y0 + eh / 2, x1, mid], fill=top)
        dr.rectangle([x0, mid, x1, y1 - eh / 2], fill=bottom)
        dr.ellipse([x0, y1 - eh, x1, y1], fill=bottom, outline=line, width=s)
        # seam + medallion
        dr.line([x0, mid, x1, mid], fill=line, width=s)
        mr = cw * 0.11
        dr.ellipse([cx - mr, mid - mr, cx + mr, mid + mr], outline=line,
                   width=s)
        # lid
        dr.ellipse([x0, y0, x1, y0 + eh], fill=top, outline=line, width=2 * s)
        dr.ellipse([x0 + 4 * s, y0 + 2 * s, x1 - 4 * s, y0 + eh - 2 * s],
                   outline=line, width=s)
        # outline
        dr.line([x0, y0 + eh / 2, x0, y1 - eh / 2], fill=line, width=2 * s)
        dr.line([x1, y0 + eh / 2, x1, y1 - eh / 2], fill=line, width=2 * s)
        # lettering
        ctext(dr, (cx, y0 + ch * 0.34), "SOUP", font(FONT_SERIF_B, int(cw * 0.21)),
              t_top)
        ctext(dr, (cx, y0 + ch * 0.78), "CONDENSED",
              font(FONT_SANS, int(cw * 0.09)), t_bot)

    for i, (bg, top, bottom, line, t_top, t_bot) in enumerate(ways):
        r, c = divmod(i, cols)
        px0, py0 = c * pw * s, r * ph * s
        dr.rectangle([px0, py0, px0 + pw * s, py0 + ph * s], fill=bg)
        can(px0 + pw * s / 2, py0 + ph * s / 2, pw * 0.52 * s, ph * 0.78 * s,
            top, bottom, line, t_top, t_bot)

    # grid lines
    for c in range(1, cols):
        dr.line([c * pw * s, 0, c * pw * s, (H - strip_h) * s], fill=BLACK,
                width=s)
    dr.line([0, ph * s, W * s, ph * s], fill=BLACK, width=s)

    dr.rectangle([0, (H - strip_h) * s, W * s, H * s], fill=BLACK)
    ctext(dr, (200 * s, (H - strip_h / 2) * s),
          "ANDY WARHOL — BORN 6 AUGUST 1928, PITTSBURGH",
          font(FONT_SANS_B, 12 * s), WHITE)
    return finalize_hard(img)


# ------------------------------------------------------ 5. Truchet multiscale
def image5_truchet():
    """Multi-scale Truchet arcs (Smith tiles), seeded by the date."""
    rng = random.Random(20260806)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    def arc_tile(x, y, size, flip, col, width):
        """Two quarter-circle arcs joining edge midpoints."""
        t = size * s
        x, y = x * s, y * s
        r = t / 2
        if not flip:
            pieces = [(x, y, 0, 90), (x + t, y + t, 180, 270)]
        else:
            pieces = [(x + t, y, 90, 180), (x, y + t, 270, 360)]
        for cx, cy, a0, a1 in pieces:
            pts = []
            for k in range(25):
                a = math.radians(a0 + (a1 - a0) * k / 24)
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            dr.line(pts, fill=col, width=width, joint="curve")

    # base grid: 20px tiles, 20 x 15
    base = 20
    cols, rows = W // base, H // base
    # choose tiles to subdivide (clustered a little for interest)
    subdiv = set()
    for _ in range(10):
        cx, cy = rng.randrange(cols), rng.randrange(rows)
        for dx in range(2):
            for dy in range(2):
                if rng.random() < 0.7:
                    subdiv.add(((cx + dx) % cols, (cy + dy) % rows))

    wid_base = int(4.4 * s)
    wid_sub = int(2.6 * s)
    for cy in range(rows):
        for cx in range(cols):
            if (cx, cy) in subdiv:
                for dx in range(2):
                    for dy in range(2):
                        col = RED if rng.random() < 0.14 else BLACK
                        arc_tile(cx * base + dx * base / 2,
                                 cy * base + dy * base / 2, base / 2,
                                 rng.random() < 0.5, col, wid_sub)
            else:
                col = RED if rng.random() < 0.12 else BLACK
                arc_tile(cx * base, cy * base, base, rng.random() < 0.5, col,
                         wid_base)
    return finalize_hard(img)


def main():
    import os
    out = os.path.dirname(os.path.abspath(__file__))
    makers = [image1_www35, image2_eclipse, image3_perseids, image4_warhol,
              image5_truchet]
    for i, mk in enumerate(makers, 1):
        im = mk()
        assert im.size == (W, H)
        path = os.path.join(out, f"{i}.png")
        im.save(path, optimize=True)
        print("wrote", path)


if __name__ == "__main__":
    main()
