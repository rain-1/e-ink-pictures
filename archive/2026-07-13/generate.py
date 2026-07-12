#!/usr/bin/env python3
"""Five pictures a day for a 400x300 black/white/red e-ink screen.

Usage:
    python generate.py YYYY-MM-DD OUTDIR    # one day's five images
    python generate.py all BASEDIR          # the whole week 2026-07-12 .. 2026-07-18

Everything renders at 3x (1200x900) and is reduced to the exact 3-color
palette at the end -- Floyd-Steinberg dithered for tonal pieces, nearest-color
for flat poster pieces.
"""
import sys, os, math, random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H, S = 400, 300, 3
BW, BH = W * S, H * S
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

_pal = Image.new("P", (16, 16))
_pal.putpalette([255, 255, 255, 0, 0, 0, 255, 0, 0] + [0, 0, 0] * 253)

FONTPATHS = {
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "serifb": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "serifi": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sansb": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "monob": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "jp": "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
}
_fc = {}
def F(name, size):
    key = (name, size)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FONTPATHS[name], size)
    return _fc[key]

def canvas(bg=WHITE):
    return Image.new("RGB", (BW, BH), bg)

def finish(img, dither=False):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=_pal, dither=d)

def rot(points, ang, cx, cy):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + (x - cx) * c - (y - cy) * s,
             cy + (x - cx) * s + (y - cy) * c) for x, y in points]

def vtext(d, x, y, text, font, fill, gap=1.05):
    """vertical (top-to-bottom) text, centered on x"""
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill, anchor="ma")
        y += int(font.size * gap)

# ---------------------------------------------------------------- moon ----
SYNODIC = 29.530588853
NEWMOON = datetime(2026, 7, 14, 9, 44)   # verified: new supermoon 09:44 UTC

def moon_age(date):
    return ((date - NEWMOON).total_seconds() / 86400.0) % SYNODIC

def moon_illum(age):
    return (1 - math.cos(2 * math.pi * age / SYNODIC)) / 2

def moon_name(age):
    p = age / SYNODIC
    names = ["new moon", "waxing crescent", "first quarter", "waxing gibbous",
             "full moon", "waning gibbous", "last quarter", "waning crescent"]
    idx = int(((p + 1 / 16) % 1) * 8)
    return names[idx]

def draw_moon(d, cx, cy, r, age, light=WHITE, dark=(25, 25, 25), outline=None):
    p = age / SYNODIC
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=dark)
    for dy in range(-r, r + 1):
        edge = math.sqrt(max(r * r - dy * dy, 0))
        t = edge * math.cos(2 * math.pi * p)
        if p <= 0.5:
            x0, x1 = t, edge          # waxing: lit on the right
        else:
            x0, x1 = -edge, -t        # waning: lit on the left
        if x1 - x0 > 0.5:
            d.line([cx + x0, cy + dy, cx + x1, cy + dy], fill=light)
    if outline:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=outline, width=S)

# ------------------------------------------------------- almanac (slot 3) ----
def almanac(date, events, footer):
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    # header band
    d.rectangle([0, 0, BW, 62 * S], fill=BLACK)
    d.text((20 * S, 12 * S), date.strftime("%A").upper(), font=F("mono", 11 * S), fill=RED)
    d.text((20 * S, 26 * S), date.strftime("%-d %B %Y"), font=F("serifb", 22 * S), fill=WHITE)
    d.rectangle([0, 62 * S, BW, 64 * S], fill=RED)
    # moon at right of header, spilling below
    age = moon_age(date.replace(hour=21))
    draw_moon(d, 340 * S, 62 * S, 42 * S, age, outline=WHITE)
    d.text((340 * S, 112 * S), moon_name(age), font=F("mono", 10 * S), fill=BLACK, anchor="ma")
    d.text((340 * S, 125 * S), "%d%% lit" % round(moon_illum(age) * 100),
           font=F("monob", 10 * S), fill=RED, anchor="ma")
    # events
    d.text((20 * S, 78 * S), "TONIGHT", font=F("monob", 11 * S), fill=BLACK)
    d.line([20 * S, 93 * S, 120 * S, 93 * S], fill=BLACK, width=S)
    y = 103 * S
    for hot, line in events:
        col = RED if hot else BLACK
        d.polygon([(24 * S, y + 5 * S), (28 * S, y + 1 * S), (32 * S, y + 5 * S), (28 * S, y + 9 * S)],
                  fill=col)
        d.text((40 * S, y), line, font=F("sans", 11 * S), fill=BLACK)
        y += 22 * S
    d.rectangle([0, 272 * S, BW, BH], fill=BLACK)
    d.text((200 * S, 286 * S), footer, font=F("mono", 9 * S), fill=WHITE, anchor="mm")
    return finish(im, dither=True)

# ------------------------------------------------------ quote/word posters ----
def quote_poster(lines, big, attrib, sub, accent_word=None):
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    d.rectangle([10 * S, 10 * S, BW - 10 * S, BH - 10 * S], outline=BLACK, width=S)
    d.rectangle([14 * S, 14 * S, BW - 14 * S, BH - 14 * S], outline=BLACK, width=1)
    y = 60 * S
    f = F("serifb", big * S)
    for ln in lines:
        if accent_word and accent_word in ln:
            pre, post = ln.split(accent_word, 1)
            wpre = d.textlength(pre, font=f)
            wacc = d.textlength(accent_word, font=f)
            wpost = d.textlength(post, font=f)
            x = (BW - (wpre + wacc + wpost)) / 2
            d.text((x, y), pre, font=f, fill=BLACK)
            d.text((x + wpre, y), accent_word, font=f, fill=RED)
            d.text((x + wpre + wacc, y), post, font=f, fill=BLACK)
        else:
            d.text((BW / 2, y), ln, font=f, fill=BLACK, anchor="ma")
        y += int(big * 1.25) * S
    y += 14 * S
    d.line([BW / 2 - 40 * S, y, BW / 2 + 40 * S, y], fill=RED, width=2 * S)
    d.text((BW / 2, y + 16 * S), attrib, font=F("serifi", 13 * S), fill=BLACK, anchor="ma")
    d.text((BW / 2, y + 38 * S), sub, font=F("mono", 9 * S), fill=BLACK, anchor="ma")
    return finish(im)

# =================================================================
# 2026-07-12  -- Thoreau / the red wedge finally
# =================================================================
def d12_lissitzky():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    # diagonal black field on the right
    d.polygon([(BW * 0.42, 0), (BW, 0), (BW, BH), (BW * 0.58, BH)], fill=BLACK)
    # white circle on the black field
    cx, cy, r = BW * 0.72, BH * 0.44, BH * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    # the red wedge, piercing from the left
    d.polygon([(BW * 0.04, BH * 0.28), (cx + r * 0.15, cy), (BW * 0.04, BH * 0.60)], fill=RED)
    # constructivist debris
    d.rectangle([BW * 0.08, BH * 0.72, BW * 0.20, BH * 0.76], fill=BLACK)
    d.rectangle([BW * 0.13, BH * 0.80, BW * 0.17, BH * 0.90], fill=RED)
    d.rectangle([BW * 0.24, BH * 0.68, BW * 0.27, BH * 0.86], fill=BLACK)
    d.rectangle([BW * 0.80, BH * 0.78, BW * 0.94, BH * 0.82], fill=RED)
    d.rectangle([BW * 0.84, BH * 0.10, BW * 0.88, BH * 0.20], fill=WHITE)
    for i in range(5):
        x = BW * (0.60 + 0.07 * i)
        d.rectangle([x, BH * 0.90, x + 4 * S, BH * 0.90 + 4 * S], fill=WHITE)
    d.text((BW * 0.05, BH * 0.06), "FIVE PICTURES", font=F("monob", 15 * S), fill=BLACK)
    d.text((BW * 0.05, BH * 0.13), "TO THE PEOPLE", font=F("monob", 15 * S), fill=RED)
    d.text((BW * 0.96, BH * 0.94), "after El Lissitzky, 1919", font=F("mono", 8 * S),
           fill=WHITE, anchor="rs")
    return finish(im)

