#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-18.

Five 400x300 images in exactly three colors (white, black, red).

Today's threads:
  * First-quarter moon tonight, 20:44 UTC (and Observe-the-Moon Night tomorrow).
  * Venus at greatest brilliancy tonight, mag -4.8, a fat crescent low in the west.
  * Samuel Johnson born this day, 1709 — his Dictionary's definition of NETWORK.
  * The equinox (23 IX 00:05 UTC) — Shūbun no Hi — and higanbana in bloom.

Technique: line-art pieces render at 3x with antialiasing and are quantized to the
palette with NO dither (crisp edges); tonal areas use Floyd–Steinberg on purpose.
"""

import math
import random
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_LSERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_LSERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_LSERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_LSANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=False):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def snap(img):
    """Nearest-palette snap for an RGB image (used after compositing dithered layers)."""
    return img.convert("RGB").quantize(palette=PAL, dither=Image.Dither.NONE)


def font(path, size):
    return ImageFont.truetype(path, size)


def rotated_text(text, fnt, fill, angle, ss=SS):
    """Return an RGBA layer of text rotated by `angle` degrees (CCW)."""
    bbox = fnt.getbbox(text)
    tw, th = bbox[2] - bbox[0] + 4 * ss, bbox[3] - bbox[1] + 4 * ss
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((2 * ss - bbox[0], 2 * ss - bbox[1]), text, font=fnt, fill=fill)
    return layer.rotate(angle, expand=True, resample=Image.BICUBIC)


# ----------------------------------------------------------------- 1. Higanbana
def image1_higanbana():
    """Red spider lilies — the equinox flower — as ink strokes on black."""
    rng = random.Random(20260918)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    def bez(p0, p1, p2, n=24):
        pts = []
        for i in range(n + 1):
            t = i / n
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            pts.append((x, y))
        return pts

    def floret(cx, cy, a, L):
        """One floret: 6 recurved petals fanned around angle a, 6+ long stamens."""
        # petals
        for i in range(6):
            off = (i - 2.5) * 0.42 + rng.uniform(-0.06, 0.06)
            ang = a + off
            l = L * rng.uniform(0.9, 1.15)
            # outward then curl back hard (recurved), with a wavy edge
            p0 = (cx, cy)
            p1 = (cx + math.cos(ang) * l * 1.3, cy + math.sin(ang) * l * 1.3)
            back = ang + (2.3 if off > 0 else -2.3)
            p2 = (p1[0] + math.cos(back) * l * 0.7, p1[1] + math.sin(back) * l * 0.7)
            pts = bez(p0, p1, p2)
            # taper: thick near base, thin at the tip
            for j in range(len(pts) - 1):
                wdt = max(1, int((4.0 - 3.0 * j / len(pts)) * s))
                dr.line([pts[j], pts[j + 1]], fill=RED, width=wdt)
        # stamens: long thin arcs bending "up" (toward -y), anther dots at the ends
        for i in range(6):
            off = (i - 2.5) * 0.13 + rng.uniform(-0.04, 0.04)
            ang = a + off
            l = L * rng.uniform(1.9, 2.4)
            p0 = (cx, cy)
            p1 = (cx + math.cos(ang) * l * 0.7, cy + math.sin(ang) * l * 0.7)
            p2 = (cx + math.cos(ang) * l, cy + math.sin(ang) * l - l * 0.45)
            pts = bez(p0, p1, p2)
            dr.line(pts, fill=RED, width=max(1, int(1.0 * s)))
            ex, ey = pts[-1]
            r = 1.6 * s
            dr.ellipse([ex - r, ey - r, ex + r, ey + r], fill=WHITE)

    def stalk(x_base, top_y, lean, L, n_florets):
        # stem: a slightly bowed line from ground to the umbel
        p0 = (x_base * s, H * s)
        p2 = ((x_base + lean) * s, top_y * s)
        p1 = ((x_base + lean * 0.3) * s, (H + top_y) / 2 * s)
        pts = bez(p0, p1, p2, 30)
        dr.line(pts, fill=WHITE, width=int(2.2 * s))
        cx, cy = p2
        # florets radiate from the umbel head, biased upward
        angs = [-math.pi / 2 + (i - (n_florets - 1) / 2) * (4.6 / (n_florets - 1))
                for i in range(n_florets)]
        for a in angs:
            a += rng.uniform(-0.12, 0.12)
            r0 = 7 * s
            floret(cx + math.cos(a) * r0, cy + math.sin(a) * r0, a, L * s)

    stalk(150, 92, -6, 21, 7)
    stalk(262, 128, 5, 18, 6)
    stalk(342, 66, 4, 16, 6)
    # a small one just opening, leaning
    stalk(240, 226, 10, 10, 4)

    # caption, bottom-left, quiet
    fj = font(F_JP, 30 * s)
    dr.text((14 * s, 214 * s), "彼岸花", font=fj, fill=WHITE)
    fs = font(F_SANS, 10 * s)
    dr.text((15 * s, 254 * s), "higanbana · the equinox flower", font=fs, fill=WHITE)
    dr.text((15 * s, 270 * s), "in bloom for the week of higan, 20–26 IX", font=fs, fill=WHITE)
    return finalize(img)


# ------------------------------------------------------------- 2. Venus crescent
def image2_venus():
    """Venus at greatest brilliancy: a fat crescent, plus the run of its evening phases."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    def crescent(cx, cy, r, k, tilt, fill=WHITE):
        """Draw a planet disc of radius r with illuminated fraction k, lit limb rotated by tilt."""
        # build in a local buffer then rotate
        size = int(r * 2 + 8)
        buf = Image.new("L", (size, size), 0)
        bd = ImageDraw.Draw(buf)
        c = size / 2
        bd.ellipse([c - r, c - r, c + r, c + r], fill=255)
        # dark side: cover the left half, then the terminator ellipse
        bd.rectangle([0, 0, c, size], fill=0)
        a = abs(1 - 2 * k) * r
        if k < 0.5:
            bd.ellipse([c - a, c - r, c + a, c + r], fill=0)
        else:
            bd.ellipse([c - a, c - r, c + a, c + r], fill=255)
        buf = buf.rotate(tilt, resample=Image.BICUBIC)
        col = Image.new("RGB", buf.size, fill)
        img.paste(col, (int(cx - c), int(cy - c)), buf)

    # twilight band along the bottom: tonal gradient, dithered at the end
    band_top = 232
    grad = Image.new("L", (1, (H - band_top) * s))
    for y in range(grad.size[1]):
        t = y / grad.size[1]
        grad.putpixel((0, y), int(20 + 130 * t ** 1.6))
    grad = grad.resize((W * s, grad.size[1]))
    gband = finalize(Image.merge("RGB", (grad, grad, grad)).resize((W, H - band_top)), dither=True)

    # main crescent: k ~ 0.27 at greatest brilliancy; lit side toward the (set) sun, lower-left
    cx, cy, r = 128 * s, 128 * s, 82 * s
    crescent(cx, cy, r, 0.27, -145)
    # faint outline of the full disc — earthshine-like hint, thin red ring
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=max(1, int(0.8 * s)))

    # titles, right column
    fT = font(F_SERIF_B, 34 * s)
    dr.text((228 * s, 44 * s), "VENUS", font=fT, fill=WHITE)
    f1 = font(F_SERIF, 11 * s)
    f2 = font(F_MONO, 10 * s)
    dr.text((230 * s, 88 * s), "greatest brilliancy", font=f1, fill=RED)
    dr.text((230 * s, 106 * s), "18 IX 2026  23:00 UTC", font=f2, fill=WHITE)
    dr.text((230 * s, 122 * s), "magnitude  −4.8", font=f2, fill=WHITE)
    dr.text((230 * s, 138 * s), "27% lit · 38″ across", font=f2, fill=WHITE)
    dr.text((230 * s, 162 * s), "low in the west after sunset;", font=f1, fill=WHITE)
    dr.text((230 * s, 176 * s), "not this bright again in the", font=f1, fill=WHITE)
    dr.text((230 * s, 190 * s), "evening sky until April 2028.", font=f1, fill=WHITE)

    # the run of phases across the evening apparition, left→right = summer→now→October
    fl = font(F_SANS, 9 * s)
    dr.text((14 * s, 212 * s), "the evening apparition, June to October", font=fl, fill=WHITE)
    xs = [30, 70, 115, 168, 232, 305]
    ks = [0.85, 0.72, 0.58, 0.42, 0.27, 0.10]
    rs = [4.5, 5.5, 7, 9.5, 13, 18]
    for i, (x, k, rr) in enumerate(zip(xs, ks, rs)):
        y = 262
        crescent(x * s, y * s, rr * s, k, -145)
        if i == 4:
            R = (rr + 5) * s
            dr.ellipse([x * s - R, y * s - R, x * s + R, y * s + R], outline=RED, width=int(1.2 * s))
            dr.text((x * s, (y - rr - 13) * s), "tonight", font=font(F_SANS_B, 10 * s), fill=RED, anchor="mm")

    out = finalize(img)
    # paste the dithered twilight band beneath the phase row, keeping the discs on top
    band = gband.convert("RGB")
    base = out.convert("RGB")
    from PIL import ImageChops
    region = base.crop((0, band_top, W, H))
    # lighten: keep drawn pixels (white/red) where they exist, else use band
    mask = region.convert("L").point(lambda v: 255 if v > 0 else 0)
    merged = Image.composite(region, band, mask)
    base.paste(merged, (0, band_top))
    return snap(base)


