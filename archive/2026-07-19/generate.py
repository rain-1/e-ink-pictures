#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-19.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Tonal scenes render at 3x then Floyd-Steinberg
dither into the exact palette; hard-edged pieces render in pure palette colors.

Today's set — moon-landing week, a founding day, and two things I'd been saving:
  1. Apollo 11 — Lunar Orbit Insertion, July 19 1969 (the day before the landing).
  2. Tonight's western sky — waxing crescent Moon by Venus and Regulus (real, 07-19).
  3. Red Wedge — constructivist homage to El Lissitzky, 1919 (the b/w/r palette IS this).
  4. Multiscale Truchet — recursively subdivided Smith arc-tiles, red loops emerging.
  5. Declaration of Sentiments — Seneca Falls Convention opened July 19, 1848.
"""

import math
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
FONT_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
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


# --------------------------------------------------------- 1. Apollo 11 orbit
def image1_apollo():
    """The command module Columbia in lunar orbit, Earthrise over the limb.
    Lunar Orbit Insertion was July 19, 1969 — the day before the landing."""
    rng = random.Random(19690719)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # starfield
    for _ in range(260):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s)
        v = rng.randint(90, 235)
        r = rng.uniform(0.4, 1.3) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # The Moon: a huge disc whose upper edge cuts across as a curved horizon.
    # Centre far below the frame so only the top limb shows in the lower third.
    mcx, mcy, mr = 200 * s, 640 * s, 430 * s
    dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=(150, 150, 150))
    # cratered / maria texture on the visible cap
    for _ in range(1400):
        ang = rng.uniform(-math.pi, 0)          # upper hemisphere only
        rad = rng.uniform(0.90, 1.0) * mr
        cx = mcx + rad * math.cos(ang)
        cy = mcy + rad * math.sin(ang)
        if cy > (H + 4) * s:
            continue
        cr = rng.uniform(1.5, 10) * s
        v = rng.choice([110, 128, 140, 168, 185, 200])
        dr.ellipse([cx - cr, cy - cr * 0.85, cx + cr, cy + cr * 0.85],
                   fill=(v, v, v))
    # a few sharp crater rings
    for _ in range(26):
        ang = rng.uniform(-math.pi, 0)
        rad = rng.uniform(0.905, 0.995) * mr
        cx = mcx + rad * math.cos(ang)
        cy = mcy + rad * math.sin(ang)
        if cy > (H - 2) * s:
            continue
        cr = rng.uniform(3, 11) * s
        dr.ellipse([cx - cr, cy - cr * 0.8, cx + cr, cy + cr * 0.8],
                   outline=(90, 90, 90), width=max(1, s // 2))
    # crisp bright limb line
    dr.arc([mcx - mr, mcy - mr, mcx + mr, mcy + mr], 185, 355,
           fill=(240, 240, 240), width=2 * s)

    # Earthrise: gibbous Earth low over the limb, right of centre.
    ex, ey, er = 300 * s, 96 * s, 40 * s
    dr.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(245, 245, 245))
    # dithered continents/cloud mottle
    for _ in range(520):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, 1) ** 0.5 * er
        cx = ex + rr * math.cos(a)
        cy = ey + rr * math.sin(a)
        cr = rng.uniform(1.2, 4.5) * s
        v = rng.choice([120, 150, 175, 205])
        dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(v, v, v))
    # night side: a shadow crescent on the left limb (Earth waxing gibbous)
    for _ in range(1600):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, 1) ** 0.5 * er
        cx = ex + rr * math.cos(a)
        cy = ey + rr * math.sin(a)
        # terminator: darken the far-left sliver
        edge = (cx - (ex - er)) / (2 * er)   # 0 at left limb .. 1 at right
        if edge < 0.22 + 0.10 * math.sin(a):
            cr = rng.uniform(1.0, 2.6) * s
            dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(20, 20, 20))
    dr.ellipse([ex - er, ey - er, ex + er, ey + er], outline=(255, 255, 255),
               width=s)

    # Dashed RED orbit arc sweeping across the frame, with Columbia riding it.
    ocx, ocy, orr = 200 * s, 470 * s, 300 * s
    def orbit_pt(deg):
        a = math.radians(deg)
        return ocx + orr * math.cos(a), ocy + orr * math.sin(a)
    deg0, deg1 = 188, 352
    ndash = 46
    for k in range(ndash):
        t0 = deg0 + (deg1 - deg0) * (k + 0.15) / ndash
        t1 = deg0 + (deg1 - deg0) * (k + 0.72) / ndash
        p0, p1 = orbit_pt(t0), orbit_pt(t1)
        dr.line([p0, p1], fill=RED, width=2 * s)

    # Columbia (CSM): conical command module + cylindrical service module + bell.
    scx, scy = orbit_pt(292)
    def draw_csm(cx, cy, k, ang):
        ca, sa = math.cos(ang), math.sin(ang)
        def T(px, py):
            return (cx + (px * ca - py * sa) * k, cy + (px * sa + py * ca) * k)
        # service module body
        dr.polygon([T(-11, -5), T(4, -5), T(4, 5), T(-11, 5)], fill=BLACK)
        # command module cone (red — the crew capsule)
        dr.polygon([T(4, -5), T(13, 0), T(4, 5)], fill=RED)
        # engine bell
        dr.polygon([T(-11, -4), T(-17, -6), T(-17, 6), T(-11, 4)], fill=BLACK)
        # high-gain antenna dish
        dr.line([T(-2, -5), T(-4, -12)], fill=(230, 230, 230), width=s)
        dr.ellipse([T(-4, -12)[0] - 3 * k, T(-4, -12)[1] - 3 * k,
                    T(-4, -12)[0] + 3 * k, T(-4, -12)[1] + 3 * k],
                   outline=(230, 230, 230), width=s)
        dr.line([T(4, -5), T(4, 5)], fill=(200, 200, 200), width=max(1, s // 2))
    draw_csm(scx, scy, 1.5 * s, math.radians(20))

    # titles
    f_ti = font(FONT_SANS_B, 15 * s)
    f_sub = font(FONT_SANS, 10 * s)
    dr.text((16 * s, 16 * s), "APOLLO 11", font=f_ti, fill=WHITE)
    dr.text((16 * s, 35 * s), "Lunar Orbit Insertion", font=f_sub, fill=RED)
    dr.text((16 * s, 49 * s), "July 19, 1969 — one day before the Eagle",
            font=f_sub, fill=(210, 210, 210))
    dr.text((W * s - 14 * s, H * s - 20 * s),
            "“the Eagle has wings” — tomorrow", font=f_sub,
            fill=(220, 220, 220), anchor="rs")
    return finalize(img)


# ------------------------------------------------------- 2. Tonight's sky
def image2_tonight():
    """Waxing crescent Moon near Venus and Regulus, low in the west after
    sunset on July 19, 2026. First-quarter Moon follows on July 21."""
    rng = random.Random(20260719)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # twilight glow: brighter (lighter, then dithers to speckle) near horizon
    horizon = 246
    for y in range(0, horizon * s):
        t = y / (horizon * s)              # 0 top .. 1 horizon
        v = int(4 + 150 * (t ** 2.4))      # dark sky to bright dusk band
        dr.line([(0, y), (W * s, y)], fill=(v, int(v * 0.9), int(v * 0.9)))

    # stars (fade out toward the bright horizon)
    for _ in range(220):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, horizon * s * 0.86)
        if rng.random() > (0.25 + 0.75 * (1 - y / (horizon * s))):
            continue
        v = rng.randint(120, 245)
        r = rng.uniform(0.4, 1.1) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    def bright_star(x, y, r, spikes=2.8):
        x, y, r = x * s, y * s, r * s
        dr.line([x - spikes * r, y, x + spikes * r, y], fill=WHITE, width=s)
        dr.line([x, y - spikes * r, x, y + spikes * r], fill=WHITE, width=s)
        for rr, v in [(2.0, 70), (1.4, 170), (1.0, 255)]:
            dr.ellipse([x - r * rr, y - r * rr, x + r * rr, y + r * rr],
                       fill=(v, v, v))

    # Venus — the brilliant one, lower right
    vx, vy = 300, 150
    bright_star(vx, vy, 4.2)
    # Regulus — fainter, to the lower right of Venus
    rx, ry = 336, 196
    bright_star(rx, ry, 2.4)

    # Waxing crescent Moon, upper-left, lit on the lower-right toward the set Sun.
    mx, my, mr = 118, 96, 40
    mx, my, mr = mx * s, my * s, mr * s
    # earthshine: faint gray full disc
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(46, 46, 46))
    # bright crescent = full disc minus an offset dark disc
    lit = Image.new("L", (W * s, H * s), 0)
    ld = ImageDraw.Draw(lit)
    ld.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=255)
    off = int(mr * 0.62)
    ld.ellipse([mx - mr - off, my - mr - int(mr * 0.18),
                mx + mr - off, my + mr - int(mr * 0.18)], fill=0)
    crescent = Image.new("RGB", (W * s, H * s), (244, 244, 244))
    img.paste(crescent, (0, 0), lit)
    dr = ImageDraw.Draw(img)
    dr.arc([mx - mr, my - mr, mx + mr, my + mr], 0, 360, fill=(210, 210, 210),
           width=max(1, s // 2))

    # ground silhouette: gentle hills + a couple of rooftops
    gy = horizon
    hill = [(0, gy + 8)]
    for px in range(0, W + 1, 8):
        hh = 8 + 6 * math.sin(px / 46.0) + 4 * math.sin(px / 17.0)
        hill.append((px, gy + 8 - hh))
    hill += [(W, gy + 8), (W, H), (0, H)]
    dr.polygon([(x * s, y * s) for x, y in hill], fill=BLACK)
    # a tiny skyline of houses
    base = (gy + 6)
    for hx, hw, hh in [(60, 26, 20), (92, 20, 30), (250, 30, 18), (300, 22, 26)]:
        dr.rectangle([hx * s, (base - hh) * s, (hx + hw) * s, base * s],
                     fill=BLACK)
        dr.polygon([((hx - 3) * s, (base - hh) * s),
                    ((hx + hw / 2) * s, (base - hh - 9) * s),
                    ((hx + hw + 3) * s, (base - hh) * s)], fill=BLACK)

    # labels
    f_lbl = font(FONT_SANS_B, 11 * s)
    f_sub = font(FONT_SANS, 9 * s)
    dr.text((vx * s + 12 * s, vy * s - 4 * s), "VENUS", font=f_lbl, fill=WHITE)
    dr.text((rx * s + 10 * s, ry * s - 3 * s), "Regulus", font=f_sub, fill=WHITE)
    dr.text((mx - mr - 4 * s, my - mr - 2 * s), "Moon", font=f_sub, fill=WHITE,
            anchor="rs")

    # title block + compass tag
    f_ti = font(FONT_SANS_B, 14 * s)
    dr.text((16 * s, H * s - 44 * s), "TONIGHT · JULY 19", font=f_ti,
            fill=WHITE)
    dr.text((16 * s, H * s - 26 * s),
            "look west after sunset: the young Moon rides", font=f_sub,
            fill=(225, 225, 225))
    dr.text((16 * s, H * s - 15 * s),
            "past Venus & Regulus — first quarter Jul 21", font=f_sub,
            fill=(225, 225, 225))
    # W compass mark
    dr.text((W * s - 16 * s, H * s - 20 * s), "W", font=font(FONT_SERIF_B, 16 * s),
            fill=RED, anchor="rs")
    return finalize(img)


# ------------------------------------------------------------- 3. Red Wedge
def image3_red_wedge():
    """Constructivist homage to El Lissitzky's 'Beat the Whites with the Red
    Wedge' (1919). Pure palette colours, hard edges — the b/w/r screen is
    exactly this poster's palette. Original composition, not a copy."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # black field occupying the right portion, angled edge
    dr.polygon([(300, 0), (400, 0), (400, 300), (150, 300)], fill=BLACK)

    # the white circle (the encircled "whites"), sitting on the black field
    ccx, ccy, cr = 292, 150, 86
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=WHITE)
    dr.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=BLACK, width=3)

    # the driving red wedge — a long triangle piercing from the left into the circle
    dr.polygon([(8, 40), (8, 260), (300, 150)], fill=RED)
    # a crisp black spine along the wedge's centreline for tension
    dr.line([(8, 150), (296, 150)], fill=BLACK, width=2)

    # suprematist "skirmishes": scattered bars and shapes on diagonals
    dr.polygon([(150, 12), (250, 12), (232, 30), (132, 30)], fill=BLACK)  # black bar
    dr.line([(24, 24), (150, 20)], fill=BLACK, width=3)
    dr.rectangle([22, 268, 120, 276], fill=BLACK)                        # base bar
    dr.polygon([(330, 250), (392, 236), (392, 268), (338, 280)], fill=RED)
    dr.ellipse([40, 210, 64, 234], fill=BLACK)                           # small dot
    dr.ellipse([352, 60, 366, 74], fill=RED)                             # red pip
    # thin flying lines
    for (x0, y0, x1, y1) in [(70, 250, 210, 96), (110, 40, 250, 120)]:
        dr.line([(x0, y0), (x1, y1)], fill=BLACK, width=1)
    # a small white square knocked out of the black field (suprematist void)
    dr.rectangle([344, 176, 372, 204], fill=WHITE)
    dr.rectangle([344, 176, 372, 204], outline=BLACK, width=2)

    # typography set on the composition
    f_t = font(FONT_SANS_B, 15)
    f_s = font(FONT_SANS, 9)
    dr.text((14, 14), "RED", font=font(FONT_SANS_B, 22), fill=RED)
    dr.text((14, 40), "WEDGE", font=font(FONT_SANS_B, 22), fill=BLACK)
    dr.text((10, 284), "after El Lissitzky, 1919  —  beat the whites with the red wedge",
            font=f_s, fill=BLACK)
    return finalize(img, dither=False)