def d12_kamon():
    rng = random.Random(20260712)
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    cx, cy, R = BW / 2, BH / 2 - 8 * S, 105 * S
    n = rng.choice([5, 6, 8])
    # double enclosure ring
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLACK, width=6 * S)
    r2 = R - 12 * S
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=BLACK, width=2 * S)
    # petals
    for k in range(n):
        ang = k * 2 * math.pi / n - math.pi / 2
        pr = R * 0.62
        pts = []
        for t in range(31):
            u = t / 30 * 2 * math.pi
            px = math.cos(u) * R * 0.20
            py = -pr / 2 + math.sin(u) * pr * 0.46
            pts.append((cx + px, cy + py))
        d.polygon(rot(pts, ang, cx, cy), fill=BLACK)
    for k in range(n):  # white keyline inside each petal
        ang = k * 2 * math.pi / n - math.pi / 2
        pr = R * 0.62
        pts = []
        for t in range(31):
            u = t / 30 * 2 * math.pi
            px = math.cos(u) * R * 0.11
            py = -pr / 2 + math.sin(u) * pr * 0.34
            pts.append((cx + px, cy + py))
        d.polygon(rot(pts, ang, cx, cy), fill=WHITE)
    rc = R * 0.14
    d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=RED)
    d.text((BW / 2, BH - 34 * S), "家紋", font=F("jp", 16 * S), fill=RED, anchor="ma")
    d.text((BW / 2, BH - 15 * S), "a crest for this house  ·  %d-fold" % n,
           font=F("mono", 9 * S), fill=BLACK, anchor="ma")
    return finish(im)

def d12_almanac():
    return almanac(datetime(2026, 7, 12), [
        (False, "Venus blazing low in the west at dusk"),
        (False, "Mars in the east before dawn"),
        (False, "Waning crescent rises with the morning"),
        (True,  "New supermoon in 2 days — dark skies ahead"),
    ], "the week: Jul 14 new supermoon · Jul 17 Venus-Regulus-Moon")

def d12_thoreau():
    return quote_poster(["Simplify,", "simplify."], 34,
                        "Henry David Thoreau",
                        "born this day, 12 July 1817 · Walden",
                        accent_word="simplify.")

def d12_walden():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    # sky gradient
    a = np.tile(np.linspace(235, 255, BH // 2).reshape(-1, 1), (1, BW)).astype(np.uint8)
    im.paste(Image.fromarray(a, "L").convert("RGB"), (0, 0))
    # sun
    d.ellipse([BW * 0.62 - 26 * S, BH * 0.18 - 26 * S, BW * 0.62 + 26 * S, BH * 0.18 + 26 * S], fill=RED)
    # far shore
    d.polygon([(0, BH * 0.50), (BW * 0.3, BH * 0.44), (BW * 0.65, BH * 0.48),
               (BW, BH * 0.45), (BW, BH * 0.52), (0, BH * 0.52)], fill=(90, 90, 90))
    # pond
    d.rectangle([0, BH * 0.52, BW, BH], fill=(210, 210, 210))
    rng = random.Random(1817)
    for i in range(220):  # ripples
        y = BH * (0.53 + 0.47 * rng.random() ** 1.6)
        x = rng.random() * BW
        ln = (8 + 50 * rng.random()) * S
        g = rng.choice([140, 160, 180, 245])
        d.line([x, y, x + ln, y], fill=(g, g, g), width=S)
    # sun reflection
    for i in range(26):
        y = BH * 0.53 + i * 4.5 * S
        wob = math.sin(i * 1.7) * 6 * S
        ln = max(6 * S, (30 - i) * 1.6 * S)
        d.line([BW * 0.62 + wob - ln / 2, y, BW * 0.62 + wob + ln / 2, y], fill=RED, width=2 * S)
    # cabin on far shore
    bx, by = BW * 0.30, BH * 0.435
    d.rectangle([bx, by - 9 * S, bx + 16 * S, by + 4 * S], fill=BLACK)
    d.polygon([(bx - 2 * S, by - 9 * S), (bx + 8 * S, by - 16 * S), (bx + 18 * S, by - 9 * S)], fill=BLACK)
    # pines left and right
    def pine(x, base, h, w):
        for i in range(4):
            t = i / 4
            d.polygon([(x - w * (1 - t) / 2, base - h * t - h * 0.28),
                       (x, base - h * t - h * 0.55),
                       (x + w * (1 - t) / 2, base - h * t - h * 0.28)], fill=BLACK)
        d.rectangle([x - w * 0.04, base - h * 0.3, x + w * 0.04, base], fill=BLACK)
    pine(BW * 0.07, BH * 0.62, BH * 0.42, BW * 0.16)
    pine(BW * 0.16, BH * 0.58, BH * 0.30, BW * 0.11)
    pine(BW * 0.93, BH * 0.60, BH * 0.36, BW * 0.13)
    d.text((BW - 12 * S, BH - 8 * S), "Walden Pond, morning", font=F("serifi", 10 * S),
           fill=BLACK, anchor="rs")
    return finish(im, dither=True)

# =================================================================
# 2026-07-13  -- Obon: the welcoming fire
# =================================================================
def d13_mukaebi():
    # radial glow around a lantern, dithered
    yy, xx = np.mgrid[0:BH, 0:BW].astype(float)
    lx, ly = BW * 0.32, BH * 0.34
    dist = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2)
    glow = np.clip(120 - dist / (2.2 * S), 0, 120)
    fx, fy = BW * 0.68, BH * 0.82
    dist2 = np.sqrt((xx - fx) ** 2 + (yy - fy) ** 2)
    glow += np.clip(90 - dist2 / (1.6 * S), 0, 90)
    a = np.clip(glow, 0, 210).astype(np.uint8)
    im = Image.fromarray(a, "L").convert("RGB")
    d = ImageDraw.Draw(im)
    # chochin lantern
    lw, lh = 34 * S, 48 * S
    d.line([lx, 0, lx, ly - lh], fill=(180, 180, 180), width=2 * S)
    d.ellipse([lx - lw, ly - lh, lx + lw, ly + lh], fill=RED, outline=BLACK, width=2 * S)
    for i in range(1, 6):
        ry = ly - lh + i * (2 * lh / 6)
        sq = math.sin(math.pi * i / 6)
        d.arc([lx - lw * (0.94 + 0.06 * sq), ry - 6 * S, lx + lw * (0.94 + 0.06 * sq), ry + 6 * S],
              0, 180, fill=BLACK, width=S)
    d.rectangle([lx - lw * 0.5, ly - lh - 5 * S, lx + lw * 0.5, ly - lh + 3 * S], fill=BLACK)
    d.rectangle([lx - lw * 0.5, ly + lh - 3 * S, lx + lw * 0.5, ly + lh + 5 * S], fill=BLACK)
    d.text((lx, ly), "火", font=F("jp", 30 * S), fill=WHITE, anchor="mm")
    # the small fire on crossed hemp sticks
    d.line([fx - 22 * S, fy + 10 * S, fx + 22 * S, fy + 2 * S], fill=BLACK, width=3 * S)
    d.line([fx - 20 * S, fy + 2 * S, fx + 20 * S, fy + 10 * S], fill=BLACK, width=3 * S)
    flames = [(0, 34), (-12, 22), (12, 24), (-6, 28), (7, 30)]
    for dx, fh in flames:
        d.polygon([(fx + dx * S - 6 * S, fy + 2 * S), (fx + dx * S, fy - fh * S),
                   (fx + dx * S + 6 * S, fy + 2 * S)], fill=RED)
    d.polygon([(fx - 4 * S, fy + 2 * S), (fx, fy - 16 * S), (fx + 4 * S, fy + 2 * S)], fill=WHITE)
    # ground line
    d.line([0, BH * 0.88, BW, BH * 0.88], fill=(120, 120, 120), width=S)
    vtext(d, BW * 0.90, BH * 0.08, "迎え火", F("jp", 26 * S), WHITE)
    d.text((BW * 0.03, BH - 10 * S), "mukaebi — a fire to guide the ancestors home · Obon begins",
           font=F("mono", 8 * S), fill=WHITE, anchor="ls")
    return finish(im, dither=True)

def d13_seigaiha():
    rng = random.Random(20260713)
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    R = 40 * S
    ry = int(R * 0.55)
    row = 0
    y = -R
    while y < BH + R:
        off = 0 if row % 2 == 0 else R
        x = -R + off - R
        while x < BW + 2 * R:
            red = rng.random() < 0.10
            for i, rr in enumerate(range(R, 6 * S, -int(R / 4.5))):
                fill = WHITE if i % 2 else (RED if red else BLACK)
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=fill)
            x += 2 * R
        y += ry
        row += 1
    d.rectangle([0, BH - 22 * S, BW, BH], fill=BLACK)
    d.text((70 * S, BH - 11 * S), "青海波", font=F("jp", 11 * S), fill=RED, anchor="mm")
    d.text((100 * S, BH - 11 * S), "seigaiha — waves of the calm blue sea",
           font=F("mono", 8 * S), fill=WHITE, anchor="lm")
    return finish(im)

