#!/usr/bin/env python3
"""
2026-08-23 — five pictures for a 400x300 black/white/red e-ink screen.

Today, August 23rd:
  * 60 years exactly since Lunar Orbiter 1 took the first photograph of
    Earth from the Moon (23 Aug 1966).
  * 170 years exactly since Eunice Foote's paper — the first to say CO2
    warms the Earth — was read to the AAAS (23 Aug 1856).
  * Chandrayaan-3 landed at the lunar south pole on this day in 2023.
  * Tonight the waxing gibbous Moon sails over the Teapot of Sagittarius;
    a deep partial lunar eclipse follows on the night of Aug 27-28.

1.png  The First Look Back      — Lunar Orbiter 1 earthrise, framelet strips
2.png  Foote, 1856              — two jars, two thermometers, one sentence
3.png  Moon over the Teapot     — tonight's sky + Thursday's eclipse
4.png  Kamon                    — generated Japanese crest (backlog item)
5.png  Sandpile                 — abelian sandpile fractal, 60,000 grains
"""

import math, random, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3                      # supersample factor for soft/dithered art
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
OUT = os.path.dirname(os.path.abspath(__file__))

F = "/usr/share/fonts/truetype/dejavu/"
FONT_SANS   = F + "DejaVuSans.ttf"
FONT_BOLD   = F + "DejaVuSans-Bold.ttf"
FONT_SERIF  = F + "DejaVuSerif.ttf"
FONT_SERIF_I= "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FONT_MONO   = F + "DejaVuSansMono.ttf"
FONT_JP     = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"

def font(path, size): return ImageFont.truetype(path, size)

def palette_image():
    p = Image.new("P", (1, 1))
    p.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)
    return p

PAL = palette_image()

def quantize(img, dither=True):
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)

def downscale(img):
    return img.resize((W, H), Image.LANCZOS)

def save(img, n):
    img.save(os.path.join(OUT, f"{n}.png"), optimize=True)

