#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-16.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

Today's hooks:
  - July 16, 1969: Apollo 11 lifts off (57 years ago today).
  - July 16, 1945: the Trinity test, 05:29 local — the atomic age begins.
  - Mid-July sky: new moon just past (Jul 14); a slender crescent meets Venus
    low in the west after sunset on Jul 17; Buck Moon full on Jul 29; the
    Southern delta-Aquariids and alpha-Capricornids build toward month's end.

Technique: render tonal scenes at 3x, LANCZOS downscale, Floyd-Steinberg
dither into the exact palette; render hard-edged graphic pieces at 1x in pure
palette colors.

Set 1: Saturn V ascent (Apollo 11).      tonal, dithered.
Set 2: Beat the Whites (constructivist). hard-edged graphic.
Set 3: Evening sky almanac.              chart + calendar.
Set 4: Kamon — a generated crest.        hard-edged, radial.
Set 5: Trinity, 05:29 — a quiet ledger.  tonal + type.
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


# ------------------------------------------------------ 1. Saturn V ascent
def image1_apollo():
    """A launch vehicle climbing out of frame on a column of dithered smoke,
    red fire at its base, against a starless dawn that darkens with altitude."""
    rng = random.Random(19690716)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # Sky: light at the horizon, darkening upward (space above). Vertical ramp.
    for y in range(H * s):
        t = y / (H * s)                     # 0 top .. 1 bottom
        v = int(18 + 230 * (t ** 1.4))      # dark up high, bright near ground
        dr.line([(0, y), (W * s, y)], fill=(v, v, v))

    # A few stars only in the dark upper band.
    for _ in range(70):
        y = rng.uniform(0, H * s * 0.34)
        x = rng.uniform(0, W * s)
        if rng.random() < 0.6:
            dr.point((x, y), fill=(210, 210, 210))

    # The rocket: a slim column rising from lower-right toward upper-left,
    # tilted a touch as it pitches over. Base sits above the bottom edge so the
    # flame and smoke column stay in frame.
    basex, basey = 246, 236
    tipx, tipy = 212, -18
    length = math.hypot(tipx - basex, tipy - basey)
    ux, uy = (tipx - basex) / length, (tipy - basey) / length   # up-axis
    px, py = -uy, ux                                            # perpendicular

    def along(d, off):
        cx = basex + ux * d + px * off
        cy = basey + uy * d + py * off
        return cx * s, cy * s

    # Smoke / exhaust plume billowing down and out below the engines.
    for _ in range(5200):
        d = rng.uniform(-150, 6)              # mostly below the base
        spread = 6 + (-d) * 0.42
        off = rng.gauss(0, spread)
        # plume drifts to the right as it falls
        drift = (-d) * 0.5
        cx, cy = along(d, off)
        cx += drift * s
        r = rng.uniform(1.0, 4.2) * s
        v = rng.randint(150, 255)
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(v, v, v))
    # darker curls inside the smoke for volume
    for _ in range(1400):
        d = rng.uniform(-140, -6)
        off = rng.gauss(0, 5 + (-d) * 0.34)
        drift = (-d) * 0.5
        cx, cy = along(d, off)
        cx += drift * s
        r = rng.uniform(1.4, 4.0) * s
        v = rng.randint(70, 140)
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(v, v, v))

    # Fire: bright red flame cone straight below the engines.
    for _ in range(2600):
        d = rng.uniform(-58, 2)
        spread = 3.0 + (-d) * 0.16
        off = rng.gauss(0, spread)
        cx, cy = along(d, off)
        r = rng.uniform(1.2, 3.4) * s
        # core hotter (pure red), edges feather into smoke
        if abs(off) < spread * 0.85:
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    # a white-hot heart at the nozzles
    for _ in range(260):
        d = rng.uniform(-10, 2)
        off = rng.gauss(0, 2.4)
        cx, cy = along(d, off)
        r = rng.uniform(0.8, 2.0) * s
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 235, 235))

    # The body: white cylinder with black roll-pattern bands, dark at the top.
    halfw = 5.2
    def body_quad(d0, d1, hw0, hw1, fill):
        a = along(d0, -hw0); b = along(d0, hw0)
        c = along(d1, hw1); e = along(d1, -hw1)
        dr.polygon([a, b, c, e], fill=fill)

    body_quad(0, 250, halfw, halfw * 0.62, WHITE)          # tapering stack
    # black bands (interstage rings)
    for d in (34, 96, 150, 196):
        hw = halfw * (1 - d / 620)
        body_quad(d, d + 7, hw, hw, BLACK)
    # the classic black roll pattern near the base
    body_quad(6, 20, halfw, halfw, BLACK)
    dr.polygon([along(6, -halfw), along(6, halfw),
                along(20, 0)], fill=WHITE)
    # nose cone / escape tower, going dark against space
    tip = along(262, 0)
    l = along(250, halfw * 0.6); r = along(250, -halfw * 0.6)
    dr.polygon([l, r, tip], fill=(30, 30, 30))
    dr.line([along(262, 0), along(276, 0)], fill=(30, 30, 30), width=int(1.6 * s))

    # Title block, lower-left, over the bright ground haze.
    f_big = font(FONT_SANS_B, 20 * s)
    f_med = font(FONT_SANS, 11 * s)
    f_sm = font(FONT_MONO, 9 * s)
    dr.text((16 * s, 236 * s), "APOLLO 11", font=f_big, fill=BLACK)
    dr.text((17 * s, 260 * s), "16 July 1969 — 13:32 UTC — LC-39A",
            font=f_med, fill=BLACK)
    dr.text((17 * s, 278 * s), "57 years ago today: liftoff for the Moon",
            font=f_sm, fill=RED)
    return finalize(img)


