#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-11-10 (Tuesday).

Theme: "calls". Five things that happened on a 10 November, each drawn as the
surface a person was looking at when it happened.

  1. Holding our own — Edmund Fitzgerald, 10 Nov 1975: the radar scope astern.
  2. Eighteen seconds — first coast-to-coast direct-dialled call, 10 Nov 1951.
  3. No. 4            — William Hogarth b. 10 Nov 1697: the seven waving lines.
  4. W S E 2 3        — the first hour of a certain street, Mon 10 Nov 1969.
  5. Tiled            — Windows announced, 10 Nov 1983: windows that cannot overlap.

Run from the repo root:  python3 archive/2026-11-10/generate.py
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

F = "/usr/share/fonts/truetype/"
MONO = F + "jetbrains-mono/JetBrainsMono-Regular.ttf"
MONO_B = F + "jetbrains-mono/JetBrainsMono-Bold.ttf"
MONO_XB = F + "jetbrains-mono/JetBrainsMono-ExtraBold.ttf"
SERIF = F + "freefont/FreeSerif.ttf"
SERIF_B = F + "freefont/FreeSerifBold.ttf"
SERIF_I = F + "liberation/LiberationSerif-Italic.ttf"
SERIF_BI = F + "freefont/FreeSerifBoldItalic.ttf"
LSERIF_B = F + "liberation/LiberationSerif-Bold.ttf"
SANS_B = F + "liberation/LiberationSans-Bold.ttf"
INTER_BLK = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
INTER_XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
SMALL = F + "dejavu/DejaVuSansMono.ttf"  # the most legible face here at 9-10 px, 1-bit
SMALL_B = F + "dejavu/DejaVuSansMono-Bold.ttf"

OUT_DIRS = ["images", "archive/2026-11-10"]


def font(path, size):
    return ImageFont.truetype(path, size)


def _pal(colors):
    p = Image.new("P", (1, 1))
    flat = []
    for c in colors:
        flat += list(c)
    p.putpalette(flat + [0, 0, 0] * (256 - len(colors)))
    return p


PAL3 = _pal([WHITE, BLACK, RED])
PAL2 = _pal([WHITE, BLACK])


def to3(img, dither=False):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL3, dither=d)


def save(img, n, post=None):
    img = to3(img)
    if post:
        img = img.convert("RGB")
        post(crisp(img))
        img = to3(img)
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        img.save(os.path.join(d, f"{n}.png"), optimize=True)


