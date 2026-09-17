#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-17.

Five 400x300 images in exactly three colors (white, black, red).

Today's threads: Mimas was discovered on this day in 1789 (Herschel);
the September equinox is six days away; tonight's waxing crescent Moon sits
beside Antares in the west; red spider lilies (higanbana) are blooming for
Higan; and two black/white/red design traditions I wanted to try — Lissitzky's
constructivism and Anni Albers' Bauhaus weaving drafts.

Techniques new today (vs. day 1):
  * line-screen "engraving" shading instead of Floyd–Steinberg (Mimas)
  * hard-edged 3x render + threshold quantize for crisp posters (Lissitzky, kamon)
  * an honest 4-shaft weaving draft with drawdown (Albers)
"""

import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"

DATE_MARK = "17·IX·26"


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


def signature(img, s=1, color=BLACK, where="br"):
    """My mark: a tiny red square and the date, in a corner."""
    dr = ImageDraw.Draw(img)
    f = font(F_MONO, 8 * s)
    tw = dr.textlength(DATE_MARK, font=f)
    if where == "br":
        x, y = W * s - tw - 6 * s, H * s - 13 * s
    else:
        x, y = 6 * s + 8 * s, H * s - 13 * s
    dr.rectangle([x - 8 * s, y + 2 * s, x - 4 * s, y + 6 * s], fill=RED)
    dr.text((x, y), DATE_MARK, font=f, fill=color)


def rotated_text(base, text, fnt, angle, center, fill):
    """Draw text rotated by `angle` degrees, centred at `center`."""
    tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
    bbox = tmp.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0] + 4, bbox[3] - bbox[1] + 4
    layer = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(layer).text((2 - bbox[0], 2 - bbox[1]), text, font=fnt, fill=255)
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    colour = Image.new("RGB", layer.size, fill)
    base.paste(colour, (int(center[0] - layer.width / 2), int(center[1] - layer.height / 2)), layer)


# ------------------------------------------------------------------ 1. Mimas
def image1_mimas():
    """Engraving-style plate of Mimas and the Herschel crater, line-screen shaded."""
    rng = random.Random(17891709)
    s = SS
    cx, cy, R = 150 * s, 150 * s, 108 * s

    # heightfield over the sphere disk (in supersampled pixel units)
    ys, xs = np.mgrid[0:H * s, 0:W * s].astype(np.float64)
    dx, dy = xs - cx, ys - cy
    rr = np.sqrt(dx * dx + dy * dy)
    inside = rr < R
    z = np.zeros_like(rr)
    z[inside] = np.sqrt(np.clip(R * R - rr[inside] ** 2, 0, None))

    def crater(ccx, ccy, cr, depth, rim, peak):
        d = np.sqrt((xs - ccx) ** 2 + (ys - ccy) ** 2) / cr
        bowl = np.where(d < 1, -depth * np.clip(1 - d * d, 0, None) ** 1.4, 0)
        ring = rim * np.exp(-((d - 1.0) / 0.10) ** 2)
        pk = peak * np.exp(-((d) / 0.16) ** 2) if peak else 0
        return bowl + ring + pk

    # Herschel: 130 km on a 398 km moon => crater radius ≈ 1/3 of the moon radius
    hx, hy = cx - 0.30 * R, cy - 0.12 * R
    z += crater(hx, hy, R * 0.33, 22 * s, 6 * s, 14 * s)
    # a scatter of small craters (Mimas is heavily cratered)
    for _ in range(90):
        ang = rng.uniform(0, 2 * math.pi)
        rad = math.sqrt(rng.random()) * R * 0.93
        px, py = cx + rad * math.cos(ang), cy + rad * math.sin(ang)
        if math.hypot(px - hx, py - hy) < R * 0.36:
            continue
        cr = rng.uniform(2.5, 8) * s
        z += crater(px, py, cr, cr * 0.5, cr * 0.15, 0)
    z[~inside] = 0

    # normals from gradient, lambert light from upper-left, plus a little ambient
    gy, gx = np.gradient(z)
    nx, ny, nz = -gx, -gy, np.ones_like(z)
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    nx, ny, nz = nx / n, ny / n, nz / n
    L = np.array([-0.55, -0.45, 0.70])
    L /= np.linalg.norm(L)
    lam = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    bright = 0.10 + 0.90 * lam
    bright[~inside] = 1.0

    # downscale brightness to 1x
    bimg = Image.fromarray((bright * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    b = np.asarray(bimg).astype(np.float64) / 255.0
    mask = np.asarray(Image.fromarray((inside * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)) > 127

    # line screen: hatch density follows darkness; second, steeper hatch for deep shadow
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    period = 4.0
    h1 = ((xx * 0.30 + yy * 0.95) / period) % 1.0
    h2 = ((xx * 0.95 - yy * 0.30) / period) % 1.0
    dark = 1 - b
    ink = (h1 < dark * 1.15) | ((dark > 0.45) & (h2 < (dark - 0.45) * 1.6))
    ink &= mask

    img = Image.new("RGB", (W, H), WHITE)
    px = np.array(img)
    px[ink] = BLACK
    img = Image.fromarray(px)
    dr = ImageDraw.Draw(img)

    # limb outline
    dr.ellipse([cx / s - R / s, cy / s - R / s, cx / s + R / s, cy / s + R / s], outline=BLACK, width=1)

    # dimension lines (plate style)
    fm = font(F_MONO, 9)
    fi = font(F_SERIF_I, 11)
    x0, x1, yd = cx / s - R / s, cx / s + R / s, cy / s + R / s + 14
    dr.line([x0, yd, x1, yd], fill=BLACK, width=1)
    for x in (x0, x1):
        dr.line([x, yd - 4, x, yd + 4], fill=BLACK)
        dr.line([x, cy / s + R / s, x, yd - 6], fill=BLACK)
    dr.text((cx / s - 22, yd + 3), "398 km", font=fm, fill=BLACK)

    # Herschel crater callout in red
    hr = R * 0.33 / s
    hcx, hcy = hx / s, hy / s
    dr.ellipse([hcx - hr, hcy - hr, hcx + hr, hcy + hr], outline=RED, width=1)
    dr.line([hcx + hr * 0.7, hcy - hr * 0.7, 290, 44], fill=RED, width=1)
    dr.line([290, 44, 318, 44], fill=RED, width=1)
    dr.text((322, 38), "Herschel", font=font(F_SERIF_B, 11), fill=RED)
    dr.text((322, 52), "130 km wide", font=fm, fill=BLACK)
    dr.text((322, 63), "10 km deep", font=fm, fill=BLACK)
    dr.text((322, 74), "6 km peak", font=fm, fill=BLACK)

    # title block
    dr.text((268, 118), "MIMAS", font=font(F_SERIF_B, 26), fill=BLACK)
    dr.text((268, 148), "Saturn I", font=fi, fill=BLACK)
    dr.line([268, 166, 392, 166], fill=BLACK)
    lines = [
        "Discovered 17 Sept 1789",
        "by William Herschel,",
        "40-foot reflector, Slough.",
        "",
        "The Death Star moon:",
        "an impact almost a third",
        "of its own width.",
    ]
    for i, t in enumerate(lines):
        dr.text((268, 172 + i * 12), t, font=font(F_SERIF, 9), fill=BLACK)
    dr.text((268, 266), "Fig. 1 — line-screen engraving", font=fi, fill=BLACK)
    signature(img, 1, BLACK, "br")
    return finalize(img, dither=False)


# ----------------------------------------------------- 2. Constructivist equinox
def image2_equinox():
    """Lissitzky homage: a red wedge splits day from night. Equinox in six days."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # night: a black field on the right, cut on a diagonal
    dr.polygon([(W * s * 0.42, 0), (W * s, 0), (W * s, H * s), (W * s * 0.62, H * s)], fill=BLACK)
    # the disk: half in day, half in night — inverted on each side
    ccx, ccy, cr = 236 * s, 142 * s, 92 * s
    disk = Image.new("L", (W * s, H * s), 0)
    ImageDraw.Draw(disk).ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=255)
    inv = Image.eval(img.convert("L"), lambda v: 255 - v).convert("RGB")
    img.paste(inv, (0, 0), disk)
    dr = ImageDraw.Draw(img)
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=RED, width=2 * s)

    # the red wedge, from the lower left, its tip at the disk's centre
    tip = (ccx - 4 * s, ccy + 2 * s)
    dr.polygon([tip, (-10 * s, H * s * 0.98), (-10 * s, H * s * 0.66)], fill=RED)
    # a hairline crack from the tip
    pts = [tip]
    x, y = tip
    for i in range(7):
        x += (12 + (i % 3) * 5) * s
        y += (9 - (i % 2) * 16) * s
        pts.append((x, y))
    dr.line(pts, fill=WHITE if False else BLACK, width=1 * s)

    # small projectiles
    dr.rectangle([48 * s, 58 * s, 66 * s, 76 * s], fill=BLACK)
    dr.rectangle([80 * s, 30 * s, 86 * s, 36 * s], fill=BLACK)
    dr.ellipse([204 * s, 262 * s, 216 * s, 274 * s], fill=BLACK)
    dr.rectangle([330 * s, 236 * s, 372 * s, 244 * s], fill=WHITE)
    dr.rectangle([352 * s, 250 * s, 358 * s, 256 * s], fill=RED)
    dr.polygon([(300 * s, 22 * s), (346 * s, 22 * s), (300 * s, 34 * s)], fill=WHITE)
    dr.ellipse([354 * s, 58 * s, 366 * s, 70 * s], fill=RED)

    # text on the diagonal
    fb = font(F_SANS_B, 15 * s)
    rotated_text(img, "РАВНОДЕНСТВИЕ", font(F_SANS_B, 13 * s), 28, (120 * s, 255 * s), BLACK)
    rotated_text(img, "EQUINOX", font(F_SANS_B, 26 * s), 28, (112 * s, 106 * s), RED)
    rotated_text(img, "DAY = NIGHT", font(F_SANS_B, 12 * s), -58, (352 * s, 160 * s), WHITE)
    dr.text((14 * s, 12 * s), "23·IX·2026", font=font(F_SANS_B, 14 * s), fill=BLACK)
    dr.text((14 * s, 30 * s), "00:05 UTC", font=font(F_SANS, 10 * s), fill=BLACK)
    dr.text((262 * s, 262 * s), "in six days the sun", font=font(F_SANS, 9 * s), fill=WHITE)
    dr.text((262 * s, 274 * s), "crosses the equator", font=font(F_SANS, 9 * s), fill=WHITE)
    signature(img, s, BLACK, "bl")
    return finalize(img, dither=False)


