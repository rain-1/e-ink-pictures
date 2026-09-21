#!/usr/bin/env python3
"""Daily e-ink plates — 2026-09-21.

Higan: the Buddhist week around the autumn equinox, when (the saying goes)
the far shore comes close. Five plates for a 400x300 black/white/red panel.

Pipeline notes (see memory-fable-5-1.md):
  * Big art is drawn at 3x in PURE palette colours, LANCZOS-downscaled, then
    snapped to the palette with NO dither -> shape-accurate, colour-pure edges.
  * Tonal passages are drawn as grey at 3x and hand-dithered to black/white
    only (never through the 3-colour quantiser, which speckles grey with red).
  * Small type is drawn at 1x directly onto the final P-mode image, so it stays
    hairline crisp instead of being smeared by the downscale.
"""

import itertools
import math
import os
import random
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, SS = 400, 300, 3
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
IW, IB, IR = 0, 1, 2  # palette indices
DATE = "2026-09-21"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"
F_MONO, F_MONO_B = FD + "DejaVuSansMono.ttf", FD + "DejaVuSansMono-Bold.ttf"
F_SANS, F_SANS_B = FL + "LiberationSans-Regular.ttf", FL + "LiberationSans-Bold.ttf"
F_SERIF = FD + "DejaVuSerif.ttf"
F_DSANS_B = FD + "DejaVuSans-Bold.ttf"
F_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def ft(path, size):
    return ImageFont.truetype(path, size)


# ------------------------------------------------------------------ palette
def _pal():
    p = Image.new("P", (1, 1))
    p.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)
    return p


PAL = _pal()


