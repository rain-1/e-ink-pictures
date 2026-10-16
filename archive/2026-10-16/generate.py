#!/usr/bin/env python3
"""Daily e-ink pictures - 2026-10-16.  Style: "almanac press".

Today's hooks: Hamilton cuts i^2 = j^2 = k^2 = ijk = -1 into Brougham Bridge
(16 Oct 1843); the Palace of Westminster burns because the Exchequer fed two
cartloads of obsolete tally sticks into a stove (16 Oct 1834); in the French
Republican calendar it is Quintidi 25 Vendemiaire an CCXXXV, day of the Ox;
plus a wordless Proun and a Chladni sand figure.

Pipeline: draw at 3x in pure palette colours, LANCZOS down, then a custom
quantizer (hue test for red, luminance threshold for black/white) so
antialiased black edges never turn red.
"""
import math
import random
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S = 400, 300, 3
SW, SH = W * S, H * S
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
FD = "/usr/share/fonts/truetype/"
SERIF = FD + "liberation/LiberationSerif-Regular.ttf"
SERIF_B = FD + "liberation/LiberationSerif-Bold.ttf"
SERIF_I = FD + "liberation/LiberationSerif-Italic.ttf"
SERIF_BI = FD + "liberation/LiberationSerif-BoldItalic.ttf"
SANS_B = FD + "dejavu/DejaVuSans-Bold.ttf"
MONO_B = FD + "dejavu/DejaVuSansMono-Bold.ttf"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
SIG = "16·X·26"


def F(path, px):  # font sized in final pixels, for a 3x canvas
    return ImageFont.truetype(path, int(px * S))


def canvas(bg=WHITE):
    im = Image.new("RGB", (SW, SH), bg)
    return im, ImageDraw.Draw(im)


def quantize(im, thresh=175):
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (r + g + b) / 3
    red = (r - np.maximum(g, b)) > 90
    idx = np.where(red, 2, np.where(lum < thresh, 1, 0)).astype(np.uint8)
    out = Image.fromarray(idx, "P")
    out.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0] * 759)
    return out


def S_(*v):
    return [x * S for x in v]


def text(d, xy, s, font, fill=BLACK, anchor="la"):
    d.text((xy[0] * S, xy[1] * S), s, font=font, fill=fill, anchor=anchor)


def mark(d, roman, ink=BLACK):
    """Signature: tiny red square + date + roman numeral, bottom-right."""
    label = f"{SIG}  {roman}"
    f = F(MONO_B, 7)
    text(d, (391, 293), label, f, ink, anchor="rs")
    w = d.textlength(label, font=f) / S
    d.rectangle(S_(391 - w - 8, 288, 391 - w - 4, 292), fill=RED)


def noise(w, h, cells, seed):
    """Smooth value noise in 0..1, shape (h, w)."""
    rng = np.random.default_rng(seed)
    gy, gx = max(2, int(cells * h / w)), max(2, cells)
    g = (rng.random((gy, gx)) * 255).astype(np.uint8)
    return np.asarray(Image.fromarray(g).resize((w, h), Image.BICUBIC)).astype(float) / 255


def fbm(w, h, seed, octaves=4, cells=4):
    out, amp, tot = np.zeros((h, w)), 1.0, 0.0
    for o in range(octaves):
        out += amp * noise(w, h, cells * 2 ** o, seed + o)
        tot += amp
        amp *= 0.5
    return out / tot


def grid():
    yy, xx = np.mgrid[0:SH, 0:SW].astype(float)
    return xx / S, yy / S  # coordinates in final pixels


def screen(coord, dark, period):
    """Line-screen engraving: ink where the line is wider than (1-dark)."""
    fr = np.abs(((coord / period) % 1) - 0.5) * 2
    return fr > 1 - dark


def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) / S > maxw and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = t
    return lines + [cur]


