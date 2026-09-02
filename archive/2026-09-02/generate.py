#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-02.

Five 400×300 pictures in exactly three colors (white paper, black ink, red ink)
made as if they came off a two-drum Risograph: separate black and red plates,
grain-touch dithering, coarse 45° halftone screens, and a deliberately
misregistered red plate.

Pipeline: every picture is two float "ink density" plates K (black) and R (red)
in [0, 1] at 400×300. Each plate is dithered independently (grain or screen),
the red plate is shifted a couple of pixels, and the result is composited:
black wins over red, red wins over paper.
"""

import math
import os
import random
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 2  # supersample for text / vector plates
DATE = "2026-09-02"
SEED = 20260902

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F_SANS_B = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
F_SANS_BO = "/usr/share/fonts/truetype/freefont/FreeSansBoldOblique.ttf"
F_DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
F_SERIF_BI = "/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# --------------------------------------------------------------------------- plates
class Plate:
    """A supersampled grayscale canvas that becomes a float ink-density array."""

    def __init__(self, ss=SS):
        self.ss = ss
        self.img = Image.new("L", (W * ss, H * ss), 0)
        self.dr = ImageDraw.Draw(self.img)

    def s(self, v):
        return v * self.ss

    def text(self, xy, txt, path, size, fill=255, anchor="la", **kw):
        f = font(path, int(size * self.ss))
        self.dr.text((xy[0] * self.ss, xy[1] * self.ss), txt, font=f, fill=fill, anchor=anchor, **kw)

    def text_width(self, txt, path, size):
        f = font(path, int(size * self.ss))
        return f.getlength(txt) / self.ss

    def crisp(self, thr=0.38):
        """Hard-thresholded mask for text and vector shapes (no grain on type)."""
        return self.density() > thr

    def density(self):
        im = self.img
        if self.ss != 1:
            im = im.resize((W, H), Image.LANCZOS)
        return np.asarray(im, dtype=np.float32) / 255.0


def bayer(n):
    m = np.array([[0]], dtype=np.float32)
    while m.shape[0] < n:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return (m + 0.5) / (m.shape[0] ** 2)


B8 = bayer(8)


def grain(d, rng, jitter=0.35):
    """Grain-touch dither: ordered matrix blended with noise so tone reads as ink grain."""
    ty = np.tile(B8, (H // 8 + 1, W // 8 + 1))[:H, :W]
    noise = rng.random((H, W), dtype=np.float32)
    t = (1 - jitter) * ty + jitter * noise
    return d > t


def screen(d, cell=5.0, angle=45.0):
    """Screen-covered halftone: a rotated dot screen whose dot area follows density."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = math.radians(angle)
    u = (xx * math.cos(a) + yy * math.sin(a)) / cell
    v = (-xx * math.sin(a) + yy * math.cos(a)) / cell
    fu = u - np.floor(u) - 0.5
    fv = v - np.floor(v) - 0.5
    dist2 = fu * fu + fv * fv
    r2 = np.clip(d, 0, 1) / math.pi  # dot area == density
    ink = dist2 < r2
    ink |= d >= 0.97
    ink &= d > 0.02
    return ink


def shift(mask, dx, dy):
    out = np.zeros_like(mask)
    ys = slice(max(dy, 0), H + min(dy, 0))
    yd = slice(max(-dy, 0), H + min(-dy, 0))
    xs = slice(max(dx, 0), W + min(dx, 0))
    xd = slice(max(-dx, 0), W + min(-dx, 0))
    out[ys, xs] = mask[yd, xd]
    return out


def composite(k_ink, r_ink, misreg=(2, 1)):
    r_ink = shift(r_ink, *misreg)
    rgb = np.full((H, W, 3), 255, dtype=np.uint8)
    rgb[r_ink] = RED
    rgb[k_ink] = BLACK
    return rgb


def registration_marks(K, R, x=W - 14, y=H - 14):
    """Tiny printer's registration cross, my signature, on both plates."""
    for P in (K, R):
        s = P.ss
        P.dr.ellipse([(x - 5) * s, (y - 5) * s, (x + 5) * s, (y + 5) * s], outline=255, width=s)
        P.dr.line([(x - 7) * s, y * s, (x + 7) * s, y * s], fill=255, width=s)
        P.dr.line([x * s, (y - 7) * s, x * s, (y + 7) * s], fill=255, width=s)


