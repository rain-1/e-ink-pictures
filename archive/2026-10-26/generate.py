#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-26 (Monday).

Five 400x300 images in exactly three colors (white, black, red).
Hooks for the day: the full Hunter's Moon (04:12 UTC today) heading for the
Pleiades, which it occults over London in the small hours of Wednesday;
the Erie Canal opening on 26 Oct 1825 (news sent down the line by cannon);
the Football Association founded on 26 Oct 1863 (Law I: no lines, no
crossbar); the last naturally occurring case of smallpox, Merca, Somalia,
26 Oct 1977; and the spring tides that follow every full moon.

Run from the repo root:  python3 archive/2026-10-26/generate.py
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F = "/usr/share/fonts/truetype/"
MONO = F + "jetbrains-mono/JetBrainsMono-Regular.ttf"
MONO_B = F + "jetbrains-mono/JetBrainsMono-Bold.ttf"
MONO_XB = F + "jetbrains-mono/JetBrainsMono-ExtraBold.ttf"
SERIF = F + "freefont/FreeSerif.ttf"
SERIF_B = F + "freefont/FreeSerifBold.ttf"
SERIF_I = F + "liberation/LiberationSerif-Italic.ttf"  # hints cleanly at 12-13 px
SERIF_BI = F + "freefont/FreeSerifBoldItalic.ttf"

OUT_DIRS = ["images", "archive/2026-10-26"]


def font(path, size):
    return ImageFont.truetype(path, size)


def _palette():
    p = Image.new("P", (1, 1))
    p.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)
    return p


PAL = _palette()


def finalize(img, dither=True):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def canvas1(bg=WHITE):
    img = Image.new("RGB", (W, H), bg)
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    return img, dr


def value_noise(w, h, seed, octaves=5):
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w))
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = 2 ** (o + 2)
        g = rng.random((n, n))
        layer = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), float) / 255
        acc += amp * layer
        tot += amp
        amp *= 0.55
    return acc / tot


# ------------------------------------------------------------ 1. Seven Sisters
# J2000 positions and V magnitudes of the bright Pleiades.
PLEIADES = [
    ("Alcyone", "3:47:29.1", "24:06:18", 2.87),
    ("Atlas", "3:49:09.7", "24:03:12", 3.62),
    ("Electra", "3:44:52.5", "24:06:48", 3.70),
    ("Maia", "3:45:49.6", "24:22:04", 3.87),
    ("Merope", "3:46:19.6", "23:56:54", 4.18),
    ("Taygeta", "3:45:12.5", "24:28:02", 4.29),
    ("Pleione", "3:49:11.2", "24:08:12", 5.05),
    ("Celaeno", "3:44:48.2", "24:17:22", 5.45),
    ("Asterope", "3:45:54.5", "24:33:16", 5.76),
]
# Topocentric Moon for London (51.5N, 0.13W), from PyEphem, computed for this
# script: (UTC on Wed 28 Oct 2026, dRA*cos(dec) arcmin, dDec arcmin) relative
# to Alcyone. Apparent lunar radius 16.66'.
MOON_TRACK = [
    ("00:00", -58.9, 16.2), ("00:30", -45.5, 20.8),
    ("01:00", -32.3, 25.2), ("01:30", -19.0, 29.2), ("02:00", -5.8, 33.0),
    ("02:30", 7.6, 36.4), ("03:00", 21.2, 39.6), ("03:30", 35.0, 42.5),
]
MOON_R = 16.66
# Disappearance / reappearance (UTC) from London, same computation.
OCCULTED = {"Celaeno": ("00:17", "01:07"), "Taygeta": ("00:26", "01:36"),
            "Asterope": ("00:48", "02:00"), "Maia": ("00:49", "01:40")}


def _hms(s):
    p = [float(x) for x in s.split(":")]
    return p[0] + p[1] / 60 + p[2] / 3600


