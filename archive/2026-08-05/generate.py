#!/usr/bin/env python3
"""
e-ink pictures — 2026-08-05 ("The wire, the wedge, the signal")

Five 400x300 images for a black/white/red e-ink panel.

1. The Red Wedge Eclipse — constructivist poster for the 12 Aug 2026 total solar eclipse
2. The Atlantic Telegraph — the first transatlantic cable, completed 5 Aug 1858
3. Perseids — star chart of the radiant, peak 12-13 Aug under a new moon
4. Kamon — date-seeded generative Japanese crest
5. STOP 1914 — the first electric traffic signal, Cleveland, 5 Aug 1914

Render at 3x with AA, LANCZOS downscale, quantize to the exact 3-color palette.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3  # supersample factor
BW, BH = W * S, H * S

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT_DIR = "/usr/share/fonts/truetype"
SANS_BOLD = f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf"
SANS = f"{FONT_DIR}/dejavu/DejaVuSans.ttf"
SERIF_BOLD = f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/dejavu/DejaVuSerif.ttf"
MONO = f"{FONT_DIR}/dejavu/DejaVuSansMono.ttf"
JP = f"{FONT_DIR}/fonts-japanese-gothic.ttf"

OUT_DIR = "images"
ARCHIVE_DIR = "archive/2026-08-05"


def font(path, size):
    return ImageFont.truetype(path, size)


def canvas(bg=WHITE):
    img = Image.new("RGB", (BW, BH), bg)
    return img, ImageDraw.Draw(img)


def finish(img, path, dither=False):
    """Downscale and quantize to the exact 3-color palette."""
    small = img.resize((W, H), Image.LANCZOS)
    pal = Image.new("P", (1, 1))
    pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0] * 759)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    out = small.quantize(palette=pal, dither=d)
    out.save(path, optimize=True)
    print("wrote", path)


def text_w(draw, text, f):
    box = draw.textbbox((0, 0), text, font=f)
    return box[2] - box[0]


def center_text(draw, cx, y, text, f, fill):
    draw.text((cx - text_w(draw, text, f) / 2, y), text, font=f, fill=fill)


# ---------------------------------------------------------------- 1. eclipse

def make_eclipse():
    img, d = canvas(WHITE)

    # sun (red) being overtaken by the moon (black) — mid-eclipse crescent
    sun_c, sun_r = (870, 290), 210
    moon_c, moon_r = (755, 365), 210
    d.ellipse([sun_c[0] - sun_r, sun_c[1] - sun_r,
               sun_c[0] + sun_r, sun_c[1] + sun_r], fill=RED)
    d.ellipse([moon_c[0] - moon_r, moon_c[1] - moon_r,
               moon_c[0] + moon_r, moon_c[1] + moon_r], fill=BLACK)

    # the red wedge, driving up from the lower right toward the dark disk
    d.polygon([(1200, 900), (1200, 772), (700, 555), (760, 655)], fill=RED)
    # a thin black companion beam
    d.line([(1150, 900), (660, 640)], fill=BLACK, width=10)

    # constructivist scaffolding: rules and a small counter-square
    d.line([(70, 120), (70, 560)], fill=BLACK, width=8)
    d.rectangle([46, 96, 94, 144], fill=BLACK)
    d.rectangle([560, 585, 616, 641], fill=RED)
    d.line([(70, 640), (640, 640)], fill=BLACK, width=4)

    # type block
    f_big = font(SANS_BOLD, 88)
    f_date = font(SANS_BOLD, 60)
    f_small = font(SANS_BOLD, 31)
    d.text((110, 130), "TOTAL", font=f_big, fill=BLACK)
    d.text((110, 230), "ECLIPSE", font=f_big, fill=BLACK)
    d.text((110, 330), "OF THE SUN", font=font(SANS_BOLD, 52), fill=BLACK)

    d.text((110, 672), "12 · VIII · 2026", font=f_date, fill=RED)
    d.text((110, 762), "TOTALITY: GREENLAND — ICELAND — SPAIN",
           font=f_small, fill=BLACK)
    d.text((110, 812), "THE PERSEIDS PEAK THE SAME NIGHT · NEW MOON",
           font=f_small, fill=BLACK)

    finish(img, f"{OUT_DIR}/1.png")


# ------------------------------------------------------- 2. atlantic telegraph

MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
}


def draw_morse(d, text, x, y, max_w, unit=7, h=16):
    """Draw morse as printed marks: dot = square, dash = bar. Returns end y."""
    cx, cy = x, y
    for word in text.split():
        # measure word width first
        ww = 0
        for ch in word:
            for sym in MORSE[ch]:
                ww += (unit if sym == "." else unit * 3) + unit
            ww += unit * 2
        if cx + ww > x + max_w:
            cx, cy = x, cy + h + 14
        for ch in word:
            for sym in MORSE[ch]:
                w = unit if sym == "." else unit * 3
                d.rectangle([cx, cy, cx + w, cy + h], fill=BLACK)
                cx += w + unit
            cx += unit * 2  # letter gap
        # word gap marker: small red diamond
        mx, my = cx + unit, cy + h / 2
        r = 5
        d.polygon([(mx, my - r), (mx + r, my), (mx, my + r), (mx - r, my)],
                  fill=RED)
        cx += unit * 5
    return cy + h


def make_telegraph():
    img, d = canvas(WHITE)

    # masthead
    f_title = font(SERIF_BOLD, 64)
    f_sub = font(SERIF, 28)
    center_text(d, BW / 2, 48, "THE ATLANTIC TELEGRAPH", f_title, BLACK)
    d.line([(120, 130), (1080, 130)], fill=BLACK, width=5)
    d.line([(120, 141), (1080, 141)], fill=BLACK, width=2)
    center_text(d, BW / 2, 152,
                "THE FIRST OCEAN CABLE · COMPLETED AUGUST 5, 1858",
                f_sub, BLACK)

    # the sea: wavy engraved lines
    sea_top, sea_bot = 320, 640
    for i, y in enumerate(range(sea_top, sea_bot, 22)):
        pts = []
        for x in range(60, BW - 60 + 1, 12):
            yy = y + 6 * math.sin(x / 55 + i * 1.1)
            pts.append((x, yy))
        d.line(pts, fill=BLACK, width=2)

    # coasts: Newfoundland (west, left) and Ireland (east, right)
    rnd = random.Random(1858)
    left_coast = [(60, sea_top - 30)]
    for y in range(sea_top - 30, sea_bot + 40, 30):
        left_coast.append((150 + rnd.randint(-35, 35), y))
    left_coast += [(60, sea_bot + 40)]
    d.polygon(left_coast, fill=BLACK)
    right_coast = [(BW - 60, sea_top - 30)]
    for y in range(sea_top - 30, sea_bot + 40, 30):
        right_coast.append((BW - 150 + rnd.randint(-35, 35), y))
    right_coast += [(BW - 60, sea_bot + 40)]
    d.polygon(right_coast, fill=BLACK)

    # the cable: a red catenary between the two shores
    x0, y0 = 165, 400
    x1, y1 = BW - 165, 380
    sag = 250
    pts = []
    for t in [i / 100 for i in range(101)]:
        x = x0 + (x1 - x0) * t
        y = (1 - t) * y0 + t * y1 + sag * 4 * t * (1 - t)
        pts.append((x, y))
    d.line(pts, fill=RED, width=9)
    for cx, cy in [(x0, y0), (x1, y1)]:
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=RED,
                  outline=BLACK, width=4)

    # labels (above the coasts, on white)
    f_lab = font(SERIF_BOLD, 27)
    f_lab2 = font(SERIF, 23)
    d.text((80, 212), "HEART'S CONTENT", font=f_lab, fill=BLACK)
    d.text((80, 246), "NEWFOUNDLAND", font=f_lab2, fill=BLACK)
    d.text((BW - 80 - text_w(d, "VALENTIA", f_lab), 212), "VALENTIA",
           font=f_lab, fill=BLACK)
    d.text((BW - 80 - text_w(d, "IRELAND", f_lab2), 246), "IRELAND",
           font=f_lab2, fill=BLACK)
    # sounding note on a cleared card
    f_depth = font(SERIF, 24)
    dep = "— 2,050 FATHOMS BELOW —"
    dw = text_w(d, dep, f_depth)
    d.rectangle([BW / 2 - dw / 2 - 18, 548, BW / 2 + dw / 2 + 18, 596],
                fill=WHITE)
    center_text(d, BW / 2, 556, dep, f_depth, BLACK)

    # morse border: the sentiment of the first official message
    d.line([(90, 690), (BW - 90, 690)], fill=BLACK, width=3)
    end_y = draw_morse(d, "EUROPE AND AMERICA ARE UNITED", 100, 716, BW - 200)
    center_text(d, BW / 2, end_y + 26,
                '"EUROPE AND AMERICA ARE UNITED BY TELEGRAPH"',
                font(SERIF, 26), BLACK)
    center_text(d, BW / 2, end_y + 62, "· 168 YEARS AGO TODAY ·",
                font(SERIF_BOLD, 24), RED)

    finish(img, f"{OUT_DIR}/2.png")


# ---------------------------------------------------------------- 3. perseids

STARS_CAS = [  # (RA hours, Dec deg, radius at 3x, name)
    (0.15, 59.15, 8, "Caph"), (0.675, 56.54, 9, "Schedar"),
    (0.945, 60.72, 8, ""), (1.43, 60.24, 7, "Ruchbah"),
    (1.90, 63.67, 6, ""),
]
STARS_PER = [
    (3.405, 49.86, 10, "Mirfak"), (3.136, 40.96, 8, "Algol"),
    (3.08, 53.51, 7, ""), (3.715, 47.79, 7, ""),
    (3.964, 40.01, 7, ""), (2.845, 55.90, 6, ""), (3.90, 31.88, 7, ""),
]
LINES_CAS = [(4, 3), (3, 2), (2, 1), (1, 0)]  # the W (indices into STARS_CAS)
LINES_PER = [(5, 2), (2, 0), (0, 3), (3, 4), (0, 1), (4, 6)]


def sky_xy(ra, dec):
    ra0, dec0 = 2.05, 50.0
    scale = 26.0  # px per degree at 3x
    x = BW / 2 + (ra - ra0) * 15 * math.cos(math.radians(dec)) * scale * -1
    y = BH / 2 - 60 - (dec - dec0) * scale
    return x, y


def make_perseids():
    img, d = canvas(BLACK)
    rnd = random.Random(812)

    # faint background field
    for _ in range(210):
        x, y = rnd.uniform(0, BW), rnd.uniform(0, BH - 200)
        r = rnd.choice([1, 1, 1, 2, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

    # constellation lines then stars
    for group, lines in [(STARS_CAS, LINES_CAS), (STARS_PER, LINES_PER)]:
        for a, b in lines:
            pa, pb = sky_xy(*group[a][:2]), sky_xy(*group[b][:2])
            d.line([pa, pb], fill=WHITE, width=2)
        for ra, dec, r, name in group:
            x, y = sky_xy(ra, dec)
            d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
            if name:
                d.text((x + 14, y - 8), name, font=font(SANS, 24), fill=WHITE)

    # radiant, between gamma Per and Cassiopeia
    rx, ry = sky_xy(3.1, 57.8)
    for ang in range(0, 360, 30):  # dashed red circle
        a0, a1 = math.radians(ang), math.radians(ang + 16)
        d.arc([rx - 55, ry - 55, rx + 55, ry + 55], math.degrees(a0),
              math.degrees(a1), fill=RED, width=6)
    d.line([(rx - 16, ry), (rx + 16, ry)], fill=RED, width=4)
    d.line([(rx, ry - 16), (rx, ry + 16)], fill=RED, width=4)
    d.text((rx + 66, ry - 46), "RADIANT", font=font(SANS_BOLD, 27), fill=RED)

    # meteors: streaks radiating away from the radiant
    for i in range(11):
        ang = rnd.uniform(0, 2 * math.pi)
        if 0.6 < ang < 2.2 and rnd.random() < 0.5:
            continue  # keep the bottom text band clearer
        d0 = rnd.uniform(130, 430)
        ln = rnd.uniform(90, 240)
        x0 = rx + d0 * math.cos(ang)
        y0 = ry + d0 * math.sin(ang)
        x1 = rx + (d0 + ln) * math.cos(ang)
        y1 = ry + (d0 + ln) * math.sin(ang)
        if not (0 < x0 < BW and 0 < x1 < BW):
            continue
        if not (0 < y0 < BH - 230 and 0 < y1 < BH - 230):
            continue
        col = RED if i % 5 == 0 else WHITE
        d.line([(x0, y0), (x1, y1)], fill=col, width=3)
        d.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=col)

    # almanac band
    d.line([(60, BH - 190), (BW - 60, BH - 190)], fill=WHITE, width=3)
    d.text((70, BH - 165), "PERSEID METEOR SHOWER",
           font=font(SANS_BOLD, 52), fill=WHITE)
    f_red = font(SANS_BOLD, 30)
    f_wht = font(SANS, 30)
    lead = "PEAK 12–13 AUGUST"
    d.text((70, BH - 95), lead, font=f_red, fill=RED)
    d.text((70 + text_w(d, lead, f_red) + 16, BH - 95),
           "· NEW MOON · UP TO 100 METEORS/HR", font=f_wht, fill=WHITE)

    finish(img, f"{OUT_DIR}/3.png")


# ------------------------------------------------------------------- 4. kamon

def petal(cx, cy, theta, r1, r2, half_w, curve=1.0):
    """Polygon for a petal running from radius r1 to r2 at angle theta."""
    pts_out, pts_back = [], []
    n = 24
    for i in range(n + 1):
        t = i / n
        u = r1 + (r2 - r1) * t
        v = half_w * math.sin(math.pi * t) ** curve
        pts_out.append((u, v))
        pts_back.append((u, -v))
    pts = pts_out + pts_back[::-1]
    ct, st = math.cos(theta), math.sin(theta)
    return [(cx + u * ct - v * st, cy + u * st + v * ct) for u, v in pts]


def make_kamon():
    img, d = canvas(WHITE)
    rnd = random.Random(20260805)
    cx, cy = BW / 2, BH / 2 - 40
    R = 330

    # enclosing rings (maru)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLACK, width=22)
    r2 = R - 40
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=BLACK, width=6)

    k = rnd.choice([5, 6, 8])
    base = rnd.uniform(0, 2 * math.pi)

    # primary petals
    p_r1, p_r2 = rnd.uniform(40, 70), r2 - rnd.uniform(30, 55)
    p_w = rnd.uniform(0.5, 0.75) * (math.pi * p_r2 / k) * 0.9
    for i in range(k):
        th = base + 2 * math.pi * i / k
        d.polygon(petal(cx, cy, th, p_r1, p_r2, p_w, curve=1.2), fill=BLACK)
        # white vein inside each petal
        d.polygon(petal(cx, cy, th, p_r1 + 26, p_r2 - 30, p_w * 0.32,
                        curve=1.4), fill=WHITE)

    # secondary marks between petals
    style = rnd.choice(["dots", "wedges", "dots"])
    for i in range(k):
        th = base + 2 * math.pi * (i + 0.5) / k
        mr = (p_r1 + p_r2) * 0.62
        mx, my = cx + mr * math.cos(th), cy + mr * math.sin(th)
        if style == "dots":
            rr = 22
            d.ellipse([mx - rr, my - rr, mx + rr, my + rr], fill=BLACK)
        else:
            d.polygon(petal(cx, cy, th, mr - 50, mr + 50, 16), fill=BLACK)

    # red heart of the crest
    rc = rnd.uniform(30, 44)
    d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=RED,
              outline=BLACK, width=6)

    # caption
    f_jp = font(JP, 46)
    center_text(d, cx, BH - 118, "家紋", f_jp, BLACK)
    center_text(d, cx, BH - 56, "GENERATIVE MON · SEED 2026·08·05",
                font(SANS, 26), BLACK)

    finish(img, f"{OUT_DIR}/4.png")


# --------------------------------------------------------------- 5. stop 1914

def make_stop():
    img, d = canvas(WHITE)

    # letterpress frame
    d.rectangle([24, 24, BW - 24, BH - 24], outline=BLACK, width=10)
    d.rectangle([48, 48, BW - 48, BH - 48], outline=BLACK, width=3)

    # ---- left: the signal
    px = 250  # post center x
    # glow rays behind the red lens
    lx, ly, lr = px, 330, 78
    for ang in range(0, 360, 30):
        a = math.radians(ang + 15)
        x0 = lx + (lr + 26) * math.cos(a)
        y0 = ly + (lr + 26) * math.sin(a)
        x1 = lx + (lr + 86) * math.cos(a)
        y1 = ly + (lr + 86) * math.sin(a)
        d.line([(x0, y0), (x1, y1)], fill=RED, width=9)

    # post and base
    d.rectangle([px - 16, 560, px + 16, 790], fill=BLACK)
    d.polygon([(px - 70, 800), (px + 70, 800), (px + 46, 762), (px - 46, 762)],
              fill=BLACK)
    # signal head
    d.rounded_rectangle([px - 105, 220, px + 105, 570], radius=26, fill=BLACK)
    # red lens (lit) with STOP
    d.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=RED,
              outline=WHITE, width=7)
    f_stop_lens = font(SANS_BOLD, 34)
    center_text(d, lx, ly - 22, "STOP", f_stop_lens, WHITE)
    # green lens (off): hollow
    gy = 480
    d.ellipse([lx - 58, gy - 58, lx + 58, gy + 58], fill=BLACK,
              outline=WHITE, width=7)
    center_text(d, lx, gy - 15, "GO", font(SANS_BOLD, 26), WHITE)

    # ---- right: the type
    tx = 470
    f_date = font(SERIF_BOLD, 36)
    d.text((tx, 105), "AUGUST 5 · 1914", font=f_date, fill=BLACK)
    d.line([(tx, 158), (tx + 620, 158)], fill=BLACK, width=4)

    d.text((tx - 12, 175), "STOP", font=font(SANS_BOLD, 205), fill=RED)

    d.text((tx, 465), "THE FIRST ELECTRIC", font=font(SANS_BOLD, 57),
           fill=BLACK)
    d.text((tx, 540), "TRAFFIC SIGNAL", font=font(SANS_BOLD, 57), fill=BLACK)

    d.line([(tx, 640), (tx + 620, 640)], fill=BLACK, width=4)
    d.text((tx, 660), "EUCLID AVE. & EAST 105TH ST.", font=font(SERIF, 31),
           fill=BLACK)
    d.text((tx, 703), "CLEVELAND, OHIO", font=font(SERIF, 31), fill=BLACK)
    d.text((tx, 760), "TWO COLORED LIGHTS — AND A BUZZER",
           font=font(SANS_BOLD, 27), fill=RED)

    finish(img, f"{OUT_DIR}/5.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    make_eclipse()
    make_telegraph()
    make_perseids()
    make_kamon()
    make_stop()
    for i in range(1, 6):
        Image.open(f"{OUT_DIR}/{i}.png").save(f"{ARCHIVE_DIR}/{i}.png",
                                              optimize=True)
    print("archived to", ARCHIVE_DIR)


if __name__ == "__main__":
    main()
