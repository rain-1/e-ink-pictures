#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-30.

Five 400x300 images in exactly three colors (white, black, red).
Today: the a-Capricornid + S d-Aquariid double meteor shower peaks tonight
under a 98% moon; Penguin published its first paperbacks 30 Jul 1935;
Emily Bronte was born 30 Jul 1818; Apollo 15 landed the first Lunar Rover
at Hadley Rille 30 Jul 1971.

1. Long-exposure star trails cut by meteors, moon glare in the corner.
2. Constructivist composition (Lissitzky homage) for the red wedge backlog.
3. A grid of six generated kamon (n-fold symmetric Japanese crests).
4. Penguin tri-band paperback homage: Wuthering Heights (two anniversaries).
5. Apollo 15 at Hadley Rille — first wheels on the Moon, 55 years ago.
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


def ctext(dr, xy, s, f, fill, anchor="mm"):
    dr.text(xy, s, font=f, fill=fill, anchor=anchor)


# ------------------------------------------------- 1. Double shower, long exposure
def image1_startrails():
    rng = random.Random(20260730)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # celestial pole upper-left; concentric star-trail arcs
    px, py = 118 * s, 84 * s
    for _ in range(260):
        r = rng.uniform(14, 430) * s
        a0 = rng.uniform(0, 360)
        sweep = rng.uniform(9, 22)  # exposure arc, degrees
        v = rng.choice([70, 90, 110, 140, 170, 200, 230])
        wdt = max(1, int(round((1 if v < 150 else rng.choice([1, 2])) * s * 0.7)))
        dr.arc([px - r, py - r, px + r, py + r], a0, a0 + sweep,
               fill=(v, v, v), width=wdt)

    # moon glare, lower right — a blown-out blob washing the sky
    mx, my = 352 * s, 246 * s
    for rad, v in [(120, 28), (95, 45), (72, 70), (54, 105), (40, 160),
                   (30, 220), (24, 255)]:
        dr.ellipse([mx - rad * s, my - rad * s, mx + rad * s, my + rad * s],
                   fill=(v, v, v))

    # meteors: straight red streaks from two radiants low in the south
    def streaks(rx, ry, n, seedoff):
        r2 = random.Random(20260730 + seedoff)
        for _ in range(n):
            ang = math.radians(r2.uniform(0, 360))
            d0 = r2.uniform(60, 130) * s
            d1 = d0 + r2.uniform(55, 150) * s
            x0, y0 = rx + d0 * math.cos(ang), ry + d0 * math.sin(ang)
            x1, y1 = rx + d1 * math.cos(ang), ry + d1 * math.sin(ang)
            if not (0 <= x1 <= W * s and -20 * s <= y1 <= H * s):
                continue
            dr.line([x0, y0, x1, y1], fill=RED, width=int(1.4 * s))

    streaks(300 * s, 330 * s, 26, 1)   # S delta Aquariids: many, faint-ish
    # alpha Capricornid fireball: one slow bright one with a flare bulge
    fx0, fy0, fx1, fy1 = 60 * s, 268 * s, 236 * s, 120 * s
    dr.line([fx0, fy0, fx1, fy1], fill=RED, width=int(2.6 * s))
    t = 0.62
    bx, by = fx0 + (fx1 - fx0) * t, fy0 + (fy1 - fy0) * t
    dr.ellipse([bx - 5 * s, by - 5 * s, bx + 5 * s, by + 5 * s], fill=RED)
    dr.ellipse([bx - 2 * s, by - 2 * s, bx + 2 * s, by + 2 * s], fill=WHITE)

    # caption strip
    dr.rectangle([0, (H - 22) * s, W * s, H * s], fill=BLACK)
    f = font(FONT_MONO, 11 * s)
    ctext(dr, (W * s / 2, (H - 11) * s),
          "α CAPRICORNIDS × δ AQUARIIDS · TONIGHT · MOON 98%",
          f, WHITE)
    return finalize(img)


