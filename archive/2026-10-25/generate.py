#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-25 (Sunday).

Five 400x300 images in exactly three colors (white, black, red).
Hooks for the day: British Summer Time ends (a 25-hour day), Chaucer
(d. 25 Oct 1400) and his Treatise on the Astrolabe, Agincourt on St
Crispin's Day 1415, Gjon Mili's 1949 light drawings with Picasso
(b. 25 Oct 1881), and Johann Strauss II (b. 25 Oct 1825).

Run from the repo root:  python3 archive/2026-10-25/generate.py
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F = "/usr/share/fonts/truetype/"
MONO = F + "jetbrains-mono/JetBrainsMono-Regular.ttf"
MONO_B = F + "jetbrains-mono/JetBrainsMono-ExtraBold.ttf"
SERIF = F + "freefont/FreeSerif.ttf"
SERIF_I = F + "liberation/LiberationSerif-Italic.ttf"  # hints cleanly at 12-13 px
SERIF_BI = F + "freefont/FreeSerifBoldItalic.ttf"

OUT_DIRS = ["images", "archive/2026-10-25"]


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


# ------------------------------------------------------------ 1. the spare hour
def image1_spare_hour():
    """The clock's hour hand traced as a spiral over the 25 hours of today.
    Radius grows with elapsed time; angle follows the clock face. At 02:00
    BST the hand snaps back to 01:00, so one sector of the face is lived twice."""
    img, dr = canvas1()
    cx, cy = 132, 152
    r0, k, jump = 58.0, 2.4, 14.0

    def pt(t):
        shown = t if t < 2 else t - 1          # what the clock face says
        a = shown / 12 * 2 * math.pi - math.pi / 2
        r = r0 + k * t + (jump if t >= 2 else 0)  # the repeat pushes the path outward
        return cx + r * math.cos(a), cy + r * math.sin(a)

    # faint face: 12 radial spokes
    for h in range(12):
        a = h / 12 * 2 * math.pi - math.pi / 2
        for rr in range(int(r0) - 8, int(r0 + k * 25 + jump) + 10, 4):
            dr.point((cx + rr * math.cos(a), cy + rr * math.sin(a)), fill=BLACK)
    dr.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=BLACK)

    def seg(t0, t1, col, w):
        n = int((t1 - t0) * 40) + 2
        pts = [pt(t0 + (t1 - t0) * i / (n - 1)) for i in range(n)]
        dr.line(pts, fill=col, width=w, joint="curve")

    seg(0, 1, BLACK, 3)
    seg(1, 1.999, RED, 5)
    seg(2, 3, RED, 5)
    seg(3, 25, BLACK, 3)
    # the snap back: dashed
    a, b = pt(1.999), pt(2)
    for i in range(0, 10, 2):
        p0 = (a[0] + (b[0] - a[0]) * i / 10, a[1] + (b[1] - a[1]) * i / 10)
        p1 = (a[0] + (b[0] - a[0]) * (i + 1) / 10, a[1] + (b[1] - a[1]) * (i + 1) / 10)
        dr.line([p0, p1], fill=RED, width=2)

    f7 = font(MONO, 9)
    for t in range(26):
        x, y = pt(t)
        col = RED if t in (1, 2, 3) else BLACK
        dr.ellipse((x - 2, y - 2, x + 2, y + 2), fill=WHITE, outline=col)
        if t in (0, 1, 2, 3, 6, 9, 12, 15, 18, 21, 25):
            shown = t if t < 2 else t - 1
            if t == 2:
                lab = "01"
            else:
                lab = "%02d" % (shown % 24) if t < 25 else "24"
            a = (shown / 12) * 2 * math.pi - math.pi / 2
            rr = math.hypot(x - cx, y - cy) + (-11 if t == 1 else 10)
            dr.text((cx + rr * math.cos(a), cy + rr * math.sin(a)), lab, font=f7,
                    fill=col, anchor="mm")

    # right column
    x0 = 268
    dr.text((x0, 26), "01:00", font=font(MONO_B, 30), fill=RED)
    dr.text((x0, 58), "01:00", font=font(MONO_B, 30), fill=BLACK)
    dr.line((x0, 100, 392, 100), fill=BLACK)
    fm = font(MONO, 9)
    lines = ["SUN 25 OCT 2026", "", "at 02:00 BST the", "clocks go back to", "01:00 GMT.",
             "", "British Summer Time", "ends; today has", "25 hours.", "",
             "the hand's path,", "midnight to midnight:", "radius = time lived,", "angle = time shown.",
             "", "red: the hour you", "get to spend twice."]
    for i, s in enumerate(lines):
        dr.text((x0, 108 + i * 10), s, font=fm, fill=RED if i >= 15 else BLACK)
    return finalize(img, dither=False)