# ----------------------------------------------------------------------
# 1. THE FIRST LOOK BACK — Lunar Orbiter 1, 23 August 1966
#    The famous first photo of Earth from the Moon was assembled from
#    vertical "framelet" strips; the strip seams are part of its beauty.
# ----------------------------------------------------------------------
def img1():
    rng = random.Random(19660823)
    w, h = W * SS, H * SS
    im = Image.new("L", (w, h), 8)          # near-black space
    dr = ImageDraw.Draw(im)

    # --- lunar surface: a rugged limb filling the lower-right, seen
    #     obliquely from orbit (as in the original photograph).
    horizon = []
    for x in range(-20, w + 21, 12):
        t = max(0.0, x / w)
        base = h * 0.86 - (h * 0.34) * (t ** 1.4) # limb climbs toward the right edge
        jitter = rng.uniform(-14, 14)
        horizon.append((x, base + jitter))
    poly = horizon + [(w + 20, h + 20), (-20, h + 20)]
    dr.polygon(poly, fill=178)

    # shade the surface darker near the limb edge for depth
    for i in range(6):
        off = 26 + i * 34
        pts = [(x, y + off) for (x, y) in horizon]
        dr.line(pts, fill=178 - i * 9, width=30)

    # craters: ellipses (foreshortened), bright rim on top, dark floor
    def crater(cx, cy, r):
        squash = 0.42
        ry = r * squash
        dr.ellipse([cx - r, cy - ry, cx + r, cy + ry], fill=120)
        dr.arc([cx - r, cy - ry, cx + r, cy + ry], 160, 380, fill=230, width=max(2, int(r // 9)))
        dr.arc([cx - r * 0.92, cy - ry * 0.92, cx + r * 0.92, cy + ry * 0.92],
               20, 160, fill=70, width=max(2, int(r // 7)))
    def horizon_y(px):
        t = max(0.0, min(1.0, px / w))
        return h * 0.86 - (h * 0.34) * (t ** 1.4)
    placed = 0
    while placed < 46:
        cx = rng.uniform(0, w)
        cy = rng.uniform(horizon_y(cx) + 30, h + 60)
        if cy > h + 40:
            continue
        r = rng.uniform(9, 70) * SS / 3
        # deeper craters lower down (closer to camera)
        r *= 0.6 + 0.8 * (cy / h)
        if cy - r * 0.42 < horizon_y(cx) + 6:      # keep whole bowl below the limb
            continue
        crater(cx, cy, r)
        placed += 1

    # --- Earth: half-lit disc hanging in the black, upper left
    ex, ey, er = w * 0.30, h * 0.30, w * 0.105
    earth = Image.new("L", (int(er * 2.4), int(er * 2.4)), 0)
    ed = ImageDraw.Draw(earth)
    ec = er * 1.2
    ed.ellipse([ec - er, ec - er, ec + er, ec + er], fill=150)
    # cloud swirls: bright arcs and blobs
    erng = random.Random(2026)
    for _ in range(90):
        a = erng.uniform(0, 2 * math.pi)
        d = erng.uniform(0, er * 0.95)
        bx, by = ec + d * math.cos(a), ec + d * math.sin(a)
        br = erng.uniform(er * 0.05, er * 0.22)
        shade = erng.choice([215, 235, 245, 110, 90])
        ed.ellipse([bx - br, by - br * 0.45, bx + br, by + br * 0.45], fill=shade)
    # clip to disc
    mask = Image.new("L", earth.size, 0)
    ImageDraw.Draw(mask).ellipse([ec - er, ec - er, ec + er, ec + er], fill=255)
    # terminator: keep the right ~55% lit, fade the left into night
    term = Image.new("L", earth.size, 255)
    td = ImageDraw.Draw(term)
    for x in range(earth.size[0]):
        t = (x - (ec - er * 0.25)) / (er * 0.5)
        v = int(max(0, min(1, t)) * 255)
        td.line([(x, 0), (x, earth.size[1])], fill=v)
    dark = Image.new("L", earth.size, 12)
    earth = Image.composite(earth, dark, term)
    im.paste(earth, (int(ex - ec), int(ey - ec)), mask)

    # --- framelet strips: vertical seams + per-strip exposure wobble
    arr = np.asarray(im).astype(np.int16)
    strip_w = 38 * SS // 3 * 3  # ~38 px at 3x
    srng = random.Random(66)
    x = 0
    while x < w:
        sw = strip_w + srng.randint(-6, 6)
        arr[:, x:x + sw] += srng.randint(-10, 10)
        if x > 0:
            arr[:, x:x + 2] = np.maximum(arr[:, x:x + 2] - 70, 0)   # dark seam
            arr[:, x + 2:x + 3] += 30                               # bright edge
        x += sw
    # mild film grain
    g = np.random.default_rng(1966).normal(0, 7, arr.shape)
    arr = np.clip(arr + g, 0, 255).astype(np.uint8)
    im = Image.fromarray(arr, "L")

    out = downscale(im.convert("RGB"))

    # --- caption drawn at 1x so it stays crisp
    dr = ImageDraw.Draw(out)
    dr.rectangle([0, H - 34, W, H], fill=BLACK)
    dr.line([0, H - 34, W, H - 34], fill=WHITE)
    f1 = font(FONT_BOLD, 13)
    f2 = font(FONT_SANS, 10)
    dr.text((8, H - 30), "THE FIRST LOOK BACK", font=f1, fill=WHITE)
    dr.text((8, H - 14), "Lunar Orbiter 1 photographs Earth from the Moon", font=f2, fill=WHITE)
    f3 = font(FONT_BOLD, 15)
    t = "23 VIII 1966"
    tw = dr.textlength(t, font=f3)
    dr.text((W - tw - 8, H - 29), t, font=f3, fill=RED)
    f4 = font(FONT_SANS, 9)
    t2 = "sixty years ago today"
    tw2 = dr.textlength(t2, font=f4)
    dr.text((W - tw2 - 8, H - 12), t2, font=f4, fill=WHITE)

    save(quantize(out, dither=True), 1)

# ----------------------------------------------------------------------
# 2. FOOTE, 1856 — the first person to write down that carbon dioxide
#    warms the Earth. Her paper was read to the AAAS 170 years ago today.
# ----------------------------------------------------------------------
def img2():
    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)

    # header
    dr.rectangle([0, 0, W, 40], fill=BLACK)
    fh = font(FONT_BOLD, 17)
    dr.text((10, 6), "AN ATMOSPHERE OF THAT GAS", font=fh, fill=WHITE)
    fh2 = font(FONT_BOLD, 10)
    dr.text((10, 26), "Eunice Newton Foote reads her experiment to science", font=fh2, fill=WHITE)

    # the sun, top right, rays slanting down onto both jars
    sx, sy, sr = W - 48, 72, 24
    dr.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=RED)
    for jar_x in (95, 210):
        for off in (-26, 0, 26):
            x0, y0 = sx - 12, sy + 8
            x1, y1 = jar_x + off * 0.55, 126
            dr.line([x0, y0, x1, y1], fill=RED, width=2)

    # two glass cylinders
    def jar(cx, label, mercury_h, temp):
        jw, jtop, jbot = 46, 118, 262
        dr.rectangle([cx - jw, jtop, cx + jw, jbot], outline=BLACK, width=3)
        dr.line([cx - jw + 8, jtop + 8, cx - jw + 8, jbot - 8], fill=BLACK, width=1)
        # thermometer
        tx = cx
        bulb_y = jbot - 22
        dr.line([tx, jtop + 26, tx, bulb_y], fill=BLACK, width=7)
        dr.line([tx, jtop + 27, tx, bulb_y], fill=WHITE, width=3)
        dr.ellipse([tx - 8, bulb_y - 8, tx + 8, bulb_y + 8], fill=RED, outline=BLACK, width=2)
        dr.line([tx, bulb_y, tx, bulb_y - mercury_h], fill=RED, width=3)
        for i, ty in enumerate(range(jtop + 30, bulb_y - 6, 12)):
            dr.line([tx + 5, ty, tx + (11 if i % 2 == 0 else 8), ty], fill=BLACK, width=1)
        # labels
        fl = font(FONT_BOLD, 12)
        tw = dr.textlength(label, font=fl)
        dr.text((cx - tw / 2, jbot + 4), label, font=fl, fill=BLACK)
        ft = font(FONT_MONO, 11)
        tw = dr.textlength(temp, font=ft)
        dr.text((cx - tw / 2, jtop - 16), temp, font=ft, fill=BLACK)

    jar(95, "COMMON AIR", 52, "100 °F")
    jar(210, "CARBONIC ACID", 108, "120 °F")

    # her sentence, right column
    fq = font(FONT_SERIF_I, 12)
    quote = ["“An atmosphere of", "that gas would give", "to our earth a", "high temperature.”"]
    qy = 152
    for line in quote:
        dr.text((330, qy), line, font=fq, fill=BLACK, anchor="ma")
        qy += 17
    fq2 = font(FONT_SANS, 9)
    dr.text((330, qy + 6), "— Eunice Foote, 1856", font=fq2, fill=BLACK, anchor="ma")

    # footer
    dr.rectangle([0, H - 20, W, H], fill=RED)
    ff = font(FONT_BOLD, 11)
    t = "23 AUGUST 1856 · 170 YEARS SINCE WE KNEW"
    while dr.textlength(t, font=ff) > W - 12 and ff.size > 8:
        ff = font(FONT_BOLD, ff.size - 1)
    tw = dr.textlength(t, font=ff)
    dr.text(((W - tw) / 2, H - 17), t, font=ff, fill=WHITE)

    save(quantize(im, dither=False), 2)

# ----------------------------------------------------------------------
# 3. MOON OVER THE TEAPOT — tonight's sky, and Thursday's eclipse.
#    The waxing gibbous Moon crosses the Teapot of Sagittarius tonight;
#    the Milky Way rises from the spout like steam.
# ----------------------------------------------------------------------
TEAPOT = {  # star: (RA deg, Dec deg, mag)
    "Alnasl":         (271.45, -30.42, 3.0),   # gamma - spout tip
    "Kaus Media":     (275.25, -29.83, 2.7),   # delta
    "Kaus Australis": (276.04, -34.38, 1.8),   # epsilon
    "Kaus Borealis":  (276.99, -25.42, 2.8),   # lambda - lid
    "Phi Sgr":        (281.41, -26.99, 3.2),
    "Nunki":          (283.82, -26.30, 2.0),   # sigma
    "Ascella":        (285.65, -29.88, 2.6),   # zeta
    "Tau Sgr":        (286.73, -27.67, 3.3),
}
TEAPOT_LINES = [
    ("Alnasl", "Kaus Media"), ("Kaus Media", "Kaus Borealis"),
    ("Kaus Borealis", "Phi Sgr"), ("Phi Sgr", "Kaus Media"),
    ("Kaus Media", "Kaus Australis"), ("Kaus Australis", "Ascella"),
    ("Ascella", "Phi Sgr"), ("Phi Sgr", "Nunki"),
    ("Nunki", "Tau Sgr"), ("Tau Sgr", "Ascella"),
]

def img3():
    w, h = W * SS, H * SS
    im = Image.new("RGB", (w, h), BLACK)
    dr = ImageDraw.Draw(im)
    rng = random.Random(20260823)

    # sky projection: RA grows to the left (east up in the sky's mirror)
    ras = [v[0] for v in TEAPOT.values()]
    decs = [v[1] for v in TEAPOT.values()]
    ra0, ra1 = min(ras), max(ras)
    de0, de1 = min(decs), max(decs)
    pad = 0.14
    def project(ra, dec):
        tx = (ra1 - ra) / (ra1 - ra0)         # flip: east on the left
        ty = (de1 - dec) / (de1 - de0)
        x = w * (0.16 + 0.58 * tx)
        y = h * (0.34 + 0.50 * ty)
        return x, y

    # faint background stars
    for _ in range(220):
        x, y = rng.uniform(0, w), rng.uniform(0, h * 0.93)
        r = rng.choice([1, 1, 1, 2, 2, 3])
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(90, 90, 90))

    # Milky Way steam rising from the spout (left, toward upper-left)
    spout = project(*TEAPOT["Alnasl"][:2])
    for _ in range(2600):
        t = rng.random() ** 1.5
        # a plume curving up-left from the spout
        px = spout[0] - t * w * 0.30 + rng.gauss(0, w * (0.02 + 0.11 * t))
        py = spout[1] - t * h * 0.66 + rng.gauss(0, h * (0.015 + 0.08 * t))
        r = rng.choice([1, 1, 2, 2, 3])
        c = rng.choice([(255, 255, 255)] * 3 + [(160, 160, 160)])
        if 0 < px < w and 0 < py < h * 0.93:
            dr.ellipse([px - r, py - r, px + r, py + r], fill=c)

    # constellation lines
    for a, b in TEAPOT_LINES:
        xa, ya = project(*TEAPOT[a][:2])
        xb, yb = project(*TEAPOT[b][:2])
        dr.line([xa, ya, xb, yb], fill=(255, 255, 255), width=6)

    # stars of the Teapot
    for name, (ra, dec, mag) in TEAPOT.items():
        x, y = project(ra, dec)
        r = (4.6 - mag) * 4.2
        dr.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
        for ang in (0, 90, 180, 270):
            dr.line([x + (r + 8) * math.cos(math.radians(ang)), y + (r + 8) * math.sin(math.radians(ang)),
                     x + (r + 15) * math.cos(math.radians(ang)), y + (r + 15) * math.sin(math.radians(ang))],
                    fill=WHITE, width=2)

    # the waxing gibbous Moon (~73% lit), riding above the lid
    lid = project(*TEAPOT["Kaus Borealis"][:2])
    mx, my, mr = lid[0] + w * 0.07, lid[1] - h * 0.22, w * 0.060
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(235, 235, 235))
    # maria blotches
    for _ in range(26):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0, mr * 0.82)
        bx, by = mx + d * math.cos(a), my + d * math.sin(a)
        br = rng.uniform(mr * 0.08, mr * 0.3)
        dr.ellipse([bx - br, by - br, bx + br, by + br], fill=(150, 150, 150))
    # waxing gibbous: a thin shadow crescent bites the eastern (left) limb.
    # shadow = disc minus a big ellipse shifted right; only a left sliver stays.
    lit = Image.new("L", im.size, 0)
    ld = ImageDraw.Draw(lit)
    ld.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=255)          # disc
    ld.ellipse([mx + mr * 0.75 - mr * 1.25, my - mr * 1.30,
                mx + mr * 0.75 + mr * 1.25, my + mr * 1.30], fill=0)    # carve lit zone
    shadow = Image.new("RGB", im.size, (20, 20, 20))
    im.paste(shadow, (0, 0), lit)   # lit mask now holds only the left sliver

    out = downscale(im)
    dr = ImageDraw.Draw(out)

    # labels at 1x
    fl = font(FONT_SANS, 9)
    for name in ("Nunki", "Kaus Australis", "Alnasl"):
        x, y = project(*TEAPOT[name][:2])
        dr.text((x / SS + 6, y / SS + 5), name, font=fl, fill=WHITE)
    ft = font(FONT_BOLD, 13)
    dr.text((10, 8), "TONIGHT", font=ft, fill=RED)
    dr.text((10, 24), "the Moon sails over the Teapot", font=font(FONT_SANS, 11), fill=WHITE)
    dr.text((10, 38), "of Sagittarius · look south, 10 pm", font=font(FONT_SANS, 11), fill=WHITE)

    # footer: the coming eclipse
    dr.rectangle([0, H - 22, W, H], fill=RED)
    fe = font(FONT_BOLD, 10)
    t = "THU 27–28: DEEP PARTIAL ECLIPSE — FULL MOON TURNS RED"
    while dr.textlength(t, font=fe) > W - 10 and fe.size > 7:
        fe = font(FONT_BOLD, fe.size - 1)
    tw = dr.textlength(t, font=fe)
    dr.text(((W - tw) / 2, H - 22 + (22 - fe.size) / 2 - 2), t, font=fe, fill=WHITE)

    save(quantize(out, dither=True), 3)

