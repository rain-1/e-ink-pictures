#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-09.

Five 400x300 images in exactly three colors (white, black, red).
Today: Venus-Regulus conjunction (tonight!), Argentina's Independence Day
(Sun of May, 210 years), a constructivist poster for "Blowin' in the Wind"
(recorded 9 July 1962), a generative kamon crest, and a pop-art soup-can
grid (Warhol's Campbell's Soup Cans debuted at Ferus Gallery, 9 July 1962).
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

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


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
    return ImageFont.truetype(path, int(size))


def ctext(dr, xy, txt, f, fill, anchor="mm"):
    dr.text(xy, txt, font=f, fill=fill, anchor=anchor)


# ------------------------------------------------- 1. Venus passes Regulus
def image1_venus_regulus():
    """Tonight, 9 July 2026: Venus (-4.1) passes 1.1 deg above Regulus (+1.4),
    low in the west 45 minutes after sunset."""
    rng = random.Random(20260709)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # Twilight gradient: pale glow hugging the horizon, black night above.
    for y in range(H * s):
        t = y / (H * s)  # 0 top -> 1 bottom
        if t < 0.58:
            v = 0
        else:
            u = min((t - 0.58) / (0.80 - 0.58), 1.0)
            v = int(190 * (u ** 3.2))
        dr.line([(0, y), (W * s, y)], fill=(v, v, v))

    # Background stars, fading out near the bright horizon
    for _ in range(170):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, H * s * 0.72)
        fade = 1.0 - (y / (H * s * 0.78)) ** 3
        v = int(rng.randint(110, 255) * max(fade, 0.15))
        r = rng.uniform(0.4, 1.2) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    def star(x, y, r, label=None, mag=None, la="left"):
        x, y = x * s, y * s
        for rr, v in [(2.2, 70), (1.5, 160), (1.0, 255)]:
            dr.ellipse([x - r * rr * s, y - r * rr * s,
                        x + r * rr * s, y + r * rr * s], fill=(v, v, v))
        return x, y

    # The Sickle of Leo, diving toward the western horizon.
    sickle = [
        ("Regulus", 168, 196, 2.6),
        ("eta", 178, 166, 1.4),
        ("Algieba", 196, 138, 1.9),
        ("zeta", 182, 110, 1.4),
        ("mu", 154, 96, 1.3),
        ("epsilon", 130, 106, 1.5),
    ]
    pts = {name: (x, y) for name, x, y, _ in sickle}
    chain = ["Regulus", "eta", "Algieba", "zeta", "mu", "epsilon"]
    for a, b in zip(chain, chain[1:]):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dr.line([x1 * s, y1 * s, x2 * s, y2 * s], fill=(255, 255, 255), width=s)
    for name, x, y, r in sickle:
        star(x, y, r)

    # Venus: blazing, 1.1 degrees above Regulus. Pure red halo, white core.
    vx, vy = 160, 172
    dr.line([(vx - 15) * s, vy * s, (vx + 15) * s, vy * s], fill=RED,
            width=int(1.4 * s))
    dr.line([vx * s, (vy - 15) * s, vx * s, (vy + 15) * s], fill=RED,
            width=int(1.4 * s))
    rr = 7.5
    dr.ellipse([(vx - rr) * s, (vy - rr) * s, (vx + rr) * s, (vy + rr) * s],
               fill=RED)
    rr = 3.6
    dr.ellipse([(vx - rr) * s, (vy - rr) * s, (vx + rr) * s, (vy + rr) * s],
               fill=WHITE)

    # Ground silhouette: rolling hill with a lone tree, pure black.
    ridge = [(0, H * 0.86)]
    for x in range(0, W + 1, 8):
        y = H * 0.86 - 14 * math.sin(x / W * math.pi) - 4 * math.sin(x / 31.0)
        ridge.append((x, y))
    ridge += [(W, H), (0, H)]
    dr.polygon([(x * s, y * s) for x, y in ridge], fill=BLACK)
    # tree
    tx, ty = 330, H * 0.86 - 10 * math.sin(330 / W * math.pi) - 4 * math.sin(330 / 31.0)
    dr.line([tx * s, ty * s, tx * s, (ty - 26) * s], fill=BLACK, width=2 * s)
    for cy, cr in [(-26, 11), (-19, 14), (-12, 15)]:
        dr.ellipse([(tx - cr) * s, (ty + cy - cr * 0.7) * s,
                    (tx + cr) * s, (ty + cy + cr * 0.7) * s], fill=BLACK)

    # Labels
    f_t = font(FONT_SERIF_B, 17 * s)
    f_s = font(FONT_SANS, 10 * s)
    f_m = font(FONT_MONO, 9 * s)
    dr.text((16 * s, 14 * s), "VENUS PASSES REGULUS", font=f_t, fill=WHITE)
    dr.text((16 * s, 38 * s), "tonight · 9 July 2026 · look west after sunset",
            font=f_s, fill=RED)
    dr.text((16 * s, 54 * s), "1.1° apart — a pinky-width at arm's length",
            font=f_s, fill=WHITE)
    dr.text(((vx + 18) * s, (vy - 8) * s), "VENUS  −4.1", font=f_m, fill=WHITE)
    dr.text(((168 + 16) * s, (196 + 4) * s), "REGULUS  +1.4", font=f_m,
            fill=WHITE)
    dr.text((214 * s, 92 * s), "the Sickle of Leo", font=f_m, fill=WHITE)
    dr.text((22 * s, (H * 0.90) * s), "W", font=font(FONT_SANS_B, 13 * s),
            fill=WHITE)
    return finalize(img, dither=True)