def image1_seven_sisters():
    """The Moon's path across the Pleiades as seen from London, in the small
    hours of Wednesday. Black sky, north up, east to the left. Ghost outlines
    every half hour; the solid disc sits where it will be at 01:00, hiding
    the four sisters it covers (marked with red ticks)."""
    S = SS
    img = Image.new("RGB", (W * S, H * S), BLACK)
    dr = ImageDraw.Draw(img)
    scale = 2.25 * S                       # px per arcminute
    ox, oy = 214 * S, 208 * S              # where Alcyone sits
    a_ra, a_de = _hms(PLEIADES[0][1]) * 15, _hms(PLEIADES[0][2])

    def sky(dx, dy):                       # east is left on a sky chart
        return ox - dx * scale, oy - dy * scale

    stars = {}
    for name, ra, de, mag in PLEIADES:
        dx = (_hms(ra) * 15 - a_ra) * math.cos(math.radians(a_de)) * 60
        dy = (_hms(de) - a_de) * 60
        stars[name] = (sky(dx, dy), mag)

    # faint field stars (seeded) so the black isn't empty
    rng = np.random.default_rng(1026)
    for _ in range(160):
        x, y = rng.uniform(0, W * S), rng.uniform(0, H * S)
        r = rng.choice([0.6, 0.8, 1.0, 1.4]) * S
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(120, 120, 120))

    # ghost moons
    R = MOON_R * scale
    for t, dx, dy in MOON_TRACK:
        cx, cy = sky(dx, dy)
        n = 90
        for k in range(n):
            if k % 2:
                continue
            a0, a1 = 360 * k / n, 360 * (k + 1) / n
            dr.arc([cx - R, cy - R, cx + R, cy + R], a0, a1, fill=WHITE, width=S)
    # centre line of the track
    pts = [sky(dx, dy) for _, dx, dy in MOON_TRACK]
    dr.line(pts, fill=(150, 150, 150), width=S)

    # stars
    for name, ((x, y), mag) in stars.items():
        r = (4.6 - 0.75 * mag) * S
        col = RED if name in OCCULTED else WHITE
        dr.ellipse([x - r, y - r, x + r, y + r], fill=col)
        if mag < 3.0:  # little diffraction cross for Alcyone
            dr.line([x - 2.6 * r, y, x + 2.6 * r, y], fill=WHITE, width=S)
            dr.line([x, y - 2.6 * r, x, y + 2.6 * r], fill=WHITE, width=S)

    # the solid Moon at 01:00 — bright disc with dithered maria
    cx, cy = sky(-32.3, 25.2)
    size = int(2 * R) + 2
    yy, xx = np.mgrid[0:size, 0:size]
    d = np.hypot(xx - size / 2, yy - size / 2) / R
    maria = value_noise(size, size, 77, octaves=4)
    tone = 255 - np.clip((maria - 0.52) * 520, 0, 120) - 30 * d ** 4
    disc = np.where(d <= 1, tone, 0).astype(np.uint8)
    mask = Image.fromarray(np.where(d <= 1, 255, 0).astype(np.uint8))
    moon = Image.merge("RGB", [Image.fromarray(disc)] * 3)
    img.paste(moon, (int(cx - size / 2), int(cy - size / 2)), mask)
    hidden = []
    # the hidden sisters: red ticks on the disc where they are
    for name in OCCULTED:
        (x, y), _ = stars[name]
        if math.hypot(x - cx, y - cy) < R:
            hidden.append((x / S, y / S))

    img = finalize(img).convert("RGB")
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"

    for x, y in hidden:  # crisp red ticks at 1x
        dr.line([x - 5, y, x - 2, y], fill=RED, width=2)
        dr.line([x + 2, y, x + 5, y], fill=RED, width=2)
        dr.line([x, y - 5, x, y - 2], fill=RED, width=2)
        dr.line([x, y + 2, x, y + 5], fill=RED, width=2)

    # labels at 1x
    f9 = font(MONO, 9)
    for t, dx, dy in MOON_TRACK[::2]:
        x, y = sky(dx, dy)
        x, y = x / S, y / S
        dr.text((x, y - MOON_R * scale / S - 12), t, font=f9, fill=WHITE, anchor="mm")
    lab = {"Alcyone": (8, 6), "Atlas": (0, 9), "Pleione": (2, -9), "Merope": (6, 6),
           "Electra": (-4, 9)}
    for name, (ddx, ddy) in lab.items():
        (x, y), _ = stars[name]
        dr.text((x / S + ddx, y / S + ddy), name.lower(), font=f9, fill=WHITE,
                anchor="lm" if ddx > 0 else "mm")

    dr.text((12, 10), "SEVEN SISTERS", font=font(MONO_XB, 18), fill=WHITE)
    dr.text((12, 31), "the Moon walks through the Pleiades", font=font(SERIF_I, 13), fill=WHITE)
    dr.text((12, 47), "London · night of Tue 27 → Wed 28 Oct (GMT)", font=f9, fill=WHITE)
    y0 = 236
    dr.text((12, y0), "COVERED", font=font(MONO_B, 9), fill=RED)
    for i, (name, (a, b)) in enumerate(OCCULTED.items()):
        dr.text((12, y0 + 12 + 11 * i), f"{name.lower():<9}{a}–{b}", font=f9, fill=WHITE)
    dr.text((388, 290), "full moon today 04:12 UTC · N up, E left", font=f9, fill=WHITE, anchor="rs")
    return img


