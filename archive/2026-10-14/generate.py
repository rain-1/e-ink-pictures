#!/usr/bin/env python3
"""2026-10-14 — five pictures for a 400x300 black/white/red e-ink panel.
Theme: things that cross a gap and arrive later.
1. Isti mirant stella — Hastings, 14 Oct 1066. The tapestry's comet in stem stitch and laid work;
   it was Halley's, and its dust is next week's Orionids.
2. Mach 1.06 — Yeager, 14 Oct 1947. Wavefronts from a source just faster than sound; red = the boom.
3. (untitled) Chorégraphie — Beauchamp–Feuillet floor tracks for two dancers; red = the mirror. No text.
4. Puzzle No. 4 — Schirra's card from Apollo 7's first live TV (14 Oct 1968), in pigpen cipher.
5. Venation — a leaf grown by space colonisation; red = one drop's way home.
Run: python3 generate.py <outdir>"""
import math, random, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
PAL = [255, 255, 255, 0, 0, 0, 255, 0, 0] + [0] * (256 * 3 - 9)
FD = "/usr/share/fonts/opentype/inter/"
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."


def font(name, size):
    return ImageFont.truetype(DJ if name == "dj" else FD + name, size)


def draw1(im):
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    return d


def snap(im):
    a = np.asarray(im.convert("RGB")).astype(int)
    cols = np.array([WHITE, BLACK, RED])
    idx = ((a[:, :, None, :] - cols[None, None]) ** 2).sum(-1).argmin(-1)
    return Image.fromarray(cols[idx].astype(np.uint8), "RGB")


def down(big):
    return snap(big.resize((W, H), Image.LANCZOS))


def save(im, name):
    a = np.asarray(im.convert("RGB")).astype(int)
    cols = np.array([WHITE, BLACK, RED])
    idx = ((a[:, :, None, :] - cols[None, None]) ** 2).sum(-1).argmin(-1).astype(np.uint8)
    p = Image.fromarray(idx, "P")
    p.putpalette(PAL)
    p.save(os.path.join(OUT, name), optimize=True)


def mark(d, x, y, fill=RED):
    d.rectangle([x, y, x + 3, y + 3], fill=fill)


def text_lines(d, x, y, lines, f, lead=13, fill=BLACK, maxw=None):
    for ln in lines:
        if ln == "":
            y += 6
            continue
        if maxw:
            assert d.textlength(ln, font=f) <= maxw, (ln, d.textlength(ln, font=f))
        d.text((x, y), ln, font=f, fill=fill)
        y += lead
    return y


def resample(pts, step):
    """Polyline -> points spaced `step` apart along its length."""
    pts = np.asarray(pts, float)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    t = np.arange(0, s[-1], step)
    return np.stack([np.interp(t, s, pts[:, 0]), np.interp(t, s, pts[:, 1])], 1)


# ------------------------------------------------------------- 1. Isti mirant stella
def stem_stitch(d, pts, S, fill, L=4.6, w=1.15):
    """Stem stitch: short slanted stitches, each overlapping the last by half."""
    pts = resample(pts, L * S / 2)
    for i in range(len(pts) - 2):
        a, b = pts[i], pts[i + 2]
        t = b - a
        n = np.array([-t[1], t[0]]) / (np.hypot(*t) + 1e-9)
        p = a + n * 0.8 * S
        q = b - n * 0.8 * S
        d.line([tuple(p), tuple(q)], fill=fill, width=max(1, int(w * S)))


def laid_fill(d, poly, S, fill, gap=2.2, couch=7, ang=0.0):
    """Laid work: parallel threads across the shape, held by couching bars at right angles."""
    mask = Image.new("L", d.im.size, 0)
    ImageDraw.Draw(mask).polygon([tuple(p) for p in poly], fill=255)
    layer = Image.new("L", d.im.size, 0)
    ld = ImageDraw.Draw(layer)
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    R = max(max(xs) - min(xs), max(ys) - min(ys))
    ca, sa = math.cos(ang), math.sin(ang)
    k = -R
    while k < R:
        p0 = (cx - R * ca - k * sa, cy - R * sa + k * ca)
        p1 = (cx + R * ca - k * sa, cy + R * sa + k * ca)
        ld.line([p0, p1], fill=255, width=int(1.3 * S))
        k += gap * S
    k = -R
    while k < R:  # couching bars, perpendicular
        p0 = (cx - k * ca - R * sa * -1 * 0 + R * sa, cy - k * sa - R * ca)
        p0 = (cx + k * ca + R * sa, cy + k * sa - R * ca)
        p1 = (cx + k * ca - R * sa, cy + k * sa + R * ca)
        ld.line([p0, p1], fill=255, width=int(0.9 * S))
        k += couch * S
    from PIL import ImageChops
    layer = ImageChops.multiply(layer, mask)
    d.bitmap((0, 0), layer, fill=fill)