# ------------------------------------------------- 2. Constructivist composition
def image2_constructivist():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # diagonal split: black field lower-right
    dr.polygon([(W * s, 0), (W * s, H * s), (0, H * s)], fill=BLACK)

    # white circle sitting on the black field
    cx, cy, cr = 258 * s, 172 * s, 78 * s
    dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=WHITE)

    # the red wedge, piercing from the white field into the circle
    dr.polygon([(18 * s, 44 * s), (18 * s, 116 * s), (cx + 8 * s, cy)],
               fill=RED)

    # supporting geometry
    dr.ellipse([cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s], fill=RED)
    dr.rectangle([30 * s, 234 * s, 176 * s, 244 * s], fill=RED)
    dr.rectangle([30 * s, 252 * s, 128 * s, 256 * s], fill=WHITE)
    for i in range(5):
        x = (306 + i * 16) * s
        dr.rectangle([x, 34 * s, x + 6 * s, 88 * s], fill=WHITE)
    dr.line([(70 * s, 20 * s), (200 * s, 150 * s)], fill=BLACK, width=2 * s)
    dr.ellipse([58 * s, 160 * s, 86 * s, 188 * s], outline=BLACK, width=3 * s)

    f_big = font(FONT_SANS_B, 34 * s)
    f_sm = font(FONT_SANS_B, 13 * s)
    dr.text((30 * s, 22 * s), "30", font=f_big, fill=BLACK)
    dr.text((32 * s, 148 * s), "ИЮЛЯ", font=f_sm, fill=BLACK)
    txt = Image.new("RGB", (152 * s, 20 * s), BLACK)
    ImageDraw.Draw(txt).text((0, 0), "КРАСНЫМ КЛИНОМ", font=f_sm, fill=WHITE)
    txt = txt.rotate(90, expand=True)
    img.paste(txt, (374 * s, 106 * s))
    return finalize(img, dither=False)


# ------------------------------------------------- 3. Kamon sextet
def kamon(size, rng, color):
    """One n-fold symmetric crest, drawn black-or-red on white, in a maru ring."""
    t = size  # tile is t x t
    im = Image.new("RGB", (t, t), WHITE)
    dr = ImageDraw.Draw(im)
    c = t / 2
    R = t * 0.46

    # outer maru ring
    ring_w = max(2, int(t * rng.choice([0.030, 0.045, 0.075])))
    dr.ellipse([c - R, c - R, c + R, c + R], outline=color, width=ring_w)

    n = rng.choice([3, 4, 5, 6, 6, 8])
    base = rng.uniform(0, 360)

    def petal(rad_in, rad_out, wid, ang):
        """teardrop petal pointing outward at angle ang (deg)"""
        a = math.radians(ang)
        steps = 40
        pts_l, pts_r = [], []
        for i in range(steps + 1):
            u = i / steps
            r = rad_in + (rad_out - rad_in) * u
            w = wid * math.sin(math.pi * min(1.0, u * 1.15))
            px, py = c + r * math.cos(a), c + r * math.sin(a)
            ox, oy = -math.sin(a) * w, math.cos(a) * w
            pts_l.append((px + ox, py + oy))
            pts_r.append((px - ox, py - oy))
        dr.polygon(pts_l + pts_r[::-1], fill=color)

    kinds = rng.sample(["petal", "dot", "diamond", "arcbar", "wedge"],
                       k=rng.choice([2, 2, 3]))
    for kind in kinds:
        if kind == "petal":
            ri = R * rng.uniform(0.05, 0.25)
            ro = R * rng.uniform(0.68, 0.86)
            wd = R * rng.uniform(0.14, 0.26)
            for i in range(n):
                petal(ri, ro, wd, base + 360 * i / n)
        elif kind == "dot":
            rr = R * rng.uniform(0.55, 0.75)
            dd = R * rng.uniform(0.08, 0.15)
            hollow = rng.random() < 0.4
            for i in range(n):
                a = math.radians(base + 360 * i / n + 180 / n)
                x, y = c + rr * math.cos(a), c + rr * math.sin(a)
                if hollow:
                    dr.ellipse([x - dd, y - dd, x + dd, y + dd],
                               outline=color, width=max(2, int(t * 0.02)))
                else:
                    dr.ellipse([x - dd, y - dd, x + dd, y + dd], fill=color)
        elif kind == "diamond":
            dd = R * rng.uniform(0.16, 0.30)
            if rng.random() < 0.5:
                dr.polygon([(c, c - dd), (c + dd, c), (c, c + dd), (c - dd, c)],
                           fill=color)
            else:
                dr.ellipse([c - dd, c - dd, c + dd, c + dd], fill=color)
                dr.ellipse([c - dd * .5, c - dd * .5, c + dd * .5, c + dd * .5],
                           fill=WHITE)
        elif kind == "arcbar":
            rr = R * rng.uniform(0.80, 0.9)
            wdt = max(2, int(R * 0.09))
            gap = rng.uniform(12, 30)
            for i in range(n):
                a0 = base + 360 * i / n + gap / 2
                a1 = base + 360 * (i + 1) / n - gap / 2
                dr.arc([c - rr, c - rr, c + rr, c + rr], a0, a1,
                       fill=color, width=wdt)
        elif kind == "wedge":
            ri, ro = R * 0.30, R * rng.uniform(0.60, 0.8)
            hw = math.radians(360 / n * rng.uniform(0.12, 0.2))
            for i in range(n):
                a = math.radians(base + 360 * i / n + 180 / n)
                dr.polygon([(c + ri * math.cos(a), c + ri * math.sin(a)),
                            (c + ro * math.cos(a - hw), c + ro * math.sin(a - hw)),
                            (c + ro * math.cos(a + hw), c + ro * math.sin(a + hw))],
                           fill=color)
    return im


