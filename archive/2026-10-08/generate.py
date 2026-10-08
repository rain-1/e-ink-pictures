#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-08 (Kanro, "cold dew").

Five 400x300 images in exactly three colours (white, black, red).

1. geese    — 鴻雁来, the wild geese return (first micro-season of Kanro)
2. tally    — Draconids: "then counting became impossible" (1933 storm)
3. fires    — 8 Oct 1871: Chicago and Peshtigo, the same night
4. dunes    — Frank Herbert b. 8 Oct 1920; dunes grown with Werner's slab model
5. dew      — 寒露, an orb web beaded by the Plateau–Rayleigh instability

Usage: python3 generate.py OUTDIR
"""

import math
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
DATE = "08·X·2026"

INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def inter(weight, size):
    return font(INTER.format(weight), size)


_pal = Image.new("P", (1, 1))
_pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)


def finalize_dither(img):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img.convert("RGB").quantize(palette=_pal, dither=Image.Dither.FLOYDSTEINBERG)


def finalize_hard(img, thr=128):
    """Downscale then snap each pixel to the nearest ink without dithering."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    a = np.asarray(img.convert("RGB")).astype(np.int32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (299 * r + 587 * g + 114 * b) // 1000
    redness = r - (g + b) // 2
    idx = np.where(lum >= thr, 0, 1).astype(np.uint8)
    idx[redness > 90] = 2
    out = Image.fromarray(idx, "P")
    out.putpalette(_pal.getpalette())
    return out


def colophon(img, n, ink=BLACK, paper=WHITE):
    """My signature: a small red square, the date, and n/5, bottom-right."""
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    f = font(MONO, 9)
    txt = f"{DATE} {n}/5"
    tw = d.textlength(txt, font=f)
    x, y = W - 6 - tw, H - 13
    d.rectangle([x - 8, y + 3, x - 4, y + 7], fill=RED)
    d.text((x, y), txt, font=f, fill=ink)
    return img


def overlay_text(pimg, fn):
    """Draw crisp 1x text on top of a finished palette image."""
    rgb = pimg.convert("RGB")
    d = ImageDraw.Draw(rgb)
    d.fontmode = "1"  # crisp, unantialiased glyphs survive the 3-ink snap
    fn(rgb, d)
    return finalize_hard(rgb)


# ------------------------------------------------------------------ 1. geese
def goose(d, x, y, s, phase, fill):
    """A small goose silhouette flying left. s = scale (px), phase = wing beat 0..1."""
    # body
    d.ellipse([x - 3.2 * s, y - 0.8 * s, x + 2.2 * s, y + 0.8 * s], fill=fill)
    # neck + head stretched forward
    d.line([(x - 2.5 * s, y), (x - 6.0 * s, y - 0.4 * s)], fill=fill, width=max(1, int(0.75 * s)))
    d.ellipse([x - 6.9 * s, y - 1.0 * s, x - 5.5 * s, y + 0.2 * s], fill=fill)
    # tail
    d.polygon([(x + 2.0 * s, y - 0.5 * s), (x + 3.6 * s, y - 0.1 * s), (x + 2.0 * s, y + 0.6 * s)], fill=fill)
    # wings — one near, one far; tip height swings with the beat
    lift = math.cos(phase * 2 * math.pi)
    for side, k in ((1, 1.0), (-1, 0.7)):
        tipx = x + 0.8 * s
        tipy = y - side * 0 - 5.5 * s * lift * k
        d.polygon([(x - 1.6 * s, y - 0.2 * s), (tipx - 1.2 * s, (y + tipy) / 2 - 0.4 * s),
                   (tipx, tipy), (x + 0.6 * s, y)], fill=fill)


