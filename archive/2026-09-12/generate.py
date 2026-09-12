#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-12.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

Today's threads:
  1. Lascaux — 86 years since Marcel Ravidat's dog Robot found the hole (12 Sep 1940).
     Red ochre + manganese black on limestone: the cave's palette *is* this screen's palette.
  2. Two Crescents — on 14 Sep the (crescent) Moon passes in front of (crescent) Venus.
  3. Red Wedge — a constructivist Proun, finally. Black/white/red is Lissitzky's palette too.
  4. Wagtails Sing — 鶺鴒鳴, the 44th of Japan's 72 microseasons, begins tomorrow.
  5. Typewriter Art — Sholes finished the first practical typewriter on 12 Sep 1873.
     A butterfly typed in the manner of Flora Stacey (1898), on a two-colour ribbon.

Technique: tonal scenes render at 3x, LANCZOS downscale, Floyd–Steinberg dither into the
exact palette; hard-edged pieces render at 3x and quantize without dither (crisp edges).
"""

import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FT = "/usr/share/fonts/truetype/"
FONT_SANS = FT + "dejavu/DejaVuSans.ttf"
FONT_SANS_B = FT + "dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = FT + "dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = FT + "dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = FT + "freefont/FreeMono.ttf"
FONT_MONO_B = FT + "freefont/FreeMonoBold.ttf"
FONT_COND = FT + "liberation/LiberationSansNarrow-Bold.ttf"
FONT_JP = FT + "fonts-japanese-gothic.ttf"
FONT_JP_MINCHO = FT + "noto/wqy-zenhei.ttc"

OUT_DIRS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__))),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "images"),
]


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
    if not os.path.exists(path):
        path = FONT_SANS
    return ImageFont.truetype(path, size)


def seal(img, s=1, corner="br", margin=6):
    """My maker's mark: a small red square with a white pinhole. Same every day."""
    dr = ImageDraw.Draw(img)
    size = 9 * s
    if corner == "br":
        x0, y0 = W * s - margin * s - size, H * s - margin * s - size
    elif corner == "tr":
        x0, y0 = W * s - margin * s - size, margin * s
    elif corner == "bl":
        x0, y0 = margin * s, H * s - margin * s - size
    else:
        x0, y0 = margin * s, margin * s
    dr.rectangle([x0, y0, x0 + size, y0 + size], fill=RED)
    c = size // 2
    dr.rectangle([x0 + c - s, y0 + c - s, x0 + c + s, y0 + c + s], fill=WHITE)


def catmull_rom(points, closed=True, steps=12):
    """Smooth a control polygon into many points."""
    pts = list(points)
    n = len(pts)
    out = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n]
        p1 = pts[i % n]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n]
        for t_i in range(steps):
            t = t_i / steps
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    if not closed:
        out.append(pts[-1])
    return out


def wobble_line(dr, pts, width, fill, rng, amp=1.0, closed=False):
    """A hand-drawn stroke: jittered polyline with varying width."""
    if closed:
        pts = list(pts) + [pts[0]]
    jit = [(x + rng.gauss(0, amp), y + rng.gauss(0, amp)) for x, y in pts]
    for i in range(len(jit) - 1):
        w = max(1, int(width * rng.uniform(0.6, 1.3)))
        dr.line([jit[i], jit[i + 1]], fill=fill, width=w)
        r = w / 2
        dr.ellipse([jit[i][0] - r, jit[i][1] - r, jit[i][0] + r, jit[i][1] + r], fill=fill)


def spray(dr, cx, cy, radius, n, fill, rng, dot=1.0, falloff=1.0):
    for _ in range(n):
        a = rng.uniform(0, 2 * math.pi)
        d = radius * (rng.random() ** falloff)
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        r = dot * rng.uniform(0.5, 1.4)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=fill)


