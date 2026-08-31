#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-08-31 (day 2: last day of summer).

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Tonal scenes render at 3x, LANCZOS downscale,
Floyd-Steinberg dither into the exact palette; hard-edged pieces render at
3x and quantize without dither so AA edges snap crisp.

Today: Threepenny Opera premiere (Berlin, 31 Aug 1928); Japan's Vegetable
Day (8/31 = ya-sa-i goroawase); the last day of meteorological summer;
the September 2026 sky; and a Truchet tiling from the backlog.
"""

import math
import os
import random
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
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
if not os.path.exists(FONT_JP):
    FONT_JP = FONT_SANS_B  # fallback; kana will not render but nothing crashes


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


def fit_font(path, text, target_w, start):
    """Largest font size <= start (1x units) rendering text within target_w (1x)."""
    size = start
    while size > 8:
        f = font(path, size * SS)
        bb = f.getbbox(text)
        if bb[2] - bb[0] <= target_w * SS:
            return f
        size -= 1
    return font(path, size * SS)


# ------------------------------------------------- 1. Die Dreigroschenoper
def image1_dreigroschenoper():
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # top rule + venue line
    dr.line([(20 * s, 26 * s), (380 * s, 26 * s)], fill=WHITE, width=s)
    f_top = font(FONT_MONO, 11 * s)
    dr.text((200 * s, 14 * s), "BERLIN · THEATER AM SCHIFFBAUERDAMM · 1928",
            font=f_top, fill=WHITE, anchor="mm")

    # stacked flush-left title, Weimar style
    x = 22 * s
    f_die = font(FONT_SANS_B, 26 * s)
    dr.text((x, 34 * s), "DIE", font=f_die, fill=WHITE)
    f_drei = fit_font(FONT_SANS_B, "DREIGROSCHEN", 356, 52)
    dr.text((x, 62 * s), "DREIGROSCHEN", font=f_drei, fill=RED)
    f_oper = font(FONT_SANS_B, 52 * s)
    dr.text((x, 108 * s), "OPER", font=f_oper, fill=WHITE)
    # red square bullet after OPER
    ob = dr.textbbox((x, 108 * s), "OPER", font=f_oper)
    dr.rectangle([ob[2] + 8 * s, ob[3] - 14 * s, ob[2] + 22 * s, ob[3]], fill=RED)

    # the Moritat shark — red silhouette, swimming left
    def P(pts):
        return [(px * s, py * s) for px, py in pts]

    body = P([
        (28, 218),            # nose tip
        (60, 205), (100, 196), (150, 190),
        (172, 186),           # before dorsal
        (185, 158), (204, 152), (207, 183),   # dorsal fin
        (250, 184), (300, 188), (340, 193),
        (378, 172),           # upper tail tip
        (357, 199),           # tail notch
        (384, 228),           # lower tail tip
        (338, 212), (300, 214), (250, 218),
        (205, 224),
        (185, 252), (163, 258), (168, 228),   # pectoral fin
        (120, 232), (70, 233),
    ])
    dr.polygon(body, fill=RED)
    # mouth
    dr.line(P([(30, 221), (55, 226), (92, 229)]), fill=BLACK, width=2 * s)
    # teeth: white triangles hanging from the mouth line
    for i, (tx, ty) in enumerate([(38, 222.5), (50, 224.5), (62, 226.2),
                                  (74, 227.4), (86, 228.4)]):
        dr.polygon(P([(tx - 3.4, ty), (tx + 3.4, ty), (tx, ty + 6.5)]), fill=WHITE)
    # eye
    dr.ellipse([56 * s, 206 * s, 66 * s, 216 * s], fill=WHITE)
    dr.ellipse([59 * s, 209 * s, 63 * s, 213 * s], fill=BLACK)
    # gill slits
    for gx in (116, 126, 136):
        dr.arc([(gx - 8) * s, 200 * s, (gx + 8) * s, 228 * s], 300, 60,
               fill=BLACK, width=2 * s)

    # quote + credits
    f_q = font(FONT_SERIF, 12 * s)
    dr.text((200 * s, 271 * s), "„Und der Haifisch, der hat Zähne …“",
            font=f_q, fill=WHITE, anchor="mm")
    f_c = font(FONT_MONO, 10 * s)
    dr.text((200 * s, 288 * s), "BRECHT × WEILL · URAUFFÜHRUNG 31. VIII. 1928 · HEUTE VOR 98 JAHREN",
            font=f_c, fill=RED, anchor="mm")
    return finalize(img, dither=False)


# ------------------------------------------------------- 2. Yasai no Hi
def image2_yasai():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    dr.rectangle([3 * s, 3 * s, W * s - 3 * s, H * s - 3 * s],
                 outline=BLACK, width=s)

    # header
    f_title = font(FONT_JP, 40 * s)
    dr.text((22 * s, 14 * s), "野菜の日", font=f_title, fill=BLACK)
    # red date seal
    dr.ellipse([320 * s, 12 * s, 382 * s, 74 * s], fill=RED)
    f_seal = font(FONT_SANS_B, 17 * s)
    dr.text((351 * s, 34 * s), "8/31", font=f_seal, fill=WHITE, anchor="mm")
    f_seal2 = font(FONT_JP, 11 * s)
    dr.text((351 * s, 53 * s), "記念日", font=f_seal2, fill=WHITE, anchor="mm")
    # goroawase subline
    f_sub = font(FONT_JP, 14 * s)
    dr.text((24 * s, 62 * s), "ごろあわせ： ８(や)・３(さ)・１(い) = やさい",
            font=f_sub, fill=BLACK)

    # 3 x 2 grid of vegetables
    cells = [(24 + c * 120, 92 + r * 100) for r in range(2) for c in range(3)]
    f_lab = font(FONT_JP, 14 * s)

    def label(cx, cy, txt):
        dr.text((cx * s, cy * s), txt, font=f_lab, fill=BLACK, anchor="mm")

    # --- daikon
    cx, cy = cells[0][0] + 56, cells[0][1] + 34
    body = [(cx - 12, cy - 22), (cx + 12, cy - 22), (cx + 9, cy + 10),
            (cx + 3, cy + 28), (cx - 3, cy + 28), (cx - 9, cy + 10)]
    dr.polygon([(px * s, py * s) for px, py in body], fill=WHITE, outline=BLACK,
               width=2 * s)
    for wy in (cy - 6, cy + 4, cy + 13):
        dr.line([(cx - 5) * s, wy * s, (cx + 5) * s, (wy + 1) * s],
                fill=BLACK, width=s)
    for ang in (-50, -20, 15, 45):
        a = math.radians(ang - 90)
        dr.line([cx * s, (cy - 22) * s,
                 (cx + 24 * math.cos(a)) * s, (cy - 22 + 24 * math.sin(a)) * s],
                fill=BLACK, width=3 * s)
    label(cells[0][0] + 56, cells[0][1] + 78, "だいこん")

    # --- tomato
    cx, cy = cells[1][0] + 56, cells[1][1] + 36
    dr.ellipse([(cx - 24) * s, (cy - 21) * s, (cx + 24) * s, (cy + 21) * s], fill=RED)
    for ang in range(0, 360, 72):  # calyx star
        a = math.radians(ang - 90)
        dr.line([cx * s, (cy - 12) * s,
                 (cx + 13 * math.cos(a)) * s, (cy - 12 + 9 * math.sin(a)) * s],
                fill=BLACK, width=3 * s)
    dr.arc([(cx - 17) * s, (cy - 15) * s, (cx + 6) * s, (cy + 8) * s],
           170, 250, fill=WHITE, width=3 * s)
    label(cells[1][0] + 56, cells[1][1] + 78, "とまと")

    # --- nasu (eggplant)
    cx, cy = cells[2][0] + 56, cells[2][1] + 38
    egg = Image.new("RGBA", (80 * s, 80 * s), (0, 0, 0, 0))
    ed = ImageDraw.Draw(egg)
    ed.ellipse([22 * s, 8 * s, 58 * s, 68 * s], fill=BLACK)
    egg = egg.rotate(28, resample=Image.BICUBIC, center=(40 * s, 38 * s))
    img.paste(egg, ((cx - 40) * s, (cy - 40) * s), egg)
    # red calyx at the top
    tipx, tipy = cx + 13, cy - 26
    for ang in (150, 195, 240, 285):
        a = math.radians(ang)
        dr.line([tipx * s, tipy * s,
                 (tipx + 14 * math.cos(a)) * s, (tipy + 14 * math.sin(a)) * s],
                fill=RED, width=4 * s)
    dr.line([tipx * s, tipy * s, (tipx + 8) * s, (tipy - 10) * s],
            fill=RED, width=4 * s)
    dr.arc([(cx - 18) * s, (cy - 6) * s, (cx + 4) * s, (cy + 20) * s],
           110, 200, fill=WHITE, width=3 * s)
    label(cells[2][0] + 56, cells[2][1] + 78, "なす")

    # --- ninjin (carrot)
    cx, cy = cells[3][0] + 56, cells[3][1] + 36
    dr.polygon([(cx - 13) * s, (cy - 18) * s, (cx + 13) * s, (cy - 18) * s,
                (cx + 2) * s, (cy + 28) * s, (cx - 2) * s, (cy + 28) * s],
               fill=RED)
    for t in (0.22, 0.5, 0.78):
        yy = cy - 18 + t * 40
        half = 12 * (1 - t * 0.75)
        dr.line([(cx - half) * s, yy * s, (cx + half) * s, (yy + 1) * s],
                fill=BLACK, width=s)
    for ang in (-40, 0, 40):
        a = math.radians(ang - 90)
        dr.line([cx * s, (cy - 18) * s,
                 (cx + 20 * math.cos(a)) * s, (cy - 18 + 20 * math.sin(a)) * s],
                fill=BLACK, width=3 * s)
    label(cells[3][0] + 56, cells[3][1] + 78, "にんじん")

    # --- negi (welsh onion)
    cx, cy = cells[4][0] + 56, cells[4][1] + 36
    for i, dx in enumerate((-14, 0, 14)):
        top = cy - 28 - (4 if i == 1 else 0)
        # white stalk
        dr.rectangle([(cx + dx - 4) * s, (cy - 2) * s,
                      (cx + dx + 4) * s, (cy + 28) * s],
                     fill=WHITE, outline=BLACK, width=2 * s)
        # dark green top, drawn black, with a slanted cut
        dr.polygon([(cx + dx - 4) * s, (cy - 2) * s,
                    (cx + dx - 4) * s, (top + 6) * s,
                    (cx + dx + 4) * s, top * s,
                    (cx + dx + 4) * s, (cy - 2) * s], fill=BLACK)
        dr.line([(cx + dx - 2) * s, (cy + 4) * s,
                 (cx + dx - 2) * s, (cy + 22) * s], fill=BLACK, width=s)
    label(cells[4][0] + 56, cells[4][1] + 78, "ねぎ")

    # --- kabocha (pumpkin)
    cx, cy = cells[5][0] + 56, cells[5][1] + 38
    dr.ellipse([(cx - 26) * s, (cy - 18) * s, (cx + 26) * s, (cy + 22) * s],
               fill=BLACK)
    for k in (-0.62, -0.22, 0.22, 0.62):
        dr.arc([(cx - 26 + 20 * abs(k)) * s, (cy - 18) * s,
                (cx + 26 - 20 * abs(k)) * s, (cy + 22) * s],
               (90 if k < 0 else 270) - 88, (90 if k < 0 else 270) + 88,
               fill=WHITE, width=2 * s)
    dr.rectangle([(cx - 3) * s, (cy - 26) * s, (cx + 3) * s, (cy - 14) * s],
                 fill=RED)
    label(cells[5][0] + 56, cells[5][1] + 78, "かぼちゃ")

    return finalize(img, dither=False)


# --------------------------------------------------- 3. Natsu no owari
def image3_natsu_no_owari():
    rng = random.Random(20260831)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    horizon = 196

    # dusk sky: light at zenith, heavier toward the horizon
    for y in range(0, horizon * s):
        t = y / (horizon * s)
        g = int(250 - 65 * (t ** 1.6))
        dr.line([(0, y), (W * s, y)], fill=(g, g, g))

    # the sun, low and huge
    sun_cx, sun_cy, sun_r = 208, 178, 52
    dr.ellipse([(sun_cx - sun_r) * s, (sun_cy - sun_r) * s,
                (sun_cx + sun_r) * s, (sun_cy + sun_r) * s], fill=RED)
    # thin cloud bars crossing the sun
    for (cy_, hh, x0, x1) in [(150, 4, 120, 305), (166, 6, 90, 330), (183, 5, 140, 290)]:
        dr.rectangle([x0 * s, cy_ * s, x1 * s, (cy_ + hh) * s], fill=(70, 70, 70))

    # far birds
    for (bx, by, bw) in [(85, 70, 9), (103, 78, 7), (300, 55, 8), (322, 63, 6), (68, 88, 6)]:
        dr.arc([(bx - bw) * s, (by - 4) * s, bx * s, (by + 4) * s], 200, 330,
               fill=BLACK, width=s)
        dr.arc([bx * s, (by - 4) * s, (bx + bw) * s, (by + 4) * s], 210, 340,
               fill=BLACK, width=s)

    # sea: darkens toward the bottom
    for y in range(horizon * s, H * s):
        t = (y - horizon * s) / ((H - horizon) * s)
        g = int(135 - 95 * t)
        dr.line([(0, y), (W * s, y)], fill=(g, g, g))
    for i in range(80):  # light streaks
        y = horizon + 2 + (i / 80) ** 1.4 * (H - horizon - 6)
        x = rng.uniform(0, W)
        ln = rng.uniform(8, 40) * (0.4 + (y - horizon) / (H - horizon))
        g = rng.randint(180, 240)
        dr.line([x * s, y * s, (x + ln) * s, y * s], fill=(g, g, g), width=s)
    # red glitter path under the sun
    for i in range(60):
        y = horizon + 3 + (i / 60) ** 1.25 * (H - horizon - 10)
        spread = 14 + 40 * (y - horizon) / (H - horizon)
        x = sun_cx + rng.uniform(-spread, spread)
        ln = rng.uniform(8, 24) * (0.5 + (y - horizon) / (H - horizon))
        dr.line([(x - ln / 2) * s, y * s, (x + ln / 2) * s, y * s],
                fill=RED, width=2 * s)

    # branch from the top-right corner, slender leaves
    pts = [(400, 22), (352, 30), (306, 42), (272, 54), (252, 64)]
    for i in range(len(pts) - 1):
        w_ = int((7 - i * 1.2) * s)
        dr.line([pts[i][0] * s, pts[i][1] * s, pts[i + 1][0] * s, pts[i + 1][1] * s],
                fill=BLACK, width=max(w_, 2 * s))
    for (lx, ly, ang) in [(336, 34, 75), (288, 50, 105), (366, 28, 60), (258, 60, 95)]:
        a = math.radians(ang)
        ex, ey = lx + 30 * math.cos(a), ly + 30 * math.sin(a)
        mx, my = (lx + ex) / 2, (ly + ey) / 2
        n = (-(ey - ly) / 30 * 4, (ex - lx) / 30 * 4)
        dr.polygon([(lx * s, ly * s),
                    ((mx + n[0]) * s, (my + n[1]) * s),
                    (ex * s, ey * s),
                    ((mx - n[0]) * s, (my - n[1]) * s)], fill=BLACK)

    # cicada perched on top of the branch, profile facing left
    ccx, ccy = 310, 30  # body center; branch surface ~y=41 here
    dr.line([(ccx - 8) * s, (ccy + 6) * s, (ccx - 12) * s, (ccy + 12) * s],
            fill=BLACK, width=2 * s)  # legs
    dr.line([(ccx + 1) * s, (ccy + 7) * s, (ccx + 1) * s, (ccy + 13) * s],
            fill=BLACK, width=2 * s)
    dr.line([(ccx + 9) * s, (ccy + 6) * s, (ccx + 13) * s, (ccy + 12) * s],
            fill=BLACK, width=2 * s)
    dr.ellipse([(ccx - 17) * s, (ccy - 7) * s, (ccx + 15) * s, (ccy + 7) * s],
               fill=BLACK)  # body
    dr.ellipse([(ccx - 25) * s, (ccy - 7) * s, (ccx - 11) * s, (ccy + 7) * s],
               fill=BLACK)  # head
    dr.ellipse([(ccx - 25) * s, (ccy - 8) * s, (ccx - 19) * s, (ccy - 2) * s],
               fill=WHITE)  # eye
    dr.ellipse([(ccx - 23) * s, (ccy - 6) * s, (ccx - 21) * s, (ccy - 4) * s],
               fill=BLACK)
    # long wing sweeping back past the tail
    dr.polygon([(ccx - 8) * s, (ccy - 6) * s,
                (ccx + 18) * s, (ccy - 12) * s,
                (ccx + 34) * s, (ccy - 4) * s,
                (ccx + 30) * s, (ccy + 4) * s,
                (ccx + 6) * s, (ccy + 2) * s],
               outline=BLACK, width=2 * s)
    for k in range(3):
        dr.line([(ccx - 2 + k * 3) * s, (ccy - 5 + k) * s,
                 (ccx + 26) * s, (ccy - 6 + k * 4) * s], fill=BLACK, width=s)

    # title on the light sky, top-left
    f_jp = font(FONT_JP, 32 * s)
    dr.text((20 * s, 16 * s), "夏の終わり", font=f_jp, fill=BLACK)
    f_en = font(FONT_MONO, 11 * s)
    dr.text((22 * s, 56 * s), "the last day of summer", font=f_en, fill=BLACK)
    # date low over the dark water, bottom-right
    dr.text((388 * s, 284 * s), "2026.08.31", font=f_en, fill=WHITE, anchor="rm")
    return finalize(img, dither=True)


# ------------------------------------------------ 4. September almanac
def image4_september():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # header band
    dr.rectangle([0, 0, W * s, 52 * s], fill=BLACK)
    dr.rectangle([0, 52 * s, W * s, 56 * s], fill=RED)
    f_h = font(FONT_SANS_B, 24 * s)
    dr.text((16 * s, 8 * s), "SEPTEMBER 2026", font=f_h, fill=WHITE)
    f_hs = font(FONT_MONO, 11 * s)
    dr.text((16 * s, 36 * s), "the sky this month", font=f_hs, fill=RED)
    f_jp = font(FONT_JP, 15 * s)
    dr.text((384 * s, 26 * s), "九月の空", font=f_jp, fill=WHITE, anchor="rm")

    def moon(cx, cy, r, kind, color=BLACK):
        """kind: new | wanc (waning crescent) | waxc | full"""
        bb = [(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s]
        if kind == "new":
            dr.ellipse(bb, fill=color)
            dr.ellipse([(cx - r + 2) * s, (cy - r + 2) * s,
                        (cx + r - 2) * s, (cy + r - 2) * s], fill=WHITE)
            dr.ellipse([(cx - r + 4) * s, (cy - r + 4) * s,
                        (cx + r - 4) * s, (cy + r - 4) * s], fill=color)
        elif kind == "full":
            dr.ellipse(bb, fill=color)
        else:
            dr.ellipse(bb, fill=color)
            off = int(r * 0.72)
            dx = -off if kind == "wanc" else off
            dr.ellipse([(cx - r + dx) * s, (cy - r - 1) * s,
                        (cx + r + dx) * s, (cy + r + 1) * s], fill=WHITE)

    rows = [
        ("SEP  6", "wanc", "waning moon rises with Mars before dawn", False),
        ("SEP 11", "new", "new moon — last dark Milky Way nights", False),
        ("SEP 14", "occ", "the crescent moon OCCULTS VENUS", True),
        ("SEP 18", "venus", "Venus at its brightest all year (evening)", False),
        ("SEP 23", "eq", "autumn equinox — aurora season opens", False),
        ("SEP 26", "harvest", "HARVEST MOON · Neptune at opposition", True),
    ]
    f_d = font(FONT_MONO_B, 14 * s)
    f_t = font(FONT_SANS, 13 * s)
    y0 = 78
    for i, (date, glyph, text, hot) in enumerate(rows):
        cy = y0 + i * 35
        col = RED if hot else BLACK
        dr.text((16 * s, cy * s), date, font=f_d, fill=col, anchor="lm")
        gx = 96
        if glyph in ("wanc", "new", "full"):
            moon(gx, cy, 10, glyph)
        elif glyph == "occ":
            dr.ellipse([(gx + 1) * s, (cy - 5) * s, (gx + 11) * s, (cy + 5) * s],
                       fill=RED)  # Venus slipping behind
            moon(gx, cy, 10, "waxc")
        elif glyph == "venus":
            for ang in range(0, 360, 45):  # bright star
                a = math.radians(ang)
                r2 = 11 if ang % 90 == 0 else 5
                dr.line([gx * s, cy * s,
                         (gx + r2 * math.cos(a)) * s, (cy + r2 * math.sin(a)) * s],
                        fill=RED, width=2 * s)
        elif glyph == "eq":
            dr.ellipse([(gx - 10) * s, (cy - 10) * s, (gx + 10) * s, (cy + 10) * s],
                       outline=BLACK, width=2 * s)
            dr.pieslice([(gx - 10) * s, (cy - 10) * s, (gx + 10) * s, (cy + 10) * s],
                        90, 270, fill=BLACK)
        elif glyph == "harvest":
            moon(gx, cy, 11, "full", color=RED)
        dr.text((120 * s, cy * s), text, font=f_t, fill=col, anchor="lm")
        if i < len(rows) - 1:
            dr.line([16 * s, (cy + 17) * s, 384 * s, (cy + 17) * s],
                    fill=BLACK, width=1)

    f_f = font(FONT_MONO, 10 * s)
    dr.text((200 * s, 290 * s),
            "tonight: waning gibbous · full was Aug 28 · new moon in 11 days",
            font=f_f, fill=BLACK, anchor="mm")
    return finalize(img, dither=False)


# ------------------------------------------------------- 5. Truchet
def image5_truchet():
    rng = random.Random(831 * 2026)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    tile = 25  # 16 x 12 grid
    cols, rows = W // tile, H // tile
    # a red disc of tiles, off-center like a sun behind lattice
    red_cx, red_cy, red_r = 260, 110, 78

    def draw_tile(x, y, size, wline):
        kind = rng.random()
        r = size // 2
        cx, cy = x + size / 2, y + size / 2
        d = math.hypot(cx - red_cx, cy - red_cy)
        col = RED if d < red_r else BLACK
        if kind < 0.44:  # arcs TL + BR
            dr.arc([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s],
                   0, 90, fill=col, width=wline)
            dr.arc([(x + size - r) * s, (y + size - r) * s,
                    (x + size + r) * s, (y + size + r) * s],
                   180, 270, fill=col, width=wline)
        elif kind < 0.88:  # arcs TR + BL
            dr.arc([(x + size - r) * s, (y - r) * s,
                    (x + size + r) * s, (y + r) * s],
                   90, 180, fill=col, width=wline)
            dr.arc([(x - r) * s, (y + size - r) * s,
                    (x + r) * s, (y + size + r) * s],
                   270, 360, fill=col, width=wline)
        else:  # cross
            dr.line([(x + r) * s, y * s, (x + r) * s, (y + size) * s],
                    fill=col, width=wline)
            dr.line([x * s, (y + r) * s, (x + size) * s, (y + r) * s],
                    fill=col, width=wline)

    for i in range(cols):
        for j in range(rows):
            x, y = i * tile, j * tile
            if rng.random() < 0.28:  # subdivide into four small tiles
                h = tile // 2
                for (ax, ay) in ((x, y), (x + h, y), (x, y + h), (x + h, y + h)):
                    draw_tile(ax, ay, h, max(2 * s, int(1.8 * s)))
            else:
                draw_tile(x, y, tile, int(3.6 * s))

    # caption strip
    dr.rectangle([0, (H - 18) * s, W * s, H * s], fill=BLACK)
    f_c = font(FONT_MONO, 9 * s)
    dr.text((200 * s, (H - 9) * s,),
            "TRUCHET TILES · seed 831×2026 · smith arcs, two scales",
            font=f_c, fill=WHITE, anchor="mm")
    return finalize(img, dither=False)


# ---------------------------------------------------------------- main
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    makers = [image1_dreigroschenoper, image2_yasai, image3_natsu_no_owari,
              image4_september, image5_truchet]
    for i, make in enumerate(makers, 1):
        im = make()
        out = os.path.join(here, f"{i}.png")
        im.save(out, optimize=True)
        print(f"saved {out} colors={sorted(set(im.getdata()))}")


if __name__ == "__main__":
    main()