def image_geese():
    rng = random.Random(1008)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)

    # dawn sky: white above, warming to a pale grey band at the horizon
    hz = 228 * s
    for y in range(hz):
        t = max(0.0, (y / hz - 0.55) / 0.45) ** 2
        v = int(255 - 60 * t)
        d.line([(0, y), (W * s, y)], fill=(v, v, v))

    # waning crescent (1%) low in the east — red, a nail-paring
    mx, my, mr = 64 * s, 150 * s, 11 * s
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=RED)
    off = 0.32 * mr
    lv = int(255 - 60 * max(0.0, (my / hz - 0.55) / 0.45) ** 2)
    d.ellipse([mx - mr + off, my - mr - off * 0.4, mx + mr + off, my + mr - off * 0.4], fill=(lv, lv, lv))

    # drained paddy: flat black ground with a few water lines catching the sky
    d.rectangle([0, hz, W * s, H * s], fill=BLACK)
    for i in range(6):
        yy = hz + (6 + i * i * 1.6) * s
        x0 = rng.uniform(0, 260) * s
        d.line([(x0, yy), (x0 + rng.uniform(40, 150) * s, yy)], fill=(150, 150, 150), width=s)
    # susuki grass plumes leaning in the wind
    for i in range(46):
        bx = rng.uniform(-10, 410) * s
        hgt = rng.uniform(14, 40) * s
        lean = rng.uniform(0.25, 0.5)
        pts = []
        for k in range(12):
            t = k / 11
            pts.append((bx + lean * hgt * t * t, hz + 4 * s - hgt * t))
        d.line(pts, fill=BLACK, width=max(1, int(0.9 * s)))
        tx, ty = pts[-1]
        for j in range(5):  # plume
            a = -0.4 + j * 0.22
            d.line([(tx, ty), (tx + 7 * s * math.cos(a), ty + 7 * s * math.sin(a) + 2 * s)],
                   fill=BLACK, width=max(1, int(0.6 * s)))

    # the skein: an uneven V flying west (left), plus a fainter distant one
    def skein(cx, cy, n, gap, scale, ink, spread=0.55):
        birds = [(cx, cy)]
        for i in range(1, n):
            arm = 1 if i % 2 else -1
            k = (i + 1) // 2
            if arm == -1:
                k += 0.4  # arms of unequal length, as real skeins are
            bx = cx + k * gap
            by = cy + arm * k * gap * spread + rng.uniform(-1.5, 1.5) * s
            birds.append((bx + rng.uniform(-2, 2) * s, by))
        for i, (bx, by) in enumerate(birds):
            goose(d, bx, by, scale, (i * 0.17 + rng.random() * 0.2) % 1, ink)

    skein(118 * s, 104 * s, 13, 21 * s, 1.9 * s, BLACK)
    skein(270 * s, 112 * s, 7, 11 * s, 0.85 * s, (90, 90, 90), spread=0.42)

    p = finalize_dither(img)

    def text(rgb, d):
        fj = font(JP, 30)
        x = 356
        for i, ch in enumerate("鴻雁来"):
            d.text((x, 16 + i * 36), ch, font=fj, fill=BLACK)
        d.line([(346, 18), (346, 118)], fill=RED, width=1)
        fi = font(SERIF_I, 13)
        d.text((14, 12), "the wild geese return", font=fi, fill=BLACK)
        f = inter("Medium", 9)
        d.text((14, 29), "KŌGAN KITARU · 8–12 OCTOBER", font=f, fill=BLACK)
        d.text((14, 41), "first kō of Kanro 寒露, cold dew", font=font(JP, 9), fill=BLACK)
        f2 = inter("Regular", 8)
        d.text((14, H - 14), "moon 1%, waning — new on the 10th", font=f2, fill=WHITE)
        colophon(rgb, 1, ink=WHITE)

    return overlay_text(p, text)