# ------------------------------------------------- 2. Sol de Mayo
def image2_sol_de_mayo():
    """9 de Julio: Argentina's Independence Day. 210 years (1816-2026).
    The Sun of May: 32 rays, 16 straight and 16 wavy, and a serene face."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    cx, cy = W * s / 2, 152 * s
    r_face = 42 * s
    r_in = 50 * s
    r_straight = 108 * s
    r_wavy = 96 * s

    def ray_straight(theta, col):
        w = 6.5 * s
        px, py = math.cos(theta), math.sin(theta)
        nx, ny = -py, px
        tip = (cx + px * r_straight, cy + py * r_straight)
        b1 = (cx + px * r_in + nx * w, cy + py * r_in + ny * w)
        b2 = (cx + px * r_in - nx * w, cy + py * r_in - ny * w)
        dr.polygon([b1, tip, b2], fill=col)

    def ray_wavy(theta, col):
        w0 = 5.5 * s
        px, py = math.cos(theta), math.sin(theta)
        nx, ny = -py, px
        n = 26
        side1, side2 = [], []
        for i in range(n + 1):
            t = i / n
            rr = r_in + (r_wavy - r_in) * t
            off = 4.2 * s * math.sin(t * math.pi * 2.5) * (1 - t * 0.3)
            hw = w0 * (1 - t)
            bx = cx + px * rr + nx * off
            by = cy + py * rr + ny * off
            side1.append((bx + nx * hw, by + ny * hw))
            side2.append((bx - nx * hw, by - ny * hw))
        dr.polygon(side1 + side2[::-1], fill=col)

    for k in range(16):
        ray_straight(k * math.tau / 16 - math.tau / 4, BLACK)
        ray_wavy((k + 0.5) * math.tau / 16 - math.tau / 4, RED)

    # Face disc
    dr.ellipse([cx - r_face, cy - r_face, cx + r_face, cy + r_face],
               fill=WHITE, outline=BLACK, width=int(3.5 * s))
    dr.ellipse([cx - r_face + 6 * s, cy - r_face + 6 * s,
                cx + r_face - 6 * s, cy + r_face - 6 * s],
               outline=BLACK, width=s)

    # The serene face: arched brows, closed-calm eyes, nose, small mouth.
    def arc(box, a0, a1, w):
        dr.arc(box, a0, a1, fill=BLACK, width=w)

    ew = 15 * s  # eye offset
    for sx in (-1, 1):
        ex = cx + sx * ew
        arc([ex - 10 * s, cy - 18 * s, ex + 10 * s, cy - 2 * s], 210, 330,
            int(2.2 * s))  # brow
        arc([ex - 8 * s, cy - 12 * s, ex + 8 * s, cy + 2 * s], 30, 150,
            int(2.2 * s))  # eye (calm, downcast)
    dr.line([cx, cy - 8 * s, cx - 4 * s, cy + 10 * s], fill=BLACK,
            width=int(2.2 * s))
    dr.line([cx - 4 * s, cy + 10 * s, cx + 4 * s, cy + 12 * s], fill=BLACK,
            width=int(2.2 * s))
    arc([cx - 9 * s, cy + 14 * s, cx + 9 * s, cy + 26 * s], 20, 160,
        int(2.4 * s))  # mouth
    # cheeks
    for sx in (-1, 1):
        dr.ellipse([cx + sx * 26 * s - 2.4 * s, cy + 8 * s - 2.4 * s,
                    cx + sx * 26 * s + 2.4 * s, cy + 8 * s + 2.4 * s], fill=RED)

    # Type
    f_top = font(FONT_SERIF_B, 24 * s)
    f_bot = font(FONT_SANS, 10.5 * s)
    f_yr = font(FONT_SANS_B, 12 * s)
    ctext(dr, (W * s / 2, 24 * s), "9 DE JULIO", f_top, BLACK)
    dr.line([120 * s, 40 * s, 168 * s, 40 * s], fill=RED, width=int(2.5 * s))
    dr.line([232 * s, 40 * s, 280 * s, 40 * s], fill=RED, width=int(2.5 * s))
    ctext(dr, (W * s / 2, 40 * s), "★", font(FONT_SANS, 11 * s), RED)
    ctext(dr, (W * s / 2, 272 * s),
          "DÍA DE LA INDEPENDENCIA ARGENTINA", f_bot, BLACK)
    ctext(dr, (W * s / 2, 289 * s), "1816 · DOSCIENTOS DIEZ AÑOS · 2026",
          f_yr, RED)
    return finalize(img, dither=False)


# ------------------------------------------------- 3. Blowin' in the Wind
def image3_blowin_constructivist():
    """Constructivist poster: Dylan recorded "Blowin' in the Wind" on
    9 July 1962. The red wedge is the wind; the black circle, the answer."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # Halftone dot field, lower-left quadrant
    for i in range(14):
        for j in range(10):
            x = (14 + i * 13) * s
            y = (170 + j * 13) * s
            r = max(0.6, 2.6 - 0.16 * i - 0.08 * j) * s
            if x < 240 * s and y < H * s - 8 * s:
                dr.ellipse([x - r, y - r, x + r, y + r], fill=BLACK)

    # The black circle (the answer, unreachable)
    ccx, ccy, cr = 292 * s, 96 * s, 66 * s
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=BLACK)

    # The red wedge (the wind) driving up from lower left into the circle
    dr.polygon([(6 * s, 286 * s), (30 * s, 298 * s), (286 * s, 112 * s)],
               fill=RED)
    # wind lines streaming past the circle
    for (x1, y1, x2, y2, wdt) in [
        (40, 250, 360, 176, 1.4),
        (26, 232, 330, 150, 1.0),
        (70, 258, 388, 200, 1.0),
        (110, 276, 396, 232, 1.4),
    ]:
        dr.line([x1 * s, y1 * s, x2 * s, y2 * s], fill=BLACK,
                width=int(wdt * s))

    # small white circle punched out of the black one, off-center
    dr.ellipse([ccx + 18 * s - 9 * s, ccy - 26 * s - 9 * s,
                ccx + 18 * s + 9 * s, ccy - 26 * s + 9 * s], fill=WHITE)
    # red bar and black bar, counterweights
    dr.rectangle([16 * s, 60 * s, 150 * s, 74 * s], fill=BLACK)
    dr.rectangle([16 * s, 78 * s, 96 * s, 86 * s], fill=RED)

    # Type
    f_big = font(FONT_SANS_B, 30 * s)
    f_mid = font(FONT_SANS_B, 15 * s)
    f_sm = font(FONT_MONO, 9.5 * s)
    dr.text((16 * s, 14 * s), "BLOWIN'", font=f_big, fill=BLACK)
    dr.text((16 * s, 96 * s), "IN THE WIND", font=f_mid, fill=BLACK)
    # rotated caption along the wedge
    cap = Image.new("RGBA", (260 * s, 16 * s), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cap)
    cd.text((0, 0), "HOW MANY ROADS MUST A MAN WALK DOWN —", font=f_sm,
            fill=(0, 0, 0, 255))
    ang = math.degrees(math.atan2((298 - 130) , (300 - 20)))
    cap = cap.rotate(35, expand=True, resample=Image.BICUBIC)
    img.paste(cap, (30 * s, 108 * s), cap)
    dr.text((W * s - 12 * s, H * s - 12 * s),
            "recorded 9 · VII · 1962 · columbia studio A",
            font=f_sm, fill=BLACK, anchor="rd")
    ctext(dr, (ccx, ccy + 22 * s), "THE ANSWER", font(FONT_SANS_B, 11 * s),
          WHITE)
    return finalize(img, dither=False)


