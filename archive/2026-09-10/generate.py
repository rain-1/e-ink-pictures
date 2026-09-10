#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-09-10.

Five 400x300 images in exactly three colors (white, black, red).
Today's set is deliberately hard-edged and graphic — no dithered tones at all —
as a counterweight to the soft, dotted first day.

1. NEW MOON      — a constructivist poster: tonight the moon is new (03:27 UTC on the 11th).
2. MONCHŌ        — a kamon sampler sheet, every crest built from circles and straight lines.
3. EVENT 10.09   — a collider event display: 18 years since the LHC's first beam.
4. DRAFT 0910    — a weaving draft in Albers notation plus the woven drawdown.
5. OCCULTATION   — Monday the Moon hides Venus in daylight over the UK.

Everything renders at 3x for smooth curves, is downscaled with LANCZOS, then
snapped (no dither) to the exact palette. The weaving draft is drawn at 1x so
every thread is pixel-exact.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
F_FREE_SANS_B = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED)
    palette += [0, 0, 0] * (256 - 3)
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def snap(img):
    """Nearest-palette snap: white / black / red, no dithering."""
    px = img.convert("RGB").load()
    w, h = img.size
    out = Image.new("P", (w, h))
    out.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)
    op = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            # red-ish if red dominates strongly; else by luminance
            if r > 140 and g < 110 and b < 110:
                op[x, y] = 2
            elif (r + g + b) / 3 > 127:
                op[x, y] = 0
            else:
                op[x, y] = 1
    return out


