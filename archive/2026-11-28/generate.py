#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-11-28.

Five 400x300 images, exactly three colours (white / black / red).
House rule from today on: NO antialiasing anywhere. Everything is drawn
straight into a 3-entry palette image, so every pixel is a decision.

  1  CP 1919          the first pulsar, found 28 Nov 1967
  2  Mar Pacifico     Magellan leaves the strait, 28 Nov 1520 (portolan)
  3  Fearful Symmetry Blake b. 28 Nov 1757 (mirrored reaction-diffusion)
  4  Sandpile         identity element of the abelian sandpile group
  5  Day 332          the year as a grid of 365 squares

Usage: python3 generate.py [outdir ...]
"""
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
WH, BK, RD = 0, 1, 2
PALETTE = [255, 255, 255, 0, 0, 0, 255, 0, 0] + [0, 0, 0] * 253

UNI = "/usr/share/fonts/opentype/unifont/unifont.otf"
INTER_BLACK = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def canvas(bg=WH):
    im = Image.new("P", (W, H), bg)
    im.putpalette(PALETTE)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"  # no antialiasing on text
    return im, d


def from_array(a):
    im = Image.fromarray(a.astype(np.uint8), "P")
    im.putpalette(PALETTE)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    return im, d


def spaced(d, xy, s, f, fill, gap=2, anchor="l"):
    """Letter-spaced text. anchor l / m / r horizontally."""
    widths = [d.textlength(c, font=f) for c in s]
    total = sum(widths) + gap * (len(s) - 1)
    x, y = xy
    if anchor == "m":
        x -= total / 2
    elif anchor == "r":
        x -= total
    for c, w in zip(s, widths):
        d.text((round(x), y), c, font=f, fill=fill)
        x += w + gap
    return total


# ---------------------------------------------------------------- 1. CP 1919
def pulsar():
    rng = np.random.default_rng(19671128)
    im, d = canvas(BK)
    x0, x1 = 62, 338
    n = x1 - x0
    xs = np.arange(n)
    rows = 59  # one trace for every year since
    top, bot = 62, 256
    red_row = rows - 1  # the newest trace, nearest the viewer
    for r in range(rows):
        yb = top + (bot - top) * r / (rows - 1)
        t = (xs - n / 2) / n
        y = rng.normal(0, 0.55, n)
        y = np.convolve(y, np.ones(3) / 3, "same")
        amp = rng.gamma(2.2, 7.0) if r != red_row else 30.0
        for _ in range(rng.integers(2, 6)):
            c = rng.normal(0, 0.045)
            w = rng.uniform(0.008, 0.03)
            y += amp * rng.uniform(0.3, 1.0) * np.exp(-((t - c) ** 2) / (2 * w * w))
        env = np.exp(-(t ** 2) / (2 * 0.11 ** 2))
        y += np.abs(rng.normal(0, 1.6, n)) * env
        y *= np.minimum(1, np.minimum(xs, n - 1 - xs) / 12)
        pts = [(x0 + i, int(round(yb - max(v, -1)))) for i, v in enumerate(y)]
        d.polygon(pts + [(x1, int(yb) + 3), (x0, int(yb) + 3)], fill=BK)
        d.line(pts, fill=RD if r == red_row else WH, width=1)
    f = font(UNI, 16)
    spaced(d, (W // 2, 14), "CP 1919", f, WH, gap=6, anchor="m")
    d.text((62, 272), "28 NOV 1967", font=f, fill=WH)
    d.text((338, 272), "P=1.3373 s", font=f, fill=RD, anchor="ra")
    return im


# ------------------------------------------------------------ 2. Mar Pacifico
def vnoise(shape, cell, rng):
    """Smooth value noise by bilinear upsampling of a random lattice."""
    h, w = shape
    gh, gw = h // cell + 2, w // cell + 2
    g = rng.random((gh, gw))
    yy, xx = np.mgrid[0:h, 0:w]
    fy, fx = yy / cell, xx / cell
    iy, ix = fy.astype(int), fx.astype(int)
    ty, tx = fy - iy, fx - ix
    ty, tx = ty * ty * (3 - 2 * ty), tx * tx * (3 - 2 * tx)
    return (g[iy, ix] * (1 - ty) * (1 - tx) + g[iy, ix + 1] * (1 - ty) * tx
            + g[iy + 1, ix] * ty * (1 - tx) + g[iy + 1, ix + 1] * ty * tx)


def erode(m, k=1):
    for _ in range(k):
        p = np.pad(m, 1, constant_values=True)
        m = p[1:-1, 1:-1] & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return m


SHIP = [
    "......#......",
    "......##.....",
    "..#...#......",
    "..##.###.....",
    "..#.#####.#..",
    ".###.###..##.",
    "#####.#..###.",
    "..#...#...#..",
    "#############",
    ".###########.",
    "..#########..",
]


def portolan():
    rng = np.random.default_rng(15201128)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    nz = (vnoise((H, W), 48, rng) - .5) * 1.0 + (vnoise((H, W), 16, rng) - .5) * .5 \
        + (vnoise((H, W), 6, rng) - .5) * .22
    # land lies to the east; the coast leans, and frays into islands westward
    coast = 205 + 0.22 * (yy - 150) + 40 * np.sin(yy / 47.0)
    field = (xx - coast) / 85.0 + nz * 1.25
    land = field > 0.05
    # the strait: a crooked channel from the east edge to the open sea
    path = [(400, 96), (352, 108), (318, 150), (296, 196), (262, 208), (226, 176), (180, 150)]
    dist = np.full((H, W), 1e9)
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        vx, vy = bx - ax, by - ay
        t = np.clip(((xx - ax) * vx + (yy - ay) * vy) / (vx * vx + vy * vy), 0, 1)
        dist = np.minimum(dist, np.hypot(xx - ax - t * vx, yy - ay - t * vy))
    land &= dist > 7 + 5 * vnoise((H, W), 20, rng)
    im, d = canvas(WH)
    # wind-rose network: 16 nodes on a hidden circle, plus the centre
    cx, cy, R = 118, 150, 136
    nodes = [(cx + R * math.sin(k * math.pi / 8), cy - R * math.cos(k * math.pi / 8)) for k in range(16)]

    def ray(p, ang, col):
        L = 900
        d.line([(p[0] - L * math.sin(ang), p[1] + L * math.cos(ang)),
                (p[0] + L * math.sin(ang), p[1] - L * math.cos(ang))], fill=col)
    for k in range(16):       # 32 winds through the centre
        ray((cx, cy), k * math.pi / 16, RD if k % 2 else BK)
    for i in range(16):       # chords between nodes
        for j in range(i + 1, 16):
            s = (i + j) % 16  # chord direction class
            if (j - i) in (8,):
                continue
            col = BK if s % 4 == 0 else (RD if s % 2 == 0 else None)
            if col is None or (j - i) % 2:
                continue
            d.line([nodes[i], nodes[j]], fill=col)
    a = np.array(im)
    inner = erode(land, 2)
    a[land] = BK                      # coastline, 2px
    a[inner] = WH
    band = erode(land, 4) & ~erode(land, 7)
    a[band & (((xx + yy) % 2) == 0)] = RD   # stippled red wash inside the coast
    im, d = from_array(a)
    # compass rose at the centre
    for k in range(8):
        ang = k * math.pi / 4
        L = 30 if k % 2 == 0 else 17
        tip = (cx + L * math.sin(ang), cy - L * math.cos(ang))
        for sgn, col in ((-1, BK), (1, RD if k % 2 == 0 else WH)):
            b = ang + sgn * math.pi / 8
            side = (cx + 6 * math.sin(b), cy - 6 * math.cos(b))
            d.polygon([(cx, cy), side, tip], fill=col, outline=BK)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=WH, outline=BK)
    # three ships, westbound out of the strait mouth
    for (sx, sy) in ((152, 104), (120, 176), (62, 206)):
        for r, row in enumerate(SHIP):
            for c, ch in enumerate(row):
                px, py = sx + 2 * (len(row) - 1 - c), sy + 2 * r   # mirrored: sailing west
                d.rectangle([px, py, px + 1, py + 1], fill=BK if ch == "#" else WH)
        d.line([(sx - 6, sy + 23), (sx + 2, sy + 23)], fill=BK)
        d.line([(sx + 8, sy + 25), (sx + 30, sy + 25)], fill=BK)
        d.rectangle([sx + 8, sy - 3, sx + 11, sy - 2], fill=RD)   # pennant
    f = font(UNI, 16)

    def label(xy, s, col, gap, anchor="l"):
        w = spaced(d, xy, s, f, col, gap, anchor)
        return w
    # knock out a white plate behind the lettering so the rhumbs don't cut it
    for (xy, s, col, gap) in (((14, 12), "MAR PACIFICO", BK, 5), ((14, 272), "28·XI·1520", RD, 2)):
        tw = sum(d.textlength(c, font=f) for c in s) + gap * (len(s) - 1)
        d.rectangle([xy[0] - 4, xy[1] - 1, xy[0] + tw + 3, xy[1] + 16], fill=WH)
        spaced(d, xy, s, f, col, gap)
    d.rectangle([14, 31, 14 + 150, 32], fill=BK)
    d.text((322, 40), "PATAGONIA", font=f, fill=BK)
    d.text((312, 236), "TIERRA", font=f, fill=BK)
    d.text((312, 252), "DEL FUEGO", font=f, fill=RD)
    # scale bar
    for k in range(6):
        d.rectangle([300 + k * 14, 282, 313 + k * 14, 286], fill=BK if k % 2 == 0 else WH, outline=BK)
    return im


# -------------------------------------------------------- 3. Fearful Symmetry
def tyger():
    rng = np.random.default_rng(17571128)
    h, w = 300, 200
    U = np.ones((h, w))
    V = np.zeros((h, w))
    V += (rng.random((h, w)) < 0.08) * 0.5
    U -= V * 0.5
    Du, Dv = 0.16, 0.08
    yy, xx = np.mgrid[0:h, 0:w]
    # feed/kill drift across the picture: mazes near the spine, spots at the rim
    g = np.clip(np.hypot((xx - 200) / 200, (yy - 140) / 190), 0, 1)
    F = 0.030 + 0.012 * g
    K = 0.0570 + 0.0045 * g

    def lap(A):
        P = np.pad(A, 1, mode="reflect")
        return (P[:-2, 1:-1] + P[2:, 1:-1] + P[1:-1, :-2] + P[1:-1, 2:]) * 0.2 \
            + (P[:-2, :-2] + P[:-2, 2:] + P[2:, :-2] + P[2:, 2:]) * 0.05 - A
    for _ in range(9000):
        uvv = U * V * V
        U += Du * lap(U) - uvv + F * (1 - U)
        V += Dv * lap(V) + uvv - (F + K) * V
    S = V > 0.2
    S = np.concatenate([S, S[:, ::-1]], axis=1)          # the symmetry
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    # the burning part: a flame-shaped field of red, mirrored like everything else
    nr = np.random.default_rng(5)
    nzh = vnoise((H, W // 2), 30, nr)
    nz = np.concatenate([nzh, nzh[:, ::-1]], axis=1)
    rr = np.hypot((xx - 199.5) / 150, (yy - 150) / 128)
    fire = rr + (nz - .5) * .55 < 0.80
    a = np.where(S, BK, np.where(fire, RD, WH)).astype(np.uint8)
    # night outside the fire: invert, so the stripes turn white on black
    night = rr + (nz - .5) * .55 > 1.02
    a = np.where(night, np.where(S, WH, BK), a).astype(np.uint8)
    im, d = from_array(a)
    # the eyes
    for sgn in (-1, 1):
        ex, ey = 199.5 + sgn * 46, 112
        pts = []
        for k in range(40):
            t = k / 40 * 2 * math.pi
            px = 21 * math.cos(t)
            py = 9.5 * math.sin(t) * (1.0 if math.sin(t) < 0 else 0.8) - sgn * px * 0.18 * -1
            pts.append((ex + px, ey + py))
        d.polygon(pts, fill=WH, outline=BK)
        d.line(pts + pts[:1], fill=BK, width=3)
        d.ellipse([ex - 7, ey - 8, ex + 7, ey + 8], fill=RD, outline=BK)
        d.ellipse([ex - 2, ey - 7, ex + 2, ey + 7], fill=BK)
    f = font(UNI, 16)
    s = "WHAT IMMORTAL HAND OR EYE"
    tw = sum(d.textlength(c, font=f) for c in s) + 2 * (len(s) - 1)
    d.rectangle([200 - tw / 2 - 7, 272, 200 + tw / 2 + 6, 293], fill=BK)
    spaced(d, (200, 274), s, f, WH, gap=2, anchor="m")
    return im


# ---------------------------------------------------------------- 4. Sandpile
def stabilise(a):
    while True:
        t = a >> 2
        if not t.any():
            return a
        a = a & 3
        a[1:, :] += t[:-1, :]
        a[:-1, :] += t[1:, :]
        a[:, 1:] += t[:, :-1]
        a[:, :-1] += t[:, 1:]


def sandpile():
    h, w = 150, 200
    six = np.full((h, w), 6, dtype=np.int64)
    ident = stabilise(six - stabilise(six.copy()))   # identity of the sandpile group
    big = np.kron(ident, np.ones((2, 2), dtype=np.int64))
    yy, xx = np.mgrid[0:H, 0:W]
    a = np.zeros((H, W), np.uint8)
    a = np.array([BK, RD, WH, BK], np.uint8)[big]     # 0,3 grains black; 1 red; 2 white
    im, d = from_array(a)
    return im


# ----------------------------------------------------------------- 5. Day 332
def year_grid():
    import datetime as dt
    today = dt.date(2026, 11, 28)
    doy = today.timetuple().tm_yday
    total = 365
    im, d = canvas(WH)
    f = font(UNI, 16)
    cell, pitch = 9, 12
    gx, gy = 24, 12
    for m in range(1, 13):
        y = gy + (m - 1) * pitch
        d.text((8, y - 4), "JFMAMJJASOND"[m - 1], font=f, fill=RD if m == today.month else BK)
        n = (dt.date(2026 + (m == 12), m % 12 + 1, 1) - dt.date(2026, m, 1)).days
        for day in range(1, n + 1):
            x = gx + (day - 1) * pitch
            date = dt.date(2026, m, day)
            box = [x, y, x + cell - 1, y + cell - 1]
            if date < today:
                if date.weekday() >= 5:
                    d.rectangle(box, fill=BK)
                else:
                    d.rectangle(box, fill=BK)
                    d.rectangle([x + 3, y + 3, x + 5, y + 5], fill=WH)
            elif date == today:
                d.rectangle([x - 1, y - 1, x + cell, y + cell], fill=RD)
            else:
                if date.weekday() >= 5:
                    d.rectangle(box, outline=BK)
                else:
                    d.rectangle([x + 3, y + 3, x + 5, y + 5], fill=BK)
    # the big number
    fb = font(INTER_BLACK, 124)
    d.text((14, 292), str(doy), font=fb, fill=BK, anchor="ls")
    x = 286
    d.text((x, 172), "SATURDAY", font=f, fill=BK)
    d.text((x, 190), "28 NOV 2026", font=f, fill=BK)
    d.rectangle([x, 211, 386, 212], fill=BK)
    d.text((x, 218), f"{total - doy} REMAIN", font=f, fill=RD)
    # the moon tonight: waning gibbous, ~4 days past full (24 Nov)
    age = 4.0 / 29.53 * 2 * math.pi
    mx, my, mr = x + 16, 264, 16
    for py in range(-mr, mr + 1):
        for px in range(-mr, mr + 1):
            if px * px + py * py <= mr * mr:
                half = math.sqrt(mr * mr - py * py)
                # waning: darkness creeps in from the right (N. hemisphere)
                lit = px <= half * math.cos(age)
                d.point((mx + px, my + py), fill=WH if lit else BK)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=BK)
    d.text((x + 40, 248), "MOON 83%", font=f, fill=BK)
    d.text((x + 40, 264), "WANING", font=f, fill=BK)
    return im


def main():
    outs = sys.argv[1:] or ["."]
    pics = [pulsar(), portolan(), tyger(), sandpile(), year_grid()]
    for o in outs:
        os.makedirs(o, exist_ok=True)
        for i, im in enumerate(pics, 1):
            assert im.size == (W, H) and set(np.unique(np.array(im))) <= {0, 1, 2}
            im.save(os.path.join(o, f"{i}.png"), optimize=True)


if __name__ == "__main__":
    main()