def figure(d, x, y, S, h, lean, arm):
    """A marvelling man: tunic, head, one arm pointing up at the star."""
    hw = h * 0.22
    body = [(x - hw, y), (x - hw * 0.6, y - h * 0.62), (x + hw * 0.6, y - h * 0.62), (x + hw, y)]
    body = [((px + lean * (y - py) * 0.15) * S, py * S) for px, py in body]
    stem_stitch(d, body + [body[0]], S, BLACK)
    # legs
    for dx in (-hw * 0.45, hw * 0.45):
        stem_stitch(d, [((x + dx) * S, y * S), ((x + dx * 1.3) * S, (y + h * 0.28) * S)], S, BLACK)
    hx, hy = x + lean * h * 0.62 * 0.15, y - h * 0.62 - h * 0.13
    ring = [((hx + h * 0.1 * math.cos(t)) * S, (hy + h * 0.12 * math.sin(t)) * S)
            for t in np.linspace(0, 2 * math.pi, 18)]
    stem_stitch(d, ring, S, BLACK)
    sx, sy = hx + 0.5 * hw * (1 if arm > 0 else -1), y - h * 0.55
    ex = sx + arm * h * 0.25
    stem_stitch(d, [(sx * S, sy * S), ((sx + arm * h * 0.12) * S, (sy - h * 0.2) * S),
                    (ex * S, (sy - h * 0.42) * S)], S, BLACK)


def tapestry():
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    top, bot = 22, 236
    # border strips with diagonal bars, like the tapestry's margins
    for y0, y1 in ((2, top - 2), (bot + 2, bot + 20)):
        stem_stitch(d, [(4 * S, y0 * S), (396 * S, y0 * S)], S, BLACK)
        stem_stitch(d, [(4 * S, y1 * S), (396 * S, y1 * S)], S, BLACK)
        for i, x in enumerate(range(12, 392, 24)):
            stem_stitch(d, [((x) * S, (y1 - 2) * S), ((x + 12) * S, (y0 + 2) * S)], S, BLACK)
    # the star: a domed head with a crown of rays, and a forked streaming tail
    cx, cy = 232, 86
    head = [((cx + 17 * math.cos(t)) * S, (cy + 14 * math.sin(t)) * S)
            for t in np.linspace(math.pi * 0.5, math.pi * 2.5, 40)]
    laid_fill(d, head, S, RED, ang=0.35)
    stem_stitch(d, head + [head[0]], S, BLACK)
    for k in range(9):  # rays from the leading side
        a = math.radians(-70 + k * 20)
        p0 = (cx + 18 * math.cos(a), cy + 15 * math.sin(a))
        p1 = (cx + 27 * math.cos(a), cy + 24 * math.sin(a))
        stem_stitch(d, [(p0[0] * S, p0[1] * S), (p1[0] * S, p1[1] * S)], S, BLACK)
    # tail: five tongues streaming left, each a laid red band edged in stem stitch
    for k, (dy, ln) in enumerate([(-11, 70), (-5, 96), (0, 118), (5, 92), (10, 66)]):
        pts_u, pts_l = [], []
        for t in np.linspace(0, 1, 30):
            x = cx - 14 - t * ln
            yc = cy + dy * (0.4 + 1.6 * t) + 3 * math.sin(t * 5 + k)
            half = 2.6 * (1 - t) + 0.5
            pts_u.append((x * S, (yc - half) * S)); pts_l.append((x * S, (yc + half) * S))
        poly = pts_u + pts_l[::-1]
        laid_fill(d, poly, S, RED, gap=2.0, couch=6, ang=0.0)
        stem_stitch(d, poly + [poly[0]], S, BLACK)
    # the marvelling men, lower left, looking up
    for i, (x, h, lean, arm) in enumerate([(40, 74, 1, 1), (78, 70, 0.5, 1),
                                           (116, 76, 1, 1), (152, 66, -0.5, -1), (292, 74, -1, -1)]):
        figure(d, x, 196, S, h, lean, arm)
    # ground line
    stem_stitch(d, [(20 * S, 222 * S), (380 * S, 222 * S)], S, BLACK)
    # Harold's hall on the right: arcades
    for i in range(3):
        x0 = 322 + i * 20
        stem_stitch(d, [(x0 * S, 222 * S), (x0 * S, 160 * S)], S, BLACK)
        arc = [((x0 + 10 - 10 * math.cos(t)) * S, (160 - 10 * math.sin(t)) * S) for t in np.linspace(0, math.pi, 12)]
        stem_stitch(d, arc, S, BLACK)
    stem_stitch(d, [(316 * S, 150 * S), (388 * S, 150 * S), (352 * S, 124 * S), (316 * S, 150 * S)], S, BLACK)
    im = down(big)
    dd = draw1(im)
    f = font("Inter-Bold.otf", 14)
    s = "ISTI · MIRANT · STELLA"
    dd.text((18, top + 6), s, font=f, fill=BLACK)
    fb = font("Inter-Bold.otf", 11)
    fr = font("Inter-Regular.otf", 10)
    dd.text((10, 260), "HASTINGS  ·  14 OCTOBER  ·  1066", font=fb, fill=BLACK)
    text_lines(dd, 10, 274, ["The star these men marvel at that spring was Halley's comet.",
                             "Its dust still arrives: the Orionids peak 21–22 October."], fr, 12, maxw=380)
    mark(dd, 392, 292)
    return im


