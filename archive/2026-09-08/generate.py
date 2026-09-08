#!/usr/bin/env python3
"""
2026-09-08 — five pictures for a 400x300 black/white/red e-ink screen.

  1. Kusa no tsuyu shiroshi — the 43rd microseason: white dew on grass, a red dragonfly
  2. Petri — Gray-Scott reaction-diffusion grown in a dish, specimen-plate style
  3. Sixty — a constructivist poster for the 60th anniversary of Star Trek's first broadcast
  4. The Block — David's marble, 5.17 m, against a 1.75 m person, unveiled 8 Sep 1504
  5. Earthshine — the 8% waning crescent beside Jupiter an hour before sunrise

Pipeline: organic pieces are drawn at 3x (1200x900), LANCZOS-downscaled and
Floyd-Steinberg dithered into the exact 3-colour palette; crisp text and hard
geometry are drawn at 1x afterwards and snapped to the nearest palette colour.
Every image carries a small red day-of-year stamp in the bottom-right corner.
"""
import math
import random
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3                       # supersample factor
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
DATE = "2026-09-08"
DOY = 251                   # day of the year
OUT = os.path.dirname(os.path.abspath(__file__))

FONT_DIR = "/usr/share/fonts/truetype"
def font(name, size):
    paths = {
        "sans": f"{FONT_DIR}/dejavu/DejaVuSans.ttf",
        "sansb": f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf",
        "mono": f"{FONT_DIR}/dejavu/DejaVuSansMono.ttf",
        "monob": f"{FONT_DIR}/dejavu/DejaVuSansMono-Bold.ttf",
        "serif": f"{FONT_DIR}/dejavu/DejaVuSerif.ttf",
        "serifb": f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf",
        "lserif": f"{FONT_DIR}/liberation/LiberationSerif-Regular.ttf",
        "lserifi": f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf",
        "lserifb": f"{FONT_DIR}/liberation/LiberationSerif-Bold.ttf",
        "freesansb": f"{FONT_DIR}/freefont/FreeSansBold.ttf",
        "jp": f"{FONT_DIR}/fonts-japanese-gothic.ttf",
    }
    return ImageFont.truetype(paths[name], size)


# ----------------------------------------------------------------- palette helpers
def _pal_image():
    p = Image.new("P", (1, 1))
    p.putpalette(list(BLACK) + list(WHITE) + list(RED) + [0, 0, 0] * 253)
    return p

PAL = _pal_image()

