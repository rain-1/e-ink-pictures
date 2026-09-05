#!/usr/bin/env python3
"""
2026-09-05 — Voyager Day.
Five pictures for a 400x300 black/white/red e-ink panel.

  1. The Cover        — a re-drawing of the Golden Record cover: pulsar map, hydrogen clock, the record and its stylus
  2. Red Wedge        — a constructivist poster: Voyager as Lissitzky's red wedge piercing the heliosphere
  3. That Dot         — the Pale Blue Dot, in a palette with no blue: sunbeams of dither and one red pixel
  4. September Sky    — this week's sky, tonight's moon, and the countdown to one light-day
  5. Eighty           — Freddie Mercury, born Stone Town, 5 September 1946

Run: python3 generate.py  -> images/1.png … images/5.png
"""
import math
import random
import datetime as dt
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H = 400, 300
S = 3                      # supersample factor
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
PALETTE = list(BLACK + WHITE + RED) + [0, 0, 0] * 253
TODAY = dt.date(2026, 9, 5)

FONT_DIR = "/usr/share/fonts/truetype/"
FONTS = {
    "sans": FONT_DIR + "dejavu/DejaVuSans.ttf",
    "sansb": FONT_DIR + "dejavu/DejaVuSans-Bold.ttf",
    "serif": FONT_DIR + "dejavu/DejaVuSerif.ttf",
    "serifb": FONT_DIR + "dejavu/DejaVuSerif-Bold.ttf",
    "mono": FONT_DIR + "dejavu/DejaVuSansMono.ttf",
    "monob": FONT_DIR + "dejavu/DejaVuSansMono-Bold.ttf",
    "lsansb": FONT_DIR + "liberation/LiberationSans-Bold.ttf",
    "lserif": FONT_DIR + "liberation/LiberationSerif-Regular.ttf",
    "lserifi": FONT_DIR + "liberation/LiberationSerif-Italic.ttf",
}


def font(name, size):
    return ImageFont.truetype(FONTS[name], size)


def pal_image():
    p = Image.new("P", (1, 1))
    p.putpalette(PALETTE)
    return p


def to_palette(img, dither):
    """Snap an RGB image to the exact 3-colour palette."""
    img = img.convert("RGB")
    q = img.quantize(palette=pal_image(),
                     dither=Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE)
    return q


def finish_hard(img):
    """3x render with anti-aliasing -> 1x, then nearest colour (clean edges, no dither)."""
    small = img.resize((W, H), Image.Resampling.LANCZOS)
    return to_palette(small, dither=False)


def finish_soft(img):
    """3x render -> 1x, then Floyd–Steinberg dither (for gradients and tone)."""
    small = img.resize((W, H), Image.Resampling.LANCZOS)
    return to_palette(small, dither=True)


def canvas(bg=WHITE, scale=S):
    img = Image.new("RGB", (W * scale, H * scale), bg)
    return img, ImageDraw.Draw(img)


def text_rotated(base, xy, text, fnt, fill, angle, anchor="mm"):
    """Draw text rotated by `angle` degrees, centred on xy."""
    bbox = fnt.getbbox(text)
    tw, th = bbox[2] - bbox[0] + 8, bbox[3] - bbox[1] + 8
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text((4 - bbox[0], 4 - bbox[1]), text, font=fnt, fill=fill)
    layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    x, y = xy
    base.paste(layer, (int(x - layer.width / 2), int(y - layer.height / 2)), layer)