# ------------------------------------------ 2. Beat the Whites (constructivist)
def image2_constructivist():
    """A homage to Lissitzky's black/white/red vocabulary — a red wedge driving
    into a white field, black bars and a floating disc. Hard-edged, 1x."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # A large black field on the right the red wedge drives into.
    dr.polygon([(212, 0), (400, 0), (400, 300), (150, 300)], fill=BLACK)

    # The red wedge — a triangle thrusting from lower-left into the black.
    dr.polygon([(6, 254), (296, 150), (10, 78)], fill=RED)
    # a thin echo of the wedge, offset, in white inside the black
    dr.polygon([(236, 150), (300, 168), (238, 175)], fill=WHITE)

    # Black bars radiating / bracing from the wedge's origin.
    for (x0, y0, x1, y1, w) in [
        (14, 268, 350, 292, 7),
        (10, 66, 300, 40, 5),
        (0, 150, 150, 150, 4),
    ]:
        dr.line([(x0, y0), (x1, y1)], fill=BLACK, width=w)

    # A white disc floating in the black field, with a red core.
    cx, cy, r = 322, 96, 40
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    dr.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=RED)
    # a black tick orbiting the disc
    dr.line([(cx + r - 2, cy), (cx + r + 22, cy - 12)], fill=BLACK, width=4)

    # Small red square + black square, constructivist punctuation, lower-right.
    dr.rectangle([300, 250, 326, 276], fill=RED)
    dr.rectangle([334, 258, 352, 276], fill=WHITE)

    # A thin red rule and a title set in the white margin, rotated feel via caps.
    f = font(FONT_SANS_B, 15)
    f2 = font(FONT_MONO, 9)
    dr.text((12, 12), "БЕЙ БЕЛЫХ", font=f, fill=BLACK)
    dr.text((12, 30), "beat the whites with the red wedge", font=f2, fill=RED)
    dr.text((12, 286), "after El Lissitzky, 1919 — the palette IS the movement",
            font=f2, fill=BLACK)
    return finalize(img, dither=False)


# ---------------------------------------------------- 3. Evening sky almanac
def image3_almanac():
    """A tonight-ish sky card: crescent Moon meeting Venus low in the west after
    sunset (Jul 17), plus a compact month calendar of moon + shower events."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # Upper 60%: a twilight sky panel (dark), lower 40%: white ledger.
    sky_h = int(H * 0.60) * s
    for y in range(sky_h):
        t = y / sky_h
        v = int(12 + 70 * (t ** 1.5))     # deep at top, glow near horizon
        dr.line([(0, y), (W * s, y)], fill=(v, v, v))
    # horizon glow (dusk), a brighter band at the bottom of the sky panel
    for y in range(sky_h - 26 * s, sky_h):
        t = (y - (sky_h - 26 * s)) / (26 * s)
        v = int(80 + 150 * t)
        dr.line([(0, y), (W * s, y)], fill=(v, v, v))

    # White ledger fills everything below the sky panel.
    dr.rectangle([0, sky_h, W * s, H * s], fill=WHITE)

    # A ragged black rooftop silhouette sitting ON the horizon line, rising a
    # little way up into the sky (does not flood the ledger below).
    rng = random.Random(20260717)
    xs = list(range(0, W * s + 20 * s, 16 * s))
    prev = sky_h - rng.randint(0, 6) * s
    pts = [(0, sky_h)]
    for x in xs:
        h = sky_h - rng.randint(0, 12) * s
        pts.append((x, prev))
        pts.append((x, h))
        prev = h
    pts.append((W * s, prev))
    pts.append((W * s, sky_h))
    dr.polygon(pts, fill=BLACK)

    # Venus: a bright star-point with a small cross flare.
    vx, vy = 250 * s, (sky_h - 66 * s)
    for rr, v in [(3.4, 90), (2.0, 190), (1.1, 255)]:
        dr.ellipse([vx - 4 * s * rr, vy - 4 * s * rr,
                    vx + 4 * s * rr, vy + 4 * s * rr], fill=(v, v, v))
    dr.line([vx - 14 * s, vy, vx + 14 * s, vy], fill=WHITE, width=s)
    dr.line([vx, vy - 14 * s, vx, vy + 14 * s], fill=WHITE, width=s)

    # Crescent Moon near Venus: bright disc minus an offset dark disc.
    mx, my, mr = 150 * s, (sky_h - 92 * s), 26 * s
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=WHITE)
    off = 12 * s
    dr.ellipse([mx - mr + off, my - mr - 4 * s,
                mx + mr + off, my + mr - 4 * s], fill=(24, 24, 24))
    # earthshine hint: faint gray fill on the dark limb
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=(120, 120, 120),
               width=s)

    f_lbl = font(FONT_SANS, 11 * s)
    dr.text((vx + 12 * s, vy - 6 * s), "Venus", font=f_lbl, fill=WHITE)
    dr.text((mx - mr, my - mr - 15 * s), "Moon", font=f_lbl, fill=WHITE)

    # Title on the sky.
    f_title = font(FONT_SERIF_B, 15 * s)
    dr.text((14 * s, 12 * s), "the western sky, just after sunset",
            font=f_title, fill=WHITE)
    f_sub = font(FONT_SANS, 10 * s)
    dr.text((14 * s, 33 * s), "Jul 17: a two-day crescent meets Venus low in the WNW",
            font=f_sub, fill=WHITE)

    # Ledger (white) — a compact almanac.
    ly = sky_h + 8 * s
    f_h = font(FONT_MONO_B, 12 * s)
    f_r = font(FONT_MONO, 11 * s)
    dr.text((16 * s, ly), "MID / LATE JULY 2026", font=f_h, fill=BLACK)
    rows = [
        ("Jul 14", "New Moon — darkest skies, Milky Way core", False),
        ("Jul 17", "Crescent Moon + Venus, low WNW at dusk", True),
        ("Jul 29", "Full Buck Moon", False),
        ("Jul 30", "delta-Aquariids + alpha-Capricornids peak", True),
    ]
    yy = ly + 20 * s
    for date, txt, hot in rows:
        col = RED if hot else BLACK
        dr.text((16 * s, yy), date, font=f_r, fill=col)
        dr.text((86 * s, yy), txt, font=f_r, fill=BLACK)
        yy += 17 * s
    return finalize(img)


