#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-17.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel.

Today's hooks:
  - Tonight the waxing crescent Moon (~13% lit, ~3 days old) sits low in the
    west with brilliant Venus and Regulus, the heart of Leo. A slow triangle.
  - 51 years ago today — 17 Jul 1975 — Apollo and Soyuz docked in orbit and
    Stafford and Leonov shook hands through the hatch: the first international
    handshake in space. The black/white/red palette is pure constructivism.
  - Word of the day: SYZYGY — a straight-line alignment of three bodies. It is
    exactly what the western sky is doing tonight.

Technique: tonal scenes render at 3x then LANCZOS + Floyd-Steinberg dither into
the exact palette; hard-edged geometric pieces render at 1x in pure colors.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
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
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------- 1. Evening triangle
def image1_evening_sky():
    """Tonight's real western sky: crescent Moon, Venus, Regulus low over a
    dithered dusk gradient. A skywatching card."""
    s = SS
    rng = random.Random(20260717)
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # Dusk gradient: darker at top, glow toward the horizon where the sun set.
    for y in range(H * s):
        t = y / (H * s)
        # brighten low, and add a warm-white pool at the bottom-right (sunset)
        base = int(6 + 70 * (t ** 2.4))
        dr.line([(0, y), (W * s, y)], fill=(base, base, base))
    # horizon sunset pool (west)
    for i in range(4000):
        ang = rng.uniform(0, math.pi)
        r = abs(rng.gauss(0, 60 * s))
        x = 250 * s + r * math.cos(ang) * 1.5
        y = H * s + 6 * s - r * math.sin(ang) * 0.7
        if 0 <= x < W * s and 0 <= y < H * s:
            v = max(0, 150 - r / s * 1.4)
            rr = rng.uniform(0.5, 2.0) * s
            dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(int(v), int(v), int(v)))

    # a low ground silhouette (rooftops) so it reads as "over the horizon"
    ground_y = H - 34
    dr.rectangle([0, ground_y * s, W * s, H * s], fill=BLACK)
    gx = 0
    while gx < W:
        bw = rng.randint(16, 40)
        bh = rng.randint(4, 22)
        dr.rectangle([gx * s, (ground_y - bh) * s, (gx + bw) * s, ground_y * s], fill=BLACK)
        # a lit window here and there
        if rng.random() < 0.5 and bh > 8:
            wx = gx + bw // 2
            dr.rectangle([wx * s, (ground_y - bh + 3) * s, (wx + 3) * s, (ground_y - bh + 7) * s],
                         fill=(120, 120, 120))
        gx += bw

    # faint background stars (above horizon only)
    for _ in range(120):
        x, y = rng.uniform(0, W * s), rng.uniform(0, (ground_y - 6) * s)
        v = rng.randint(60, 150)
        rr = rng.uniform(0.4, 1.1) * s
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(v, v, v))

    def glow_star(x, y, r, spikes=1.0, red=False):
        x, y = x * s, y * s
        col = RED if red else WHITE
        for rr, v in [(3.2 * r, 30), (2.0 * r, 80), (1.3 * r, 180), (0.8 * r, 255)]:
            fill = col if (red and rr <= 1.3 * r) else (v, v, v)
            dr.ellipse([x - rr * s, y - rr * s, x + rr * s, y + rr * s], fill=fill)
        if spikes:
            L = 5.0 * r * spikes
            dr.line([x - L * s, y, x + L * s, y], fill=col if red else WHITE, width=s)
            dr.line([x, y - L * s, x, y + L * s], fill=col if red else WHITE, width=s)

    # Positions (schematic but true to tonight: Moon low, Venus upper-left of Moon,
    # Regulus close above the Moon). West sky, all fairly low.
    moon_x, moon_y = 205, 176
    venus_x, venus_y = 150, 120
    regu_x, regu_y = 232, 128

    # thin triangle connecting the three (the "slow triangle")
    dr.line([(venus_x * s, venus_y * s), (moon_x * s, moon_y * s)], fill=(70, 70, 70), width=s)
    dr.line([(moon_x * s, moon_y * s), (regu_x * s, regu_y * s)], fill=(70, 70, 70), width=s)
    dr.line([(regu_x * s, regu_y * s), (venus_x * s, venus_y * s)], fill=(70, 70, 70), width=s)

    # Venus — brilliant, white
    glow_star(venus_x, venus_y, 3.4, spikes=1.3)
    # Regulus — a touch of red for the star's heart of the Lion
    glow_star(regu_x, regu_y, 2.0, spikes=1.0, red=True)

    # Crescent Moon (~13% lit, lit side toward the west/lower-right where sun set)
    mr = 20
    cx, cy = moon_x * s, moon_y * s
    # bright disc
    dr.ellipse([cx - mr * s, cy - mr * s, cx + mr * s, cy + mr * s], fill=(245, 245, 245))
    # subtract the shadow: offset dark disc to carve a thin crescent on lower-right
    off = 0.72 * mr
    ang = math.radians(-58)  # lit limb toward lower-right (sunset)
    dx, dy = math.cos(ang) * off, math.sin(ang) * off
    dr.ellipse([cx - dx - mr * s, cy - dy - mr * s, cx - dx + mr * s, cy - dy + mr * s],
               fill=(14, 14, 14))
    # earthshine: faint fill of the dark part
    dr.ellipse([cx - (mr - 1) * s, cy - (mr - 1) * s, cx + (mr - 1) * s, cy + (mr - 1) * s],
               outline=(60, 60, 60), width=s)

    # labels
    f_lbl = font(FONT_SANS_B, 12 * s)
    f_sub = font(FONT_SANS, 9 * s)
    dr.text((venus_x * s - 10 * s, venus_y * s - 4 * s), "VENUS", font=f_lbl, fill=WHITE, anchor="rm")
    dr.text((regu_x * s + 12 * s, regu_y * s - 2 * s), "REGULUS", font=f_lbl, fill=WHITE, anchor="lm")
    dr.text((regu_x * s + 12 * s, regu_y * s + 9 * s), "heart of Leo", font=f_sub, fill=(180, 180, 180), anchor="lm")
    dr.text((moon_x * s + 24 * s, moon_y * s + 8 * s), "MOON", font=f_lbl, fill=WHITE, anchor="lm")
    dr.text((moon_x * s + 24 * s, moon_y * s + 19 * s), "13% · 3 days old", font=f_sub, fill=(180, 180, 180), anchor="lm")

    # title block
    f_ti = font(FONT_SANS_B, 15 * s)
    f_cap = font(FONT_SANS, 10 * s)
    dr.text((14 * s, 16 * s), "THE WESTERN SKY TONIGHT", font=f_ti, fill=WHITE)
    dr.text((14 * s, 34 * s), "17 July 2026 · look low in the west after sunset", font=f_cap, fill=(190, 190, 190))
    dr.text((W * s - 12 * s, (H - 12) * s), "a slow triangle, gone within two hours",
            font=f_cap, fill=(170, 170, 170), anchor="rs")
    return finalize(img)


