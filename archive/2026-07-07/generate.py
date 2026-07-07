#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-07 (Tanabata).

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Render tonal scenes at 3x, LANCZOS downscale,
then Floyd-Steinberg dither into the exact palette; hard-edged pieces render
at 1x in pure palette colors.
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


# ---------------------------------------------------------------- 1. Amanogawa
def image1_amanogawa():
    rng = random.Random(20260707)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # Milky Way: a diagonal band of layered soft gray blobs, upper-right to lower-left
    def band_center(t):  # t in 0..1 along the band
        x = (0.95 - 0.75 * t) * W * s
        y = (0.02 + 0.9 * t) * H * s
        return x, y

    for i in range(2400):
        t = rng.random()
        cx, cy = band_center(t)
        spread = (22 + 14 * math.sin(t * math.pi)) * s
        x = rng.gauss(cx, spread)
        y = rng.gauss(cy, spread * 0.7)
        v = rng.randint(40, 110)
        r = rng.uniform(0.6, 2.4) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))
    # dark rift down the middle of the band
    for i in range(700):
        t = rng.random()
        cx, cy = band_center(t)
        x = rng.gauss(cx + 6 * s, 9 * s)
        y = rng.gauss(cy, 8 * s)
        r = rng.uniform(1.5, 4.5) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=BLACK)

    # background stars
    for i in range(230):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s * 0.93)
        v = rng.randint(120, 255)
        r = rng.uniform(0.4, 1.3) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    def bright_star(x, y, r, spikes=True):
        x, y, r = x * s, y * s, r * s
        if spikes:
            dr.line([x - 3.2 * r, y, x + 3.2 * r, y], fill=WHITE, width=s)
            dr.line([x, y - 3.2 * r, x, y + 3.2 * r], fill=WHITE, width=s)
        for rr, v in [(2.0, 60), (1.4, 150), (1.0, 255)]:
            dr.ellipse([x - r * rr, y - r * rr, x + r * rr, y + r * rr],
                       fill=(v, v, v))

    # Vega (Orihime) west of the river, Altair (Hikoboshi) east of it
    vx, vy = 78, 62
    ax, ay = 315, 172
    bright_star(vx, vy, 4.2)
    bright_star(ax, ay, 3.6)

    f_lbl = font(FONT_SANS, 11 * s)
    f_sub = font(FONT_SANS, 9 * s)
    dr.text((vx * s + 14 * s, vy * s - 7 * s), "VEGA", font=f_lbl, fill=WHITE)
    dr.text((vx * s + 14 * s, vy * s + 6 * s), "Orihime, the weaver",
            font=f_sub, fill=WHITE)
    dr.text((ax * s - 4 * s, ay * s + 10 * s), "ALTAIR", font=f_lbl, fill=WHITE,
            anchor="ra")
    dr.text((ax * s - 4 * s, ay * s + 23 * s), "Hikoboshi, the cowherd",
            font=f_sub, fill=WHITE, anchor="ra")

    # Bamboo on the left with red tanzaku (wish tags)
    bx = 24
    dr.line([(bx * s, H * s), (bx * s + 10 * s, 20 * s)], fill=(210, 210, 210),
            width=int(2.4 * s))
    for frac in (0.35, 0.55, 0.75):
        jx = (bx + 10 * (1 - frac)) * s
        jy = H * s * frac
        dr.line([jx - 4 * s, jy, jx + 4 * s, jy], fill=BLACK, width=s)
    # leaves
    for (lx, ly, angdeg, ln) in [(30, 60, -25, 30), (28, 100, 15, 34),
                                 (31, 150, -15, 30), (27, 205, 20, 30),
                                 (33, 45, 35, 24)]:
        a = math.radians(angdeg)
        x2 = lx + ln * math.cos(a)
        y2 = ly + ln * math.sin(a) * 0.45
        dr.line([(lx * s, ly * s), (x2 * s, y2 * s)], fill=(200, 200, 200),
                width=int(1.6 * s))
    # tanzaku
    for (tx, ty, ang) in [(48, 78, -8), (44, 132, 6), (52, 185, -4)]:
        wds, hds = 13, 26
        a = math.radians(ang)
        cs, sn = math.cos(a), math.sin(a)
        pts = []
        for px, py in [(-wds / 2, 0), (wds / 2, 0), (wds / 2, hds), (-wds / 2, hds)]:
            pts.append(((tx + px * cs - py * sn) * s, (ty + px * sn + py * cs) * s))
        # string to the stalk
        dr.line([( (tx) * s, ty * s), ((tx - 12) * s, (ty - 14) * s)],
                fill=(180, 180, 180), width=s)
        dr.polygon(pts, fill=RED)

    # title
    f_jp = font(FONT_JP, 30 * s)
    f_ti = font(FONT_SANS, 11 * s)
    dr.text((W * s - 12 * s, H * s - 46 * s), "七夕", font=f_jp, fill=RED, anchor="rs")
    dr.text((W * s - 12 * s, H * s - 28 * s),
            "TANABATA — the stars cross the river tonight",
            font=f_ti, fill=WHITE, anchor="rs")
    dr.text((W * s - 12 * s, H * s - 12 * s),
            "if it rains, the magpies cannot build their bridge",
            font=f_sub, fill=WHITE, anchor="rs")
    return finalize(img)


