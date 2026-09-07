#!/usr/bin/env python3
"""
2026-07-28 — five pictures for a 400x300 black/white/red e-ink screen.

Today: 175th anniversary of the first photograph of a total solar eclipse
(Berkowski, Königsberg, 28 July 1851). Bach died on this day in 1750.
Full Buck Moon tomorrow; Perseids + new supermoon coming Aug 12-13.

1. berkowski   — the 1851 eclipse daguerreotype, reimagined (dithered)
2. red wedge   — homage to El Lissitzky, 1919 (hard-edged)
3. b-a-c-h     — the fugue that ends mid-measure (hard-edged)
4. almanac     — Buck Moon card + late-summer sky calendar (dithered)
5. mitsudomoe  — kamon crest generator, first motif: three commas (hard-edged)
"""

import math
import os
import random
import shutil

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 400, 300
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "images")

F = "/usr/share/fonts/truetype"
SERIF = f"{F}/dejavu/DejaVuSerif.ttf"
SERIF_B = f"{F}/dejavu/DejaVuSerif-Bold.ttf"
SANS = f"{F}/dejavu/DejaVuSans.ttf"
SANS_B = f"{F}/dejavu/DejaVuSans-Bold.ttf"
MONO = f"{F}/dejavu/DejaVuSansMono.ttf"
JP = f"{F}/fonts-japanese-gothic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def palette_image():
    p = Image.new("P", (1, 1))
    p.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0] * 253 * 3)
    return p


PAL = palette_image()


def finish(img, name, dither):
    """Downscale to 400x300 and lock into the exact 3-color palette."""
    small = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    q = small.convert("RGB").quantize(palette=PAL, dither=d)
    q.save(os.path.join(OUT, name))
    print("wrote", name)


