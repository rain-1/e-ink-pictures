#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-14 (Monday).

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

Today's threads:
  1. KLIN        — a constructivist wedge, the Lissitzky idea I saved on day one.
  2. CHIRP       — GW150914, first gravitational-wave detection, 14 Sep 2015.
  3. ELEVEN DAYS — Britain's September 1752: Wed 2nd was followed by Thu 14th.
  4. TONIGHT     — 5 % crescent Moon 5½° left of Venus, low WSW after sunset.
  5. ASANOHA     — kumiko hemp-leaf lattice with a red moon behind the shoji.

Tonal pieces render at 3x, LANCZOS downscale, Floyd–Steinberg into the palette.
Hard-edged pieces render at 3x and downscale WITHOUT dither (nearest color),
which keeps lines crisp and avoids speckle on the panel.
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

FD = "/usr/share/fonts/truetype/"
FONT_SANS = FD + "dejavu/DejaVuSans.ttf"
FONT_SANS_B = FD + "dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = FD + "dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = FD + "dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = FD + "dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = FD + "dejavu/DejaVuSansMono-Bold.ttf"
FONT_LIB_SERIF = FD + "liberation/LiberationSerif-Regular.ttf"
FONT_LIB_SERIF_B = FD + "liberation/LiberationSerif-Bold.ttf"
FONT_LIB_SANS_B = FD + "liberation/LiberationSans-Bold.ttf"
FONT_JP = FD + "fonts-japanese-gothic.ttf"

OUT_DIRS = ["images", "archive/2026-09-14"]


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


def save(img, n):
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        img.save(os.path.join(d, f"{n}.png"), optimize=True)


def text_w(dr, s, f):
    l, t, r, b = dr.textbbox((0, 0), s, font=f)
    return r - l