def d13_almanac():
    return almanac(datetime(2026, 7, 13), [
        (True,  "Mukaebi — Obon welcoming fires are lit"),
        (False, "Venus low in the west after sunset"),
        (False, "Old crescent moon, thin as paper, pre-dawn"),
        (True,  "Tomorrow: new supermoon, 09:44 UTC"),
    ], "obon: mukaebi Jul 13 · okuribi sends them home Jul 16")

def d13_monoaware():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    d.rectangle([10 * S, 10 * S, BW - 10 * S, BH - 10 * S], outline=BLACK, width=S)
    chars = "物の哀れ"
    xs = BW / 2 - 105 * S
    for i, ch in enumerate(chars):
        col = RED if ch == "哀" else BLACK
        d.text((xs + i * 60 * S, 88 * S), ch, font=F("jp", 52 * S), fill=col, anchor="mm")
    d.text((BW / 2, 150 * S), "mono no aware", font=F("serifi", 17 * S), fill=BLACK, anchor="ma")
    d.line([BW / 2 - 40 * S, 182 * S, BW / 2 + 40 * S, 182 * S], fill=RED, width=2 * S)
    for j, ln in enumerate(["the gentle, bittersweet ache of watching",
                            "things pass — and loving them because they do"]):
        d.text((BW / 2, (196 + j * 17) * S), ln, font=F("serif", 11 * S), fill=BLACK, anchor="ma")
    d.text((BW / 2, 260 * S), "a word for Obon week", font=F("mono", 8 * S), fill=BLACK, anchor="ma")
    return finish(im)

def d13_wave():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    # red sun
    d.ellipse([BW * 0.70 - 30 * S, BH * 0.16 - 30 * S, BW * 0.70 + 30 * S, BH * 0.16 + 30 * S], fill=RED)
    # Fuji
    d.polygon([(BW * 0.56, BH * 0.46), (BW * 0.66, BH * 0.30), (BW * 0.76, BH * 0.46)], fill=BLACK)
    d.polygon([(BW * 0.632, BH * 0.345), (BW * 0.66, BH * 0.30), (BW * 0.688, BH * 0.345),
               (BW * 0.672, BH * 0.36), (BW * 0.66, BH * 0.345), (BW * 0.648, BH * 0.36)], fill=WHITE)
    # layered sea
    def waveband(base, amp, per, phase, fill):
        pts = [(x, base + amp * math.sin(x / per + phase)) for x in range(0, BW + 1, 4 * S)]
        d.polygon(pts + [(BW, BH), (0, BH)], fill=fill)
    waveband(BH * 0.52, 8 * S, 60 * S, 0.0, BLACK)
    waveband(BH * 0.60, 10 * S, 48 * S, 2.0, WHITE)
    waveband(BH * 0.68, 12 * S, 55 * S, 4.2, BLACK)
    waveband(BH * 0.78, 12 * S, 44 * S, 1.1, WHITE)
    waveband(BH * 0.86, 10 * S, 62 * S, 3.3, BLACK)
    # the great claw wave, from the left
    cx, cy = BW * 0.30, BH * 0.46
    d.pieslice([cx - 95 * S, cy - 95 * S, cx + 95 * S, cy + 95 * S], 150, 340, fill=BLACK)
    d.pieslice([cx - 68 * S, cy - 68 * S, cx + 68 * S, cy + 68 * S], 140, 330, fill=WHITE)
    d.pieslice([cx - 44 * S, cy - 44 * S, cx + 44 * S, cy + 44 * S], 150, 340, fill=BLACK)
    d.pieslice([cx - 24 * S, cy - 24 * S, cx + 24 * S, cy + 24 * S], 140, 330, fill=WHITE)
    rng = random.Random(31)
    for i in range(26):  # foam claws along the crest
        ang = math.radians(150 + i * 7.3)
        fr = 95 * S
        px, py = cx + fr * math.cos(ang), cy + fr * math.sin(ang)
        rr = (4 + 5 * rng.random()) * S
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=WHITE)
    for i in range(40):  # spray
        px = cx + (rng.random() * 190 - 40) * S
        py = cy - (30 + rng.random() * 80) * S
        rr = (1 + 2 * rng.random()) * S
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=BLACK)
    d.text((BW - 10 * S, BH - 8 * S), "the sea, after Hokusai", font=F("mono", 8 * S),
           fill=WHITE, anchor="rs")
    return finish(im)

