#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-19 (Saturday).

International Observe the Moon Night · Higan approaching · :-) turns 44.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

  1. Higanbana        — botanical plate of Lycoris radiata (red spider lily)
  2. Observe the Moon — numpy-shaded 53% waxing gibbous moon, real maria
  3. :-)              — the 19-Sep-82 bulletin board post, read sideways
  4. Equinox          — constructivist poster for Sep 23 00:05 UTC
  5. Asanoha          — hemp-leaf lattice with a red hexagonal bloom

Tonal pieces render at 3x with anti-aliasing, LANCZOS down, Floyd–Steinberg
into the palette. Hard-edged pieces render at 1x in pure palette colors.
"""

import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F = "/usr/share/fonts/truetype/"
FONT_SANS = F + "dejavu/DejaVuSans.ttf"
FONT_SANS_B = F + "dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = F + "dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = F + "dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF_I = F + "liberation/LiberationSerif-Italic.ttf"
FONT_MONO = F + "dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = F + "dejavu/DejaVuSansMono-Bold.ttf"
FONT_FREESANS_B = F + "freefont/FreeSansBold.ttf"
FONT_JP = F + "fonts-japanese-gothic.ttf"

OUT = os.path.dirname(os.path.abspath(__file__))


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED)
    palette += [0, 0, 0] * (256 - 3)
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=True):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def crisp(img):
    """Return (RGB image at 1x, ImageDraw with anti-aliasing off) for text overlays."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    img = img.convert("RGB")
    dr = ImageDraw.Draw(img)
    dr.fontmode = "1"
    return img, dr


def nearest3(img):
    """Snap an RGB image to the palette by nearest color (no dither)."""
    a = np.asarray(img.convert("RGB")).astype(np.int32)
    cols = np.array([WHITE, BLACK, RED], dtype=np.int32)
    d = ((a[:, :, None, :] - cols[None, None, :, :]) ** 2).sum(-1)
    idx = d.argmin(-1).astype(np.uint8)
    out = Image.fromarray(idx, "P")
    out.putpalette(PAL.getpalette())
    return out


# ---------------------------------------------------------------- 1. Higanbana
def stroke(dr, pts, w0, w1, color):
    """Tapered polyline: width goes from w0 at the start to w1 at the end."""
    n = len(pts)
    for i in range(n - 1):
        t = i / max(1, n - 2)
        w = w0 + (w1 - w0) * t
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        dr.line([x0, y0, x1, y1], fill=color, width=max(1, int(round(w))))
        r = w / 2
        dr.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=color)


