#!/usr/bin/env python3
"""
2026-07-11 — day 3. "Departures."
Five pictures for a 400x300 black/white/red e-ink screen.

July 11 is a day of departures and descents:
  1405 - Zheng He's treasure fleet sails from Liujiagang (62 treasure ships, 27,800 men)
  1897 - Andrée's balloon Örnen (the Eagle) lifts off from Danskøya for the North Pole
  1960 - To Kill a Mockingbird is published
  1979 - Skylab comes down over the Indian Ocean and Western Australia
  tonight - dark-of-the-moon week begins; new supermoon July 14, best Milky Way of the month

1. skylab      - constructivist re-entry poster (crisp)
2. fleet       - Zheng He's junks on a seigaiha sea, red sun (crisp)
3. mockingbird - generative tree + bird, homage to the 1960 first-edition cover (crisp)
4. eagle       - Örnen over the pack ice, midnight sun (dithered scene)
5. almanac     - dark-of-the-moon card, moon strip Jul 11 -> 14 (crisp)
"""

import math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3                      # supersample factor
BW, BH = W * S, H * S      # big canvas

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

DJV = "/usr/share/fonts/truetype/dejavu/"
F_SANS_B = DJV + "DejaVuSans-Bold.ttf"
F_SERIF_B = DJV + "DejaVuSerif-Bold.ttf"
F_SERIF = DJV + "DejaVuSerif.ttf"
F_MONO = DJV + "DejaVuSansMono.ttf"
F_MONO_B = DJV + "DejaVuSansMono-Bold.ttf"
F_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def font(path, px):
    return ImageFont.truetype(path, px)


def palette_img():
    p = Image.new("P", (1, 1))
    p.putpalette(list(BLACK) + list(WHITE) + list(RED) + [0, 0, 0] * 253)
    return p


PAL = palette_img()


def finish(img, name, dither):
    """Downscale 3x -> 1x, snap to the 3-color palette, save mode-P PNG."""
    small = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    out = small.quantize(palette=PAL, dither=d)
    out.save(name)
    print("wrote", name)


