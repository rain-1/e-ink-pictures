"""2026-09-29 — Michaelmas. Five pictures for a 400x300 black/white/red e-ink panel.
Run from repo root: python3 archive/2026-09-29/generate.py
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
DATE = "29·IX·2026"

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

# ---------------------------------------------------------------- 1. Michaelmas bramble
def michaelmas():
    rng = random.Random(2909)
    im = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(im)

    def leaflet(cx, cy, ang, size):
        pts = []
        n = 44
        for i in range(n):
            t = 2 * math.pi * i / n
            # ovate with pointed tip along +x, serrated edge
            rr = size * (0.55 + 0.45 * math.cos(t)) ** 0.8 * (1 + 0.08 * (i % 2))
            px, py = rr * math.cos(t) * 1.0, rr * math.sin(t) * 0.55
            px += size * 0.45
            ca, sa = math.cos(ang), math.sin(ang)
            pts.append((cx + px * ca - py * sa, cy + px * sa + py * ca))
        d.polygon(pts, fill=WHITE, outline=BLACK, width=S)
        ca, sa = math.cos(ang), math.sin(ang)
        tip = (cx + size * 1.4 * ca, cy + size * 1.4 * sa)
        d.line([(cx, cy), tip], fill=BLACK, width=S)
        for k in range(1, 6):  # veins
            f = k / 6.5
            bx, by = cx + size * 1.4 * f * ca, cy + size * 1.4 * f * sa
            for sgn in (-1, 1):
                va = ang + sgn * 0.75
                L = size * 0.42 * (1 - f * 0.6)
                d.line([(bx, by), (bx + L * math.cos(va), by + L * math.sin(va))], fill=BLACK, width=max(1, S - 1))

    def leaf(x, y, ang, size):
        for off, sc in ((-0.9, 0.75), (0.9, 0.75), (0.0, 1.0)):
            leaflet(x, y, ang + off, size * sc)

    def berry(cx, cy, r, ripe):
        pts = []
        ga = math.pi * (3 - math.sqrt(5))
        n = 22
        for i in range(n):
            rr = r * math.sqrt((i + 0.5) / n)
            pts.append((cx + rr * math.cos(i * ga) * 0.85, cy + rr * math.sin(i * ga)))
        pts.sort(key=lambda p: p[1])
        dr = r * 0.34
        for (px, py) in pts:
            if ripe:
                d.ellipse([px - dr, py - dr, px + dr, py + dr], fill=BLACK, outline=WHITE, width=1)
                d.ellipse([px - dr * 0.5, py - dr * 0.55, px - dr * 0.1, py - dr * 0.15], fill=WHITE)
            else:
                d.ellipse([px - dr, py - dr, px + dr, py + dr], fill=RED, outline=BLACK, width=S)
        # sepals
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * 0.5
            d.line([(cx, cy - r), (cx + r * 0.9 * math.cos(a), cy - r + r * 0.6 * math.sin(a) - 2)], fill=BLACK, width=S)

    def cane(x, y, ang, steps, curv):
        pts = [(x, y)]
        for i in range(steps):
            ang += curv * (1 + i / steps * 1.5) + rng.uniform(-0.02, 0.02)
            x += 12 * math.cos(ang); y += 12 * math.sin(ang)
            pts.append((x, y))
        return pts

    canes = []
    for i in range(8):
        x0 = rng.uniform(-60, W * S + 60)
        side = -1 if x0 > W * S / 2 else 1
        ang = -math.pi / 2 + side * rng.uniform(0.05, 0.45)
        canes.append(cane(x0, H * S + 20, ang, rng.randint(60, 90), side * rng.uniform(0.009, 0.017)))
    # the fall: from the morning star, into the thickest part of the bush
    star = (W * S * 0.86, 70)
    top = [p for c in canes for p in c if W * S * 0.35 < p[0] < W * S * 0.75 and p[1] > 0]
    land = min(top, key=lambda p: p[1])
    land = (land[0], land[1] + 30)
    for pts in canes:
        d.line(pts, fill=BLACK, width=4 * S // 2 + 2, joint="curve")
        for i in range(2, len(pts) - 1, 2):  # thorns
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            a = math.atan2(y2 - y1, x2 - x1)
            s = 1 if i % 4 == 0 else -1
            nx, ny = -math.sin(a) * s, math.cos(a) * s
            base = (x1 + nx * 4, y1 + ny * 4)
            tip = (x1 + nx * 14 - math.cos(a) * 8, y1 + ny * 14 - math.sin(a) * 8)
            d.polygon([base, (base[0] + math.cos(a) * 8, base[1] + math.sin(a) * 8), tip], fill=BLACK)
        for i in range(8, len(pts) - 4, rng.randint(9, 13)):
            x, y = pts[i]
            if 0 < x < W * S and 40 < y < H * S - 40:
                leaf(x, y, rng.uniform(0, 2 * math.pi), rng.uniform(34, 50))
        # fruit truss at tip and along cane
        for i in list(range(len(pts) - 1, 10, -rng.randint(14, 22)))[:3]:
            x, y = pts[i]
            if 20 < x < W * S - 20 and 20 < y < H * S - 60:
                for k in range(rng.randint(2, 4)):
                    bx, by = x + rng.uniform(-40, 40), y + rng.uniform(10, 50)
                    d.line([(x, y), (bx, by - 20)], fill=BLACK, width=S)
                    berry(bx, by, rng.uniform(17, 23), rng.random() < 0.86)
    # the red fall line, and a splash where it lands
    fp = []
    for i in range(60):
        t = i / 59
        fp.append((star[0] + (land[0] - star[0]) * (1 - (1 - t) ** 2),
                   star[1] + (land[1] - star[1]) * t))
    d.line(fp, fill=RED, width=2 * S)
    for k in range(9):
        a = -math.pi + k * math.pi / 8
        d.line([(land[0] + 10 * math.cos(a), land[1] + 10 * math.sin(a)),
                (land[0] + 34 * math.cos(a), land[1] + 30 * math.sin(a))], fill=RED, width=S)
    for i in range(0, 60, 7):  # tumbling sparks shed on the way down
        x, y = fp[i]
        d.line([(x + 10, y - 4), (x + 22, y - 12)], fill=RED, width=S)
    sx, sy = star
    for a in range(4):
        th = a * math.pi / 2
        d.polygon([(sx + 30 * math.cos(th), sy + 30 * math.sin(th)),
                   (sx + 6 * math.cos(th + math.pi / 4), sy + 6 * math.sin(th + math.pi / 4)),
                   (sx, sy), (sx + 6 * math.cos(th - math.pi / 4), sy + 6 * math.sin(th - math.pi / 4))], fill=RED)
    img = hard(im)
    d = crisp(img)
    d.rectangle([0, 0, 138, 44], fill=WHITE)
    d.text((6, 3), "MICHAELMAS", font=font(SERIFB, 22), fill=BLACK)
    d.text((7, 27), "pick no blackberries after today", font=font(SERIFI, 11), fill=BLACK)
    d.rectangle([0, H - 16, W, H], fill=WHITE)
    d.line([(0, H - 16), (W, H - 16)], fill=BLACK)
    footer(d, 1, "the fallen star cursed the brambles")
    return img

# ---------------------------------------------------------------- 2. Fermi 125
def fermi():
    img = Image.new("RGB", (W, H), WHITE)
    d = crisp(img)
    d.text((8, 2), "FERMI", font=font(SANSB, 30), fill=BLACK)
    d.text((112, 2), "125", font=font(SANSB, 30), fill=RED)
    d.text((10, 38), "born Rome, 29 Sep 1901 · how many piano tuners in Chicago?", font=font(FD + "DejaVuSans.ttf", 10), fill=BLACK)
    rows = [("", "Chicagoans", 3e6, "3,000,000"),
            ("÷ 2", "people per home", 1.5e6, "1,500,000"),
            ("÷ 20", "homes own a piano", 7.5e4, "75,000"),
            ("× 1", "tuning a year each", 7.5e4, "75,000"),
            ("÷ 1000", "a tuner does a year", 75, "75")]
    bx0, bx1 = 168, 392
    X = lambda v: bx0 + (bx1 - bx0) * math.log10(v) / 7
    top, rh = 62, 34
    # decade grid
    for k in range(8):
        x = X(10 ** k)
        for y in range(top - 4, top + rh * 5, 3):
            d.point((x, y), fill=BLACK)
        d.text((x, top + rh * 5 + 2), f"1e{k}", font=font(MONO, 8), fill=BLACK, anchor="mt")
    fo, fl, fv = font(SANSB, 11), font(FD + "DejaVuSans.ttf", 10), font(MONO, 9)
    for i, (op, lab, v, vs) in enumerate(rows):
        y = top + i * rh
        last = i == len(rows) - 1
        d.text((6, y + 7), op, font=fo, fill=BLACK)
        d.text((64, y + 8), lab, font=fl, fill=BLACK)
        c = RED if last else BLACK
        x = X(v)
        if last:
            d.rectangle([bx0, y + 6, x, y + 24], fill=RED)
        else:
            d.rectangle([bx0, y + 6, x, y + 24], outline=BLACK)
            for hx in range(bx0 - 20, int(x), 4):  # hatching
                d.line([(max(hx, bx0), y + 6 + max(0, bx0 - hx)), (min(hx + 18, x), y + 24 - max(0, hx + 18 - x))], fill=BLACK)
        d.text((x + 4 if x < 330 else x - 4, y + 10), vs, font=font(MONOB, 10), fill=c,
               anchor="lm" if x < 330 else "rm")
        if x >= 330:  # knock out behind label
            tw = d.textlength(vs, font=font(MONOB, 10))
            d.rectangle([x - tw - 7, y + 3, x - 1, y + 17], fill=WHITE)
            d.text((x - 4, y + 10), vs, font=font(MONOB, 10), fill=c, anchor="rm")
        if i:
            d.line([(4, y - 2), (bx1, y - 2)], fill=BLACK)
    d.text((W - 8, 6), "≈ 75", font=font(SANSB, 26), fill=RED, anchor="ra")
    d.text((W - 8, 250), "guess each factor boldly — the errors tend to cancel.", font=font(SERIFI, 12), fill=BLACK, anchor="ra")
    d.rectangle([0, H - 16, W, H], fill=BLACK)
    footer(d, 2, "Trinity 1945: dropped paper in the blast → '10 kt'", fill=WHITE)
    return img

# ---------------------------------------------------------------- 3. Alouette ionogram
def alouette():
    rng = np.random.default_rng(1962272)
    hs, hm, H0, fo = 1000.0, 300.0, 62.0, 7.2  # satellite alt, F2 peak alt, scale ht, foF2 (MHz)
    fH = 0.75
    z = np.linspace(hs, 0, 6000)
    def fn2(h):
        zz = (h - hm) / H0
        v = fo ** 2 * np.exp(0.5 * (1 - zz - np.exp(-zz)))
        v[h < 90] = 0
        return v
    F2 = fn2(z)
    dz = z[0] - z[1]
    def vrange(f):
        """group path downward from the satellite, O-mode, no-field approximation."""
        x = F2 / f ** 2
        if x.max() < 1:  # penetrates: echo from the ground
            return dz * np.sum(1 / np.sqrt(1 - x)), True
        k = np.argmax(x >= 1)
        return dz * np.sum(1 / np.sqrt(np.clip(1 - x[:k], 1e-4, None))), False
    im = Image.new("RGB", (W * S, H * S), BLACK)
    d = ImageDraw.Draw(im)
    fx = lambda f: (24 + (f - 0.2) / 11.8 * 366) * S
    ry = lambda r: (40 + r / 1700 * 225) * S
    # frequency marker lines along the top, range scale on the left (as on the film records)
    fm = font(MONO, 8 * S)
    for f in np.arange(0.5, 12.01, 0.5):
        L = 10 if f % 2 == 0 else 5
        d.line([(fx(f), 30 * S), (fx(f), (30 + L) * S)], fill=WHITE, width=S)
        if f % 2 == 0:
            d.text((fx(f), 21 * S), f"{int(f)}", font=fm, fill=WHITE, anchor="mt")
    for r in range(0, 1700, 200):
        d.line([(10 * S, ry(r)), (18 * S, ry(r))], fill=WHITE, width=S)
        for xx in range(int(fx(0.3)), int(fx(12)), 14 * S):
            d.rectangle([xx, ry(r), xx + 1, ry(r) + 1], fill=WHITE)
    # traces
    for f in np.arange(0.35, 12.0, 0.018):
        # plasma resonance spikes at the satellite: fN, fH, 2fH, upper hybrid
        fN = math.sqrt(F2[0])
        for fr in (fN, fH, 2 * fH, math.sqrt(fN ** 2 + fH ** 2)):
            if abs(f - fr) < 0.02:
                d.line([(fx(f), ry(0)), (fx(f), ry(rng.uniform(180, 420)))], fill=WHITE, width=S)
        vr, ground = vrange(f)
        dot = lambda r, c, s=S: d.ellipse([fx(f) - s, ry(r) - s, fx(f) + s, ry(r) + s], fill=c)
        if f > fN * 1.05 and vr < 1690 and rng.random() < 0.9:
            dot(vr, RED if ground else WHITE, S + (1 if not ground else 0))
            if ground and rng.random() < 0.6:  # second hop smear under the ground echo
                dot(vr + rng.uniform(8, 20), RED, S - 1)
        # X-mode: reflects where fN^2 = f(f - fH); approximate as O-trace at an equivalent frequency
        fe2 = f * (f - fH)
        if fe2 > F2[0] * 1.1:
            vx, gx = vrange(math.sqrt(fe2))
            if not gx and vx < 1690 and rng.random() < 0.55:
                dot(vx, WHITE, S - 1)
    # grain and scratches
    for _ in range(900):
        x, y = rng.uniform(0, W * S), rng.uniform(26 * S, 272 * S)
        d.rectangle([x, y, x + 2, y + 2], fill=WHITE)
    for _ in range(3):
        x = rng.uniform(40, W - 40) * S
        d.line([(x, 26 * S), (x + rng.uniform(-9, 9) * S, 272 * S)], fill=WHITE, width=1)
    img = hard(im)
    d = crisp(img)
    # sprocket holes
    for x in range(8, W, 22):
        d.rounded_rectangle([x, 3, x + 11, 11], 2, fill=WHITE)
        d.rounded_rectangle([x, H - 11, x + 11, H - 3], 2, fill=WHITE)
    f9 = font(MONO, 9)
    d.text((W - 8, 46), "ALOUETTE-I  1962 272 1905 UT", font=f9, fill=WHITE, anchor="ra")
    d.text((W - 8, 58), "sweep 0.5–12 MHz  100 W", font=f9, fill=WHITE, anchor="ra")
    d.text((fx(9.3) / S, ry(1260) / S), "EARTH", font=font(MONOB, 10), fill=RED, anchor="mm")
    d.text((fx(6.2) / S, ry(1150) / S), "F2 peak", font=f9, fill=WHITE, anchor="mm")
    d.text((4, 20), "MHz", font=font(MONO, 8), fill=WHITE)
    # the satellite and its tape-measure antennas, bottom-left
    cx, cy = 34, 244
    d.line([(cx - 26, cy + 14), (cx + 26, cy - 14)], fill=WHITE)
    d.line([(cx - 14, cy - 18), (cx + 14, cy + 18)], fill=WHITE)
    d.ellipse([cx - 6, cy - 5, cx + 6, cy + 5], fill=WHITE, outline=RED)
    footer(d, 3, "Alouette: built for 1 yr, sang for 10", fill=WHITE, y=H - 27, x="r")
    return img

# ---------------------------------------------------------------- 4. Moon among the Seven Sisters
def pleiades():
    ra0, de0, sc = 3 + 39.5 / 60, 22.9, 56.0  # centre (h, deg), px/deg
    def P(ra_h, de):
        x = W / 2 - (ra_h - ra0) * 15 * math.cos(math.radians(de0)) * sc
        y = H / 2 - (de - de0) * sc
        return x, y
    stars = [  # name, RA h m s, Dec d m, mag (J2000)
        ("Alcyone", (3, 47, 29.1), (24, 6.3), 2.87), ("Atlas", (3, 49, 9.7), (24, 3.2), 3.62),
        ("Electra", (3, 44, 52.5), (24, 6.8), 3.70), ("Maia", (3, 45, 49.6), (24, 22.1), 3.87),
        ("Merope", (3, 46, 19.6), (23, 56.9), 4.18), ("Taygeta", (3, 45, 12.5), (24, 28.0), 4.30),
        ("Pleione", (3, 49, 11.2), (24, 8.2), 5.05), ("Celaeno", (3, 44, 48.2), (24, 17.4), 5.45),
        ("Asterope", (3, 45, 54.4), (24, 33.3), 5.76)]
    moon_ra, moon_de, mr = 3 + 31 / 60, 21.2, 0.26 * sc * 1.0
    mx, my = P(moon_ra, moon_de)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    rng0 = np.random.default_rng(930)
    dx, dy = xx - mx, yy - my
    rr = np.hypot(dx, dy)
    L = np.zeros_like(rr)
    glow = (rng0.random(rr.shape) < 0.32 * np.exp(-(rr - mr) / 24)) & (rr > mr + 1)  # moonlight glare drowning the sky
    # the moon disc: 93% lit waning gibbous, dark sliver on the west (right)
    inside = rr <= mr
    nx, ny = dx / mr, dy / mr
    nz = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
    phase = math.acos(2 * 0.935 - 1)  # sun-moon-earth angle
    sun = np.array([-math.sin(phase), 0.0, math.cos(phase)])  # sun off to the east (left)
    lam = np.clip(nx * sun[0] + nz * sun[2], 0, 1) ** 0.5 * (0.75 + 0.25 * nz)
    rng = np.random.default_rng(29)
    maria = np.zeros_like(L)
    for (ux, uy, ur) in [(-0.2, -0.35, 0.33), (0.25, -0.3, 0.25), (0.35, 0.1, 0.3), (-0.45, 0.15, 0.3), (0.1, 0.35, 0.2), (0.55, -0.45, 0.14)]:
        maria += 0.45 * np.exp(-((nx - ux) ** 2 + (ny - uy) ** 2) / ur ** 2)
    moon = np.clip(lam * (1 - np.clip(maria, 0, 0.6)), 0, 1)
    L[inside] = moon[inside]
    ix, iy, ir = 188, 188, 36.0
    ddx, ddy = (xx - ix) / ir, (yy - iy) / ir
    ins = ddx ** 2 + ddy ** 2 <= 1
    nz2 = np.sqrt(np.clip(1 - ddx ** 2 - ddy ** 2, 0, 1))
    lam2 = np.clip(ddx * sun[0] + nz2 * sun[2], 0, 1) ** 0.5 * (0.75 + 0.25 * nz2)
    mar2 = np.zeros_like(L)
    for (ux, uy, ur) in [(-0.2, -0.35, 0.33), (0.25, -0.3, 0.25), (0.35, 0.1, 0.3), (-0.45, 0.15, 0.3), (0.1, 0.35, 0.2), (0.55, -0.45, 0.14)]:
        mar2 += 0.45 * np.exp(-((ddx - ux) ** 2 + (ddy - uy) ** 2) / ur ** 2)
    for _ in range(40):  # craters
        cx_, cy_, cr_ = rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.9), rng.uniform(0.03, 0.09)
        dd_ = np.hypot(ddx - cx_, ddy - cy_)
        mar2 += 0.35 * ((dd_ < cr_) & (ddx - cx_ > 0)) - 0.25 * ((dd_ < cr_) & (ddx - cx_ < 0))
    L[ins] = np.clip(lam2 * (1 - np.clip(mar2, -0.2, 0.6)), 0, 1)[ins]
    glow &= ~(np.hypot(xx - ix, yy - iy) <= ir + 2)
    img = tonal(L, np.zeros((H, W), np.int8))
    ga = np.asarray(img).copy(); ga[glow] = WHITE; img = Image.fromarray(ga)
    d = crisp(img)
    f9 = font(MONO, 9)
    for name, (h, m_, s), (dd, dm), mag in stars:
        x, y = P(h + m_ / 60 + s / 3600, dd + dm / 60)
        r = max(1.2, 5.2 - 0.85 * mag)
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
        if mag < 4.3 and r > 1.5:
            d.line([(x - r - 4, y), (x + r + 4, y)], fill=WHITE)
    pos = {n_: P(h + m_ / 60 + s_ / 3600, dd + dm / 60) for n_, (h, m_, s_), (dd, dm), mag in stars}
    lab = {"Alcyone": (0, 12, "mt"), "Atlas": (-8, 6, "rt"), "Pleione": (-8, -6, "rb"),
           "Electra": (8, 2, "lm"), "Celaeno": (8, -4, "lb"), "Merope": (7, 5, "lt"),
           "Maia": (-7, -3, "rb"), "Taygeta": (8, -3, "lb"), "Asterope": (0, -6, "mb")}
    for name, (ox, oy, anc) in lab.items():
        x, y = pos[name]
        d.text((x + ox, y + oy), name, font=font(MONO, 8), fill=WHITE, anchor=anc)
    # Aldebaran is 12° off-frame to the south-east: the red eye of the Bull points in
    ax, ay_ = P(4 + 35.9 / 60, 16.51)
    ang = math.atan2(ay_ - H / 2, ax - W / 2)
    ex, ey = 10, H - 58
    d.polygon([(ex - 4, ey), (ex + 10, ey - 7), (ex + 10, ey + 7)], fill=RED)
    d.line([(ex + 10, ey), (ex + 34, ey)], fill=RED, width=2)
    d.text((ex, ey + 10), "ALDEBARAN 12° ←", font=f9, fill=RED)
    d.text((ex, ey + 21), "the Bull's red eye", font=font(SERIFI, 10), fill=WHITE)
    d.text((W - 8, 8), "THE SEVEN SISTERS", font=font(SERIFB, 17), fill=WHITE, anchor="ra")
    d.text((W - 8, 29), "and a 93% moon, late tonight", font=font(SERIFI, 12), fill=WHITE, anchor="ra")
    d.rectangle([mx - 16, my + mr + 5, mx + 16, my + mr + 16], fill=BLACK)
    d.text((mx, my + mr + 6), "MOON", font=f9, fill=WHITE, anchor="ma")
    ix, iy, ir = 188, 188, 36.0
    d.ellipse([mx - mr - 3, my - mr - 3, mx + mr + 3, my + mr + 3], outline=WHITE)
    for k in range(0, 10, 2):  # dotted zoom lines from the real moon to the inset
        t0, t1 = k / 10, (k + 1) / 10
        for sgn in (-1, 1):
            d.line([(mx + sgn * mr + (ix + sgn * ir * 0.7 - mx - sgn * mr) * t0, my - mr + (iy + ir * 0.7 - my + mr) * t0),
                    (mx + sgn * mr + (ix + sgn * ir * 0.7 - mx - sgn * mr) * t1, my - mr + (iy + ir * 0.7 - my + mr) * t1)], fill=WHITE)
    # 1° scale bar
    d.rectangle([W - 12 - sc, H - 34, W - 4, H - 16], fill=BLACK)
    d.line([(W - 8 - sc, H - 30), (W - 8, H - 30)], fill=WHITE)
    d.text((W - 8 - sc / 2, H - 28), "1°", font=f9, fill=WHITE, anchor="ma")
    footer(d, 4, "east is left · positions approximate", fill=WHITE)
    return img

# ---------------------------------------------------------------- 5. Caravaggio: one window of light
def caravaggio():
    SS = 2
    w, h = W * SS, H * SS
    cam = np.array([0.15, 0.45, -2.9])
    js, is_ = np.meshgrid(np.arange(w), np.arange(h))
    u = (js + 0.5 - w / 2) / (h / 2) * 0.52
    v = -(is_ + 0.5 - h / 2) / (h / 2) * 0.52
    D = np.stack([u, v - 0.12, np.ones_like(u)], -1)
    D /= np.linalg.norm(D, axis=-1, keepdims=True)
    D = D.reshape(-1, 3)
    O = np.broadcast_to(cam, D.shape)
    light = np.array([-5.0, 4.6, -2.6])
    TOP = -0.5
    # objects: spheres/ellipsoids (centre, radii, albedo, spec, red?)
    objs = [((0.30, TOP + 0.44, 0.75), (0.44, 0.42, 0.44), 0.95, 0.9, 1),    # apple
            ((1.18, TOP + 0.50, 1.15), (0.31, 0.50, 0.31), 0.85, 0.3, 0),    # pear
            ((0.95, TOP + 0.23, 0.25), (0.23, 0.22, 0.23), 0.55, 0.5, 0),    # fig
            ((-0.35, TOP + 0.13, 0.05), (0.14,) * 3, 0.15, 1.0, 0)]          # a fallen grape
    rng = np.random.default_rng(1571)
    gpos = []
    for layer, (n, yy) in enumerate([(6, 0.14), (4, 0.39), (2, 0.63)]):
        for k in range(n):
            gpos.append((-0.85 + (k - (n - 1) / 2) * 0.24 + rng.uniform(-0.03, 0.03), TOP + yy,
                         0.9 + (k % 2) * 0.2 + layer * 0.06))
    for g in gpos:
        objs.append((g, (0.14,) * 3, 0.42, 1.0, 0))

    def hit_ellipsoid(O, D, c, r):
        c, r = np.array(c), np.array(r)
        o = (O - c) / r; dd = D / r
        a = (dd * dd).sum(-1); b = 2 * (o * dd).sum(-1); cc = (o * o).sum(-1) - 1
        disc = b * b - 4 * a * cc
        t = (-b - np.sqrt(np.clip(disc, 0, None))) / (2 * a)
        t[(disc < 0) | (t < 1e-4)] = np.inf
        return t

    def box(O, D, lo, hi):
        lo, hi = np.array(lo), np.array(hi)
        with np.errstate(divide="ignore", invalid="ignore"):
            t1 = (lo - O) / D; t2 = (hi - O) / D
        tmin = np.nanmax(np.minimum(t1, t2), -1); tmax = np.nanmin(np.maximum(t1, t2), -1)
        t = np.where((tmax >= tmin) & (tmin > 1e-4), tmin, np.inf)
        return t

    KNIFE = ((-0.05, TOP, -0.95), (0.08, TOP + 0.05, -0.25))   # handle
    BLADE = ((-0.02, TOP, -0.25), (0.05, TOP + 0.012, 0.35))
    def scene(O, D):
        n = D.shape[0]
        best = np.full(n, np.inf); idx = np.full(n, -1)
        for i, (c, r, *_ ) in enumerate(objs):
            t = hit_ellipsoid(O, D, c, r)
            m = t < best; best[m] = t[m]; idx[m] = i
        for k, (lo, hi) in enumerate(()):
            t = box(O, D, lo, hi)
            m = t < best; best[m] = t[m]; idx[m] = 100 + k
        with np.errstate(divide="ignore", invalid="ignore"):
            tt = (TOP - O[:, 1]) / D[:, 1]
        P = O + D * tt[:, None]
        m = (tt > 1e-4) & (tt < best) & (P[:, 2] > -0.6) & (P[:, 2] < 3.0)
        best[m] = tt[m]; idx[m] = 200
        with np.errstate(divide="ignore", invalid="ignore"):
            tf = (-0.6 - O[:, 2]) / D[:, 2]
        P = O + D * tf[:, None]
        m = (tf > 1e-4) & (tf < best) & (P[:, 1] < TOP)
        best[m] = tf[m]; idx[m] = 201
        with np.errstate(divide="ignore", invalid="ignore"):
            tw = (3.0 - O[:, 2]) / D[:, 2]
        m = (tw > 1e-4) & (tw < best)
        best[m] = tw[m]; idx[m] = 202
        return best, idx

    t, idx = scene(O, D)
    P = O + D * np.where(np.isfinite(t), t, 0)[:, None]
    N = np.zeros_like(P)
    for i, (c, r, *_ ) in enumerate(objs):
        m = idx == i
        N[m] = (P[m] - np.array(c)) / np.array(r) ** 2
    for k, (lo, hi) in enumerate((KNIFE, BLADE)):
        m = idx == 100 + k
        c = (np.array(lo) + np.array(hi)) / 2; hsz = (np.array(hi) - np.array(lo)) / 2
        q = (P[m] - c) / hsz
        ax_ = np.argmax(np.abs(q), -1)
        nn = np.zeros_like(q); nn[np.arange(len(q)), ax_] = np.sign(q[np.arange(len(q)), ax_])
        N[m] = nn
    N[idx == 200] = (0, 1, 0); N[idx == 201] = (0, 0, -1); N[idx == 202] = (0, 0, -1)
    N /= np.linalg.norm(N, axis=-1, keepdims=True) + 1e-9
    Ldir = light - P
    ld = np.linalg.norm(Ldir, axis=-1, keepdims=True); Ldir /= ld
    ts, _ = scene(P + N * 1e-3, Ldir)
    lit = (ts > ld[:, 0]).astype(np.float64)
    diff = np.clip((N * Ldir).sum(-1), 0, 1)
    Rv = 2 * (N * Ldir).sum(-1, keepdims=True) * N - Ldir
    spec = np.clip((Rv * -D).sum(-1), 0, 1)
    alb = np.full(len(P), 0.5); ks = np.zeros(len(P)); red = np.zeros(len(P), bool)
    for i, (c, r, a, s, isred) in enumerate(objs):
        m = idx == i; alb[m] = a; ks[m] = s; red[m] = bool(isred)
    alb[idx >= 100] = 0.25; ks[idx == 101] = 1.2; alb[idx == 101] = 0.6
    alb[idx == 200] = 0.62; alb[idx == 201] = 0.0; alb[idx == 202] = 0.55
    # the famous raking shaft on the back wall: light enters through a high window, left
    wall = idx == 202
    shaft = 1 / (1 + np.exp(-((P[:, 1] - (-0.55 * P[:, 0] + 1.25)) / 0.07)))
    shaft = 1 - shaft  # lit below the diagonal line
    fall = np.clip(1 - (P[:, 0] + 2.2) / 5.5, 0, 1) ** 1.3
    Lum = alb * diff * lit + ks * spec ** 36 * lit
    Lum[wall] = (alb * diff * shaft * fall)[wall] * 1.15
    Lum[idx == 200] *= np.clip(1.3 - (P[idx == 200, 0] + 1.5) / 4, 0.1, 1.1)
    Lum = np.clip(Lum, 0, 1) ** 1.2
    Lum[red] = np.clip(alb[red] * diff[red] * lit[red] * 0.62 + ks[red] * spec[red] ** 40 * lit[red], 0, 1)
    Lum = Lum.reshape(h, w); red = red.reshape(h, w)
    L1 = Lum.reshape(H, SS, W, SS).mean((1, 3))
    m1 = (red.reshape(H, SS, W, SS).mean((1, 3)) > 0.5).astype(np.int8)
    L1 = L1 + np.random.default_rng(5).normal(0, 0.025, L1.shape) * (L1 > 0.03)
    img = tonal(L1, m1)
    d = crisp(img)
    d.text((W - 10, 12), "CARAVAGGIO", font=font(SERIFB, 15), fill=WHITE, anchor="ra")
    d.text((W - 10, 30), "born 29 September 1571", font=font(SERIFI, 11), fill=WHITE, anchor="ra")
    footer(d, 5, "one window of light", fill=WHITE, x="r")
    return img

if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["1", "2", "3", "4", "5"]
    fns = {"1": michaelmas, "2": fermi, "3": alouette, "4": pleiades, "5": caravaggio}
    names = {"1": "michaelmas", "2": "fermi", "3": "alouette", "4": "pleiades", "5": "caravaggio"}
    for k in which:
        save(fns[k](), k, names[k])