# ------------------------------------------------------------ 2. astrolabe
STARS = [  # name, RA hours, Dec deg (J2000)
    ("Aldebaran", 4.598, 16.51), ("Rigel", 5.242, -8.20), ("Betelgeuse", 5.919, 7.41),
    ("Capella", 5.278, 46.00), ("Sirius", 6.752, -16.72), ("Procyon", 7.655, 5.22),
    ("Pollux", 7.755, 28.03), ("Regulus", 10.139, 11.97), ("Dubhe", 11.062, 61.75),
    ("Spica", 13.420, -11.16), ("Alkaid", 13.792, 49.31), ("Arcturus", 14.261, 19.18),
    ("Vega", 18.616, 38.78), ("Altair", 19.846, 8.87), ("Deneb", 20.690, 45.28),
    ("Alpheratz", 0.140, 29.09), ("Algol", 3.136, 40.96), ("Markab", 23.079, 15.21),
]


def gmst_hours(y, m, d, ut):
    a = (14 - m) // 12
    yy, mm = y + 4800 - a, m + 12 * a - 3
    jdn = d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045
    jd = jdn - 0.5 + ut / 24
    return (18.697374558 + 24.06570982441908 * (jd - 2451545.0)) % 24


def image2_astrolabe():
    """Chaucer's astrolabe 'for the latitude of Oxenforde', its rete set for
    21:00 GMT tonight. Stereographic projection from the south pole."""
    img, dr = canvas1()
    cx, cy, R = 140, 158, 126          # R = tropic of Capricorn
    eps = math.radians(23.44)
    phi = math.radians(51 + 50 / 60)
    Req = R / math.tan(math.radians(90 + 23.44) / 2)
    lst = (gmst_hours(2026, 10, 25, 21.0) - 1.25 / 15) % 24

    def proj(dec, ha):  # dec, hour angle in radians; meridian up, east left
        r = Req * math.tan((math.pi / 2 - dec) / 2)
        return cx + r * math.sin(ha), cy - r * math.cos(ha)

    def inside(p, rr=R):
        return (p[0] - cx) ** 2 + (p[1] - cy) ** 2 <= rr * rr

    def polyline(pts, col, w=1):
        run = []
        for p in pts:
            if inside(p):
                run.append(p)
            else:
                if len(run) > 1:
                    dr.line(run, fill=col, width=w)
                run = []
        if len(run) > 1:
            dr.line(run, fill=col, width=w)

    # mater rim with degree scale
    dr.ellipse((cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10), outline=BLACK, width=2)
    dr.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLACK, width=1)
    for i in range(360):
        if i % 5:
            continue
        a = math.radians(i)
        l = 9 if i % 15 == 0 else 4
        dr.line((cx + (R + 10 - l) * math.sin(a), cy - (R + 10 - l) * math.cos(a),
                 cx + (R + 10) * math.sin(a), cy - (R + 10) * math.cos(a)), fill=BLACK)
    # plate: equator, tropic of Cancer
    for dec in (0, 23.44):
        r = Req * math.tan(math.radians(90 - dec) / 2)
        dr.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK)
    # almucantars every 10 degrees + horizon
    def alt_circle(h_deg, n=360):
        h = math.radians(h_deg)
        out = []
        for i in range(n + 1):
            A = 2 * math.pi * i / n
            dec = math.asin(math.sin(phi) * math.sin(h) + math.cos(phi) * math.cos(h) * math.cos(A))
            ha = math.atan2(-math.sin(A) * math.cos(h),
                            math.cos(phi) * math.sin(h) - math.sin(phi) * math.cos(h) * math.cos(A))
            out.append(proj(dec, ha))
        return out
    for hd in range(10, 90, 10):
        polyline(alt_circle(hd), BLACK)
    polyline(alt_circle(0), BLACK, 2)
    # zenith mark
    zx, zy = proj(phi, 0)
    dr.line((zx - 3, zy, zx + 3, zy), fill=BLACK)
    dr.line((zx, zy - 3, zx, zy + 3), fill=BLACK)
    # azimuth lines (every 30 deg) between horizon and zenith
    for Ad in range(0, 360, 30):
        A = math.radians(Ad)
        pts = []
        for j in range(0, 86):
            h = math.radians(j)
            dec = math.asin(math.sin(phi) * math.sin(h) + math.cos(phi) * math.cos(h) * math.cos(A))
            ha = math.atan2(-math.sin(A) * math.cos(h),
                            math.cos(phi) * math.sin(h) - math.sin(phi) * math.cos(h) * math.cos(A))
            pts.append(proj(dec, ha))
        for i, p in enumerate(pts):
            if i % 3 == 0 and inside(p):
                dr.point(p, fill=BLACK)
    # meridian line
    dr.line((cx, cy - R, cx, cy + R), fill=BLACK)

    # rete: ecliptic ring
    def ecl(lam):
        ra = math.atan2(math.sin(lam) * math.cos(eps), math.cos(lam))
        dec = math.asin(math.sin(eps) * math.sin(lam))
        return dec, math.radians(lst * 15) - ra
    ring = [proj(*ecl(math.radians(i))) for i in range(361)]
    dr.line(ring, fill=RED, width=5)
    dr.line(ring, fill=WHITE, width=1)
    # zodiac sign boundaries on the ring
    for s in range(12):
        d, ha = ecl(math.radians(30 * s))
        r = Req * math.tan((math.pi / 2 - d) / 2)
        ux, uy = math.sin(ha), -math.cos(ha)
        p = proj(d, ha)
        dr.line((p[0] - 3 * ux, p[1] - 3 * uy, p[0] + 3 * ux, p[1] + 3 * uy), fill=BLACK, width=1)
    # star pointers: small red flames from a tracery line to the ecliptic ring centre
    f6 = font(MONO, 9)
    for name, ra, dec in STARS:
        d = math.radians(dec)
        ha = math.radians((lst - ra) * 15)
        p = proj(d, ha)
        if not inside(p, R - 2):
            continue
        # tracery back toward the centre
        q = proj(d + math.radians(9), ha)
        dr.line((p, q), fill=RED, width=2)
        ang = math.atan2(p[1] - q[1], p[0] - q[0])
        tip = p
        bx, by = p[0] - 6 * math.cos(ang), p[1] - 6 * math.sin(ang)
        side = [(bx + 3 * math.cos(ang + math.pi / 2), by + 3 * math.sin(ang + math.pi / 2)),
                (bx + 3 * math.cos(ang - math.pi / 2), by + 3 * math.sin(ang - math.pi / 2))]
        dr.polygon([tip, side[0], side[1]], fill=RED)
        if name in ("Vega", "Capella", "Aldebaran", "Arcturus", "Deneb", "Altair", "Sirius", "Regulus"):
            lx = tip[0] + 3 if tip[0] >= cx else tip[0] - 3
            dr.text((lx, tip[1]), name, font=f6, fill=BLACK,
                    anchor="lm" if tip[0] >= cx else "rm")
    # rule (alidade/label) and pin
    dr.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=BLACK)
    dr.ellipse((cx - 1, cy - 1, cx + 1, cy + 1), fill=WHITE)
    # throne
    dr.rectangle((cx - 9, cy - R - 20, cx + 9, cy - R - 11), fill=BLACK)
    dr.ellipse((cx - 3, cy - R - 19, cx + 3, cy - R - 13), fill=WHITE)

    # right column
    x0 = 304
    dr.text((x0, 12), "Astrelabie", font=font(SERIF_BI, 18), fill=BLACK)
    dr.line((x0, 36, 396, 36), fill=RED, width=2)
    fq = font(SERIF_I, 13)
    quote = ["“Litel Lowys my", "sone, I aperceyve", "wel by certeyne", "evidences thyn",
             "abilite to lerne", "sciences touching", "nombres and", "proporciouns…”"]
    for i, s in enumerate(quote):
        dr.text((x0, 42 + i * 13), s, font=fq, fill=BLACK)
    fm = font(MONO, 9)
    info = ["Geoffrey Chaucer", "d. 25 Oct 1400", "", "plate for", "Oxenforde,", "51°50′ N",
            "", "rete set for", "21:00 GMT", "tonight", "", "red: ecliptic", "& star points"]
    for i, s in enumerate(info):
        dr.text((x0, 156 + i * 10), s, font=fm, fill=RED if i >= 11 else BLACK)
    return finalize(img, dither=False)


