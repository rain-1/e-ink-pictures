#!/usr/bin/env python3
"""Plates 006-010 · 2026-10-18 · 400x300 black/white/red e-ink.

006 8.90        Beamon's jump, 18 Oct 1968, as a Marey chronophotograph
007 VENERA 4    first probe to report from inside another planet's air, 18 Oct 1967
008 蟋蟀在戸     microseason 51: crickets at the door (a night, a light, a count)
009 TR-1        the pocket transistor radio, announced 18 Oct 1954
010 (untitled)  Lichtenberg figure — random-weight shortest-path tree, red trunk

Run from anywhere:  python3 generate.py [outdir]
"""
import heapq
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
SEED = 20261018

F = "/usr/share/fonts/truetype/"
MONO = F + "dejavu/DejaVuSansMono.ttf"
MONO_B = F + "dejavu/DejaVuSansMono-Bold.ttf"
SANS = F + "dejavu/DejaVuSans.ttf"
SERIF_I = F + "liberation/LiberationSerif-Italic.ttf"
INTER_B = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
CJK = F + "wqy/wqy-zenhei.ttc"


def font(p, s):
    return ImageFont.truetype(p, s)


PALETTE = np.array([WHITE, BLACK, RED], dtype=np.int32)


def to_palette(img):
    """Nearest-colour snap (no dithering) to the exact 3-colour palette."""
    a = np.asarray(img.convert("RGB"), dtype=np.int32)
    d = ((a[:, :, None, :] - PALETTE[None, None]) ** 2).sum(-1)
    idx = d.argmin(-1).astype(np.uint8)
    out = Image.fromarray(idx, "P")
    out.putpalette([255, 255, 255, 0, 0, 0, 255, 0, 0] + [0] * (253 * 3))
    return out


