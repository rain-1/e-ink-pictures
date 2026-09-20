#!/usr/bin/env python3
"""
e-ink pictures — 2026-09-20
Five images for a 400x300 black/white/red e-ink panel.

Today: Ohigan week — the red spider lilies (higanbana) bloom for the autumn
equinox, which falls in two days (23 Sep 00:05 UTC). Magellan's five ships left
Sanlúcar de Barrameda 507 years ago today (20 Sep 1519). Tonight's Moon is a
66% waxing gibbous, just past apogee.

1. HIGANBANA   — generative red spider lilies, the equinox flower
2. KAMON       — six family crests invented by a compass-and-ruler generator
3. PORTOLAN    — a rhumb-line chart for Magellan's departure, red & black winds
4. ANALEMMA    — the Sun's figure-eight, today marked, equinox in two days
5. LONG LIFE   — Conway's Life as a long exposure: history black, survivors red
"""

import math, os, random, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "images")

FONT_DIR = "/usr/share/fonts/truetype"
F_SANS_B = f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf"
F_SANS = f"{FONT_DIR}/dejavu/DejaVuSans.ttf"
F_SERIF_B = f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = f"{FONT_DIR}/dejavu/DejaVuSerif.ttf"
F_SERIF_I = f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf"
F_MONO = f"{FONT_DIR}/dejavu/DejaVuSansMono.ttf"
F_MONO_B = f"{FONT_DIR}/dejavu/DejaVuSansMono-Bold.ttf"
F_JP = f"{FONT_DIR}/fonts-japanese-gothic.ttf"

SEED = 20260920


def font(path, size):
    return ImageFont.truetype(path, size)


def palette_img():
    p = Image.new("P", (1, 1))
    p.putpalette(list(WHITE) + list(BLACK) + list(RED) + list(BLACK) * 253)
    return p


PAL = palette_img()


def save_P(arr_idx, name):
    """arr_idx: HxW uint8 with 0=white 1=black 2=red."""
    im = Image.fromarray(arr_idx.astype(np.uint8), "P")
    im.putpalette(list(WHITE) + list(BLACK) + list(RED) + list(BLACK) * 253)
    im.save(os.path.join(OUT, name), optimize=True)
    print("saved", name)