def dither(img_rgb):
    """Floyd-Steinberg into the 3-colour palette; returns RGB."""
    return img_rgb.quantize(palette=PAL, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")

def snap(img_rgb):
    """Nearest palette colour, no dithering; returns mode-P image ready to save."""
    a = np.asarray(img_rgb.convert("RGB")).astype(np.int32)
    pal = np.array([BLACK, WHITE, RED], dtype=np.int32)
    d = ((a[:, :, None, :] - pal[None, None, :, :]) ** 2).sum(-1)
    idx = d.argmin(-1).astype(np.uint8)
    out = Image.fromarray(idx, mode="P")
    out.putpalette(PAL.getpalette())
    return out

def downscale(big):
    return big.resize((W, H), Image.LANCZOS)

def stamp(draw):
    """Red day-of-year stamp, bottom right. My signature."""
    x0, y0 = W - 26, H - 26
    draw.rectangle([x0, y0, x0 + 20, y0 + 20], fill=RED)
    f = font("monob", 10)
    t = str(DOY)
    tw = draw.textlength(t, font=f)
    draw.text((x0 + 10 - tw / 2, y0 + 4), t, font=f, fill=WHITE)

def finish(img_rgb, text_fn, path):
    """Draw crisp 1x layer on top of an RGB image, snap, save."""
    d = ImageDraw.Draw(img_rgb)
    text_fn(d)
    stamp(d)
    snap(img_rgb).save(path, optimize=True)
    print("wrote", path)


# ----------------------------------------------------------------- 1. white dew
def bezier(p0, p1, p2, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts

def tapered_stroke(draw, pts, w0, w1, fill):
    """Draw a polyline whose width tapers from w0 to w1."""
    n = len(pts)
    for i in range(n - 1):
        w = w0 + (w1 - w0) * i / (n - 1)
        draw.line([pts[i], pts[i + 1]], fill=fill, width=max(1, int(w)))
        if w > 3:
            r = w / 2
            draw.ellipse([pts[i][0] - r, pts[i][1] - r, pts[i][0] + r, pts[i][1] + r], fill=fill)

def piece_white_dew():
    rng = random.Random(DATE + "dew")
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    horizon = int(H * S * 0.72)
    # ground: black, with a gently uneven edge
    ground = [(0, H * S), (0, horizon)]
    for x in range(0, W * S + 1, 12):
        y = horizon + 10 * math.sin(x / 140) + 5 * math.sin(x / 37 + 1)
        ground.append((x, y))
    ground.append((W * S, H * S))
    d.polygon(ground, fill=BLACK)

    blades = []
    for i in range(60):
        x0 = rng.uniform(-40, W * S + 40)
        h = rng.uniform(140, 420)
        lean = rng.uniform(-160, 160)
        p0 = (x0, horizon + rng.uniform(0, 60))
        # keep the upper-left clear for the title
        if x0 + lean < 250 * S:
            h = min(h, p0[1] - 165 * S)
        p2 = (x0 + lean, p0[1] - h)
        p1 = (x0 + lean * 0.25, p0[1] - h * 0.65)
        pts = bezier(p0, p1, p2, 40)
        blades.append(pts)
    # far blades thinner, near blades thicker
    blades.sort(key=lambda b: b[0][1])
    for k, pts in enumerate(blades):
        near = k / len(blades)
        tapered_stroke(d, pts, 6 + 8 * near, 1, BLACK)

    # dew drops: sit on blades, white with a black outline (so they read on white sky)
    for pts in blades:
        if rng.random() < 0.5:
            for _ in range(rng.choice([1, 1, 2])):
                t = rng.uniform(0.35, 0.95)
                i = int(t * (len(pts) - 1))
                x, y = pts[i]
                r = rng.uniform(8, 15)
                d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE, outline=BLACK, width=2)
                # tiny highlight dot (black) at the top-left for a bit of sparkle
                d.ellipse([x - r * 0.35 - 1.5, y - r * 0.35 - 1.5, x - r * 0.35 + 1.5, y - r * 0.35 + 1.5], fill=BLACK)

    # the red dragonfly (akatombo), perched on one tall blade, upper right
    perch = max(blades, key=lambda b: (b[-1][0] > W * S * 0.6) * 1000 - b[-1][1])
    tapered_stroke(d, perch, 16, 3, BLACK)     # make the perch blade read clearly
    px, py = perch[-1]
    cx, cy = px + 20, py - 14
    ang = -0.3
    def rot(x, y):
        return (cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang))
    # body
    body = [rot(-100, 0), rot(110, 0)]
    d.line(body, fill=RED, width=10)
    d.line([rot(60, 0), rot(110, 0)], fill=RED, width=6)   # tail thins
    d.ellipse([*map(lambda v: v - 13, rot(-104, 0)), *map(lambda v: v + 13, rot(-104, 0))], fill=RED)  # head
    # wings: two pairs, long ellipses, white with a red outline
    for sign in (-1, 1):
        for (ox, L, wdt, tilt) in ((-40, 140, 30, 0.55), (0, 150, 32, 0.35)):
            wing = []
            for j in range(41):
                a = 2 * math.pi * j / 40
                wx = ox + L / 2 * math.cos(a)
                wy = sign * (wdt / 2 * math.sin(a))
                # rotate wing about its root to sweep it back
                t = sign * tilt
                rx = ox + (wx - ox) * math.cos(t) - wy * math.sin(t)
                ry = (wx - ox) * math.sin(t) + wy * math.cos(t)
                wing.append(rot(rx, ry - sign * 8))
            d.polygon(wing, fill=WHITE)
            d.line(wing + [wing[0]], fill=RED, width=4)
            # a vein down the middle of each wing
            d.line([wing[0], wing[20]], fill=RED, width=2)
    small = downscale(big)
    img = dither(small)

    def text(dr):
        dr.text((18, 14), "白露", font=font("jp", 44), fill=BLACK)
        dr.text((18, 66), "草露白", font=font("jp", 22), fill=RED)
        dr.text((18, 94), "kusa no tsuyu shiroshi", font=font("lserifi", 15), fill=BLACK)
        dr.text((18, 112), "dew glistens white on grass", font=font("lserifi", 15), fill=BLACK)
        dr.text((18, 134), "43rd of the 72 seasons · 8–12 Sep", font=font("mono", 9), fill=BLACK)
        dr.text((12, H - 22), "a red dragonfly means the summer is over", font=font("mono", 9), fill=WHITE)
    finish(img, text, f"{OUT}/1.png")