# ------------------------------------------------------------- 2. Mach 1.06
def mach():
    S = 4
    M = 1.06
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    ay = 118          # flight line
    ax = 318          # where the aircraft is now
    c = 13.0          # px per tick of sound travel
    n = 16
    for k in range(1, n + 1):
        r = c * k
        x = ax - M * r
        d.ellipse([(x - r) * S, (ay - r) * S, (x + r) * S, (ay + r) * S], outline=BLACK, width=int(1.1 * S))
        d.ellipse([(x - 1.5) * S, (ay - 1.5) * S, (x + 1.5) * S, (ay + 1.5) * S], fill=BLACK)
    mu = math.asin(1 / M)
    L = 400
    for sgn in (-1, 1):  # the envelope: the boom
        ex = ax - L * math.cos(math.pi / 2 - mu) * 0 - L * math.cos(mu)
        ey = ay + sgn * L * math.sin(mu)
        d.line([(ax * S, ay * S), (ex * S, ey * S)], fill=RED, width=int(2.4 * S))
    # the X-1: a bullet with stubby wings
    body = [(ax + 2, ay), (ax - 3, ay - 2.2), (ax - 17, ay - 2.2), (ax - 19, ay), (ax - 17, ay + 2.2), (ax - 3, ay + 2.2)]
    d.polygon([(x * S, y * S) for x, y in body], fill=BLACK)
    d.polygon([(x * S, y * S) for x, y in [(ax - 8, ay), (ax - 13, ay - 7), (ax - 15, ay - 7), (ax - 13, ay)]], fill=BLACK)
    d.line([(ax - 18) * S, ay * S, (ax - 21) * S, (ay - 5) * S], fill=BLACK, width=2 * S)
    im = down(big)
    dd = draw1(im)
    # clear a white panel for text, bottom right
    dd.rectangle([236, 196, 400, 300], fill=WHITE)
    dd.line([236, 196, 236, 300], fill=BLACK)
    fbig = font("InterDisplay-Black.otf", 34)
    dd.text((246, 200), "M 1.06", font=fbig, fill=BLACK)
    fr = font("Inter-Regular.otf", 10)
    fb = font("Inter-Bold.otf", 10)
    text_lines(dd, 246, 242, ["Yeager, Bell X-1, 14 Oct 1947,",
                              "~43,000 ft over the Mojave."], fr, 12, maxw=150)
    text_lines(dd, 246, 270, ["sin μ = 1/M  →  μ = 70.6°"], fb, 12, fill=RED, maxw=150)
    text_lines(dd, 246, 283, ["Barely past sound: a wall."], fr, 12, maxw=152)
    mark(dd, 4, 292)
    return im


# ------------------------------------------------------------- 3. Chorégraphie (no text)
def spline(ctrl, n=400):
    """Catmull-Rom through control points."""
    P = np.asarray(ctrl, float)
    P = np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n // (len(P) - 3), endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-2])
    return np.array(out)


