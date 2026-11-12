#!/usr/bin/env python3
"""2026-11-12 — theme: arrivals.  Run from the repo root: python3 archive/2026-11-12/generate.py"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
K, WH, R = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = ["images", "archive/2026-11-12"]
F = "/usr/share/fonts/truetype/"
PATHS = {"mono": F + "dejavu/DejaVuSansMono.ttf", "monob": F + "dejavu/DejaVuSansMono-Bold.ttf",
         "ital": F + "liberation/LiberationSerif-Italic.ttf", "serif": F + "liberation/LiberationSerif-Regular.ttf",
         "serifb": F + "liberation/LiberationSerif-Bold.ttf", "bital": F + "liberation/LiberationSerif-BoldItalic.ttf",
         "black": "/usr/share/fonts/opentype/inter/Inter-Black.otf",
         "bold": "/usr/share/fonts/opentype/inter/Inter-Bold.otf"}
def font(name, size): return ImageFont.truetype(PATHS[name], size)
def canvas(bg=WH):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im); d.fontmode = "1"; return im, d
def save(im, n):
    pal = Image.new("P", (1, 1)); pal.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0, 0, 0] * 253)
    q = im.quantize(palette=pal, dither=Image.Dither.NONE)
    for o in OUT:
        os.makedirs(o, exist_ok=True); q.save(f"{o}/{n}.png")
def lines(d, x, y, rows, f, fill, lead=13):
    for i, s in enumerate(rows): d.text((x, y + i * lead), s, font=f, fill=fill)

# ---------------------------------------------------------------- 1. Saturn, a vidicon frame
def saturn():
    S = 3; w, h = W * S, H * S
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    cx, cy, Rp = 204 * S, 112 * S, 60 * S
    roll, B = math.radians(-16), math.radians(17)
    x = (xx - cx) / Rp; y = -(yy - cy) / Rp
    u = x * math.cos(roll) + y * math.sin(roll); wv = -x * math.sin(roll) + y * math.cos(roll)
    sB, cB = math.sin(B), math.cos(B); f = 0.90
    P0 = (-wv * sB, u, wv * cB); v = (cB, 0.0, sB)
    az, el = math.radians(-38), math.radians(9)
    s = (math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))

    def hit(P, D):  # ray P + t D against the oblate globe; returns (mask, far root)
        a = D[0] ** 2 + D[1] ** 2 + (D[2] / f) ** 2
        b = 2 * (P[0] * D[0] + P[1] * D[1] + P[2] * D[2] / f ** 2)
        c = P[0] ** 2 + P[1] ** 2 + (P[2] / f) ** 2 - 1
        disc = b * b - 4 * a * c
        return disc >= 0, (-b + np.sqrt(np.maximum(disc, 0))) / (2 * a)

    def rings(rho):  # brightness, opacity
        br = np.zeros_like(rho); op = np.zeros_like(rho)
        fine = 0.5 + 0.5 * np.sin(rho * 140) * np.sin(rho * 37 + 1)
        for lo, hi, b0, o0, k in ((1.24, 1.53, .16, .22, .08), (1.53, 1.95, .92, .95, .16),
                                  (1.95, 2.03, .03, .08, 0), (2.03, 2.27, .58, .7, .12)):
            m = (rho >= lo) & (rho < hi)
            br[m] = b0 - k * fine[m]; op[m] = o0
        g = (rho > 2.205) & (rho < 2.222); br[g] = 0; op[g] = 0
        return br, op

    on, ts = hit(P0, v)
    G = [P0[i] + ts * v[i] for i in range(3)]
    n = np.stack([G[0], G[1], G[2] / f ** 2]); n /= np.linalg.norm(n, axis=0)
    lam = np.clip(n[0] * s[0] + n[1] * s[1] + n[2] * s[2], 0, 1) ** 0.75
    lat = np.arcsin(np.clip(G[2] / f, -1, 1))
    bands = 0.74 + 0.11 * np.sin(lat * 13) + 0.07 * np.sin(lat * 29 + 1.2) + 0.04 * np.sin(lat * 61)
    globe = lam * bands
    tsh = -G[2] / s[2]                                   # ring shadow thrown on the globe
    rs = np.hypot(G[0] + tsh * s[0], G[1] + tsh * s[1])
    _, ops = rings(rs); globe *= np.where(tsh > 0, 1 - 0.85 * ops, 1)
    globe = np.where(on, globe, 0)

    tr = -P0[2] / v[2]
    Q = [P0[i] + tr * v[i] for i in range(3)]
    br, op = rings(np.hypot(Q[0], Q[1]))
    sh, tq = hit(Q, s); br = np.where(sh & (tq > 0), br * 0.02, br)   # the globe's shadow on the rings
    front = ~on | (tr > ts)
    img = np.where(front, br * op + globe * (1 - op), globe)
    img = img.reshape(H, S, W, S).mean(axis=(1, 3)) ** 0.9
    rng = np.random.default_rng(1980)
    img = np.clip(img + (img > 0.02) * rng.normal(0, 0.02, img.shape), 0, 1)
    bw = Image.fromarray((img * 255).astype(np.uint8)).convert("1").convert("RGB")
    d = ImageDraw.Draw(bw); d.fontmode = "1"
    for gy in range(14, 236, 34):                        # reseau marks, as burnt into every Voyager frame
        for gx in range(13, W, 34):
            d.rectangle((gx, gy, gx + 1, gy + 1), fill=K)
    d.rectangle((0, 236, W, H), fill=K)
    d.ellipse((43, 37, 51, 45), fill=R)
    fm = font("mono", 10)
    d.text((58, 36), "TITAN, the day before", font=fm, fill=WH)
    d.line((14, 244, W - 15, 244), fill=WH)
    d.text((14, 251), "12 NOV 1980", font=font("monob", 10), fill=R)
    d.text((86, 251), "Voyager 1 passes Saturn, some 125,000 km", font=fm, fill=WH)
    lines(d, 14, 264, ["above the clouds. Titan has bent its path north, out of the",
                       "plane of the planets. It has not stopped since."], fm, WH)
    save(bw, 1)

# ---------------------------------------------------------------- 2. Léotard, a chronophotograph
def leotard():
    im, d = canvas(K)
    yy, xx = np.mgrid[0:H, 0:W]
    screens = {1: (xx % 2 == 0) & (yy % 2 == 0), 2: (xx + yy) % 2 == 0, 4: np.ones((H, W), bool)}
    L, top = 112, 12
    def figure(md, hx, hy, phi, spread=5):
        dx, dy = math.sin(phi), math.cos(phi); px, py = dy, -dx
        at = lambda t, o=0: (hx + dx * t + px * o, hy + dy * t + py * o)
        for o in (-7, 7): md.line([at(0, o * 0.3), at(24, o)], fill=255, width=3)
        hc = at(15); md.ellipse((hc[0] - 6, hc[1] - 6, hc[0] + 6, hc[1] + 6), fill=255)
        md.polygon([at(23, -8), at(23, 8), at(48, 5), at(48, -5)], fill=255)
        sp = math.radians(spread)
        for sgn in (-1, 1):
            a = phi + sgn * sp; h = at(47, sgn * 3)
            k = (h[0] + math.sin(a) * 17, h[1] + math.cos(a) * 17)
            a2 = a - sgn * sp * 0.6; e = (k[0] + math.sin(a2) * 17, k[1] + math.cos(a2) * 17)
            md.line([h, k, e], fill=255, width=5)
            md.line([e, (e[0] + px * 5, e[1] + py * 5)], fill=255, width=3)
    def stamp(draw_fn, level, col):
        m = Image.new("L", (W, H), 0); draw_fn(ImageDraw.Draw(m))
        a = (np.array(m) > 0) & screens[level]
        arr = np.array(im); arr[a] = col; im.paste(Image.fromarray(arr))
    def swing(pivot, th, level):
        bx, by = pivot + L * math.sin(th), top + L * math.cos(th)
        def fn(md):
            md.line((pivot, top, bx, by), fill=255, width=1 if level < 4 else 2)
            md.ellipse((bx - 2, by - 2, bx + 2, by + 2), fill=255)
            figure(md, bx, by, th * 1.1, spread=7)
        stamp(fn, level, WH)
    A, Bp = 104, 296
    for th in (-36, -4, 28): swing(A, math.radians(th), 2)
    swing(Bp, math.radians(24), 2)
    swing(Bp, math.radians(-38), 4)
    stamp(lambda md: figure(md, 212, 80, math.radians(-74), spread=16), 4, R)   # in the air
    d = ImageDraw.Draw(im); d.fontmode = "1"
    d.rectangle((0, top - 4, W, top - 1), fill=WH)
    for p in (A, Bp): d.rectangle((p - 3, top - 1, p + 3, top + 2), fill=WH)
    d.rectangle((0, 232, W, H), fill=K)
    d.line((14, 236, W - 15, 236), fill=WH)
    d.text((13, 244), "LÉOTARD", font=font("black", 36), fill=WH)
    fm = font("mono", 10)
    d.text((196, 249), "12 NOV 1859", font=font("monob", 10), fill=R)
    lines(d, 196, 262, ["Cirque Napoléon, Paris. He lets", "go of one bar to catch another."], fm, WH)
    save(im, 2)

# ---------------------------------------------------------------- 3. Philae, three landings
def philae():
    im, d = canvas()
    x0, sc, base = 38, 2.72, 214
    t = [0, 111, 118]                                    # minutes after 15:34 UTC
    X = [x0 + sc * m for m in t]
    rng = np.random.default_rng(67)
    gx = np.arange(0, W); gy = base + 1 + np.cumsum(rng.normal(0, 0.35, W)); gy -= np.linspace(0, gy[-1] - base - 1, W)
    for a, b in zip(gx, gy): d.point((a, max(b, base + 1)), fill=K)
    def arc(xa, xb, hgt, step):
        n = int((xb - xa) * 3)
        for i in range(n + 1):
            p = i / n; x = xa + (xb - xa) * p; y = base - hgt * 4 * p * (1 - p)
            if i % step == 0: d.point((x, y), fill=K)
    arc(X[0], X[1], 162, 6); arc(X[1], X[2], 8, 2)
    for i in range(0, 48, 3): d.point((X[0] - 26 + i * 26 / 48, 18 + (base - 18) * (i / 48) ** 1.6), fill=K)  # coming in
    for xk in X[:2]: d.line((xk, base - 3, xk, base + 3), fill=K)
    d.ellipse((X[2] - 4, base - 8, X[2] + 4, base), fill=R)
    fm = font("mono", 10)
    d.text((X[0] - 15, base + 9), "15:34", font=fm, fill=K)
    d.text((X[1] - 34, base + 9), "17:25", font=fm, fill=K)
    d.text((X[2] - 2, base + 9), "17:32", font=fm, fill=R)
    d.text(((X[0] + X[1]) / 2 - 33, base - 180), "about 1 km", font=fm, fill=K)
    d.text((W - 138, 12), "Three landings", font=font("ital", 20), fill=K)
    d.text((14, 252), "12 NOV 2014", font=font("monob", 10), fill=R)
    d.text((86, 252), "Philae reaches comet 67P. The harpoons do", font=fm, fill=K)
    lines(d, 14, 265, ["not fire, and the comet barely pulls. It lands, and lands,",
                       "and lands. (Times UTC.)"], fm, K)
    save(im, 3)

# ---------------------------------------------------------------- 4. Rayleigh, what gets through
def rayleigh():
    im, d = canvas()
    xa, xb = 70, 380; rows = [400, 450, 500, 550, 600, 700]; L400 = 46.0
    d.text((12, 8), "The long way through the air", font=font("ital", 20), fill=K)
    d.ellipse((-157, 38, 33, 228), fill=R)       # the sun, at the left edge
    fm = font("mono", 10)
    for i, lam in enumerate(rows):
        yc = 58 + i * 30; Ld = L400 * (lam / 400) ** 4; col = R if lam == 700 else K
        pts = []
        for k in range((xb - xa) * 4 + 1):
            x = xa + k / 4; amp = 12 * math.exp(-(x - xa) / (2 * Ld))
            pts.append((x, yc - amp * math.sin(2 * math.pi * (x - xa) / (lam / 25))))
        d.line(pts, fill=col, width=2)
        d.text((40, yc - 6), f"{lam}", font=fm, fill=col)
    d.text((40, 222), "nm", font=fm, fill=K)
    d.line((xb + 6, 46, xb + 6, 220), fill=K); d.text((xb - 16, 224), "you", font=fm, fill=K)
    d.line((14, 244, W - 15, 244), fill=K)
    d.text((14, 251), "12 NOV 1842", font=font("monob", 10), fill=R)
    d.text((86, 251), "Lord Rayleigh is born. In 1871 he shows air", font=fm, fill=K)
    lines(d, 14, 264, ["scatters light by the inverse fourth power of its wavelength.",
                       "Violet goes nine times faster than red. Sunset is the rest."], fm, K)
    save(im, 4)

# ---------------------------------------------------------------- 5. Ellis Island, a tag
def ellis():
    im, d = canvas()
    yy, xx = np.mgrid[0:H, 0:W]
    arr = np.where(((xx + yy) % 2 == 0)[..., None], np.uint8(0), np.uint8(255)).repeat(3, axis=2)
    im = Image.fromarray(arr.astype(np.uint8)); d = ImageDraw.Draw(im); d.fontmode = "1"
    tag = [(62, 24), (386, 24), (386, 276), (62, 276), (20, 234), (20, 66)]
    d.polygon([(x + 4, y + 4) for x, y in tag], fill=K)
    d.polygon(tag, fill=WH); d.line(tag + [tag[0]], fill=K, width=2)
    ex, ey = 50, 150
    d.ellipse((ex - 15, ey - 15, ex + 15, ey + 15), outline=K, width=1)
    d.ellipse((ex - 9, ey - 9, ex + 9, ey + 9), fill=K)
    d.ellipse((ex - 6, ey - 6, ex + 6, ey + 6), fill=WH)
    for dy in (-34, 30):                                  # the string
        pts = [(ex - 2 - t * 52, ey + dy * t ** 1.5) for t in np.linspace(0, 1, 30)]
        d.line(pts, fill=K, width=5); d.line(pts, fill=WH, width=3)
    fm = font("mono", 10)
    d.text((80, 36), "U.S. DEPARTMENT OF JUSTICE", font=fm, fill=K)
    d.text((80, 48), "IMMIGRATION AND NATURALIZATION SERVICE", font=fm, fill=K)
    d.text((78, 62), "ELLIS ISLAND", font=font("black", 41), fill=K)
    d.line((80, 114, 370, 114), fill=K, width=2)
    fv = font("monob", 12)
    for y, lab, val in ((122, "OPENED", "1 January 1892"), (160, "PASSED THROUGH", "some twelve million"),
                        (198, "LAST HELD", "Arne Peterssen, seaman, of Norway")):
        d.text((80, y), lab, font=fm, fill=K); d.text((82, y + 14), val, font=fv, fill=K)
        for x in range(80, 371, 3): d.point((x, y + 31), fill=K)
    d.text((80, 244), "PORT OF NEW YORK", font=fm, fill=K)
    d.text((80, 256), "No. 12-11-54", font=fm, fill=K)
    # the rubber stamp
    sw, sh = 138, 62; m = Image.new("L", (sw, sh), 0); md = ImageDraw.Draw(m); md.fontmode = "1"
    md.rounded_rectangle((1, 1, sw - 2, sh - 2), radius=7, outline=255, width=3)
    md.rounded_rectangle((6, 6, sw - 7, sh - 7), radius=4, outline=255, width=1)
    fb = font("black", 30); tw = md.textlength("CLOSED", font=fb); md.text(((sw - tw) / 2, 6), "CLOSED", font=fb, fill=255)
    fs = font("black", 14); tw = md.textlength("NOV 12 1954", font=fs); md.text(((sw - tw) / 2, 40), "NOV 12 1954", font=fs, fill=255)
    m = m.rotate(11, resample=Image.Resampling.BICUBIC, expand=True).point(lambda p: 255 if p > 110 else 0)
    rng = np.random.default_rng(1954); a = np.array(m) > 0
    noise = rng.random(a.shape); blot = Image.fromarray((rng.random((a.shape[0] // 6 + 1, a.shape[1] // 6 + 1)) * 255).astype(np.uint8))
    blot = np.array(blot.resize((a.shape[1], a.shape[0]), Image.Resampling.BICUBIC)) / 255
    a &= (noise > 0.06) & ~((blot > 0.78) & (noise < 0.45))
    ox, oy = 236, 128; arr = np.array(im)
    arr[oy:oy + a.shape[0], ox:ox + a.shape[1]][a] = R
    save(Image.fromarray(arr), 5)

if __name__ == "__main__":
    saturn(); leotard(); philae(); rayleigh(); ellis()
    sheet = os.environ.get("SHEET")
    if sheet:
        s = Image.new("RGB", (W * 2 + 30, H * 3 + 40), (120, 120, 160))
        for i in range(5):
            s.paste(Image.open(f"images/{i + 1}.png").convert("RGB"), (10 + (i % 2) * (W + 10), 10 + (i // 2) * (H + 10)))
        s.resize((s.width * 2, s.height * 2), Image.Resampling.NEAREST).save(sheet)
