#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-23.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

Today's threads:
  1. Antares & the Moon  — tonight's real sky: the waxing gibbous Moon beside
     red Antares in Scorpius (the Moon passes near Antares on Jul 23-24 2026).
  2. Telstar            — on 23 July 1962 the first live transatlantic
     television signal crossed the Atlantic via the Telstar 1 satellite.
  3. Seigaiha (青海波)   — generative overlapping wave-scales; a classic
     Japanese pattern, mined from the standing-interest list.
  4. Kepler-452b        — announced 23 July 2015, "Earth's older cousin".
  5. Dog Days           — a typographic almanac card for late July, the season
     of Sirius, with the week's sky notes.

Technique: tonal scenes render at SSx then LANCZOS downscale + Floyd-Steinberg
dither into the exact 3-color palette; crisp type/line art is drawn directly
on the quantized P image in pure palette indices so edges stay sharp.
"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# palette indices (order below): white=0, black=1, red=2
IW, IB, IR = 0, 1, 2

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


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


def text_center(dr, cx, y, s, fnt, fill, anchor="mm"):
    dr.text((cx, y), s, font=fnt, fill=fill, anchor=anchor)


# ----------------------------------------------------------- 1. Antares & Moon
def image1_antares():
    s = SS
    rng = random.Random(20260723)
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # faint Milky Way glow along the lower-left (galactic centre lies in Scorpius)
    for _ in range(2600):
        t = rng.random()
        cx = (0.10 + 0.55 * t) * W * s
        cy = (1.02 - 0.65 * t) * H * s
        x = rng.gauss(cx, 60 * s)
        y = rng.gauss(cy, 34 * s)
        v = rng.randint(22, 66)
        r = rng.uniform(0.6, 2.2) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # scattered background stars
    for _ in range(320):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, H * s)
        v = rng.randint(90, 210)
        r = rng.uniform(0.5, 1.4) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # Scorpius — stylised fish-hook of the scorpion (x,y in 0..1, brightness)
    scorpius = [
        (0.30, 0.16, 175, "β"),   # claws (upper)
        (0.40, 0.14, 150, "δ"),
        (0.24, 0.24, 140, "π"),
        (0.46, 0.30, 255, "ANTARES"),  # α — the heart
        (0.50, 0.42, 150, "τ"),
        (0.53, 0.52, 150, "ε"),
        (0.58, 0.62, 150, "μ"),
        (0.63, 0.72, 160, "ζ"),
        (0.70, 0.79, 170, "η"),
        (0.78, 0.80, 190, "θ"),   # Sargas
        (0.85, 0.75, 150, "ι"),
        (0.88, 0.66, 150, "κ"),
        (0.83, 0.58, 210, "λ"),   # Shaula — the sting
        (0.78, 0.56, 150, "υ"),
    ]
    pts = [(x * W * s, y * H * s) for (x, y, _, _) in scorpius]

    # connecting lines (thin, dim white)
    for i in range(len(pts) - 1):
        dr.line([pts[i], pts[i + 1]], fill=(120, 120, 120), width=max(1, s // 2))

    # draw the stars (Antares is red + glow)
    for (x, y, _, name), (px, py) in zip(scorpius, pts):
        if name == "ANTARES":
            for gr, gv in [(11, 70), (7, 130), (4.2, 220)]:
                dr.ellipse([px - gr * s, py - gr * s, px + gr * s, py + gr * s],
                           fill=(gv, 0, 0))
            dr.ellipse([px - 2.4 * s, py - 2.4 * s, px + 2.4 * s, py + 2.4 * s],
                       fill=RED)
        else:
            r = (1.3 + (name in ("θ", "λ", "β")) * 1.0) * s
            dr.ellipse([px - r, py - r, px + r, py + r], fill=(240, 240, 240))

    # the waxing gibbous Moon (~65% lit, terminator on the left), upper-right
    mx, my, mr = 0.80 * W * s, 0.20 * H * s, 30 * s
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(245, 245, 245))
    # carve the unlit crescent on the left with an offset black disc
    off = 0.62 * mr
    dr.ellipse([mx - mr - off, my - mr, mx + mr - off, my + mr], fill=(18, 18, 18))
    # a couple of maria
    for dxp, dyp, rr in [(0.35, -0.2, 0.16), (0.5, 0.25, 0.12), (0.2, 0.4, 0.1)]:
        dr.ellipse([mx + dxp * mr - rr * mr, my + dyp * mr - rr * mr,
                    mx + dxp * mr + rr * mr, my + dyp * mr + rr * mr],
                   fill=(205, 205, 205))

    out = finalize(img, dither=True)
    d = ImageDraw.Draw(out)
    f_small = font(FONT_SANS, 11)
    f_lab = font(FONT_SANS_B, 13)
    f_title = font(FONT_SERIF, 15)
    # crisp labels on top
    d.text((13, 12), "SCORPIUS", font=f_lab, fill=IW)
    d.text((13, 27), "the rival of Mars", font=f_small, fill=IW)
    d.text((122, 96), "ANTARES", font=font(FONT_SANS_B, 12), fill=IR)
    d.text((236, 42), "Moon", font=f_small, fill=IW)
    d.text((330, 88), "Shaula", font=f_small, fill=IW)
    # footer bar
    d.line([(13, 278), (387, 278)], fill=IW, width=1)
    d.text((13, 283), "23 July 2026 — waxing gibbous, 65%, beside Antares",
           font=f_small, fill=IW)
    return out


# --------------------------------------------------------------- 2. Telstar
def _icosa_vertices():
    phi = (1 + 5 ** 0.5) / 2
    raw = []
    for a in (1, -1):
        for b in (phi, -phi):
            raw += [(0, a, b), (a, b, 0), (b, 0, a)]
    # dedupe
    seen, verts = set(), []
    for v in raw:
        key = tuple(round(c, 4) for c in v)
        if key not in seen:
            seen.add(key)
            verts.append(v)
    n = math.sqrt(1 + phi * phi)
    return [(x / n, y / n, z / n) for (x, y, z) in verts]


def image2_telstar():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # --- constructivist ground: a red wedge sweeping up from lower-left
    dr.polygon([(0, H * s), (0, 0.62 * H * s), (0.52 * W * s, H * s)], fill=RED)

    # --- the satellite: a white faceted sphere, upper-right
    cx, cy, R = 0.66 * W * s, 0.40 * H * s, 0.30 * H * s
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=WHITE, outline=BLACK,
               width=max(2, s))
    # rotate icosahedron vertices, draw front-facing ones as black pentagons
    verts = _icosa_vertices()
    ax, ay = math.radians(22), math.radians(-34)
    cosx, sinx, cosy, siny = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay)
    proj = []
    for (x, y, z) in verts:
        y2 = y * cosx - z * sinx
        z2 = y * sinx + z * cosx
        x3 = x * cosy + z2 * siny
        z3 = -x * siny + z2 * cosy
        proj.append((x3, y2, z3))
    proj.sort(key=lambda p: p[2])  # back-to-front
    for (x, y, z) in proj:
        if z < -0.05:
            continue
        px, py = cx + x * R, cy - y * R
        fore = 0.45 + 0.55 * max(0.0, z)
        pr = 0.17 * R * fore
        ang0 = math.atan2(y, x)
        poly = []
        for k in range(5):
            a = ang0 + k * 2 * math.pi / 5 + math.pi / 10
            poly.append((px + pr * math.cos(a), py + pr * math.sin(a)))
        dr.polygon(poly, fill=BLACK)
    # a couple of latitude seams for a "signal dish" feel
    for frac in (0.5, 0.78):
        rr = R * frac
        dr.arc([cx - R, cy - rr, cx + R, cy + rr], 200, 340, fill=BLACK,
               width=max(1, s // 2))

    # --- orbit ellipse behind/around
    dr.arc([0.10 * W * s, 0.16 * H * s, 1.02 * W * s, 0.86 * H * s],
           205, 8, fill=BLACK, width=max(1, s))

    # --- transmission: red beam arc from lower-left (America) up to the sat,
    # drawn as a fan of short dashes following a quadratic curve
    ax0, ay0 = 0.10 * W * s, 0.80 * H * s
    bx0, by0 = cx - 0.5 * R, cy + 0.55 * R
    ctrlx, ctrly = 0.30 * W * s, 0.08 * H * s
    prev = None
    for i in range(41):
        t = i / 40
        x = (1 - t) ** 2 * ax0 + 2 * (1 - t) * t * ctrlx + t * t * bx0
        y = (1 - t) ** 2 * ay0 + 2 * (1 - t) * t * ctrly + t * t * by0
        if prev and i % 2 == 0:
            dr.line([prev, (x, y)], fill=RED, width=max(2, int(1.6 * s)))
        prev = (x, y)
    # small ground station triangle at the start
    dr.polygon([(ax0 - 6 * s, ay0), (ax0 + 6 * s, ay0), (ax0, ay0 - 12 * s)],
               fill=BLACK)

    out = finalize(img, dither=False)
    d = ImageDraw.Draw(out)
    d.text((20, 18), "TELSTAR", font=font(FONT_SANS_B, 34), fill=IB)
    d.text((22, 56), "23 JULY 1962", font=font(FONT_MONO_B, 15), fill=IR)
    d.text((20, 250), "first live television across the Atlantic",
           font=font(FONT_SANS, 13), fill=IB)
    d.text((20, 268), "88-cm sphere · 950 km up · a picture in a heartbeat",
           font=font(FONT_SANS, 11), fill=IB)
    return out


# --------------------------------------------------------------- 3. Seigaiha
def image3_seigaiha():
    s = SS
    rng = random.Random(723723)
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    R = 30 * s          # fan radius
    n_arc = 5           # concentric arcs per fan
    dx = R              # horizontal spacing (fans overlap by R each side)
    dy = R * 0.5        # vertical spacing
    lw = max(1, int(0.9 * s))

    rows = int(H * s / dy) + 3
    cols = int(W * s / dx) + 3
    for j in range(rows):
        yc = j * dy
        xoff = (j % 2) * (dx / 2)
        for i in range(cols):
            xc = i * dx - dx + xoff
            # every so often a red-crested wave
            red_fan = ((i * 7 + j * 3) % 23 == 0)
            for k in range(n_arc):
                rr = R * (1 - k / n_arc)
                col = RED if (red_fan and k >= n_arc - 2) else BLACK
                dr.arc([xc - rr, yc - rr, xc + rr, yc + rr], 180, 360,
                       fill=col, width=lw)

    out = finalize(img, dither=False)
    d = ImageDraw.Draw(out)
    # a clean white plate for the title so it stays legible
    d.rectangle([12, 250, 388, 288], fill=IW)
    d.line([(12, 250), (388, 250)], fill=IB, width=1)
    d.text((18, 256), "青海波", font=font(FONT_JP, 24), fill=IB)
    d.text((92, 258), "SEIGAIHA", font=font(FONT_SANS_B, 15), fill=IR)
    d.text((92, 275), "the blue-sea-wave — calm seas, endless good fortune",
           font=font(FONT_SANS, 10), fill=IB)
    return out


# ------------------------------------------------------------- 4. Kepler-452b
def _shaded_sphere(diam, light=(-0.5, -0.6, 0.62), seed=0, bands=False):
    """Return (rgb_array uint8 grayscale, alpha uint8) for a lit sphere."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:diam, 0:diam].astype(np.float64)
    r = diam / 2.0
    nx = (x - r) / r
    ny = (y - r) / r
    d2 = nx * nx + ny * ny
    mask = d2 <= 1.0
    nz = np.sqrt(np.clip(1 - d2, 0, 1))
    lx, ly, lz = light
    ln = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx, ly, lz = lx / ln, ly / ln, lz / ln
    shade = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    shade = 0.10 + 0.9 * shade ** 0.9
    # texture
    if bands:
        tex = 0.12 * np.sin(ny * 9 + 0.6 * np.sin(nx * 4))
    else:
        # low-freq mottling -> continents
        noise = rng.standard_normal((diam // 8 + 2, diam // 8 + 2))
        big = np.array(Image.fromarray(
            ((noise - noise.min()) / (np.ptp(noise) + 1e-6) * 255).astype(np.uint8)
        ).resize((diam, diam), Image.BICUBIC), dtype=np.float64) / 255.0
        tex = 0.22 * (big - 0.5)
    val = np.clip(shade + tex, 0, 1)
    # limb darkening
    val *= (0.55 + 0.45 * nz)
    gray = (val * 255).astype(np.uint8)
    alpha = (mask * 255).astype(np.uint8)
    return gray, alpha


def image4_kepler():
    s = 3
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # starry top band? keep it clean, white poster. baseline
    baseline = int(0.60 * H * s)

    # Earth (left, smaller)
    de = int(70 * s)
    ge, ae = _shaded_sphere(de, seed=1, bands=False)
    earth = Image.merge("RGBA", [Image.fromarray(ge)] * 3 + [Image.fromarray(ae)])
    ex = int(0.28 * W * s - de / 2)
    ey = baseline - de
    img.paste(earth, (ex, ey), earth)

    # Kepler-452b (right, ~1.6x)
    dk = int(112 * s)
    gk, ak = _shaded_sphere(dk, seed=7, bands=True)
    kep = Image.merge("RGBA", [Image.fromarray(gk)] * 3 + [Image.fromarray(ak)])
    kx = int(0.70 * W * s - dk / 2)
    ky = baseline - dk
    img.paste(kep, (kx, ky), kep)
    # red highlight arc on Kepler-452b's lit limb
    dr.arc([kx, ky, kx + dk, ky + dk], -70, 40, fill=RED, width=max(2, s))

    out = finalize(img, dither=True)
    d = ImageDraw.Draw(out)
    # crisp type
    d.text((200, 20), "KEPLER-452b", font=font(FONT_SANS_B, 26), fill=IB,
           anchor="mm")
    d.text((200, 40), "Earth's older cousin", font=font(FONT_SERIF, 13),
           fill=IR, anchor="mm")
    # baselines / labels
    d.text((int(0.28 * W), 205), "EARTH", font=font(FONT_SANS_B, 12), fill=IB,
           anchor="mm")
    d.text((int(0.70 * W), 190), "KEPLER-452b", font=font(FONT_SANS_B, 12),
           fill=IB, anchor="mm")
    d.text((int(0.70 * W), 203), "~1.6× Earth", font=font(FONT_SANS, 10),
           fill=IB, anchor="mm")
    # fact strip
    d.line([(16, 222), (384, 222)], fill=IB, width=1)
    facts = [
        "1,400 light-years away, in Cygnus",
        "orbits a Sun-like star every 385 days",
        "in the habitable zone — liquid water could pool",
        "announced 23 July 2015 by NASA's Kepler mission",
    ]
    yy = 230
    for fct in facts:
        d.ellipse([18, yy + 3, 23, yy + 8], fill=IR)
        d.text((30, yy), fct, font=font(FONT_SANS, 11), fill=IB)
        yy += 16
    return out


# --------------------------------------------------------------- 5. Dog Days
def image5_dogdays():
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)
    rng = random.Random(52526)

    # faint star dust
    for _ in range(260):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, H * s)
        v = rng.randint(60, 150)
        r = rng.uniform(0.5, 1.3) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # Canis Major, stylised, lower-right; Sirius as the bright (red) star
    cm = [
        (0.62, 0.40, "Sirius", 255),
        (0.72, 0.30, "", 150),
        (0.82, 0.34, "Wezen-ish", 150),
        (0.90, 0.44, "", 150),
        (0.80, 0.52, "Adhara", 170),
        (0.70, 0.55, "", 140),
        (0.60, 0.52, "", 140),
    ]
    pts = [(x * W * s, y * H * s) for (x, y, _, _) in cm]
    order = [0, 1, 2, 3, 4, 5, 6, 0]
    for a, b in zip(order, order[1:]):
        dr.line([pts[a], pts[b]], fill=(110, 110, 110), width=max(1, s // 2))
    for (x, y, name, _), (px, py) in zip(cm, pts):
        if name == "Sirius":
            for gr, gv in [(10, 90), (6, 160), (3.5, 255)]:
                dr.ellipse([px - gr * s, py - gr * s, px + gr * s, py + gr * s],
                           fill=(gv, 0, 0))
            dr.ellipse([px - 2.2 * s, py - 2.2 * s, px + 2.2 * s, py + 2.2 * s],
                       fill=RED)
        else:
            dr.ellipse([px - 1.6 * s, py - 1.6 * s, px + 1.6 * s, py + 1.6 * s],
                       fill=(235, 235, 235))

    out = finalize(img, dither=True)
    d = ImageDraw.Draw(out)
    # big type upper-left
    d.text((20, 20), "THE", font=font(FONT_SERIF, 20), fill=IW)
    d.text((18, 40), "DOG DAYS", font=font(FONT_SANS_B, 40), fill=IR)
    d.text((22, 88), "of summer", font=font(FONT_SERIF, 20), fill=IW)
    d.text((22, 118),
           "late July: Sirius, the Dog Star, rises",
           font=font(FONT_SANS, 11), fill=IW)
    d.text((22, 132),
           "with the Sun — the year's hottest weeks.",
           font=font(FONT_SANS, 11), fill=IW)
    d.text((int(0.62 * W) + 14, int(0.40 * H) - 2), "Sirius",
           font=font(FONT_SANS_B, 11), fill=IR)
    d.text((int(0.78 * W), int(0.40 * H) + 62), "CANIS MAJOR",
           font=font(FONT_SANS, 9), fill=IW, anchor="mm")
    # almanac strip
    d.line([(20, 210), (250, 210)], fill=IW, width=1)
    d.text((20, 216), "THIS WEEK'S SKY", font=font(FONT_MONO_B, 11), fill=IW)
    notes = [
        "Jul 23  Moon beside red Antares",
        "Jul 28  δ-Aquariid meteors peak",
        "Jul 29  Full Buck Moon",
    ]
    yy = 234
    for nt in notes:
        d.ellipse([20, yy + 3, 25, yy + 8], fill=IR)
        d.text((32, yy), nt, font=font(FONT_MONO, 11), fill=IW)
        yy += 17
    return out


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(os.path.join(here, "..", ".."))
    builders = [
        image1_antares, image2_telstar, image3_seigaiha,
        image4_kepler, image5_dogdays,
    ]
    for i, b in enumerate(builders, 1):
        out = b()
        assert out.size == (W, H)
        out.save(os.path.join(here, f"{i}.png"))
        out.save(os.path.join(repo, "images", f"{i}.png"))
        print(f"wrote {i}.png ({b.__name__})")


if __name__ == "__main__":
    main()