def crisp(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return d


def ctext(d, x, y, s, f, fill, anchor="mm"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def spaced(d, x, y, s, f, fill, gap=2, anchor="m"):
    """Letter-spaced text; x is centre (anchor m) or left (anchor l)."""
    widths = [d.textlength(c, font=f) for c in s]
    total = sum(widths) + gap * (len(s) - 1)
    cx = x - total / 2 if anchor == "m" else x
    for c, w in zip(s, widths):
        d.text((round(cx), y), c, font=f, fill=fill, anchor="ls")
        cx += w + gap
    return total


# ───────────────────────── 1. Holding our own ─────────────────────────
def picture1():
    rng = np.random.default_rng(19751110)
    cx, cy, R = 150, 150, 138
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    dx, dy = xx - cx, yy - cy
    r = np.hypot(dx, dy)
    # bearing clockwise from "up" (ship's head), 0..2pi
    th = np.mod(np.arctan2(dx, -dy), 2 * np.pi)
    inside = r <= R

    def noise(scale, seed):
        g = np.random.default_rng(seed).random((H // scale + 2, W // scale + 2))
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
        return np.array(im).astype(float) / 255

    g = np.zeros((H, W))
    # the sweep: bright leading edge at `sweep`, phosphor afterglow behind it
    sweep = math.radians(52)
    behind = np.mod(sweep - th, 2 * np.pi)
    glow = np.exp(-behind / 1.1)
    g += 0.05 + 0.30 * glow
    # sea clutter: dense near own ship, heavy seas
    clutter = noise(3, 1) * noise(7, 2)
    g += 1.9 * clutter * np.exp(-r / 34) * (0.5 + 0.5 * glow)
    # snow squalls (it was snowing; the squall hid her lights)
    squall = np.clip(noise(26, 3) - 0.52, 0, 1) * noise(2, 4)
    g += 2.3 * squall * (0.35 + 0.65 * glow)
    # the Canadian shore, off the port side
    shore = (np.mod(th - math.radians(250), 2 * np.pi) < math.radians(70)) & (
        r > R * (0.80 + 0.10 * noise(18, 5)))
    g += shore * (0.25 + 0.6 * noise(2, 6)) * (0.4 + 0.6 * glow)
    # range rings (4-mile) and the heading flash
    for k in range(1, 5):
        g += 0.22 * np.exp(-((r - R * k / 4) / 0.8) ** 2)
    g += 0.35 * np.exp(-(dx / 0.7) ** 2) * (dy < 0)
    # sweep line itself
    d_ang = np.abs(np.angle(np.exp(1j * (th - sweep))))
    g += 0.9 * np.exp(-(d_ang * r / 1.0) ** 2) * (r > 3)
    g = np.clip(g, 0, 1) * inside

    gi = Image.fromarray((g * 255).astype(np.uint8), "L").convert("RGB")
    img = gi.quantize(palette=PAL2, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    # invert roles: PAL2 is white/black, so bright=white on black already.
    px = img.load()

    # the contact: ~10 miles ahead, a little to starboard — painted red
    br, rg = math.radians(7), R * 10 / 16
    bx, by = cx + rg * math.sin(br), cy - rg * math.cos(br)
    for j in range(H):
        for i in range(W):
            dd = math.hypot((i - bx) / 1.5, j - by)
            if dd < 2.6:
                px[i, j] = RED
            elif dd < 9 and rng.random() < 0.55 * math.exp(-(dd - 2.6) / 2.2):
                px[i, j] = RED

    d = crisp(img)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=WHITE)
    d.ellipse([cx - R - 3, cy - R - 3, cx + R + 3, cy + R + 3], outline=WHITE)
    # bearing ticks
    for a in range(0, 360, 10):
        t = math.radians(a)
        l = 7 if a % 30 == 0 else 3
        d.line([cx + (R + 3) * math.sin(t), cy - (R + 3) * math.cos(t),
                cx + (R + 3 + l) * math.sin(t), cy - (R + 3 + l) * math.cos(t)], fill=WHITE)
    # own ship
    d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], fill=WHITE)

    # side panel
    x0 = 304
    m9, m10 = font(SMALL, 9), font(SMALL_B, 10)
    d.text((x0, 14), "S.S. ARTHUR M.", font=m9, fill=WHITE)
    d.text((x0, 25), "ANDERSON", font=m9, fill=WHITE)
    d.text((x0, 36), "RADAR 16 MI", font=m9, fill=WHITE)
    d.line([x0, 52, 392, 52], fill=WHITE)
    d.text((x0, 58), "LAKE SUPERIOR", font=m9, fill=WHITE)
    d.text((x0, 69), "MON 10 NOV 1975", font=m9, fill=WHITE)
    d.text((x0, 86), "19:10", font=font(MONO_XB, 26), fill=WHITE)
    it = font(SERIF_BI, 19)
    for k, s in enumerate(["\u201cWe are", "holding", "our own.\u201d"]):
        d.text((x0, 128 + k * 21), s, font=it, fill=WHITE)
    d.line([x0, 200, 392, 200], fill=WHITE)
    d.rectangle([x0, 211, x0 + 5, 216], fill=RED)
    d.text((x0 + 10, 208), "EDMUND", font=m10, fill=WHITE)
    d.text((x0 + 10, 220), "FITZGERALD", font=m10, fill=WHITE)
    d.text((x0, 238), "last on scope", font=m9, fill=WHITE)
    d.text((x0, 249), "about 19:15.", font=m9, fill=WHITE)
    d.text((x0, 264), "29 men.", font=m10, fill=WHITE)
    d.text((x0, 278), "46\u00b059.9'N 85\u00b006.6'W", font=font(SMALL, 8), fill=WHITE)
    save(img, 1)


# ───────────────────────── 2. Eighteen seconds ─────────────────────────
def picture2():
    S = SS
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)
    cx, cy, R = 122 * S, 134 * S, 114 * S

    def circ(x, y, r, **kw):
        d.ellipse([x - r, y - r, x + r, y + r], **kw)

    # number plate (under the wheel) — a ring just outside
    circ(cx, cy, R + 6 * S, fill=WHITE, outline=BLACK, width=2 * S)
    circ(cx, cy, R, fill=BLACK)
    # holes
    letters = {1: "", 2: "ABC", 3: "DEF", 4: "GHI", 5: "JKL", 6: "MNO",
               7: "PRS", 8: "TUV", 9: "WXY", 10: "OPER"}
    dialled = {4, 1, 5, 2, 3, 9, 7}
    hr, ring = 15.5 * S, 86 * S
    fd = font(INTER_BLK, 19 * S)
    for n in range(1, 11):
        a = math.radians(55 + (n - 1) * 28.5)
        x, y = cx + ring * math.cos(a), cy - ring * math.sin(a)
        circ(x, y, hr, fill=WHITE)
        digit = str(n % 10)
        col = RED if (n % 10) in dialled else BLACK
        ctext(d, x, y, digit, fd, col)
    # centre card
    circ(cx, cy, 50 * S, fill=WHITE)
    circ(cx, cy, 46 * S, outline=BLACK, width=S)
    ctext(d, cx, cy - 12 * S, "415", font(INTER_BLK, 32 * S), RED)
    ctext(d, cx, cy + 12 * S, "LAkehurst", font(SERIF_BI, 15 * S), BLACK)
    ctext(d, cx, cy + 28 * S, "3-9727", font(MONO_XB, 13 * S), BLACK)
    # finger stop
    a = math.radians(-12)
    x1, y1 = cx + (R + 12 * S) * math.cos(a), cy - (R + 12 * S) * math.sin(a)
    x2, y2 = cx + (ring - 4 * S) * math.cos(a), cy - (ring - 4 * S) * math.sin(a)
    d.line([x1, y1, x2, y2], fill=WHITE, width=11 * S)
    d.line([x1, y1, x2, y2], fill=RED, width=6 * S)
    circ(x2, y2, 3 * S, fill=RED)

    # right column: the ten digits as pulse trains
    x0 = 262 * S
    d.text((x0, 8 * S), "18", font=font(INTER_BLK, 44 * S), fill=BLACK)
    d.text((x0 + 62 * S, 17 * S), "seconds", font=font(SERIF_BI, 20 * S), fill=BLACK)
    d.text((x0 + 62 * S, 39 * S), "to ring.", font=font(SERIF_I, 14 * S), fill=BLACK)
    seq = [("4", 4), ("1", 1), ("5", 5), ("L", 5), ("A", 2), ("3", 3),
           ("9", 9), ("7", 7), ("2", 2), ("7", 7)]
    fb = font(MONO_XB, 12 * S)
    y = 66 * S
    for k, (lab, n) in enumerate(seq):
        if k in (3, 5):
            y += 5 * S
        d.text((x0, y), lab, font=fb, fill=BLACK)
        for i in range(n):
            xx = x0 + 18 * S + i * 11 * S
            d.rectangle([xx, y + 3 * S, xx + 6 * S, y + 12 * S], fill=RED)
        d.line([x0 + 18 * S, y + 14 * S, x0 + 127 * S, y + 14 * S], fill=BLACK, width=1)
        y += 17 * S
    ynote = y // S + 3

    # footer
    d.line([10 * S, 262 * S, 390 * S, 262 * S], fill=BLACK, width=S)

    def post(p):
        f = font(SMALL, 10)
        p.text((262, ynote), "45 clicks, no operator", font=f, fill=BLACK)
        p.text((10, 267), "SAT 10 NOV 1951, 1 P.M.  Mayor Denning of Englewood, N.J.", font=f, fill=BLACK)
        p.text((10, 280), "dials Mayor Osborn of Alameda, California, himself.", font=f, fill=BLACK)

    save(img, 2, post)


# ───────────────────────── 3. No. 4 ─────────────────────────
def picture3():
    S = SS
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)
    # plate mark
    d.rectangle([6 * S, 6 * S, 394 * S - 1, 294 * S - 1], outline=BLACK, width=S)
    d.rectangle([10 * S, 10 * S, 390 * S - 1, 290 * S - 1], outline=BLACK, width=1)

    spaced(d, 200 * S, 34 * S, "THE ANALYSIS OF BEAUTY", font(SERIF_B, 17 * S), BLACK, gap=3 * S)

    top, bot = 66 * S, 206 * S
    xs = [52, 100, 148, 200, 252, 302, 354]
    amps = [1.5, 5, 9.5, 15, 21, 28, 36]
    for k, (x, a) in enumerate(zip(xs, amps)):
        col = RED if k == 3 else BLACK
        n = 500
        for i in range(n):
            t = i / (n - 1)
            px = x * S + a * S * math.sin(2 * math.pi * t)
            py = top + (bot - top) * t
            # engraver's swelling stroke: thin at the tips, fat in the belly
            wdt = (0.7 + (3.4 if k == 3 else 2.4) * math.sin(math.pi * t) ** 1.5) * S
            d.ellipse([px - wdt / 2, py - wdt / 2, px + wdt / 2, py + wdt / 2], fill=col)
        ctext(d, x * S, 220 * S, str(k + 1), font(SERIF_B if k == 3 else SERIF, 15 * S), col)

    # braces under 1-3 and 5-7
    labels = []

    def brace(xa, xb, y, label):
        d.line([xa * S, y * S, xa * S, (y + 4) * S], fill=BLACK, width=S)
        d.line([xb * S, y * S, xb * S, (y + 4) * S], fill=BLACK, width=S)
        d.line([xa * S, (y + 4) * S, xb * S, (y + 4) * S], fill=BLACK, width=S)
        labels.append(((xa + xb) / 2, y + 14, label))

    brace(44, 156, 231, "\u201cmean and poor\u201d")
    brace(244, 362, 231, "\u201cgross and clumsy\u201d")
    ctext(d, 200 * S, 238 * S, "\u25b2", font(F + "dejavu/DejaVuSans.ttf", 8 * S), RED)

    def post(p):
        fi = font(SERIF_I, 13)
        ctext(p, 200, 49, "Plate I, fig. 49: the seven waving lines", fi, BLACK)
        for x, y, s_ in labels:
            ctext(p, x, y, s_, fi, BLACK)
        fb = font(SERIF_BI, 15)
        ctext(p, 200, 249, "the line", fb, RED)
        ctext(p, 200, 263, "of beauty", fb, RED)
        ctext(p, 200, 280, "WILLIAM HOGARTH, BORN IN LONDON 10 NOVEMBER 1697", font(SMALL, 10), BLACK)

    save(img, 3, post)