def feuillet():
    S = 4
    rnd = random.Random(20261014)
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    # the man's track (left half), from the bottom centre, a loop, an S, back to the axis
    ctrl = [(190, 272), (150, 250), (92, 252), (58, 214), (78, 168), (130, 160), (150, 196),
            (112, 214), (84, 182), (96, 120), (60, 84), (82, 42), (140, 34), (176, 64), (186, 30)]
    track = spline(ctrl, 900)
    for colour, sgn in ((BLACK, 1), (RED, -1)):
        tr = track.copy()
        if sgn < 0:
            tr[:, 0] = 400 - tr[:, 0]
        d.line([tuple(p * S) for p in tr], fill=colour, width=int(1.0 * S), joint="curve")
        pts = resample(tr, 1.0)
        tang = np.gradient(pts, axis=0)
        tang /= np.hypot(*tang.T)[:, None] + 1e-9
        norm = np.stack([-tang[:, 1], tang[:, 0]], 1) * sgn
        # the dancer's starting sign: half-circle facing along the track
        p, t, nn = pts[0], tang[0], norm[0]
        arc = [p + 7 * (math.cos(a) * nn + math.sin(a) * -t) for a in np.linspace(-math.pi / 2, math.pi / 2, 16)]
        d.line([tuple(q * S) for q in arc], fill=colour, width=int(1.8 * S))
        d.line([tuple((p + 7 * nn) * S), tuple((p - 7 * nn) * S)], fill=colour, width=int(1.8 * S))
        step, i, side, count = 17, 14, 1, 0
        r = random.Random(7)  # same choreography for both
        while i + 13 < len(pts):
            off = norm[i] * side * 6.5
            a = pts[i] + off
            b = pts[i + 11] + norm[i + 11] * side * 6.5
            kind = r.choice(["plain", "plain", "plain", "wave", "beat", "rise", "open"])
            d.ellipse([(a[0] - 2.2) * S, (a[1] - 2.2) * S, (a[0] + 2.2) * S, (a[1] + 2.2) * S], fill=colour)
            if kind == "wave":
                seg = [pts[i + j] + norm[i + j] * side * (6.5 + 1.8 * math.sin(j * 1.4)) for j in range(12)]
            elif kind == "open":
                seg = [pts[i + j] + norm[i + j] * side * (6.5 + 4.5 * math.sin(j / 11 * math.pi)) for j in range(12)]
            else:
                seg = [pts[i + j] + norm[i + j] * side * 6.5 for j in range(12)]
            d.line([tuple(q * S) for q in seg], fill=colour, width=int(1.3 * S), joint="curve")
            tb = tang[i + 11]
            # the foot: a short bar across the end of the stem
            d.line([tuple((b - norm[i + 11] * 3) * S), tuple((b + norm[i + 11] * 3) * S)],
                   fill=colour, width=int(1.4 * S))
            m = pts[i + 6] + norm[i + 6] * side * 6.5
            if kind == "beat":   # a small hook: beaten step
                d.line([tuple(m * S), tuple((m + norm[i + 6] * side * 4 + tang[i + 6] * 2) * S)], fill=colour, width=int(1.2 * S))
            if kind == "rise":   # oblique tick: rise
                d.line([tuple((m - tang[i + 6] * 2) * S), tuple((m + norm[i + 6] * side * 4 + tang[i + 6] * 2) * S)],
                       fill=colour, width=int(1.2 * S))
            count += 1
            side = -side
            i += step
            if count % 2 == 0 and i + 13 < len(pts):  # bar line: two little strokes across the track
                for k in (-1.2, 1.2):
                    q = pts[i - 3] + tang[i - 3] * k
                    d.line([tuple((q - norm[i - 3] * 10) * S), tuple((q + norm[i - 3] * 10) * S)],
                           fill=colour, width=int(0.9 * S))
                i += 4
    im = down(big)
    dd = draw1(im)
    mark(dd, 392, 292)
    return im


# ------------------------------------------------------------- 4. Puzzle No. 4 (pigpen)
MESSAGE = "KEEP THOSE CARDS AND LETTERS COMING IN FOLKS"


