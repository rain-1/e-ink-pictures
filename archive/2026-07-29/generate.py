#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-29.

Full Buck Moon day. Van Gogh's death (1890), International Tiger Day,
NASA's founding (1958), and the moon-washed double meteor shower.
Five 400x300 images in exactly white/black/red. Tonal scenes render at 3x,
LANCZOS downscale, Floyd-Steinberg dither into the palette; hard-edged
pieces quantize without dithering.
"""

import math
import os
import random
import shutil

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


def text_center(dr, cx, y, s, f, fill):
    x0, y0, x1, y1 = dr.textbbox((0, 0), s, font=f)
    dr.text((cx - (x1 - x0) / 2 - x0, y), s, font=f, fill=fill)


def rotated_text(base, cx, cy, s, f, fill, angle):
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(tmp)
    x0, y0, x1, y1 = dr.textbbox((0, 0), s, font=f)
    dr.text((cx - (x1 - x0) / 2 - x0, cy - (y1 - y0) / 2 - y0), s, font=f, fill=fill)
    tmp = tmp.rotate(angle, center=(cx, cy), resample=Image.BICUBIC)
    base.paste(tmp, (0, 0), tmp)


# ------------------------------------------------------------- 1. Buck Moon
def image1_buck_moon():
    rng = random.Random(20260729)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # stars
    for _ in range(140):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s * 0.75)
        r = rng.choice([1, 1, 1, 2, 2, 3])
        g = rng.randint(140, 255)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(g, g, g))

    # the full moon, huge, low over the ridge
    mcx, mcy, mr = 590, 400, 300
    # faint halo
    for hr, g in [(mr + 90, 26), (mr + 55, 44), (mr + 26, 70)]:
        dr.ellipse([mcx - hr, mcy - hr, mcx + hr, mcy + hr], fill=(g, g, g))
    dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=(235, 235, 235))

    # lunar maria (nearside, roughly): irregular gray blobs
    def blob(cx, cy, r, g, n=11, wob=0.42):
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            rr = r * (1 + rng.uniform(-wob, wob))
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        dr.polygon(pts, fill=(g, g, g))

    def m(dx, dy):  # maria coords in moon units (-1..1)
        return mcx + dx * mr, mcy + dy * mr

    blob(*m(-0.28, -0.38), mr * 0.24, 150)   # Imbrium
    blob(*m(0.08, -0.34), mr * 0.17, 158)    # Serenitatis
    blob(*m(0.30, -0.10), mr * 0.16, 152)    # Tranquillitatis
    blob(*m(0.62, -0.32), mr * 0.11, 160)    # Crisium
    blob(*m(0.48, 0.14), mr * 0.11, 162)     # Fecunditatis
    blob(*m(0.30, 0.22), mr * 0.09, 165)     # Nectaris
    blob(*m(-0.58, -0.05), mr * 0.20, 168)   # Procellanum
    blob(*m(-0.45, 0.22), mr * 0.13, 170)    # Humorum-ish
    # Tycho + rays
    tx, ty = m(-0.12, 0.62)
    for _ in range(16):
        a = rng.uniform(0, 2 * math.pi)
        ln = rng.uniform(mr * 0.15, mr * 0.55)
        ex, ey = tx + ln * math.cos(a), ty + ln * math.sin(a)
        if (ex - mcx) ** 2 + (ey - mcy) ** 2 < (mr * 0.97) ** 2:
            dr.line([tx, ty, ex, ey], fill=(250, 250, 250), width=3)
    dr.ellipse([tx - 12, ty - 12, tx + 12, ty + 12], fill=(255, 255, 255))
    # small craters
    for _ in range(26):
        a = rng.uniform(0, 2 * math.pi)
        d = mr * math.sqrt(rng.uniform(0, 0.9))
        cx2, cy2 = mcx + d * math.cos(a), mcy + d * math.sin(a)
        cr = rng.uniform(3, 10)
        g = rng.randint(175, 205)
        dr.ellipse([cx2 - cr, cy2 - cr, cx2 + cr, cy2 + cr], fill=(g, g, g))

    # ridge silhouette
    ridge = [(0, 700)]
    y = 700
    for x in range(0, W * s + 40, 40):
        y = min(max(y + rng.uniform(-26, 26), 640), 760)
        ridge.append((x, y))
    ridge += [(W * s, H * s), (0, H * s)]
    dr.polygon(ridge, fill=BLACK)

    # the buck — silhouette standing on the ridge inside the moon disc
    def stag(ox, oy, sc):
        P = lambda x, y: (ox + x * sc, oy + y * sc)
        # body
        dr.ellipse([*P(40, 52), *P(78, 72)], fill=BLACK)
        # neck + chest
        dr.polygon([P(44, 62), P(38, 38), P(48, 36), P(56, 58)], fill=BLACK)
        # head (muzzle to the left)
        dr.polygon([P(40, 40), P(26, 42), P(25, 46), P(38, 48), P(46, 44)],
                   fill=BLACK)
        # ear
        dr.polygon([P(42, 38), P(48, 30), P(46, 39)], fill=BLACK)
        # tail
        dr.polygon([P(76, 54), P(82, 50), P(78, 60)], fill=BLACK)
        # legs (front pair, rear pair with hock)
        lw = max(2, int(2.2 * sc))
        dr.line([*P(46, 68), *P(45, 82), *P(46, 96)], fill=BLACK, width=lw)
        dr.line([*P(52, 69), *P(52, 83), *P(51, 96)], fill=BLACK, width=lw)
        dr.line([*P(68, 69), *P(73, 80), *P(70, 96)], fill=BLACK, width=lw)
        dr.line([*P(74, 66), *P(78, 79), *P(76, 96)], fill=BLACK, width=lw)
        # antlers — two beams with forward tines
        aw = max(2, int(1.6 * sc))
        for dx in (0, 5):
            beam = [P(37 + dx, 37), P(33 + dx, 25), P(35 + dx, 14), P(42 + dx, 5)]
            dr.line(beam, fill=BLACK, width=aw)
            dr.line([*P(34 + dx, 27), *P(27 + dx, 22)], fill=BLACK, width=aw)
            dr.line([*P(34 + dx, 19), *P(28 + dx, 12)], fill=BLACK, width=aw)
            dr.line([*P(38 + dx, 11), *P(33 + dx, 4)], fill=BLACK, width=aw)
            dr.line([*P(42 + dx, 5), *P(47 + dx, 0)], fill=BLACK, width=aw)

    stag(430, 285, 4.4)

    # title top-left, almanac line in the dark foreground
    f_big = font(FONT_SERIF_B, 34 * s)
    f_sub = font(FONT_MONO, 11 * s)
    dr.text((26 * s, 12 * s), "BUCK MOON", font=f_big, fill=RED)
    dr.rectangle([26 * s, 262 * s, 30 * s, 284 * s], fill=RED)
    dr.text((38 * s, 262 * s), "FULL 14:36 UT · 29 JULY 2026", font=f_sub,
            fill=WHITE)
    dr.text((38 * s, 276 * s), "antlers in velvet, moon in glory", font=f_sub,
            fill=(170, 170, 170))
    return finalize(img)


# ------------------------------------------------------------- 2. Vincent
def image2_vincent():
    rng = random.Random(18900729)
    s = SS
    img = Image.new("RGB", (W * s, H * s), (30, 30, 30))
    dr = ImageDraw.Draw(img)
    horizon = int(H * s * 0.68)

    # swirling flow field: two vortices + drift
    vort = [(330, 260, 1.0), (830, 180, -1.0)]

    def field(x, y):
        vx, vy = 1.0, 0.0  # ambient drift
        for cx, cy, sp in vort:
            dx, dy = x - cx, y - cy
            d2 = dx * dx + dy * dy + 1
            k = 220000 * sp / d2
            vx += -dy * k / math.sqrt(d2)
            vy += dx * k / math.sqrt(d2)
        n = math.hypot(vx, vy) + 1e-9
        return vx / n, vy / n

    # short strokes following the field
    for _ in range(2600):
        x = rng.uniform(-40, W * s + 40)
        y = rng.uniform(-30, horizon + 10)
        g = rng.choice([70, 90, 110, 130, 150, 170, 190, 210])
        wdt = rng.choice([2, 3, 3, 4])
        pts = [(x, y)]
        for _ in range(rng.randint(8, 18)):
            vx, vy = field(x, y)
            x, y = x + vx * 7, y + vy * 7
            pts.append((x, y))
        dr.line(pts, fill=(g, g, g), width=wdt)

    # stars: bright cores with swirl halos, two red
    stars = [(180, 140, 26, WHITE), (330, 260, 34, RED), (560, 90, 22, WHITE),
             (700, 300, 24, WHITE), (830, 180, 30, RED), (450, 380, 18, WHITE),
             (90, 380, 20, WHITE)]
    for cx, cy, r, col in stars:
        for hr in (int(r * 2.1), int(r * 1.55)):
            dr.arc([cx - hr, cy - hr, cx + hr, cy + hr], 0, 330,
                   fill=(200, 200, 200), width=3)
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        dr.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
                   fill=WHITE if col == RED else col)

    # crescent moon, top right, red-rimmed
    mx, my, mr = 1050, 110, 62
    dr.ellipse([mx - mr - 8, my - mr - 8, mx + mr + 8, my + mr + 8], fill=RED)
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(245, 245, 245))
    dr.ellipse([mx - mr - 34, my - mr - 12, mx + mr - 34, my + mr - 12],
               fill=(30, 30, 30))

    # village horizon: dark band, tiny houses, one red window each
    dr.rectangle([0, horizon, W * s, H * s], fill=(15, 15, 15))
    hills = [(0, horizon)]
    for x in range(0, W * s + 60, 60):
        hills.append((x, horizon - rng.uniform(0, 30)))
    hills += [(W * s, horizon + 4)]
    dr.polygon(hills, fill=(15, 15, 15))
    hx = 150
    while hx < W * s - 100:
        hw, hh = rng.randint(40, 70), rng.randint(30, 50)
        hy = horizon + rng.randint(15, 60)
        dr.rectangle([hx, hy, hx + hw, hy + hh], fill=BLACK)
        dr.polygon([(hx - 6, hy), (hx + hw + 6, hy), (hx + hw / 2, hy - 22)],
                   fill=BLACK)
        if rng.random() < 0.75:
            wx = hx + rng.randint(8, hw - 16)
            dr.rectangle([wx, hy + 10, wx + 9, hy + 22], fill=RED)
        hx += hw + rng.randint(30, 90)
    # church spire
    sx = 720
    dr.rectangle([sx - 14, horizon - 30, sx + 14, horizon + 60], fill=BLACK)
    dr.polygon([(sx - 18, horizon - 30), (sx + 18, horizon - 30),
                (sx, horizon - 105)], fill=BLACK)

    # cypress — black flame on the left, foreground
    cx = 130
    flame = []
    for i in range(40):
        t = i / 39
        yy = H * s - t * (H * s * 0.94)
        ww = (1 - t) ** 0.7 * 95 + 8
        wob = math.sin(t * 21 + 1.2) * 26 * (0.35 + t)
        flame.append((cx + wob + ww, yy))
    flame.append((cx + math.sin(21 + 1.2) * 26 * 1.35, H * s * 0.045))
    for i in range(39, -1, -1):
        t = i / 39
        yy = H * s - t * (H * s * 0.94)
        ww = (1 - t) ** 0.7 * 95 + 8
        wob = math.sin(t * 21 + 1.2) * 26 * (0.35 + t)
        flame.append((cx + wob - ww, yy))
    dr.polygon(flame, fill=BLACK)

    # memorial line
    f_cap = font(FONT_SERIF, 12 * s)
    dr.text((252 * s, 283 * s), "Vincent · 1853–1890", font=f_cap,
            fill=(210, 210, 210))
    return finalize(img)


# ------------------------------------------------------------- 3. Tiger
def image3_tiger():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    cx, cy = W * s // 2, H * s // 2 - 26 * s
    u = 1.15 * s  # unit

    def A(x, y):
        return (cx + x * u, cy + y * u)

    def Pm(pts, fill):  # polygon + its mirror
        dr.polygon([A(x, y) for x, y in pts], fill=fill)
        dr.polygon([A(-x, y) for x, y in pts], fill=fill)

    # thin double ring behind the head (kamon feel)
    for R, col, wd in [(100, BLACK, 3), (92, RED, 2)]:
        dr.ellipse([cx - R * u, cy - R * u, cx + R * u, cy + R * u],
                   outline=col, width=int(wd * s))

    # ears — pointed, mostly black
    Pm([(26, -60), (36, -92), (62, -66)], BLACK)
    Pm([(33, -66), (38, -82), (52, -68)], WHITE)

    # head with jagged cheek ruff
    right = [(0, -74), (28, -70), (52, -56), (68, -36), (76, -14),
             (70, -2), (90, 6), (70, 14), (92, 26), (70, 32),
             (84, 46), (58, 50), (40, 62), (16, 70), (0, 72)]
    outline = right + [(-x, y) for x, y in reversed(right[:-1])]
    dr.polygon([A(x, y) for x, y in outline], fill=WHITE)
    dr.line([A(x, y) for x, y in outline] + [A(*right[0])], fill=BLACK,
            width=int(3 * s))

    # stripes — bold black wedges
    Pm([(12, -70), (18, -42), (26, -68)], BLACK)      # forehead verticals
    Pm([(32, -64), (36, -38), (46, -58)], BLACK)
    Pm([(58, -46), (40, -28), (64, -30)], BLACK)      # temple
    Pm([(74, -8), (34, 0), (72, 8)], BLACK)           # cheek horizontals
    Pm([(70, 16), (36, 20), (68, 28)], BLACK)
    Pm([(60, 36), (34, 34), (54, 46)], BLACK)

    # 王 forehead mark, red (the king mark)
    f_wang = font(FONT_JP, int(30 * u))
    x0, y0, x1, y1 = dr.textbbox((0, 0), "王", font=f_wang)
    dr.text((cx - (x1 - x0) / 2 - x0, cy - 72 * u), "王", font=f_wang, fill=RED)

    # eyes — angled slits, red iris
    Pm([(14, -24), (46, -38), (54, -26), (44, -18), (18, -12)], BLACK)
    for sign in (1, -1):
        ex, ey = 33 * sign, -25
        dr.ellipse([*A(ex - 6, ey - 6), *A(ex + 6, ey + 6)], fill=RED)
        dr.ellipse([*A(ex - 2, ey - 3), *A(ex + 2, ey + 1)], fill=BLACK)

    # muzzle
    dr.ellipse([*A(-30, -4), *A(30, 48)], fill=WHITE, outline=BLACK,
               width=int(3 * s))
    # nose — red
    dr.polygon([A(-12, 4), A(12, 4), A(0, 18)], fill=RED)
    # mouth + open jaw with fangs
    dr.line([A(0, 18), A(0, 28)], fill=BLACK, width=int(3 * s))
    dr.polygon([A(-16, 30), A(16, 30), A(10, 40), A(-10, 40)], fill=BLACK)
    dr.polygon([A(-11, 30), A(-7, 40), A(-3, 30)], WHITE)
    dr.polygon([A(11, 30), A(7, 40), A(3, 30)], WHITE)
    # chin
    dr.line([A(0, 48), A(0, 60)], fill=BLACK, width=int(2 * s))

    # whiskers
    for sy, ey in [(6, -2), (14, 12), (22, 26)]:
        for sign in (1, -1):
            dr.line([A(sign * 30, sy), A(sign * 84, ey)], fill=BLACK,
                    width=int(1.8 * s))

    # caption, clear of the ring
    f_t = font(FONT_SANS_B, 15 * s)
    f_s = font(FONT_MONO, 9 * s)
    text_center(dr, W * s / 2, 250 * s, "INTERNATIONAL TIGER DAY", f_t, BLACK)
    text_center(dr, W * s / 2, 272 * s,
                "JULY 29 · ~5,500 LEFT IN THE WILD", f_s, RED)
    return finalize(img, dither=True)


# ------------------------------------------------------------- 4. Red Wedge
def image4_red_wedge():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # the grey circle (flat 50% grey — the panel cannot show it; it will
    # dissolve into dither, which is the joke)
    ccx, ccy, cr = 268 * s, 128 * s, 92 * s
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(128, 128, 128))
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=BLACK,
               width=2 * s)
    # a darker inner grey crescent for depth
    dr.ellipse([ccx - cr * 0.55, ccy - cr * 0.62, ccx + cr * 0.75,
                ccy + cr * 0.68], fill=(96, 96, 96))

    # the red wedge, from lower-left, tip piercing the circle's heart
    tip = (ccx - 6 * s, ccy + 4 * s)
    base1 = (-30 * s, 292 * s)
    base2 = (108 * s, 322 * s)
    # white keyline so the wedge separates from the grey
    dr.polygon([tip, base1, base2], fill=WHITE)
    inset = 6 * s

    def shrink(p, q, r_):
        # move p toward centroid
        gx = (p[0] + q[0] + r_[0]) / 3
        gy = (p[1] + q[1] + r_[1]) / 3
        d = math.hypot(p[0] - gx, p[1] - gy)
        t = inset / d
        return (p[0] + (gx - p[0]) * t, p[1] + (gy - p[1]) * t)

    tri = [tip, base1, base2]
    dr.polygon([shrink(tri[i], tri[(i + 1) % 3], tri[(i + 2) % 3])
                for i in range(3)], fill=RED)

    # constructivist scaffolding
    dr.line([(20 * s, 40 * s), (392 * s, 262 * s)], fill=BLACK, width=3 * s)
    dr.rectangle([330 * s, 210 * s, 388 * s, 232 * s], fill=BLACK)
    dr.rectangle([30 * s, 34 * s, 66 * s, 52 * s], fill=RED)
    dr.rectangle([348 * s, 60 * s, 360 * s, 118 * s], fill=BLACK)
    dr.ellipse([30 * s, 96 * s, 54 * s, 120 * s], fill=BLACK)
    dr.line([(42 * s, 108 * s), (48 * s, 52 * s)], fill=BLACK, width=2 * s)
    for i in range(5):
        x = (300 + i * 18) * s
        dr.line([(x, 20 * s), (x + 26 * s, 20 * s)], fill=BLACK, width=2 * s)

    # slogan along the wedge: one line above it, one below
    ang = -math.degrees(math.atan2(tip[1] - (base1[1] + base2[1]) / 2,
                                   tip[0] - (base1[0] + base2[0]) / 2))
    f_slog = font(FONT_SANS_B, 16 * s)
    rotated_text(img, 106 * s, 168 * s, "BEAT THE GREYS", f_slog, BLACK, ang)
    rotated_text(img, 244 * s, 220 * s, "WITH THE RED WEDGE", f_slog, BLACK,
                 ang)

    f_cap = font(FONT_MONO, 8 * s)
    dr.text((162 * s, 281 * s),
            "after Lissitzky — no greys here, only dither",
            font=f_cap, fill=BLACK)
    return finalize(img, dither=True)


# ------------------------------------------------------------- 5. Double Shower
def image5_double_shower():
    rng = random.Random(730)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    dr.rectangle([6 * s, 6 * s, 394 * s, 294 * s], outline=BLACK, width=2 * s)

    f_title = font(FONT_SERIF_B, 20 * s)
    f_sub = font(FONT_MONO, 10 * s)
    f_row = font(FONT_SANS, 11 * s)
    f_rowb = font(FONT_SANS_B, 11 * s)
    f_tiny = font(FONT_MONO, 8 * s)

    text_center(dr, W * s / 2, 16 * s, "DOUBLE METEOR SHOWER", f_title, BLACK)
    text_center(dr, W * s / 2, 44 * s,
                "S. δ AQUARIIDS  ×  α CAPRICORNIDS", f_sub, RED)

    # sky panel
    px0, py0, px1, py1 = 22 * s, 64 * s, 378 * s, 196 * s
    dr.rectangle([px0, py0, px1, py1], fill=BLACK)
    for _ in range(90):
        x = rng.uniform(px0 + 6, px1 - 6)
        y = rng.uniform(py0 + 6, py1 - 6)
        g = rng.randint(120, 230)
        dr.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=(g, g, g))

    # the interfering full moon, top right of panel, with glow rings
    mx, my, mr2 = px1 - 52 * s, py0 + 34 * s, 24 * s
    for hr, g in [(mr2 * 2.4, 60), (mr2 * 1.8, 105), (mr2 * 1.35, 160)]:
        dr.ellipse([mx - hr, my - hr, mx + hr, my + hr], fill=(g, g, g))
    dr.ellipse([mx - mr2, my - mr2, mx + mr2, my + mr2], fill=WHITE)

    # radiant + meteors (washed near the moon: fewer, shorter)
    rx, ry = px0 + 96 * s, py0 + 58 * s
    dr.ellipse([rx - 3 * s, ry - 3 * s, rx + 3 * s, ry + 3 * s], outline=RED,
               width=int(1.5 * s))
    for _ in range(15):
        a = rng.uniform(0, 2 * math.pi)
        r0 = rng.uniform(14 * s, 30 * s)
        ln = rng.uniform(18 * s, 60 * s)
        x0m, y0m = rx + r0 * math.cos(a), ry + r0 * math.sin(a)
        x1m, y1m = rx + (r0 + ln) * math.cos(a), ry + (r0 + ln) * math.sin(a)
        if not (px0 + 4 < x1m < px1 - 4 and py0 + 4 < y1m < py1 - 4):
            continue
        moon_d = math.hypot(x1m - mx, y1m - my)
        g = 255 if moon_d > 90 * s else 150
        dr.line([x0m, y0m, x1m, y1m], fill=(g, g, g), width=int(1.2 * s))
    # two α Cap fireballs: slow, bright, red heads
    for (fx0, fy0, fx1, fy1) in [(px0 + 40 * s, py1 - 22 * s, px0 + 150 * s,
                                  py1 - 58 * s),
                                 (px0 + 210 * s, py1 - 14 * s, px0 + 300 * s,
                                  py1 - 44 * s)]:
        dr.line([fx0, fy0, fx1, fy1], fill=WHITE, width=int(2.6 * s))
        dr.ellipse([fx1 - 4 * s, fy1 - 4 * s, fx1 + 4 * s, fy1 + 4 * s],
                   fill=RED)
    # clip anything (moon glow) that spilled outside the sky panel
    dr.rectangle([0, 0, W * s, py0 - 1], fill=WHITE)
    dr.rectangle([px1 + 1, 0, W * s, H * s], fill=WHITE)
    dr.rectangle([6 * s, 6 * s, 394 * s, 294 * s], outline=BLACK, width=2 * s)
    dr.rectangle([px0, py0, px1, py1], outline=BLACK, width=int(1 * s))
    text_center(dr, W * s / 2, 16 * s, "DOUBLE METEOR SHOWER", f_title, BLACK)
    text_center(dr, W * s / 2, 44 * s,
                "S. δ AQUARIIDS  ×  α CAPRICORNIDS", f_sub, RED)

    dr.text((px0 + 8 * s, py0 + 6 * s), "RADIANT: AQUARIUS, SE AFTER MIDNIGHT",
            font=f_tiny, fill=(200, 200, 200))
    # moon label on a white tag so it survives the glow
    tw = 62 * s
    dr.rectangle([mx - tw / 2, my + mr2 + 4 * s, mx + tw / 2,
                  my + mr2 + 17 * s], fill=WHITE, outline=BLACK, width=s)
    text_center(dr, mx, my + mr2 + 6 * s, "MOON 98%", f_tiny, BLACK)

    # almanac rows
    rows = [
        ("PEAK", "tonight → Jul 30, ZHR 15–25 (+ α Cap fireballs)"),
        ("PROBLEM", "full Buck Moon floods the sky — faint meteors lost"),
        ("TACTIC", "look away from the moon — fireballs punch through"),
        ("NEXT", "Perseids peak Aug 12–13 — moonless and excellent"),
    ]
    y = 208 * s
    for k, v in rows:
        dr.text((26 * s, y), k, font=f_rowb, fill=RED)
        dr.text((92 * s, y), v, font=f_row, fill=BLACK)
        y += 19 * s
    return finalize(img)


# ---------------------------------------------------------------------- main
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(os.path.dirname(here))
    os.makedirs(os.path.join(repo, "images"), exist_ok=True)
    makers = [image1_buck_moon, image2_vincent, image3_tiger,
              image4_red_wedge, image5_double_shower]
    for i, mk in enumerate(makers, 1):
        im = mk()
        out = os.path.join(repo, "images", f"{i}.png")
        im.save(out, optimize=True)
        shutil.copy(out, os.path.join(here, f"{i}.png"))
        print("wrote", out)


if __name__ == "__main__":
    main()
