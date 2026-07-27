#!/usr/bin/env python3
"""
e-ink pictures — 2026-07-27
Five 400x300 images in pure black / white / red for a 3-color e-ink panel.

Today: the Buck Moon is nearly full (full Jul 29). On this day: the de Havilland
Comet's maiden flight (1949, first jet airliner), and Vincent van Gogh's fatal
wound in a wheatfield at Auvers (1890).

1. buck moon almanac card
2. constructivist poster for the Comet (square windows -> oval windows)
3. "Wheatfield with Crows" homage — generative pen-stroke landscape
4. kamon (Japanese family crest) generator, date-seeded
5. Truchet tiles with red threads
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3                      # supersample factor for painterly pieces
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

DEJA = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def palette_img():
    p = Image.new("P", (1, 1))
    p.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0] * 759)
    return p


def finish(img, path, dither=True):
    """Downscale if supersampled, then quantize to the exact 3-color palette."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.FLOYDSTEINBERG if dither else Image.NONE
    out = img.convert("RGB").quantize(palette=palette_img(), dither=d)
    out.save(path, optimize=True)
    print("wrote", path)


# ----------------------------------------------------------------------
# 1. Buck Moon almanac
# ----------------------------------------------------------------------
def buck_moon():
    rng = random.Random(20260727)
    img = Image.new("RGB", (W * S, H * S), BLACK)
    d = ImageDraw.Draw(img)

    # scatter of stars, kept away from the moon
    cx, cy, R = 300, 430, 235
    for _ in range(140):
        x, y = rng.uniform(0, W * S), rng.uniform(0, H * S)
        if math.hypot(x - cx, y - cy) < R + 60:
            continue
        r = rng.choice([1, 1, 2, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

    # moon: waxing gibbous ~95%. Lit disc with a thin dark sliver on the left.
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(235, 235, 235))
    # maria — soft grey patches, the dither turns them into speckle
    maria = [(-60, -90, 95), (55, -30, 80), (-30, 40, 70), (85, 70, 55), (-95, 95, 45)]
    for mx, my, mr in maria:
        d.ellipse([cx + mx - mr, cy + my - mr, cx + mx + mr, cy + my + mr],
                  fill=(178, 178, 178))
    # craters
    for _ in range(26):
        a = rng.uniform(0, 2 * math.pi)
        rr = R * math.sqrt(rng.uniform(0, 0.92))
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        r = rng.uniform(3, 12)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(150, 150, 150), width=2)
    # terminator sliver (illumination ~95%, lit side east/right)
    f = 0.95
    a_term = R * (2 * f - 1)  # semi-minor axis of terminator ellipse
    arc = [(cx + R * math.cos(t), cy - R * math.sin(t))
           for t in [math.pi / 2 + i * math.pi / 60 for i in range(61)]]
    term = [(cx - a_term * math.sin(v), cy - R * math.cos(v))
            for v in [math.pi - i * math.pi / 60 for i in range(61)]]
    d.polygon(arc + term, fill=(22, 22, 22))

    # right column of text
    tx = 580
    f_ttl = ImageFont.truetype(SERIF_B, 82)
    f_sub = ImageFont.truetype(SERIF, 38)
    f_row = ImageFont.truetype(DEJA, 31)
    f_rowb = ImageFont.truetype(DEJA_B, 31)
    d.text((tx, 90), "BUCK MOON", font=f_ttl, fill=WHITE)
    d.line([tx + 4, 192, tx + 560, 192], fill=RED, width=8)
    d.text((tx, 216), "waxing gibbous · 95% lit", font=f_sub, fill=WHITE)

    rows = [
        ("TONIGHT", "δ Aquariid peak, moonlit", WHITE),
        ("WED 29", "FULL BUCK MOON", RED),
        ("FRI 31", "α Cap + δ Aqr showers", WHITE),
        ("AUG 12", "Perseid maximum", WHITE),
    ]
    y = 320
    for when, what, col in rows:
        d.text((tx, y), when, font=f_rowb, fill=RED if col is RED else WHITE)
        d.text((tx + 175, y), what, font=f_row, fill=col)
        y += 62

    f_cap = ImageFont.truetype(SERIF, 34)
    d.text((tx, 630), "the moon that names itself:", font=f_cap, fill=(200, 200, 200))
    d.text((tx, 674), "new antlers rising in velvet", font=f_cap, fill=(200, 200, 200))
    f_date = ImageFont.truetype(MONO, 30)
    d.text((70, 820), "27 JULY 2026", font=f_date, fill=WHITE)
    d.text((tx, 820), "e-ink almanac", font=f_date, fill=(160, 160, 160))
    finish(img, "1.png")