# -------------------------------------------------------------- 2. Hitomezashi
def image2_hitomezashi():
    # Seed bits from the date; regions of a hitomezashi pattern are 2-colorable.
    rng = random.Random(7726)
    cell = 14
    ox, oy = 10, 10
    cols = (W - 2 * ox) // cell   # 27
    rows = (H - 2 * oy - 26) // cell  # leave room for caption
    a = [rng.randint(0, 1) for _ in range(rows + 1)]  # row offsets
    b = [rng.randint(0, 1) for _ in range(cols + 1)]  # column offsets

    def hstitch(i, j):  # horizontal stitch left of lattice point (j..j+1, row i)
        return (j + a[i]) % 2 == 0

    def vstitch(i, j):  # vertical stitch on column j from row i..i+1
        return (i + b[j]) % 2 == 0

    # 2-color the cells: crossing a stitched edge flips color, unstitched keeps.
    color = [[None] * cols for _ in range(rows)]
    color[0][0] = 0
    stack = [(0, 0)]
    while stack:
        i, j = stack.pop()
        c = color[i][j]
        # neighbor over the top edge (row line i): edge segment j..j+1
        for ni, nj, edge in [
            (i - 1, j, ("h", i, j)), (i + 1, j, ("h", i + 1, j)),
            (i, j - 1, ("v", i, j)), (i, j + 1, ("v", i, j + 1)),
        ]:
            if 0 <= ni < rows and 0 <= nj < cols and color[ni][nj] is None:
                kind, ei, ej = edge
                stitched = hstitch(ei, ej) if kind == "h" else vstitch(ei, ej)
                color[ni][nj] = c ^ (1 if stitched else 0)
                stack.append((ni, nj))

    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)
    for i in range(rows):
        for j in range(cols):
            if color[i][j]:
                x0, y0 = ox + j * cell, oy + i * cell
                dr.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], fill=RED)

    # stitches: dashed look — draw segment with small gaps at lattice points
    gap = 3
    for i in range(rows + 1):        # horizontal rows of stitches
        y = oy + i * cell
        for j in range(cols):
            if hstitch(i, j):
                x0 = ox + j * cell
                dr.line([x0 + gap, y, x0 + cell - gap, y], fill=BLACK, width=2)
    for j in range(cols + 1):        # vertical columns of stitches
        x = ox + j * cell
        for i in range(rows):
            if vstitch(i, j):
                y0 = oy + i * cell
                dr.line([x, y0 + gap, x, y0 + cell - gap], fill=BLACK, width=2)

    f_cap = font(FONT_SANS, 10)
    f_capb = font(FONT_SANS_B, 10)
    ytxt = oy + rows * cell + 8
    dr.text((ox, ytxt), "HITOMEZASHI", font=f_capb, fill=BLACK)
    dr.text((ox + 92, ytxt),
            "one-stitch sashiko from two random binary strings", font=f_cap,
            fill=BLACK)
    dr.text((W - 10, ytxt), "07·07", font=f_capb, fill=RED, anchor="ra")
    return finalize(img, dither=False)