def finish_soft(img, name):
    """Tonal pieces: LANCZOS downscale + Floyd–Steinberg into the 3 colours."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    q = img.convert("RGB").quantize(palette=PAL, dither=Image.Dither.FLOYDSTEINBERG)
    q.save(os.path.join(OUT, name), optimize=True)
    print("saved", name)


def finish_hard(img, name):
    """Hard-edged pieces: downscale, then classify each pixel explicitly so
    grey anti-aliased edges never turn into red speckle."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    a = np.asarray(img.convert("RGB")).astype(np.int32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (299 * r + 587 * g + 114 * b) // 1000
    is_red = (r > 140) & (g < 120) & (b < 120) & (r - (g + b) // 2 > 70)
    idx = np.where(is_red, 2, np.where(lum > 128, 0, 1))
    save_P(idx, name)


def rotated_text(base, xy, text, fnt, angle, fill, anchor="mm"):
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text(xy, text, font=fnt, fill=fill + (255,), anchor=anchor)
    tmp = tmp.rotate(angle, resample=Image.BICUBIC, center=xy)
    base.paste(tmp, (0, 0), tmp)


def polyline(d, pts, fill, width):
    d.line(pts, fill=fill, width=width, joint="curve")


# ----------------------------------------------------------------------------
# 1. HIGANBANA — red spider lilies
# ----------------------------------------------------------------------------
def img1():
    rng = random.Random(SEED + 1)
    w, h = W * S, H * S
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)

    def curve(p0, p1, p2, n=24):
        """quadratic bezier"""
        out = []
        for i in range(n + 1):
            t = i / n
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            out.append((x, y))
        return out

    def stroke_taper(pts, fill, w0, w1):
        n = len(pts)
        for i in range(n - 1):
            wd = max(1, int(round(w0 + (w1 - w0) * i / (n - 1))))
            d.line([pts[i], pts[i + 1]], fill=fill, width=wd)

    def floret(cx, cy, ang, scale):
        """one flower: 6 reflexed petals + 6 long stamens, facing direction ang"""
        ux, uy = math.cos(ang), math.sin(ang)
        px, py = -uy, ux  # perpendicular
        # petals
        for k in range(6):
            spread = (k - 2.5) / 2.5  # -1..1
            L = scale * rng.uniform(0.85, 1.05)
            bend = rng.uniform(0.35, 0.6) * (1 if spread >= 0 else -1)
            end = (cx + ux * L * 0.55 + px * spread * L * 0.75,
                   cy + uy * L * 0.55 + py * spread * L * 0.75)
            ctrl = (cx + ux * L * 0.9 + px * spread * L * 0.15,
                    cy + uy * L * 0.9 + py * spread * L * 0.15)
            pts = curve((cx, cy), ctrl, end)
            # wavy edge
            pts = [(x + px * math.sin(i * 0.9) * scale * 0.05, y + py * math.sin(i * 0.9) * scale * 0.05)
                   for i, (x, y) in enumerate(pts)]
            stroke_taper(pts, RED, int(scale * 0.075), 2)
        # stamens: long thin arcs curving up/out, past the petals
        for k in range(6):
            spread = (k - 2.5) / 2.5
            L = scale * rng.uniform(1.5, 1.9)
            end = (cx + ux * L * 0.9 + px * spread * L * 0.55,
                   cy + uy * L * 0.9 + py * spread * L * 0.55)
            ctrl = (cx + ux * L * 0.35 + px * spread * L * 0.05,
                    cy + uy * L * 0.35 + py * spread * L * 0.05)
            pts = curve((cx, cy), ctrl, end, 30)
            polyline(d, pts, RED, 3)
            ex, ey = pts[-1]
            d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=RED)

    def plant(bx, top_y, scale, lean):
        # stem: slightly curved black line from bottom to top_y
        p0 = (bx, h + 10)
        p2 = (bx + lean, top_y)
        p1 = (bx + lean * 0.2, (h + top_y) / 2)
        pts = curve(p0, p1, p2, 40)
        polyline(d, pts, BLACK, 7)
        # umbel: 5-7 florets around the tip
        n = rng.choice([5, 6, 7])
        base_ang = rng.uniform(0, 2 * math.pi)
        tx, ty = p2
        for k in range(n):
            a = base_ang + 2 * math.pi * k / n + rng.uniform(-0.15, 0.15)
            # pedicel
            pl = scale * 0.35
            fx, fy = tx + math.cos(a) * pl, ty + math.sin(a) * pl
            d.line([(tx, ty), (fx, fy)], fill=BLACK, width=4)
            floret(fx, fy, a, scale)

    # a field of lilies: back row small, front row large
    plants = []
    for i in range(4):
        bx = 260 + i * 230 + rng.uniform(-40, 40)
        top = rng.uniform(330, 520)
        plants.append((bx, top, rng.uniform(62, 80), rng.uniform(-60, 60)))
    for i in range(2):
        bx = 430 + i * 440 + rng.uniform(-60, 60)
        top = rng.uniform(170, 260)
        plants.append((bx, top, rng.uniform(100, 118), rng.uniform(-80, 80)))
    # draw back-to-front (smaller scale first)
    for bx, top, sc, lean in sorted(plants, key=lambda p: p[2]):
        plant(bx, top, sc, lean)

    # ground: a thin black horizon strip at the bottom
    d.rectangle([0, h - 18, w, h], fill=BLACK)

    # title, vertical, top-left, with white backing so stems don't cut through it
    fjp = font(F_JP, 78)
    d.rectangle([28, 22, 28 + 92, 22 + 3 * 84 + 10], fill=WHITE)
    for i, ch in enumerate("彼岸花"):
        d.text((74, 22 + 42 + i * 84), ch, font=fjp, fill=BLACK, anchor="mm")
    # caption block bottom-right on white
    f1 = font(F_SANS_B, 36)
    f2 = font(F_SANS, 27)
    lines = [("HIGANBANA", f1, RED),
             ("red spider lily — it blooms for the equinox week", f2, BLACK),
             ("the leaves and the flowers never meet", f2, BLACK)]
    y = h - 18 - 14 - 3 * 40
    x = w - 30
    # backing
    d.rectangle([x - 700, y - 14, w, h - 18], fill=WHITE)
    for t, f, c in lines:
        d.text((x, y), t, font=f, fill=c, anchor="ra")
        y += 40
    finish_hard(im, "1.png")