def snap(img):
    """Downscale to 400x300 and snap to the 3-colour palette without dithering."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img.convert("RGB").quantize(palette=PAL, dither=Image.Dither.NONE)


def fs_bw(gray):
    """Floyd-Steinberg a float array to 0/255 only (no red contamination)."""
    g = gray.astype(np.float64).copy()
    h, w = g.shape
    for y in range(h):
        row = g[y]
        for x in range(w):
            old = row[x]
            new = 255.0 if old >= 128.0 else 0.0
            err = old - new
            row[x] = new
            if x + 1 < w:
                row[x + 1] += err * 0.4375
            if y + 1 < h:
                nxt = g[y + 1]
                if x > 0:
                    nxt[x - 1] += err * 0.1875
                nxt[x] += err * 0.3125
                if x + 1 < w:
                    nxt[x + 1] += err * 0.0625
    return g


def snap_with_tonal(img, tonal_mask_3x):
    """Snap, but hand-dither the masked region to black/white."""
    small = img.resize((W, H), Image.LANCZOS)
    base = np.array(snap(small))
    m = np.array(tonal_mask_3x.convert("L").resize((W, H), Image.LANCZOS)) > 127
    if m.any():
        lum = np.array(small.convert("L"), dtype=np.float64)
        dith = fs_bw(lum)
        base[m] = np.where(dith[m] > 127, IW, IB)
    out = Image.fromarray(base.astype(np.uint8), mode="P")
    out.putpalette(PAL.getpalette())
    return out


def new3x(bg=WHITE):
    img = Image.new("RGB", (W * SS, H * SS), bg)
    return img, ImageDraw.Draw(img)


def cartouche(p, box, lines, font=None, pad=6, lead=11, border=True):
    """White label panel with a hairline border, drawn 1x on the final image."""
    dr = ImageDraw.Draw(p)
    x0, y0, x1, y1 = box
    dr.rectangle([x0, y0, x1, y1], fill=IW, outline=IB if border else None)
    f = font or ft(F_MONO, 8)
    y = y0 + pad
    for ln, colour in lines:
        dr.text((x0 + pad, y), ln, font=f, fill=colour)
        y += lead
    return dr


def sign(p, left, right=DATE.replace("-", "·"), y=None, colour=IB):
    dr = ImageDraw.Draw(p)
    f = ft(F_MONO, 8)
    y = H - 13 if y is None else y
    dr.text((11, y), left, font=f, fill=colour)
    dr.text((W - 11 - dr.textlength(right, font=f), y), right, font=f, fill=colour)


# ------------------------------------------------------------------ geometry
def qbez(p0, p1, p2, n=40):
    out = []
    for i in range(n):
        t = i / (n - 1)
        u = 1 - t
        out.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return out


def ribbon(pts, widths):
    left, right = [], []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1:
            dx, dy = x - pts[-2][0], y - pts[-2][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        hw = widths[i] * 0.5
        left.append((x + nx * hw, y + ny * hw))
        right.append((x - nx * hw, y - ny * hw))
    return left + right[::-1]


def arc_path(x, y, ang, length, turn, n=30):
    pts, step = [], length / (n - 1)
    a = ang
    for _ in range(n):
        pts.append((x, y))
        x += step * math.cos(a)
        y += step * math.sin(a)
        a += turn / (n - 1)
    return pts


# ============================================================ 1. HIGANBANA
def plate1():
    """彼岸花 — the flower of the far shore. Bare stems, recurved red petals."""
    rng = random.Random(20260921)
    s = SS
    img, dr = new3x()

    # --- earth: a grey wash that darkens downward, hand-dithered later
    mask = Image.new("L", (W * s, H * s), 0)
    mdr = ImageDraw.Draw(mask)
    top = 254 * s
    mdr.rectangle([0, top, W * s, H * s], fill=255)
    for yy in range(top, H * s):
        t = (yy - top) / (H * s - top)
        v = int(196 - 176 * (t ** 0.55))
        dr.line([(0, yy), (W * s, yy)], fill=(v, v, v))
    # a scatter of pebbles/stubble silhouettes at the soil line
    for _ in range(90):
        px = rng.uniform(0, W * s)
        py = top + rng.uniform(-2 * s, 10 * s)
        r = rng.uniform(0.6 * s, 2.2 * s)
        g = rng.randint(30, 120)
        dr.ellipse([px - r, py - r * 0.6, px + r, py + r * 0.6], fill=(g, g, g))

    def stem(x0, y0, x1, y1, w):
        ctrl = ((x0 + x1) / 2 + rng.uniform(-16, 16) * s, (y0 + y1) / 2)
        pts = qbez((x0, y0), ctrl, (x1, y1), 34)
        ws = [w * s * (1.25 - 0.45 * i / 33) for i in range(34)]
        dr.polygon(ribbon(pts, ws), fill=BLACK)

    def lily(cx, cy, R, rot):
        cx, cy, R = cx * s, cy * s, R * s
        # six narrow tepals: long, wavy, curving back on themselves
        for i in range(6):
            a = rot + i * math.tau / 6 + rng.uniform(-0.13, 0.13)
            ln = R * rng.uniform(1.35, 1.62)
            sgn = 1.0 if rng.random() < 0.5 else -1.0
            pts = arc_path(cx, cy, a, ln, sgn * rng.uniform(0.95, 1.40), 36)
            ws = []
            for k in range(36):
                t = k / 35
                w = 0.115 * R * (math.sin(math.pi * t) ** 0.38)
                w *= 1 + 0.32 * math.sin(t * 15 + i * 1.7)
                ws.append(max(w, 0.8 * s))
            dr.polygon(ribbon(pts, ws), fill=RED)
        # six long stamens, fanned up and out over the flower
        for i in range(6):
            base = -math.pi / 2 + (i - 2.5) * 0.48 + rng.uniform(-0.05, 0.05)
            ln = R * rng.uniform(1.9, 2.3)
            turn = (base + math.pi / 2) * 1.2 + rng.uniform(-0.12, 0.12)
            pts = arc_path(cx, cy, base, ln, turn, 34)
            dr.line([(px, py) for px, py in pts], fill=BLACK,
                    width=max(3, int(1.25 * s)), joint="curve")
            tx, ty = pts[-1]
            ar = 1.8 * s
            dr.ellipse([tx - ar, ty - ar * 0.7, tx + ar, ty + ar * 0.7], fill=BLACK)
        hr = 0.085 * R
        dr.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=BLACK)

    heads = [(214, 122, 42, 0.30), (296, 70, 48, 1.05), (352, 156, 34, 2.10)]
    for hx, hy, R, rot in heads:
        stem(hx * s + rng.uniform(-3, 3) * s, 264 * s, hx * s, hy * s, 2.1)
    # one stem with no flower on it: the leaves and the flowers never meet
    stem(180 * s, 262 * s, 174 * s, 186 * s, 1.6)
    for hx, hy, R, rot in heads:
        lily(hx, hy, R, rot)

    # --- 彼岸花 vertically, left column
    fj = ft(F_JP, 33 * s)
    for i, ch in enumerate("彼岸花"):
        dr.text((24 * s, (30 + i * 37) * s), ch, font=fj, fill=BLACK)
    dr.line([(24 * s, 146 * s), (57 * s, 146 * s)], fill=RED, width=max(2, s))

    p = snap_with_tonal(img, mask)
    d = ImageDraw.Draw(p)
    f8 = ft(F_MONO, 8)
    d.text((22, 178), "HIGANBANA", font=ft(F_MONO_B, 8), fill=IB)
    d.text((22, 189), "Lycoris radiata", font=f8, fill=IB)
    d.text((22, 205), "the flower of the far shore:", font=f8, fill=IB)
    d.text((22, 216), "it opens on bare stems in", font=f8, fill=IB)
    d.text((22, 227), "the equinox week, and", font=f8, fill=IB)
    d.text((22, 238), "never meets its own leaves.", font=f8, fill=IB)
    sign(p, "HIGAN · 彼岸", colour=IW)
    return p


# ============================================================ 2. SHUBUN
def plate2():
    """秋分 — the one day the shadow line runs through both poles."""
    s = SS
    img, dr = new3x()
    cx, cy, R = 126 * s, 150 * s, 100 * s

    # globe, wireframe, built white-on-black then half-inverted
    gl = Image.new("L", (W * s, H * s), 0)
    gd = ImageDraw.Draw(gl)
    gd.ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
    lw = max(2, int(0.9 * s))
    for lat in range(-75, 76, 15):
        yy = cy - R * math.sin(math.radians(lat))
        hw = R * math.cos(math.radians(lat))
        gd.line([(cx - hw, yy), (cx + hw, yy)], fill=0, width=lw)
    for k in range(6):
        lon = k * 30
        b = abs(R * math.cos(math.radians(lon)))
        if b < 1:
            gd.line([(cx, cy - R), (cx, cy + R)], fill=0, width=lw)
        else:
            gd.ellipse([cx - b, cy - R, cx + b, cy + R], outline=0, width=lw)
    gd.ellipse([cx - R, cy - R, cx + R, cy + R], outline=0, width=max(2, int(1.2 * s)))
    ga = np.array(gl)
    disc = np.zeros_like(ga, dtype=bool)
    yy, xx = np.mgrid[0:H * s, 0:W * s]
    disc = (xx - cx) ** 2 + (yy - cy) ** 2 <= R * R
    night = disc & (xx < cx)
    ga[night] = 255 - ga[night]
    base = np.array(img)
    g3 = np.stack([ga] * 3, axis=-1)
    base[disc] = g3[disc]
    img = Image.fromarray(base)
    dr = ImageDraw.Draw(img)

    # the terminator, dead vertical today, and the equator, edge to edge in red
    dr.line([(cx, cy - R), (cx, cy + R)], fill=RED, width=max(2, int(1.3 * s)))
    dr.rectangle([0, cy - int(1.5 * s), W * s, cy + int(1.5 * s)], fill=RED)
    # the sun itself, riding the equator off the right edge
    sx, sr = 404 * s, 22 * s
    dr.ellipse([sx - sr, cy - sr, sx + sr, cy + sr], fill=RED)

    # 玄鳥去 — swallows leaving, upper left
    def swallow(x, y, k, flip=1):
        x, y = x * s, y * s
        pts = [(x, y), (x - 9 * k, y - 6 * k), (x - 3.5 * k, y - 1.5 * k),
               (x - 10 * k, y + 5.5 * k), (x - 2.5 * k, y + 1.2 * k),
               (x + 2 * k, y + 4 * k)]
        dr.polygon([(px, y + flip * (py - y)) for px, py in pts], fill=BLACK)

    swallow(74, 26, 1.5 * s)
    swallow(122, 16, 1.1 * s, -1)
    swallow(166, 33, 1.3 * s)
    swallow(205, 20, 0.9 * s, -1)

    fj = ft(F_JP, 46 * s)
    dr.text((248 * s, 34 * s), "秋分", font=fj, fill=BLACK)
    dr.line([(249 * s, 92 * s), (386 * s, 92 * s)], fill=BLACK, width=max(2, s))

    dr.text((249 * s, 236 * s), "玄鳥去", font=ft(F_JP, 17 * s), fill=BLACK)

    p = snap(img)
    d = ImageDraw.Draw(p)
    f8, f8b = ft(F_MONO, 8), ft(F_MONO_B, 8)
    d.text((249, 100), "SHUBUN", font=f8b, fill=IB)
    d.text((249, 111), "AUTUMN EQUINOX", font=f8b, fill=IB)
    d.text((249, 127), "2026-09-23  00:05", font=f8, fill=IB)
    d.text((249, 138), "UTC", font=f8, fill=IB)
    para = ["the sun crosses the", "celestial equator;", "the shadow line",
            "touches both poles;", "day and night are", "of one length."]
    for i, ln in enumerate(para):
        d.text((249, 166 + i * 11), ln, font=f8, fill=IB)
    d.rectangle([249, 230, 357, 230], fill=IB)
    d.text((249, 258), "swallows depart:", font=f8, fill=IB)
    d.text((249, 269), "the 45th microseason", font=f8, fill=IB)
    sign(p, "TERMINATOR · POLE TO POLE", y=286)
    return p


# ============================================================ 3. SANDPILE
def plate3():
    """An abelian sandpile: 2^17 grains dropped on a single square."""
    n, size = 1 << 17, 401
    g = np.zeros((size, size), dtype=np.int64)
    c = size // 2
    g[c, c] = n
    while True:
        t = g >> 2
        if not t.any():
            break
        g -= t << 2
        g[1:, :] += t[:-1, :]
        g[:-1, :] += t[1:, :]
        g[:, 1:] += t[:, :-1]
        g[:, :-1] += t[:, 1:]

    win = g[c - 150:c + 150, c - 200:c + 200]  # 300 x 400, pile centred
    idx = np.full((H, W), IW, dtype=np.uint8)
    yy, xx = np.mgrid[0:H, 0:W]
    checker = (xx + yy) % 2 == 0
    idx[win == 1] = IR
    idx[(win == 2) & checker] = IB
    idx[win == 3] = IB
    p = Image.fromarray(idx, mode="P")
    p.putpalette(PAL.getpalette())

    cartouche(p, (10, 10, 191, 47), [
        ("ABELIAN SANDPILE", IB),
        ("131 072 grains, one square", IB),
    ], font=ft(F_MONO_B, 8))
    d = ImageDraw.Draw(p)
    f8 = ft(F_MONO, 8)
    d.rectangle([236, 259, 390, 290], fill=IW, outline=IB)
    d.text((242, 265), "each cell keeps at most 3;", font=f8, fill=IB)
    d.text((242, 276), "a fourth topples outward.", font=f8, fill=IB)
    d.text((12, 281), DATE.replace("-", "·"), font=f8, fill=IB)
    return p


# ============================================================ 4. HEPTAGRID
def plate4():
    """A sevenfold quasicrystal by de Bruijn's dual method: 3 rhombi, 3 colours."""
    N, KR, E_ = 7, 14, 25.4
    rng = random.Random(264)
    gam = [rng.uniform(0.05, 0.95) for _ in range(N)]
    E = [(math.cos(math.pi * j / N), math.sin(math.pi * j / N)) for j in range(N)]
    s = SS
    img, dr = new3x()
    ox, oy = W * s * 0.5, H * s * 0.5
    fill = {1: RED, 2: BLACK, 3: WHITE}
    tiles = []
    for j, l in itertools.combinations(range(N), 2):
        ej, el = E[j], E[l]
        det = ej[0] * el[1] - ej[1] * el[0]
        for kj in range(-KR, KR + 1):
            for kl in range(-KR, KR + 1):
                aj, al = kj - gam[j], kl - gam[l]
                x = (aj * el[1] - al * ej[1]) / det
                y = (al * ej[0] - aj * el[0]) / det
                K = [math.ceil(x * E[m][0] + y * E[m][1] + gam[m]) for m in range(N)]
                K[j], K[l] = kj, kl
                vx = sum(K[m] * E[m][0] for m in range(N))
                vy = sum(K[m] * E[m][1] for m in range(N))
                px, py = ox + vx * E_ * s, oy + vy * E_ * s
                cxx = px + (ej[0] + el[0]) * E_ * s * 0.5
                cyy = py + (ej[1] + el[1]) * E_ * s * 0.5
                if -40 * s < cxx < (W + 40) * s and -40 * s < cyy < (H + 40) * s:
                    cls = min(abs(j - l), N - abs(j - l))
                    tiles.append((cls, px, py, ej, el))
    for cls, px, py, ej, el in tiles:
        q = [(px, py),
             (px + ej[0] * E_ * s, py + ej[1] * E_ * s),
             (px + (ej[0] + el[0]) * E_ * s, py + (ej[1] + el[1]) * E_ * s),
             (px + el[0] * E_ * s, py + el[1] * E_ * s)]
        dr.polygon(q, fill=fill[cls], outline=BLACK, width=max(2, int(1.1 * s)))

    p = snap(img)
    cartouche(p, (10, 236, 263, 289), [
        ("HEPTAGRID", IB),
        ("a sevenfold quasicrystal: three rhombi,", IB),
        ("three colours, no repeating unit.", IB),
        ("de Bruijn dual of seven line families", IB),
    ], font=ft(F_MONO, 8), pad=5, lead=11)
    d = ImageDraw.Draw(p)
    f8 = ft(F_MONO_B, 8)
    d.rectangle([301, 10, 390, 27], fill=IW, outline=IB)
    d.text((306, 15), DATE.replace("-", "·"), font=f8, fill=IB)
    return p


