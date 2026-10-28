#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-27.

Hooks for today: Roy Lichtenstein born 27 Oct 1923; the first New York
subway (IRT, 28 stations) opened 27 Oct 1904; the Hunter's Moon was full
yesterday and slides toward the Pleiades tomorrow night; Chladni's sand
figures (1787); Turing's morphogenesis (1952).

Five 400x300 images in exactly three colors (white, black, red).
Hard-edged work is drawn at 3x and downscaled with a no-dither snap
to the palette, so edges stay crisp and nothing turns to mush.
"""

import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_COND_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F_INTER_X = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"


def font(path, size):
    return ImageFont.truetype(path, size)


_pal = Image.new("P", (1, 1))
_pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)


def finalize(img, dither=False):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=_pal, dither=d)


def canvas(color=WHITE, s=SS):
    img = Image.new("RGB", (W * s, H * s), color)
    return img, ImageDraw.Draw(img)


def text_box(dr, xy, lines, fnt, pad, s=SS, fill=WHITE, ink=BLACK, border=2):
    """Comic-style caption box at 1x coordinates; returns its bbox."""
    x, y = xy
    lh = fnt.size * 1.15
    w = max(dr.textlength(l, font=fnt) for l in lines)
    box = (x * s, y * s, x * s + w + 2 * pad * s, y * s + lh * len(lines) + 2 * pad * s)
    dr.rectangle(box, fill=fill, outline=ink, width=border * s)
    for i, l in enumerate(lines):
        dr.text((box[0] + pad * s, box[1] + pad * s + i * lh), l, font=fnt, fill=ink)
    return box


# ------------------------------------------------- 1. Meanwhile, above Manhattan
def image1_pop_moon():
    """Lichtenstein's 103rd birthday: the day-after-full Hunter's Moon in Ben-Day dots."""
    s = SS
    img, dr = canvas(WHITE)
    # Ben-Day sky: red dots on a staggered grid, growing toward the horizon
    step = 8 * s
    for j, y in enumerate(range(0, H * s + step, step)):
        off = step // 2 if j % 2 else 0
        t = y / (H * s)
        r = (0.9 + 2.9 * t ** 1.3) * s
        for x in range(-step, W * s + step, step):
            cx = x + off
            dr.ellipse((cx - r, y - r, cx + r, y + r), fill=RED)

    # the moon, 1.6 days past full: lit disc, thin shadowed east limb in hatching
    mx, my, mr = 255 * s, 112 * s, 72 * s
    dr.ellipse((mx - mr - 4 * s, my - mr - 4 * s, mx + mr + 4 * s, my + mr + 4 * s), fill=BLACK)
    moon = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(moon)
    md.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=255)
    img.paste(WHITE, mask=moon)
    # terminator: waning gibbous ~97% lit; shadow is a slim crescent on the east limb.
    # lit = left half-disc + terminator half-ellipse; shadow = right half-disc minus that ellipse
    k = 0.84  # exaggerated a touch from the true 0.94 so it reads at this size
    shadow = Image.new("L", img.size, 0)
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=255)
    sd.rectangle((0, 0, mx, H * s), fill=0)
    sd.ellipse((mx - k * mr, my - mr, mx + k * mr, my + mr), fill=0)
    hatch = Image.new("RGB", img.size, WHITE)
    hd = ImageDraw.Draw(hatch)
    for x in range(-H * s, W * s, 5 * s):
        hd.line((x, 0, x + H * s, H * s), fill=BLACK, width=2 * s)
    img.paste(hatch, mask=shadow)
    # maria: patches of small black Ben-Day dots, no outlines, the way Roy shaded
    maria = Image.new("L", img.size, 0)
    mdr = ImageDraw.Draw(maria)
    for (dx, dy, rx, ry) in [(-30, -22, 20, 15), (-6, -34, 15, 11), (-40, 10, 15, 22),
                              (6, 0, 13, 10), (-14, 30, 13, 9), (22, -20, 10, 13), (-22, -2, 10, 8)]:
        mdr.ellipse((mx + (dx - rx) * s, my + (dy - ry) * s, mx + (dx + rx) * s, my + (dy + ry) * s), fill=255)
    dots = Image.new("RGB", img.size, WHITE)
    dd = ImageDraw.Draw(dots)
    st = 5 * s
    for j, y in enumerate(range(0, H * s, st)):
        off = st // 2 if j % 2 else 0
        for x in range(0, W * s, st):
            dd.ellipse((x + off - 1.3 * s, y - 1.3 * s, x + off + 1.3 * s, y + 1.3 * s), fill=BLACK)
    img.paste(dots, mask=maria)
    # Tycho with rays
    tx, ty = mx - 6 * s, my + 52 * s
    dr.ellipse((tx - 4 * s, ty - 4 * s, tx + 4 * s, ty + 4 * s), fill=BLACK)
    for a in range(0, 360, 40):
        ra = math.radians(a + 15)
        dr.line((tx + 7 * s * math.cos(ra), ty + 7 * s * math.sin(ra),
                 tx + 15 * s * math.cos(ra), ty + 15 * s * math.sin(ra)), fill=BLACK, width=s)
    # re-ink the limb so hatching never leaks
    dr.ellipse((mx - mr, my - mr, mx + mr, my + mr), outline=BLACK, width=3 * s)

    # the Pleiades waiting up-left for tomorrow night
    def star(x, y, r):
        x, y = x * s, y * s
        dr.polygon([(x, y - r * s), (x + r * 0.28 * s, y - r * 0.28 * s), (x + r * s, y),
                    (x + r * 0.28 * s, y + r * 0.28 * s), (x, y + r * s), (x - r * 0.28 * s, y + r * 0.28 * s),
                    (x - r * s, y), (x - r * 0.28 * s, y - r * 0.28 * s)], fill=BLACK)
    for (x, y, r) in [(92, 92, 9), (106, 82, 6), (80, 106, 6), (116, 98, 7), (100, 108, 5), (126, 84, 5), (88, 74, 4)]:
        star(x, y, r)

    # skyline: solid black, white windows, one red
    rng = random.Random(1923)
    x = 0
    while x < W:
        bw = rng.randint(18, 42)
        bh = rng.randint(30, 82)
        top = H - bh
        dr.rectangle((x * s, top * s, (x + bw) * s, H * s), fill=BLACK)
        if rng.random() < 0.25:
            dr.rectangle(((x + bw // 2 - 2) * s, (top - 14) * s, (x + bw // 2 + 2) * s, top * s), fill=BLACK)
        for wy in range(top + 6, H - 4, 9):
            for wx in range(x + 4, x + bw - 5, 7):
                if rng.random() < 0.28:
                    dr.rectangle((wx * s, wy * s, (wx + 3) * s, (wy + 4) * s), fill=WHITE)
        x += bw + rng.randint(0, 3)
    # one lit studio window, red
    dr.rectangle((60 * s, 262 * s, 66 * s, 268 * s), fill=RED)

    cap = font(F_COND_B, 11 * s)
    text_box(dr, (8, 8), ["MEANWHILE, ABOVE MANHATTAN,", "THE HUNTER'S MOON STARTS", "TO WANE..."], cap, 5)
    text_box(dr, (246, 196), ["27 OCT 1923 — A BOY IS", "BORN WHO WILL PAINT", "EVERY SINGLE DOT."], cap, 5)
    # panel border
    dr.rectangle((0, 0, W * s - 1, H * s - 1), outline=BLACK, width=5 * s)
    return finalize(img)


# ---------------------------------------------- 2. Beat the dark with the red train
def image2_wedge():
    """Suprematist poster for the subway's birthday, after Lissitzky (1919)."""
    s = SS
    img, dr = canvas(WHITE)
    # the underground: black field, split on a slant
    dr.polygon([(170 * s, 0), (W * s, 0), (W * s, H * s), (230 * s, H * s)], fill=BLACK)
    # tunnel mouth: the white circle
    cx, cy, r = 292 * s, 150 * s, 74 * s
    dr.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE)
    # the red wedge: the first train, driven by the mayor himself
    tip = (300 * s, 146 * s)
    dr.polygon([(28 * s, 70 * s), (64 * s, 212 * s), tip], fill=RED)
    # concentric track ties inside the tunnel, receding
    for i, rr in enumerate([58, 44, 32, 22, 14]):
        w = 2 * s if i < 3 else s
        dr.arc((cx - rr * s, cy - rr * s, cx + rr * s, cy + rr * s), 200, 340, fill=BLACK, width=w)
    # flying suprematist debris
    dr.rectangle((196 * s, 236 * s, 214 * s, 290 * s), fill=RED)
    dr.polygon([(330 * s, 18 * s), (390 * s, 30 * s), (386 * s, 40 * s), (326 * s, 28 * s)], fill=WHITE)
    dr.rectangle((20 * s, 240 * s, 120 * s, 246 * s), fill=BLACK)
    dr.rectangle((20 * s, 252 * s, 70 * s, 256 * s), fill=BLACK)
    dr.ellipse((356 * s, 250 * s, 372 * s, 266 * s), fill=RED)
    dr.ellipse((132 * s, 30 * s, 144 * s, 42 * s), fill=BLACK)

    # diagonal type along the wedge, Lissitzky-style
    def rotated_text(txt, fnt, color, center, angle, bg=(0, 0, 0, 0)):
        tw = int(dr.textlength(txt, font=fnt)) + 8
        th = int(fnt.size * 1.4)
        layer = Image.new("RGBA", (tw, th), bg)
        ImageDraw.Draw(layer).text((4, 0), txt, font=fnt, fill=color)
        layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
        img.paste(layer, (int(center[0] - layer.width / 2), int(center[1] - layer.height / 2)), layer)

    ang = -math.degrees(math.atan2(146 - 141, 300 - 46))
    rotated_text("27·X·1904", font(F_INTER_X, 26 * s), WHITE, (150 * s, 140 * s), ang)
    rotated_text("9.1 MILES", font(F_INTER_X, 13 * s), BLACK, (92 * s, 56 * s), 18)
    rotated_text("28 STATIONS", font(F_INTER_X, 13 * s), BLACK, (78 * s, 228 * s), -14)
    big = font(F_INTER_X, 42 * s)
    dr.text((12 * s, 6 * s), "5¢", font=big, fill=BLACK)
    small = font(F_COND_B, 10 * s)
    dr.text((246 * s, 254 * s), "BEAT THE DARK", font=small, fill=WHITE)
    dr.text((246 * s, 267 * s), "WITH THE RED TRAIN", font=small, fill=RED)
    dr.text((246 * s, 280 * s), "after El Lissitzky, 1919", font=font(F_SERIF_I, 11 * s), fill=WHITE)
    return finalize(img)


