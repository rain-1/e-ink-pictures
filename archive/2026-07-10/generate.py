#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-10.

Theme: ELECTRICITY & SIGNALS. July 10 is Nikola Tesla's birthday (1856 — 170
years today) and the anniversary of Telstar 1 (1962), the satellite that carried
the first live TV across an ocean. Plus tomorrow's pre-dawn moon/Pleiades pass,
a DLA-grown Lichtenberg figure, and a circuit-board Truchet tiling.

Five 400x300 images in exactly three colors (white, black, red).
Tonal scenes render at 3x and downscale; hard-edged pieces stay flat.
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
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


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


# ------------------------------------------------- 1. Tesla 170 (constructivist)
def image1_tesla():
    """Lissitzky-style poster for Tesla's 170th birthday. Red circle = the coil's
    field; a black bolt strikes it; AC sine beats DC flatline along the bottom."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # black diagonal bar, lower-left to upper-right (drawn first: deepest layer)
    bar = [(-20 * s, 268 * s), (10 * s, 292 * s), (420 * s, 92 * s), (390 * s, 68 * s)]
    dr.polygon(bar, fill=BLACK)

    # big red circle over the bar, lower-left of center
    cx, cy, r = 125 * s, 158 * s, 80 * s
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    # white inner ring — makes it read as a field, not a dot
    r2 = 56 * s
    dr.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=WHITE, width=3 * s)

    # lightning bolt from top-right striking the circle's heart
    bolt = [
        (398 * s, -6 * s), (300 * s, 68 * s), (330 * s, 74 * s),
        (218 * s, 136 * s), (240 * s, 141 * s), (122 * s, 200 * s),
        (196 * s, 120 * s), (172 * s, 116 * s), (266 * s, 52 * s),
        (240 * s, 48 * s), (398 * s, -6 * s),
    ]
    dr.polygon(bolt, fill=BLACK)
    # white core inside the bolt tip so it crackles against the red
    dr.line([(212 * s, 130 * s), (146 * s, 186 * s)], fill=WHITE, width=2 * s)

    # typography — clear of the bar, bottom right
    f_big = font(FONT_SANS_B, 40 * s)
    f_num = font(FONT_SANS_B, 54 * s)
    f_sm = font(FONT_MONO, 10 * s)
    dr.text((248 * s, 190 * s), "TESLA", font=f_big, fill=BLACK)
    dr.text((248 * s, 230 * s), "170", font=f_num, fill=RED)

    # AC sine (red, alive) over DC flatline (black, static) — the war of currents
    y0 = 22 * s
    dr.line([(14 * s, y0), (186 * s, y0)], fill=BLACK, width=1 * s)
    pts = []
    for i in range(0, 173):
        x = (14 + i) * s
        y = y0 - math.sin(i / 172 * 4 * math.pi) * 12 * s
        pts.append((x, y))
    dr.line(pts, fill=RED, width=4 * s)
    dr.text((14 * s, 40 * s), "alternating current wins", font=f_sm, fill=BLACK)
    dr.text((14 * s, 54 * s), "b. 10 July 1856, at midnight,", font=f_sm, fill=BLACK)
    dr.text((14 * s, 67 * s), "in a thunderstorm", font=f_sm, fill=BLACK)

    return finalize(img, dither=False)


# ------------------------------------------------- 2. Lichtenberg figure (DLA)
def image2_lichtenberg():
    """A genuine diffusion-limited aggregation cluster — the same physics that
    draws branching discharge patterns in struck acrylic. Grown from a seed,
    newest growth glows red."""
    rng = random.Random(20260710)
    gw, gh = 200, 150
    cx, cy = gw // 2, gh // 2
    grid = [[0] * gw for _ in range(gh)]
    order = {}
    grid[cy][cx] = 1
    order[(cx, cy)] = 0
    max_r = 2.0
    n_target = 6500
    stick_prob = 0.22  # lower sticking probability -> denser, meatier branches
    steps4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neigh8 = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    count = 1
    while count < n_target and max_r < 68:
        rb = max_r + 4
        a = rng.uniform(0, 2 * math.pi)
        x = int(cx + rb * math.cos(a))
        y = int(cy + rb * math.sin(a))
        kill2 = (rb + 12) ** 2
        for _ in range(6000):
            dx, dy = rng.choice(steps4)
            x2, y2 = x + dx, y + dy
            if not (0 < x2 < gw - 1 and 0 < y2 < gh - 1):
                break
            if grid[y2][x2]:
                continue  # blocked by the cluster; try another direction
            x, y = x2, y2
            ddx, ddy = x - cx, y - cy
            if ddx * ddx + ddy * ddy > kill2:
                break
            stuck = False
            for nx, ny in neigh8:
                if grid[y + ny][x + nx]:
                    stuck = True
                    break
            if stuck and rng.random() < stick_prob:
                grid[y][x] = 1
                order[(x, y)] = count
                count += 1
                d = math.hypot(ddx, ddy)
                if d > max_r:
                    max_r = d
                break

    img = Image.new("RGB", (W, H), BLACK)
    px = img.load()
    red_after = count * 0.80  # newest 20% of growth is still hot
    for (x, y), k in order.items():
        c = RED if k >= red_after else WHITE
        for ox in (0, 1):
            for oy in (0, 1):
                X, Y = 2 * x + ox, 2 * y + oy
                if 0 <= X < W and 0 <= Y < H:
                    px[X, Y] = c

    dr = ImageDraw.Draw(img)
    f_t = font(FONT_MONO_B, 13)
    f_s = font(FONT_MONO, 10)
    dr.text((10, 268), "LICHTENBERG FIGURE", font=f_t, fill=WHITE)
    dr.text((10, 284), "electricity always finds a way · est. 1777", font=f_s, fill=RED)
    return finalize(img, dither=False)


# ------------------------------------------------- 3. Telstar 1, 64 years on
def image3_telstar():
    """10 July 1962: a 77 kg faceted sphere relays the first live television
    across the Atlantic. Night-side schematic: two ground stations, one hop."""
    rng = random.Random(1962)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # stars
    for _ in range(130):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, 205 * s)
        r = rng.choice([1, 1, 1, 2])
        dr.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

    # Earth: huge circle whose top arc is the horizon
    ecx, ecy, er = 200 * s, 950 * s, 720 * s
    dr.ellipse([ecx - er, ecy - er, ecx + er, ecy + er], fill=BLACK,
               outline=WHITE, width=2 * s)
    # subtle texture dots inside the earth near the horizon
    for _ in range(500):
        x = rng.uniform(0, W * s)
        y = rng.uniform(232 * s, 300 * s)
        if (x - ecx) ** 2 + (y - ecy) ** 2 < er * er:
            dr.point((x, y), fill=WHITE)

    def horizon_y(x):
        return ecy - math.sqrt(max(er * er - (x - ecx) ** 2, 0))

    # satellite: faceted sphere, upper right of center (clear of the title block)
    scx, scy, sr = 258 * s, 72 * s, 26 * s
    dr.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=WHITE)
    for frac in (-0.55, 0.0, 0.55):  # latitude lines
        yy = scy + sr * frac
        half = sr * math.cos(math.asin(frac))
        dr.line([(scx - half, yy), (scx + half, yy)], fill=BLACK, width=1 * s)
    dr.line([(scx, scy - sr), (scx, scy + sr)], fill=BLACK, width=1 * s)
    # red equator band — the TWT amplifier belt
    dr.line([(scx - sr, scy), (scx + sr, scy)], fill=RED, width=3 * s)
    # tiny antenna nub
    dr.line([(scx, scy - sr), (scx, scy - sr - 8 * s)], fill=WHITE, width=2 * s)

    # ground stations
    ax, bx = 60 * s, 340 * s
    ay, by = horizon_y(ax), horizon_y(bx)
    for gx, gy in ((ax, ay), (bx, by)):
        dr.polygon([(gx - 8 * s, gy), (gx + 8 * s, gy), (gx, gy - 14 * s)], fill=RED)

    # signal: dashed white beams up, red arc hop
    def dashed(p0, p1, dash=7, gap=6, width=2, fill=WHITE):
        x0, y0 = p0
        x1, y1 = p1
        L = math.hypot(x1 - x0, y1 - y0)
        n = int(L / ((dash + gap) * s))
        for i in range(n + 1):
            t0 = i * (dash + gap) * s / L
            t1 = min(t0 + dash * s / L, 1)
            dr.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                     (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=fill, width=width * s)

    dashed((ax, ay - 16 * s), (scx - sr * 0.5, scy + sr * 0.9))
    dashed((scx + sr * 0.5, scy + sr * 0.9), (bx, by - 16 * s))

    f_t = font(FONT_SANS_B, 24 * s)
    f_s = font(FONT_MONO, 10 * s)
    f_l = font(FONT_MONO_B, 10 * s)
    dr.text((14 * s, 12 * s), "TELSTAR 1", font=f_t, fill=WHITE)
    dr.text((14 * s, 40 * s), "10 JUL 1962 · 64 years ago today", font=f_s, fill=RED)
    dr.text((14 * s, 54 * s), "first live TV across an ocean", font=f_s, fill=WHITE)
    dr.text((ax - 46 * s, ay + 10 * s), "ANDOVER, USA", font=f_l, fill=WHITE)
    tw = dr.textlength("PLEUMEUR-BODOU, FR", font=f_l)
    dr.text((min(bx - 46 * s, W * s - tw - 6 * s), by + 10 * s), "PLEUMEUR-BODOU, FR",
            font=f_l, fill=WHITE)
    return finalize(img, dither=False)


# ------------------------------------------------- 4. Moon meets the Pleiades
def image4_almanac():
    """Tomorrow before dawn: a ~10%-lit old crescent slides past the Pleiades,
    with Mars and Saturn strung along the morning line. New supermoon Jul 14."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)
    rng = random.Random(711)

    sky_h = 208
    # faint star field
    for _ in range(110):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, sky_h * s)
        r = rng.choice([1, 1, 2])
        dr.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

    def star4(x, y, r, fill=WHITE, w=2):
        dr.line([(x - r, y), (x + r, y)], fill=fill, width=w * s)
        dr.line([(x, y - r), (x, y + r)], fill=fill, width=w * s)

    # Pleiades — approximate cluster shape (little dipper-like)
    pcx, pcy = 268 * s, 84 * s
    cluster = [("Alcyone", 0, 0, 7), ("Atlas", 26, 10, 6), ("Pleione", 30, 2, 4),
               ("Merope", -12, 16, 6), ("Electra", -34, 8, 6),
               ("Maia", -22, -12, 6), ("Taygeta", -38, -16, 5), ("Celaeno", -30, -4, 3)]
    for name, ox, oy, r in cluster:
        star4(pcx + ox * s, pcy + oy * s, r * s)
    f_l = font(FONT_MONO, 10 * s)
    dr.text((pcx - 34 * s, pcy + 30 * s), "PLEIADES", font=f_l, fill=WHITE)

    # old crescent moon, ~10% lit (sun below eastern horizon = lit on the left-low side)
    mcx, mcy, mr = 118 * s, 108 * s, 34 * s
    dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], outline=WHITE, width=1 * s)
    dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=WHITE)
    # occluding disc offset to leave a left crescent
    off = mr * 0.62
    dr.ellipse([mcx - mr + off, mcy - mr - off * 0.2, mcx + mr + off, mcy + mr - off * 0.2],
               fill=BLACK)
    dr.text((mcx - 30 * s, mcy + mr + 8 * s), "MOON 10%", font=f_l, fill=WHITE)

    # red dotted path moon -> pleiades
    n = 14
    for i in range(n):
        t = i / (n - 1)
        x = mcx + (pcx - mcx) * t
        y = mcy + (pcy - mcy) * t - math.sin(t * math.pi) * 16 * s
        if 0.12 < t < 0.92:
            dr.ellipse([x - 2 * s, y - 2 * s, x + 2 * s, y + 2 * s], fill=RED)

    # Mars (red) and Saturn along the ecliptic, lower left
    mx, my = 52 * s, 168 * s
    dr.ellipse([mx - 5 * s, my - 5 * s, mx + 5 * s, my + 5 * s], fill=RED)
    dr.text((mx - 14 * s, my + 10 * s), "MARS", font=f_l, fill=RED)
    sx, sy = 356 * s, 40 * s
    star4(sx, sy, 7 * s, fill=WHITE, w=2)
    dr.ellipse([sx - 11 * s, sy - 4 * s, sx + 11 * s, sy + 4 * s], outline=WHITE, width=1 * s)
    dr.text((sx - 24 * s, sy + 12 * s), "SATURN", font=f_l, fill=WHITE)

    # horizon line + E marker
    dr.line([(0, sky_h * s), (W * s, sky_h * s)], fill=WHITE, width=1 * s)
    dr.text((374 * s, (sky_h - 16) * s), "E", font=font(FONT_MONO_B, 12 * s), fill=WHITE)

    # white info panel
    dr.rectangle([0, (sky_h + 1) * s, W * s, H * s], fill=WHITE)
    dr.rectangle([0, (sky_h + 1) * s, W * s, (sky_h + 5) * s], fill=RED)
    f_h = font(FONT_SANS_B, 15 * s)
    f_b = font(FONT_SANS, 11 * s)
    dr.text((14 * s, 220 * s), "TOMORROW BEFORE DAWN — SAT 11 JUL", font=f_h, fill=BLACK)
    dr.text((14 * s, 242 * s), "Look east around 4 am: the old crescent moon", font=f_b, fill=BLACK)
    dr.text((14 * s, 257 * s), "glides past the Pleiades, Mars and Saturn nearby.", font=f_b, fill=BLACK)
    dr.text((14 * s, 277 * s), "New supermoon Tue 14 Jul — darkest sky of the month.",
            font=font(FONT_SANS_B, 11 * s), fill=RED)
    return finalize(img, dither=False)