# ------------------------------------------------------------ 2. Erie Canal
# Schematic profile along the 1825 route (miles from Buffalo, feet above
# the Hudson). Steps are locks; real lock counts are folded together.
CANAL = [
    (0, 565), (28, 565), (30, 505), (93, 505), (130, 440), (150, 385),
    (175, 400), (213, 420), (228, 420), (260, 320), (290, 260), (330, 215),
    (350, 180), (355, 30), (363, 0),
]
HUDSON_END = 363 + 150


def _canal_elev(m):
    if m >= 363:
        return 0
    for (m0, e0), (m1, e1) in zip(CANAL, CANAL[1:]):
        if m0 <= m <= m1:
            return e0 if m < m1 else e1
    return 0


def image2_erie():
    """The canal's profile as a lock staircase, with a cannon every ~10 miles
    below it. On 26 Oct 1825 the first gun at Buffalo fired at 10 a.m. and each
    gun answered the one before; the sound reached New York in about 81
    minutes. Seneca Chief, carrying Governor Clinton and a keg of Lake Erie,
    took until 4 November."""
    img, dr = canvas1()
    x0, x1 = 24, 384
    yb, ytop = 150, 74

    def X(m):
        return x0 + (x1 - x0) * m / HUDSON_END

    def Y(e):
        return yb - (yb - ytop) * e / 565

    # water body under the profile: hatched
    for m in range(0, HUDSON_END + 1):
        x = X(m)
        if int(x) % 3 == 0:
            dr.line([x, Y(_canal_elev(m)) + 2, x, yb], fill=BLACK)
    # staircase outline: each drop is a lock
    pts = []
    for (m0, e0), (m1, e1) in zip(CANAL, CANAL[1:]):
        if e0 == e1:
            pts += [(X(m0), Y(e0)), (X(m1), Y(e1))]
        else:
            steps = max(1, abs(e1 - e0) // 22)
            for k in range(steps):
                ma = m0 + (m1 - m0) * k / steps
                mb = m0 + (m1 - m0) * (k + 1) / steps
                ea = e0 + (e1 - e0) * k / steps
                eb = e0 + (e1 - e0) * (k + 1) / steps
                pts += [(X(ma), Y(ea)), (X(mb), Y(ea)), (X(mb), Y(eb))]
    pts += [(X(HUDSON_END), Y(0))]
    dr.line(pts, fill=BLACK, width=2)
    dr.line([X(0), yb, X(HUDSON_END), yb], fill=BLACK)

    f9 = font(MONO, 9)
    for m, name in [(0, "BUFFALO"), (160, "Syracuse"), (228, "Utica"),
                    (363, "ALBANY"), (HUDSON_END, "NEW YORK")]:
        dr.line([X(m), yb, X(m), yb + 3], fill=BLACK)
        anc = "lt" if m == 0 else ("rt" if m == HUDSON_END else "mt")
        dr.text((X(m), yb + 5), name, font=f9, fill=BLACK, anchor=anc)
    dr.text((X(440), Y(0) - 6), "Hudson River", font=font(SERIF_I, 12), fill=BLACK, anchor="ms")
    dr.text((X(0), Y(565) - 4), "Lake Erie, 565 ft", font=f9, fill=BLACK, anchor="ls")

    # the line of guns, and the red sound front
    yg = 180
    guns = list(range(0, HUDSON_END + 1, 15)) + [HUDSON_END]
    for m in guns:
        x = X(m)
        dr.rectangle([x - 1, yg, x + 1, yg + 3], fill=BLACK)      # carriage
        dr.line([x, yg, x + 3, yg - 2], fill=BLACK)               # barrel
    for m in guns[::1]:
        x = X(m)
        dr.ellipse([x + 3, yg - 6, x + 8, yg - 1], fill=RED)       # puff
    # time axis: minutes after 10:00
    yt = 200
    dr.line([x0, yt, x1, yt], fill=BLACK)
    for mins in range(0, 82, 10):
        x = x0 + (x1 - x0) * mins / 81
        dr.line([x, yt, x, yt + 3], fill=BLACK)
        dr.text((x, yt + 5), f"{10 + mins // 60}:{mins % 60:02d}", font=f9, fill=BLACK, anchor="mt")
    dr.line([x0, yt - 1, x1, yt - 1], fill=RED)
    dr.line([x0, yt - 2, x1, yt - 2], fill=RED)
    dr.text((x1, yt + 15), "≈11:21", font=font(MONO_B, 9), fill=RED, anchor="rt")

    # title + comparison
    dr.text((24, 12), "NEWS BY GUNFIRE", font=font(MONO_XB, 18), fill=BLACK)
    dr.text((24, 33), "Erie Canal opens · Wednesday 26 October 1825", font=font(SERIF_I, 13), fill=BLACK)
    dr.text((384, 14), "363 mi", font=f9, fill=BLACK, anchor="ra")
    dr.text((384, 25), "83 locks", font=f9, fill=BLACK, anchor="ra")
    dr.text((384, 36), "(schematic)", font=font(MONO, 8), fill=BLACK, anchor="ra")
    dr.line([24, 228, 384, 228], fill=BLACK)
    big = font(MONO_XB, 26)
    dr.text((24, 234), "81 min", font=big, fill=RED)
    dr.text((24, 266), "the sound of the guns,\nBuffalo to Sandy Hook", font=f9, fill=BLACK, spacing=1)
    dr.text((214, 234), "9 days", font=big, fill=BLACK)
    dr.text((214, 266), "Seneca Chief, with a keg\nof Lake Erie for the sea", font=f9, fill=BLACK, spacing=1)
    return img


# ------------------------------------------------------------ 3. Law I
def image3_law_one():
    """A page from an imagined 1863 rule-book: the largest ground Law I
    allows, drawn to scale. Flags at the corners, two posts eight yards apart
    at each end — and nothing else: no lines, no crossbar."""
    S = SS
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)
    # pitch 200 x 100 yd at 1.3 px/yd
    k = 1.25 * S
    px0, py0 = 75 * S, 112 * S
    pw, ph = 200 * k, 100 * k
    # turf: sparse stipple that thins toward the edges, mown stripes
    rng = np.random.default_rng(1863)
    for i in range(4200):
        x = rng.uniform(px0, px0 + pw)
        y = rng.uniform(py0, py0 + ph)
        stripe = int((x - px0) / (20 * k)) % 2
        if rng.random() < (0.6 if stripe else 0.25):
            dr.line([x, y, x + rng.uniform(-1, 1) * S, y - 2.2 * S], fill=(90, 90, 90), width=S)
    # corner flags
    for fx, fy in [(px0, py0), (px0 + pw, py0), (px0, py0 + ph), (px0 + pw, py0 + ph)]:
        dr.line([fx, fy, fx, fy - 13 * S], fill=BLACK, width=S)
        dr.polygon([(fx, fy - 13 * S), (fx + 9 * S, fy - 10 * S), (fx, fy - 7 * S)], fill=RED)
    # goals: posts 8 yd apart, no bar
    for gx in [px0, px0 + pw]:
        for gy in [py0 + ph / 2 - 4 * k, py0 + ph / 2 + 4 * k]:
            r = 2.2 * S
            dr.ellipse([gx - r, gy - r, gx + r, gy + r], fill=BLACK)
    # one ball, mid-field
    bx, by = px0 + pw * 0.56, py0 + ph * 0.43
    dr.ellipse([bx - 3 * S, by - 3 * S, bx + 3 * S, by + 3 * S], fill=RED)
    img = finalize(img, dither=False).convert("RGB")
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"

    f9 = font(MONO, 9)
    X0, Y0, PW, PH = px0 / S, py0 / S, pw / S, ph / S
    # dimension lines
    yd = Y0 + PH + 14
    dr.line([X0, yd, X0 + PW, yd], fill=BLACK)
    for x in (X0, X0 + PW):
        dr.line([x, yd - 3, x, yd + 3], fill=BLACK)
    dr.rectangle([X0 + PW / 2 - 26, yd - 5, X0 + PW / 2 + 26, yd + 5], fill=WHITE)
    dr.text((X0 + PW / 2, yd), "200 yds", font=f9, fill=BLACK, anchor="mm")
    xd = X0 - 16
    dr.line([xd, Y0, xd, Y0 + PH], fill=BLACK)
    for y in (Y0, Y0 + PH):
        dr.line([xd - 3, y, xd + 3, y], fill=BLACK)
    dr.rectangle([xd - 6, Y0 + PH / 2 - 20, xd + 6, Y0 + PH / 2 + 20], fill=WHITE)
    tmp = Image.new("L", (44, 12), 255)
    td = ImageDraw.Draw(tmp)
    td.fontmode = "1"
    td.text((22, 6), "100 yds", font=f9, fill=0, anchor="mm")
    tmp = tmp.rotate(90, expand=True)
    img.paste(Image.new("RGB", tmp.size, BLACK), (int(xd - 6), int(Y0 + PH / 2 - 22)),
              tmp.point(lambda v: 255 - v))
    gx = X0 + PW + 6
    dr.text((gx + 4, Y0 + PH / 2), "8 yds", font=f9, fill=BLACK, anchor="lm")
    dr.text((gx + 4, Y0 + PH / 2 + 11), "no bar", font=f9, fill=RED, anchor="lm")

    # header like a rule-book page
    dr.line([20, 12, 380, 12], fill=BLACK, width=2)
    dr.line([20, 15, 380, 15], fill=BLACK)
    dr.text((200, 22), "LAWS OF THE GAME", font=font(SERIF_B, 17), fill=BLACK, anchor="mt")
    dr.text((200, 42), "I.", font=font(SERIF_B, 15), fill=RED, anchor="mt")
    q = ("“The maximum length of the ground shall be 200 yards, the maximum breadth\n"
         "100 yards, the length and breadth shall be marked off with flags; and the goals\n"
         "defined by two upright posts, eight yards apart, without any tape or bar.”")
    dr.multiline_text((200, 61), q, font=font(SERIF_I, 11), fill=BLACK, anchor="ma", align="center", spacing=1)
    dr.line([20, 268, 380, 268], fill=BLACK)
    dr.text((20, 274), "THE FOOTBALL ASSOCIATION · Freemasons' Tavern, Great Queen St", font=f9, fill=BLACK)
    dr.text((20, 286), "Monday 26 Oct 1863 · no lines yet: the flags were the field", font=f9, fill=BLACK)
    dr.text((380, 286), "163", font=font(MONO_B, 9), fill=RED, anchor="ra")
    return img