def ctext(d, xy, text, f, fill, anchor="mm"):
    d.text(xy, text, font=f, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- 1. SKYLAB
def skylab():
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    # black field of space: whole top, sweeping down-left
    d.polygon([(0, 0), (BW, 0), (BW, int(BH * 0.30)), (0, int(BH * 0.78))], fill=BLACK)

    # the station: white circle with cross (solar wings) inside the black field
    cx, cy, r = int(BW * 0.24), int(BH * 0.24), int(BH * 0.15)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    d.ellipse([cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18], outline=BLACK, width=10)
    # solar panel wings as black bars across the circle
    d.rectangle([cx - r + 30, cy - 22, cx + r - 30, cy + 22], fill=BLACK)
    d.rectangle([cx - 22, cy - r + 30, cx + 22, cy + r - 30], fill=BLACK)

    # the red wedge of re-entry: from the circle down toward lower right
    x0, y0 = cx + int(r * 0.5), cy + int(r * 0.5)
    x1, y1 = int(BW * 0.86), int(BH * 0.80)
    wedge_w = 130
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    d.polygon([(x0 + nx * wedge_w, y0 + ny * wedge_w),
               (x0 - nx * wedge_w, y0 - ny * wedge_w),
               (x1, y1)], fill=RED)

    # fragments breaking off the wedge
    rng = random.Random(19790711)
    placed = 0
    while placed < 12:
        i = placed
        t = 0.35 + 0.6 * rng.random()
        px = x0 + dx * t + nx * (wedge_w + 40 + rng.random() * 150) * (1 if i % 2 else -1)
        py = y0 + dy * t + ny * (wedge_w + 40 + rng.random() * 150) * (1 if i % 2 else -1)
        if py > BH * 0.68 or px > BW * 0.96 or (px > BW * 0.50 and py < BH * 0.30):
            placed += 1        # keep clear of caption zone, edge, and headline
            continue
        placed += 1
        s = 14 + rng.random() * 36
        ang = rng.random() * math.pi
        ca, sa = math.cos(ang), math.sin(ang)
        pts = [(px + ca * s - sa * s * .4, py + sa * s + ca * s * .4),
               (px - ca * s - sa * s * .4, py - sa * s + ca * s * .4),
               (px - ca * s + sa * s * .4, py - sa * s - ca * s * .4),
               (px + ca * s + sa * s * .4, py + sa * s - ca * s * .4)]
        d.polygon(pts, fill=RED if i % 3 else BLACK)

    # the coastline strip at the bottom (Western Australia, roughly)
    base = int(BH * 0.93)
    coast = [(0, BH), (0, base + 20)]
    xs = 0
    rng2 = random.Random(7)
    while xs <= BW:
        coast.append((xs, base + int(18 * math.sin(xs / 260.0)) + rng2.randint(-8, 8)))
        xs += 60
    coast.append((BW, BH))
    d.polygon(coast, fill=BLACK)

    # type — size the headline to fit the right 45% exactly
    fsize = 124
    while d.textlength("SKYLAB", font=font(F_SANS_B, fsize)) > BW * 0.46:
        fsize -= 4
    ctext(d, (BW - 40, int(BH * 0.11)), "SKYLAB", font(F_SANS_B, fsize), WHITE, "rm")
    ctext(d, (BW - 40, int(BH * 0.235)), "IS FALLING", font(F_SANS_B, 58), RED, "rm")
    ctext(d, (int(BW * 0.045), int(BH * 0.83)), "RE-ENTRY · 11 JULY 1979", font(F_MONO_B, 40), BLACK, "lm")
    ctext(d, (int(BW * 0.045), int(BH * 0.885)), "77 t · indian ocean → esperance, w. australia", font(F_MONO, 31), BLACK, "lm")
    ctext(d, (BW - 30, BH - 26), "no one was hurt", font(F_MONO, 29), WHITE, "rd")

    finish(img, "1.png", dither=False)


# ---------------------------------------------------------------- 2. TREASURE FLEET
def fleet():
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    horizon = int(BH * 0.44)

    # red sun, top right — the big junk sails in front of it
    scx, scy, sr = int(BW * 0.82), int(BH * 0.22), int(BH * 0.13)
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=RED)

    # seigaiha sea: rows of concentric-arc "scales", far -> near, radius growing
    rng = random.Random(1405)
    y = horizon
    row = 0
    while y < BH + 200:
        t = (y - horizon) / (BH - horizon + 1)
        R = int(60 + 150 * t)            # scale radius grows toward viewer
        step_x = R                        # half-overlap horizontally
        off = (R // 2) if row % 2 else 0
        x = -R + off
        while x < BW + R:
            # occlude what's behind
            d.ellipse([x - R, y - R, x + R, y + R], fill=WHITE)
            # concentric rings; occasionally a red innermost set
            red_scale = rng.random() < 0.07
            for k, f in enumerate([1.0, 0.78, 0.56, 0.34]):
                rr = int(R * f)
                col = RED if (red_scale and k >= 2) else BLACK
                w = max(6, R // 16)
                d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=col, width=w)
            x += step_x
        y += int(R * 0.42)
        row += 1

    # junk silhouettes on the horizon (drawn after far rows? sea covers below horizon,
    # so ships sit in the white sky band, hulls touching the horizon)
    def junk(cx, base, scale):
        # hull with raised stern
        hull = [(cx - 90 * scale, base - 26 * scale), (cx + 78 * scale, base - 26 * scale),
                (cx + 100 * scale, base - 62 * scale), (cx + 60 * scale, base - 40 * scale),
                (cx - 60 * scale, base - 40 * scale), (cx - 104 * scale, base - 56 * scale)]
        d.polygon([(cx - 90 * scale, base), (cx + 78 * scale, base),
                   (cx + 104 * scale, base - 58 * scale), (cx - 110 * scale, base - 50 * scale)], fill=BLACK)
        # three battened lugsails
        for mx, mh, mw in [(-52, 120, 40), (2, 168, 56), (58, 132, 44)]:
            mastx = cx + mx * scale
            top = base - (58 + mh) * scale
            d.line([mastx, base - 40 * scale, mastx, top], fill=BLACK, width=max(3, int(6 * scale)))
            sail = [(mastx - mw * scale, top + 14 * scale),
                    (mastx + mw * scale * 0.75, top),
                    (mastx + mw * scale * 0.95, base - 64 * scale),
                    (mastx - mw * scale * 0.8, base - 58 * scale)]
            d.polygon(sail, fill=BLACK)
            # battens shown as white lines through the sail
            for bi in range(1, 5):
                fy = bi / 5.0
                ax = mastx - mw * scale * (1 - 0.2 * fy)
                bx2 = mastx + mw * scale * (0.75 + 0.2 * fy)
                ay = top + 14 * scale + (base - 64 * scale - top - 14 * scale) * fy
                d.line([ax, ay, bx2, ay + 6 * scale], fill=WHITE, width=max(2, int(4 * scale)))

    junk(int(BW * 0.76), horizon + 8, 1.0)
    junk(int(BW * 0.40), horizon + 6, 0.6)
    junk(int(BW * 0.14), horizon + 4, 0.5)

    # title cartouche, top left, drawn last so nothing collides with it
    d.rectangle([24, 24, 704, 244], fill=WHITE, outline=BLACK, width=5)
    ctext(d, (52, 44), "鄭和下西洋", font(F_JP, 74), BLACK, "la")
    ctext(d, (52, 140), "the treasure fleet sails · 11 july 1405", font(F_MONO_B, 26), BLACK, "la")
    ctext(d, (52, 186), "62 treasure ships · 317 sail · 27,800 men", font(F_MONO, 25), RED, "la")

    finish(img, "2.png", dither=False)


# ---------------------------------------------------------------- 3. MOCKINGBIRD
def mockingbird():
    img = Image.new("RGB", (BW, BH), BLACK)
    d = ImageDraw.Draw(img)

    band_h = int(BH * 0.30)

    # generative tree, white on black — drawn first; the band will crop its crown
    rng = random.Random(19600711)
    branch_tips = []

    def branch(x, y, angle, length, depth, width):
        if depth == 0 or length < 14:
            branch_tips.append((x, y))
            return
        x2 = x + math.cos(angle) * length
        y2 = y - math.sin(angle) * length
        d.line([x, y, x2, y2], fill=WHITE, width=max(3, int(width)))
        n = 2 if rng.random() < 0.6 else 3
        for k in range(n):
            da = rng.uniform(0.25, 0.95) * (1 if (k + (1 if rng.random() < 0.5 else 0)) % 2 else -1)
            # bend branches back down if they climb toward the band
            if y2 < band_h + BH * 0.22 and angle + da > math.pi * 0.35:
                da -= 0.8
            branch(x2, y2, angle + da, length * rng.uniform(0.58, 0.76), depth - 1, width * 0.62)

    trunk_x = int(BW * 0.30)
    d.line([trunk_x, BH, trunk_x - 14, int(BH * 0.70)], fill=WHITE, width=48)
    branch(trunk_x - 14, int(BH * 0.70), math.pi / 2 + 0.05, BH * 0.155, 8, 30)

    # the knothole: a red oval on the trunk (where Boo left the gifts)
    kx, ky = trunk_x - 6, int(BH * 0.82)
    d.ellipse([kx - 22, ky - 36, kx + 22, ky + 36], fill=RED)

    # red title band across the top, like the 1960 jacket (crops the tree crown)
    d.rectangle([0, 0, BW, band_h], fill=RED)
    ctext(d, (BW // 2, int(band_h * 0.30)), "TO KILL A", font(F_SERIF_B, 78), WHITE)
    ctext(d, (BW // 2, int(band_h * 0.68)), "MOCKINGBIRD", font(F_SERIF_B, 100), BLACK)

    # the bird: perched on the rightmost branch tip below the band
    tips = [t for t in branch_tips if t[0] > BW * 0.42 and band_h + 100 < t[1] < BH * 0.66]
    bx, by = max(tips, key=lambda t: t[0]) if tips else (int(BW * 0.62), int(BH * 0.5))
    # legs down to the tip
    d.line([bx - 10, by - 14, bx - 4, by], fill=WHITE, width=5)
    d.line([bx + 12, by - 14, bx + 6, by], fill=WHITE, width=5)
    # body
    d.ellipse([bx - 34, by - 70, bx + 34, by - 12], fill=WHITE)
    # head
    d.ellipse([bx + 14, by - 96, bx + 52, by - 58], fill=WHITE)
    # beak
    d.polygon([(bx + 50, by - 82), (bx + 74, by - 74), (bx + 50, by - 68)], fill=WHITE)
    # tail
    d.polygon([(bx - 28, by - 48), (bx - 94, by - 10), (bx - 24, by - 24)], fill=WHITE)
    # eye
    d.ellipse([bx + 30, by - 84, bx + 40, by - 74], fill=BLACK)

    ctext(d, (BW - 40, BH - 90), "harper lee", font(F_SERIF, 44), WHITE, "rs")
    ctext(d, (BW - 40, BH - 40), "first published 11 july 1960", font(F_MONO, 30), RED, "rs")

    finish(img, "3.png", dither=False)


# ---------------------------------------------------------------- 4. THE EAGLE
def eagle():
    img = Image.new("RGB", (BW, BH), WHITE)
    d = ImageDraw.Draw(img)

    horizon = int(BH * 0.58)

    # sky: gentle gradient, brightest at the horizon
    for yy in range(0, horizon):
        g = 150 + int(105 * (yy / horizon))
        d.line([0, yy, BW, yy], fill=(g, g, g))

    # midnight sun: red disc sitting on the horizon
    scx, sr = int(BW * 0.78), int(BH * 0.11)
    d.ellipse([scx - sr, horizon - sr - 10, scx + sr, horizon + sr - 10], fill=RED)

    # sea band at the horizon
    d.rectangle([0, horizon - 8, BW, horizon + 30], fill=(40, 40, 40))

    # pack ice: white polygonal floes with dark leads between them
    rng = random.Random(1897)
    d.rectangle([0, horizon + 20, BW, BH], fill=(230, 230, 230))
    yy = horizon + 26
    rowi = 0
    while yy < BH + 60:
        t = (yy - horizon) / (BH - horizon)
        fw = 90 + 320 * t
        fh = 22 + 90 * t
        x = -rng.randint(0, int(fw)) + (rowi % 2) * fw * 0.5
        while x < BW + fw:
            pts = []
            n = 6
            for k in range(n):
                a = 2 * math.pi * k / n
                rr = (fw / 2) * (0.75 + 0.3 * rng.random())
                pts.append((x + math.cos(a) * rr, yy + math.sin(a) * rr * (fh / fw)))
            d.polygon(pts, fill=WHITE, outline=(70, 70, 70), width=4)
            x += fw * rng.uniform(0.85, 1.1)
        yy += fh * 0.9
        rowi += 1

    # the balloon
    bcx, bcy, br = int(BW * 0.30), int(BH * 0.235), int(BH * 0.155)
    d.ellipse([bcx - br, bcy - br, bcx + br, bcy + br], fill=(245, 245, 245), outline=BLACK, width=8)
    # netting
    for k in range(1, 6):
        off = br * k / 6.0
        d.arc([bcx - br, bcy - br, bcx + br, bcy + br], 0, 360, fill=BLACK, width=2)
        d.line([bcx - math.sqrt(max(br * br - off * off, 0)), bcy + off,
                bcx + math.sqrt(max(br * br - off * off, 0)), bcy + off], fill=BLACK, width=3)
        d.arc([bcx - off, bcy - br, bcx + off, bcy + br], 0, 360, fill=BLACK, width=3)
    # basket
    bky = bcy + br + int(BH * 0.10)
    d.line([bcx - br * 0.6, bcy + br * 0.75, bcx - 30, bky], fill=BLACK, width=5)
    d.line([bcx + br * 0.6, bcy + br * 0.75, bcx + 30, bky], fill=BLACK, width=5)
    d.rectangle([bcx - 34, bky, bcx + 34, bky + 46], fill=BLACK)
    # drag ropes trailing to the ice
    for ex, sag in [(-260, 240), (-140, 320), (30, 380)]:
        pts = []
        for k in range(24):
            tt = k / 23.0
            px = bcx + (ex - 0) * tt
            py = bky + 46 + (sag * tt * tt) + 60 * math.sin(tt * 2.2)
            pts.append((px, py))
        d.line(pts, fill=BLACK, width=3)

    # caption plate (solid white behind text)
    d.rectangle([BW - 640, 40, BW - 36, 210], fill=WHITE, outline=BLACK, width=4)
    ctext(d, (BW - 338, 84), "ÖRNEN · THE EAGLE", font(F_SERIF_B, 44), BLACK)
    ctext(d, (BW - 338, 136), "Danskøya, Svalbard · 11 July 1897", font(F_MONO, 29), BLACK)
    ctext(d, (BW - 338, 178), "three men flew for the pole", font(F_MONO, 29), RED)

    finish(img, "4.png", dither=True)


# ---------------------------------------------------------------- 5. ALMANAC
def almanac():
    img = Image.new("RGB", (BW, BH), BLACK)
    d = ImageDraw.Draw(img)

    ctext(d, (BW // 2, 62), "DARK OF THE MOON", font(F_SANS_B, 72), WHITE)
    ctext(d, (BW // 2, 130), "the moon leaves the night sky · best milky way week", font(F_MONO, 30), WHITE)

    # moon strip Jul 11 -> 14
    days = [("JUL 11", 0.13), ("JUL 12", 0.06), ("JUL 13", 0.02), ("JUL 14", 0.0)]
    n = len(days)
    r = int(BH * 0.115)
    y = int(BH * 0.42)
    for i, (label, frac) in enumerate(days):
        x = int(BW * (i + 0.5) / n)
        if frac <= 0.005:
            # new moon: black disc with red ring — the supermoon
            d.ellipse([x - r, y - r, x + r, y + r], outline=RED, width=10)
        else:
            # waning crescent, lit on the left: white disc, shadow disc shifted right
            d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
            shift = int(2 * r * frac * 1.6)
            d.ellipse([x - r + shift, y - r - 6, x + r + shift, y + r + 6], fill=BLACK)
        ctext(d, (x, y + r + 44), label, font(F_MONO_B, 34), RED if frac == 0.0 else WHITE)
    ctext(d, (int(BW * 0.875), y - r - 40), "NEW SUPERMOON", font(F_MONO_B, 28), RED)

    # notes
    ny = int(BH * 0.72)
    lines = [
        ("this morning", "moon · mars · pleiades before dawn", WHITE),
        ("jul 14 09:44", "new supermoon — 4th of 5 in a row", RED),
        ("all week", "moonless nights, milky way at its best", WHITE),
    ]
    for i, (a, b, col) in enumerate(lines):
        yy = ny + i * 62
        ctext(d, (60, yy), a, font(F_MONO_B, 31), col, "lm")
        ctext(d, (430, yy), b, font(F_MONO, 31), WHITE, "lm")

    finish(img, "5.png", dither=False)


if __name__ == "__main__":
    skylab()
    fleet()
    mockingbird()
    eagle()
    almanac()