# =================================================================
# 2026-07-14  -- new supermoon / Bastille day
# =================================================================
def d14_supermoon():
    im = canvas(BLACK)
    d = ImageDraw.Draw(im)
    rng = random.Random(714)
    for i in range(240):  # a moonless night is a starry night
        x, y = rng.random() * BW, rng.random() * BH
        r = S * (0.6 + 1.2 * rng.random() ** 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(200, 200, 200))
    cx, cy, r = BW * 0.66, BH * 0.46, 78 * S
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(16, 16, 16), outline=WHITE, width=S)
    d.arc([cx - r - 10 * S, cy - r - 10 * S, cx + r + 10 * S, cy + r + 10 * S],
          300, 200, fill=RED, width=2 * S)
    d.text((cx, cy + r + 18 * S), "at perigee — it pulls the highest tides",
           font=F("mono", 8 * S), fill=(200, 200, 200), anchor="ma")
    d.text((20 * S, 26 * S), "NEW", font=F("serifb", 34 * S), fill=WHITE)
    d.text((20 * S, 64 * S), "SUPERMOON", font=F("serifb", 34 * S), fill=RED)
    for j, ln in enumerate(["14 JULY 2026 · 09:44 UTC",
                            "4th of five in a row",
                            "no moon tonight —",
                            "the Milky Way's best night"]):
        d.text((20 * S, (120 + j * 15) * S), ln, font=F("mono", 9 * S), fill=WHITE)
    return finish(im, dither=True)

def d14_truchet():
    rng = random.Random(20260714)
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    cell = 40 * S
    wdt = 9 * S
    for gy in range(0, BH, cell):
        for gx in range(0, BW, cell):
            col = RED if rng.random() < 0.13 else BLACK
            if rng.random() < 0.5:
                d.arc([gx - cell / 2, gy - cell / 2, gx + cell / 2, gy + cell / 2],
                      0, 90, fill=col, width=wdt)
                d.arc([gx + cell / 2, gy + cell / 2, gx + cell * 1.5, gy + cell * 1.5],
                      180, 270, fill=col, width=wdt)
            else:
                d.arc([gx + cell / 2, gy - cell / 2, gx + cell * 1.5, gy + cell / 2],
                      90, 180, fill=col, width=wdt)
                d.arc([gx - cell / 2, gy + cell / 2, gx + cell / 2, gy + cell * 1.5],
                      270, 360, fill=col, width=wdt)
    return finish(im)

def d14_almanac():
    return almanac(datetime(2026, 7, 14), [
        (True,  "NEW SUPERMOON, 09:44 UTC — no moon at all"),
        (True,  "Milky Way overhead after midnight"),
        (False, "Saturn rising late evening"),
        (False, "Vega nearly overhead — the Summer Triangle"),
    ], "darkest sky of the month — go outside")

def d14_bastille():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    # abstracted tricolour: three vertical constructivist bands
    d.rectangle([0, 0, BW * 0.16, BH], fill=BLACK)
    d.rectangle([BW * 0.84, 0, BW, BH], fill=RED)
    words = ["LIBERTÉ", "ÉGALITÉ", "FRATERNITÉ"]
    cols = [BLACK, RED, BLACK]
    for i, (wd, col) in enumerate(zip(words, cols)):
        d.text((BW / 2, (70 + i * 55) * S), wd, font=F("serifb", 30 * S), fill=col, anchor="mm")
    d.line([BW * 0.28, 40 * S, BW * 0.72, 40 * S], fill=BLACK, width=2 * S)
    d.line([BW * 0.28, 232 * S, BW * 0.72, 232 * S], fill=BLACK, width=2 * S)
    d.text((BW / 2, 252 * S), "LE QUATORZE JUILLET · 1789", font=F("mono", 10 * S),
           fill=BLACK, anchor="ma")
    return finish(im)