def finalize(img):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return snap(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def canvas(bg=WHITE, s=SS):
    img = Image.new("RGB", (W * s, H * s), bg)
    return img, ImageDraw.Draw(img)


def seal(dr, s, day="10", corner="br", bg=WHITE):
    """My signature: a small red seal-square with the day number in white."""
    size = 15 * s
    m = 8 * s
    if corner == "br":
        x0, y0 = W * s - m - size, H * s - m - size
    elif corner == "tr":
        x0, y0 = W * s - m - size, m
    elif corner == "bl":
        x0, y0 = m, H * s - m - size
    else:
        x0, y0 = m, m
    dr.rectangle([x0, y0, x0 + size, y0 + size], fill=RED)
    f = font(F_MONO_B, 9 * s)
    tw = dr.textlength(day, font=f)
    dr.text((x0 + size / 2 - tw / 2, y0 + 2 * s), day, font=f, fill=WHITE)


def rotated_text(img, text, f, angle, center, fill):
    """Draw text rotated by `angle` degrees, centered at `center`."""
    tmp = Image.new("RGBA", (int(img.size[0] * 1.5), int(f.size * 1.6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    tw = d.textlength(text, font=f)
    d.text(((tmp.size[0] - tw) / 2, 0), text, font=f, fill=fill + (255,))
    tmp = tmp.crop(tmp.getbbox())
    tmp = tmp.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.paste(tmp, (int(center[0] - tmp.size[0] / 2), int(center[1] - tmp.size[1] / 2)), tmp)


# ------------------------------------------------------------ 1. NEW MOON
def image1_new_moon():
    """Constructivist poster. The black disc is the unlit moon; the red wedge is
    tonight's dark sky driving into it. Lissitzky's grammar, my subject."""
    s = SS
    img, dr = canvas(WHITE)

    cx, cy = 262 * s, 138 * s
    R = 96 * s

    # thin diagonal rulings behind everything
    for k in range(-6, 8):
        x0 = k * 70 * s
        dr.line([x0, H * s, x0 + H * s * 1.2, 0], fill=BLACK, width=1 * s)

    # a white quiet zone so the rulings don't fight the type
    dr.rectangle([0, 0, W * s, 40 * s], fill=WHITE)
    dr.rectangle([0, H * s - 36 * s, W * s, H * s], fill=WHITE)

    # black disc (the new moon)
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)
    # a white ring floating across the disc's edge — the invisible lit limb
    r2 = 44 * s
    ox, oy = cx + 62 * s, cy - 58 * s
    dr.ellipse([ox - r2, oy - r2, ox + r2, oy + r2], outline=WHITE, width=3 * s)
    dr.ellipse([ox - r2, oy - r2, ox + r2, oy + r2], outline=BLACK, width=1 * s)

    # red wedge from bottom-left piercing the disc
    tip = (cx - 6 * s, cy + 4 * s)
    base_mid = (-20 * s, 300 * s)
    ang = math.atan2(base_mid[1] - tip[1], base_mid[0] - tip[0])
    half = 46 * s
    nx, ny = -math.sin(ang), math.cos(ang)
    p1 = (base_mid[0] + nx * half, base_mid[1] + ny * half)
    p2 = (base_mid[0] - nx * half, base_mid[1] - ny * half)
    dr.polygon([tip, p1, p2], fill=RED)

    # a small black bar and a red square, punctuation in the suprematist manner
    dr.rectangle([300 * s, 236 * s, 384 * s, 246 * s], fill=BLACK)
    dr.rectangle([318 * s, 60 * s, 334 * s, 76 * s], fill=RED)
    dr.rectangle([40 * s, 60 * s, 56 * s, 76 * s], fill=BLACK)

    # type — the title runs straight across the disc, black on white, white on black
    title = "NEW MOON"
    ft = font(F_FREE_SANS_B, 42 * s)
    tmask = Image.new("L", img.size, 0)
    tmp = Image.new("L", (int(W * s * 1.5), int(ft.size * 1.6)), 0)
    d = ImageDraw.Draw(tmp)
    tw = d.textlength(title, font=ft)
    d.text(((tmp.size[0] - tw) / 2, 0), title, font=ft, fill=255)
    tmp = tmp.crop(tmp.getbbox()).rotate(22, resample=Image.BICUBIC, expand=True)
    tc = (150 * s, 138 * s)
    tmask.paste(tmp, (int(tc[0] - tmp.size[0] / 2), int(tc[1] - tmp.size[1] / 2)))
    dmask = Image.new("L", img.size, 0)
    ImageDraw.Draw(dmask).ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
    from PIL import ImageChops
    on_disc = ImageChops.multiply(tmask, dmask)
    off_disc = ImageChops.subtract(tmask, on_disc)
    img.paste(BLACK, (0, 0), off_disc)
    img.paste(WHITE, (0, 0), on_disc)
    rotated_text(img, "the darkest night of the month", font(F_SANS_B, 11 * s), 22,
                 (150 * s, 200 * s), WHITE)
    f = font(F_MONO_B, 11 * s)
    dr.text((14 * s, 12 * s), "11 · IX · 2026   03:27 UTC", font=f, fill=BLACK)
    dr.text((14 * s, H * s - 26 * s), "no moon · no glare · milky way overhead by 22:00",
            font=font(F_MONO, 10 * s), fill=BLACK)
    # red rule under the title line
    dr.rectangle([14 * s, 30 * s, 226 * s, 33 * s], fill=RED)
    seal(dr, s, corner="br")
    return finalize(img)


# ------------------------------------------------------------ 2. MONCHŌ (kamon sampler)
def circle(dr, c, r, **kw):
    dr.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], **kw)


def polar(c, r, deg):
    a = math.radians(deg)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def maru(dr, c, R, s, color=BLACK):
    """The enclosing ring (maru) — most crests sit inside one."""
    circle(dr, c, R, outline=color, width=int(R * 0.09))


def mon_mitsudomoe(dr, c, R, s, color=BLACK):
    """Three comma shapes chasing each other. Built from: a head circle and a
    tail that follows the outer circle and tapers to nothing."""
    Ri = R * 0.80
    for k in range(3):
        a0 = k * 120 + 90
        pts = []
        # outer edge: along the boundary circle
        for t in range(0, 61):
            u = t / 60
            pts.append(polar(c, Ri, a0 + u * 150))
        # inner edge back: radius shrinks then swings into the head
        for t in range(60, -1, -1):
            u = t / 60
            r = Ri * (1 - 0.62 * (1 - u) ** 1.2)
            pts.append(polar(c, r, a0 + u * 150))
        dr.polygon(pts, fill=color)
        head_c = polar(c, Ri * 0.46, a0 + 8)
        circle(dr, head_c, Ri * 0.34, fill=color)


def mon_ume(dr, c, R, s, color=BLACK):
    """Plum blossom: five round petals = five circles, a center ring, five stamens."""
    Ri = R * 0.82
    pr = Ri * 0.40
    for k in range(5):
        p = polar(c, Ri - pr, -90 + k * 72)
        circle(dr, p, pr, fill=color)
    circle(dr, c, Ri * 0.30, fill=WHITE)
    circle(dr, c, Ri * 0.19, fill=color)
    for k in range(5):
        p = polar(c, Ri * 0.44, -90 + k * 72)
        circle(dr, p, Ri * 0.055, fill=WHITE)


def mon_mitsu_uroko(dr, c, R, s, color=BLACK):
    """Three scales (Hōjō clan): one triangle above two, all pointing up."""
    Ri = R * 0.78
    h = Ri * 0.82
    w = h * 1.12
    top = c[1] - h * 0.85
    def tri(cx, cy):
        dr.polygon([(cx, cy - h / 2), (cx - w / 2, cy + h / 2), (cx + w / 2, cy + h / 2)], fill=color)
    tri(c[0], top + h / 2)
    tri(c[0] - w / 2, top + h / 2 + h)
    tri(c[0] + w / 2, top + h / 2 + h)


def mon_kikyo(dr, c, R, s, color=BLACK):
    """Bellflower: five pointed petals, each a vesica (two circle arcs)."""
    Ri = R * 0.82
    for k in range(5):
        a = -90 + k * 72
        tip = polar(c, Ri, a)
        base = polar(c, Ri * 0.12, a)
        pts = []
        # arc bulge on either side of the axis
        for t in range(0, 41):
            u = t / 40
            x = base[0] + (tip[0] - base[0]) * u
            y = base[1] + (tip[1] - base[1]) * u
            bulge = math.sin(u * math.pi) * Ri * 0.30
            nx, ny = -math.sin(math.radians(a)), math.cos(math.radians(a))
            pts.append((x + nx * bulge, y + ny * bulge))
        for t in range(40, -1, -1):
            u = t / 40
            x = base[0] + (tip[0] - base[0]) * u
            y = base[1] + (tip[1] - base[1]) * u
            bulge = math.sin(u * math.pi) * Ri * 0.30
            nx, ny = -math.sin(math.radians(a)), math.cos(math.radians(a))
            pts.append((x - nx * bulge, y - ny * bulge))
        dr.polygon(pts, fill=color)
    circle(dr, c, Ri * 0.13, fill=color)
    circle(dr, c, Ri * 0.07, fill=WHITE)


def mon_tsuki_ni_hoshi(dr, c, R, s, color=BLACK):
    """Moon with stars: a crescent (two circles) and three small discs."""
    Ri = R * 0.80
    circle(dr, c, Ri, fill=color)
    circle(dr, (c[0] + Ri * 0.38, c[1] - Ri * 0.10), Ri * 0.86, fill=WHITE)
    for k, (dx, dy) in enumerate([(0.30, -0.42), (0.55, 0.05), (0.30, 0.50)]):
        circle(dr, (c[0] + Ri * dx, c[1] + Ri * dy), Ri * 0.13, fill=color)


def mon_kuginuki(dr, c, R, s, color=BLACK):
    """Nail-puller: a square ring with a square hole, set on the diagonal."""
    Ri = R * 0.78
    a = Ri * 0.86
    pts = [polar(c, a, 45 + 90 * k) for k in range(4)]
    dr.polygon(pts, fill=color)
    pts = [polar(c, a * 0.58, 45 + 90 * k) for k in range(4)]
    dr.polygon(pts, fill=WHITE)
    pts = [polar(c, a * 0.24, 45 + 90 * k) for k in range(4)]
    dr.polygon(pts, fill=color)


def image2_moncho():
    s = SS
    img, dr = canvas(WHITE)
    # hero: red mitsudomoe in a black ring
    hc = (118 * s, 138 * s)
    HR = 92 * s
    maru(dr, hc, HR, s, BLACK)
    mon_mitsudomoe(dr, hc, HR * 0.96, s, RED)

    # four smaller crests, in a 2x2 block on the right
    small = [
        (mon_ume, "梅", "ume"),
        (mon_mitsu_uroko, "三つ鱗", "mitsu-uroko"),
        (mon_kikyo, "桔梗", "kikyō"),
        (mon_tsuki_ni_hoshi, "月に星", "tsuki ni hoshi"),
    ]
    sr = 38 * s
    fj = font(F_JP, 10 * s)
    fr = font(F_MONO, 8 * s)
    for i, (fn, kanji, romaji) in enumerate(small):
        col, row = i % 2, i // 2
        c = ((262 + col * 98) * s, (66 + row * 112) * s)
        maru(dr, c, sr, s, BLACK)
        fn(dr, c, sr * 0.96, s, BLACK)
        tw = dr.textlength(kanji, font=fj)
        dr.text((c[0] - tw / 2, c[1] + sr + 5 * s), kanji, font=fj, fill=BLACK)
        tw = dr.textlength(romaji, font=fr)
        dr.text((c[0] - tw / 2, c[1] + sr + 17 * s), romaji, font=fr, fill=BLACK)

    # hero labels
    fj2 = font(F_JP, 16 * s)
    dr.text((14 * s, 248 * s), "三つ巴", font=fj2, fill=BLACK)
    dr.text((72 * s, 252 * s), "mitsudomoe", font=font(F_MONO_B, 10 * s), fill=BLACK)
    dr.text((14 * s, 270 * s), "紋帳 · a sampler of crests · circles & lines only",
            font=font(F_JP, 9 * s), fill=BLACK)
    # thin frame
    dr.rectangle([6 * s, 6 * s, W * s - 6 * s, H * s - 6 * s], outline=BLACK, width=1 * s)
    seal(dr, s, corner="br")
    return finalize(img)


# ------------------------------------------------------------ 3. EVENT 10.09 (LHC)
def image3_event_display():
    """A transverse-view collision event display, the way ATLAS/CMS draw them:
    curved tracks in the solenoid field, calorimeter towers around the rim,
    two jets back-to-back and a pair of muons escaping."""
    rng = random.Random(20080910)
    s = SS
    img, dr = canvas(BLACK)
    cx, cy = 186 * s, 148 * s
    R_trk = 76 * s
    R_ecal0, R_ecal1 = 84 * s, 94 * s
    R_hcal0, R_hcal1 = 98 * s, 114 * s

    # detector layers
    circle(dr, (cx, cy), R_trk, outline=WHITE, width=1 * s)
    for r in (24, 40, 56):
        circle(dr, (cx, cy), r * s, outline=(90, 90, 90), width=1 * s)
    circle(dr, (cx, cy), R_ecal0, outline=WHITE, width=1 * s)
    circle(dr, (cx, cy), R_ecal1, outline=WHITE, width=1 * s)
    circle(dr, (cx, cy), R_hcal1, outline=WHITE, width=2 * s)
    # calorimeter segmentation ticks
    for k in range(72):
        a = k * 5
        p0 = polar((cx, cy), R_ecal0, a)
        p1 = polar((cx, cy), R_ecal1, a)
        dr.line([p0, p1], fill=(120, 120, 120), width=1 * s)
    for k in range(36):
        a = k * 10
        p0 = polar((cx, cy), R_ecal1, a)
        p1 = polar((cx, cy), R_hcal1, a)
        dr.line([p0, p1], fill=(120, 120, 120), width=1 * s)

    # two jets (back to back, slightly unbalanced) + a few soft tracks
    jet_a = rng.uniform(0, 360)
    jet_b = jet_a + 180 + rng.uniform(-18, 18)

    def track(phi_deg, pt, charge, color=WHITE, width=2, rmax=R_trk):
        """Charged track from the origin: a circle arc of radius ∝ pT."""
        rad = pt * 26 * s  # curvature radius
        phi = math.radians(phi_deg)
        # circle center perpendicular to the initial direction
        ccx = cx + charge * rad * -math.sin(phi)
        ccy = cy + charge * rad * math.cos(phi)
        pts = []
        for i in range(0, 400):
            t = i / 400 * math.pi * 1.2
            ang = math.atan2(cy - ccy, cx - ccx) + charge * t
            x = ccx + rad * math.cos(ang)
            y = ccy + rad * math.sin(ang)
            if math.hypot(x - cx, y - cy) > rmax:
                break
            pts.append((x, y))
        if len(pts) > 1:
            dr.line(pts, fill=color, width=width * s)
        return pts

    for jet, n in ((jet_a, 9), (jet_b, 7)):
        for _ in range(n):
            phi = rng.gauss(jet, 9)
            pt = rng.choice([1.5, 2, 3, 4, 6, 9, 14])
            track(phi, pt, rng.choice([-1, 1]))
    for _ in range(11):
        track(rng.uniform(0, 360), rng.choice([0.6, 0.9, 1.3, 2]), rng.choice([-1, 1]),
              color=(170, 170, 170), width=1)

    # calorimeter towers: energy deposits as radial bars (red) on the rim
    def towers(center_deg, n, spread, scale):
        for _ in range(n):
            a = rng.gauss(center_deg, spread)
            e = abs(rng.gauss(0, 1)) * scale + 0.15
            k = int(a // 5) * 5 + 2.5
            r1 = R_ecal0 + min(1.0, e) * (R_hcal1 - R_ecal0)
            p0 = polar((cx, cy), R_ecal0 + 1 * s, k)
            p1 = polar((cx, cy), r1, k)
            dr.line([p0, p1], fill=RED, width=4 * s)
    towers(jet_a, 10, 8, 0.7)
    towers(jet_b, 8, 8, 0.55)
    for _ in range(9):
        towers(rng.uniform(0, 360), 1, 1, 0.18)

    # two muons: nearly straight, red, punching out through everything
    mu = rng.uniform(0, 360)
    track(mu, 40, 1, color=RED, width=2, rmax=R_hcal1 + 14 * s)
    track(mu + 150 + rng.uniform(-20, 20), 32, -1, color=RED, width=2, rmax=R_hcal1 + 14 * s)

    # beam spot
    circle(dr, (cx, cy), 3 * s, fill=WHITE)

    # ring schematic, top-left: the 27 km ring with its four experiments
    rc, rr = (40 * s, 44 * s), 20 * s
    circle(dr, rc, rr, outline=WHITE, width=1 * s)
    for name, ang in (("ATLAS", 90), ("ALICE", 45), ("CMS", 270), ("LHCb", 135)):
        p = polar(rc, rr, ang)
        circle(dr, p, 3 * s, fill=RED if name in ("ATLAS", "CMS") else WHITE)
    fs = font(F_MONO, 8 * s)
    dr.text((rc[0] - 12 * s, rc[1] + rr + 4 * s), "ATLAS", font=fs, fill=WHITE)
    dr.text((rc[0] - 7 * s, rc[1] - rr - 12 * s), "CMS", font=fs, fill=WHITE)
    dr.text((rc[0] + rr - 2 * s, rc[1] + 14 * s), "ALICE", font=fs, fill=WHITE)
    dr.text((rc[0] - rr - 22 * s, rc[1] + 14 * s), "LHCb", font=fs, fill=WHITE)

    # text
    x = 312 * s
    fb = font(F_MONO_B, 12 * s)
    dr.text((x, 10 * s), "LHC", font=font(F_FREE_SANS_B, 26 * s), fill=WHITE)
    dr.text((x, 42 * s), "first", font=fb, fill=WHITE)
    dr.text((x, 56 * s), "beam", font=fb, fill=WHITE)
    dr.text((x, 74 * s), "10.09.08", font=fb, fill=RED)
    dr.text((x, 90 * s), "10:28 CEST", font=font(F_MONO, 8 * s), fill=WHITE)
    dr.text((x, 102 * s), "27 km round", font=font(F_MONO, 8 * s), fill=WHITE)
    fm = font(F_MONO, 9 * s)
    dr.text((12 * s, H * s - 34 * s), "18 years ago today the first proton bunch", font=fm, fill=WHITE)
    dr.text((12 * s, H * s - 22 * s), "went all the way round.", font=fm, fill=WHITE)
    dr.text((x, H * s - 22 * s), "13.6 TeV", font=font(F_MONO_B, 9 * s), fill=RED)
    seal(dr, s, corner="tr")
    return finalize(img)


# ------------------------------------------------------------ 4. DRAFT 0910 (weaving)
def image4_weaving_draft():
    """Anni Albers' draft notation: threading across the top, tie-up in the corner,
    treadling down the side, and the drawdown as actual interlaced threads —
    black warp, red weft, white light between them. Drawn at 1x, pixel-exact."""
    rng = random.Random(910)
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    SHAFTS = 4
    NW = 31  # warp ends
    NF = 22  # weft picks
    cell = 8

    # threading: point twill with seeded run lengths (1-2-3-4-3-2-1 ... with
    # the turning points wandering), which weaves as diamonds and chevrons
    threading = []
    shaft, step = 0, 1
    while len(threading) < NW:
        threading.append(shaft)
        nxt = shaft + step
        if nxt < 0 or nxt >= SHAFTS:
            step = -step
            nxt = shaft + step
        elif rng.random() < 0.12 and shaft in (1, 2):
            step = -step
            nxt = shaft + step
        shaft = nxt
    # tie-up: each treadle lifts two adjacent shafts (balanced 2/2 twill)
    tieup = []
    for t in range(SHAFTS):
        row = [0] * SHAFTS
        row[t] = 1
        row[(t + 1) % SHAFTS] = 1
        tieup.append(row)
    # treadling: straight twill that reverses direction once — chevrons
    treadling = []
    t, step = 0, 1
    turn = rng.randint(8, 13)
    while len(treadling) < NF:
        treadling.append(t)
        if len(treadling) == turn:
            step = -step
        t = (t + step) % SHAFTS

    # layout
    x_dd = 30
    y_dd = 84
    dd_w, dd_h = NW * cell, NF * cell        # 248 x 176
    x_side = x_dd + dd_w + 10                 # tie-up + treadling column
    y_top = y_dd - SHAFTS * cell - 10         # threading rows

    # drawdown as woven threads: whichever thread is on top fills the cell,
    # with a hairline of white along its own edges so the direction reads
    for j in range(NF):
        for i in range(NW):
            x0 = x_dd + i * cell
            y0 = y_dd + j * cell
            warp_up = tieup[treadling[j]][threading[i]] == 1
            if warp_up:
                dr.rectangle([x0 + 1, y0, x0 + cell - 2, y0 + cell - 1], fill=BLACK)
            else:
                dr.rectangle([x0, y0 + 1, x0 + cell - 1, y0 + cell - 2], fill=RED)
    # threading grid
    for i in range(NW):
        for sh in range(SHAFTS):
            x0 = x_dd + i * cell
            y0 = y_top + (SHAFTS - 1 - sh) * cell
            dr.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], outline=(170, 170, 170))
            if threading[i] == sh:
                dr.rectangle([x0 + 1, y0 + 1, x0 + cell - 2, y0 + cell - 2], fill=BLACK)
    # tie-up grid (treadles across, shafts down)
    for t in range(SHAFTS):
        for sh in range(SHAFTS):
            x0 = x_side + t * cell
            y0 = y_top + (SHAFTS - 1 - sh) * cell
            dr.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], outline=(170, 170, 170))
            if tieup[t][sh]:
                dr.rectangle([x0 + 1, y0 + 1, x0 + cell - 2, y0 + cell - 2], fill=RED)
    # treadling grid
    for j in range(NF):
        for t in range(SHAFTS):
            x0 = x_side + t * cell
            y0 = y_dd + j * cell
            dr.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], outline=(170, 170, 170))
            if treadling[j] == t:
                dr.rectangle([x0 + 1, y0 + 1, x0 + cell - 2, y0 + cell - 2], fill=BLACK)

    # labels
    fm = font(F_MONO, 9)
    fb = font(F_MONO_B, 11)
    dr.text((x_dd, 12), "DRAFT No. 0910", font=fb, fill=BLACK)
    dr.text((x_dd, 27), "4 shafts · 2/2 twill · point threading · warp black · weft red",
            font=font(F_MONO, 8), fill=BLACK)
    dr.text((x_side + 34, y_top + 10), "tie-up", font=font(F_MONO, 8), fill=RED)
    dr.text((x_side + 34, y_dd + 2), "treadling", font=font(F_MONO, 8), fill=BLACK)
    rotated_text(img, "threading", font(F_MONO, 8), 90, (x_dd - 12, y_top + 16), BLACK)
    rotated_text(img, "drawdown", font(F_MONO, 8), 90, (x_dd - 12, y_dd + dd_h / 2), BLACK)
    dr.text((x_dd, H - 24), "draft notation after Anni Albers, On Weaving (1965)",
            font=font(F_MONO, 8), fill=BLACK)
    # seal at 1x
    seal(dr, 1, corner="br")
    return snap(img)


