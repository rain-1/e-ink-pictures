#!/usr/bin/env python3
"""
2026-09-01 — five pictures for a 400x300 black/white/red e-ink screen.

1. martha       — the last passenger pigeon died Sept 1, 1914
2. znanie       — constructivist Knowledge Day poster (Sep 1, first day of school)
3. subway       — America's first subway opened in Boston, Sept 1, 1897
4. almanac      — the September 2026 sky, as a month timeline
5. nihyakutoka  — 二百十日, the 210th day: Japan's traditional storm-watching day
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
S = 3                       # supersample factor
W, H = 400 * S, 300 * S
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT_DIR = "/usr/share/fonts/truetype"
SANS = f"{FONT_DIR}/dejavu/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf"
SERIF = f"{FONT_DIR}/dejavu/DejaVuSerif.ttf"
SERIF_B = f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf"
MONO = f"{FONT_DIR}/dejavu/DejaVuSansMono.ttf"
JP = f"{FONT_DIR}/fonts-japanese-gothic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def save3(img, name, dither=False):
    """Downscale to 400x300 and quantize to the exact 3-color palette."""
    if img.size != (400, 300):
        img = img.resize((400, 300), Image.LANCZOS)
    pal = Image.new("P", (1, 1))
    pal.putpalette([255, 255, 255, 0, 0, 0, 255, 0, 0] + [0] * (256 - 3) * 3)
    out = img.convert("RGB").quantize(
        palette=pal, dither=Image.FLOYDSTEINBERG if dither else Image.NONE
    )
    out.save(os.path.join(HERE, name))
    print("wrote", name)


def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def rotated_text(img, cxy, s, f, angle, fill):
    d0 = ImageDraw.Draw(img)
    b = d0.textbbox((0, 0), s, font=f)
    tw, th = b[2] - b[0] + 8, b[3] - b[1] + 8
    tmp = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((4 - b[0], 4 - b[1]), s, font=f, fill=fill + (255,))
    tmp = tmp.rotate(angle, expand=1, resample=Image.BICUBIC)
    img.paste(tmp, (cxy[0] - tmp.width // 2, cxy[1] - tmp.height // 2), tmp)


# ----------------------------------------------------------------------------
# 1. MARTHA — a sky that was once dark with pigeons, thinning to a single bird
# ----------------------------------------------------------------------------
def martha():
    rng = random.Random(19140901)
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    def bird(x, y, s, color, wdt):
        # a shallow two-arc glyph, like a distant swift
        d.arc([x - s, y - s * 0.5, x, y + s * 0.9], 200, 330, fill=color, width=wdt)
        d.arc([x, y - s * 0.5, x + s, y + s * 0.9], 210, 340, fill=color, width=wdt)

    sky_h = H * 0.66
    # the flock streams left -> right and thins out to nothing;
    # on the left the sky is nearly dark with birds, as the real flocks were
    n = 90000
    for _ in range(n):
        u = rng.random()
        x = u * W * 0.96
        p = math.exp(-4.2 * u)          # density collapses across the panel
        if rng.random() > p:
            continue
        # a loose undulating stream
        band = sky_h * (0.45 + 0.22 * math.sin(u * 4.6 + 0.8))
        y = rng.gauss(band, sky_h * 0.20)
        if not (S * 5 < y < sky_h - S * 4):
            continue
        s = rng.uniform(4.5, 14) * S / 3
        bird(x, y, s, BLACK, max(2, S - 1))

    # one red bird, alone, at the thin end of the sky
    bx, by = W * 0.868, sky_h * 0.44
    bird(bx, by, 9 * S, RED, S + 1)

    # text block
    y0 = int(H * 0.70)
    d.line([W * 0.06, y0, W * 0.94, y0], fill=BLACK, width=S)
    f_name = font(SERIF_B, 34 * S)
    f_sub = font(SERIF, 12 * S)
    f_mono = font(MONO, 9 * S)
    d.text((W * 0.06, y0 + 8 * S), "MARTHA", font=f_name, fill=BLACK)
    nw = text_w(d, "MARTHA", f_name)
    d.text(
        (W * 0.06, y0 + 48 * S),
        "c. 1885 – September 1, 1914 · the last passenger pigeon",
        font=f_sub,
        fill=BLACK,
    )
    d.text(
        (W * 0.06, y0 + 66 * S),
        "1800: five billion birds   1900: the last wild one   1914: none",
        font=f_mono,
        fill=BLACK,
    )
    # small red tally beside her name
    f_tick = font(MONO, 10 * S)
    d.text((W * 0.06 + nw + 12 * S, y0 + 26 * S), "5 000 000 000 → 1 → 0",
           font=f_tick, fill=RED)
    save3(img, "1.png")


# ----------------------------------------------------------------------------
# 2. ЗНАНИЕ — СИЛА: constructivist poster for the first day of school
# ----------------------------------------------------------------------------
def znanie():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # black field: the upper-right diagonal half (the unknown, the dark)
    d.polygon([(W * 0.30, 0), (W, 0), (W, H * 0.78)], fill=BLACK)

    # white circle sitting in the black field
    cx, cy, r = W * 0.665, H * 0.335, H * 0.27
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)

    # the red wedge of knowledge piercing the circle from the lower left
    d.polygon(
        [(0, H * 0.98), (W * 0.10, H * 0.60), (cx + r * 0.20, cy + r * 0.12),
         (W * 0.02, H)],
        fill=RED,
    )
    # wedge tip highlight: thin black edge line continuing the thrust
    d.line([(W * 0.10, H * 0.60), (cx + r * 0.42, cy - r * 0.02)], fill=BLACK,
           width=S)

    # satellite geometry
    d.ellipse([W * 0.85 - 14 * S, H * 0.82 - 14 * S, W * 0.85 + 14 * S,
               H * 0.82 + 14 * S], fill=RED)
    d.rectangle([W * 0.045, H * 0.10, W * 0.075, H * 0.44], fill=BLACK)
    d.rectangle([W * 0.10, H * 0.16, W * 0.115, H * 0.38], fill=RED)
    for i in range(5):
        x = W * 0.60 + i * 9 * S
        d.line([(x, H * 0.86), (x + 22 * S, H * 0.70)], fill=BLACK, width=S)

    # typography
    f_big = font(SANS_B, 34 * S)
    f_small = font(SANS_B, 11 * S)
    f_tiny = font(SANS, 9 * S)
    rotated_text(img, (int(W * 0.315), int(H * 0.735)), "ЗНАНИЕ", f_big, 20,
                 BLACK)
    rotated_text(img, (int(W * 0.685), int(H * 0.545)), "— СИЛА!", f_big, 20,
                 RED)
    d = ImageDraw.Draw(img)
    d.text((W * 0.035, H * 0.015), "1 СЕНТЯБРЯ", font=f_small, fill=BLACK)
    d.text((W * 0.035, H * 0.065), "ДЕНЬ ЗНАНИЙ", font=f_small, fill=RED)
    d.text((W * 0.97, H * 0.955), "knowledge is power · first day of school",
           font=f_tiny, fill=BLACK, anchor="rm")
    save3(img, "2.png")


# ----------------------------------------------------------------------------
# 3. THE FIRST SUBWAY — Boston, September 1, 1897
# ----------------------------------------------------------------------------
def subway():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    f_title = font(SANS_B, 20 * S)
    f_sub = font(SANS, 10 * S)
    f_st = font(SANS_B, 10 * S)
    f_leg = font(SANS, 8.5 * S)

    d.text((W * 0.05, H * 0.045), "AMERICA'S FIRST SUBWAY", font=f_title,
           fill=BLACK)
    d.text((W * 0.05, H * 0.135),
           "Boston · opened September 1, 1897 · fare 5¢", font=f_sub, fill=BLACK)
    d.line([W * 0.05, H * 0.20, W * 0.95, H * 0.20], fill=BLACK, width=S)

    # Boston Common: hatched block the line burrows under
    gx0, gy0, gx1, gy1 = W * 0.13, H * 0.30, W * 0.52, H * 0.62
    step = 7 * S
    x = gx0 - (gy1 - gy0)
    while x < gx1:
        xa, ya = max(gx0, x), gy1 - max(0, gx0 - x)
        xb, yb = min(gx1, x + (gy1 - gy0)), gy0 + max(0, x + (gy1 - gy0) - gx1)
        d.line([xa, ya, xb, yb], fill=BLACK, width=2)
        x += step
    d.rectangle([gx0, gy0, gx1, gy1], outline=BLACK, width=S)
    d.text(((gx0 + gx1) / 2, gy0 - 6 * S), "BOSTON COMMON", font=f_leg,
           fill=BLACK, anchor="mb")

    lw = 6 * S
    # 1897 line: Public Garden incline -> Boylston -> Park Street (solid red)
    p_a = (W * 0.08, H * 0.78)                  # Public Garden incline
    p_b = (W * 0.335, H * 0.78)                 # Boylston
    p_c = (W * 0.62, H * 0.495)                 # Park Street (after 45° bend)
    d.line([p_a, p_b], fill=RED, width=lw)
    d.line([p_b, p_c], fill=RED, width=lw)

    # 1898 continuation: Park St -> Scollay Sq -> Haymarket (dashed black)
    def dashed(a, b, dash=9 * S, gap=6 * S, width=3 * S):
        ax, ay = a
        bx, by = b
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        t = 0
        while t < L:
            t2 = min(t + dash, L)
            d.line([ax + ux * t, ay + uy * t, ax + ux * t2, ay + uy * t2],
                   fill=BLACK, width=width)
            t += dash + gap

    p_d = (W * 0.62, H * 0.335)                 # Scollay Sq
    p_e = (W * 0.80, H * 0.335)
    p_f = (W * 0.92, H * 0.455)                 # Haymarket, heading out
    dashed(p_c, p_d)
    dashed(p_d, p_e)
    dashed(p_e, p_f)

    def station(p, name, dx, dy, opened=True, anchor="lm"):
        r = 5.5 * S
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=WHITE,
                  outline=BLACK, width=2 * S)
        if opened:
            rr = 2.2 * S
            d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=RED)
        d.text((p[0] + dx * S, p[1] + dy * S), name, font=f_st, fill=BLACK,
               anchor=anchor)

    station(p_a, "PUBLIC GARDEN\nINCLINE", -2, 14, anchor="la")
    station(p_b, "BOYLSTON", -8, 14, anchor="la")
    station(p_c, "PARK STREET", 12, 0)
    station((p_d[0], p_d[1]), "SCOLLAY SQ", -14, 0, opened=False, anchor="rm")
    station((p_e[0] + (p_f[0] - p_e[0]) * 0.5, p_e[1] + (p_f[1] - p_e[1]) * 0.5),
            "HAYMARKET", 0, 12, opened=False, anchor="ma")

    # legend
    ly = H * 0.90
    d.line([W * 0.05, ly, W * 0.115, ly], fill=RED, width=lw)
    d.text((W * 0.13, ly), "in service Sept 1, 1897", font=f_leg, fill=BLACK,
           anchor="lm")
    dashed((W * 0.48, ly), (W * 0.545, ly))
    d.text((W * 0.56, ly), "opened 1898", font=f_leg, fill=BLACK, anchor="lm")
    save3(img, "3.png")


# ----------------------------------------------------------------------------
# 4. ALMANAC — the September 2026 sky as a timeline
# ----------------------------------------------------------------------------
def draw_moon(d, cx, cy, r, phase, outline_w):
    """phase in [0,1): 0=new, 0.25=first quarter, 0.5=full, 0.75=last quarter.
    Drawn for a black background."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK, outline=WHITE,
              width=outline_w)
    p = phase % 1.0
    illum = (1 - math.cos(2 * math.pi * p)) / 2
    if illum < 0.02:
        return
    lit_right = p < 0.5          # waxing: lit on the right
    a0, a1 = (-90, 90) if lit_right else (90, 270)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=WHITE)
    wterm = abs(math.cos(2 * math.pi * p)) * r
    if wterm > 0.5:
        fill = WHITE if illum > 0.5 else BLACK
        d.ellipse([cx - wterm, cy - r, cx + wterm, cy + r], fill=fill)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=outline_w)


