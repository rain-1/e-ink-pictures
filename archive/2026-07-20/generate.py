#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-20.

Theme: TWO WORLDS. July 20 is the only date on which humanity has touched two
other worlds — Apollo 11 set down in the Sea of Tranquility (1969) and, seven
years later to the day, Viking 1 became the first U.S. craft to land on Mars,
in Chryse Planitia (1976). Today is Viking 1's 50th anniversary.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Tonal scenes render at 3x then Floyd-Steinberg
dither into the exact palette; hard-edged constructivist/line work renders at
1x in pure palette colors.

Technique discovered today: the panel's single red can act as a *tonal field*,
not just an accent — dithering red-with-white yields a stippled pink and
red-with-black a maroon, which is exactly the palette Mars wants. See image 2.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3  # supersample factor
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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
    """Downscale (if supersampled) and quantize to the exact 3-color palette."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


# ==================================================== 1. Sea of Tranquility
def image1_tranquility():
    """Apollo 11 on the Moon, July 20 1969. Black sky, dithered gray regolith,
    the LM Eagle, the flag (the one true red accent), Earth hanging overhead."""
    rng = random.Random(19690720)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    horizon = 176  # lunar-surface horizon in 1x units
    hy = horizon * s

    # --- starless black sky (the Moon has no atmosphere; only a few faint) ---
    for _ in range(40):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, hy - 8 * s)
        v = rng.randint(70, 150)
        dr.point((x, y), fill=(v, v, v))

    # --- Earth, gibbous, hanging in the black sky ---
    ex, ey, er = 322, 60, 34
    ex, ey, er = ex * s, ey * s, er * s
    # ocean base (mid gray dithers to a soft tone)
    dr.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(120, 120, 120))
    # continents (lighter blotches)
    for _ in range(26):
        a = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(0, 0.82) * er
        cx = ex + rad * math.cos(a)
        cy = ey + rad * math.sin(a)
        cr = rng.uniform(3, 9) * s
        dr.ellipse([cx - cr, cy - cr * 0.8, cx + cr, cy + cr * 0.8],
                   fill=(215, 215, 215))
    # cloud swirls
    for _ in range(30):
        a = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(0, 0.9) * er
        cx = ex + rad * math.cos(a)
        cy = ey + rad * math.sin(a)
        cr = rng.uniform(2, 5) * s
        dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(245, 245, 245))
    # shadow terminator: darken the lower-left crescent
    for _ in range(1400):
        a = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(0, 1.0) * er
        cx = ex + rad * math.cos(a)
        cy = ey + rad * math.sin(a)
        # phase plane: darken where (dx*0.7 + dy*0.7) beyond a threshold
        d = (cx - ex) * -0.6 + (cy - ey) * 0.8
        if d > 6 * s and (cx - ex) ** 2 + (cy - ey) ** 2 <= er * er:
            k = min(1.0, (d - 6 * s) / (er))
            if rng.random() < k:
                dr.point((cx, cy), fill=BLACK)
    dr.ellipse([ex - er, ey - er, ex + er, ey + er], outline=(150, 150, 150),
               width=s)

    # --- lunar surface: bright gray regolith, gently rolling ---
    dr.rectangle([0, hy, W * s, H * s], fill=(210, 210, 210))
    # subtle tonal variation + scattered pebbles/craters for texture
    for _ in range(2600):
        x = rng.uniform(0, W * s)
        y = rng.uniform(hy + 2 * s, H * s)
        depth = (y - hy) / (H * s - hy)
        cr = rng.uniform(0.6, 3.2) * s * (0.5 + depth)
        v = rng.choice([170, 185, 190, 230, 240])
        dr.ellipse([x - cr, y - cr * 0.7, x + cr, y + cr * 0.7], fill=(v, v, v))
    # a few small craters with shadowed rims
    for _ in range(22):
        x = rng.uniform(20 * s, (W - 20) * s)
        y = rng.uniform(hy + 10 * s, H * s - 6 * s)
        cr = rng.uniform(4, 11) * s
        dr.ellipse([x - cr, y - cr * 0.55, x + cr, y + cr * 0.55],
                   fill=(150, 150, 150))
        dr.arc([x - cr, y - cr * 0.55, x + cr, y + cr * 0.55], 20, 160,
               fill=(90, 90, 90), width=s)

    # --- the Lunar Module "Eagle" (simplified, foil-gold rendered as light) ---
    lmx, lmy = 96, horizon  # base of descent stage sits on horizon
    lmx = lmx * s
    base_y = (horizon + 6) * s
    # descent stage: a squat octagon-ish box
    dsw, dsh = 34 * s, 20 * s
    dsx0, dsy0 = lmx - dsw / 2, base_y - dsh
    dr.polygon([(dsx0 + 4 * s, dsy0), (dsx0 + dsw - 4 * s, dsy0),
                (dsx0 + dsw, dsy0 + 6 * s), (dsx0 + dsw, dsy0 + dsh),
                (dsx0, dsy0 + dsh), (dsx0, dsy0 + 6 * s)], fill=(225, 225, 225),
               outline=BLACK)
    # crinkled-foil texture on descent stage
    for _ in range(120):
        px = rng.uniform(dsx0 + 2 * s, dsx0 + dsw - 2 * s)
        py = rng.uniform(dsy0 + 2 * s, dsy0 + dsh - 2 * s)
        dr.line([px, py, px + rng.uniform(-3, 3) * s, py + rng.uniform(-3, 3) * s],
                fill=rng.choice([(150, 150, 150), (110, 110, 110), (250, 250, 250)]),
                width=s)
    # landing legs
    for dx in (-1, 1):
        footx = lmx + dx * 26 * s
        dr.line([lmx + dx * 12 * s, dsy0 + dsh - 3 * s, footx, base_y + 2 * s],
                fill=(230, 230, 230), width=int(1.6 * s))
        dr.ellipse([footx - 3 * s, base_y, footx + 3 * s, base_y + 3 * s],
                   fill=(240, 240, 240), outline=BLACK)
    # ascent stage: smaller box + hatch on top
    asw, ash = 22 * s, 15 * s
    asx0, asy0 = lmx - asw / 2, dsy0 - ash
    dr.polygon([(asx0, asy0 + 4 * s), (asx0 + 5 * s, asy0),
                (asx0 + asw - 5 * s, asy0), (asx0 + asw, asy0 + 4 * s),
                (asx0 + asw, asy0 + ash), (asx0, asy0 + ash)],
               fill=(235, 235, 235), outline=BLACK)
    # black hatch window + a red docking target dot (tiny craft accent)
    dr.rectangle([lmx - 3 * s, asy0 + 4 * s, lmx + 3 * s, asy0 + 10 * s],
                 fill=BLACK)
    # antenna
    dr.line([lmx + 6 * s, asy0, lmx + 6 * s, asy0 - 9 * s], fill=(230, 230, 230),
            width=s)
    dr.ellipse([lmx + 4 * s, asy0 - 12 * s, lmx + 8 * s, asy0 - 8 * s],
               fill=(230, 230, 230))

    # --- the flag: the single true red in the scene ---
    fx = 168 * s
    dr.line([fx, base_y + 2 * s, fx, base_y - 30 * s], fill=(240, 240, 240),
            width=int(1.4 * s))
    dr.line([fx, base_y - 30 * s, fx + 20 * s, base_y - 30 * s],
            fill=(240, 240, 240), width=int(1.4 * s))  # top rail (held out)
    dr.rectangle([fx, base_y - 30 * s, fx + 20 * s, base_y - 18 * s], fill=RED)
    # a few white stripes carved into the flag so it reads as a flag
    for k in range(1, 5, 2):
        yy = base_y - 30 * s + k * 3 * s
        dr.line([fx, yy, fx + 20 * s, yy], fill=WHITE, width=s)
    dr.rectangle([fx, base_y - 30 * s, fx + 8 * s, base_y - 24 * s], fill=WHITE)

    # --- a bootprint in the foreground regolith ---
    btx, bty = 250 * s, 268 * s
    dr.ellipse([btx - 7 * s, bty - 11 * s, btx + 7 * s, bty + 11 * s],
               fill=(120, 120, 120))
    for k in range(-2, 3):
        dr.line([btx - 5 * s, bty + k * 4 * s, btx + 5 * s, bty + k * 4 * s],
                fill=(70, 70, 70), width=s)

    # --- type ---
    f_title = font(FONT_SERIF_B, 21 * s)
    f_sub = font(FONT_SANS, 10 * s)
    f_small = font(FONT_SANS, 9 * s)
    dr.text((16 * s, 16 * s), "TRANQUILITY BASE", font=f_title, fill=WHITE)
    dr.text((17 * s, 40 * s), "“The Eagle has landed.”",
            font=f_sub, fill=WHITE)
    dr.text((16 * s, (H - 20) * s),
            "APOLLO 11  ·  July 20, 1969  ·  20:17 UTC", font=f_small,
            fill=WHITE)
    dr.text((W * s - 16 * s, (H - 20) * s), "57 years", font=font(FONT_SANS_B, 9 * s),
            fill=RED, anchor="ra")
    return finalize(img)


# ==================================================== 2. Chryse Planitia
def image2_chryse():
    """Viking 1 on Mars, 50 years. The panel's red becomes a tonal field:
    red+white dithers to a pink sky, red+black to maroon ground."""
    rng = random.Random(19760720)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    horizon = 118
    hy = horizon * s

    # --- salmon-pink Martian sky: vertical gradient red->white (dithers pink) ---
    for y in range(0, horizon):
        t = y / horizon
        col = lerp((250, 150, 150), (255, 205, 205), t)  # top deeper, low hazy
        dr.rectangle([0, y * s, W * s, (y + 1) * s], fill=col)
    # faint dust banding near horizon
    for _ in range(500):
        x = rng.uniform(0, W * s)
        y = rng.uniform(hy - 30 * s, hy)
        dr.point((x, y), fill=(255, 225, 225))
    # the small pale sun of Mars, low and washed out
    sux, suy = 78 * s, 40 * s
    dr.ellipse([sux - 8 * s, suy - 8 * s, sux + 8 * s, suy + 8 * s],
               fill=(255, 235, 235))

    # --- rusty rock-strewn plain: red->black gradient (dithers maroon) ---
    for y in range(horizon, H):
        t = (y - horizon) / (H - horizon)
        col = lerp((200, 55, 40), (120, 20, 15), t)
        dr.rectangle([0, y * s, W * s, (y + 1) * s], fill=col)
    # gravel / regolith stippling
    for _ in range(4200):
        x = rng.uniform(0, W * s)
        y = rng.uniform(hy, H * s)
        depth = (y - hy) / (H * s - hy)
        cr = rng.uniform(0.6, 2.6) * s * (0.5 + depth)
        v = rng.choice([(160, 40, 30), (230, 90, 70), (90, 15, 10),
                        (255, 120, 100)])
        dr.ellipse([x - cr, y - cr * 0.6, x + cr, y + cr * 0.6], fill=v)
    # scattered rocks with dark shadows (Chryse is famously bouldered)
    for _ in range(34):
        x = rng.uniform(10 * s, (W - 10) * s)
        y = rng.uniform(hy + 14 * s, H * s - 6 * s)
        depth = (y - hy) / (H * s - hy)
        rw = rng.uniform(4, 16) * s * (0.5 + depth)
        rh = rw * rng.uniform(0.5, 0.75)
        # shadow to the right (sun at left)
        dr.ellipse([x - rw + 3 * s, y - rh * 0.3, x + rw + 4 * s, y + rh],
                   fill=(50, 8, 5))
        dr.ellipse([x - rw, y - rh, x + rw, y + rh], fill=(150, 45, 35))
        # lit crown
        dr.ellipse([x - rw * 0.7, y - rh, x + rw * 0.2, y - rh * 0.2],
                   fill=(235, 95, 75))

    # --- the Viking lander footpad + strut in the near corner (its first view
    #     from the surface famously showed one of its own footpads) ---
    px, py = 316, 250  # pad center, 1x
    px, py = px * s, py * s
    padr = 40 * s
    # strut coming down from upper right
    dr.line([(W - 8) * s, 150 * s, px + 8 * s, py - 20 * s],
            fill=(80, 80, 80), width=int(5 * s))
    dr.line([(W - 40) * s, 138 * s, px - 6 * s, py - 18 * s],
            fill=(105, 105, 105), width=int(4 * s))
    # footpad shadow
    dr.ellipse([px - padr + 5 * s, py - padr * 0.35 + 4 * s,
                px + padr + 6 * s, py + padr * 0.5 + 6 * s], fill=(45, 8, 5))
    # footpad: a shallow light-gray dish half-sunk in the soil
    dr.ellipse([px - padr, py - padr * 0.4, px + padr, py + padr * 0.5],
               fill=(215, 215, 215), outline=BLACK, width=s)
    dr.ellipse([px - padr * 0.6, py - padr * 0.22, px + padr * 0.6,
                py + padr * 0.28], fill=(160, 160, 160))
    # disturbed soil piled at the pad rim
    for _ in range(120):
        a = rng.uniform(math.pi * 0.9, math.pi * 2.1)
        rr = padr * rng.uniform(0.95, 1.15)
        sx = px + rr * math.cos(a)
        sy = py + rr * 0.5 * math.sin(a)
        dr.ellipse([sx - 2 * s, sy - 1.4 * s, sx + 2 * s, sy + 1.4 * s],
                   fill=(120, 30, 22))

    # --- type on a dark placard so it stays legible over the busy plain ---
    f_title = font(FONT_SERIF_B, 20 * s)
    f_sub = font(FONT_SANS_B, 11 * s)
    f_small = font(FONT_SANS, 9 * s)
    dr.rectangle([10 * s, 126 * s, 300 * s, 202 * s], fill=BLACK,
                 outline=WHITE, width=s)
    dr.text((18 * s, 130 * s), "CHRYSE PLANITIA", font=f_title, fill=WHITE)
    dr.text((19 * s, 156 * s), "VIKING 1 — 50 YEARS ON MARS", font=f_sub,
            fill=RED)
    dr.text((19 * s, 173 * s),
            "first U.S. craft to land on another world", font=f_small, fill=WHITE)
    dr.text((19 * s, 186 * s),
            "July 20, 1976  ·  11:53 UTC  ·  22.5° N", font=f_small,
            fill=WHITE)
    # a red banner tag
    dr.rectangle([14 * s, 14 * s, 150 * s, 34 * s], fill=RED)
    dr.text((22 * s, 17 * s), "1976 → 2026", font=font(FONT_MONO_B, 13 * s),
            fill=WHITE)
    return finalize(img)


# ==================================================== 3. Two Worlds (constructivist)
def image3_constructivist():
    """El Lissitzky homage — hard-edged, pure palette, no antialiasing.
    'Beat the whites with the red wedge', turned skyward. Long-saved idea."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # thick black frame
    dr.rectangle([0, 0, W - 1, H - 1], outline=BLACK, width=6)

    # big diagonal black bar sweeping up from lower-left
    dr.polygon([(0, 300), (0, 250), (400, 70), (400, 120)], fill=BLACK)

    # the red wedge — a triangle driving up and to the right (the rocket's thrust)
    dr.polygon([(40, 300), (150, 300), (300, 30), (250, 30)], fill=RED)

    # black circle = a world (Moon), red disk = a world (Mars)
    dr.ellipse([250, 150, 350, 250], fill=BLACK)          # Moon, black
    dr.ellipse([300, 40, 356, 96], fill=RED, outline=BLACK)  # Mars, red
    dr.ellipse([272, 172, 300, 200], fill=WHITE)          # bite of light on Moon

    # radiating construction lines from a node (Rodchenko rays)
    node = (300, 30)
    for ang in range(-8, 92, 12):
        a = math.radians(ang)
        dr.line([node, (node[0] + 260 * math.cos(a),
                        node[1] + 260 * math.sin(a))], fill=BLACK, width=1)

    # a white rocket form riding the wedge
    dr.polygon([(120, 250), (140, 250), (150, 150), (130, 120), (110, 150)],
               fill=WHITE, outline=BLACK)
    dr.polygon([(110, 150), (95, 175), (120, 168)], fill=BLACK)   # left fin
    dr.polygon([(150, 150), (165, 175), (140, 168)], fill=RED)    # right fin
    dr.ellipse([124, 168, 136, 180], fill=RED)                    # porthole
    # exhaust bars
    for i, w in enumerate([16, 11, 6]):
        cy = 258 + i * 9
        dr.rectangle([130 - w, cy, 130 + w, cy + 5], fill=BLACK)

    # constructivist type — bold, stacked in the left column
    f_huge = font(FONT_SANS_B, 36)
    f_mid = font(FONT_SANS_B, 20)
    f_small = font(FONT_SANS_B, 12)
    f_cyr = font(FONT_SANS_B, 11)

    dr.text((20, 22), "TWO", font=f_huge, fill=BLACK)
    dr.text((20, 60), "WORLDS", font=f_huge, fill=RED)
    dr.text((22, 100), "ONE DATE", font=f_mid, fill=BLACK)
    # Cyrillic homage — "to the stars"
    dr.text((24, 129), "К ЗВЁЗДАМ", font=f_cyr, fill=RED)
    # year labels in clear white zones
    dr.text((24, 150), "MOON 1969", font=f_small, fill=BLACK)
    dr.text((300, 276), "MARS 1976", font=f_small, fill=BLACK, anchor="ra")

    # constructivism renders best with NO dithering (flat pure-color planes)
    return finalize(img, dither=False)