# ------------------------------------------------------------- 3. The first 28
IRT_1904 = ["City Hall", "Brooklyn Bridge", "Worth St", "Canal St", "Spring St",
            "Bleecker St", "Astor Pl", "14 St", "18 St", "23 St", "28 St", "33 St",
            "Grand Central", "Times Sq", "50 St", "Columbus Circle", "66 St", "72 St",
            "79 St", "86 St", "91 St", "96 St", "103 St", "110 St", "116 St",
            "Manhattan St", "137 St", "145 St"]


def image3_map():
    """Strip map of the original IRT line as it ran on opening night."""
    s = SS
    img, dr = canvas(WHITE)
    # route polyline at 1x: City Hall loop -> north on Lex/Park -> 42 St shuttle -> Broadway north
    route = [(182, 282), (182, 158), (128, 158), (98, 128), (98, 22)]
    seglen = [math.dist(route[i], route[i + 1]) for i in range(len(route) - 1)]
    # where along the route each station sits (hand-placed proportions)
    pos = {}
    lower = IRT_1904[:13]  # City Hall .. Grand Central on the east-side leg
    for i, name in enumerate(lower):
        pos[name] = (182, 282 - i * (124 / 12))
    pos["Times Sq"] = (128, 158)
    pos["50 St"] = (116, 146)
    pos["Columbus Circle"] = (98, 128)
    upper = IRT_1904[16:]
    for i, name in enumerate(upper):
        pos[name] = (98, 116 - i * (94 / (len(upper) - 1)))

    # City Hall balloon loop
    dr.ellipse((172 * s, 280 * s, 192 * s, 296 * s), outline=RED, width=7 * s)
    pts = [(x * s, y * s) for x, y in route]
    dr.line(pts, fill=RED, width=9 * s, joint="curve")

    lab = font(F_COND_B, 8 * s)
    labr = font(F_SANS, 8 * s)
    major = {"City Hall", "Brooklyn Bridge", "14 St", "Grand Central", "Times Sq",
             "Columbus Circle", "96 St", "145 St", "116 St"}
    for name in IRT_1904:
        x, y = pos[name]
        X, Y = x * s, y * s
        if name in major:
            dr.ellipse((X - 6 * s, Y - 6 * s, X + 6 * s, Y + 6 * s), fill=WHITE, outline=BLACK, width=2 * s)
        else:
            if x == 182:
                dr.line((X + 4 * s, Y, X + 9 * s, Y), fill=BLACK, width=2 * s)
            else:
                dr.line((X - 9 * s, Y, X - 4 * s, Y), fill=BLACK, width=2 * s)
        f = lab if name in major else labr
        if x == 182:
            dr.text((X + 12 * s, Y - 5 * s), name.upper() if name in major else name, font=f, fill=BLACK)
        elif name in ("Times Sq",):
            dr.text((X - 4 * s, Y + 8 * s), name.upper(), font=f, fill=BLACK)
        elif name == "50 St":
            dr.text((X + 9 * s, Y - 10 * s), name, font=f, fill=BLACK)
        else:
            t = name.upper() if name in major else name
            dr.text((X - 12 * s - dr.textlength(t, font=f), Y - 5 * s), t, font=f, fill=BLACK)

    # title block
    dr.rectangle((262 * s, 14 * s, 392 * s, 112 * s), fill=BLACK)
    dr.text((270 * s, 18 * s), "THE", font=font(F_INTER_X, 14 * s), fill=WHITE)
    dr.text((270 * s, 30 * s), "FIRST", font=font(F_INTER_X, 30 * s), fill=WHITE)
    dr.text((270 * s, 64 * s), "28", font=font(F_INTER_X, 40 * s), fill=RED)
    dr.text((322 * s, 72 * s), "IRT\nSUBWAY", font=font(F_COND_B, 11 * s), fill=WHITE, spacing=2 * s)
    small = font(F_SANS, 8 * s)
    notes = ["Opened 7 p.m.,", "27 October 1904.", "", "City Hall to 145 St", "in 9.1 miles.",
             "", "Over 100,000 people", "paid a nickel each", "that first evening."]
    for i, l in enumerate(notes):
        dr.text((272 * s, (128 + i * 12) * s), l, font=small, fill=BLACK)
    dr.text((272 * s, 250 * s), "122 years ago", font=font(F_SERIF_I, 11 * s), fill=RED)
    # compass tick
    dr.polygon([(30 * s, 250 * s), (36 * s, 266 * s), (24 * s, 266 * s)], fill=BLACK)
    dr.text((26 * s, 236 * s), "N", font=lab, fill=BLACK)
    return finalize(img)