# ----------------------------------------------------------------------------
# 2. KAMON — six generated family crests
# ----------------------------------------------------------------------------
def img2():
    rng = random.Random(SEED + 2)
    w, h = W * S, H * S
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)

    def rot(pts, cx, cy, a):
        ca, sa = math.cos(a), math.sin(a)
        return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]

    def ellipse_pts(rx, ry, n=48):
        return [(rx * math.cos(2 * math.pi * i / n), ry * math.sin(2 * math.pi * i / n)) for i in range(n)]

    borders = ["none", "maru", "futomaru", "yukiwa", "kikko", "maru"]
    motifs = ["hoshi", "hishi", "hana", "tsuki", "ya", "wa"]
    counts = [3, 4, 5, 6, 8, 5]
    rng.shuffle(borders); rng.shuffle(motifs); rng.shuffle(counts)

    def crest(cx, cy, R, ink, i):
        n = counts[i]
        border = borders[i]
        motif = motifs[i]
        inner = R
        # --- border
        if border == "maru":
            d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=ink, width=int(R * 0.06))
            inner = R * 0.80
        elif border == "futomaru":
            d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=ink, width=int(R * 0.16))
            inner = R * 0.72
        elif border == "yukiwa":  # snow ring: ring with six notches
            d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=ink, width=int(R * 0.10))
            for k in range(6):
                a = 2 * math.pi * k / 6 + math.pi / 6
                nx, ny = cx + math.cos(a) * R, cy + math.sin(a) * R
                r = R * 0.13
                d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=WHITE)
            inner = R * 0.74
        elif border == "kikko":  # tortoise-shell hexagon
            pts = rot([(R * math.cos(2 * math.pi * i / 6), R * math.sin(2 * math.pi * i / 6)) for i in range(6)], cx, cy, math.pi / 6)
            d.polygon(pts, outline=ink, width=int(R * 0.08))
            inner = R * 0.68
        # --- motif, n-fold
        ring_r = inner * (0.55 if n <= 4 else 0.6)
        phase = -math.pi / 2 + (math.pi / n if rng.random() < 0.5 else 0)
        for k in range(n):
            a = phase + 2 * math.pi * k / n
            ex, ey = cx + math.cos(a) * ring_r, cy + math.sin(a) * ring_r
            if motif == "hoshi":  # stars = discs
                r = inner * (0.30 if n <= 4 else 0.22 if n <= 6 else 0.17)
                d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=ink)
            elif motif == "hishi":  # diamonds pointing outward
                L, Wd = inner * 0.36, inner * 0.20
                pts = rot([(-L / 2, 0), (0, -Wd / 2), (L / 2, 0), (0, Wd / 2)], ex, ey, a)
                d.polygon(pts, fill=ink)
            elif motif == "hana":  # petal ellipses radiating from centre
                L, Wd = inner * 0.42, inner * (0.28 if n <= 5 else 0.20)
                pts = rot([(x + L * 0.55, y) for x, y in ellipse_pts(L * 0.5, Wd * 0.5)], cx, cy, a)
                d.polygon(pts, fill=ink)
            elif motif == "tsuki":  # crescents
                r = inner * (0.30 if n <= 4 else 0.22 if n <= 6 else 0.17)
                d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=ink)
                ox, oy = ex + math.cos(a) * r * 0.45, ey + math.sin(a) * r * 0.45
                d.ellipse([ox - r * 0.8, oy - r * 0.8, ox + r * 0.8, oy + r * 0.8], fill=WHITE)
            elif motif == "ya":  # arrows: shaft + head, radiating
                L = inner * 0.9
                shaft = rot([(0, 0), (L * 0.62, 0)], cx, cy, a)
                d.line(shaft, fill=ink, width=int(inner * 0.07))
                head = rot([(L * 0.62, -inner * 0.13), (L * 0.95, 0), (L * 0.62, inner * 0.13)], cx, cy, a)
                d.polygon(head, fill=ink)
            elif motif == "wa":  # small rings
                r = inner * (0.30 if n <= 4 else 0.22 if n <= 6 else 0.17)
                d.ellipse([ex - r, ey - r, ex + r, ey + r], outline=ink, width=int(r * 0.45))
        # centre element
        if motif in ("hoshi", "tsuki", "wa", "hishi") and rng.random() < 0.6:
            r = inner * 0.12
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ink)
        # --- name
        bname = {"none": "", "maru": "丸に", "futomaru": "太丸に", "yukiwa": "雪輪に", "kikko": "亀甲に"}[border]
        cnt = {3: "三つ", 4: "四つ", 5: "五つ", 6: "六つ", 8: "八つ"}[n]
        mname = {"hoshi": "星", "hishi": "菱", "hana": "花", "tsuki": "月", "ya": "矢", "wa": "輪"}[motif]
        return bname + cnt + mname

    cols, rows = 3, 2
    cw, ch = w / cols, (h - 110) / rows
    R = 140
    fjp = font(F_JP, 38)
    red_slot = rng.randrange(6)
    for i in range(6):
        cx = (i % cols + 0.5) * cw
        cy = (i // cols + 0.5) * ch + 10
        ink = RED if i == red_slot else BLACK
        name = crest(cx, cy - 18, R, ink, i)
        d.text((cx, cy + R + 8), name, font=fjp, fill=ink, anchor="mm")
    # footer
    d.line([(60, h - 100), (w - 60, h - 100)], fill=BLACK, width=3)
    d.text((60, h - 84), "KAMON  家紋", font=font(F_JP, 40), fill=BLACK, anchor="la")
    d.text((w - 60, h - 80), "six family crests that never existed", font=font(F_SANS, 27), fill=BLACK, anchor="ra")
    d.text((w - 60, h - 48), "drawn with compass and ruler · seed 2026-09-20", font=font(F_MONO, 27), fill=RED, anchor="ra")
    finish_hard(im, "2.png")


# ----------------------------------------------------------------------------
# 3. PORTOLAN — Magellan leaves Sanlúcar, 20 Sep 1519
# ----------------------------------------------------------------------------
def img3():
    rng = random.Random(SEED + 3)
    w, h = W * S, H * S
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)

    # --- rhumb-line network: centre + 16 nodes on a circle; 32 winds from each
    cx, cy, Rn = w * 0.42, h * 0.50, h * 0.44
    nodes = [(cx, cy)] + [(cx + Rn * math.cos(2 * math.pi * k / 16), cy + Rn * math.sin(2 * math.pi * k / 16)) for k in range(16)]
    L = 3000
    for (nx, ny) in nodes:
        for k in range(16):
            a = 2 * math.pi * k / 16
            if k % 2 == 0:
                col, wd = BLACK, 3
            else:
                col, wd = RED, 3
            d.line([(nx, ny), (nx + L * math.cos(a), ny + L * math.sin(a))], fill=col, width=wd)

    # --- coastline on the right: a wandering N–S coast (Iberia / Morocco), land white
    def fbm(t, seed):
        r = random.Random(seed)
        amps = [(r.uniform(0, 2 * math.pi), r.uniform(0.6, 1.0)) for _ in range(6)]
        return sum(ap * math.sin(t * (i + 1) * 1.7 + ph) / (i + 1) for i, (ph, ap) in enumerate(amps))

    coast = []
    for i in range(0, h + 1, 6):
        t = i / h * 3.0
        x = w * 0.74 + 110 * fbm(t, 7) + 60 * math.sin(t * 5.1)
        coast.append((x, i))
    land = coast + [(w, h), (w, 0)]
    d.polygon(land, fill=WHITE)
    polyline(d, coast, BLACK, 6)
    # hatching along the coast on the sea side (portolan style shading)
    for i in range(0, len(coast) - 1, 2):
        x, y = coast[i]
        d.line([(x - 6, y), (x - 22, y)], fill=BLACK, width=2)

    # some islands (Canaries) in the sea, lower-left of the coast
    for k in range(5):
        ix, iy = w * 0.50 + rng.uniform(-60, 60) + k * 40, h * 0.86 + rng.uniform(-30, 30)
        rr = rng.uniform(9, 18)
        d.ellipse([ix - rr, iy - rr * 0.7, ix + rr, iy + rr * 0.7], fill=RED)

    # place names, written perpendicular to the coast, on the land side
    fser = font(F_SERIF_I, 28)
    names = [(0.06, "lisboa", BLACK), (0.20, "cabo s. vicente", BLACK), (0.32, "sanlucar", RED),
             (0.40, "cadiz", BLACK), (0.50, "tanger", BLACK), (0.62, "rabat", BLACK), (0.78, "mogador", BLACK)]
    for frac, nm, col in names:
        y = frac * h
        i = min(range(len(coast)), key=lambda j: abs(coast[j][1] - y))
        x = coast[i][0]
        f = font(F_SERIF_B, 32) if col == RED else fser
        rotated_text(im, (x + 16, y), nm, f, -90 + 0, col, anchor="lm")
    # the Canaries label
    d.text((w * 0.50, h * 0.86 + 44), "insule canarie", font=fser, fill=BLACK, anchor="mm")

    # --- compass rose at the centre node
    r0 = 70
    d.ellipse([cx - r0, cy - r0, cx + r0, cy + r0], fill=WHITE, outline=BLACK, width=3)
    for k in range(8):
        a = -math.pi / 2 + 2 * math.pi * k / 8
        tip = (cx + math.cos(a) * (r0 - 6), cy + math.sin(a) * (r0 - 6))
        base_r = 14
        l = (cx + math.cos(a + math.pi / 2) * base_r, cy + math.sin(a + math.pi / 2) * base_r)
        rgt = (cx + math.cos(a - math.pi / 2) * base_r, cy + math.sin(a - math.pi / 2) * base_r)
        d.polygon([tip, l, (cx, cy), rgt], fill=(RED if k == 0 else BLACK) if k % 2 == 0 else WHITE, outline=BLACK)
    # north: fleur-de-lis stand-in — a red triangle above the rose
    d.polygon([(cx, cy - r0 - 34), (cx - 12, cy - r0 - 4), (cx + 12, cy - r0 - 4)], fill=RED)

    # --- a tiny fleet leaving the coast, heading SW
    def ship(x, y, sc):
        # white backing so the rhumb lines don't cut through the little ship
        d.ellipse([x - 34 * sc, y - 42 * sc, x + 34 * sc, y + 16 * sc], fill=WHITE)
        # hull: a long low crescent, stern-castle at right
        d.polygon([(x - 30 * sc, y - 4 * sc), (x + 30 * sc, y - 10 * sc), (x + 22 * sc, y + 10 * sc), (x - 20 * sc, y + 10 * sc)], fill=BLACK)
        # mast + square red sail
        d.line([(x, y - 4 * sc), (x, y - 40 * sc)], fill=BLACK, width=max(2, int(3 * sc)))
        d.rectangle([x - 13 * sc, y - 36 * sc, x + 13 * sc, y - 12 * sc], fill=RED)
    ship(w * 0.61, h * 0.40, 1.5)
    ship(w * 0.55, h * 0.49, 1.3)
    ship(w * 0.64, h * 0.56, 1.2)
    ship(w * 0.51, h * 0.59, 1.1)
    ship(w * 0.58, h * 0.67, 1.0)

    # --- cartouche, lower-left
    bx0, by0, bx1, by1 = 24, h - 336, 24 + 690, h - 24
    d.rectangle([bx0, by0, bx1, by1], fill=WHITE, outline=BLACK, width=4)
    d.rectangle([bx0 + 8, by0 + 8, bx1 - 8, by1 - 8], outline=RED, width=2)
    fb = font(F_SERIF_B, 40)
    fs = font(F_SERIF, 31)
    fi = font(F_SERIF_I, 32)
    tx = bx0 + 26
    d.text((tx, by0 + 24), "20 · IX · 1519", font=fb, fill=RED, anchor="la")
    d.text((tx, by0 + 80), "Five ships and 270 men sail west", font=fs, fill=BLACK, anchor="la")
    d.text((tx, by0 + 118), "from Sanlúcar, under Magellan.", font=fs, fill=BLACK, anchor="la")
    d.text((tx, by0 + 176), "6 · IX · 1522", font=fb, fill=BLACK, anchor="la")
    d.text((tx, by0 + 232), "One ship, Victoria, and 18 men return,", font=fs, fill=BLACK, anchor="la")
    d.text((tx, by0 + 270), "having sailed around the whole world.", font=fi, fill=BLACK, anchor="la")

    # title along the top-left
    d.rectangle([24, 24, 24 + 680, 24 + 50], fill=WHITE)
    d.text((34, 49), "CARTA DE MAREAR · 507 years ago today", font=font(F_SANS_B, 28), fill=BLACK, anchor="lm")
    finish_hard(im, "3.png")


