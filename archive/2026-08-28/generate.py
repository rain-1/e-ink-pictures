#!/usr/bin/env python3
"""Day 2 — 2026-08-28. Five pictures for a 400x300 black/white/red e-ink screen.

1. Umbra       — diagram of last night's 96% partial lunar eclipse (Aug 27-28)
2. Farbenlehre — Goethe's 1809 allegorical color wheel, for his 277th birthday
3. Proun       — constructivist composition after El Lissitzky
4. Kamon       — date-seeded Japanese family-crest generator
5. Truchet     — multi-scale quarter-circle Truchet tiling
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 4  # supersample factor
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PALETTE = [WHITE, BLACK, RED]

FONT_DIR = "/usr/share/fonts/truetype"
SERIF = f"{FONT_DIR}/dejavu/DejaVuSerif.ttf"
SERIF_B = f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf"
SANS = f"{FONT_DIR}/dejavu/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf"
MONO = f"{FONT_DIR}/dejavu/DejaVuSansMono.ttf"
JP = f"{FONT_DIR}/fonts-japanese-gothic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def canvas(bg=WHITE):
    img = Image.new("RGB", (W * SS, H * SS), bg)
    return img, ImageDraw.Draw(img)


def quantize_nearest(img):
    """Downscale supersampled image and snap every pixel to the 3-color palette."""
    img = img.resize((W, H), Image.LANCZOS)
    px = img.load()
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y][:3]
            best = min(PALETTE, key=lambda c: (r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2)
            px[x, y] = best
    pal = Image.new("P", (1, 1))
    flat = [v for c in PALETTE for v in c] + [0] * (768 - 9)
    pal.putpalette(flat)
    return img.quantize(palette=pal, dither=Image.Dither.NONE)


def save(img, n):
    out = quantize_nearest(img)
    out.save(f"images/{n}.png")
    out.save(f"archive/2026-08-28/{n}.png")
    print(f"saved {n}.png")


def ctext(d, xy, text, font, fill=BLACK, anchor="mm"):
    d.text((xy[0] * SS, xy[1] * SS), text, font=font, fill=fill, anchor=anchor)


# ----------------------------------------------------------------------------
# 1. UMBRA — last night's partial lunar eclipse, 96% umbral magnitude
# ----------------------------------------------------------------------------
def picture1():
    img, d = canvas(WHITE)
    s = SS

    ctext(d, (200, 24), "PARTIAL LUNAR ECLIPSE", F(SERIF_B, 21 * s))
    ctext(d, (200, 46), "2026 August 27–28  ·  umbral magnitude 0.96", F(MONO, 10 * s))

    # Shadow geometry: penumbra and umbra circles, moon path crossing low through umbra.
    cx, cy = 200, 160
    r_pen, r_umb, r_moon = 104, 74, 20

    # Penumbra: dotted ring
    steps = 220
    for i in range(steps):
        a = 2 * math.pi * i / steps
        if i % 2 == 0:
            x = cx + r_pen * math.cos(a)
            y = cy + r_pen * math.sin(a)
            d.ellipse([(x - 1.1) * s, (y - 1.1) * s, (x + 1.1) * s, (y + 1.1) * s], fill=BLACK)
    # Umbra: solid black disc
    d.ellipse([(cx - r_umb) * s, (cy - r_umb) * s, (cx + r_umb) * s, (cy + r_umb) * s], fill=BLACK)

    ctext(d, (cx, cy - r_umb - 12), "umbra", F(SERIF_I, 11 * s))
    ctext(d, (cx - r_pen + 4, cy - r_pen + 32), "penumbra", F(SERIF_I, 11 * s))

    # Moon path: slightly inclined chord, five positions left to right.
    # Mid-eclipse moon sits deep in the umbra (96%), a sliver out the bottom.
    path_y0, path_y1 = cy + 68, cy + 48   # gentle upward slope L->R
    d.line([(cx - 185) * s, path_y0 * s, (cx + 185) * s, path_y1 * s], fill=BLACK, width=1 * s)

    def path_pos(t):  # t in [0,1] across the screen
        return cx - 185 + 370 * t, path_y0 + (path_y1 - path_y0) * t

    for t, phase in [(0.08, "out"), (0.35, "partial"), (0.5, "max"), (0.65, "partial"), (0.92, "out")]:
        mx, my = path_pos(t)
        box = [(mx - r_moon) * s, (my - r_moon) * s, (mx + r_moon) * s, (my + r_moon) * s]
        dist = math.hypot(mx - cx, my - cy)
        if phase == "out":
            d.ellipse(box, fill=WHITE, outline=BLACK, width=1 * s)
        else:
            # inside shadow: red where covered by umbra, white sliver elsewhere
            d.ellipse(box, fill=WHITE, outline=BLACK, width=1 * s)
            if dist < r_umb + r_moon:
                # draw red disc clipped to the umbra circle via per-pixel-ish wedge:
                # approximate by drawing the red moon then restoring the sliver
                d.ellipse(box, fill=RED, outline=BLACK, width=1 * s)
                # white sliver: part of moon outside umbra
                # sample-based restore
                for yy in range(int((my - r_moon)), int((my + r_moon)) + 1):
                    for xx in range(int((mx - r_moon)), int((mx + r_moon)) + 1):
                        if (xx - mx) ** 2 + (yy - my) ** 2 <= r_moon ** 2:
                            if (xx - cx) ** 2 + (yy - cy) ** 2 > r_umb ** 2:
                                d.rectangle([xx * s, yy * s, (xx + 1) * s - 1, (yy + 1) * s - 1], fill=WHITE)
                d.ellipse(box, outline=BLACK, width=1 * s)

    ctext(d, (20, 246), "moon's path →", F(SERIF_I, 11 * s), anchor="lm")
    ctext(d, (388, 268), "96% of the Moon\nin Earth's shadow", F(SERIF, 10 * s), anchor="rm")
    ctext(d, (200, 288), "last night, over this desk", F(SERIF_I, 10 * s))

    save(img, 1)


# ----------------------------------------------------------------------------
# 2. FARBENLEHRE — Goethe's allegorical color wheel, b. 28 Aug 1749
# ----------------------------------------------------------------------------
def picture2():
    img, d = canvas(WHITE)
    s = SS
    cx, cy, r_out, r_in = 138, 158, 108, 46

    # Goethe's 1809 wheel: color, quality, and a hatch texture standing in for the hue.
    # Textures: density of engraved lines (red gets true red).
    sectors = [
        ("ROT", "schön", RED, None),
        ("ORANGE", "edel", None, ("radial", 3)),
        ("GELB", "gut", None, ("radial", 7)),
        ("GRÜN", "nützlich", None, ("cross", 5)),
        ("BLAU", "gemein", None, ("ring", 4)),
        ("VIOLETT", "unnöthig", None, ("ring", 2)),
    ]
    # Start at -120° so sector midpoints avoid the horizontal extremes:
    # ROT lands at top, GRÜN at bottom, the rest on diagonals.
    n = len(sectors)
    for i, (name, quality, solid, tex) in enumerate(sectors):
        a0 = -120 + i * 360 / n
        a1 = a0 + 360 / n
        bbox_out = [(cx - r_out) * s, (cy - r_out) * s, (cx + r_out) * s, (cy + r_out) * s]
        if solid:
            d.pieslice(bbox_out, a0, a1, fill=solid)
        else:
            kind, step = tex
            if kind == "radial":
                for k in range(0, 61):
                    if k % step:
                        continue
                    a = math.radians(a0 + (a1 - a0) * k / 60)
                    d.line([(cx + r_in * 0.4 * math.cos(a)) * s, (cy + r_in * 0.4 * math.sin(a)) * s,
                            (cx + r_out * math.cos(a)) * s, (cy + r_out * math.sin(a)) * s],
                           fill=BLACK, width=1 * s)
            elif kind == "ring":
                rr = r_in
                while rr < r_out:
                    d.arc(bbox_out if rr == r_out else
                          [(cx - rr) * s, (cy - rr) * s, (cx + rr) * s, (cy + rr) * s],
                          a0, a1, fill=BLACK, width=1 * s)
                    rr += step
            elif kind == "cross":
                for k in range(0, 61, step):
                    a = math.radians(a0 + (a1 - a0) * k / 60)
                    d.line([(cx + r_in * 0.4 * math.cos(a)) * s, (cy + r_in * 0.4 * math.sin(a)) * s,
                            (cx + r_out * math.cos(a)) * s, (cy + r_out * math.sin(a)) * s],
                           fill=BLACK, width=1 * s)
                rr = r_in
                while rr < r_out:
                    d.arc([(cx - rr) * s, (cy - rr) * s, (cx + rr) * s, (cy + rr) * s],
                          a0, a1, fill=BLACK, width=1 * s)
                    rr += 6
        # sector division lines
        for a in (a0,):
            ar = math.radians(a)
            d.line([(cx) * s, (cy) * s,
                    (cx + r_out * math.cos(ar)) * s, (cy + r_out * math.sin(ar)) * s],
                   fill=BLACK, width=2 * s)
        # labels on a mid radius, clamped away from the screen edges,
        # on white plates so they stay legible over the textures
        am = math.radians((a0 + a1) / 2)
        lx = min(max(cx + (r_out + 18) * math.cos(am), 48), 250)
        ly = cy + (r_out + 18) * math.sin(am)
        fn, fq = F(SERIF_B, 11 * s), F(SERIF_I, 10 * s)
        bb1 = d.textbbox((lx * s, (ly - 6) * s), name, font=fn, anchor="mm")
        bb2 = d.textbbox((lx * s, (ly + 7) * s), quality, font=fq, anchor="mm")
        pad = 3 * s
        d.rectangle([min(bb1[0], bb2[0]) - pad, bb1[1] - pad,
                     max(bb1[2], bb2[2]) + pad, bb2[3] + pad], fill=WHITE)
        ctext(d, (lx, ly - 6), name, fn)
        ctext(d, (lx, ly + 7), quality, fq)

    # outer rim + white center with title
    d.ellipse([(cx - r_out) * s, (cy - r_out) * s, (cx + r_out) * s, (cy + r_out) * s],
              outline=BLACK, width=2 * s)
    d.ellipse([(cx - r_in) * s, (cy - r_in) * s, (cx + r_in) * s, (cy + r_in) * s],
              fill=WHITE, outline=BLACK, width=2 * s)
    ctext(d, (cx, cy - 10), "ZUR", F(SERIF, 11 * s))
    ctext(d, (cx, cy + 4), "FARBEN", F(SERIF_B, 12 * s))
    ctext(d, (cx, cy + 18), "LEHRE", F(SERIF_B, 12 * s))

    # right column
    x = 330
    ctext(d, (x, 40), "GOETHE", F(SERIF_B, 20 * s))
    ctext(d, (x, 62), "geb. 28. August 1749", F(SERIF, 10 * s))
    ctext(d, (x, 76), "277 Jahre", F(SERIF_I, 10 * s))
    d.line([(x - 38) * s, 94 * s, (x + 38) * s, 94 * s], fill=BLACK, width=1 * s)
    quote = "Die Farben sind\nTaten des Lichts,\nTaten und Leiden."
    ctext(d, (x, 130), quote, F(SERIF_I, 11 * s))
    ctext(d, (x, 168), "— Farbenlehre, 1810", F(SERIF, 9 * s))
    # a small solid red square as a specimen chip
    d.rectangle([(x - 14) * s, 196 * s, (x + 14) * s, 224 * s], fill=RED, outline=BLACK, width=1 * s)
    ctext(d, (x, 238), "die schönste", F(SERIF_I, 9 * s))

    save(img, 2)


# ----------------------------------------------------------------------------
# 3. PROUN — after El Lissitzky
# ----------------------------------------------------------------------------
def picture3():
    img, d = canvas(WHITE)
    s = SS
    rng = random.Random(20260828)

    def poly(pts, **kw):
        d.polygon([(x * s, y * s) for x, y in pts], **kw)

    # black half-plane, low diagonal
    poly([(0, 300), (400, 300), (400, 208), (0, 268)], fill=BLACK)

    # large black circle, off-center
    ccx, ccy, cr = 258, 128, 86
    d.ellipse([(ccx - cr) * s, (ccy - cr) * s, (ccx + cr) * s, (ccy + cr) * s], fill=BLACK)
    # white inner circle ring
    d.ellipse([(ccx - cr + 10) * s, (ccy - cr + 10) * s, (ccx + cr - 10) * s, (ccy + cr - 10) * s],
              outline=WHITE, width=2 * s)

    # the red wedge, piercing the circle from lower left
    poly([(6, 236), (252, 118), (208, 172)], fill=RED)
    # small white counter-wedge inside the circle
    poly([(252, 118), (300, 96), (286, 130)], fill=WHITE)

    # diagonal bars
    def bar(x0, y0, ang_deg, length, w, fill):
        a = math.radians(ang_deg)
        dx, dy = math.cos(a), math.sin(a)
        px, py = -dy * w / 2, dx * w / 2
        poly([(x0 + px, y0 + py), (x0 - px, y0 - py),
              (x0 + dx * length - px, y0 + dy * length - py),
              (x0 + dx * length + px, y0 + dy * length + py)], fill=fill)

    bar(24, 64, 16, 130, 7, BLACK)
    bar(40, 86, 16, 86, 3, BLACK)
    bar(322, 226, -64, 68, 9, RED)
    bar(120, 262, -12, 74, 4, WHITE)

    # scattered rectangles
    d.rectangle([340 * s, 36 * s, 366 * s, 62 * s], fill=RED)
    d.rectangle([28 * s, 148 * s, 44 * s, 164 * s], fill=BLACK)
    d.rectangle([352 * s, 250 * s, 384 * s, 258 * s], fill=WHITE)

    # sparse type
    ctext(d, (16, 18), "PROUN", F(SANS_B, 17 * s), anchor="lm")
    ctext(d, (16, 36), "nach El Lissitzky · 1919/2026", F(SANS, 8 * s), anchor="lm")
    ctext(d, (388, 288), "28 VIII", F(SANS_B, 10 * s), fill=WHITE, anchor="rm")

    save(img, 3)


# ----------------------------------------------------------------------------
# 4. KAMON — date-seeded family crest generator
# ----------------------------------------------------------------------------
def picture4():
    img, d = canvas(WHITE)
    s = SS
    rng = random.Random("kamon-2026-08-28")
    cx, cy, R = 200, 142, 104

    # enclosure: thick black ring with a thin red ring inside it
    d.ellipse([(cx - R) * s, (cy - R) * s, (cx + R) * s, (cy + R) * s], fill=BLACK)
    d.ellipse([(cx - R + 8) * s, (cy - R + 8) * s, (cx + R - 8) * s, (cy + R - 8) * s], fill=RED)
    d.ellipse([(cx - R + 12) * s, (cy - R + 12) * s, (cx + R - 12) * s, (cy + R - 12) * s], fill=WHITE)

    n = rng.choice([6, 8])          # fold symmetry
    motif_r = R - 26

    def rot(px, py, a):
        return (cx + (px - cx) * math.cos(a) - (py - cy) * math.sin(a),
                cy + (px - cx) * math.sin(a) + (py - cy) * math.cos(a))

    def rpoly(pts, a, **kw):
        d.polygon([tuple(v * s for v in rot(x, y, a)) for x, y in pts], **kw)

    # petal: pointed leaf built from a polygon spine with width profile
    def petal(a, length, width, fill):
        pts_l, pts_r = [], []
        for t in range(0, 21):
            tt = t / 20
            wl = width * math.sin(math.pi * tt) * (1 - 0.35 * tt)
            px = cx
            py = cy - length * tt
            pts_l.append((px - wl, py))
            pts_r.append((px + wl, py))
        rpoly(pts_l + pts_r[::-1], a, fill=fill)

    style = rng.choice(["petals", "petals"])  # one family this run; more next time
    for i in range(n):
        a = 2 * math.pi * i / n
        petal(a, motif_r, motif_r * 0.30, BLACK)
    for i in range(n):
        a = 2 * math.pi * i / n + math.pi / n
        petal(a, motif_r * 0.58, motif_r * 0.14, BLACK)
    # center: white ring + red core
    d.ellipse([(cx - 26) * s, (cy - 26) * s, (cx + 26) * s, (cy + 26) * s], fill=WHITE)
    d.ellipse([(cx - 17) * s, (cy - 17) * s, (cx + 17) * s, (cy + 17) * s], fill=BLACK)
    d.ellipse([(cx - 9) * s, (cy - 9) * s, (cx + 9) * s, (cy + 9) * s], fill=RED)

    ctext(d, (200, 270), "家紋", F(JP, 22 * s))         # 家紋
    kanji_n = {6: "六", 8: "八"}[n]
    ctext(d, (200, 292), f"{kanji_n}弁の花・二〇二六", F(JP, 9 * s))

    save(img, 4)


# ----------------------------------------------------------------------------
# 5. TRUCHET — multi-scale quarter-circle tiling
# ----------------------------------------------------------------------------
def picture5():
    img, d = canvas(WHITE)
    s = SS
    rng = random.Random(828)

    def tile(x, y, size, depth):
        # subdivide some tiles
        if depth < 2 and size > 25 and rng.random() < 0.42:
            h = size / 2
            for dx in (0, h):
                for dy in (0, h):
                    tile(x + dx, y + dy, h, depth + 1)
            return
        lw = max(2, int(size * 0.16))
        color = RED if rng.random() < 0.07 else BLACK
        flip = rng.random() < 0.5
        # two quarter-circle arcs, Smith-tile style
        if flip:
            b1 = [(x - size / 2) * s, (y - size / 2) * s, (x + size / 2) * s, (y + size / 2) * s]
            b2 = [(x + size / 2) * s, (y + size / 2) * s, (x + 3 * size / 2) * s, (y + 3 * size / 2) * s]
            d.arc(b1, 0, 90, fill=color, width=lw * s)
            d.arc(b2, 180, 270, fill=color, width=lw * s)
        else:
            b1 = [(x + size / 2) * s, (y - size / 2) * s, (x + 3 * size / 2) * s, (y + size / 2) * s]
            b2 = [(x - size / 2) * s, (y + size / 2) * s, (x + size / 2) * s, (y + 3 * size / 2) * s]
            d.arc(b1, 90, 180, fill=color, width=lw * s)
            d.arc(b2, 270, 360, fill=color, width=lw * s)

    N = 50  # base tile size
    for gy in range(H // N):
        for gx in range(W // N):
            tile(gx * N, gy * N, N, 0)

    save(img, 5)


if __name__ == "__main__":
    picture1()
    picture2()
    picture3()
    picture4()
    picture5()
