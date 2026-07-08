#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-08.

Five 400x300 images in exactly three colors (white, black, red).

Today: 15 years since the final Space Shuttle launch (STS-135, 8 July 2011),
Count Ferdinand von Zeppelin's birthday (1838), the kamon generator from the
backlog, this morning's half-moon standing by Saturn, and Truchet tiles.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"

SEED = 20260708


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


def rotated_text(base, center, text, fnt, angle, fill):
    """Draw text rotated by `angle` degrees, centered on `center`."""
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text(center, text, font=fnt, fill=tuple(fill) + (255,), anchor="mm")
    tmp = tmp.rotate(angle, center=center, resample=Image.BICUBIC)
    base.paste(tmp, (0, 0), tmp)


# ------------------------------------------------- 1. The Final Ascent (STS-135)
def image1_final_ascent():
    """Lissitzky-style constructivist poster: the red wedge is the last shuttle
    climbing into the black circle of space. 8 July 2011 + 15 years."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    ccx, ccy, cr = 293 * s, 128 * s, 84 * s

    # thin rules parallel to the wedge, running off-canvas
    ang = math.atan2((128 - 62) * s, (300 - 0) * s)

    def line_through(px, py, width, fill):
        dx, dy = math.cos(ang), math.sin(ang)
        dr.line(
            [px - dx * 900 * s, py - dy * 900 * s, px + dx * 900 * s, py + dy * 900 * s],
            fill=fill, width=width,
        )

    line_through(0, 30 * s, s, BLACK)

    # the black circle of space
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=BLACK)
    # a dotted orbit around it
    orr = cr + 10 * s
    for k in range(64):
        a = 2 * math.pi * k / 64
        if 0.35 < a < 2.1:  # leave a gap where the wedge enters
            continue
        px, py = ccx + orr * math.cos(a), ccy + orr * math.sin(a)
        dr.ellipse([px - 1.2 * s, py - 1.2 * s, px + 1.2 * s, py + 1.2 * s], fill=BLACK)

    # the red wedge — base on the left edge, apex driven into the circle
    apex = (302 * s, 130 * s)
    dr.polygon([(-8 * s, 26 * s), (-8 * s, 100 * s), apex], fill=RED)

    # the orbiter, abstracted: a small white delta escaping ahead of the wedge
    dx, dy = math.cos(ang), math.sin(ang)
    nx, ny = -dy, dx
    tipx, tipy = 342 * s, 138 * s
    b = 14 * s
    dr.polygon(
        [
            (tipx + dx * b * 1.5, tipy + dy * b * 1.5),
            (tipx - dx * b + nx * b * 0.62, tipy - dy * b + ny * b * 0.62),
            (tipx - dx * b - nx * b * 0.62, tipy - dy * b - ny * b * 0.62),
        ],
        fill=WHITE,
    )

    # small red moon and black bar, lower right — counterweight
    dr.ellipse([352 * s, 232 * s, 376 * s, 256 * s], fill=RED)
    dr.rectangle([330 * s, 264 * s, 398 * s, 268 * s], fill=BLACK)

    # typography
    dr.text((16 * s, 168 * s), "STS·135", font=font(FONT_SANS_B, 46 * s), fill=BLACK)
    dr.rectangle([18 * s, 222 * s, 150 * s, 226 * s], fill=RED)
    dr.text((16 * s, 232 * s), "THE FINAL ASCENT", font=font(FONT_SANS_B, 15 * s), fill=BLACK)
    dr.text(
        (16 * s, 256 * s),
        "ATLANTIS LEFT PAD 39A ON 8 JULY 2011.\n135 FLIGHTS · 1981–2011 · 15 YEARS AGO TODAY",
        font=font(FONT_MONO, 9 * s), fill=BLACK, spacing=4 * s,
    )
    rotated_text(
        img, (150 * s, 46 * s), "БЫСТРЕЕ ВВЕРХ — FASTER, UPWARD",
        font(FONT_MONO, 9 * s), -math.degrees(ang), BLACK,
    )
    return finalize(img, dither=False)


# ------------------------------------------------------------- 2. Zeppelin poster
def image2_zeppelin():
    """Travel-poster zeppelin crossing a red sun over seigaiha clouds.
    Ferdinand von Zeppelin, b. 8 July 1838."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # red sun
    scx, scy, sr = 272 * s, 118 * s, 86 * s
    dr.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=RED)

    # zeppelin hull: nose right, tapered tail left
    hcx, hcy = 205 * s, 128 * s
    ha, hb = 138 * s, 24 * s  # half-length, half-height
    pts_top, pts_bot = [], []
    for i in range(81):
        t = -1 + 2 * i / 80  # -1 tail .. +1 nose
        w = (1 - t * t) ** (0.62 if t > 0 else 0.85)
        x = hcx + t * ha
        pts_top.append((x, hcy - hb * w))
        pts_bot.append((x, hcy + hb * w))
    dr.polygon(pts_top + pts_bot[::-1], fill=BLACK)

    # tail fins
    tx = hcx - ha
    dr.polygon([(tx + 40 * s, hcy - 14 * s), (tx - 4 * s, hcy - 30 * s),
                (tx + 12 * s, hcy - 2 * s)], fill=BLACK)
    dr.polygon([(tx + 40 * s, hcy + 14 * s), (tx - 4 * s, hcy + 30 * s),
                (tx + 12 * s, hcy + 2 * s)], fill=BLACK)

    # hull panel lines (white)
    for tf in (-0.62, -0.28, 0.06, 0.4, 0.7):
        x = hcx + tf * ha
        w = (1 - tf * tf) ** (0.62 if tf > 0 else 0.85)
        dr.line([x, hcy - hb * w + 2 * s, x, hcy + hb * w - 2 * s], fill=WHITE, width=s)
    dr.line([hcx - ha * 0.75, hcy, hcx + ha * 0.92, hcy], fill=WHITE, width=s)

    # gondola
    gx = hcx + 20 * s
    dr.rounded_rectangle([gx - 26 * s, hcy + hb - 2 * s, gx + 26 * s, hcy + hb + 10 * s],
                         radius=4 * s, fill=BLACK)
    for k in range(4):
        wx = gx - 18 * s + k * 12 * s
        dr.rectangle([wx, hcy + hb + 1 * s, wx + 5 * s, hcy + hb + 5 * s], fill=WHITE)

    # seigaiha cloud band along the bottom (rows painted back to front)
    r0, dxs, dys = 34 * s, 44 * s, 16 * s
    y = 212 * s
    row = 0
    while y < H * s + r0:
        off = (row % 2) * (dxs // 2)
        x = -off
        while x < W * s + r0:
            dr.ellipse([x - r0, y - r0, x + r0, y + r0], fill=WHITE, outline=BLACK, width=2 * s)
            for rr in (24 * s, 14 * s, 5 * s):
                dr.ellipse([x - rr, y - rr, x + rr, y + rr], outline=BLACK, width=2 * s)
            x += dxs
        y += dys
        row += 1

    # typography
    dr.text((16 * s, 14 * s), "ZEPPELIN", font=font(FONT_SERIF_B, 40 * s), fill=BLACK)
    dr.rectangle([19 * s, 62 * s, 31 * s, 74 * s], fill=RED)
    dr.text((38 * s, 62 * s), "GRAF FERDINAND VON ZEPPELIN",
            font=font(FONT_SANS_B, 12 * s), fill=BLACK)
    dr.text((38 * s, 78 * s), "b. 8 JULY 1838 · KONSTANZ, BODENSEE",
            font=font(FONT_MONO, 10 * s), fill=BLACK)
    return finalize(img, dither=False)


# ------------------------------------------------------------------- 3. Kamon six
def kamon_layer(rng, size):
    """One generated crest as an L-mode ink mask (255 = ink) of size x size."""
    n = rng.choice([3, 4, 5, 5, 6, 6, 8, 12])
    c = size // 2
    R = size * 0.46  # motif radius

    single = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(single)

    motif = rng.choice(["petal", "teardrop", "crescent", "diamond", "ray"])
    dist = R * rng.uniform(0.42, 0.58)
    if motif == "petal":
        a, b = R * rng.uniform(0.30, 0.42), R * rng.uniform(0.16, 0.26)
        d.ellipse([c - b, c - dist - a, c + b, c - dist + a], fill=255)
        if rng.random() < 0.5:  # hollow petal
            a2, b2 = a * 0.55, b * 0.5
            d.ellipse([c - b2, c - dist - a2, c + b2, c - dist + a2], fill=0)
    elif motif == "teardrop":
        a, b = R * rng.uniform(0.32, 0.44), R * rng.uniform(0.18, 0.28)
        d.ellipse([c - b, c - dist - a * 0.6, c + b, c - dist + a], fill=255)
        d.polygon([(c - b * 0.8, c - dist - a * 0.4), (c, c - dist - a * 1.5),
                   (c + b * 0.8, c - dist - a * 0.4)], fill=255)
    elif motif == "crescent":
        rr = R * rng.uniform(0.26, 0.34)
        cy = c - dist
        d.ellipse([c - rr, cy - rr, c + rr, cy + rr], fill=255)
        sh = rr * 0.45
        d.ellipse([c - rr + sh * 0.6, cy - rr + sh, c + rr + sh * 0.6, cy + rr + sh], fill=0)
    elif motif == "diamond":
        a, b = R * rng.uniform(0.3, 0.42), R * rng.uniform(0.18, 0.3)
        cy = c - dist
        d.polygon([(c, cy - a), (c + b, cy), (c, cy + a), (c - b, cy)], fill=255)
        if rng.random() < 0.5:
            d.polygon([(c, cy - a * 0.5), (c + b * 0.5, cy), (c, cy + a * 0.5),
                       (c - b * 0.5, cy)], fill=0)
    else:  # ray
        wdt = max(2, int(R * rng.uniform(0.05, 0.1)))
        d.line([c, c - R * 0.18, c, c - R * 0.92], fill=255, width=wdt * 2)
        d.ellipse([c - wdt * 1.6, c - R * 0.95 - wdt, c + wdt * 1.6, c - R * 0.95 + wdt],
                  fill=255)

    ink = Image.new("L", (size, size), 0)
    for k in range(n):
        rot = single.rotate(360 * k / n, center=(c, c), resample=Image.BICUBIC)
        ink = Image.composite(Image.new("L", ink.size, 255), ink, rot.point(lambda v: 255 if v > 96 else 0))

    d2 = ImageDraw.Draw(ink)
    # dots between motifs
    if rng.random() < 0.55:
        dd = R * rng.uniform(0.62, 0.8)
        rr = R * rng.uniform(0.05, 0.09)
        for k in range(n):
            a = 2 * math.pi * (k + 0.5) / n - math.pi / 2
            px, py = c + dd * math.cos(a), c + dd * math.sin(a)
            d2.ellipse([px - rr, py - rr, px + rr, py + rr], fill=255)
    # center: dot or ring
    if rng.random() < 0.6:
        rr = R * rng.uniform(0.1, 0.17)
        d2.ellipse([c - rr, c - rr, c + rr, c + rr], fill=255)
    else:
        rr = R * rng.uniform(0.14, 0.2)
        wd = max(2, int(R * 0.05))
        d2.ellipse([c - rr, c - rr, c + rr, c + rr], outline=255, width=wd)
    # enclosing ring
    if rng.random() < 0.65:
        wd = max(3, int(R * rng.uniform(0.05, 0.09)))
        d2.ellipse([c - R, c - R, c + R, c + R], outline=255, width=wd)
        if rng.random() < 0.4:
            d2.ellipse([c - R + wd * 2.2, c - R + wd * 2.2, c + R - wd * 2.2, c + R - wd * 2.2],
                       outline=255, width=max(2, wd // 2))
    return ink


def image3_kamon():
    """Six generated family crests, seeded by the date."""
    rng = random.Random(SEED)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    centers = [(70, 72), (200, 72), (330, 72), (70, 190), (200, 190), (330, 190)]
    disc_r = 52
    styles = ["bw", "bw", "bw", "rw", "wb", "bw"]
    rng.shuffle(styles)

    for (cx, cy), style in zip(centers, styles):
        cx, cy, r = cx * s, cy * s, disc_r * s
        ink = kamon_layer(rng, 2 * r)
        if style == "wb":
            # black disc with white ring border, white motif
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2 * s)
            color = WHITE
        else:
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
            color = RED if style == "rw" else BLACK
        # crest slightly smaller than the disc
        m = int(2 * r * 0.86)
        ink = ink.resize((m, m), Image.LANCZOS)
        block = Image.new("RGB", (m, m), color)
        img.paste(block, (cx - m // 2, cy - m // 2), ink)

    dr.text((16 * s, 258 * s), "家紋", font=font(FONT_JP, 26 * s), fill=RED)
    dr.text((82 * s, 262 * s), "KAMON — six family crests that never existed",
            font=font(FONT_SERIF, 12 * s), fill=WHITE)
    dr.text((82 * s, 280 * s), f"drawn from seed {SEED}",
            font=font(FONT_MONO, 9 * s), fill=WHITE)
    return finalize(img, dither=False)


# ---------------------------------------------------------- 4. Moon & Saturn dawn
def image4_moon_saturn():
    """This morning's sky: the waning half-moon beside Saturn."""
    rng = random.Random(SEED + 4)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # stars
    for _ in range(150):
        x, y = rng.uniform(0, W * s), rng.uniform(0, 195 * s)
        r = rng.choice([0.5, 0.7, 0.9, 1.3]) * s
        v = rng.randint(120, 255)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # moon
    mcx, mcy, mr = 128 * s, 108 * s, 64 * s
    dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=(205, 205, 205))
    # maria
    for _ in range(10):
        a = rng.uniform(0, 2 * math.pi)
        d0 = rng.uniform(0, 0.62) * mr
        bx, by = mcx + d0 * math.cos(a), mcy + d0 * math.sin(a)
        br = rng.uniform(0.12, 0.3) * mr
        g = rng.randint(148, 172)
        dr.ellipse([bx - br, by - br * 0.8, bx + br, by + br * 0.8], fill=(g, g, g))
    # craters
    for _ in range(26):
        a = rng.uniform(0, 2 * math.pi)
        d0 = rng.uniform(0, 0.88) * mr
        bx, by = mcx + d0 * math.cos(a), mcy + d0 * math.sin(a)
        br = rng.uniform(0.02, 0.07) * mr
        g = rng.choice([135, 150, 228, 238])
        dr.ellipse([bx - br, by - br, bx + br, by + br], outline=(g, g, g), width=s)

    # terminator: waning, lit on the left, 47% illuminated
    f = 0.47
    k = 2 * f - 1  # signed bulge of the terminator
    px = img.load()
    for yy in range(int(mcy - mr), int(mcy + mr) + 1):
        dy = yy - mcy
        ch = math.sqrt(max(0.0, mr * mr - dy * dy))
        xt = mcx + k * ch
        for xx in range(int(xt), int(mcx + ch) + 1):
            # soften the edge slightly; the dither will do the rest
            t = min(1.0, (xx - xt) / (6.0 * s))
            r0, g0, b0 = px[xx, yy]
            v = int(r0 * (1 - t) + 10 * t)
            px[xx, yy] = (v, v, v)

    dr.text((mcx - mr, mcy + mr + 8 * s), "MOON · 47% · WANING",
            font=font(FONT_MONO, 10 * s), fill=WHITE)

    # Saturn
    scx, scy = 300 * s, 78 * s
    for rr, tilt in ((26 * s, 0.32),):
        dr.ellipse([scx - rr, scy - rr * tilt, scx + rr, scy + rr * tilt],
                   outline=(230, 230, 230), width=s)
        dr.ellipse([scx - rr + 5 * s, scy - (rr - 5 * s) * tilt, scx + rr - 5 * s,
                    scy + (rr - 5 * s) * tilt], outline=(180, 180, 180), width=s)
    br = 10 * s
    dr.ellipse([scx - br, scy - br, scx + br, scy + br], fill=(235, 235, 235))
    dr.text((scx - 24 * s, scy + 22 * s), "SATURN", font=font(FONT_MONO, 10 * s), fill=WHITE)

    # caption block
    dr.line([16 * s, 208 * s, 384 * s, 208 * s], fill=(150, 150, 150), width=s)
    dr.text((16 * s, 216 * s), "BEFORE DAWN — 8 JULY 2026",
            font=font(FONT_SERIF_B, 16 * s), fill=WHITE)
    dr.text((16 * s, 240 * s),
            "The waning half-moon stands beside Saturn, high in the southeast.",
            font=font(FONT_SANS, 11 * s), fill=(220, 220, 220))
    dr.text((16 * s, 260 * s), "JUL 9", font=font(FONT_MONO, 10 * s), fill=RED)
    dr.text((58 * s, 260 * s), "Venus brushes Regulus at dusk",
            font=font(FONT_MONO, 10 * s), fill=(200, 200, 200))
    dr.text((16 * s, 276 * s), "JUL 14", font=font(FONT_MONO, 10 * s), fill=RED)
    dr.text((58 * s, 276 * s), "New supermoon — the month's darkest sky",
            font=font(FONT_MONO, 10 * s), fill=(200, 200, 200))
    return finalize(img, dither=True)


# ------------------------------------------------------------- 5. Truchet rivers
def image5_truchet():
    """Truchet arc tiles; a few enclosed pools flooded red."""
    rng = random.Random(SEED + 5)
    s = SS
    tile = 25
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    lw = int(3.4 * s)

    for gy in range(H // tile):
        for gx in range(W // tile):
            x0, y0 = gx * tile * s, gy * tile * s
            x1, y1 = x0 + tile * s, y0 + tile * s
            t = tile * s
            if rng.random() < 0.5:
                dr.arc([x0 - t // 2, y0 - t // 2, x0 + t // 2, y0 + t // 2],
                       0, 90, fill=BLACK, width=lw)
                dr.arc([x1 - t // 2, y1 - t // 2, x1 + t // 2, y1 + t // 2],
                       180, 270, fill=BLACK, width=lw)
            else:
                dr.arc([x1 - t // 2, y0 - t // 2, x1 + t // 2, y0 + t // 2],
                       90, 180, fill=BLACK, width=lw)
                dr.arc([x0 - t // 2, y1 - t // 2, x0 + t // 2, y1 + t // 2],
                       270, 360, fill=BLACK, width=lw)

    out = finalize(img, dither=False).convert("RGB")

    # flood a handful of enclosed white pools with red
    px = out.load()
    filled = 0
    attempts = 0
    while filled < 6 and attempts < 400:
        attempts += 1
        sx, sy = rng.randrange(W), rng.randrange(H)
        if px[sx, sy] != WHITE:
            continue
        # BFS to measure the region
        seen = {(sx, sy)}
        queue = [(sx, sy)]
        touches_border = False
        while queue and len(seen) <= 6000:
            x, y = queue.pop()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < W and 0 <= ny < H:
                    if (nx, ny) not in seen and px[nx, ny] == WHITE:
                        seen.add((nx, ny))
                        queue.append((nx, ny))
                else:
                    touches_border = True
        if touches_border or not (140 <= len(seen) <= 6000):
            continue
        for x, y in seen:
            px[x, y] = RED
        filled += 1

    return out.quantize(palette=PAL, dither=Image.Dither.NONE)


def main():
    for i, fn in enumerate(
        [image1_final_ascent, image2_zeppelin, image3_kamon,
         image4_moon_saturn, image5_truchet], start=1,
    ):
        im = fn()
        assert im.size == (W, H)
        im.save(f"images/{i}.png", optimize=True)
        print(f"images/{i}.png done")


if __name__ == "__main__":
    main()