# --------------------------------------------------------- 3. NETWORK (Johnson)
def image3_network():
    """Samuel Johnson, born this day 1709. His Dictionary defines NETWORK as
    'Any thing reticulated or decussated, at equal distances, with interstices
    between the intersections.'  So: a diagram of exactly that."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # headword, dictionary style
    fH = font(F_LSERIF_B, 30 * s)
    dr.text((16 * s, 10 * s), "NETWORK.", font=fH, fill=BLACK)
    fI = font(F_LSERIF_I, 11 * s)
    dr.text((186 * s, 26 * s), "n. ſ.", font=fI, fill=BLACK)
    fsm = font(F_LSERIF, 11 * s)
    dr.text((384 * s, 12 * s), "Johnſon's Dictionary, 1755", font=fsm, fill=RED, anchor="ra")
    dr.text((384 * s, 26 * s), "S. Johnſon born this day, 1709", font=fsm, fill=BLACK, anchor="ra")

    fD = font(F_LSERIF_I, 13 * s)
    lines = [
        "Any thing reticulated or decuſſated, at equal",
        "diſtances, with interſtices between the interſections.",
    ]
    y = 48
    for ln in lines:
        dr.text((16 * s, y * s), ln, font=fD, fill=BLACK)
        y += 17
    dr.line([(16 * s, 86 * s), (384 * s, 86 * s)], fill=BLACK, width=s)

    # --- the net: two families of parallel lines (decussated) at equal distances,
    # drooping like a hung net, knots at every crossing.
    x0, x1 = 16, 384
    ytop, ybot = 100, 288
    n = 9
    pitch = (x1 - x0) / n
    sag = 18.0

    def warp(x, y):
        # gentle catenary sag: lines droop more toward the middle of the net
        t = (x - x0) / (x1 - x0)
        d = sag * (1 - (2 * t - 1) ** 2) * ((y - ytop) / (ybot - ytop))
        return x * s, (y + d) * s

    # diagonal family A (down-right) and B (down-left)
    segs = []
    knots = set()
    for i in range(-n, 2 * n + 1):
        # family A: x = x0 + i*pitch + (y - ytop)
        ptsA, ptsB = [], []
        for yy in range(ytop, ybot + 1, 4):
            xa = x0 + i * pitch + (yy - ytop) * 0.72
            xb = x0 + i * pitch - (yy - ytop) * 0.72
            if x0 <= xa <= x1:
                ptsA.append(warp(xa, yy))
            if x0 <= xb <= x1:
                ptsB.append(warp(xb, yy))
        for pts in (ptsA, ptsB):
            if len(pts) > 1:
                dr.line(pts, fill=BLACK, width=int(1.3 * s))
    # knots: crossings of the two families
    for i in range(-n, 2 * n + 1):
        for j in range(-n, 2 * n + 1):
            # x0 + i p + 0.72 dy = x0 + j p - 0.72 dy  ->  dy = (j - i) p / 1.44
            dy = (j - i) * pitch / 1.44
            yy = ytop + dy
            xx = x0 + i * pitch + 0.72 * dy
            if ytop <= yy <= ybot and x0 <= xx <= x1:
                px, py = warp(xx, yy)
                knots.add((round(px), round(py), i, j))
    for (px, py, i, j) in knots:
        r = 1.9 * s
        dr.ellipse([px - r, py - r, px + r, py + r], fill=BLACK)

    # one interstice, filled red; one intersection, ringed red; equal distances, bracketed
    def knot_at(i, j):
        dy = (j - i) * pitch / 1.44
        return warp(x0 + i * pitch + 0.72 * dy, ytop + dy)

    # interstice bounded by knots (i,j),(i+1,j),(i+1,j+1),(i,j+1)
    ii, jj = 4, 6
    quad = [knot_at(ii, jj), knot_at(ii + 1, jj), knot_at(ii + 1, jj + 1), knot_at(ii, jj + 1)]
    dr.polygon(quad, fill=RED)
    qx = sum(p[0] for p in quad) / 4
    qy = sum(p[1] for p in quad) / 4

    kx, ky = knot_at(7, 9)
    R = 6 * s
    dr.ellipse([kx - R, ky - R, kx + R, ky + R], outline=RED, width=int(1.4 * s))

    fL = font(F_LSERIF_I, 12 * s)
    # callouts with thin red leaders
    def callout(px, py, tx, ty, label, anchor="la"):
        dr.line([(px, py), (tx, ty)], fill=RED, width=max(1, int(0.9 * s)))
        pad = 3 * s
        bb = fL.getbbox(label)
        tw = bb[2] - bb[0]
        if anchor == "la":
            box = [tx, ty - 7 * s, tx + tw + 2 * pad, ty + 7 * s]
            dr.rectangle(box, fill=WHITE)
            dr.text((tx + pad, ty), label, font=fL, fill=RED, anchor="lm")
        else:
            box = [tx - tw - 2 * pad, ty - 7 * s, tx, ty + 7 * s]
            dr.rectangle(box, fill=WHITE)
            dr.text((tx - pad, ty), label, font=fL, fill=RED, anchor="rm")

    callout(qx, qy, 250 * s, 118 * s, "interſtice")
    callout(kx + R, ky, 330 * s, 214 * s, "interſection")
    # "at equal distances": bracket between two adjacent knots on the top edge
    a = knot_at(2, 2)
    b = knot_at(3, 3)
    by = a[1] - 9 * s
    dr.line([(a[0], by), (b[0], by)], fill=RED, width=s)
    dr.line([(a[0], by - 3 * s), (a[0], by + 3 * s)], fill=RED, width=s)
    dr.line([(b[0], by - 3 * s), (b[0], by + 3 * s)], fill=RED, width=s)
    callout((a[0] + b[0]) / 2, by, 20 * s, 130 * s, "at equal diſtances", anchor="la")
    # "reticulated / decussated" label bottom-left, over the net
    callout(knot_at(0, 4)[0] + 30 * s, knot_at(0, 4)[1] + 20 * s, 20 * s, 262 * s,
            "reticulated; decuſſated")
    return finalize(img)


# ----------------------------------------------------- 4. First quarter (Proun)
def image4_proun():
    """A Suprematist composition for tonight's first-quarter moon:
    the disc split by the diagonal, the red wedge driving at its centre."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # the diagonal ground: black lower-right
    # line through (0, 300) → (400, 60)  (steep-ish)
    A, B = (0, 300), (400, 60)
    def side(x, y):
        return (B[0] - A[0]) * (y - A[1]) - (B[1] - A[1]) * (x - A[0])
    dr.polygon([(A[0] * s, A[1] * s), (B[0] * s, B[1] * s), (W * s, B[1] * s), (W * s, H * s)],
               fill=BLACK)
    # the extra: fill the whole right side below the line
    dr.polygon([(A[0] * s, A[1] * s), (B[0] * s, B[1] * s), (W * s, 0), (W * s, H * s)], fill=BLACK)

    # the disc: centred on the line; each half inverts its ground
    cx, cy, r = 214, 172, 78
    disc = Image.new("L", (W * s, H * s), 0)
    ImageDraw.Draw(disc).ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=255)
    inv = Image.eval(img.convert("L"), lambda v: 255 - v)
    img.paste(Image.merge("RGB", (inv, inv, inv)), (0, 0), disc)
    dr = ImageDraw.Draw(img)

    # the red wedge: from the top-left corner, tip exactly at the disc centre
    tip = (cx * s, cy * s)
    dr.polygon([(-10 * s, 22 * s), (30 * s, -10 * s), tip], fill=RED)
    # a thin black bar crossing the wedge, and a second smaller wedge answering from below
    dr.polygon([(60 * s, 250 * s), (66 * s, 256 * s), (230 * s, 292 * s), (226 * s, 284 * s)], fill=RED)
    dr.rectangle([300 * s, 44 * s, 316 * s, 60 * s], fill=RED)
    dr.rectangle([322 * s, 50 * s, 330 * s, 58 * s], fill=BLACK)
    dr.polygon([(330 * s, 120 * s), (392 * s, 84 * s), (392 * s, 88 * s), (330 * s, 124 * s)], fill=WHITE)
    # projectiles: a row of small circles fading along a diagonal, on the white ground
    for i in range(6):
        rr = (1.2 + 0.55 * i) * s
        px, py = (30 + i * 17) * s, (215 - i * 9) * s
        dr.ellipse([px - rr, py - rr, px + rr, py + rr], fill=BLACK)
    dr.rectangle([18 * s, 236 * s, 44 * s, 242 * s], fill=BLACK)
    # tiny square cluster on the black ground
    for i in range(3):
        dr.rectangle([(236 + i * 14) * s, (262 + i * 6) * s, (242 + i * 14) * s, (268 + i * 6) * s], fill=WHITE)

    # text on the diagonal of the wedge
    ang = math.degrees(math.atan2(cy - (-10), cx - (-10)))  # slope of wedge
    fT = font(F_LSANS_B, 15 * s)
    lay = rotated_text("FIRST QUARTER", fT, BLACK, -ang * 0.999)
    img.paste(lay, (int(64 * s), int(28 * s)), lay)
    fS = font(F_LSANS_B, 12 * s)
    d2 = ImageDraw.Draw(img)
    d2.text((388 * s, 236 * s), "18 · IX · 2026", font=fS, fill=WHITE, anchor="ra")
    d2.text((388 * s, 252 * s), "20:44 UTC", font=fS, fill=RED, anchor="ra")
    fsm = font(F_SANS, 9 * s)
    d2.text((388 * s, 288 * s), "PROUN 18.IX", font=fsm, fill=WHITE, anchor="rs")
    return finalize(img)


