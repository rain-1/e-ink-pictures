#!/usr/bin/env python3
"""2026-10-13 — five pictures for a 400x300 black/white/red e-ink panel.
Theme: lines people agree on.
1. Prime Meridian — Washington, 13 Oct 1884: Greenwich wins 22–1. The rival meridians it replaced, dotted.
2. Rungholt — a gradiometer plot of the town drowned in 1362; its church found by magnetism in 2023 (red).
3. (untitled) Kvæði — Faroese chain dance, two steps left and one back; time runs outward. No text.
4. Eratosthenes — one shadow, 7.2°, 1/50 of a circle; red = the same angle, twice.
5. Puzzle No. 3 — a Queens puzzle (one crown per row, column, region; none touching). Red = the walls.
Run: python3 generate.py <outdir>"""
import math, random, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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


# ------------------------------------------------------------- 1. Prime Meridian
def meridian():
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    cx, cy, R = 128 * S, 150 * S, 116 * S
    lat0 = math.radians(28)

    def proj(lat, lon):
        la, lo = math.radians(lat), math.radians(lon)
        x = math.cos(la) * math.sin(lo)
        y = math.cos(lat0) * math.sin(la) - math.sin(lat0) * math.cos(la) * math.cos(lo)
        vis = math.sin(lat0) * math.sin(la) + math.cos(lat0) * math.cos(la) * math.cos(lo)
        return cx + R * x, cy - R * y, vis > 0

    def curve(pts, fill, w, dash=None):
        seg = []
        segs = []
        for p in pts:
            x, y, v = p
            if v:
                seg.append((x, y))
            elif seg:
                segs.append(seg); seg = []
        if seg:
            segs.append(seg)
        for s in segs:
            if dash is None:
                d.line(s, fill=fill, width=w, joint="curve")
            else:
                on, off = dash
                acc, draw = 0.0, True
                for (x0, y0), (x1, y1) in zip(s, s[1:]):
                    L = math.hypot(x1 - x0, y1 - y0)
                    if draw:
                        d.line([(x0, y0), (x1, y1)], fill=fill, width=w)
                    acc += L
                    if acc >= (on if draw else off):
                        acc, draw = 0.0, not draw

    # engraved shading: horizontal hairlines on the night side (light from the upper left)
    for yy in range(cy - R, cy + R, 3 * S):
        dy = (yy - cy) / R
        half = math.sqrt(max(0, 1 - dy * dy))
        xs = np.linspace(-half, half, 300)
        z = np.sqrt(np.maximum(0, 1 - xs ** 2 - dy ** 2))
        lam = np.clip(-0.55 * xs - 0.45 * dy + 0.7 * z, 0, 1)
        dark = np.clip(0.62 - lam, 0, 1) ** 1.3
        for i in range(len(xs) - 1):
            t = dark[i]
            if t > 0.04:
                w = max(1, int(round(t * 1.7 * S)))
                d.line([(cx + R * xs[i], yy), (cx + R * xs[i + 1], yy)], fill=BLACK, width=w)
    # parallels
    for lat in range(-75, 90, 15):
        pts = [proj(lat, lo) for lo in np.arange(-180, 181, 1.0)]
        curve(pts, BLACK, 1 * S if lat else 2 * S)
    # the rival meridians of 1884, dashed
    rivals = {"Ferro": -17.66, "Cádiz": -6.20, "Paris": 2.34, "Rome": 12.45,
              "Pulkovo": 30.33, "Washington": -77.06, "Lisbon": -9.13, "Copenhagen": 12.58,
              "Stockholm": 18.06, "Rio": -43.18, "Jerusalem": 35.23}
    for lon in rivals.values():
        pts = [proj(la, lon) for la in np.arange(-90, 90.1, 0.5)]
        curve(pts, BLACK, int(1.6 * S), dash=(5 * S, 3.5 * S))
    # Greenwich, red
    pts = [proj(la, 0) for la in np.arange(-90, 90.1, 0.5)]
    curve(pts, RED, 3 * S)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLACK, width=2 * S)
    im = down(big)
    d = draw1(im)
    # Greenwich dot
    gx, gy, _ = proj(51.48, 0)
    gx, gy = gx / S, gy / S
    d.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=RED, outline=BLACK)

    x0 = 262
    fb = font("Inter-Bold.otf", 16)
    fr = font("Inter-Regular.otf", 10)
    d.text((x0, 18), "PRIME", font=fb, fill=BLACK)
    d.text((x0, 36), "MERIDIAN", font=fb, fill=BLACK)
    y = text_lines(d, x0, 64, ["Washington, 13 Oct 1884.", "Twenty-five nations vote", "on where zero should be."],
                   fr, maxw=W - x0 - 6)
    # the vote, as 25 squares: 22 for, 1 against, 2 abstain
    y += 8
    for i in range(25):
        bx, by = x0 + (i % 9) * 13, y + (i // 9) * 13
        if i < 22:
            d.rectangle([bx, by, bx + 9, by + 9], fill=BLACK)
        elif i == 22:
            d.rectangle([bx, by, bx + 9, by + 9], outline=BLACK)
            d.line([bx, by, bx + 9, by + 9], fill=BLACK)
            d.line([bx, by + 9, bx + 9, by], fill=BLACK)
        else:
            d.rectangle([bx, by, bx + 9, by + 9], outline=BLACK)
    y += 3 * 13 + 4
    fs = font("dj", 9)
    y = text_lines(d, x0, y, ["22 for Greenwich", "1 against: San Domingo", "2 abstain: France, Brazil"], fs, lead=12,
                   maxw=W - x0 - 6)
    y += 8
    y = text_lines(d, x0, y, ["Dashed: the zeros that", "lost — Paris, Ferro, Cádiz,", "Pulkovo, Rome, Rio …"],
                   fr, maxw=W - x0 - 6)
    mark(d, W - 8, H - 8)
    return im


# ------------------------------------------------------------- 2. Rungholt
def rungholt(seed=1362):
    rng = np.random.default_rng(seed)
    # 1 px = 1 m. A synthetic gradiometer survey (nT), in the style of the 2023 Kiel/Mainz plots.
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    field = np.zeros((H, W))

    def smooth_noise(scale, amp):
        n = rng.normal(size=(H // scale + 3, W // scale + 3))
        im = Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8))
        im = im.resize(((W // scale + 3) * scale, (H // scale + 3) * scale), Image.BICUBIC)
        a = np.asarray(im).astype(float)[:H, :W] / 255 - 0.5
        return a * amp

    field += smooth_noise(40, 1.0) + smooth_noise(9, 0.5)
    # tidal creek (priel) sediments: meandering low band
    cpath = 120 + 40 * np.sin(xx / 70 + 1.3) + 14 * np.sin(xx / 23)
    field -= 1.8 * np.exp(-((yy - cpath) / 9) ** 2) * (xx > 210)
    # medieval drainage ditches: a rectilinear field system, slightly skewed
    ang = math.radians(8)
    u = xx * math.cos(ang) + yy * math.sin(ang)
    v = -xx * math.sin(ang) + yy * math.cos(ang)
    ditch = (np.abs(((u + 7) % 31) - 15.5) > 14.4) & (v > 150) & (v < 262) & (u > 215)
    ditch |= (np.abs(((v + 3) % 47) - 23.5) > 22.4) & (u > 215) & (u < 340) & (v > 140) & (v < 262)
    field -= 2.2 * ditch
    # a chain of terps (dwelling mounds): positive anomaly with a negative halo to the north
    terps = [(52, 64, 26), (118, 82, 31), (188, 104, 36), (262, 92, 28), (332, 70, 25), (372, 196, 22)]
    for (tx, ty, tr) in terps:
        r = np.hypot(xx - tx, (yy - ty) * 1.15)
        field += 1.0 * np.exp(-(r / tr) ** 4)
        field -= 0.9 * np.exp(-((xx - tx) ** 2 + (yy - ty + tr * 0.9) ** 2) / (tr * 0.7) ** 2)
        # hearths and wells: small strong dipoles
        for _ in range(4):
            a, rr = rng.uniform(0, 2 * math.pi), rng.uniform(0, tr * 0.7)
            px, py = tx + rr * math.cos(a), ty + rr * math.sin(a)
            field += 3.5 * np.exp(-((xx - px) ** 2 + (yy - py) ** 2) / 5)
            field -= 2.5 * np.exp(-((xx - px) ** 2 + (yy - py + 3) ** 2) / 5)
    # the church: brick foundations, 40 x 15 m, east–west, on the big terp
    chx, chy = 188, 104
    cw, chh = 40, 15
    inside = (np.abs(xx - chx) < cw / 2) & (np.abs(yy - chy) < chh / 2)
    wall = inside & ~((np.abs(xx - chx) < cw / 2 - 2.5) & (np.abs(yy - chy) < chh / 2 - 2.5))
    field += 4.5 * wall
    # survey traverse striping: each 1 m line has a small offset
    field += rng.normal(0, 0.18, size=(H, 1)) * (xx < 400)
    field += rng.normal(0, 0.12, size=(H, W))
    # grey map, 0 = black (high nT)
    z = (field - np.median(field)) / field.std()
    g = np.clip(0.72 - 0.30 * z, 0, 1)
    gi = Image.fromarray((g * 255).astype(np.uint8), "L").convert("1")  # Floyd–Steinberg
    im = gi.convert("RGB")
    d = draw1(im)
    # the church, traced in red (offset ring so the anomaly still shows through)
    x0, y0, x1, y1 = chx - cw // 2 - 4, chy - chh // 2 - 4, chx + cw // 2 + 3, chy + chh // 2 + 3
    d.rectangle([x0, y0, x1, y1], outline=RED, width=2)
    d.line([x1, y1, x1 + 22, y1 + 34], fill=RED, width=1)
    # caption panel
    px, py, pw, ph = 12, 212, 186, 76
    d.rectangle([px, py, px + pw, py + ph], fill=WHITE, outline=BLACK)
    d.text((px + 8, py + 7), "RUNGHOLT", font=font("Inter-Bold.otf", 15), fill=BLACK)
    text_lines(d, px + 8, py + 29, ["Drowned 16 January 1362.", "Its church, found in 2023", "by the magnetism of its bricks."],
               font("Inter-Regular.otf", 10), maxw=pw - 12)
    # label for the church
    lx, ly = x1 + 24, y1 + 34
    d.rectangle([lx - 2, ly, lx + 74, ly + 13], fill=WHITE)
    d.text((lx, ly + 1), "church, 40 × 15 m", font=font("dj", 9), fill=RED)
    # scale bar 50 m and north
    sx, sy = 300, 276
    d.rectangle([sx - 6, sy - 14, sx + 92, sy + 12], fill=WHITE)
    d.rectangle([sx, sy, sx + 50, sy + 3], fill=BLACK)
    d.rectangle([sx + 25, sy + 1, sx + 49, sy + 2], fill=WHITE)
    d.text((sx, sy - 12), "50 m", font=font("dj", 9), fill=BLACK)
    d.text((sx + 60, sy - 12), "N", font=font("Inter-Bold.otf", 10), fill=BLACK)
    d.polygon([(sx + 64, sy - 1), (sx + 60, sy + 9), (sx + 68, sy + 9)], fill=BLACK)
    mark(d, W - 8, 4)
    return im


# ------------------------------------------------------------- 3. Kvæði (chain dance)
def chain_dance():
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    cx, cy = 200 * S, 150 * S
    r0, r1 = 22 * S, 146 * S
    n = 16                    # dancers
    beats = 3 * 9             # 9 bars of three steps
    step = math.radians(11.0)  # each step, around the ring
    phase = 2 * math.pi / n

    def offset(t):            # two steps left, one back, smoothed
        bar, f = divmod(t, 3.0)
        base = bar * 1.0
        k = int(f)
        e = (1 - math.cos(math.pi * (f - k))) / 2
        seq = [0, 1, 2, 1]
        return (base + seq[k] + (seq[k + 1] - seq[k]) * e) * step

    ts = np.linspace(0, beats, beats * 24)
    offs = np.array([offset(t) for t in ts])
    rad = r0 + (r1 - r0) * (ts / beats) ** 0.9
    red_i = 0
    for i in list(range(1, n)) + [red_i]:
        th = i * phase + offs - math.pi / 2
        pts = list(zip(cx + rad * np.cos(th), cy + rad * np.sin(th)))
        if i == red_i:
            d.line(pts, fill=WHITE, width=int(6 * S), joint="curve")
            d.line(pts, fill=RED, width=int(2.6 * S), joint="curve")
        else:
            d.line(pts, fill=BLACK, width=int(2.2 * S), joint="curve")
    # the linked hands: at the end of each bar, a faint ring of joined hands
    for b in range(0, 0):
        t = 3.0 * b
        rr = r0 + (r1 - r0) * (t / beats) ** 0.9
        if b % 2 == 0:
            for i in range(n):
                th = i * phase + offset(t) - math.pi / 2
                x, y = cx + rr * math.cos(th), cy + rr * math.sin(th)
                d.ellipse([x - 1.6 * S, y - 1.6 * S, x + 1.6 * S, y + 1.6 * S], fill=BLACK)
    im = down(big)
    d = draw1(im)
    mark(d, W - 8, H - 8)
    return im


# ------------------------------------------------------------- 4. Eratosthenes
def eratosthenes():
    S = 4
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    cx, cy, R = 112 * S, 290 * S, 196 * S
    ang = math.radians(7.2)
    syene = (cx, cy - R)
    alex = (cx - R * math.sin(ang), cy - R * math.cos(ang))
    # the red angle at the centre (the 1/50)
    d.pieslice([cx - R, cy - R, cx + R, cy + R], -90 - 7.2, -90, fill=RED)
    # Earth: concentric engraved strata, below the surface
    for k in range(1, 40):
        rr = R - k * 8 * S
        if rr <= 8 * S:
            break
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 180, 360, fill=BLACK, width=max(1, int(0.8 * S)))
    d.pieslice([cx - R + 3 * S, cy - R + 3 * S, cx + R - 3 * S, cy + R - 3 * S], -90 - 7.2, -90, fill=RED)
    d.arc([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=BLACK, width=int(2.4 * S))
    # radii
    d.line([syene, (cx, cy)], fill=BLACK, width=int(1.4 * S))
    d.line([alex, (cx, cy)], fill=BLACK, width=int(1.4 * S))
    # sun rays: vertical hairlines over the sky only
    for x in range(6 * S, 236 * S, 6 * S):
        dx = x - cx
        ytop = 0
        ysurf = cy - math.sqrt(max(0, R * R - dx * dx)) if abs(dx) < R else H * S
        if abs(x - syene[0]) < 3 * S:
            continue
        d.line([(x, ytop), (x, ysurf - 3 * S)], fill=BLACK, width=max(1, int(0.75 * S)))
    # the ray down the well at Syene (no shadow)
    d.line([(syene[0], 0), (syene[0], syene[1] + 30 * S)], fill=BLACK, width=int(1.4 * S))
    # well shaft
    wx = syene[0]
    d.rectangle([wx - 5 * S, syene[1] - 1 * S, wx - 3 * S, syene[1] + 34 * S], fill=BLACK)
    d.rectangle([wx + 3 * S, syene[1] - 1 * S, wx + 5 * S, syene[1] + 34 * S], fill=BLACK)
    d.ellipse([wx - 3 * S, syene[1] + 28 * S, wx + 3 * S, syene[1] + 34 * S], fill=WHITE, outline=BLACK, width=S)
    # gnomon at Alexandria: a tall obelisk along the radius (height exaggerated, angles true)
    gh = 48 * S
    ux, uy = math.sin(-ang), -math.cos(ang)  # outward radial direction
    top = (alex[0] + ux * gh, alex[1] + uy * gh)
    px, py = math.cos(ang), math.sin(-ang)   # tangent (to the east)
    # the sun ray grazing the gnomon tip, down to the ground: the shadow's end
    gx = top[0]
    dx = gx - cx
    gy = cy - math.sqrt(R * R - dx * dx)
    # the red angle at the tip, between gnomon and ray
    d.polygon([top, (gx, gy), alex], fill=RED)
    d.line([(gx, 0), (gx, gy)], fill=BLACK, width=int(1.4 * S))
    bw = 4.5 * S
    d.polygon([(alex[0] - px * bw, alex[1] - py * bw), (alex[0] + px * bw, alex[1] + py * bw),
               (top[0] + px * 0.8 * S, top[1] + py * 0.8 * S), (top[0] - px * 0.8 * S, top[1] - py * 0.8 * S)],
              fill=BLACK)
    # shadow on the ground
    d.line([alex, (gx, gy)], fill=BLACK, width=int(3 * S))
    im = down(big)
    d = draw1(im)
    fs = font("dj", 9)
    fr = font("Inter-Regular.otf", 10)
    # city labels
    sx, sy = syene[0] / S, syene[1] / S
    ax, ay = alex[0] / S, alex[1] / S
    for (lx, ly, s, anchor) in [(sx + 9, sy - 22, "Syene", "la"), (ax - 12, ay - 22, "Alexandria", "ra")]:
        tw = d.textlength(s, font=fs)
        bx = lx if anchor == "la" else lx - tw
        d.rectangle([bx - 2, ly - 1, bx + tw + 1, ly + 10], fill=WHITE)
        d.text((bx, ly), s, font=fs, fill=BLACK)
    d.text((cx / S + 22, cy / S - 22), "7.2°", font=font("Inter-Bold.otf", 10), fill=RED)
    x0 = 244
    d.text((x0, 14), "ERATOSTHENES", font=font("Inter-Bold.otf", 15), fill=BLACK)
    text_lines(d, x0, 38, ["Noon, midsummer, c. 240 BC.", "At Syene the sun lights the", "bottom of a well. At Alexandria",
                           "an obelisk casts a shadow."], fr, maxw=W - x0 - 4)
    # the arithmetic, inside the Earth
    ty = 196
    fb = font("Inter-Bold.otf", 11)
    d.rectangle([236, ty - 6, 396, ty + 64], fill=WHITE)
    d.text((244, ty), "7.2° = 1/50 of a circle", font=fb, fill=RED)
    text_lines(d, 244, ty + 18, ["5,000 stadia × 50", "= 250,000 stadia ≈ 40,000 km",
                                 "(obelisk not to scale; angles are)"], fs, lead=13, maxw=150)
    mark(d, W - 8, H - 8)
    return im


# ------------------------------------------------------------- 5. Puzzle No. 3 (Queens)
N = 9


def solve_queens(reg, limit=2):
    sols = []
    regcells = {}
    for r in range(N):
        for c in range(N):
            regcells.setdefault(reg[r][c], []).append((r, c))
    used_c, used_g = set(), set()
    cur = []

    def rec(r):
        if len(sols) >= limit:
            return
        if r == N:
            sols.append(list(cur)); return
        for c in range(N):
            if c in used_c or reg[r][c] in used_g:
                continue
            if cur and abs(cur[-1] - c) <= 1:
                continue
            used_c.add(c); used_g.add(reg[r][c]); cur.append(c)
            rec(r + 1)
            cur.pop(); used_c.discard(c); used_g.discard(reg[r][c])
    rec(0)
    return sols


def make_queens(seed=20261013):
    rng = random.Random(seed)
    while True:
        # a random arrangement of non-touching queens
        cols = list(range(N))
        rng.shuffle(cols)
        if any(abs(cols[i] - cols[i + 1]) <= 1 for i in range(N - 1)):
            continue
        reg = [[-1] * N for _ in range(N)]
        frontier = []
        for r, c in enumerate(cols):
            reg[r][c] = r
            frontier.append((r, c))
        # grow regions at random until the board is full
        while any(-1 in row for row in reg):
            r, c = rng.choice(frontier)
            nb = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= r + dr < N and 0 <= c + dc < N and reg[r + dr][c + dc] == -1]
            if not nb:
                frontier.remove((r, c)); continue
            rr, cc = rng.choice(nb)
            reg[rr][cc] = reg[r][c]
            frontier.append((rr, cc))
        sols = solve_queens(reg)
        if len(sols) == 1 and sols[0] == cols:
            sizes = [sum(row.count(k) for row in reg) for k in range(N)]
            if min(sizes) >= 3:
                return reg, cols


def queens_image(reg, cols=None):
    im = Image.new("RGB", (W, H), WHITE)
    d = draw1(im)
    cs = 30
    gx, gy = 14, 15
    # thin grid
    for i in range(N + 1):
        d.line([gx + i * cs, gy, gx + i * cs, gy + N * cs], fill=BLACK, width=1)
        d.line([gx, gy + i * cs, gx + N * cs, gy + i * cs], fill=BLACK, width=1)
    # red walls between regions
    for r in range(N):
        for c in range(N):
            x, y = gx + c * cs, gy + r * cs
            if c + 1 < N and reg[r][c] != reg[r][c + 1]:
                d.rectangle([x + cs - 1, y - 1, x + cs + 1, y + cs + 1], fill=RED)
            if r + 1 < N and reg[r][c] != reg[r + 1][c]:
                d.rectangle([x - 1, y + cs - 1, x + cs + 1, y + cs + 1], fill=RED)
    d.rectangle([gx - 1, gy - 1, gx + N * cs + 1, gy + N * cs + 1], outline=BLACK, width=3)
    if cols:
        for r, c in enumerate(cols):
            x, y = gx + c * cs + cs // 2, gy + r * cs + cs // 2
            crown(d, x, y)
    x0 = gx + N * cs + 14
    d.text((x0, 16), "PUZZLE", font=font("Inter-Bold.otf", 14), fill=BLACK)
    d.text((x0, 32), "No. 3", font=font("Inter-Bold.otf", 14), fill=BLACK)
    fr = font("Inter-Regular.otf", 10)
    text_lines(d, x0, 60, ["Place nine", "crowns:", "", "one in each", "row,", "column,", "and walled", "region.", "",
                           "No two may", "touch, not", "even at a", "corner."], fr, maxw=W - x0 - 4)
    crown(d, x0 + 10, 252)
    d.text((x0, 272), "solution in archive", font=font("dj", 9), fill=BLACK)
    return im


def crown(d, x, y):
    d.polygon([(x - 8, y + 6), (x - 9, y - 5), (x - 4, y), (x, y - 8), (x + 4, y), (x + 9, y - 5), (x + 8, y + 6)],
              fill=BLACK)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save(meridian(), "1.png")
    save(rungholt(), "2.png")
    save(chain_dance(), "3.png")
    save(eratosthenes(), "4.png")
    reg, cols = make_queens()
    save(queens_image(reg), "5.png")
    save(queens_image(reg, cols), "solution.png")
    with open(os.path.join(OUT, "solutions.txt"), "w") as f:
        f.write("Puzzle No. 3 (Queens) — crown in each row, as column numbers 1–9 from the left:\n")
        f.write(" ".join(str(c + 1) for c in cols) + "\n")