# ------------------------------------------------------------- 4. Kamon crest
def image4_kamon():
    """A generated family-crest (kamon): a bold radial emblem — here a plum
    blossom (ume) inside a ring, the way Japanese mon distill a thing to pure
    rotational symmetry. Hard-edged, pure palette."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    cx, cy = W * s / 2, H * s / 2 - 6 * s
    R = 118 * s

    # Outer ring (kai — a bold circle enclosing the mon).
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)
    dr.ellipse([cx - R + 12 * s, cy - R + 12 * s,
                cx + R - 12 * s, cy + R - 12 * s], fill=WHITE)

    # Five-petal plum blossom, black on white, filling the ring.
    petal_r = 40 * s          # distance of each petal centre from middle
    pr = 40 * s               # petal radius
    def blossom(fill, scale=1.0, ir=0.0):
        for k in range(5):
            a = -math.pi / 2 + k * 2 * math.pi / 5
            px = cx + math.cos(a) * petal_r * scale
            py = cy + math.sin(a) * petal_r * scale
            rr = pr * scale
            dr.ellipse([px - rr, py - rr, px + rr, py + rr], fill=fill)
    blossom(BLACK, 1.0)
    # white notch at each petal tip (the classic ume cleft)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        tx = cx + math.cos(a) * (petal_r + pr) * 0.98
        ty = cy + math.sin(a) * (petal_r + pr) * 0.98
        nr = 9 * s
        dr.ellipse([tx - nr, ty - nr, tx + nr, ty + nr], fill=WHITE)
    # inner white blossom to make the petals into outlines
    blossom(WHITE, 0.62)
    # red core stamen — the single accent
    cr = 15 * s
    dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=RED)
    # five short black stamens radiating from the core
    for k in range(10):
        a = k * 2 * math.pi / 10
        x2 = cx + math.cos(a) * 30 * s
        y2 = cy + math.sin(a) * 30 * s
        dr.line([cx + math.cos(a) * 15 * s, cy + math.sin(a) * 15 * s,
                 x2, y2], fill=BLACK, width=int(2.2 * s))
        dr.ellipse([x2 - 3 * s, y2 - 3 * s, x2 + 3 * s, y2 + 3 * s], fill=BLACK)

    # Caption.
    f_jp = font(FONT_JP, 20 * s)
    f_en = font(FONT_SANS, 11 * s)
    dr.text((W * s / 2, 264 * s), "梅鉢 — umebachi", font=f_jp,
            fill=BLACK, anchor="ma")
    dr.text((W * s / 2, 285 * s), "a plum-blossom mon, drawn by rotational symmetry",
            font=f_en, fill=RED, anchor="ma")
    return finalize(img, dither=False)


# ------------------------------------------------------ 5. Trinity, 05:29
def image5_trinity():
    """A quiet, sober card for the first light of the atomic age: a single
    expanding ring of light on the desert dark, 05:29:45 MWT, 16 July 1945.
    Restrained on purpose — this is a ledger of a morning, not a spectacle."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    cx, cy = W * s * 0.5, H * s * 0.46

    # The flash: concentric rings, brightest at the core, fading out. Rendered
    # as soft gray so dithering gives it grain rather than a hard edge.
    maxr = 150 * s
    rng = random.Random(19450716)
    for _ in range(52000):
        rr = (rng.random() ** 0.5) * maxr
        a = rng.uniform(0, 2 * math.pi)
        x = cx + math.cos(a) * rr
        y = cy + math.sin(a) * rr * 0.82      # slightly oblate
        # brightness falls with radius
        t = rr / maxr
        v = int(255 * (1 - t) ** 1.7)
        if v < 6:
            continue
        # a faint reddish inner shell (the fireball), then white shock
        pr = 1.0 * s
        if t < 0.18:
            dr.ellipse([x - pr, y - pr, x + pr, y + pr], fill=RED)
        else:
            dr.ellipse([x - pr, y - pr, x + pr, y + pr], fill=(v, v, v))
    # a bright white core disc
    core = 20 * s
    for rr, v in [(1.0, 90), (0.7, 200), (0.45, 255)]:
        dr.ellipse([cx - core * rr, cy - core * rr * 0.82,
                    cx + core * rr, cy + core * rr * 0.82], fill=(v, v, v))

    # The desert horizon: a thin lit line low in frame.
    hy = H * s * 0.80
    dr.line([(0, hy), (W * s, hy)], fill=(60, 60, 60), width=s)
    for _ in range(600):
        x = rng.uniform(0, W * s)
        yy = rng.uniform(hy, hy + 18 * s)
        v = int(40 * (1 - (yy - hy) / (18 * s)))
        dr.point((x, yy), fill=(v, v, v))

    # Type, restrained, in the dark lower band.
    f_h = font(FONT_SERIF_B, 15 * s)
    f_t = font(FONT_MONO, 10 * s)
    f_q = font(FONT_SERIF, 11 * s)
    dr.text((W * s / 2, hy + 22 * s), "TRINITY", font=f_h, fill=WHITE,
            anchor="ma")
    dr.text((W * s / 2, hy + 42 * s),
            "16 July 1945 — 05:29:45 — Jornada del Muerto, NM",
            font=f_t, fill=(200, 200, 200), anchor="ma")
    dr.text((W * s / 2, hy + 57 * s),
            "“Now I am become Death, the destroyer of worlds.”",
            font=f_q, fill=RED, anchor="ma")
    return finalize(img)


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_apollo, image2_constructivist, image3_almanac,
              image4_kamon, image5_trinity]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(f"wrote {path}  colors={len(cols)}")