# ------------------------------------------------------------------ 2. tally
def image_tally():
    rng = random.Random(1933)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    d = ImageDraw.Draw(img)

    rad = np.array([352.0, 46.0]) * s  # the radiant, in Draco's head

    # 40 orderly groups of five = 200 tallies, then disorder takes over
    marks = []
    x0, y0 = 16 * s, 64 * s
    gx, gy = 30 * s, 26 * s
    cols = 8
    for g in range(40):
        cx = x0 + (g % cols) * gx
        cy = y0 + (g // cols) * gy
        for k in range(5):
            marks.append((g, k, cx, cy))

    N = len(marks)
    for i, (g, k, cx, cy) in enumerate(marks):
        t = i / (N - 1)
        chaos = max(0.0, (t - 0.25) / 0.75) ** 1.6  # 0 for the first quarter
        if k < 4:
            p0 = np.array([cx + k * 5 * s, cy])
            p1 = np.array([cx + k * 5 * s, cy + 16 * s])
        else:
            p0 = np.array([cx - 3 * s, cy + 13 * s])
            p1 = np.array([cx + 19 * s, cy + 3 * s])
        mid = (p0 + p1) / 2
        # the meteor this tally becomes: aligned away from the radiant, longer
        v = mid - rad
        dist = np.linalg.norm(v)
        u = v / dist
        L = (14 + chaos * rng.uniform(20, 70)) * s
        jitter = np.array([rng.gauss(0, 1), rng.gauss(0, 1)]) * chaos * 18 * s
        m = mid + jitter
        q0 = m - u * L * 0.5
        q1 = m + u * L * 0.5
        a0 = p0 * (1 - chaos) + q0 * chaos
        a1 = p1 * (1 - chaos) + q1 * chaos
        # tapered streak: thin at the head (toward radiant), thicker at the tail
        steps = 10
        for j in range(steps):
            f0, f1 = j / steps, (j + 1) / steps
            w = int(round((1.2 + 1.6 * (1 - chaos) + chaos * 2.4 * f1) * s / 1.6))
            d.line([tuple(a0 + (a1 - a0) * f0), tuple(a0 + (a1 - a0) * f1)], fill=WHITE, width=max(1, w))

    # beyond counting: pure streaks radiating from Draco
    for i in range(170):
        ang = rng.uniform(math.radians(95), math.radians(260))
        r0 = rng.uniform(30, 420) * s
        L = rng.uniform(10, 60) * s
        p0 = rad + r0 * np.array([math.cos(ang), math.sin(ang)])
        p1 = rad + (r0 + L) * np.array([math.cos(ang), math.sin(ang)])
        if not (0 < p0[0] < W * s and 0 < p1[0] < W * s and 66 * s < min(p0[1], p1[1]) and max(p0[1], p1[1]) < 258 * s):
            continue
        d.line([tuple(p0), tuple(p1)], fill=(200, 200, 200), width=s)

    # the radiant: a red reticle
    rx, ry = rad
    d.ellipse([rx - 6 * s, ry - 6 * s, rx + 6 * s, ry + 6 * s], outline=RED, width=s)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        d.line([(rx + dx * 9 * s, ry + dy * 9 * s), (rx + dx * 15 * s, ry + dy * 15 * s)], fill=RED, width=s)

    p = finalize_hard(img, thr=110)

    def text(rgb, d):
        d.rectangle([0, 0, W, 50], fill=BLACK)
        fi = font(SERIF_I, 15)
        d.text((14, 10), "“I counted 200 meteors in two minutes,", font=fi, fill=WHITE)
        d.text((14, 28), "and then counting became impossible.”", font=fi, fill=WHITE)
        d.rectangle([0, 262, W, H], fill=BLACK)
        f = inter("Medium", 9)
        d.text((14, 266), "REV. W.F.A. ELLISON · DRACONID STORM · 9 OCT 1933", font=f, fill=WHITE)
        f2 = inter("Regular", 8)
        d.text((14, 280), "Tonight: Draconids peak, moon 1% — expect ~10/hr, not 10,000", font=f2, fill=RED)
        d.text((340, 66), "DRACO", font=inter("Medium", 8), fill=RED)
        colophon(rgb, 2, ink=WHITE)

    return overlay_text(p, text)


# ------------------------------------------------------------------ 3. fires
def image_fires():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"

    d.text((14, 10), "8 OCTOBER 1871", font=inter("Bold", 22), fill=BLACK)
    d.text((14, 36), "The same dry night, the same wind. Two fires.",
           font=font(SERIF_I, 12), fill=BLACK)
    d.line([(14, 54), (W - 14, 54)], fill=BLACK)

    pitch, dot = 5, 3

    def block(x0, y0, cols, n_full, n_hollow, ink):
        for i in range(n_full + n_hollow):
            cx = x0 + (i % cols) * pitch
            cy = y0 + (i // cols) * pitch
            if i < n_full:
                d.rectangle([cx, cy, cx + dot - 1, cy + dot - 1], fill=ink)
            else:
                d.rectangle([cx, cy, cx + dot - 1, cy + dot - 1], outline=ink)
                d.point((cx + 1, cy + 1), fill=WHITE)
        rows = math.ceil((n_full + n_hollow) / cols)
        return y0 + rows * pitch

    # Chicago: ~300 dead
    cy0 = 92
    cx0 = 18
    yend = block(cx0, cy0, 15, 300, 0, BLACK)
    d.text((cx0, 64), "CHICAGO", font=inter("Bold", 11), fill=BLACK)
    d.text((cx0, 78), "c. 300 dead", font=inter("Regular", 9), fill=BLACK)
    d.text((cx0, yend + 4), "the one", font=font(SERIF_I, 12), fill=BLACK)
    d.text((cx0, yend + 18), "you remember", font=font(SERIF_I, 12), fill=BLACK)

    # Peshtigo: 1,152 known + ~350 believed dead
    px0 = 122
    yend2 = block(px0, cy0, 52, 1152, 350, RED)
    d.text((px0, 64), "PESHTIGO, WISCONSIN", font=inter("Bold", 11), fill=RED)
    d.text((px0, 78), "1,152 known dead  ·  ~350 more believed (hollow)", font=inter("Regular", 9), fill=BLACK)
    d.text((px0, yend2 + 4), "the one you don’t — America’s deadliest wildfire,",
           font=font(SERIF_I, 12), fill=BLACK)
    d.text((px0, yend2 + 18), "a forest 10 miles wide burned in about two hours",
           font=font(SERIF_I, 12), fill=BLACK)

    d.text((14, H - 14), "one square = one life · 155 years ago tonight",
           font=inter("Regular", 8), fill=BLACK)
    colophon(img, 3)
    return finalize_hard(img)


# ------------------------------------------------------------------ 4. dunes
def werner_dunes(nx=120, ny=90, steps=5000, seed=1920, sand=2.0):
    """Werner (1995) slab model, vectorised: many slabs hop at once each step."""
    rng = np.random.default_rng(seed)
    h = rng.poisson(sand, size=(ny, nx)).astype(np.int32)
    L = 4  # hop length
    tan_shadow = 0.6  # shadow zone slope (in slab units per cell)

    def shadow(h):
        sh = np.zeros_like(h, dtype=bool)
        for k in range(1, 18):
            sh |= (np.roll(h, k, axis=1) - k * tan_shadow) > h
        return sh

    def avalanche(h):
        for _ in range(6):
            for axis, sgn in ((1, 1), (1, -1), (0, 1), (0, -1)):
                nb = np.roll(h, -sgn, axis=axis)
                over = (h - nb) > 2
                if not over.any():
                    continue
                h = h - over
                h = h + np.roll(over, sgn, axis=axis)
        return h

    for it in range(steps):
        sh = shadow(h)
        pick = (rng.random(h.shape) < 0.03) & (h > 0) & ~sh
        h = h - pick
        carrying = pick.copy()
        for hop in range(25):
            carrying = np.roll(carrying, L, axis=1)
            # wind wobble: a little lateral drift
            if hop % 3 == 2:
                carrying = np.roll(carrying, rng.choice([-1, 1]), axis=0)
            sh = shadow(h)
            p = np.where(sh, 1.0, np.where(h > 0, 0.6, 0.4))
            land = carrying & (rng.random(h.shape) < p)
            h = h + land
            carrying &= ~land
            if not carrying.any():
                break
        h = h + carrying
        h = avalanche(h)
    return h.astype(np.float64)


def image_dunes():
    h = werner_dunes()
    # smooth a touch, upscale to screen
    from scipy.ndimage import gaussian_filter, zoom
    hs = gaussian_filter(h, 1.0, mode="wrap")
    # the field is periodic: tile it and frame a window ~1.6 fields wide
    ny, nx = hs.shape
    hs = np.tile(hs, (2, 2))[ny // 3: ny // 3 + 144, nx // 4: nx // 4 + 192]
    hs = zoom(hs, (H / hs.shape[0], W / hs.shape[1]), order=3) * (H / hs.shape[0]) * 0.2
    # hillshade: low sun from the left (the wind's direction)
    gy, gx = np.gradient(hs)
    sun = np.array([-0.85, -0.25, 0.45])
    sun /= np.linalg.norm(sun)
    nz = 1.0 / np.sqrt(1 + (gx * 1.6) ** 2 + (gy * 1.6) ** 2)
    shade = (-gx * 1.6 * nz) * sun[0] + (-gy * 1.6 * nz) * sun[1] + nz * sun[2]
    shade = np.clip((shade - 0.35) / 0.6, 0, 1) ** 0.8
    # bare flats between dunes stay pale paper; dunes carry the light and shadow
    flat = np.clip(1 - hs / (hs.max() * 0.18), 0, 1)
    shade = shade * (1 - flat) + 0.93 * flat
    g = (np.clip(shade, 0, 1) * 255).astype(np.uint8)
    img = Image.fromarray(g, "L").convert("RGB")
    d = ImageDraw.Draw(img)

    # worm sign: a long sinuous red furrow
    pts = []
    for i in range(160):
        t = i / 159
        x = 30 + 330 * t
        y = 150 + 46 * math.sin(t * 5.2 + 0.6) + 18 * math.sin(t * 13.0)
        pts.append((x, y))
    d.line(pts, fill=RED, width=2)

    p = finalize_dither(img)

    def text(rgb, d):
        d.rectangle([0, 248, W, H], fill=WHITE)
        d.line([(0, 248), (W, 248)], fill=BLACK)
        d.text((14, 254), "FRANK HERBERT", font=inter("Bold", 14), fill=BLACK)
        d.text((136, 257), "born 8 October 1920", font=font(SERIF_I, 12), fill=BLACK)
        d.text((14, 274), "Dunes grown from 21,600 sand slabs (Werner’s 1995 model), wind from the left.",
               font=inter("Regular", 8), fill=BLACK)
        d.text((14, 286), "The red line is worm sign.", font=inter("Regular", 8), fill=RED)
        colophon(rgb, 4)

    return overlay_text(p, text)


# ------------------------------------------------------------------ 5. dew
def image_dew():
    rng = random.Random(72)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    d = ImageDraw.Draw(img)
    hub = np.array([210.0, 138.0]) * s

    # frame threads: the web hangs inside an irregular polygon
    n_rad = 31
    angles = sorted(rng.uniform(0, 2 * math.pi) * 0 + (i + rng.uniform(-0.3, 0.3)) * 2 * math.pi / n_rad
                    for i in range(n_rad))
    frame = [np.array([34, 12]) * s, np.array([392, 26]) * s, np.array([372, 292]) * s, np.array([22, 270]) * s]

    def ray_frame(a):
        dvec = np.array([math.cos(a), math.sin(a)])
        best = None
        for i in range(4):
            p, q = frame[i], frame[(i + 1) % 4]
            e = q - p
            m = np.array([[dvec[0], -e[0]], [dvec[1], -e[1]]])
            if abs(np.linalg.det(m)) < 1e-9:
                continue
            tt, uu = np.linalg.solve(m, p - hub)
            if tt > 0 and 0 <= uu <= 1 and (best is None or tt < best):
                best = tt
        return best

    rmax = [ray_frame(a) for a in angles]
    for i in range(4):
        d.line([tuple(frame[i]), tuple(frame[(i + 1) % 4])], fill=(170, 170, 170), width=s)
    for a, r in zip(angles, rmax):
        e = hub + r * np.array([math.cos(a), math.sin(a)])
        d.line([tuple(hub), tuple(e)], fill=(200, 200, 200), width=s)

    # capture spiral, outer to inner; radius as a fraction of each radial
    drops = []
    turns = 14
    seg = []
    total = turns * n_rad
    for k in range(total):
        i = k % n_rad
        r = (158 - 128 * (k / total) + 2 * math.sin(k * 0.7)) * s
        r = min(r, 0.94 * rmax[i])
        a = angles[i]
        seg.append(hub + r * np.array([math.cos(a), math.sin(a)]))
    for k in range(len(seg) - 1):
        p0, p1 = seg[k], seg[k + 1]
        # threads sag slightly under the weight of dew
        mid = (p0 + p1) / 2 + np.array([0, 1.2 * s])
        d.line([tuple(p0), tuple(mid), tuple(p1)], fill=(230, 230, 230), width=s)
        # Plateau–Rayleigh beading: big drops with tiny satellites between
        length = np.linalg.norm(p1 - p0)
        n = int(length / (10 * s))
        for j in range(n):
            t = (j + 0.5 + rng.uniform(-0.15, 0.15)) / max(n, 1)
            pt = (p0 * (1 - t) + p1 * t) if t < 0.5 else (p1 * t + p0 * (1 - t))
            # follow the sag
            sag = 4 * t * (1 - t) * 1.2 * s
            pt = pt + np.array([0, sag])
            r_big = rng.uniform(1.3, 2.4) * s * (0.6 + 0.6 * (1 - k / total))
            drops.append((pt, r_big))
            sat_t = t + 0.5 / max(n, 1)
            if sat_t < 1:
                sp = p0 * (1 - sat_t) + p1 * sat_t + np.array([0, 4 * sat_t * (1 - sat_t) * 1.2 * s])
                drops.append((sp, 0.55 * s))

    # draw drops: dark rim, white body, black refraction core, a glint
    red_idx = None
    best = 1e9
    for i, (pt, r) in enumerate(drops):
        dist = np.linalg.norm(pt - np.array([296, 190]) * s)
        if r > 1.6 * s and dist < best:
            best, red_idx = dist, i
    for i, (pt, r) in enumerate(drops):
        x, y = pt
        if r < 1 * s:
            d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
            continue
        d.ellipse([x - r - s, y - r - s, x + r + s, y + r + s], fill=BLACK)
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
        cr = r * 0.45
        d.ellipse([x - cr + 0.25 * r, y - cr + 0.25 * r, x + cr + 0.25 * r, y + cr + 0.25 * r], fill=BLACK)
    # one big drop holds the sunrise
    pt, _ = drops[red_idx]
    x, y = pt
    R = 7 * s
    d.ellipse([x - R - s, y - R - s, x + R + s, y + R + s], fill=BLACK)
    d.ellipse([x - R, y - R, x + R, y + R], fill=RED)
    d.ellipse([x - 3.2 * s, y - 4.2 * s, x - 0.6 * s, y - 1.8 * s], fill=WHITE)

    p = finalize_hard(img, thr=90)

    def text(rgb, d):
        d.rectangle([8, 236, 132, 290], fill=BLACK)
        d.text((14, 238), "寒露", font=font(JP, 26), fill=WHITE)
        d.text((14, 268), "KANRO · cold dew", font=inter("Medium", 9), fill=WHITE)
        d.text((14, 280), "8–22 October", font=inter("Regular", 8), fill=RED)
        colophon(rgb, 5, ink=WHITE)

    return overlay_text(p, text)


def main(outdir):
    import os
    os.makedirs(outdir, exist_ok=True)
    for n, fn in enumerate([image_geese, image_tally, image_fires, image_dunes, image_dew], 1):
        im = fn()
        assert im.size == (W, H)
        im.save(f"{outdir}/{n}.png", optimize=True)
        print("wrote", n, fn.__name__)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