# ------------------------------------------------------------ 3. Crispin Crispian
def image3_crispin():
    """Agincourt in side elevation: arrow flights as a tonal cloud."""
    rng = np.random.default_rng(14151025)
    w, h = W * SS, H * SS
    ground = 252 * SS
    n_arcs = 520
    arcs = []
    for i in range(n_arcs):
        x0 = rng.uniform(12, 80) * SS
        x1 = rng.uniform(270, 398) * SS
        apex = np.clip(rng.normal(140, 34), 60, 195) * SS
        arcs.append((x0, x1, apex))
    acc = np.zeros((h, w), np.float32)
    for b in range(0, n_arcs, 35):
        layer = Image.new("L", (w, h), 0)
        ld = ImageDraw.Draw(layer)
        for x0, x1, apex in arcs[b:b + 35]:
            pts = [(x0 + (x1 - x0) * s, ground - 4 * apex * s * (1 - s) * (1 - 0.15 * s))
                   for s in np.linspace(0, 1, 90)]
            ld.line(pts, fill=1, width=2)
        acc += np.asarray(layer, np.float32)
    ink = 1 - np.exp(-acc * 0.16)
    grey = 255 * (1 - ink)
    # mud: furrowed band
    yy, xx = np.mgrid[0:h, 0:w]
    noise = rng.random((h // 6 + 1, w // 6 + 1)).astype(np.float32)
    noise = np.asarray(Image.fromarray((noise * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
                       np.float32) / 255
    furrow = 0.5 + 0.5 * np.sin((yy - ground) * 0.9 / SS * (1 + (yy - ground) / (40 * SS)))
    mud = 40 + 50 * furrow * noise
    grey = np.where(yy >= ground, mud, grey)
    rgb = np.stack([grey] * 3, -1).astype(np.uint8)
    img = Image.fromarray(rgb)
    dr = ImageDraw.Draw(img)
    # one red flight
    x0, x1, apex = 46 * SS, 342 * SS, 168 * SS
    pts = [(x0 + (x1 - x0) * s, ground - 4 * apex * s * (1 - s) * (1 - 0.15 * s))
           for s in np.linspace(0, 1, 200)]
    dr.line(pts, fill=RED, width=2 * SS)
    img = img.resize((W, H), Image.LANCZOS)
    img = finalize(img, dither=True).convert("RGB")
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    # archers (left) and lances (right), drawn crisp at 1x
    for x in range(14, 82, 4):
        dr.line((x, 252, x, 244), fill=BLACK)
        dr.arc((x - 3, 241, x + 3, 251), 270, 90, fill=BLACK)
    for x in range(292, 398, 5):
        dr.line((x, 252, x + 1, 232), fill=BLACK)
    dr.rectangle((0, 0, 210, 52), fill=WHITE)
    dr.text((10, 6), "Crispin Crispian", font=font(SERIF_BI, 26), fill=BLACK)
    dr.text((11, 38), "AGINCOURT · 25 OCT 1415 · 611 YEARS AGO",
            font=font(MONO, 9), fill=RED)
    dr.rectangle((0, 268, 400, 300), fill=BLACK)
    dr.text((10, 272), "“we few, we happy few, we band of brothers”",
            font=font(SERIF_I, 13), fill=WHITE)
    dr.text((10, 287), "a ploughed field between two woods, after a night of rain",
            font=font(MONO, 9), fill=WHITE)
    return img.quantize(palette=PAL, dither=Image.Dither.NONE)


# ------------------------------------------------------------ 4. light drawing
def image4_light():
    """One gesture in the dark, photographed by two cameras at once
    (front and side), as Gjon Mili did with Picasso at Vallauris, 1949."""
    rng = np.random.default_rng(18811025)
    t = np.linspace(0, 1, 2400)
    def comp(scale):
        v = np.zeros_like(t)
        for k in range(1, 6):
            v += rng.normal(0, 1) / k ** 1.1 * np.sin(2 * math.pi * k * t * 1.6 + rng.uniform(0, 6.3))
        return v * scale
    X, Y, Z = comp(1.0), comp(0.8), comp(1.0)
    # a little flourish: a loop in the middle
    loop = np.exp(-((t - 0.55) / 0.05) ** 2)
    X += 0.5 * loop * np.cos(2 * math.pi * t * 20)
    Y += 0.5 * loop * np.sin(2 * math.pi * t * 20)
    w, h = W * SS, H * SS

    def panel(u, v, box):
        x0, y0, x1, y1 = box
        u = (u - u.min()) / (np.ptp(u) + 1e-9)
        v = (v - v.min()) / (np.ptp(v) + 1e-9)
        m = 14 * SS
        px = x0 + m + u * (x1 - x0 - 2 * m)
        py = y0 + m + v * (y1 - y0 - 2 * m)
        return list(zip(px, py))

    core = Image.new("L", (w, h), 0)
    cd = ImageDraw.Draw(core)
    boxes = [(0, 0, 200 * SS, 262 * SS), (200 * SS, 0, 400 * SS, 262 * SS)]
    p_front = panel(X, Y, boxes[0])
    p_side = panel(Z, Y, boxes[1])
    for pts in (p_front, p_side):
        cd.line(pts, fill=255, width=2 * SS, joint="curve")
    c = np.asarray(core, np.float32) / 255
    halo = np.asarray(core.filter(ImageFilter.GaussianBlur(5 * SS)), np.float32) / 255
    halo = np.clip(halo * 2.2, 0, 1)
    r = np.clip(halo * 255 + c * 255, 0, 255)
    g = c * 255
    rgb = np.stack([r, g, g], -1).astype(np.uint8)
    img = Image.fromarray(rgb).resize((W, H), Image.LANCZOS)
    img = finalize(img, dither=True).convert("RGB")
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    # the flashlight's last position
    ex, ey = p_front[-1][0] / SS, p_front[-1][1] / SS
    dr.ellipse((ex - 3, ey - 3, ex + 3, ey + 3), fill=WHITE)
    dr.line((200, 8, 200, 255), fill=RED)
    fm = font(MONO, 9)
    dr.text((8, 6), "CAMERA A · FRONT", font=fm, fill=WHITE)
    dr.text((208, 6), "CAMERA B · SIDE", font=fm, fill=WHITE)
    dr.rectangle((0, 262, 400, 300), fill=WHITE)
    dr.text((8, 265), "Drawing with light", font=font(SERIF_BI, 15), fill=BLACK)
    dr.text((8, 284), "two shutters left open on one gesture · after Gjon Mili & Picasso, 1949",
            font=fm, fill=BLACK)
    dr.text((392, 270), "b. 25.X.1881", font=fm, fill=RED, anchor="ra")
    return img.quantize(palette=PAL, dither=Image.Dither.NONE)


# ------------------------------------------------------------ 5. organette strip
ROWS = ["A2", "D3", "E3", "F#3", "G3", "A3", "C#4", "D4", "E4", "F#4", "G4", "A4", "B4",
        "C#5", "D5", "E5", "F#5", "G5", "A5", "B5", "C#6", "D6"]


def blue_danube():
    """Opening theme of the first waltz, simplified: (row, start beat, beats, echo?)."""
    phrases = [
        (["D4", "F#4", "A4"], "A4", "A5", "F#5", "D"),
        (["D4", "F#4", "A4"], "A4", "A5", "G5", "D"),
        (["C#4", "E4", "B4"], "B4", "B5", "G5", "A"),
        (["C#4", "E4", "B4"], "B4", "B5", "F#5", "A"),
        (["D4", "F#4", "A4"], "D5", "D6", "A5", "D"),
        (["D4", "F#4", "A4"], "D5", "D6", "B5", "D"),
    ]
    notes, beat = [], 0
    for up, held, e1, e2, chord in phrases:
        for i, n in enumerate(up):
            notes.append((n, beat + i, 1, False))
        notes.append((held, beat + 3, 3, False))
        notes += [(e1, beat + 7, 1, True), (e1, beat + 8, 1, True),
                  (e2, beat + 10, 1, True), (e2, beat + 11, 1, True)]
        root, upper = (("D3", ["F#3", "A3"]) if chord == "D" else ("A2", ["E3", "G3"]))
        for bar in range(4):
            b0 = beat + 3 * bar
            notes.append((root, b0, 1, False))
            for u in upper:
                notes += [(u, b0 + 1, 1, False), (u, b0 + 2, 1, False)]
        beat += 12
    return notes, beat


def image5_organette():
    img, dr = canvas1()
    notes, total = blue_danube()
    x0, x1 = 30, 394
    y_top, row_h = 66, 8.4
    y_bot = int(y_top + row_h * len(ROWS))
    bw = (x1 - x0) / total
    # paper strip with sprocket edges
    dr.rectangle((x0 - 4, y_top - 12, x1 + 6, y_bot + 12), outline=BLACK)
    for x in range(x0, x1, 8):
        dr.rectangle((x, y_top - 9, x + 3, y_top - 6), fill=BLACK)
        dr.rectangle((x, y_bot + 6, x + 3, y_bot + 9), fill=BLACK)
    # row guides (dotted), bar lines
    for i in range(len(ROWS)):
        y = y_bot - (i + 0.5) * row_h
        for x in range(x0, x1, 3):
            dr.point((x, y), fill=BLACK)
    fm = font(MONO, 9)
    for b in range(0, total + 1, 3):
        x = x0 + b * bw
        col = BLACK
        for y in range(y_top - 4, y_bot + 4, 2 if b % 12 else 1):
            dr.point((x, y), fill=col)
    # holes
    for name, b, dur, echo in notes:
        i = ROWS.index(name)
        yc = y_bot - (i + 0.5) * row_h
        xa = x0 + b * bw + 1
        xb = x0 + (b + dur) * bw - 1
        dr.rounded_rectangle((xa, yc - 2.5, xb, yc + 2.5), radius=2, fill=RED if echo else BLACK)
    # note names at left
    for i, n in enumerate(ROWS):
        if n in ("A2", "D3", "D4", "A4", "D5", "A5", "D6"):
            dr.text((x0 - 6, y_bot - (i + 0.5) * row_h), n, font=fm, fill=BLACK, anchor="rm")
    # title
    dr.text((10, 8), "An der schönen blauen Donau", font=font(SERIF_BI, 24), fill=BLACK)
    dr.text((11, 38), "JOHANN STRAUSS II · b. VIENNA 25 OCT 1825 · OP. 314",
            font=fm, fill=BLACK)
    dr.text((10, y_bot + 20), "a punched strip for an organette: 24 bars in 3/4, read left to right.",
            font=fm, fill=BLACK)
    dr.text((10, y_bot + 32), "red holes: the echo — ta-ta, ta-ta — after every rising phrase.",
            font=fm, fill=RED)
    return img.quantize(palette=PAL, dither=Image.Dither.NONE)


def main():
    makers = [image1_spare_hour, image2_astrolabe, image3_crispin, image4_light, image5_organette]
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
    for i, mk in enumerate(makers, 1):
        im = mk()
        assert im.size == (W, H)
        for d in OUT_DIRS:
            im.save(os.path.join(d, "%d.png" % i), optimize=True)
        print("wrote", i, mk.__name__)


if __name__ == "__main__":
    main()
