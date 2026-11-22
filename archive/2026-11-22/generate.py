#!/usr/bin/env python3
"""2026-11-22 (Sun). Theme: passing through.
Run from the repo root:  python3 archive/2026-11-22/generate.py
Writes images/1..5.png and archive/2026-11-22/1..5.png (400x300, black/white/red)."""
import math, os, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, S = 400, 300, 3
K, Wh, R = (0, 0, 0), (255, 255, 255), (255, 0, 0)
INKS = np.array([K, Wh, R], dtype=np.int32)
OUT = "archive/2026-11-22"
F = "/usr/share/fonts/truetype/dejavu/"
MONO = F + "DejaVuSansMono.ttf"
MONOB = F + "DejaVuSansMono-Bold.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-Black.otf"


def font(p, s):
    return ImageFont.truetype(p, s)


def snap(img):
    a = np.asarray(img.convert("RGB"), dtype=np.int32)
    d = ((a[:, :, None, :] - INKS[None, None]) ** 2).sum(-1)
    return Image.fromarray(INKS[d.argmin(-1)].astype(np.uint8), "RGB")


def down(img):
    return snap(img.resize((W, H), Image.LANCZOS))


def save(img, n):
    img = snap(img)
    pal = Image.new("P", (1, 1))
    pal.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0] * 759)
    q = img.quantize(palette=pal, dither=Image.NONE)
    os.makedirs("images", exist_ok=True)
    q.save(f"{OUT}/{n}.png")
    shutil.copy(f"{OUT}/{n}.png", f"images/{n}.png")