# ------------------------------------------------- 4. Kamon
def image4_kamon():
    """A generative kamon (Japanese family crest) seeded by today's date.
    Circles, lines and n-fold symmetry only, as the tradition demands."""
    rng = random.Random(20260709 * 7)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    cx, cy = 200 * s, 150 * s
    R = 118 * s

    # maru: the enclosing double ring
    for rr, wdt in [(R, 7 * s), (R - 14 * s, 2 * s)]:
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=BLACK,
                   width=int(wdt))

    n = rng.choice([6, 8])
    base = rng.uniform(0, math.tau)

    def petal(theta, r0, r1, width, col, outline_only=False):
        """A pointed petal from radius r0 to r1 along angle theta."""
        px, py = math.cos(theta), math.sin(theta)
        nx, ny = -py, px
        pts = []
        m = 24
        for i in range(m + 1):
            t = i / m
            rr = r0 + (r1 - r0) * t
            hw = width * math.sin(t * math.pi) ** 0.8
            pts.append((cx + px * rr + nx * hw, cy + py * rr + ny * hw))
        for i in range(m + 1):
            t = 1 - i / m
            rr = r0 + (r1 - r0) * t
            hw = width * math.sin(t * math.pi) ** 0.8
            pts.append((cx + px * rr - nx * hw, cy + py * rr - ny * hw))
        if outline_only:
            dr.polygon(pts, outline=col, width=int(2.2 * s))
        else:
            dr.polygon(pts, fill=col)

    # main petals
    for k in range(n):
        th = base + k * math.tau / n
        petal(th, 18 * s, 92 * s, 16 * s if n == 6 else 13 * s, BLACK)
        # white vein inside each petal
        petal(th, 26 * s, 80 * s, 4.5 * s if n == 6 else 3.6 * s, WHITE)
    # secondary small circles between petals
    r_dot = rng.choice([7, 9]) * s
    for k in range(n):
        th = base + (k + 0.5) * math.tau / n
        dx = cx + math.cos(th) * 84 * s
        dy = cy + math.sin(th) * 84 * s
        dr.ellipse([dx - r_dot, dy - r_dot, dx + r_dot, dy + r_dot],
                   fill=BLACK)
        dr.ellipse([dx - r_dot + 2.6 * s, dy - r_dot + 2.6 * s,
                    dx + r_dot - 2.6 * s, dy + r_dot - 2.6 * s], fill=WHITE)

    # center: black disc with red core
    dr.ellipse([cx - 16 * s, cy - 16 * s, cx + 16 * s, cy + 16 * s], fill=BLACK)
    dr.ellipse([cx - 8 * s, cy - 8 * s, cx + 8 * s, cy + 8 * s], fill=RED)

    # hanko-style red seal, bottom right, vertical date
    f_jp = font(FONT_JP, 13 * s)
    seal_x, seal_y = 356 * s, 214 * s
    dr.rectangle([seal_x, seal_y, seal_x + 26 * s, seal_y + 76 * s],
                 outline=RED, width=int(2 * s))
    for i, ch in enumerate("七月九日"):
        ctext(dr, (seal_x + 13 * s, seal_y + (11 + i * 18) * s), ch, f_jp, RED)
    # title, small, top left vertical
    f_jp2 = font(FONT_JP, 15 * s)
    for i, ch in enumerate("家紋"):
        ctext(dr, (26 * s, (26 + i * 20) * s), ch, f_jp2, BLACK)
    return finalize(img, dither=False)