PAL_IMG = Image.new("P", (1, 1))
PAL_IMG.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)


def save(rgb, n):
    img = Image.fromarray(rgb, "RGB").quantize(palette=PAL_IMG, dither=Image.Dither.NONE)
    assert len(np.unique(rgb.reshape(-1, 3), axis=0)) <= 3
    os.makedirs("images", exist_ok=True)
    os.makedirs(f"archive/{DATE}", exist_ok=True)
    img.save(f"images/{n}.png", optimize=True)
    img.save(f"archive/{DATE}/{n}.png", optimize=True)
    print(f"wrote {n}.png")


# --------------------------------------------------------------------------- noise
def value_noise(rng, shape, scale):
    """Smooth value noise by upscaling a small random grid."""
    h, w = shape
    gh, gw = max(2, int(h / scale) + 2), max(2, int(w / scale) + 2)
    g = rng.random((gh, gw), dtype=np.float32)
    im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(im, dtype=np.float32) / 255.0


def fbm(rng, shape, scale, octaves=4):
    out = np.zeros(shape, np.float32)
    amp, tot = 1.0, 0.0
    for _ in range(octaves):
        out += amp * value_noise(rng, shape, scale)
        tot += amp
        scale /= 2
        amp /= 2
    return out / tot


# =========================================================================== 1. Pudding Lane
def image1_pudding_lane():
    rng = np.random.default_rng(SEED + 1)
    prng = random.Random(SEED + 1)
    K, R = Plate(), Plate()
    s = SS
    base = 226  # skyline baseline (river bank)

    # --- black plate: 1666 skyline ------------------------------------------
    def house(x, w, h, gable=True):
        y0 = base - h
        K.dr.rectangle([x * s, y0 * s, (x + w) * s, base * s], fill=255)
        if gable:
            K.dr.polygon([(x * s, y0 * s), ((x + w / 2) * s, (y0 - w * 0.55) * s), ((x + w) * s, y0 * s)], fill=255)
        # chimney
        cx = x + prng.uniform(0.15, 0.8) * w
        K.dr.rectangle([cx * s, (y0 - w * 0.55 - 6) * s, (cx + 3) * s, y0 * s], fill=255)

    def spire(x, w, tower_h, spire_h):
        K.dr.rectangle([x * s, (base - tower_h) * s, (x + w) * s, base * s], fill=255)
        K.dr.polygon([(x * s, (base - tower_h) * s), ((x + w / 2) * s, (base - tower_h - spire_h) * s),
                      ((x + w) * s, (base - tower_h) * s)], fill=255)
        K.dr.line([(x + w / 2) * s, (base - tower_h - spire_h) * s, (x + w / 2) * s, (base - tower_h - spire_h - 7) * s],
                  fill=255, width=s)

    x = -4
    while x < W + 10:
        w = prng.uniform(9, 20)
        h = prng.uniform(14, 40)
        house(x, w, h)
        x += w + prng.uniform(0, 2)
    # parish churches
    for sx, sw, th, sh in [(38, 10, 55, 40), (112, 12, 48, 30), (175, 9, 62, 44), (300, 11, 50, 34), (355, 9, 58, 46)]:
        spire(sx, sw, th, sh)
    # Old St Paul's: long nave, squat central tower (its spire fell in 1561)
    K.dr.rectangle([205 * s, (base - 62) * s, 285 * s, base * s], fill=255)
    K.dr.polygon([(205 * s, (base - 62) * s), (245 * s, (base - 84) * s), (285 * s, (base - 62) * s)], fill=255)
    K.dr.rectangle([236 * s, (base - 110) * s, 256 * s, base * s], fill=255)
    for px in (236, 251):  # pinnacles
        K.dr.polygon([(px * s, (base - 110) * s), ((px + 2.5) * s, (base - 122) * s), ((px + 5) * s, (base - 110) * s)], fill=255)
    # river bank / quay
    K.dr.rectangle([0, base * s, W * s, (base + 3) * s], fill=255)

    # pigeons "loth to leave their houses"
    def bird(cx, cy, sz, flap):
        pts = [(cx - sz, cy - flap * sz * 0.5), (cx - sz * 0.5, cy), (cx, cy - sz * 0.25), (cx + sz * 0.5, cy), (cx + sz, cy - flap * sz * 0.5)]
        K.dr.line([(p[0] * s, p[1] * s) for p in pts], fill=255, width=max(1, int(s * 0.9)), joint="curve")

    for _ in range(11):
        bird(prng.uniform(20, 380), prng.uniform(30, 120), prng.uniform(3, 6.5), prng.choice([0.6, 1.0, 1.4]))

    # type
    K.text((14, 12), "PUDDING LANE", F_SANS_B, 36)
    K.text((14, 268), "the poor pigeons were loth to leave their houses,", F_MONO, 9)
    K.text((14, 279), "but hovered about the windows and balconys  — Pepys, Sun. 2 Sep 1666", F_MONO, 9)
    R.text((16, 50), "2 SEPTEMBER 1666 · 360 YEARS", F_MONO_B, 11)

    Kd = np.zeros((H, W), np.float32)

    # --- red plate: the fire ----------------------------------------------
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    turb = fbm(rng, (H, W), 60, 5)
    tongues = fbm(rng, (H, W), 18, 3)
    # flames rise from the skyline; strongest around Pudding Lane / the bridge end (right of centre)
    hot = np.exp(-((xx - 250) / 150) ** 2)
    rise = np.clip((base + 6 - yy) / 150.0, 0, 1)  # 1 at skyline, 0 high in sky
    flame = (1 - rise) ** 1.2  # ink lighter with height
    d = (1.35 * flame + 0.8 * (turb - 0.5) + 0.7 * (tongues - 0.5)) * (0.6 + 0.7 * hot) + 0.25 * rise ** 3
    d = np.clip(d, 0, 1)
    d[yy > base + 2] = 0
    d[yy < 62] *= 0.35
    # keep the title area clear
    d[(yy < 60) & (xx < 300)] = 0
    # river: reflection of the fire, streaky
    river = (yy > base + 3) & (yy < 262)
    ref = np.clip(0.55 * hot * (1 - (yy - base) / 40) + 0.35 * (tongues - 0.5), 0, 1)
    ref *= (np.sin(xx * 0.9 + tongues * 9) > 0.1)
    d[river] = ref[river]
    Rd = d

    # black smoke drifting up-left, sparse grain on the black plate
    smoke = np.clip(0.5 * (fbm(rng, (H, W), 45, 4) - 0.55) * np.clip((yy - 40) / 100, 0, 1), 0, 1)
    smoke[yy > base - 20] = 0
    smoke[(yy < 60)] = 0
    Kd = np.maximum(Kd, smoke)
    # river lines
    wave = ((yy > base + 6) & (yy < 262) & (((yy + 0.5 * np.sin(xx / 9)) % 9) < 1.2) & (np.sin(xx / 21 + yy) > -0.3))
    Kd[wave] = 1

    registration_marks(K, R)
    Kd[yy > 262] = 0
    Rd[yy > 262] = 0
    k_ink = grain(Kd, rng) | K.crisp()
    r_ink = grain(Rd, rng) | R.crisp()
    save(composite(k_ink, r_ink, (2, -1)), 1)


