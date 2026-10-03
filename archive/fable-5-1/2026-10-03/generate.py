"""fable-5-1 / 2026-10-03 — "Traces".
Things that leave a record of their own motion: sand on a bowed plate, an ant's
walk, a pendulum's pen, a loom's draft, and the first transistor (patent granted today, 1950).
Style: engraved hairline plates. No dithering. Draw at 4x, box-downsample, snap to
3 inks; text is drawn last at 1x with no antialiasing.
Run: python generate.py <outdir>
"""
import sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 4
W, H = 400 * S, 300 * S
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, px): return ImageFont.truetype(FD + name, px * S)
MONO = lambda px: font("DejaVuSansMono.ttf", px)
MONOB = lambda px: font("DejaVuSansMono-Bold.ttf", px)
SERIF = lambda px: font("DejaVuSerif.ttf", px)
PAL = list(BLACK + WHITE + RED) + [0] * (256 - 3) * 3

TEXTS = []
def text(xy, s, f, fill, anchor="la", spacing=0):
    """Queue text (coords in 4x space); drawn at native 1x, no AA, after snapping."""
    TEXTS.append(((xy[0] / S, xy[1] / S), s, f.path, f.size // S, fill, anchor, spacing))

def _draw_texts(out):
    d = ImageDraw.Draw(out)
    d.fontmode = "1"
    idx = {BLACK: 0, WHITE: 1, RED: 2}
    for (x, y), s, path, px, fill, anchor, spacing in TEXTS:
        f = ImageFont.truetype(path, px)
        if spacing:
            ws = [d.textlength(c, font=f) for c in s]
            total = sum(ws) + spacing * (len(s) - 1)
            if anchor[0] == "m": x -= total / 2
            elif anchor[0] == "r": x -= total
            for c, w in zip(s, ws):
                d.text((round(x), round(y)), c, font=f, fill=idx[fill], anchor="l" + anchor[1])
                x += w + spacing
        else:
            d.text((round(x), round(y)), s, font=f, fill=idx[fill], anchor=anchor)
    TEXTS.clear()

def from_idx(idx):
    out = Image.fromarray(idx.astype(np.uint8), "P")
    out.putpalette(PAL)
    _draw_texts(out)
    return out

def snap(img):
    a = np.asarray(img.resize((400, 300), Image.BOX)).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    redness = r - np.maximum(g, b)
    lum = (r + g + b) / 3
    return from_idx(np.where(redness > 90, 2, np.where(lum > 120, 1, 0)))

# ------------------------------------------------------------ 1. Chladni (no text)
def chladni():
    rng = np.random.default_rng(20261003)
    n, m = 9, 4
    def u(x, y):  # free square plate, clamped at centre: symmetric mode combination
        return (np.cos(n * np.pi * x) * np.cos(m * np.pi * y)
                + np.cos(m * np.pi * x) * np.cos(n * np.pi * y))
    def grad(x, y):
        ux = (-n * np.pi * np.sin(n * np.pi * x) * np.cos(m * np.pi * y)
              - m * np.pi * np.sin(m * np.pi * x) * np.cos(n * np.pi * y))
        uy = (-m * np.pi * np.cos(n * np.pi * x) * np.sin(m * np.pi * y)
              - n * np.pi * np.cos(m * np.pi * x) * np.sin(n * np.pi * y))
        return ux, uy
    N = 70000
    x, y = rng.random(N), rng.random(N)
    for it in range(140):
        v = u(x, y)
        ux, uy = grad(x, y)
        # grains on vibrating regions get kicked; drift down |u|^2
        kick = np.abs(v) * 0.006 + 0.0007
        x += -0.0005 * v * ux + rng.normal(0, 1, N) * kick
        y += -0.0005 * v * uy + rng.normal(0, 1, N) * kick
        # grains bounce off plate edges
        x = np.abs(x); x = 1 - np.abs(1 - x)
        y = np.abs(y); y = 1 - np.abs(1 - y)
    P, ox, oy = 272, 64, 14
    idx = np.zeros((300, 400), np.uint8)
    # plate outline: a white hairline frame, 3px off the plate
    idx[oy - 4, ox - 4:ox + P + 4] = 1; idx[oy + P + 3, ox - 4:ox + P + 4] = 1
    idx[oy - 4:oy + P + 4, ox - 4] = 1; idx[oy - 4:oy + P + 4, ox + P + 3] = 1
    px = np.clip((x * (P - 1)).astype(int), 0, P - 1) + ox
    py = np.clip((y * (P - 1)).astype(int), 0, P - 1) + oy
    idx[py, px] = 1
    # red: the clamp at the centre, and the bow drawn across the right edge
    yy, xx = np.mgrid[0:300, 0:400]
    c = (ox + P / 2 - 0.5, oy + P / 2 - 0.5)
    rr = np.hypot(xx - c[0], yy - c[1])
    idx[rr < 4.5] = 2
    idx[(rr < 2)] = 0
    bx = ox + P + 3
    for k in range(-1, 2):          # three hair strands of the bow
        idx[oy + 70: oy + 200, bx + 6 + k * 2] = 2
    idx[oy + 66: oy + 70, bx + 3: bx + 11] = 2
    idx[oy + 200: oy + 204, bx + 3: bx + 11] = 2
    idx[oy + 96: oy + 100, bx: bx + 6] = 2   # where the hair touches the plate
    return from_idx(idx)

# ------------------------------------------------------------ 2. Path integration
def ants():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    rnd = random.Random(1003)
    nest = (300 * S, 236 * S)
    # outbound: a correlated random walk with a weak pull away from home
    x, y = nest
    th = math.radians(-150)
    pts = [(x, y)]
    total = 0
    for i in range(900):
        th += rnd.gauss(0, 0.2)
        ax = math.atan2(y - nest[1], x - nest[0])
        th += 0.03 * math.sin(ax - th) if i > 40 else 0
        step = 3.2 * S * 0.5
        nx, ny = x + step * math.cos(th), y + step * math.sin(th)
        if not (20 * S < nx < 380 * S and 40 * S < ny < 262 * S):
            th += math.pi * 0.6
            continue
        x, y = nx, ny
        total += step
        pts.append((x, y))
    food = (x, y)
    d.line(pts, fill=BLACK, width=S, joint="curve")
    # the crumb she found
    d.rectangle([food[0] - 3 * S, food[1] - 3 * S, food[0] + 3 * S, food[1] + 3 * S], fill=BLACK)
    # home: one straight red line, ending a little short (path integration has error)
    err = (9 * S, -6 * S)
    end = (nest[0] + err[0], nest[1] + err[1])
    d.line([food, end], fill=RED, width=2 * S)
    # systematic search: widening loops around where she believes home is
    sp = []
    for k in range(240):
        a = k * 0.21
        r = (0.5 + 0.045 * k) * S * (1 + 0.45 * math.sin(a * 1.618))
        sp.append((end[0] + r * math.cos(a), end[1] + r * math.sin(a)))
    d.line(sp, fill=RED, width=S, joint="curve")
    # nest entrance: a ring
    d.ellipse([nest[0] - 5 * S, nest[1] - 5 * S, nest[0] + 5 * S, nest[1] + 5 * S], outline=BLACK, width=S)
    d.ellipse([nest[0] - 1.5 * S, nest[1] - 1.5 * S, nest[0] + 1.5 * S, nest[1] + 1.5 * S], fill=BLACK)
    # scale bar: 1 px at 1x = 5 cm of salt pan
    mpp = 0.25
    L = 10 / mpp  # 10 m in px
    sx, sy = 16 * S, 282 * S
    d.line([sx, sy, sx + L * S, sy], fill=BLACK, width=S)
    for t in (0, L / 2, L):
        d.line([sx + t * S, sy - 3 * S, sx + t * S, sy], fill=BLACK, width=S)
    text((sx + L * S + 6 * S, sy - 4 * S), "10 m", MONO(9), BLACK)
    out_m = total / S * mpp
    home_m = math.dist(food, nest) / S * mpp
    text((16 * S, 12 * S), "PATH INTEGRATION", MONOB(12), BLACK, spacing=3)
    text((16 * S, 28 * S), "Cataglyphis fortis, salt pan, Tunisia", SERIF(10), BLACK)
    text((384 * S, 12 * S), f"out  {out_m:5.0f} m", MONO(9), BLACK, "ra")
    text((384 * S, 24 * S), f"home {home_m:5.0f} m", MONO(9), RED, "ra")
    text((nest[0] + 22 * S, nest[1] + 10 * S), "nest", MONO(9), BLACK)
    text((384 * S, 278 * S), "she wanders; she walks home in one line.", SERIF(10), BLACK, "rs")
    return snap(img)

# ------------------------------------------------------------ 3. Point contact
def transistor():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    cx = 200 * S
    yy, xx = np.mgrid[0:H, 0:W]
    ink = np.zeros((H, W), bool)
    # metal base: solid black block, engraved with white hairlines that widen downward
    by0, by1 = 216 * S, 248 * S
    base = (abs(xx - cx) < 92 * S) & (yy >= by0) & (yy < by1)
    rows = ((yy - by0) // S) % 3
    base_ink = base & ~((rows == 0) & ((yy - by0) > 4 * S) & (abs(xx - cx) < 88 * S))
    # germanium slab: vertical line screen, period 3px, heavier at the edges (a round-ish crystal)
    gy0, gy1 = 180 * S, 216 * S
    slab = (abs(xx - cx) < 56 * S) & (yy >= gy0) & (yy < gy1)
    t = np.abs(xx - cx) / (56 * S)
    wpx = (0.6 + 1.6 * t ** 2) * S
    slab_ink = slab & (((xx - cx) % (3 * S)) < wpx)
    slab_ink |= slab & ((yy < gy0 + S) | (yy >= gy1 - S) | (abs(xx - cx) >= 55 * S))
    # wedge: polystyrene triangle with horizontal hairlines, line weight grows toward the apex
    top = 98 * S
    half = 48 * S
    frac = (yy - top) / (gy0 - top)
    inside = (yy >= top) & (yy < gy0) & (np.abs(xx - cx) < half * (1 - frac))
    wl = (0.5 + 1.8 * frac) * S
    wedge_ink = inside & (((yy - top) % (4 * S)) < wl)
    ink |= base_ink | slab_ink | wedge_ink
    img = Image.fromarray(np.where(ink[..., None], 0, 255).astype(np.uint8).repeat(3, 2))
    d = ImageDraw.Draw(img)
    L, R, T = (cx - half, top), (cx + half, top), (cx, gy0)
    # gold foil along both faces, slit at the apex by a razor blade
    d.line([L, (cx - 2 * S, gy0 - 1 * S)], fill=BLACK, width=3 * S)
    d.line([R, (cx + 2 * S, gy0 - 1 * S)], fill=BLACK, width=3 * S)
    d.line([L[0], top, R[0], top], fill=BLACK, width=S)
    # spring pressing the wedge onto the crystal
    zig = [(cx, top)]
    for i in range(1, 10):
        zig.append((cx + (7 * S if i % 2 else -7 * S), top - i * 4.5 * S))
    zig.append((cx, 52 * S))
    d.line(zig, fill=BLACK, width=S, joint="curve")
    d.line([cx - 34 * S, 52 * S, cx + 34 * S, 52 * S], fill=BLACK, width=3 * S)
    # leads out to the signals
    ly = 158 * S
    lx, rx = L[0] - 46 * S, R[0] + 46 * S
    d.line([L, (lx, top), (lx, ly - 6 * S)], fill=BLACK, width=S)
    d.line([R, (rx, top), (rx, ly - 26 * S)], fill=BLACK, width=S)
    d.line([cx, by1, cx, 256 * S], fill=BLACK, width=S)
    def wave(x0, x1, y0, amp, cyc):
        pts = [(x, y0 - amp * math.sin((x - x0) / (x1 - x0) * cyc * 2 * math.pi))
               for x in range(int(x0), int(x1) + 1, S)]
        d.line(pts, fill=RED, width=2 * S, joint="curve")
    wave(lx - 36 * S, lx + 36 * S, ly + 6 * S, 3 * S, 3)
    wave(rx - 36 * S, rx + 36 * S, ly + 6 * S, 26 * S, 3)
    text((lx, 196 * S), "EMITTER", MONO(9), BLACK, "ma", spacing=1)
    text((rx, 196 * S), "COLLECTOR", MONO(9), BLACK, "ma", spacing=1)
    text((cx + 6 * S, 254 * S), "BASE", MONO(9), BLACK, "lm", spacing=1)
    text((16 * S, 12 * S), "US 2,524,035", MONOB(12), BLACK, spacing=3)
    text((16 * S, 28 * S), "granted 3 Oct 1950", SERIF(10), BLACK)
    text((384 * S, 12 * S), "germanium, gold foil,", MONO(9), BLACK, "ra")
    text((384 * S, 24 * S), "a razor cut, a spring", MONO(9), BLACK, "ra")
    text((cx, 282 * S), "a whisper in, a voice out.", SERIF(10), RED, "ma")
    return snap(img)


# ------------------------------------------------------------ 4. Harmonograph
def harmonograph():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    f1, f2 = 2.0, 3.0 * 1.004
    T = 260.0
    ts = np.linspace(0, T, 60000)
    x = (np.sin(f1 * ts + 0.3) * np.exp(-0.006 * ts) + 0.35 * np.sin(f2 * ts + 1.1) * np.exp(-0.009 * ts))
    y = (np.sin(f2 * ts + 0.0) * np.exp(-0.007 * ts) + 0.30 * np.sin(f1 * ts + 2.0) * np.exp(-0.005 * ts))
    sx = 200 * S + x * 118 * S
    sy = 142 * S + y * 104 * S
    cut = int(len(ts) * 0.93)
    step = 6
    pts = list(zip(sx[:cut:step], sy[:cut:step]))
    d.line(pts, fill=WHITE, width=S, joint="curve")
    pts = list(zip(sx[cut - step::step], sy[cut - step::step]))
    d.line(pts, fill=RED, width=2 * S, joint="curve")
    d.ellipse([sx[-1] - 3 * S, sy[-1] - 3 * S, sx[-1] + 3 * S, sy[-1] + 3 * S], fill=RED)
    text((16 * S, 280 * S), "HARMONOGRAPH", MONOB(11), WHITE, "ls", spacing=3)
    text((16 * S, 292 * S), "two pendulums, 2 : 3, one slightly out of tune", MONO(9), WHITE, "ls")
    text((384 * S, 292 * S), "until it stops.", SERIF(10), RED, "rs")
    return snap(img)

# ------------------------------------------------------------ 5. Weaving draft
def weaving():
    C = 6                       # cell size at 1x
    shafts, cols, rows = 4, 40, 36
    # threading: point-twill runs whose lengths come from today's date, then mirrored
    runs = [int(c) + 3 for c in "20261003"]
    th, s, dr = [], 0, 1
    for r in runs:
        for _ in range(r):
            th.append(s); s = (s + dr) % shafts
        dr = -dr
    half_ = th[:cols // 2]
    th = half_ + half_[::-1]
    tie = [[1 if (t - sh) % 4 in (0, 1) else 0 for sh in range(4)] for t in range(4)]  # 2/2 twill
    tr = [th[j % cols] for j in range(rows)]   # tromp as writ: treadle as threaded
    red_picks = set(range(16, 20))                    # one red stripe in the weft
    idx = np.ones((300, 400), np.uint8)
    x0, y0 = 122, 44
    tx0 = x0 + cols * C + C
    ty0 = 12
    def cell(gx, gy, v):
        idx[gy + 1:gy + C, gx + 1:gx + C] = v
    def grid(gx, gy, nx, ny):
        for i in range(nx + 1): idx[gy:gy + ny * C + 1, gx + i * C] = 0
        for j in range(ny + 1): idx[gy + j * C, gx:gx + nx * C + 1] = 0
    grid(x0, ty0, cols, shafts)
    for i in range(cols):
        cell(x0 + (cols - 1 - i) * C, ty0 + (shafts - 1 - th[i]) * C, 0)
    grid(tx0, ty0, 4, shafts)
    for t in range(4):
        for sh in range(4):
            if tie[t][sh]: cell(tx0 + t * C, ty0 + (shafts - 1 - sh) * C, 0)
    grid(tx0, y0, 4, rows)
    for j in range(rows):
        cell(tx0 + tr[j] * C, y0 + j * C, 2 if j in red_picks else 0)
    # drawdown: warp up -> black; weft up -> white (red in the stripe)
    for j in range(rows):
        for i in range(cols):
            up = tie[tr[j]][th[i]]
            gx = x0 + (cols - 1 - i) * C
            gy = y0 + j * C
            idx[gy:gy + C, gx:gx + C] = 0 if up else (2 if j in red_picks else 1)
    out = from_idx(idx)
    d = ImageDraw.Draw(out); d.fontmode = "1"
    fb = ImageFont.truetype(FD + "DejaVuSansMono-Bold.ttf", 12)
    fm = ImageFont.truetype(FD + "DejaVuSansMono.ttf", 9)
    fs = ImageFont.truetype(FD + "DejaVuSerif.ttf", 10)
    d.text((16, 14), "D R A F T", font=fb, fill=0)
    d.text((16, 30), "No. 1003", font=fm, fill=0)
    for k, s_ in enumerate(["threading  ^", "tie-up    ^>", "treadling  >"]):
        d.text((16, 60 + k * 12), s_, font=fm, fill=0)
    d.text((16, 106), "4 shafts", font=fm, fill=0)
    d.text((16, 118), "4 treadles", font=fm, fill=0)
    d.text((16, 130), "2/2 twill,", font=fm, fill=0)
    d.text((16, 142), "tromp as writ", font=fm, fill=0)
    d.text((16, 166), "four picks", font=fm, fill=2)
    d.text((16, 178), "of red weft", font=fm, fill=2)
    for k, s_ in enumerate(["The whole cloth", "is already here,", "in the margins."]):
        d.text((16, 246 + k * 13), s_, font=fs, fill=0)
    return out


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    for i, fn in enumerate([chladni, ants, transistor, harmonograph, weaving], 1):
        fn().save(f"{out}/{i}.png")
