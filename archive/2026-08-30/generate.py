#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-08-30.

Five 400x300 images in exactly three colors (white, black, red) for a
black/white/red e-ink panel. Tonal scenes render at 3x, LANCZOS downscale,
then Floyd-Steinberg dither into the exact palette; hard-edged pieces render
at 3x and quantize without dithering for crisp edges.

Today: Mary Shelley's birthday (30 Aug 1797), Charlie "Bird" Parker,
a constructivist manifesto for a three-color screen, seigaiha waves with an
inverted red sun, and the week's sky almanac (waning gibbous, two nights
after the Aug 28 partial lunar eclipse).
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


def ctext(dr, cx, y, text, fnt, fill, anchor="ma"):
    dr.text((cx, y), text, font=fnt, fill=fill, anchor=anchor)


# ------------------------------------------------------------- 1. Frankenstein
def image1_frankenstein():
    """Mary Shelley born 30 August 1797. A storm, a tower, one lit window."""
    rng = random.Random(1797)
    s = SS
    img = Image.new("RGB", (W * s, H * s), (12, 12, 12))
    dr = ImageDraw.Draw(img)

    # Storm sky: layered ragged cloud blobs, brighter near the strike point.
    strike_x, strike_top = 258 * s, 8 * s
    for i in range(650):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, 175 * s) * rng.uniform(0.4, 1.0)
        d2 = math.hypot(x - strike_x, y - 60 * s) / (W * s)
        base = 105 - 130 * d2 + rng.uniform(-28, 28)
        g = max(8, min(150, base))
        rx = rng.uniform(9, 34) * s
        ry = rx * rng.uniform(0.28, 0.5)
        dr.ellipse((x - rx, y - ry, x + rx, y + ry), fill=(int(g),) * 3)

    # Hill silhouette
    hill = [(0, H * s)]
    for px in range(0, W + 1, 8):
        hy = 232 - 34 * math.exp(-((px - 258) / 120.0) ** 2) + 6 * math.sin(px * 0.05)
        hill.append((px * s, hy * s))
    hill.append((W * s, H * s))
    dr.polygon(hill, fill=(0, 0, 0))

    # The watchtower on the hill
    tx, base_y, tw, th = 258, 206, 30, 74
    dr.rectangle((s * (tx - tw // 2), s * (base_y - th), s * (tx + tw // 2), s * base_y),
                 fill=(0, 0, 0))
    # battlements
    for i in range(4):
        bx = tx - tw // 2 + 2 + i * 8
        dr.rectangle((s * bx, s * (base_y - th - 7), s * (bx + 5), s * (base_y - th)),
                     fill=(0, 0, 0))
    # one window, lit red — the experiment is running
    dr.rectangle((s * (tx - 5), s * (base_y - 52), s * (tx + 5), s * (base_y - 36)),
                 fill=RED)
    dr.line((s * tx, s * (base_y - 52), s * tx, s * (base_y - 36)), fill=(0, 0, 0), width=s)
    dr.line((s * (tx - 5), s * (base_y - 44), s * (tx + 5), s * (base_y - 44)),
            fill=(0, 0, 0), width=s)

    # Lightning: jagged main bolt from sky to the tower, with branches.
    def bolt(x0, y0, x1, y1, width, jag, depth=0):
        pts = [(x0, y0)]
        n = 9
        for i in range(1, n):
            t = i / n
            bx = x0 + (x1 - x0) * t + rng.uniform(-jag, jag) * s
            by = y0 + (y1 - y0) * t + rng.uniform(-jag * 0.3, jag * 0.3) * s
            pts.append((bx, by))
        pts.append((x1, y1))
        for a, b in zip(pts, pts[1:]):
            dr.line([a, b], fill=(255, 255, 255), width=width)
        if depth < 2:
            for a in rng.sample(pts[1:-1], 2):
                ex = a[0] + rng.uniform(-70, 70) * s
                ey = a[1] + rng.uniform(30, 70) * s
                bolt(a[0], a[1], ex, ey, max(1, width - 2 * s), jag * 0.6, depth + 1)

    bolt(strike_x * 0.98, strike_top, s * (tx - 2), s * (base_y - th - 8), 3 * s, 16)

    # Title block
    ctext(dr, W * s // 2, 236 * s, "FRANKENSTEIN", font(FONT_SERIF_B, 34 * s), WHITE)
    dr.line((70 * s, 231 * s, 152 * s, 231 * s), fill=RED, width=s)
    dr.line((248 * s, 231 * s, 330 * s, 231 * s), fill=RED, width=s)
    ctext(dr, W * s // 2, 271 * s, "or, The Modern Prometheus",
          font(FONT_SERIF, 13 * s), (210, 210, 210))
    ctext(dr, W * s // 2, 287 * s, "MARY SHELLEY  ·  BORN 30 AUGUST 1797",
          font(FONT_MONO, 9 * s), RED)
    return finalize(img, dither=True)


# -------------------------------------------------------------- 2. Ornithology
def image2_ornithology():
    """Birds on five wires: a phrase of bebop scored in silhouettes.
    For Charlie "Bird" Parker (1920-1955)."""
    rng = random.Random(1955)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    ctext(dr, W * s // 2, 20 * s, "O R N I T H O L O G Y",
          font(FONT_SANS_B, 25 * s), BLACK)

    top, gap, x0, x1 = 78, 30, 34, 366
    # utility poles
    for px in (x0 - 10, x1 + 10):
        dr.rectangle((s * (px - 3), s * (top - 22), s * (px + 3), s * (top + 4 * gap + 24)),
                     fill=BLACK)
        dr.rectangle((s * (px - 12), s * (top - 22), s * (px + 12), s * (top - 17)),
                     fill=BLACK)

    def wire_y(i, x):  # slight catenary sag
        t = (x - x0) / (x1 - x0)
        return top + i * gap + 7 * math.sin(math.pi * t)

    for i in range(5):
        pts = [(s * x, s * wire_y(i, x)) for x in range(x0 - 10, x1 + 11, 4)]
        dr.line(pts, fill=BLACK, width=s)

    def bird(cx, cy, sc, color, flip=False):
        """Perched songbird silhouette; (cx, cy) is where feet meet the wire."""
        f = -1 if flip else 1
        b = ImageDraw.Draw(img)
        bx, by = cx * s, cy * s
        # legs
        b.line((bx - 2 * s, by, bx - 3 * s, by - 5 * sc * s), fill=color, width=s)
        b.line((bx + 2 * s, by, bx + 2 * s, by - 5 * sc * s), fill=color, width=s)
        # body
        b.ellipse((bx - 9 * sc * s, by - 16 * sc * s, bx + 9 * sc * s, by - 3 * sc * s),
                  fill=color)
        # head
        hx = bx + f * 7 * sc * s
        b.ellipse((hx - 6 * sc * s, by - 25 * sc * s, hx + 6 * sc * s, by - 13 * sc * s),
                  fill=color)
        # beak
        tipx = hx + f * 11 * sc * s
        b.polygon([(hx + f * 4 * sc * s, by - 21 * sc * s),
                   (hx + f * 4 * sc * s, by - 17 * sc * s),
                   (tipx, by - 19 * sc * s)], fill=color)
        # tail
        b.polygon([(bx - f * 6 * sc * s, by - 12 * sc * s),
                   (bx - f * 18 * sc * s, by - 4 * sc * s),
                   (bx - f * 15 * sc * s, by - 13 * sc * s)], fill=color)
        # eye
        er = max(s, int(1.2 * sc * s))
        ex, ey = hx + f * 2 * sc * s, by - 20 * sc * s
        b.ellipse((ex - er, ey - er, ex + er, ey + er),
                  fill=WHITE if color != WHITE else BLACK)

    # A phrase: birds as notes. One red bird — Bird himself, off the beaten scale.
    melody = [(70, 3), (100, 2), (124, 1), (150, 2), (186, 0), (214, 1),
              (244, 2), (272, 1), (300, 3), (330, 2), (352, 4)]
    red_idx = 4  # the high note
    for k, (mx, wi) in enumerate(melody):
        sc = rng.uniform(0.75, 0.95)
        color = RED if k == red_idx else BLACK
        bird(mx, wire_y(wi, mx), sc, color, flip=rng.random() < 0.35)

    # a few distant flyers
    for _ in range(4):
        fx, fy = rng.uniform(60, 340) * s, rng.uniform(38, 60) * s
        wsp = rng.uniform(4, 7) * s
        dr.arc((fx - wsp, fy - wsp * 0.8, fx, fy + wsp * 0.8), 180, 320, fill=BLACK, width=s)
        dr.arc((fx, fy - wsp * 0.8, fx + wsp, fy + wsp * 0.8), 220, 360, fill=BLACK, width=s)

    dr.line((34 * s, 252 * s, 366 * s, 252 * s), fill=RED, width=s)
    ctext(dr, W * s // 2, 260 * s, "for Charlie “Bird” Parker  ·  1920–1955",
          font(FONT_SERIF, 12 * s), BLACK)
    ctext(dr, W * s // 2, 278 * s, "♪  eleven notes on five wires  ♪",
          font(FONT_SANS, 9 * s), BLACK)
    return finalize(img, dither=False)


# ------------------------------------------------- 3. Constructivist manifesto
def image3_red_wedge():
    """After El Lissitzky — a manifesto for a screen with no grey."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # Diagonal field: lower-left triangle is black
    dr.polygon([(0, 92 * s), (W * s, H * s), (0, H * s)], fill=BLACK)

    # Black circle, upper right
    ccx, ccy, cr = 272 * s, 118 * s, 78 * s
    dr.ellipse((ccx - cr, ccy - cr, ccx + cr, ccy + cr), fill=BLACK)
    # white inner ring
    dr.ellipse((ccx - cr + 6 * s, ccy - cr + 6 * s, ccx + cr - 6 * s, ccy + cr - 6 * s),
               outline=WHITE, width=2 * s)

    # The red wedge, piercing the circle from the lower left
    tip = (ccx + 8 * s, ccy - 2 * s)
    dr.polygon([(6 * s, 226 * s), (30 * s, 280 * s), tip], fill=RED)
    # white halo where the wedge enters the circle
    dr.polygon([(tip[0] + 2 * s, tip[1] - 3 * s), (tip[0] + 26 * s, tip[1] - 26 * s),
                (tip[0] + 30 * s, tip[1] + 8 * s)], fill=WHITE)

    # Satellites: small hard shapes in tension
    dr.rectangle((330 * s, 220 * s, 356 * s, 246 * s), fill=RED)
    dr.rectangle((360 * s, 236 * s, 376 * s, 252 * s), fill=WHITE)
    dr.ellipse((30 * s, 30 * s, 48 * s, 48 * s), fill=RED)
    dr.rectangle((58 * s, 36 * s, 130 * s, 42 * s), fill=BLACK)
    for i in range(5):
        yy = (58 + i * 7) * s
        dr.line((58 * s, yy, (108 - i * 9) * s, yy), fill=BLACK, width=s)
    # thin diagonal rails
    dr.line((0, 92 * s, W * s, H * s), fill=BLACK, width=2 * s)
    dr.line((120 * s, 300 * s, 400 * s, 118 * s), fill=WHITE, width=s)

    # Rotated type on the diagonal
    def diag_text(text, fnt, fill, pos, angle, stroke=0, stroke_fill=None):
        tw, th_ = dr.textbbox((0, 0), text, font=fnt)[2:]
        tmp = Image.new("RGBA", (tw + 12 * s, th_ + 12 * s), (0, 0, 0, 0))
        ImageDraw.Draw(tmp).text((6 * s, 6 * s), text, font=fnt, fill=fill,
                                 stroke_width=stroke, stroke_fill=stroke_fill)
        tmp = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
        img.paste(tmp, pos, tmp)

    diag_text("BEAT THE GREY", font(FONT_SANS_B, 21 * s), WHITE, (52 * s, 168 * s), 27.5,
              stroke=2 * s, stroke_fill=BLACK)
    diag_text("WITH THE RED WEDGE", font(FONT_SANS_B, 13 * s), RED, (120 * s, 176 * s), 27.5)

    ctext(dr, 12 * s, 282 * s, "THREE COLOURS ARE ENOUGH · 1919/2026",
          font(FONT_MONO, 8 * s), WHITE, anchor="la")
    return finalize(img, dither=False)


# ----------------------------------------------------------------- 4. Seigaiha
def image4_seigaiha():
    """Blue-sea waves in black on white; a red sun where the pattern inverts."""
    rng = random.Random(20260830)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    R = 34  # fan radius (1x px)
    row_h = R // 2
    sun_c, sun_r = (284, 96), 74

    def in_sun(x, y):
        return math.hypot(x - sun_c[0], y - sun_c[1]) < sun_r

    rows = int(H / row_h) + 3
    for row in range(-1, rows):
        cy = row * row_h
        xoff = 0 if row % 2 == 0 else R
        for col in range(-1, W // (2 * R) + 2):
            cx = col * 2 * R + xoff
            inside = in_sun(cx, cy)
            bg = RED if inside else WHITE
            fg = WHITE if inside else BLACK
            # occasionally a solid accent fan, kept clear of the sun's rim
            near_sun = math.hypot(cx - sun_c[0], cy - sun_c[1]) < sun_r + 55
            if not inside and not near_sun and rng.random() < 0.045:
                bg, fg = BLACK, WHITE
            dr.ellipse((s * (cx - R), s * (cy - R), s * (cx + R), s * (cy + R)), fill=bg)
            for k in range(4):
                rr = R - 4 - k * 7
                if rr <= 2:
                    break
                dr.ellipse((s * (cx - rr), s * (cy - rr), s * (cx + rr), s * (cy + rr)),
                           outline=fg, width=2 * s)

    # signature block, bottom left
    card_w, card_h = 30, 96
    dr.rectangle((10 * s, (H - card_h - 10) * s, (10 + card_w) * s, (H - 10) * s),
                 fill=WHITE, outline=BLACK, width=s)
    jp = font(FONT_JP, 22 * s)
    for i, ch in enumerate("青海波"):
        ctext(dr, (10 + card_w // 2) * s, (H - card_h - 4 + i * 28) * s, ch, jp, BLACK)
    return finalize(img, dither=False)


# -------------------------------------------------------------- 5. Sky almanac
def image5_almanac():
    """The week ahead: waning gibbous after the Aug 28 partial eclipse."""
    rng = random.Random(20260830)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # header
    dr.rectangle((0, 0, W * s, 34 * s), fill=BLACK)
    ctext(dr, 12 * s, 8 * s, "SKY ALMANAC", font(FONT_SANS_B, 15 * s), WHITE, anchor="la")
    ctext(dr, 388 * s, 8 * s, "SUN 30 AUG 2026", font(FONT_MONO_B, 12 * s), RED, anchor="ra")

    # left: night panel with the moon
    px0, py0, px1, py1 = 12, 46, 172, 252
    dr.rectangle((px0 * s, py0 * s, px1 * s, py1 * s), fill=BLACK)
    for _ in range(60):
        sx = rng.uniform(px0 + 4, px1 - 4) * s
        sy = rng.uniform(py0 + 4, py1 - 4) * s
        r = rng.choice([1, 1, 1, 2]) * s // 2 + s // 3
        dr.ellipse((sx - r, sy - r, sx + r, sy + r), fill=WHITE)

    mcx, mcy, mr = (px0 + px1) // 2 * s, 148 * s, 56 * s
    # moon face: pale disc with crater shading (greys -> dither texture)
    dr.ellipse((mcx - mr, mcy - mr, mcx + mr, mcy + mr), fill=(228, 228, 228))
    for _ in range(26):
        a = rng.uniform(0, 2 * math.pi)
        d = mr * math.sqrt(rng.uniform(0, 0.92))
        cx2, cy2 = mcx + d * math.cos(a), mcy + d * math.sin(a)
        cr2 = rng.uniform(2, 11) * s
        if math.hypot(cx2 - mcx, cy2 - mcy) + cr2 > mr - s:
            continue
        g = rng.choice([168, 185, 200])
        dr.ellipse((cx2 - cr2, cy2 - cr2, cx2 + cr2, cy2 + cr2), fill=(g, g, g))
    # maria blotches
    for (ox, oy, orx, ory) in [(-0.3, -0.35, 0.38, 0.28), (0.15, -0.1, 0.3, 0.34),
                               (-0.15, 0.3, 0.26, 0.2)]:
        dr.ellipse((mcx + (ox - orx) * mr, mcy + (oy - ory) * mr,
                    mcx + (ox + orx) * mr, mcy + (oy + ory) * mr), fill=(178, 178, 178))
    # waning gibbous 94%: dark sliver on the right (mask = right half-disc minus
    # right half of the terminator ellipse)
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.pieslice((mcx - mr, mcy - mr, mcx + mr, mcy + mr), -90, 90, fill=255)
    ea = mr * (2 * 0.94 - 1)
    md.ellipse((mcx - ea, mcy - mr, mcx + ea, mcy + mr), fill=0)
    img.paste(Image.new("RGB", img.size, (5, 5, 5)), (0, 0), mask)

    ctext(dr, (px0 + px1) // 2 * s, 216 * s, "WANING GIBBOUS",
          font(FONT_MONO_B, 10 * s), WHITE)
    ctext(dr, (px0 + px1) // 2 * s, 230 * s, "94% · rises late evening",
          font(FONT_MONO, 8 * s), WHITE)

    # right: event list
    events = [
        ("AUG 28", "partial lunar eclipse", "(two nights ago — 93% in umbra)", False),
        ("SEP  1", "Venus meets Spica", "dusk, WSW — a fine close pair", True),
        ("DAWN  ", "Jupiter & Mars", "low in the east before sunrise", False),
        ("SEP 14", "Moon occults Venus", "in broad daylight!", True),
        ("SEP 23", "autumn equinox", "aurora season opens", False),
        ("SEP 26", "Harvest Moon", "Neptune at opposition Sep 25", False),
    ]
    ey = 50
    for date, title, sub, hot in events:
        dx = 184
        col = RED if hot else BLACK
        dr.ellipse(((dx) * s, (ey + 4) * s, (dx + 6) * s, (ey + 10) * s), fill=col)
        ctext(dr, (dx + 12) * s, ey * s, date, font(FONT_MONO_B, 10 * s), col, anchor="la")
        ctext(dr, (dx + 62) * s, ey * s, title, font(FONT_SANS_B, 12 * s), BLACK, anchor="la")
        ctext(dr, (dx + 62) * s, (ey + 15) * s, sub, font(FONT_SANS, 9 * s), BLACK, anchor="la")
        ey += 34

    dr.line((12 * s, 262 * s, 388 * s, 262 * s), fill=BLACK, width=s)
    ctext(dr, 12 * s, 270 * s, "tonight the gibbous moon slides past Saturn in Pisces",
          font(FONT_SERIF, 11 * s), BLACK, anchor="la")
    dr.ellipse((382 * s, 273 * s, 388 * s, 279 * s), fill=RED)
    return finalize(img, dither=True)


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    makers = [image1_frankenstein, image2_ornithology, image3_red_wedge,
              image4_seigaiha, image5_almanac]
    for i, fn in enumerate(makers, 1):
        im = fn()
        im.save(os.path.join(here, f"{i}.png"))
        print(f"saved {i}.png ({fn.__name__})")
