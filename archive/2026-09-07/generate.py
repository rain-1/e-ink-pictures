#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-07.

Five 400x300 images in exactly three colours (white, black, red) for a
black/white/red e-ink panel.  Today's five deliberately use modes that the
previous 46 days never touched: a television test card, a linocut animal,
a Penrose tiling, an op-art bulge, and a weaver's drawdown.

Run:  python3 generate.py            (writes ../../images/1..5.png and ./1..5.png)
"""

import cmath
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIRS = [os.path.join(HERE, "..", "..", "images"), HERE]

F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_HELV_B = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=False):
    """Downscale from the supersampled canvas and snap to the 3-colour palette."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def save(img, n):
    assert img.mode == "P" and img.size == (W, H)
    colours = {c for _, c in img.convert("RGB").getcolors()}
    assert colours <= {WHITE, BLACK, RED}, colours
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        img.save(os.path.join(d, f"{n}.png"), optimize=True)


def s(v):
    """scale a 1x coordinate to the supersampled canvas"""
    return v * SS


# ------------------------------------------------------------ 1. Test card
def image1_test_card():
    """A television test card for a three-colour screen.  7 Sept 1927: Philo
    Farnsworth's image dissector transmitted the first all-electronic television
    picture — a single straight line painted on a glass slide."""
    img = Image.new("RGB", (W * SS, H * SS), BLACK)
    dr = ImageDraw.Draw(img)
    cx, cy = 200, 138

    # outer frame + corner registration circles
    dr.rectangle([s(4), s(4), s(W - 5), s(H - 5)], outline=WHITE, width=s(2))
    for (x, y) in [(18, 18), (W - 18, 18), (18, H - 18), (W - 18, H - 18)]:
        dr.ellipse([s(x - 8), s(y - 8), s(x + 8), s(y + 8)], outline=WHITE, width=s(2))
        dr.line([s(x - 8), s(y), s(x + 8), s(y)], fill=WHITE, width=s(1))
        dr.line([s(x), s(y - 8), s(x), s(y + 8)], fill=WHITE, width=s(1))

    # background grid (every 25 px)
    for gx in range(25, W, 25):
        dr.line([s(gx), s(6), s(gx), s(H - 6)], fill=(70, 70, 70), width=s(1))
    for gy in range(25, H, 25):
        dr.line([s(6), s(gy), s(W - 6), s(gy)], fill=(70, 70, 70), width=s(1))

    # side panels: resolution wedges (bar frequency tests) left and right
    def wedge(x0, y0, w, h, widths):
        y = y0
        for bw in widths:
            n = 0
            yy = y
            while yy + bw <= y + h / len(widths) - 2:
                col = WHITE if n % 2 == 0 else BLACK
                dr.rectangle([s(x0), s(yy), s(x0 + w), s(yy + bw) - 1], fill=col)
                yy += bw
                n += 1
            y += h / len(widths)

    wedge(14, 44, 36, 180, [1, 2, 3, 4, 6])
    wedge(W - 50, 44, 36, 180, [6, 4, 3, 2, 1])

    # big white circle + crosshair
    R = 102
    dr.ellipse([s(cx - R), s(cy - R), s(cx + R), s(cy + R)], fill=WHITE, outline=BLACK, width=s(2))
    dr.line([s(cx - R), s(cy), s(cx + R), s(cy)], fill=BLACK, width=s(1))
    dr.line([s(cx), s(cy - R), s(cx), s(cy + R)], fill=BLACK, width=s(1))
    dr.ellipse([s(cx - R + 8), s(cy - R + 8), s(cx + R - 8), s(cy + R - 8)], outline=BLACK, width=s(1))

    # grey-step ramp across the top of the circle (dither will render the greys)
    steps = 9
    x0, x1, y0, y1 = cx - 72, cx + 72, cy - 84, cy - 60
    for i in range(steps):
        v = int(255 * i / (steps - 1))
        xa = x0 + (x1 - x0) * i / steps
        xb = x0 + (x1 - x0) * (i + 1) / steps
        dr.rectangle([s(xa), s(y0), s(xb), s(y1)], fill=(v, v, v))
    dr.rectangle([s(x0), s(y0), s(x1), s(y1)], outline=BLACK, width=s(1))

    # colour bars: the whole gamut of this screen
    y0, y1 = cy - 54, cy - 34
    for i, col in enumerate([BLACK, RED, WHITE, RED, BLACK, WHITE, RED]):
        xa = x0 + (x1 - x0) * i / 7
        xb = x0 + (x1 - x0) * (i + 1) / 7
        dr.rectangle([s(xa), s(y0), s(xb), s(y1)], fill=col)
    dr.rectangle([s(x0), s(y0), s(x1), s(y1)], outline=BLACK, width=s(1))

    # centre: the first picture. A black plate with one white straight line.
    px0, py0, px1, py1 = cx - 44, cy - 22, cx + 44, cy + 30
    dr.rectangle([s(px0), s(py0), s(px1), s(py1)], fill=BLACK)
    dr.line([s(cx), s(py0 + 6), s(cx), s(py1 - 6)], fill=WHITE, width=s(3))
    # faint scan lines over the plate (the image dissector scanned at 1x)
    for yy in range(py0 + 2, py1, 3):
        dr.line([s(px0), s(yy), s(px1), s(yy)], fill=(90, 90, 90), width=1)

    # red ring: the dissector's target
    dr.ellipse([s(cx - 58), s(cy - 28), s(cx + 58), s(cy + 36)], outline=RED, width=s(3))

    # lower half of the circle: fine checks + text
    for i in range(0, 12):
        for j in range(0, 3):
            if (i + j) % 2 == 0:
                xa = cx - 72 + i * 12
                ya = cy + 42 + j * 7
                dr.rectangle([s(xa), s(ya), s(xa + 12), s(ya + 7)], fill=BLACK)
    dr.rectangle([s(cx - 72), s(cy + 42), s(cx + 72), s(cy + 63)], outline=BLACK, width=s(1))

    f_big = font(F_HELV_B, s(13))
    f_sm = font(F_MONO, s(8))
    t = "7 · IX · 1927"
    tw = dr.textlength(t, font=f_big)
    dr.text((s(cx) - tw / 2, s(cy + 67)), t, font=f_big, fill=BLACK)
    t = "the first picture"
    tw = dr.textlength(t, font=f_sm)
    dr.text((s(cx) - tw / 2, s(cy + 84)), t, font=f_sm, fill=BLACK)

    # bottom black caption band (outside the circle)
    f_cap = font(F_MONO, s(9))
    f_capb = font(F_MONO_B, s(9))
    cap1 = "TEST CARD · 400×300 · 3 INKS"
    cap2 = "Farnsworth's image dissector, 202 Green St, San Francisco:"
    cap3 = "the first electronic television image was a straight line."
    for y_, t_, f_, c_ in [(H - 50, cap1, f_capb, RED), (H - 37, cap2, f_cap, WHITE), (H - 25, cap3, f_cap, WHITE)]:
        tw = dr.textlength(t_, font=f_)
        dr.text((s(cx) - tw / 2, s(y_)), t_, font=f_, fill=c_)

    # top band: station id
    f_top = font(F_HELV_B, s(11))
    dr.text((s(54), s(12)), "E-INK 1", font=f_top, fill=WHITE)
    t = "MON 7 SEPT 2026"
    tw = dr.textlength(t, font=f_top)
    dr.text((s(W - 54) - tw, s(12)), t, font=f_top, fill=WHITE)

    return finalize(img, dither=True)