def image3_kamon():
    rng = random.Random(20260730 * 3)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    tile = 118 * s
    red_slot = rng.randrange(6)
    xs = [24 * s, 141 * s, 258 * s]
    ys = [14 * s, 140 * s]
    k = 0
    for row in range(2):
        for col in range(3):
            color = RED if k == red_slot else BLACK
            km = kamon(tile, rng, color)
            img.paste(km, (xs[col], ys[row]))
            k += 1
    f = font(FONT_JP, 12 * s)
    ctext(dr, (W * s / 2, 273 * s), "家紋六つ — 二〇二六年七月三十日", f, BLACK)
    dr.rectangle([160 * s, 288 * s, 240 * s, 290 * s], fill=RED)
    return finalize(img, dither=False)


# ------------------------------------------------- 4. Penguin tri-band homage
def draw_penguin(dr, cx, cy, h, ink=BLACK, paper=WHITE):
    """A little dancing penguin silhouette, roughly h tall, centered at cx,cy."""
    w = h * 0.62
    top, bot = cy - h / 2, cy + h / 2
    # body
    dr.ellipse([cx - w / 2, top + h * 0.18, cx + w / 2, bot], fill=ink)
    # head, cocked slightly
    hx, hy, hr = cx + h * 0.06, top + h * 0.16, h * 0.155
    dr.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=ink)
    # belly
    dr.ellipse([cx - w * 0.30, top + h * 0.34, cx + w * 0.34, bot - h * 0.06],
               fill=paper)
    # beak
    dr.polygon([(hx + hr * 0.6, hy - hr * 0.25), (hx + hr * 2.0, hy + hr * 0.1),
                (hx + hr * 0.6, hy + hr * 0.45)], fill=ink)
    # eye
    er = max(2, int(h * 0.022))
    dr.ellipse([hx + hr * 0.15 - er, hy - hr * 0.2 - er,
                hx + hr * 0.15 + er, hy - hr * 0.2 + er], fill=paper)
    # flipper
    dr.polygon([(cx - w * 0.42, top + h * 0.40), (cx - w * 0.78, top + h * 0.72),
                (cx - w * 0.28, top + h * 0.66)], fill=ink)
    # feet
    dr.polygon([(cx - w * 0.22, bot), (cx - w * 0.02, bot),
                (cx - w * 0.30, bot + h * 0.06)], fill=ink)
    dr.polygon([(cx + w * 0.10, bot), (cx + w * 0.30, bot),
                (cx + w * 0.38, bot + h * 0.06)], fill=ink)