# ----------------------------------------------------------------- 2. gray-scott petri
def gray_scott(n, m, F, k, steps, seed, mask):
    rng = np.random.default_rng(seed)
    Du, Dv = 0.64, 0.32      # 4x the classic 0.16/0.08 because the 9-point stencil is normalised
    U = np.ones((n, m), dtype=np.float32)
    V = np.zeros((n, m), dtype=np.float32)
    # seed: a ring of small patches + centre
    cy, cx = n // 2, m // 2
    for a in np.linspace(0, 2 * np.pi, 7, endpoint=False):
        y = int(cy + 22 * np.sin(a)); x = int(cx + 22 * np.cos(a))
        V[y - 3:y + 3, x - 3:x + 3] = 1.0
    V[cy - 4:cy + 4, cx - 4:cx + 4] = 1.0
    U -= V
    U += rng.uniform(-0.02, 0.02, U.shape).astype(np.float32)
    def lap(A):
        # 9-point Laplacian: less square-grid bias than the 5-point one
        return (0.2 * (np.roll(A, 1, 0) + np.roll(A, -1, 0) + np.roll(A, 1, 1) + np.roll(A, -1, 1))
                + 0.05 * (np.roll(np.roll(A, 1, 0), 1, 1) + np.roll(np.roll(A, 1, 0), -1, 1)
                          + np.roll(np.roll(A, -1, 0), 1, 1) + np.roll(np.roll(A, -1, 0), -1, 1))
                - A)
    for _ in range(steps):
        Lu = lap(U)
        Lv = lap(V)
        uvv = U * V * V
        U += Du * Lu - uvv + F * (1 - U)
        V += Dv * Lv + uvv - (F + k) * V
        # the dish wall: nothing lives outside the mask
        V[~mask] = 0.0
        U[~mask] = 1.0
    return U, V

def piece_petri():
    n, m = 280, 280          # simulation grid (1 cell = 1 pixel on the dish)
    yy, xx = np.mgrid[0:n, 0:m]
    R = 130
    mask = (yy - n / 2) ** 2 + (xx - m / 2) ** 2 <= R ** 2
    F, k, steps = 0.0545, 0.0620, 9000
    U, V = gray_scott(n, m, F, k, steps, seed=DOY * 2026, mask=mask)
    img = Image.new("RGB", (W, H), WHITE)
    a = np.full((n, m, 3), 255, dtype=np.uint8)
    coral = (V > 0.18) & mask
    a[coral] = 0
    # a thin red rim where the pattern is actively growing (mid V)
    front = (V > 0.09) & (V <= 0.18) & mask
    a[front] = (255, 0, 0)
    dish = Image.fromarray(a, "RGB")
    ox, oy = 10, (H - n) // 2
    img.paste(dish, (ox, oy))
    d = ImageDraw.Draw(img)
    # dish rim
    d.ellipse([ox + m / 2 - R - 2, oy + n / 2 - R - 2, ox + m / 2 + R + 2, oy + n / 2 + R + 2], outline=BLACK, width=2)
    d.ellipse([ox + m / 2 - R - 7, oy + n / 2 - R - 7, ox + m / 2 + R + 7, oy + n / 2 + R + 7], outline=BLACK, width=1)

    def text(dr):
        x = 300
        dr.text((x, 22), "PETRI", font=font("sansb", 20), fill=BLACK)
        dr.line([x, 48, W - 12, 48], fill=BLACK, width=2)
        f = font("mono", 9)
        lines = [
            "Gray–Scott",
            "reaction–diffusion",
            "",
            f"F  = {F:.4f}",
            f"k  = {k:.4f}",
            "Du = 2 Dv",
            f"t  = {steps}",
            "",
            "seed: one centre",
            "  + a ring of 7",
            "",
            "black: v > 0.18",
            "red:   the front",
        ]
        y = 58
        for ln in lines:
            if ln.startswith("red"):
                dr.rectangle([x, y + 2, x + 7, y + 9], fill=RED)
                dr.text((x + 11, y), ln[5:].strip(), font=f, fill=BLACK)
            elif ln.startswith("black"):
                dr.rectangle([x, y + 2, x + 7, y + 9], fill=BLACK)
                dr.text((x + 11, y), ln[7:].strip(), font=f, fill=BLACK)
            else:
                dr.text((x, y), ln, font=f, fill=BLACK)
            y += 13
        dr.text((x, H - 40), "specimen 251", font=font("mono", 9), fill=RED)
        dr.text((x, H - 28), DATE, font=font("mono", 9), fill=BLACK)
    finish(img, text, f"{OUT}/2.png")


