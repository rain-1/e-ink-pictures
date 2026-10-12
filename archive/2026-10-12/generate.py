#!/usr/bin/env python3
"""2026-10-12 — five pictures for a 400x300 black/white/red e-ink panel.
Theme: counting, crowding, and reaching.
1. Voskhod 1 — 12 Oct 1964, three men in a capsule built for one; red = the helmets they couldn't wear.
2. Mercury at full stretch — greatest eastern elongation today, 25.2° from the Sun; red = our sightline.
3. Khipu — twelve cords knotted in base ten (Fibonacci 1…144); the red top cord holds their sum.
4. (untitled) Sunflower — Vogel's model, 1,000 florets at the golden angle; one red parastichy. No text.
5. Puzzle No. 2 — a theta maze, from the red gap to the red heart. Solution: solution.png.
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
    d.fontmode = "1"  # crisp text, never dithered
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


def caption(d, x, y, title, lines, tsize=15, lead=13):
    d.text((x, y), title, font=font("Inter-Bold.otf", tsize), fill=BLACK)
    y += tsize + 8
    f = font("Inter-Regular.otf", 10)
    for ln in lines:
        if ln == "":
            y += 6
            continue
        d.text((x, y), ln, font=f, fill=BLACK)
        y += lead
    return y


def dashed_circle(d, cx, cy, r, w, fill, n=24, duty=0.55, phase=0.0):
    for i in range(n):
        a0 = 360 * (i + phase) / n
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 360 * duty / n, fill=fill, width=w)


# ------------------------------------------------------------- 1. Voskhod 1
def voskhod():
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    a = np.full((H * S, W * S), 255, np.uint8)
    cx, cy, R = 116 * S, 150 * S, 106 * S
    Ri = 84 * S
    yy, xx = np.mgrid[0:H * S, 0:W * S]
    dx, dy = (xx - cx) / R, (yy - cy) / R
    rr = dx * dx + dy * dy
    hull = rr <= 1.0
    # sphere shading (light from upper left), drawn as horizontal engraving lines
    nz = np.sqrt(np.clip(1 - rr, 0, 1))
    lam = np.clip(-0.55 * dx - 0.6 * dy + 0.6 * nz, 0, 1)
    dark = 1 - lam
    # heat shield: offset inner cavity -> hull thicker at the bottom
    icx, icy = cx, cy - 8 * S
    inner = (xx - icx) ** 2 + (yy - icy) ** 2 <= Ri ** 2
    period = 3 * S
    phase = (yy % period).astype(float)
    thick = 0.2 * S + dark ** 1.4 * 1.9 * S
    ink = hull & ~inner & (phase < thick)
    a[ink] = 0
    big = Image.fromarray(a).convert("RGB")
    d = ImageDraw.Draw(big)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLACK, width=2 * S)
    d.ellipse([icx - Ri, icy - Ri, icx + Ri, icy + Ri], outline=BLACK, width=int(1.5 * S))
    # hatch (porthole) on the hull, upper right
    hx, hy = cx + int(0.70 * R), cy - int(0.70 * R)
    d.ellipse([hx - 13 * S, hy - 13 * S, hx + 13 * S, hy + 13 * S], fill=WHITE, outline=BLACK, width=2 * S)
    d.ellipse([hx - 8 * S, hy - 8 * S, hx + 8 * S, hy + 8 * S], outline=BLACK, width=S)

    # three crew, shoulder to shoulder; middle one sits a little forward
    crew = [(-48, -8, 1.0), (48, -8, 1.0), (0, 6, 1.08)]
    floor_y = icy + int(0.80 * Ri)
    for ox, oy, sc in crew:
        x0, y0 = icx + ox * S, icy + oy * S
        hr = int(15 * S * sc)
        sw = int(34 * S * sc)
        top = y0 + hr + 4 * S
        # torso: shoulders down to the couch
        body = [(x0 - sw, floor_y), (x0 - sw, top + 14 * S), (x0 - sw + 12 * S, top),
                (x0 + sw - 12 * S, top), (x0 + sw, top + 14 * S), (x0 + sw, floor_y)]
        d.polygon(body, fill=WHITE, outline=BLACK, width=int(1.5 * S))
        # collar
        d.line([(x0 - 7 * S, top), (x0, top + 9 * S), (x0 + 7 * S, top)], fill=BLACK, width=int(1.5 * S))
        # head
        d.ellipse([x0 - hr, y0 - hr, x0 + hr, y0 + hr], fill=WHITE, outline=BLACK, width=int(1.5 * S))
        # a flat ear-cap headset (they flew in wool suits and leather caps)
        d.arc([x0 - hr, y0 - hr, x0 + hr, y0 + hr], 200, 340, fill=BLACK, width=4 * S)
    # clip everything to the cavity: repaint the hull ring over the crew
    a2 = np.asarray(big).copy()
    keep = ~inner
    a2[keep] = np.asarray(Image.fromarray(a).convert("RGB"))[keep]
    big = Image.fromarray(a2)
    d = ImageDraw.Draw(big)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLACK, width=2 * S)
    d.ellipse([icx - Ri, icy - Ri, icx + Ri, icy + Ri], outline=BLACK, width=int(1.5 * S))
    d.ellipse([hx - 13 * S, hy - 13 * S, hx + 13 * S, hy + 13 * S], fill=WHITE, outline=BLACK, width=2 * S)
    d.ellipse([hx - 8 * S, hy - 8 * S, hx + 8 * S, hy + 8 * S], outline=BLACK, width=S)
    # red: the helmets that didn't fit
    for ox, oy, sc in crew:
        x0, y0 = icx + ox * S, icy + oy * S
        dashed_circle(d, x0, y0, int(24 * S * sc), int(1.6 * S), RED, n=18, duty=0.55)
    im = down(big)
    d = draw1(im)
    y = caption(d, 240, 52, "VOSKHOD 1", [
        "12 October 1964",
        "",
        "Komarov, Feoktistov, Yegorov:",
        "the first crew of three, in a",
        "sphere built for one.",
        "",
        "To make room, the ejection",
        "seat went. So did the suits.",
        "",
        "Red: the helmets",
        "that would not fit.",
    ], tsize=17)
    mark(d, 391, 291)
    return im


# ------------------------------------------------------------- 2. Mercury
def mercury():
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    sx, sy = 110 * S, 116 * S
    ex, ey = 336 * S, 116 * S
    dist = ex - sx
    elong = math.radians(25.2)
    rm = dist * math.sin(elong)
    # Earth's orbit: arc through Earth
    d.arc([sx - dist, sy - dist, sx + dist, sy + dist], -24, 24, fill=BLACK, width=S)
    # Mercury's orbit: dotted
    n = 120
    for i in range(n):
        t = 2 * math.pi * i / n
        px, py = sx + rm * math.cos(t), sy + rm * math.sin(t)
        d.ellipse([px - 1.1 * S, py - 1.1 * S, px + 1.1 * S, py + 1.1 * S], fill=BLACK)
    # Sun: engraved rays
    for i in range(72):
        t = 2 * math.pi * i / 72
        r0 = 13 * S
        r1 = (24 if i % 2 == 0 else 19) * S
        d.line([(sx + r0 * math.cos(t), sy + r0 * math.sin(t)),
                (sx + r1 * math.cos(t), sy + r1 * math.sin(t))], fill=BLACK, width=S)
    d.ellipse([sx - 10 * S, sy - 10 * S, sx + 10 * S, sy + 10 * S], fill=BLACK)
    # tangent point: Mercury, above the Sun–Earth line (evening sky, east of the Sun)
    # tangent point seen from Earth: the angle at the Sun between SE and SM is 90° - elongation
    ang = math.pi / 2 - elong
    mx, my = sx + rm * math.cos(ang), sy - rm * math.sin(ang)
    # sightlines
    d.line([(ex, ey), (sx + 28 * S, sy)], fill=BLACK, width=S)
    ux, uy = mx - ex, my - ey
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    d.line([(ex, ey), (ex + ux * (L + 26 * S), ey + uy * (L + 26 * S))], fill=RED, width=2 * S)
    # right angle at the tangent point
    vx, vy = (sx - mx) / rm, (sy - my) / rm
    k = 6 * S
    p1 = (mx - ux * k, my - uy * k)
    p2 = (p1[0] + vx * k, p1[1] + vy * k)
    p3 = (mx + vx * k, my + vy * k)
    d.line([p1, p2, p3], fill=BLACK, width=S)
    # elongation arc at Earth
    ar = 70 * S
    d.arc([ex - ar, ey - ar, ex + ar, ey + ar], 180, 180 + math.degrees(elong), fill=RED, width=2 * S)
    # Mercury: half-lit disc, lit side facing the Sun
    mr = 7 * S
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=BLACK)
    lit = math.degrees(math.atan2(sy - my, sx - mx))
    d.pieslice([mx - mr, my - mr, mx + mr, my + mr], lit - 90, lit + 90, fill=WHITE)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=BLACK, width=S)
    # Earth
    er = 8 * S
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=WHITE, outline=BLACK, width=S)
    d.pieslice([ex - er, ey - er, ex + er, ey + er], -90, 90, fill=BLACK)
    im = down(big)
    d = draw1(im)
    la = elong / 2
    d.text((ex // S - 96 * math.cos(la), ey // S - 96 * math.sin(la)), "25.2°",
           font=font("Inter-Bold.otf", 13), fill=RED, anchor="mm")
    small = font("Inter-Regular.otf", 10)
    d.text((sx // S - 10, sy // S + 28), "Sun", font=small, fill=BLACK)
    d.text((ex // S - 14, ey // S + 13), "Earth", font=small, fill=BLACK)
    d.text((int(mx // S) - 18, int(my // S) - 22), "Mercury", font=small, fill=BLACK)
    y = 226
    d.text((14, y), "MERCURY, AT FULL STRETCH", font=font("Inter-Bold.otf", 15), fill=BLACK)
    d.text((14, y + 23), "Greatest eastern elongation, 12 October 2026: as far from the Sun as it gets.",
           font=font("Inter-Regular.otf", 10), fill=BLACK)
    d.text((14, y + 37), "Our line of sight just grazes its orbit. Look low in the west after sunset.",
           font=font("Inter-Regular.otf", 10), fill=BLACK)
    d.text((14, y + 51), "The leash never gets longer than this.",
           font=font("Inter-Regular.otf", 10), fill=BLACK)
    mark(d, 391, 291)
    return im


# ------------------------------------------------------------- 3. Khipu
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]


def khipu():
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    rng = random.Random(1012)
    main_y = 36 * S
    x_l, x_r = 24 * S, 376 * S
    # main cord: twisted (S-ply) rope
    d.line([(x_l, main_y), (x_r, main_y)], fill=BLACK, width=5 * S)
    for x in range(x_l, x_r, 3 * S):
        d.line([(x, main_y + 2 * S), (x + 2 * S, main_y - 2 * S)], fill=WHITE, width=int(0.7 * S))
    # loose ends of the main cord
    d.line([(x_l, main_y), (x_l - 10 * S, main_y + 18 * S)], fill=BLACK, width=3 * S)

    BANDS = {100: 96, 10: 150, 1: 206}  # y (1x) of each decimal band

    def cord(x, y0, y1, color, sway):
        pts = []
        for y in range(y0, y1, 2 * S):
            t = (y - y0) / max(1, (y1 - y0))
            pts.append((x + sway * math.sin(t * 2.2) * t, y))
        d.line(pts, fill=color, width=int(1.6 * S), joint="curve")
        return lambda y: x + sway * math.sin((y - y0) / (y1 - y0) * 2.2) * (y - y0) / (y1 - y0)

    def single(xf, y, color):
        x = xf(y)
        d.ellipse([x - 5 * S, y - 3.2 * S, x + 5 * S, y + 3.2 * S], fill=WHITE, outline=color, width=int(1.4 * S))
        d.line([(x - 4 * S, y + 2 * S), (x + 4 * S, y - 2 * S)], fill=color, width=int(1.4 * S))

    def long_knot(xf, y, turns, color):
        h = (3 + 3.2 * turns) * S
        x = xf(y)
        d.rounded_rectangle([x - 4 * S, y - h / 2, x + 4 * S, y + h / 2], radius=3 * S,
                            fill=WHITE, outline=color, width=int(1.4 * S))
        for i in range(turns):
            yy = y - h / 2 + (i + 0.5 + 0.5) * (h - 3 * S) / turns
            d.line([(x - 4 * S, yy + 1.4 * S), (x + 4 * S, yy - 1.4 * S)], fill=color, width=int(1.3 * S))

    def figure8(xf, y, color):
        x = xf(y)
        d.ellipse([x - 3.5 * S, y - 7 * S, x + 3.5 * S, y], fill=WHITE, outline=color, width=int(1.4 * S))
        d.ellipse([x - 3.5 * S, y - 0.5 * S, x + 3.5 * S, y + 6.5 * S], fill=WHITE, outline=color, width=int(1.4 * S))

    def knots(xf, value, color, bands, up=False):
        h, t, u = value // 100, (value // 10) % 10, value % 10
        for place, cnt in ((100, h), (10, t)):
            yc = bands[place]
            for i in range(cnt):
                off = (i - (cnt - 1) / 2) * 7 * S
                single(xf, yc * S + (-off if up else off), color)
        if u == 1:
            figure8(xf, bands[1] * S, color)
        elif u > 1:
            long_knot(xf, bands[1] * S, u, color)

    n = len(FIB)
    xs = [int((40 + i * (322 / n)) * S) for i in range(n + 1)]
    vals = [sum(FIB)] + FIB
    for i, (x, v) in enumerate(zip(xs, vals)):
        col = RED if i == 0 else BLACK
        L = (226 + rng.randint(-6, 12)) * S
        xf = cord(x, main_y, L, col, rng.uniform(-5, 5) * S)
        # attachment loop
        d.ellipse([x - 3 * S, main_y - 4 * S, x + 3 * S, main_y + 5 * S], outline=BLACK, width=int(1.2 * S))
        knots(xf, v, col, BANDS)
        # frayed tail
        ex = xf(L - 2 * S)
        for k in (-1, 0, 1):
            d.line([(ex, L), (ex + k * 2 * S, L + 6 * S)], fill=col, width=S)
    im = down(big)
    d = draw1(im)
    f = font("Inter-Regular.otf", 10)
    d.text((14, 248), "KHIPU", font=font("Inter-Bold.otf", 15), fill=BLACK)
    d.text((74, 251), "twelve cords, knotted in base ten", font=f, fill=BLACK)
    d.text((14, 270), "hundreds · tens · units (long knot = turns, figure-eight = one).", font=f, fill=BLACK)
    d.text((14, 283), "Read them; they follow a rule. The red cord holds their sum.", font=f, fill=BLACK)
    mark(d, 391, 291)
    return im


# ------------------------------------------------------------- 4. Sunflower (no text)
def sunflower():
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    cx, cy = 200 * S, 150 * S
    N = 1000
    ga = math.pi * (3 - math.sqrt(5))
    Rd = 112 * S
    c = Rd / math.sqrt(N)
    # petals: two rings of outlined pointed petals
    for ring, (np_, r0, r1, off) in enumerate([(34, 0.97, 1.31, 0.5), (34, 0.97, 1.24, 0.0)]):
        for i in range(np_):
            t = 2 * math.pi * (i + off) / np_
            wid = 2 * math.pi / np_ * 0.42
            pts = []
            for k in range(13):
                s = k / 12
                rad = Rd * (r0 + (r1 - r0) * s)
                w = wid * math.sin(math.pi * min(1, s * 1.15)) ** 0.7
                pts.append((cx + rad * math.cos(t - w * (1 - s * 0.3)), cy + rad * math.sin(t - w * (1 - s * 0.3))))
            for k in range(12, -1, -1):
                s = k / 12
                rad = Rd * (r0 + (r1 - r0) * s)
                w = wid * math.sin(math.pi * min(1, s * 1.15)) ** 0.7
                pts.append((cx + rad * math.cos(t + w * (1 - s * 0.3)), cy + rad * math.sin(t + w * (1 - s * 0.3))))
            d.polygon(pts, fill=WHITE, outline=BLACK, width=int(1.3 * S))
    d.ellipse([cx - Rd * 1.0, cy - Rd * 1.0, cx + Rd * 1.0, cy + Rd * 1.0], fill=WHITE)
    # one parastichy: florets k, k+34, k+68, ...
    FAM, K = 34, 7
    pts = [(n, cx + c * math.sqrt(n) * math.cos(n * ga), cy + c * math.sqrt(n) * math.sin(n * ga))
           for n in range(1, N + 1)]
    for n, x, y in pts:
        r = c * math.sqrt(n)
        fr = c * (0.5 + 0.08 * r / Rd)
        col = RED if n % FAM == K else BLACK
        d.ellipse([x - fr, y - fr, x + fr, y + fr], fill=col)
    im = down(big)
    d = draw1(im)
    mark(d, 391, 291)
    return im


# ------------------------------------------------------------- 5. Theta maze
def theta_maze(seed=20261012):
    rng = random.Random(seed)
    RINGS = 11
    counts = []
    c = 6
    for r in range(RINGS):
        # keep cells roughly square: double the sectors when the arc gets too long
        if r > 0 and (r + 0.5) * 2 * math.pi / c > 2.0:
            c *= 2
        counts.append(c)
    cells = [(r, i) for r in range(RINGS) for i in range(counts[r])]

    def nbrs(r, i):
        out = [(r, (i - 1) % counts[r]), (r, (i + 1) % counts[r])]
        if r + 1 < RINGS:
            k = counts[r + 1] // counts[r]
            out += [(r + 1, i * k + j) for j in range(k)]
        if r > 0:
            k = counts[r] // counts[r - 1]
            out.append((r - 1, i // k))
        return out

    # recursive backtracker -> spanning tree (every cell reachable, unique solution)
    start = (RINGS - 1, 0)
    seen = {start}
    stack = [start]
    links = set()
    while stack:
        cur = stack[-1]
        nb = [n for n in nbrs(*cur) if n not in seen]
        if not nb:
            stack.pop()
            continue
        nx = rng.choice(nb)
        links.add(frozenset((cur, nx)))
        seen.add(nx)
        stack.append(nx)
    assert len(seen) == len(cells)
    # merge the innermost ring into one open centre: link all ring-0 cells
    for i in range(counts[0]):
        links.add(frozenset(((0, i), (0, (i + 1) % counts[0]))))
    entry = (RINGS - 1, rng.randrange(counts[-1]))
    # solve: BFS from entry to ring 0
    from collections import deque
    prev = {entry: None}
    q = deque([entry])
    while q:
        cur = q.popleft()
        for n in nbrs(*cur):
            if n not in prev and frozenset((cur, n)) in links:
                prev[n] = cur
                q.append(n)
    goal = (0, 0)
    assert goal in prev
    path = []
    p = goal
    while p is not None:
        path.append(p)
        p = prev[p]
    return RINGS, counts, links, entry, path[::-1]


def maze_image(show_solution=False):
    RINGS, counts, links, entry, path = theta_maze()
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    cx, cy = 150 * S, 150 * S
    r0 = 16 * S
    dr = (138 * S - r0) / (RINGS - 1)

    def rad(r):  # inner radius of ring r (ring 0 = the open centre)
        return 0 if r == 0 else r0 + (r - 1) * dr

    lw = 2 * S
    # circular walls: outer boundary of ring r between ring r and r+1
    for r in range(RINGS):
        R = rad(r + 1) if r + 1 < RINGS else rad(r) + dr
        n = counts[r]
        for i in range(n):
            a0, a1 = 360 * i / n, 360 * (i + 1) / n
            if r + 1 < RINGS:
                k = counts[r + 1] // n
                for j in range(k):
                    if frozenset(((r, i), (r + 1, i * k + j))) not in links:
                        b0 = a0 + (a1 - a0) * j / k
                        b1 = a0 + (a1 - a0) * (j + 1) / k
                        d.arc([cx - R, cy - R, cx + R, cy + R], b0 - 90, b1 - 90, fill=BLACK, width=lw)
            else:
                if (r, i) != entry:
                    d.arc([cx - R, cy - R, cx + R, cy + R], a0 - 90, a1 - 90, fill=BLACK, width=int(2.4 * S))
    # radial walls
    for r in range(1, RINGS):
        n = counts[r]
        for i in range(n):
            if frozenset(((r, i), (r, (i + 1) % n))) not in links:
                t = 2 * math.pi * (i + 1) / n - math.pi / 2
                a, b = rad(r), rad(r) + dr
                d.line([(cx + a * math.cos(t), cy + a * math.sin(t)), (cx + b * math.cos(t), cy + b * math.sin(t))],
                       fill=BLACK, width=lw)
    # red heart in the centre, red tick at the entry gap
    hr = 7 * S
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=RED)
    er, ei = entry
    t = 2 * math.pi * (ei + 0.5) / counts[er] - math.pi / 2
    Ro = rad(er) + dr
    for k in (6, 12):
        pass
    tip = (cx + (Ro + 4 * S) * math.cos(t), cy + (Ro + 4 * S) * math.sin(t))
    base = Ro + 14 * S
    nx, ny = -math.sin(t), math.cos(t)
    bx, by = cx + base * math.cos(t), cy + base * math.sin(t)
    d.polygon([tip, (bx + nx * 6 * S, by + ny * 6 * S), (bx - nx * 6 * S, by - ny * 6 * S)], fill=RED)
    if show_solution:
        pts = []
        for (r, i) in path:
            n = counts[r]
            tt = 2 * math.pi * (i + 0.5) / n - math.pi / 2
            rr = 0 if r == 0 else rad(r) + dr / 2
            pts.append((cx + rr * math.cos(tt), cy + rr * math.sin(tt)))
        # draw along arcs between same-ring cells
        out = [pts[0]]
        for (a, pa), (b, pb) in zip(zip(path, pts), zip(path[1:], pts[1:])):
            if a[0] == b[0] and a[0] > 0:
                n = counts[a[0]]
                rr = rad(a[0]) + dr / 2
                t0 = 2 * math.pi * (a[1] + 0.5) / n
                t1 = 2 * math.pi * (b[1] + 0.5) / n
                dt = (t1 - t0 + math.pi) % (2 * math.pi) - math.pi
                for s in range(1, 9):
                    tt = t0 + dt * s / 8 - math.pi / 2
                    out.append((cx + rr * math.cos(tt), cy + rr * math.sin(tt)))
            else:
                out.append(pb)
        d.line(out, fill=RED, width=int(2.2 * S), joint="curve")
    im = down(big)
    d = draw1(im)
    y = caption(d, 304, 40, "PUZZLE", [
        "No. 2 · theta maze",
        "",
        "Enter at the red",
        "arrow; find the",
        "red heart.",
        "",
        f"{RINGS - 1} rings,",
        "one true path.",
    ], tsize=17)
    d.text((304, 262), "Solution in", font=font("Inter-Regular.otf", 10), fill=BLACK)
    d.text((304, 275), "the archive.", font=font("Inter-Regular.otf", 10), fill=BLACK)
    mark(d, 391, 291)
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([voskhod, mercury, khipu, sunflower, maze_image], 1):
        save(fn(), f"{i}.png")
    save(maze_image(True), "solution.png")
    print("ok")