# ------------------------------------------------- 5. Circuit Truchet
def image5_circuit_truchet():
    """Truchet arcs drawn as printed-circuit traces, seeded by today's date.
    Red vias where the current surfaces."""
    rng = random.Random(20260710)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    t = 25  # tile size at 1x
    cols, rows = W // t, H // t  # 16 x 12
    lw = 4 * s

    def arc(cx, cy, r, a0, a1):
        dr.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=BLACK, width=lw)

    for j in range(rows):
        for i in range(cols):
            x0, y0 = i * t * s, j * t * s
            ts = t * s
            r = ts // 2
            kind = rng.random()
            if kind < 0.44:
                arc(x0, y0, r, 0, 90)            # top-left corner arc
                arc(x0 + ts, y0 + ts, r, 180, 270)
            elif kind < 0.88:
                arc(x0 + ts, y0, r, 90, 180)
                arc(x0, y0 + ts, r, 270, 360)
            else:
                # straight crossing traces with a little bridge hop
                dr.line([(x0, y0 + r), (x0 + ts, y0 + r)], fill=BLACK, width=lw)
                dr.ellipse([x0 + r - 6 * s, y0 + r - 6 * s, x0 + r + 6 * s, y0 + r + 6 * s],
                           fill=WHITE, outline=BLACK, width=lw // 2)
                dr.line([(x0 + r, y0), (x0 + r, y0 + r - 6 * s)], fill=BLACK, width=lw)
                dr.line([(x0 + r, y0 + r + 6 * s), (x0 + r, y0 + ts)], fill=BLACK, width=lw)

    # red vias at a sparse set of grid corners
    for j in range(rows + 1):
        for i in range(cols + 1):
            if rng.random() < 0.055:
                x, y = i * t * s, j * t * s
                R = 7 * s
                dr.ellipse([x - R, y - R, x + R, y + R], fill=RED)
                dr.ellipse([x - 2 * s, y - 2 * s, x + 2 * s, y + 2 * s], fill=WHITE)

    return finalize(img, dither=False)


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(here))
    makers = [image1_tesla, image2_lichtenberg, image3_telstar,
              image4_almanac, image5_circuit_truchet]
    for i, fn in enumerate(makers, 1):
        im = fn()
        assert im.size == (W, H)
        for d in (here, os.path.join(root, "images")):
            im.save(os.path.join(d, f"{i}.png"), optimize=True)
        print(f"{i}.png done: {fn.__doc__.splitlines()[0]}")


if __name__ == "__main__":
    main()