# =========================================================================== 2. The Eleven Days
def image2_eleven_days():
    rng = np.random.default_rng(SEED + 2)
    prng = random.Random(SEED + 2)
    K, R = Plate(), Plate()
    s = SS

    K.text((14, 12), "SEPTEMBER 1752", F_SANS_B, 26)
    K.text((14, 42), "England, Wales, Ireland & the colonies adopt the Gregorian calendar", F_MONO, 9)

    # the famous `cal 9 1752` layout
    cols = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
    x0, y0, cw, rh = 22, 70, 36, 36
    for i, c in enumerate(cols):
        K.text((x0 + i * cw + cw / 2, y0), c, F_MONO_B, 11, anchor="ma")
    K.dr.line([x0 * s, (y0 + 16) * s, (x0 + 7 * cw) * s, (y0 + 16) * s], fill=255, width=s)
    rows = [[None, None, 1, 2, 14, 15, 16], [17, 18, 19, 20, 21, 22, 23], [24, 25, 26, 27, 28, 29, 30]]
    for r_i, row in enumerate(rows):
        for c_i, dnum in enumerate(row):
            if dnum is None:
                continue
            K.text((x0 + c_i * cw + cw / 2, y0 + 26 + r_i * rh + rh / 2), str(dnum), F_SANS_B, 20, anchor="mm")
    # a red gap between 2 and 14: the seam where the days were cut out
    gx = x0 + 4 * cw
    R.dr.line([gx * s, (y0 + 22) * s, gx * s, (y0 + 26 + rh) * s], fill=255, width=2 * s)
    for t in range(0, 40, 6):  # stitches
        R.dr.line([(gx - 3) * s, (y0 + 24 + t) * s, (gx + 3) * s, (y0 + 27 + t) * s], fill=255, width=s)

    # the eleven lost days tumbling out of the page in red
    lost = list(range(3, 14))
    for i, dnum in enumerate(lost):
        size = prng.uniform(26, 40)
        ang = prng.uniform(-40, 40)
        f = font(F_SANS_B, int(size * s))
        txt = str(dnum)
        tw, th = f.getbbox(txt)[2:]
        tile = Image.new("L", (tw + 8 * s, th + 8 * s), 0)
        ImageDraw.Draw(tile).text((4 * s, 4 * s), txt, font=f, fill=255)
        tile = tile.rotate(ang, expand=True, resample=Image.BICUBIC)
        # scatter along a falling arc from top-right to bottom-left of the right half
        cx, cy = [(372, 22), (330, 50), (386, 78), (338, 104), (300, 132), (372, 150),
                  (326, 182), (386, 206), (300, 222), (352, 240), (260, 250)][i]
        cx += prng.uniform(-6, 6)
        cy += prng.uniform(-4, 4)
        R.img.paste(tile, (int(cx * s - tile.width / 2), int(cy * s - tile.height / 2)), tile)

    K.text((14, 212), "GIVE US OUR", F_SANS_B, 22)
    K.text((14, 236), "ELEVEN DAYS", F_SANS_B, 22)
    K.text((14, 266), "Calendar (New Style) Act 1750: Wednesday 2 September", F_MONO, 9)
    K.text((14, 277), "was followed by Thursday 14 September. Nobody died.", F_MONO, 9)

    registration_marks(K, R)
    Kd, Rd = K.density(), R.density()
    # the falling numbers get a grainy, half-vanished texture
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fade = np.clip(0.7 + 0.6 * fbm(rng, (H, W), 30, 3), 0, 1)
    Rd = np.where(Rd > 0.5, Rd * fade, 0)
    k_ink = K.crisp()
    r_ink = grain(Rd, rng, jitter=0.6) | (R.crisp() & (Rd == 0)) | (R.density() > 0.5) & (fade > 0.85)
    save(composite(k_ink, r_ink, (-2, 2)), 2)