# ------------------------------------------------------------ 3. Higanbana
def image3_higanbana():
    """Tonight: waxing crescent (34%) beside Antares, over a field of red spider lilies."""
    rng = random.Random(20260917)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # dusk gradient sky: dark at top, pale at the horizon
    horizon = 205 * s
    sky = np.zeros((H * s, W * s), dtype=np.uint8)
    for y in range(horizon):
        t = y / horizon
        v = int(30 + 225 * (t ** 1.6))
        sky[y, :] = v
    img.paste(Image.fromarray(sky).convert("RGB"), (0, 0))
    dr = ImageDraw.Draw(img)

    # moon: 34% waxing crescent, lit on the right (evening, western sky)
    mx, my, mr = 300 * s, 60 * s, 26 * s
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=WHITE)
    # the shadowed part: an ellipse whose width follows the phase
    k = 1 - 2 * 0.34  # terminator ellipse semi-axis ratio (0.32)
    dark = Image.new("L", (W * s, H * s), 0)
    dd = ImageDraw.Draw(dark)
    dd.pieslice([mx - mr, my - mr, mx + mr, my + mr], 90, 270, fill=255)
    dd.ellipse([mx - mr * k, my - mr, mx + mr * k, my + mr], fill=255)
    skycol = Image.new("RGB", (W * s, H * s), (34, 34, 34))
    img.paste(skycol, (0, 0), dark)
    dr = ImageDraw.Draw(img)

    # Antares, red, a little to the lower-left of the moon tonight
    ax, ay = mx - 62 * s, my + 30 * s
    for r, c in ((5 * s, RED), (2 * s, WHITE)):
        dr.ellipse([ax - r, ay - r, ax + r, ay + r], fill=c)
    dr.line([ax - 11 * s, ay, ax + 11 * s, ay], fill=RED, width=s)
    dr.line([ax, ay - 11 * s, ax, ay + 11 * s], fill=RED, width=s)
    # a few faint stars of Scorpius
    for _ in range(26):
        x, y = rng.uniform(0, W * s), rng.uniform(0, 120 * s)
        r = rng.uniform(0.8, 1.8) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(200, 200, 200))

    # ground
    dr.rectangle([0, horizon, W * s, H * s], fill=BLACK)

    def lily(x, y, size, front):
        """One higanbana umbel: 6 florets, each with recurved petals and long stamens."""
        col = RED
        # stem: black against the sky, white against the ground (woodcut logic)
        x2 = x + rng.uniform(-3, 3) * s
        yb = y + size * 0.3
        if yb < horizon:
            xh = x + (x2 - x) * (horizon - yb) / (H * s + 4 * s - yb)
            dr.line([x, yb, xh, horizon], fill=BLACK, width=3)
            dr.line([xh, horizon, x2, H * s + 4 * s], fill=WHITE, width=3)
        else:
            dr.line([x, yb, x2, H * s + 4 * s], fill=WHITE, width=3)
        # stamens: long thin arcs fanning up and out
        for i in range(18):
            a = math.radians(rng.uniform(-150, -30))
            L = size * rng.uniform(1.5, 2.3)
            pts = []
            for t in np.linspace(0, 1, 8):
                px = x + math.cos(a) * L * t + math.sin(a) * size * 0.35 * (t * t)
                py = y + math.sin(a) * L * t - size * 0.25 * (t * t)
                pts.append((px, py))
            dr.line(pts, fill=col, width=max(1, int(0.9 * s)))
            tx, ty = pts[-1]
            dr.ellipse([tx - s, ty - s, tx + s, ty + s], fill=col)
        # petals: strongly recurved narrow strokes with wavy edges
        for i in range(6):
            base = math.radians(-180 + i * 36 + rng.uniform(-8, 8))
            pts = []
            for t in np.linspace(0, 1, 10):
                curl = math.sin(t * math.pi) * size * 0.35
                px = x + math.cos(base) * size * t * 1.1 + math.sin(base) * curl
                py = y + math.sin(base) * size * t * 1.1 - math.cos(base) * curl * 0.6 + size * 0.15 * t
                pts.append((px, py))
            wdt = max(1, int(size * 0.12))
            dr.line(pts, fill=col, width=wdt)
            dr.line(pts[:5], fill=col, width=wdt + int(0.08 * size))
        dr.ellipse([x - size * 0.12, y - size * 0.12, x + size * 0.12, y + size * 0.12], fill=col)

    # rows: far, small; near, large (drawn later so they overlap)
    flowers = []
    for _ in range(11):
        flowers.append((rng.uniform(10, 390) * s, rng.uniform(178, 196) * s, rng.uniform(7, 10) * s))
    for _ in range(9):
        flowers.append((rng.uniform(0, 400) * s, rng.uniform(196, 232) * s, rng.uniform(12, 17) * s))
    for _ in range(5):
        flowers.append((rng.uniform(10, 390) * s, rng.uniform(232, 262) * s, rng.uniform(19, 25) * s))
    flowers.sort(key=lambda f: f[1])
    for x, y, size in flowers:
        lily(x, y, size, True)

    # kanji, vertical, top-left: 彼岸花
    fj = font(F_JP, 30 * s)
    for i, ch in enumerate("彼岸花"):
        dr.text((14 * s, 12 * s + i * 34 * s), ch, font=fj, fill=WHITE)
    fs = font(F_SANS, 9 * s)
    dr.text((50 * s, 14 * s), "higanbana — the flower of the other shore", font=fs, fill=WHITE)
    dr.text((50 * s, 26 * s), "blooms for Higan; the leaves come only after", font=fs, fill=WHITE)
    dr.text((mx - 30 * s, my + mr + 6 * s), "moon 34%", font=fs, fill=WHITE)
    dr.text((ax - 20 * s, ay + 10 * s), "Antares", font=fs, fill=RED)
    signature(img, s, WHITE, "br")
    return finalize(img, dither=True)


