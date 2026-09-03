#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-03.

Five 400x300 images in exactly three colors (white, black, red).

Today's hooks:
  1. Viking 2 landed in Utopia Planitia on 3 Sept 1976 — 50 years ago today.
  2. Dagen H — Sweden switched from left- to right-hand traffic, 3 Sept 1967, 05:00.
  3. Louis H. Sullivan born 3 Sept 1856 — a generative "seed-germ" ornament.
  4. Abelian sandpile — 2^17 grains dropped on one cell and allowed to topple.
  5. A constructivist page for the third of September (Lissitzky, finally).

Technique: tonal pieces render at 3x and Floyd–Steinberg dither into the
palette; hard-edged pieces render at 3x and snap to nearest color (no dither).
Every image carries the small red-in-white "chop" at bottom right.
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
IDX_WHITE, IDX_BLACK, IDX_RED = 0, 1, 2


def finalize(img, dither=True):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    out = img.convert("RGB").quantize(palette=PAL, dither=d)
    return chop(out)


def chop(p_img):
    """Signature: a red square inside a white square, bottom-right."""
    px = p_img.load()
    x0, y0 = W - 15, H - 15
    for y in range(10):
        for x in range(10):
            px[x0 + x, y0 + y] = IDX_WHITE
    for y in range(2, 8):
        for x in range(2, 8):
            px[x0 + x, y0 + y] = IDX_RED
    return p_img


def font(path, size):
    return ImageFont.truetype(path, size)


def canvas(bg):
    img = Image.new("RGB", (W * SS, H * SS), bg)
    return img, ImageDraw.Draw(img)


def S(v):
    return v * SS