# ----------------------------------------------------------------------------
# 1. The Cover — Golden Record, re-engraved in black, white and red
# ----------------------------------------------------------------------------
def image_1():
    rng = random.Random(19770905)
    img, d = canvas(BLACK)
    lw = 3  # engraved line weight at 3x

    # --- top left: the record, seen from above, with the stylus arm ---
    cx, cy, r = 105 * S, 82 * S, 62 * S
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=WHITE, width=lw)
    for rr in range(14, 60, 6):  # grooves
        rr *= S
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=BLACK, width=2)
    d.ellipse([cx - 6 * S, cy - 6 * S, cx + 6 * S, cy + 6 * S], fill=BLACK, outline=WHITE, width=lw)
    # stylus / cartridge hanging over the record from the top right
    ax, ay = cx + 84 * S, cy - 76 * S
    d.line([ax, ay, cx + 16 * S, cy - 22 * S], fill=WHITE, width=lw + 1)
    d.rectangle([ax - 5 * S, ay - 5 * S, ax + 5 * S, ay + 5 * S], fill=WHITE)
    d.polygon([(cx + 16 * S, cy - 22 * S), (cx + 26 * S, cy - 28 * S), (cx + 22 * S, cy - 14 * S)], fill=WHITE)
    # binary time under the record: one rotation = 3.6 s written in hydrogen ticks
    bits = "100110000110010000000000000000000000000"
    bx, by = 44 * S, 152 * S
    for i, b in enumerate(bits[:24]):
        x = bx + i * 5 * S
        d.line([x, by, x, by - (7 if b == "1" else 3) * S], fill=WHITE, width=2)
    d.line([bx, by, bx + 23 * 5 * S, by], fill=WHITE, width=2)

    # --- top right: side view of the record and the stylus ---
    sx, sy = 262 * S, 60 * S
    d.rectangle([sx, sy + 40 * S, sx + 120 * S, sy + 46 * S], fill=WHITE)
    d.line([sx + 60 * S, sy + 40 * S, sx + 60 * S, sy - 2 * S], fill=WHITE, width=lw)
    d.polygon([(sx + 60 * S, sy + 40 * S), (sx + 52 * S, sy + 22 * S), (sx + 68 * S, sy + 22 * S)], fill=WHITE)
    d.line([sx + 60 * S, sy - 2 * S, sx + 118 * S, sy - 2 * S], fill=WHITE, width=lw)
    # the wave the stylus reads (video signal encoding a picture)
    pts = []
    for i in range(0, 120):
        x = sx + i * S
        y = sy + 66 * S + (math.sin(i * 0.6) * 4 + math.sin(i * 1.7) * 2) * S
        pts.append((x, y))
    d.line(pts, fill=WHITE, width=2)
    # the picture raster that the wave decodes into
    gx, gy = sx + 20 * S, sy + 80 * S
    for row in range(8):
        d.line([gx, gy + row * 4 * S, gx + 80 * S, gy + row * 4 * S], fill=WHITE, width=1)
    d.rectangle([gx, gy, gx + 80 * S, gy + 28 * S], outline=WHITE, width=2)
    d.ellipse([gx + 30 * S, gy + 4 * S, gx + 50 * S, gy + 24 * S], outline=RED, width=lw)  # the circle test image

    # --- bottom left: the pulsar map ---
    px, py = 108 * S, 232 * S
    # 14 pulsars: (angle deg, length px) — spread the way the real map is: a burst of long spokes
    spokes = [(8, 62), (25, 48), (41, 70), (63, 55), (86, 40), (108, 66), (131, 52),
              (156, 64), (178, 44), (201, 58), (226, 50), (250, 68), (283, 46), (312, 60)]
    for ang, ln in spokes:
        a = math.radians(ang)
        ex, ey = px + math.cos(a) * ln * S, py - math.sin(a) * ln * S
        d.line([px, py, ex, ey], fill=WHITE, width=2)
        # binary period ticks along the spoke
        nbits = rng.randint(9, 15)
        for i in range(nbits):
            t = 0.18 + 0.78 * i / nbits
            tx, ty = px + (ex - px) * t, py + (ey - py) * t
            nx, ny = -(ey - py), (ex - px)
            nl = math.hypot(nx, ny)
            nx, ny = nx / nl, ny / nl
            tl = (4 if rng.random() < 0.5 else 2) * S
            d.line([tx, ty, tx + nx * tl, ty + ny * tl], fill=WHITE, width=2)
    # the long line to the galactic centre
    d.line([px, py, px + 150 * S, py + 4 * S], fill=WHITE, width=2)
    d.ellipse([px - 4 * S, py - 4 * S, px + 4 * S, py + 4 * S], fill=RED)

    # --- bottom right: the hydrogen atom, the clock everything is measured by ---
    hx, hy = 312 * S, 224 * S
    for k, (dx, spin) in enumerate([(-34, 1), (34, -1)]):
        c = hx + dx * S
        d.ellipse([c - 22 * S, hy - 22 * S, c + 22 * S, hy + 22 * S], outline=WHITE, width=lw)
        d.ellipse([c - 3 * S, hy - 3 * S, c + 3 * S, hy + 3 * S], fill=WHITE)
        # spin arrow on the nucleus and on the electron
        d.line([c, hy - 12 * S, c, hy + 12 * S], fill=WHITE, width=2)
        d.polygon([(c, hy - 14 * S * spin), (c - 3 * S, hy - 8 * S * spin), (c + 3 * S, hy - 8 * S * spin)], fill=WHITE)
        d.ellipse([c + 22 * S - 3 * S, hy - 3 * S, c + 22 * S + 3 * S, hy + 3 * S], fill=RED)
    d.line([hx - 12 * S, hy + 34 * S, hx + 12 * S, hy + 34 * S], fill=WHITE, width=lw)
    d.line([hx, hy + 30 * S, hx, hy + 38 * S], fill=WHITE, width=lw)  # the "1": one unit of time
    d.text((hx, hy + 50 * S), "1", font=font("mono", 13 * S), fill=RED, anchor="mm")

    # --- caption ---
    d.text((8 * S, 291 * S), "THE SOUNDS OF EARTH", font=font("sansb", 8 * S), fill=WHITE, anchor="ls")
    d.text((392 * S, 291 * S), "VOYAGER 1 · launched 5 Sep 1977 · 49 years out", font=font("sans", 7 * S),
           fill=WHITE, anchor="rs")
    return finish_hard(img)