# ------------------------------------------------------------ 4. Kamon sheet
def image4_kamon():
    """A catalogue page of generated crests, each built from circles and lines only."""
    rng = random.Random(1789 + 917)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    def ring(cx, cy, r, w, col):
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=int(w))

    def disc(cx, cy, r, col):
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    def polar(cx, cy, r, a):
        return cx + r * math.cos(a), cy + r * math.sin(a)

    def crest(cx, cy, R, col, n, kind, enclosure):
        # enclosure
        if enclosure == "maru":
            ring(cx, cy, R, R * 0.09, col)
        elif enclosure == "hoso":
            ring(cx, cy, R, R * 0.04, col)
        elif enclosure == "yuki":  # snow ring: dots on the ring
            ring(cx, cy, R, R * 0.05, col)
            for i in range(n * 4):
                a = 2 * math.pi * i / (n * 4)
                px, py = polar(cx, cy, R, a)
                disc(px, py, R * 0.06, col)
        inner = R * 0.72
        rot = -math.pi / 2
        if kind == "hanabishi":  # flower diamond: n lozenges around the centre
            for i in range(n):
                a = rot + 2 * math.pi * i / n
                p0 = polar(cx, cy, inner * 0.18, a)
                p1 = polar(cx, cy, inner * 0.55, a + 0.42)
                p2 = polar(cx, cy, inner * 0.95, a)
                p3 = polar(cx, cy, inner * 0.55, a - 0.42)
                dr.polygon([p0, p1, p2, p3], fill=col)
        elif kind == "hoshi":  # stars: n discs on a ring plus one in the middle
            for i in range(n):
                px, py = polar(cx, cy, inner * 0.62, rot + 2 * math.pi * i / n)
                disc(px, py, inner * 0.30, col)
            disc(cx, cy, inner * 0.30, col)
        elif kind == "tomoe":  # comma shapes: circles minus offset circles
            big = inner * 0.98
            disc(cx, cy, big, col)
            for i in range(n):
                a = rot + 2 * math.pi * i / n
                px, py = polar(cx, cy, big * 0.5, a)
                disc(px, py, big * 0.5, WHITE)
                px2, py2 = polar(cx, cy, big * 0.5, a + 2 * math.pi / n * 0.5)
            for i in range(n):
                a = rot + 2 * math.pi * i / n
                px, py = polar(cx, cy, big * 0.5, a)
                disc(px, py, big * 0.28, col)
        elif kind == "kikyo":  # bellflower: petals as pointed leaves from circles
            for i in range(n):
                a = rot + 2 * math.pi * i / n
                px, py = polar(cx, cy, inner * 0.52, a)
                disc(px, py, inner * 0.40, col)
                tip = polar(cx, cy, inner * 1.0, a)
                l = polar(px, py, inner * 0.40, a + math.pi / 2)
                r_ = polar(px, py, inner * 0.40, a - math.pi / 2)
                dr.polygon([l, tip, r_], fill=col)
            for i in range(n):  # white veins
                a = rot + 2 * math.pi * i / n
                dr.line([polar(cx, cy, inner * 0.2, a), polar(cx, cy, inner * 0.9, a)], fill=WHITE, width=int(R * 0.05))
            disc(cx, cy, inner * 0.16, col)
        elif kind == "wachigai":  # interlocking rings
            for i in range(n):
                px, py = polar(cx, cy, inner * 0.42, rot + 2 * math.pi * i / n)
                ring(px, py, inner * 0.52, R * 0.08, col)
        elif kind == "hishi":  # nested lozenges
            for k, w in ((1.0, 0.09), (0.66, 0.07)):
                pts = [polar(cx, cy, inner * k, rot + i * math.pi / 2) for i in range(4)]
                pts = [(cx + (p[0] - cx) * 1.25, cy + (p[1] - cy) * 0.8) for p in pts]
                dr.polygon(pts, outline=col, width=int(R * w))
            disc(cx, cy, inner * 0.16, col)
        elif kind == "kiri":  # sun rays: n wedges of alternating length
            for i in range(2 * n):
                a = rot + math.pi * i / n
                Lr = inner * (0.98 if i % 2 == 0 else 0.72)
                w = 0.09
                p0 = polar(cx, cy, inner * 0.28, a - w)
                p1 = polar(cx, cy, inner * 0.28, a + w)
                p2 = polar(cx, cy, Lr, a + w * 0.45)
                p3 = polar(cx, cy, Lr, a - w * 0.45)
                dr.polygon([p0, p1, p2, p3], fill=col)
            ring(cx, cy, inner * 0.24, R * 0.07, col)
        elif kind == "seigaiha":  # a single wave crest of concentric arcs
            for k in range(4):
                rr = inner * (0.95 - k * 0.22)
                dr.arc([cx - rr, cy + inner * 0.15 - rr, cx + rr, cy + inner * 0.15 + rr], 200, 340, fill=col, width=int(R * 0.07))
            disc(cx, cy + inner * 0.15, inner * 0.14, col)

    kinds = ["hanabishi", "hoshi", "tomoe", "kikyo", "wachigai", "hishi", "kiri", "seigaiha"]
    rng.shuffle(kinds)
    encl = ["maru", "hoso", "yuki", "none", "maru", "none", "hoso", "maru"]
    rng.shuffle(encl)
    nfold = {"hanabishi": (4, 5, 6, 8), "hoshi": (5, 6, 8), "tomoe": (3,), "kikyo": (5, 6, 8),
             "wachigai": (3, 4, 5), "hishi": (4,), "kiri": (5, 6, 8, 12), "seigaiha": (1,)}
    red_slot = rng.randrange(8)
    cols, rows = 4, 2
    cellw, cellh = W * s / cols, 118 * s
    top = 30 * s
    fl = font(F_MONO, 8 * s)
    for idx, (kind, enc) in enumerate(zip(kinds, encl)):
        c, r = idx % cols, idx // cols
        cx = (c + 0.5) * cellw
        cy = top + r * cellh + 46 * s
        n = rng.choice(nfold[kind])
        col = RED if idx == red_slot else BLACK
        crest(cx, cy, 38 * s, col, n, kind, enc)
        sym = "D%d" % n if kind != "tomoe" else "C%d" % n
        label = "%s · %s" % (kind, sym)
        tw = dr.textlength(label, font=fl)
        dr.text((cx - tw / 2, cy + 46 * s), label, font=fl, fill=BLACK)
        if idx == red_slot:
            dr.text((cx - tw / 2, cy + 56 * s), "today's crest", font=fl, fill=RED)

    # rules and heading
    dr.line([12 * s, 22 * s, W * s - 12 * s, 22 * s], fill=BLACK, width=s)
    fj = font(F_JP, 13 * s)
    dr.text((12 * s, 5 * s), "家紋", font=fj, fill=BLACK)
    dr.text((44 * s, 8 * s), "KAMON — eight crests from compass and straightedge", font=font(F_SERIF, 9 * s), fill=BLACK)
    dr.line([12 * s, 276 * s, W * s - 12 * s, 276 * s], fill=BLACK, width=s)
    dr.text((12 * s, 280 * s), "n-fold symmetry needs a constructible n-gon: 3, 4, 5, 6, 8, 12 — never 7 or 9",
            font=font(F_SANS, 8 * s), fill=BLACK)
    signature(img, s, BLACK, "br")
    return finalize(img, dither=False)


