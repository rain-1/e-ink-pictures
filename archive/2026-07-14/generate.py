#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-14.

Two hooks today: it is Bastille Day (14 July 1789), and tonight is the new
supermoon — the darkest, best deep-sky night of the month. Plus three fresh
techniques mined from the backlog: seigaiha waves, Truchet arc-tiling, and an
abelian sandpile.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Tonal scenes render at 3x then Floyd-Steinberg
dither; hard-edged pieces render at 3x and quantize with no dither for crisp
edges; the sandpile is computed per-pixel and mapped straight to the palette.
"""

import math
import random
import numpy as np
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


def rotated_text(draw_img, xy, text, fnt, fill, angle, anchor="mm"):
    """Render text on its own layer, rotate, and paste onto draw_img (RGB)."""
    tmp = Image.new("RGBA", draw_img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text(xy, text, font=fnt, fill=fill + (255,), anchor=anchor)
    tmp = tmp.rotate(angle, center=xy, resample=Image.BICUBIC)
    draw_img.paste(tmp, (0, 0), tmp)


# ------------------------------------------------ 1. Beat the Whites (Bastille)
def image1_bastille():
    """El Lissitzky's 'Beat the Whites with the Red Wedge' energy, turned to
    14 July 1789 — the red wedge storms the white bastion."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # Black field: whole top-left is black, a hard diagonal down to the right.
    dr.polygon([(0, 0), (W * s, 0), (W * s, int(0.30 * H * s)),
                (int(0.24 * W * s), H * s), (0, H * s)], fill=BLACK)

    # The white bastion: a white disc straddling the divide (the old order).
    cx, cy, cr = int(0.36 * W * s), int(0.48 * H * s), int(0.28 * H * s)
    dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=WHITE, outline=BLACK,
               width=2 * s)

    # THE red wedge, thrusting from the left into the disc.
    tip = (cx + int(0.14 * H * s), cy)
    dr.polygon([(0, int(0.12 * H * s)), (0, int(0.84 * H * s)), tip], fill=RED)

    # thin dynamic constructivist rays + floating punctuation
    for (x1, y1, x2, y2, col, wd) in [
        (tip[0], tip[1], W * s, int(0.62 * H * s), RED, 2 * s),
        (int(0.55 * W * s), 0, W * s, int(0.14 * H * s), RED, 1 * s),
    ]:
        dr.line([x1, y1, x2, y2], fill=col, width=wd)
    for (bx, by, br, col) in [(int(0.90 * W * s), int(0.20 * H * s), 5 * s, RED),
                              (int(0.68 * W * s), int(0.08 * H * s), 3 * s, WHITE)]:
        dr.ellipse([bx - br, by - br, bx + br, by + br], fill=col)

    # Typography — rotated slabs, Lissitzky style.
    f_huge = font(FONT_SANS_B, 52 * s)
    f_mid = font(FONT_SANS_B, 22 * s)
    f_sm = font(FONT_SANS_B, 12 * s)
    f_ser = font(FONT_SERIF_B, 13 * s)

    # "14 JUILLET" set large in the black upper-right, where white text reads.
    rotated_text(img, (int(0.78 * W * s), int(0.22 * H * s)), "14", f_huge, WHITE,
                 -6, anchor="mm")
    rotated_text(img, (int(0.80 * W * s), int(0.40 * H * s)), "JUILLET", f_mid,
                 RED, -6, anchor="mm")
    # "1789" running up the red wedge in white
    rotated_text(img, (int(0.14 * W * s), int(0.50 * H * s)), "1789", f_mid,
                 WHITE, 68, anchor="mm")
    # context in the white lower-right triangle, in black
    rotated_text(img, (int(0.94 * W * s), int(0.70 * H * s)),
                 "THE BASTILLE FALLS", f_sm, BLACK, -6, anchor="rm")

    # the motto along the bottom
    dr.rectangle([0, int(0.90 * H * s), W * s, H * s], fill=BLACK)
    dr.text((W * s // 2, int(0.95 * H * s)),
            "LIBERTÉ · ÉGALITÉ · FRATERNITÉ", font=f_ser, fill=WHITE,
            anchor="mm")
    return finalize(img, dither=False)


# ----------------------------------------------- 2. The Darkest Night (new moon)
def image2_darkest_night():
    rng = random.Random(20260714)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # Milky Way core (Sagittarius) low along the bottom, rising in the SE.
    def band_center(t):
        x = (0.05 + 0.9 * t) * W * s
        y = (0.98 - 0.28 * math.sin(t * math.pi * 0.9)) * H * s
        return x, y

    for _ in range(2600):
        t = rng.random()
        cx, cy = band_center(t)
        spread = (26 + 16 * math.sin(t * math.pi)) * s
        x = rng.gauss(cx, spread)
        y = rng.gauss(cy, spread * 0.6)
        v = rng.randint(40, 120)
        r = rng.uniform(0.6, 2.3) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))
    # background stars
    for _ in range(260):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s)
        v = rng.randint(110, 255)
        r = rng.uniform(0.4, 1.2) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # The new moon: a disc you cannot see — dark, ringed in faint red, up by the sun.
    mx, my, mr = 60, 52, 26
    mx, my, mr = mx * s, my * s, mr * s
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=BLACK,
               outline=(90, 0, 0), width=1 * s)
    dr.text((mx, my + mr + 6 * s), "new moon", font=font(FONT_SANS, 8 * s),
            fill=(150, 150, 150), anchor="ma")

    # header
    f_h = font(FONT_SERIF_B, 19 * s)
    f_sub = font(FONT_SANS, 10 * s)
    dr.text(((W - 14) * s, 14 * s), "THE DARKEST NIGHT", font=f_h, fill=RED,
            anchor="ra")
    dr.text(((W - 14) * s, 36 * s), "new moon 09:44 UTC — no moonlight until dawn",
            font=f_sub, fill=WHITE, anchor="ra")

    # deep-sky targets to hunt tonight, with tiny glyphs
    targets = [
        ("M13", "Great Hercules cluster"),
        ("M57", "the Ring Nebula, Lyra"),
        ("M8", "the Lagoon, Sagittarius"),
        ("M11", "the Wild Duck cluster"),
        ("Albireo", "gold-&-blue double star"),
    ]
    x0 = 176
    y = 66
    f_t = font(FONT_SANS_B, 11 * s)
    f_d = font(FONT_SANS, 9 * s)
    dr.text((x0 * s, (y - 16) * s), "TONIGHT, HUNT FAINT THINGS:", font=f_t,
            fill=WHITE)
    for tag, desc in targets:
        # a little fuzzy cluster glyph
        gx, gy = (x0 + 5) * s, (y + 4) * s
        for _ in range(14):
            ang = rng.uniform(0, 2 * math.pi)
            rr = rng.uniform(0, 5) * s
            dr.point((gx + rr * math.cos(ang), gy + rr * math.sin(ang)), fill=WHITE)
        dr.text(((x0 + 16) * s, y * s), tag, font=f_t, fill=RED)
        dr.text(((x0 + 74) * s, y * s), desc, font=f_d, fill=(210, 210, 210))
        y += 20

    dr.text((14 * s, (H - 18) * s),
            "the moon is closest of the year tonight — but it rises with the sun,",
            font=f_d, fill=(200, 200, 200))
    dr.text((14 * s, (H - 30) * s),
            "so the sky is yours. 4th of five supermoons in a row.",
            font=f_d, fill=(200, 200, 200))
    return finalize(img)