def pigpen(d, ch, x, y, s, lw, dotc):
    """Draw one pigpen glyph in an s×s box at (x, y). A–I grid, J–R grid+dot, S–V X, W–Z X+dot."""
    k = ord(ch) - 65
    dot = False
    if k < 18:
        dot = k >= 9
        k %= 9
        r, c = divmod(k, 3)
        sides = {"top": r > 0, "bottom": r < 2, "left": c > 0, "right": c < 2}
        if sides["top"]: d.line([x, y, x + s, y], fill=BLACK, width=lw)
        if sides["bottom"]: d.line([x, y + s, x + s, y + s], fill=BLACK, width=lw)
        if sides["left"]: d.line([x, y, x, y + s], fill=BLACK, width=lw)
        if sides["right"]: d.line([x + s, y, x + s, y + s], fill=BLACK, width=lw)
        cx, cy = x + s / 2, y + s / 2
    else:
        k -= 18
        dot = k >= 4
        k %= 4
        cx, cy = x + s / 2, y + s / 2
        h = s / 2
        # S: top quadrant (V), T: left (>), U: right (<), V: bottom (Λ)
        if k == 0:
            pts = [(x, y), (cx, cy), (x + s, y)]; cy = y + s * 0.22
        elif k == 1:
            pts = [(x, y), (cx, cy), (x, y + s)]; cx = x + s * 0.22
        elif k == 2:
            pts = [(x + s, y), (cx, cy), (x + s, y + s)]; cx = x + s * 0.78
        else:
            pts = [(x, y + s), (cx, cy), (x + s, y + s)]; cy = y + s * 0.78
        d.line(pts, fill=BLACK, width=lw, joint="curve")
    if dot:
        rr = max(2, s // 7)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=dotc)


def puzzle():
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    # the TV: a black rounded screen with scan lines, and Schirra's card inside
    sx0, sy0, sx1, sy1 = 10, 10, 390, 206
    d.rounded_rectangle([sx0 * S, sy0 * S, sx1 * S, sy1 * S], radius=26 * S, fill=BLACK)
    for y in range(sy0 + 3, sy1 - 2, 3):
        d.line([(sx0 + 4) * S, y * S + S, (sx1 - 4) * S, y * S + S], fill=WHITE, width=int(1.0 * S))
    cx0, cy0, cx1, cy1 = 26, 24, 374, 192
    d.polygon([(cx0 * S, (cy0 + 4) * S), (cx1 * S, cy0 * S), ((cx1 + 2) * S, cy1 * S), ((cx0 - 1) * S, (cy1 + 2) * S)], fill=WHITE)
    words = MESSAGE.split()
    lines = [words[0:3], words[3:5], words[5:7]]
    gs, gap, wgap, lw = 17, 6, 15, int(2.0 * S)
    y = 34
    for ln in lines:
        wtot = sum(len(w) * (gs + gap) - gap for w in ln) + wgap * (len(ln) - 1)
        x = 200 - wtot / 2
        for w in ln:
            for ch in w:
                pigpen(d, ch, x * S, y * S, gs * S, lw, RED)
                x += gs + gap
            x += wgap - gap
        y += gs + 33
    im = down(big)
    dd = draw1(im)
    fb = font("Inter-Bold.otf", 13)
    fr = font("Inter-Regular.otf", 10)
    dd.text((10, 214), "PUZZLE NO. 4", font=fb, fill=BLACK)
    text_lines(dd, 10, 232, ["Apollo 7, 14 Oct 1968: the first live TV from an American",
                             "spacecraft. Schirra held a card up to the camera. Read it.",
                             "",
                             "Key: a noughts-and-crosses grid for A–I, another for J–R, an X for",
                             "S–V, another for W–Z, read in order. A red dot: the second one."],
               fr, 12, maxw=382)
    mark(dd, 392, 292)
    return im


# ------------------------------------------------------------- 5. Venation
NSRC, KILL = 1700, 10.0


def venation():
    rnd = np.random.default_rng(1014)
    S = 4
    # leaf outline: tip at right, petiole at left
    def outline(t):  # t in [0, 1] along midrib, returns half-width
        return 104 * (np.sin(np.pi * t ** 0.8) ** 1.1) * (1 - 0.25 * t)
    x0, x1, yc = 30.0, 384.0, 132.0
    L = x1 - x0
    # sample auxin sources inside the blade (rejection)
    pts = []
    while len(pts) < NSRC:
        x, y = rnd.uniform(x0, x1), rnd.uniform(yc - 106, yc + 106)
        t = (x - x0) / L
        if 4 < abs(y - yc) < outline(t) - 1.0:
            pts.append((x, y))
    src = np.array(pts)
    # the midrib is laid down first, petiole to tip; everything else is grown from it
    mid = [np.array([x, yc + 3 * math.sin((x - x0) / L * math.pi)]) for x in np.arange(x0 - 14, x1 - 8, 2.5)]
    nodes = list(mid)
    parent = [-1] + list(range(len(mid) - 1))
    D, Ri, Rk = 2.2, 40.0, KILL
    for it in range(400):
        N = np.array(nodes)
        if len(src) == 0:
            break
        dist = np.hypot(src[:, None, 0] - N[None, :, 0], src[:, None, 1] - N[None, :, 1])
        # only every 7th midrib node may sprout a secondary vein, upper and lower alternating
        for j in range(len(mid)):
            if j % 7 != 0:
                dist[:, j] = np.inf
            else:
                side = 1 if (j // 7) % 2 else -1
                dist[(src[:, 1] - yc) * side < 0, j] = np.inf
        near = dist.argmin(1)
        ok = dist[np.arange(len(src)), near] < Ri
        grow = {}
        for s_i in np.where(ok)[0]:
            v = src[s_i] - N[near[s_i]]
            grow.setdefault(near[s_i], np.zeros(2))
            grow[near[s_i]] += v / (np.hypot(*v) + 1e-9)
        if not grow:
            break
        for n_i, v in grow.items():
            if np.hypot(*v) < 1e-6:
                continue
            v = v / np.hypot(*v)
            v = v + np.array([0.55 if n_i >= len(mid) else 1.1, 0.0])  # everything sweeps towards the tip
            v /= np.hypot(*v)
            nodes.append(N[n_i] + D * v)
            parent.append(n_i)
        N = np.array(nodes)
        dist = np.hypot(src[:, None, 0] - N[None, :, 0], src[:, None, 1] - N[None, :, 1])
        src = src[dist.min(1) > Rk]
    N = np.array(nodes)
    par = np.array(parent)
    # pipe model widths (da Vinci): leaves = 1, w^2 = sum of children w^2
    w = np.zeros(len(N))
    kids = [[] for _ in N]
    for i, p in enumerate(par):
        if p >= 0:
            kids[p].append(i)
    for i in range(len(N) - 1, -1, -1):
        w[i] = 1.0 if not kids[i] else sum(w[k] ** 2 for k in kids[i]) ** 0.5
    # the red path: from the node nearest the tip back to the stalk
    tip = np.argmin(np.hypot(N[:, 0] - (x1 - 6), N[:, 1] - yc))
    # pick a node near the margin, upper side, two-thirds along, for a more interesting path
    target = np.array([x0 + 0.62 * L, yc - outline(0.62) + 8])
    leaf_i = np.argmin(np.hypot(*(N - target).T))
    path = set()
    i = leaf_i
    while i >= 0:
        path.add(i); i = par[i]
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    for i in range(1, len(N)):
        p = par[i]
        if p < 0 or i in path:
            continue
        lw = 1.2 + 0.55 * (w[i] - 1)
        d.line([tuple(N[p] * S), tuple(N[i] * S)], fill=BLACK, width=max(1, int(lw * S)))
    for i in path:
        p = par[i]
        if p >= 0:
            lw = 1.2 + 0.55 * (w[i] - 1)
            d.line([tuple(N[p] * S), tuple(N[i] * S)], fill=RED, width=max(int(1.6 * S), int(lw * S)))
    ts = np.linspace(0, 1, 300)
    up = [((x0 + t * L) * S, (yc - outline(t)) * S) for t in ts]
    lo = [((x0 + t * L) * S, (yc + outline(t)) * S) for t in ts]
    d.line(up, fill=BLACK, width=int(1.3 * S), joint="curve")
    d.line(lo, fill=BLACK, width=int(1.3 * S), joint="curve")
    im = down(big)
    dd = draw1(im)
    fb = font("Inter-Bold.otf", 11)
    fr = font("Inter-Regular.otf", 10)
    dd.text((10, 254), "VENATION", font=fb, fill=BLACK)
    dd.text((10, 268), "Grown, not drawn: each vein reaches for the nearest unfed cell.", font=fr, fill=BLACK)
    dd.text((10, 281), "Red: one drop's way home to the stalk.", font=fr, fill=RED)
    mark(dd, 392, 292)
    print("venation nodes", len(N))
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    for n, fn in enumerate([tapestry, mach, feuillet, puzzle, venation], 1):
        if only and str(n) not in only:
            continue
        save(fn(), f"{n}.png")