# ------------------------------------------------------------ 4. Merca
def image4_merca():
    """A bifurcated vaccination needle, drawn large: a cheap steel rod whose
    flattened, forked end holds one dose of vaccine between its tines by
    surface tension. It carried the eradication campaign to its end."""
    S = SS
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)
    ang = math.radians(-27)
    ux, uy = math.cos(ang), math.sin(ang)
    vx, vy = -uy, ux
    bx, by = 13 * S, 316 * S                 # butt end, just off-page bottom-left

    def P(s, t):
        return (bx + (ux * s + vx * t) * S, by + (uy * s + vy * t) * S)

    L, hw = 300, 6.0                         # rod length, half-width (1x px)
    fork0, fl = L, 56                        # flattened fork starts at L
    # rod body with engraved shading: hatch lines along the shadow side
    dr.polygon([P(0, -hw), P(L, -hw), P(L, hw), P(0, hw)], fill=WHITE, outline=BLACK, width=S)
    for t in (1.6, 3.2):
        dr.line([P(0, t), P(L - 2, t)], fill=BLACK, width=S)
    dr.line([P(0, -2.6), P(L - 2, -2.6)], fill=BLACK, width=S // 2 + 1)
    # shoulder where the rod is flattened
    sh = [P(L, -hw), P(L + 10, -hw * 1.5), P(L + 10, hw * 1.5), P(L, hw)]
    dr.polygon(sh, fill=WHITE, outline=BLACK, width=S)
    # two tines with a slot between them
    gap, tw = 2.4, 4.2
    for sg in (-1, 1):
        poly = [P(L + 10, sg * gap), P(L + 10, sg * hw * 1.5),
                P(L + fl - 4, sg * (gap + tw * 0.8)), P(L + fl, sg * (gap + 0.6)),
                P(L + fl - 1, sg * gap)]
        dr.polygon(poly, fill=WHITE, outline=BLACK, width=S)
        dr.line([P(L + 12, sg * (gap + 1.6)), P(L + fl - 6, sg * (gap + 1.4))], fill=BLACK, width=S)
    # the dose, a red bead in the slot near the tips
    for s_ in range(int(L + fl - 16), int(L + fl - 3)):
        a, b = P(s_, -gap + 0.3), P(s_, gap - 0.3)
        dr.line([a, b], fill=RED, width=S)
    cx, cy = P(L + fl - 4, 0)
    r = 3.0 * S
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    img = finalize(img, dither=False).convert("RGB")
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"

    dr.text((20, 16), "MERCA", font=font(MONO_XB, 30), fill=BLACK)
    dr.text((20, 50), "26 · X · 1977", font=font(MONO_B, 14), fill=RED)
    body = ("Ali Maow Maalin, 23, a hospital cook\n"
            "in southern Somalia, falls ill. His is\n"
            "the last naturally caught case of\n"
            "smallpox on Earth. He recovers, and\n"
            "later spends years vaccinating\n"
            "children against polio.")
    dr.multiline_text((20, 74), body, font=font(SERIF_I, 12), fill=BLACK, spacing=2)
    f9 = font(MONO, 9)
    tx, ty = P(L + fl, 0)
    tx, ty = tx / S, ty / S
    dr.line([tx + 4, ty - 6, tx + 20, ty - 30], fill=BLACK)
    dr.text((388, ty - 47), "one dose, held", font=f9, fill=BLACK, anchor="rt")
    dr.text((388, ty - 36), "between the tines", font=f9, fill=BLACK, anchor="rt")
    dr.text((388, 289), "eradication certified 1979–80", font=f9, fill=BLACK, anchor="rs")
    return img


# ------------------------------------------------------------ 5. tide machine
# Illustrative harmonic constituents (period h, amplitude m), phased so that
# M2 and S2 line up ~1.5 days after the full moon — the "age of the tide".
CONSTITUENTS = [("M2", 12.4206, 2.6), ("S2", 12.0, 0.95), ("N2", 12.6583, 0.5),
                ("K1", 23.9345, 0.22), ("O1", 25.8193, 0.18)]


def image5_tide():
    """Kelvin's tide-predicting machine (1872) in diagram: each pulley turns
    at one constituent's speed, a single wire passes over them all (and under
    fixed guides between), and its free end — the pen — draws their sum.
    Below, the trace for this week, springs arriving just after the full moon."""
    img, dr = canvas1()
    f9 = font(MONO, 9)
    t_full = 4.2                      # 04:12 Mon 26 Oct, hours from Mon 00:00
    t_align = t_full + 36             # springs ~1.5 days later
    t0, t1 = -48, 6 * 24              # Sat 24 → Sun 1 Nov

    def tide(t):
        z = 0.0
        for i, (_, per, amp) in enumerate(CONSTITUENTS):
            ph = 0.0 if i < 2 else (1.3 * i)
            z += amp * math.cos(2 * math.pi * (t - t_align) / per + ph)
        return z

    t_now = t_full + 10
    py, gy_ = 64, 102                  # pulley row, guide row
    xs = [56, 118, 180, 242, 304]
    wire = [(20, gy_ + 4)]
    for j, ((name, per, amp), x) in enumerate(zip(CONSTITUENTS, xs)):
        r = 9 + amp * 6
        ang = 2 * math.pi * (t_now - t_align) / per
        dr.ellipse([x - r, py - r, x + r, py + r], outline=BLACK, width=2)
        for k in range(8):            # spokes
            a = ang + k * math.pi / 4
            dr.line([x, py, x + (r - 2) * math.cos(a), py + (r - 2) * math.sin(a)], fill=BLACK)
        cx, cy = x + r * 0.55 * math.cos(ang), py + r * 0.55 * math.sin(ang)
        dr.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
        dr.text((x, py - r - 7), name, font=font(MONO_B, 9), fill=BLACK, anchor="mm")
        wire += [(x - r, py), (x - r * 0.7, py - r * 0.7), (x, py - r), (x + r * 0.7, py - r * 0.7), (x + r, py)]
        gx = x + 31                   # fixed guide pulley between
        dr.ellipse([gx - 4, gy_ - 4, gx + 4, gy_ + 4], fill=BLACK)
        wire += [(gx - 4, gy_), (gx, gy_ + 4), (gx + 4, gy_)]
    pen_x = xs[-1] + 31 + 4
    wire += [(pen_x, 121)]
    dr.rectangle([16, gy_ + 1, 22, gy_ + 9], fill=BLACK)        # wire anchor
    dr.line(wire, fill=BLACK)
    dr.polygon([(pen_x - 3, 120), (pen_x + 3, 120), (pen_x, 127)], fill=RED)

    # paper strip with the trace
    gx0, gx1, gy = 20, 380, 194
    amp_px = 11
    dr.rectangle([gx0 - 4, 130, gx1 + 4, 262], outline=BLACK)
    for d in range(0, 9):
        t = t0 + d * 24
        x = gx0 + (gx1 - gx0) * (t - t0) / (t1 - t0)
        for y in range(134, 259, 3):
            dr.point((x, y), fill=BLACK)
        if d < 8:
            lbl = ["Sat", "Sun", "MON", "Tue", "Wed", "Thu", "Fri", "Sat"][d]
            dr.text((x + (gx1 - gx0) / 16, 257), lbl, font=f9,
                    fill=RED if lbl == "MON" else BLACK, anchor="ms")
    dr.line([gx0, gy, gx1, gy], fill=BLACK)
    pts = []
    for i in range(0, 1500):
        t = t0 + (t1 - t0) * i / 1499
        x = gx0 + (gx1 - gx0) * i / 1499
        pts.append((x, gy - tide(t) * amp_px))
    dr.line(pts, fill=RED, width=1)
    # full-moon and springs markers in the top margin of the strip
    xm = gx0 + (gx1 - gx0) * (t_full - t0) / (t1 - t0)
    dr.ellipse([xm - 4, 133, xm + 4, 141], fill=WHITE, outline=BLACK)
    dr.text((xm - 7, 137), "full moon", font=f9, fill=BLACK, anchor="rm")
    xs_ = gx0 + (gx1 - gx0) * (t_align - t0) / (t1 - t0)
    dr.line([xs_, 137, xs_ + 14, 137], fill=BLACK)
    dr.polygon([(xs_, 134), (xs_, 140), (xs_ - 4, 137)], fill=BLACK)
    dr.text((xs_ + 17, 137), "springs", font=font(SERIF_I, 12), fill=BLACK, anchor="lm")

    dr.text((20, 4), "SUM OF FIVE SINES", font=font(MONO_XB, 16), fill=BLACK)
    dr.text((380, 8), "after Kelvin, 1872", font=font(SERIF_I, 12), fill=BLACK, anchor="ra")
    dr.text((20, 270), "each pulley turns at one tidal constituent's speed; one wire", font=f9, fill=BLACK)
    dr.text((20, 282), "over them all sums them, and its end is the pen.", font=f9, fill=BLACK)
    dr.text((376, 137), "amplitudes illustrative", font=font(MONO, 8), fill=BLACK, anchor="rm")
    return img


def main():
    makers = [image1_seven_sisters, image2_erie, image3_law_one, image4_merca, image5_tide]
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
    for i, fn in enumerate(makers, 1):
        im = finalize(fn(), dither=False)
        for d in OUT_DIRS:
            im.save(os.path.join(d, f"{i}.png"), optimize=True)
        print("wrote", i, fn.__name__)


if __name__ == "__main__":
    main()