# ----------------------------------------------------------------- 3. sixty
def rotated_text(base, xy, txt, fnt, fill, angle_deg, anchor="ls"):
    """Draw rotated text onto base (RGB). xy = anchor point on the base."""
    bbox = fnt.getbbox(txt)
    tw, th = bbox[2] - bbox[0] + 4, bbox[3] - bbox[1] + 4
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((2 - bbox[0], 2 - bbox[1]), txt, font=fnt, fill=fill + (255,))
    rot = layer.rotate(angle_deg, expand=True, resample=Image.BICUBIC)
    # place so that the text's left-baseline lands at xy
    a = math.radians(angle_deg)
    # centre of layer relative to left-baseline corner (approx)
    cx, cy = tw / 2, th / 2
    lx, ly = 2, th - 2
    dx, dy = cx - lx, cy - ly
    rdx = dx * math.cos(a) + dy * math.sin(a)
    rdy = -dx * math.sin(a) + dy * math.cos(a)
    px = int(xy[0] + rdx - rot.width / 2)
    py = int(xy[1] + rdy - rot.height / 2)
    base.paste(rot, (px, py), rot)

def piece_sixty():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    # the planet
    cx, cy, r = 292, 108, 92
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK)
    # thin orbit ring, slightly off-centre
    d.ellipse([cx - r - 16, cy - r + 6, cx + r + 16, cy + r + 30], outline=BLACK, width=1)
    # the red wedge, from bottom-left into the planet
    tip = (cx + 6, cy - 4)
    d.polygon([(-10, 262), (30, 300), tip], fill=RED)
    # small counter-forms
    d.rectangle([14, 14, 26, 26], fill=RED)
    d.line([14, 34, 96, 34], fill=BLACK, width=2)
    d.line([14, 40, 96, 40], fill=BLACK, width=1)
    # a white "hull" line crossing the planet, constructivist axis
    d.line([cx - r - 30, cy + 46, cx + r + 20, cy - 60], fill=WHITE, width=2)
    d.line([cx - r - 30, cy + 46, cx + r + 20, cy - 60], fill=BLACK, width=1)
    # big number
    f = font("freesansb", 118)
    d.text((236, 168), "60", font=f, fill=BLACK)
    # tiny red delta near the number
    d.polygon([(226, 180), (232, 194), (220, 194)], fill=RED)
    # rotated legend along the wedge
    ang = math.degrees(math.atan2(262 - tip[1], tip[0] + 10))
    rotated_text(img, (52, 268), "1966 · SIXTY YEARS · 2026", font("monob", 12), BLACK, ang)

    def text(dr):
        dr.text((14, 48), "STAR TREK", font=font("sansb", 13), fill=BLACK)
        dr.text((14, 64), "first broadcast", font=font("mono", 9), fill=BLACK)
        dr.text((14, 76), "8 · IX · 1966", font=font("mono", 9), fill=BLACK)
        dr.text((14, 88), "the final frontier", font=font("mono", 9), fill=BLACK)
        dr.text((14, 100), "is still out there", font=font("mono", 9), fill=BLACK)
    finish(img, text, f"{OUT}/3.png")