# ------------------------------------------------------------ 4. Chladni plates
def image4_chladni():
    """Sand gathers where the plate is silent: nodal lines of a square plate."""
    s = 1
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)
    rng = np.random.default_rng(1787)
    modes = [(1, 3), (2, 5), (3, 7), (1, 6), (4, 9), (3, 5)]
    size, gap = 116, 12
    x0 = (W - 3 * size - 2 * gap) // 2
    y0 = 44
    for idx, (n, m) in enumerate(modes):
        col, row = idx % 3, idx // 3
        px, py = x0 + col * (size + gap), y0 + row * (size + gap + 2)
        ink = RED if idx == 4 else BLACK
        # throw sand; keep grains with probability that decays with |f|
        N = 26000
        u = rng.random(N)
        v = rng.random(N)
        N = 60000
        u = rng.random(N)
        v = rng.random(N)
        f = (np.cos(n * np.pi * u) * np.cos(m * np.pi * v)
             - np.cos(m * np.pi * u) * np.cos(n * np.pi * v))
        fu = np.pi * (-n * np.sin(n * np.pi * u) * np.cos(m * np.pi * v)
                      + m * np.sin(m * np.pi * u) * np.cos(n * np.pi * v))
        fv = np.pi * (-m * np.cos(n * np.pi * u) * np.sin(m * np.pi * v)
                      + n * np.cos(m * np.pi * u) * np.sin(n * np.pi * v))
        dist = np.abs(f) / (np.hypot(fu, fv) + 1e-6)  # ~distance to the nearest nodal line
        keep = rng.random(N) < np.exp(-(dist / 0.012) ** 2) * 0.55
        for a, b in zip(u[keep], v[keep]):
            img.putpixel((px + 2 + int(a * (size - 4)), py + 2 + int(b * (size - 4))), ink)
        dr.rectangle((px, py, px + size - 1, py + size - 1), outline=BLACK, width=2)
        dr.ellipse((px + size // 2 - 2, py + size // 2 - 2, px + size // 2 + 2, py + size // 2 + 2), fill=BLACK)
    big = font(F_INTER_X, 22)
    dr.text((x0, 8), "CHLADNI", font=big, fill=BLACK)
    tw = dr.textlength("CHLADNI ", font=big)
    dr.text((x0 + tw, 16), "· 1787 · sand finds the silence", font=font(F_SERIF_I, 12), fill=RED)
    return img.quantize(palette=_pal, dither=Image.Dither.NONE)


# --------------------------------------------------------- 5. Morphogenesis
def image5_turing():
    """Gray-Scott reaction-diffusion grown out of a seed reading '1952'."""
    h, w = H, W
    U = np.ones((h, w))
    V = np.zeros((h, w))
    seed = Image.new("L", (w, h), 0)
    sd = ImageDraw.Draw(seed)
    f = font(F_INTER_X, 120)
    tw = sd.textlength("1952", font=f)
    sd.text(((w - tw) / 2, 70), "1952", font=f, fill=255)
    m = np.asarray(seed) > 128
    rng = np.random.default_rng(1952)
    U[m] = 0.5
    V[m] = 0.25 + 0.05 * rng.random(m.sum())
    Du, Dv, F, k = 0.16, 0.08, 0.0545, 0.062  # coral regime: the digits sprout fingers

    def lap(Z):
        return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)

    for _ in range(1500):
        uvv = U * V * V
        U += Du * lap(U) - uvv + F * (1 - U)
        V += Dv * lap(V) + uvv - (F + k) * V
    out = np.zeros((h, w, 3), np.uint8) + 255
    out[V > 0.12] = BLACK
    out[V > 0.30] = RED
    img = Image.fromarray(out, "RGB")
    dr = ImageDraw.Draw(img)
    dr.text((14, 12), "MORPHOGENESIS", font=font(F_INTER_X, 22), fill=BLACK)
    dr.text((16, 40), "a year, left alone with its chemistry", font=font(F_SERIF_I, 13), fill=RED)
    cap = font(F_COND_B, 9)
    lines = ["A. M. TURING", "THE CHEMICAL BASIS OF MORPHOGENESIS", "seed: four digits · 1500 steps"]
    bw = max(dr.textlength(l, font=cap) for l in lines) + 10
    dr.rectangle((W - bw - 8, H - 46, W - 8, H - 8), fill=WHITE, outline=BLACK, width=2)
    for i, l in enumerate(lines):
        dr.text((W - bw - 3, H - 43 + i * 12), l, font=cap, fill=RED if i == 0 else BLACK)
    return img.quantize(palette=_pal, dither=Image.Dither.NONE)


def main(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    for i, fn in enumerate([image1_pop_moon, image2_wedge, image3_map, image4_chladni, image5_turing], 1):
        im = fn()
        assert im.size == (W, H)
        im.save(out / f"{i}.png", optimize=True)
        print("wrote", out / f"{i}.png")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