# ------------------------------------------------------------ 5. OCCULTATION (Moon hides Venus)
def image5_occultation():
    s = SS
    img, dr = canvas(BLACK)
    cx, cy = 148 * s, 142 * s
    R = 100 * s

    # the unlit disc: a faint dotted limb (earthshine memory)
    for k in range(0, 360, 4):
        p = polar((cx, cy), R, k)
        circle(dr, p, 1.0 * s, fill=(110, 110, 110))

    # 12%-lit waxing crescent, lit on the right (evening side)
    circle(dr, (cx, cy), R, fill=WHITE)
    dr.rectangle([cx - R - 2, cy - R - 2, cx, cy + R + 2], fill=BLACK)
    k = 0.12
    b = R * (1 - 2 * k)  # terminator semi-minor axis
    dr.ellipse([cx - b, cy - R, cx + b, cy + R], fill=BLACK)
    # re-dot the dark limb over the black fill so the whole moon is implied
    for kk in range(100, 260, 4):
        p = polar((cx, cy), R, kk)
        circle(dr, p, 1.0 * s, fill=(110, 110, 110))

    # Venus: a red planet with four spikes, just clear of the dark limb
    vx, vy = cx - R * 0.985 - 6 * s, cy - R * 0.10
    for ang, ln in ((0, 26), (90, 26), (180, 26), (270, 26)):
        p = polar((vx, vy), ln * s, ang)
        dr.line([(vx, vy), p], fill=RED, width=2 * s)
    circle(dr, (vx, vy), 9 * s, fill=RED)
    circle(dr, (vx, vy), 3 * s, fill=WHITE)

    # text block, right side
    x = 268 * s
    dr.text((x, 40 * s), "MON", font=font(F_FREE_SANS_B, 20 * s), fill=WHITE)
    dr.text((x, 62 * s), "14 SEP", font=font(F_FREE_SANS_B, 20 * s), fill=RED)
    dr.rectangle([x, 90 * s, x + 118 * s, 91 * s], fill=WHITE)
    dr.text((x, 98 * s), "the Moon hides", font=font(F_SANS_B, 11 * s), fill=WHITE)
    dr.text((x, 112 * s), "VENUS", font=font(F_FREE_SANS_B, 24 * s), fill=WHITE)
    dr.rectangle([x, 144 * s, x + 118 * s, 145 * s], fill=WHITE)
    fm = font(F_MONO, 9 * s)
    dr.text((x, 152 * s), "in daylight.", font=fm, fill=WHITE)
    dr.text((x, 166 * s), "reappears", font=fm, fill=WHITE)
    dr.text((x, 178 * s), "11:30 BST", font=font(F_MONO_B, 11 * s), fill=RED)
    dr.text((x, 196 * s), "3° up · SE", font=fm, fill=WHITE)
    dr.text((x, 208 * s), "mag −4.4", font=fm, fill=WHITE)
    dr.text((x, 226 * s), "binoculars;", font=fm, fill=WHITE)
    dr.text((x, 238 * s), "find the Moon", font=fm, fill=WHITE)
    dr.text((x, 250 * s), "first.", font=fm, fill=WHITE)

    # phase strip along the bottom: tonight (new) → Monday (12%)
    fs = font(F_MONO, 7 * s)
    labels = ["THU 10", "FRI 11", "SAT 12", "SUN 13", "MON 14"]
    fracs = [0.00, 0.01, 0.03, 0.07, 0.12]
    for i, (lab, fr) in enumerate(zip(labels, fracs)):
        mx, my, mr = (28 + i * 44) * s, 274 * s, 8 * s
        circle(dr, (mx, my), mr, outline=(120, 120, 120), width=1 * s)
        if fr > 0.005:
            circle(dr, (mx, my), mr, fill=WHITE)
            dr.rectangle([mx - mr - 1, my - mr - 1, mx, my + mr + 1], fill=BLACK)
            bb = mr * (1 - 2 * fr)
            dr.ellipse([mx - bb, my - mr, mx + bb, my + mr], fill=BLACK)
        tw = dr.textlength(lab, font=fs)
        dr.text((mx - tw / 2, my + mr + 4 * s), lab, font=fs, fill=RED if i == 4 else WHITE)
    dr.text((12 * s, 12 * s), "OCCULTATION", font=font(F_MONO_B, 11 * s), fill=WHITE)
    dr.text((12 * s, 26 * s), "as seen from the UK", font=fs, fill=WHITE)
    seal(dr, s, corner="tr")
    return finalize(img)


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", ".."))
    makers = [image1_new_moon, image2_moncho, image3_event_display,
              image4_weaving_draft, image5_occultation]
    for i, fn in enumerate(makers, 1):
        im = fn()
        assert im.size == (W, H)
        assert max(im.tobytes()) <= 2
        im.save(os.path.join(here, f"{i}.png"), optimize=True)
        im.save(os.path.join(root, "images", f"{i}.png"), optimize=True)
        print("wrote", i, fn.__name__)


if __name__ == "__main__":
    main()