# ------------------------------------------------------------ 5. Weaving draft
def image5_weave():
    """An honest 4-shaft weaving draft (threading, tie-up, treadling, drawdown),
    black and white warp with a red-and-white weft — Anni Albers' three threads."""
    rng = random.Random(1922 + 20260917)
    shafts = 4
    cell = 4  # px per thread
    # layout (1x pixels): drawdown occupies the left/bottom, notation the top/right
    L, T = 8, 8
    n_warp = 78
    n_weft = 54
    draft_w = n_warp * cell           # 312
    draft_h = n_weft * cell           # 216
    tie_x = L + draft_w + 6           # tie-up / treadling column
    top_y = T + shafts * cell + 6     # drawdown starts here

    # threading: an advancing point twill, seeded
    threading = []
    x = 0
    direction = 1
    run = rng.choice([3, 4, 5, 6])
    while len(threading) < n_warp:
        for _ in range(run):
            threading.append(x % shafts)
            x += direction
        direction *= -1
        x += rng.choice([0, 1])
        run = rng.choice([2, 3, 4, 5, 6, 7])
    threading = threading[:n_warp]

    # tie-up: 4 treadles, each lifting 2 shafts (a balanced 2/2 structure), distinct
    tieups = []
    pairs = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)]
    rng.shuffle(pairs)
    treadles = pairs[:4]

    # treadling: "as drawn in" with occasional reversals
    treadling = []
    t = 0
    d = 1
    while len(treadling) < n_weft:
        block = rng.choice([2, 3, 4, 5, 6])
        for _ in range(block):
            treadling.append(t % 4)
            t += d
        if rng.random() < 0.5:
            d *= -1
    treadling = treadling[:n_weft]

    # colour orders: warp mostly black with white stripes; weft red with white bands
    warp_col = []
    i = 0
    while len(warp_col) < n_warp:
        wblk = rng.choice([6, 8, 12, 16, 20])
        warp_col += [BLACK] * wblk
        warp_col += [WHITE] * rng.choice([2, 2, 4, 6])
    warp_col = warp_col[:n_warp]
    weft_col = []
    while len(weft_col) < n_weft:
        weft_col += [RED] * rng.choice([8, 10, 14, 18])
        weft_col += [WHITE] * rng.choice([2, 3, 4])
    weft_col = weft_col[:n_weft]

    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # threading notation (top): a mark in the shaft row for each warp end
    for j, sh in enumerate(threading):
        x = L + j * cell
        y = T + (shafts - 1 - sh) * cell
        dr.rectangle([x, y, x + cell - 1, y + cell - 1], fill=warp_col[j])
    dr.rectangle([L - 1, T - 1, L + draft_w, T + shafts * cell], outline=BLACK)

    # tie-up (top right): treadle columns vs shaft rows
    for k, (a, b) in enumerate(treadles):
        for sh in (a, b):
            x = tie_x + k * cell
            y = T + (shafts - 1 - sh) * cell
            dr.rectangle([x, y, x + cell - 1, y + cell - 1], fill=BLACK)
    dr.rectangle([tie_x - 1, T - 1, tie_x + 4 * cell, T + shafts * cell], outline=BLACK)

    # treadling (right): one mark per pick
    for i, tr in enumerate(treadling):
        x = tie_x + tr * cell
        y = top_y + i * cell
        dr.rectangle([x, y, x + cell - 1, y + cell - 1], fill=weft_col[i])
    dr.rectangle([tie_x - 1, top_y - 1, tie_x + 4 * cell, top_y + draft_h], outline=BLACK)

    # drawdown: warp shows where its shaft is lifted by the pick's treadle
    px = np.zeros((draft_h, draft_w, 3), dtype=np.uint8)
    for i in range(n_weft):
        lifted = treadles[treadling[i]]
        for j in range(n_warp):
            c = warp_col[j] if threading[j] in lifted else weft_col[i]
            y0, x0 = i * cell, j * cell
            px[y0:y0 + cell, x0:x0 + cell] = c
    img.paste(Image.fromarray(px), (L, top_y))
    dr.rectangle([L - 1, top_y - 1, L + draft_w, top_y + draft_h], outline=BLACK)

    # captions
    fm = font(F_MONO, 8)
    fs = font(F_SERIF, 10)
    yb = top_y + draft_h + 6
    dr.text((L, yb), "DRAFT No. 260917 — 4 shafts, 4 treadles, 2/2 tie-up", font=fs, fill=BLACK)
    dr.text((L, yb + 14), "warp black/white · weft red/white · %d ends x %d picks" % (n_warp, n_weft), font=fm, fill=BLACK)
    dr.text((L, yb + 25), "threading above, tie-up & treadling right · after Anni Albers, 1926", font=fm, fill=BLACK)
    signature(img, 1, BLACK, "br")
    return finalize(img, dither=False)


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", ".."))
    makers = [image1_mimas, image2_equinox, image3_higanbana, image4_kamon, image5_weave]
    for i, mk in enumerate(makers, 1):
        im = mk()
        assert im.size == (W, H)
        for d in (here, os.path.join(root, "images")):
            im.save(os.path.join(d, "%d.png" % i), optimize=True)
        print("wrote", i, mk.__name__)


if __name__ == "__main__":
    main()
