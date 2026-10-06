#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-06. (memory: memory-fable-5-1.md)

Theme: "things that pass in front of other things".
  1. Occultation  — this morning the crescent Moon swallowed Jupiter.
  2. Modulor      — Le Corbusier born 6 Oct 1887; a golden-ratio construction.
  3. Euridice     — 6 Oct 1600, the earliest surviving opera. Don't look back.
  4. Draconids    — radiant forecast for Oct 8-9, moonless peak.
  5. Kon-Tiki     — Thor Heyerdahl born 6 Oct 1914; 101 days of woodcut sea.

House style ("almanac woodcut"): tonal layers rendered at 3x and dithered;
then crisp 1x linework/type drawn with NO antialiasing on top; a thin footer
rule with a folio; red reserved for the single thing that matters.
"""
import math, random, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, SS = 400, 300, 3
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
INTER = "/usr/share/fonts/opentype/inter/"
def F(name, size): return ImageFont.truetype(INTER + name + ".otf", size)

_pal = Image.new("P", (1, 1))
_pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)

def dither(img):
    """3x RGB tonal image -> 1x RGB in exact palette (Floyd–Steinberg)."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img.convert("RGB").quantize(palette=_pal, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")

def crisp(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return d

def finish(img, path):
    img.convert("RGB").quantize(palette=_pal, dither=Image.Dither.NONE).save(path, optimize=True)

def footer(d, n, title, ink=BLACK, bg=None):
    f = F("Inter-Medium", 9)
    if bg is not None:
        d.rectangle([0, H - 14, W, H], fill=bg)
    d.line([8, H - 15, W - 8, H - 15], fill=ink)
    d.text((8, H - 13), title.upper(), font=f, fill=ink)
    folio = f"06·X·26  {n}/5"
    w = d.textlength(folio, font=f)
    d.text((W - 8 - w - 8, H - 13), folio, font=f, fill=ink)
    d.rectangle([W - 13, H - 11, W - 9, H - 7], fill=RED)   # the red seal

def tw(d, s, f): return d.textlength(s, font=f)


# ----------------------------------------------------------------- 1. Occultation
def img_occultation(path):
    s = SS
    big = Image.new("RGB", (W * s, H * s), BLACK)
    a = np.zeros((H * s, W * s), np.float32)
    yy, xx = np.mgrid[0:H * s, 0:W * s].astype(np.float32)
    cx, cy, R = 200 * s, 128 * s, 92 * s
    # waning crescent, 20% lit, lit limb on the LEFT (east, toward the dawn sun)
    r = np.hypot(xx - cx, yy - cy)
    disc = r < R
    k = 0.6  # terminator ellipse half-width ratio (20% illum -> 1-2*0.2)
    xn = (xx - cx) / R
    yn = (yy - cy) / R
    term = -k * np.sqrt(np.clip(1 - yn ** 2, 0, 1))  # terminator x
    lit = disc & (xn < term)
    # limb darkening + a little mare texture
    rng = np.random.default_rng(20261006)
    noise = np.zeros_like(a)
    for sc, amp in [(40, .25), (14, .12), (5, .06)]:
        g = rng.random((H * s // sc + 2, W * s // sc + 2)).astype(np.float32)
        gi = np.array(Image.fromarray((g * 255).astype(np.uint8)).resize((W * s + 2 * sc, H * s + 2 * sc), Image.BICUBIC), np.float32)[:H * s, :W * s] / 255
        noise += (gi - .5) * amp
    shade = np.clip(1 - 0.35 * (r / R) ** 3 + noise, 0, 1)
    # soft terminator falloff
    soft = np.clip((term - xn) / 0.12, 0, 1)
    a = np.where(disc, shade * soft * 0.97, 0)
    # earthshine: barely there
    a = np.where(disc & ~lit, np.maximum(a, 0.07 + noise * 0.05), a)
    # a few stars
    for _ in range(140):
        x, y = rng.integers(0, W * s), rng.integers(0, H * s)
        if np.hypot(x - cx, y - cy) > R + 10 * s:
            b = rng.random() ** 3
            a[max(0, y - 1):y + 2, max(0, x - 1):x + 2] = np.maximum(a[max(0, y - 1):y + 2, max(0, x - 1):x + 2], b)
    big = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGB")
    img = dither(big)
    d = crisp(img)
    # Jupiter's path across the disc, left (bright limb) to right (dark limb)
    py = 128 - 30  # chord above center
    x_in = 200 - math.sqrt(92 ** 2 - 30 ** 2)
    x_out = 200 + math.sqrt(92 ** 2 - 30 ** 2)
    # dotted path where it's hidden — drawn in red on the moon
    for x in range(int(x_in) + 3, int(x_out) - 2, 5):
        d.point((x, py), fill=RED)
    # Jupiter beads approaching and leaving (positions every ~20 min)
    def jup(x, rad=4):
        d.ellipse([x - rad, py - rad, x + rad, py + rad], fill=RED)
        d.line([x - rad + 1, py - 1, x + rad - 1, py - 1], fill=BLACK)
        d.line([x - rad + 2, py + 1, x + rad - 2, py + 1], fill=BLACK)
    for i, x in enumerate([24, 50, 76, x_in - 2]):
        jup(int(x), 2 + i if i < 3 else 5)
    for i, x in enumerate([x_out + 2, 324, 350, 376]):
        jup(int(x), 5 - i if i else 5)
    # tick labels
    f9 = F("Inter-Medium", 9)
    fb = F("InterDisplay-Bold", 13)
    def lab(x, t1, t2, side):
        # leader drops then runs outward, away from the disc
        ex = x + side * 16
        d.line([x, py + 8, x, py + 26, ex, py + 26], fill=WHITE)
        w1 = tw(d, t1, fb); w2 = tw(d, t2, f9)
        tx = ex + 3 if side > 0 else ex - 3 - max(w1, w2)
        d.text((tx, py + 18), t1, font=fb, fill=WHITE)
        d.text((tx, py + 33), t2, font=f9, fill=WHITE)
    lab(int(x_in - 2), "08:22", "BRIGHT LIMB", -1)
    lab(int(x_out + 2), "09:29", "DARK LIMB", 1)
    # title block
    ft = F("InterDisplay-Black", 26)
    d.text((10, 228), "OCCULTATION", font=ft, fill=WHITE)
    fs = F("Inter-Regular", 10)
    d.text((10, 258), "Moon 20%, waning · Jupiter hidden 67 min · times UTC", font=fs, fill=WHITE)
    d.text((10, 270), "Seen from eastern N. America, before dawn", font=fs, fill=WHITE)
    fl = F("Inter-Medium", 9)
    d.text((10, 8), "E", font=fl, fill=WHITE); d.text((W - 16, 8), "W", font=fl, fill=WHITE)
    d.line([20, 13, 40, 13], fill=WHITE); d.line([W - 40, 13, W - 22, 13], fill=WHITE)
    footer(d, 1, "This morning", ink=WHITE)
    finish(img, path)


# ----------------------------------------------------------------- 2. Modulor
def img_modulor(path):
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    phi = (1 + 5 ** .5) / 2
    rng = random.Random(1887)
    # Golden-rectangle recursive subdivision of the left panel (red/black/white)
    def split(x, y, w, h, depth, col_i):
        if depth == 0 or w < 6 or h < 6:
            return
        if w >= h:
            sq = h if h <= w else w
            sq = min(sq, w)
            a = (x, y, x + sq, y + h)
            rest = (x + sq, y, w - sq, h)
        else:
            sq = w
            a = (x, y, x + w, y + sq)
            rest = (x, y + sq, w, h - sq)
        c = [WHITE, BLACK, RED, WHITE, WHITE][col_i % 5]
        d.rectangle(a, fill=c, outline=BLACK, width=2)
        # quarter arc of the golden spiral
        split(*rest, depth - 1, col_i + 1)
    # spiral drawn after: rebuild with arc
    px, py, pw = 12, 12, 214
    ph = pw / phi
    # rotate the subdivision direction each step to make the true spiral
    def spiral(x, y, w, h, k, depth):
        cols = [RED, WHITE, BLACK, WHITE, RED, WHITE, BLACK, WHITE, WHITE, WHITE]
        boxes = []
        for i in range(depth):
            if w < 3 or h < 3: break
            dirn = (k + i) % 4
            if dirn == 0:   # square on left
                sq = h; box = (x, y, x + sq, y + h); x += sq; w -= sq
            elif dirn == 1: # square on top
                sq = w; box = (x, y, x + w, y + sq); y += sq; h -= sq
            elif dirn == 2: # square on right
                sq = h; box = (x + w - sq, y, x + w, y + h); w -= sq
            else:           # square on bottom
                sq = w; box = (x, y + h - sq, x + w, y + h); h -= sq
            boxes.append((box, dirn, cols[i % len(cols)]))
        return boxes
    boxes = spiral(px, py, pw, ph, 0, 9)
    for box, dirn, c in boxes:
        d.rectangle([round(v) for v in box], fill=c, outline=BLACK, width=2)
    # golden spiral arcs, in the opposite ink
    for box, dirn, c in boxes:
        x0, y0, x1, y1 = box
        sq = x1 - x0
        # corner for arc centre depends on direction
        if dirn == 0: cx, cy, st = x1, y1, 180
        elif dirn == 1: cx, cy, st = x0, y1, 270
        elif dirn == 2: cx, cy, st = x0, y0, 0
        else: cx, cy, st = x1, y0, 90
        ink = WHITE if c in (BLACK, RED) else BLACK
        d.arc([cx - sq, cy - sq, cx + sq, cy + sq], st, st + 90, fill=ink, width=2)
    # Modulor man: geometric figure on the right, height 183 units -> pixels
    base = 262; scale = 1.15  # px per cm
    fx = 300
    def Y(cm): return base - cm * scale
    # ladders: red series (27,43,70,113,183) left of figure, "blue" (black) series right
    red = [27, 43, 70, 113, 183]
    blue = [33, 53, 86, 140, 226]
    lx, rx = 256, 352
    d.line([lx, Y(0), lx, Y(183)], fill=RED, width=3)
    for v in red:
        d.line([lx - 5, Y(v), lx + 5, Y(v)], fill=RED, width=2)
        t = str(v); f = F("Inter-Bold", 9)
        d.text((lx - 9 - tw(d, t, f), Y(v) - 6), t, font=f, fill=RED)
    d.line([rx, Y(0), rx, Y(226)], fill=BLACK, width=3)
    for v in blue:
        d.line([rx - 5, Y(v), rx + 5, Y(v)], fill=BLACK, width=2)
        f = F("Inter-Bold", 9)
        d.text((rx + 9, Y(v) - 6), str(v), font=f, fill=BLACK)
    # the man, built from the measures: head, torso, raised arm to 226
    head_r = 11
    hy = Y(183) + head_r
    d.ellipse([fx - head_r, hy - head_r, fx + head_r, hy + head_r], fill=BLACK)
    sh = Y(150); hip = Y(98); knee = Y(50); navel = Y(113)
    d.polygon([(fx - 16, sh), (fx + 14, sh), (fx + 10, hip), (fx - 12, hip)], fill=BLACK)
    # legs
    d.polygon([(fx - 12, hip), (fx - 1, hip), (fx - 6, Y(0)), (fx - 18, Y(0))], fill=BLACK)
    d.polygon([(fx + 1, hip), (fx + 10, hip), (fx + 12, Y(0)), (fx + 3, Y(0))], fill=BLACK)
    d.line([fx - 18, Y(0), fx - 30, Y(0)], fill=BLACK, width=4)
    d.line([fx + 12, Y(0), fx + 22, Y(0)], fill=BLACK, width=4)
    # raised right arm reaching to 226
    d.line([fx + 12, sh + 2, fx + 20, Y(226) + 4], fill=BLACK, width=7)
    d.ellipse([fx + 15, Y(226), fx + 25, Y(226) + 10], fill=BLACK)
    # lowered left arm, hand at 86
    d.line([fx - 14, sh + 2, fx - 20, Y(86)], fill=BLACK, width=6)
    # navel — the golden point
    d.ellipse([fx - 3, navel - 3, fx + 3, navel + 3], fill=RED)
    d.line([lx + 6, navel, fx - 5, navel], fill=RED)
    d.line([fx - 30, Y(0) + 2, rx + 2, Y(0) + 2], fill=BLACK, width=2)
    # caption under the spiral
    ft = F("InterDisplay-Black", 22)
    d.text((12, 166), "LE MODULOR", font=ft, fill=BLACK)
    fs = F("Inter-Regular", 10)
    lines = ["Charles-Édouard Jeanneret,",
             "\"Le Corbusier\", born today 1887.",
             "A man 183 cm tall, navel at 113,",
             "hand raised to 226. Every step",
             "on the ladder is the last × φ."]
    for i, l in enumerate(lines):
        d.text((12, 196 + i * 13), l, font=fs, fill=BLACK)
    d.text((168, 254), "φ = 1.618…", font=F("Inter-SemiBold", 10), fill=RED)
    footer(d, 2, "139 years")
    finish(img, path)


# ----------------------------------------------------------------- 3. Euridice
def img_euridice(path):
    s = SS
    big = Image.new("L", (W * s, H * s), 255)
    d = ImageDraw.Draw(big)
    # receding arches: a tunnel into the underworld, getting darker with depth
    vx, vy = 200 * s, 150 * s
    n = 26
    for i in range(n):
        t = i / (n - 1)
        sc = (1 - t) ** 1.7
        w = 380 * s * sc + 6 * s
        h = 300 * s * sc + 8 * s
        x0, x1 = vx - w / 2, vx + w / 2
        ytop = vy - h * 0.55 + t * 18 * s
        ybot = vy + h * 0.45 - t * 6 * s
        ybot = max(ybot, ytop + w * 0.3 + 2)
        tone = int(255 * (1 - t) ** 0.6 * 0.95)
        ring = int(tone * 0.55)
        # arch = rectangle bottom + half-ellipse top
        rr = w / 2
        d.rectangle([x0, ytop + rr * 0.6, x1, ybot], fill=ring)
        d.ellipse([x0, ytop, x1, ytop + rr * 1.2], fill=ring)
        inset = max(2, w * 0.045)
        d.rectangle([x0 + inset, ytop + rr * 0.6, x1 - inset, ybot], fill=tone)
        d.ellipse([x0 + inset, ytop + inset, x1 - inset, ytop + rr * 1.2 - inset], fill=tone)
    # floor steps lines
    for i in range(14):
        t = i / 13
        y = vy + (1 - t) ** 1.7 * 135 * s + 14 * s
        half = (1 - t) ** 1.7 * 190 * s + 4 * s
        d.line([vx - half, y, vx + half, y], fill=int(120 * (1 - t)), width=s)
    img = dither(big.convert("RGB"))
    dd = crisp(img)
    # two figures: Orpheus ahead (white silhouette going up toward us),
    # Euridice behind in red, deeper in the tunnel.
    def figure(x, y, hgt, col, outline=None):
        hr = hgt * 0.11
        dd.ellipse([x - hr, y - hgt, x + hr, y - hgt + 2 * hr], fill=col, outline=outline)
        dd.polygon([(x - hgt * .16, y - hgt + 2.3 * hr), (x + hgt * .16, y - hgt + 2.3 * hr),
                    (x + hgt * .22, y), (x - hgt * .22, y)], fill=col, outline=outline)
    figure(196, 156, 15, RED)          # Euridice, deep in the dark, following
    figure(206, 232, 56, BLACK, outline=WHITE)
    # lyre on Orpheus
    dd.arc([213, 196, 227, 216], 180, 360, fill=WHITE)
    for k in range(3): dd.line([216 + k * 2, 200, 216 + k * 2, 212], fill=WHITE)
    # title
    ft = F("InterDisplay-Black", 24)
    t = "EURIDICE"
    dd.rectangle([0, 0, W, 34], fill=WHITE)
    dd.text(((W - tw(dd, t, ft)) / 2, 3), t, font=ft, fill=BLACK)
    fs = F("Inter-Medium", 9)
    sub = "PALAZZO PITTI, FIRENZE · 6 OCTOBER 1600 · THE OLDEST OPERA THAT SURVIVES"
    dd.rectangle([0, 34, W, 46], fill=WHITE)
    dd.text(((W - tw(dd, sub, fs)) / 2, 34), sub, font=fs, fill=BLACK)
    dd.rectangle([0, 240, W, H], fill=WHITE)
    fq = F("Inter-SemiBoldItalic", 13)
    q = "Whatever you do, don't look back."
    dd.text(((W - tw(dd, q, fq)) / 2, 248), q, font=fq, fill=RED)
    fs2 = F("Inter-Regular", 9)
    q2 = "Peri himself sang Orfeo. (Rinuccini let them both live — it was a wedding.)"
    dd.text(((W - tw(dd, q2, fs2)) / 2, 266), q2, font=fs2, fill=BLACK)
    footer(dd, 3, "426 years")
    finish(img, path)


# ----------------------------------------------------------------- 4. Draconids
def img_draconids(path):
    rng = random.Random(9)
    img = Image.new("RGB", (W, H), WHITE)   # inverted sky: white paper, black stars
    d = crisp(img)
    ra0, dec0 = 17.47 * 15, 54.0
    def proj(ra_h, dec):
        ra = ra_h * 15
        # gnomonic projection about the radiant
        a, dd_, a0, d0 = map(math.radians, (ra, dec, ra0, dec0))
        c = math.sin(d0) * math.sin(dd_) + math.cos(d0) * math.cos(dd_) * math.cos(a - a0)
        x = math.cos(dd_) * math.sin(a - a0) / c
        y = (math.cos(d0) * math.sin(dd_) - math.sin(d0) * math.cos(dd_) * math.cos(a - a0)) / c
        k = 230
        return 228 - x * k, 140 - y * k     # east to the left
    stars = {
        "λ": (11.52, 69.33, 3.8), "κ": (12.56, 69.79, 3.9), "α": (14.07, 64.38, 3.7),
        "ι": (15.42, 58.97, 3.3), "θ": (16.03, 58.57, 4.0), "η": (16.40, 61.51, 2.7),
        "ζ": (17.15, 65.71, 3.2), "ω": (17.62, 68.76, 4.8), "δ": (19.21, 67.66, 3.1),
        "ε": (19.80, 70.27, 3.8), "χ": (18.35, 72.73, 3.6), "ξ": (17.89, 56.87, 3.7),
        "ν": (17.54, 55.18, 4.9), "β": (17.51, 52.30, 2.8), "γ": (17.94, 51.49, 2.2),
    }
    P = {k: proj(v[0], v[1]) for k, v in stars.items()}
    # meteors radiating from the radiant (don't start AT it — they appear some way out)
    rx, ry = proj(17.47, 54.0)
    for i in range(46):
        ang = rng.uniform(0, 2 * math.pi)
        r0 = rng.uniform(30, 190)
        L = rng.uniform(14, 60) * (0.5 + r0 / 190)
        x0, y0 = rx + math.cos(ang) * r0, ry + math.sin(ang) * r0
        x1, y1 = rx + math.cos(ang) * (r0 + L), ry + math.sin(ang) * (r0 + L)
        # tapered streak: thin tail near radiant, thicker head
        steps = int(L)
        for j in range(steps):
            t = j / steps
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            if t < 0.5 and j % 2: continue
            wdt = 0 if t < 0.75 else 1
            d.ellipse([px - wdt, py - wdt, px + wdt, py + wdt], fill=BLACK)
    # one bright red fireball
    ang = math.radians(150); r0 = 60; L = 120
    x0, y0 = rx + math.cos(ang) * r0, ry + math.sin(ang) * r0
    x1, y1 = rx + math.cos(ang) * (r0 + L), ry + math.sin(ang) * (r0 + L)
    for j in range(L):
        t = j / L
        px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        w = t * 3
        d.ellipse([px - w, py - w, px + w, py + w], fill=RED)
    d.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=RED)
    # constellation lines, white gap outline then black
    lines = ["λκ", "κα", "αι", "ιθ", "θη", "ηζ", "ζω", "ωχ", "χε", "εδ", "δξ", "ξν", "νβ", "βγ", "γξ"]
    for a_, b_ in lines:
        d.line([P[a_], P[b_]], fill=WHITE, width=5)
    for a_, b_ in lines:
        d.line([P[a_], P[b_]], fill=BLACK, width=1)
    for k, (ra, dec, mag) in stars.items():
        x, y = P[k]
        r = max(1.5, (5.2 - mag) * 1.6)
        d.ellipse([x - r - 2, y - r - 2, x + r + 2, y + r + 2], fill=WHITE)
        d.ellipse([x - r, y - r, x + r, y + r], fill=BLACK)
    # radiant marker
    d.ellipse([rx - 7, ry - 7, rx + 7, ry + 7], outline=RED, width=2)
    d.line([rx - 12, ry, rx - 9, ry], fill=RED); d.line([rx + 9, ry, rx + 12, ry], fill=RED)
    d.line([rx, ry - 12, rx, ry - 9], fill=RED); d.line([rx, ry + 9, rx, ry + 12], fill=RED)
    f9 = F("Inter-Medium", 9)
    gx, gy = P["γ"]; d.text((gx - 44, gy + 4), "Eltanin", font=f9, fill=BLACK)
    tx, ty = P["α"]; d.text((tx - 40, ty - 4), "Thuban", font=f9, fill=BLACK)
    # info block, top-left, on white
    d.rectangle([0, 0, 150, 92], fill=WHITE)
    d.text((10, 8), "DRACONIDS", font=F("InterDisplay-Black", 22), fill=BLACK)
    fs = F("Inter-Regular", 10)
    for i, l in enumerate(["Peak: 9 Oct, 01:00 UTC", "Look: at dusk, north-west",
                           "Rate: ~5 / hour", "Moon: absent. Perfect."]):
        d.text((10, 36 + i * 13), l, font=fs, fill=RED if i == 3 else BLACK)
    # countdown
    d.rectangle([W - 70, 8, W - 8, 62], outline=BLACK, width=2)
    fn = F("InterDisplay-Black", 30)
    d.text((W - 39 - tw(d, "2", fn) / 2, 10), "2", font=fn, fill=RED)
    d.text((W - 39 - tw(d, "NIGHTS", f9) / 2, 47), "NIGHTS", font=f9, fill=BLACK)
    d.text((10, 260), "Dust from comet 21P/Giacobini–Zinner,", font=fs, fill=BLACK)
    d.text((10, 272), "falling out of the dragon's head.", font=fs, fill=BLACK)
    footer(d, 4, "Forecast")
    finish(img, path)


# ----------------------------------------------------------------- 5. Kon-Tiki
def img_kontiki(path):
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    rng = random.Random(1947)
    horizon = 132
    # sky: horizontal woodcut hatching getting sparser upward; a sun disc carved out
    sx, sy, sr = 318, 70, 30
    for y in range(4, horizon, 3):
        density = (y / horizon) ** 1.6
        x = 0
        while x < W:
            seg = rng.randint(6, 40)
            if rng.random() < density * 0.9 + 0.05:
                for xx in range(x, min(W, x + seg)):
                    if math.hypot(xx - sx, y - sy) > sr + 5:
                        d.point((xx, y), fill=BLACK)
            x += seg + rng.randint(2, 10)
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=BLACK, width=2)
    # sea: 101 wave rows, one per day of the voyage, carved in black
    rows = 101
    for i in range(rows):
        t = i / (rows - 1)
        y0 = horizon + (H - 20 - horizon) * t ** 1.35
        amp = 0.6 + 5 * t
        freq = 0.09 / (0.35 + t)
        ph = rng.uniform(0, 6.28)
        pts = []
        for x in range(0, W + 1, 2):
            y = y0 + amp * math.sin(x * freq + ph) + amp * 0.5 * math.sin(x * freq * 2.3 + ph * 1.7)
            pts.append((x, y))
        d.line(pts, fill=BLACK, width=1 if t < 0.55 else 2)
    # mark day 101 (Raroia) — the last row — little red tick at right
    # raft — clear a patch of calm water first
    rxc, ryc = 140, 196
    d.polygon([(rxc - 66, ryc - 3), (rxc + 62, ryc - 5), (rxc + 54, ryc + 14), (rxc - 60, ryc + 16)], fill=WHITE)
    d.polygon([(rxc - 62, ryc), (rxc + 58, ryc - 2), (rxc + 50, ryc + 10), (rxc - 56, ryc + 12)], fill=BLACK)
    for k in range(9):
        x = rxc - 56 + k * 13
        d.line([x, ryc + 1, x + 2, ryc + 10], fill=WHITE)
    # cabin
    d.polygon([(rxc - 4, ryc - 1), (rxc + 30, ryc - 2), (rxc + 26, ryc - 20), (rxc + 2, ryc - 20)], fill=BLACK)
    d.line([rxc, ryc - 21, rxc + 14, ryc - 30, rxc + 28, ryc - 21], fill=BLACK, width=3)
    # A-frame mast
    top = (rxc - 16, ryc - 112)
    d.line([(rxc - 34, ryc), top], fill=BLACK, width=3)
    d.line([(rxc + 2, ryc), top], fill=BLACK, width=3)
    # square sail with the red Tiki face
    sl, st, sr_, sb = rxc - 58, ryc - 104, rxc + 26, ryc - 26
    d.line([sl - 4, st, sr_ + 4, st], fill=BLACK, width=3)
    d.rectangle([sl, st + 2, sr_, sb], fill=WHITE, outline=BLACK, width=2)
    fcx, fcy = (sl + sr_) / 2, (st + sb) / 2 + 2
    # Tiki: bearded sun-face, after Erik Hesselberg's sail
    d.ellipse([fcx - 30, fcy - 32, fcx + 30, fcy + 30], fill=RED)
    for k in range(14):  # radiating hair/rays
        a = math.pi + k * math.pi / 13
        d.line([fcx + math.cos(a) * 28, fcy + math.sin(a) * 30,
                fcx + math.cos(a) * 36, fcy + math.sin(a) * 37], fill=RED, width=3)
    d.ellipse([fcx - 18, fcy - 12, fcx - 6, fcy - 2], fill=WHITE)
    d.ellipse([fcx + 6, fcy - 12, fcx + 18, fcy - 2], fill=WHITE)
    d.ellipse([fcx - 14, fcy - 9, fcx - 9, fcy - 4], fill=BLACK)
    d.ellipse([fcx + 9, fcy - 9, fcx + 14, fcy - 4], fill=BLACK)
    d.line([fcx - 20, fcy - 17, fcx - 5, fcy - 14], fill=BLACK, width=2)
    d.line([fcx + 5, fcy - 14, fcx + 20, fcy - 17], fill=BLACK, width=2)
    d.polygon([(fcx, fcy - 6), (fcx - 6, fcy + 6), (fcx + 6, fcy + 6)], fill=BLACK)
    d.rectangle([fcx - 14, fcy + 11, fcx + 14, fcy + 16], fill=WHITE)
    for k in range(-12, 14, 4):
        d.line([fcx + k, fcy + 11, fcx + k, fcy + 16], fill=BLACK)
    # whitewater under the raft
    d.line([rxc - 66, ryc + 13, rxc + 60, ryc + 11], fill=WHITE, width=3)
    # title
    d.rectangle([0, 0, 168, 50], fill=WHITE)
    d.text((10, 6), "KON-TIKI", font=F("InterDisplay-Black", 26), fill=BLACK)
    d.text((10, 36), "Thor Heyerdahl, born 6 Oct 1914", font=F("Inter-Medium", 9), fill=BLACK)
    # legend in the sea
    f9 = F("Inter-Bold", 9)
    lbl = " 101 LINES = 101 DAYS · CALLAO → RAROIA, 1947 "
    wl = tw(d, lbl, f9)
    d.rectangle([W - wl - 10, 262, W - 8, 276], fill=WHITE, outline=BLACK)
    d.text((W - wl - 9, 263), lbl, font=f9, fill=BLACK)
    footer(d, 5, "Balsa, rope, nerve", bg=WHITE)
    finish(img, path)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    for i, fn in enumerate([img_occultation, img_modulor, img_euridice, img_draconids, img_kontiki], 1):
        fn(os.path.join(out, f"{i}.png"))
        print("wrote", i)