# ----------------------------------------------------------------------
# 2. Comet — constructivist poster
# ----------------------------------------------------------------------
def comet_poster():
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)

    # big red circle — the rising jet age
    d.ellipse([120, 60, 560, 500], fill=RED)

    # black diagonal band = the fuselage / flight path, lower-left to upper-right
    ang = math.radians(-14)
    ux, uy = math.cos(ang), math.sin(ang)   # along band
    nx, ny = -uy, ux                        # normal
    cx0, cy0 = 90, 640                      # band start (left edge)
    hw = 82                                 # half width
    L = 1400
    band = [(cx0 + nx * hw, cy0 + ny * hw),
            (cx0 - nx * hw, cy0 - ny * hw),
            (cx0 + ux * L - nx * hw, cy0 + uy * L - ny * hw),
            (cx0 + ux * L + nx * hw, cy0 + uy * L + ny * hw)]
    band = [band[0], band[3], band[2], band[1]]
    d.polygon(band, fill=BLACK)
    # nose cone
    tipx, tipy = cx0 + ux * L, cy0 + uy * L
    d.polygon([(tipx + nx * hw, tipy + ny * hw),
               (tipx - nx * hw, tipy - ny * hw),
               (tipx + ux * 130, tipy + uy * 130)], fill=BLACK)

    # the infamous square windows, then the oval that fixed them
    sq = 46
    for i in range(6):
        t = 220 + i * 118
        wx, wy = cx0 + ux * t, cy0 + uy * t
        c, s_ = math.cos(ang), math.sin(ang)
        half = sq / 2
        corners = [(-half, -half), (half, -half), (half, half), (-half, half)]
        rot = [(wx + px * c - py * s_, wy + px * s_ + py * c) for px, py in corners]
        d.polygon(rot, fill=WHITE)
    # oval window — the lesson learned — in red
    t = 220 + 6 * 118
    wx, wy = cx0 + ux * t, cy0 + uy * t
    ov = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse([30, 22, 90, 98], fill=RED)
    ov = ov.rotate(-math.degrees(ang), resample=Image.BICUBIC)
    img.paste(ov, (int(wx) - 60, int(wy) - 60), ov)

    # typography
    f_h1 = ImageFont.truetype(DEJA_B, 118)
    f_h2 = ImageFont.truetype(DEJA_B, 52)
    f_sm = ImageFont.truetype(MONO, 33)
    d.text((620, 130), "COMET", font=f_h1, fill=BLACK)
    d.text((624, 268), "THE JET AGE", font=f_h2, fill=RED)
    d.text((624, 330), "BEGINS", font=f_h2, fill=BLACK)
    d.text((90, 790), "de HAVILLAND DH.106 · FIRST FLIGHT 27 JULY 1949", font=f_sm, fill=BLACK)
    d.text((90, 834), "SIX SQUARE WINDOWS AND THE OVAL THAT LEARNED BETTER", font=f_sm, fill=(120, 120, 120))
    finish(img, "2.png")


# ----------------------------------------------------------------------
# 3. Wheatfield with Crows — for Vincent
# ----------------------------------------------------------------------
def wheatfield():
    rng = random.Random(1890_0727)
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)
    horizon = 330

    # sky: near-black, built from swirling pen strokes
    d.rectangle([0, 0, W * S, horizon], fill=(15, 15, 15))
    for _ in range(900):
        x = rng.uniform(0, W * S)
        y = rng.uniform(0, horizon)
        a = math.sin(x * 0.004 + y * 0.01) * 1.4 + math.cos(y * 0.006) * 0.8
        ln = rng.uniform(14, 40)
        x2, y2 = x + ln * math.cos(a), y + ln * math.sin(a) * 0.45
        g = rng.choice([70, 90, 110, 130])
        d.line([x, y, x2, y2], fill=(g, g, g), width=3)

    # wheat: white-gold field of short curved strokes
    d.rectangle([0, horizon, W * S, H * S], fill=(250, 250, 250))
    for _ in range(2600):
        x = rng.uniform(0, W * S)
        y = rng.uniform(horizon, H * S)
        depth = (y - horizon) / (H * S - horizon)
        ln = 8 + 34 * depth
        sway = rng.uniform(-0.5, 0.5)
        x2 = x + ln * math.sin(sway)
        y2 = y - ln
        g = rng.choice([0, 0, 60, 100])
        d.line([x, y, x2, y2], fill=(g, g, g), width=max(2, int(1 + 3 * depth)))

    # the red path, forking through the wheat like in the painting
    def path(x_at, w_at):
        pts_l, pts_r = [], []
        for i in range(41):
            u = i / 40
            y = horizon + u * (H * S - horizon)
            x = x_at(u)
            w_ = w_at(u)
            pts_l.append((x - w_ / 2, y))
            pts_r.append((x + w_ / 2, y))
        d.polygon(pts_l + pts_r[::-1], fill=RED)
    path(lambda u: 600 + 320 * (1 - u) * math.sin(3.2 * u) - 40 * u,
         lambda u: 14 + 150 * u)
    path(lambda u: 600 - 40 * u ** 0.5 - 500 * u,      # left fork
         lambda u: 10 + 60 * u)
    path(lambda u: 640 + 90 * u ** 0.5 + 460 * u,      # right fork
         lambda u: 10 + 60 * u)

    # crows — scattered "m" strokes lifting off toward the sky
    for _ in range(17):
        x = rng.uniform(120, W * S - 140)
        y = rng.uniform(150, horizon + 220)
        sz = rng.uniform(10, 26)
        wgt = max(3, int(sz / 4))
        d.line([x - sz, y, x - sz * 0.3, y - sz * 0.55, x, y], width=wgt,
               fill=WHITE if y < horizon - 20 else BLACK, joint="curve")
        d.line([x, y, x + sz * 0.3, y - sz * 0.55, x + sz, y], width=wgt,
               fill=WHITE if y < horizon - 20 else BLACK, joint="curve")

    f_cap = ImageFont.truetype(SERIF, 34)
    cap = "for Vincent · Auvers-sur-Oise · 27 July 1890"
    tw = d.textlength(cap, font=f_cap)
    d.rectangle([24, H * S - 76, 24 + tw + 40, H * S - 20], fill=WHITE, outline=BLACK, width=3)
    d.text((44, H * S - 68), cap, font=f_cap, fill=BLACK)
    finish(img, "3.png")