def ctext(draw, xy, s, fnt, fill, anchor="mm"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def fitfont(dr, path, size, text, maxw):
    """Largest font of `path` at most `size` that fits `text` in maxw px."""
    f = font(path, size)
    while size > 12 and dr.textlength(text, font=f) > maxw:
        size -= 2
        f = font(path, size)
    return f


# ---------------------------------------------------------------- 1. eclipse
def berkowski():
    """28 July 1851: Johann Julius Friedrich Berkowski exposes a daguerreotype
    for 84 seconds at the Royal Observatory, Königsberg, and catches the
    corona and prominences of a total solar eclipse for the first time."""
    random.seed("berkowski-1851")
    S = 3
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)

    # daguerreotype plate mount: white frame, deep bottom band for the caption
    ml, mt, mr, mb = 66, 66, 66, 210
    px0, py0, px1, py1 = ml, mt, W * S - mr, H * S - mb
    dr.rectangle([px0, py0, px1, py1], fill=BLACK)
    dr.rectangle([px0 - 6, py0 - 6, px1 + 6, py1 + 6], outline=BLACK, width=3)

    cx, cy = (px0 + px1) // 2, (py0 + py1) // 2
    r0 = 168  # lunar disk radius

    # faint stars visible during totality
    for _ in range(70):
        x = random.randint(px0 + 10, px1 - 10)
        y = random.randint(py0 + 10, py1 - 10)
        if math.hypot(x - cx, y - cy) > r0 * 2.1:
            v = random.randint(70, 200)
            dr.ellipse([x, y, x + 2, y + 2], fill=(v, v, v))

    # corona: radial streamers, longest near the solar equator
    cor = Image.new("L", img.size, 0)
    cd = ImageDraw.Draw(cor)
    for _ in range(950):
        th = random.uniform(0, 2 * math.pi)
        eq = math.exp(-(math.sin(th) ** 2) * 3.2)  # equatorial boost
        L = 26 + 330 * eq * random.uniform(0.25, 1.0) + 55 * random.random()
        r1 = r0 - 4
        r2 = r0 + L
        x1, y1 = cx + r1 * math.cos(th), cy + r1 * math.sin(th)
        x2, y2 = cx + r2 * math.cos(th), cy + r2 * math.sin(th)
        v = random.randint(90, 255)
        cd.line([x1, y1, x2, y2], fill=v, width=random.choice([2, 2, 3, 4]))
    # polar brushes: short fine tufts
    for _ in range(240):
        th = random.choice([math.pi / 2, -math.pi / 2]) + random.uniform(-0.5, 0.5)
        L = 20 + 80 * random.random()
        x1, y1 = cx + (r0 - 2) * math.cos(th), cy + (r0 - 2) * math.sin(th)
        x2, y2 = cx + (r0 + L) * math.cos(th), cy + (r0 + L) * math.sin(th)
        cd.line([x1, y1, x2, y2], fill=random.randint(60, 160), width=2)
    # inner glow ring
    for rr in range(r0, r0 + 26):
        a = int(255 * (1 - (rr - r0) / 26) ** 1.5)
        cd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=a, width=2)
    cor = cor.filter(ImageFilter.GaussianBlur(5))
    img.paste(WHITE, (0, 0), cor)

    # the moon
    dr.ellipse([cx - r0, cy - r0, cx + r0, cy + r0], fill=BLACK)

    # red prominences peeking past the limb (what amazed the astronomers)
    for th_deg in (18, 71, 152, 233, 297, 335):
        th = math.radians(th_deg)
        n = random.randint(2, 4)
        for i in range(n):
            t2 = th + random.uniform(-0.05, 0.05)
            pr = random.randint(7, 15)
            d = r0 + pr * random.uniform(0.1, 0.55)
            x, y = cx + d * math.cos(t2), cy + d * math.sin(t2)
            dr.ellipse([x - pr, y - pr, x + pr, y + pr], fill=RED)
    # re-cut the disk so prominences only show outside the limb
    dr.ellipse([cx - r0 + 2, cy - r0 + 2, cx + r0 - 2, cy + r0 - 2], fill=BLACK)

    # caption on the mount
    maxw = W * S - 140
    t1 = "THE CORONA, PHOTOGRAPHED FOR THE FIRST TIME"
    t2 = "J. BERKOWSKI · ROYAL OBSERVATORY, KÖNIGSBERG · 28 JULY 1851"
    t3 = "175 YEARS AGO TODAY"
    fs2 = fitfont(dr, SERIF_B, 44, t1, maxw)
    fs1 = fitfont(dr, SERIF, 34, t2, maxw)
    fs3 = font(SERIF_B, 40)
    ccx = W * S // 2
    by = H * S - mb + 52
    ctext(dr, (ccx, by), t1, fs2, BLACK)
    ctext(dr, (ccx, by + 56), t2, fs1, BLACK)
    ctext(dr, (ccx, by + 118), t3, fs3, RED)

    finish(img, "1.png", dither=True)