# ------------------------------------------------------------- 3. Moon almanac
def image3_moon():
    rng = random.Random(714)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # header
    f_h = font(FONT_SERIF_B, 20 * s)
    f_d = font(FONT_SANS, 11 * s)
    dr.text((16 * s, 14 * s), "LAST QUARTER", font=f_h, fill=RED)
    dr.text((16 * s, 40 * s), "Tuesday July 7, 2026 — 51% illuminated",
            font=f_d, fill=BLACK)
    dr.line([16 * s, 58 * s, (W - 16) * s, 58 * s], fill=BLACK, width=s)

    # moon: left half lit, right half dark (last quarter, dawn sky)
    mx, my, mr = 105, 168, 78
    mx, my, mr = mx * s, my * s, mr * s
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=BLACK)
    dr.pieslice([mx - mr, my - mr, mx + mr, my + mr], 90, 270, fill=(235, 235, 235))
    # maria / craters on the lit half
    for _ in range(46):
        ang = rng.uniform(math.pi / 2, 3 * math.pi / 2)
        rad = rng.uniform(0, 0.92) * mr
        cx = mx + rad * math.cos(ang)
        cy = my + rad * math.sin(ang)
        if cx > mx - 4 * s:
            continue
        cr = rng.uniform(2, 9) * s
        v = rng.choice([150, 170, 190, 205])
        dr.ellipse([cx - cr, cy - cr * 0.8, cx + cr, cy + cr * 0.8], fill=(v, v, v))
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=BLACK, width=s)
    # terminator line
    dr.line([mx, my - mr, mx, my + mr], fill=BLACK, width=s)

    # Saturn, small, in the gap between the moon and the events column
    sx, sy = 199 * s, 236 * s
    dr.ellipse([sx - 5 * s, sy - 5 * s, sx + 5 * s, sy + 5 * s], fill=BLACK)
    dr.ellipse([sx - 12 * s, sy - 3.5 * s, sx + 12 * s, sy + 3.5 * s],
               outline=BLACK, width=s)
    dr.text((sx, sy + 9 * s), "Saturn", font=font(FONT_SANS, 9 * s), fill=BLACK,
            anchor="ma")
    dr.text((105 * s, (168 + 84) * s), "look southeast before dawn",
            font=font(FONT_SANS, 9 * s), fill=BLACK, anchor="ma")

    # this-week column
    cx0 = 216
    f_wk = font(FONT_SANS_B, 11 * s)
    f_it = font(FONT_SANS, 10 * s)
    dr.text((cx0 * s, 76 * s), "THIS WEEK IN THE SKY", font=f_wk, fill=BLACK)
    events = [
        ("JUL 9", "Venus meets Regulus"),
        ("JUL 11", "Moon, Mars & Pleiades"),
        ("JUL 14", "NEW SUPERMOON"),
        ("", "best Milky Way night"),
        ("JUL 31", "double meteor shower"),
    ]
    y = 98
    for tag, txt in events:
        if tag:
            dr.text((cx0 * s, y * s), tag, font=f_wk, fill=RED)
        dr.text(((cx0 + 48) * s, y * s), txt, font=f_it, fill=BLACK)
        y += 22
    dr.line([cx0 * s, (y + 2) * s, (W - 16) * s, (y + 2) * s], fill=BLACK, width=s)
    dr.text((cx0 * s, (y + 10) * s),
            "the 4th of 5 supermoons\nin a row this year",
            font=font(FONT_SANS, 9 * s), fill=BLACK)
    return finalize(img)