# ------------------------------------------------------------ 2. Thylacine
def chaikin(points, iterations=4, closed=True):
    pts = list(points)
    for _ in range(iterations):
        new = []
        n = len(pts)
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            p = pts[i]
            q = pts[(i + 1) % n]
            new.append((0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]))
            new.append((0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1]))
        if not closed:
            new = [pts[0]] + new + [pts[-1]]
        pts = new
    return pts


def image2_thylacine():
    """Linocut.  The last known thylacine died at Beaumaris Zoo, Hobart, on
    7 September 1936 — ninety years ago today.  Australia keeps the date as
    National Threatened Species Day."""
    rng = random.Random(19360907)
    img = Image.new("RGB", (W * SS, H * SS), WHITE)
    dr = ImageDraw.Draw(img)

    # red sun, low, behind the animal
    sx, sy, sr = 118, 118, 82
    dr.ellipse([s(sx - sr), s(sy - sr), s(sx + sr), s(sy + sr)], fill=RED)

    # animal silhouette: control polygon in 1x coords, walking to the left,
    # head low, long stiff tail out to the right.
    body = [
        (58, 150), (62, 142), (72, 134), (84, 128), (94, 126),                    # muzzle -> forehead
        (98, 118), (102, 110), (108, 112), (110, 122),                            # ear
        (120, 124), (140, 120), (165, 116), (190, 118), (215, 124), (238, 132),   # neck, back
        (258, 140), (278, 148), (300, 152), (330, 156), (360, 160), (380, 164),   # tail top
        (382, 170), (364, 170), (334, 168), (304, 166), (282, 164),               # tail underside
        (272, 178), (274, 206), (278, 228), (272, 234), (258, 232), (254, 208), (248, 186),   # hind leg (rear)
        (242, 192), (246, 216), (248, 234), (234, 236), (228, 230), (226, 204), (220, 182),   # hind leg (front)
        (204, 176), (180, 178),                                                   # belly
        (164, 184), (160, 210), (164, 232), (150, 234), (144, 226), (146, 202), (144, 184),   # foreleg (rear)
        (136, 190), (132, 214), (134, 232), (120, 234), (114, 226), (118, 202), (122, 180),   # foreleg (front)
        (116, 166), (106, 158), (92, 156), (78, 156), (64, 156), (58, 154),       # throat, jaw
    ]
    outline = chaikin(body, 3)
    mask = Image.new("L", (W * SS, H * SS), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(s(x), s(y)) for x, y in outline], fill=255)

    # stripes: white cuts across the rump and tail base
    cuts = Image.new("L", (W * SS, H * SS), 0)
    cd = ImageDraw.Draw(cuts)
    for i in range(16):
        t = i / 15
        x = 176 + 104 * t
        top = 118 + 24 * t
        length = 36 + 22 * math.sin(t * math.pi) - 10 * t
        wtop = 3.2 - 1.2 * t
        poly = [(x - wtop, top - 6), (x + wtop, top - 6), (x + 4 + wtop * 0.4, top + length), (x + 4 - wtop * 0.4, top + length)]
        cd.polygon([(s(a), s(b)) for a, b in poly], fill=255)
    # gouge texture: short white strokes in the black
    for _ in range(170):
        x = rng.uniform(118, 390)
        y = rng.uniform(112, 240)
        L = rng.uniform(4, 11)
        ang = rng.uniform(-0.5, 0.5)
        cd.line([s(x), s(y), s(x + L * math.cos(ang)), s(y + L * math.sin(ang))], fill=255, width=s(1))
    # eye and nostril
    cd.ellipse([s(84), s(133), s(91), s(139)], fill=255)
    cd.ellipse([s(60), s(146), s(63), s(149)], fill=255)

    body_final = Image.fromarray(np.where((np.array(mask) > 127) & (np.array(cuts) <= 127), 255, 0).astype(np.uint8))
    img.paste(BLACK, mask=body_final)
    # pupil back in
    dr.ellipse([s(86), s(134.5), s(89.5), s(138)], fill=BLACK)
    # mouth line (the famous gape) — a thin white cut
    dr.line([s(60), s(153), s(88), s(155)], fill=WHITE, width=s(1))

    # ground: black band with white grass cuts
    gy = 236
    dr.rectangle([0, s(gy), s(W), s(H)], fill=BLACK)
    for _ in range(140):
        x = rng.uniform(0, W)
        h = rng.uniform(6, 22)
        lean = rng.uniform(-6, 6)
        dr.line([s(x), s(gy + 1), s(x + lean), s(gy - h)], fill=WHITE, width=s(1))
        dr.line([s(x), s(gy + 1), s(x + lean), s(gy - h)], fill=BLACK if rng.random() < 0.3 else WHITE, width=1)
    for _ in range(90):
        x = rng.uniform(0, W)
        y = rng.uniform(gy + 6, H - 4)
        L = rng.uniform(6, 20)
        dr.line([s(x), s(y), s(x + L), s(y - rng.uniform(0, 3))], fill=WHITE, width=s(1))

    # caption on the ground band
    f_t = font(F_SERIF_B, s(20))
    f_c = font(F_SERIF_I, s(11))
    f_cb = font(F_SERIF_B, s(11))
    dr.rectangle([s(14), s(H - 56), s(262), s(H - 8)], fill=BLACK)
    dr.text((s(20), s(H - 54)), "THYLACINE", font=f_t, fill=WHITE)
    dr.text((s(20), s(H - 30)), "Beaumaris Zoo, Hobart · 7 September 1936", font=f_c, fill=WHITE)
    dr.text((s(20), s(H - 18)), "the last one.", font=f_cb, fill=RED)
    dr.text((s(92), s(H - 18)), "ninety years ago today", font=f_c, fill=WHITE)

    return finalize(img, dither=False)