# ------------------------------------------------------------------ 1. Lascaux
def image1_lascaux():
    rng = random.Random(19400912)
    s = SS
    Ws, Hs = W * s, H * s

    # Limestone: a warm, mottled pale ground made from layered noise.
    noise = np.zeros((Hs, Ws), dtype=np.float32)
    nrng = np.random.default_rng(1940)
    for octave, amp in ((6, 0.5), (14, 0.28), (40, 0.14), (120, 0.08)):
        small = nrng.random((octave * 3 // 4 + 1, octave + 1)).astype(np.float32)
        layer = np.array(Image.fromarray((small * 255).astype(np.uint8)).resize((Ws, Hs), Image.BICUBIC), dtype=np.float32) / 255.0
        noise += amp * layer
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    stone = 200 + 55 * noise  # light grey with slight variation -> mostly white after dither
    img = Image.fromarray(stone.astype(np.uint8)).convert("RGB")
    dr = ImageDraw.Draw(img)

    # Cracks in the rock
    for _ in range(5):
        x, y = rng.uniform(0, Ws), rng.uniform(0, Hs)
        pts = [(x, y)]
        ang = rng.uniform(0, 2 * math.pi)
        for _ in range(rng.randint(20, 60)):
            ang += rng.gauss(0, 0.5)
            x += math.cos(ang) * 9 * s
            y += math.sin(ang) * 9 * s
            pts.append((x, y))
        dr.line(pts, fill=(120, 120, 120), width=1 * s)

    # --- The great aurochs (manganese black outline, ochre wash inside) ---
    # Control polygon in a 0..1 box, drawn facing left.
    bull = [
        (0.02, 0.46),  # muzzle top
        (0.06, 0.34), (0.12, 0.26),  # forehead, poll
        (0.20, 0.22), (0.30, 0.12), (0.42, 0.10),  # neck, hump
        (0.56, 0.13), (0.72, 0.15), (0.88, 0.20),  # back to rump
        (0.96, 0.30), (0.97, 0.46),  # rump
        (0.92, 0.56), (0.90, 0.75), (0.89, 0.94),  # hind leg back
        (0.82, 0.94), (0.81, 0.74), (0.77, 0.60),  # hind leg front
        (0.60, 0.62), (0.44, 0.62),  # belly
        (0.40, 0.76), (0.40, 0.94),  # foreleg back
        (0.31, 0.94), (0.31, 0.76), (0.28, 0.62),  # foreleg front
        (0.18, 0.64), (0.08, 0.62), (0.02, 0.56),  # dewlap, jaw, muzzle bottom
    ]
    bx, by, bw, bh = 30 * s, 38 * s, 330 * s, 166 * s
    body = [(bx + px * bw, by + py * bh) for px, py in bull]
    outline = catmull_rom(body, closed=True, steps=10)

    # ochre wash: sprayed red inside the body, denser along the back and shoulder
    mask = Image.new("L", (Ws, Hs), 0)
    ImageDraw.Draw(mask).polygon(outline, fill=255)
    wash = Image.new("RGB", (Ws, Hs), (255, 255, 255))
    wd = ImageDraw.Draw(wash)
    for _ in range(3200):
        x = rng.uniform(bx, bx + bw)
        y = rng.uniform(by, by + bh)
        # more paint high on the body
        if rng.random() < ((y - by) / bh) ** 1.2:
            continue
        r = rng.uniform(0.8, 2.4) * s
        wd.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    img.paste(wash, (0, 0), mask)
    dr = ImageDraw.Draw(img)

    # black outline, hand-drawn, thick
    wobble_line(dr, outline, 5 * s, BLACK, rng, amp=1.2 * s, closed=True)
    # horns: two long forward curves
    horn1 = catmull_rom([(bx + 0.12 * bw, by + 0.27 * bh), (bx + 0.07 * bw, by + 0.12 * bh), (bx + 0.05 * bw, by - 0.04 * bh), (bx + 0.10 * bw, by - 0.14 * bh)], closed=False, steps=10)
    horn2 = catmull_rom([(bx + 0.17 * bw, by + 0.24 * bh), (bx + 0.13 * bw, by + 0.08 * bh), (bx + 0.12 * bw, by - 0.08 * bh), (bx + 0.18 * bw, by - 0.18 * bh)], closed=False, steps=10)
    wobble_line(dr, horn1, 4 * s, BLACK, rng, amp=0.8 * s)
    wobble_line(dr, horn2, 4 * s, BLACK, rng, amp=0.8 * s)
    # eye, nostril
    ex, ey = bx + 0.10 * bw, by + 0.40 * bh
    dr.ellipse([ex - 4 * s, ey - 4 * s, ex + 4 * s, ey + 4 * s], fill=BLACK)
    dr.ellipse([ex - 1.5 * s, ey - 1.5 * s, ex + 1.5 * s, ey + 1.5 * s], fill=WHITE)
    wobble_line(dr, [(bx + 0.03 * bw, by + 0.50 * bh), (bx + 0.06 * bw, by + 0.48 * bh)], 3 * s, BLACK, rng, amp=0.3 * s)
    # shoulder / haunch modelling lines in black
    wobble_line(dr, catmull_rom([(bx + 0.30 * bw, by + 0.22 * bh), (bx + 0.26 * bw, by + 0.42 * bh), (bx + 0.31 * bw, by + 0.58 * bh)], closed=False), 3 * s, BLACK, rng, amp=0.6 * s)
    wobble_line(dr, catmull_rom([(bx + 0.88 * bw, by + 0.30 * bh), (bx + 0.80 * bw, by + 0.40 * bh), (bx + 0.80 * bw, by + 0.58 * bh)], closed=False), 3 * s, BLACK, rng, amp=0.6 * s)

    # --- A small red horse running the other way, low right ---
    horse = [
        (0.94, 0.42), (0.90, 0.30), (0.82, 0.24), (0.70, 0.22), (0.52, 0.20), (0.36, 0.22), (0.22, 0.26),
        (0.10, 0.34), (0.08, 0.50), (0.14, 0.62), (0.24, 0.68), (0.20, 0.92), (0.28, 0.92), (0.32, 0.70),
        (0.60, 0.70), (0.64, 0.92), (0.72, 0.92), (0.72, 0.68), (0.84, 0.66), (0.92, 0.60), (0.98, 0.52),
    ]
    hx, hy, hw, hh = 284 * s, 206 * s, 92 * s, 46 * s
    hpts = catmull_rom([(hx + px * hw, hy + py * hh) for px, py in horse], closed=True, steps=8)
    dr.polygon(hpts, fill=RED)
    # mane: black comb strokes along the neck/back
    for i in range(9):
        t = 0.30 + i * 0.055
        x0 = hx + t * hw
        y0 = hy + 0.21 * hh
        wobble_line(dr, [(x0, y0), (x0 - 4 * s, y0 - 10 * s)], 2 * s, BLACK, rng, amp=0.4 * s)
    wobble_line(dr, hpts, 2 * s, BLACK, rng, amp=0.5 * s, closed=True)

    # --- Negative hand stencil, top right: spray red around a hand ---
    hand_mask = Image.new("L", (Ws, Hs), 0)
    hd = ImageDraw.Draw(hand_mask)
    hcx, hcy = 345 * s, 62 * s
    hd.ellipse([hcx - 16 * s, hcy - 6 * s, hcx + 16 * s, hcy + 34 * s], fill=255)  # palm
    fingers = [(-17, -30, 3.6), (-6, -40, 3.8), (6, -38, 3.8), (17, -26, 3.4)]
    for fx, fy, fw in fingers:
        hd.line([(hcx + fx * 0.6 * s, hcy + 2 * s), (hcx + fx * s, hcy + fy * s)], fill=255, width=int(fw * 2 * s))
        dr_r = fw * s
        hd.ellipse([hcx + fx * s - dr_r, hcy + fy * s - dr_r, hcx + fx * s + dr_r, hcy + fy * s + dr_r], fill=255)
    hd.line([(hcx - 12 * s, hcy + 14 * s), (hcx - 34 * s, hcy - 2 * s)], fill=255, width=int(8 * s))  # thumb
    hd.ellipse([hcx - 38 * s, hcy - 6 * s, hcx - 30 * s, hcy + 2 * s], fill=255)
    hd.rectangle([hcx - 11 * s, hcy + 30 * s, hcx + 11 * s, hcy + 64 * s], fill=255)  # wrist
    sprayed = Image.new("RGB", (Ws, Hs), (255, 255, 255))
    sd = ImageDraw.Draw(sprayed)
    # blown pigment: dense near the hand, thinning outward
    for _ in range(2600):
        a = rng.uniform(0, 2 * math.pi)
        d = abs(rng.gauss(0, 26 * s)) + 8 * s
        x, y = hcx + d * math.cos(a), hcy + 2 * s + d * math.sin(a) * 1.15
        r = rng.uniform(0.5, 1.2) * s
        sd.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    hand_inv = hand_mask.point(lambda v: 255 - v)
    spray_mask = Image.new("L", (Ws, Hs), 0)
    ImageDraw.Draw(spray_mask).ellipse([hcx - 60 * s, hcy - 62 * s, hcx + 60 * s, hcy + 70 * s], fill=255)
    both = Image.fromarray(np.minimum(np.array(hand_inv), np.array(spray_mask)))
    # only keep the red dots where mask says so
    red_only = np.array(sprayed)
    keep = (red_only[:, :, 1] < 128) & (np.array(both) > 128)
    base = np.array(img)
    base[keep] = RED
    img = Image.fromarray(base)
    dr = ImageDraw.Draw(img)

    # rows of red dots (the cave's mysterious signs)
    for i in range(6):
        x = 16 * s + i * 11 * s
        y = 264 * s + (i % 2) * 6 * s
        r = rng.uniform(2.5, 3.5) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    # a black quadrangular sign
    wobble_line(dr, [(88 * s, 257 * s), (122 * s, 257 * s), (122 * s, 277 * s), (88 * s, 277 * s)], 2 * s, BLACK, rng, amp=0.5 * s, closed=True)
    wobble_line(dr, [(105 * s, 257 * s), (105 * s, 277 * s)], 2 * s, BLACK, rng, amp=0.4 * s)
    wobble_line(dr, [(88 * s, 267 * s), (122 * s, 267 * s)], 2 * s, BLACK, rng, amp=0.4 * s)

    # caption
    f = font(FONT_SERIF_B, 12 * s)
    f2 = font(FONT_SERIF, 8 * s)
    dr.text((136 * s, 254 * s), "LASCAUX", font=f, fill=BLACK)
    dr.text((136 * s, 270 * s), "12 · IX · 1940 — 86 years since Robot the dog found the hole", font=f2, fill=BLACK)
    dr.text((136 * s, 281 * s), "ochre red, manganese black — the cave's own palette", font=f2, fill=BLACK)
    seal(img, s)
    return finalize(img, dither=True)


# ------------------------------------------------------------- 2. Two crescents
def crescent(dr, cx, cy, R, illum, lit_angle_deg, lit=WHITE, dark=None, steps=240):
    """Draw a lit crescent of a sphere: illuminated fraction `illum` (0..1),
    with the bright limb pointing toward lit_angle_deg (0 = right, 90 = down)."""
    # terminator is an ellipse of semi-minor axis R*|cos(phase)|
    # terminator ellipse: +1 (coincides with bright limb) at new, 0 at half, -1 (far limb) at full
    k = 1 - 2 * illum
    a = math.radians(lit_angle_deg)
    ux, uy = math.cos(a), math.sin(a)  # toward the sun
    vx, vy = -uy, ux
    pts = []
    # bright limb: half circle on the sun side
    for i in range(steps + 1):
        t = -math.pi / 2 + math.pi * i / steps
        px = R * math.cos(t)
        py = R * math.sin(t)
        pts.append((cx + px * ux + py * vx, cy + px * uy + py * vy))
    # terminator: back along the ellipse
    for i in range(steps + 1):
        t = math.pi / 2 - math.pi * i / steps
        px = R * k * math.cos(t)
        py = R * math.sin(t)
        pts.append((cx + px * ux + py * vx, cy + px * uy + py * vy))
    if dark is not None:
        dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=dark)
    dr.polygon(pts, fill=lit)


def image2_two_crescents():
    rng = random.Random(20260914)
    s = SS
    Ws, Hs = W * s, H * s
    img = Image.new("RGB", (Ws, Hs), BLACK)
    dr = ImageDraw.Draw(img)

    # faint stars
    for _ in range(140):
        x, y = rng.uniform(0, Ws), rng.uniform(0, Hs * 0.8)
        v = rng.choice([90, 120, 170, 255])
        r = rng.choice([0.6, 0.8, 1.2]) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # The Moon: 3.3 days old, ~12% lit, lit limb toward lower-right (evening, west)
    mcx, mcy, R = 150 * s, 140 * s, 96 * s
    # earthshine: the dark side is faintly visible
    dr.ellipse([mcx - R, mcy - R, mcx + R, mcy + R], fill=(34, 34, 34))
    # some faint maria on the earthshine side
    for (fx, fy, fr) in ((-0.25, -0.30, 0.22), (-0.05, -0.05, 0.18), (-0.35, 0.10, 0.16), (-0.10, 0.30, 0.14), (0.05, -0.40, 0.12)):
        dr.ellipse([mcx + fx * R - fr * R, mcy + fy * R - fr * R, mcx + fx * R + fr * R, mcy + fy * R + fr * R], fill=(20, 20, 20))
    crescent(dr, mcx, mcy, R, 0.12, 30, lit=(235, 235, 235))
    # a few craters on the lit limb as tiny dark specks
    for _ in range(30):
        t = rng.uniform(-1.1, 1.1)
        rr = R * rng.uniform(0.86, 0.99)
        a = math.radians(30) + t
        x, y = mcx + rr * math.cos(a), mcy + rr * math.sin(a)
        r = rng.uniform(0.6, 1.4) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(140, 140, 140))

    # Venus: a bright point just off the dark limb, about to be covered
    vx, vy = mcx - R * math.cos(math.radians(30)) - 9 * s, mcy - R * math.sin(math.radians(30)) - 9 * s
    for r, v in ((5.5, 60), (3.6, 150), (2.2, 255)):
        dr.ellipse([vx - r * s, vy - r * s, vx + r * s, vy + r * s], fill=(v, v, v))
    # red dotted "path" arrow showing the Moon's motion toward Venus
    for i in range(0, 60, 6):
        x = vx + (i + 24) * s * math.cos(math.radians(210 + 180))
        y = vy + (i + 24) * s * math.sin(math.radians(210 + 180))
    # inset: magnified Venus, a 25%-lit crescent, in a red ring
    icx, icy, iR = 318 * s, 105 * s, 52 * s
    dr.ellipse([icx - iR, icy - iR, icx + iR, icy + iR], fill=BLACK, outline=RED, width=2 * s)
    crescent(dr, icx, icy, iR * 0.62, 0.25, 30, lit=(255, 255, 255))
    # connector from Venus point to the inset
    dr.line([(vx + 8 * s, vy - 6 * s), (icx - iR * 0.75, icy + iR * 0.62)], fill=RED, width=1 * s)
    dr.ellipse([vx - 9 * s, vy - 9 * s, vx + 9 * s, vy + 9 * s], outline=RED, width=1 * s)

    # text
    fh = font(FONT_SERIF_B, 20 * s)
    fs = font(FONT_SANS, 9 * s)
    fm = font(FONT_MONO, 9 * s)
    dr.text((256 * s, 168 * s), "VENUS", font=font(FONT_SANS_B, 10 * s), fill=RED)
    dr.text((256 * s, 180 * s), "a 25%-lit crescent, 40″ wide", font=fs, fill=(200, 200, 200))
    dr.text((256 * s, 192 * s), "brightest of the year: 18 Sep", font=fs, fill=(200, 200, 200))
    dr.text((14 * s, 232 * s), "TWO CRESCENTS", font=fh, fill=WHITE)
    dr.text((14 * s, 258 * s), "Sun 14 Sep — the 3-day-old Moon passes in front of Venus.", font=fs, fill=(220, 220, 220))
    dr.text((14 * s, 270 * s), "Europe & Africa see it in daylight, ~09:26–13:42 UTC; SE Asia at dusk.", font=fs, fill=(220, 220, 220))
    dr.text((14 * s, 282 * s), "Both worlds are crescents tonight. One is 400× farther away.", font=fs, fill=RED)
    seal(img, s)
    return finalize(img, dither=True)


