#!/usr/bin/env python3
"""
e-ink pictures — 2026-08-01 (day 2)
Five 400x300 images in black / white / red for Edward's desk e-ink screen.

Today: Lughnasadh (first harvest) · Herman Melville b. 1 Aug 1819 ·
Swiss National Day · and the August sky ahead (total solar eclipse +
Perseids under a new moon, BOTH on Aug 12).

1.png  Kamon sampler — six procedurally built Japanese family crests
2.png  The August Sky — eclipse-and-Perseids almanac card
3.png  Constructivist composition — the long-promised Lissitzky homage
4.png  Lughnasadh — wheat field with harvest sun
5.png  Call me Ishmael — Moby-Dick for Melville's 207th birthday
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3                      # supersample factor
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SEED = 20260801

FONT_DIR = "/usr/share/fonts/truetype"
SANS = f"{FONT_DIR}/dejavu/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf"
SERIF = f"{FONT_DIR}/dejavu/DejaVuSerif.ttf"
SERIF_I = f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf"
MONO = f"{FONT_DIR}/dejavu/DejaVuSansMono.ttf"
JP = f"{FONT_DIR}/fonts-japanese-gothic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def canvas(bg=WHITE):
    im = Image.new("RGB", (W * S, H * S), bg)
    return im, ImageDraw.Draw(im)


def finish(im, name):
    """Downscale from 3x, snap every pixel to the exact 3-color palette."""
    small = im.resize((W, H), Image.LANCZOS)
    pal = Image.new("P", (1, 1))
    pal.putpalette(list(BLACK) + list(WHITE) + list(RED) + [0] * 741)
    out = small.quantize(palette=pal, dither=Image.Dither.NONE)
    out.save(name)
    print("wrote", name)


def text_center(d, xy, s, f, fill):
    x, y = xy
    box = d.textbbox((0, 0), s, font=f)
    d.text((x - (box[2] - box[0]) / 2 - box[0], y - (box[3] - box[1]) / 2 - box[1]),
           s, font=f, fill=fill)


# ----------------------------------------------------------------------------
# 1 · KAMON SAMPLER
# ----------------------------------------------------------------------------

def tomoe(d, cx, cy, R, n, fill):
    """n comma-swirls (tomoe) inside radius R."""
    for k in range(n):
        a0 = 2 * math.pi * k / n
        steps = 80
        for i in range(steps):
            t = i / (steps - 1)
            ang = a0 + t * math.radians(150)
            dist = R * (0.42 + 0.26 * t)
            r = R * 0.18 * (1 - t) ** 1.7 + R * 0.006
            x = cx + dist * math.cos(ang)
            y = cy + dist * math.sin(ang)
            d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def petals(d, cx, cy, R, n, fill, bg):
    """n-petal blossom with an open center."""
    for k in range(n):
        a = 2 * math.pi * k / n - math.pi / 2
        px = cx + R * 0.55 * math.cos(a)
        py = cy + R * 0.55 * math.sin(a)
        rl, rw = R * 0.42, R * 0.24
        pts = []
        for i in range(24):
            th = 2 * math.pi * i / 24
            ex = rl * math.cos(th)
            ey = rw * math.sin(th)
            pts.append((px + ex * math.cos(a) - ey * math.sin(a),
                        py + ex * math.sin(a) + ey * math.cos(a)))
        d.polygon(pts, fill=fill)
    r = R * 0.22
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg)
    r = R * 0.12
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def nested_diamonds(d, cx, cy, R, fill, bg):
    """takeda-bishi style: four diamonds in a diamond."""
    def diamond(x, y, r, c):
        d.polygon([(x, y - r), (x + r * 0.72, y), (x, y + r), (x - r * 0.72, y)], fill=c)
    r = R * 0.40
    off = R * 0.42
    for (x, y) in [(cx, cy - off), (cx + off * 0.72, cy), (cx, cy + off), (cx - off * 0.72, cy)]:
        diamond(x, y, r, fill)
        diamond(x, y, r * 0.45, bg)


def moon_star(d, cx, cy, R, fill, bg, accent):
    """tsuki ni hoshi — crescent moon with a star."""
    r = R * 0.72
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    r2 = R * 0.62
    ox, oy = R * 0.28, -R * 0.18
    d.ellipse([cx + ox - r2, cy + oy - r2, cx + ox + r2, cy + oy + r2], fill=bg)
    sx, sy = cx + R * 0.30, cy - R * 0.05
    sr = R * 0.16
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = sr if i % 2 == 0 else sr * 0.45
        pts.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
    d.polygon(pts, fill=accent)


def waves_circle(d, cx, cy, R, fill, bg):
    """seigaiha clipped to a disc: stacked concentric arc fans."""
    disc = R * 0.80
    d.ellipse([cx - disc, cy - disc, cx + disc, cy + disc], fill=fill)
    lw = max(2, int(R * 0.055))
    rows = [(-0.55, 0.0), (-0.15, 0.5), (0.25, 0.0), (0.65, 0.5)]
    rad = R * 0.42
    for dy, phase in rows:
        y = cy + dy * R
        x = cx - disc + (phase - 1) * rad * 2
        while x < cx + disc + rad:
            for f in (1.0, 0.66, 0.33):
                rr = rad * f
                dx2 = (x - cx)
                dy2 = (y - rad * 0.0 - cy)
                if math.hypot(dx2, dy2) < disc + rad * 0.2:
                    d.arc([x - rr, y - rr, x + rr, y + rr], 180, 360, fill=bg, width=lw)
            x += rad * 2
    # re-mask outside of disc
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=bg, width=int(R * 0.21))


def wheel(d, cx, cy, R, fill, bg):
    """genji-guruma cart wheel."""
    r = R * 0.78
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    r2 = R * 0.60
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=bg)
    for k in range(8):
        a = 2 * math.pi * k / 8 + math.pi / 8
        x2 = cx + r2 * math.cos(a)
        y2 = cy + r2 * math.sin(a)
        d.line([(cx, cy), (x2, y2)], fill=fill, width=int(R * 0.11))
    rh = R * 0.24
    d.ellipse([cx - rh, cy - rh, cx + rh, cy + rh], fill=fill)
    rh2 = R * 0.10
    d.ellipse([cx - rh2, cy - rh2, cx + rh2, cy + rh2], fill=bg)


def img1():
    im, d = canvas(WHITE)
    cells = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)]
    cw, ch = W * S / 3, (H - 42) * S / 2
    R = 52 * S
    ring = int(4.2 * S)
    for i, (gx, gy) in enumerate(cells):
        cx = (gx + 0.5) * cw
        cy = (gy + 0.5) * ch + 6 * S
        col = RED if i in (1, 5) else BLACK
        bg = WHITE
        d.ellipse([cx - R - ring, cy - R - ring, cx + R + ring, cy + R + ring], fill=col)
        d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=bg)
        Rin = R * 0.86
        if i == 0:
            tomoe(d, cx, cy, Rin, 3, col)
        elif i == 1:
            petals(d, cx, cy, Rin, 8, col, bg)
        elif i == 2:
            nested_diamonds(d, cx, cy, Rin, col, bg)
        elif i == 3:
            moon_star(d, cx, cy, Rin, col, bg, RED)
        elif i == 4:
            waves_circle(d, cx, cy, Rin, col, bg)
        else:
            wheel(d, cx, cy, Rin, col, bg)
    # caption band
    d.rectangle([0, (H - 34) * S, W * S, H * S], fill=BLACK)
    fjp = font(JP, 15 * S)
    fs = font(SANS, 10 * S)
    text_center(d, (W * S / 2, (H - 21.5) * S), "家紋 KAMON", fjp, WHITE)
    text_center(d, (W * S / 2, (H - 8.5) * S),
                "tomoe · blossom · diamonds · moon & star · waves · wheel", fs, WHITE)
    finish(im, "1.png")


# ----------------------------------------------------------------------------
# 2 · THE AUGUST SKY
# ----------------------------------------------------------------------------

def img2():
    rng = random.Random(SEED)
    im, d = canvas(BLACK)
    # meteor streaks from a radiant at top-right
    rx, ry = 195 * S, -30 * S
    kept = 0
    while kept < 9:
        a = math.radians(rng.uniform(215, 305))
        d0 = rng.uniform(90, 240) * S
        ln = rng.uniform(20, 55) * S
        x1 = rx + d0 * math.cos(a)
        y1 = ry - d0 * math.sin(a)
        x2 = x1 + ln * math.cos(a)
        y2 = y1 - ln * math.sin(a)
        # keep streaks clear of the title, the text column and the bottom band
        ok = True
        for (x, y) in [(x1, y1), (x2, y2)]:
            if x > 196 * S or y < 46 * S or y > 250 * S or x < 4 * S:
                ok = False
        if not ok:
            continue
        kept += 1
        d.line([(x1, y1), (x2, y2)], fill=WHITE, width=S)
    # scattered stars
    for _ in range(70):
        x = rng.uniform(0, W) * S
        y = rng.uniform(0, H - 30) * S
        r = rng.uniform(0.5, 1.3) * S
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    # eclipse: corona + black moon
    cx, cy = 103 * S, 128 * S
    R = 48 * S
    for k in range(60):
        a = 2 * math.pi * k / 60
        ln = R * (1.25 + 0.55 * abs(math.sin(3 * a + 0.7)) + rng.uniform(0, 0.18))
        d.line([(cx + R * 1.02 * math.cos(a), cy + R * 1.02 * math.sin(a)),
                (cx + ln * math.cos(a), cy + ln * math.sin(a))],
               fill=WHITE, width=S)
    d.ellipse([cx - R * 1.14, cy - R * 1.14, cx + R * 1.14, cy + R * 1.14], fill=WHITE)
    # prominences: red flecks at the limb, then the moon
    for k in range(9):
        a = rng.uniform(0, 2 * math.pi)
        pr = R * 1.06
        r = rng.uniform(2.5, 5) * S
        d.ellipse([cx + pr * math.cos(a) - r, cy + pr * math.sin(a) - r,
                   cx + pr * math.cos(a) + r, cy + pr * math.sin(a) + r], fill=RED)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)

    ft = font(SANS_B, 20 * S)
    fh = font(SANS_B, 11 * S)
    fb = font(SANS, 10 * S)
    fsm = font(SANS, 9 * S)
    d.text((16 * S, 12 * S), "THE AUGUST SKY", font=ft, fill=WHITE)
    d.line([(16 * S, 40 * S), (215 * S, 40 * S)], fill=RED, width=2 * S)

    x = 208 * S
    entries = [
        ("12 VIII  TOTAL SOLAR ECLIPSE", "Arctic → Greenland → Iceland → Spain", 58),
        ("12–13 VIII  PERSEIDS PEAK", "~100 meteors/hr, moonless dark sky", 106),
        ("15 VIII  VENUS", "greatest elongation — evening star", 154),
        ("27 VIII  LUNAR ECLIPSE", "partial, 93% into Earth's shadow", 202),
    ]
    for head, sub, y in entries:
        d.text((x, y * S), head, font=fh, fill=RED)
        d.text((x, (y + 16) * S), sub, font=fb, fill=WHITE)
    d.rectangle([0, (H - 26) * S, W * S, H * S], fill=RED)
    text_center(d, (W * S / 2, (H - 13) * S),
                "eclipse by day, meteors by night — one date: August 12", font(SANS_B, 10 * S), WHITE)
    finish(im, "2.png")


# ----------------------------------------------------------------------------
# 3 · CONSTRUCTIVIST COMPOSITION (Lissitzky homage)
# ----------------------------------------------------------------------------

def img3():
    rng = random.Random(SEED + 3)
    im, d = canvas(WHITE)
    # thick black diagonal bar
    def bar(x1, y1, x2, y2, w, fill):
        a = math.atan2(y2 - y1, x2 - x1)
        dx, dy = -math.sin(a) * w / 2, math.cos(a) * w / 2
        d.polygon([(x1 + dx, y1 + dy), (x2 + dx, y2 + dy),
                   (x2 - dx, y2 - dy), (x1 - dx, y1 - dy)], fill=fill)

    # one thick black diagonal bar across the whole frame
    bar(-20 * S, 302 * S, 430 * S, 88 * S, 16 * S, BLACK)
    # big red circle
    cx, cy, R = 268 * S, 104 * S, 80 * S
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=RED)
    # white wedge piercing bar and circle from the lower left
    wedge = [(18 * S, 238 * S), (60 * S, 282 * S), (cx - 4 * S, cy + 2 * S)]
    d.polygon(wedge, fill=WHITE)
    d.polygon(wedge, outline=BLACK, width=int(1.6 * S))
    # satellites: a few small filled blocks, kept away from circle and type
    blocks = [(330, 232, 20, 12, BLACK), (356, 250, 10, 8, RED),
              (40, 200, 14, 9, BLACK), (90, 246, 9, 9, RED),
              (150, 22, 30, 5, BLACK)]
    for x, y, w, h, c in blocks:
        d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], fill=c)
    # cross ticks top-right
    d.line([(330 * S, 24 * S), (392 * S, 24 * S)], fill=BLACK, width=2 * S)
    d.line([(352 * S, 10 * S), (352 * S, 58 * S)], fill=BLACK, width=2 * S)
    # rotated type climbing the same diagonal
    layer = Image.new("RGBA", (280 * S, 60 * S), (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    dl.text((0, 0), "АВГУСТ", font=font(SANS_B, 36 * S), fill=BLACK + (255,))
    layer = layer.rotate(27, expand=True, resample=Image.BICUBIC)
    im.paste(layer, (14 * S, 40 * S), layer)
    d.text((206 * S, 282 * S), "1.VIII.2026 · после красного клина", font=font(MONO, 9 * S), fill=BLACK)
    finish(im, "3.png")


# ----------------------------------------------------------------------------
# 4 · LUGHNASADH — FIRST HARVEST
# ----------------------------------------------------------------------------

def img4():
    rng = random.Random(SEED + 4)
    im, d = canvas(WHITE)
    # harvest sun
    scx, scy, sr = 200 * S, 108 * S, 92 * S
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=RED)
    # birds
    for bx, by, bw in [(60, 48, 9), (88, 60, 7), (330, 40, 8), (352, 55, 6)]:
        d.arc([(bx - bw) * S, (by - 4) * S, bx * S, (by + 5) * S], 200, 340, fill=BLACK, width=S)
        d.arc([bx * S, (by - 4) * S, (bx + bw) * S, (by + 5) * S], 200, 340, fill=BLACK, width=S)
    # wheat field
    def stalk(x, hgt, bend, head_n):
        base = (H - 26) * S
        pts = []
        for i in range(25):
            t = i / 24
            xx = x + bend * (t ** 2) * S
            yy = base - hgt * t * S
            pts.append((xx, yy))
        d.line(pts, fill=BLACK, width=int(1.6 * S))
        # awns + grains at the top
        tipx, tipy = pts[-1]
        ang = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
        for g in range(head_n):
            t = g / head_n
            gx = tipx - math.cos(ang) * t * 34 * S * -1
            gy = tipy - math.sin(ang) * t * 34 * S * -1
            for side in (-1, 1):
                ex = gx + side * 4.2 * S * math.cos(ang + math.pi / 2)
                ey = gy + side * 4.2 * S * math.sin(ang + math.pi / 2)
                r1, r2 = 4.6 * S, 2.5 * S
                d.ellipse([ex - r1, ey - r2, ex + r1, ey + r2], fill=BLACK)
                ax = ex + math.cos(ang - side * 0.35) * 13 * S
                ay = ey + math.sin(ang - side * 0.35) * 13 * S
                d.line([(ex, ey), (ax, ay)], fill=BLACK, width=S)
    xs = sorted(rng.uniform(-10, 410) for _ in range(34))
    for x in xs:
        hgt = rng.uniform(95, 205)
        bend = rng.uniform(-26, 26)
        stalk(x * S, hgt, bend, rng.randint(4, 6))
    # ground + caption
    d.rectangle([0, (H - 26) * S, W * S, H * S], fill=BLACK)
    text_center(d, (W * S / 2, (H - 13) * S),
                "L U G H N A S A D H  ·  the first harvest  ·  1 August", font(SANS_B, 11 * S), WHITE)
    finish(im, "4.png")


# ----------------------------------------------------------------------------
# 5 · CALL ME ISHMAEL — Melville's 207th birthday
# ----------------------------------------------------------------------------

def img5():
    rng = random.Random(SEED + 5)
    im, d = canvas(WHITE)
    # sea: wavy black mass over the lower part
    sea_y = 150
    pts = [(0, H * S)]
    for x in range(0, W + 1, 4):
        y = sea_y + 6 * math.sin(x / 26) + 3.4 * math.sin(x / 9 + 2)
        pts.append((x * S, y * S))
    pts.append((W * S, H * S))
    d.polygon(pts, fill=BLACK)
    # secondary white wave lines inside the sea
    for row in range(3):
        yy = sea_y + 34 + row * 38
        wl = []
        for x in range(0, W + 1, 4):
            y = yy + 5 * math.sin(x / 22 + row * 1.7) + 3 * math.sin(x / 8 + row)
            wl.append((x * S, y * S))
        d.line(wl, fill=WHITE, width=S)

    # the white whale (sperm whale, facing left), silhouette in the sea
    ox, oy = 60, 175          # placement
    sc = 1.05 * S
    body = [(0, 18), (14, 11), (46, 6), (86, 4), (128, 8), (168, 16),
            (200, 25), (222, 31), (230, 33),          # tail stock top
            (230, 45),                                 # stock bottom
            (206, 47), (168, 52), (120, 56), (76, 58), (34, 56),
            (10, 50), (0, 44)]
    d.polygon([(ox * S + x * sc, oy * S + y * sc) for x, y in body], fill=WHITE)
    flukes = [(226, 30), (252, 8), (268, 4), (256, 30), (286, 46),
              (272, 58), (244, 46), (228, 48)]
    d.polygon([(ox * S + x * sc, oy * S + y * sc) for x, y in flukes], fill=WHITE)
    fin = [(84, 56), (100, 76), (106, 57)]
    d.polygon([(ox * S + x * sc, oy * S + y * sc) for x, y in fin], fill=WHITE)
    # eye
    ex, ey = ox * S + 26 * sc, oy * S + 38 * sc
    d.ellipse([ex - 2.4 * S, ey - 2.4 * S, ex + 2.4 * S, ey + 2.4 * S], fill=RED)
    # spout
    sx, sy = ox * S + 16 * sc, oy * S + 6 * sc
    for a in (-0.5, -0.15, 0.2):
        d.line([(sx, sy), (sx + 26 * S * math.sin(a), sy - 26 * S * math.cos(a))],
               fill=WHITE, width=int(1.6 * S))
    # harpoon line arcing in from the sky, red
    rope = []
    for i in range(50):
        t = i / 49
        x = 388 - 152 * t ** 1.9
        y = 18 + 172 * t + 8 * math.sin(t * 7)
        rope.append((x * S, y * S))
    d.line(rope, fill=RED, width=int(2 * S))
    hx, hy = rope[-1]
    d.polygon([(hx - 4 * S, hy + 2 * S), (hx + 12 * S, hy - 10 * S), (hx + 13 * S, hy - 1 * S)],
              fill=RED)

    # type
    d.text((22 * S, 30 * S), "Call me Ishmael.", font=font(SERIF_I, 30 * S), fill=BLACK)
    d.text((24 * S, 72 * S), "MOBY-DICK · Herman Melville, born 1 August 1819",
           font=font(SANS, 10 * S), fill=BLACK)
    d.line([(24 * S, 66 * S), (200 * S, 66 * S)], fill=RED, width=int(1.5 * S))
    finish(im, "5.png")


if __name__ == "__main__":
    img1()
    img2()
    img3()
    img4()
    img5()