# ------------------------------------------------- 5. Soup cans
def image5_soup_cans():
    """Repetition as art: Warhol's Campbell's Soup Cans opened at the
    Ferus Gallery, Los Angeles, on 9 July 1962. Twelve cans, three inks."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    cols, rows = 4, 3
    cell_w, cell_h = W / cols, (H - 26) / rows
    can_w, can_h = 56, 78

    schemes = [
        (RED, WHITE, BLACK),   # classic: red top, white bottom
        (BLACK, WHITE, RED),
        (WHITE, RED, BLACK),
        (RED, BLACK, WHITE),
    ]

    def can(x0, y0, top_col, bot_col, acc_col):
        """Draw one can with top-left corner (x0, y0), 1x coordinates."""
        x0, y0 = x0 * s, y0 * s
        w, h = can_w * s, can_h * s
        lid_h = 12 * s
        split = y0 + h * 0.52
        # body halves
        dr.rectangle([x0, y0 + lid_h / 2, x0 + w, split], fill=top_col)
        dr.rectangle([x0, split, x0 + w, y0 + h], fill=bot_col)
        # bottom curve
        dr.ellipse([x0, y0 + h - 8 * s, x0 + w, y0 + h + 8 * s], fill=bot_col,
                   outline=BLACK, width=int(1.6 * s))
        dr.rectangle([x0, y0 + lid_h / 2, x0 + w, y0 + h], outline=BLACK,
                     width=int(1.6 * s))
        # lid
        dr.ellipse([x0, y0, x0 + w, y0 + lid_h], fill=WHITE, outline=BLACK,
                   width=int(1.6 * s))
        dr.ellipse([x0 + 5 * s, y0 + 2.6 * s, x0 + w - 5 * s,
                    y0 + lid_h - 2.6 * s], outline=BLACK, width=s)
        # gold-medal medallion at the split
        mcx, mcy, mr = x0 + w / 2, split, 7 * s
        dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=WHITE,
                   outline=BLACK, width=int(1.4 * s))
        ctext(dr, (mcx, mcy), "★", font(FONT_SANS, 7 * s), acc_col)
        # wordmark on the top half
        top_ink = WHITE if top_col in (RED, BLACK) else BLACK
        f_scr = font(FONT_SERIF_B, 10 * s)
        ctext(dr, (x0 + w / 2, y0 + lid_h / 2 + 12 * s), "Soup!", f_scr,
              top_ink)
        # variety on the bottom half
        bot_ink = WHITE if bot_col in (RED, BLACK) else BLACK
        f_var = font(FONT_SANS_B, 8 * s)
        ctext(dr, (x0 + w / 2, y0 + h - 14 * s), "TOMATO", f_var, bot_ink)

    k = 0
    for r in range(rows):
        for c in range(cols):
            top, bot, acc = schemes[(k + r) % 4]
            x0 = c * cell_w + (cell_w - can_w) / 2
            y0 = r * cell_h + (cell_h - can_h) / 2 + 2
            can(x0, y0, top, bot, acc)
            k += 1

    # caption bar
    dr.rectangle([0, (H - 24) * s, W * s, H * s], fill=BLACK)
    f_cap = font(FONT_MONO, 9 * s)
    ctext(dr, (W * s / 2, (H - 12) * s),
          "WARHOL · 32 CANS · FERUS GALLERY, L.A. · OPENED 9 JULY 1962",
          f_cap, WHITE)
    return finalize(img, dither=False)


# ------------------------------------------------- main
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(os.path.dirname(here))
    os.makedirs(os.path.join(repo, "images"), exist_ok=True)
    makers = [
        image1_venus_regulus,
        image2_sol_de_mayo,
        image3_blowin_constructivist,
        image4_kamon,
        image5_soup_cans,
    ]
    for i, fn in enumerate(makers, 1):
        im = fn()
        assert im.size == (W, H)
        im.save(os.path.join(repo, "images", f"{i}.png"))
        im.save(os.path.join(here, f"{i}.png"))
        print(f"image {i}: {fn.__name__} ok")


if __name__ == "__main__":
    main()