# ---------------------------------------------------------------- 3. Red wedge
def image3_proun():
    s = SS
    Ws, Hs = W * s, H * s
    img = Image.new("RGB", (Ws, Hs), WHITE)
    dr = ImageDraw.Draw(img)

    def rot(pts, cx, cy, deg):
        a = math.radians(deg)
        out = []
        for x, y in pts:
            dx, dy = x - cx, y - cy
            out.append((cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)))
        return out

    # black half-field: everything to the right of a diagonal is black
    ang = -28
    cx, cy = 250 * s, 150 * s
    field = rot([(cx, -400 * s), (cx + 900 * s, -400 * s), (cx + 900 * s, 900 * s), (cx, 900 * s)], cx, cy, ang)
    dr.polygon(field, fill=BLACK)

    # the white circle, sitting on the boundary, mostly in the black field
    ccx, ccy, cr = 294 * s, 114 * s, 88 * s
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=WHITE)

    # the red wedge, flying in from the lower-left, tip inside the circle
    tip = (ccx - 12 * s, ccy + 20 * s)
    base_c = (-40 * s, 300 * s)
    wedge_dir = math.atan2(tip[1] - base_c[1], tip[0] - base_c[0])
    half = 52 * s
    nx, ny = -math.sin(wedge_dir), math.cos(wedge_dir)
    wedge = [tip, (base_c[0] + nx * half, base_c[1] + ny * half), (base_c[0] - nx * half, base_c[1] - ny * half)]
    dr.polygon(wedge, fill=RED)

    # thin black ray lines parallel to the wedge, on the white side
    for off in (-70, -96, 118, 140):
        p0 = (base_c[0] + nx * off * s, base_c[1] + ny * off * s)
        L = 520 * s
        p1 = (p0[0] + math.cos(wedge_dir) * L, p0[1] + math.sin(wedge_dir) * L)
        dr.line([p0, p1], fill=BLACK, width=int(1.5 * s))

    # small projectiles: red and black rectangles/triangles, scattered along the axis
    pieces = [
        ((60, 60), 22, 8, 25, RED), ((110, 40), 10, 10, 25, BLACK), ((30, 150), 30, 5, 25, BLACK),
        ((120, 230), 16, 16, 25, RED), ((200, 250), 46, 6, -62, BLACK), ((372, 272), 16, 16, 25, WHITE),
        ((360, 44), 8, 30, -62, WHITE), ((300, 260), 12, 4, 25, RED), ((150, 92), 6, 6, 25, BLACK),
        ((385, 150), 4, 60, -62, RED),
    ]
    for (px, py), w_, h_, deg, col in pieces:
        px, py = px * s, py * s
        rect = [(px - w_ * s / 2, py - h_ * s / 2), (px + w_ * s / 2, py - h_ * s / 2), (px + w_ * s / 2, py + h_ * s / 2), (px - w_ * s / 2, py + h_ * s / 2)]
        dr.polygon(rot(rect, px, py, deg), fill=col)
    # small black triangles inside the white circle, echoing the wedge
    for (px, py, sz) in ((326, 88, 11), (346, 112, 6), (312, 58, 4)):
        tri = [(px * s, py * s), (px * s - sz * s * 2.2, py * s + sz * s * 0.9), (px * s - sz * s * 2.2, py * s - sz * s * 0.9)]
        dr.polygon(rot(tri, px * s, py * s, -25), fill=BLACK)

    # rotated typography along the axis
    def rotated_text(txt, fnt, fill, anchor_xy, deg):
        tw, th = dr.textbbox((0, 0), txt, font=fnt)[2:]
        layer = Image.new("RGBA", (tw + 8 * s, th + 8 * s), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((4 * s, 4 * s), txt, font=fnt, fill=fill + (255,))
        layer = layer.rotate(deg, expand=True, resample=Image.BICUBIC)
        img.paste(layer, (int(anchor_xy[0] - layer.width / 2), int(anchor_xy[1] - layer.height / 2)), layer)

    rotated_text("PROUN", font(FONT_COND, 30 * s), BLACK, (86 * s, 236 * s), 25)
    rotated_text("12 · IX · 26", font(FONT_COND, 13 * s), BLACK, (128 * s, 268 * s), 25)
    rotated_text("красным клином", font(FONT_COND, 10 * s), WHITE, (350 * s, 234 * s), 25)
    seal(img, s, corner="tl")
    return finalize(img, dither=False)


# --------------------------------------------------------------- 4. Wagtails sing
def image4_wagtail():
    rng = random.Random(44)
    s = SS
    Ws, Hs = W * s, H * s
    img = Image.new("RGB", (Ws, Hs), WHITE)
    dr = ImageDraw.Draw(img)

    # a river stone: a low, flat, dithered grey boulder
    stone = [(40, 250), (60, 214), (110, 196), (180, 192), (250, 200), (300, 216), (322, 246), (300, 268), (60, 268)]
    stone_pts = catmull_rom([(x * s, y * s) for x, y in stone], closed=True, steps=10)
    dr.polygon(stone_pts, fill=(150, 150, 150))
    # darker underside gradient via bands
    for i in range(6):
        y0 = (238 + i * 5) * s
        band = Image.new("L", (Ws, Hs), 0)
        ImageDraw.Draw(band).polygon(stone_pts, fill=255)
        arr = np.array(band)
        arr[: int(y0), :] = 0
        img.paste(Image.new("RGB", (Ws, Hs), (150 - i * 14,) * 3), (0, 0), Image.fromarray(arr))
    dr = ImageDraw.Draw(img)
    # water line below the stone: a few thin ripples
    for i, y in enumerate((276, 282, 289)):
        x0 = (20 + i * 30) * s
        x1 = (380 - i * 40) * s
        dr.line([(x0, y * s), (x1, y * s)], fill=BLACK, width=1 * s)

    # The white wagtail (ハクセキレイ): standing on the stone, facing left, tail cocked up.
    # Body
    bcx, bcy = 190 * s, 172 * s
    body = catmull_rom([(bcx - 46 * s, bcy - 2 * s), (bcx - 30 * s, bcy - 22 * s), (bcx + 4 * s, bcy - 26 * s), (bcx + 40 * s, bcy - 14 * s), (bcx + 52 * s, bcy + 2 * s), (bcx + 30 * s, bcy + 20 * s), (bcx - 10 * s, bcy + 24 * s), (bcx - 40 * s, bcy + 14 * s)], closed=True, steps=10)
    dr.polygon(body, fill=WHITE, outline=BLACK, width=2 * s)
    # grey/black back and wing (black on this screen)
    wing = catmull_rom([(bcx - 22 * s, bcy - 20 * s), (bcx + 6 * s, bcy - 25 * s), (bcx + 40 * s, bcy - 12 * s), (bcx + 62 * s, bcy + 4 * s), (bcx + 36 * s, bcy + 4 * s), (bcx + 8 * s, bcy - 2 * s), (bcx - 16 * s, bcy - 8 * s)], closed=True, steps=10)
    dr.polygon(wing, fill=BLACK)
    # white wing bar
    dr.line([(bcx - 4 * s, bcy - 13 * s), (bcx + 34 * s, bcy - 4 * s)], fill=WHITE, width=3 * s)
    # long tail, angled up-right (wagging)
    tail = [(bcx + 44 * s, bcy - 6 * s), (bcx + 118 * s, bcy - 44 * s), (bcx + 124 * s, bcy - 34 * s), (bcx + 56 * s, bcy + 6 * s)]
    dr.polygon(tail, fill=BLACK)
    dr.line([(bcx + 50 * s, bcy + 2 * s), (bcx + 121 * s, bcy - 36 * s)], fill=WHITE, width=2 * s)  # white outer tail feather
    # head
    hcx, hcy = bcx - 50 * s, bcy - 18 * s
    dr.ellipse([hcx - 18 * s, hcy - 16 * s, hcx + 18 * s, hcy + 16 * s], fill=WHITE, outline=BLACK, width=2 * s)
    # black cap and nape
    cap = catmull_rom([(hcx - 8 * s, hcy - 16 * s), (hcx + 10 * s, hcy - 16 * s), (hcx + 18 * s, hcy - 4 * s), (hcx + 16 * s, hcy + 8 * s), (hcx + 4 * s, hcy - 6 * s), (hcx - 6 * s, hcy - 12 * s)], closed=True, steps=8)
    dr.polygon(cap, fill=BLACK)
    # black eye-stripe and black bib
    dr.line([(hcx - 16 * s, hcy - 2 * s), (hcx + 8 * s, hcy - 4 * s)], fill=BLACK, width=int(2.5 * s))
    dr.ellipse([hcx - 6 * s, hcy - 5 * s, hcx - 1 * s, hcy], fill=WHITE)
    bib = catmull_rom([(hcx - 6 * s, hcy + 10 * s), (hcx + 12 * s, hcy + 8 * s), (hcx + 26 * s, hcy + 16 * s), (hcx + 16 * s, hcy + 30 * s), (hcx - 2 * s, hcy + 22 * s)], closed=True, steps=8)
    dr.polygon(bib, fill=BLACK)
    # beak
    dr.polygon([(hcx - 17 * s, hcy - 3 * s), (hcx - 32 * s, hcy + 1 * s), (hcx - 17 * s, hcy + 4 * s)], fill=BLACK)
    # legs: thin, standing on the stone
    for lx in (bcx - 14 * s, bcx + 6 * s):
        dr.line([(lx, bcy + 22 * s), (lx + 4 * s, bcy + 34 * s)], fill=BLACK, width=2 * s)
        dr.line([(lx + 4 * s, bcy + 34 * s), (lx + 8 * s, bcy + 40 * s)], fill=BLACK, width=2 * s)
        for tx in (-8, 0, 8):
            dr.line([(lx + 8 * s, bcy + 40 * s), (lx + 8 * s + tx * s, bcy + 45 * s)], fill=BLACK, width=int(1.5 * s))

    # tail-wag motion marks: three short red arcs behind the tail
    for i, r in enumerate((16, 24, 32)):
        cx_, cy_ = bcx + 110 * s, bcy - 30 * s
        dr.arc([cx_ - r * s, cy_ - r * s, cx_ + r * s, cy_ + r * s], start=250, end=330, fill=RED, width=int(1.6 * s))

    # dew drops on the stone: small white circles with black rim
    for _ in range(9):
        x = rng.uniform(70, 300) * s
        y = rng.uniform(206, 240) * s
        r = rng.uniform(2, 3.5) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=WHITE, outline=BLACK, width=1 * s)

    # vertical Japanese title, top-left, big
    fj = font(FONT_JP, 40 * s)
    for i, ch in enumerate("鶺鴒鳴"):
        dr.text((22 * s, (18 + i * 44) * s), ch, font=fj, fill=BLACK)
    # small english
    fs = font(FONT_SERIF, 10 * s)
    fsb = font(FONT_SERIF_B, 11 * s)
    dr.text((80 * s, 24 * s), "sekirei naku", font=fsb, fill=BLACK)
    dr.text((80 * s, 38 * s), "wagtails sing", font=fs, fill=BLACK)
    dr.text((80 * s, 60 * s), "44th of the 72 microseasons", font=fs, fill=BLACK)
    dr.text((80 * s, 73 * s), "13 – 17 September · 白露 White Dew", font=font(FONT_JP, 10 * s), fill=BLACK)
    # red hanko seal, top right
    sx, sy = 344 * s, 22 * s
    dr.rectangle([sx, sy, sx + 40 * s, sy + 40 * s], fill=RED)
    fh = font(FONT_JP, 17 * s)
    dr.text((sx + 3 * s, sy + 2 * s), "白", font=fh, fill=WHITE)
    dr.text((sx + 21 * s, sy + 2 * s), "露", font=fh, fill=WHITE)
    dr.text((sx + 3 * s, sy + 21 * s), "四", font=fh, fill=WHITE)
    dr.text((sx + 21 * s, sy + 21 * s), "四", font=fh, fill=WHITE)
    seal(img, s)
    return finalize(img, dither=True)