# ───────────────────────── 4. W S E 2 3 ─────────────────────────
def picture4():
    S = SS
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)
    cw, rh = 400 / 3, 130
    cells = [
        (0, 0, "W", INTER_BLK, 118, BLACK, WHITE, 0),
        (1, 0, "S", SERIF_BI, 150, WHITE, RED, -4),
        (2, 0, "E", MONO_XB, 132, RED, WHITE, -2),
        (0, 1, "2", LSERIF_B, 150, WHITE, BLACK, 4),
        (1, 1, "3", INTER_BLK, 128, BLACK, WHITE, 0),
    ]
    for cxi, ryi, ch, fp, size, bg, fg, dy in cells:
        x0, y0 = cxi * cw * S, ryi * rh * S
        x1, y1 = (cxi + 1) * cw * S, (ryi + 1) * rh * S
        d.rectangle([x0, y0, x1, y1], fill=bg)
        f = font(fp, size * S)
        bb = d.textbbox((0, 0), ch, font=f)
        tx = (x0 + x1) / 2 - (bb[0] + bb[2]) / 2
        ty = (y0 + y1) / 2 - (bb[1] + bb[3]) / 2 + dy * S
        d.text((tx, ty), ch, font=f, fill=fg)
    # the white "W" cell and the white "3" cell get a dotted Ben-Day corner for texture
    for (gx, gy) in [(0, 0), (1, 1)]:
        for j in range(4):
            for i in range(4 - j):
                x = (gx * cw + 9 + i * 7) * S
                y = (gy * rh + 9 + j * 7) * S
                d.ellipse([x - 2 * S, y - 2 * S, x + 2 * S, y + 2 * S], fill=RED)
    # sixth cell: the announcement
    x0, y0 = 2 * cw * S, rh * S
    d.rectangle([x0, y0, W * S, 2 * rh * S], fill=RED)
    lines = [("TODAY IS", INTER_XB, 12, 13.5), ("BROUGHT TO", INTER_XB, 12, 13.5),
             ("YOU BY THE", INTER_XB, 12, 13.5), ("LETTERS", INTER_XB, 12, 15),
             ("W, S and E", SERIF_BI, 19, 18), ("AND THE", INTER_XB, 12, 16),
             ("NUMBERS", INTER_XB, 12, 13.5), ("2 and 3.", SERIF_BI, 19, 18)]
    y = y0 + 139 * S
    for s, fp, sz, lead in reversed(lines):
        y -= lead * S
        d.text((x0 + 12 * S, y), s, font=font(fp, sz * S), fill=WHITE, anchor="ls")
    # grid rules
    for k in (1, 2):
        d.line([k * cw * S, 0, k * cw * S, 2 * rh * S], fill=BLACK, width=2 * S)
    d.line([0, rh * S, W * S, rh * S], fill=BLACK, width=2 * S)
    d.rectangle([0, 2 * rh * S, W * S, H * S], fill=BLACK)

    def post(p):
        ctext(p, 200, 273, "...as was the very first hour, on a street in New York,", font(SMALL, 10), WHITE)
        ctext(p, 200, 287, "MONDAY 10 NOVEMBER 1969", font(SMALL_B, 10), WHITE)

    save(img, 4, post)