# ------------------------------------------------------ 4. The Summer Triangle
def image4_summer_triangle():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    rng = random.Random(1977)

    # chart area
    ra_max, ra_min = 21.3, 18.1     # hours; RA increases to the left
    dec_max, dec_min = 52.0, 2.0

    def P(ra, dec):
        x = (ra_max - ra) / (ra_max - ra_min)   # ra_max at left
        x = 1 - x                                # flip: ra_max -> x=0? keep charts E-left
        # facing south: east (higher RA) on the left
        x = (ra_max - ra) / (ra_max - ra_min)
        y = (dec_max - dec) / (dec_max - dec_min)
        return (24 + x * (W - 48)) * s, (34 + y * (H - 78)) * s

    stars = {
        "Vega":    (18.615, 38.78, 0.03),
        "Deneb":   (20.690, 45.28, 1.25),
        "Altair":  (19.846, 8.87, 0.77),
        "Sadr":    (20.371, 40.26, 2.23),
        "GienahC": (20.770, 33.97, 2.48),
        "DeltaCyg": (19.750, 45.13, 2.87),
        "Albireo": (19.512, 27.96, 3.08),
        "Tarazed": (19.771, 10.61, 2.72),
        "Alshain": (19.922, 6.41, 3.71),
        "ZetaAql": (19.090, 13.86, 2.99),
        "Sheliak": (18.835, 33.36, 3.52),
        "Sulafat": (18.982, 32.69, 3.25),
        "ZetaLyr": (18.746, 37.60, 4.36),
        "DeltaLyr": (18.908, 36.90, 4.30),
    }

    # Milky Way band through Cygnus down to Aquila (dithered gray blobs)
    band = [(20.9, 48), (20.6, 42), (20.3, 36), (19.9, 28), (19.6, 20),
            (19.3, 12), (19.1, 5)]
    for k in range(len(band) - 1):
        (r1, d1), (r2, d2) = band[k], band[k + 1]
        for _ in range(210):
            t = rng.random()
            ra = r1 + (r2 - r1) * t + rng.gauss(0, 0.16)
            dec = d1 + (d2 - d1) * t + rng.gauss(0, 2.6)
            x, y = P(ra, dec)
            rr = rng.uniform(0.8, 2.6) * s
            v = rng.randint(190, 228)
            dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(v, v, v))

    # constellation lines
    lines = [
        ("Deneb", "Sadr"), ("Sadr", "GienahC"), ("Sadr", "DeltaCyg"),
        ("Sadr", "Albireo"),
        ("Vega", "ZetaLyr"), ("ZetaLyr", "Sheliak"), ("Sheliak", "Sulafat"),
        ("Sulafat", "DeltaLyr"), ("DeltaLyr", "ZetaLyr"),
        ("Altair", "Tarazed"), ("Altair", "Alshain"), ("Tarazed", "ZetaAql"),
    ]
    for n1, n2 in lines:
        x1, y1 = P(*stars[n1][:2])
        x2, y2 = P(*stars[n2][:2])
        dr.line([x1, y1, x2, y2], fill=(120, 120, 120), width=s)

    # THE red triangle
    tri = [P(*stars["Vega"][:2]), P(*stars["Deneb"][:2]), P(*stars["Altair"][:2])]
    def dashed(p1, p2, dash=7 * s, gapf=0.45, width=2 * s, fill=RED):
        d = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        n = max(1, int(d / dash))
        for k in range(n):
            t0, t1 = k / n, (k + (1 - gapf)) / n
            dr.line([p1[0] + (p2[0] - p1[0]) * t0, p1[1] + (p2[1] - p1[1]) * t0,
                     p1[0] + (p2[0] - p1[0]) * t1, p1[1] + (p2[1] - p1[1]) * t1],
                    fill=fill, width=width)
    dashed(tri[0], tri[1]); dashed(tri[1], tri[2]); dashed(tri[2], tri[0])

    # stars sized by magnitude
    for name, (ra, dec, mag) in stars.items():
        x, y = P(ra, dec)
        r = max(1.2, (5.0 - mag) * 1.35) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=BLACK)

    f_big = font(FONT_SERIF_B, 12 * s)
    f_sm = font(FONT_SANS, 9 * s)
    for name, dx, dy, anchor in [("Vega", 10, -16, "la"), ("Deneb", 8, -18, "la"),
                                 ("Altair", 10, 2, "la")]:
        x, y = P(*stars[name][:2])
        dr.text((x + dx * s, y + dy * s), name.upper(), font=f_big, fill=RED,
                anchor=anchor)
    for name, label, dx, dy in [("Albireo", "Albireo", 7, -3),
                                ("Sadr", "Cygnus", 12, 6),
                                ("Sheliak", "Lyra", -34, 4),
                                ("Tarazed", "Aquila", 10, -2)]:
        x, y = P(*stars[name][:2])
        dr.text((x + dx * s, y + dy * s), label, font=f_sm, fill=BLACK)

    f_t = font(FONT_SERIF_B, 15 * s)
    dr.text((16 * s, 8 * s), "THE SUMMER TRIANGLE", font=f_t, fill=BLACK)
    dr.text((W * s - 16 * s, 13 * s), "facing south, midnight",
            font=f_sm, fill=BLACK, anchor="ra")
    dr.text((16 * s, (H - 32) * s),
            "the Milky Way is the river Amanogawa; Vega and Altair stand on its banks",
            font=f_sm, fill=BLACK)
    dr.text((16 * s, (H - 19) * s),
            "tonight they are allowed to cross", font=f_sm, fill=RED)
    dr.rectangle([8 * s, 6 * s, (W - 8) * s, (H - 6) * s], outline=BLACK, width=s)
    return finalize(img)