# ------------------------------------------------------------ 3. Penrose
def image3_penrose():
    """Penrose P3 rhombus tiling by Robinson-triangle subdivision, five-fold
    sun at the centre, no words."""
    phi = (1 + math.sqrt(5)) / 2
    tris = []
    for i in range(10):
        B = cmath.rect(1, (2 * i - 1) * math.pi / 10)
        C = cmath.rect(1, (2 * i + 1) * math.pi / 10)
        if i % 2 == 0:
            B, C = C, B
        tris.append((0, 0j, B, C))

    def subdivide(triangles):
        out = []
        for col, A, B, C in triangles:
            if col == 0:
                P = A + (B - A) / phi
                out += [(0, C, P, B), (1, P, C, A)]
            else:
                Q = B + (A - B) / phi
                R = B + (C - B) / phi
                out += [(1, R, C, A), (1, Q, R, B), (0, R, Q, A)]
        return out

    for _ in range(5):
        tris = subdivide(tris)

    scale = 300.0   # radius of the initial wheel in 1x px
    cx, cy = 200, 150

    def pt(z):
        return (s(cx + z.real * scale), s(cy + z.imag * scale))

    img = Image.new("RGB", (W * SS, H * SS), WHITE)
    dr = ImageDraw.Draw(img)
    for col, A, B, C in tris:
        cen = (A + B + C) / 3
        d = abs(cen) * scale
        if d > 330:
            continue
        if d < 40:
            fill = RED
        else:
            fill = WHITE if col == 0 else BLACK
        dr.polygon([pt(A), pt(B), pt(C)], fill=fill)
    for col, A, B, C in tris:
        cen = (A + B + C) / 3
        if abs(cen) * scale > 330:
            continue
        dr.line([pt(C), pt(A), pt(B)], fill=BLACK, width=s(1))
    return finalize(img, dither=False)