# ------------------------------------------------------- 4. Multiscale Truchet
def image4_truchet():
    """Smith's arc tiles (two quarter-circles joining midpoints of adjacent
    sides) on a recursively subdivided grid — Carlson-style multiscale Truchet.
    Arcs connect across scales into emergent loops; some run red."""
    rng = random.Random(0x19072026)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    ox, oy = 18, 16
    top = 40                      # leave a title strip
    grid = 360                    # square-ish play area
    base = 4                      # base grid = 4x4 big cells
    cell0 = grid / base

    def draw_tile(x, y, size, orient, color, wln):
        """Smith tile: two quarter-circle arcs of radius size/2 centred on two
        opposite corners, joining the midpoints of the sides."""
        r = size / 2.0
        # corners
        tl = (x, y); tr = (x + size, y)
        bl = (x, y + size); br = (x + size, y + size)
        w = int(wln * s)
        bb = lambda c: [c[0] - r, c[1] - r, c[0] + r, c[1] + r]
        if orient == 0:
            # arcs centred at top-left and bottom-right corners
            dr.arc([ (tl[0]-r)*s,(tl[1]-r)*s,(tl[0]+r)*s,(tl[1]+r)*s ], 0, 90, fill=color, width=w)
            dr.arc([ (br[0]-r)*s,(br[1]-r)*s,(br[0]+r)*s,(br[1]+r)*s ], 180, 270, fill=color, width=w)
        else:
            # arcs centred at top-right and bottom-left corners
            dr.arc([ (tr[0]-r)*s,(tr[1]-r)*s,(tr[0]+r)*s,(tr[1]+r)*s ], 90, 180, fill=color, width=w)
            dr.arc([ (bl[0]-r)*s,(bl[1]-r)*s,(bl[0]+r)*s,(bl[1]+r)*s ], 270, 360, fill=color, width=w)

    def recurse(x, y, size, depth):
        # decide whether to subdivide this cell into 2x2
        p_split = 0.55 if depth < 1 else (0.42 if depth < 2 else 0.0)
        if depth < 3 and rng.random() < p_split:
            h = size / 2.0
            for dx in (0, 1):
                for dy in (0, 1):
                    recurse(x + dx * h, y + dy * h, h, depth + 1)
        else:
            orient = rng.randint(0, 1)
            red = rng.random() < 0.16
            color = RED if red else BLACK
            wln = max(2.2, size * 0.11)
            draw_tile(x, y, size, orient, color, wln)

    for i in range(base):
        for j in range(base):
            recurse(ox + i * cell0, top + oy + j * cell0, cell0, 0)

    # frame + title
    dr.rectangle([ (ox-4)*s,(top+oy-4)*s,(ox+grid+4)*s,(top+oy+grid+4)*s ],
                 outline=BLACK, width=s)
    f_t = font(FONT_SANS_B, 14 * s)
    f_s = font(FONT_SANS, 9 * s)
    dr.text((ox * s, 12 * s), "MULTISCALE TRUCHET", font=f_t, fill=BLACK)
    dr.text(((ox + grid) * s, 18 * s),
            "Smith arc-tiles, recursively subdivided", font=f_s, fill=RED,
            anchor="ra")
    return finalize(img, dither=False)