# ---------------------------------------------------------- 5. Typewriter butterfly
def image5_typewriter():
    rng = random.Random(1873)
    s = 1  # typed at 1x with aliased glyphs: crisp, like real typewriter impressions
    Ws, Hs = W * s, H * s

    # 1) Draw the butterfly as a tone map: 0 paper, 1 light, 2 mid, 3 dark, 4 red
    cols, rows = 55, 21
    cw, ch = W / cols, 12.0  # cell size in 1x pixels; 21 rows * 12 = 252
    tone = Image.new("L", (cols * 4, rows * 4), 0)  # 4 samples per cell
    td = ImageDraw.Draw(tone)
    K = 4
    ccx, ccy = cols * K / 2, rows * K / 2 - 1 * K  # center in tone px

    def wing(sign):
        # forewing: a rounded triangle sweeping up and out; hindwing: a lobe below.
        fw = [(0, -1), (5 * sign, -8), (13 * sign, -10), (21 * sign, -8), (23 * sign, -4), (18 * sign, 0), (9 * sign, 1)]
        hw = [(0, 1), (6 * sign, 0), (14 * sign, 2), (18 * sign, 5), (12 * sign, 9), (5 * sign, 8), (1 * sign, 5)]
        sx_, sy_ = 1.18, 1.0
        fwp = catmull_rom([(ccx + x * sx_ * K, ccy + y * sy_ * K) for x, y in fw], closed=True, steps=8)
        hwp = catmull_rom([(ccx + x * sx_ * K, ccy + y * sy_ * K) for x, y in hw], closed=True, steps=8)
        for poly in (fwp, hwp):
            td.polygon(poly, fill=3)  # dark border
        # inner lighter field: shrink polygons toward their centroid
        for poly in (fwp, hwp):
            mx = sum(p[0] for p in poly) / len(poly)
            my = sum(p[1] for p in poly) / len(poly)
            inner = [(mx + (x - mx) * 0.86, my + (y - my) * 0.82) for x, y in poly]
            td.polygon(inner, fill=1)
        # veins: dark lines radiating from the body
        for (x, y) in fw[1:6]:
            td.line([(ccx, ccy - 1 * K), (ccx + x * sx_ * K * 0.92, ccy + y * sy_ * K * 0.92)], fill=2, width=2)
        for (x, y) in hw[1:5]:
            td.line([(ccx, ccy + 1 * K), (ccx + x * sx_ * K * 0.92, ccy + y * sy_ * K * 0.92)], fill=2, width=2)
        # eyespots in red
        for (x, y, r) in ((14 * sign, -6, 2.0), (11 * sign, 5, 1.6)):
            td.ellipse([ccx + x * sx_ * K - r * K, ccy + y * sy_ * K - r * K, ccx + x * sx_ * K + r * K, ccy + y * sy_ * K + r * K], fill=4)

    wing(-1)
    wing(1)
    # body: dark vertical bar; antennae: light lines
    td.rectangle([ccx - 0.9 * K, ccy - 6 * K, ccx + 0.9 * K, ccy + 7 * K], fill=3)
    td.ellipse([ccx - 1.4 * K, ccy - 8 * K, ccx + 1.4 * K, ccy - 5.5 * K], fill=3)
    for sign in (-1, 1):
        td.line([(ccx, ccy - 7 * K), (ccx + sign * 6 * K, ccy - 11.5 * K)], fill=2, width=2)
        td.ellipse([ccx + sign * 6 * K - 0.6 * K, ccy - 12.1 * K, ccx + sign * 6 * K + 0.6 * K, ccy - 10.9 * K], fill=3)

    tone_arr = np.array(tone)

    # 2) Type it. Each cell gets a character chosen by its dominant tone.
    img = Image.new("RGB", (Ws, Hs), WHITE)
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    fm = font(FONT_MONO, int(12 * s))
    fmb = font(FONT_MONO_B, int(12 * s))
    chars = {
        1: list("==:=+="),
        2: list("##%#"),
        3: list("MWMW"),
        4: list("O0@*"),
    }
    ink = BLACK
    for r in range(rows):
        for c in range(cols):
            block = tone_arr[r * K:(r + 1) * K, c * K:(c + 1) * K]
            if block.max() == 0:
                continue
            counts = np.bincount(block.flatten(), minlength=5)
            counts[0] = 0
            if counts[4] >= 4:
                t = 4
            else:
                t = int(np.argmax(counts[1:4])) + 1
            ch_ = rng.choice(chars[t])
            x = round(c * cw * s + rng.choice((0, 0, 0, -1, 1)))
            y = round(6 * s + r * ch * s + rng.choice((0, 0, 0, -1, 1)))
            col = RED if t == 4 else ink
            f_ = fmb
            dr.text((x, y), ch_, font=f_, fill=col)
            if t == 3:
                # overstrike, as typists did for darker tone
                dr.text((x + 1, y), rng.choice("MW#"), font=fmb, fill=ink)
            elif t == 4:
                dr.text((x + 1, y), "*", font=fmb, fill=RED)

    # 3) The typed caption in the lower margin, with a red-ribbon line
    y = 6 * s + rows * ch * s - 6 * s
    cap1 = "PAPILIO MACHINALIS  ·  typed, not drawn"
    cap2 = "Sholes' typewriter, 12 Sep 1873 · Flora Stacey's butterfly, 1898"
    fcap = font(FONT_MONO_B, 9 * s)
    dr.text((10 * s, 266 * s), cap1, font=font(FONT_MONO_B, 11 * s), fill=RED)
    dr.text((10 * s, 282 * s), cap2, font=fcap, fill=ink)
    # faint ribbon-worn texture: erase a sprinkle of pixels so the ink looks typed
    arr = np.array(img)
    nz = np.random.default_rng(1873)
    holes = nz.random(arr.shape[:2]) < 0.06
    dark = arr[:, :, 0] < 100
    arr[holes & dark] = (255, 255, 255)
    img = Image.fromarray(arr)
    seal(img, s, corner="tr")
    return finalize(img, dither=False)


def main():
    makers = [image1_lascaux, image2_two_crescents, image3_proun, image4_wagtail, image5_typewriter]
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else range(1, 6)
    for i, mk in enumerate(makers, start=1):
        if i not in only:
            continue
        im = mk()
        assert im.size == (W, H)
        for d in OUT_DIRS:
            os.makedirs(d, exist_ok=True)
            im.save(os.path.join(d, f"{i}.png"), optimize=True)
        print("wrote", i, mk.__name__)


if __name__ == "__main__":
    main()
