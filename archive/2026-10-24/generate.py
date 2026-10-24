#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-24.

Five 400x300 images in exactly three colors (white, black, red).
Hooks for the day: first photograph of Earth from space (V-2 No. 13,
24 Oct 1946), the nearly-full Hunter's Moon beside Saturn tonight,
Houdini's last performance (24 Oct 1926), Black Thursday (24 Oct 1929),
and Anni Albers' trapezoid prints.

Run from the repo root:  python3 archive/2026-10-24/generate.py
"""

import math
import os
import random

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
SERIF_B = F + "dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = F + "freefont/FreeSerifItalic.ttf"
SERIF_BI = F + "freefont/FreeSerifBoldItalic.ttf"
SANS_B = F + "liberation/LiberationSans-Bold.ttf"
CONDENSED = F + "dejavu/DejaVuSans-Bold.ttf"

OUT_DIRS = ["images", "archive/2026-10-24"]


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


def value_noise(w, h, rng, octaves=5, base=4):
    """Fractal value noise in [0,1], shape (h, w)."""
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        n = base * (2 ** o)
        grid = rng.random((n + 1, int(n * w / h) + 2)).astype(np.float32)
        layer = Image.fromarray((grid * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += amp * np.asarray(layer, np.float32) / 255.0
        total += amp
        amp *= 0.5
    out /= total
    return (out - out.min()) / (out.max() - out.min() + 1e-9)


def text_c(dr, xy, s, f, fill, anchor="mm"):
    dr.text(xy, s, font=f, fill=fill, anchor=anchor)


# ------------------------------------------------------------ 1. 105 km
def image1_first_photo():
    """A frame of 35mm film from V-2 No. 13: the first picture of Earth from space."""
    rng = np.random.default_rng(19461024)
    s = SS
    w, h = W * s, H * s
    # Film strip: black, frame window in the middle, sprocket holes on both sides.
    fx0, fx1, fy0, fy1 = 52 * s, 348 * s, 30 * s, 262 * s
    fw, fh = fx1 - fx0, fy1 - fy0

    # Build the photograph as a float luminance field.
    yy, xx = np.mgrid[0:fh, 0:fw].astype(np.float32)
    # Earth limb: a huge circle, centre far below and to the right, tilted horizon.
    cx, cy, R = fw * 0.62, fh * 2.05, fh * 1.55
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    earth = d < R
    clouds = value_noise(fw, fh, rng, octaves=6, base=3)
    streak = value_noise(fw, fh, rng, octaves=3, base=2)
    # Perspective squash of clouds toward the horizon: darker, flatter near limb.
    depth = np.clip((R - d) / (fh * 0.9), 0, 1)
    ground = 0.30 + 0.25 * streak
    cloud = np.clip((clouds - 0.45) * 3.6, 0, 1)
    lum = np.where(earth, ground * (0.55 + 0.45 * depth) + cloud * (0.35 + 0.55 * depth), 0.0)
    # Atmospheric haze glow just above the limb.
    haze = np.exp(-np.clip(d - R, 0, None) / (fh * 0.022)) * (~earth)
    lum = lum + 0.95 * haze
    lum = np.where(earth & (R - d < fh * 0.02), lum + 0.35, lum)
    # Space is not perfectly black on old film: faint fog.
    lum = lum + 0.02
    # Lens vignette and grain.
    vx = (xx / fw - 0.5) * 2
    vy = (yy / fh - 0.5) * 2
    lum *= 1.0 - 0.38 * (vx ** 2 + vy ** 2) ** 1.2
    lum += rng.normal(0, 0.06, lum.shape).astype(np.float32)
    lum = np.clip(lum, 0, 1)
    photo = Image.fromarray((lum * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))
    # A scratch down the emulsion.
    pd = ImageDraw.Draw(photo)
    sx = int(fw * 0.31)
    pts = [(sx + int(6 * math.sin(t / 50.0)), t) for t in range(0, fh, 6)]
    pd.line(pts, fill=225, width=2)
    for _ in range(40):  # dust
        x, y = int(rng.integers(0, fw)), int(rng.integers(0, fh))
        r = int(rng.integers(1, 4))
        pd.ellipse([x - r, y - r, x + r, y + r], fill=int(rng.choice([10, 240])))

    img = Image.new("RGB", (w, h), BLACK)
    img.paste(photo.convert("RGB"), (fx0, fy0))
    dr = ImageDraw.Draw(img)
    # Rounded frame corners: mask with black.
    dr.rounded_rectangle([fx0, fy0, fx1, fy1], radius=6 * s, outline=BLACK, width=3 * s)
    # Sprocket holes.
    for y in range(8 * s, h, 22 * s):
        for x in (14 * s, 370 * s):
            dr.rounded_rectangle([x, y, x + 16 * s, y + 11 * s], radius=3 * s, fill=WHITE)
    # Edge printing in red, like film edge codes.
    fm = font(MONO_B, 9 * s)
    dr.text((fx0, 268 * s), "V-2 No.13  WHITE SANDS N.M.", font=fm, fill=RED)
    dr.text((fx1, 268 * s), "24·X·1946", font=fm, fill=RED, anchor="ra")
    fm2 = font(MONO, 8 * s)
    dr.text((fx0, 14 * s), "105 km ▲", font=fm2, fill=WHITE)
    dr.text((fx1, 14 * s), "FRAME 0216  Δt 1.5 s", font=fm2, fill=WHITE, anchor="ra")
    # Rotated edge text along the right margin.
    t = Image.new("RGB", (240 * s, 12 * s), BLACK)
    ImageDraw.Draw(t).text((0, 0), "DEVRY 35  ·  FILM SURVIVED IN A STEEL CASSETTE", font=font(MONO, 7 * s), fill=RED)
    t = t.rotate(90, expand=True)
    img.paste(t, (356 * s, 32 * s))
    return finalize(img)


# ------------------------------------------------------------ 2. Hunter's Moon
def image2_hunters_moon():
    """Nearly-full Hunter's Moon rising red beside Saturn, over a stubble field."""
    rng = np.random.default_rng(20261024)
    s = SS
    w, h = W * s, H * s
    img = Image.new("RGB", (w, h), BLACK)
    dr = ImageDraw.Draw(img)
    hz = 196 * s  # horizon

    # Stars (sparse — moonlight washes them out).
    for _ in range(70):
        x, y = int(rng.integers(0, w)), int(rng.integers(0, hz - 20 * s))
        r = s * (1 if rng.random() < 0.85 else 1.6)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(200, 200, 200))

    # Moon: 97% lit, red from the long path through the evening air.
    mx, my, mr = 262 * s, 128 * s, 50 * s
    moon = np.zeros((2 * mr, 2 * mr, 3), np.float32)
    yy, xx = np.mgrid[-mr:mr, -mr:mr].astype(np.float32)
    rr = np.sqrt(xx ** 2 + yy ** 2)
    disk = rr < mr
    maria = value_noise(2 * mr, 2 * mr, rng, octaves=4, base=3)
    lit = 1.0 - 0.75 * np.clip((maria - 0.52) * 4, 0, 1)
    # Terminator sliver on the left (waxing gibbous, ~97%).
    term = xx < -mr * np.sqrt(np.clip(1 - (yy / mr) ** 2, 0, 1)) * 0.93
    lit = np.where(term, 0.15, lit)
    limb = 0.82 + 0.18 * np.sqrt(np.clip(1 - (rr / mr) ** 2, 0, 1))
    lit *= limb
    moon[..., 0] = np.where(disk, 255 * np.clip(lit, 0, 1), 0)
    mimg = Image.fromarray(moon.astype(np.uint8))
    mask = Image.fromarray((disk * 255).astype(np.uint8))
    img.paste(mimg, (mx - mr, my - mr), mask)
    # Faint halo rings.
    for k, rad in enumerate((mr + 9 * s, mr + 17 * s)):
        dr.ellipse([mx - rad, my - rad, mx + rad, my + rad], outline=(90, 0, 0), width=s)

    # Saturn: small white globe with ring, up and to the right.
    sx, sy = 352 * s, 70 * s
    dr.ellipse([sx - 10 * s, sy - 3 * s, sx + 10 * s, sy + 3 * s], outline=WHITE, width=s)
    dr.ellipse([sx - 4 * s, sy - 4 * s, sx + 4 * s, sy + 4 * s], fill=WHITE)
    dr.line([sx - 10 * s, sy, sx - 4 * s, sy + 1 * s], fill=BLACK, width=s)
    fl = font(SERIF_I, 13 * s)
    dr.text((sx, sy + 9 * s), "Saturn", font=fl, fill=WHITE, anchor="ma")

    # Distant tree line silhouette.
    ridge = [(0, h)]
    noise = value_noise(w, 4, rng, octaves=5, base=2)[0]
    for x in range(0, w + s, s):
        bump = noise[min(x, w - 1)] * 14 * s
        tree = (math.sin(x / (3.1 * s)) * 0.5 + 0.5) * 4 * s * (noise[min(x, w - 1)] > 0.5)
        ridge.append((x, hz - bump - tree))
    ridge.append((w, h))
    dr.polygon(ridge, fill=(18, 18, 18))
    dr.rectangle([0, hz, w, h], fill=BLACK)

    # Stubble rows converging on a vanishing point under the moon.
    vx, vy = mx, hz
    for i in range(-30, 31):
        x_bottom = vx + i * 34 * s
        dr.line([(vx + i * 2 * s, vy + 2 * s), (x_bottom, h)], fill=(120, 120, 120), width=s)
    # Moonlight glitter on the furrows, a path toward the viewer.
    for _ in range(520):
        t = rng.random() ** 1.6
        y = hz + 4 * s + t * (h - hz)
        spread = 6 * s + t * 120 * s
        x = mx + rng.normal(0, 1) * spread * 0.45
        r = s * (0.6 + 1.6 * t)
        dr.ellipse([x - r, y - r * 0.5, x + r, y + r * 0.5], fill=(255, 40, 40) if rng.random() < 0.5 else (230, 230, 230))
    # Round hay bales.
    for bx, by, br in ((70, 238, 26), (150, 214, 13), (345, 226, 18), (205, 205, 7)):
        bx, by, br = bx * s, by * s, br * s
        dr.ellipse([bx - br, by - br, bx + br, by + br * 0.85], fill=BLACK)
        dr.arc([bx - br, by - br, bx + br, by + br * 0.85], 280, 360, fill=RED, width=2 * s)
        dr.arc([bx - br * 0.6, by - br * 0.6, bx + br * 0.6, by + br * 0.5], 290, 350, fill=(140, 0, 0), width=s)

    # Caption.
    dr.text((14 * s, 16 * s), "HUNTER'S MOON", font=font(MONO_B, 13 * s), fill=WHITE)
    dr.text((14 * s, 33 * s), "24 Oct 2026 · 97% · waxing", font=font(MONO, 9 * s), fill=WHITE)
    dr.text((14 * s, 46 * s), "full by Monday", font=font(MONO, 9 * s), fill=WHITE)
    return finalize(img)