# ------------------------------------------------ 1. Utopia Planitia (Viking 2)
def image1_utopia():
    rng = random.Random(19760903)
    img, dr = canvas(WHITE)
    horizon = 118

    # sky: pure white so the type stays crisp; a faint grey haze just above the horizon
    for y in range(S(horizon - 30), S(horizon)):
        t = (y - S(horizon - 30)) / S(30)
        v = int(255 - 40 * t * t)
        dr.line([(0, y), (S(W), y)], fill=(v, v, v))
    # a small, distant sun: a thin ring (Mars' sun is two-thirds the size of ours)
    sx, sy, sr = S(72), S(40), S(9)
    dr.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=(40, 40, 40), width=S(1))
    dr.ellipse([sx - sr * 0.45, sy - sr * 0.45, sx + sr * 0.45, sy + sr * 0.45], fill=(150, 150, 150))

    # distant hills / low ridge, hazed
    pts = [(0, S(horizon))]
    x = 0
    yv = horizon - 4
    while x <= W:
        yv += rng.uniform(-1.4, 1.4)
        yv = max(horizon - 9, min(horizon - 1, yv))
        pts.append((S(x), S(yv)))
        x += 6
    pts.append((S(W), S(horizon)))
    pts.append((S(W), S(horizon) + 2))
    pts.append((0, S(horizon) + 2))
    dr.polygon(pts, fill=(196, 96, 84))

    # ground: reddish, darker toward the viewer, with a cold frost glaze
    for y in range(S(horizon), S(H)):
        t = (y - S(horizon)) / (S(H) - S(horizon))
        r = int(206 - 70 * t)
        g = int(96 - 60 * t)
        b = int(78 - 50 * t)
        dr.line([(0, y), (S(W), y)], fill=(r, g, b))

    # frost patches (Viking 2 saw morning frost at 48°N): pale streaks in hollows
    for _ in range(140):
        t = rng.random() ** 0.6
        y = horizon + 6 + t * (H - horizon - 20)
        x = rng.uniform(-20, W + 20)
        w = rng.uniform(6, 30) * (0.3 + t)
        h = rng.uniform(1.2, 3.5) * (0.4 + t)
        c = (238, 226, 222)
        dr.ellipse([S(x - w), S(y - h), S(x + w), S(y + h)], fill=c)

    # rocks: far small, near large; lit from upper-left, black shadow to the right
    rocks = []
    for _ in range(420):
        t = rng.random() ** 1.7
        y = horizon + 2 + t * (H - horizon - 14)
        x = rng.uniform(-10, W + 10)
        size = (0.6 + 15 * t ** 1.6) * rng.uniform(0.6, 1.4)
        rocks.append((y, x, size))
    rocks.sort()
    for y, x, size in rocks:
        w = size * rng.uniform(1.0, 1.9)
        h = size * rng.uniform(0.55, 0.9)
        base = rng.randint(70, 120)
        # shadow cast to the lower-right
        dr.ellipse([S(x - w * 0.6), S(y - h * 0.3), S(x + w * 1.5), S(y + h * 0.9)],
                   fill=(int(base * 0.35), int(base * 0.12), int(base * 0.1)))
        # body
        dr.ellipse([S(x - w), S(y - h), S(x + w), S(y + h)],
                   fill=(base + 40, int(base * 0.55), int(base * 0.45)))
        # lit facet
        dr.ellipse([S(x - w * 0.75), S(y - h * 0.9), S(x + w * 0.15), S(y - h * 0.1)],
                   fill=(min(255, base + 120), int(base * 1.1), int(base)))

    # the lander, lower left, as a black silhouette: body, three legs, dish, boom
    bx, by = 96, 236
    body = [(bx - 46, by - 10), (bx + 44, by - 10), (bx + 52, by + 6), (bx - 54, by + 6)]
    dr.polygon([(S(a), S(b)) for a, b in body], fill=BLACK)
    dr.rectangle([S(bx - 30), S(by - 22), S(bx + 30), S(by - 10)], fill=BLACK)
    for lx, ly in [(bx - 70, by + 30), (bx + 66, by + 32), (bx + 4, by + 40)]:
        dr.line([(S(bx - 20 if lx < bx else bx + 20), S(by + 4)), (S(lx), S(ly))], fill=BLACK, width=S(3))
        dr.ellipse([S(lx - 6), S(ly - 2), S(lx + 6), S(ly + 2)], fill=BLACK)
    # high-gain antenna on a mast
    dr.line([(S(bx + 30), S(by - 10)), (S(bx + 40), S(by - 50))], fill=BLACK, width=S(2))
    dr.pieslice([S(bx + 20), S(by - 66), S(bx + 62), S(by - 34)], 200, 340, fill=BLACK)
    dr.ellipse([S(bx + 38), S(by - 53), S(bx + 44), S(by - 47)], fill=BLACK)
    # sampler boom reaching to the right, with the scoop
    dr.line([(S(bx + 44), S(by - 2)), (S(bx + 150), S(by + 26))], fill=BLACK, width=S(2))
    dr.rectangle([S(bx + 146), S(by + 20), S(bx + 160), S(by + 30)], fill=BLACK)
    # RTG cover and camera cylinder
    dr.rectangle([S(bx - 44), S(by - 34), S(bx - 22), S(by - 22)], fill=BLACK)
    dr.rectangle([S(bx - 8), S(by - 40), S(bx + 2), S(by - 22)], fill=BLACK)
    dr.rectangle([S(bx - 10), S(by - 42), S(bx + 4), S(by - 38)], fill=BLACK)

    # text block, top right, in the sky
    f_big = font(FONT_SANS_B, S(40))
    f_lab = font(FONT_MONO_B, S(10))
    f_sm = font(FONT_MONO, S(9))
    dr.text((S(392), S(8)), "50", font=f_big, fill=RED, anchor="ra")
    dr.text((S(392), S(54)), "YEARS ON MARS", font=f_lab, fill=BLACK, anchor="ra")
    lines = ["VIKING 2 · UTOPIA PLANITIA",
             "TOUCHDOWN 1976-09-03 22:37 UTC",
             "47.97°N 225.74°W · SOL 0"]
    for i, ln in enumerate(lines):
        dr.text((S(392), S(70 + 12 * i)), ln, font=f_sm, fill=BLACK, anchor="ra")
    dr.rectangle([S(6), S(H - 26), S(130), S(H - 8)], fill=WHITE)
    dr.text((S(10), S(H - 22)), "morning frost, 48°N", font=f_sm, fill=BLACK)
    return finalize(img, dither=True)