# ----------------------------------------------------------------------
# 4. Kamon — date-seeded family crest
# ----------------------------------------------------------------------
def kamon():
    rng = random.Random(20260727)
    S4 = 4
    img = Image.new("RGB", (W * S4, H * S4), WHITE)
    d = ImageDraw.Draw(img)
    cx, cy = W * S4 // 2, 132 * S4
    R = 108 * S4

    # maru — the enclosing ring
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)
    ring_in = int(R * 0.90)
    d.ellipse([cx - ring_in, cy - ring_in, cx + ring_in, cy + ring_in], fill=WHITE)
    disc = int(R * 0.84)
    d.ellipse([cx - disc, cy - disc, cx + disc, cy + disc], fill=BLACK)

    # k-fold flower of white petals on the black disc
    k = rng.choice([5, 6, 8])
    layer = Image.new("L", (2 * disc, 2 * disc), 0)
    ld = ImageDraw.Draw(layer)
    pl = int(disc * 0.78)   # petal length
    pw = int(disc * 2 * math.sin(math.pi / k) * 0.52)  # petal width
    ld.ellipse([disc - pw // 2, disc - pl, disc + pw // 2, disc - int(pl * 0.08)], fill=255)
    petals = Image.new("L", (2 * disc, 2 * disc), 0)
    for i in range(k):
        petals.paste(255, (0, 0), layer.rotate(i * 360 / k, resample=Image.BICUBIC))
    img.paste(WHITE, (cx - disc, cy - disc), petals)

    # small black eye inside each petal
    for i in range(k):
        a = math.radians(i * 360 / k - 90)
        px = cx + int(disc * 0.52 * math.cos(a))
        py = cy + int(disc * 0.52 * math.sin(a))
        r = int(disc * 0.10)
        d.ellipse([px - r, py - r, px + r, py + r], fill=BLACK)

    # red core
    r = int(disc * 0.20)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    r2 = int(disc * 0.09)
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=WHITE)

    # caption: fumizuki, the old name for the seventh month — "the month of letters"
    f_jp = ImageFont.truetype(JP, 46 * S4 // 3)
    f_sm = ImageFont.truetype(MONO, 12 * S4)
    txt = "文月"
    tw = d.textlength(txt, font=f_jp)
    d.text((cx - tw / 2, 252 * S4), txt, font=f_jp, fill=BLACK)
    sub = f"FUMIZUKI · MONTH OF LETTERS · {k}-FOLD CREST 20260727"
    tw = d.textlength(sub, font=f_sm)
    d.text((cx - tw / 2, 278 * S4), sub, font=f_sm, fill=RED)
    finish(img, "4.png")


# ----------------------------------------------------------------------
# 5. Truchet tiles
# ----------------------------------------------------------------------
def truchet():
    rng = random.Random(0x20260727)
    ts = 25 * S               # tile size at 3x  -> 16 x 12 grid
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)
    lw = 14

    def qarc(cxa, cya, a0, a1, col):
        # clean quarter-circle stroke: filled annulus sector (pieslice minus core)
        r_out = ts // 2 + lw // 2
        r_in = ts // 2 - lw // 2
        d.pieslice([cxa - r_out, cya - r_out, cxa + r_out, cya + r_out],
                   a0, a1, fill=col)
        d.pieslice([cxa - r_in, cya - r_in, cxa + r_in, cya + r_in],
                   a0, a1, fill=WHITE)

    for gy in range(H * S // ts):
        for gx in range(W * S // ts):
            x, y = gx * ts, gy * ts
            col = RED if rng.random() < 0.11 else BLACK
            if rng.random() < 0.5:
                qarc(x, y, 0, 90, col)
                qarc(x + ts, y + ts, 180, 270, col)
            else:
                qarc(x + ts, y, 90, 180, col)
                qarc(x, y + ts, 270, 360, col)
    finish(img, "5.png")


if __name__ == "__main__":
    buck_moon()
    comet_poster()
    wheatfield()
    kamon()
    truchet()