# =========================================================================== 3. Moon & Pleiades
def image3_moon_pleiades():
    rng = np.random.default_rng(SEED + 3)
    K, R = Plate(), Plate()
    s = SS

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy, rad = 138, 158, 108
    dx, dy = (xx - cx) / rad, (yy - cy) / rad
    rr = dx * dx + dy * dy
    inside = rr < 1
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    # waning gibbous (~62 %): sunlit side to the left (east) as seen from the north
    phase = 0.62
    lx = -math.cos(math.acos(2 * phase - 1))  # direction of sun in the moon's x
    light = np.clip(dx * (-lx) * 0 + (-dx) * 0.0 + (dx * (-1) * 0.0) + 0, 0, 1)  # placeholder
    # terminator: illuminate points whose x is left of an ellipse edge
    term_x = -np.sqrt(np.clip(1 - dy * dy, 0, 1)) * (2 * phase - 1) * -1  # ellipse offset
    lit = dx < term_x
    # lambert-ish shading with the sun to the left
    lam = np.clip((-dx) * 0.55 + z * 0.8, 0, 1)
    bright = np.where(lit, 0.28 + 0.72 * lam, 0.0)
    # maria (approximate, near-side, north up, east left)
    maria = [(-0.28, -0.32, 0.30, 0.24, -10), (0.05, -0.36, 0.22, 0.16, 0), (0.18, -0.02, 0.22, 0.20, 0),
             (0.55, -0.14, 0.14, 0.10, 0), (0.30, 0.18, 0.15, 0.17, 0), (-0.55, 0.02, 0.30, 0.42, 0),
             (-0.22, 0.28, 0.16, 0.12, 0), (0.10, 0.50, 0.11, 0.08, 0)]
    mar = np.zeros_like(bright)
    for mx, my, ma, mb, ang in maria:
        a = math.radians(ang)
        ux = (dx - mx) * math.cos(a) + (dy - my) * math.sin(a)
        uy = -(dx - mx) * math.sin(a) + (dy - my) * math.cos(a)
        e = (ux / ma) ** 2 + (uy / mb) ** 2
        mar = np.maximum(mar, np.clip(1.3 - e, 0, 1) * 0.35)
    craters = fbm(rng, (H, W), 14, 3)
    bright = bright * (1 - mar) - 0.08 * (craters - 0.5)
    Kd = np.where(inside, 1 - np.clip(bright, 0, 1), 0)
    Kd[inside & ~lit] = 0.93
    k_ink = screen(Kd, cell=4.6, angle=45)
    # crisp limb
    limb = (rr > 0.965) & (rr < 1.0)
    k_ink |= limb

    # Pleiades in red: positions in arcmin relative to Alcyone (north up, east left)
    stars = [("Alcyone", 0, 0, 2.9), ("Atlas", -23, -3, 3.6), ("Pleione", -23, 2, 5.0), ("Merope", 16, -9, 4.1),
             ("Electra", 36, 1, 3.7), ("Maia", 23, 16, 3.9), ("Taygeta", 31, 22, 4.3), ("Celaeno", 37, 11, 5.4),
             ("Asterope", 22, 27, 5.8)]
    pcx, pcy, sc = 318, 96, 1.55
    Rd = np.zeros((H, W), np.float32)
    for name, ex, ny, mag in stars:
        px, py = pcx + ex * sc, pcy - ny * sc
        r_core = 1.6 + (6.0 - mag) * 1.1
        core = ((xx - px) ** 2 + (yy - py) ** 2) < r_core ** 2
        halo = np.exp(-((xx - px) ** 2 + (yy - py) ** 2) / (2 * (r_core * 2.6) ** 2)) * 0.7
        Rd = np.maximum(Rd, halo)
        Rd[core] = 1
        if name == "Alcyone":
            K.text((px + 3, py + 12), name, F_MONO, 7, anchor="la")
    # reflection nebula: soft red grain around Merope and Maia
    neb = np.exp(-((xx - (pcx + 16 * sc)) ** 2 + (yy - (pcy + 9 * sc)) ** 2) / (2 * 22 ** 2)) * 0.28
    neb += np.exp(-((xx - (pcx + 23 * sc)) ** 2 + (yy - (pcy - 16 * sc)) ** 2) / (2 * 16 ** 2)) * 0.2
    Rd = np.maximum(Rd, neb * (0.6 + 0.8 * fbm(rng, (H, W), 10, 2)))

    K.text((252, 178), "MOON &", F_SANS_B, 30)
    K.text((252, 208), "PLEIADES", F_SANS_B, 30)
    K.text((254, 246), "before dawn, Thu 3 Sep 2026", F_MONO, 9)
    K.text((254, 257), "waning gibbous, 62 % lit,", F_MONO, 9)
    K.text((254, 268), "passing the Seven Sisters", F_MONO, 9)
    R.text((254, 281), "look east, high, after 1am", F_MONO_B, 9)
    registration_marks(K, R, x=W - 14, y=14)
    k_ink |= K.crisp()
    r_ink = grain(Rd, rng, jitter=0.5) | R.crisp()
    save(composite(k_ink, r_ink, (2, 1)), 3)