# --------------------------------------------------------------- 2. Dagen H
def image2_dagen_h():
    img, dr = canvas(WHITE)

    # the road: a black band with a white dashed centre line, running up the page
    rx0, rx1 = 150, 250
    dr.rectangle([S(rx0), 0, S(rx1), S(H)], fill=BLACK)
    for y in range(-10, H, 22):
        dr.rectangle([S(198), S(y), S(202), S(y + 11)], fill=WHITE)

    # cars as blunt rounded rectangles: before 05:00 they are on the left,
    # after they are on the right. The crossing point is the hour itself.
    def car(cx, cy, color, up=True):
        w, h = 22, 40
        dr.rounded_rectangle([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)],
                             radius=S(7), fill=color)
        # windscreen
        wy = cy - h / 2 + (8 if up else h - 16)
        dr.rectangle([S(cx - w / 2 + 4), S(wy), S(cx + w / 2 - 4), S(wy + 8)], fill=BLACK)

    # swap arrows: white arrow starts left lane bottom, crosses to right lane top
    def s_curve(x0, x1, y0, y1, n=60):
        pts = []
        for i in range(n + 1):
            t = i / n
            e = t * t * (3 - 2 * t)
            pts.append((S(x0 + (x1 - x0) * e), S(y0 + (y1 - y0) * t)))
        return pts

    lane_l, lane_r = 175, 225
    dr.line(s_curve(lane_l, lane_r, 300, 0), fill=WHITE, width=S(5))
    dr.line(s_curve(lane_r, lane_l, 0, 300), fill=RED, width=S(5))
    # arrowheads
    dr.polygon([(S(lane_r), S(0)), (S(lane_r - 11), S(22)), (S(lane_r + 11), S(22))], fill=WHITE)
    dr.polygon([(S(lane_l), S(300)), (S(lane_l - 11), S(278)), (S(lane_l + 11), S(278))], fill=RED)
    car(lane_l, 262, WHITE, up=True)
    car(lane_r, 38, RED, up=False)

    # the hexagon H, big, left of the road
    hx, hy, hr = 75, 92, 58
    hexpts = [(S(hx + hr * math.cos(math.radians(60 * k + 30))),
               S(hy + hr * math.sin(math.radians(60 * k + 30)))) for k in range(6)]
    dr.polygon(hexpts, fill=BLACK)
    inner = [(S(hx + (hr - 6) * math.cos(math.radians(60 * k + 30))),
              S(hy + (hr - 6) * math.sin(math.radians(60 * k + 30)))) for k in range(6)]
    dr.polygon(inner, fill=RED)
    f_h = font(FONT_SANS_B, S(78))
    dr.text((S(hx), S(hy + 3)), "H", font=f_h, fill=WHITE, anchor="mm")

    # left column text
    f_t = font(FONT_SANS_B, S(22))
    f_s = font(FONT_SANS, S(11))
    dr.text((S(75), S(168)), "DAGEN H", font=f_t, fill=BLACK, anchor="ma")
    dr.text((S(75), S(196)), "Söndag 3 september 1967", font=f_s, fill=BLACK, anchor="ma")
    dr.text((S(75), S(210)), "kl. 04.50 – 05.00", font=f_s, fill=BLACK, anchor="ma")
    dr.text((S(75), S(232)), "Sverige byter till", font=f_s, fill=BLACK, anchor="ma")
    dr.text((S(75), S(246)), "högertrafik", font=font(FONT_SANS_B, S(12)), fill=RED, anchor="ma")

    # right column: the numbers, stacked
    f_n = font(FONT_SANS_B, S(24))
    f_l = font(FONT_SANS, S(10))
    col = 325
    rows = [("130 000", "vägskyltar bytta"),
            ("12 000 000", "broschyrer utdelade"),
            ("360 000", "vägmärken flyttade"),
            ("1", "natt")]
    y = 34
    for n, lab in rows:
        dr.text((S(col), S(y)), n, font=f_n, fill=BLACK, anchor="ma")
        dr.text((S(col), S(y + 28)), lab, font=f_l, fill=BLACK, anchor="ma")
        y += 60
    dr.text((S(col), S(H - 30)), "VÄNSTER  →  HÖGER", font=font(FONT_SANS_B, S(10)), fill=RED, anchor="ma")
    return finalize(img, dither=False)