# ----------------------------------------------------------------------------
# 2. Red Wedge — Lissitzky's poster, re-aimed at interstellar space
# ----------------------------------------------------------------------------
def image_2():
    img, d = canvas(WHITE)
    # the diagonal split: white (the known solar system) / black (interstellar space)
    d.polygon([(150 * S, 0), (W * S, 0), (W * S, H * S), (330 * S, H * S)], fill=BLACK)
    # the heliosphere: a white circle sitting on the boundary
    cx, cy, r = 262 * S, 138 * S, 92 * S
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=BLACK, width=2 * S)
    # a thin second ring — the termination shock
    r2 = 62 * S
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=BLACK, width=S)
    # the sun and the planets as small marks inside
    d.ellipse([cx - 7 * S, cy - 7 * S, cx + 7 * S, cy + 7 * S], fill=BLACK)
    for k, dist in enumerate([14, 19, 24, 30, 42, 50]):
        a = math.radians(200 + k * 23)
        px, py = cx + math.cos(a) * dist * S, cy + math.sin(a) * dist * S
        rr = (3 if k in (3, 4) else 2) * S
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=BLACK)
    # the red wedge: from the lower left, through the sun, out past the heliopause
    tip = (cx + 118 * S, cy - 76 * S)
    base_c = (20 * S, 262 * S)
    ux, uy = tip[0] - base_c[0], tip[1] - base_c[1]
    L = math.hypot(ux, uy)
    nx, ny = -uy / L, ux / L
    hw = 46 * S
    d.polygon([tip, (base_c[0] + nx * hw, base_c[1] + ny * hw), (base_c[0] - nx * hw, base_c[1] - ny * hw)], fill=RED)
    # small projectiles in the constructivist manner
    d.rectangle([40 * S, 40 * S, 62 * S, 62 * S], fill=BLACK)
    d.rectangle([70 * S, 52 * S, 82 * S, 64 * S], fill=RED)
    d.ellipse([28 * S, 200 * S, 44 * S, 216 * S], outline=BLACK, width=2 * S)
    d.rectangle([330 * S, 236 * S, 386 * S, 244 * S], fill=WHITE)
    d.rectangle([346 * S, 252 * S, 386 * S, 258 * S], fill=RED)
    d.ellipse([354 * S, 40 * S, 366 * S, 52 * S], fill=WHITE)
    d.polygon([(372 * S, 268 * S), (392 * S, 268 * S), (392 * S, 288 * S)], fill=WHITE)
    # the words follow the wedge
    ang = math.degrees(math.atan2(-uy, ux))
    text_rotated(img, (150 * S, 178 * S), "VOYAGER", font("lsansb", 26 * S), WHITE, ang)
    text_rotated(img, (92 * S, 224 * S), "BEYOND THE HELIOPAUSE", font("lsansb", 9 * S), BLACK, ang)
    d.text((10 * S, 12 * S), "1977", font=font("lsansb", 22 * S), fill=BLACK)
    d.text((392 * S, 292 * S), "∞", font=font("sans", 22 * S), fill=WHITE, anchor="rs")
    return finish_hard(img)