# ----------------------------------------------------------------------------
# 4. ANALEMMA — equinox in two days
# ----------------------------------------------------------------------------
def img4():
    w, h = W * S, H * S
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)

    # low-precision solar ephemeris (Astronomical Almanac): n = day of 2026
    J2000_OFFSET = 9761.5  # days from 2000-01-01 12:00 UT to 2026-09-20... computed below
    import datetime as _dt
    epoch = _dt.datetime(2000, 1, 1, 12)
    def _sun(n):
        t = _dt.datetime(2026, 1, 1) + _dt.timedelta(days=n - 1)
        D = (t - epoch).total_seconds() / 86400
        g = math.radians((357.529 + 0.98560028 * D) % 360)
        q = (280.459 + 0.98564736 * D) % 360
        lam = math.radians(q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g))
        e = math.radians(23.439 - 0.00000036 * D)
        ra = math.degrees(math.atan2(math.cos(e) * math.sin(lam), math.cos(lam))) % 360
        dec = math.degrees(math.asin(math.sin(e) * math.sin(lam)))
        eot = ((q - ra + 180) % 360 - 180) * 4  # minutes, sundial minus clock
        return eot, dec

    def eot(n):
        return _sun(n)[0]

    def decl(n):
        return _sun(n)[1]

    # plot area on the left
    px0, px1 = 120, 560
    py0, py1 = 60, h - 60
    def P(n):
        x = px0 + (eot(n) + 16) / 33 * (px1 - px0)
        y = py0 + (23.44 - decl(n)) / 46.88 * (py1 - py0)
        return x, y

    # axes: equator line (declination 0) and the EoT=0 line
    ex, ey = P(0)
    y0 = py0 + 0.5 * (py1 - py0)
    x0 = px0 + 16 / 33 * (px1 - px0)
    d.line([(px0 - 60, y0), (px1 + 60, y0)], fill=BLACK, width=2)
    for yy in range(py0, py1, 12):
        d.point((x0, yy), fill=BLACK)
    d.line([(x0, py0), (x0, py1)], fill=BLACK, width=1)

    # the curve
    pts = [P(n) for n in range(1, 367)]
    polyline(d, pts, BLACK, 3)
    # a dot per day
    for n in range(1, 366):
        x, y = P(n)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=BLACK)
    # month labels at the 1st of each month
    fm = font(F_MONO, 22)
    firsts = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    mon = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    for i, n in enumerate(firsts):
        x, y = P(n)
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=WHITE, outline=BLACK, width=2)
        side = -1 if eot(n) < eot(n + 15) else 1  # label on the outside of the loop
        # decide by direction of travel; put labels away from the curve
        lx = x + side * 22
        d.text((lx, y), mon[i], font=fm, fill=BLACK, anchor="rm" if side < 0 else "lm")

    # today: Sep 20 = day 263
    today = 263
    tx, ty = P(today)
    d.ellipse([tx - 16, ty - 16, tx + 16, ty + 16], fill=RED)
    d.ellipse([tx - 26, ty - 26, tx + 26, ty + 26], outline=RED, width=3)
    # equinox crossing: Sep 23 00:05 UTC = day 266.0
    qx, qy = P(266.0)
    d.line([(qx, qy - 30), (qx, qy + 30)], fill=RED, width=3)
    d.text((qx - 16, qy + 30), "23 SEP", font=fm, fill=RED, anchor="ra")

    # labels near the plot
    fl = font(F_SANS, 24)
    d.text((px1 + 66, y0 - 4), "δ = 0°", font=fl, fill=BLACK, anchor="lb")
    d.text((px1 + 66, y0 + 4), "equator", font=fl, fill=BLACK, anchor="la")
    d.text((30, py0 + 6), "+23.4°", font=fl, fill=BLACK, anchor="lm")
    d.text((30, py1 - 6), "−23.4°", font=fl, fill=BLACK, anchor="lm")
    d.text((x0, py1 + 34), "← sundial slow · sundial fast →", font=fl, fill=BLACK, anchor="mm")

    # right column text
    rx = 640
    d.text((rx, 70), "ANALEMMA", font=font(F_SANS_B, 46), fill=BLACK, anchor="la")
    d.text((rx, 130), "where the noon Sun stands,", font=font(F_SANS, 24), fill=BLACK, anchor="la")
    d.text((rx, 160), "one dot for every day of the year", font=font(F_SANS, 24), fill=BLACK, anchor="la")

    d.rectangle([rx, 230, w - 40, 236], fill=RED)
    d.text((rx, 256), "TODAY", font=font(F_SANS_B, 26), fill=RED, anchor="la")
    d.text((rx, 292), f"Sun at {decl(today):+.1f}°, sundial {eot(today):+.0f} min", font=font(F_SANS, 24), fill=BLACK, anchor="la")
    d.text((rx, 322), "sliding south 0.4° a day", font=font(F_SANS, 24), fill=BLACK, anchor="la")

    d.text((rx, 400), "EQUINOX", font=font(F_SANS_B, 60), fill=BLACK, anchor="la")
    d.text((rx, 478), "in 2 days", font=font(F_SANS_B, 40), fill=RED, anchor="la")
    d.text((rx, 540), "23 Sep 2026 · 00:05 UTC", font=font(F_MONO_B, 26), fill=BLACK, anchor="la")
    d.text((rx, 584), "the Sun crosses the equator heading", font=font(F_SANS, 24), fill=BLACK, anchor="la")
    d.text((rx, 614), "south; day and night come out even", font=font(F_SANS, 24), fill=BLACK, anchor="la")
    d.text((rx, 644), "for everyone on Earth at once.", font=font(F_SANS, 24), fill=BLACK, anchor="la")

    d.text((rx, h - 60), "Harvest Moon meets Saturn on the 26th", font=font(F_SANS, 22), fill=BLACK, anchor="lb")
    finish_hard(im, "4.png")


