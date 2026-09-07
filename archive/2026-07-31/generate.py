#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-31.

Tonight the α Capricornids and Southern δ Aquariids both peak — and a 98%
moon (full on the 29th) floods the sky, so only the fireballs get through.
Also on this day: US Patent No. 1 (1790) and the wreck of the 1715 Spanish
plate fleet. Five 400x300 images in exactly white/black/red.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageChops

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
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def rotpts(pts, ang, cx=0.0, cy=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + (x - cx) * ca - (y - cy) * sa,
             cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


# ----------------------------------------------------------- 1. Moonwashed
def image1_moonwashed():
    """Double meteor shower peak — drowned by a 98% moon sitting right in
    the radiant. Only the α Capricornid fireballs get through."""
    rng = random.Random(20260731)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    mx, my, mr = 292 * s, 92 * s, 58 * s
    glare = int(mr * 2.6)

    # moonlight glare: radial gradient that will dither into speckle
    for rr in range(glare, mr - s, -2 * s):
        t = (glare - rr) / (glare - mr)          # 0 at edge, 1 at moon
        v = int(4 + 120 * t * t)
        dr.ellipse([mx - rr, my - rr, mx + rr, my + rr], fill=(v, v, v))

    # stars, only where the glare hasn't drowned them
    for _ in range(150):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s * 0.9)
        d = math.hypot(x - mx, y - my)
        if d < glare * 1.1:
            continue
        v = rng.randint(90, 220)
        r = rng.uniform(0.4, 1.2) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # meteors radiate AWAY from the radiant — which the moon is sitting on.
    # δ Aquariids: numerous but faint; barely surviving the moonlight.
    for _ in range(9):
        ang = rng.uniform(0, 2 * math.pi)
        if -1.9 < ang - math.pi / 2 < -0.4:   # don't start inside the moon glare
            continue
        r0 = rng.uniform(glare * 1.05, glare * 1.9)
        ln = rng.uniform(18, 42) * s
        x0 = mx + r0 * math.cos(ang)
        y0 = my + r0 * math.sin(ang)
        x1 = x0 + ln * math.cos(ang)
        y1 = y0 + ln * math.sin(ang)
        if not (0 < x1 < W * s and 0 < y1 < H * s * 0.86):
            continue
        v = rng.randint(90, 150)
        dr.line([x0, y0, x1, y1], fill=(v, v, v), width=s)

    # one α Capricornid FIREBALL, lower left, bright enough to beat the moon
    fang = math.radians(152)
    fx0 = mx + glare * 1.35 * math.cos(fang)
    fy0 = my + glare * 1.35 * math.sin(fang) + 30 * s
    fx1 = fx0 + 120 * s * math.cos(fang)
    fy1 = fy0 + 120 * s * math.sin(fang)
    dr.line([fx0, fy0, fx1, fy1], fill=RED, width=int(3.2 * s))
    dr.line([(fx0 + fx1) / 2, (fy0 + fy1) / 2, fx1, fy1], fill=WHITE, width=s)
    for rr, col in [(5.5, RED), (3.2, WHITE)]:
        dr.ellipse([fx1 - rr * s, fy1 - rr * s, fx1 + rr * s, fy1 + rr * s],
                   fill=col)
    # a couple of small red shards behind it
    for (ox, oy, ln) in [(30, -14, 22), (54, 10, 15)]:
        x0, y0 = fx0 + ox * s, fy0 + oy * s
        x1 = x0 + ln * s * math.cos(fang)
        y1 = y0 + ln * s * math.sin(fang)
        dr.line([x0, y0, x1, y1], fill=RED, width=s)

    # the moon itself: 98% waning gibbous, craters, thin dark sliver on one limb
    pad = 4 * s
    msz = 2 * (mr + pad)
    moon = Image.new("RGB", (msz, msz), (0, 0, 0))
    mdr = ImageDraw.Draw(moon)
    c = mr + pad
    mdr.ellipse([c - mr, c - mr, c + mr, c + mr], fill=(238, 238, 238))
    mrng = random.Random(731)
    for _ in range(60):
        a = mrng.uniform(0, 2 * math.pi)
        rad = mrng.uniform(0, 0.9) * mr
        cx = c + rad * math.cos(a)
        cy = c + rad * math.sin(a)
        cr = mrng.uniform(2, 10) * s
        v = mrng.choice([155, 175, 195, 210])
        mdr.ellipse([cx - cr, cy - cr * 0.85, cx + cr, cy + cr * 0.85],
                    fill=(v, v, v))
    # waning: dark lune on the trailing limb (two-circle difference)
    m1 = Image.new("L", (msz, msz), 0)
    ImageDraw.Draw(m1).ellipse([c - mr, c - mr, c + mr, c + mr], fill=255)
    m2 = Image.new("L", (msz, msz), 0)
    off = 7 * s
    ImageDraw.Draw(m2).ellipse([c - mr - off, c - mr, c + mr - off, c + mr],
                               fill=255)
    lune = ImageChops.subtract(m1, m2)
    moon.paste((22, 22, 22), (0, 0), lune)
    img.paste(moon, (mx - c, my - c), m1)

    # caption block, lower left on black
    f_t = font(FONT_SANS_B, 13 * s)
    f_m = font(FONT_SANS, 10 * s)
    f_s = font(FONT_SANS, 9 * s)
    x0, y0 = 14 * s, (H - 66) * s
    dr.text((x0, y0), "DOUBLE METEOR SHOWER TONIGHT", font=f_t, fill=WHITE)
    dr.text((x0, y0 + 18 * s), "α Capricornids  ·  Southern δ Aquariids",
            font=f_m, fill=WHITE)
    dr.text((x0, y0 + 34 * s),
            "but the Moon is 98% full and parked in the radiant —",
            font=f_s, fill=(200, 200, 200))
    dr.text((x0, y0 + 47 * s), "only the fireballs get through",
            font=f_s, fill=RED)
    dr.text((14 * s, 10 * s), "31 JULY 2026", font=font(FONT_MONO, 9 * s),
            fill=(170, 170, 170))
    return finalize(img)