# -------------------------------------------------------------- 2. red wedge
def red_wedge():
    """Homage to El Lissitzky's 1919 'Beat the Whites with the Red Wedge' —
    the poster that made black, white and red a complete universe.
    This screen's palette is that poster."""
    random.seed("lissitzky")
    S = 4
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)
    w, h = W * S, H * S

    # black field on the right, split by a hard diagonal
    dr.polygon([(w * 0.62, 0), (w, 0), (w, h), (w * 0.38, h)], fill=BLACK)

    # the white circle on the dark side
    ccx, ccy, R = w * 0.655, h * 0.44, h * 0.28
    dr.ellipse([ccx - R, ccy - R, ccx + R, ccy + R], fill=WHITE)

    # the red wedge, piercing the circle
    dr.polygon([(w * 0.03, h * 0.36), (w * 0.03, h * 0.52), (ccx + R * 0.12, ccy)], fill=RED)

    # satellites: order on the white side, scatter on the black side
    dr.rectangle([w * 0.06, h * 0.70, w * 0.30, h * 0.735], fill=BLACK)
    dr.rectangle([w * 0.06, h * 0.765, w * 0.22, h * 0.79], fill=BLACK)
    dr.rectangle([w * 0.06, h * 0.815, w * 0.14, h * 0.833], fill=BLACK)
    dr.ellipse([w * 0.31, h * 0.10, w * 0.355, h * 0.16], fill=RED)
    dr.polygon([(w * 0.20, h * 0.20), (w * 0.27, h * 0.20), (w * 0.20, h * 0.29)], fill=BLACK)

    for i in range(7):  # white debris field
        x = w * random.uniform(0.72, 0.95)
        y = h * random.uniform(0.62, 0.92)
        s = h * random.uniform(0.012, 0.045)
        if i % 2:
            dr.ellipse([x, y, x + s, y + s], fill=WHITE)
        else:
            dr.polygon([(x, y), (x + s, y), (x, y + s)], fill=WHITE)
    dr.polygon([(w * 0.86, h * 0.13), (w * 0.955, h * 0.10), (w * 0.90, h * 0.23)], fill=RED)

    # dashed white orbit line across the black field
    th = math.atan2(h, w * -0.24)
    for t in range(0, 100, 8):
        x1 = w * 0.98 - t * 0.006 * w
        y1 = h * 0.30 + t * 0.0052 * h
        x2 = x1 - 0.003 * w
        y2 = y1 + 0.0026 * h
        dr.line([x1, y1, x2, y2], fill=WHITE, width=6)

    fb = font(SANS_B, 66)
    fsm = font(SANS, 38)
    dr.text((w * 0.045, h * 0.055), "КЛИНОМ", font=fb, fill=BLACK)
    dr.text((w * 0.96, h * 0.86), "КРАСНЫМ", font=fb, fill=RED, anchor="rs")
    dr.text((w * 0.96, h * 0.945), "après El Lissitzky · 1919", font=fsm, fill=WHITE, anchor="rs")

    finish(img, "2.png", dither=False)


# ------------------------------------------------------------------ 3. bach
def bach():
    """J. S. Bach died 28 July 1750, leaving The Art of Fugue unfinished —
    Contrapunctus XIV breaks off just after the notes B-A-C-H
    (B-flat, A, C, B-natural) enter as a subject."""
    random.seed("bach-1750")
    S = 4
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)
    w, h = W * S, H * S

    # staff
    sx0, sx1 = 200, w - 200
    lines_y = [230 + i * 46 for i in range(5)]
    for y in lines_y:
        dr.line([sx0, y, sx1, y], fill=BLACK, width=4)
    dr.line([sx0, lines_y[0], sx0, lines_y[-1]], fill=BLACK, width=8)
    # final barline: thin + thick (the end)
    dr.line([sx1 - 28, lines_y[0], sx1 - 28, lines_y[-1]], fill=BLACK, width=4)
    dr.rectangle([sx1 - 14, lines_y[0], sx1, lines_y[-1]], fill=BLACK)

    mid = lines_y[2]
    step = 23  # half a line-gap
    # pitch offsets from middle line B4, in staff steps
    notes = [("B", 0, "♭"), ("A", -1, None), ("C", 1, None), ("H", 0, "♮")]
    xs = [430, 700, 970, 1240]
    facc = font(SERIF, 96)
    flet = font(SERIF_B, 110)
    for (name, off, acc), x in zip(notes, xs):
        y = mid - off * step
        if acc:
            dr.text((x - 100, y - 14), acc, font=facc, fill=BLACK, anchor="mm")
        dr.ellipse([x - 30, y - 22, x + 30, y + 22], fill=RED, outline=BLACK, width=4)
        dr.line([x + 27, y - 4, x + 27, y - 130], fill=BLACK, width=7)
        dr.text((x, lines_y[-1] + 74), name, font=flet, fill=BLACK, anchor="mm")

    # piano-roll fugue on the B-A-C-H subject
    rx0, ry0, rx1, ry1 = 200, 590, w - 200, 1010
    dr.rectangle([rx0, ry0, rx1, ry1], outline=BLACK, width=4)
    beats, lo, hi = 24, -13, 20
    bw = (rx1 - rx0) / beats
    ch = (ry1 - ry0) / (hi - lo + 1)
    subject = [(0, 10), (1, 9), (2, 12), (3, 11)]  # (beat, semitone): B♭ A C B♮

    def put(t, p, fill, pad, tail=0.0):
        if t < 0 or t + 1 > beats or p < lo or p > hi:
            return
        x0 = rx0 + t * bw
        y0 = ry1 - (p - lo + 1) * ch
        dr.rectangle([x0 + pad, y0 + pad, x0 + bw * (1 + tail) - pad, y0 + ch - pad], fill=fill)

    # voices state the subject in turn; inverted answers in black
    for start, tr in [(0, 6), (5, -1), (10, -8), (15, 3)]:
        for b, p in subject:
            put(start + b, p + tr, RED, pad=2, tail=0.25)
    for start, tr in [(3, 7), (8, -13), (13, 8), (17, -6)]:
        for b, p in subject:
            put(start + b, (21 - p) + tr, BLACK, pad=3, tail=0.25)
    # the last entry breaks off before its final note — the H never comes
    for b, p in subject[:3]:
        put(19 + b, p - 1, RED, pad=2, tail=0.25)
    # the manuscript ends: the last measure falls silent
    dr.line([rx1 - 2 * bw, ry0, rx1 - 2 * bw, ry1], fill=BLACK, width=3)
    fend = font(SERIF, 40)
    dr.text((rx1 - bw, (ry0 + ry1) / 2), "…", font=fend, fill=BLACK, anchor="mm")
    # tick marks every 4 beats
    for b in range(4, beats, 4):
        x = rx0 + b * bw
        dr.line([x, ry1, x, ry1 + 14], fill=BLACK, width=3)

    fcap = font(SERIF_B, 46)
    t2 = "The Art of Fugue breaks off as these four notes enter"
    fsub = fitfont(dr, SERIF, 42, t2, w - 320)
    ctext(dr, (w / 2, 1080), "JOHANN SEBASTIAN BACH · 1685 — 28 JULY 1750", fcap, BLACK)
    ctext(dr, (w / 2, 1142), t2, fsub, RED)

    finish(img, "3.png", dither=False)


