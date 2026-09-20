#!/usr/bin/env python3
"""
e-ink pictures — 2026-08-29
Five images for a 400x300 black/white/red e-ink panel.

Today: Faraday demonstrated the first transformer on this day in 1831 (195 years);
the Beatles played their last real concert at Candlestick Park on this day in 1966
(60 years); tonight the 96% waning gibbous Moon rides beside Saturn.

1. INDUCTION      — constructivist poster for Faraday's iron ring, 29 Aug 1831
2. SEIGAIHA       — Japanese overlapping-wave pattern rolling toward a red sun
3. MOON & SATURN  — tonight's sky through an eyepiece reticle
4. TICKET STUB    — Candlestick Park, The Beatles' final concert, 60 years ago
5. SANDPILE       — abelian sandpile fractal, 2^16 grains toppled to rest
"""

import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 400, 300
S = 3  # supersample factor for smooth pieces
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "images")

FONT_DIR = "/usr/share/fonts/truetype"
F_SANS_B = f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf"
F_SANS = f"{FONT_DIR}/dejavu/DejaVuSans.ttf"
F_SERIF_B = f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = f"{FONT_DIR}/dejavu/DejaVuSerif.ttf"
F_MONO = f"{FONT_DIR}/dejavu/DejaVuSansMono.ttf"
F_MONO_B = f"{FONT_DIR}/dejavu/DejaVuSansMono-Bold.ttf"
F_JP = f"{FONT_DIR}/fonts-japanese-gothic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def palette_img():
    p = Image.new("P", (1, 1))
    p.putpalette(list(WHITE) + list(BLACK) + list(RED) + list(BLACK) * 253)
    return p


PAL = palette_img()