def image4_penguin():
    s = SS
    img = Image.new("RGB", (W * s, H * s), RED)
    dr = ImageDraw.Draw(img)

    band_top, band_bot = 62 * s, 224 * s
    dr.rectangle([0, band_top, W * s, band_bot], fill=WHITE)

    # top band: cartouche
    f_c = font(FONT_SANS_B, 15 * s)
    ew, eh = 150 * s, 34 * s
    dr.ellipse([W * s / 2 - ew / 2, 31 * s - eh / 2 - 2 * s,
                W * s / 2 + ew / 2, 31 * s + eh / 2 - 2 * s], fill=WHITE)
    ctext(dr, (W * s / 2, 29 * s), "PAPERBACKS", f_c, BLACK)

    # middle band: title
    f_small = font(FONT_SANS, 12 * s)
    f_title = font(FONT_SANS_B, 30 * s)
    f_by = font(FONT_SANS, 15 * s)
    ctext(dr, (W * s / 2, 80 * s), "COMPLETE · UNABRIDGED", f_small, BLACK)
    dr.line([120 * s, 92 * s, 280 * s, 92 * s], fill=BLACK, width=s)
    ctext(dr, (W * s / 2, 121 * s), "WUTHERING", f_title, BLACK)
    ctext(dr, (W * s / 2, 154 * s), "HEIGHTS", f_title, BLACK)
    dr.line([120 * s, 176 * s, 280 * s, 176 * s], fill=BLACK, width=s)
    ctext(dr, (W * s / 2, 192 * s), "EMILY BRONTË", f_by, BLACK)
    ctext(dr, (W * s / 2, 211 * s), "born 30 July 1818", f_small, BLACK)

    # bottom band: penguin + footnote
    draw_penguin(dr, W * s / 2, 258 * s, 52 * s, ink=BLACK, paper=RED)
    f_foot = font(FONT_SANS, 10 * s)
    ctext(dr, (58 * s, 288 * s), "SIXPENCE", f_foot, WHITE)
    ctext(dr, (322 * s, 288 * s), "b. 30 JULY 1935", f_foot, WHITE)
    return finalize(img, dither=False)