# --------------------------------------------------------------- 4. almanac
def almanac():
    """Tonight's moon and the late-summer sky calendar."""
    random.seed("buckmoon-2026")
    S = 3
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)
    w, h = W * S, H * S

    fhdr = font(SANS_B, 40)
    dr.text((60, 42), "SKY ALMANAC", font=fhdr, fill=BLACK)
    dr.text((w - 60, 42), "28 JULY 2026", font=fhdr, fill=BLACK, anchor="ra")
    dr.line([60, 108, w - 60, 108], fill=BLACK, width=4)

    # night panel with the moon
    nx0, ny0, nx1, ny1 = 60, 140, 540, h - 60
    dr.rectangle([nx0, ny0, nx1, ny1], fill=BLACK)
    for _ in range(90):
        x = random.randint(nx0 + 8, nx1 - 8)
        y = random.randint(ny0 + 8, ny1 - 8)
        v = random.randint(90, 230)
        s = random.choice([2, 2, 3])
        dr.ellipse([x, y, x + s, y + s], fill=(v, v, v))

    mcx, mcy, mr = (nx0 + nx1) // 2, (ny0 + ny1) // 2 - 20, 175
    dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=(250, 250, 250))
    # maria
    for _ in range(9):
        a = random.uniform(0, 2 * math.pi)
        d = mr * random.uniform(0.15, 0.62)
        bx, by = mcx + d * math.cos(a), mcy + d * math.sin(a)
        rw, rh = mr * random.uniform(0.16, 0.4), mr * random.uniform(0.12, 0.3)
        v = random.randint(168, 205)
        dr.ellipse([bx - rw, by - rh, bx + rw, by + rh], fill=(v, v, v))
    # a few craters
    for _ in range(6):
        a = random.uniform(0, 2 * math.pi)
        d = mr * random.uniform(0.3, 0.85)
        bx, by = mcx + d * math.cos(a), mcy + d * math.sin(a)
        cr = random.randint(6, 14)
        dr.ellipse([bx - cr, by - cr, bx + cr, by + cr], outline=(150, 150, 150), width=3)
    fmoon = font(SANS_B, 34)
    ctext(dr, (mcx, ny1 - 46), "99% · RISES AT SUNSET", fmoon, WHITE)

    # right column
    rx = 590
    colw = w - 60 - rx
    ftitle = fitfont(dr, SERIF_B, 92, "BUCK MOON", colw)
    dr.text((rx, 148), "BUCK MOON", font=ftitle, fill=BLACK)
    fsub = font(SERIF, 42)
    dr.text((rx, 262), "full tomorrow · 29 July", font=fsub, fill=RED)

    fdate = font(SANS_B, 34)
    fbody = font(SANS, 34)
    rows = [
        ("JUL 29", "Full Buck Moon", BLACK),
        ("JUL 31", "double meteor peak —", BLACK),
        ("", "washed out by the moon", BLACK),
        ("AUG 12", "PERSEIDS · NEW MOON", RED),
        ("", "best display since 2018", RED),
    ]
    y = 366
    for d, txt, col in rows:
        if d:
            dr.text((rx, y), d, font=fdate, fill=col)
        dr.text((rx + 150, y), txt, font=fbody, fill=col)
        y += 54
    dr.line([rx, y + 14, w - 60, y + 14], fill=BLACK, width=3)
    ffoot = font(SANS, 33)
    for i, line in enumerate([
        "Aug 12 is also 2026's fifth and",
        "final new supermoon — the",
        "darkest possible Perseid sky.",
    ]):
        dr.text((rx, y + 44 + i * 46), line, font=ffoot, fill=BLACK)

    finish(img, "4.png", dither=True)