# ------------------------------------------------------ 5. Asa-no-ha equinox
def image5_asanoha():
    """Hemp-leaf kumiko lattice, split day/night down the middle for the equinox,
    with the red sun sitting exactly on the divide."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    split = 200
    dr.rectangle([split * s, 0, W * s, H * s], fill=BLACK)

    side = 30.0
    hgt = side * math.sqrt(3) / 2
    lw = int(1.6 * s)

    def col_for(x):
        return WHITE if x >= split else BLACK

    def seg(p, q):
        # split a segment at the divide so each half takes its ground's inverse colour
        (x1, y1), (x2, y2) = p, q
        if (x1 < split) == (x2 < split):
            dr.line([(x1 * s, y1 * s), (x2 * s, y2 * s)], fill=col_for((x1 + x2) / 2), width=lw)
        else:
            t = (split - x1) / (x2 - x1)
            mx, my = split, y1 + t * (y2 - y1)
            dr.line([(x1 * s, y1 * s), (mx * s, my * s)], fill=col_for(x1), width=lw)
            dr.line([(mx * s, my * s), (x2 * s, y2 * s)], fill=col_for(x2), width=lw)

    # triangular grid; each triangle gets centroid→vertex spokes (asa-no-ha)
    rows = int(H / hgt) + 3
    cols = int(W / side) + 3
    for r in range(-1, rows):
        y = r * hgt
        xoff = (r % 2) * side / 2
        for c in range(-1, cols):
            x = c * side + xoff
            # up-pointing triangle: (x,y+h),(x+side,y+h),(x+side/2,y)
            tri_up = [(x, y + hgt), (x + side, y + hgt), (x + side / 2, y)]
            # down-pointing: (x,y),(x+side,y),(x+side/2,y+h)  (shifted so grid tiles)
            tri_dn = [(x + side / 2, y), (x + 1.5 * side, y), (x + side, y + hgt)]
            for tri in (tri_up, tri_dn):
                gx = sum(p[0] for p in tri) / 3
                gy = sum(p[1] for p in tri) / 3
                for k in range(3):
                    seg(tri[k], tri[(k + 1) % 3])
                    seg((gx, gy), tri[k])

    # the sun: a red disc on the divide, lattice cleared underneath
    cx, cy, R = split, 150, 44
    # half-white/half-black halo behind the sun, then the sun
    halo = Image.new("L", (W * s, H * s), 0)
    ImageDraw.Draw(halo).ellipse([(cx - R - 5) * s, (cy - R - 5) * s, (cx + R + 5) * s, (cy + R + 5) * s], fill=255)
    ground = Image.new("RGB", (W * s, H * s), WHITE)
    ImageDraw.Draw(ground).rectangle([split * s, 0, W * s, H * s], fill=BLACK)
    img.paste(ground, (0, 0), halo)
    dr = ImageDraw.Draw(img)
    dr.ellipse([(cx - R) * s, (cy - R) * s, (cx + R) * s, (cy + R) * s], fill=RED)

    # captions, in each ground's ink, with cleared plates behind
    fj = font(F_JP, 22 * s)
    fs = font(F_SANS, 10 * s)
    dr.rectangle([10 * s, 244 * s, 150 * s, 290 * s], fill=WHITE)
    dr.text((16 * s, 246 * s), "秋分", font=fj, fill=BLACK)
    dr.text((16 * s, 276 * s), "equal day", font=fs, fill=BLACK)
    dr.rectangle([222 * s, 244 * s, 390 * s, 290 * s], fill=BLACK)
    dr.text((384 * s, 246 * s), "彼岸", font=fj, fill=WHITE, anchor="ra")
    dr.text((384 * s, 276 * s), "equal night · 23 IX 00:05 UTC", font=fs, fill=WHITE, anchor="ra")
    return finalize(img)


def main(outdir):
    makers = [image1_higanbana, image2_venus, image3_network, image4_proun, image5_asanoha]
    for i, mk in enumerate(makers, 1):
        im = mk()
        assert im.size == (W, H)
        im.save(f"{outdir}/{i}.png", optimize=True)
        print("wrote", f"{outdir}/{i}.png")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
