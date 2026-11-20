#!/usr/bin/env python3
"""2026-11-19 — "Plates": five atlas plates for a 400x300 black/white/red e-ink screen.
Run from this directory: python3 generate.py  (writes 1.png .. 5.png here)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S = 400, 300, 4
K, WH, R = (0, 0, 0), (255, 255, 255), (255, 0, 0)
PAL = np.array([K, WH, R], dtype=np.int32)
FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size): return ImageFont.truetype(FD + name + ".ttf", size)
MONO = lambda s: font("DejaVuSansMono", s)
MONOB = lambda s: font("DejaVuSansMono-Bold", s)
SANSB = lambda s: font("DejaVuSans-Bold", s)
SERIF = lambda s: font("DejaVuSerif", s)
SERIFI = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", s)

def snap(img):
    """Force every pixel to the nearest of the three inks (no dithering: crisp)."""
    a = np.asarray(img.convert("RGB"), dtype=np.int32)
    d = ((a[:, :, None, :] - PAL[None, None]) ** 2).sum(-1)
    return Image.fromarray(PAL[d.argmin(-1)].astype(np.uint8), "RGB")

def big(bg): 
    im = Image.new("RGB", (W * S, H * S), bg); return im, ImageDraw.Draw(im)
def down(im): return snap(im.resize((W, H), Image.LANCZOS))
def pen(im):
    d = ImageDraw.Draw(im); d.fontmode = "1"; return d
def save(im, n):
    im = snap(im)
    p = Image.new("P", (1, 1)); p.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0] * 759)
    im.quantize(palette=p, dither=Image.NONE).save(f"{n}.png", optimize=True)
def sig(d, n, title, fill, xy=(8, 287)):
    d.text(xy, f"{n}/V  {title}  19·XI·2026", font=MONO(8), fill=fill)

# ---------------------------------------------------------------- I. one light-day
def plate1():
    rnd = random.Random(1977)
    im, d = big(K)
    AU = 2.02; sx, sy = 26, 138
    P = lambda au, ang=0.0: ((sx + au * AU * math.cos(ang)) * S, (sy + au * AU * math.sin(ang)) * S)
    def ring(au, w, fill=WH, dash=None):
        r = au * AU * S
        if dash is None:
            d.ellipse([sx * S - r, sy * S - r, sx * S + r, sy * S + r], outline=fill, width=w)
        else:
            for i in range(0, 360, dash * 2):
                d.arc([sx * S - r, sy * S - r, sx * S + r, sy * S + r], i, i + dash, fill=fill, width=w)
    for _ in range(170):                                   # far stars
        x, y = rnd.uniform(0, W * S), rnd.uniform(0, 232 * S); r = rnd.choice([1, 1, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=WH)
    for _ in range(1500):                                  # Kuiper belt, 30–50 au
        a, au = rnd.uniform(0, 6.283), rnd.gauss(42, 4.5)
        x, y = P(au, a); d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=WH)
    for au in (5.2, 9.6, 19.2, 30.1): ring(au, 3)
    ring(121.6, 3, dash=2)                                 # heliopause, crossed Aug 2012
    d.ellipse([sx * S - 12, sy * S - 12, sx * S + 12, sy * S + 12], fill=WH)
    vx, vy = P(173.14)
    d.line([sx * S + 16, sy * S, vx - 20, vy], fill=R, width=5)   # the signal
    d.polygon([(vx, vy - 22), (vx + 22, vy), (vx, vy + 22), (vx - 22, vy)], fill=R)
    im = down(im); d = pen(im)
    # light-hour ruler
    y0 = 214
    d.line([sx, y0, sx + 173.14 * AU, y0], fill=WH)
    for h in range(25):
        x = round(sx + h * 173.14 / 24 * AU)
        d.line([x, y0 - (6 if h % 6 == 0 else 3), x, y0], fill=WH)
        if h % 6 == 0: d.text((x, y0 + 4), f"{h}h", font=MONO(8), fill=WH, anchor="ma")
    d.text((sx + 121.6 * AU + 4, 30), "heliopause", font=MONO(8), fill=WH)
    d.text((sx + 46 * AU, 56), "Kuiper belt", font=MONO(8), fill=WH)
    d.text((376, 118), "VOYAGER 1", font=MONOB(9), fill=R, anchor="rs")
    d.text((14, 240), "ONE LIGHT-DAY", font=SANSB(24), fill=WH)
    d.text((14, 270), "173.14 au · 25.9 billion km · crossed 18 XI 2026, 10:16 UTC", font=MONO(8), fill=WH)
    d.text((14, 281), "49 years and 74 days after launch. A hello now takes a day to arrive.", font=MONO(8), fill=WH)
    d.text((392, 8), "I/V", font=MONO(8), fill=WH, anchor="ra")
    save(im, 1)

# ---------------------------------------------------------------- II. Chladni
def plate2():
    rnd = np.random.default_rng(1787)
    im = Image.new("RGB", (W, H), WH); d = pen(im)
    x0, y0, L = 14, 14, 256
    d.rectangle([x0 + 5, y0 + 5, x0 + L + 5, y0 + L + 5], fill=R)        # red shadow
    d.rectangle([x0, y0, x0 + L, y0 + L], fill=K)
    n, m = 4, 7
    f = lambda x, y, n, m: np.cos(n*np.pi*x)*np.cos(m*np.pi*y) - np.cos(m*np.pi*x)*np.cos(n*np.pi*y)
    px = im.load(); got = 0
    while got < 15000:
        xs, ys = rnd.random(40000), rnd.random(40000)
        keep = rnd.random(40000) < np.exp(-(np.abs(f(xs, ys, n, m)) / 0.11) ** 2)
        for x, y in zip(xs[keep], ys[keep]):
            px[x0 + 1 + int(x * (L - 1)), y0 + 1 + int(y * (L - 1))] = WH; got += 1
    d.ellipse([x0 + L/2 - 4, y0 + L/2 - 4, x0 + L/2 + 4, y0 + L/2 + 4], fill=R)   # the clamp
    # text column
    tx = 288
    d.text((tx, 14), "Klang-", font=SERIFI(20), fill=K)
    d.text((tx, 36), "figuren", font=SERIFI(20), fill=K)
    d.line([tx, 64, 388, 64], fill=R, width=2)
    for i, s in enumerate(["Sand on a", "bowed plate", "flees the", "motion and", "settles", "where the", "metal is", "still."]):
        d.text((tx, 72 + i * 12), s, font=MONO(9), fill=K)
    d.text((tx, 176), "n = 4", font=MONOB(11), fill=K); d.text((tx, 190), "m = 7", font=MONOB(11), fill=K)
    # three small sibling modes, as sign maps
    for i, (a, b) in enumerate([(1, 2), (2, 5), (3, 6)]):
        g = np.linspace(0, 1, 30); X, Y = np.meshgrid(g, g); z = f(X, Y, a, b) > 0
        ox, oy = tx + i * 35, 212
        for yy in range(30):
            for xx in range(30):
                px[ox + xx, oy + yy] = K if z[yy, xx] else WH
        d.rectangle([ox, oy, ox + 29, oy + 29], outline=K)
        d.text((ox + 15, oy + 33), f"{a},{b}", font=MONO(8), fill=K, anchor="ma")
    d.text((tx, 258), "E. Chladni", font=MONO(8), fill=K); d.text((tx, 268), "Leipzig 1787", font=MONO(8), fill=K)
    sig(d, "II", "CHLADNI — cos nπx cos mπy − cos mπx cos nπy", K, (14, 284))
    save(im, 2)

# ---------------------------------------------------------------- III. (Dés)Ordres
def plate3():
    rnd = random.Random(19741119)
    im, d = big(WH)
    C, cols, rows = 46, 8, 6
    mx, my = (W - cols * C) // 2, 6
    empty = {(7, 5), (6, 5), (5, 5), (2, 3)}
    red = {(5, 1), (1, 4)}
    for cy in range(rows):
        for cx in range(cols):
            if (cx, cy) in empty: continue
            chaos = (cx / (cols - 1)) ** 1.6                    # order on the left, disorder on the right
            k = rnd.randint(3, 9)
            ox, oy = mx + cx * C + C / 2, my + cy * C + C / 2
            drift = [rnd.gauss(0, 2.2 * chaos), rnd.gauss(0, 2.2 * chaos)]
            for i in range(k):
                if rnd.random() < 0.18 * chaos + 0.04: continue
                h = (C / 2 - 2) * (i + 1) / k
                j = 0.4 + 4.2 * chaos
                pts = [((ox + drift[0] * (k - i) / k + sxn * h + rnd.gauss(0, j) * .5) * S,
                        (oy + drift[1] * (k - i) / k + syn * h + rnd.gauss(0, j) * .5) * S)
                       for sxn, syn in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                d.line(pts + [pts[0]], fill=R if (cx, cy) in red else K, width=S, joint="curve")
    im = down(im); d = pen(im)
    bx = mx + 5 * C + 6
    d.text((bx, my + 5 * C + 4), "(Dés)Ordres", font=SERIFI(15), fill=K)
    d.text((bx, my + 5 * C + 24), "after Vera Molnár, 1974", font=MONO(8), fill=K)
    d.text((bx, my + 5 * C + 34), "III/V  19·XI·2026", font=MONO(8), fill=R)
    save(im, 3)

# ---------------------------------------------------------------- IV. wedge
def plate4():
    im, d = big(WH)
    q = lambda pts: [(x * S, y * S) for x, y in pts]
    def hatch(box, step, w, ang=1):                              # "grey" made of honest lines
        m = Image.new("L", im.size, 0); md = ImageDraw.Draw(m)
        for t in range(-400, 800, step):
            md.line(q([(t, 0), (t + ang * 300, 300)]), fill=255, width=w * S)
        clip = Image.new("L", im.size, 0); ImageDraw.Draw(clip).polygon(q(box_poly(box)), fill=255)
        im.paste(K, mask=Image.composite(m, Image.new("L", im.size, 0), clip))
    def box_poly(b): return b if isinstance(b[0], tuple) else [(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])]
    hatch([(0, 300), (0, 96), (150, 300)], 6, 2)                 # hatched corner field
    d.polygon(q([(400, 0), (400, 300), (232, 300), (318, 0)]), fill=K)          # black right mass
    d.ellipse([196 * S, 62 * S, 372 * S, 238 * S], fill=WH)                     # white disc
    d.ellipse([196 * S, 62 * S, 372 * S, 238 * S], outline=K, width=3 * S)
    d.polygon(q([(18, 34), (40, 150), (296, 152)]), fill=R)                     # the wedge
    d.line(q([(60, 292), (392, 20)]), fill=K, width=2 * S)                      # long diagonals
    d.line(q([(76, 296), (398, 32)]), fill=K, width=1 * S)
    d.polygon(q([(120, 204), (212, 186), (216, 204), (124, 222)]), fill=K)      # bars
    d.polygon(q([(140, 236), (196, 225), (198, 233), (142, 244)]), fill=R)
    d.rectangle([338 * S, 250 * S, 362 * S, 274 * S], fill=R)                   # red square on black
    d.rectangle([372 * S, 250 * S, 380 * S, 274 * S], fill=WH)
    for i, r in enumerate((9, 6, 3)):                                           # satellites
        x, y = 150 + i * 30, 66 - i * 14
        d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=K)
    # rotated lettering
    t = Image.new("L", (1200, 600), 0); td = ImageDraw.Draw(t)
    td.text((40, 40), "19", font=SANSB(340), fill=255)
    t = t.crop(t.getbbox()).rotate(39.4, expand=True, resample=Image.BICUBIC)
    im.paste(K, (292 * S - t.width // 2, 158 * S - t.height // 2), t)
    t = Image.new("L", (1500, 160), 0); td = ImageDraw.Draw(t)
    td.text((10, 10), "N O V E M B E R", font=SANSB(68), fill=255)
    t = t.crop(t.getbbox()).rotate(90, expand=True)
    im.paste(WH, (378 * S, 232 * S - t.height), t)
    im = down(im); d = pen(im)
    d.text((10, 8), "IV/V  WEDGE  19·XI·2026", font=MONO(8), fill=K)
    save(im, 4)

# ---------------------------------------------------------------- V. morphogenesis
def plate5():
    rng = np.random.default_rng(19521119)
    gw, gh = 200, 150
    U = np.ones((gh, gw)); V = np.zeros((gh, gw))
    for _ in range(90):
        y, x = rng.integers(3, gh - 3), rng.integers(3, gw - 3)
        V[y-2:y+3, x-2:x+3] = 0.5 + rng.random((5, 5)) * 0.3; U[y-2:y+3, x-2:x+3] = 0.4
    gx = np.linspace(0, 1, gw)[None, :]; gy = np.linspace(0, 1, gh)[:, None]
    F = 0.022 + 0.022 * gx + 0 * gy                 # spots → worms → maze, west to east
    k = 0.059 + 0.004 * (1 - gx) + 0.0015 * (gy - 0.5)
    lap = lambda a: (np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1)
                     + 0.5 * (np.roll(np.roll(a, 1, 0), 1, 1) + np.roll(np.roll(a, 1, 0), -1, 1)
                              + np.roll(np.roll(a, -1, 0), 1, 1) + np.roll(np.roll(a, -1, 0), -1, 1)) - 6 * a) / 3
    for _ in range(9000):
        uvv = U * V * V
        U += 0.21 * lap(U) - uvv + F * (1 - U)
        V += 0.105 * lap(V) + uvv - (F + k) * V
    v = Image.fromarray((np.clip(V / V.max(), 0, 1) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    ink = np.asarray(v) > 70
    yy, xx = np.mgrid[0:H, 0:W]
    sun = (xx - 278) ** 2 + (yy - 118) ** 2 < 84 ** 2
    out = np.full((H, W, 3), 255, np.uint8)
    out[ink] = K; out[ink & sun] = R
    im = Image.fromarray(out, "RGB"); d = pen(im)
    d.rectangle([0, 278, W, H], fill=WH); d.line([0, 278, W, 278], fill=K)
    d.text((8, 284), "V/V  MORPHOGENESIS  19·XI·2026", font=MONO(8), fill=K)
    d.text((392, 284), "two chemicals, one rule; feed rises eastward", font=MONO(8), fill=K, anchor="ra")
    save(im, 5)

if __name__ == "__main__":
    for p in (plate1, plate2, plate3, plate4, plate5): p()