# --------------------------------------------------------------- 3. Seigaiha
def image3_seigaiha():
    """Blue-ocean-wave pattern (青海波), recolored to the panel's three inks:
    concentric scalloped arcs, offset row to row like fish scales."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    R = 34            # scallop radius (unscaled)
    bands = [BLACK, WHITE, RED, WHITE, BLACK, WHITE]  # outer -> inner rings
    bw = R / len(bands)
    dx = R          # horizontal centre spacing (half-overlap)
    dy = int(R * 0.62)

    def scallop(cx, cy):
        for k, col in enumerate(bands):
            rr = (R - k * bw) * s
            if rr <= 0:
                continue
            box = [cx * s - rr, cy * s - rr, cx * s + rr, cy * s + rr]
            # upper half-disc only -> the wave crest
            dr.pieslice(box, 180, 360, fill=col)

    row = 0
    y = 6
    while y < H + R:
        offset = 0 if row % 2 == 0 else dx // 2
        x = -R + offset
        while x < W + R:
            scallop(x, y)
            x += dx
        y += dy
        row += 1

    # title strip
    dr.rectangle([0, (H - 26) * s, W * s, H * s], fill=WHITE)
    dr.line([0, (H - 26) * s, W * s, (H - 26) * s], fill=BLACK, width=s)
    dr.text((12 * s, (H - 20) * s), "青海波", font=font(FONT_JP, 15 * s), fill=RED)
    dr.text((70 * s, (H - 17) * s),
            "SEIGAIHA — waves of the blue ocean, an unbroken run of calm seas",
            font=font(FONT_SANS, 9 * s), fill=BLACK)
    return finalize(img, dither=False)


# --------------------------------------------------------------- 4. Truchet
def image4_truchet():
    """Truchet arc-tiling: each cell carries two quarter-circle arcs in one of
    two orientations, seeded from the date; the arcs join into flowing loops."""
    rng = random.Random(714_1789)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    n = 20                       # tiles across
    cell = W // n                # 20 px cells -> 20 x 15 grid
    rows = H // cell
    ox = (W - n * cell) // 2
    oy = (H - rows * cell) // 2
    lw = max(2, int(cell * 0.24)) * s

    for i in range(rows):
        for j in range(n):
            x0 = (ox + j * cell) * s
            y0 = (oy + i * cell) * s
            c = cell * s
            # ~16% of tiles carry a red arc-pair, the rest black
            col = RED if rng.random() < 0.16 else BLACK
            if rng.random() < 0.5:
                # arcs in top-left and bottom-right corners
                dr.arc([x0 - c // 2, y0 - c // 2, x0 + c // 2, y0 + c // 2],
                       0, 90, fill=col, width=lw)
                dr.arc([x0 + c // 2, y0 + c // 2, x0 + 3 * c // 2, y0 + 3 * c // 2],
                       180, 270, fill=col, width=lw)
            else:
                # arcs in top-right and bottom-left corners
                dr.arc([x0 + c // 2, y0 - c // 2, x0 + 3 * c // 2, y0 + c // 2],
                       90, 180, fill=col, width=lw)
                dr.arc([x0 - c // 2, y0 + c // 2, x0 + c // 2, y0 + 3 * c // 2],
                       270, 360, fill=col, width=lw)

    # caption plate
    plate_h = 24
    dr.rectangle([0, (H - plate_h) * s, W * s, H * s], fill=WHITE)
    dr.line([0, (H - plate_h) * s, W * s, (H - plate_h) * s], fill=BLACK, width=s)
    dr.text((12 * s, (H - plate_h + 6) * s), "TRUCHET", font=font(FONT_SANS_B, 12 * s),
            fill=BLACK)
    dr.text((95 * s, (H - plate_h + 7) * s),
            "one tile, two turns, a coin-flip each — 300 flips make this maze",
            font=font(FONT_SANS, 9 * s), fill=BLACK)
    return finalize(img, dither=False)


# --------------------------------------------------------------- 5. Sandpile
def image5_sandpile():
    """Abelian sandpile: drop a great heap of sand on one cell and let it
    topple to rest. The stable configuration is a strange fourfold fractal."""
    N = 90_000
    G = 261                      # odd, so there is a centre cell
    pile = np.zeros((G, G), dtype=np.int64)
    pile[G // 2, G // 2] = N
    while True:
        topple = pile >= 4
        if not topple.any():
            break
        pile[topple] -= 4
        pile[1:, :] += topple[:-1, :]
        pile[:-1, :] += topple[1:, :]
        pile[:, 1:] += topple[:, :-1]
        pile[:, :-1] += topple[:, 1:]

    # crop to the active support (non-zero bounding box) with a little margin
    nz = np.argwhere(pile > 0)
    (r0, c0), (r1, c1) = nz.min(0), nz.max(0) + 1
    m = 4
    r0, c0 = max(0, r0 - m), max(0, c0 - m)
    r1, c1 = min(G, r1 + m), min(G, c1 + m)
    sub = pile[r0:r1, c0:c1]

    # map the four grain counts to the three inks. The three abundant states
    # (0, 2, 3) each get their own ink so the fractal structure stays legible;
    # the rare state 1 rides along with the red.
    #   0 -> black, 1 -> red, 2 -> red, 3 -> white
    lut = np.array([BLACK, RED, RED, WHITE], dtype=np.uint8)
    rgb = lut[sub]
    tile = Image.fromarray(rgb, "RGB")

    # scale the square pile up crisply and centre it on the panel
    side = 232
    tile = tile.resize((side, side), Image.NEAREST)
    canvas = Image.new("RGB", (W, H), WHITE)
    px = (W - side) // 2
    py = 8
    canvas.paste(tile, (px, py))
    dr = ImageDraw.Draw(canvas)
    dr.rectangle([px - 2, py - 2, px + side + 1, py + side + 1], outline=BLACK)

    dr.text((W // 2, py + side + 10), "ABELIAN SANDPILE",
            font=font(FONT_SANS_B, 13), fill=BLACK, anchor="ma")
    dr.text((W // 2, py + side + 28),
            f"{N:,} grains on one cell, toppled until still — a coin of order",
            font=font(FONT_SANS, 9), fill=BLACK, anchor="ma")
    dr.text((W // 2, py + side + 40),
            "each cell keeps 0–3 grains; the fourfold symmetry emerges on its own",
            font=font(FONT_SANS, 9), fill=RED, anchor="ma")
    return finalize(canvas, dither=False)


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_bastille, image2_darkest_night, image3_seigaiha,
              image4_truchet, image5_sandpile]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", cols)
