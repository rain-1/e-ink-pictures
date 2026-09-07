#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-06.

Five 400x300 images in exactly three colours (white, black, red) for a
black/white/red e-ink panel.

Today:
  1. Red Wedge     — a constructivist composition (finally), after Lissitzky 1919
  2. Kamon         — six family crests built from circles and straight lines only,
                     the sixth one invented today and drawn in red
  3. Victoria      — 6 Sept 1522: the first ship to sail around the world comes home
  4. Moon & Mars   — this dawn's waning crescent (26%) 3° from Mars in Gemini
  5. Sand          — Norman Woodland's birthday: Morse code pulled into bars,
                     and a real, scannable Code 39 barcode of today's date

Run from this folder:  python3 generate.py   (needs pillow + numpy;
ne_110m_land.geojson sits next to this file).
"""

import json
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253
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


def canvas(bg=WHITE, s=SS):
    img = Image.new("RGB", (W * s, H * s), bg)
    return img, ImageDraw.Draw(img)


def rotated_text(img, text, fnt, xy, angle, fill):
    """Draw text rotated by `angle` degrees, centred on xy."""
    l, t, r, b = fnt.getbbox(text)
    tw, th = r - l, b - t
    pad = 8
    layer = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((pad - l, pad - t), text, font=fnt, fill=fill + (255,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    x, y = xy
    img.paste(layer, (int(x - layer.width / 2), int(y - layer.height / 2)), layer)


# ---------------------------------------------------------------- 1. Red Wedge
def image1_red_wedge():
    s = SS
    img, dr = canvas(WHITE, s)
    sw, sh = W * s, H * s

    # The field: a black slab covering the lower-right, cut on a steep diagonal.
    dr.polygon([(sw * 0.62, 0), (sw, 0), (sw, sh), (sw * 0.20, sh)], fill=BLACK)

    # The white circle sits astride the diagonal, mostly in the black.
    cx, cy, r = sw * 0.66, sh * 0.50, sh * 0.31
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)

    # A thin black ring inside it, off-centre: the circle has a pupil.
    r2 = r * 0.62
    ox, oy = cx + r * 0.12, cy - r * 0.10
    dr.ellipse([ox - r2, oy - r2, ox + r2, oy + r2], outline=BLACK, width=int(2.2 * s))

    # The red wedge: enters from the upper-left, tip buried in the circle.
    tip = (cx + r * 0.08, cy + r * 0.02)
    base_a = (-10 * s, sh * 0.08)
    base_b = (-10 * s, sh * 0.44)
    dr.polygon([base_a, base_b, tip], fill=RED)

    # A few small constructivist satellites.
    # black bar on the white side
    dr.rectangle([sw * 0.03, sh * 0.95, sw * 0.17, sh * 0.95 + 5 * s], fill=BLACK)
    # small red disc echoing the big circle
    rr = sh * 0.045
    dr.ellipse([sw * 0.08 - rr, sh * 0.60 - rr, sw * 0.08 + rr, sh * 0.60 + rr], fill=RED)
    # black wedge counter-thrust from below, tiny
    dr.polygon([(sw * 0.30, sh), (sw * 0.38, sh), (sw * 0.335, sh * 0.72)], fill=BLACK)
    # thin white rule crossing the black field, parallel to the cut
    dr.line([(sw * 0.72, 0), (sw * 0.30, sh)], fill=WHITE, width=int(1.2 * s))
    # a white square, up in the black corner
    q = sh * 0.06
    dr.rectangle([sw * 0.90 - q, sh * 0.10, sw * 0.90, sh * 0.10 + q], fill=WHITE)
    # red square inside the circle's lower rim
    q2 = sh * 0.035
    dr.rectangle([cx + r * 0.45, cy + r * 0.45, cx + r * 0.45 + q2, cy + r * 0.45 + q2], fill=RED)

    # Typography on the diagonal.
    # text runs parallel to the cut, just inside the white
    ang = math.degrees(math.atan2(sh, sw * 0.42))  # slope of the cut (~60°)
    nx, ny = -sh, -sw * 0.42
    nl = math.hypot(nx, ny)
    nx, ny = nx / nl, ny / nl

    def along(t, off):
        return (sw * 0.62 - sw * 0.42 * t + nx * off, sh * t + ny * off)

    rotated_text(img, "THREE COLOURS", font(F_SANS_B, 20 * s), along(0.72, 54 * s), ang, BLACK)
    rotated_text(img, "ARE ENOUGH", font(F_SANS_B, 20 * s), along(0.72, 26 * s), ang, BLACK)
    rotated_text(img, "6 · IX · 2026", font(F_MONO_B, 9 * s), (sw * 0.84, sh * 0.90), 0, WHITE)
    rotated_text(img, "after Lissitzky, 1919", font(F_MONO, 7 * s), (sw * 0.84, sh * 0.95), 0, WHITE)
    return finalize(img, dither=False)


# ---------------------------------------------------------------- 2. Kamon
def ring(dr, c, r, w, fill):
    x, y = c
    dr.ellipse([x - r, y - r, x + r, y + r], fill=fill)
    dr.ellipse([x - r + w, y - r + w, x + r - w, y + r - w], fill=WHITE)


def disc(dr, c, r, fill):
    x, y = c
    dr.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def polar(c, r, ang_deg):
    a = math.radians(ang_deg)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def kamon_mitsuboshi(dr, c, R, col):
    ring(dr, c, R, R * 0.08, col)
    r = R * 0.31
    d = r / math.cos(math.radians(30)) * 1.0  # tangent triangle
    for k in range(3):
        disc(dr, polar(c, d, -90 + 120 * k), r, col)


def kamon_kuyo(dr, c, R, col):
    disc(dr, c, R * 0.34, col)
    for k in range(8):
        disc(dr, polar(c, R * 0.70, 45 * k), R * 0.215, col)


def kamon_mitsu_uroko(dr, c, R, col):
    h = R * 1.55
    side = h / (math.sqrt(3) / 2)
    top = (c[0], c[1] - h * 0.55)
    ring(dr, c, R, R * 0.07, col)
    for (ox, oy) in [(0, 0), (-side / 4, h / 2), (side / 4, h / 2)]:
        p = (top[0] + ox, top[1] + oy)
        dr.polygon([p, (p[0] - side / 4, p[1] + h / 2), (p[0] + side / 4, p[1] + h / 2)], fill=col)


def kamon_mitsudomoe(dr, c, R, col):
    """Three commas. Each is a head disc plus a tail that sweeps along the rim
    and thins to nothing."""
    ring(dr, c, R, R * 0.06, col)
    Ri = R * 0.86
    for k in range(3):
        phi = -90 + 120 * k
        head_c = polar(c, Ri * 0.50, phi)
        disc(dr, head_c, Ri * 0.34, col)
        pts_out, pts_in = [], []
        n = 40
        for i in range(n + 1):
            t = i / n
            a = phi - 175 * t
            thick = Ri * 0.52 * (1 - t) ** 1.6
            pts_out.append(polar(c, Ri * 0.98, a))
            pts_in.append(polar(c, Ri * 0.98 - thick, a))
        dr.polygon(pts_out + pts_in[::-1], fill=col)


def kamon_wachigai(dr, c, R, col):
    """Four interlocking rings (yotsu-wachigai), with an over-under weave."""
    rr = R * 0.47
    d = R * 0.50
    w = R * 0.11
    centers = [polar(c, d, 45 + 90 * k) for k in range(4)]
    for cc in centers:
        ring(dr, cc, rr, w, col)
    # weave: at each crossing between ring i and i+1, re-draw one ring's arc on top
    for i in range(4):
        a, b = centers[i], centers[(i + 1) % 4]
        # the two rings cross near the midpoint between their centres, at two spots
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        # crossing points lie on the perpendicular bisector
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        h = math.sqrt(max(rr * rr - (L / 2) ** 2, 0))
        nx, ny = -dy / L, dx / L
        for sgn, top in [(1, a), (-1, b)]:
            px, py = mx + sgn * h * nx, my + sgn * h * ny
            # redraw the small arc of `top` around (px,py): clip via a disc mask
            ang = math.degrees(math.atan2(py - top[1], px - top[0]))
            box = [top[0] - rr + w / 2, top[1] - rr + w / 2, top[0] + rr - w / 2, top[1] + rr - w / 2]
            dr.arc(box, ang - 14, ang + 14, fill=WHITE, width=int(w * 1.9))
            dr.arc(box, ang - 12, ang + 12, fill=col, width=int(w))


def kamon_today(dr, c, R, col, rng):
    """A crest that did not exist yesterday: n-fold symmetry, circles and lines."""
    n = rng.choice([5, 6, 7, 8])
    ring(dr, c, R, R * rng.choice([0.05, 0.08, 0.12]), col)
    kind = rng.choice(["petals", "rays", "beads"])
    rot = -90
    if kind == "petals":
        pr = R * rng.uniform(0.22, 0.30)
        d = R * 0.62
        for k in range(n):
            disc(dr, polar(c, d, rot + 360 * k / n), pr, col)
        for k in range(n):
            disc(dr, polar(c, d, rot + 360 * k / n), pr * 0.45, WHITE)
        disc(dr, c, R * 0.20, col)
    elif kind == "rays":
        for k in range(n):
            a = rot + 360 * k / n
            p1 = polar(c, R * 0.30, a)
            p2 = polar(c, R * 0.80, a)
            dr.line([p1, p2], fill=col, width=int(R * 0.12))
            disc(dr, p2, R * 0.10, col)
        ring(dr, c, R * 0.30, R * 0.08, col)
        disc(dr, c, R * 0.10, col)
    else:
        ring(dr, c, R * 0.58, R * 0.09, col)
        for k in range(n):
            a = rot + 360 * k / n
            disc(dr, polar(c, R * 0.58, a), R * 0.14, col)
            disc(dr, polar(c, R * 0.58, a), R * 0.06, WHITE)
        disc(dr, c, R * 0.16, col)
    return n, kind


def image2_kamon():
    s = SS
    rng = random.Random(20260906)
    img, dr = canvas(WHITE, s)
    cols, rows = 3, 2
    cell_w, cell_h = W / cols, 128
    R = 44 * s
    crests = [
        ("丸に三つ星", "maru ni mitsuboshi", kamon_mitsuboshi),
        ("九曜", "kuyō — nine stars", kamon_kuyo),
        ("丸に三つ鱗", "mitsu uroko — three scales", kamon_mitsu_uroko),
        ("三つ巴", "mitsudomoe", kamon_mitsudomoe),
        ("四つ輪違い", "yotsu wachigai", kamon_wachigai),
    ]
    f_jp = font(F_JP, 9 * s)
    f_small = font(F_SANS, 6 * s)
    today_desc = ""
    for i in range(6):
        col_i, row_i = i % cols, i // cols
        cx = (col_i + 0.5) * cell_w * s
        cy = (row_i * cell_h + 58) * s
        if i < 5:
            jp, name, fn = crests[i]
            fn(dr, (cx, cy), R, BLACK)
        else:
            n, kind = kamon_today(dr, (cx, cy), R, RED, rng)
            jp, name = "今日の紋", f"today's crest · {n}-fold {kind}"
            today_desc = name
        dr.text((cx, cy + R + 8 * s), jp, font=f_jp, fill=BLACK, anchor="mt")
        dr.text((cx, cy + R + 20 * s), name, font=f_small, fill=BLACK, anchor="mt")
    # bottom strip
    y0 = 262 * s
    dr.rectangle([0, y0, W * s, H * s], fill=BLACK)
    dr.text((10 * s, 281 * s), "KAMON", font=font(F_SANS_B, 13 * s), fill=WHITE, anchor="lm")
    dr.text((72 * s, 281 * s), "family crests: perfect circles and straight lines, nothing drawn freehand",
            font=font(F_SANS, 7 * s), fill=WHITE, anchor="lm")
    dr.text((390 * s, 281 * s), "家紋", font=font(F_JP, 14 * s), fill=RED, anchor="rm")
    return finalize(img, dither=False)


# ---------------------------------------------------------------- 3. Victoria
ROUTE = [  # (lon, lat)
    (-6.35, 36.78), (-10.5, 33.0), (-16.5, 28.2), (-19.5, 20.0), (-22.0, 12.0),
    (-26.0, 4.0), (-33.0, -6.0), (-38.5, -14.0), (-43.2, -22.9), (-48.0, -28.5),
    (-55.5, -35.0), (-62.0, -41.0), (-67.7, -49.3), (-68.4, -52.3), (-71.5, -53.4),
    (-75.0, -52.8), (-77.5, -47.0), (-80.0, -38.0), (-86.0, -27.0), (-95.0, -16.0),
    (-108.0, -8.0), (-125.0, 0.0), (-145.0, 6.0), (-165.0, 10.0), (180.0, 12.5),
    (165.0, 13.2), (144.8, 13.4), (130.0, 12.0), (125.5, 11.0), (123.9, 10.3),
    (121.5, 8.5), (118.7, 9.5), (115.0, 5.0), (116.5, 3.5), (120.5, 4.5),
    (124.5, 3.0), (127.4, 0.7), (128.5, -3.0), (127.0, -7.0), (125.0, -9.5),
    (118.0, -14.0), (105.0, -24.0), (90.0, -32.0), (72.0, -38.0), (52.0, -40.5),
    (34.0, -39.0), (18.5, -35.5), (13.0, -28.0), (7.0, -18.0), (0.0, -8.0),
    (-8.0, 0.0), (-16.0, 7.0), (-23.5, 15.0), (-24.0, 21.0), (-20.0, 27.0),
    (-13.5, 32.5), (-8.5, 35.5), (-6.35, 36.78),
]


def image3_victoria():
    s = SS
    img, dr = canvas(WHITE, s)
    lon0, lon1 = -145.0, 165.0          # 310° of longitude across the full width
    lat_top, lat_bot = 72.0, -62.0
    sx = W * s / (lon1 - lon0)
    map_top = 12 * s
    map_h = (lat_top - lat_bot) * sx
    map_bot = map_top + map_h

    def proj(lon, lat):
        return ((lon - lon0) * sx, map_top + (lat_top - lat) * sx)

    # land
    with open(os.path.join(HERE, "ne_110m_land.geojson")) as f:
        land = json.load(f)
    for feat in land["features"]:
        for ringc in feat["geometry"]["coordinates"]:
            pts = [proj(lon, lat) for lon, lat in ringc]
            if len(pts) >= 3:
                dr.polygon(pts, fill=BLACK)
    # tidy the map edges
    dr.rectangle([0, 0, W * s, map_top - 1], fill=WHITE)
    dr.rectangle([0, map_bot, W * s, H * s], fill=WHITE)
    # graticule: equator and tropics as thin white-on-black / black-on-white dashes
    for lat in (23.44, 0.0, -23.44):
        y = proj(0, lat)[1]
        for x in range(0, W * s, 6 * s):
            dr.line([(x, y), (x + 2 * s, y)], fill=RED if lat == 0 else BLACK, width=max(1, s // 2))

    # route, split where it wraps off the edge
    lw = int(2.2 * s)
    segs, cur = [], []
    for i, (lon, lat) in enumerate(ROUTE):
        if i and abs(lon - ROUTE[i - 1][0]) > 180:
            segs.append(cur)
            cur = []
        cur.append(proj(lon, lat))
    segs.append(cur)
    for seg in segs:
        if len(seg) > 1:
            dr.line(seg, fill=RED, width=lw, joint="curve")
    # extend the edge-leaving segments to the very border
    # (the Pacific leg goes off the left edge and returns from the right)
    # markers
    marks = [(-6.35, 36.78, "Sanlúcar", (-34, -4)), (-68.4, -52.3, "the Strait", (-2, 6)),
             (123.9, 10.3, "Mactan", (6, -3)), (127.4, 0.7, "Tidore", (6, 4)),
             (18.5, -35.5, "Good Hope", (4, 6)), (-23.5, 15.0, "C. Verde", (-46, -2))]
    f_lab = font(F_SANS, 6.5 * s)
    for lon, lat, name, (dx, dy) in marks:
        x, y = proj(lon, lat)
        disc(dr, (x, y), 3.2 * s, WHITE)
        disc(dr, (x, y), 2.0 * s, RED)
        # label with a white halo so it stays legible over land
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                dr.text((x + dx * s + ox * s * 0.7, y + dy * s + oy * s * 0.7), name, font=f_lab, fill=WHITE)
        dr.text((x + dx * s, y + dy * s), name, font=f_lab, fill=BLACK)

    # text block below the map
    ty = map_bot + 6 * s
    dr.text((10 * s, ty), "VICTORIA", font=font(F_SERIF_B, 26 * s), fill=BLACK)
    dr.text((10 * s, ty + 30 * s), "6 September 1522 · Sanlúcar de Barrameda", font=font(F_SERIF_I, 9.5 * s), fill=BLACK)
    body = ("Five ships and about 270 men left in 1519. One ship and 18 men\n"
            "came back, the hold full of cloves, having sailed west until home —\n"
            "and found the calendar ashore one day ahead of their own.")
    dr.multiline_text((10 * s, ty + 44 * s), body, font=font(F_SERIF, 9 * s), fill=BLACK, spacing=2.5 * s)
    dr.text((390 * s, ty + 4 * s), "504", font=font(F_SERIF_B, 30 * s), fill=RED, anchor="ra")
    dr.text((390 * s, ty + 38 * s), "years ago today", font=font(F_SERIF_I, 8 * s), fill=BLACK, anchor="ra")
    return finalize(img, dither=False)


# ---------------------------------------------------------------- 4. Moon & Mars
def image4_moon_mars():
    s = SS
    img, dr = canvas(BLACK, s)
    sky_h = 212 * s
    rng = random.Random(906)
    # faint stars
    for _ in range(140):
        x, y = rng.uniform(0, W * s), rng.uniform(0, sky_h)
        v = rng.choice([90, 130, 180, 255])
        r = rng.choice([0.5, 0.7, 1.0]) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # the Moon: waning crescent, 26% lit, lit limb on the left, earthshine on the rest
    cx, cy, R = 150 * s, 100 * s, 66 * s
    f_ill = 0.26
    c = 2 * f_ill - 1  # cos of phase angle (-0.48)
    yy, xx = np.mgrid[0:H * s, 0:W * s]
    dx, dy = (xx - cx) / R, (yy - cy) / R
    inside = dx * dx + dy * dy <= 1.0
    half_w = np.sqrt(np.clip(1 - dy * dy, 0, 1))
    lit = inside & (dx <= c * half_w)
    arr = np.array(img)
    # earthshine: dim grey disc with a subtle gradient (brighter toward the lit limb)
    shade = (38 + 30 * (1 - (dx + 1) / 2)).clip(0, 255)
    for ch in range(3):
        arr[..., ch][inside] = shade[inside]
    # lit crescent
    for ch in range(3):
        arr[..., ch][lit] = 255
    img = Image.fromarray(arr)
    dr = ImageDraw.Draw(img)
    # a few maria on the lit part (grey blobs) to suggest the face
    for (mx, my, mr) in [(-0.78, -0.35, 0.16), (-0.70, 0.05, 0.13), (-0.62, 0.42, 0.11)]:
        px, py, pr = cx + mx * R, cy + my * R, mr * R
        # only draw where lit; cheap: draw then re-mask below
        dr.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(165, 165, 165))
    arr = np.array(img)
    for ch in range(3):
        arr[..., ch][inside & ~lit] = shade[inside & ~lit]
    img = Image.fromarray(arr)
    dr = ImageDraw.Draw(img)

    # Mars, 3° south of the Moon (not to scale: about six moon-widths)
    mx, my = 208 * s, 178 * s
    for a in range(0, 360, 90):
        dr.line([polar((mx, my), 4 * s, a), polar((mx, my), 11 * s, a)], fill=RED, width=int(1.2 * s))
    disc(dr, (mx, my), 4.2 * s, RED)
    dr.text((mx + 15 * s, my), "MARS", font=font(F_SANS_B, 9 * s), fill=RED, anchor="lm")
    dr.text((mx + 15 * s, my + 11 * s), "3° south of the Moon", font=font(F_SANS, 6.5 * s), fill=WHITE, anchor="lm")

    # Castor & Pollux, and the Twins' shoulders as a faint stick figure
    stars = {"Castor": (300 * s, 42 * s, 3.0), "Pollux": (335 * s, 66 * s, 3.4)}
    for name, (x, y, r) in stars.items():
        disc(dr, (x, y), r * s, WHITE)
        dr.text((x + 8 * s, y), name, font=font(F_SANS, 7 * s), fill=WHITE, anchor="lm")
    # Gemini body lines, dim
    body = [((300, 42), (292, 95)), ((292, 95), (286, 150)), ((335, 66), (330, 118)), ((330, 118), (322, 168))]
    for (a, b) in body:
        dr.line([(a[0] * s, a[1] * s), (b[0] * s, b[1] * s)], fill=(90, 90, 90), width=s)
    for (x, y) in [(292, 95), (286, 150), (330, 118), (322, 168)]:
        disc(dr, (x * s, y * s), 1.6 * s, (200, 200, 200))
    dr.text((312 * s, 24 * s), "GEMINI", font=font(F_SANS, 7 * s), fill=WHITE, anchor="mm")

    # header
    dr.text((12 * s, 12 * s), "DAWN · 6 SEPTEMBER", font=font(F_SANS_B, 11 * s), fill=WHITE)
    dr.text((12 * s, 27 * s), "waning crescent, 26% lit · earthshine on the dark side", font=font(F_SANS, 7 * s), fill=(200, 200, 200))
    dr.text((12 * s, 190 * s), "look east, an hour before sunrise", font=font(F_SANS, 7 * s), fill=(200, 200, 200))

    # almanac strip
    dr.rectangle([0, sky_h, W * s, H * s], fill=WHITE)
    dr.rectangle([0, sky_h, W * s, sky_h + 2 * s], fill=RED)
    f_d = font(F_MONO_B, 8 * s)
    f_t = font(F_SANS, 7.5 * s)
    rows = [("SEP 8", "Moon hides Jupiter (occultation, N. America)"),
            ("SEP 11", "New Moon — darkest skies"),
            ("SEP 14", "Moon hides Venus"),
            ("SEP 18", "Venus at greatest brilliance"),
            ("SEP 22", "Equinox · SEP 26 Harvest Moon · Neptune opposition")]
    y = sky_h + 12 * s
    for d, t in rows:
        dr.text((12 * s, y), d, font=f_d, fill=RED)
        dr.text((60 * s, y), t, font=f_t, fill=BLACK)
        y += 15.5 * s
    return finalize(img, dither=True)


# ---------------------------------------------------------------- 5. Sand
MORSE = {"S": "...", "A": ".-", "N": "-.", "D": "-.."}
CODE39 = {
    "0": "000110100", "1": "100100001", "2": "001100001", "3": "101100000",
    "4": "000110001", "5": "100110000", "6": "001110000", "7": "000100101",
    "8": "100100100", "9": "001100100", "A": "100001001", "B": "001001001",
    "C": "101001000", "D": "000011001", "E": "100011000", "F": "001011000",
    "G": "000001101", "H": "100001100", "I": "001001100", "J": "000011100",
    "K": "100000011", "L": "001000011", "M": "101000010", "N": "000010011",
    "O": "100010010", "P": "001010010", "Q": "000000111", "R": "100000110",
    "S": "001000110", "T": "000010110", "U": "110000001", "V": "011000001",
    "W": "111000000", "X": "010010001", "Y": "110010000", "Z": "011010000",
    "-": "010000101", ".": "110000100", " ": "011000100", "$": "010101000",
    "/": "010100010", "+": "010001010", "%": "000101010", "*": "010010100",
}


def code39_widths(text, narrow, wide):
    """Return a list of (is_bar, width) runs for '*text*' incl. inter-character gaps."""
    runs = []
    for ch in "*" + text + "*":
        pat = CODE39[ch]
        for i, bit in enumerate(pat):
            runs.append((i % 2 == 0, wide if bit == "1" else narrow))
        runs.append((False, narrow))
    return runs[:-1]


def image5_sand():
    s = SS
    img, dr = canvas(WHITE, s)

    # Top: Morse for SAND, in red — each mark pulled downward into a bar.
    x = 40 * s
    y_mark = 34 * s
    unit = 7 * s
    y_bar_top = y_mark + 12 * s
    y_bar_bot = 118 * s
    f_letter = font(F_MONO_B, 9 * s)
    for li, letter in enumerate("SAND"):
        x_start = x
        for mark in MORSE[letter]:
            wdt = unit if mark == "." else unit * 3
            if mark == ".":
                dr.ellipse([x, y_mark - unit / 2, x + unit, y_mark + unit / 2], fill=RED)
            else:
                dr.rounded_rectangle([x, y_mark - unit / 2, x + wdt, y_mark + unit / 2], radius=unit / 2, fill=RED)
            # the bar below it, thin where the mark was a dot, wide where a dash
            dr.rectangle([x, y_bar_top, x + wdt, y_bar_bot], fill=RED)
            x += wdt + unit
        # letter label under the group
        dr.text(((x_start + x - unit) / 2, y_bar_bot + 4 * s), letter, font=f_letter, fill=BLACK, anchor="mt")
        x += unit * 2
    dr.text((40 * s, 12 * s), "dots and dashes", font=font(F_SANS_B, 9 * s), fill=BLACK)
    dr.text((300 * s, 60 * s), "pulled downward\ninto lines:\na linear Morse code", font=font(F_SANS, 8 * s), fill=BLACK, spacing=2 * s)

    # Bottom: a real Code 39 barcode of today's date (scan it!)
    text = "6 SEP 2026"
    narrow, wide = 2 * s, 5 * s
    runs = code39_widths(text, narrow, wide)
    total = sum(w for _, w in runs)
    x = (W * s - total) / 2
    y0, y1 = 158 * s, 236 * s
    for is_bar, wdt in runs:
        if is_bar:
            dr.rectangle([x, y0, x + wdt - 1, y1], fill=BLACK)
        x += wdt
    dr.text((W * s / 2, y1 + 6 * s), "* 6 S E P 2 0 2 6 *", font=font(F_MONO, 9 * s), fill=BLACK, anchor="mt")

    # caption
    dr.rectangle([0, 268 * s, W * s, H * s], fill=BLACK)
    dr.text((10 * s, 284 * s), "N. J. WOODLAND", font=font(F_SANS_B, 9 * s), fill=RED, anchor="lm")
    dr.text((98 * s, 284 * s), "b. 6 Sept 1921 · four fingers dragged through the sand, Miami Beach, 1949",
            font=font(F_SANS, 7 * s), fill=WHITE, anchor="lm")
    return finalize(img, dither=False)


def main():
    out_dirs = [HERE, os.path.join(HERE, "..", "..", "images")]
    makers = [image1_red_wedge, image2_kamon, image3_victoria, image4_moon_mars, image5_sand]
    for i, mk in enumerate(makers, 1):
        im = mk()
        assert im.size == (W, H)
        for d in out_dirs:
            os.makedirs(d, exist_ok=True)
            im.save(os.path.join(d, f"{i}.png"), optimize=True)
        print("wrote", i)


if __name__ == "__main__":
    main()