# =========================================================================== 4. Gray–Scott
def image4_gray_scott():
    rng = np.random.default_rng(SEED + 4)
    K, R = Plate(), Plate()
    s = SS
    F, k = 0.0545, 0.062  # coral
    Du, Dv = 0.16, 0.08
    h, w = H, W
    U = np.ones((h, w), np.float32)
    V = np.zeros((h, w), np.float32)
    for _ in range(9):
        y, x = rng.integers(20, h - 20), rng.integers(20, w - 20)
        r = rng.integers(3, 7)
        V[y - r:y + r, x - r:x + r] = 1.0
        U[y - r:y + r, x - r:x + r] = 0.5
    V += 0.02 * rng.random((h, w), dtype=np.float32)

    def lap(a):
        return (np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1) - 4 * a)

    for _ in range(6000):
        uvv = U * V * V
        U += Du * lap(U) - uvv + F * (1 - U)
        V += Dv * lap(V) + uvv - (F + k) * V

    Vn = (V - V.min()) / (V.max() - V.min() + 1e-9)
    # black plate: the outline of the coral (gradient magnitude), red plate: the body
    gy, gx = np.gradient(Vn)
    edge = np.sqrt(gx * gx + gy * gy)
    edge = edge / (edge.max() + 1e-9)
    Kd = np.clip(edge * 2.8 - 0.3, 0, 1)
    Rd = np.clip((Vn - 0.12) * 1.8, 0, 1) ** 0.8
    # print margin
    m = 14
    yy, xx = np.mgrid[0:H, 0:W]
    frame = (xx < m) | (xx >= W - m) | (yy < m) | (yy >= H - 34)
    Rd[frame | (xx >= W - m - 2) | (yy >= H - 35)] = 0
    Kd[(xx < m + 3) | (xx >= W - m - 3) | (yy < m + 3) | (yy >= H - 37)] = 0

    K.text((m, 270), "GRAY–SCOTT", F_SANS_B, 16)
    K.text((m + 108, 268), "∂u/∂t = Du∇²u − uv² + F(1−u)", F_MONO, 9)
    K.text((m + 108, 279), "∂v/∂t = Dv∇²v + uv² − (F+k)v", F_MONO, 9)
    R.text((m + 274, 268), f"F {F} k {k}", F_MONO_B, 9)
    R.text((m + 274, 279), "coral, 6000 steps", F_MONO_B, 9)
    registration_marks(K, R, x=W - 20, y=20)
    k_ink = grain(Kd, rng, jitter=0.25) | K.crisp()
    r_ink = screen(Rd, cell=3.6, angle=30) | R.crisp()
    save(composite(k_ink, r_ink, (2, 1)), 4)