# ───────────────────────── 5. Tiled ─────────────────────────
def picture5():
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    m9, m9b = font(SMALL, 10), font(SMALL_B, 9)
    px = img.load()

    def window(x0, y0, x1, y1, title, active=False):
        d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=BLACK)
        bar = RED if active else BLACK
        d.rectangle([x0, y0, x1, y0 + 12], fill=bar)
        # system-menu box and title
        d.rectangle([x0 + 2, y0 + 2, x0 + 10, y0 + 10], fill=WHITE)
        d.line([x0 + 4, y0 + 6, x0 + 8, y0 + 6], fill=BLACK)
        d.text(((x0 + x1) // 2 + 4, y0 + 6), title, font=m9b, fill=WHITE, anchor="mm")
        return x0 + 1, y0 + 13, x1 - 1, y1 - 1

    def menubar(x0, y0, x1, items):
        x = x0 + 4
        for s in items:
            d.text((x, y0 + 1), s, font=m9, fill=BLACK)
            x += d.textlength(s, font=m9) + 9
        d.line([x0, y0 + 12, x1, y0 + 12], fill=BLACK)
        return y0 + 13

    bottom = 262  # icon area below

    # ── MS-DOS Executive (top left)
    x0, y0, x1, y1 = window(0, 0, 150, 118, "MS-DOS Executive")
    yy = menubar(x0, y0, x1, ["File", "View", "Special"])
    d.rectangle([x0 + 4, yy + 3, x0 + 22, yy + 13], outline=BLACK)
    d.text((x0 + 8, yy + 4), "A", font=m9b, fill=BLACK)
    d.rectangle([x0 + 27, yy + 3, x0 + 45, yy + 13], fill=BLACK)
    d.text((x0 + 31, yy + 4), "C", font=m9b, fill=WHITE)
    d.text((x0 + 52, yy + 4), "C:\\1983", font=m9, fill=BLACK)
    files = ["CALENDAR.EXE", "CLOCK.EXE", "NOTEPAD.EXE", "REVERSI.EXE",
             "TODAY.TXT", "WIN.COM"]
    for k, s in enumerate(files):
        ty = yy + 19 + k * 11
        if s == "TODAY.TXT":
            d.rectangle([x0 + 3, ty, x0 + 80, ty + 10], fill=BLACK)
            d.text((x0 + 5, ty), s, font=m9, fill=WHITE)
        else:
            d.text((x0 + 5, ty), s, font=m9, fill=BLACK)

    # ── Clock (bottom left) — hands at 11:10, for the 10th of the 11th
    x0, y0, x1, y1 = window(0, 118, 150, bottom, "Clock")
    ccx, ccy, cr = (x0 + x1) // 2, (y0 + y1) // 2, 58
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=BLACK, width=2)
    for k in range(60):
        a = math.radians(k * 6)
        if k % 5 == 0:
            bx, by = ccx + (cr - 8) * math.sin(a), ccy - (cr - 8) * math.cos(a)
            d.rectangle([bx - 2, by - 2, bx + 2, by + 2], fill=BLACK)
        else:
            px[int(round(ccx + (cr - 6) * math.sin(a))), int(round(ccy - (cr - 6) * math.cos(a)))] = BLACK

    def hand(angle_deg, length, width, col):
        a = math.radians(angle_deg)
        d.line([ccx, ccy, ccx + length * math.sin(a), ccy - length * math.cos(a)], fill=col, width=width)

    hand((11 + 10 / 60) * 30, 30, 5, BLACK)
    hand(10 * 6, 44, 3, BLACK)
    hand(37 * 6, 48, 1, RED)
    d.ellipse([ccx - 3, ccy - 3, ccx + 3, ccy + 3], fill=RED)

    # ── Notepad (middle, active)
    x0, y0, x1, y1 = window(150, 0, 290, bottom, "Notepad - TODAY.TXT", active=True)
    yy = menubar(x0, y0, x1, ["File", "Edit", "Search"])
    text = ["New York, Thursday",
            "10 November 1983.",
            "",
            "At the Helmsley",
            "Palace a company",
            "from Bellevue",
            "announces a thing",
            "called Windows.",
            "",
            "It will ship two",
            "years late, on",
            "20 November 1985.",
            "",
            "Its windows tile.",
            "They may never",
            "overlap, so every",
            "one of them gets",
            "to be seen."]
    for k, s in enumerate(text):
        d.text((x0 + 6, yy + 5 + k * 12), s, font=m9, fill=BLACK)
    # caret
    cxp = x0 + 6 + d.textlength(text[-1], font=m9) + 2
    d.rectangle([cxp, yy + 5 + 17 * 12, cxp + 1, yy + 15 + 17 * 12], fill=RED)

    # ── Reversi (top right)
    x0, y0, x1, y1 = window(290, 0, 399, 132, "Reversi")
    yy = menubar(x0, y0, x1, ["Game", "Skill"])
    cs = 12
    gx, gy = x0 + (x1 - x0 - 8 * cs) // 2, yy + 4
    board = ["........",
             "..o.....",
             "..ox.x..",
             "..oxxo..",
             "...xoo..",
             "..xoxo..",
             ".....o..",
             "........"]
    for j in range(8):
        for i in range(8):
            X, Y = gx + i * cs, gy + j * cs
            d.rectangle([X, Y, X + cs, Y + cs], outline=BLACK)
            c = board[j][i]
            if c == "x":
                d.ellipse([X + 2, Y + 2, X + cs - 2, Y + cs - 2], fill=RED)
            elif c == "o":
                d.ellipse([X + 2, Y + 2, X + cs - 2, Y + cs - 2], fill=BLACK)

    # ── Calendar (bottom right) — November 2026, starts on a Sunday
    x0, y0, x1, y1 = window(290, 132, 399, bottom, "Calendar")
    d.text(((x0 + x1) // 2, y0 + 8), "NOVEMBER 2026", font=m9b, fill=BLACK, anchor="mm")
    d.line([x0, y0 + 15, x1, y0 + 15], fill=BLACK)
    colw = 15
    ox = x0 + 2
    for i, c in enumerate("SMTWTFS"):
        d.text((ox + i * colw + 7, y0 + 22), c, font=m9b, fill=BLACK, anchor="mm")
    for day in range(1, 31):
        i, j = (day - 1) % 7, (day - 1) // 7
        X, Y = ox + i * colw + 7, y0 + 36 + j * 15
        if day == 10:
            d.rectangle([X - 7, Y - 7, X + 7, Y + 6], fill=RED)
            d.text((X, Y), str(day), font=m9b, fill=WHITE, anchor="mm")
        else:
            d.text((X, Y), str(day), font=font(SMALL, 9), fill=BLACK, anchor="mm")

    # ── icon area: 50% checker "grey", with three minimised icons
    for j in range(bottom + 1, H):
        for i in range(W):
            px[i, j] = BLACK if (i + j) % 2 == 0 else WHITE
    d.line([0, bottom, W, bottom], fill=BLACK)
    for k, lab in enumerate(["PAINT", "WRITE", "CARDFILE"]):
        X = 14 + k * 78
        d.rectangle([X, bottom + 6, X + 26, bottom + 31], fill=WHITE, outline=BLACK)
        if k == 0:
            d.line([X + 5, bottom + 26, X + 21, bottom + 11], fill=RED, width=3)
        elif k == 1:
            for r in range(4):
                d.line([X + 5, bottom + 12 + r * 5, X + 21 - (r % 2) * 5, bottom + 12 + r * 5], fill=BLACK)
        else:
            d.rectangle([X + 4, bottom + 14, X + 22, bottom + 27], outline=BLACK)
            d.rectangle([X + 4, bottom + 10, X + 12, bottom + 14], outline=BLACK)
            d.line([X + 7, bottom + 19, X + 19, bottom + 19], fill=RED)
        tw = int(d.textlength(lab, font=m9b))
        d.rectangle([X + 30, bottom + 13, X + 34 + tw, bottom + 25], fill=WHITE)
        d.text((X + 32, bottom + 14), lab, font=m9b, fill=BLACK)
    save(img, 5)


if __name__ == "__main__":
    picture1()
    picture2()
    picture3()
    picture4()
    picture5()
    print("done")