# ---------------------------------------------------------------- 5. Ridgelines
def image5_ridgelines():
    rng = random.Random(20260707 + 5)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # red sun
    sunx, suny, sunr = 300 * s, 96 * s, 46 * s
    dr.ellipse([sunx - sunr, suny - sunr, sunx + sunr, suny + sunr], fill=RED)

    # layered ridges: back (light, dithers to speckle) to front (solid black)
    def ridge(base, amp, freqs, phase, jag):
        pts = []
        for px in range(0, W * s + 1, 2 * s):
            t = px / (W * s)
            y = base
            for k, (fq, a) in enumerate(freqs):
                y += a * math.sin(2 * math.pi * (fq * t + phase * (k + 1)))
            y += jag * (rng.random() - 0.5)
            pts.append((px, y * s))
        return pts

    layers = [
        (150, [(1.3, 16), (3.1, 7), (6.7, 3)], 0.15, 3, 205),
        (178, [(1.1, 20), (2.7, 9), (5.3, 4)], 0.42, 4, 165),
        (208, [(0.9, 22), (2.3, 11), (4.9, 5)], 0.77, 5, 90),
        (242, [(0.8, 24), (1.9, 12), (4.1, 6)], 0.31, 6, 0),
    ]
    for base, freqs, phase, jag, v in layers:
        pts = ridge(base, 0, freqs, phase, jag)
        poly = pts + [(W * s, H * s), (0, H * s)]
        dr.polygon(poly, fill=(v, v, v))
        # crisp ridge crest
        dr.line(pts, fill=(max(0, v - 60),) * 3, width=s)

    # mist: soft partial-width drifts, not hard full-width stripes
    for (mx0, mx1, my, mh) in [(0, 265, 197, 6), (120, 400, 228, 8)]:
        for px in range(mx0 * s, mx1 * s, 2 * s):
            t = (px / s - mx0) / max(1, (mx1 - mx0))
            fade = min(1.0, 3.5 * min(t, 1 - t) + 0.15)
            hh = mh * s * fade / 2
            cy = (my + mh / 2) * s + 2 * s * math.sin(px / (55 * s))
            dr.rectangle([px, cy - hh, px + 2 * s, cy + hh], fill=WHITE)

    # birds
    for (bx, by, sz) in [(96, 60, 7), (122, 74, 5), (78, 82, 4)]:
        bx, by, sz = bx * s, by * s, sz * s
        dr.arc([bx - sz, by - sz // 2, bx, by + sz], 200, 340, fill=BLACK,
               width=s)
        dr.arc([bx, by - sz // 2, bx + sz, by + sz], 200, 340, fill=BLACK,
               width=s)

    f_sm = font(FONT_SANS, 9 * s)
    dr.text((12 * s, (H - 20) * s), "ridgelines, from three sine waves and a little noise",
            font=f_sm, fill=WHITE)
    return finalize(img)


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_amanogawa, image2_hitomezashi, image3_moon,
              image4_summer_triangle, image5_ridgelines]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        # verify palette discipline
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", cols)