# ----------------------------------------------------------------------------
# 3. That Dot — the Pale Blue Dot without any blue
# ----------------------------------------------------------------------------
def image_3():
    rng = np.random.default_rng(14021990)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    # three sunbeams: bands of scattered light crossing the frame at a steep diagonal
    lum = np.zeros((H, W))
    ang = math.radians(72)
    dirx, diry = math.cos(ang), math.sin(ang)
    # signed distance to a line through (x0, 0) at that angle
    def band(x0, width, strength):
        dist = (xx - x0) * diry - (yy - 0) * dirx
        return strength * np.exp(-(dist / width) ** 2)
    lum += band(118, 26, 0.55)
    lum += band(206, 14, 0.85)
    lum += band(296, 34, 0.35)
    # gentle vertical fall-off, the glare fades toward the bottom
    lum *= (1.0 - 0.45 * (yy / H))
    # fine grain of the original vidicon frame, and a floor so the dark sky stays truly black
    lum += rng.normal(0, 0.025, (H, W))
    lum = np.clip(lum - 0.04, 0, 1)
    # fade everything out under the caption
    lum *= np.clip((262 - yy) / 22.0, 0, 1)
    gray = (lum * 255).astype(np.uint8)
    img = Image.fromarray(gray, "L").convert("RGB")
    q = to_palette(img, dither=True).convert("RGB")
    d = ImageDraw.Draw(q)
    # the dot itself: sits inside the brightest beam, a little below centre
    dx, dy = 213, 176
    d.rectangle([dx - 2, dy - 2, dx + 1, dy + 1], fill=RED)
    # caption, rendered crisp at 3x on its own black strip
    cap, cd = canvas(BLACK)
    cd.text((12 * S, 268 * S), "That's here. That's home. That's us.", font=font("lserifi", 14 * S), fill=WHITE)
    cd.text((12 * S, 286 * S), "Voyager 1 · 14 February 1990 · 6 billion km · Earth is 0.12 of a pixel",
            font=font("sans", 7 * S), fill=WHITE)
    cap = finish_hard(cap).convert("RGB")
    q.paste(cap.crop((0, 262, W, H)), (0, 262))
    return to_palette(q, dither=False)