def d14_milkyway():
    rng = np.random.default_rng(20260714)
    a = np.zeros((BH // S, BW // S), float)  # work at 1x, dither will texture it
    h, w = a.shape
    # star field
    n = 900
    xs = rng.random(n) * w
    ys = rng.random(n) * h
    for x, y in zip(xs, ys):
        a[int(y) % h, int(x) % w] += 60 + 160 * rng.random() ** 2
    # the band, diagonal
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    dband = np.abs((yy - 0.9 * xx * h / w - h * 0.06)) / (h * 0.16)
    band = np.exp(-dband ** 2) * 95
    a += band
    # dust lanes
    for k in range(5):
        cx0, t = rng.random() * w, rng.random()
        dl = np.abs(yy - 0.9 * xx * h / w - h * (0.02 + 0.08 * t)) / (h * 0.012)
        lane = np.exp(-dl ** 2) * np.exp(-((xx - cx0) / (w * 0.2)) ** 2)
        a -= lane * 80
    # extra stars inside the band
    m = 2600
    xs = rng.random(m) * w
    ys = (0.9 * xs * h / w + h * 0.06 + rng.normal(0, h * 0.11, m))
    for x, y in zip(xs, ys):
        if 0 <= int(y) < h:
            a[int(y), int(x) % w] += 90 + 120 * rng.random() ** 2
    a = np.clip(a, 0, 255)
    im = Image.fromarray(a.astype(np.uint8), "L").resize((BW, BH), Image.NEAREST).convert("RGB")
    im = im.filter(ImageFilter.GaussianBlur(1))
    d = ImageDraw.Draw(im)
    # horizon treeline
    rng2 = random.Random(7)
    pts = [(0, BH)]
    x = 0
    while x < BW:
        ht = BH * (0.88 - 0.08 * rng2.random())
        pts += [(x, ht), (x + 14 * S, ht)]
        x += 14 * S
    pts += [(BW, BH)]
    d.polygon(pts, fill=BLACK)
    d.text((12 * S, BH - 10 * S), "the Milky Way, on the month's darkest night",
           font=F("mono", 8 * S), fill=WHITE, anchor="ls")
    d.text((BW - 12 * S, BH - 10 * S), "14.vii", font=F("mono", 8 * S), fill=RED, anchor="rs")
    return finish(im, dither=True)

# =================================================================
# 2026-07-15  -- St. Swithin / Rembrandt 420
# =================================================================
def d15_swithin():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    rng = random.Random(40)
    for i in range(240):  # the rain
        x, y = rng.random() * BW, rng.random() * BH * 0.92
        ln = (6 + 6 * rng.random()) * S
        d.line([x, y, x - ln * 0.35, y + ln], fill=BLACK, width=S)
    # umbrella
    cx, cy, R = BW / 2, BH * 0.44, 95 * S
    d.pieslice([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=RED, outline=BLACK, width=3 * S)
    for k in range(1, 4):  # scallops
        sx = cx - R + k * (2 * R / 4)
        d.arc([sx - R / 4, cy - R / 8, sx + R / 4, cy + R / 8], 0, 180, fill=BLACK, width=3 * S)
    for k in range(5):  # ribs
        ang = math.pi + k * math.pi / 4
        d.line([cx, cy, cx + R * 0.97 * math.cos(ang), cy + R * 0.97 * math.sin(ang)],
               fill=BLACK, width=S)
    d.line([cx, cy - R, cx, cy - R - 8 * S], fill=BLACK, width=2 * S)
    d.line([cx, cy, cx, cy + 70 * S], fill=BLACK, width=4 * S)
    d.arc([cx - 14 * S, cy + 56 * S, cx + 14 * S, cy + 84 * S], 0, 180, fill=BLACK, width=4 * S)
    d.rectangle([0, BH * 0.86, BW, BH], fill=WHITE)
    d.text((BW / 2, BH * 0.875), "ST SWITHIN'S DAY · 15 JULY", font=F("monob", 10 * S),
           fill=RED, anchor="ma")
    d.text((BW / 2, BH * 0.925), "if thou dost rain, for forty days it will remain",
           font=F("serifi", 11 * S), fill=BLACK, anchor="ma")
    return finish(im)

def d15_sandpile():
    g = np.zeros((100, 134), dtype=np.int64)
    g[50, 67] = 58000
    while (g >= 4).any():
        o = g >= 4
        g[o] -= 4
        g[1:, :] += o[:-1, :]
        g[:-1, :] += o[1:, :]
        g[:, 1:] += o[:, :-1]
        g[:, :-1] += o[:, 1:]
    pal = np.array([[255, 255, 255], [255, 0, 0], [255, 255, 255], [0, 0, 0]], np.uint8)
    a = pal[np.clip(g, 0, 3)]
    im = Image.fromarray(a, "RGB").resize((BW, BH), Image.NEAREST)
    d = ImageDraw.Draw(im)
    d.rectangle([0, BH - 20 * S, BW, BH], fill=BLACK)
    d.text((BW / 2, BH - 10 * S),
           "abelian sandpile · 58,000 grains dropped on one point, then left to topple",
           font=F("mono", 7 * S), fill=WHITE, anchor="mm")
    return finish(im)

def d15_almanac():
    return almanac(datetime(2026, 7, 15), [
        (False, "Day-old moon, invisible — still dark skies"),
        (False, "Venus sinking toward Regulus in the west"),
        (True,  "Watch them draw together: triangle on the 17th"),
        (False, "Saturn up by midnight"),
    ], "st swithin's day: whatever today does, 40 days follow")

def d15_rembrandt():
    im = canvas(BLACK)
    # a spotlight out of darkness -- chiaroscuro
    yy, xx = np.mgrid[0:BH, 0:BW].astype(float)
    cx, cy = BW * 0.5, BH * 0.34
    dist = np.sqrt(((xx - cx) / 1.7) ** 2 + (yy - cy) ** 2)
    a = (238 * np.exp(-((dist / (68 * S)) ** 2))).astype(np.uint8)
    im = Image.fromarray(a, "L").convert("RGB")
    d = ImageDraw.Draw(im)
    d.text((cx, BH * 0.28), "REMBRANDT", font=F("serifb", 34 * S), fill=BLACK, anchor="mm")
    d.text((cx, BH * 0.42), "van Rijn", font=F("serifi", 18 * S), fill=BLACK, anchor="mm")
    d.text((BW * 0.5, BH * 0.62), "born in Leiden, 15 July 1606", font=F("mono", 9 * S),
           fill=WHITE, anchor="mm")
    d.text((BW * 0.5, BH * 0.74), "420", font=F("serifb", 30 * S), fill=RED, anchor="mm")
    d.text((BW * 0.5, BH * 0.84), "years of light out of darkness", font=F("mono", 9 * S),
           fill=WHITE, anchor="mm")
    return finish(im, dither=True)

def d15_rainwindow():
    # city through a wet window
    rng = np.random.default_rng(1606)
    im = canvas((225, 225, 225))
    d = ImageDraw.Draw(im)
    r2 = random.Random(16062)
    x = -10 * S
    while x < BW:  # skyline, soft grey
        wd = (20 + 40 * r2.random()) * S
        ht = BH * (0.25 + 0.4 * r2.random())
        g = int(120 + 60 * r2.random())
        d.rectangle([x, BH * 0.78 - ht, x + wd, BH * 0.78], fill=(g, g, g))
        x += wd * 0.8
    d.rectangle([0, BH * 0.78, BW, BH], fill=(70, 70, 70))
    im = im.filter(ImageFilter.GaussianBlur(3 * S))
    d = ImageDraw.Draw(im)
    # one red umbrella in the street
    ux, uy = BW * 0.62, BH * 0.80
    d.pieslice([ux - 16 * S, uy - 14 * S, ux + 16 * S, uy + 14 * S], 180, 360, fill=RED)
    d.line([ux, uy, ux, uy + 12 * S], fill=BLACK, width=S)
    d.ellipse([ux - 3 * S, uy + 10 * S, ux + 3 * S, uy + 16 * S], fill=BLACK)
    # rain trails on the glass
    for i in range(70):
        tx = rng.random() * BW
        ty = rng.random() * BH * 0.9
        ln = (10 + 60 * rng.random()) * S
        wob = rng.random() * 4 - 2
        d.line([tx, ty, tx + wob * S, ty + ln], fill=(245, 245, 245), width=2 * S)
        d.ellipse([tx + wob * S - 2.4 * S, ty + ln - 2.4 * S,
                   tx + wob * S + 2.4 * S, ty + ln + 2.4 * S], fill=(250, 250, 250))
    # window frame
    d.rectangle([0, 0, BW, BH], outline=BLACK, width=10 * S)
    d.line([BW / 2, 0, BW / 2, BH], fill=BLACK, width=6 * S)
    d.line([0, BH / 2, BW, BH / 2], fill=BLACK, width=6 * S)
    d.text((BW - 16 * S, BH - 16 * S), "forty days of this?", font=F("serifi", 10 * S),
           fill=WHITE, anchor="rs")
    return finish(im, dither=True)

# =================================================================
# 2026-07-16  -- Apollo 11 launch day
# =================================================================
def d16_saturnv():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    d.text((BW * 0.05, 18 * S), "APOLLO 11", font=F("serifb", 30 * S), fill=BLACK)
    d.text((BW * 0.05, 56 * S), "16 JULY 1969 · 13:32 UTC", font=F("mono", 10 * S), fill=RED)
    d.text((BW * 0.05, 70 * S), "KENNEDY SPACE CENTER LC-39A", font=F("mono", 10 * S), fill=BLACK)
    for j, ln in enumerate(["CREW", "ARMSTRONG", "ALDRIN", "COLLINS"]):
        d.text((BW * 0.05, (110 + j * 14) * S), ln, font=F("monob" if j == 0 else "mono", 9 * S),
               fill=RED if j == 0 else BLACK)
    d.text((BW * 0.05, 180 * S), "DESTINATION", font=F("monob", 9 * S), fill=RED)
    d.text((BW * 0.05, 194 * S), "MARE TRANQUILLITATIS", font=F("mono", 9 * S), fill=BLACK)
    # the stack
    rx, rw = BW * 0.72, 26 * S
    top, base = 24 * S, BH * 0.82
    d.polygon([(rx - 4 * S, top + 14 * S), (rx, top), (rx + 4 * S, top + 14 * S)], fill=RED)  # escape tower
    d.line([rx, top + 8 * S, rx, top + 22 * S], fill=BLACK, width=2 * S)
    d.polygon([(rx - rw * 0.35, top + 42 * S), (rx, top + 18 * S), (rx + rw * 0.35, top + 42 * S)],
              fill=WHITE, outline=BLACK)  # capsule
    d.rectangle([rx - rw, top + 42 * S, rx + rw, base], fill=WHITE, outline=BLACK, width=2 * S)
    for fy in (top + 42 * S + 40 * S, top + 42 * S + 100 * S):  # interstage bands
        d.rectangle([rx - rw, fy, rx + rw, fy + 8 * S], fill=BLACK)
    d.text((rx, base - 60 * S), "USA", font=F("monob", 16 * S), fill=BLACK, anchor="mm")
    d.rectangle([rx - rw, base - 26 * S, rx - rw + 8 * S, base], fill=BLACK)
    d.rectangle([rx + rw - 8 * S, base - 26 * S, rx + rw, base], fill=BLACK)
    d.polygon([(rx - rw, base), (rx - rw - 14 * S, base + 16 * S), (rx - rw, base - 22 * S)], fill=BLACK)
    d.polygon([(rx + rw, base), (rx + rw + 14 * S, base + 16 * S), (rx + rw, base - 22 * S)], fill=BLACK)
    # flame
    rng = random.Random(1969)
    for k in range(7):
        fx = rx - rw * 0.8 + k * rw * 0.27
        fl = (16 + 22 * rng.random()) * S
        d.polygon([(fx - 4 * S, base + 6 * S), (fx, base + 6 * S + fl), (fx + 4 * S, base + 6 * S)],
                  fill=RED)
    # gantry
    gx = rx + rw + 22 * S
    d.rectangle([gx, top + 30 * S, gx + 7 * S, base + 10 * S], fill=BLACK)
    for k in range(8):
        gy = top + 40 * S + k * 26 * S
        d.line([gx, gy, rx + rw, gy - 8 * S], fill=BLACK, width=S)
    d.rectangle([0, base + 22 * S, BW, base + 26 * S], fill=BLACK)
    d.text((BW * 0.05, base + 32 * S), "T MINUS ZERO — GO", font=F("monob", 11 * S), fill=RED)
    return finish(im)

def d16_tenprint():
    rng = random.Random(20260716)
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    cell = 25 * S
    for gy in range(0, BH, cell):
        for gx in range(0, BW, cell):
            col = RED if rng.random() < 0.07 else BLACK
            if rng.random() < 0.5:
                d.line([gx, gy, gx + cell, gy + cell], fill=col, width=5 * S)
            else:
                d.line([gx + cell, gy, gx, gy + cell], fill=col, width=5 * S)
    for k in range(14):  # solder pads, a nod to the AGC
        px = rng.randrange(0, BW // cell) * cell
        py = rng.randrange(0, BH // cell) * cell
        d.ellipse([px - 5 * S, py - 5 * S, px + 5 * S, py + 5 * S], fill=WHITE, outline=BLACK, width=2 * S)
    d.rectangle([0, BH - 20 * S, BW, BH], fill=BLACK)
    d.text((BW / 2, BH - 10 * S), '10 PRINT CHR$(205.5+RND(1)); : GOTO 10',
           font=F("mono", 9 * S), fill=WHITE, anchor="mm")
    return finish(im)

def d16_almanac():
    return almanac(datetime(2026, 7, 16), [
        (True,  "57 years since Apollo 11 left Earth"),
        (False, "Two-day crescent very low at dusk"),
        (False, "Venus and Regulus almost touching in the west"),
        (True,  "Tomorrow evening: Moon joins them — a triangle"),
    ], "okuribi tonight: the obon fires send the ancestors home")

def d16_jfk():
    return quote_poster(["“We choose to go", "to the Moon…", "not because they", "are easy.”"],
                        22, "John F. Kennedy, 1962",
                        "Apollo 11 launched this day, 1969", accent_word="Moon…")

def d16_earthrise():
    im = canvas(BLACK)
    d = ImageDraw.Draw(im)
    rng = random.Random(1969)
    for i in range(120):
        x, y = rng.random() * BW, rng.random() * BH * 0.55
        d.point((x, y), fill=WHITE)
        if rng.random() < 0.2:
            d.ellipse([x - S, y - S, x + S, y + S], fill=(180, 180, 180))
    # lunar regolith foreground
    a = (np.random.default_rng(11).random((BH // S, BW // S)) * 28 + 118).astype(np.uint8)
    ground = Image.fromarray(a, "L").resize((BW, BH), Image.NEAREST).filter(ImageFilter.GaussianBlur(3))
    im.paste(ground.convert("RGB"), (0, int(BH * 0.66)))
    d = ImageDraw.Draw(im)
    d.line([0, BH * 0.66, BW, BH * 0.66], fill=(60, 60, 60), width=2 * S)
    # craters
    r3 = random.Random(20)
    for i in range(8):
        cx = r3.random() * BW
        cy = BH * (0.72 + 0.24 * r3.random())
        cr = (8 + 20 * r3.random()) * S
        sq = 0.42
        d.ellipse([cx - cr, cy - cr * sq, cx + cr, cy + cr * sq], fill=(95, 95, 95))
        d.arc([cx - cr, cy - cr * sq, cx + cr, cy + cr * sq], 200, 340, fill=(230, 230, 230), width=3 * S)
        d.arc([cx - cr, cy - cr * sq, cx + cr, cy + cr * sq], 20, 160, fill=(30, 30, 30), width=3 * S)
    # the Earth, half lit
    ex, ey, er = BW * 0.70, BH * 0.30, 42 * S
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(15, 15, 15), outline=(90, 90, 90))
    d.pieslice([ex - er, ey - er, ex + er, ey + er], 90, 270, fill=(235, 235, 235))
    r4 = random.Random(3)
    for i in range(26):  # cloud swirls on the lit half
        wx = ex - er * (0.15 + 0.7 * r4.random())
        wy = ey - er * 0.85 + 1.7 * er * r4.random()
        if (wx - ex) ** 2 + (wy - ey) ** 2 < (er * 0.92) ** 2 and wx < ex:
            wl = (5 + 12 * r4.random()) * S
            d.arc([wx - wl, wy - wl * 0.5, wx + wl, wy + wl * 0.5], 20, 200,
                  fill=(120, 120, 120), width=2 * S)
    d.line([ex - er - 8 * S, ey, ex - er - 26 * S, ey], fill=RED, width=2 * S)
    d.text((ex - er - 32 * S, ey - 6 * S), "everyone you", font=F("mono", 8 * S), fill=RED, anchor="rm")
    d.text((ex - er - 32 * S, ey + 6 * S), "have ever known", font=F("mono", 8 * S), fill=RED, anchor="rm")
    d.text((12 * S, BH * 0.60), "Mare Tranquillitatis, looking home", font=F("mono", 8 * S),
           fill=WHITE, anchor="ls")
    return finish(im, dither=True)

# =================================================================
# 2026-07-17  -- Gion Matsuri
# =================================================================
def d17_hoko():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    cx = BW * 0.58
    # shingi (sacred pole) all the way up
    d.line([cx, 8 * S, cx, BH * 0.42], fill=BLACK, width=3 * S)
    d.polygon([(cx - 5 * S, 16 * S), (cx, 6 * S), (cx + 5 * S, 16 * S)], fill=RED)
    for k in range(4):
        ty = (30 + k * 22) * S
        d.line([cx - 8 * S, ty, cx + 8 * S, ty], fill=BLACK, width=2 * S)
    # roof
    d.polygon([(cx - 62 * S, BH * 0.46), (cx - 40 * S, BH * 0.40), (cx + 40 * S, BH * 0.40),
               (cx + 62 * S, BH * 0.46)], fill=BLACK)
    # body with tapestry
    bx0, bx1 = cx - 46 * S, cx + 46 * S
    by0, by1 = BH * 0.46, BH * 0.74
    d.rectangle([bx0, by0, bx1, by1], fill=WHITE, outline=BLACK, width=3 * S)
    for i in range(3):  # woven diamond tapestry rows
        for j in range(4):
            dxm = bx0 + (j + 0.5) * (bx1 - bx0) / 4
            dym = by0 + (i + 0.5) * (by1 - by0) / 3
            ddx, ddy = (bx1 - bx0) / 9.2, (by1 - by0) / 7
            col = RED if (i + j) % 2 else BLACK
            d.polygon([(dxm - ddx, dym), (dxm, dym - ddy), (dxm + ddx, dym), (dxm, dym + ddy)],
                      outline=col, width=2 * S)
    # lantern strings on both sides
    for sx in (bx0 - 14 * S, bx1 + 14 * S):
        d.line([sx, by0 - 6 * S, sx, by1 + 4 * S], fill=BLACK, width=S)
        for k in range(4):
            ly = by0 + 4 * S + k * (by1 - by0) / 4
            d.ellipse([sx - 8 * S, ly - 10 * S, sx + 8 * S, ly + 10 * S],
                      fill=RED, outline=BLACK, width=S)
            d.line([sx - 6 * S, ly, sx + 6 * S, ly], fill=WHITE, width=S)
    # wheels
    for wx in (cx - 34 * S, cx + 34 * S):
        wy, wr = BH * 0.82, 24 * S
        d.ellipse([wx - wr, wy - wr, wx + wr, wy + wr], fill=WHITE, outline=BLACK, width=4 * S)
        for k in range(8):
            ang = k * math.pi / 4
            d.line([wx, wy, wx + wr * 0.85 * math.cos(ang), wy + wr * 0.85 * math.sin(ang)],
                   fill=BLACK, width=2 * S)
        d.ellipse([wx - 4 * S, wy - 4 * S, wx + 4 * S, wy + 4 * S], fill=RED)
    # rope and pullers
    d.line([bx0, BH * 0.78, BW * 0.06, BH * 0.84], fill=BLACK, width=2 * S)
    r5 = random.Random(717)
    for k in range(5):
        px = BW * (0.06 + 0.05 * k)
        py = BH * 0.84 + (k % 2) * 3 * S
        d.ellipse([px - 4 * S, py - 10 * S, px + 4 * S, py - 2 * S], fill=BLACK)
        d.rectangle([px - 5 * S, py - 2 * S, px + 5 * S, py + 14 * S], fill=BLACK)
    d.line([0, BH * 0.895, BW, BH * 0.895], fill=BLACK, width=2 * S)
    vtext(d, BW * 0.10, 12 * S, "祇園祭", F("jp", 26 * S), RED)
    d.text((BW - 10 * S, BH - 8 * S), "Yamaboko Junko · Kyoto · 23 floats at 9 a.m.",
           font=F("mono", 8 * S), fill=BLACK, anchor="rs")
    return finish(im)

def d17_kumiko():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    a = 46 * S           # triangle side
    hgt = a * math.sqrt(3) / 2
    rng = random.Random(20260717)
    row = 0
    y = 0.0
    while y < BH + hgt:
        off = 0 if row % 2 == 0 else -a / 2
        x = off - a
        while x < BW + a:
            up = [(x, y + hgt), (x + a / 2, y), (x + a, y + hgt)]
            dn = [(x + a / 2, y), (x + a * 1.5, y), (x + a, y + hgt)]
            for tri in (up, dn):
                gx = sum(p[0] for p in tri) / 3
                gy = sum(p[1] for p in tri) / 3
                if rng.random() < 0.08:
                    d.polygon(tri, fill=RED)
                for p in tri:  # asanoha: vertex-to-incenter spokes
                    d.line([p[0], p[1], gx, gy], fill=BLACK, width=2 * S)
                d.polygon(tri, outline=BLACK, width=3 * S)
            x += a
        y += hgt
        row += 1
    d.rectangle([0, BH - 20 * S, BW, BH], fill=BLACK)
    d.text((52 * S, BH - 10 * S), "麻の葉", font=F("jp", 11 * S), fill=RED, anchor="mm")
    d.text((80 * S, BH - 10 * S), "asanoha kumiko — hemp-leaf lattice, no nails, no glue",
           font=F("mono", 8 * S), fill=WHITE, anchor="lm")
    return finish(im)

def d17_almanac():
    return almanac(datetime(2026, 7, 17), [
        (True,  "Venus, Regulus, Moon — a dusk triangle"),
        (True,  "Look west 45 min after sunset"),
        (False, "Earthshine on the crescent's dark side"),
        (False, "Gion Matsuri floats roll through Kyoto today"),
    ], "the sky's best gathering of the week — don't miss dusk")

def d17_konchikichin():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    word = "コンチキチン"
    rows = 5
    for r in range(rows):
        y = (34 + r * 46) * S
        sz = [30, 22, 38, 26, 34][r]
        rep = "".join(word for _ in range(3))
        xoff = -(r * 53) * S
        col = RED if r == 2 else BLACK
        d.text((xoff, y), rep, font=F("jp", sz * S), fill=col)
    d.rectangle([0, BH - 42 * S, BW, BH], fill=BLACK)
    d.text((BW / 2, BH - 30 * S), "kon-chiki-chin — the bell song of the Gion bayashi",
           font=F("mono", 9 * S), fill=WHITE, anchor="mm")
    d.text((BW / 2, BH - 13 * S), "heard in Kyoto every July for ~1,150 years",
           font=F("mono", 9 * S), fill=RED, anchor="mm")
    return finish(im)

def d17_lanterns():
    # dusk street, strings of chochin receding
    a = np.tile(np.linspace(140, 40, BH).reshape(-1, 1), (1, BW)).astype(np.uint8)
    im = Image.fromarray(a, "L").convert("RGB")
    d = ImageDraw.Draw(im)
    vx, vy = BW * 0.5, BH * 0.44   # vanishing point
    # buildings
    d.polygon([(0, BH), (0, BH * 0.10), (vx - 30 * S, vy)], fill=(15, 15, 15))
    d.polygon([(BW, BH), (BW, BH * 0.10), (vx + 30 * S, vy)], fill=(15, 15, 15))
    d.rectangle([0, vy + 40 * S, BW, BH], fill=(25, 25, 25))
    # two lantern strings, left and right, receding
    for side in (-1, 1):
        for k in range(6):
            t = k / 6.0
            lx = vx + side * (BW * 0.46) * (1 - t) ** 1.4
            ly = vy + (BH * 0.34) * (1 - t) ** 1.4 - 70 * S * (1 - t)
            lr = max(4 * S, 30 * S * (1 - t) ** 1.2)
            d.line([lx, ly - lr * 1.7, lx, ly - lr], fill=(120, 120, 120), width=S)
            d.ellipse([lx - lr * 0.8, ly - lr, lx + lr * 0.8, ly + lr],
                      fill=WHITE, outline=BLACK, width=max(1, S))
            if lr > 6 * S:
                d.text((lx, ly), "祭", font=F("jp", int(lr * 0.9)), fill=RED, anchor="mm")
    # crowd silhouettes
    r6 = random.Random(9)
    for i in range(30):
        px = r6.random() * BW
        ph = (10 + 8 * r6.random()) * S
        py = BH - r6.random() * 26 * S
        d.ellipse([px - ph * 0.22, py - ph, px + ph * 0.22, py - ph * 0.6], fill=BLACK)
        d.polygon([(px - ph * 0.32, py), (px, py - ph * 0.65), (px + ph * 0.32, py)], fill=BLACK)
    d.text((12 * S, 14 * S), "宵山", font=F("jp", 16 * S), fill=WHITE)
    d.text((12 * S, 36 * S), "lantern night", font=F("mono", 8 * S), fill=(200, 200, 200))
    return finish(im, dither=True)

# =================================================================
# 2026-07-18  -- Mandela Day / week's end
# =================================================================
def d18_mandela():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    d.text((BW / 2 + 3 * S, BH * 0.36 + 3 * S), "67", font=F("serifb", 110 * S), fill=BLACK, anchor="mm")
    d.text((BW / 2, BH * 0.36), "67", font=F("serifb", 110 * S), fill=RED, anchor="mm")
    d.text((BW / 2, BH * 0.68), "M I N U T E S", font=F("sansb", 22 * S), fill=BLACK, anchor="mm")
    d.line([BW * 0.2, BH * 0.76, BW * 0.8, BH * 0.76], fill=BLACK, width=2 * S)
    for j, ln in enumerate(["one minute of good for each year Nelson Mandela",
                            "served the public — Mandela Day · 18 July"]):
        d.text((BW / 2, BH * (0.80 + j * 0.06)), ln, font=F("serif", 10 * S), fill=BLACK, anchor="ma")
    return finish(im)

def d18_life():
    rng = np.random.default_rng(20260718)
    h, w = 75, 100
    a = rng.random((h, w)) < 0.33
    visits = np.zeros((h, w), np.int32)
    for t in range(240):
        n = sum(np.roll(np.roll(a, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1)) - a
        a = (n == 3) | (a & (n == 2))
        visits += a
    img = np.full((h, w, 3), 255, np.uint8)
    img[visits > 12] = [0, 0, 0]          # long-lived structures burn in black
    img[a] = [255, 0, 0]                  # still alive right now: red
    im = Image.fromarray(img, "RGB").resize((BW, BH), Image.NEAREST)
    d = ImageDraw.Draw(im)
    d.rectangle([0, BH - 20 * S, BW, BH], fill=BLACK)
    d.text((BW / 2, BH - 10 * S),
           "Conway's Life, 240 generations · black = what lasted, red = what lives",
           font=F("mono", 8 * S), fill=WHITE, anchor="mm")
    return finish(im)

def d18_almanac():
    return almanac(datetime(2026, 7, 18), [
        (True,  "Venus-Regulus-Moon triangle, tighter"),
        (False, "Crescent higher and easier than yesterday"),
        (False, "Mars pre-dawn; Saturn before midnight"),
        (False, "Jul 31: double meteor shower — mark it"),
    ], "first-quarter moon Jul 21: best crater shadows")

def d18_quote():
    return quote_poster(["“It always seems", "impossible", "until it is done.”"], 26,
                        "Nelson Mandela", "Mandela Day · 18 July", accent_word="impossible")

def d18_savanna():
    im = canvas(WHITE)
    d = ImageDraw.Draw(im)
    a = np.tile(np.linspace(250, 170, int(BH * 0.72)).reshape(-1, 1), (1, BW)).astype(np.uint8)
    im.paste(Image.fromarray(a, "L").convert("RGB"), (0, 0))
    # huge half-set sun
    sr = 62 * S
    d.pieslice([BW * 0.60 - sr, BH * 0.72 - sr, BW * 0.60 + sr, BH * 0.72 + sr], 180, 360, fill=RED)
    d.rectangle([0, BH * 0.72, BW, BH], fill=BLACK)
    # acacia
    tx, ty = BW * 0.26, BH * 0.72
    d.line([tx, ty, tx - 6 * S, ty - 52 * S], fill=BLACK, width=4 * S)
    d.line([tx - 6 * S, ty - 52 * S, tx - 22 * S, ty - 72 * S], fill=BLACK, width=3 * S)
    d.line([tx - 6 * S, ty - 52 * S, tx + 14 * S, ty - 74 * S], fill=BLACK, width=3 * S)
    d.ellipse([tx - 52 * S, ty - 92 * S, tx + 44 * S, ty - 64 * S], fill=BLACK)
    # birds
    for bx, by in [(0.45, 0.22), (0.52, 0.18), (0.48, 0.28)]:
        d.arc([BW * bx - 7 * S, BH * by - 4 * S, BW * bx, BH * by + 4 * S], 200, 340, fill=BLACK, width=2 * S)
        d.arc([BW * bx, BH * by - 4 * S, BW * bx + 7 * S, BH * by + 4 * S], 200, 340, fill=BLACK, width=2 * S)
    # grass fringe
    r7 = random.Random(67)
    for i in range(160):
        gx = r7.random() * BW
        gh = (4 + 9 * r7.random()) * S
        d.line([gx, BH * 0.72, gx + (r7.random() * 4 - 2) * S, BH * 0.72 - gh], fill=BLACK, width=S)
    d.text((BW - 12 * S, BH - 24 * S), "week's end", font=F("serifi", 11 * S), fill=WHITE, anchor="rs")
    d.text((BW - 12 * S, BH - 10 * S), "drawn ahead for you, with care — Claude",
           font=F("mono", 8 * S), fill=RED, anchor="rs")
    return finish(im, dither=True)

# =================================================================
DAYS = {
    "2026-07-12": [d12_lissitzky, d12_kamon, d12_almanac, d12_thoreau, d12_walden],
    "2026-07-13": [d13_mukaebi, d13_seigaiha, d13_almanac, d13_monoaware, d13_wave],
    "2026-07-14": [d14_supermoon, d14_truchet, d14_almanac, d14_bastille, d14_milkyway],
    "2026-07-15": [d15_swithin, d15_sandpile, d15_almanac, d15_rembrandt, d15_rainwindow],
    "2026-07-16": [d16_saturnv, d16_tenprint, d16_almanac, d16_jfk, d16_earthrise],
    "2026-07-17": [d17_hoko, d17_kumiko, d17_almanac, d17_konchikichin, d17_lanterns],
    "2026-07-18": [d18_mandela, d18_life, d18_almanac, d18_quote, d18_savanna],
}

def run_day(day, outdir):
    os.makedirs(outdir, exist_ok=True)
    for i, fn in enumerate(DAYS[day], 1):
        img = fn()
        assert img.size == (W, H)
        img.save(os.path.join(outdir, "%d.png" % i))
        print("  %s/%d.png  (%s)" % (outdir, i, fn.__name__))

if __name__ == "__main__":
    if sys.argv[1] == "all":
        base = sys.argv[2]
        for day in DAYS:
            print(day)
            run_day(day, os.path.join(base, day))
    else:
        run_day(sys.argv[1], sys.argv[2])
