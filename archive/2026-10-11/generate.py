#!/usr/bin/env python3
"""2026-10-11 — five pictures for a 400x300 black/white/red e-ink panel.
Theme: what grows by rule, and what the sea takes back.
1. Strand — the Burchardi flood, night of 11–12 Oct 1634, splits one island into three.
2. (untitled) Conus textile — Rule 30 from one red cell; the shell is its light cone. No text.
3. Romain du Roi — the king's letter R on the 48×48 grid of 1692, compass work in red.
4. Nonogram No. 1 — a puzzle to solve at the desk. Red marks where to begin.
5. First frost — diffusion-limited aggregation from the bottom of the glass;
   red is the lineage of the highest crystal.
Run: python3 generate.py <outdir>"""
import math, random, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
PAL = [255, 255, 255, 0, 0, 0, 255, 0, 0] + [0] * (256 * 3 - 9)
FD = "/usr/share/fonts/opentype/inter/"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."


def font(name, size):
    return ImageFont.truetype(FD + name, size)


def draw1(im):
    d = ImageDraw.Draw(im)
    d.fontmode = "1"  # crisp text, never dithered
    return d


def snap(im):
    """Nearest palette colour, no dither; returns RGB."""
    a = np.asarray(im.convert("RGB")).astype(int)
    cols = np.array([WHITE, BLACK, RED])
    idx = ((a[:, :, None, :] - cols[None, None]) ** 2).sum(-1).argmin(-1)
    return Image.fromarray(cols[idx].astype(np.uint8), "RGB")


def save(im, n):
    a = np.asarray(im.convert("RGB")).astype(int)
    cols = np.array([WHITE, BLACK, RED])
    idx = ((a[:, :, None, :] - cols[None, None]) ** 2).sum(-1).argmin(-1).astype(np.uint8)
    p = Image.fromarray(idx, "P")
    p.putpalette(PAL)
    p.save(os.path.join(OUT, f"{n}.png"), optimize=True)


def mark(d, x, y, fill=RED):
    d.rectangle([x, y, x + 3, y + 3], fill=fill)


# ------------------------------------------------------------- 1. Strand 1634
def blob(cx, cy, rx, ry, seed, rough=0.18, n=160, rot=0.0):
    rng = random.Random(seed)
    harm = [(k, rng.uniform(-1, 1) * rough / k ** 0.8, rng.uniform(0, 6.28)) for k in range(2, 9)]
    pts = []
    for i in range(n):
        t = i / n * 2 * math.pi
        r = 1 + sum(a * math.cos(k * t + ph) for k, a, ph in harm)
        x, y = rx * r * math.cos(t), ry * r * math.sin(t)
        x, y = x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)
        pts.append((cx + x, cy + y))
    return pts


