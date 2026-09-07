#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-15 (anniversaries: Rosetta, Apollo-Soyuz, Mariner 4).

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Tonal scenes render at 3x, LANCZOS downscale, then
Floyd-Steinberg dither into the exact palette; hard-edged pieces render at 1x in
pure palette colors.

Today's set:
  1. The Rosetta Stone      — uncovered at Rashid, 15 July 1799
  2. Apollo-Soyuz           — the handshake in orbit, 15 July 1975 (constructivist)
  3. Mariner 4              — first close-up of Mars, 15 July 1965 (paint-by-numbers)
  4. Seigaiha 青海波         — the sea-wave scallop pattern
  5. Evening sky            — the two-day crescent returns beside Venus (Jul 17)
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


# ================================================================ 1. Rosetta Stone
def image1_rosetta():
    """A dark basalt stele, three registers of script, a red royal cartouche.
    No hieroglyph font on this box, so the top register glyphs are drawn as icons."""
    rng = random.Random(17990715)
    s = SS
    img = Image.new("RGB", (W * s, H * s), (28, 28, 28))
    dr = ImageDraw.Draw(img)

    # --- stone body: an irregular slab with the real stone's broken top corners ---
    # outline points (in 1x coords), broken upper-left & upper-right, base intact
    top = 16
    body = [
        (60, top + 22), (150, top + 4), (250, top + 10), (330, top + 30),
        (352, 70), (350, 250), (356, 284),
        (44, 284), (50, 250), (48, 70),
    ]
    body_s = [(x * s, y * s) for x, y in body]
    # cast shadow
    dr.polygon([(x + 5 * s, y + 6 * s) for x, y in body_s], fill=(10, 10, 10))
    dr.polygon(body_s, fill=(40, 39, 38))

    # stone mottling: low-contrast dark flecks -> dithers to a sparse granite speckle
    # (keep the base DARK so the engraved light script reads clearly on top)
    minx = min(p[0] for p in body_s); maxx = max(p[0] for p in body_s)
    miny = min(p[1] for p in body_s); maxy = max(p[1] for p in body_s)
    from PIL import ImageDraw as _ID  # local mask
    mask = Image.new("1", img.size, 0)
    _ID.Draw(mask).polygon(body_s, fill=1)
    for _ in range(5500):
        x = rng.uniform(minx, maxx); y = rng.uniform(miny, maxy)
        if mask.getpixel((int(x), int(y))):
            v = int(rng.gauss(44, 12))
            v = max(26, min(74, v))
            r = rng.uniform(0.7, 2.4) * s
            dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))
    # a few pale chips / highlights along the top break
    for _ in range(80):
        x = rng.uniform(minx, maxx); y = rng.uniform(miny, miny + 46 * s)
        if mask.getpixel((int(x), int(y))):
            r = rng.uniform(0.8, 1.8) * s
            dr.ellipse([x - r, y - r, x + r, y + r], fill=(120, 118, 116))

    inx0, inx1 = 66, 334          # register inset (1x)
    def hline(y, col=(150, 148, 146), w=1):
        dr.line([inx0 * s, y * s, inx1 * s, y * s], fill=col, width=int(w * s))

    # --- register 1: HIEROGLYPHS (drawn as little icons) ---
    hg_light = (222, 220, 218)
    def glyph(kind, cx, cy, gs, col=hg_light):
        cx, cy, gs = cx * s, cy * s, gs * s
        w = max(1, int(0.9 * s))
        if kind == "bird":  # simple sitting bird
            dr.line([cx - gs*0.5, cy, cx + gs*0.4, cy - gs*0.1], fill=col, width=w)
            dr.line([cx + gs*0.4, cy - gs*0.1, cx + gs*0.55, cy - gs*0.4], fill=col, width=w)  # head
            dr.line([cx - gs*0.5, cy, cx - gs*0.6, cy + gs*0.5], fill=col, width=w)  # tail
            dr.line([cx - gs*0.1, cy, cx + gs*0.05, cy + gs*0.45], fill=col, width=w)  # leg
        elif kind == "owl":  # m-glyph, an owl -> two eyes + body
            dr.ellipse([cx - gs*0.4, cy - gs*0.5, cx + gs*0.4, cy + gs*0.5], outline=col, width=w)
            dr.ellipse([cx - gs*0.25, cy - gs*0.35, cx - gs*0.05, cy - gs*0.15], outline=col, width=w)
            dr.ellipse([cx + gs*0.05, cy - gs*0.35, cx + gs*0.25, cy - gs*0.15], outline=col, width=w)
        elif kind == "eye":  # eye of horus-ish
            dr.arc([cx - gs*0.5, cy - gs*0.4, cx + gs*0.5, cy + gs*0.4], 200, 340, fill=col, width=w)
            dr.arc([cx - gs*0.5, cy - gs*0.4, cx + gs*0.5, cy + gs*0.4], 20, 160, fill=col, width=w)
            dr.ellipse([cx - gs*0.12, cy - gs*0.12, cx + gs*0.12, cy + gs*0.12], fill=col)
        elif kind == "water":  # n-glyph, zigzag
            pts = []
            for k in range(5):
                pts.append((cx - gs*0.5 + gs*0.25*k, cy + (gs*0.2 if k % 2 else -gs*0.2)))
            dr.line(pts, fill=col, width=w)
        elif kind == "reed":  # i-glyph, a tall reed
            dr.line([cx, cy - gs*0.55, cx, cy + gs*0.55], fill=col, width=w)
            dr.line([cx, cy - gs*0.55, cx + gs*0.22, cy - gs*0.35], fill=col, width=w)
        elif kind == "mouth":  # r-glyph, a mouth (horizontal oval)
            dr.ellipse([cx - gs*0.5, cy - gs*0.18, cx + gs*0.5, cy + gs*0.18], outline=col, width=w)
        elif kind == "sun":  # ra, disc with center dot
            dr.ellipse([cx - gs*0.42, cy - gs*0.42, cx + gs*0.42, cy + gs*0.42], outline=col, width=w)
            dr.ellipse([cx - gs*0.08, cy - gs*0.08, cx + gs*0.08, cy + gs*0.08], fill=col)
        elif kind == "feather":  # maat feather
            dr.line([cx, cy + gs*0.55, cx - gs*0.1, cy - gs*0.55], fill=col, width=w)
            dr.arc([cx - gs*0.4, cy - gs*0.55, cx + gs*0.2, cy + gs*0.2], 250, 20, fill=col, width=w)
        elif kind == "ankh":
            dr.ellipse([cx - gs*0.2, cy - gs*0.55, cx + gs*0.2, cy - gs*0.15], outline=col, width=w)
            dr.line([cx, cy - gs*0.15, cx, cy + gs*0.55], fill=col, width=w)
            dr.line([cx - gs*0.3, cy + gs*0.05, cx + gs*0.3, cy + gs*0.05], fill=col, width=w)
        elif kind == "basket":  # nb / neb
            dr.arc([cx - gs*0.5, cy - gs*0.35, cx + gs*0.5, cy + gs*0.5], 0, 180, fill=col, width=w)
            dr.line([cx - gs*0.5, cy + gs*0.07, cx + gs*0.5, cy + gs*0.07], fill=col, width=w)
        elif kind == "hand":  # d-glyph
            dr.line([cx - gs*0.5, cy + gs*0.2, cx + gs*0.4, cy + gs*0.2], fill=col, width=w)
            for k in range(4):
                fx = cx - gs*0.35 + gs*0.22*k
                dr.line([fx, cy + gs*0.2, fx, cy - gs*0.3], fill=col, width=w)
        elif kind == "loaf":  # t-glyph, half-oval
            dr.chord([cx - gs*0.35, cy - gs*0.1, cx + gs*0.35, cy + gs*0.5], 180, 360, outline=col, width=w)

    kinds = ["bird", "owl", "eye", "water", "reed", "mouth", "sun", "feather",
             "ankh", "basket", "hand", "loaf"]
    gy0, gstep, cols = 44, 15, 14
    gx0, gxstep = 74, 18.4
    for row in range(4):
        cy = gy0 + row * gstep
        for col_i in range(cols):
            cx = gx0 + col_i * gxstep
            glyph(kinds[(row * 5 + col_i * 3 + 1) % len(kinds)], cx, cy, 10)
    # a royal CARTOUCHE in red around a name near the top-right of register 1
    cxr, cyr, cwd, chd = 232, 44, 96, 16
    dr.rounded_rectangle([cxr * s, (cyr - chd//2) * s, (cxr + cwd) * s, (cyr + chd//2) * s],
                         radius=chd * s // 2, outline=RED, width=int(1.8 * s))
    dr.line([(cxr + cwd) * s, cyr * s, (cxr + cwd + 8) * s, cyr * s], fill=RED, width=int(1.8 * s))  # tie bar
    for i, k in enumerate(["reed", "water", "reed", "sun", "feather"]):
        glyph(k, cxr + 12 + i * 17, cyr, 10, col=RED)
    hline(104)

    # --- register 2: DEMOTIC (cursive scribbly strokes) ---
    dm = (208, 206, 204)
    for line_i in range(6):
        y = 116 + line_i * 12
        x = inx0 + 4
        while x < inx1 - 6:
            seg = rng.uniform(4, 11)
            dy = rng.uniform(-3, 3)
            wobble = rng.uniform(-2, 2)
            dr.line([x * s, (y + wobble) * s, (x + seg) * s, (y + dy) * s], fill=dm, width=int(1.1 * s))
            if rng.random() < 0.3:  # little tick
                dr.line([(x + seg) * s, (y + dy) * s, (x + seg) * s, (y + dy - 3) * s], fill=dm, width=s)
            x += seg + rng.uniform(1.5, 4)
    hline(192)

    # --- register 3: GREEK capitals (DejaVu has Greek). Near the true opening. ---
    greek = [
        "ΒΑΣΙΛΕΥΟΝΤΟΣ ΤΟΥ ΝΕΟΥ ΚΑΙ ΠΑΡΑΛΑΒΟΝΤΟΣ",
        "ΤΗΝ ΒΑΣΙΛΕΙΑΝ ΠΑΡΑ ΤΟΥ ΠΑΤΡΟΣ ΚΥΡΙΟΥ",
        "ΒΑΣΙΛΕΙΩΝ ΜΕΓΑΛΟΔΟΞΟΥ ΤΟΥ ΤΗΝ ΑΙΓΥΠΤΟΝ",
        "ΚΑΤΑΣΤΗΣΑΜΕΝΟΥ ΚΑΙ ΤΑ ΠΡΟΣ ΤΟΥΣ ΘΕΟΥΣ",
        "ΕΥΣΕΒΟΥΣ ΑΝΤΙΠΑΛΩΝ ΥΠΕΡΤΕΡΟΥ ΤΟΥ ΤΟΝ",
        "ΒΙΟΝ ΤΩΝ ΑΝΘΡΩΠΩΝ ΕΠΑΝΟΡΘΩΣΑΝΤΟΣ",
    ]
    fg = font(FONT_SERIF, int(6.6 * s))
    for i, ln in enumerate(greek):
        dr.text((inx0 * s + 3 * s, (198 + i * 12) * s), ln, font=fg, fill=(214, 212, 210))

    im = finalize(img)
    # captions on top of the dithered stone, crisp: draw AFTER on the P-image? No —
    # draw them in the RGB before finalize so they dither too, but keep them punchy.
    # (Redraw title/credit here for crispness by pasting on the quantized image.)
    dr2 = ImageDraw.Draw(im)
    ftitle = font(FONT_SERIF_B, 15)
    fcred = font(FONT_SANS, 9)
    dr2.text((200, 289), "found at Rashid (Rosetta), 15 July 1799 — the key that unlocked hieroglyphs",
             font=fcred, fill=BLACK, anchor="mm")
    # title engraved at very top-center gap between broken corners
    dr2.text((201, 21), "THE ROSETTA STONE", font=ftitle, fill=RED, anchor="mm")
    dr2.text((199, 20), "THE ROSETTA STONE", font=ftitle, fill=WHITE, anchor="mm")
    return im


# ============================================================= 2. Apollo-Soyuz
def image2_apollo_soyuz():
    """Constructivist / El Lissitzky homage. The handshake in orbit, 15 July 1975.
    Hard-edged, pure palette, bold diagonal, red wedge, the two craft docking."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # black void field in the lower-left (space)
    dr.polygon([(0, 150), (232, 300), (0, 300)], fill=BLACK)
    # the great RED WEDGE driving from lower-left up toward the docking point
    dr.polygon([(2, 296), (286, 150), (120, 300)], fill=RED)
    # a black circle tucked in the top-right corner: a planet limb / the orbit
    dr.ellipse([300, -96, 476, 80], fill=BLACK)
    dr.ellipse([314, -82, 462, 66], fill=WHITE)       # ring
    dr.ellipse([328, -68, 448, 52], fill=RED)         # red disc (accent)

    # --- the docking: two stylised spacecraft meeting at center ---
    dockx, docky = 205, 150
    # Apollo (from the right): a command cone + service cylinder, black
    dr.polygon([(dockx + 78, docky - 18), (dockx + 78, docky + 18),
                (dockx + 128, docky + 30), (dockx + 128, docky - 30)], fill=BLACK)  # service module
    dr.polygon([(dockx + 50, docky), (dockx + 78, docky - 18),
                (dockx + 78, docky + 18)], fill=BLACK)  # command cone
    dr.rectangle([dockx + 100, docky - 26, dockx + 106, docky + 26], fill=WHITE)  # panel line
    # docking module (the bridge) — a short white/red barrel at center
    dr.rectangle([dockx + 24, docky - 11, dockx + 52, docky + 11], fill=WHITE, outline=BLACK, width=3)
    dr.rectangle([dockx + 35, docky - 11, dockx + 41, docky + 11], fill=RED)
    # Soyuz (from the left): a barrel + two flat solar wings, black
    dr.ellipse([dockx - 16, docky - 15, dockx + 26, docky + 15], fill=BLACK)  # orbital+descent
    dr.rectangle([dockx - 34, docky - 11, dockx - 6, docky + 11], fill=BLACK)
    dr.polygon([(dockx - 34, docky - 6), (dockx - 80, docky - 27),
                (dockx - 80, docky - 15), (dockx - 34, docky + 2)], fill=BLACK)  # wing up
    dr.polygon([(dockx - 34, docky + 6), (dockx - 80, docky + 27),
                (dockx - 80, docky + 15), (dockx - 34, docky - 2)], fill=BLACK)  # wing down
    # the spark of contact
    for r in (11, 6, 3):
        dr.ellipse([dockx + 38 - r, docky - r, dockx + 38 + r, docky + r],
                   fill=(RED if r == 6 else WHITE))

    # --- typography: bold, rotated on the wedge's diagonal, both fully in frame ---
    def rotated_word(text, fnt, fill, cx, cy, angle):
        pad = 8
        tmp = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
        bb = ImageDraw.Draw(tmp).textbbox((0, 0), text, font=fnt)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        layer = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((pad - bb[0], pad - bb[1]), text, font=fnt, fill=fill + (255,))
        layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
        img.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)

    big = font(FONT_SANS_B, 40)
    rotated_word("APOLLO", big, RED, 158, 80, 15)      # upper-left, red on white
    rotated_word("СОЮЗ", big, BLACK, 298, 232, 15)     # lower-right, black on white

    # a hard black bar with reversed date, top-left
    dr.rectangle([0, 0, 150, 26], fill=BLACK)
    dr.text((8, 5), "15 · VII · 1975", font=font(FONT_SANS_B, 15), fill=WHITE)
    dr.text((10, 278), "a handshake in orbit", font=font(FONT_SANS_B, 14), fill=WHITE)
    dr.text((392, 290), "ЭПАС · ASTP", font=font(FONT_SANS_B, 11), fill=BLACK, anchor="ra")

    return finalize(img, dither=False)


# ================================================================ 3. Mariner 4
def image3_mariner():
    """The true JPL story: while the computer lagged, staff hand-colored the teletype
    NUMBERS like a paint-by-numbers to make the first close-up of Mars, 15 July 1965.
    A grid of monospace digits colored across the curved limb of the planet."""
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)
    rng = random.Random(19650715)

    # header band
    dr.rectangle([0, 0, W, 34], fill=BLACK)
    dr.text((10, 6), "FIRST TV IMAGE OF MARS", font=font(FONT_SANS_B, 15), fill=WHITE)
    dr.text((W - 10, 9), "MARINER 4 · 15 JULY 1965", font=font(FONT_MONO, 11),
            fill=RED, anchor="ra")

    # grid area
    gx0, gy0 = 8, 40
    gw, gh = W - 16, 232
    ncol, nrow = 42, 24
    cw = gw / ncol
    ch = gh / nrow
    fdig = font(FONT_MONO_B, int(min(cw, ch) * 0.92))

    # Mars limb: planet fills lower-right, space upper-left. Boundary is a big circle.
    # circle center far to the lower-right, so the visible edge curves across the frame.
    ccx, ccy, crad = ncol * 0.98, nrow * 1.55, nrow * 1.72
    for r in range(nrow):
        for c in range(ncol):
            # distance from planet center in cell units (aspect-corrected)
            dx = (c - ccx)
            dy = (r - ccy) * (ch / cw)
            dist = math.hypot(dx, dy * (cw / ch))
            edge = dist - crad
            # brightness model: space dark; a bright rim at the limb; disc mid, mottled
            if edge > 0.4:
                band = "space"
            elif edge > -2.2:
                band = "limb"       # bright sunlit edge
            else:
                band = "disc"
            # colour + digit value
            if band == "space":
                val = rng.randint(0, 2)
                fill = BLACK
                dcol = (58, 58, 58)         # dark digit on dark -> near invisible, like the panel
                if rng.random() < 0.05:
                    dcol = (120, 120, 120)
            elif band == "limb":
                val = rng.randint(6, 9)
                fill = RED                  # the hand-colored bright rim
                dcol = BLACK
            else:
                # disc: mottled light with occasional red mare
                mott = rng.random()
                if mott < 0.18:
                    fill = RED
                    dcol = WHITE
                    val = rng.randint(4, 6)
                else:
                    fill = WHITE
                    dcol = BLACK
                    val = rng.randint(2, 5)
            x0 = gx0 + c * cw
            y0 = gy0 + r * ch
            dr.rectangle([x0, y0, x0 + cw + 0.6, y0 + ch + 0.6], fill=fill)
            dr.text((x0 + cw / 2, y0 + ch / 2 - 1), str(val), font=fdig,
                    fill=dcol, anchor="mm")

    # thin frame around the grid, like the mounted strips
    dr.rectangle([gx0 - 1, gy0 - 1, gx0 + gw + 1, gy0 + gh + 1], outline=BLACK, width=1)
    # vertical hairlines suggesting the taped teletype strips
    for c in range(0, ncol + 1, 6):
        x = gx0 + c * cw
        dr.line([x, gy0, x, gy0 + gh], fill=(0, 0, 0), width=1)

    # caption
    dr.text((8, 278), "JPL colored the data by hand while the computer caught up — "
            "Richard Grumm's pastels from the corner art store",
            font=font(FONT_SANS, 9), fill=BLACK)
    return finalize(img, dither=False)


# ================================================================= 4. Seigaiha
def image4_seigaiha():
    """青海波 — the 'blue sea wave'. Staggered rows of concentric-arc scallops.
    Here rendered black/white with red accent fans. Supersampled for smooth arcs."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    R = 34            # scallop radius (1x)
    rings = 5         # concentric arcs per scallop
    dx = R            # horizontal spacing = R (they overlap by half)
    dy = int(R * 0.5)
    ring_cols = [BLACK, WHITE, RED, WHITE, BLACK]  # from outer to inner band edges

    def scallop(cx, cy, accent=False):
        cx, cy = cx * s, cy * s
        for k in range(rings):
            rr = (R - k * (R / rings)) * s
            # band between ring k and k+1 filled; approximate with thick arcs
            col = ring_cols[k % len(ring_cols)]
            if accent and col == BLACK:
                col = RED
            width = int((R / rings) * s) + s
            dr.arc([cx - rr, cy - rr, cx + rr, cy + rr], 180, 360, fill=col, width=width)
        # crisp thin outline of the outermost arc
        rr = R * s
        dr.arc([cx - rr, cy - rr, cx + rr, cy + rr], 180, 360, fill=BLACK, width=s)

    rng = random.Random(20260715)
    rows = int(H / dy) + 2
    cols = int(W / dx) + 2
    for row in range(rows):
        cy = row * dy - 6
        offset = 0 if row % 2 == 0 else dx / 2
        for col in range(-1, cols):
            cx = col * dx + offset
            # sprinkle a few red-accent fans in a gentle diagonal
            accent = ((row * 3 + col) % 11 == 0)
            scallop(cx, cy, accent=accent)

    im = finalize(img, dither=True)
    # title plate, crisp
    dr2 = ImageDraw.Draw(im)
    plate_w = 196
    dr2.rectangle([W // 2 - plate_w // 2, 128, W // 2 + plate_w // 2, 172], fill=WHITE,
                  outline=BLACK, width=2)
    dr2.text((W // 2, 140), "青海波", font=font(FONT_JP, 22), fill=RED, anchor="mm")
    dr2.text((W // 2, 162), "SEIGAIHA — the calm sea wave", font=font(FONT_SANS, 9),
             fill=BLACK, anchor="mm")
    return im


# =============================================================== 5. Evening sky
def image5_evening():
    """After sunset, look WEST: the two-day waxing crescent moon returns beside Venus.
    New moon was Jul 14; on Jul 17 the slim crescent and Venus pair up low in the dusk."""
    rng = random.Random(20260717)
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)

    # dusk gradient: deep dark at top, a low glow toward the horizon. Keep it DARK
    # so the Floyd-Steinberg dither stays sparse and reads as night, not static.
    horizon = 228
    for y in range(H):
        t = y / horizon if y < horizon else 1.0
        v = int(1 + 52 * (t ** 2.6))       # near-black up high, gentle glow low
        v = min(v, 54)
        dr.rectangle([0, y * s, W * s, (y + 1) * s], fill=(v, v, v))
    # warm afterglow band right at the horizon = RED accent
    for y in range(horizon - 18, horizon):
        t = (y - (horizon - 18)) / 18
        if rng.random() < t * 0.9:
            for _ in range(int(60 * t)):
                x = rng.uniform(0, W * s)
                dr.rectangle([x, y * s, x + 2 * s, (y + 1) * s], fill=RED)

    # a sparse scatter of stars in the darker upper sky
    for _ in range(55):
        x = rng.uniform(0, W * s); y = rng.uniform(0, (horizon - 70) * s)
        v = rng.randint(170, 255)
        r = rng.uniform(0.5, 1.3) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # --- the crescent moon (waxing, ~2 days, lit on the lower-right toward the sun) ---
    mx, my, mr = 118, 150, 40
    mxs, mys, mrs = mx * s, my * s, mr * s
    # earthshine: faint full disc
    dr.ellipse([mxs - mrs, mys - mrs, mxs + mrs, mys + mrs], fill=(52, 52, 52))
    # bright lit crescent = full white disc minus an offset dark disc
    lit = Image.new("L", img.size, 0)
    ld = ImageDraw.Draw(lit)
    ld.ellipse([mxs - mrs, mys - mrs, mxs + mrs, mys + mrs], fill=255)
    off = int(mr * 0.62)
    ld.ellipse([mxs - mrs - off * s, mys - mrs - int(off*0.15)*s,
                mxs + mrs - off * s, mys + mrs - int(off*0.15)*s], fill=0)
    white_disc = Image.new("RGB", img.size, (245, 245, 245))
    img.paste(white_disc, (0, 0), lit)
    dr = ImageDraw.Draw(img)

    # --- Venus: brilliant, below-left of the moon ---
    vx, vy = 236, 196
    vxs, vys = vx * s, vy * s
    dr.line([vxs - 13 * s, vys, vxs + 13 * s, vys], fill=WHITE, width=s)
    dr.line([vxs, vys - 13 * s, vxs, vys + 13 * s], fill=WHITE, width=s)
    for rr, v in [(4.5, 90), (2.8, 200), (1.6, 255)]:
        dr.ellipse([vxs - rr*s, vys - rr*s, vxs + rr*s, vys + rr*s], fill=(v, v, v))

    # --- foreground: a low black rooftop / hill silhouette ---
    sky_line = []
    x = 0
    base = horizon
    while x <= W:
        sky_line.append((x, base + rng.randint(-3, 2)))
        x += rng.randint(14, 40)
    # a couple of little buildings
    roof = [(0, horizon)]
    roof += sky_line
    roof += [(W, horizon), (W, H), (0, H)]
    dr.polygon([(px * s, py * s) for px, py in roof], fill=BLACK)
    # a thin tree / antenna or two
    for tx in (300, 60):
        dr.line([tx * s, horizon * s, tx * s, (horizon - rng.randint(14, 22)) * s],
                fill=BLACK, width=int(1.4 * s))

    im = finalize(img)
    # crisp labels
    dr2 = ImageDraw.Draw(im)
    dr2.text((mx + 4, my - 58), "the 2-day moon", font=font(FONT_SANS, 10), fill=WHITE, anchor="mm")
    dr2.text((vx, vy + 16), "VENUS", font=font(FONT_SANS_B, 10), fill=WHITE, anchor="mm")
    dr2.text((12, 10), "AFTER SUNSET · LOOK WEST", font=font(FONT_SANS_B, 12), fill=RED)
    dr2.text((12, 26), "the crescent returns beside Venus — Jul 17", font=font(FONT_SANS, 10), fill=WHITE)
    dr2.text((W - 10, H - 16), "new moon was Jul 14", font=font(FONT_SANS, 9), fill=WHITE, anchor="ra")
    return im


if __name__ == "__main__":
    import os
    outdir = os.environ.get("OUTDIR", ".")
    makers = [image1_rosetta, image2_apollo_soyuz, image3_mariner,
              image4_seigaiha, image5_evening]
    for n, fn in enumerate(makers, 1):
        im = fn()
        path = os.path.join(outdir, f"{n}.png")
        im.save(path, optimize=True)
        rgb = im.convert("RGB")
        cols = {c for _, c in rgb.getcolors(16)}
        assert cols <= {WHITE, BLACK, RED}, (path, cols)
        print(path, "colors:", cols)