def finish(img, dither=False, name="x.png"):
    """Downscale if supersampled, snap to the 3-color palette, save."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    q = img.convert("RGB").quantize(
        palette=PAL, dither=Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    )
    q.save(os.path.join(OUT, name), optimize=True)
    print("saved", name)


def rotated_text(base, xy, text, fnt, angle, fill, anchor="mm"):
    """Draw rotated text onto base image (RGB)."""
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text(xy, text, font=fnt, fill=fill + (255,), anchor=anchor)
    tmp = tmp.rotate(angle, resample=Image.BICUBIC, center=xy)
    base.paste(tmp, (0, 0), tmp)


# ----------------------------------------------------------------------------
# 1. INDUCTION — constructivist poster, Faraday's ring, 29 Aug 1831
# ----------------------------------------------------------------------------
def img1():
    w, h = W * S, H * S
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)

    # The iron ring: a massive red annulus, off-center to the upper right.
    cx, cy, r_out, r_in = int(w * 0.63), int(h * 0.42), int(h * 0.40), int(h * 0.26)
    d.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], fill=RED)
    d.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], fill=WHITE)

    # Primary coil: black winding bars across the left limb of the ring.
    rm = (r_out + r_in) / 2
    for k in range(-4, 5):
        ang = math.radians(180 + k * 9)
        px, py = cx + rm * math.cos(ang), cy + rm * math.sin(ang)
        bw, bl = int(h * 0.012), (r_out - r_in) * 0.75
        dx, dy = math.cos(ang), math.sin(ang)
        d.line([px - dx * bl, py - dy * bl, px + dx * bl, py + dy * bl],
               fill=BLACK, width=bw * 2)
    # Secondary coil: winding bars on the right limb.
    for k in range(-4, 5):
        ang = math.radians(0 + k * 9)
        px, py = cx + rm * math.cos(ang), cy + rm * math.sin(ang)
        bw, bl = int(h * 0.012), (r_out - r_in) * 0.75
        dx, dy = math.cos(ang), math.sin(ang)
        d.line([px - dx * bl, py - dy * bl, px + dx * bl, py + dy * bl],
               fill=BLACK, width=bw * 2)

    # The black diagonal — the wedge of current — piercing the composition.
    bar_w = int(h * 0.055)
    x0, y0 = int(-w * 0.05), int(h * 0.98)
    x1, y1 = int(w * 0.74), int(h * 0.04)
    d.line([x0, y0, x1, y1], fill=BLACK, width=bar_w)
    # Arrowhead at the top of the diagonal.
    ang = math.atan2(y1 - y0, x1 - x0)
    ah = h * 0.09
    for spread in (math.radians(150), math.radians(-150)):
        d.line([x1, y1,
                x1 + ah * math.cos(ang + spread), y1 + ah * math.sin(ang + spread)],
               fill=BLACK, width=bar_w)

    # Galvanometer kick: a red spark polyline leaping off the secondary side.
    spark = [(cx + r_out * 0.72, cy + r_out * 0.72)]
    sx, sy = spark[0]
    rnd = random.Random(1831)
    for i in range(5):
        sx += w * 0.030
        sy += h * 0.055 + (h * 0.045) * (1 if i % 2 == 0 else -1) * rnd.uniform(0.6, 1.2)
        spark.append((sx, sy))
    d.line(spark, fill=RED, width=int(h * 0.020), joint="curve")

    # Small black counter-circle, lower left (Lissitzky loved these).
    d.ellipse([w * 0.10 - h * 0.045, h * 0.72 - h * 0.045,
               w * 0.10 + h * 0.045, h * 0.72 + h * 0.045], fill=BLACK)

    # Typography.
    rotated_text(im, (w * 0.40, h * 0.60), "INDUCTION",
                 font(F_SANS_B, int(h * 0.135)), 34.5, BLACK)
    d = ImageDraw.Draw(im)
    d.text((w * 0.035, h * 0.045), "29 VIII 1831", font=font(F_SANS_B, int(h * 0.07)),
           fill=BLACK)
    d.text((w * 0.035, h * 0.125), "M. FARADAY WINDS\nTWO COILS ON ONE\nIRON RING",
           font=font(F_MONO, int(h * 0.036)), fill=BLACK)
    d.text((w * 0.97, h * 0.96),
           "195 YEARS OF THE TRANSFORMER · ROYAL INSTITUTION, LONDON",
           font=font(F_MONO, int(h * 0.033)), fill=BLACK, anchor="rs")
    finish(im, dither=False, name="1.png")


# ----------------------------------------------------------------------------
# 2. SEIGAIHA — blue-ocean-waves pattern (in black & white), red sun rising
# ----------------------------------------------------------------------------
def img2():
    w, h = W * S, H * S
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)
    rnd = random.Random(20260829)

    horizon = h * 0.30

    # Sky: white, with a large red sun and thin black cloud slats.
    sun_r = h * 0.16
    sun_x, sun_y = w * 0.70, horizon - h * 0.02
    d.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r], fill=RED)

    # Sea: rows of seigaiha fans, back (small) to front (large), each row
    # overlapping the previous. A unit is a filled circle with nested rings.
    n_rings = 4
    y = horizon
    row = 0
    while y < h + h * 0.2:
        t = (y - horizon) / (h - horizon)  # 0 at horizon, 1 at bottom
        R = h * (0.035 + 0.085 * t)  # circle radius grows toward viewer
        step_x = R * 2
        y += R * 0.75  # rows overlap: circles sit deep in the previous row
        off = (row % 2) * R  # half-unit offset per row
        x = -R + (off - step_x)
        while x < w + step_x:
            # Occasionally a whole fan is red — a catch of sunlight.
            hot = rnd.random() < 0.055 and t > 0.05
            ring_fill = [WHITE, RED][hot]
            d.ellipse([x - R, y - R, x + R, y + R], fill=BLACK)
            for i in range(n_rings):
                rr = R * (1 - (i + 0.55) / n_rings)
                col = ring_fill if i % 2 == 0 else BLACK
                if i == n_rings - 1:
                    col = ring_fill
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col)
            x += step_x
        row += 1

    # Caption: 青海波 (seigaiha), vertical, upper left.
    jp = font(F_JP, int(h * 0.085))
    for i, ch in enumerate("青海波"):
        d.text((w * 0.055, h * 0.035 + i * h * 0.095), ch, font=jp, fill=BLACK)
    d.text((w * 0.055 + h * 0.005, h * 0.035 + 3 * h * 0.095 + h * 0.01), "SEIGAIHA",
           font=font(F_MONO, int(h * 0.028)), fill=BLACK)
    finish(im, dither=False, name="2.png")


# ----------------------------------------------------------------------------
# 3. MOON & SATURN — tonight through an eyepiece
# ----------------------------------------------------------------------------
def img3():
    w, h = W * S, H * S
    im = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(im)
    rnd = random.Random(829)

    # Star field.
    for _ in range(140):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice([1, 1, 1, 2, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

    # The Moon: 96% waning gibbous. Build as grayscale disk with craters,
    # then shave a bright sliver off the western limb with a dark ellipse.
    mr = int(h * 0.30)
    mx, my = int(w * 0.36), int(h * 0.46)
    moon = Image.new("L", (mr * 2, mr * 2), 0)
    md = ImageDraw.Draw(moon)
    md.ellipse([0, 0, mr * 2, mr * 2], fill=225)
    # Maria: big soft dark blotches.
    for _ in range(9):
        a = rnd.uniform(0, 2 * math.pi)
        rad = rnd.uniform(0.15, 0.62) * mr
        bx, by = mr + rad * math.cos(a), mr + rad * math.sin(a)
        br = rnd.uniform(0.14, 0.34) * mr
        blot = Image.new("L", moon.size, 0)
        bd = ImageDraw.Draw(blot)
        bd.ellipse([bx - br, by - br, bx + br, by + br], fill=60)
        moon = Image.composite(Image.new("L", moon.size, 168), moon, blot.point(lambda v: v))
        md = ImageDraw.Draw(moon)
    # Craters: rings.
    for _ in range(26):
        a = rnd.uniform(0, 2 * math.pi)
        rad = rnd.uniform(0, 0.85) * mr
        bx, by = mr + rad * math.cos(a), mr + rad * math.sin(a)
        br = rnd.uniform(0.02, 0.09) * mr
        md.ellipse([bx - br, by - br, bx + br, by + br], outline=120,
                   width=max(2, int(br * 0.35)))
    # Mask to disk, terminator: waning gibbous — dark sliver on the east limb.
    mask = Image.new("L", moon.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, mr * 2, mr * 2], fill=255)
    term = ImageDraw.Draw(moon)
    # 96% waning: shave a thin dark sliver off the eastern limb with a big
    # circle whose edge dips only ~0.16 mr into the disk
    term.ellipse([mr * 1.68, -mr * 2.0, mr * 7.68, mr * 4.0], fill=4)
    im.paste(ImageOps.colorize(moon, BLACK, WHITE), (mx - mr, my - mr), mask)
    d = ImageDraw.Draw(im)

    # Saturn: upper right of the moon, ~20x exaggerated, rings nearly edge-on-ish tilt.
    sx, sy = int(w * 0.76), int(h * 0.30)
    sr = int(h * 0.045)
    sat = Image.new("RGBA", (sr * 8, sr * 8), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sat)
    c = sr * 4
    sd.ellipse([c - sr * 2.3, c - sr * 0.62, c + sr * 2.3, c + sr * 0.62],
               outline=WHITE + (255,), width=max(2, int(sr * 0.16)))
    sd.ellipse([c - sr, c - sr, c + sr, c + sr], fill=BLACK + (255,))
    sd.ellipse([c - sr * 0.92, c - sr * 0.92, c + sr * 0.92, c + sr * 0.92],
               fill=WHITE + (255,))
    sd.line([c - sr * 0.9, c + sr * 0.35, c + sr * 0.9, c + sr * 0.35],
            fill=BLACK + (255,), width=max(2, int(sr * 0.10)))
    sat = sat.rotate(-18, resample=Image.BICUBIC)
    im.paste(sat, (sx - sr * 4, sy - sr * 4), sat)

    # Eyepiece reticle: red crosshairs + circle, thin.
    d = ImageDraw.Draw(im)
    rw = max(2, S)
    d.ellipse([w * 0.5 - h * 0.47, h * 0.5 - h * 0.47, w * 0.5 + h * 0.47,
               h * 0.5 + h * 0.47], outline=RED, width=rw)
    for x0, y0, x1, y1 in [(w * 0.5, h * 0.02, w * 0.5, h * 0.14),
                           (w * 0.5, h * 0.86, w * 0.5, h * 0.98),
                           (w * 0.5 - h * 0.48, h * 0.5, w * 0.5 - h * 0.36, h * 0.5),
                           (w * 0.5 + h * 0.36, h * 0.5, w * 0.5 + h * 0.48, h * 0.5)]:
        d.line([x0, y0, x1, y1], fill=RED, width=rw)

    # Labels.
    mono = font(F_MONO, int(h * 0.037))
    d.text((mx, my + mr + h * 0.035), "MOON · 96% · WANING GIBBOUS", font=mono,
           fill=WHITE, anchor="mm")
    d.text((sx, sy - sr * 3.2), "SATURN", font=mono, fill=WHITE, anchor="mm")
    d.text((w * 0.03, h * 0.945), "2026·08·29", font=font(F_MONO_B, int(h * 0.04)),
           fill=RED)
    d.text((w * 0.97, h * 0.945), "TOGETHER IN THE SOUTHEAST, LATE EVENING",
           font=font(F_MONO, int(h * 0.032)), fill=WHITE, anchor="rm")
    finish(im, dither=True, name="3.png")


# ----------------------------------------------------------------------------
# 4. TICKET STUB — The Beatles, Candlestick Park, 29 Aug 1966 (60 years)
# ----------------------------------------------------------------------------
def img4():
    w, h = W * S, H * S
    im = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(im)

    # Halftone-ish dotted background.
    for yy in range(0, h, int(h * 0.028)):
        for xx in range(0, w, int(h * 0.028)):
            if (xx // int(h * 0.028) + yy // int(h * 0.028)) % 2 == 0:
                d.ellipse([xx, yy, xx + S, yy + S], fill=WHITE)

    # Ticket body, slightly rotated for a tossed-on-the-desk feel.
    tw, th = int(w * 0.92), int(h * 0.62)
    ticket = Image.new("RGB", (tw, th), WHITE)
    td = ImageDraw.Draw(ticket)
    bord = int(h * 0.012)
    td.rectangle([bord, bord, tw - bord, th - bord], outline=RED, width=bord)
    td.rectangle([bord * 2.6, bord * 2.6, tw - bord * 2.6, th - bord * 2.6],
                 outline=BLACK, width=int(bord * 0.5))

    # Perforation + stub at the right.
    stub_x = int(tw * 0.76)
    dash = int(th * 0.035)
    yy = bord * 3
    while yy < th - bord * 3:
        td.line([stub_x, yy, stub_x, yy + dash], fill=BLACK, width=int(bord * 0.5))
        yy += dash * 2
    # Stub content, rotated 90°.
    stub = Image.new("RGB", (th, tw - stub_x), WHITE)
    sd = ImageDraw.Draw(stub)
    sd.text((th // 2, (tw - stub_x) // 2 - int(th * 0.05)), "SEC 12 · ROW B · SEAT 29",
            font=font(F_MONO_B, int(th * 0.062)), fill=BLACK, anchor="mm")
    sd.text((th // 2, (tw - stub_x) // 2 + int(th * 0.05)), "EST. PRICE $4.50",
            font=font(F_MONO, int(th * 0.055)), fill=RED, anchor="mm")
    stub = stub.rotate(90, expand=True)
    ticket.paste(stub.crop((0, int(th * 0.06), stub.width, stub.height - int(th * 0.06))),
                 (stub_x + int(bord * 1.5), int(th * 0.06)))

    # Main face.
    cxm = (bord * 3 + stub_x) // 2
    td.text((cxm, th * 0.155), "CANDLESTICK PARK · SAN FRANCISCO",
            font=font(F_MONO, int(th * 0.055)), fill=BLACK, anchor="mm")
    td.text((cxm, th * 0.33), "THE BEATLES", font=font(F_SERIF_B, int(th * 0.19)),
            fill=RED, anchor="mm")
    td.line([cxm - tw * 0.3, th * 0.445, cxm + tw * 0.3, th * 0.445], fill=BLACK,
            width=int(bord * 0.5))
    td.text((cxm, th * 0.53), "IN PERSON · FINAL CONCERT",
            font=font(F_SANS_B, int(th * 0.062)), fill=BLACK, anchor="mm")
    td.text((cxm, th * 0.68), "MONDAY AUGUST 29, 1966 · 8 P.M.",
            font=font(F_MONO_B, int(th * 0.06)), fill=BLACK, anchor="mm")
    td.text((cxm, th * 0.84), "11 SONGS · 33 MINUTES · THEN NEVER AGAIN",
            font=font(F_MONO, int(th * 0.048)), fill=BLACK, anchor="mm")

    ticket = ticket.rotate(2.4, resample=Image.BICUBIC, expand=True,
                           fillcolor=(1, 2, 3))
    tmask = Image.new("L", ticket.size, 0)
    # mask out the fill color introduced by expand
    px = ticket.load()
    npx = np.array(ticket)
    mask_arr = ((npx[:, :, 0] != 1) | (npx[:, :, 1] != 2) | (npx[:, :, 2] != 3))
    tmask = Image.fromarray((mask_arr * 255).astype(np.uint8))
    im.paste(ticket, ((w - ticket.width) // 2, int(h * 0.10)), tmask)

    d = ImageDraw.Draw(im)
    d.text((w * 0.5, h * 0.055), "60 YEARS AGO TONIGHT",
           font=font(F_MONO_B, int(h * 0.045)), fill=RED, anchor="mm")
    d.text((w * 0.5, h * 0.945),
           "THEY CLOSED WITH LONG TALL SALLY AND WALKED OFF FOREVER",
           font=font(F_MONO, int(h * 0.032)), fill=WHITE, anchor="mm")
    finish(im, dither=False, name="4.png")


# ----------------------------------------------------------------------------
# 5. SANDPILE — abelian sandpile, 2^16 grains dropped on one cell
# ----------------------------------------------------------------------------
def img5():
    N = 2 ** 16
    G = 161  # odd grid so the pile is centered on a cell
    grid = np.zeros((G, G), dtype=np.int64)
    grid[G // 2, G // 2] = N
    while True:
        over = grid >= 4
        if not over.any():
            break
        spill = grid // 4 * over
        grid -= spill * 4
        grid[1:, :] += spill[:-1, :]
        grid[:-1, :] += spill[1:, :]
        grid[:, 1:] += spill[:, :-1]
        grid[:, :-1] += spill[:, 1:]

    # Crop to the occupied square, keep a small margin.
    occ = np.argwhere(grid > 0)
    r0, c0 = occ.min(axis=0)
    r1, c1 = occ.max(axis=0)
    pad = 2
    grid = grid[max(0, r0 - pad):r1 + pad + 1, max(0, c0 - pad):c1 + pad + 1]

    # Map heights to the palette: 0 white, 1 red, 2 white, 3 black —
    # the 3s draw the fractal filigree, the 1s thread red through it.
    lut = {0: WHITE, 1: RED, 2: WHITE, 3: BLACK}
    gh, gw = grid.shape
    arr = np.zeros((gh, gw, 3), dtype=np.uint8)
    for v, col in lut.items():
        arr[grid == v] = col
    pile = Image.fromarray(arr, "RGB")

    # Fill the panel height (nearest-neighbor; slight cell unevenness is fine).
    target_h = H - 40
    scale = target_h / gh
    pile = pile.resize((int(gw * scale), target_h), Image.NEAREST)

    im = Image.new("RGB", (W, H), WHITE)
    px = (W - pile.width) // 2
    py = (H - 30 - pile.height) // 2
    im.paste(pile, (px, py))
    d = ImageDraw.Draw(im)
    d.rectangle([px - 2, py - 2, px + pile.width + 1, py + pile.height + 1],
                outline=BLACK, width=1)
    d.text((W // 2, H - 16), "ABELIAN SANDPILE · 65536 GRAINS · ONE CELL",
           font=font(F_MONO, 11), fill=BLACK, anchor="mm")
    finish(im, dither=False, name="5.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    img1()
    img2()
    img3()
    img4()
    img5()
    # Archive copies alongside this script.
    for i in range(1, 6):
        Image.open(os.path.join(OUT, f"{i}.png")).save(os.path.join(HERE, f"{i}.png"))
    print("done")