# ------------------------------------------------------------------ 1. KLIN
def image1_klin():
    """A wedge. Not Lissitzky's — mine — but speaking his grammar:
    a white field, a black field, a disc that the red wedge enters."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # Black field: everything right of a steep diagonal.
    dr.polygon([(W * s * 0.62, 0), (W * s, 0), (W * s, H * s), (W * s * 0.40, H * s)], fill=BLACK)

    # The disc sits astride the boundary: white on black side, black on white side.
    cx, cy, r = W * s * 0.60, H * s * 0.47, 78 * s
    disc = Image.new("L", (W * s, H * s), 0)
    ImageDraw.Draw(disc).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    inverted = Image.new("RGB", (W * s, H * s), WHITE)
    ImageDraw.Draw(inverted).polygon([(W * s * 0.62, 0), (W * s, 0), (W * s, H * s), (W * s * 0.40, H * s)], fill=BLACK)
    inverted = Image.eval(inverted, lambda v: 255 - v)
    img.paste(inverted, (0, 0), disc)
    dr = ImageDraw.Draw(img)

    # The red wedge: from the lower-left corner, its point buried in the disc.
    tip = (cx + 6 * s, cy + 2 * s)
    base_c = (-30 * s, H * s + 40 * s)
    ang = math.atan2(tip[1] - base_c[1], tip[0] - base_c[0])
    half = 52 * s
    nx, ny = -math.sin(ang) * half, math.cos(ang) * half
    dr.polygon([tip, (base_c[0] + nx, base_c[1] + ny), (base_c[0] - nx, base_c[1] - ny)], fill=RED)

    # Small skirmishes: bars and a square, scattered on the diagonal axis.
    dr.rectangle([300 * s, 40 * s, 380 * s, 47 * s], fill=WHITE)
    dr.rectangle([318 * s, 58 * s, 380 * s, 61 * s], fill=WHITE)
    dr.rectangle([40 * s, 42 * s, 47 * s, 118 * s], fill=BLACK)
    dr.rectangle([22 * s, 66 * s, 30 * s, 92 * s], fill=RED)
    dr.rectangle([352 * s, 226 * s, 372 * s, 246 * s], fill=RED)
    dr.rectangle([332 * s, 254 * s, 388 * s, 257 * s], fill=WHITE)
    dr.rectangle([300 * s, 176 * s, 306 * s, 214 * s], fill=WHITE)

    # A ring: thin black circle on the white field, overlapping nothing.
    rr = 22 * s
    dr.ellipse([88 * s - rr, 40 * s - rr, 88 * s + rr, 40 * s + rr], outline=BLACK, width=2 * s)

    # Diagonal type running parallel to the wedge, just above its upper edge.
    # Drawn on a full-size transparent layer, then rotated about the anchor
    # point so the text's bottom-left corner stays put.
    f1 = font(FONT_SANS_B, 24 * s)
    f2 = font(FONT_SANS_B, 9 * s)
    ax, ay = 22 * s, 226 * s
    label = Image.new("RGBA", (W * s, H * s), (0, 0, 0, 0))
    ld = ImageDraw.Draw(label)
    ld.text((ax, ay), "КЛИНОМ", font=f1, fill=BLACK, anchor="ls")
    ld.text((ax, ay - 27 * s), "with a wedge · monday 14 · ix · 2026", font=f2, fill=BLACK, anchor="ld")
    label = label.rotate(-math.degrees(ang), resample=Image.BICUBIC, expand=False, center=(ax, ay))
    img.paste(label, (0, 0), label)

    return finalize(img, dither=False)


# ----------------------------------------------------------------- 2. CHIRP
def chirp(tc=0.0, t0=-0.20, mc=30.0, dt=1 / 4096):
    """Newtonian inspiral chirp for chirp mass mc (solar masses), then a
    damped ringdown. Returns (times, strain) in arbitrary units."""
    G, c, Msun = 6.674e-11, 2.998e8, 1.989e30
    k = (G * mc * Msun / c ** 3)  # seconds
    ts, hs = [], []
    phi = 0.0
    t = t0
    f_last = 35.0
    while t < tc - 0.004:
        tau = tc - t
        f = (1 / (8 * math.pi)) * (5 / (256 * tau)) ** (3 / 8) * k ** (-5 / 8)
        f = min(f, 260)
        amp = (f / 35) ** (2 / 3)
        phi += 2 * math.pi * f * dt
        ts.append(t)
        hs.append(amp * math.cos(phi))
        f_last = f
        t += dt
    # merger peak + ringdown: decaying oscillation at ~250 Hz
    peak_amp = (f_last / 35) ** (2 / 3) * 1.15
    t_end = t + 0.025
    while t < t_end:
        d = (t - (tc - 0.004))
        amp = peak_amp * math.exp(-d / 0.0045)
        phi += 2 * math.pi * 250 * dt
        ts.append(t)
        hs.append(amp * math.cos(phi))
        t += dt
    return ts, hs


def image2_chirp():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # Header
    fh = font(FONT_MONO_B, 18 * s)
    dr.text((14 * s, 10 * s), "GW150914", font=fh, fill=BLACK)
    fs = font(FONT_SANS_B, 9.5 * s)
    dr.text((116 * s, 15 * s), "09:50:45 UTC · 14 Sep 2015 · eleven years ago today", font=fs, fill=BLACK)
    dr.text((14 * s, 32 * s),
            "two black holes, 36 and 29 suns, 1.3 billion light-years off, became one",
            font=fs, fill=BLACK)

    # Plot area
    px0, px1 = 14 * s, 386 * s
    py0, py1 = 52 * s, 232 * s
    ts, hs = chirp()
    hmax = max(abs(v) for v in hs)
    t_min, t_max = -0.20, 0.07

    def X(t):
        return px0 + (t - t_min) / (t_max - t_min) * (px1 - px0)

    # faint grid in x every 50 ms
    for ms in range(-200, 31, 50):
        x = X(ms / 1000)
        for y in range(int(py0), int(py1), 4 * s):
            dr.point((x, y), fill=BLACK)
    # zero-line for each trace
    yH, yL = (py0 + py1) / 2 - 42 * s, (py0 + py1) / 2 + 42 * s
    scale = 40 * s / hmax

    def trace(y0, sign, shift, color, width):
        pts = [(X(t + shift), y0 - sign * h * scale) for t, h in zip(ts, hs)]
        pts = [(x, y) for x, y in pts if px0 <= x <= px1]
        dr.line(pts, fill=color, width=width, joint="curve")

    # Livingston (red, inverted, 7 ms earlier) and Hanford (black)
    trace(yL, -1, -0.007, RED, int(2.2 * s))
    trace(yH, 1, 0.0, BLACK, int(2.2 * s))

    fl = font(FONT_MONO_B, 9 * s)
    dr.text((px0 + 2 * s, yH - 52 * s), "H1  Hanford", font=fl, fill=BLACK)
    dr.text((px0 + 2 * s, yL - 52 * s), "L1  Livingston  (inverted, +7 ms)", font=fl, fill=RED)
    # strain scale bar, in the quiet after the ringdown
    sx = px1 - 6 * s
    dr.line([(sx, yH - 20 * s), (sx, yH + 20 * s)], fill=BLACK, width=int(1.5 * s))
    dr.line([(sx - 4 * s, yH - 20 * s), (sx + 4 * s, yH - 20 * s)], fill=BLACK, width=int(1.5 * s))
    dr.line([(sx - 4 * s, yH + 20 * s), (sx + 4 * s, yH + 20 * s)], fill=BLACK, width=int(1.5 * s))
    dr.text((sx - 46 * s, yH + 24 * s), "1e-21", font=fl, fill=BLACK)
    dr.text((sx - 46 * s, yH + 35 * s), "strain", font=fl, fill=BLACK)

    # time axis
    dr.line([(px0, py1 + 4 * s), (px1, py1 + 4 * s)], fill=BLACK, width=int(1.5 * s))
    for ms in range(-200, 51, 50):
        x = X(ms / 1000)
        dr.line([(x, py1 + 2 * s), (x, py1 + 7 * s)], fill=BLACK, width=int(1.5 * s))
        lab = f"{ms:+d}" if ms else "0"
        dr.text((x - text_w(dr, lab, fl) / 2, py1 + 9 * s), lab, font=fl, fill=BLACK)
    dr.text((X(0.05) + 14 * s, py1 + 9 * s), "ms", font=fl, fill=BLACK)

    # footer: the sound of it
    ff = font(FONT_SERIF_B, 10 * s)
    dr.text((14 * s, 262 * s), "0.2 s · 35 → 250 Hz · a rising whoop, then silence.", font=ff, fill=BLACK)
    dr.text((14 * s, 278 * s), "The first sound ever heard from spacetime itself.", font=ff, fill=BLACK)

    # Tiny inspiral glyph bottom-right: two dots spiralling in.
    gx, gy = 356 * s, 268 * s
    rng = random.Random(150914)
    for i in range(46):
        a = i * 0.42
        rr = 18 * s * (1 - i / 50)
        for sign, col in ((1, BLACK), (-1, RED)):
            x = gx + sign * rr * math.cos(a)
            y = gy + sign * rr * math.sin(a)
            d = max(0.7 * s, 2.0 * s * (1 - i / 50))
            dr.ellipse([x - d, y - d, x + d, y + d], fill=col)

    return finalize(img, dither=False)


# ----------------------------------------------------------- 3. ELEVEN DAYS
def image3_eleven_days():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    ft = font(FONT_LIB_SERIF_B, 30 * s)
    title = "SEPTEMBER"
    dr.text((W * s / 2 - text_w(dr, title, ft) / 2, 8 * s), title, font=ft, fill=BLACK)
    fy = font(FONT_LIB_SERIF, 16 * s)
    yr = "M DCC LII"
    dr.text((W * s / 2 - text_w(dr, yr, fy) / 2, 42 * s), yr, font=fy, fill=RED)
    dr.line([(40 * s, 64 * s), (360 * s, 64 * s)], fill=BLACK, width=s)

    # grid: 7 columns, header row + 3 rows
    gx0, gx1 = 28 * s, 372 * s
    cw = (gx1 - gx0) / 7
    gy0 = 70 * s
    hh = 18 * s
    rh = 46 * s
    fhd = font(FONT_LIB_SERIF, 10 * s)
    for i, d in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        x = gx0 + i * cw + cw / 2 - text_w(dr, d, fhd) / 2
        dr.text((x, gy0 + 3 * s), d, font=fhd, fill=BLACK)
    dr.line([(gx0, gy0 + hh), (gx1, gy0 + hh)], fill=BLACK, width=s)

    # Sept 1752 as lived: Tue 1, Wed 2, Thu 14 ... Sat 30
    cells = [None, None, 1, 2, 14, 15, 16] + list(range(17, 24)) + list(range(24, 31))
    fn = font(FONT_LIB_SERIF, 20 * s)
    for idx, day in enumerate(cells):
        r, c = divmod(idx, 7)
        x0 = gx0 + c * cw
        y0 = gy0 + hh + r * rh
        if day is None:
            continue
        col = RED if day == 14 else BLACK
        dr.text((x0 + 6 * s, y0 + 5 * s), str(day), font=fn, fill=col)
    # cell rules
    for r in range(4):
        y = gy0 + hh + r * rh
        dr.line([(gx0, y), (gx1, y)], fill=BLACK, width=s)
    for c in range(8):
        x = gx0 + c * cw
        dr.line([(x, gy0 + hh), (x, gy0 + hh + 3 * rh)], fill=BLACK, width=s)

    # The eleven missing days: a red seam between Wed 2 and Thu 14, and the
    # numbers themselves struck out beneath the grid.
    seam_x = gx0 + 4 * cw
    dr.line([(seam_x, gy0 + hh), (seam_x, gy0 + hh + rh)], fill=RED, width=3 * s)
    fx = font(FONT_LIB_SERIF, 14 * s)
    missing = "3  4  5  6  7  8  9  10  11  12  13"
    mw = text_w(dr, missing, fx)
    mx0 = W * s / 2 - mw / 2
    my0 = gy0 + hh + 3 * rh + 6 * s
    dr.text((mx0, my0), missing, font=fx, fill=RED)
    dr.line([(mx0 - 6 * s, my0 + 9 * s), (mx0 + mw + 6 * s, my0 + 9 * s)], fill=RED, width=2 * s)
    # tie the struck row to the seam
    dr.line([(seam_x, gy0 + hh + rh), (seam_x, gy0 + hh + rh + 6 * s)], fill=RED, width=3 * s)

    # footer
    ff = font(FONT_LIB_SERIF, 11 * s)
    fi = font(FD + "liberation/LiberationSerif-Italic.ttf", 11 * s)
    dr.text((28 * s, 256 * s), "Wednesday the 2nd was followed by Thursday the 14th: Britain caught up", font=ff, fill=BLACK)
    dr.text((28 * s, 270 * s), "with the Gregorian calendar, and eleven days never happened.", font=ff, fill=BLACK)
    dr.text((28 * s, 285 * s), "“Give us our eleven days!” — a riot that probably never happened either.", font=fi, fill=RED)

    return finalize(img, dither=False)


# --------------------------------------------------------------- 4. TONIGHT
def image4_tonight():
    """Dusk, low in the west-southwest: a 5 % crescent 5½° left of Venus."""
    s = SS
    rng = random.Random(20260914)
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # Twilight gradient: dark at top, pale at horizon.
    horizon = 212 * s
    for y in range(0, horizon):
        t = y / horizon
        v = int(28 + (215 - 28) * (t ** 1.6))
        dr.line([(0, y), (W * s, y)], fill=(v, v, v))

    # a few stars up high (twilight: only the brightest)
    for _ in range(28):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, horizon * 0.55)
        if rng.random() < 0.25:
            dr.ellipse([x - s, y - s, x + s, y + s], fill=WHITE)
        else:
            dr.point((x, y), fill=WHITE)

    # Venus: the brightest thing. Sun is below the horizon to the right (west).
    vx, vy = 262 * s, 118 * s
    for r, v in ((14, 60), (9, 130), (5, 220)):
        rr = r * s
        dr.ellipse([vx - rr, vy - rr, vx + rr, vy + rr], fill=(v, v, v))
    dr.ellipse([vx - 3 * s, vy - 3 * s, vx + 3 * s, vy + 3 * s], fill=WHITE)
    for a in (0, 90):
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        dr.line([(vx - 24 * s * dx, vy - 24 * s * dy), (vx + 24 * s * dx, vy + 24 * s * dy)], fill=WHITE, width=s)

    # Crescent Moon 5.5° to the left (east), slightly higher. Scale: ~13 px per degree.
    mx, my = vx - 5.5 * 13 * s, vy - 16 * s
    mr = 20 * s
    # Sun is to the lower right, so the lit limb faces lower-right.
    moon = Image.new("L", (W * s, H * s), 0)
    md = ImageDraw.Draw(moon)
    md.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=255)
    # subtract an offset disc to leave a thin sliver
    off = mr * 0.30
    ang = math.radians(215)  # direction of the dark disc offset (away from sun)
    ox, oy = mx + off * math.cos(ang), my + off * math.sin(ang)
    md.ellipse([ox - mr * 1.06, oy - mr * 1.06, ox + mr * 1.06, oy + mr * 1.06], fill=0)
    img.paste(WHITE, (0, 0), moon)
    dr = ImageDraw.Draw(img)
    # earthshine: faint outline of the full disc
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=(120, 120, 120), width=s)

    # Horizon: low hills and a few rooftops, black silhouette.
    pts = [(0, horizon)]
    x = 0
    while x <= W * s:
        h = 10 * s * math.sin(x / (70 * s)) + 6 * s * math.sin(x / (23 * s) + 1.2)
        pts.append((x, horizon - 8 * s - h))
        x += 4 * s
    pts += [(W * s, H * s), (0, H * s)]
    dr.polygon(pts, fill=BLACK)
    # rooftops / chimneys, a church spire
    for bx, bw, bh in ((30, 26, 22), (70, 18, 30), (120, 34, 18), (300, 22, 26), (340, 40, 16)):
        dr.rectangle([bx * s, horizon - bh * s, (bx + bw) * s, horizon], fill=BLACK)
    dr.polygon([(190 * s, horizon), (196 * s, horizon - 58 * s), (202 * s, horizon)], fill=BLACK)
    dr.rectangle([186 * s, horizon - 30 * s, 206 * s, horizon], fill=BLACK)
    # lit windows: red points
    for wx, wy in ((78, 18), (84, 18), (132, 8), (312, 14), (352, 8), (36, 12)):
        dr.rectangle([wx * s, (horizon / s - wy) * s, (wx + 3) * s, (horizon / s - wy + 3) * s], fill=RED)

    # Text block on the black ground
    ft = font(FONT_SANS_B, 13 * s)
    fs = font(FONT_SANS, 9 * s)
    fm = font(FONT_MONO, 8.5 * s)
    dr.text((12 * s, 222 * s), "TONIGHT, LOW IN THE WEST-SOUTHWEST", font=ft, fill=WHITE)
    dr.text((12 * s, 240 * s), "30–45 min after sunset: a 5 % crescent Moon 5½° left of Venus,", font=fs, fill=WHITE)
    dr.text((12 * s, 252 * s), "which is at its greatest brilliancy this week. Set early.", font=fs, fill=WHITE)
    dr.line([(12 * s, 268 * s), (388 * s, 268 * s)], fill=RED, width=s)
    dr.text((12 * s, 273 * s), "Wed–Thu 16–17  Moon near Antares", font=fm, fill=WHITE)
    dr.text((12 * s, 285 * s), "Fri 18  first quarter 20:44 UTC", font=fm, fill=WHITE)
    dr.text((214 * s, 273 * s), "Wed 23  equinox", font=fm, fill=WHITE)
    dr.text((214 * s, 285 * s), "Sat 26  Harvest Moon", font=fm, fill=RED)
    # labels in sky
    fl = font(FONT_SANS, 8 * s)
    dr.text((vx + 18 * s, vy + 14 * s), "Venus", font=fl, fill=WHITE)
    dr.text((mx - 18 * s, my + 24 * s), "Moon", font=fl, fill=WHITE)
    # degree bracket
    dr.line([(mx, my + 40 * s), (vx, my + 40 * s)], fill=RED, width=s)
    dr.line([(mx, my + 37 * s), (mx, my + 43 * s)], fill=RED, width=s)
    dr.line([(vx, my + 37 * s), (vx, my + 43 * s)], fill=RED, width=s)
    dr.text(((mx + vx) / 2 - 8 * s, my + 43 * s), "5½°", font=fl, fill=RED)

    return finalize(img, dither=True)


# --------------------------------------------------------------- 5. ASANOHA
def image5_asanoha():
    """Kumiko: a triangular grid, each triangle split by lines from its centroid
    to its corners. That is all it takes to make a field of hemp leaves.
    Behind the lattice, a red moon in the shoji."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # Red moon behind the lattice
    cx, cy, R = 262 * s, 126 * s, 86 * s
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=RED)

    # Triangle grid geometry
    a = 44 * s                      # triangle side
    hgt = a * math.sqrt(3) / 2      # row height
    lw = int(1.6 * s)
    rows = int(H * s / hgt) + 3
    cols = int(W * s / a) + 3

    def vertex(i, j):
        # row j, column i; odd rows shifted half a side
        x = i * a + (a / 2 if j % 2 else 0) - a
        y = j * hgt - hgt
        return (x, y)

    tris = []
    for j in range(rows):
        for i in range(cols):
            p0 = vertex(i, j)
            p1 = vertex(i + 1, j)
            if j % 2 == 0:
                q_up = vertex(i, j + 1)     # apex above-ish? build both up and down triangles
                q_dn = vertex(i + 1, j + 1)
                tris.append((p0, p1, vertex(i, j + 1)))
                tris.append((p1, vertex(i, j + 1), vertex(i + 1, j + 1)))
            else:
                tris.append((p0, p1, vertex(i + 1, j + 1)))
                tris.append((p0, vertex(i, j + 1), vertex(i + 1, j + 1)))

    # Frame lines (the grid itself) and the leaf lines (centroid spokes)
    for (p, q, r) in tris:
        dr.line([p, q, r, p], fill=BLACK, width=lw)
        gx = (p[0] + q[0] + r[0]) / 3
        gy = (p[1] + q[1] + r[1]) / 3
        for v in (p, q, r):
            dr.line([(gx, gy), v], fill=BLACK, width=lw)

    # Wooden frame: thick border, white margin with caption at bottom.
    dr.rectangle([0, 0, W * s, H * s], outline=BLACK, width=6 * s)
    dr.rectangle([0, 262 * s, W * s, H * s], fill=WHITE)
    dr.line([(0, 262 * s), (W * s, 262 * s)], fill=BLACK, width=6 * s)
    fj = font(FONT_JP, 18 * s)
    dr.text((14 * s, 270 * s), "麻の葉", font=fj, fill=BLACK)
    fs = font(FONT_SANS, 9 * s)
    dr.text((78 * s, 271 * s), "asanoha, hemp leaf: a triangle grid, each triangle split from its centre.", font=fs, fill=BLACK)
    dr.text((78 * s, 284 * s), "Kumiko lattice, no nails. A red moon behind the paper window.", font=fs, fill=BLACK)

    return finalize(img, dither=False)


def main():
    save(image1_klin(), 1)
    save(image2_chirp(), 2)
    save(image3_eleven_days(), 3)
    save(image4_tonight(), 4)
    save(image5_asanoha(), 5)
    print("done")


if __name__ == "__main__":
    main()