# --------------------------------------------- 3. Seed-germ (Louis H. Sullivan)
def image3_seed_germ():
    rng = random.Random(18560903)
    img, dr = canvas(WHITE)
    cx, cy = 160, 150
    N = 5  # five-fold, the pentagon Sullivan loved

    def rot(pts, ang):
        c, s = math.cos(ang), math.sin(ang)
        return [(cx + (x * c - y * s), cy + (x * s + y * c)) for x, y in pts]

    def bez(p0, p1, p2, p3, n=24):
        out = []
        for i in range(n + 1):
            t = i / n
            u = 1 - t
            out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                        u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
        return out

    def leaf(base, tip, bulge, side=1):
        """Closed leaf outline from base to tip; bulge = width factor."""
        dx, dy = tip[0] - base[0], tip[1] - base[1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * bulge * side, dx / L * bulge * side
        a = bez(base, (base[0] + dx * 0.15 + nx, base[1] + dy * 0.15 + ny),
                (base[0] + dx * 0.7 + nx * 0.9, base[1] + dy * 0.7 + ny * 0.9), tip)
        b = bez(tip, (base[0] + dx * 0.7 - nx * 0.25, base[1] + dy * 0.7 - ny * 0.25),
                (base[0] + dx * 0.2 - nx * 0.15, base[1] + dy * 0.2 - ny * 0.15), base)
        return a + b[1:]

    def poly(pts, fill, outline=None, width=1):
        p = [(S(x), S(y)) for x, y in pts]
        dr.polygon(p, fill=fill)
        if outline is not None:
            dr.line(p + [p[0]], fill=outline, width=max(1, int(round(S(width)))))

    def line(pts, fill, width):
        dr.line([(S(x), S(y)) for x, y in pts], fill=fill, width=max(1, int(round(S(width)))), joint="curve")

    # inorganic frame: the pentagon and its axes, faint, as construction lines
    R = 118
    pent = [(R * math.cos(math.radians(-90 + 72 * k)), R * math.sin(math.radians(-90 + 72 * k))) for k in range(N)]
    pent_abs = [(cx + x, cy + y) for x, y in pent]
    line(pent_abs + [pent_abs[0]], BLACK, 0.8)
    for k in range(N):
        a = math.radians(-90 + 72 * k)
        line([(cx, cy), (cx + (R + 14) * math.cos(a), cy + (R + 14) * math.sin(a))], BLACK, 0.6)
    dr.ellipse([S(cx - R * 0.62), S(cy - R * 0.62), S(cx + R * 0.62), S(cy + R * 0.62)],
               outline=BLACK, width=2)

    # one arm, drawn in local coordinates pointing up (-y), then rotated N times
    def draw_arm(ang):
        # main stem: a gentle S from the germ outward
        stem = bez((0, -12), (14, -40), (-12, -70), (4, -104), n=40)
        line(rot(stem, ang), BLACK, 2.2)
        # leaves alternate along the stem
        for i, t in enumerate((0.28, 0.5, 0.7)):
            k = int(t * 40)
            b = stem[k]
            nxt = stem[k + 1]
            tx, ty = nxt[0] - b[0], nxt[1] - b[1]
            L = math.hypot(tx, ty)
            tx, ty = tx / L, ty / L
            side = 1 if i % 2 == 0 else -1
            # leaf points outward and to the side
            px, py = -ty * side, tx * side
            ln = 30 - 6 * i
            tip = (b[0] + px * ln * 0.75 + tx * ln * 0.5, b[1] + py * ln * 0.75 + ty * ln * 0.5)
            lf = leaf(b, tip, 8 - i, side=side)
            poly(rot(lf, ang), BLACK)
            # vein in white
            vein = bez(b, (b[0] + (tip[0] - b[0]) * 0.4, b[1] + (tip[1] - b[1]) * 0.4),
                       (b[0] + (tip[0] - b[0]) * 0.75, b[1] + (tip[1] - b[1]) * 0.75), tip, n=10)
            line(rot(vein[:-2], ang), WHITE, 0.9)
        # terminal bloom: a red bud in a black calyx
        tip = stem[-1]
        cal = leaf((tip[0], tip[1] + 6), (tip[0], tip[1] - 16), 9)
        poly(rot(cal, ang), BLACK)
        # the bud: rotate its centre
        bcx, bcy = rot([(tip[0], tip[1] - 6)], ang)[0]
        dr.ellipse([S(bcx - 4.2), S(bcy - 4.2), S(bcx + 4.2), S(bcy + 4.2)], fill=RED)
        # a curl (tendril) between arms
        curl = [(0, -60)]
        for j in range(1, 30):
            tt = j / 30
            r = 22 * (1 - tt)
            th = tt * math.pi * 1.9
            curl.append((r * math.sin(th) + 18 * tt, -60 - r * (1 - math.cos(th)) * 0.7 - 10 * tt))
        line(rot(curl, ang + math.radians(36)), BLACK, 1.2)

    for k in range(N):
        draw_arm(math.radians(72 * k))

    # the seed germ at centre: a red square rotated, cotyledons as two black lobes
    g = 9
    poly(rot([(-g, -g), (g, -g), (g, g), (-g, g)], math.radians(45)), RED, BLACK, 1.2)
    poly(rot(leaf((0, 0), (-22, 0), 7), math.radians(90)), BLACK)
    poly(rot(leaf((0, 0), (22, 0), 7), math.radians(90)), BLACK)
    poly(rot([(-g, -g), (g, -g), (g, g), (-g, g)], math.radians(45)), RED, BLACK, 1.2)

    # right column caption, in Sullivan's own didactic voice
    f_t = font(FONT_SERIF_B, S(15))
    f_i = font(FONT_SANS, S(10))
    x = 296
    dr.text((S(x), S(48)), "THE SEED", font=f_t, fill=BLACK)
    dr.text((S(x), S(66)), "GERM", font=f_t, fill=RED)
    para = ["The inorganic:", "a pentagon,", "five axes,", "a circle.", "",
            "Awakened by the", "will, it puts", "forth leaf, stem,", "tendril, bloom.", "",
            "Louis H. Sullivan", "b. 3 Sept 1856", "Boston"]
    for i, ln in enumerate(para):
        dr.text((S(x), S(96 + 12.5 * i)), ln, font=f_i, fill=BLACK)
    return finalize(img, dither=False)


# ---------------------------------------------------------- 4. Sandpile
def image4_sandpile():
    grains = 2 ** 17
    z = np.zeros((H, W), dtype=np.int64)
    z[H // 2, W // 2] = grains
    while True:
        t = z // 4
        if not t.any():
            break
        z -= 4 * t
        z[1:, :] += t[:-1, :]
        z[:-1, :] += t[1:, :]
        z[:, 1:] += t[:, :-1]
        z[:, :-1] += t[:, 1:]
        # grains falling off the edge are lost (open boundary)
    # 3 -> black, 2 -> red, 1 -> white, 0 -> white; outside the pile, white.
    idx = np.full((H, W), IDX_WHITE, dtype=np.uint8)
    idx[z == 3] = IDX_BLACK
    idx[z == 2] = IDX_RED
    # 1s become a sparse black stipple so the pattern's three interior tones stay distinct
    ones = (z == 1)
    yy, xx = np.mgrid[0:H, 0:W]
    idx[ones & (((yy + xx) % 2) == 0)] = IDX_BLACK
    img = Image.fromarray(idx, mode="P")
    img.putpalette(PAL.getpalette())
    dr = ImageDraw.Draw(img)
    # a small caption card
    f = font(FONT_MONO, 9)
    fb = font(FONT_MONO_B, 9)
    dr.text((8, 8), "ABELIAN SANDPILE", font=fb, fill=IDX_BLACK)
    dr.text((8, 20), "2^17 grains · one cell", font=f, fill=IDX_BLACK)
    dr.text((8, 32), "toppled until still", font=f, fill=IDX_BLACK)
    dr.text((W - 8, H - 40), "3 = black", font=f, fill=IDX_BLACK, anchor="ra")
    dr.text((W - 8, H - 28), "2 = red", font=f, fill=IDX_RED, anchor="ra")
    return chop(img)


# --------------------------------------------------- 5. Third of September (Proun)
def image5_proun():
    img, dr = canvas(WHITE)
    # diagonal split: black field to the lower right
    dr.polygon([(S(250), 0), (S(W), 0), (S(W), S(H)), (S(100), S(H))], fill=BLACK)
    # the white circle, sitting in the black
    ccx, ccy, cr = 268, 150, 78
    dr.ellipse([S(ccx - cr), S(ccy - cr), S(ccx + cr), S(ccy + cr)], fill=WHITE)
    # the red wedge, from the upper left, piercing the circle
    dr.polygon([(S(-10), S(20)), (S(-10), S(110)), (S(ccx + 12), S(ccy + 4))], fill=RED)
    # small projectiles: floating shapes in the white and in the black
    dr.rectangle([S(36), S(184), S(66), S(196)], fill=BLACK)
    dr.rectangle([S(44), S(204), S(52), S(250)], fill=BLACK)
    dr.rectangle([S(120), S(160), S(128), S(168)], fill=RED)
    dr.ellipse([S(150), S(228), S(166), S(244)], fill=BLACK)
    dr.rectangle([S(330), S(230), S(380), S(236)], fill=WHITE)
    dr.rectangle([S(350), S(246), S(358), S(280)], fill=RED)
    dr.ellipse([S(312), S(50), S(322), S(60)], fill=RED)
    dr.ellipse([S(356), S(76), S(362), S(82)], fill=WHITE)
    dr.line([(S(300), S(262)), (S(392), S(212))], fill=WHITE, width=4)
    dr.line([(S(20), S(150)), (S(20), S(276))], fill=BLACK, width=S(1))

    # rotated typography, riding the wedge
    def rotated_text(txt, fnt, fill, angle, pos):
        tw, th = dr.textbbox((0, 0), txt, font=fnt)[2:]
        layer = Image.new("RGBA", (tw + S(10), th + S(10)), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((S(5), S(5)), txt, font=fnt, fill=fill + (255,))
        layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
        img.paste(layer, (S(pos[0]) - layer.width // 2, S(pos[1]) - layer.height // 2), layer)

    rotated_text("SEPTEMBER", font(FONT_SANS_B, S(24)), BLACK, 16, (112, 42))
    dr.text((S(ccx + 30), S(ccy - 24)), "3", font=font(FONT_SANS_B, S(64)), fill=BLACK, anchor="mm")
    f_s = font(FONT_SANS_B, S(10))
    dr.text((S(10), S(H - 24)), "3 · IX · 2026", font=f_s, fill=RED)
    dr.text((S(10), S(H - 12)), "EQUINOX IN 19 DAYS", font=font(FONT_SANS, S(8)), fill=BLACK)
    # sky note in the black: last quarter moon tomorrow morning
    dr.text((S(390), S(10)), "LAST QUARTER MOON", font=font(FONT_MONO_B, S(8)), fill=WHITE, anchor="ra")
    dr.text((S(390), S(21)), "4 IX · 07:51 UTC", font=font(FONT_MONO, S(8)), fill=WHITE, anchor="ra")
    return finalize(img, dither=False)


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", ".."))
    makers = [image1_utopia, image2_dagen_h, image3_seed_germ, image4_sandpile, image5_proun]
    for i, mk in enumerate(makers, 1):
        im = mk()
        assert im.size == (W, H) and im.mode == "P"
        for d in (here, os.path.join(root, "images")):
            os.makedirs(d, exist_ok=True)
            im.save(os.path.join(d, f"{i}.png"), optimize=True)
        print("wrote", i)


if __name__ == "__main__":
    main()