# ============================================================ 5. MIR
def plate5():
    """МИР — the same word for peace and for world. International Day of Peace."""
    s = SS
    size = (W * s, H * s)
    DX, DY, DR = 135, 132, 88

    m_disc = Image.new("L", size, 0)
    ImageDraw.Draw(m_disc).ellipse([(DX - DR) * s, (DY - DR) * s,
                                    (DX + DR) * s, (DY + DR) * s], fill=255)
    m_ring = Image.new("L", size, 0)
    ImageDraw.Draw(m_ring).ellipse([(DX - DR - 9) * s, (DY - DR - 9) * s,
                                    (DX + DR + 9) * s, (DY + DR + 9) * s],
                                   outline=255, width=max(2, s))
    m_band = Image.new("L", size, 0)
    bd = ImageDraw.Draw(m_band)
    a = math.radians(-17)
    nx, ny = -math.sin(a), math.cos(a)
    th = 23 * s
    p0 = (-40 * s, 300 * s)
    p1 = (450 * s, (300 + math.tan(a) * 490) * s)
    bd.polygon([(p0[0] + nx * th, p0[1] + ny * th), (p1[0] + nx * th, p1[1] + ny * th),
                (p1[0] - nx * th, p1[1] - ny * th), (p0[0] - nx * th, p0[1] - ny * th)],
               fill=255)
    m_sq = Image.new("L", size, 0)
    sq = ImageDraw.Draw(m_sq)
    sq.rectangle([344 * s, 26 * s, 376 * s, 58 * s], fill=255)
    sq.rectangle([24 * s, 26 * s, 32 * s, 196 * s], fill=255)

    tl = Image.new("L", (900 * s, 220 * s), 0)
    ImageDraw.Draw(tl).text((0, 0), "\u041c\u0418\u0420",
                            font=ft(F_DSANS_B, 92 * s), fill=255)
    tl = tl.crop(tl.getbbox()).rotate(17, expand=True, resample=Image.BICUBIC)
    m_text = Image.new("L", size, 0)
    m_text.paste(tl, (int(98 * s), int(92 * s)))

    D = np.array(m_disc) > 127
    B = np.array(m_band) > 127
    T = np.array(m_text) > 127
    S = np.array(m_sq) > 127
    Rg = np.array(m_ring) > 127

    out = np.full((H * s, W * s, 3), 255, dtype=np.uint8)
    out[Rg & ~D] = BLACK
    out[D] = RED
    out[B & ~D] = BLACK
    out[B & D] = WHITE
    out[S] = BLACK
    out[T] = BLACK
    out[T & (D | B | S)] = WHITE

    p = snap(Image.fromarray(out))
    d = ImageDraw.Draw(p)
    d.rectangle([6, 6, W - 7, H - 7], outline=IB)
    f8, f8b = ft(F_MONO, 8), ft(F_MONO_B, 8)
    d.rectangle([44, 258, 356, 288], fill=IW, outline=IB)
    d.text((50, 264), "\u041c\u0418\u0420 \u00b7 one word for peace and for world",
           font=f8b, fill=IB)
    d.text((50, 275), "international day of peace \u00b7 21 september 2026",
           font=f8, fill=IB)
    d.text((46, 20), "IN PLACE OF THE RED WEDGE", font=f8, fill=IB)
    return p


# ------------------------------------------------------------------- driver
def main():
    plates = [
        ("1", plate1, "higanbana"),
        ("2", plate2, "shubun"),
        ("3", plate3, "sandpile"),
        ("4", plate4, "heptagrid"),
        ("5", plate5, "mir"),
    ]
    os.makedirs(os.path.join(REPO, "images"), exist_ok=True)
    for num, fn, slug in plates:
        p = fn()
        assert p.size == (W, H) and p.mode == "P"
        arr = np.array(p)
        assert arr.max() <= 2, f"plate {num} used a colour outside the palette"
        out = os.path.join(HERE, f"{num}.png")
        p.save(out, optimize=True)
        shutil.copyfile(out, os.path.join(REPO, "images", f"{num}.png"))
        cnt = [int((arr == k).sum()) for k in range(3)]
        print(f"plate {num} {slug:10s} white/black/red = {cnt}")


if __name__ == "__main__":
    main()