# ------------------------------------------------- 5. Apollo 15 at Hadley Rille
def image5_apollo():
    rng = random.Random(19710730)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # stars
    for _ in range(90):
        x, y = rng.uniform(0, W * s), rng.uniform(0, 150 * s)
        r = rng.uniform(0.4, 1.1) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    # Earth, small in the black sky
    ex, ey, er = 330 * s, 44 * s, 15 * s
    dr.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(210, 210, 210))
    dr.chord([ex - er, ey - er, ex + er, ey + er], 110, 250, fill=(60, 60, 60))

    # Apennine front: big smooth mountains (Hadley Delta), mid gray
    def ridge(base_y, amp, freq, ph, col):
        pts = [(0, H * s)]
        for x in range(0, W * s + 1, 2 * s):
            y = base_y
            y += amp * math.sin(freq * x / (W * s) * math.pi * 2 + ph)
            y += amp * 0.5 * math.sin(2.7 * freq * x / (W * s) * math.pi * 2 + ph * 2)
            pts.append((x, y))
        pts.append((W * s, H * s))
        dr.polygon(pts, fill=col)

    ridge(120 * s, 26 * s, 1.1, 0.7, (95, 95, 95))
    ridge(158 * s, 16 * s, 1.7, 2.9, (150, 150, 150))
    # foreground regolith
    dr.rectangle([0, 196 * s, W * s, H * s], fill=(190, 190, 190))
    # Hadley Rille: sinuous dark channel across the plain
    rille = []
    for x in range(-10, W + 11, 4):
        y = 216 + 10 * math.sin(x / 52) + 4 * math.sin(x / 17 + 2)
        rille.append((x * s, y * s))
    for wdt, col in [(16, (120, 120, 120)), (9, (70, 70, 70)), (4, (30, 30, 30))]:
        dr.line(rille, fill=col, width=wdt * s, joint="curve")
    # craters
    for _ in range(26):
        x = rng.uniform(0, W) * s
        y = rng.uniform(238, 296) * s
        cr = rng.uniform(2, 9) * (0.5 + (y / (H * s))) * s
        dr.ellipse([x - cr, y - cr * 0.45, x + cr, y + cr * 0.45],
                   outline=(120, 120, 120), width=max(1, int(0.8 * s)))
        dr.arc([x - cr, y - cr * 0.45, x + cr, y + cr * 0.45], 200, 340,
               fill=(235, 235, 235), width=max(1, int(0.8 * s)))

    # the Lunar Roving Vehicle, black silhouette, facing left
    ox, oy = 96 * s, 262 * s   # ground line under rover
    def P(px, py):
        return (ox + px * s, oy - py * s)
    # wheels: two wire-mesh wheels visible
    for wx in (0, 62):
        wr = 13 * s
        cx, cy = P(wx, 13)
        dr.ellipse([cx - wr, cy - wr, cx + wr, cy + wr],
                   outline=BLACK, width=3 * s)
        for i in range(6):
            a = math.pi * i / 3 + 0.3
            dr.line([cx - wr * math.cos(a), cy - wr * math.sin(a),
                     cx + wr * math.cos(a), cy + wr * math.sin(a)],
                    fill=BLACK, width=s)
    # chassis
    dr.line([P(-12, 22), P(76, 22)], fill=BLACK, width=4 * s)
    dr.line([P(-2, 22), P(0, 13)], fill=BLACK, width=3 * s)
    dr.line([P(60, 22), P(62, 13)], fill=BLACK, width=3 * s)
    # seats + console
    dr.rectangle([P(18, 34)[0], P(18, 34)[1], P(30, 22)[0], P(30, 22)[1]],
                 fill=BLACK)
    dr.rectangle([P(36, 34)[0], P(36, 34)[1], P(48, 22)[0], P(48, 22)[1]],
                 fill=BLACK)
    dr.line([P(8, 22), P(8, 32)], fill=BLACK, width=2 * s)
    dr.rectangle([P(2, 38)[0], P(2, 38)[1], P(14, 32)[0], P(14, 32)[1]],
                 fill=BLACK)
    # high-gain antenna dish
    dr.line([P(-6, 22), P(-6, 44)], fill=BLACK, width=2 * s)
    dr.arc([P(-16, 56)[0], P(-16, 56)[1], P(4, 40)[0], P(4, 40)[1]],
           200, 340, fill=BLACK, width=3 * s)
    # the flag: red stripes
    fx, fy = P(150, 0)
    dr.line([fx, fy, fx, fy - 44 * s], fill=BLACK, width=2 * s)
    flag_w, flag_h = 30 * s, 19 * s
    dr.rectangle([fx, fy - 44 * s, fx + flag_w, fy - 44 * s + flag_h],
                 fill=WHITE)
    for i in range(4):  # 4 red stripes, each ~3px at final scale
        yy = fy - 44 * s + (2 * i) * flag_h / 7
        dr.rectangle([fx, yy, fx + flag_w, yy + flag_h / 7], fill=RED)
    dr.rectangle([fx, fy - 44 * s, fx + flag_w * 0.42, fy - 44 * s + flag_h * 0.5],
                 fill=BLACK)

    # caption
    dr.rectangle([0, (H - 24) * s, W * s, H * s], fill=BLACK)
    f = font(FONT_MONO, 11 * s)
    ctext(dr, (W * s / 2, (H - 12) * s),
          "APOLLO 15 · 30 JUL 1971 · FIRST WHEELS ON THE MOON",
          f, WHITE)
    dr.rectangle([0, (H - 24) * s, W * s, (H - 23) * s], fill=RED)
    return finalize(img)


# ----------------------------------------------------------------------- main
def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(here))
    makers = [image1_startrails, image2_constructivist, image3_kamon,
              image4_penguin, image5_apollo]
    for i, mk in enumerate(makers, 1):
        im = mk()
        assert im.size == (W, H)
        for d in (here, os.path.join(root, "images")):
            im.save(os.path.join(d, f"{i}.png"), optimize=True)
        print(f"{i}.png done")


if __name__ == "__main__":
    main()