# ---------------------------------------------- 2. Red wedge vs the moonlight
def image2_red_wedge():
    """After El Lissitzky, 'Beat the Whites with the Red Wedge' (1919) —
    tonight the wedge is an α Capricornid fireball and the target is a 98%
    moon. Constructivism owns this palette; finally using it."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # diagonal field: black below the line from (0,300) to (400,60)
    dr.polygon([(0, H * s), (W * s, 60 * s), (W * s, H * s)], fill=BLACK)

    # the moon: a plain white disc deep in the black field
    cx, cy, r = 262 * s, 176 * s, 72 * s
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    # a thin orbit arc around it (open at the bottom, clear of the slogan)
    r2 = int(r * 1.26)
    dr.arc([cx - r2, cy - r2, cx + r2, cy + r2], start=115, end=55,
           fill=WHITE, width=s)

    # THE RED WEDGE, from the upper left, tip buried in the disc
    tip = (cx + 6 * s, cy - 2 * s)
    wedge = [(0, 30 * s), (0, 116 * s), tip]
    dr.polygon(wedge, fill=RED)

    # small hard geometry scattered on the white field
    dr.rectangle([304 * s, 22 * s, 384 * s, 30 * s], fill=BLACK)
    dr.rectangle([304 * s, 38 * s, 356 * s, 44 * s], fill=BLACK)
    dr.ellipse([160 * s, 24 * s, 184 * s, 48 * s], outline=BLACK, width=2 * s)
    dr.ellipse([196 * s, 60 * s, 208 * s, 72 * s], fill=RED)

    # big date numerals on the white field, red square full stop
    f_big = font(FONT_SANS_B, 56 * s)
    dr.text((26 * s, 138 * s), "31", font=f_big, fill=BLACK)
    dr.rectangle([32 * s, 212 * s, 46 * s, 226 * s], fill=RED)

    # slogan on the black field
    f_a = font(FONT_SANS_B, 12 * s)
    f_b = font(FONT_SANS, 9 * s)
    dr.text(((W - 14) * s, (H - 44) * s), "BEAT THE MOONLIGHT",
            font=f_a, fill=WHITE, anchor="rs")
    dr.text(((W - 14) * s, (H - 28) * s), "WITH THE RED WEDGE",
            font=f_a, fill=RED, anchor="rs")
    dr.text(((W - 14) * s, (H - 13) * s),
            "after El Lissitzky, 1919 — for tonight's fireballs",
            font=f_b, fill=WHITE, anchor="rs")
    return finalize(img, dither=False)


# ------------------------------------------------------- 3. Kamon generator
def kamon_ring(dr, cx, cy, R, s, w=3.5, double=True):
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLACK,
               width=int(w * s))
    if double:
        r2 = R - int(6.5 * s)
        dr.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=BLACK,
                   width=s)


def petal_poly(base_r, length, width, ang, cx, cy):
    pts_l, pts_r = [], []
    for i in range(13):
        t = i / 12
        rr = base_r + length * t
        ww = width * math.sin(math.pi * t) ** 0.85
        pts_l.append((rr, -ww / 2))
        pts_r.append((rr, ww / 2))
    poly = pts_l + pts_r[::-1]
    poly = [(cx + x, cy + y) for x, y in poly]
    return rotpts(poly, ang, cx, cy)


def draw_crest(dr, img, cx, cy, R, seed, color, s, recipe):
    rng = random.Random(seed)
    kamon_ring(dr, cx, cy, R, s, double=rng.random() < 0.6)
    inner = R - 12 * s
    k = rng.choice([5, 6, 8]) if recipe != "rays" else rng.choice([6, 8, 12])
    a0 = rng.uniform(0, math.pi)

    if recipe == "orbit":
        orb = inner * rng.uniform(0.58, 0.68)
        r0 = inner * rng.uniform(0.2, 0.26)
        hollow = rng.random() < 0.5
        for i in range(k):
            a = a0 + 2 * math.pi * i / k
            x, y = cx + orb * math.cos(a), cy + orb * math.sin(a)
            if hollow:
                dr.ellipse([x - r0, y - r0, x + r0, y + r0], outline=color,
                           width=int(2.5 * s))
            else:
                dr.ellipse([x - r0, y - r0, x + r0, y + r0], fill=color)
        rc = inner * 0.2
        dr.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=color)

    elif recipe == "petals":
        L = inner * 0.82
        wd = 2 * math.pi * inner * 0.78 / k * rng.uniform(0.62, 0.8)
        for i in range(k):
            a = a0 + 2 * math.pi * i / k
            dr.polygon(petal_poly(inner * 0.12, L, wd, a, cx, cy), fill=color)
        rc = inner * 0.16
        dr.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=WHITE)
        dr.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], outline=color,
                   width=int(2 * s))

    elif recipe == "rays":
        swirl = rng.uniform(0.25, 0.5) * rng.choice([-1, 1])
        for i in range(k):
            a = a0 + 2 * math.pi * i / k
            base_w = 2 * math.pi * inner * 0.3 / k * 0.7
            p = [(cx + inner * 0.18 * math.cos(a - base_w / inner),
                  cy + inner * 0.18 * math.sin(a - base_w / inner)),
                 (cx + inner * 0.18 * math.cos(a + base_w / inner),
                  cy + inner * 0.18 * math.sin(a + base_w / inner)),
                 (cx + inner * 0.94 * math.cos(a + swirl),
                  cy + inner * 0.94 * math.sin(a + swirl))]
            dr.polygon(p, fill=color)
        rc = inner * 0.14
        dr.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=color)

    elif recipe == "geo":
        # nested squares/diamonds
        n = rng.choice([3, 4])
        for i in range(n):
            rr = inner * (0.92 - 0.26 * i)
            ang = a0 + (math.pi / 4 if i % 2 else 0)
            pts = [(cx + rr * math.cos(ang + j * math.pi / 2),
                    cy + rr * math.sin(ang + j * math.pi / 2))
                   for j in range(4)]
            dr.polygon(pts, outline=color, width=int(2.8 * s))
        rc = inner * 0.12
        dr.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=color)

    elif recipe == "crescents":
        # k crescents chasing each other around the centre
        orb = inner * 0.55
        r0 = inner * 0.3
        for i in range(k if k <= 6 else 5):
            kk = min(k, 5)
            a = a0 + 2 * math.pi * i / kk
            x, y = cx + orb * math.cos(a), cy + orb * math.sin(a)
            dr.ellipse([x - r0, y - r0, x + r0, y + r0], fill=color)
        for i in range(k if k <= 6 else 5):
            kk = min(k, 5)
            a = a0 + 2 * math.pi * i / kk
            x, y = cx + orb * math.cos(a), cy + orb * math.sin(a)
            ox = 0.42 * r0 * math.cos(a + math.pi / 2)
            oy = 0.42 * r0 * math.sin(a + math.pi / 2)
            dr.ellipse([x - r0 + ox, y - r0 + oy, x + r0 + ox, y + r0 + oy],
                       fill=WHITE)

    elif recipe == "tsuki":
        # 月に星 — moon and star, the crest of the Chiba clan, in red:
        # tonight's moon deserves a crest
        r0 = inner * 0.62
        dr.ellipse([cx - r0, cy - r0, cx + r0, cy + r0], fill=color)
        off = r0 * 0.46
        dr.ellipse([cx - r0 + off, cy - r0 - off * 0.2,
                    cx + r0 + off, cy + r0 - off * 0.2], fill=WHITE)
        rs_ = inner * 0.2
        sx, sy = cx + inner * 0.34, cy + inner * 0.1
        dr.ellipse([sx - rs_, sy - rs_, sx + rs_, sy + rs_], fill=color)


def image3_kamon():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    R = 55 * s
    centers = [(67, 70), (200, 70), (333, 70), (67, 200), (200, 200),
               (333, 200)]
    recipes = ["orbit", "petals", "rays", "geo", "crescents", "tsuki"]
    for i, ((cx, cy), rc) in enumerate(zip(centers, recipes)):
        col = RED if rc == "tsuki" else BLACK
        if rc == "tsuki":
            dr.ellipse([cx * s - R, cy * s - R, cx * s + R, cy * s + R],
                       outline=RED, width=int(3.5 * s))
            draw_crest(dr, img, cx * s, cy * s, R, 20260731 + i, RED, s, rc)
        else:
            draw_crest(dr, img, cx * s, cy * s, R, 20260731 + i, col, s, rc)

    f_jp = font(FONT_JP, 18 * s)
    f_jp_s = font(FONT_JP, 9 * s)
    f_cb = font(FONT_SANS_B, 9 * s)
    y = 268
    dr.text((14 * s, y * s), "家紋", font=f_jp, fill=RED)
    dr.text((56 * s, (y + 4) * s),
            "KAMON — six crests that did not exist yesterday",
            font=f_cb, fill=BLACK)
    dr.text((56 * s, (y + 16) * s),
            "last one: 月に星 (moon and star), for tonight's 98% moon",
            font=f_jp_s, fill=BLACK)
    return finalize(img, dither=False)


# ------------------------------------------------------- 4. US Patent No. 1
def image4_patent():
    """July 31, 1790: the first United States patent, signed by George
    Washington, granted to Samuel Hopkins for an improved way of making
    potash. Drawn like a patent sheet."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    dr.rectangle([6 * s, 6 * s, (W - 6) * s, (H - 6) * s], outline=BLACK,
                 width=s)
    dr.rectangle([10 * s, 10 * s, (W - 10) * s, (H - 10) * s], outline=BLACK,
                 width=s)

    f_h1 = font(FONT_SERIF_B, 16 * s)
    f_h2 = font(FONT_SERIF, 10 * s)
    f_sm = font(FONT_SERIF, 9 * s)
    f_no = font(FONT_SERIF_B, 13 * s)
    cx = W * s // 2
    dr.text((cx, 20 * s), "UNITED STATES PATENT", font=f_h1, fill=BLACK,
            anchor="ma")
    dr.text((cx, 42 * s), "granted this day, July 31, 1790, to Samuel Hopkins",
            font=f_h2, fill=BLACK, anchor="ma")
    dr.text((cx, 56 * s),
            "for an improvement in the making of Pot ash and Pearl ash",
            font=f_sm, fill=BLACK, anchor="ma")
    dr.text(((W - 22) * s, 22 * s), "No. 1", font=f_no, fill=RED, anchor="ra")
    dr.line([60 * s, 72 * s, (W - 60) * s, 72 * s], fill=BLACK, width=s)

    # ---- Fig. 1: the potash kettle on its furnace, hatched like an engraving
    fx, fy = 150 * s, 200 * s   # furnace centre-ish
    # furnace body
    fw, fh = 108 * s, 78 * s
    dr.rectangle([fx - fw // 2, fy - fh // 2, fx + fw // 2, fy + fh // 2],
                 outline=BLACK, width=int(1.8 * s))
    # diagonal hatching on the furnace body
    step = 8 * s
    x0, y0 = fx - fw // 2, fy - fh // 2
    x1, y1 = fx + fw // 2, fy + fh // 2
    for i in range(-20, 40):
        xa = x0 + i * step
        pts = []
        p1 = (xa, y1)
        p2 = (xa + fh, y1 - fh)
        # clip by drawing only within box via line intersection: cheap clamp
        if p2[0] < x0 or p1[0] > x1:
            continue
        dr.line([max(p1[0], x0), y1 - max(0, x0 - p1[0]),
                 min(p2[0], x1), y1 - fh + max(0, p2[0] - x1)],
                fill=BLACK, width=s)
    # firebox arch, black, with red fire
    ax, ay, aw, ah = fx, y1, 46 * s, 40 * s
    dr.pieslice([ax - aw // 2, ay - ah, ax + aw // 2, ay + ah], 180, 360,
                fill=WHITE, outline=BLACK, width=int(1.5 * s))
    flame_rng = random.Random(1790)
    for i in range(5):
        bx = ax - aw // 2 + (i + 0.5) * aw / 5
        hgt = flame_rng.uniform(0.4, 0.95) * (ah - 6 * s)
        dr.polygon([(bx - 3.5 * s, ay), (bx + 3.5 * s, ay), (bx, ay - hgt)],
                   fill=RED)
    # kettle sitting on top: wide-mouth pot
    kw_top, kw_bot, kh = 96 * s, 64 * s, 46 * s
    ky1 = y0
    ky0 = ky1 - kh
    pot = [(fx - kw_top // 2, ky0), (fx + kw_top // 2, ky0),
           (fx + kw_bot // 2, ky1), (fx - kw_bot // 2, ky1)]
    dr.polygon(pot, outline=BLACK, width=int(1.8 * s))
    # sparse vertical hatching on the pot
    for i in range(1, 8):
        t = i / 8
        xt = fx - kw_top // 2 + t * kw_top
        xb = fx - kw_bot // 2 + t * kw_bot
        dr.line([xt, ky0 + 2 * s, xb, ky1 - 2 * s], fill=BLACK, width=s)
    # rim
    dr.rectangle([fx - kw_top // 2 - 5 * s, ky0 - 6 * s,
                  fx + kw_top // 2 + 5 * s, ky0], outline=BLACK,
                 width=int(1.8 * s))
    # steam curls
    for (sx0, amp) in [(fx - 26 * s, 9), (fx, 12), (fx + 26 * s, 9)]:
        pts = []
        for j in range(26):
            t = j / 25
            pts.append((sx0 + amp * s * math.sin(t * math.pi * 2.6),
                        ky0 - 10 * s - t * 34 * s))
        dr.line(pts, fill=BLACK, width=s)

    dr.text((fx, (y1 + 12 * s)), "Fig. 1.", font=font(FONT_SERIF_B, 10 * s),
            fill=BLACK, anchor="ma")

    # labels with leader lines
    f_lb = font(FONT_SERIF_B, 11 * s)
    labels = [("A", fx + kw_top // 2 + 26 * s, ky0 + 6 * s,
               fx + kw_top // 2 - 4 * s, ky0 + 12 * s, "the kettle"),
              ("B", fx - fw // 2 - 26 * s, fy - 6 * s,
               fx - fw // 2 + 3 * s, fy, "the furnace"),
              ("C", fx + fw // 2 + 26 * s, y1 - 12 * s,
               ax + aw // 2 - 6 * s, y1 - 10 * s, "the fire")]
    for lab, lx, ly, tx, ty, _ in labels:
        dr.line([lx, ly, tx, ty], fill=BLACK, width=s)
        dr.text((lx, ly - 6 * s), lab, font=f_lb, fill=BLACK, anchor="ma")

    # ---- right column: the story
    rx = 268 * s
    f_tx = font(FONT_SERIF, 9.5 * s)
    lines = [
        "The whole patent system",
        "of the United States",
        "begins here: with better",
        "ashes.  Potash — burnt",
        "hardwood, boiled down in",
        "iron kettles — was young",
        "America's first industrial",
        "chemical: soap, glass,",
        "gunpowder, fertilizer.",
        "",
        "Three patents were issued",
        "in 1790.  Examined and",
        "signed by the President",
        "himself.",
    ]
    yy = 92
    for ln in lines:
        dr.text((rx, yy * s), ln, font=f_tx, fill=BLACK)
        yy += 12

    # signature
    f_sig = font(FONT_SERIF, 12 * s)
    dr.text((rx, (yy + 4) * s), "Geo. Washington", font=f_sig, fill=BLACK)
    dr.line([rx, (yy + 18) * s, rx + 92 * s, (yy + 18) * s], fill=BLACK,
            width=s)
    dr.text((rx, (yy + 21) * s), "President", font=f_sm, fill=BLACK)

    # red wax seal, bottom left area
    sx, sy, sr = 52 * s, 252 * s, 22 * s
    srng = random.Random(31)
    scallop = []
    for i in range(28):
        a = 2 * math.pi * i / 28
        rr = sr * (1.0 + 0.09 * (i % 2))
        scallop.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
    dr.polygon(scallop, fill=RED)
    dr.ellipse([sx - sr * 0.72, sy - sr * 0.72, sx + sr * 0.72,
                sy + sr * 0.72], outline=WHITE, width=s)
    dr.text((sx, sy), "US", font=font(FONT_SERIF_B, 13 * s), fill=WHITE,
            anchor="mm")
    return finalize(img, dither=False)


# --------------------------------------------- 5. The 1715 fleet, seigaiha
def image5_fleet():
    """July 31, 1715: eleven ships of the Spanish treasure fleet sink in a
    hurricane off Florida. The sea is drawn as seigaiha — 'blue ocean waves'
    — and keeps the silver."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    sea_y = 118  # waterline

    # ---- the galleon, stern up, sliding under (drawn first; waves overlap)
    gx, gy = 236, 104   # roughly where hull meets water
    tilt = math.radians(-24)

    def T(pts):
        return [(x * s, y * s) for x, y in
                rotpts([(gx + px, gy + py) for px, py in pts], tilt, gx, gy)]

    hull = [(-70, 0), (66, 0), (54, 22), (-48, 22)]
    dr.polygon(T(hull), fill=BLACK)
    # raised stern castle
    dr.polygon(T([(42, -18), (66, -18), (66, 0), (42, 0)]), fill=BLACK)
    # masts + yards + rag sails
    for (mx_, mh, yw) in [(-38, 66, 34), (2, 84, 44), (40, 60, 28)]:
        dr.line(T([(mx_, 0), (mx_, -mh)]), fill=BLACK, width=int(2.2 * s))
        dr.line(T([(mx_ - yw / 2, -mh + 10), (mx_ + yw / 2, -mh + 10)]),
                fill=BLACK, width=int(1.6 * s))
        # torn sail: a sagging triangle from the yard
        dr.polygon(T([(mx_ - yw / 2 + 3, -mh + 12), (mx_ + yw / 2 - 3, -mh + 12),
                      (mx_ + 2, -mh + 34)]), fill=BLACK)
    # bowsprit dipping into the sea
    dr.line(T([(-70, 2), (-96, 14)]), fill=BLACK, width=int(2 * s))

    # storm strokes in the sky
    wrng = random.Random(1715)
    for _ in range(26):
        x = wrng.uniform(8, W - 60)
        y = wrng.uniform(12, sea_y - 30)
        ln = wrng.uniform(14, 42)
        if abs(x - gx) < 80 and y > 30:
            continue
        if x < 225 and y < 60:   # keep the title clear
            continue
        dr.line([x * s, y * s, (x + ln) * s, (y - ln * 0.12) * s],
                fill=BLACK, width=s)

    # ---- seigaiha sea
    R = 30
    stepx, stepy = R, int(R * 0.38)  # overlap
    rings = [1.0, 0.74, 0.48, 0.22]
    row = 0
    y = sea_y + 24   # first row sits low enough to leave the hull half-visible
    while y < H + R:
        xoff = 0 if row % 2 == 0 else R // 2 - R  # offset alternate rows
        x = xoff - R
        while x < W + R:
            xs, ys = x * s, y * s
            dr.ellipse([xs - R * s, ys - R * s, xs + R * s, ys + R * s],
                       fill=WHITE)
            for rr in rings:
                rr *= R * s
                dr.ellipse([xs - rr, ys - rr, xs + rr, ys + rr],
                           outline=BLACK, width=int(1.6 * s))
            x += stepx
        y += stepy
        row += 1

    # ---- pieces of eight, sinking between the waves
    coin_rng = random.Random(88)
    coins = [(120, 160), (140, 205), (117, 248), (258, 172), (243, 222),
             (276, 262), (196, 190), (186, 245)]
    for (cx_, cy_) in coins:
        r0 = coin_rng.uniform(5.5, 7.5) * s
        cx_, cy_ = cx_ * s, cy_ * s
        dr.ellipse([cx_ - r0, cy_ - r0, cx_ + r0, cy_ + r0], fill=RED)
        dr.line([cx_ - r0 * 0.5, cy_, cx_ + r0 * 0.5, cy_], fill=WHITE,
                width=s)
        dr.line([cx_, cy_ - r0 * 0.5, cx_, cy_ + r0 * 0.5], fill=WHITE,
                width=s)

    # ---- captions
    f_t = font(FONT_SERIF_B, 14 * s)
    f_m = font(FONT_SERIF, 9 * s)
    dr.text((14 * s, 12 * s), "31 JULY 1715", font=f_t, fill=RED)
    dr.text((14 * s, 32 * s), "the Spanish plate fleet — eleven ships —",
            font=f_m, fill=BLACK)
    dr.text((14 * s, 44 * s), "lost to a hurricane off the Florida coast",
            font=f_m, fill=BLACK)
    # caption plate at the bottom so it reads over the waves
    dr.rectangle([94 * s, (H - 26) * s, 306 * s, (H - 8) * s], fill=WHITE,
                 outline=BLACK, width=s)
    dr.text((200 * s, (H - 17) * s),
            "the sea kept the silver for 250 years",
            font=f_m, fill=BLACK, anchor="mm")
    return finalize(img, dither=False)


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_moonwashed, image2_red_wedge, image3_kamon,
              image4_patent, image5_fleet]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", len(cols))