# ----------------------------------------------------------------------------
# 5. LONG LIFE — Conway's Life, long exposure
# ----------------------------------------------------------------------------
def img5():
    rs = np.random.RandomState(SEED + 5)
    GW, GH = 200, 138  # cells; 2px each -> 400 x 276, leaving 24px for a caption
    GENS = 300
    grid = np.zeros((GH, GW), dtype=np.uint8)
    # a few dense random "seed" blobs so the soup has room to throw gliders
    for _ in range(16):
        cx, cy = rs.randint(25, GW - 25), rs.randint(18, GH - 18)
        r = rs.randint(7, 15)
        yy, xx = np.ogrid[:GH, :GW]
        mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
        grid[mask] = (rs.rand(mask.sum()) < 0.45).astype(np.uint8)

    exposure = np.zeros((GH, GW), dtype=np.int32)
    for g in range(GENS):
        exposure += grid
        n = sum(np.roll(np.roll(grid, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dx, dy) != (0, 0))
        grid = ((n == 3) | ((grid == 1) & (n == 2))).astype(np.uint8)
        # edges are walls: kill wraparound
        grid[0, :] = grid[-1, :] = 0
        grid[:, 0] = grid[:, -1] = 0

    # 5-level ordered dither per 2x2 cell from exposure
    lvl = np.clip(np.sqrt(exposure / 45.0) * 4, 0, 4).round().astype(int)
    # bayer 2x2 order of which subpixels fill first
    order = [(0, 0), (1, 1), (0, 1), (1, 0)]
    idx = np.zeros((H, W), dtype=np.uint8)
    for k in range(4):
        oy, ox = order[k]
        fill = (lvl > k)
        idx[oy:GH * 2:2, ox:GW * 2:2][fill] = 1
    alive = grid == 1
    for oy in (0, 1):
        for ox in (0, 1):
            idx[oy:GH * 2:2, ox:GW * 2:2][alive] = 2

    # caption strip
    im = Image.fromarray(idx, "P")
    im.putpalette(list(WHITE) + list(BLACK) + list(RED) + list(BLACK) * 253)
    d = ImageDraw.Draw(im)
    d.rectangle([0, GH * 2, W, H], fill=0)
    d.line([(0, GH * 2), (W, GH * 2)], fill=1, width=1)
    d.text((6, GH * 2 + 6), "LIFE · LONG EXPOSURE", font=font(F_MONO_B, 12), fill=1, anchor="la")
    d.text((W - 6, GH * 2 + 6), f"{GENS} generations · red = still alive", font=font(F_MONO, 11), fill=2, anchor="ra")
    im.save(os.path.join(OUT, "5.png"), optimize=True)
    print("saved 5.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    img1(); img2(); img3(); img4(); img5()
    for i in range(1, 6):
        shutil.copy(os.path.join(OUT, f"{i}.png"), os.path.join(HERE, f"{i}.png"))