def strand():
    S = 3
    old = blob(205, 140, 150, 82, 1634, 0.32, rot=-0.12)
    pell = blob(118, 158, 40, 34, 11, 0.14)
    nord = blob(282, 158, 40, 30, 12, 0.16, rot=0.3)
    moor = blob(202, 104, 11, 7, 13, 0.2)
    sued = blob(190, 205, 7, 5, 14, 0.2)
    lands = [pell, nord, moor, sued]
    # mainland: right edge
    rng = random.Random(1)
    coast = [(372 + 8 * math.sin(y / 23) + rng.uniform(-2, 2), y) for y in range(0, 301, 6)]
    main = coast + [(400, 300), (400, 0)]

    def mask(polys):
        m = Image.new("L", (W * S, H * S), 0)
        dm = ImageDraw.Draw(m)
        for p in polys:
            dm.polygon([(x * S, y * S) for x, y in p], fill=255)
        return np.asarray(m.resize((W, H), Image.BOX)) > 127

    m_old, m_land, m_main = mask([old]), mask(lands), mask([main])
    land = m_land | m_main
    im = Image.new("RGB", (W, H), WHITE)
    a = np.array(im)
    # sea: wavy hairlines; red where the drowned island lay
    for y0 in range(2, H, 4):
        for x in range(W):
            y = int(round(y0 + 1.2 * math.sin(x / 9.0 + y0 * 0.7)))
            if 0 <= y < H and not land[y, x]:
                a[y, x] = RED if m_old[y, x] else BLACK
    im = Image.fromarray(a)
    # outlines at 3x
    big = im.resize((W * S, H * S), Image.NEAREST)
    db = ImageDraw.Draw(big)
    for p in lands + [main]:
        pp = [(x * S, y * S) for x, y in p]
        db.polygon(pp, fill=WHITE)
        db.line(pp + [pp[0]], fill=BLACK, width=4)
    # old coastline, dashed red
    pp = [(x * S, y * S) for x, y in old] + [(old[0][0] * S, old[0][1] * S)]
    acc = 0
    for (x1, y1), (x2, y2) in zip(pp, pp[1:]):
        L = math.hypot(x2 - x1, y2 - y1)
        if (acc // 14) % 2 == 0:
            db.line([(x1, y1), (x2, y2)], fill=RED, width=5)
        acc += L
    im = snap(big.resize((W, H), Image.LANCZOS))
    d = draw1(im)
    # marsh stipple on surviving land
    rng = random.Random(7)
    for _ in range(900):
        x, y = rng.randrange(W), rng.randrange(H)
        if m_land[y, x] and not m_land[max(0, y - 3):y + 4, max(0, x - 3):x + 4].all() is False:
            if rng.random() < 0.5:
                d.point((x, y), fill=BLACK)
    f9, f10 = font("Inter-Regular.otf", 9), font("Inter-Medium.otf", 10)

    def label(x, y, s, f=f9, fill=BLACK, box=False):
        w = d.textlength(s, font=f)
        if box:
            d.rectangle([x - 2, y - 1, x + w + 1, y + 11], fill=WHITE)
        d.text((x, y), s, font=f, fill=fill)

    label(96, 154, "PELLWORM", f10)
    label(250, 154, "NORDSTRAND", f10)
    label(154, 86, "NORDSTRANDISCHMOOR", f9, box=True)
    label(198, 200, "SÜDFALL", f9, box=True)
    d.ellipse([379, 140, 383, 144], fill=BLACK)
    label(342, 128, "HUSUM", f9, box=True)
    # title block
    d.rectangle([10, 10, 168, 58], fill=WHITE, outline=BLACK)
    d.text((18, 15), "STRAND", font=font("Inter-Bold.otf", 20), fill=BLACK)
    d.text((18, 40), "night of 11–12 October 1634", font=f10, fill=RED)
    d.rectangle([10, 243, 300, 289], fill=WHITE, outline=BLACK)
    lines = ["The Burchardi flood. In the evening, one island of 22,000 ha;",
             "by morning, three, and the Halligen. Thousands drowned.",
             "Red is the sea where the land was."]
    for i, s in enumerate(lines):
        d.text((17, 247 + i * 13), s, font=f9, fill=RED if i == 2 else BLACK)
    mark(d, W - 12, H - 12)
    return im


# --------------------------------------------- 2. Conus textile (Rule 30), no text
def rule30(steps, width):
    row = np.zeros(width, dtype=np.uint8)
    row[width // 2] = 1
    out = [row.copy()]
    for _ in range(steps - 1):
        l, r = np.roll(row, 1), np.roll(row, -1)
        row = (l ^ (row | r)).astype(np.uint8)
        out.append(row.copy())
    return np.array(out)


def conus():
    S = 4
    dx, dy = 2 * S, 2 * S  # one CA step / one cell; light cone is 45°, the shell sits inside it
    steps = 122
    slope = 0.46  # the shell's half-angle, tan ~25°
    tipx, cy = 40 * S, 150 * S  # the red seed cell sits at the anterior tip
    ca = rule30(steps + 60, 2 * (steps + 60) + 1)
    mid = ca.shape[1] // 2
    yy, xx = np.mgrid[0:H * S, 0:W * S]
    t = (xx - tipx) / dx
    shoulder = steps
    tn = np.clip(t / shoulder, 0, 1)
    round_ = np.sqrt(np.clip(1 - (np.clip(t - shoulder + 10, 0, None) / 10.0) ** 2, 0, 1))
    half = t * dx * slope * (1 + 0.05 * np.sin(np.pi * tn)) * round_
    body = (t >= 0) & (t <= shoulder) & (np.abs(yy - cy) <= half)
    # spire: a low cone beyond the shoulder; later generations, squeezed toward the apex
    sx0 = tipx + (shoulder - 4) * dx
    Hs = shoulder * dx * slope * 0.92
    spire_len = 30 * S
    u = (xx - sx0) / spire_len
    sh = Hs * np.clip(1 - u, 0, 1) ** 1.15
    spire = (u >= 0) & (u <= 1) & (np.abs(yy - cy) <= sh) & ~body
    ti = t.astype(int).clip(0, ca.shape[0] - 1)
    sc = (yy - cy) / dy
    ci = (np.round(sc).astype(int) + mid).clip(0, ca.shape[1] - 1)
    cell = ca[ti, ci].astype(bool)
    a = np.full((H * S, W * S, 3), 255, np.uint8)
    a[(body | spire) & cell] = BLACK
    # whorl sutures on the spire
    for k in range(1, 5):
        uk = 1 - (1 - k / 5) ** 0.7
        hh = Hs * (1 - uk) ** 1.15
        for yv in range(int(cy - hh), int(cy + hh)):
            q = (yv - cy) / max(hh, 1)
            xs = int(sx0 + uk * spire_len + 6 * S * (1 - q * q))
            a[yv, xs - 9:xs + 9] = WHITE
            a[yv, xs - 4:xs + 4] = BLACK
    edge = body | spire
    e = edge & ~(np.roll(edge, 5, 0) & np.roll(edge, -5, 0) & np.roll(edge, 5, 1) & np.roll(edge, -5, 1))
    a[e] = BLACK
    big = Image.fromarray(a)
    db = ImageDraw.Draw(big)
    db.rectangle([tipx - 3 * S, cy - 3 * S, tipx + 2 * S, cy + 2 * S], fill=RED)
    im = snap(big.resize((W, H), Image.LANCZOS))
    d = draw1(im)
    mark(d, W - 12, H - 12)
    return im


# --------------------------------------------------------- 3. Romain du Roi
def romain():
    S = 4
    U = 5 * S              # one grid unit (1/48) = 5 px at 1x
    ox, oy = 28 * S, 30 * S
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    P = lambda x, y: (ox + x * U, oy + y * U)
    # the grid: dots every unit, lines every 6
    for i in range(49):
        for j in range(49):
            if i % 6 and j % 6:
                x, y = P(i, j)
                d.rectangle([x - 1, y - 1, x + 2, y + 2], fill=BLACK)
    for i in range(0, 49, 6):
        d.line([P(i, 0), P(i, 48)], fill=BLACK, width=3)
        d.line([P(0, i), P(48, i)], fill=BLACK, width=3)

    def rect(x0, y0, x1, y1, c=BLACK):
        d.rectangle([P(x0, y0), P(x1, y1)], fill=c)

    def disc(cx, cy, r, c=BLACK):
        d.ellipse([P(cx - r, cy - r), P(cx + r, cy + r)], fill=c)

    # letter R. cap height 4..44
    rect(11, 4, 18, 44)                       # stem
    rect(18, 4, 27, 24)                       # bowl, outer
    disc(27, 14, 10)
    rect(18, 5.6, 25, 22.4, WHITE)            # counter
    disc(25, 14, 8.4, WHITE)
    rect(11, 4, 18, 44)                       # restore stem edge
    # leg: thick diagonal from the bowl to the baseline, ending in a flat hairline serif
    d.polygon([P(23, 23), P(29.5, 23), P(41.5, 42.8), P(35, 42.8)], fill=BLACK)
    d.polygon([P(18, 22.4), P(27, 22.4), P(27, 24), P(18, 24)], fill=BLACK)
    # flat hairline serifs (the Romain du Roi's signature)
    rect(6, 4, 18, 5.4)
    rect(6, 42.6, 23, 44)
    rect(32, 42.6, 46, 44)
    # the stroke-end flick on the leg: a little kink to the right
    d.polygon([P(41.5, 42.8), P(35, 42.8), P(36, 41), P(44, 42.6)], fill=BLACK)
    # compass work in red
    def circ(cx, cy, r):
        d.ellipse([P(cx - r, cy - r), P(cx + r, cy + r)], outline=RED, width=3)
        x, y = P(cx, cy)
        d.line([x - 14, y, x + 14, y], fill=RED, width=3)
        d.line([x, y - 14, x, y + 14], fill=RED, width=3)
    circ(27, 14, 10)
    circ(25, 14, 8.4)
    d.line([P(23, 23), P(41.5, 42.8)], fill=RED, width=3)
    d.line([P(29.5, 23), P(47, 41.7)], fill=RED, width=3)
    im = snap(big.resize((W, H), Image.LANCZOS))
    t = draw1(im)
    x0 = 285
    t.text((x0, 30), "ROMAIN", font=font("Inter-Bold.otf", 18), fill=BLACK)
    t.text((x0, 50), "DU ROI", font=font("Inter-Bold.otf", 18), fill=BLACK)
    t.text((x0, 76), "Paris, 1692", font=font("Inter-Medium.otf", 10), fill=RED)
    f = font("Inter-Regular.otf", 10)
    body = ["The king's committee", "drew every capital on", "a grid of 48 × 48:",
            "2,304 squares a letter.", "", "The first type made", "by ruler and compass",
            "before a punch was cut.", "", "Truchet sat on it."]
    for i, s in enumerate(body):
        t.text((x0, 98 + i * 14), s, font=f, fill=BLACK)
    t.text((x0, 252), "48 × 48", font=font("InterDisplay-Black.otf", 22), fill=BLACK)
    mark(t, W - 12, H - 12)
    return im


# ------------------------------------------------------------- 4. Nonogram
PUZZLE = [
    "...............",
    "......#........",
    ".....###.##....",
    "....#####.#....",
    "...#########...",
    "..###########..",
    ".#############.",
    "...#.##.##.#...",
    "...#.##.##.#...",
    "...#########...",
    ".#############.",
    "###############",
    "...............",
    ".##...##...##..",
    "###############",
]


def runs(line):
    out, n = [], 0
    for c in line:
        if c:
            n += 1
        elif n:
            out.append(n); n = 0
    if n:
        out.append(n)
    return out or [0]


def line_options(clue, n):
    if clue == [0]:
        return [[0] * n]
    res = []
    def rec(i, pos, acc):
        if i == len(clue):
            res.append(acc + [0] * (n - len(acc)))
            return
        for s in range(pos, n - sum(clue[i:]) - (len(clue) - i - 1) + 1):
            seg = acc + [0] * (s - len(acc)) + [1] * clue[i]
            if i < len(clue) - 1:
                seg = seg + [0]
            rec(i + 1, len(seg), seg)
    rec(0, 0, [])
    return [r[:n] for r in res]


def solve(rc, cc, n):
    """Line-solve; returns grid of 1/0/-1 (unknown)."""
    g = [[-1] * n for _ in range(n)]
    ro = [line_options(c, n) for c in rc]
    co = [line_options(c, n) for c in cc]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            ro[i] = [o for o in ro[i] if all(g[i][j] in (-1, o[j]) for j in range(n))]
            for j in range(n):
                vals = {o[j] for o in ro[i]}
                if len(vals) == 1 and g[i][j] == -1:
                    g[i][j] = vals.pop(); changed = True
        for j in range(n):
            co[j] = [o for o in co[j] if all(g[i][j] in (-1, o[i]) for i in range(n))]
            for i in range(n):
                vals = {o[i] for o in co[j]}
                if len(vals) == 1 and g[i][j] == -1:
                    g[i][j] = vals.pop(); changed = True
    return g


def nonogram():
    sol = [[1 if c == "#" else 0 for c in r] for r in PUZZLE]
    n = len(sol)
    rc = [runs(r) for r in sol]
    cc = [runs([sol[i][j] for i in range(n)]) for j in range(n)]
    g = solve(rc, cc, n)
    assert all(v != -1 for r in g for v in r), "puzzle is not line-solvable"
    assert g == sol
    im = Image.new("RGB", (W, H), WHITE)
    d = draw1(im)
    C = 14
    gx, gy = 58, 72
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    fr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
    start = max(range(n), key=lambda i: sum(rc[i]))  # the full row: where to begin
    for i, clue in enumerate(rc):
        s = " ".join(map(str, clue))
        w = d.textlength(s, font=f)
        d.text((gx - 5 - w, gy + i * C + 2), s, font=fr if i == start else f,
               fill=RED if i == start else BLACK)
    for j, clue in enumerate(cc):
        for k, v in enumerate(reversed(clue)):
            s = str(v)
            w = d.textlength(s, font=f)
            d.text((gx + j * C + (C - w) / 2 + 0.5, gy - 13 - k * 11), s, font=f, fill=BLACK)
    for k in range(n + 1):
        wd = 2 if k % 5 == 0 else 1
        d.line([gx + k * C, gy, gx + k * C, gy + n * C], fill=BLACK, width=wd)
        d.line([gx, gy + k * C, gx + n * C, gy + k * C], fill=BLACK, width=wd)
    # a red tick in the margin beside the starting row
    d.polygon([(gx + n * C + 4, gy + start * C + C // 2), (gx + n * C + 10, gy + start * C + 3),
               (gx + n * C + 10, gy + start * C + C - 3)], fill=RED)
    x0 = 290
    d.text((x0, 72), "NONOGRAM", font=font("Inter-Bold.otf", 13), fill=BLACK)
    d.text((x0, 89), "No. 1", font=font("Inter-Medium.otf", 10), fill=RED)
    fb = font("Inter-Regular.otf", 10)
    lines = ["Shade each row", "and column in runs", "of the given lengths,", "in order, with gaps.",
             "", "Begin at the red.", "", "The picture is of", "something that kept",
             "dry on the night of", "11 October 1634."]
    assert all(d.textlength(t, font=fb) <= W - 6 - x0 for t in lines)
    for i, s in enumerate(lines):
        d.text((x0, 108 + i * 13), s, font=fb, fill=BLACK)
    mark(d, W - 12, H - 12)
    return im


# ------------------------------------------------------------- 5. first frost (DLA)
def frost():
    rng = np.random.default_rng(20261011)
    gw, gh = 200, 150          # 2 px cells
    occ = np.zeros((gh, gw), bool)
    occ[gh - 1, :] = True      # the bottom of the glass
    parent = -np.ones((gh, gw, 2), int)
    order = np.zeros((gh, gw), int)
    top = gh - 1
    nw = 500
    def spawn(k):
        y = np.full(k, max(top - 25, 1))
        x = rng.integers(0, gw, k)
        return x, y
    wx, wy = spawn(nw)
    stuck, it = 0, 0
    nb = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while stuck < 9000 and top > 34 and it < 3000000:
        it += 1
        mv = rng.integers(0, 4, nw)
        wx = (wx + (mv == 0) - (mv == 1)) % gw
        wy = np.clip(wy + (mv == 2) - (mv == 3), 0, gh - 2)
        # too far above the frost: drift back down
        far = wy < top - 45
        wy[far] = max(top - 25, 1)
        near = np.zeros(nw, bool)
        for ddy, ddx in nb:
            near |= occ[np.clip(wy + ddy, 0, gh - 1), (wx + ddx) % gw]
        cand = np.nonzero(near & ~occ[wy, wx] & (rng.random(nw) < 0.9))[0]
        for k in cand:
            y, x = wy[k], wx[k]
            if occ[y, x]:
                continue
            ps = [(y + a, (x + b) % gw) for a, b in nb if 0 <= y + a < gh and occ[y + a, (x + b) % gw]]
            if not ps:
                continue
            py, px = ps[rng.integers(len(ps))]
            occ[y, x] = True
            parent[y, x] = (py, px)
            stuck += 1
            order[y, x] = stuck
            top = min(top, y)
            wx[k], wy[k] = rng.integers(0, gw), max(top - 25, 1)
    # lineage of the highest crystal
    ys, xs = np.nonzero(occ[:gh - 1])
    k = np.argmin(ys)
    y, x = ys[k], xs[k]
    path = []
    while parent[y, x][0] >= 0:
        path.append((y, x))
        y, x = parent[y, x]
    im = Image.new("RGB", (W, H), BLACK)
    a = np.array(im)
    big = np.kron(occ, np.ones((2, 2), bool))
    a[big] = WHITE
    for (y, x) in path:
        a[2 * y:2 * y + 2, 2 * x:2 * x + 2] = RED
    a[H - 2:, :] = WHITE
    im = Image.fromarray(a)
    d = draw1(im)
    d.text((14, 14), "FIRST FROST", font=font("Inter-Bold.otf", 13), fill=WHITE)
    d.text((14, 31), f"{stuck:,} random walks, each stopping where it touched.",
           font=font("Inter-Regular.otf", 9), fill=WHITE)
    d.text((14, 43), "Red: the one line from the highest crystal back to the glass.",
           font=font("Inter-Regular.otf", 9), fill=RED)
    mark(d, W - 12, 12)
    return im, stuck, len(path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save(strand(), 1)
    save(conus(), 2)
    save(romain(), 3)
    save(nonogram(), 4)
    im, s, p = frost()
    save(im, 5)
    print("frost:", s, "particles, path", p)