def pen(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return d


def s3(pts):
    return [(x * S, y * S) for x, y in pts]


# ---------------------------------------------------------------- 1. Under the wires
def under_the_wires():
    rng = np.random.default_rng(1935)
    big = Image.new("RGB", (W * S, H * S), Wh)
    d = ImageDraw.Draw(big)
    SEA = 246
    TX = (62, 338)
    TOP = 26

    # far shore: low hills in a 50 % screen (painted after the downscale)
    # main cable: parabola in the centre span, straight-ish backstays off the frame
    def cable(x):
        if TX[0] <= x <= TX[1]:
            u = (x - 200) / (TX[1] - 200)
            return 150 - (150 - TOP) * u * u
        dx = TX[0] - x if x < TX[0] else x - TX[1]
        return TOP + dx * 1.45 + 0.004 * dx * dx

    pts = [(x, cable(x)) for x in np.arange(-4, 404.5, 0.5)]
    d.line(s3(pts), fill=K, width=7)
    # catwalk slung just under the cable, with hangers
    cw = [(x, cable(x) + 7) for x in np.arange(-4, 404.5, 0.5)]
    for i in range(0, len(cw) - 6, 14):
        d.line(s3(cw[i:i + 9]), fill=K, width=3)
    for x in range(4, 400, 12):
        d.line(s3([(x, cable(x)), (x, cable(x) + 7)]), fill=K, width=2)
    # the first suspender ropes, hanging loose near each tower (no deck yet)
    for x, L in [(86, 150), (98, 96), (110, 120), (122, 52), (134, 70), (314, 140), (302, 110),
                 (290, 64), (278, 84), (266, 40)]:
        d.line(s3([(x, cable(x)), (x, min(cable(x) + L, 214))]), fill=K, width=2)
    # towers
    for tx in TX:
        d.polygon(s3([(tx - 4.5, TOP - 6), (tx + 4.5, TOP - 6), (tx + 8, SEA - 14), (tx - 8, SEA - 14)]), fill=K)
        for y in range(TOP + 8, SEA - 30, 22):       # portal slots
            w = 2.2 + 2.2 * (y - TOP) / (SEA - TOP)
            d.rectangle([(tx - w) * S, y * S, (tx + w) * S, (y + 13) * S], fill=Wh)
            d.line(s3([(tx - w, y), (tx + w, y + 13)]), fill=K, width=2)
            d.line(s3([(tx + w, y), (tx - w, y + 13)]), fill=K, width=2)
        d.rectangle([(tx - 7) * S, (TOP - 10) * S, (tx + 7) * S, (TOP - 5) * S], fill=K)   # saddle
        d.polygon(s3([(tx - 13, SEA - 14), (tx + 13, SEA - 14), (tx + 17, SEA + 2), (tx - 17, SEA + 2)]), fill=K)
    # sea
    d.rectangle([0, SEA * S, W * S, H * S], fill=K)

    # the flying boat, nose to the west (left), nosed down a little
    P = Image.new("L", (110 * S, 60 * S), 0)
    p = ImageDraw.Draw(P)
    ox, oy = 20, 34

    def T(pts):
        return [((ox + x) * S, (oy + y) * S) for x, y in pts]
    hull = [(0, 1), (3, -3), (9, -6), (15, -7), (44, -6), (60, -9), (72, -12), (72, -9), (58, -3),
            (44, 3), (36, 5.5), (35, 7.5), (12, 7.5), (4, 5)]
    p.polygon(T(hull), fill=255)
    p.polygon(T([(60, -9), (64, -24), (72, -25), (74, -10)]), fill=255)            # fin
    p.rectangle([(ox + 57) * S, (oy - 16) * S, (ox + 78) * S, (oy - 14) * S], fill=255)  # tailplane
    p.polygon(T([(22, -7), (25, -14), (36, -14), (38, -7)]), fill=255)             # wing pylon
    p.polygon(T([(14, -17), (20, -19.5), (44, -17), (46, -15), (20, -14)]), fill=255)   # wing, edge on
    p.ellipse([(ox + 11) * S, (oy - 20) * S, (ox + 27) * S, (oy - 12.5) * S], fill=255)  # nacelle
    p.line(T([(10, -29), (10, -4)]), fill=255, width=2)                            # propeller disc
    p.polygon(T([(18, 3), (38, 3), (36, 6), (20, 6)]), fill=255)                   # sea-wing
    p.line(T([(30, -13), (27, 3)]), fill=255, width=2)
    p.line(T([(36, -13), (34, 3)]), fill=255, width=2)
    for wx in range(14, 44, 5):                                                    # cabin windows
        p.rectangle([(ox + wx) * S, (oy - 3) * S, (ox + wx + 2) * S, (oy - 1) * S], fill=0)
    p.polygon(T([(4.5, -2.5), (8.5, -5), (11, -5), (11, -2.5)]), fill=0)           # windscreen
    P = P.rotate(5, resample=Image.BICUBIC).resize((int(110 * S * 1.3), int(60 * S * 1.3)), Image.LANCZOS)
    big.paste(R, (140 * S, 146 * S), P)
    img = down(big)

    a = np.array(img)
    yy, xx = np.mgrid[0:H, 0:W]
    # far shore in a true grey
    hill = SEA - (7 + 5 * np.sin(xx / 47 + 1) + 3 * np.sin(xx / 19) + 4 * np.sin(xx / 91 + 2))
    m = (yy >= hill) & (yy < SEA) & ((xx + yy) % 2 == 0) & (a.sum(-1) == 765)
    a[m] = K
    # water: white dashes, longer and sparser towards the viewer
    for y in range(SEA + 3, H - 16, 3):
        t = (y - SEA) / (H - SEA)
        x = int(rng.integers(0, 12))
        while x < W:
            L = int(rng.integers(2, 5 + int(26 * t)))
            if rng.random() < 0.55 - 0.3 * t:
                a[y, x:min(W, x + L)] = Wh
            x += L + int(rng.integers(3, 8 + int(20 * t)))
    # the boat's reflection: a broken red smear
    for y in range(SEA + 5, SEA + 20, 3):
        for x in range(166, 246, 1):
            if rng.random() < 0.5 - (y - SEA) * 0.02:
                a[y, x] = R
    a[H - 15:] = K
    img = Image.fromarray(a)
    d = pen(img)
    d.text((W // 2, H - 8), "22 NOV 1935  CHINA CLIPPER, TOO HEAVY TO CLIMB, GOES UNDER",
           font=font(MONO, 10), fill=Wh, anchor="mm")
    save(img, 1)


# ---------------------------------------------------------------- 2. One figure, 169 times
def bolero():
    big = Image.new("RGB", (W * S, H * S), R)
    d = ImageDraw.Draw(big)
    N = 169
    rho = [0.8 + 7.4 * (i / (N - 1)) ** 1.55 for i in range(N)]
    g = 2.0
    r, th = 5.0, 0.0
    pos = []
    for i in range(N):
        pos.append((r * math.cos(th), r * math.sin(th)))
        if i == N - 1:
            break
        ds = rho[i] + rho[i + 1] + g
        j = min(N - 1, i + int(2 * math.pi * r / (2 * rho[i] + g)) + 1)   # the dot one turn further out
        pitch = rho[i] + rho[j] + g + 0.6
        th += ds / r
        r += pitch * ds / (2 * math.pi * r)
    xs = [p[0] for p in pos]; ys = [p[1] for p in pos]
    # rotate so the last dot ends lower right, then centre on the left two-thirds
    a0 = math.atan2(ys[-1], xs[-1]); rot = math.radians(38) - a0
    pos = [(x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)) for x, y in pos]
    xs = [p[0] for p in pos]; ys = [p[1] for p in pos]
    cx = 142 - (max(xs) + min(xs)) / 2; cy = 150 - (max(ys) + min(ys)) / 2
    for i, (x, y) in enumerate(pos):
        c = K if i == N - 1 else Wh
        d.ellipse([(cx + x - rho[i]) * S, (cy + y - rho[i]) * S, (cx + x + rho[i]) * S, (cy + y + rho[i]) * S], fill=c)
    img = down(big)
    d = pen(img)
    X0 = 284
    d.text((X0, 22), "BOLÉRO", font=font(INTER, 24), fill=Wh)
    for k, line in enumerate(["Paris Opéra", "22 Nov 1928"]):
        d.text((X0, 56 + 13 * k), line, font=font(MONOB, 11), fill=Wh)
    # the two-bar snare figure: tall ticks are quavers, short ones the triplets
    on = [0, 3, 4, 5, 6, 9, 10, 11, 12, 15, 18, 21, 22, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    y0 = 236
    for t in on:
        x = X0 + t * 3
        if t in (0, 6, 12, 15, 18, 24):
            d.rectangle([x, y0 - 13, x + 1, y0], fill=Wh)
        else:
            d.rectangle([x, y0 - 6, x, y0], fill=Wh)
    d.line([X0, y0 + 3, X0 + 107, y0 + 3], fill=Wh)
    d.line([X0 + 53, y0 + 3, X0 + 53, y0 + 7], fill=Wh)
    for k, line in enumerate(["one snare-drum", "figure, 24 taps,", "169 times over,", "ever louder"]):
        d.text((X0, 248 + 11 * k - 4), line, font=font(MONO, 10), fill=Wh)
    save(img, 2)


# ---------------------------------------------------------------- 3. Starlight bent
def bent_light():
    rng = np.random.default_rng(1919)
    cx, cy, R0 = 200, 128, 44
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    dx, dy = xx - cx, yy - cy
    r = np.hypot(dx, dy); th = np.arctan2(dy, dx)
    # corona: scale length varies with angle (streamers), fine radial striation on top
    s = 9 + 13 * np.abs(np.sin(1.5 * (th - 0.5))) ** 3 + 9 * np.abs(np.sin(2.5 * th + 1.1)) ** 6 \
        + 3 * np.sin(7 * th + 2)
    I = np.exp(-(r - R0) / np.maximum(s, 4))
    stri = 0.72 + 0.28 * np.sin(th * 46 + 3 * np.sin(th * 5) + r / 30)
    I = np.clip(I * stri, 0, 1)
    I[r < R0] = 0
    ink = rng.random((H, W)) < I ** 1.15
    ink |= (r >= R0) & (r < R0 + 1.6)
    a = np.zeros((H, W, 3), np.uint8)
    a[ink] = Wh
    # the great prominence of 1919 on the limb, and a small one
    for pa, hgt, wid in [(math.radians(-158), 9, 0.20), (math.radians(40), 3.5, 0.09)]:
        dth = np.angle(np.exp(1j * (th - pa)))
        prom = (r >= R0 - 0.5) & (r < R0 + hgt * np.clip(1 - (dth / wid) ** 2, 0, 1) + 0.5) & (np.abs(dth) < wid)
        hollow = (r < R0 + (hgt - 3.2) * np.clip(1 - (dth / (wid * 0.62)) ** 2, 0, 1)) & (r > R0 + 1.5)
        a[prom & ~hollow] = R
    a[H - 44:] = K
    img = Image.fromarray(a)
    d = pen(img)
    # stars: hollow ring = where the star really is, red stroke = the shift, white point = where it is seen
    stars = [(-62, 78), (-20, 104), (18, 128), (74, 92), (100, 112), (151, 84), (-112, 122), (-143, 168),
             (-170, 96), (171, 176)]
    for ang, rr in stars:
        t = math.radians(ang)
        x0, y0 = cx + rr * math.cos(t), cy + rr * math.sin(t)
        sh = 1150 / rr
        x1, y1 = cx + (rr + sh) * math.cos(t), cy + (rr + sh) * math.sin(t)
        ImageDraw.Draw(img).ellipse([min(x0, x1) - 6, min(y0, y1) - 6, max(x0, x1) + 6, max(y0, y1) + 6], fill=K)
    for ang, rr in stars:
        t = math.radians(ang)
        x0, y0 = cx + rr * math.cos(t), cy + rr * math.sin(t)
        sh = 1150 / rr
        x1, y1 = cx + (rr + sh) * math.cos(t), cy + (rr + sh) * math.sin(t)
        d.line([x0, y0, x1, y1], fill=R, width=2)
        d.ellipse([x0 - 2.5, y0 - 2.5, x0 + 2.5, y0 + 2.5], outline=Wh, fill=K)
        d.ellipse([x1 - 2, y1 - 2, x1 + 2, y1 + 2], fill=Wh)
        d.line([x1 - 4, y1, x1 + 4, y1], fill=Wh)
        d.line([x1, y1 - 4, x1, y1 + 4], fill=Wh)
    d.text((W // 2, H - 35), "ARTHUR EDDINGTON  d. 22 NOV 1944", font=font(MONOB, 10), fill=Wh, anchor="mm")
    d.text((W // 2, H - 22), "Eclipse of 29 May 1919: starlight bends past the Sun,", font=font(MONO, 10), fill=Wh, anchor="mm")
    d.text((W // 2, H - 10), "1.75 arcsec at the limb. Shifts drawn far too large.", font=font(MONO, 10), fill=Wh, anchor="mm")
    save(img, 3)


# ---------------------------------------------------------------- 4. Two doors
def two_doors():
    rng = np.random.default_rng(1963)
    f, hy, cx, hcam = 420.0, 140.0, 215.0, 1.5
    ZW, HALF, CEIL = 7.0, 2.5, 3.0
    DX0, DX1, DH = -0.117, 0.783, 2.1          # door opening in the back wall (metres)
    LX, LZ = 0.30, 11.5                        # the lamp outside
    n = S
    yy, xx = np.mgrid[0:H * n, 0:W * n].astype(float)
    xx = (xx + 0.5) / n; yy = (yy + 0.5) / n
    a = np.zeros((H * n, W * n), np.uint8)     # 0 black 1 white 2 red 3 grey(50 %)
    # floor
    with np.errstate(divide="ignore", invalid="ignore"):
        Z = f * hcam / (yy - hy)
    X = (xx - cx) * Z / f
    floor = (yy > hy) & (Z < ZW) & (Z > 0)
    xw = LX + (X - LX) * (LZ - ZW) / (LZ - Z)            # where the ray to the lamp crosses the wall
    lit = floor & (xw > DX0) & (xw < DX1)
    pen_ = floor & (xw > DX0 - 0.16) & (xw < DX1 + 0.16) & ~lit
    tile = ((np.floor(X / 0.5) + np.floor(Z / 0.5)) % 2 == 0)
    a[lit & tile] = 1
    a[pen_ & tile] = 3
    a[floor & (np.abs(X) > HALF)] = 0
    img3 = np.zeros((H * n, W * n, 3), np.uint8)
    img3[a == 1] = Wh
    big = Image.fromarray(img3)
    d = ImageDraw.Draw(big)

    def pr(Xm, Ym, Zm):          # Ym = height above floor
        return ((cx + Xm * f / Zm) * n, (hy - (Ym - hcam) * f / Zm) * n)
    # doorway: the outside
    x0, yb = pr(DX0, 0, ZW); x1, yt = pr(DX1, DH, ZW)
    x0, x1, yt, yb = int(x0), int(x1), int(yt), int(yb)
    out = np.zeros((yb - yt, x1 - x0, 3), np.uint8)
    oh, ow = out.shape[:2]
    oy, ox = np.mgrid[0:oh, 0:ow].astype(float)
    hor = hy * n - yt
    out[:] = Wh
    big.paste(Image.fromarray(out), (x0, yt))
    # firs against the snow-sky, the lamp-post, footprints
    sky = Image.new("L", (ow, oh), 0)
    sd = ImageDraw.Draw(sky)

    def fir(px, base, hgt):
        for k in range(5):
            w = hgt * (0.10 + 0.085 * k); top = base - hgt + k * hgt * 0.17
            sd.polygon([(px, top), (px - w, top + hgt * 0.30), (px + w, top + hgt * 0.30)], fill=255)
        sd.rectangle([px - 2, base - hgt * 0.12, px + 2, base], fill=255)
    for px, base, hgt in [(14, hor + 8, 96), (142, hor + 6, 84), (160, hor + 16, 118)]:
        fir(px, base, hgt)
    big.paste(K, (x0, yt), sky)
    lampx, lampy = cx + LX * f / LZ, hy - (2.05 - hcam) * f / LZ
    d = ImageDraw.Draw(big)
    for k in range(60):                              # a far wood along the horizon
        px = x0 + k * ow / 59; hh = 6 + 9 * abs(math.sin(k * 1.7)) + 5 * abs(math.sin(k * 0.61))
        d.polygon([(px - 5, hor + yt + 1), (px + 5, hor + yt + 1), (px, hor + yt - hh)], fill=K)
    fl = rng.random((60, 2))
    for u, v in fl:                                  # snow in the air
        px, py = x0 + u * ow, yt + v * hor * 0.95
        d.rectangle([px, py, px + 2, py + 2], fill=K)
    d.ellipse([lampx * n - 30, lampy * n - 36, lampx * n + 30, lampy * n + 24], fill=Wh)
    bx, by = pr(LX, 0, LZ)
    d.rectangle([lampx * n - 2, lampy * n, lampx * n + 2, by], fill=K)
    d.rectangle([lampx * n - 6, by - 4, lampx * n + 6, by], fill=K)
    d.line([lampx * n - 9, lampy * n + 16, lampx * n + 9, lampy * n + 16], fill=K, width=3)
    d.polygon([(lampx * n - 8, lampy * n - 14), (lampx * n + 8, lampy * n - 14), (lampx * n + 5, lampy * n + 2),
               (lampx * n - 5, lampy * n + 2)], fill=R)
    d.polygon([(lampx * n - 11, lampy * n - 14), (lampx * n + 11, lampy * n - 14), (lampx * n, lampy * n - 24)], fill=K)
    for k in range(9):                               # footprints out to the lamp
        Zk = ZW + 0.35 + k * 0.42
        Xk = 0.42 + (LX + 0.25 - 0.42) * k / 8 + (0.09 if k % 2 else -0.09)
        px, py = pr(Xk, 0, Zk)
        w = 34 / Zk
        d.ellipse([px - w, py - w * 0.45, px + w, py + w * 0.45], fill=K)
    # door frame and the leaf standing open into the room
    d.rectangle([x0 - 4, yt - 4, x1 + 4, yb], outline=Wh, width=4)
    ang = math.radians(68)
    XF, ZF = DX1 + 0.9 * math.cos(ang), ZW - 0.9 * math.sin(ang)
    leaf = [pr(DX1, DH, ZW), pr(XF, DH, ZF), pr(XF, 0, ZF), pr(DX1, 0, ZW)]
    d.polygon(leaf, fill=K, outline=Wh)
    lm = Image.new("L", (W * n, H * n), 0)
    ImageDraw.Draw(lm).polygon(leaf, fill=255)
    lm = np.asarray(lm.resize((W, H), Image.LANCZOS)) > 150
    d.line([leaf[1], leaf[2]], fill=Wh, width=4)
    for lo, hi in [(0.25, 0.95), (1.1, 1.95)]:       # two panels
        q = [pr(DX1 + 0.14 * math.cos(ang), hi, ZW - 0.14 * math.sin(ang)),
             pr(DX1 + 0.76 * math.cos(ang), hi, ZW - 0.76 * math.sin(ang)),
             pr(DX1 + 0.76 * math.cos(ang), lo, ZW - 0.76 * math.sin(ang)),
             pr(DX1 + 0.14 * math.cos(ang), lo, ZW - 0.14 * math.sin(ang))]
        d.line(q + [q[0]], fill=Wh, width=2)
    hx, hyk = pr(DX1 + 0.80 * math.cos(ang), 1.0, ZW - 0.80 * math.sin(ang))
    d.ellipse([hx - 4, hyk - 4, hx + 4, hyk + 4], fill=R)
    img = down(big)
    out = np.array(img)
    small = a.reshape(H, n, W, n).astype(float)
    grey = ((small == 3).mean((1, 3)) > 0.5)
    Y, Xp = np.mgrid[0:H, 0:W]
    out[(grey | lm) & ((Xp + Y) % 2 == 0) & (out.sum(-1) == 0)] = Wh
    # room edges, dotted
    img = Image.fromarray(out)
    d = pen(img)

    def dotted(p, q, step=3):
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        for k in range(0, int(L), step):
            x = p[0] + (q[0] - p[0]) * k / L; y = p[1] + (q[1] - p[1]) * k / L
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((int(x), int(y)), Wh)

    def p1(Xm, Ym, Zm):
        x, y = pr(Xm, Ym, Zm)
        return (x / n, y / n)
    for sx in (-1, 1):
        dotted(p1(sx * HALF, 0, ZW), p1(sx * HALF, CEIL, ZW))
        dotted(p1(sx * HALF, 0, ZW), p1(sx * HALF, 0, 1.2))
        dotted(p1(sx * HALF, CEIL, ZW), p1(sx * HALF, CEIL, 1.2))
    dotted(p1(-HALF, CEIL, ZW), p1(HALF, CEIL, ZW))
    d.text((12, 262), "C. S. LEWIS", font=font(MONOB, 10), fill=Wh)
    d.text((12, 273), "ALDOUS HUXLEY", font=font(MONOB, 10), fill=Wh)
    d.text((12, 284), "d. 22 Nov 1963", font=font(MONO, 10), fill=Wh)
    save(img, 4)


# ---------------------------------------------------------------- 5. Cutty Sark
def cutty_sark():
    big = Image.new("RGB", (W * S, H * S), Wh)
    d = ImageDraw.Draw(big)
    WL = 236
    DECK = 208

    def sail(x, yt, yb, wt, wb, lean=3.0):
        """square sail seen broadside: head on the upper yard, foot arched (roach), belly forward"""
        n = 14
        L = [(x - wt + lean * 0.3, yt)] + [(x - wt + (wt - wb) * t - 0 * t + lean * math.sin(math.pi * t) * -0.6, yt + (yb - yt) * t)
                                           for t in np.linspace(0, 1, n)][1:]
        Rr = [(x + wt + (wb - wt) * t + lean * math.sin(math.pi * t), yt + (yb - yt) * t) for t in np.linspace(0, 1, n)]
        foot = [(x + wb - 2 * wb * t, yb - (yb - yt) * 0.13 * math.sin(math.pi * t)) for t in np.linspace(0, 1, n)]
        d.polygon(s3(Rr + foot + L[::-1]), fill=K)
        d.line(s3([(x - wt - 3, yt - 1), (x + wt + 3, yt - 1)]), fill=K, width=5)   # the yard

    masts = [  # x, levels (yard heights, last is the foot of the course), half-widths
        (263, [36, 54, 77, 103, 130, 190], [13, 18, 24, 28, 32, 31]),
        (192, [20, 36, 55, 80, 107, 134, 192], [10, 14, 19, 26, 30, 34, 33]),
        (121, [52, 68, 88, 111, 135, 186], [11, 15, 20, 24, 27, 25]),
    ]
    # hull
    hull = [(64, 200), (70, 204), (120, 209), (220, 210), (296, 206), (322, 199), (333, 196), (318, 214),
            (310, WL + 8), (84, WL + 8), (74, WL - 6)]
    d.polygon(s3(hull), fill=K)
    d.line(s3([(70, 208), (120, 213), (220, 214), (296, 210), (318, 204)]), fill=Wh, width=2)
    d.line(s3([(318, 201), (392, 178)]), fill=K, width=5)            # bowsprit and jib-boom
    d.line(s3([(344, 193), (322, 226)]), fill=K, width=2)            # martingale-ish stays
    d.line(s3([(344, 193), (348, 210), (322, 220)]), fill=K, width=2)
    d.line(s3([(348, 210), (390, 179)]), fill=K, width=2)
    for x, lv, hw in masts:
        d.line(s3([(x, lv[0] - 9), (x, DECK)]), fill=K, width=5)
        for dxs in (-1, 1):                                          # shrouds
            d.line(s3([(x, lv[-3]), (x + dxs * 13, DECK - 2)]), fill=K, width=2)
            d.line(s3([(x, lv[-3]), (x + dxs * 7, DECK - 2)]), fill=K, width=2)
        for k in range(len(lv) - 1):
            sail(x, lv[k] + 2, lv[k + 1] - 3, hw[k], hw[k + 1])
    # stays between the masts and down to the bowsprit; backstay
    d.line(s3([(192, 14), (263, 60)]), fill=K, width=2)
    d.line(s3([(121, 46), (192, 84)]), fill=K, width=2)
    stays = [((263, 30), (391, 179)), ((263, 62), (366, 187)), ((263, 96), (340, 195))]
    for p, q in stays:
        d.line(s3([p, q]), fill=K, width=2)
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
        at = lambda t: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
        head, tack, c = at(0.30), at(0.96), at(0.72)
        clew = (c[0] - uy * 17, c[1] + ux * 17)
        belly = ((head[0] + clew[0]) / 2 - 2, (head[1] + clew[1]) / 2 + 3)
        d.polygon(s3([head, tack, clew, belly]), fill=K)
    # spanker on gaff and boom
    d.polygon(s3([(117, 146), (80, 126), (58, 194), (117, 190)]), fill=K)
    d.line(s3([(121, 147), (76, 123)]), fill=K, width=4)
    d.line(s3([(121, 192), (52, 196)]), fill=K, width=4)
    # red: the house flag at the main truck, streaming aft, and the copper below the waterline
    fl = [(192 - t * 52, 11 + 3.2 * math.sin(t * 7.5) * t) for t in np.linspace(0, 1, 30)]
    d.polygon(s3([(192, 8)] + [(x, y + 2 + 4 * (1 - t)) for (x, y), t in zip(fl, np.linspace(0, 1, 30))][::-1][::-1]
                 + [(x, y - 2 - 3 * (1 - t)) for (x, y), t in zip(fl, np.linspace(0, 1, 30))][::-1]), fill=R)
    d.rectangle([0, (WL - 5) * S, W * S, H * S], fill=Wh)
    d.polygon(s3([(75, WL - 5), (316, WL - 5), (313, WL + 1), (79, WL + 1)]), fill=R)
    # the sea: long swells drawn as lines, broken by a bow wave and a wake
    for k, y in enumerate(range(WL + 2, H + 6, 5)):
        amp = 1.0 + 0.28 * k; lam = 26 + 5 * k
        pts = [(x, y + amp * math.sin(x / lam * 2 * math.pi + k * 1.9) + 0.6 * amp * math.sin(x / (lam * 0.37) + k))
               for x in range(-4, 406, 2)]
        d.line(s3(pts), fill=K, width=3)
    d.polygon(s3([(300, WL + 1), (318, WL - 9), (326, WL - 10), (334, WL - 4), (346, WL + 3), (330, WL + 1), (320, WL - 3),
                  (312, WL + 3)]), fill=Wh, outline=K)
    img = down(big)
    d = pen(img)
    d.text((10, 10), "CUTTY", font=font(INTER, 19), fill=K)
    d.text((10, 30), "SARK", font=font(INTER, 19), fill=K)
    for k, line in enumerate(["launched at", "Dumbarton,", "22 Nov 1869", "", "32,000 sq", "ft of sail"]):
        d.text((11, 57 + 11 * k), line, font=font(MONO, 10), fill=K)
    save(img, 5)


if __name__ == "__main__":
    under_the_wires()
    bolero()
    bent_light()
    two_doors()
    cutty_sark()
    print("ok")