# -------------------------------------------------------------- 5. kamon
def kamon():
    """Kamon generator, motif one: mitsudomoe — three commas chasing each
    other in a circle. A water symbol, painted on roof tiles to ward off
    fire; also the crest of Hachiman and the taiko drum."""
    random.seed("kamon-2026-07-28")
    S = 4
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)
    w, h = W * S, H * S

    ccx, ccy = w * 0.56, h * 0.5
    R = h * 0.40
    dr.ellipse([ccx - R, ccy - R, ccx + R, ccy + R], outline=BLACK, width=26)
    R2 = R * 0.90
    dr.ellipse([ccx - R2, ccy - R2, ccx + R2, ccy + R2], outline=BLACK, width=7)

    field = R * 0.82
    d0 = field * 0.42      # tomoe head orbit radius
    rh = field * 0.30      # tomoe head radius

    def tomoe(phase):
        # head
        hx = ccx + d0 * math.cos(phase)
        hy = ccy + d0 * math.sin(phase)
        dr.ellipse([hx - rh, hy - rh, hx + rh, hy + rh], fill=RED)
        # tapering tail sweeping around, drifting out toward the rim
        steps = 90
        sweep = math.radians(150)
        for i in range(steps):
            t = i / steps
            a = phase + t * sweep
            rr = rh * (1 - t) ** 1.25
            pd = d0 + (field - rh * 0.4 - d0) * t
            x = ccx + pd * math.cos(a)
            y = ccy + pd * math.sin(a)
            dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=RED)

    for k in range(3):
        tomoe(math.radians(90 + k * 120))

    # vertical kanji, hand-set on the left
    fjp = font(JP, 96)
    for i, ch in enumerate("三つ巴"):
        dr.text((150, 170 + i * 128), ch, font=fjp, fill=BLACK, anchor="ma")
    # red seal
    dr.rectangle([120, 640, 216, 736], fill=RED)
    fseal = font(JP, 64)
    ctext(dr, (168, 690), "紋", fseal, WHITE)

    fen = font(SANS, 40)
    dr.text((w - 70, h - 124), "MITSUDOMOE — the water-whirl crest,", font=fen, fill=BLACK, anchor="ra")
    dr.text((w - 70, h - 70), "set on roof tiles to guard against fire", font=fen, fill=BLACK, anchor="ra")

    finish(img, "5.png", dither=False)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    berkowski()
    red_wedge()
    bach()
    almanac()
    kamon()
    for i in range(1, 6):
        shutil.copy2(os.path.join(OUT, f"{i}.png"), os.path.join(HERE, f"{i}.png"))
    print("archived copies in", HERE)