# ----------------------------------------------------------------------
# 4. KAMON — a generated Japanese family crest, seeded by today's date.
#    Bold n-fold rotational symmetry inside a ring; one red heart.
# ----------------------------------------------------------------------
def img4():
    rng = random.Random("kamon-2026-08-23")
    w, h = W * SS, H * SS
    im = Image.new("RGB", (w, h), WHITE)

    def draw_kamon(center, R, rng, red_center=False):
        cx, cy = center
        layer = Image.new("L", (w, h), 0)   # ink mask
        ld = ImageDraw.Draw(layer)
        n = rng.choice([5, 6, 8])
        # enclosing ring (maru)
        ld.ellipse([cx - R, cy - R, cx + R, cy + R], outline=255, width=int(R * 0.075))
        inner = R * 0.82
        # petals: ellipse petals rotated n-fold
        petal_len = inner * rng.uniform(0.52, 0.72)
        petal_wid = petal_len * rng.uniform(0.34, 0.55)
        petal_r0 = inner * rng.uniform(0.28, 0.42)
        petal = Image.new("L", (int(petal_len * 2), int(petal_wid * 2)), 0)
        pd = ImageDraw.Draw(petal)
        pd.ellipse([0, 0, petal_len * 2 - 1, petal_wid * 2 - 1], fill=255)
        # cut a white vein in the petal
        if rng.random() < 0.7:
            pd.ellipse([petal_len * 0.45, petal_wid * 0.55,
                        petal_len * 1.55, petal_wid * 1.45], fill=0)
        for k in range(n):
            ang = 360 / n * k + rng.uniform(0, 360 / n) * 0
            rot = petal.rotate(ang, expand=True, resample=Image.BICUBIC)
            a = math.radians(-ang)
            px = cx + (petal_r0 + petal_len * 0.5) * math.cos(a)
            py = cy + (petal_r0 + petal_len * 0.5) * math.sin(a)
            layer.paste(rot, (int(px - rot.width / 2), int(py - rot.height / 2)), rot)
        # small circles between petals
        if rng.random() < 0.8:
            dot_r = inner * rng.uniform(0.05, 0.09)
            dot_d = inner * rng.uniform(0.72, 0.88)
            for k in range(n):
                a = math.radians(360 / n * (k + 0.5))
                px, py = cx + dot_d * math.cos(a), cy + dot_d * math.sin(a)
                ld.ellipse([px - dot_r, py - dot_r, px + dot_r, py + dot_r], fill=255)
        ink = Image.new("RGB", (w, h), BLACK)
        im.paste(ink, (0, 0), layer)
        # center disc
        cr = inner * rng.uniform(0.14, 0.2)
        cd = ImageDraw.Draw(im)
        col = RED if red_center else BLACK
        cd.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=col,
                   outline=WHITE, width=int(R * 0.02) + 2)

    # one large crest, off-centre; two small companions
    draw_kamon((w * 0.38, h * 0.5), h * 0.40, random.Random(823), red_center=True)
    draw_kamon((w * 0.83, h * 0.28), h * 0.135, random.Random(824))
    draw_kamon((w * 0.83, h * 0.72), h * 0.135, random.Random(825))

    out = downscale(im)
    dr = ImageDraw.Draw(out)
    # vertical caption, right edge: 家紋 (kamon)
    fj = font(FONT_JP, 22)
    dr.text((W - 30, H - 66), "家", font=fj, fill=BLACK)
    dr.text((W - 30, H - 40), "紋", font=fj, fill=BLACK)
    fs = font(FONT_SANS, 8)
    dr.text((8, H - 14), "three crests grown from today's date · 2026-08-23", font=fs, fill=BLACK)

    save(quantize(out, dither=False), 4)