# ------------------------------------------------------------ 4. Vasarely bulge
def image4_bulge():
    """Op art: a checkerboard pushed out by a sphere, after Vasarely's Vega
    pictures.  Inside the bulge the black squares turn red.  No words."""
    ww, hh = W * SS, H * SS
    ys, xs = np.mgrid[0:hh, 0:ww].astype(np.float64)
    xs = xs / SS + 0.5 / SS
    ys = ys / SS + 0.5 / SS
    cx, cy, R = 200.0, 150.0, 128.0
    dx, dy = xs - cx, ys - cy
    r = np.sqrt(dx * dx + dy * dy)
    inside = r < R
    rr = np.clip(r / R, 0, 1)
    scale = np.ones_like(r)
    # inverse of the bulge: flat radius = (2/pi) asin(bulge radius)  -> magnifies the centre
    flat = (2 / math.pi) * np.arcsin(rr)
    scale = np.where(inside & (r > 0), flat * R / np.maximum(r, 1e-9), 1.0)
    ux = cx + dx * scale
    uy = cy + dy * scale
    cell = 25.0
    ci = np.floor(ux / cell).astype(np.int64)
    cj = np.floor(uy / cell).astype(np.int64)
    dark = ((ci + cj) % 2) == 0
    rgb = np.empty((hh, ww, 3), dtype=np.uint8)
    rgb[...] = 255
    rgb[dark & ~inside] = (0, 0, 0)
    rgb[dark & inside] = (255, 0, 0)
    img = Image.fromarray(rgb, "RGB")
    return finalize(img, dither=False)


