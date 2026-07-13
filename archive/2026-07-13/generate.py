#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-13 (day two — the dark of the moon).

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Tonal scenes render at 3x then Floyd-Steinberg
dither into the exact palette; hard-edged geometric pieces render supersampled
and quantize with no dither so edges snap clean.

Today's five (see memory.md):
  1. Krasnym Klinom  — El Lissitzky "Beat the Whites with the Red Wedge" homage
  2. Nami            — generative Hokusai-esque great wave with a red sun
  3. Truchet         — multiscale quarter-arc Truchet tiling with red sparks
  4. 星月夜           — "hoshizukiyo": a moonless, star-filled night (typography)
  5. Rule 30         — elementary cellular automaton spacetime, red light-cone
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3  # supersample factor
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED)
    palette += [0, 0, 0] * (256 - 3)
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=True):
    """Downscale (if supersampled) and quantize to the exact 3-color palette."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def rot(cx, cy, x, y, ang):
    """Rotate point (x,y) about (cx,cy) by ang radians."""
    c, s = math.cos(ang), math.sin(ang)
    dx, dy = x - cx, y - cy
    return (cx + dx * c - dy * s, cy + dx * s + dy * c)


# ------------------------------------------------ 1. Krasnym Klinom (Lissitzky)
def image1_klin():
    """Beat the Whites with the Red Wedge — generative Constructivist homage.
    The black/white/red panel *is* this movement; overdue since day one."""
    rng = random.Random(20260713)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    def sc(*pts):
        return [(x * s, y * s) for x, y in pts]

    # The white camp: a big black circle, right of centre.
    ccx, ccy, cr = 272, 150, 104
    dr.ellipse([(ccx - cr) * s, (ccy - cr) * s, (ccx + cr) * s, (ccy + cr) * s],
               fill=BLACK)
    # a small white disc bitten out near the wedge tip — the split
    dr.ellipse([(ccx - 20) * s, (ccy - 20) * s, (ccx + 20) * s, (ccy + 20) * s],
               fill=WHITE)

    # The red wedge: a sharp triangle driving in from the upper-left, tip at
    # the circle's heart.
    tip = (ccx - 4, ccy)
    base_top = (34, 52)
    base_bot = (92, 250)
    dr.polygon(sc(tip, base_top, base_bot), fill=RED)
    # a second, thinner red shard for momentum
    dr.polygon(sc((ccx - 4, ccy), (150, 26), (196, 40)), fill=RED)

    # Black constructivist bars — long thin rectangles at dynamic angles.
    bars = [
        (60, 250, 250, 44, 3.5, BLACK),
        (300, 40, 120, 8, -0.7, BLACK),
        (250, 118, 150, 5, 0.9, BLACK),
    ]
    for bx, by, ln, th, ang, col in bars:
        pts = [(-ln / 2, -th / 2), (ln / 2, -th / 2),
               (ln / 2, th / 2), (-ln / 2, th / 2)]
        pts = [rot(0, 0, px, py, ang) for px, py in pts]
        pts = [(bx + px, by + py) for px, py in pts]
        dr.polygon(sc(*pts), fill=col)

    # Scatter: small squares and a couple of thin lines, seeded — every day differs.
    for _ in range(7):
        qx = rng.uniform(20, 175)
        qy = rng.uniform(200, 285)
        q = rng.uniform(4, 13)
        a = rng.uniform(0, math.pi)
        col = rng.choice([BLACK, BLACK, RED])
        pts = [rot(0, 0, -q, -q, a), rot(0, 0, q, -q, a),
               rot(0, 0, q, q, a), rot(0, 0, -q, q, a)]
        pts = [(qx + px, qy + py) for px, py in pts]
        dr.polygon(sc(*pts), fill=col)
    # thin radiating black lines from the tip
    for _ in range(5):
        a = rng.uniform(-0.9, 0.9)
        ln = rng.uniform(70, 150)
        x2 = tip[0] - ln * math.cos(a)
        y2 = tip[1] - ln * math.sin(a)
        dr.line(sc(tip, (x2, y2)), fill=BLACK, width=max(1, s // 2))

    # a lone red dot far bottom-right for balance
    dr.ellipse([360 * s, 255 * s, 374 * s, 269 * s], fill=RED)

    # Typography — the slogan, Cyrillic, set small and rotated like the original.
    f_cyr = font(FONT_SANS_B, 13 * s)
    slogan = ["КЛИНОМ", "КРАСНЫМ", "БЕЙ БЕЛЫХ"]
    ty = 66
    for line in slogan:
        dr.text((16 * s, ty * s), line, font=f_cyr, fill=BLACK)
        ty += 17
    f_sm = font(FONT_SANS_B, 8 * s)
    dr.text((16 * s, (ty + 3) * s),
            "BEAT THE WHITES WITH THE RED WEDGE", font=f_sm, fill=BLACK)

    f_cap = font(FONT_MONO, 8 * s)
    dr.text((W * s - 10 * s, H * s - 12 * s),
            "after El Lissitzky, 1919", font=f_cap, fill=BLACK, anchor="rs")
    return finalize(img, dither=False)


# --------------------------------------------------------------------- 2. Nami
def image2_nami():
    """Generative great wave: layered swells, dithered foam, a flat red sun."""
    rng = random.Random(20260713 + 2)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # pale, softly graded sky (dithers to a faint stipple up top)
    for y in range(0, int(H * 0.62 * s)):
        t = y / (H * 0.62 * s)
        v = int(255 - 22 * (1 - t))
        dr.line([(0, y), (W * s, y)], fill=(v, v, v))

    # red sun disc, low, sitting in the trough between the back swells
    sunx, suny, sunr = 268, 118, 40
    dr.ellipse([(sunx - sunr) * s, (suny - sunr) * s,
                (sunx + sunr) * s, (suny + sunr) * s], fill=RED)

    def swell(base, amp, freqs, phase, jag, seed):
        r = random.Random(seed)
        pts = []
        for px in range(0, W * s + 2 * s, 2 * s):
            t = px / (W * s)
            y = base
            for k, (fq, a) in enumerate(freqs):
                y += a * math.sin(2 * math.pi * (fq * t + phase * (k + 1)))
            y += jag * (r.random() - 0.5)
            pts.append((px, y * s))
        return pts

    # back-to-front swells; front ones darker so the dither reads as deep water
    layers = [
        (150, [(1.1, 12), (2.6, 6), (5.1, 3)], 0.20, 4, 120, 20260101),
        (182, [(0.9, 16), (2.2, 8), (4.4, 4)], 0.55, 5, 70, 20260202),
        (216, [(0.8, 20), (1.8, 10), (3.9, 5)], 0.83, 6, 26, 20260303),
        (250, [(0.7, 22), (1.6, 11), (3.3, 6)], 0.37, 7, 0, 20260404),
    ]
    crest_pts = []
    for base, freqs, phase, jag, v, seed in layers:
        pts = swell(base, 0, freqs, phase, jag, seed)
        poly = pts + [(W * s, H * s), (0, H * s)]
        dr.polygon(poly, fill=(v, v, v))
        crest_pts.append((pts, v))

    # foam: white speckle + little curl fingers riding each crest line
    for pts, v in crest_pts:
        for (px, py) in pts:
            if rng.random() < 0.5:
                r = rng.uniform(0.6, 2.2) * s
                dr.ellipse([px - r, py - r, px + r, py + r], fill=WHITE)
        # occasional Hokusai-ish claw of foam thrown forward
        for _ in range(int(len(pts) * 0.06)):
            i = rng.randrange(len(pts))
            fx, fy = pts[i]
            n = rng.randint(3, 6)
            for k in range(n):
                a = -math.pi / 2 + rng.uniform(-0.7, 0.7)
                ln = rng.uniform(4, 12) * s
                ex = fx + ln * math.cos(a)
                ey = fy + ln * math.sin(a)
                dr.line([fx, fy, ex, ey], fill=WHITE, width=max(1, s // 2))
                dr.ellipse([ex - 1.3 * s, ey - 1.3 * s,
                            ex + 1.3 * s, ey + 1.3 * s], fill=WHITE)

    # a few birds against the sky
    for (bx, by, sz) in [(96, 58, 7), (120, 70, 5), (150, 52, 5)]:
        bx, by, sz = bx * s, by * s, sz * s
        dr.arc([bx - sz, by - sz // 2, bx, by + sz], 200, 340, fill=BLACK, width=s)
        dr.arc([bx, by - sz // 2, bx + sz, by + sz], 200, 340, fill=BLACK, width=s)

    f_jp = font(FONT_JP, 20 * s)
    f_sm = font(FONT_SANS, 9 * s)
    dr.text((14 * s, (H - 30) * s), "波", font=f_jp, fill=RED)
    dr.text((40 * s, (H - 20) * s),
            "nami — the sea, from sine waves, noise, and a low red sun",
            font=f_sm, fill=WHITE)
    return finalize(img)


# ------------------------------------------------------------------ 3. Truchet
def image3_truchet():
    """Multiscale quarter-arc Truchet tiling. Two tile orientations; a subset of
    cells recurse into 2x2; a scatter of cells drawn in red."""
    rng = random.Random(20260713 + 3)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    top = 8       # margin for content
    bottom = 26   # caption band
    base = 48     # base cell size (px)
    cols = W // base
    x0 = (W - cols * base) // 2

    # Each tile draws two quarter arcs, centred on opposite corners; the two
    # orientations connect the four edge-midpoints the two possible ways.
    def truchet(px, py, size, orient, col, lw):
        w = max(1, int(lw * s))
        L, T = px * s, py * s
        R, B = (px + size) * s, (py + size) * s
        d = size * s  # arc box diameter = full cell
        if orient == 0:
            # arc centred at top-left corner, and arc centred at bottom-right
            dr.arc([L - d / 2, T - d / 2, L + d / 2, T + d / 2], 0, 90,
                   fill=col, width=w)
            dr.arc([R - d / 2, B - d / 2, R + d / 2, B + d / 2], 180, 270,
                   fill=col, width=w)
        else:
            # arc centred at top-right, and arc centred at bottom-left
            dr.arc([R - d / 2, T - d / 2, R + d / 2, T + d / 2], 90, 180,
                   fill=col, width=w)
            dr.arc([L - d / 2, B - d / 2, L + d / 2, B + d / 2, ], 270, 360,
                   fill=col, width=w)

    rows = (H - top - bottom) // base
    for j in range(rows):
        for i in range(cols):
            px = x0 + i * base
            py = top + j * base
            if rng.random() < 0.42:
                # recurse: 2x2 of half-size cells
                h = base // 2
                for jj in range(2):
                    for ii in range(2):
                        o = rng.randint(0, 1)
                        col = RED if rng.random() < 0.14 else BLACK
                        truchet(px + ii * h, py + jj * h, h, o, col, 2.0)
            else:
                o = rng.randint(0, 1)
                col = RED if rng.random() < 0.16 else BLACK
                truchet(px, py, base, o, col, 3.0)

    dr.rectangle([x0 * s, top * s, (x0 + cols * base) * s,
                  (top + rows * base) * s], outline=BLACK, width=s)

    f_capb = font(FONT_SANS_B, 10 * s)
    f_cap = font(FONT_SANS, 10 * s)
    yt = (top + rows * base + 8)
    dr.text((x0 * s, yt * s), "TRUCHET", font=f_capb, fill=BLACK)
    dr.text(((x0 + 66) * s, yt * s),
            "one tile, two turns, endless contours", font=f_cap, fill=BLACK)
    dr.text(((x0 + cols * base) * s, yt * s), "13·07",
            font=f_capb, fill=RED, anchor="ra")
    return finalize(img, dither=False)


# ----------------------------------------------------------------- 4. 星月夜
def image4_hoshizukiyo():
    """Word of the day: 星月夜 (hoshizukiyo) — a night so bright with stars it
    needs no moon. Which is literally the sky tonight, on the eve of the new moon."""
    rng = random.Random(20260713 + 4)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # faint star field, denser toward the top (dithers to a sparse stipple)
    for _ in range(520):
        x = rng.uniform(0, W)
        y = rng.uniform(0, H)
        p = 1.0 - y / H
        if rng.random() > 0.25 + 0.7 * p:
            continue
        v = rng.randint(150, 232)
        r = rng.uniform(0.4, 1.5) * s
        dr.ellipse([x * s - r, y * s - r, x * s + r, y * s + r], fill=(v, v, v))
    # a couple of brighter (near-black) stars with tiny spikes
    for (x, y, r) in [(56, 40, 2.0), (330, 58, 1.7), (300, 210, 1.6),
                      (80, 250, 1.5)]:
        x, y, r = x * s, y * s, r * s
        dr.line([x - 4 * r, y, x + 4 * r, y], fill=(90, 90, 90), width=max(1, s // 2))
        dr.line([x, y - 4 * r, x, y + 4 * r], fill=(90, 90, 90), width=max(1, s // 2))
        dr.ellipse([x - r, y - r, x + r, y + r], fill=BLACK)

    # the three big kanji, in red, centred
    f_jp = font(FONT_JP, 92 * s)
    chars = "星月夜"
    widths = [dr.textbbox((0, 0), c, font=f_jp)[2] for c in chars]
    gap = 10 * s
    total = sum(widths) + gap * (len(chars) - 1)
    x = (W * s - total) // 2
    cy = 118 * s
    for c, wch in zip(chars, widths):
        dr.text((x, cy), c, font=f_jp, fill=RED, anchor="lm")
        x += wch + gap

    # thin red rules bracketing the title
    dr.line([40 * s, 172 * s, (W - 40) * s, 172 * s], fill=RED, width=s)

    # romaji, letterspaced
    f_rom = font(FONT_SERIF, 15 * s)
    romaji = "H O S H I Z U K I Y O"
    dr.text((W * s // 2, 190 * s), romaji, font=f_rom, fill=BLACK, anchor="ma")

    # gloss
    f_glo = font(FONT_SERIF_I, 12 * s)
    dr.text((W * s // 2, 214 * s),
            "a night so bright with stars it wants no moon",
            font=f_glo, fill=BLACK, anchor="ma")

    # per-character etymology, small
    f_et = font(FONT_JP, 11 * s)
    f_ets = font(FONT_SANS, 9 * s)
    parts = [("星", "hoshi · star"), ("月", "tsuki · moon"), ("夜", "yo · night")]
    seg = W // len(parts)
    for k, (kj, gl) in enumerate(parts):
        bx = seg * k + seg // 2
        dr.text((bx * s, 244 * s), kj, font=f_et, fill=RED, anchor="ma")
        dr.text((bx * s, 260 * s), gl, font=f_ets, fill=BLACK, anchor="ma")

    f_note = font(FONT_SANS, 9 * s)
    dr.text((W * s // 2, 282 * s),
            "new moon Jul 14 — tonight the sky keeps only its stars",
            font=f_note, fill=BLACK, anchor="ma")
    return finalize(img)


# ------------------------------------------------------------------ 5. Rule 30
def image5_rule30():
    """Elementary cellular automaton, rule 30 — a single seed at the top decays
    into chaos. Red traces the light-cone envelope (left/right-most live cells)."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    top = 30       # header band
    bottom = 8
    cell = 3
    cols = W // cell
    rows = (H - top - bottom) // cell
    x0 = (W - cols * cell) // 2

    rule = 30
    table = [(rule >> k) & 1 for k in range(8)]  # table[left*4+mid*2+right]

    state = [0] * cols
    state[cols // 2] = 1
    for j in range(rows):
        # envelope of this row
        live = [i for i, v in enumerate(state) if v]
        lo, hi = (min(live), max(live)) if live else (None, None)
        for i, v in enumerate(state):
            if not v:
                continue
            col = RED if (i == lo or i == hi) else BLACK
            px = (x0 + i * cell) * s
            py = (top + j * cell) * s
            dr.rectangle([px, py, px + cell * s - 1, py + cell * s - 1], fill=col)
        # advance
        nxt = [0] * cols
        for i in range(cols):
            l = state[(i - 1) % cols]
            m = state[i]
            r = state[(i + 1) % cols]
            nxt[i] = table[l * 4 + m * 2 + r]
        state = nxt

    # header
    f_h = font(FONT_MONO_B, 17 * s)
    f_d = font(FONT_MONO, 9 * s)
    dr.text((x0 * s, 6 * s), "RULE 30", font=f_h, fill=BLACK)
    dr.text(((x0 + 92) * s, 8 * s), "one seed → chaos", font=f_d, fill=RED)
    dr.text(((x0 + cols * cell) * s, 8 * s),
            "111 110 101 100 011 010 001 000", font=font(FONT_MONO, 7 * s),
            fill=BLACK, anchor="ra")
    dr.text(((x0 + cols * cell) * s, 17 * s),
            " 0   0   0   1   1   1   1   0", font=font(FONT_MONO, 7 * s),
            fill=BLACK, anchor="ra")
    return finalize(img, dither=False)


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_klin, image2_nami, image3_truchet,
              image4_hoshizukiyo, image5_rule30]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", sorted(cols))