def almanac():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)

    f_title = font(SANS_B, 22 * S)
    f_sub = font(SANS, 10 * S)
    f_day = font(MONO, 8 * S)
    f_ev = font(SANS_B, 9.5 * S)
    f_ev2 = font(SANS, 8.5 * S)

    d.text((W * 0.05, H * 0.05), "SEPTEMBER 2026", font=f_title, fill=WHITE)
    tw = text_w(d, "SEPTEMBER 2026", f_title)
    d.line([W * 0.05, H * 0.155, W * 0.05 + tw, H * 0.155], fill=RED,
           width=2 * S)
    d.text((W * 0.05, H * 0.175), "the sky this month", font=f_sub, fill=WHITE)

    # timeline axis
    ax0, ax1, ay = W * 0.07, W * 0.93, H * 0.56

    def dx(day):
        return ax0 + (day - 1) / 29 * (ax1 - ax0)

    d.line([ax0, ay, ax1, ay], fill=WHITE, width=S)
    for day in range(1, 31):
        x = dx(day)
        tick = 4 * S if day % 5 == 0 or day == 1 else 2 * S
        d.line([x, ay - tick, x, ay + tick], fill=WHITE, width=S)
        if day in (1, 5, 10, 15, 20, 25, 30):
            d.text((x, ay + 7 * S), str(day), font=f_day, fill=WHITE,
                   anchor="ma")

    NEW_MOON = 11.4              # new moon Sep 11; full ("Harvest") Sep 26
    def phase_of(day):
        return ((day - NEW_MOON) / 29.53) % 1.0

    def event(day, above, icon, line1, line2, red_dot=False):
        x = dx(day)
        ey = ay - H * 0.145 if above else ay + H * 0.155
        d.line([x, ay + (-6 * S if above else 6 * S), x, ey], fill=RED
               if red_dot else WHITE, width=S)
        icon(x, ey + (-16 * S if above else 14 * S))
        ty = ey + (-40 * S if above else 38 * S)
        # keep labels on the panel
        half = max(text_w(d, line1, f_ev), text_w(d, line2, f_ev2)) / 2
        tx = min(max(x, W * 0.02 + half), W * 0.98 - half)
        d.text((tx, ty), line1, font=f_ev, fill=RED if red_dot else WHITE,
               anchor="mm")
        d.text((tx, ty + 11 * S), line2, font=f_ev2, fill=WHITE, anchor="mm")

    def icon_today(x, y):
        d.ellipse([x - 5 * S, y - 5 * S, x + 5 * S, y + 5 * S], fill=RED)

    def icon_new(x, y):
        draw_moon(d, x, y, 9 * S, 0.0, S)

    def icon_venus(x, y):
        r1, r2 = 11 * S, 3.2 * S
        pts = []
        for i in range(8):
            r = r1 if i % 2 == 0 else r2
            a = math.pi / 2 * (i / 2) - math.pi / 2 + (0 if i % 2 == 0
                                                       else math.pi / 4)
            a = -math.pi / 2 + i * math.pi / 4
            pts.append((x + r * math.cos(a), y + r * math.sin(a)))
        d.polygon(pts, fill=RED)

    def icon_equinox(x, y):
        r = 9 * S
        d.ellipse([x - r, y - r, x + r, y + r], outline=WHITE, width=S)
        d.pieslice([x - r, y - r, x + r, y + r], 90, 270, fill=WHITE)

    def icon_full(x, y):
        draw_moon(d, x, y, 9 * S, 0.5, S)

    event(1, True, icon_today, "TODAY", "autumn begins", red_dot=True)
    event(11, False, icon_new, "NEW MOON", "darkest skies")
    event(18, True, icon_venus, "VENUS", "at its brightest")
    event(23, False, icon_equinox, "EQUINOX", "sun crosses south")
    event(26, True, icon_full, "HARVEST MOON", "full 26th")

    # bottom strip: the whole month of moons
    sy = H * 0.915
    for day in range(1, 31):
        draw_moon(d, dx(day), sy, 5.2 * S, phase_of(day), max(1, S // 2))
    save3(img, "4.png")


# ----------------------------------------------------------------------------
# 5. NIHYAKUTOKA — 二百十日, the 210th day from Risshun: storm-watching day
# ----------------------------------------------------------------------------
def nihyakutoka():
    rng = random.Random(20260901)
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # red sun, high and calm above the coming wind
    scx, scy, sr = W * 0.27, H * 0.28, H * 0.155
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=RED)

    # wind: long streamlines rushing left -> right, some ending in curls
    def streamline(y0, amp, curl):
        pts = []
        x = -W * 0.05
        ph = rng.uniform(0, 6.28)
        while x < W * (0.78 if curl else 1.05):
            y = y0 + amp * math.sin(x / W * 6.0 + ph) + (x / W) * H * 0.03
            pts.append((x, y))
            x += 6 * S
        d.line(pts, fill=BLACK, width=S)
        if curl and pts:
            ex, ey = pts[-1]
            # spiral curl
            spts = []
            r0 = 16 * S
            for i in range(40):
                t = i / 39
                a = t * 3.6 * math.pi
                r = r0 * (1 - t * 0.85)
                spts.append((ex + r * math.sin(a), ey - r0 + r * math.cos(a)))
            d.line(spts, fill=BLACK, width=S)

    for i in range(9):
        y0 = H * (0.10 + 0.055 * i) + rng.uniform(-4, 4) * S
        streamline(y0, rng.uniform(4, 10) * S, curl=(i in (2, 5)))

    # susuki grass bending hard in the wind
    base_y = H * 0.995

    def blade(x0, height, lean):
        n = 26
        pts = []
        for i in range(n):
            t = i / (n - 1)
            bend = lean * (t ** 2.2)
            x = x0 + bend * height
            y = base_y - t * height
            pts.append((x, y))
        wdt = max(1, int((1 - 0.6 * rng.random()) * 2.6 * S))
        d.line(pts, fill=BLACK, width=wdt)
        return pts[-1], lean

    def seedhead(tip, lean):
        tx, ty = tip
        for _ in range(7):
            a = -math.pi / 2 + lean * 1.1 + rng.uniform(-0.55, 0.35)
            ln = rng.uniform(9, 20) * S
            d.line([tx, ty, tx + ln * math.cos(a) + ln * 0.6,
                    ty + ln * math.sin(a)], fill=BLACK, width=max(1, S - 1))

    for _ in range(85):
        x0 = rng.uniform(-W * 0.02, W * 1.0)
        height = rng.uniform(0.14, 0.52) * H
        lean = rng.uniform(0.45, 0.95)
        tip, ln = blade(x0, height, lean)
        if height > 0.30 * H and rng.random() < 0.75:
            seedhead(tip, ln)

    # vertical kanji, top right: 二百十日
    f_jp = font(JP, 34 * S)
    x_k = W * 0.895
    for i, ch in enumerate("二百十日"):
        d.text((x_k, H * 0.065 + i * 40 * S), ch, font=f_jp, fill=BLACK,
               anchor="ma")
    f_lat = font(SANS, 8.5 * S)
    d.text((W * 0.03, H * 0.03),
           "NIHYAKUTŌKA — the 210th day · when the typhoon winds come",
           font=f_lat, fill=BLACK)
    save3(img, "5.png")


if __name__ == "__main__":
    martha()
    znanie()
    subway()
    almanac()
    nihyakutoka()