def down(img):
    """Big RGB render -> 1x, snapped (crisp AA edges)."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return to_palette(img).convert("RGB")


def dither(gray):
    """Grayscale 'L' (any size) -> 1x Floyd–Steinberg black/white RGB."""
    if gray.size != (W, H):
        gray = gray.resize((W, H), Image.LANCZOS)
    return gray.convert("1").convert("RGB")


def text1(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"  # no AA on 1x text, ever
    return d


def colophon(d, n, fg=BLACK, bg=None, x=None, y=None):
    """My mark: a small red lozenge and a running plate number."""
    f = font(MONO, 9)
    t = f"№{n:03d}"
    tw = d.textlength(t, font=f)
    x = W - tw - 6 if x is None else x
    y = H - 13 if y is None else y
    if bg is not None:
        d.rectangle([x - 12, y - 1, x + tw + 2, y + 11], fill=bg)
    d.polygon([(x - 8, y + 5), (x - 5, y + 2), (x - 2, y + 5), (x - 5, y + 8)], fill=RED)
    d.text((x, y), t, font=f, fill=fg)


def lerp(a, b, t):
    return a + (b - a) * t


# ------------------------------------------------------------- 006 Beamon
# Joint keyframes relative to the hip, metres (x forward, y up).
JOINTS = ["head", "neck", "elbowA", "handA", "elbowB", "handB",
          "kneeA", "footA", "kneeB", "footB"]
POSES = [
    # take-off: drive knee up, take-off leg trailing, opposite arm punching up
    dict(head=(.16, .72), neck=(.10, .55), elbowA=(.30, .72), handA=(.38, .95),
         elbowB=(-.12, .34), handB=(-.30, .22), kneeA=(.36, -.04), footA=(.30, -.46),
         kneeB=(-.20, -.40), footB=(-.42, -.76)),
    # hitch-kick in the air, arms circling high
    dict(head=(.03, .73), neck=(.00, .55), elbowA=(.10, .84), handA=(.22, 1.04),
         elbowB=(-.12, .80), handB=(-.04, 1.02), kneeA=(.14, -.36), footA=(.02, -.76),
         kneeB=(-.04, -.30), footB=(-.36, -.58)),
    # sail: legs coming through together, arms swinging forward
    dict(head=(.12, .70), neck=(.06, .53), elbowA=(.24, .62), handA=(.44, .66),
         elbowB=(.20, .60), handB=(.40, .62), kneeA=(.36, -.10), footA=(.56, -.48),
         kneeB=(.34, -.06), footB=(.58, -.42)),
    # landing reach: jack-knifed, heels far forward
    dict(head=(.40, .54), neck=(.28, .44), elbowA=(.36, .20), handA=(.58, .06),
         elbowB=(.32, .24), handB=(.54, .10), kneeA=(.42, .02), footA=(.82, -.04),
         kneeB=(.44, .06), footB=(.84, .02)),
]


def pose_at(t):
    seg = min(int(t * 3), 2)
    u = t * 3 - seg
    u = u * u * (3 - 2 * u)
    a, b = POSES[seg], POSES[seg + 1]
    return {k: (lerp(a[k][0], b[k][0], u), lerp(a[k][1], b[k][1], u)) for k in JOINTS}


def plate_beamon():
    S = 3
    img = Image.new("RGB", (W * S, H * S), BLACK)
    d = ImageDraw.Draw(img)
    board_x, ground = 34, 236          # px
    ppm = 36.0                         # px per metre
    X = lambda m: (board_x + m * ppm) * S
    Y = lambda m: (ground - m * ppm) * S
    # ground & pit
    d.line([0, Y(0), W * S, Y(0)], fill=WHITE, width=S)
    pit0, pit1 = 1.0, 9.6
    rng = np.random.default_rng(SEED)
    for _ in range(900):  # sand grain stipple
        mx = rng.uniform(pit0, pit1)
        my = -rng.uniform(0, 0.28) ** 1.6
        d.point([X(mx), Y(my) + S * 2], fill=WHITE)
    d.rectangle([X(-0.2), Y(0) - S, X(0), Y(0) + 3 * S], fill=WHITE)  # board
    # flight: hip parabola from take-off (1.05 m) to landing (0.55 m), apex 1.80 m
    x_take, x_land = 0.10, 8.20     # hip x; heels land at 8.90 on the last pose
    h0, hp, h1 = 1.05, 1.80, 0.55
    # solve parabola y = a x^2 + b x + c through three points with apex near 45%
    xs = np.array([x_take, lerp(x_take, x_land, .46), x_land])
    a_, b_, c_ = np.polyfit(xs, np.array([h0, hp, h1]), 2)
    hip = lambda m: a_ * m * m + b_ * m + c_
    # dotted hip path (Marey's point-trace)
    for m in np.arange(x_take, x_land, 0.07):
        r = 0.6 * S
        d.ellipse([X(m) - r, Y(hip(m)) - r, X(m) + r, Y(hip(m)) + r], fill=WHITE)
    n = 13
    for i in range(n):
        t = i / (n - 1)
        hx = lerp(x_take, x_land, t)
        hy = hip(hx)
        p = pose_at(t)
        P = lambda k: (X(hx + p[k][0]), Y(hy + p[k][1]))
        hipP = (X(hx), Y(hy))
        lw = int(1.3 * S)
        for chain in (["neck", "elbowA", "handA"], ["neck", "elbowB", "handB"],
                      ["kneeA", "footA"], ["kneeB", "footB"]):
            pts = [P(c) for c in chain]
            if chain[0].startswith("knee"):
                pts = [hipP] + pts
            d.line(pts, fill=WHITE, width=lw, joint="curve")
        d.line([hipP, P("neck")], fill=WHITE, width=lw)
        hx_, hy_ = P("head")
        r = 0.11 * ppm * S
        d.ellipse([hx_ - r, hy_ - r, hx_ + r, hy_ + r], outline=WHITE, width=lw)
    img = down(img)
    d = text1(img)
    # the tape: red, under the ground, from board to 8.90
    ty = ground + 18
    xb = board_x
    x890 = board_x + 8.90 * ppm
    x835 = board_x + 8.35 * ppm
    d.rectangle([xb, ty, x890, ty + 4], fill=RED)
    for m in range(0, 9):
        x = board_x + m * ppm
        d.line([x, ty + 5, x, ty + 8], fill=WHITE)
        d.text((x - 2, ty + 9), str(m), font=font(MONO, 8), fill=WHITE)
    d.line([x890, ground + 2, x890, ty + 12], fill=RED, width=1)
    d.line([x835, ty - 6, x835, ty - 1], fill=WHITE)
    f8 = font(MONO, 8)
    d.text((x835 - 52, ty - 13), "8.35 old WR", font=f8, fill=WHITE)
    # headline
    d.text((10, 6), "8.90", font=font(INTER_B, 52), fill=WHITE)
    d.text((12, 64), "MEXICO CITY · 18·X·1968 · 2240 m", font=f8, fill=WHITE)
    fi = font(SERIF_I, 13)
    d.text((10, 276), "He was in the air for under a second; the record stood 23 years.",
           font=fi, fill=WHITE)
    d.text((W - 132, 12), "BOB BEAMON", font=font(MONO_B, 10), fill=WHITE)
    d.text((W - 132, 25), "13 frames, after Marey", font=f8, fill=WHITE)
    d.text((W - 132, 35), "+55 cm on the world", font=f8, fill=WHITE)
    colophon(d, 6, fg=WHITE, bg=BLACK, y=H - 40)
    return img


# ------------------------------------------------------------- 007 Venera 4
def plate_venera():
    top_km, alt_y0, alt_y1 = 72, 14, 262
    A = lambda km: alt_y1 - (km / top_km) * (alt_y1 - alt_y0)
    # atmosphere as tone: pale above the clouds, a textured cloud deck, then
    # density pressing toward black at the surface.
    yy, xx = np.mgrid[0:H * 2, 0:W * 2] / 2.0
    km = (alt_y1 - yy) / (alt_y1 - alt_y0) * top_km
    rng = np.random.default_rng(SEED + 7)
    kmc = np.clip(km, 0, None)
    tone = np.clip(0.04 + 0.66 * (kmc / 48) ** 1.6, 0, 0.70)   # below the deck
    tone = np.where(kmc > 64, 0.97, tone)
    # cloud deck 48-68 km: banded, streaky noise (superrotation: long in x)
    noise = np.zeros_like(tone)
    for k, amp in [(6, .5), (14, .3), (30, .2)]:
        g = rng.normal(size=(k * 5, max(2, k // 2)))
        g = np.array(Image.fromarray(((g - g.min()) / np.ptp(g) * 255).astype(np.uint8))
                     .resize((W * 2, H * 2), Image.BICUBIC)) / 255.0
        noise += amp * (g - .5)
    deck = np.clip(1 - np.abs(km - 57) / 9, 0, 1) ** 0.7
    streak = np.tanh(noise * 7) * 0.5 + 0.5
    tone = np.clip(tone * (1 - deck) + deck * (0.25 + 0.75 * streak), 0, 1)
    tone[km < 0] = 0
    gray = Image.fromarray((tone * 255).astype(np.uint8), "L")
    img = dither(gray)
    d = text1(img)
    # surface
    d.rectangle([0, A(0), W, H], fill=BLACK)
    # temperature axis: 0-500 C on x
    T = lambda c: 150 + c / 500 * 236
    # descent profile (lapse rate ~8.5 K/km below the deck)
    prof = [(52, 33), (45, 92), (40, 135), (35, 178), (30, 220), (26, 255), (25, 262)]
    # the trace drawn as telemetry pulses, every ~0.6 km
    pts = []
    for (k0, c0), (k1, c1) in zip(prof, prof[1:]):
        for u in np.linspace(0, 1, 9, endpoint=False):
            pts.append((lerp(k0, k1, u), lerp(c0, c1, u)))
    pts.append(prof[-1])
    for kmv, c in pts:
        x, y = T(c), A(kmv)
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=RED)
    # the unheard part, as later probes found it (Venera 7: 475 C at surface)
    for kmv in np.arange(24, 0, -1.2):
        c = 262 + (25 - kmv) * 8.5
        x, y = T(c), A(kmv)
        d.point((x, y), fill=WHITE)
    x_end, y_end = T(262), A(25)
    d.line([x_end + 4, y_end, x_end + 18, y_end], fill=RED)
    # label box for signal loss
    fm = font(MONO, 8)
    lab = ["SIGNAL LOST", "~25 km · 262 °C", "18–22 atm"]
    bx, by = x_end + 20, y_end - 14
    d.rectangle([bx - 2, by - 2, bx + 82, by + 30], fill=WHITE, outline=RED)
    for i, s in enumerate(lab):
        d.text((bx + 2, by + i * 9), s, font=fm, fill=RED if i == 0 else BLACK)
    # parachute + capsule silhouette at 52 km
    S = 4
    cap = Image.new("RGBA", (60 * S, 60 * S), (0, 0, 0, 0))
    c = ImageDraw.Draw(cap)
    cx = 30 * S
    c.pieslice([cx - 22 * S, 2 * S, cx + 22 * S, 30 * S], 180, 360, fill=BLACK)
    for dx in (-21, -10, 0, 10, 21):
        c.line([cx + dx * S, 16 * S, cx, 42 * S], fill=BLACK, width=S // 2 + 1)
    c.ellipse([cx - 6 * S, 40 * S, cx + 6 * S, 52 * S], fill=BLACK)
    cap = cap.resize((60, 60), Image.LANCZOS)
    mask = cap.split()[3].point(lambda v: 255 if v > 100 else 0)
    px, py = int(T(33)) - 30, int(A(52)) - 50
    halo = Image.new("L", (60, 60), 0)
    halo.paste(255, (0, 0), mask)
    from PIL import ImageFilter
    halo = halo.filter(ImageFilter.MaxFilter(5))
    img.paste(WHITE, (px, py), halo)
    img.paste(BLACK, (px, py), mask)
    d = text1(img)
    # altitude scale
    for kmv in range(0, 61, 10):
        y = A(kmv)
        d.line([0, y, 5, y], fill=WHITE if kmv < 20 else BLACK)
        if kmv:
            d.rectangle([6, y - 5, 19, y + 4], fill=WHITE)
            d.text((7, y - 5), f"{kmv}", font=fm, fill=BLACK)
    d.text((7, A(0) + 6), "surface · 465 °C · 92 atm — learned in 1970", font=fm,
           fill=WHITE)
    d.text((7, A(0) + 17), "the first voice from inside another world's air",
           font=font(SERIF_I, 11), fill=WHITE)
    # headline block
    d.rectangle([236, 4, 396, 70], fill=WHITE, outline=BLACK)
    d.text((242, 4), "VENERA 4", font=font(INTER_B, 30), fill=BLACK)
    d.text((243, 38), "18·X·1967 · 93 min", font=fm, fill=BLACK)
    d.text((243, 48), "under a parachute", font=fm, fill=BLACK)
    d.text((243, 58), "air: CO₂ 90 %, no sea", font=fm, fill=BLACK)
    colophon(d, 7, fg=WHITE, bg=BLACK, y=H - 26)
    return img


# ------------------------------------------------------------- 008 crickets
def draw_cricket(d, x, y, s, fill):
    """Field cricket in profile, facing left; (x,y) = belly centre; s = px/unit."""
    P = lambda u, v: (x + u * s, y + v * s)
    d.ellipse([*P(-3.0, -1.3), *P(3.2, 1.0)], fill=fill)          # abdomen+wings
    d.polygon([P(-2.6, -1.2), P(4.2, -0.9), P(3.4, 0.2), P(-2.4, 0.2)], fill=fill)
    d.ellipse([*P(-4.6, -1.5), *P(-2.4, 0.8)], fill=fill)          # pronotum
    d.ellipse([*P(-6.0, -1.4), *P(-4.0, 0.6)], fill=fill)          # head
    w = max(1, int(s * 0.62))
    # antennae: long sweeping curves back over the body
    for k, (ax, ay) in enumerate([(-9, -6), (-2, -9.5)]):
        pts = []
        for t in np.linspace(0, 1, 30):
            u = lerp(-5.6, 4 + 9 * k, t) - 6 * math.sin(t * math.pi) * (1 - k * .4)
            v = -1.2 - 7.5 * math.sin(t * math.pi * (0.55 + .1 * k)) + t * 2
            pts.append(P(u, v))
        d.line(pts, fill=fill, width=max(1, int(w * .6)), joint="curve")
    # cerci
    d.line([P(3.8, -0.4), P(7.2, -1.2)], fill=fill, width=max(1, w // 2))
    d.line([P(3.8, -0.1), P(7.0, 0.6)], fill=fill, width=max(1, w // 2))
    # legs: two front pairs, then the great hind femur
    d.line([P(-3.8, 0.4), P(-5.6, 2.0), P(-7.0, 2.6)], fill=fill, width=w)
    d.line([P(-2.0, 0.5), P(-2.6, 2.2), P(-4.0, 2.7)], fill=fill, width=w)
    d.polygon([P(-0.6, -0.6), P(1.6, -1.6), P(4.9, -2.3), P(5.2, -1.6), P(1.8, 1.0),
               P(-0.4, 0.9)], fill=fill)                         # hind femur
    d.line([P(5.0, -1.9), P(2.8, 2.6), P(4.6, 2.8)], fill=fill, width=w)


def plate_crickets():
    # light: a vertical slit (the door ajar) spilling a fan onto the floor
    S = 2
    yy, xx = np.mgrid[0:H * S, 0:W * S] / S
    gap_x0, gap_x1 = 236, 248
    floor_y = 212
    tone = np.zeros((H * S, W * S))
    # slit itself
    slit = (xx >= gap_x0) & (xx <= gap_x1) & (yy >= 24) & (yy <= floor_y)
    tone[slit] = 1.0
    # spill: a fan widening toward the viewer, brightness falling with distance
    below = yy > floor_y
    depth = (yy - floor_y) / (H - floor_y)
    half = 6 + depth * 92
    cx = (gap_x0 + gap_x1) / 2 - depth * 46
    edge = np.clip((half - np.abs(xx - cx)) / (6 + depth * 26), 0, 1)
    tone[below] = (edge * (1.0 - 0.5 * depth))[below]
    # faint glow on the floorboards' seams outside the fan
    # spill on the door edge (the door's thickness catching light)
    edge_col = (xx > gap_x1) & (xx < gap_x1 + 3) & (yy > 24) & (yy < floor_y)
    tone[edge_col] = 0.35
    gray = Image.fromarray((tone * 255).astype(np.uint8), "L")
    img = dither(gray)
    # the cricket on the threshold, in the light (black on lit floor)
    big = Image.new("RGB", (W * 4, H * 4), (0, 0, 0))
    m = ImageDraw.Draw(big)
    draw_cricket(m, 214 * 4, 262 * 4, 3.4 * 4, (255, 255, 255))
    big = big.convert("L").resize((W, H), Image.LANCZOS).point(lambda v: 255 if v > 90 else 0)
    from PIL import ImageFilter
    img.paste(WHITE, (0, 0), big.filter(ImageFilter.MaxFilter(5)))
    img.paste(BLACK, (0, 0), big)
    d = text1(img)
    # 17 chirps in 15 seconds, as a score along the top of the dark
    rng = np.random.default_rng(SEED + 8)
    x0, x1, sy = 24, 214, 150
    for i in range(17):
        x = lerp(x0, x1, i / 16) + rng.uniform(-1.2, 1.2)
        # each chirp = 3-4 pulses (wing strokes)
        for p in range(3 + (i % 3 == 0)):
            d.line([x + p * 2.2, sy - 4, x + p * 2.2, sy + 4], fill=RED)
    d.line([x0, sy + 9, x1 + 8, sy + 9], fill=WHITE)
    d.line([x0, sy + 7, x0, sy + 11], fill=WHITE)
    d.line([x1 + 8, sy + 7, x1 + 8, sy + 11], fill=WHITE)
    fm = font(MONO, 8)
    d.text((x0, sy + 13), "15 s · 17 chirps · +40 = 57 °F", font=fm, fill=WHITE)
    # vertical kanji, right edge
    fk = font(CJK, 22)
    for i, ch in enumerate("蟋蟀在戸"):
        d.text((362, 30 + i * 28), ch, font=fk, fill=WHITE)
    d.text((24, sy + 24), "Dolbear 1897", font=fm, fill=WHITE)
    d.text((300, 160), "kō 51 · 18–22 Oct", font=fm, fill=WHITE)
    fi = font(SERIF_I, 13)
    d.text((24, 40), "crickets at the door —", font=fi, fill=WHITE)
    d.text((24, 56), "the cold has moved them", font=fi, fill=WHITE)
    d.text((24, 72), "one room closer.", font=fi, fill=WHITE)
    colophon(d, 8, fg=WHITE, bg=BLACK)
    return img


# ------------------------------------------------------------- 009 TR-1
def transistor_symbol(d, x, y, r, col, w=1):
    d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=w)
    d.line([x - r * .35, y - r * .55, x - r * .35, y + r * .55], fill=col, width=w + 1)
    d.line([x - r * 1.5, y, x - r * .35, y], fill=col, width=w)
    d.line([x - r * .35, y - r * .25, x + r * .45, y - r * .8], fill=col, width=w)
    d.line([x + r * .45, y - r * .8, x + r * .45, y - r * 1.5], fill=col, width=w)
    d.line([x - r * .35, y + r * .25, x + r * .45, y + r * .8], fill=col, width=w)
    d.line([x + r * .45, y + r * .8, x + r * .45, y + r * 1.5], fill=col, width=w)
    ax, ay = x + r * .45, y + r * .8          # emitter arrow
    d.polygon([(ax, ay), (ax - r * .42, ay - r * .06), (ax - r * .18, ay - r * .38)], fill=col)


def plate_tr1():
    S = 3
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)
    # case: 3 x 5 inches, upright, mandarin red
    x0, y0, cw, ch = 30, 22, 156, 260
    sx = lambda v: v * S
    d.rounded_rectangle([sx(x0 + 4), sx(y0 + 5), sx(x0 + cw + 4), sx(y0 + ch + 5)],
                        radius=sx(18), fill=BLACK)              # shadow side
    d.rounded_rectangle([sx(x0), sx(y0), sx(x0 + cw), sx(y0 + ch)], radius=sx(18), fill=RED)
    # dial: a white disc in the upper half, tick ring
    dcx, dcy, dr = x0 + cw / 2, y0 + 70, 50
    d.ellipse([sx(dcx - dr - 4), sx(dcy - dr - 4), sx(dcx + dr + 4), sx(dcy + dr + 4)],
              fill=BLACK)
    d.ellipse([sx(dcx - dr), sx(dcy - dr), sx(dcx + dr), sx(dcy + dr)], fill=WHITE)
    labels = ["55", "60", "70", "80", "100", "120", "140", "160"]
    for i, lab in enumerate(labels):
        a = math.radians(210 - i * (240 / 7))
        r0, r1 = dr - 6, dr - 1
        d.line([sx(dcx + r0 * math.cos(a)), sx(dcy - r0 * math.sin(a)),
                sx(dcx + r1 * math.cos(a)), sx(dcy - r1 * math.sin(a))], fill=BLACK, width=S)
    for k in range(57):
        a = math.radians(210 - k * (240 / 56))
        r0, r1 = dr - 3, dr - 1
        d.line([sx(dcx + r0 * math.cos(a)), sx(dcy - r0 * math.sin(a)),
                sx(dcx + r1 * math.cos(a)), sx(dcy - r1 * math.sin(a))], fill=BLACK, width=1)
    # pointer, tuned to ~ 88 (kc x10)
    a = math.radians(210 - 3.3 * (240 / 7))
    d.line([sx(dcx), sx(dcy), sx(dcx + (dr - 8) * math.cos(a)), sx(dcy - (dr - 8) * math.sin(a))],
           fill=RED, width=2 * S)
    d.ellipse([sx(dcx - 5), sx(dcy - 5), sx(dcx + 5), sx(dcy + 5)], fill=RED)
    # grille: a field of punched holes, clipped to a rounded window
    gx0, gy0, gx1, gy1 = x0 + 18, y0 + 136, x0 + cw - 18, y0 + ch - 20
    d.rounded_rectangle([sx(gx0 - 3), sx(gy0 - 3), sx(gx1 + 3), sx(gy1 + 3)], radius=sx(8),
                        outline=BLACK, width=S)
    pitch = 7.0
    rows = int((gy1 - gy0) / (pitch * 0.87))
    cols = int((gx1 - gx0) / pitch)
    for j in range(rows + 1):
        for i in range(cols + 1):
            hx = gx0 + i * pitch + (pitch / 2 if j % 2 else 0)
            hy = gy0 + j * pitch * 0.87
            if hx > gx1 or hy > gy1:
                continue
            r = 2.0
            d.ellipse([sx(hx - r), sx(hy - r), sx(hx + r), sx(hy + r)], fill=BLACK)
    img = down(img)
    d = text1(img)
    # dial numerals at 1x
    f7 = font(SANS, 7)
    for i, lab in enumerate(labels):
        a = math.radians(210 - i * (240 / 7))
        r = dr - 14
        tx, ty = dcx + r * math.cos(a), dcy - r * math.sin(a)
        tw = d.textlength(lab, font=f7)
        d.text((tx - tw / 2, ty - 4), lab, font=f7, fill=BLACK)
    d.text((dcx - 7, dcy + 16), "KC", font=f7, fill=BLACK)
    # right column
    tx = 214
    d.text((tx, 22), "TR-1", font=font(INTER_B, 54), fill=BLACK)
    fm = font(MONO, 9)
    rows_ = ["announced 18 Oct 1954", "on sale 1 Nov · $49.95",
             "3 × 5 × 1¼ in", "22.5 V · 20 h", "germanium × 4"]
    for i, s in enumerate(rows_):
        d.text((tx + 2, 88 + i * 12), s, font=fm, fill=BLACK)
    # the four transistors themselves
    roles = ["mix/osc", "IF", "IF", "audio"]
    for i, role in enumerate(roles):
        x = tx + 20 + i * 44
        transistor_symbol(d, x, 172, 9, BLACK)
        tw = d.textlength(role, font=font(MONO, 8))
        d.text((x - tw / 2 + 2, 190), role, font=font(MONO, 8), fill=BLACK)
    fi = font(SERIF_I, 13)
    d.text((tx, 214), "Thin, tinny, and the first", font=fi, fill=BLACK)
    d.text((tx, 230), "music you could put", font=fi, fill=BLACK)
    d.text((tx, 246), "in a pocket.", font=fi, fill=BLACK)
    colophon(d, 9)
    return img


# ------------------------------------------------------------- 010 Lichtenberg
def plate_lichtenberg():
    cell = 2
    gw, gh = W // cell, H // cell
    rng = np.random.default_rng(SEED + 10)
    # heavy-tailed random resistance: the discharge takes the cheapest road
    wgt = rng.lognormal(0.0, 1.1, size=(gh, gw))
    root = (gh // 2 + 6, gw // 2 - 18)
    INF = float("inf")
    dist = np.full((gh, gw), INF)
    parent = np.full((gh, gw, 2), -1, dtype=np.int32)
    dist[root] = 0.0
    pq = [(0.0, root)]
    nbrs = [(dy, dx, math.hypot(dy, dx)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
            if dy or dx]
    while pq:
        dv, (y, x) = heapq.heappop(pq)
        if dv > dist[y, x]:
            continue
        for dy, dx, L in nbrs:
            ny, nx = y + dy, x + dx
            if 0 <= ny < gh and 0 <= nx < gw:
                nd = dv + L * 0.5 * (wgt[y, x] + wgt[ny, nx])
                if nd < dist[ny, nx]:
                    dist[ny, nx] = nd
                    parent[ny, nx] = (y, x)
                    heapq.heappush(pq, (nd, (ny, nx)))
    # flow: each cell drains one unit to the root; trunks carry the most
    order = np.argsort(-dist, axis=None)
    flow = np.ones((gh, gw))
    for idx in order:
        y, x = divmod(int(idx), gw)
        py, px = parent[y, x]
        if py >= 0:
            flow[py, px] += flow[y, x]
    # the main channel: from root, always follow the heaviest child
    children = {}
    for y in range(gh):
        for x in range(gw):
            py, px = parent[y, x]
            if py >= 0:
                children.setdefault((py, px), []).append((y, x))
    trunk = [root]
    while trunk[-1] in children:
        trunk.append(max(children[trunk[-1]], key=lambda c: flow[c]))
    trunk_set = set(trunk[: int(len(trunk) * 0.9)])
    S = 3
    img = Image.new("RGB", (W * S, H * S), BLACK)
    d = ImageDraw.Draw(img)
    C = lambda y, x: ((x + .5) * cell * S, (y + .5) * cell * S)
    thresh = 9
    ys, xs = np.nonzero(flow >= thresh)
    for y, x in zip(ys, xs):
        py, px = parent[y, x]
        if py < 0:
            continue
        f = flow[y, x]
        wpx = 0.35 + 0.62 * math.log10(f / thresh + 1) * 1.6
        col = RED if (y, x) in trunk_set else WHITE
        d.line([C(y, x), C(py, px)], fill=col, width=max(1, int(wpx * S)))
    # electrode: a small white disc with a red heart
    cxp, cyp = C(*root)
    d.ellipse([cxp - 5 * S, cyp - 5 * S, cxp + 5 * S, cyp + 5 * S], fill=WHITE)
    d.ellipse([cxp - 2 * S, cyp - 2 * S, cxp + 2 * S, cyp + 2 * S], fill=RED)
    img = down(img)
    d = text1(img)
    colophon(d, 10, fg=WHITE, bg=BLACK)
    d.rectangle([2, H - 15, 196, H - 2], fill=BLACK)
    d.text((6, H - 13), f"lognormal σ1.1 · flow ≥ {thresh} · seed {SEED + 10}",
           font=font(MONO, 8), fill=WHITE)
    return img


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    plates = [plate_beamon, plate_venera, plate_crickets, plate_tr1, plate_lichtenberg]
    for i, fn in enumerate(plates, 1):
        im = to_palette(fn())
        assert im.size == (W, H)
        im.save(os.path.join(outdir, f"{i}.png"), optimize=True)
        print("wrote", i, fn.__name__)


if __name__ == "__main__":
    main()