# ----------------------------------------------------------------- 4. the block
def piece_block():
    rng = random.Random(DATE + "marble")
    big = Image.new("RGB", (W * S, H * S), BLACK)
    d = ImageDraw.Draw(big)
    # scale: 5.17 m -> 250 px
    ppm = 250 / 5.17
    base_y = 272
    bx0, bx1 = 120, 120 + int(1.9 * ppm)
    by0 = int(base_y - 5.17 * ppm)
    # marble block: mostly white, with a soft grey gradient and veins
    arr = np.zeros((H * S, W * S, 3), dtype=np.uint8)
    blk = np.zeros((H * S, W * S), dtype=bool)
    blk[by0 * S:base_y * S, bx0 * S:bx1 * S] = True
    yy, xx = np.mgrid[0:H * S, 0:W * S]
    shade = 232 - 40 * ((xx - bx0 * S) / ((bx1 - bx0) * S))   # lit from the left
    shade = np.clip(shade, 0, 255).astype(np.uint8)
    for c in range(3):
        arr[:, :, c] = np.where(blk, shade, 0)
    big = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(big)
    # veins: faint grey bezier curves within the block
    for _ in range(9):
        x0 = rng.uniform(bx0 * S, bx1 * S)
        y0 = rng.uniform(by0 * S, base_y * S)
        pts = bezier((x0, y0), (x0 + rng.uniform(-200, 200), y0 + rng.uniform(-300, 300)),
                     (x0 + rng.uniform(-150, 150), y0 + rng.uniform(200, 500)), 60)
        pts = [(min(max(x, bx0 * S + 2), bx1 * S - 2), min(max(y, by0 * S + 2), base_y * S - 2)) for x, y in pts]
        g = rng.randint(120, 175)
        d.line(pts, fill=(g, g, g), width=rng.choice([2, 3, 4]))
    # chisel marks: short black ticks along the left and right edges (rough-hewn)
    for y in range(by0 * S, base_y * S, 14):
        L = rng.randint(6, 26)
        d.line([(bx0 * S, y), (bx0 * S + L, y + rng.randint(-4, 4))], fill=BLACK, width=2)
        L = rng.randint(6, 20)
        d.line([(bx1 * S - L, y + 7), (bx1 * S, y + 7 + rng.randint(-4, 4))], fill=BLACK, width=2)
    # ground line
    d.line([(0, base_y * S + 3), (W * S, base_y * S + 3)], fill=WHITE, width=3)
    # the person, 1.75 m, in red, standing to the right of the block
    ph = 1.75 * ppm
    px = bx1 + 36
    top = base_y - ph
    hr = ph * 0.07
    d.ellipse([(px - hr) * S, top * S, (px + hr) * S, (top + 2 * hr) * S], fill=RED)
    # torso + legs as a slim silhouette
    body = [(px - ph * 0.10, top + 2.3 * hr), (px + ph * 0.10, top + 2.3 * hr),
            (px + ph * 0.085, top + ph * 0.56), (px + ph * 0.06, base_y),
            (px + ph * 0.015, base_y), (px + ph * 0.0, top + ph * 0.62),
            (px - ph * 0.015, base_y), (px - ph * 0.06, base_y),
            (px - ph * 0.085, top + ph * 0.56)]
    d.polygon([(x * S, y * S) for x, y in body], fill=RED)
    img = dither(downscale(big))

    def text(dr):
        # dimension lines
        dx = bx0 - 22
        dr.line([dx, by0, dx, base_y], fill=WHITE, width=1)
        dr.line([dx - 4, by0, dx + 4, by0], fill=WHITE, width=1)
        dr.line([dx - 4, base_y, dx + 4, base_y], fill=WHITE, width=1)
        dr.text((dx - 60, (by0 + base_y) // 2 - 6), "5.17 m", font=font("mono", 10), fill=WHITE)
        px2 = px + 20
        dr.line([px2, top, px2, base_y], fill=RED, width=1)
        dr.line([px2 - 4, top, px2 + 4, top], fill=RED, width=1)
        dr.text((px - 18, top - 16), "1.75 m", font=font("mono", 10), fill=RED)
        # title block, right side
        x = 284
        dr.text((x, 22), "DAVID", font=font("lserifb", 34), fill=WHITE)
        dr.text((x, 62), "unveiled 8 IX 1504", font=font("lserifi", 12), fill=WHITE)
        dr.text((x, 77), "Piazza della Signoria", font=font("lserifi", 12), fill=WHITE)
        f = font("mono", 9)
        lines = ["one block of Carrara", "refused twice,", "left 40 years", "in the yard;",
                 "40 men, 4 days", "to move it.", "", "522 years today"]
        y = 100
        for ln in lines:
            dr.text((x, y), ln, font=f, fill=RED if ln.startswith("522") else WHITE)
            y += 11
    finish(img, text, f"{OUT}/4.png")


# ----------------------------------------------------------------- 5. earthshine
def piece_earthshine():
    rng = random.Random(DATE + "moon")
    n, m = H * S, W * S
    yy, xx = np.mgrid[0:n, 0:m].astype(np.float32)
    # sky: black at top, a dawn glow near the horizon
    horizon = int(n * 0.86)
    glow = np.clip((yy - n * 0.50) / (horizon - n * 0.50), 0, 1) ** 2.0 * 80
    sky = glow.copy()
    # stars: a sparse sprinkle, fading into the glow
    for _ in range(140):
        sx, sy = rng.randrange(m), rng.randrange(int(horizon * 0.9))
        if rng.random() > glow[sy, sx] / 80:
            sky[sy:sy + 3, sx:sx + 3] = 255
    # the moon: a sphere lit at 8%
    cx, cy, R = 150 * S, 128 * S, 84 * S
    ux = (xx - cx) / R
    uy = (yy - cy) / R
    rr = ux ** 2 + uy ** 2
    inside = rr <= 1
    uz = np.sqrt(np.clip(1 - rr, 0, 1))
    frac = 0.08
    alpha = math.acos(2 * frac - 1)          # phase angle
    sxv, szv = -math.sin(alpha), math.cos(alpha)   # sun to the left and behind
    illum = np.clip(ux * sxv + uz * szv, 0, 1)
    lit = np.where(illum > 0.03, 255.0, 0.0)   # the sliver: solid white, hard edge
    earthshine = 26 + 12 * uz               # the dark side, faintly lit by Earth
    moon = np.maximum(lit, earthshine)
    sky = np.where(inside, moon, sky)
    arr = np.stack([sky, sky, sky], -1).astype(np.uint8)
    # ground: black with a ragged treeline
    ground = np.zeros_like(inside)
    for x in range(m):
        h = horizon + 10 * S * math.sin(x / 260) + 5 * S * math.sin(x / 71 + 2) + rng.uniform(-6, 6)
        ground[int(h):, x] = True
    arr[ground] = 0
    big = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(big)
    # a thin white horizon-ish line where the glow meets the ground
    # Jupiter: bright, with the four Galilean moons in a line
    jx, jy = 80 * S, 228 * S
    d.ellipse([jx - 8, jy - 8, jx + 8, jy + 8], fill=WHITE)
    for off in (-42, -24, 20, 36):
        d.ellipse([jx + off - 2, jy - 2 + off * 0.12, jx + off + 2, jy + 2 + off * 0.12], fill=WHITE)
    # Mars, red, up near the twins
    mx, my = 300 * S, 60 * S
    d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=RED)
    # Castor and Pollux
    for (sx_, sy_, r) in ((326 * S, 30 * S, 5), (352 * S, 48 * S, 6)):
        d.ellipse([sx_ - r, sy_ - r, sx_ + r, sy_ + r], fill=WHITE)
    img = dither(downscale(big))

    def text(dr):
        f = font("mono", 9)
        dr.text((12, 12), "EAST · one hour before sunrise", font=font("sansb", 11), fill=WHITE)
        dr.text((12, 28), "8 September", font=f, fill=WHITE)
        dr.text((cx // S + R // S + 6, cy // S + 30), "8 % lit", font=f, fill=WHITE)
        dr.text((cx // S + R // S + 6, cy // S + 42), "the rest is earthshine", font=f, fill=WHITE)
        dr.text((jx // S + 16, jy // S - 6), "Jupiter", font=f, fill=WHITE)
        dr.text((mx // S - 22, my // S + 10), "Mars", font=f, fill=RED)
        dr.text((326 - 20, 30 - 14), "Castor", font=f, fill=WHITE)
        dr.text((352 + 8, 48 - 4), "Pollux", font=f, fill=WHITE)
        dr.text((12, H - 22), "the new moon in the old moon's arms", font=font("lserifi", 12), fill=WHITE)
    finish(img, text, f"{OUT}/5.png")


if __name__ == "__main__":
    piece_white_dew()
    piece_petri()
    piece_sixty()
    piece_block()
    piece_earthshine()