# ------------------------------------------------- 5. Declaration of Sentiments
def image5_seneca():
    """Typographic anniversary. The Seneca Falls Convention opened July 19,
    1848; its Declaration of Sentiments amended Jefferson's words to read
    'all men and women are created equal.'"""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # top red rule + kicker
    dr.rectangle([0, 0, W, 6], fill=RED)
    f_kick = font(FONT_SANS_B, 11)
    dr.text((20, 18), "JULY 19, 1848", font=f_kick, fill=RED)
    dr.text((W - 20, 18), "SENECA FALLS, NEW YORK", font=f_kick, fill=BLACK,
            anchor="ra")
    dr.line([20, 34, W - 20, 34], fill=BLACK, width=1)

    # headline
    f_h1 = font(FONT_SERIF_B, 27)
    f_h2 = font(FONT_SERIF_I, 15)
    dr.text((20, 44), "Declaration", font=f_h1, fill=BLACK)
    dr.text((20, 76), "of Sentiments", font=f_h1, fill=BLACK)
    dr.text((W - 20, 60), "the convention that", font=f_h2, fill=BLACK, anchor="ra")
    dr.text((W - 20, 78), "launched a movement", font=f_h2, fill=BLACK, anchor="ra")

    # the quotation, with 'and women' struck in red
    f_q = font(FONT_SERIF, 14)
    f_qb = font(FONT_SERIF_B, 14)
    lines = [
        [("We hold these truths to be", BLACK, f_q)],
        [("self-evident: that all men ", BLACK, f_q), ("and women", RED, f_qb)],
        [("are created equal.", BLACK, f_q)],
    ]
    y = 128
    for parts in lines:
        x = 24
        for txt, col, ft in parts:
            dr.text((x, y), txt, font=ft, fill=col)
            x += int(dr.textlength(txt, font=ft))
        y += 22

    # a quiet decorative red mark (the amendment caret)
    dr.line([200, 218, 214, 206], fill=RED, width=2)
    dr.line([214, 206, 228, 218], fill=RED, width=2)

    # signatories footer
    dr.line([20, 236, W - 20, 236], fill=BLACK, width=1)
    f_ft = font(FONT_SANS, 9)
    f_ftb = font(FONT_SANS_B, 9)
    dr.text((20, 244),
            "Drafted by Elizabeth Cady Stanton. Signed by 68 women",
            font=f_ft, fill=BLACK)
    dr.text((20, 256),
            "and 32 men, among them Frederick Douglass.",
            font=f_ft, fill=BLACK)
    dr.text((20, 274), "THE FIRST WOMEN’S RIGHTS CONVENTION IN THE U.S.",
            font=f_ftb, fill=RED)
    return finalize(img, dither=False)


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_apollo, image2_tonight, image3_red_wedge,
              image4_truchet, image5_seneca]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        # verify palette discipline
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", sorted(cols))