# ==================================================== 4. The Sky Tonight
def image4_sky_tonight():
    """A useful desk card: tonight's waxing-crescent Moon (43%, first quarter
    tomorrow) plus what's up in the late-July sky."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)
    rng = random.Random(20260720)

    # header
    f_h = font(FONT_SERIF_B, 19 * s)
    f_d = font(FONT_SANS, 11 * s)
    dr.text((16 * s, 13 * s), "THE SKY TONIGHT", font=f_h, fill=BLACK)
    dr.text((16 * s, 37 * s), "Monday, July 20, 2026", font=f_d, fill=RED)
    dr.line([16 * s, 56 * s, (W - 16) * s, 56 * s], fill=BLACK, width=s)

    # --- waxing crescent Moon, 43% illuminated, right side lit ---
    mx, my, mr = 92, 150, 62
    mx, my, mr = mx * s, my * s, mr * s
    frac = 0.43
    t = mr * (1 - 2 * frac)   # signed terminator semi-axis (positive => crescent)
    # dark disk
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(35, 35, 35),
               outline=BLACK, width=s)
    # lit lune polygon: terminator ellipse (top->bottom) then right limb (bottom->up)
    N = 90
    pts = []
    for k in range(N + 1):        # terminator, top to bottom
        yy = -mr + 2 * mr * k / N
        w = math.sqrt(max(0.0, mr * mr - yy * yy))
        pts.append((mx + t * w / mr, my + yy))
    for k in range(N + 1):        # right limb, bottom to top
        yy = mr - 2 * mr * k / N
        w = math.sqrt(max(0.0, mr * mr - yy * yy))
        pts.append((mx + w, my + yy))
    dr.polygon(pts, fill=(225, 225, 225))
    # craters on the lit part
    for _ in range(40):
        a = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(0, 0.9) * mr
        cx = mx + rad * math.cos(a)
        cy = my + rad * math.sin(a)
        if cx < mx + t * math.sqrt(max(0.0, mr * mr - (cy - my) ** 2)) / mr:
            continue
        cr = rng.uniform(1.5, 6) * s
        v = rng.choice([160, 180, 195, 205])
        dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(v, v, v))
    # labels under the Moon
    f_wb = font(FONT_SANS_B, 11 * s)
    f_it = font(FONT_SANS, 9 * s)
    dr.text((mx, (my + mr / s * 0 + 74) * 1), "", font=f_it, fill=BLACK)
    dr.text((92 * s, 224 * s), "WAXING CRESCENT", font=f_wb, fill=BLACK,
            anchor="ma")
    dr.text((92 * s, 238 * s), "43% lit · 6.7 days old", font=f_it,
            fill=BLACK, anchor="ma")
    dr.text((92 * s, 252 * s), "First Quarter tomorrow", font=f_it, fill=RED,
            anchor="ma")
    dr.text((92 * s, 264 * s), "(Jul 21) — best crater relief", font=f_it,
            fill=BLACK, anchor="ma")

    # --- events column ---
    cx0 = 196
    f_wk = font(FONT_SANS_B, 11 * s)
    f_ev = font(FONT_SANS, 10 * s)
    dr.text((cx0 * s, 70 * s), "UP AFTER DARK", font=f_wk, fill=BLACK)
    rows = [
        ("VENUS", "bright, low in W at dusk"),
        ("SATURN", "rises ~1 a.m."),
        ("MARS", "pre-dawn E, rising"),
        ("PERSEIDS", "have begun"),
        ("", "building to Aug 12"),
        ("JUL 30", "δ-Aqr + Capricornids"),
    ]
    y = 92
    for tag, txt in rows:
        if tag:
            dr.text((cx0 * s, y * s), tag, font=f_wk, fill=RED)
        dr.text(((cx0 + 62) * s, y * s), txt, font=f_ev, fill=BLACK)
        y += 20
    dr.line([cx0 * s, (y + 2) * s, (W - 16) * s, (y + 2) * s], fill=BLACK, width=s)
    dr.text((cx0 * s, (y + 9) * s),
            "50 years ago today Viking 1\nreached Mars — look before dawn",
            font=font(FONT_SANS, 9 * s), fill=BLACK)
    dr.rectangle([8 * s, 6 * s, (W - 8) * s, (H - 6) * s], outline=BLACK, width=s)
    return finalize(img)


# ==================================================== 5. Hohmann transfer
def image5_hohmann():
    """The geometry that links the two worlds of today: the minimum-energy
    transfer ellipse from Earth's orbit to Mars's. Clean line-art, red Sun
    and red Mars orbit."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    cx, cy = 168 * s, 152 * s      # the Sun
    r_earth = 78 * s
    r_mars = 118 * s

    def dashed_circle(c, r, dash_deg=5, gap_deg=4, fill=BLACK, width=s):
        ang = 0.0
        while ang < 360:
            a0 = math.radians(ang)
            a1 = math.radians(min(360, ang + dash_deg))
            dr.arc([c[0] - r, c[1] - r, c[0] + r, c[1] + r],
                   math.degrees(a0), math.degrees(a1), fill=fill, width=width)
            ang += dash_deg + gap_deg

    # Earth orbit (solid black), Mars orbit (dashed red)
    dr.ellipse([cx - r_earth, cy - r_earth, cx + r_earth, cy + r_earth],
               outline=BLACK, width=s)
    dashed_circle((cx, cy), r_mars, fill=RED, width=s)

    # transfer ellipse: perihelion at Earth (left), aphelion at Mars (right).
    a = (r_earth + r_mars) / 2      # semi-major axis
    c_off = a - r_earth             # center offset from Sun toward aphelion
    b = math.sqrt(max(0.0, r_earth * r_mars))  # semi-minor (geometric mean)
    ecx = cx + c_off
    # draw the transfer ellipse dashed in black
    npts = 360
    ell = [(ecx + a * math.cos(math.radians(k)),
            cy + b * math.sin(math.radians(k))) for k in range(npts + 1)]
    for k in range(0, npts, 9):
        seg = ell[k:k + 6]
        if len(seg) > 1:
            dr.line(seg, fill=BLACK, width=int(1.4 * s))

    # the Sun
    dr.ellipse([cx - 8 * s, cy - 8 * s, cx + 8 * s, cy + 8 * s], fill=RED)
    for ang in range(0, 360, 30):
        a2 = math.radians(ang)
        dr.line([cx + 10 * s * math.cos(a2), cy + 10 * s * math.sin(a2),
                 cx + 15 * s * math.cos(a2), cy + 15 * s * math.sin(a2)],
                fill=RED, width=s)

    # departure point: Earth at perihelion (left end of transfer, on Earth orbit)
    dep = (cx - r_earth, cy)
    dr.ellipse([dep[0] - 5 * s, dep[1] - 5 * s, dep[0] + 5 * s, dep[1] + 5 * s],
               fill=BLACK)
    # arrival point: Mars at aphelion (right end, on Mars orbit)
    arr = (ecx + a, cy)
    dr.ellipse([arr[0] - 6 * s, arr[1] - 6 * s, arr[0] + 6 * s, arr[1] + 6 * s],
               fill=RED, outline=BLACK, width=s)

    # motion arrowheads on the transfer ellipse (counter-clockwise)
    def arrow(p, ang):
        a2 = math.radians(ang)
        for da in (150, 210):
            ab = math.radians(ang + da)
            dr.line([p[0], p[1], p[0] + 8 * s * math.cos(ab),
                     p[1] + 8 * s * math.sin(ab)], fill=BLACK, width=s)
    mid = (ecx + a * math.cos(math.radians(90)), cy + b * math.sin(math.radians(90)))
    arrow((mid[0], mid[1]), 180)

    # labels
    f_t = font(FONT_SERIF_B, 15 * s)
    f_l = font(FONT_SANS_B, 10 * s)
    f_s = font(FONT_SANS, 9 * s)
    dr.text((16 * s, 12 * s), "HOHMANN TRANSFER", font=f_t, fill=BLACK)
    dr.text((16 * s, 32 * s), "the cheapest road from Earth to Mars",
            font=f_s, fill=BLACK)
    dr.text((dep[0] - 6 * s, dep[1] + 8 * s), "EARTH", font=f_l, fill=BLACK,
            anchor="ra")
    dr.text((dep[0] - 6 * s, dep[1] + 20 * s), "departure", font=f_s, fill=BLACK,
            anchor="ra")
    dr.text((arr[0] + 8 * s, arr[1] - 6 * s), "MARS", font=f_l, fill=RED)
    dr.text((arr[0] + 8 * s, arr[1] + 6 * s), "arrival", font=f_s, fill=BLACK)
    dr.text((cx + 12 * s, cy + 4 * s), "SUN", font=f_s, fill=RED)
    # facts, lower-left
    dr.text((16 * s, (H - 46) * s), "half an ellipse · one burn out, one burn in",
            font=f_s, fill=BLACK)
    dr.text((16 * s, (H - 33) * s), "crossing time ≈ 259 days",
            font=font(FONT_SANS_B, 9 * s), fill=RED)
    dr.text((16 * s, (H - 20) * s),
            "Viking 1 launched Aug 1975, arrived Jul 20 1976", font=f_s, fill=BLACK)
    dr.rectangle([6 * s, 6 * s, (W - 6) * s, (H - 6) * s], outline=BLACK, width=s)
    return finalize(img)


if __name__ == "__main__":
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_tranquility, image2_chryse, image3_constructivist,
              image4_sky_tonight, image5_hohmann]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", sorted(cols))