# ------------------------------------------------------- 2. Handshake in Space
def image2_handshake():
    """Apollo-Soyuz, 51 years. A Lissitzky-flavoured constructivist poster.
    Hard-edged, pure palette, no antialiasing."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # Big red diagonal band = the shared orbit, sweeping up to the right.
    dr.polygon([(0, 250), (0, 300), (400, 150), (400, 100)], fill=RED)
    # a black counter-wedge driving in from the left (the constructivist tension)
    dr.polygon([(0, 0), (250, 0), (0, 210)], fill=BLACK)

    # The two craft meeting on the band. Represent them as bold blocky forms.
    # Soyuz (left, black) and Apollo (right, black) with a red docking collar
    # between them — the "handshake".
    def module(x, y, w, h, col):
        dr.rectangle([x, y, x + w, y + h], fill=col)

    # docking axis roughly along the red band near center
    ax, ay = 200, 168
    # Apollo command+service (right): cylinder + cone, drawn as blocks
    module(ax + 22, ay - 16, 70, 32, BLACK)          # service module body
    dr.polygon([(ax + 92, ay - 16), (ax + 122, ay), (ax + 92, ay + 16)], fill=BLACK)  # nose cone
    # Soyuz (left): body + two solar panels
    module(ax - 96, ay - 13, 66, 26, BLACK)          # orbital+service body
    dr.rectangle([ax - 150, ay - 4, ax - 96, ay + 4], fill=BLACK)   # left panel arm
    dr.rectangle([ax - 172, ay - 22, ax - 150, ay + 22], fill=BLACK)  # left panel
    dr.rectangle([ax + 92, ay - 4, ax + 118, ay + 4], fill=BLACK)   # (right panel arm handled by cone side)
    # the androgynous docking collar — RED, where they clasp
    dr.rectangle([ax - 30, ay - 10, ax + 22, ay + 10], fill=RED)
    dr.rectangle([ax - 6, ay - 14, ax + 2, ay + 14], fill=WHITE)   # the seam / clasp line
    # small white portholes
    for px in (ax - 78, ax + 46):
        dr.ellipse([px - 4, ay - 4, px + 4, ay + 4], fill=WHITE)

    # Flags as pure color blocks flanking the collar (no stars/hammer, just fields)
    dr.rectangle([ax - 92, ay + 30, ax - 60, ay + 46], fill=RED)     # USSR field
    dr.rectangle([ax + 58, ay + 30, ax + 92, ay + 46], outline=BLACK, width=2, fill=WHITE)  # US field
    dr.rectangle([ax + 58, ay + 30, ax + 76, ay + 38], fill=RED)     # US canton hint

    # Typography — constructivist stacked headline.
    f_big = font(FONT_SANS_B, 40)
    f_mid = font(FONT_SANS_B, 22)
    f_cyr = font(FONT_SANS_B, 22)
    f_sm = font(FONT_SANS, 12)
    f_yr = font(FONT_SANS_B, 15)

    dr.text((14, 8), "APOLLO", font=f_big, fill=BLACK)
    dr.text((386, 8), "СОЮЗ", font=f_cyr, fill=RED, anchor="ra")
    dr.text((386, 34), "SOYUZ", font=f_sm, fill=BLACK, anchor="ra")

    # Bottom-left caption on white
    dr.rectangle([0, 256, 400, 300], fill=WHITE)
    dr.line([(0, 256), (400, 256)], fill=BLACK, width=2)
    dr.text((14, 260), "HANDSHAKE IN SPACE", font=f_mid, fill=BLACK)
    dr.text((14, 290), "first international docking · 17 July 1975",
            font=f_sm, fill=BLACK, anchor="lm")
    dr.text((386, 262), "1975", font=f_yr, fill=RED, anchor="ra")
    dr.text((386, 290), "+51 years", font=f_sm, fill=BLACK, anchor="rm")
    return finalize(img, dither=False)


# ---------------------------------------------------------------------- 3. Kamon
def image3_kamon():
    """A generated kamon (Japanese family crest): a bold, radially symmetric
    monogram. Pure palette, rendered at 3x for clean curved edges then
    downscaled WITHOUT dither so it stays crisp."""
    s = SS
    rng = random.Random(717_2026)
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    cx, cy = W * s // 2, (H // 2 - 8) * s
    R = 108 * s

    # outer ring (maru)
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)
    dr.ellipse([cx - (R - 9 * s), cy - (R - 9 * s), cx + (R - 9 * s), cy + (R - 9 * s)], fill=WHITE)

    petals = rng.choice([5, 6, 8])
    inner = R - 20 * s
    accent = rng.random() < 0.6

    def petal(angle, r0, r1, wfrac, col):
        # a leaf/petal shape as a filled polygon, symmetric about `angle`
        pts = []
        steps = 24
        for k in range(steps + 1):
            t = k / steps
            rr = r0 + (r1 - r0) * math.sin(t * math.pi)
            spread = wfrac * math.sin(t * math.pi) ** 0.7
            a = angle - spread + 2 * spread * t
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        for k in range(steps + 1):
            t = 1 - k / steps
            rr = r0 + (r1 - r0) * math.sin(t * math.pi) * 0.62
            a = angle
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        dr.polygon(pts, fill=col)

    # main petals radiating out
    for i in range(petals):
        a = -math.pi / 2 + i * 2 * math.pi / petals
        petal(a, 14 * s, inner, 0.62 * math.pi / petals * 1.9, BLACK)

    # inner white cut to give each petal a hollow (mon detail)
    for i in range(petals):
        a = -math.pi / 2 + i * 2 * math.pi / petals
        petal(a, 26 * s, inner - 16 * s, 0.42 * math.pi / petals * 1.9, WHITE)
        if accent:
            petal(a, 40 * s, inner - 30 * s, 0.24 * math.pi / petals * 1.9, RED)

    # central boss
    dr.ellipse([cx - 20 * s, cy - 20 * s, cx + 20 * s, cy + 20 * s], fill=BLACK)
    dr.ellipse([cx - 11 * s, cy - 11 * s, cx + 11 * s, cy + 11 * s],
               fill=RED if accent else WHITE)
    if accent:
        dr.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], fill=BLACK)

    # caption
    f_jp = font(FONT_JP, 22 * s)
    f_en = font(FONT_SANS, 11 * s)
    names = ["Kikyō — the bellflower", "Ha-guruma — the toothed wheel",
             "Hana-mon — the flower crest", "Kuruma — the wheel of return"]
    name = rng.choice(names)
    dr.text((cx, (H - 34) * s), "家 紋", font=f_jp, fill=BLACK, anchor="mm")
    dr.text((cx, (H - 12) * s), name, font=f_en, fill=BLACK, anchor="mm")
    return finalize(img, dither=False)


# -------------------------------------------------------------------- 4. Seigaiha
def image4_seigaiha():
    """Seigaiha (青海波) — 'blue sea and waves' — the endless overlapping-arc
    pattern, here in black on white with red-crested rows. Hard-edged."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    R = 30 * s          # scale radius
    rings = 5           # concentric arcs per scale
    dx = R              # horizontal spacing between scale centers
    dy = int(R * 0.62)  # vertical spacing between rows

    def scale(cx, cy, crest_red):
        for k in range(rings):
            rr = R * (rings - k) / rings
            col = RED if (crest_red and k == 0) else (BLACK if k % 2 == 0 else WHITE)
            dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
        # tiny white core
        dr.ellipse([cx - R * 0.14, cy - R * 0.14, cx + R * 0.14, cy + R * 0.14], fill=WHITE)

    # We only need the top half of each circle to read as a wave scale, but
    # drawing full circles and letting lower rows overpaint gives the classic
    # fish-scale interlock. Draw top-to-bottom so lower rows sit in front.
    row = 0
    y = 0
    while y < H * s + R:
        offset = (dx // 2) if (row % 2) else 0
        crest_red = (row % 4 == 1)
        x = -R + offset
        while x < W * s + R:
            scale(x, y, crest_red)
            x += dx
        y += dy
        row += 1

    # Because full circles overpaint, redraw a clean white mask below each row's
    # baseline is unnecessary — the interlock is intentional. Add a caption bar.
    dr.rectangle([0, (H - 26) * s, W * s, H * s], fill=WHITE)
    dr.line([(0, (H - 26) * s), (W * s, (H - 26) * s)], fill=BLACK, width=s)
    f_jp = font(FONT_JP, 15 * s)
    f_en = font(FONT_SANS, 10 * s)
    dr.text((12 * s, (H - 13) * s), "青海波", font=f_jp, fill=RED, anchor="lm")
    dr.text((W * s - 12 * s, (H - 13) * s),
            "seigaiha — calm seas without end", font=f_en, fill=BLACK, anchor="rm")
    return finalize(img, dither=False)


# ---------------------------------------------------------------------- 5. Syzygy
def image5_syzygy():
    """Word of the day. SYZYGY — a straight-line alignment of three celestial
    bodies. Exactly what the western sky is doing tonight."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # top hairline rule + kicker
    dr.line([(24, 40), (376, 40)], fill=BLACK, width=2)
    f_kick = font(FONT_MONO, 11)
    dr.text((24, 24), "WORD OF THE DAY", font=f_kick, fill=BLACK)
    dr.text((376, 24), "n.  ·  astronomy", font=f_kick, fill=RED, anchor="ra")

    # the word, huge
    f_word = font(FONT_SERIF_B, 74)
    dr.text((200, 92), "syzygy", font=f_word, fill=BLACK, anchor="mm")

    # phonetics
    f_ph = font(FONT_SERIF, 15)
    dr.text((200, 138), "/ˈsɪz.ɪ.dʒi/", font=f_ph, fill=RED, anchor="mm")

    # three aligned bodies — the diagram, dead center on a red axis
    axis_y = 178
    dr.line([(60, axis_y), (340, axis_y)], fill=RED, width=2)
    for (x, r, col) in [(90, 6, BLACK), (200, 13, BLACK), (310, 9, RED)]:
        dr.ellipse([x - r, axis_y - r, x + r, axis_y + r], fill=col)
    # crescent notch on the middle body to hint 'moon'
    dr.ellipse([200 - 13 + 6, axis_y - 13, 200 + 13 + 6, axis_y + 13], fill=WHITE)

    # definition block
    f_def = font(FONT_SERIF, 14)
    lines = [
        "A straight-line configuration of three",
        "celestial bodies — as the Sun, a planet,",
        "and the Moon fall into one line.",
    ]
    yy = 206
    for ln in lines:
        dr.text((200, yy), ln, font=f_def, fill=BLACK, anchor="mm")
        yy += 19

    # etymology footer
    dr.line([(24, 266), (376, 266)], fill=BLACK, width=1)
    f_et = font(FONT_SERIF, 11)
    dr.text((200, 280), "from Greek σύζυγος súzugos — ‘yoked together’",
            font=f_et, fill=BLACK, anchor="mm")
    dr.text((200, 294), "look west tonight", font=f_et, fill=RED, anchor="mm")
    return finalize(img, dither=False)


BUILDERS = [
    image1_evening_sky,
    image2_handshake,
    image3_kamon,
    image4_seigaiha,
    image5_syzygy,
]


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(os.path.dirname(here))
    images_dir = os.path.join(repo, "images")
    for i, build in enumerate(BUILDERS, 1):
        im = build()
        im.save(os.path.join(here, f"{i}.png"))
        im.save(os.path.join(images_dir, f"{i}.png"))
        print(f"built {i}: {build.__name__}")


if __name__ == "__main__":
    main()