# ------------------------------------------------------------ 5. Weave
def image5_weave():
    """A weaver's drawdown: four shafts, point threading, 2/2 twill tie-up,
    point treadling — the goose-eye diamond.  Warp white, weft black, with a
    band of red weft.  The draft notation sits in the corner as weavers write it."""
    threading_unit = [0, 1, 2, 3, 2, 1]          # shaft per warp end (point draft)
    treadling_unit = [0, 1, 2, 3, 2, 1]          # treadle per pick
    tieup = [{0, 1}, {1, 2}, {2, 3}, {3, 0}]     # shafts lifted by each treadle (2/2 twill)

    pitch = 6          # px per thread at 1x
    thick = 5
    n_warp = 44        # threads across the cloth area
    n_weft = 40
    ox, oy = 12, 12    # cloth origin (1x)

    img = Image.new("RGB", (W * SS, H * SS), WHITE)
    dr = ImageDraw.Draw(img)

    shaft_of = [threading_unit[j % len(threading_unit)] for j in range(n_warp)]
    treadle_of = [treadling_unit[i % len(treadling_unit)] for i in range(n_weft)]

    def warp_col(j):
        return WHITE
    def weft_col(i):
        return RED if 14 <= i < 22 else BLACK

    # cloth background: dark gaps between threads
    dr.rectangle([s(ox - 2), s(oy - 2), s(ox + n_warp * pitch + 1), s(oy + n_weft * pitch + 1)], fill=BLACK)
    # draw weft threads (horizontal) first
    for i in range(n_weft):
        y = oy + i * pitch
        dr.rectangle([s(ox), s(y), s(ox + n_warp * pitch - 1), s(y + thick) - 1], fill=weft_col(i))
    # then warp threads where they float over the weft
    for j in range(n_warp):
        x = ox + j * pitch
        for i in range(n_weft):
            y = oy + i * pitch
            lifted = shaft_of[j] in tieup[treadle_of[i]]
            if lifted:
                dr.rectangle([s(x), s(y - 1), s(x + thick) - 1, s(y + thick)], fill=warp_col(j))
                # tiny shadow at the end of each float for relief
                dr.line([s(x), s(y + thick), s(x + thick) - 1, s(y + thick)], fill=BLACK, width=s(1))
    # warp outline so white threads read against white gaps at the edge
    dr.rectangle([s(ox - 2), s(oy - 2), s(ox + n_warp * pitch + 1), s(oy + n_weft * pitch + 1)], outline=BLACK, width=s(2))

    # --- the draft, right-hand side
    cellp = 6
    # threading (top-right): 12 ends x 4 shafts
    tx, ty = 288, oy
    gx = tx + 100
    for j in range(12):
        for k in range(4):
            x = tx + j * cellp
            y = ty + (3 - k) * cellp
            dr.rectangle([s(x), s(y), s(x + cellp), s(y + cellp)], outline=BLACK, width=1)
            if shaft_of[j] == k:
                dr.rectangle([s(x + 1), s(y + 1), s(x + cellp - 1), s(y + cellp - 1)], fill=BLACK)
    # tie-up (top-right corner): 4 treadles x 4 shafts
    ux_, uy_ = tx + 12 * cellp + 4, ty
    for t in range(4):
        for k in range(4):
            x = ux_ + t * cellp
            y = uy_ + (3 - k) * cellp
            dr.rectangle([s(x), s(y), s(x + cellp), s(y + cellp)], outline=BLACK, width=1)
            if k in tieup[t]:
                dr.rectangle([s(x + 1), s(y + 1), s(x + cellp - 1), s(y + cellp - 1)], fill=RED)
    # treadling (below tie-up): 12 picks x 4 treadles
    vx, vy = ux_, uy_ + 4 * cellp + 4
    for i in range(12):
        for t in range(4):
            x = vx + t * cellp
            y = vy + i * cellp
            dr.rectangle([s(x), s(y), s(x + cellp), s(y + cellp)], outline=BLACK, width=1)
            if treadle_of[i] == t:
                dr.rectangle([s(x + 1), s(y + 1), s(x + cellp - 1), s(y + cellp - 1)], fill=BLACK)

    # labels
    f_h = font(F_SERIF_B, s(15))
    f_c = font(F_SERIF_I, s(9))
    f_m = font(F_MONO, s(9))
    ly = vy + 12 * cellp + 10
    dr.text((s(tx), s(ly)), "GOOSE-EYE", font=f_h, fill=BLACK)
    dr.text((s(tx), s(ly + 22)), "four shafts", font=f_c, fill=BLACK)
    dr.text((s(tx), s(ly + 34)), "2/2 twill tie-up", font=f_c, fill=BLACK)
    dr.text((s(tx), s(ly + 46)), "point draft, both ways", font=f_c, fill=BLACK)
    dr.text((s(tx), s(ly + 62)), "warp: white", font=f_m, fill=BLACK)
    dr.text((s(tx), s(ly + 73)), "weft: black + red", font=f_m, fill=BLACK)
    dr.text((s(tx), s(ly + 90)), "the draft is read", font=f_c, fill=BLACK)
    dr.text((s(tx), s(ly + 102)), "from the corner out", font=f_c, fill=BLACK)

    # caption under the cloth
    f_m9 = font(F_MONO, s(9))
    dr.text((s(ox), s(oy + n_weft * pitch + 8)), "drawdown: a warp end shows where its shaft is lifted for that pick",
            font=f_m9, fill=BLACK)
    dr.text((s(ox), s(oy + n_weft * pitch + 21)), "threading × tie-up × treadling  →  the cloth", font=f_m9, fill=RED)

    return finalize(img, dither=False)


if __name__ == "__main__":
    save(image1_test_card(), 1)
    save(image2_thylacine(), 2)
    save(image3_penrose(), 3)
    save(image4_bulge(), 4)
    save(image5_weave(), 5)
    print("done")