# ----------------------------------------------------------------------------
# 4. September Sky — an almanac card
# ----------------------------------------------------------------------------
def draw_moon(d, cx, cy, r, illum, waning=True):
    """Draw a moon of the given illuminated fraction at 3x. Lit limb on the left when waning."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK)
    # lit portion: scan lines
    k = 1 - 2 * illum  # terminator ellipse half-width fraction (signed)
    for y in range(-r, r + 1):
        half = math.sqrt(max(r * r - y * y, 0))
        tx = k * half  # terminator x at this row
        if waning:
            x0, x1 = -half, tx
        else:
            x0, x1 = tx, half
        if x1 > x0:
            d.line([cx + x0, cy + y, cx + x1, cy + y], fill=WHITE)
    # a few maria as small dark patches on the lit side (waning => left side)
    for (mx, my, mr) in [(-0.38, -0.3, 0.17), (-0.52, 0.18, 0.13), (-0.2, 0.36, 0.1)]:
        px, py, pr = cx + mx * r, cy + my * r, mr * r
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(150, 150, 150))


def image_4():
    img, d = canvas(WHITE)
    # header band
    d.rectangle([0, 0, W * S, 34 * S], fill=BLACK)
    d.text((10 * S, 17 * S), "SEPTEMBER SKY", font=font("sansb", 15 * S), fill=WHITE, anchor="lm")
    d.text((390 * S, 17 * S), "Sat 5 Sep 2026", font=font("sans", 9 * S), fill=RED, anchor="rm")
    # tonight's moon
    draw_moon(d, 68 * S, 108 * S, 46 * S, illum=0.40, waning=True)
    d.text((68 * S, 166 * S), "waning crescent", font=font("sansb", 8 * S), fill=BLACK, anchor="mm")
    d.text((68 * S, 178 * S), "40% · rises after midnight", font=font("sans", 7 * S), fill=BLACK, anchor="mm")
    d.text((68 * S, 190 * S), "new moon Thu 11th", font=font("sans", 7 * S), fill=RED, anchor="mm")
    # the events
    events = [
        ("6", "Moon beside Mars before dawn"),
        ("8", "Moon < 1° from Jupiter, pre-dawn"),
        ("9", "Thin crescent near Regulus"),
        ("18", "Venus at peak brilliance, dusk"),
        ("23", "Equinox, 00:06 UTC"),
        ("26", "Full Moon · Neptune at opposition"),
    ]
    y = 52 * S
    for day, what in events:
        d.text((178 * S, y), day, font=font("sansb", 12 * S), fill=RED, anchor="rm")
        d.text((186 * S, y), what, font=font("sans", 9 * S), fill=BLACK, anchor="lm")
        d.line([148 * S, y + 11 * S, 392 * S, y + 11 * S], fill=(200, 200, 200), width=1)
        y += 24 * S
    # footer: the countdown that matters this autumn
    d.rectangle([0, 214 * S, W * S, 300 * S], fill=WHITE)
    d.line([12 * S, 214 * S, 388 * S, 214 * S], fill=BLACK, width=2)
    days_left = (dt.date(2026, 11, 18) - TODAY).days
    d.text((12 * S, 226 * S), "VOYAGER 1", font=font("sansb", 9 * S), fill=BLACK, anchor="lm")
    d.text((12 * S, 240 * S), "25.5 billion km out · signal takes 23 h to arrive",
           font=font("sans", 8 * S), fill=BLACK, anchor="lm")
    # progress bar to one light-day (25.902 billion km)
    frac = 25.5 / 25.902
    bx0, bx1, by0, by1 = 12 * S, 388 * S, 254 * S, 268 * S
    d.rectangle([bx0, by0, bx1, by1], outline=BLACK, width=2)
    d.rectangle([bx0 + 2, by0 + 2, bx0 + int((bx1 - bx0) * frac), by1 - 2], fill=RED)
    d.text((bx1, by1 + 6 * S), "one light-day, 18 Nov 2026", font=font("sans", 7 * S), fill=BLACK, anchor="rt")
    d.text((bx0, by1 + 6 * S), f"{days_left} days to go", font=font("sansb", 7 * S), fill=RED, anchor="lt")
    return finish_soft(img)


# ----------------------------------------------------------------------------
# 5. Eighty — Freddie Mercury, 5 September 1946
# ----------------------------------------------------------------------------
def image_5():
    img, d = canvas(WHITE)
    # a piano keyboard across the middle
    top, bot = 118 * S, 196 * S
    nwhite = 21
    kw = W * S / nwhite
    for i in range(nwhite):
        x0 = i * kw
        d.rectangle([x0, top, x0 + kw, bot], fill=WHITE, outline=BLACK, width=2)
    # black keys: pattern over an octave starting at C: C# D# _ F# G# A# _
    pattern = [1, 1, 0, 1, 1, 1, 0]
    for i in range(nwhite - 1):
        if pattern[i % 7]:
            x0 = (i + 1) * kw - kw * 0.3
            d.rectangle([x0, top, x0 + kw * 0.6, top + (bot - top) * 0.62], fill=BLACK)
    # one red key: the note the whole room is waiting for
    i = 10
    x0 = (i + 1) * kw - kw * 0.3
    d.rectangle([x0, top, x0 + kw * 0.6, top + (bot - top) * 0.62], fill=RED)
    # the big number
    d.text((200 * S, 62 * S), "80", font=font("lsansb", 104 * S), fill=BLACK, anchor="mm")
    # a small crown above the number, drawn from polygons
    cx, cy = 200 * S, 8 * S
    d.polygon([(cx - 30 * S, cy + 16 * S), (cx - 34 * S, cy - 2 * S), (cx - 16 * S, cy + 6 * S), (cx, cy - 8 * S),
               (cx + 16 * S, cy + 6 * S), (cx + 34 * S, cy - 2 * S), (cx + 30 * S, cy + 16 * S)], fill=RED)
    d.rectangle([cx - 30 * S, cy + 16 * S, cx + 30 * S, cy + 20 * S], fill=BLACK)
    # the text below
    d.text((200 * S, 216 * S), "FREDDIE MERCURY", font=font("lsansb", 20 * S), fill=BLACK, anchor="mm")
    d.text((200 * S, 236 * S), "Farrokh Bulsara · born Stone Town, Zanzibar · 5 September 1946",
           font=font("sans", 8 * S), fill=BLACK, anchor="mm")
    d.line([120 * S, 250 * S, 280 * S, 250 * S], fill=RED, width=2 * S)
    d.text((200 * S, 266 * S), "four octaves, one moustache, no half measures",
           font=font("lserifi", 11 * S), fill=BLACK, anchor="mm")
    d.text((200 * S, 286 * S), "also today: Voyager 1 leaves Earth, 1977 · Louis XIV born, 1638 · Great Fire of London out, 1666",
           font=font("sans", 7 * S), fill=BLACK, anchor="mm")
    return finish_hard(img)


if __name__ == "__main__":
    import os
    os.makedirs("images", exist_ok=True)
    for i, fn in enumerate([image_1, image_2, image_3, image_4, image_5], start=1):
        out = fn()
        assert out.size == (W, H), out.size
        out.save(f"images/{i}.png", optimize=True)
        print(f"images/{i}.png  ok")