# =========================================================================== 5. 137.5°
def image5_phyllotaxis():
    rng = np.random.default_rng(SEED + 5)
    prng = random.Random(SEED + 5)
    K, R = Plate(), Plate()
    s = SS
    cx, cy = 262, 158
    golden = math.radians(137.507764)

    # petals (34 of them, a Fibonacci number) on the red plate with black veins
    npet = 34
    for i in range(npet):
        a = i * 2 * math.pi / npet + prng.uniform(-0.04, 0.04)
        L = prng.uniform(118, 140)
        wdt = prng.uniform(9, 13)
        pts = []
        for t in np.linspace(0, 1, 18):
            rad = 82 + L * t
            wid = wdt * math.sin(math.pi * t) * (1 - 0.3 * t)
            pts.append((cx + rad * math.cos(a) - wid * math.sin(a), cy + rad * math.sin(a) + wid * math.cos(a)))
        for t in np.linspace(1, 0, 18):
            rad = 82 + L * t
            wid = wdt * math.sin(math.pi * t) * (1 - 0.3 * t)
            pts.append((cx + rad * math.cos(a) + wid * math.sin(a), cy + rad * math.sin(a) - wid * math.cos(a)))
        R.dr.polygon([(p[0] * s, p[1] * s) for p in pts], fill=255)
        K.dr.line([(p[0] * s, p[1] * s) for p in pts] + [(pts[0][0] * s, pts[0][1] * s)], fill=255, width=s)
        K.dr.line([(cx + 84 * math.cos(a)) * s, (cy + 84 * math.sin(a)) * s,
                   (cx + (82 + L * 0.75) * math.cos(a)) * s, (cy + (82 + L * 0.75) * math.sin(a)) * s], fill=255, width=s)

    # disc: black, with florets punched out — Vogel's model
    K.dr.ellipse([(cx - 90) * s, (cy - 90) * s, (cx + 90) * s, (cy + 90) * s], fill=255)
    disc = Image.new("L", (W * s, H * s), 0)
    dd = ImageDraw.Draw(disc)
    n = 0
    c = 3.05
    while True:
        r = c * math.sqrt(n)
        if r > 86:
            break
        th = n * golden
        px, py = cx + r * math.cos(th), cy + r * math.sin(th)
        fr = 0.9 + 1.55 * (r / 86) ** 0.9
        dd.ellipse([(px - fr) * s, (py - fr) * s, (px + fr) * s, (py + fr) * s], fill=255)
        n += 1
    # florets: white holes in the black disc in the centre, red dots outward
    K.img = Image.composite(Image.new("L", K.img.size, 0), K.img, disc)
    K.dr = ImageDraw.Draw(K.img)
    ring = Image.new("L", (W * s, H * s), 0)
    ImageDraw.Draw(ring).ellipse([(cx - 90) * s, (cy - 90) * s, (cx + 90) * s, (cy + 90) * s], fill=255)
    inner = Image.new("L", (W * s, H * s), 0)
    ImageDraw.Draw(inner).ellipse([(cx - 46) * s, (cy - 46) * s, (cx + 46) * s, (cy + 46) * s], fill=255)
    outer_florets = Image.composite(disc, Image.new("L", disc.size, 0), ring)
    outer_florets = Image.composite(Image.new("L", disc.size, 0), outer_florets, inner)
    R.img.paste(outer_florets, (0, 0), outer_florets)

    # knock out a white label box for the type (a printer's caption panel) and a caption strip
    K.dr.rectangle([0, 262 * s, W * s, H * s], fill=0)
    R.dr.rectangle([0, 262 * s, W * s, H * s], fill=0)
    box = (8, 8, 156, 184)
    K.dr.rectangle([box[0] * s, box[1] * s, box[2] * s, box[3] * s], fill=0)
    R.dr.rectangle([box[0] * s, box[1] * s, box[2] * s, box[3] * s], fill=0)
    K.dr.rectangle([box[0] * s, box[1] * s, box[2] * s, box[3] * s], outline=255, width=s)
    K.text((14, 14), "137.5°", F_SANS_B, 44)
    K.text((16, 62), "THE GOLDEN ANGLE", F_MONO_B, 10)
    lines = ["every floret sits 137.508°", "round from the last one,", f"r = c·√n   ({n} florets)",
             "so no two ever line up", "and the seed head packs", "itself without a plan."]
    for i, ln in enumerate(lines):
        K.text((16, 84 + i * 12), ln, F_MONO, 9)
    R.text((16, 166), "Vogel, 1979", F_MONO_B, 9)
    K.text((14, 268), "sunflowers are in season · 2 Sep 2026", F_MONO, 9)
    registration_marks(K, R)
    Kd, Rd = K.density(), R.density()
    # petals get a light halftone toward their tips so they aren't a flat red slab
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    fall = np.clip(1.6 - (dist - 88) / 90, 0.45, 1)
    Rd_pet = np.where((dist > 88) & (Rd > 0.5), Rd * fall, Rd)
    k_ink = K.crisp()
    inbox = (xx >= box[0]) & (xx <= box[2]) & (yy >= box[1]) & (yy <= box[3])
    petal = (dist > 88) & (Rd > 0.5) & ~inbox & (yy < 262)
    r_ink = (petal & screen(Rd_pet, cell=3.2, angle=15)) | (R.crisp() & ~petal)
    save(composite(k_ink, r_ink, (2, 2)), 5)


if __name__ == "__main__":
    image1_pudding_lane()
    image2_eleven_days()
    image3_moon_pleiades()
    image4_gray_scott()
    image5_phyllotaxis()
    shutil.copy(__file__, f"archive/{DATE}/generate.py")