# ----------------------------------------------------------------------
# 5. SANDPILE — 60,000 grains dropped on one cell, toppled until calm.
#    (60,000 for sixty years since the first look back.)
# ----------------------------------------------------------------------
def img5():
    N = 30000
    cells_w, cells_h = 200, 150        # 2px cells -> 400x300
    grid = np.zeros((cells_h, cells_w), dtype=np.int64)
    grid[cells_h // 2, cells_w // 2] = N
    while True:
        over = grid >= 4
        if not over.any():
            break
        spill = grid // 4 * over
        grid = grid - spill * 4
        grid[1:, :]  += spill[:-1, :]
        grid[:-1, :] += spill[1:, :]
        grid[:, 1:]  += spill[:, :-1]
        grid[:, :-1] += spill[:, 1:]

    # heights 0..3 -> colors (0 also covers the untouched background)
    colmap = {0: WHITE, 1: RED, 2: WHITE, 3: BLACK}
    rgb = np.zeros((cells_h, cells_w, 3), dtype=np.uint8)
    for v, c in colmap.items():
        rgb[grid == v] = c
    im = Image.fromarray(rgb, "RGB").resize((W, H), Image.NEAREST)

    dr = ImageDraw.Draw(im)
    fs = font(FONT_MONO, 9)
    dr.rectangle([0, H - 16, W, H], fill=WHITE)
    dr.line([0, H - 16, W, H - 16], fill=BLACK)
    t = "abelian sandpile · 30 000 grains on one cell, toppled until still"
    tw = dr.textlength(t, font=fs)
    dr.text(((W - tw) / 2, H - 13), t, font=fs, fill=BLACK)
    save(quantize(im, dither=False), 5)

if __name__ == "__main__":
    img1(); print("1 ok")
    img2(); print("2 ok")
    img3(); print("3 ok")
    img4(); print("4 ok")
    img5(); print("5 ok")