# ------------------------------------------------- i. Brougham Bridge, 1843
def img_bridge():
    X, Y = grid()
    ink = np.zeros((SH, SW), bool)
    WL = 182.0                     # water line
    cx, a, b = 200.0, 72.0, 60.0   # arch: half-ellipse on the water line
    e = ((X - cx) / a) ** 2 + ((Y - WL) / b) ** 2
    e_ring = ((X - cx) / (a + 10)) ** 2 + ((Y - WL) / (b + 10)) ** 2
    above = Y < WL

    # sky: faint lines thickening upward
    sky = (Y > 22) & (Y < 76)
    ink |= sky & screen(Y, 0.30 * np.clip(1 - (Y - 22) / 54, 0, 1) ** 1.6, 3.4)
    # far tree line, bumpy top, vertical hatch
    tn = fbm(SW, 1, 11, octaves=4, cells=10)[0]
    ttop = 50 + 16 * tn
    trees = (Y > ttop[None, :]) & (Y < 78)
    tdark = 0.55 + 0.25 * fbm(SW, SH, 12, 3, 16)
    ink |= trees & screen(X + 0.6 * np.sin(Y * 1.3), tdark, 2.6)
    ink |= trees & (Y < ttop[None, :] + 0.9)

    # parapet with coping
    par = (Y >= 76) & (Y < 100)
    ink |= par & screen(Y, 0.22, 3.0)
    for yl in (76, 80, 100):
        ink |= np.abs(Y - yl) < 0.6
    # parapet joints
    ink |= par & (Y > 80) & (np.abs(((X + 7) % 31) - 15.5) > 15.0)

    # bridge face: ashlar courses
    face = (Y >= 100) & above & (e_ring >= 1)
    ink |= face & screen(Y + 0.5, 0.26 + 0.12 * fbm(SW, SH, 13, 3, 6), 3.0)
    row = np.floor((Y - 100) / 10)
    ink |= face & (np.abs(((Y - 100) % 10) - 5) > 4.45)
    ink |= face & (np.abs(((X + 13 * (row % 2)) % 26) - 13) > 12.45)

    # voussoir ring: dressed stone, radial joints
    ring = above & (e_ring < 1) & (e >= 1)
    ang = np.arctan2(WL - Y, (X - cx) * b / a)
    ink |= ring & screen(Y, 0.14, 3.0)
    ink |= ring & (np.abs(((ang / (math.pi / 17)) % 1) - 0.5) > 0.44)
    ink |= above & (np.abs(np.sqrt(e_ring) - 1) < 0.012)
    ink |= above & (np.abs(np.sqrt(e) - 1) < 0.014)
    # keystone in red-free relief: slightly bolder

    # barrel of the arch: dark, light at the far end
    barrel = above & (e < 1)
    far = ((X - cx) / 34) ** 2 + ((Y - WL) / 27) ** 2
    bd = np.clip(0.95 - 0.55 * np.clip(1.25 - np.sqrt(far), 0, 1), 0, 1)
    ink |= barrel & (far >= 1) & screen(Y, bd, 3.0)
    ink |= barrel & (far >= 1) & (bd > 0.6) & screen(X + Y, bd - 0.35, 3.4)
    ink |= barrel & (far < 1) & screen(Y, 0.12, 3.0)
    ink |= barrel & (np.abs(np.sqrt(far) - 1) < 0.03)

    # water: reflection of everything above, rippled
    water = (Y >= WL) & (Y < 238)
    my = 2 * WL - Y
    me = ((X - cx) / a) ** 2 + ((my - WL) / b) ** 2
    mfar = ((X - cx) / 34) ** 2 + ((my - WL) / 27) ** 2
    refl = np.where(me < 1, np.where(mfar < 1, 0.25, 0.85), np.where(my > 100, 0.5, 0.3))
    depth = (Y - WL) / (238 - WL)
    wd = refl * (1 - 0.45 * depth) + 0.12
    rip = fbm(SW, SH, 14, 3, 14)
    wob = Y + 0.7 * np.sin(X / 5.0 + 3 * rip) + 1.6 * (rip - 0.5)
    gl = noise(SW // 10, SH, 6, 15)  # horizontally stretched ripple highlights
    gl = np.asarray(Image.fromarray((gl * 255).astype(np.uint8)).resize((SW, SH),
                    Image.BICUBIC)).astype(float) / 255
    glint = gl > 0.70
    ink |= water & screen(wob, wd, 3.0) & ~glint
    ink |= np.abs(Y - WL) < 0.5

    a_ = np.full((SH, SW, 3), 255, np.uint8)
    a_[ink] = 0
    im = Image.fromarray(a_)
    d = ImageDraw.Draw(im)

    # the carved stone: Hamilton's rule, in red
    f = F(SERIF_BI, 15)
    rule = "i² = j² = k² = ijk = −1"
    tw = d.textlength(rule, font=f) / S
    px0, px1 = 200 - tw / 2 - 9, 200 + tw / 2 + 9
    d.rectangle(S_(px0, 81.5, px1, 98.5), fill=WHITE, outline=BLACK, width=S)
    text(d, (200, 90.5), rule, f, RED, "mm")

    # header / footer
    d.rectangle(S_(0, 0, W, 21), fill=WHITE)
    text(d, (10, 8), "BROUGHAM BRIDGE · ROYAL CANAL · DUBLIN", F(SERIF_B, 9.5), anchor="lm")
    text(d, (390, 8), "16 October 1843", F(SERIF_I, 11), anchor="rm")
    d.line(S_(10, 17, 390, 17), fill=BLACK, width=S)
    d.rectangle(S_(0, 238, W, H), fill=WHITE)
    d.line(S_(10, 240, 390, 240), fill=BLACK, width=S)
    q = ("“I then and there felt the galvanic circuit of thought close; and the sparks "
         "which fell from it were the fundamental equations between i, j, k.”")
    fq = F(SERIF_I, 10.5)
    for k, ln in enumerate(wrap(d, q, fq, 378)):
        text(d, (11, 246 + k * 13), ln, fq)
    text(d, (11, 286), "— W. R. Hamilton, walking with Lady Hamilton to the Academy",
         F(SERIF, 8.5), anchor="lm")
    mark(d, "i")
    return quantize(im)


# ------------------------------------------- ii. The tally sticks, 1834
def tally(d, x0, y0, length, h, notches, flip=False):
    """A split tally: white wood, V notches cut into the top edge."""
    pts = [(x0, y0)]
    x = x0 + 10
    for wdt, dep in notches:
        pts += [(x, y0), (x + wdt / 2, y0 + dep), (x + wdt, y0)]
        x += wdt + 4
    pts += [(x0 + length - 8, y0), (x0 + length, y0 + h / 2),
            (x0 + length - 8, y0 + h), (x0, y0 + h)]
    d.polygon([(px * S, py * S) for px, py in pts], fill=WHITE, outline=BLACK)
    d.line([(px * S, py * S) for px, py in pts + [pts[0]]], fill=BLACK, width=S)
    return x


def img_tallies():
    X, Y = grid()
    rng = random.Random(1834)
    SKY = 168  # river line
    # flames: a ragged field rising behind the palace, tongues stretched upward
    n1 = fbm(SW, SH, 21, 4, 5)
    n2 = noise(SW, SH, 40, 22)
    cxf = 205
    spread = np.exp(-((X - cxf) / 150) ** 2)
    top = SKY - 30 - 125 * spread * (0.5 + 0.7 * n1) - 14 * n2
    fire = (Y > top) & (Y < SKY)
    # tongues: stretched noise sampled with heavy vertical compression
    tongue = noise(SW, SH // 6, 60, 23)
    tongue = np.asarray(Image.fromarray((tongue * 255).astype(np.uint8)).resize((SW, SH),
                        Image.BICUBIC)).astype(float) / 255
    fire &= ~((tongue > 0.66) & (Y < top + 28 * (tongue - 0.66) / 0.34))
    # smoke: black-on-black is invisible, so smoke is the unlit night; embers are white
    a = np.zeros((SH, SW, 3), np.uint8)
    a[fire] = RED
    # embers rising
    for _ in range(140):
        ex = rng.gauss(cxf, 70)
        ey = rng.uniform(20, SKY - 30)
        ty = (SKY - ey) / SKY
        if rng.random() < 0.85 * ty + 0.1:
            pass
        r_ = rng.choice([0.6, 0.8, 1.0])
        yy0, xx0 = int((ey - r_) * S), int((ex - r_) * S)
        a[max(0, yy0):int((ey + r_) * S), max(0, xx0):int((ex + r_) * S)] = \
            (255, 0, 0) if rng.random() < 0.5 else (255, 255, 255)
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)

    # silhouette of the OLD palace (pre-Barry): Westminster Hall's great roof,
    # St Stephen's Chapel with four pinnacled turrets, sundry roofs
    def P(pts):
        d.polygon([(px * S, py * S) for px, py in pts], fill=BLACK)
    base = SKY
    P([(0, base), (0, 140), (30, 140), (30, 128), (60, 128), (60, 136), (88, 136),
       (88, 124), (96, 124), (96, base)])
    # Westminster Hall: steep gable, lantern
    P([(96, base), (96, 112), (150, 84), (204, 112), (204, base)])
    d.rectangle(S_(144, 70, 156, 88), fill=BLACK)
    P([(143, 70), (150, 58), (157, 70)])
    # St Stephen's chapel: tall block, four turrets with pinnacles
    d.rectangle(S_(214, 96, 266, base), fill=BLACK)
    for tx in (210, 236, 262):
        d.rectangle(S_(tx, 78, tx + 8, base), fill=BLACK)
        P([(tx - 1, 78), (tx + 4, 60), (tx + 9, 78)])
    # Lords / Commons ranges with chimneys and windows lit by fire
    P([(266, base), (266, 118), (300, 118), (300, 108), (330, 108), (330, 124),
       (370, 124), (370, 134), (400, 134), (400, base)])
    for cx_ in (276, 288, 314, 346, 358):
        d.rectangle(S_(cx_, 100 if cx_ < 330 else 116, cx_ + 4, 125), fill=BLACK)
    # lancet windows glowing (red) in chapel and hall
    for wx in range(220, 262, 9):
        d.rectangle(S_(wx, 108, wx + 4, 128), fill=RED)
        d.pieslice(S_(wx, 105, wx + 4, 111), 180, 360, fill=RED)
    for wx in range(108, 196, 12):
        d.rectangle(S_(wx, 128, wx + 4, 148), fill=RED)
        d.pieslice(S_(wx, 125, wx + 4, 131), 180, 360, fill=RED)
    # the river: broken red reflections under the fire
    rr = random.Random(7)
    for k in range(26):
        yv = SKY + 3 + k * 1.75
        spanw = 150 * math.exp(-k / 18)
        x = cxf - spanw
        while x < cxf + spanw:
            seg = rr.uniform(4, 22) * (1 - k / 40)
            if rr.random() < 0.62:
                d.rectangle(S_(x, yv, x + seg, yv + 0.9), fill=RED)
            x += seg + rr.uniform(2, 9)
    d.line(S_(0, SKY, W, SKY), fill=BLACK, width=S)

    # the ledger panel: one Exchequer tally, its notches keyed
    d.rectangle(S_(0, 216, W, H), fill=WHITE)
    d.line(S_(0, 216, W, 216), fill=WHITE, width=S)
    notches = [(18, 9), (18, 9), (10, 7), (10, 7), (10, 7), (5, 5), (2.6, 3), (2.6, 3)]
    tally(d, 14, 224, 150, 13, notches)
    text(d, (14, 245), "£2,322", F(SERIF_B, 10), anchor="la")
    text(d, (14, 257), "palm £1000 · thumb £100", F(SERIF_I, 8.5))
    text(d, (14, 267), "little finger £20 · barleycorn £1", F(SERIF_I, 8.5))
    d.line(S_(176, 222, 176, 284), fill=BLACK, width=S)
    text(d, (186, 223), "16 October 1834", F(SERIF_B, 12))
    body = ("The Exchequer, tidying up an accounting system abolished in 1826, "
            "feeds two cartloads of tally sticks into the Lords' stoves. "
            "By nightfall the Palace of Westminster is ablaze.")
    fb = F(SERIF, 9)
    for k, ln in enumerate(wrap(d, body, fb, 204)):
        text(d, (186, 240 + k * 11), ln, fb)
    text(d, (14, 282), "Turner watched from a boat.", F(SERIF_I, 8.5), anchor="lm")
    mark(d, "ii")
    return quantize(im)


# -------------------------------------------------------- iii. Proun (no words)
def img_proun():
    im, d = canvas()
    rng = random.Random(20261016)

    def poly(pts, fill):
        d.polygon([(px * S, py * S) for px, py in pts], fill=fill)

    def rot(cx, cy, w_, h_, ang):
        c, s = math.cos(ang), math.sin(ang)
        return [(cx + c * x - s * y, cy + s * x + c * y)
                for x, y in ((-w_ / 2, -h_ / 2), (w_ / 2, -h_ / 2),
                             (w_ / 2, h_ / 2), (-w_ / 2, h_ / 2))]

    # the black field, tilted
    tilt = math.radians(-9)
    poly(rot(262, 150, 300, 330, tilt), BLACK)
    # the white disc, bitten into the black
    d.ellipse(S_(186, 62, 338, 214), fill=WHITE)
    # thin long bars crossing the whole sheet
    for (x0, y0, x1, y1, w_) in [(-10, 252, 410, 196, 2.2), (30, 0, 120, 300, 1.4),
                                 (0, 40, 400, 66, 1.0)]:
        d.line(S_(x0, y0, x1, y1), fill=BLACK, width=int(w_ * S))
    # the red wedge, driving into the disc
    poly([(18, 236), (262, 128), (40, 262)], RED)
    # a black splinter answering it, on the white
    poly([(300, 152), (392, 118), (392, 126)], WHITE)
    poly([(60, 60), (128, 96), (54, 70)], BLACK)
    # axonometric block floating at upper left
    bx, by, s_ = 66, 120, 26
    top = [(bx, by), (bx + s_, by - s_ * 0.5), (bx + 2 * s_, by), (bx + s_, by + s_ * 0.5)]
    poly(top, WHITE)
    d.line([(px * S, py * S) for px, py in top + [top[0]]], fill=BLACK, width=S * 2)
    poly([(bx, by), (bx + s_, by + s_ * 0.5), (bx + s_, by + s_ * 1.6), (bx, by + s_ * 1.1)], BLACK)
    poly([(bx + s_, by + s_ * 0.5), (bx + 2 * s_, by), (bx + 2 * s_, by + s_ * 1.1),
          (bx + s_, by + s_ * 1.6)], RED)
    # small scattered rectangles on the black field (white) and the white field (black/red)
    for k, ln in enumerate((54, 34, 18)):
        poly(rot(318 - k * 1.3, 238 + k * 9, ln, 3, tilt), WHITE)
    poly(rot(150, 34, 46, 9, math.radians(-24)), BLACK)
    poly(rot(176, 22, 12, 12, math.radians(-24)), RED)
    d.ellipse(S_(330, 20, 346, 36), fill=RED)
    # a ring around the disc, broken by the wedge
    d.arc(S_(176, 52, 348, 224), 200, 520, fill=RED, width=S * 2)
    mark(d, "iii", ink=WHITE)
    return quantize(im, thresh=120)


# ----------------------------------------- iv. 25 Vendemiaire an CCXXXV: Boeuf
def ox_head(d, cx, cy, s, fill):
    def P(pts, f=fill):
        d.polygon([((cx + px * s) * S, (cy + py * s) * S) for px, py in pts], fill=f)
    # horns: rooted on the poll, sweeping out then up, tapering to a point
    for sg in (-1, 1):
        cl = []
        for k in range(25):
            t = k / 24
            cl.append((sg * (0.45 + 0.95 * math.sin(t * math.pi * 0.55)),
                       -0.62 - 0.05 * t - 0.75 * t ** 2.4))
        left, right = [], []
        for k, (hx, hy) in enumerate(cl):
            t = k / 24
            nx_, ny_ = cl[min(k + 1, 24)][0] - cl[max(k - 1, 0)][0], cl[min(k + 1, 24)][1] - cl[max(k - 1, 0)][1]
            L = math.hypot(nx_, ny_) or 1
            th = 0.17 * (1 - t) ** 0.9 + 0.01
            left.append((hx - ny_ / L * th, hy + nx_ / L * th))
            right.append((hx + ny_ / L * th, hy - nx_ / L * th))
        P(left + right[::-1])
    # ears
    for sg in (-1, 1):
        P([(sg * 0.42, -0.45), (sg * 1.12, -0.5), (sg * 1.02, -0.28), (sg * 0.45, -0.2)])
    # skull and face: a long tapering shield
    P([(-0.55, -0.72), (0.55, -0.72), (0.62, -0.35), (0.42, 0.55), (0.40, 0.95),
       (-0.40, 0.95), (-0.42, 0.55), (-0.62, -0.35)])
    # muzzle
    d.ellipse([((cx - 0.5 * s) * S), ((cy + 0.72 * s) * S), ((cx + 0.5 * s) * S),
               ((cy + 1.22 * s) * S)], fill=fill)
    # white details: eyes, blaze, nostrils
    for sg in (-1, 1):
        ex = cx + sg * 0.33 * s
        d.ellipse([(ex - 0.08 * s) * S, (cy - 0.2 * s) * S, (ex + 0.08 * s) * S, (cy - 0.06 * s) * S],
                  fill=WHITE)
        nx = cx + sg * 0.2 * s
        d.ellipse([(nx - 0.07 * s) * S, (cy + 0.92 * s) * S, (nx + 0.07 * s) * S,
                   (cy + 1.04 * s) * S], fill=WHITE)
    P([(-0.12, -0.6), (0.12, -0.6), (0.0, -0.25)], WHITE)
    # forelock curls
    for k in range(-2, 3):
        d.arc([(cx + (k * 0.16 - 0.07) * s) * S, (cy - 0.78 * s) * S,
               (cx + (k * 0.16 + 0.07) * s) * S, (cy - 0.64 * s) * S], 0, 180, fill=WHITE, width=S)


def img_vendemiaire():
    im, d = canvas()
    # left column: the date as the Republic would print it
    text(d, (14, 12), "CALENDRIER RÉPUBLICAIN", F(SERIF_B, 9))
    d.line(S_(14, 25, 196, 25), fill=BLACK, width=S)
    text(d, (14, 32), "Quintidi", F(SERIF_I, 15))
    text(d, (10, 48), "25", F(SERIF_B, 92))
    text(d, (14, 150), "VENDÉMIAIRE", F(SERIF_B, 19))
    text(d, (14, 172), "an CCXXXV de la République", F(SERIF_I, 11))
    text(d, (14, 188), "month of the grape harvest", F(SERIF_I, 9))
    # right: the day's patron, the ox
    ox_head(d, 296, 92, 52, RED)
    text(d, (296, 176), "BŒUF", F(SERIF_B, 17), anchor="mm")
    text(d, (296, 192), "every fifth day is an animal", F(SERIF_I, 8.5), anchor="mm")
    # the décade strip
    names = ["Chanvre", "Pêche", "Navet", "Amaryllis", "Bœuf",
             "Aubergine", "Piment", "Tomate", "Orge", "Tonneau"]
    eng = ["hemp", "peach", "turnip", "amaryllis", "ox",
           "aubergine", "chilli", "tomato", "barley", "barrel"]
    x0, y0, cw, ch = 10, 212, 38, 56
    d.line(S_(x0, y0 - 3, x0 + 10 * cw, y0 - 3), fill=BLACK, width=S)
    for i in range(10):
        x = x0 + i * cw
        today = i == 4
        if today:
            d.rectangle(S_(x + 1, y0 - 2, x + cw - 1, y0 + ch + 2), outline=RED, width=S * 2)
        col = RED if today else BLACK
        text(d, (x + cw / 2, y0 + 11), str(21 + i), F(SERIF_B, 14), col, "mm")
        fname = F(SERIF, 8.5) if len(names[i]) < 9 else F(SERIF, 7.5)
        text(d, (x + cw / 2, y0 + 28), names[i], fname, col, "mm")
        text(d, (x + cw / 2, y0 + 40), eng[i], F(SERIF_I, 7.5), col, "mm")
        if i and i not in (4, 5):
            d.line(S_(x, y0 + 4, x, y0 + ch - 4), fill=BLACK, width=S)
    d.line(S_(x0, y0 + ch + 3, x0 + 10 * cw, y0 + ch + 3), fill=BLACK, width=S)
    text(d, (10, 289), "décade III · 16 October 2026", F(SERIF_I, 8.5), anchor="lm")
    mark(d, "iv")
    return quantize(im)


# --------------------------------------------------- v. Klangfigur (Chladni)
def img_chladni():
    im, d = canvas(BLACK)
    rng = np.random.default_rng(1016)
    # plate geometry (final px)
    px0, py0, P_ = 22, 22, 256
    n, m = 3, 7
    N = 260000
    x = rng.random(N)
    y = rng.random(N)
    u = (np.cos(n * np.pi * x) * np.cos(m * np.pi * y)
         + np.cos(m * np.pi * x) * np.cos(n * np.pi * y))
    keep = rng.random(N) < np.exp(-(u / 0.07) ** 2)
    xs, ys = x[keep], y[keep]
    a = np.asarray(im).copy()
    ix = ((px0 + xs * P_) * S).astype(int)
    iy = ((py0 + ys * P_) * S).astype(int)
    for dx in (0, 1):
        for dy in (0, 1):
            a[np.clip(iy + dy, 0, SH - 1), np.clip(ix + dx, 0, SW - 1)] = 255
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    # plate edge and the clamp bolt at its centre
    d.rectangle(S_(px0 - 4, py0 - 4, px0 + P_ + 4, py0 + P_ + 4), outline=WHITE, width=S)
    c = px0 + P_ / 2
    d.ellipse(S_(c - 4, c - 4, c + 4, c + 4), fill=RED)
    # the bow, drawn up the right-hand edge, in red
    bx = px0 + P_ + 4
    d.line(S_(bx + 1, 46, bx + 1, 150), fill=RED, width=S)          # hair on the edge
    d.line(S_(bx + 8, 40, bx + 8, 156), fill=RED, width=S * 3)      # stick
    d.line(S_(bx + 1, 46, bx + 8, 40), fill=RED, width=S * 2)       # tip
    d.rectangle(S_(bx + 1, 148, bx + 8, 160), fill=RED)             # frog
    # caption column
    cx_ = 338
    text(d, (cx_, 160), "KLANG-", F(SERIF_B, 14), WHITE, "mm")
    text(d, (cx_, 177), "FIGUR", F(SERIF_B, 14), WHITE, "mm")
    text(d, (cx_, 196), f"mode ({n}, {m})", F(SERIF_B, 11), WHITE, "mm")
    text(d, (cx_, 214), "sand gathers", F(SANS_B, 8.5), WHITE, "mm")
    text(d, (cx_, 226), "where the plate", F(SANS_B, 8.5), WHITE, "mm")
    text(d, (cx_, 238), "stands still", F(SANS_B, 8.5), WHITE, "mm")
    mark(d, "v", ink=WHITE)
    return quantize(im, thresh=120)


if __name__ == "__main__":
    makers = [img_bridge, img_tallies, img_proun, img_vendemiaire, img_chladni]
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    for i, fn in enumerate(makers, 1):
        if only and str(i) not in only:
            continue
        fn().save(f"{OUT}/{i}.png")
        print("wrote", i, fn.__name__)