def bezier(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
        out.append((x, y))
    return out


def flower(dr, rng, bx, by, ang, scale, s):
    """One Lycoris flower: funnel base at (bx, by) pointing along `ang`.

    Six narrow tepals, strongly reflexed (they curl backwards), and six long
    stamens thrown forward like spider legs.
    """
    ux, uy = math.cos(ang), math.sin(ang)
    # tepals
    for k in range(6):
        a = ang + (k - 2.5) * math.radians(26) + rng.uniform(-0.08, 0.08)
        L = scale * rng.uniform(0.8, 1.0)
        dx, dy = math.cos(a), math.sin(a)
        # perpendicular, pointing away from the flower axis (for reflex curl)
        side = 1 if (k - 2.5) > 0 else -1
        px, py = -dy * side, dx * side
        p0 = (bx, by)
        p1 = (bx + dx * L * 0.55, by + dy * L * 0.55)
        p2 = (bx + dx * L * 0.95 + px * L * 0.25, by + dy * L * 0.95 + py * L * 0.25)
        p3 = (bx + dx * L * 0.75 + px * L * 0.55, by + dy * L * 0.75 + py * L * 0.55)
        pts = bezier(p0, p1, p2, p3, 22)
        # wavy edge: jitter the middle of the tepal
        pts = [
            (x + math.sin(i * 1.7) * 0.6 * s * (0.3 < i / 22 < 0.9), y + math.cos(i * 1.3) * 0.6 * s * (0.3 < i / 22 < 0.9))
            for i, (x, y) in enumerate(pts)
        ]
        stroke(dr, pts, 1.0 * s, 2.2 * s, RED)
        stroke(dr, pts[-6:], 2.0 * s, 0.8 * s, RED)
    # stamens (thin, long, arcing forward and up)
    for k in range(6):
        a = ang + (k - 2.5) * math.radians(11) + rng.uniform(-0.05, 0.05)
        L = scale * rng.uniform(1.8, 2.3)
        dx, dy = math.cos(a), math.sin(a)
        p0 = (bx + ux * scale * 0.2, by + uy * scale * 0.2)
        p1 = (bx + dx * L * 0.5, by + dy * L * 0.5)
        p2 = (bx + dx * L * 0.85, by + dy * L * 0.85 - 0.12 * L)
        p3 = (bx + dx * L, by + dy * L - 0.22 * L)
        pts = bezier(p0, p1, p2, p3, 18)
        stroke(dr, pts, 0.8 * s, 0.8 * s, RED)
        ex, ey = pts[-1]
        r = 1.4 * s
        dr.ellipse([ex - r, ey - r, ex + r, ey + r], fill=RED)
    # the funnel base in black-ish dark (perianth tube)
    r = 1.6 * s
    dr.ellipse([bx - r, by - r, bx + r, by + r], fill=RED)


def image1_higanbana():
    rng = random.Random(20260919)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # ground line + faint horizon
    dr.line([0, 262 * s, W * s, 262 * s], fill=BLACK, width=int(1.2 * s))

    stems = [
        (128, 262, 128 + 10, 104, 0.95),
        (236, 262, 236 - 14, 92, 1.1),
        (318, 262, 318 + 6, 128, 0.85),
    ]
    for (x0, y0, x1, y1, sc) in stems:
        # scape: a tall, nearly straight, leafless stem
        pts = bezier((x0 * s, y0 * s), (x0 * s, (y0 - 60) * s), (x1 * s, (y1 + 60) * s), (x1 * s, y1 * s), 30)
        stroke(dr, pts, 2.6 * s, 1.6 * s, BLACK)
        # umbel: 5 flowers radiating from the top of the scape
        n = 5
        for k in range(n):
            ang = -math.pi / 2 + (k - (n - 1) / 2) * math.radians(52) + rng.uniform(-0.1, 0.1)
            d = 11 * s * sc
            bx = x1 * s + math.cos(ang) * d
            by = y1 * s + math.sin(ang) * d
            # pedicel (short stalk) in black
            dr.line([x1 * s, y1 * s, bx, by], fill=BLACK, width=int(1.4 * s))
            flower(dr, rng, bx, by, ang, 26 * s * sc, s)
        # black umbel node
        r = 2.2 * s
        dr.ellipse([x1 * s - r, y1 * s - r, x1 * s + r, y1 * s + r], fill=BLACK)

    # vertical kanji, right side, like a woodblock signature block
    fjp = font(FONT_JP, 26 * s)
    x = 356 * s
    y = 26 * s
    for ch in "彼岸花":
        dr.text((x, y), ch, font=fjp, fill=BLACK)
        y += 28 * s
    # red seal
    dr.rectangle([352 * s, 118 * s, 380 * s, 146 * s], fill=RED)
    fseal = font(FONT_JP, 11 * s)
    dr.text((355 * s, 120 * s), "秋", font=fseal, fill=WHITE)
    dr.text((367 * s, 120 * s), "分", font=fseal, fill=WHITE)
    dr.text((355 * s, 133 * s), "近", font=fseal, fill=WHITE)
    dr.text((367 * s, 133 * s), "し", font=fseal, fill=WHITE)

    # captions, crisp at 1x
    img, dr = crisp(img)
    dr.text((16, 268), "Lycoris radiata", font=font(FONT_SERIF_I, 12), fill=BLACK)
    dr.text((16, 283), "red spider lily · blooms at the equinox, before its leaves · Higan week begins Sep 20", font=font(FONT_SANS, 9), fill=BLACK)
    dr.text((16, 206), "HIGANBANA", font=font(FONT_SANS_B, 11), fill=BLACK)
    dr.text((16, 220), "the flower of", font=font(FONT_SANS, 9), fill=BLACK)
    dr.text((16, 232), "the distant shore", font=font(FONT_SANS, 9), fill=BLACK)
    return nearest3(img)


# ---------------------------------------------------------------- 2. The Moon
MARIA = [  # (lon E+, lat N+, semi-axis a, semi-axis b, rotation deg, albedo drop)
    ("Crisium", 59, 17, 9, 7, 0, 0.45),
    ("Fecunditatis", 51, -8, 12, 9, 30, 0.35),
    ("Tranquillitatis", 31, 9, 14, 11, 20, 0.40),
    ("Serenitatis", 18, 28, 11, 10, 0, 0.42),
    ("Nectaris", 35, -15, 7, 6, 0, 0.35),
    ("Vaporum", 3, 13, 5, 4, 0, 0.35),
    ("Imbrium", -16, 33, 18, 14, -10, 0.42),
    ("Frigoris", 1, 56, 26, 5, 0, 0.35),
    ("Nubium", -17, -21, 11, 9, 0, 0.35),
    ("Humorum", -39, -24, 7, 6, 0, 0.38),
    ("Procellarum", -57, 18, 16, 28, 10, 0.32),
    ("Cognitum", -23, -10, 5, 4, 0, 0.3),
]
CRATERS = [  # (lon, lat, radius deg, depth)
    ("Tycho", -11, -43, 2.6, 1.0),
    ("Copernicus", -20, 10, 2.8, 1.0),
    ("Kepler", -38, 8, 1.8, 0.8),
    ("Plato", -9, 51, 3.0, 0.5),
    ("Aristarchus", -47, 24, 1.6, 0.9),
    ("Clavius", -15, -58, 4.5, 0.6),
    ("Ptolemaeus", -2, -9, 4.0, 0.5),
    ("Alphonsus", -3, -13, 3.2, 0.5),
    ("Arzachel", -2, -18, 2.8, 0.7),
    ("Theophilus", 26, -11, 3.0, 0.9),
    ("Langrenus", 61, -9, 3.5, 0.8),
    ("Petavius", 60, -25, 4.0, 0.8),
    ("Posidonius", 30, 32, 2.8, 0.6),
    ("Aristoteles", 17, 50, 2.6, 0.7),
    ("Eudoxus", 16, 44, 2.0, 0.7),
    ("Hipparchus", 5, -5, 4.0, 0.4),
    ("Albategnius", 4, -11, 3.5, 0.6),
    ("Grimaldi", -68, -5, 5.0, 0.5),
    ("Schickard", -55, -44, 5.0, 0.4),
    ("Endymion", 57, 54, 3.0, 0.6),
    ("Cleomedes", 56, 27, 3.5, 0.6),
]


def image2_moon():
    rng = np.random.default_rng(20260919)
    s = 2
    R = 124 * s
    cx, cy = 160 * s, 150 * s
    Wd, Hd = W * s, H * s
    yy, xx = np.mgrid[0:Hd, 0:Wd].astype(np.float64)
    X = (xx - cx) / R
    Y = -(yy - cy) / R
    inside = X * X + Y * Y <= 1.0
    Z = np.sqrt(np.clip(1 - X * X - Y * Y, 0, 1))

    # selenographic coordinates of each pixel (orthographic, sub-earth point at 0,0)
    lat = np.arcsin(np.clip(Y, -1, 1))
    lon = np.arctan2(X, Z)  # east positive -> right

    # albedo: bright highlands + darker maria + fine grain
    albedo = np.full((Hd, Wd), 0.85)
    for (_, lo, la, a, b, rot, drop) in MARIA:
        lo_r, la_r = math.radians(lo), math.radians(la)
        # angular offsets on the sphere (approx, small-angle in a local tangent frame)
        dlo = (lon - lo_r) * np.cos(la_r)
        dla = lat - la_r
        th = math.radians(rot)
        u = dlo * math.cos(th) + dla * math.sin(th)
        v = -dlo * math.sin(th) + dla * math.cos(th)
        d = (u / math.radians(a)) ** 2 + (v / math.radians(b)) ** 2
        edge = np.clip(1.4 - d, 0, 1)  # soft, slightly lumpy edge
        albedo -= drop * 1.25 * np.clip(edge, 0, 1) ** 0.7
    # lumpy noise for the maria edges + highland texture
    noise = rng.normal(0, 1, (Hd // 8 + 1, Wd // 8 + 1))
    noise_img = Image.fromarray(((noise - noise.min()) / (noise.max() - noise.min()) * 255).astype(np.uint8)).resize((Wd, Hd), Image.BICUBIC)
    noise = np.asarray(noise_img).astype(np.float64) / 255 - 0.5
    albedo += 0.12 * noise
    albedo += rng.normal(0, 0.03, (Hd, Wd))

    # height map: craters (bowl + rim) drawn in tangent-plane coordinates
    height = np.zeros((Hd, Wd))
    crater_list = list(CRATERS)
    for _ in range(160):  # anonymous small craters
        la = math.degrees(math.asin(rng.uniform(-1, 1)))
        lo = rng.uniform(-88, 88)
        crater_list.append(("", lo, la, rng.uniform(0.5, 1.6), rng.uniform(0.3, 0.8)))
    for (_, lo, la, rad, depth) in crater_list:
        lo_r, la_r = math.radians(lo), math.radians(la)
        dlo = (lon - lo_r) * np.cos(la_r)
        dla = lat - la_r
        d = np.sqrt(dlo * dlo + dla * dla) / math.radians(rad)
        bowl = -depth * np.clip(1 - d * d, 0, 1)  # parabolic bowl
        rim = depth * 0.55 * np.exp(-((d - 1.0) ** 2) / 0.02)
        height += np.where(d < 1.6, bowl + rim, 0) * math.radians(rad) * 6

    # normals: sphere normal perturbed by the height gradient (in image space)
    gy, gx = np.gradient(height)
    nx = X - gx * 22
    ny = Y + gy * 22
    nz = Z
    nrm = np.sqrt(nx * nx + ny * ny + nz * nz) + 1e-9
    nx, ny, nz = nx / nrm, ny / nrm, nz / nrm

    # sun direction for 53% illuminated waxing gibbous (lit side on the right)
    k = 0.53
    phase = math.acos(2 * k - 1)  # angle sun-moon-earth
    Lx, Lz = math.sin(phase), math.cos(phase)
    shade = np.clip(nx * Lx + nz * Lz, 0, 1)
    # lunar surface is not Lambertian: flatten the falloff a little (Lommel-Seeliger-ish)
    shade = shade ** 0.6
    tone = albedo * shade
    tone = np.clip(tone, 0, 1)
    img_arr = np.where(inside, tone * 255, 0).astype(np.uint8)
    moon = Image.fromarray(img_arr, "L").convert("RGB")

    # earthshine hint: very faint disc on the dark side so the limb reads
    dark = inside & (shade < 0.02)
    arr = np.asarray(moon).copy()
    arr[dark] = 0
    moon = Image.fromarray(arr)

    out = finalize(moon, dither=True).convert("RGB")
    dr = ImageDraw.Draw(out)
    dr.fontmode = "1"

    # red reticle + labels (hard-edged, drawn at 1x after dithering)
    cx1, cy1, R1 = cx // s, cy // s, R // s
    dr.ellipse([cx1 - R1 - 4, cy1 - R1 - 4, cx1 + R1 + 4, cy1 + R1 + 4], outline=RED, width=1)
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        x0 = cx1 + math.cos(a) * (R1 + 4)
        y0 = cy1 + math.sin(a) * (R1 + 4)
        x1 = cx1 + math.cos(a) * (R1 + 12)
        y1 = cy1 + math.sin(a) * (R1 + 12)
        dr.line([x0, y0, x1, y1], fill=RED, width=2)
    # terminator marker
    tx = cx1 + int(R1 * math.sin(math.radians(-3.4)))
    dr.line([tx, cy1 - R1 - 2, tx, cy1 - R1 + 6], fill=RED, width=1)
    dr.line([tx, cy1 + R1 - 6, tx, cy1 + R1 + 2], fill=RED, width=1)

    fb = font(FONT_SANS_B, 13)
    fs = font(FONT_SANS, 10)
    fm = font(FONT_SANS_B, 9)
    x = 296
    dr.text((x, 20), "OBSERVE", font=fb, fill=WHITE)
    dr.text((x, 36), "THE MOON", font=fb, fill=WHITE)
    dr.text((x, 52), "NIGHT", font=fb, fill=RED)
    dr.text((x, 74), "Sat 19 Sep 2026", font=fs, fill=WHITE)
    dr.line([x, 90, x + 90, 90], fill=RED, width=1)
    rows = [
        ("phase", "waxing gibbous"),
        ("lit", "53 %"),
        ("age", "7.3 days"),
        ("first qtr", "18 Sep 20:44"),
        ("terminator", "3.4° W"),
        ("full", "26 Sep"),
    ]
    y = 98
    for k_, v in rows:
        dr.text((x, y), k_, font=fm, fill=RED)
        dr.text((x, y + 10), v, font=fs, fill=WHITE)
        y += 26
    dr.text((x, 268), "shadows are longest", font=fs, fill=WHITE)
    dr.text((x, 280), "along the line.", font=fs, fill=WHITE)
    # mark a couple of features along the terminator with tiny red ticks
    for name, lo, la in (("Ptolemaeus", -2, -9), ("Plato", -9, 51), ("Tycho", -11, -43)):
        px = cx1 + R1 * math.cos(math.radians(la)) * math.sin(math.radians(lo))
        py = cy1 - R1 * math.sin(math.radians(la))
        dr.ellipse([px - 3, py - 3, px + 3, py + 3], outline=RED, width=1)
    return nearest3(out)


# ---------------------------------------------------------------- 3. :-)
def image3_smiley():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # the huge emoticon, rendered on its own canvas then rotated so it reads as a face
    fbig = font(FONT_MONO_B, 150 * s)
    txt = ":-)"
    bbox = dr.textbbox((0, 0), txt, font=fbig)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    face = Image.new("RGB", (tw + 20 * s, th + 20 * s), WHITE)
    fd = ImageDraw.Draw(face)
    fd.text((10 * s - bbox[0], 10 * s - bbox[1]), txt, font=fbig, fill=BLACK)
    face = face.rotate(-90, expand=True, fillcolor=WHITE)
    fx = 22 * s
    fy = (H * s - face.height) // 2 + 6 * s
    img.paste(face, (fx, fy))

    img, dr = crisp(img)

    # bulletin-board printout on the right, crisp at 1x
    fm = font(FONT_MONO, 9)
    fmb = font(FONT_MONO_B, 9)
    x0 = 170
    y = 18
    lines = [
        ("19-Sep-82 11:44  Scott E  Fahlman", BLACK, fmb),
        ("From: Fahlman at Cmu-20c", BLACK, fm),
        ("", BLACK, fm),
        ("I propose that the following character", BLACK, fm),
        ("sequence for joke markers:", BLACK, fm),
        ("", BLACK, fm),
        ("             :-)", RED, fmb),
        ("", BLACK, fm),
        ("Read it sideways.  Actually, it is", BLACK, fm),
        ("probably more economical to mark", BLACK, fm),
        ("things that are NOT jokes, given", BLACK, fm),
        ("current trends.  For this, use", BLACK, fm),
        ("", BLACK, fm),
        ("             :-(", BLACK, fmb),
    ]
    for t, col, f in lines:
        dr.text((x0, y), t, font=f, fill=col)
        y += 11
    dr.line([x0, 194, 386, 194], fill=RED, width=1)
    dr.text((x0, 200), "44 years old", font=font(FONT_SANS_B, 22), fill=BLACK)
    fs = font(FONT_SANS, 9)
    for i, t in enumerate([
        "CMU computer science bboard, Pittsburgh.",
        "The thread was about a canary in a falling",
        "elevator; nobody could tell the jokes from",
        "the physics. Three characters fixed it.",
    ]):
        dr.text((x0, 232 + 12 * i), t, font=fs, fill=BLACK)
    dr.text((28, 280), "we read it sideways for you", font=font(FONT_SANS, 9), fill=RED)
    return nearest3(img)


# ---------------------------------------------------------------- 4. Equinox
def image4_equinox():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # the diagonal: the line the sun rides at the equinox — due east to due west
    # A black wedge from the bottom-left, its top edge the diagonal.
    dr.polygon([(0, H * s), (0, 205 * s), (W * s, 20 * s), (W * s, 62 * s)], fill=BLACK)
    # thin white hairline inside the wedge for tension
    dr.line([(0, 236 * s), (W * s, 52 * s)], fill=WHITE, width=int(1.0 * s))

    # the sun: a red disc sitting on the horizon-line, half above (day) half below (night)
    cx, cy, r = 228 * s, 118 * s, 62 * s
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    # re-cut the disc with the diagonal: below the line it becomes white on black
    # (build a mask of the half-plane below the top edge of the wedge)
    m = Image.new("L", (W * s, H * s), 0)
    md = ImageDraw.Draw(m)
    md.polygon([(0, H * s), (0, 205 * s), (W * s, 20 * s), (W * s, H * s)], fill=255)
    disc = Image.new("L", (W * s, H * s), 0)
    ImageDraw.Draw(disc).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    both = Image.fromarray(np.minimum(np.asarray(m), np.asarray(disc)))
    img.paste(Image.new("RGB", img.size, WHITE), (0, 0), both)
    small = img.resize((W, H), Image.LANCZOS)
    img, dr = crisp(small)

    # typography (crisp, 1x)
    fbig = font(FONT_FREESANS_B, 50)
    dr.text((14, 4), "EQUI", font=fbig, fill=BLACK)
    dr.text((14, 50), "NOX", font=fbig, fill=BLACK)
    fs = font(FONT_SANS, 9)
    dr.text((16, 104), "the sun crosses the equator", font=fs, fill=BLACK)
    dr.text((16, 116), "rises due east · sets due west", font=fs, fill=BLACK)
    fmid = font(FONT_FREESANS_B, 15)
    dr.text((16, 132), "23·IX·2026", font=fmid, fill=RED)
    dr.text((16, 150), "00:05 UTC", font=fmid, fill=BLACK)
    # bottom-right, on the white below the band
    fw = font(FONT_FREESANS_B, 28)
    dr.text((214, 214), "12h = 12h", font=fw, fill=BLACK)
    dr.text((214, 250), "day and night, for one turn, equal.", font=fs, fill=BLACK)
    dr.text((214, 262), "autumn in the north, spring in the south.", font=fs, fill=BLACK)
    dr.text((214, 280), "in 3 days", font=font(FONT_SANS_B, 10), fill=RED)
    # small black disc: the night side, resting under the band
    dr.ellipse([352, 160, 380, 188], fill=BLACK)
    # rotated label along the diagonal, drawn AA then snapped (it is red on white)
    lab = Image.new("RGBA", (200, 16), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lab)
    ld.fontmode = "1"
    ld.text((0, 1), "HORIZON  ·  秋分  ·  SHŪBUN", font=font(FONT_JP, 12), fill=WHITE + (255,))
    ang = math.degrees(math.atan2(185, 400))
    lab = lab.rotate(ang, expand=True, resample=Image.NEAREST)
    lab = lab.crop(lab.getbbox())
    cx_, cy_ = 118, 212
    img.paste(lab, (cx_ - lab.width // 2, cy_ - lab.height // 2), lab)
    return nearest3(img)


# ---------------------------------------------------------------- 5. Asanoha
def image5_asanoha():
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)
    rng = random.Random(919)

    a = 26.0  # triangle side
    h = a * math.sqrt(3) / 2
    ox, oy = 200.0, 140.0  # a lattice vertex at the picture centre

    def tri_center(p, q, r):
        return ((p[0] + q[0] + r[0]) / 3, (p[1] + q[1] + r[1]) / 3)

    tris = []
    for j in range(-8, 9):
        for i in range(-10, 11):
            x = ox + i * a + (j % 2) * a / 2
            y = oy + j * h
            p = (x, y)
            q = (x + a, y)
            r_up = (x + a / 2, y - h)
            r_dn = (x + a / 2, y + h)
            tris.append((p, q, r_up))
            tris.append((p, q, r_dn))

    # the bloom: every kite that touches one of the "bloom vertices" is red.
    # The six kites around a vertex form a six-pointed hemp-leaf star; seven
    # adjacent stars make one big leaf. A few stray single stars fall outside.
    def kite(v, tri):
        p, q, r = tri
        c = tri_center(p, q, r)
        others = [w for w in (p, q, r) if w != v]
        m1 = ((v[0] + others[0][0]) / 2, (v[1] + others[0][1]) / 2)
        m2 = ((v[0] + others[1][0]) / 2, (v[1] + others[1][1]) / 2)
        return [v, m1, c, m2]

    bloom = [(ox, oy)]
    for k in range(6):
        t = math.radians(60 * k)
        bloom.append((ox + a * math.cos(t), oy + a * math.sin(t)))
    for k in range(6):  # second ring, every other vertex: the leaf's outer points
        t = math.radians(60 * k + 30)
        bloom.append((ox + a * math.sqrt(3) * math.cos(t), oy + a * math.sqrt(3) * math.sin(t)))
    strays = []
    for _ in range(9):
        i, j = rng.randint(-7, 7), rng.randint(-5, 5)
        x = ox + i * a + (j % 2) * a / 2
        y = oy + j * h
        if (x - ox) ** 2 + (y - oy) ** 2 > (3.2 * a) ** 2 and 10 < y < 250:
            strays.append((x, y))
    targets = bloom + strays

    def near(v):
        return any(abs(v[0] - t[0]) < 0.5 and abs(v[1] - t[1]) < 0.5 for t in targets)

    for tri in tris:
        for v in tri:
            if near(v):
                dr.polygon(kite(v, tri), fill=RED)

    # the lattice lines (drawn after fills so they sit on top)
    for (p, q, r) in tris:
        c = tri_center(p, q, r)
        dr.line([p, q], fill=BLACK, width=1)
        dr.line([q, r], fill=BLACK, width=1)
        dr.line([r, p], fill=BLACK, width=1)
        for v in (p, q, r):
            dr.line([c, v], fill=BLACK, width=1)

    # frame + white caption band at the bottom
    dr.rectangle([0, 262, W, H], fill=WHITE)
    dr.line([0, 262, W, 262], fill=BLACK, width=2)
    dr.rectangle([0, 0, W - 1, H - 1], outline=BLACK, width=2)
    dr.fontmode = "1"
    fjp = font(FONT_JP, 16)
    dr.text((14, 270), "麻の葉", font=fjp, fill=BLACK)
    fs = font(FONT_SANS, 9)
    dr.text((72, 270), "ASANOHA, hemp leaf: a triangle lattice, each centre joined to its corners", font=fs, fill=BLACK)
    dr.text((72, 283), "Sewn into newborns' clothes; hemp grows fast and straight. 19 Sep 2026", font=fs, fill=BLACK)
    return nearest3(img)


def main():
    makers = [image1_higanbana, image2_moon, image3_smiley, image4_equinox, image5_asanoha]
    for i, mk in enumerate(makers, 1):
        im = mk()
        assert im.size == (W, H), im.size
        assert im.mode == "P"
        used = set(np.unique(np.asarray(im)))
        assert used <= {0, 1, 2}, used
        path = os.path.join(OUT, f"{i}.png")
        im.save(path, optimize=True)
        print("wrote", path, "colors", sorted(used))


if __name__ == "__main__":
    main()