# ------------------------------------------------------------ 3. Éclat
def image3_albers():
    """Interlocking trapezoids & parallelograms, after Anni Albers' PO II / Éclat.

    Each band is cut by lines of slope +k, -k (or vertical). Between two cuts:
    opposite slants -> trapezoid, same slants -> parallelogram. Bands are mirrored
    and rotated in pairs, as Albers rotated her units.
    """
    rnd = random.Random(1973)
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    mx, my = 22, 26
    bands = 7
    gap = 4
    bh = (H - 2 * my - gap * (bands - 1)) // bands
    k = bh * 0.55  # horizontal offset of a slanted cut over one band height
    colors = [BLACK, RED, WHITE]

    def make_band():
        cuts = []
        x = mx
        while x < W - mx - 30:
            step = rnd.choice([14, 22, 22, 30, 38, 52])
            x += step
            cuts.append((x, rnd.choice([1, -1, 1, -1, 0])))
        return cuts

    proto = [make_band() for _ in range(3)]
    for b in range(bands):
        y0 = my + b * (bh + gap)
        y1 = y0 + bh
        cuts = proto[b % 3]
        flip = (b // 3) % 2 == 1  # every third band: rotate 180 degrees
        prev_top, prev_bot = mx, mx
        last = None
        pieces = []
        for (cx, sl) in cuts + [(W - mx, 0)]:
            top = cx + sl * k / 2
            bot = cx - sl * k / 2
            top = min(max(top, mx), W - mx)
            bot = min(max(bot, mx), W - mx)
            pieces.append([(prev_top, y0), (top, y0), (bot, y1), (prev_bot, y1)])
            prev_top, prev_bot = top, bot
        rng_c = random.Random(b % 3)
        for i, poly in enumerate(pieces):
            if flip:
                poly = [(W - x, y0 + y1 - y) for (x, y) in poly]
            choices = [c for c in colors if c != last]
            c = rng_c.choices(choices, weights=[5 if cc == BLACK else 2 if cc == RED else 3 for cc in choices])[0]
            last = c
            dr.polygon(poly, fill=c)
            if c == WHITE:
                dr.polygon(poly, outline=BLACK)
        dr.rectangle([mx, y0, W - mx, y1], outline=BLACK)
    f = font(MONO, 10)
    dr.text((mx, H - 17), "after Anni Albers: trapezoids + parallelograms, rotated", font=f, fill=BLACK)
    dr.text((W - mx, 8), "PO II / 1973", font=font(MONO_B, 10), fill=RED, anchor="ra")
    return finalize(img, dither=False)


# ------------------------------------------------------------ 4. Houdini
def image4_houdini():
    """Playbill for Houdini's last performance, Garrick Theatre, Detroit, 24 Oct 1926."""
    s = SS
    w, h = W * s, H * s
    img = Image.new("RGB", (w, h), WHITE)
    dr = ImageDraw.Draw(img)
    # Double border with corner stars.
    dr.rectangle([6 * s, 6 * s, w - 6 * s, h - 6 * s], outline=BLACK, width=3 * s)
    dr.rectangle([11 * s, 11 * s, w - 11 * s, h - 11 * s], outline=RED, width=s)

    def star(cx, cy, r, fill):
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rad = r if i % 2 == 0 else r * 0.42
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
        dr.polygon(pts, fill=fill)

    for cx, cy in ((22, 22), (378, 22), (22, 278), (378, 278)):
        star(cx * s, cy * s, 7 * s, RED)

    text_c(dr, (w / 2, 34 * s), "GARRICK THEATRE · DETROIT", font(MONO_B, 11 * s), BLACK)
    # HOUDINI, big red, with a black drop shadow.
    fh = font(SERIF_B, 54 * s)
    text_c(dr, (w / 2 + 3 * s, 76 * s + 3 * s), "HOUDINI", fh, BLACK)
    text_c(dr, (w / 2, 76 * s), "HOUDINI", fh, RED)
    text_c(dr, (w / 2, 112 * s), "— the final performance —", font(SERIF_I, 16 * s), BLACK)

    # The trunk, bound in chain, with a red padlock.
    tx0, ty0, tx1, ty1 = 132 * s, 132 * s, 268 * s, 222 * s
    dr.rectangle([tx0, ty0, tx1, ty1], fill=BLACK)
    for x in (tx0 + 22 * s, tx1 - 22 * s):
        dr.rectangle([x - 4 * s, ty0, x + 4 * s, ty1], fill=WHITE)
        dr.rectangle([x - 2 * s, ty0, x + 2 * s, ty1], fill=BLACK)
    for y in range(ty0 + 8 * s, ty1, 10 * s):  # wood planks
        dr.line([tx0 + 30 * s, y, tx1 - 30 * s, y], fill=(70, 70, 70), width=s)
    dr.rectangle([tx0, ty0, tx1, ty1], outline=BLACK, width=2 * s)

    def chain(p0, p1, link=15 * s):
        (x0, y0), (x1, y1) = p0, p1
        L = math.hypot(x1 - x0, y1 - y0)
        n = int(L / (link * 0.8))
        ang = math.atan2(y1 - y0, x1 - x0)
        for i in range(n + 1):
            t = i / n
            cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            a, b = (link * 0.7, link * 0.42) if i % 2 == 0 else (link * 0.7, link * 0.16)
            # draw a rotated ellipse as a polygon
            pts = [(cx + a * math.cos(u) * math.cos(ang) - b * math.sin(u) * math.sin(ang),
                    cy + a * math.cos(u) * math.sin(ang) + b * math.sin(u) * math.cos(ang))
                   for u in np.linspace(0, 2 * math.pi, 28)]
            inner = [(cx + (px - cx) * 0.5, cy + (py - cy) * 0.45) for px, py in pts]
            if i % 2 == 0:
                dr.polygon(pts, fill=WHITE, outline=BLACK, width=int(2 * s))
                dr.polygon(inner, fill=BLACK)
            else:
                dr.polygon(pts, fill=WHITE, outline=BLACK, width=int(2 * s))

    chain((tx0 - 18 * s, ty0 - 8 * s), (tx1 + 18 * s, ty1 + 8 * s))
    chain((tx1 + 18 * s, ty0 - 8 * s), (tx0 - 18 * s, ty1 + 8 * s))
    # Padlock where the chains cross.
    cx, cy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
    dr.arc([cx - 11 * s, cy - 26 * s, cx + 11 * s, cy - 2 * s], 180, 360, fill=BLACK, width=5 * s)
    dr.rounded_rectangle([cx - 16 * s, cy - 12 * s, cx + 16 * s, cy + 16 * s], radius=4 * s, fill=RED, outline=BLACK, width=2 * s)
    dr.ellipse([cx - 3 * s, cy - 2 * s, cx + 3 * s, cy + 4 * s], fill=BLACK)
    dr.polygon([(cx - 2 * s, cy + 2 * s), (cx + 2 * s, cy + 2 * s), (cx + 1 * s, cy + 10 * s), (cx - 1 * s, cy + 10 * s)], fill=BLACK)

    text_c(dr, (w / 2, 244 * s), "SUNDAY · OCTOBER 24 · 1926", font(MONO_B, 13 * s), BLACK)
    text_c(dr, (w / 2, 263 * s), "he played on with a burst appendix; gone by Halloween",
           font(SERIF_BI, 13 * s), BLACK)
    # Side flourishes.
    f = font(SERIF_BI, 15 * s)
    text_c(dr, (66 * s, 176 * s), "Escapes!", f, BLACK)
    text_c(dr, (334 * s, 176 * s), "Illusions!", f, BLACK)
    text_c(dr, (66 * s, 196 * s), "★", font(CONDENSED, 14 * s), RED)
    text_c(dr, (334 * s, 196 * s), "★", font(CONDENSED, 14 * s), RED)
    return finalize(img, dither=False)


# ------------------------------------------------------------ 5. Black Thursday
def image5_ticker():
    """Ticker tape unspooling across a falling chart, 24 Oct 1929."""
    rnd = random.Random(1929)
    s = SS
    w, h = W * s, H * s
    img = Image.new("RGB", (w, h), WHITE)
    dr = ImageDraw.Draw(img)
    # Graph paper.
    for x in range(0, w, 10 * s):
        dr.line([x, 0, x, h], fill=(222, 222, 222), width=1)
    for y in range(0, h, 10 * s):
        dr.line([0, y, w, y], fill=(222, 222, 222), width=1)
    for x in range(0, w, 50 * s):
        dr.line([x, 0, x, h], fill=(190, 190, 190), width=s)
    for y in range(0, h, 50 * s):
        dr.line([0, y, w, y], fill=(190, 190, 190), width=s)

    # Price line in red: the morning cliff, then the bankers' afternoon rally.
    pts = []
    v = 30.0
    for i in range(0, 401, 4):
        if i < 140:
            v += rnd.uniform(-1.8, 2.0)
        elif i < 250:
            v += rnd.uniform(0.0, 5.2)
        else:
            v -= rnd.uniform(-1.0, 2.4)
        pts.append((i * s, (v + 10) * s))
    dr.line(pts, fill=RED, width=4 * s, joint="curve")

    # Ticker tape: a ribbon along a looping parametric path.
    def path(t):
        x = -20 + 440 * t + 38 * math.sin(t * 2 * math.pi * 2.2)
        y = 60 + 150 * t + 52 * math.sin(t * 2 * math.pi * 1.1 + 0.6) - 26 * math.cos(t * 2 * math.pi * 2.2)
        return x * s, y * s

    N = 1400
    samples = [path(i / N) for i in range(N + 1)]
    half = 13 * s
    # Draw ribbon as many short quads (so self-overlaps stack in order) with text.
    tokens = []
    stocks = [("X", 205.5), ("GM", 58.0), ("RCA", 68.75), ("T", 272.0), ("GE", 315.0),
              ("KO", 160.0), ("WX", 190.0), ("NYC", 230.0), ("AN", 120.0), ("MW", 83.0)]
    for rep in range(6):
        for sym, p in stocks:
            p_now = p * (1 - 0.035 * rep - rnd.uniform(0, 0.05))
            frac = rnd.choice(["", "¼", "½", "¾"])
            tokens.append(f"{sym} {int(p_now)}{frac} ▼   ")
    tape_text = "" .join(tokens)
    ff = font(MONO_B, 15 * s)

    # Precompute arc length.
    arc = [0.0]
    for i in range(1, len(samples)):
        arc.append(arc[-1] + math.dist(samples[i - 1], samples[i]))
    char_w = ff.getlength("M")

    def normal(i):
        i = min(max(i, 1), len(samples) - 2)
        (x0, y0), (x1, y1) = samples[i - 1], samples[i + 1]
        L = math.hypot(x1 - x0, y1 - y0) or 1
        return (-(y1 - y0) / L, (x1 - x0) / L), math.atan2(y1 - y0, x1 - x0)

    ci = 0
    next_char_at = 0.0
    pending = []
    for i in range(1, len(samples)):
        (nx, ny), ang = normal(i)
        (px, py), _ = normal(i - 1)
        a, b = samples[i - 1], samples[i]
        quad = [(a[0] + px * half, a[1] + py * half), (b[0] + nx * half, b[1] + ny * half),
                (b[0] - nx * half, b[1] - ny * half), (a[0] - px * half, a[1] - py * half)]
        # drop shadow
        sh = [(x + 3 * s, y + 4 * s) for x, y in quad]
        dr.polygon(sh, fill=(150, 150, 150))
        dr.polygon(quad, fill=WHITE)
        dr.line([quad[0], quad[1]], fill=BLACK, width=s)
        dr.line([quad[3], quad[2]], fill=BLACK, width=s)
        if arc[i] >= next_char_at and ci < len(tape_text):
            ch = tape_text[ci]
            ci += 1
            next_char_at += char_w
            if ch != " ":
                g = Image.new("L", (int(char_w * 2), int(char_w * 2)), 0)
                ImageDraw.Draw(g).text((char_w, char_w), ch, font=ff, fill=255, anchor="mm")
                if ch != "▼":  # the down-arrows always point down
                    g = g.rotate(-math.degrees(ang), resample=Image.BICUBIC)
                col = RED if ch == "▼" else BLACK
                pending.append((arc[i], g, col, (int(b[0] - char_w), int(b[1] - char_w))))
        # Stamp glyphs once the tape beneath and just ahead of them is laid down.
        while pending and pending[0][0] < arc[i] - char_w * 1.5:
            _, g, col, pos = pending.pop(0)
            img.paste(Image.new("RGB", g.size, col), pos, g)
    for _, g, col, pos in pending:
        img.paste(Image.new("RGB", g.size, col), pos, g)

    # Headline block.
    dr.rectangle([12 * s, 232 * s, 222 * s, 288 * s], fill=BLACK)
    dr.text((20 * s, 238 * s), "BLACK THURSDAY", font=font(MONO_B, 17 * s), fill=WHITE)
    dr.text((20 * s, 260 * s), "24 OCT 1929 · 12,894,650 SHARES", font=font(MONO, 9 * s), fill=WHITE)
    dr.text((20 * s, 273 * s), "the tickers ran hours behind", font=font(MONO, 9 * s), fill=RED)
    return finalize(img)


def main():
    makers = [image1_first_photo, image2_hunters_moon, image3_albers, image4_houdini, image5_ticker]
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
    for i, mk in enumerate(makers, 1):
        im = mk()
        assert im.size == (W, H)
        for d in OUT_DIRS:
            im.save(os.path.join(d, f"{i}.png"))
        print("made", i, mk.__name__)


if __name__ == "__main__":
    main()
