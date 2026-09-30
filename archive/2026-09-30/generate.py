"""2026-09-30 — Jerome, Geiger, the Drapers, the Queen of the Night, Rumi. Five pictures for a 400x300 black/white/red e-ink panel.
Run from repo root: python3 archive/2026-09-30/generate.py
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3  # supersample factor for hard-edged drawing
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(OUT, "..", "..", "images")
FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"
DATE = "30·IX·2026"

def font(name, size):
    return ImageFont.truetype(name, size)

MONO = FD + "DejaVuSansMono.ttf"
MONOB = FD + "DejaVuSansMono-Bold.ttf"
SERIF = FL + "LiberationSerif-Regular.ttf"
SERIFI = FL + "LiberationSerif-Italic.ttf"
SERIFB = FL + "LiberationSerif-Bold.ttf"
SANSB = FD + "DejaVuSans-Bold.ttf"

# ---------------------------------------------------------------- quantizers
def hard(img3x):
    """Downsample a 3x RGB drawing and snap each pixel to black/white/red (no dither)."""
    a = np.asarray(img3x.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    redness = r - np.maximum(g, b)
    lum = (r + g + b) / 3
    out = np.zeros((H, W, 3), np.uint8)
    out[lum > 0.5] = WHITE
    out[redness > 0.38] = RED
    return Image.fromarray(out)

def tonal(L, m):
    """Serpentine Floyd–Steinberg on a luminance field.
    m=0: {black, white}; m=1: {black, red(0.45), white}; m=2: {black, red}."""
    L = L.astype(np.float64).copy()
    h, w = L.shape
    out = np.zeros((h, w, 3), np.uint8)
    lv = {0: ((0.0, BLACK), (1.0, WHITE)),
          1: ((0.0, BLACK), (0.45, RED), (1.0, WHITE)),
          2: ((0.0, BLACK), (0.45, RED))}
    for y in range(h):
        xs = range(w) if y % 2 == 0 else range(w - 1, -1, -1)
        d = 1 if y % 2 == 0 else -1
        row, nxt = L[y], (L[y + 1] if y + 1 < h else None)
        mrow = m[y]
        for x in xs:
            v = row[x]
            best = min(lv[mrow[x]], key=lambda t: abs(t[0] - v))
            out[y, x] = best[1]
            e = v - best[0]
            if 0 <= x + d < w:
                row[x + d] += e * 7 / 16
            if nxt is not None:
                if 0 <= x - d < w: nxt[x - d] += e * 3 / 16
                nxt[x] += e * 5 / 16
                if 0 <= x + d < w: nxt[x + d] += e * 1 / 16
    return Image.fromarray(out)

def save(img, n, name):
    p = img.convert("RGB")
    pal = Image.new("P", (1, 1))
    pal.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0] * 759)
    q = p.quantize(palette=pal, dither=Image.Dither.NONE)
    for d in (OUT, IMG):
        q.save(os.path.join(d, f"{n}.png"))
    print("saved", n, name)

def crisp(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return d

def footer(d, n, text, fill=BLACK, y=None, x=6):
    f = font(MONO, 9)
    if x == "r":
        x = W - 6 - d.textlength(f"{n}/5 · {DATE} · {text}", font=f)
    d.text((x, H - 13 if y is None else y), f"{n}/5 · {DATE} · {text}", font=f, fill=fill)


SANS = FD + "DejaVuSans.ttf"
LSANS = FL + "LiberationSans-Regular.ttf"
LSANSB = FL + "LiberationSans-Bold.ttf"

def blur(a, s):
    """Separable gaussian blur (numpy only)."""
    r = int(3 * s) + 1
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / s) ** 2); k /= k.sum()
    a = np.apply_along_axis(lambda v: np.convolve(np.pad(v, r, mode="edge"), k, "valid"), 0, a)
    return np.apply_along_axis(lambda v: np.convolve(np.pad(v, r, mode="edge"), k, "valid"), 1, a)

def fbm(h, w, rng, octaves=5):
    out = np.zeros((h, w))
    for o in range(octaves):
        n = 2 ** (o + 2)
        g = Image.fromarray((rng.random((n, n)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += np.asarray(g, np.float64) / 255 / 2 ** o
    return out / sum(1 / 2 ** o for o in range(octaves))

# ---------------------------------------------------------------- 1. Geiger
def geiger():
    rng = random.Random(1882)
    im = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(im)
    s = lambda *v: tuple(x * S for x in v)
    # tube
    y0, rad, xa, xb = 122, 36, 40, 352
    d.rectangle(s(xa, y0 - rad, xb, y0 + rad), fill=WHITE)
    for x in range(xa, xb, 3):  # cathode wall seen in section: hatched bands
        d.line(s(x, y0 - rad - 5, x + 4, y0 - rad), fill=BLACK, width=S)
        d.line(s(x, y0 + rad, x + 4, y0 + rad + 5), fill=BLACK, width=S)
    d.line(s(xa, y0 - rad, xb, y0 - rad), fill=BLACK, width=2 * S)
    d.line(s(xa, y0 + rad, xb, y0 + rad), fill=BLACK, width=2 * S)
    d.line(s(xa, y0 - rad - 5, xa, y0 + rad + 5), fill=BLACK, width=2 * S)       # mica window end
    d.rectangle(s(xb, y0 - rad - 5, xb + 8, y0 + rad + 5), fill=BLACK)            # insulating plug
    d.line(s(xa + 6, y0, xb + 30, y0), fill=BLACK, width=S)                      # anode wire
    d.ellipse(s(xb + 28, y0 - 3, xb + 34, y0 + 3), fill=BLACK)
    # 60 seconds of background clicks, one of them ours
    sy = 236
    t, clicks = 0.0, []
    trng = random.Random(30)
    while True:
        t += trng.expovariate(0.55)
        if t > 60: break
        clicks.append(t)
    hit = min(clicks, key=lambda c: abs(c - 31))
    hx = 20 + hit / 60 * 360
    # particle track (red) crossing the tube and landing on its click
    p0, p1 = (hx - 70, 52), (hx, sy - 32)
    d.line(s(*p0, *p1), fill=RED, width=2 * S)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for sg in (-1, 1):
        d.line(s(p1[0], p1[1], p1[0] - 8 * math.cos(ang + sg * 0.45), p1[1] - 8 * math.sin(ang + sg * 0.45)), fill=RED, width=2 * S)
    d.line(s(20, sy, 380, sy), fill=BLACK, width=S)
    for c in clicks:
        x = 20 + c / 60 * 360
        red = c == hit
        d.line(s(x, sy, x, sy - (26 if red else 16)), fill=RED if red else BLACK, width=(2 if red else 1) * S)
    for sec in range(0, 61, 10):
        x = 20 + sec / 60 * 360
        d.line(s(x, sy, x, sy + 3), fill=BLACK, width=S)
    ions = []
    for k in range(8):
        yy_ = y0 - rad + 5 + k * 9
        t = (yy_ - p0[1]) / (p1[1] - p0[1])
        ions.append((p0[0] + t * (p1[0] - p0[0]), yy_))
    im = hard(im)
    d = crisp(im)
    d.text((8, 2), "GEIGER", font=font(SERIFB, 30), fill=BLACK)
    d.text((140, 8), "born 30 September 1882", font=font(SERIFI, 13), fill=BLACK)
    d.text((140, 23), "Neustadt an der Haardt", font=font(SERIFI, 13), fill=BLACK)
    f9 = font(MONO, 9)
    # the avalanche hugs the anode and, via UV photons, runs its whole length
    xc = hx - 70 + (y0 - 52) / (sy - 32 - 52) * 70
    for _ in range(1500):
        x = rng.gauss(xc, 45) if rng.random() < 0.55 else rng.uniform(xa + 10, xb - 4)
        if not (xa + 10 < x < xb - 4): continue
        near = math.exp(-((x - xc) / 50) ** 2)
        yy_ = y0 + rng.gauss(0, 1.2 + 3.5 * near)
        d.point((int(x), int(round(yy_))), fill=BLACK)
    # drifting electrons: dotted paths from each ion pair to the wire
    for (ix, iy) in ions:
        if abs(iy - y0) < 5: continue
        d.text((ix + 3, iy - 5), "+", font=f9, fill=BLACK)
        for yy_ in range(int(iy), y0, 3 if iy < y0 else -3):
            d.point((int(ix - 3), yy_), fill=BLACK)
    d.text((xa, y0 + rad + 9), "mica window", font=f9, fill=BLACK)
    d.text((xb - 60, y0 - rad - 18), "anode +400 V", font=f9, fill=BLACK)
    d.text((xb - 90, y0 + rad + 9), "cathode · neon gas", font=f9, fill=BLACK)
    d.text((xa + 8, y0 - rad + 5), "track ionises the gas", font=f9, fill=BLACK)
    d.text((xa + 8, y0 + rad - 14), "each e⁻ → ~10⁷ at the wire", font=f9, fill=BLACK)
    for sec in range(0, 61, 10):
        x = 20 + sec / 60 * 360
        d.text((x, sy + 5), f"{sec}s", font=f9, fill=BLACK, anchor="ma")
    d.text((20, sy - 44), f"background: {len(clicks)} clicks in one minute", font=f9, fill=BLACK)
    d.line((0, H - 17, W, H - 17), fill=BLACK)
    footer(d, 1, "every click is an avalanche")
    return im

# ---------------------------------------------------------------- 2. The first plate of M42
def draper():
    rng = np.random.default_rng(1880)
    px0, py0, pw, ph = 14, 14, 236, 262
    yy, xx = np.mgrid[0:ph, 0:pw].astype(np.float64)
    tx, ty = 128.0, 146.0   # Trapezium in plate coords

    def g(cx, cy, sx, sy, th=0.0):
        c, s_ = math.cos(th), math.sin(th)
        u = (xx - cx) * c + (yy - cy) * s_
        v = -(xx - cx) * s_ + (yy - cy) * c
        return np.exp(-0.5 * ((u / sx) ** 2 + (v / sy) ** 2))

    D = (1.6 * g(tx, ty, 11, 13)
         + 0.9 * g(tx + 8, ty + 18, 26, 44, 0.35)
         + 0.55 * g(tx - 30, ty + 40, 20, 60, -0.5)      # southern wing sweeping west
         + 0.5 * g(tx + 40, ty - 12, 14, 48, 0.9)        # eastern wing
         + 0.35 * g(tx - 20, ty - 44, 40, 18, 0.2)
         + 0.55 * g(tx + 16, ty - 62, 11, 10))           # M43
    D -= 0.9 * g(tx - 26, ty - 18, 13, 20, 0.6)          # the dark bay ("fish's mouth")
    D -= 0.5 * g(tx + 12, ty - 44, 26, 4, 0.1)           # lane between M42 and M43
    D = np.clip(D, 0, None)
    N = fbm(ph, pw, rng)
    N2 = fbm(ph, pw, np.random.default_rng(42), octaves=6)
    wisps = np.abs(np.sin((N2 - 0.5) * 22))       # filamentary ridges
    D *= 0.35 + 1.3 * N ** 1.8
    D *= 0.35 + 1.0 * wisps
    D = blur(D, 2.2)      # 1880 guiding: soft
    # stars (point-ish, also a little soft)
    St = np.zeros_like(D)
    for _ in range(70):
        sx_, sy_ = rng.uniform(0, pw), rng.uniform(0, ph)
        St += rng.uniform(0.6, 2.5) * g(sx_, sy_, rng.uniform(0.7, 1.2), rng.uniform(0.7, 1.2))
    St += 3.5 * g(tx + 6, ph - 30, 2.2, 2.2)   # iota Orionis
    St += 2.0 * g(tx + 30, 34, 1.6, 1.6)
    dens = 1 - np.exp(-1.35 * (D + St))
    L = 1.0 - 1.05 * dens ** 0.9                 # a negative: light → dark
    L += rng.normal(0, 0.06, L.shape)            # silver grain
    # vignetting of the lens at plate edge
    r = np.hypot((xx - pw / 2) / pw, (yy - ph / 2) / ph)
    L -= 0.12 * np.clip(r - 0.42, 0, None) * 6
    L = np.clip(L, 0, 1)
    full = np.ones((H, W))
    full[py0:py0 + ph, px0:px0 + pw] = L
    im = tonal(np.clip(full, 0, 1), np.zeros((H, W), int))
    d = crisp(im)
    d.rectangle((px0 - 1, py0 - 1, px0 + pw, py0 + ph), outline=BLACK)
    # the Trapezium, red
    TX, TY = px0 + tx, py0 + ty
    tz = ((-3, -3), (3, -4), (-4, 3), (3, 3))
    for ox, oy in tz:
        d.rectangle((TX + ox - 2, TY + oy - 2, TX + ox + 1, TY + oy + 1), fill=WHITE)
    for ox, oy in tz:
        d.rectangle((TX + ox - 1, TY + oy - 1, TX + ox, TY + oy), fill=RED)
    # paper label gummed to the plate
    d.rectangle((px0 + 6, py0 + ph - 24, px0 + 176, py0 + ph - 6), fill=WHITE, outline=BLACK)
    d.text((px0 + 11, py0 + ph - 22), "Orion Neb.  Sept 30. 1880  50m", font=font(SERIFI, 12), fill=BLACK)
    # right column
    x = 262
    d.text((x, 12), "M42", font=font(SERIFB, 34), fill=BLACK)
    d.text((x, 50), "the first photograph", font=font(SERIFI, 13), fill=BLACK)
    d.text((x, 65), "of a nebula", font=font(SERIFI, 13), fill=BLACK)
    f = font(MONO, 9)
    for i, t in enumerate(["30 September 1880", "Henry & Anna Draper", "Hastings-on-Hudson",
                           "11-in Clark refractor", "50-minute exposure", "", "shown here as the",
                           "plate saw it: a negative"]):
        d.text((x, 92 + i * 12), t, font=f, fill=BLACK)
    d.rectangle((x, 208, x + 3, 211), fill=RED)
    d.text((x + 8, 203), "the Trapezium:", font=f, fill=RED)
    d.text((x + 8, 215), "four young stars", font=f, fill=BLACK)
    d.text((x + 8, 227), "that light it all", font=f, fill=BLACK)
    for xx_ in range(int(TX) + 6, x - 4, 3):   # dotted leader
        d.point((xx_, TY + (209 - TY) * (xx_ - TX) / (x - TX)), fill=RED)
    footer(d, 2, "M42 after Draper, simulated", x="r")
    return im

# ---------------------------------------------------------------- 3. Queen of the Night
def queen():
    rng = random.Random(1791)
    im = Image.new("RGB", (W * S, H * S), BLACK)
    d = ImageDraw.Draw(im)
    s = lambda *v: tuple(x * S for x in v)

    def star(x, y, r):
        d.polygon([s(x, y - r), s(x + r * 0.3, y - r * 0.3), s(x + r, y), s(x + r * 0.3, y + r * 0.3),
                   s(x, y + r), s(x - r * 0.3, y + r * 0.3), s(x - r, y), s(x - r * 0.3, y - r * 0.3)], fill=WHITE)

    zx, zy, zr = 200, 34, 24
    for k, rr in enumerate((zr, zr - 6, zr - 11)):
        n = int(2 * math.pi * rr / 6)
        for i in range(n):
            a = 2 * math.pi * (i + 0.5 * k) / n
            star(zx + rr * math.cos(a), zy + rr * 0.8 * math.sin(a), 1.6)
    # ribs: chains of stars, three abreast, rising to the zenith ring
    nrib = 14
    for i in range(nrib):
        u = (i + 0.5) / nrib
        a_end = math.pi * (0.05 + 0.9 * u)                     # where it meets the ring (lower half)
        ex, ey = zx - (zr + 3) * math.cos(a_end), zy + (zr + 3) * 0.8 * math.sin(a_end)
        bx = -120 + u * 640
        by = 250
        cx, cy = zx + (bx - zx) * 1.05, zy + 20 + abs(bx - zx) * 0.05
        steps = 40
        for j in range(steps):
            t = j / steps
            x = (1 - t) ** 2 * bx + 2 * (1 - t) * t * cx + t * t * ex
            y = (1 - t) ** 2 * by + 2 * (1 - t) * t * cy + t * t * ey
            dx = -2 * (1 - t) * bx + 2 * (1 - 2 * t) * cx + 2 * t * ex
            dy = -2 * (1 - t) * by + 2 * (1 - 2 * t) * cy + 2 * t * ey
            ln = math.hypot(dx, dy); nx, ny = -dy / ln, dx / ln
            wdt = 2.2 + 4.5 * (1 - t)
            for o in (-1, 0, 1):
                star(x + nx * o * wdt, y + ny * o * wdt, 0.9 + 1.4 * (1 - t))
    # clouds, merging into the white paper strip
    d.rectangle(s(0, 222, W, H), fill=WHITE)
    for _ in range(90):
        x = rng.uniform(-10, 410)
        y = rng.uniform(200, 225) + 12 * (abs(x - 200) / 200) ** 2 * -1 + 8
        r = rng.uniform(7, 16)
        d.ellipse(s(x - r, y - r, x + r, y + r), fill=WHITE, outline=BLACK, width=S)
    for _ in range(60):
        x = rng.uniform(-10, 410); y = rng.uniform(222, 234); r = rng.uniform(8, 15)
        d.ellipse(s(x - r, y - r, x + r, y + r), fill=WHITE)
    d.rectangle(s(0, 228, W, H), fill=WHITE)
    d.rectangle(s(0, 219, 40, H), fill=WHITE)
    # the Queen: dark star-strewn gown, arms raised, outlined in white
    q = [(200, 110), (206, 116), (219, 97), (222, 99), (211, 126), (218, 158), (236, 200),
         (164, 200), (182, 158), (189, 126), (178, 99), (181, 97), (194, 116)]
    d.polygon([s(*p) for p in q], fill=BLACK, outline=WHITE, width=S)
    d.ellipse(s(195, 99, 205, 111), fill=BLACK, outline=WHITE, width=S)
    star(200, 91, 4.5)
    for k in range(14):
        yk = rng.uniform(132, 192)
        half = 7 + (yk - 126) * 0.45
        star(200 + rng.uniform(-half, half) * 0.8, yk, 1.3)
    # crescent, horns up, cradling her hem
    mx, my, mr = 200, 172, 44
    cres = Image.new("L", (W * S, H * S), 0)
    cd = ImageDraw.Draw(cres)
    cd.ellipse(s(mx - mr, my - mr, mx + mr, my + mr), fill=255)
    cd.ellipse(s(mx - mr * 0.93, my - mr * 1.2, mx + mr * 0.93, my + mr * 0.7), fill=0)
    im.paste(WHITE, (0, 0), cres)
    d = ImageDraw.Draw(im)
    im = hard(im)
    d = crisp(im)
    # staff
    x0, x1 = 150, 392
    top = 250
    for k in range(5):
        d.line((x0, top + 5 * k, x1, top + 5 * k), fill=BLACK)
    notes = [("F5", 0), ("A5", -2), ("C6", -4), ("F6", -7), ("C6", -4), ("A5", -2), ("F5", 0), ("D5", 2)]
    im3 = Image.new("RGB", (W * S, H * S), WHITE)
    for i, (nm, st) in enumerate(notes):
        x = x0 + 22 + i * 28
        y = top + st * 2.5
        col = RED if nm == "F6" else BLACK
        for ly in range(top - 5, int(y) - 1, -5):     # ledger lines
            d.line((x - 7, ly, x + 7, ly), fill=BLACK)
        e = Image.new("L", (14 * S, 10 * S), 0)
        ImageDraw.Draw(e).ellipse((1 * S, 2 * S, 13 * S, 8 * S), fill=255)
        e = e.rotate(20, resample=Image.BICUBIC).resize((14, 10), Image.LANCZOS).point(lambda v: 255 if v > 110 else 0)
        im.paste(col, (int(x - 7), int(y - 5)), e)
        d.line((x - 5, y + 1, x - 5, y + 17), fill=col)              # stem down
        d.rectangle((x - 1, y - 8, x, y - 7), fill=col)            # staccato
    d.text((x0 + 22 + 3 * 28 + 9, top - 20), "F6", font=font(MONOB, 10), fill=RED)
    d.text((8, 234), "Der Hölle Rache", font=font(SERIFI, 16), fill=BLACK)
    d.text((8, 253), "the Queen's high F", font=font(MONO, 9), fill=BLACK)
    d.text((8, 265), "1397 Hz, staccato", font=font(MONO, 9), fill=BLACK)
    d.text((8, 6), "DIE ZAUBERFLÖTE", font=font(SERIFB, 15), fill=WHITE)
    d.text((8, 23), "first night: Vienna,", font=font(SERIFI, 12), fill=WHITE)
    d.text((8, 36), "30 September 1791", font=font(SERIFI, 12), fill=WHITE)
    footer(d, 3, "hall of stars after Schinkel, 1815 · notes stylised")
    return im

# ---------------------------------------------------------------- 4. Jerome's horns
PROFILE = [(0.30, 0.80), (0.12, 0.62), (0.06, 0.40), (0.12, 0.20), (0.30, 0.06), (0.50, 0.02), (0.66, 0.10),
           (0.72, 0.26), (0.69, 0.33), (0.74, 0.40), (0.84, 0.52), (0.74, 0.56), (0.75, 0.60), (0.80, 0.68),
           (0.82, 0.85), (0.76, 1.02), (0.66, 1.14), (0.58, 1.08), (0.56, 1.02), (0.86, 1.12), (1.02, 1.30),
           (-0.30, 1.30), (-0.18, 1.10), (0.18, 1.00), (0.34, 0.92)]

def smooth(pts, n=6):
    out, m = [], len(pts)
    for i in range(m):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % m], pts[(i + 2) % m]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    return out

def jerome():
    im = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(im)

    def head(cx, cy, sc, flip):
        def P(x, y):
            return ((cx + (-x if flip else x) * sc) * S, (cy + y * sc) * S)
        d.polygon([P(x, y) for x, y in smooth(PROFILE)], fill=BLACK)
        for k in range(4):                 # beard locks
            pts = [P(0.62 + 0.04 * k + 0.02 * math.sin(j * 1.3 + k), 0.72 + 0.06 * j) for j in range(6)]
            d.line(pts, fill=WHITE, width=S)
        return P

    def bundles(P, red):
        for bx in (0.28, 0.55):            # two tufts at the brow-top, as in the old pictures
            base = (bx, 0.08 if bx < 0.4 else 0.07)
            if red:
                pts_l, pts_r = [], []
                for k in range(13):
                    t = k / 12
                    x = base[0] + (0.07 if bx > 0.4 else -0.02) * t + 0.05 * math.sin(t * 2.2)
                    y = base[1] - 0.36 * t
                    w = 0.055 * (1 - t) + 0.004
                    pts_l.append(P(x - w, y)); pts_r.append(P(x + w, y))
                d.polygon(pts_l + pts_r[::-1], fill=RED)
            else:
                for a in np.linspace(-0.55, 0.55, 7):
                    a0 = -math.pi / 2 + a + (0.15 if bx > 0.4 else -0.15)
                    r0, r1 = 0.07, 0.34 + 0.04 * math.cos(a * 5)
                    d.line([P(base[0] + r0 * math.cos(a0), base[1] + r0 * math.sin(a0)),
                            P(base[0] + r1 * math.cos(a0), base[1] + r1 * math.sin(a0))], fill=BLACK, width=S)

    P = head(84, 128, 82, False); bundles(P, False)
    P = head(316, 128, 82, True); bundles(P, True)
    im = hard(im)
    d = crisp(im)
    heb = font(FL + "LiberationSerif-Bold.ttf", 54)
    d.text((200, 36), "קרן", font=heb, fill=BLACK, anchor="mm", direction="rtl")  # logical order; raqm lays it out RTL
    d.text((200, 72), "qeren", font=font(SERIFI, 14), fill=BLACK, anchor="mm")
    d.text((200, 90), "a horn · a ray of light", font=font(MONO, 9), fill=BLACK, anchor="mm")
    d.text((200, 104), "Exodus 34:29", font=font(MONO, 9), fill=BLACK, anchor="mm")
    d.text((200, 168), "or", font=font(SERIFI, 20), fill=BLACK, anchor="mm")
    d.text((8, 6), "ST JEROME", font=font(MONOB, 11), fill=BLACK)
    d.text((8, 20), "30 September", font=font(MONO, 9), fill=BLACK)
    d.text((8, 31), "translators' day", font=font(MONO, 9), fill=BLACK)
    d.text((W - 8, 6), "VULGATE", font=font(MONOB, 11), fill=BLACK, anchor="ra")
    d.text((W - 8, 20), "c. 405 AD", font=font(MONO, 9), fill=BLACK, anchor="ra")
    d.text((84, 250), "“his face shone”", font=font(SERIFI, 13), fill=BLACK, anchor="mm")
    d.text((316, 250), "cornuta esset facies sua", font=font(SERIFI, 13), fill=RED, anchor="mm")
    d.text((84, 264), "one reading", font=font(MONO, 9), fill=BLACK, anchor="mm")
    d.text((316, 264), "Jerome's reading", font=font(MONO, 9), fill=BLACK, anchor="mm")
    d.line((0, H - 17, W, H - 17), fill=BLACK)
    footer(d, 4, "Jerome chose horns; Michelangelo carved them")
    return im

# ---------------------------------------------------------------- 5. Sema
def sema():
    rng = np.random.default_rng(1207)
    SS = 2
    hx, hy, hr = 244 * SS, 152 * SS, 128 * SS
    acc = np.zeros((H * SS, W * SS))
    n = 7
    for i in range(n):
        R = (26 + 92 * i / (n - 1)) * SS
        th0 = rng.uniform(0, 2 * math.pi)
        om = rng.uniform(13, 17) * (1 + i * 0.12)      # outer dancers have further to go
        turns = rng.uniform(0.3, 0.55)
        t = np.linspace(0, 2 * math.pi * turns, 120000)
        cx = hx + R * np.cos(th0 - t)
        cy = hy + R * np.sin(th0 - t)
        sk = rng.uniform(9, 12) * SS
        for h in range(2):
            ph = math.pi * h
            x = cx + sk * np.cos(ph - om * t)
            y = cy + sk * np.sin(ph - om * t)
            ok = (x >= 0) & (x < W * SS) & (y >= 0) & (y < H * SS)
            np.add.at(acc, (y[ok].astype(int), x[ok].astype(int)), 1.0)
        # where the dancer stops: the skirt's last bell, bright
        a = np.linspace(0, 2 * math.pi, 400)
        for rr in np.linspace(0, sk, 12):
            x = cx[-1] + rr * np.cos(a); y = cy[-1] + rr * np.sin(a)
            np.add.at(acc, (y.astype(int), x.astype(int)), 6.0)
    A = np.asarray(Image.fromarray(np.clip(acc / 4 * 255, 0, 255).astype(np.uint8)).resize((W, H), Image.LANCZOS), np.float64) / 255
    L = np.clip(A / np.percentile(A[A > 0], 97), 0, 1) ** 0.7
    L[L < 0.05] = 0
    im = tonal(np.clip(L, 0, 1), np.zeros((H, W), int))
    d = crisp(im)
    # the hall's boundary, dotted
    for a in np.linspace(0, 2 * math.pi, 260, endpoint=False):
        d.point((hx / SS + (hr / SS) * math.cos(a), hy / SS + (hr / SS) * math.sin(a)), fill=WHITE)
    # the red post (sheepskin) at the hall's edge
    pa = math.radians(180)
    px, py = hx / SS + (hr / SS + 10) * math.cos(pa), hy / SS + (hr / SS + 10) * math.sin(pa)
    pts = []
    for k in range(24):
        a = 2 * math.pi * k / 24
        rr = 6 + 1.6 * (k % 2)
        pts.append((px + rr * 0.8 * math.cos(a), py + rr * 1.15 * math.sin(a)))
    d.polygon(pts, fill=RED)
    d.text((8, 6), "SEMA", font=font(SERIFB, 26), fill=WHITE)
    d.text((8, 34), "Rumi, born", font=font(SERIFI, 12), fill=WHITE)
    d.text((8, 48), "30 September 1207", font=font(SERIFI, 12), fill=WHITE)
    d.text((8, py + 16), "the red post:", font=font(MONO, 9), fill=RED)
    d.text((8, py + 28), "the sheikh's", font=font(MONO, 9), fill=WHITE)
    d.text((8, py + 40), "sheepskin", font=font(MONO, 9), fill=WHITE)
    footer(d, 5, "seven dancers, one long exposure", fill=WHITE)
    return im

if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["1", "2", "3", "4", "5"]
    fns = {"1": geiger, "2": draper, "3": queen, "4": jerome, "5": sema}
    for k in which:
        save(fns[k](), int(k), fns[k].__name__)
