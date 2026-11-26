#!/usr/bin/env python3
"""2026-11-26 (Thu, Thanksgiving) — theme: what was there.
Run from the repo root: python3 archive/2026-11-26/generate.py
Needs numpy + pillow. Writes images/1..5.png and archive/2026-11-26/1..5.png."""
import math, os, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
K, WH, R = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = "archive/2026-11-26"
F = "/usr/share/fonts/"
MONO = F + "truetype/dejavu/DejaVuSansMono.ttf"
MONOB = F + "truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANSB = F + "truetype/dejavu/DejaVuSans-Bold.ttf"
SERI = F + "truetype/liberation/LiberationSerif-Italic.ttf"
FSI = F + "truetype/freefont/FreeSerifItalic.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


def snap(img):
    """RGB image -> nearest of the three inks."""
    a = np.asarray(img.convert("RGB")).astype(int)
    pal = np.array([K, WH, R])
    d = ((a[:, :, None, :] - pal[None, None]) ** 2).sum(-1)
    return Image.fromarray(pal[d.argmin(-1)].astype(np.uint8), "RGB")


def down(img3):
    return snap(img3.resize((W, H), Image.LANCZOS))


def save(img, n):
    img = snap(img)
    p = Image.new("P", (1, 1))
    p.putpalette(list(K) + list(WH) + list(R) + [0] * 753)
    q = img.quantize(palette=p, dither=Image.NONE)
    q.save(f"{OUT}/{n}.png")
    os.makedirs("images", exist_ok=True)
    shutil.copy(f"{OUT}/{n}.png", f"images/{n}.png")


def crisp(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return d


# ---------------------------------------------------------------- 1. the hole
def p1():
    rng = np.random.default_rng(19221126)
    # ragged breach in the sealed doorway
    hole = Image.new("L", (W, H), 0)
    hd = ImageDraw.Draw(hole)
    pts = []
    N = 90
    ph = rng.random(6) * 6.28
    for i in range(N):
        t = 2 * math.pi * i / N
        r = 1 + 0.07 * math.sin(3 * t + ph[0]) + 0.05 * math.sin(5 * t + ph[1]) + 0.04 * math.sin(9 * t + ph[2])
        r += rng.normal(0, 0.022)
        pts.append((200 + 158 * r * math.cos(t), 138 + 108 * r * math.sin(t)))
    hd.polygon(pts, fill=255)
    hm = np.asarray(hole) > 0

    # things in the dark, drawn as a mask
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    # cow-headed couch
    d.rounded_rectangle((92, 142, 262, 152), 4, fill=255)
    for x in (104, 244):
        d.polygon([(x - 5, 152), (x + 5, 152), (x + 3, 196), (x + 9, 204), (x - 7, 204), (x - 3, 196)], fill=255)
    d.polygon([(92, 150), (104, 150), (100, 112), (88, 108)], fill=255)        # neck
    d.polygon([(78, 96), (104, 92), (106, 112), (80, 120), (68, 116), (68, 108)], fill=255)  # head
    d.arc((66, 52, 96, 100), 100, 250, fill=255, width=4)                      # horns
    d.arc((88, 52, 118, 100), 290, 80, fill=255, width=4)
    d.ellipse((81, 58, 103, 80), fill=255)                                     # sun disc
    d.arc((246, 96, 290, 150), 300, 90, fill=255, width=4)                     # tail
    # oval food boxes under the couch
    for (x, y) in ((128, 184), (166, 184), (204, 184), (147, 166), (185, 166)):
        d.ellipse((x - 20, y - 9, x + 20, y + 9), outline=255, width=3)
    # chariot wheels leaning on the right
    for (cx, cy, r) in ((318, 138, 44), (300, 160, 40)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=255, width=4)
        d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=255)
        for k in range(6):
            a = k * math.pi / 3 + 0.3
            d.line((cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)), fill=255, width=2)
    # lotus vase, left
    d.polygon([(52, 204), (72, 204), (68, 190), (74, 172), (66, 160), (70, 150), (54, 150), (58, 160), (50, 172), (56, 190)], fill=255)
    # a chair, right front
    d.polygon([(280, 214), (322, 214), (322, 208), (330, 170), (324, 170), (316, 204), (280, 204)], fill=255)
    d.line((284, 214, 284, 232), fill=255, width=4)
    d.line((318, 214, 318, 232), fill=255, width=4)

    ma = np.asarray(m).astype(float) / 255
    edge = ma - np.asarray(m.filter(ImageFilter.MinFilter(5))).astype(float) / 255
    edge = np.asarray(Image.fromarray((edge * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(float) / 255
    yy, xx = np.mgrid[0:H, 0:W]
    fx, fy = 200, 236
    dist = np.hypot(xx - fx, yy - fy)
    fall = np.exp(-dist / 150) + 0.12
    T = (1.5 * edge + 0.30 * ma) * fall + 0.012
    # lit rim of the broken plaster
    rim = (np.asarray(hole.filter(ImageFilter.MaxFilter(9))) > 0) & ~hm
    T = np.where(hm, T, 0)
    T = T + rim * 0.9 * np.exp(-dist / 70)
    ink = rng.random((H, W)) < np.clip(T, 0, 1) ** 1.1
    a = np.zeros((H, W, 3), np.uint8)
    a[ink] = WH
    img = Image.fromarray(a, "RGB")

    # the candle (3x layer)
    L = Image.new("RGB", (W * 3, H * 3), K)
    ld = ImageDraw.Draw(L)
    s = 3
    ld.polygon([(193 * s, 262 * s), (207 * s, 262 * s), (207 * s, 300 * s), (193 * s, 300 * s)], fill=WH)
    fl = []
    for i in range(41):
        t = i / 40
        w = 8.5 * math.sin(math.pi * t) ** 0.8 * (1 - 0.55 * t)
        fl.append((200 - w + 1.5 * t, 258 - 34 * t))
    fl += [(200 + 8.5 * math.sin(math.pi * t) ** 0.8 * (1 - 0.55 * t) + 1.5 * t, 258 - 34 * t) for t in [i / 40 for i in range(40, -1, -1)]]
    ld.polygon([(x * s, y * s) for x, y in fl], fill=R)
    ld.ellipse((197 * s, 244 * s, 203 * s, 257 * s), fill=WH)
    ld.line((200 * s, 262 * s, 200 * s, 256 * s), fill=K, width=3)
    cm = np.asarray(down(L))
    a = np.asarray(img).copy()
    sel = cm.sum(-1) > 0
    # black moat round flame
    moat = np.asarray(Image.fromarray((sel * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
    a[moat] = K
    a[sel] = cm[sel]
    img = Image.fromarray(a, "RGB")
    d = crisp(img)
    d.text((8, 289), "VALLEY OF THE KINGS", font=font(MONO, 10), fill=WH, anchor="lm")
    d.text((W - 8, 289), "26 NOV 1922", font=font(MONO, 10), fill=WH, anchor="rm")
    save(img, 1)


# ---------------------------------------------------------------- 2. the tale
TALE = ["We lived beneath the mat,", "Warm and snug and fat,", "But one woe, and that", "Was the cat!",
        "To our joys a clog,", "In our eyes a fog,", "On our hearts a log", "Was the dog!",
        "When the cat's away,", "Then the mice will play,", "But, alas! one day;", "(So they say)",
        "Came the dog and cat,", "Hunting for a rat,", "Crushed the mice all flat,", "Each one as he sat,",
        "Underneath the mat,", "Warm and snug and fat.", "Think of that!"]


def p2():
    img = Image.new("RGB", (W, H), R)
    d = crisp(img)
    n = len(TALE)
    y = 47
    prev = None
    for i, line in enumerate(TALE):
        t = i / (n - 1)
        s = int(round(14 - 5.4 * t))
        A = 96 * (1 - t) ** 1.25 + 6
        cx = 205 + A * math.sin(0.35 + t * 3.3 * math.pi)
        f = font(SANSB, s)
        d.text((cx, y), line, font=f, fill=WH, anchor="mt")
        y += s + 1
    # tail tip flourish
    pts = [(cx + 2 + 9 * math.sin(k / 3.0) * (1 - k / 14), y + k) for k in range(14)]
    d.line(pts, fill=WH, width=1)
    # the mouse (3x mask), nose to the left, tail end towards the first line
    L = Image.new("L", (W * 3, H * 3), 0)
    ld = ImageDraw.Draw(L)

    def E(x0, y0, x1, y1, fill=255):
        ld.ellipse((x0 * 3, y0 * 3, x1 * 3, y1 * 3), fill=fill)
    E(150, 14, 214, 46)                         # body
    ld.polygon([(p * 3, q * 3) for p, q in ((118, 37), (160, 18), (166, 44))], fill=255)  # snout
    E(152, 4, 172, 24)                          # ear
    E(164, 7, 180, 24)
    E(156, 8, 168, 20, 0)
    E(156.5, 8.5, 167.5, 19.5, 90)
    E(146, 26, 151, 31, 0)                      # eye
    E(116, 34, 122, 40)                         # nose
    for x in (166, 196):
        E(x, 41, x + 14, 48)
    ld.line([(p * 3, q * 3) for p, q in ((212, 32), (232, 34), (246, 44), (240, 50))], fill=255, width=7, joint="curve")
    Lm = np.asarray(L.resize((W, H), Image.LANCZOS))
    a = np.asarray(img).copy()
    a[Lm > 128] = K
    img = Image.fromarray(a, "RGB")
    d = crisp(img)
    d.ellipse((146, 26, 150, 30), fill=WH)
    for dy in (-5, 0, 5):                        # whiskers
        d.line((126, 37, 108, 37 + dy), fill=K, width=1)
    f = font(MONO, 10)
    for k, s in enumerate(("ALICE'S ADVENTURES", "UNDER GROUND", "given 26 Nov 1864")):
        d.text((8, 262 + k * 11), s, font=f, fill=WH)
    save(img, 2)


# ---------------------------------------------------------------- 3. the morning after
def p3():
    rng = np.random.default_rng(1703)
    img = Image.new("RGB", (W, H), WH)
    d = crisp(img)
    hz = 205
    for x in range(0, W, 4):
        d.point((x, hz), fill=K)
    # reef
    reef = [(168, hz + 1), (176, hz - 3), (188, hz - 5), (197, hz - 9), (206, hz - 10), (222, hz - 9), (233, hz - 6),
            (241, hz - 7), (250, hz - 3), (262, hz + 1)]
    d.polygon(reef, fill=K)
    d.polygon([(280, hz + 1), (287, hz - 3), (296, hz + 1)], fill=K)
    d.polygon([(140, hz + 1), (146, hz - 2), (153, hz + 1)], fill=K)
    # bent iron stanchions, all that stayed
    for (x, y, dx, hh) in ((199, hz - 9, 3, 9), (212, hz - 10, -2, 12), (224, hz - 9, 5, 7)):
        d.line((x, y, x + dx, y - hh), fill=K, width=1)
    # a little water
    for _ in range(13):
        x = rng.integers(20, 380); y = rng.integers(hz + 8, hz + 46)
        ln = rng.integers(5, 16) * (1 + (y - hz) / 40)
        d.line((x, y, x + ln, y), fill=K, width=1)
    # where the tower was: dotted red outline of Winstanley's light
    cx, base = 211, hz - 10

    def dots(pts, step=4.0):
        acc = 0.0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            n = int(L // 0.5) + 1
            for k in range(n):
                acc += 0.5
                if acc >= step:
                    acc = 0
                    t = k / max(n - 1, 1)
                    x = int(round(x0 + (x1 - x0) * t)); y = int(round(y0 + (y1 - y0) * t))
                    d.rectangle((x, y, x + 1, y + 1), fill=R)

    def sym(half):  # half: list of (halfwidth, height above base), bottom to top
        left = [(cx - w, base - h) for w, h in half]
        right = [(cx + w, base - h) for w, h in half]
        dots(left); dots(right)
    sym([(13, 0), (11, 40), (16, 44), (16, 50), (11, 50), (10, 62), (15, 65), (15, 70), (9, 70), (9, 86), (11, 88), (6, 98), (2, 102), (0.5, 103), (0.5, 128)])
    for h, w in ((44, 16), (50, 16), (65, 15), (70, 15), (88, 11)):
        dots([(cx - w, base - h), (cx + w, base - h)])
    # weather vane, crane arm and flag
    dots([(cx - 9, base - 120), (cx + 10, base - 120)]); dots([(cx + 10, base - 124), (cx + 10, base - 116)])
    dots([(cx + 15, base - 66), (cx + 34, base - 80), (cx + 34, base - 62)])
    dots([(cx - 15, base - 68), (cx - 26, base - 96)]); dots([(cx - 26, base - 96), (cx - 40, base - 92), (cx - 27, base - 87)])
    f = font(SERI, 13)
    d.text((14, 255), "Eddystone, the morning after.", font=f, fill=K)
    d.text((14, 283), "GREAT STORM, 26–27 NOV 1703 (OLD STYLE)", font=font(MONO, 10), fill=K, anchor="lm")
    save(img, 3)


# ---------------------------------------------------------------- 4. the sign
def p4():
    s = 3
    L = Image.new("RGB", (W * s, H * s), WH)
    d = ImageDraw.Draw(L)
    cx, cy, rx, ry = 200, 134, 128, 116
    d.ellipse(((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s), outline=K, width=9)
    d.line(((cx - rx) * s, cy * s, (cx + rx) * s, cy * s), fill=K, width=9)
    # the concept: a tree, in red
    rng = np.random.default_rng(1857)
    tb = cy - 12
    d.polygon([(p * s, q * s) for p, q in ((194, tb), (196, tb - 34), (186, tb - 52), (191, tb - 54), (199, tb - 40),
                                           (204, tb - 58), (209, tb - 56), (204, tb - 34), (207, tb))], fill=R)
    for _ in range(46):
        a = rng.random() * 6.283; r = rng.random() ** 0.6
        x = 199 + 43 * r * math.cos(a); y = tb - 62 + 27 * r * math.sin(a)
        q = rng.uniform(7, 13)
        d.ellipse(((x - q) * s, (y - q) * s, (x + q) * s, (y + q) * s), fill=R)
    d.line((150 * s, tb * s, 250 * s, tb * s), fill=R, width=6)
    # arrows of signification

    def arrow(x, y0, y1):
        d.line((x * s, y0 * s, x * s, y1 * s), fill=K, width=9)
        sg = 1 if y1 > y0 else -1
        d.polygon([((x - 9) * s, (y1 - sg * 4) * s), ((x + 9) * s, (y1 - sg * 4) * s), (x * s, (y1 + sg * 14) * s)], fill=K)
    arrow(40, 190, 78)
    arrow(360, 78, 190)
    img = down(L)
    d = crisp(img)
    d.text((cx, cy + 52), "arbor", font=font(FSI, 78), fill=K, anchor="ms")
    d.text((cx, 276), "F. DE SAUSSURE, BORN GENEVA 26 NOV 1857", font=font(MONO, 10), fill=K, anchor="mm")
    save(img, 4)


# ---------------------------------------------------------------- 5. the feather
def p5():
    rng = np.random.default_rng(20261126)
    s = 3
    L = Image.new("RGB", (W * s, H * s), K)
    d = ImageDraw.Draw(L)
    P0, P1, P2 = np.array([28., 262.]), np.array([190., 196.]), np.array([372., 52.])

    def B(t):
        return (1 - t) ** 2 * P0 + 2 * (1 - t) * t * P1 + t * t * P2

    def Tn(t):
        v = 2 * (1 - t) * (P1 - P0) + 2 * t * (P2 - P1)
        return v / np.hypot(*v)
    NB = 205
    t0 = 0.17
    split = set(rng.choice(NB, 9, replace=False).tolist())
    for side, wmax in ((1, 50), (-1, 28)):
        skew = 0.0
        for i in range(NB):
            u = i / (NB - 1)
            t = t0 + (0.95 - t0) * u
            p = B(t); tg = Tn(t); nm = np.array([-tg[1], tg[0]]) * side
            # vane width profile: quick swell, long body, rounded tip
            prof = min(1, (u / 0.10) ** 0.6) * (1 - max(0, (u - 0.72) / 0.28) ** 2.0) ** 0.5
            wv = wmax * prof * (1 + 0.05 * math.sin(u * 23))
            if i in split:
                skew = rng.uniform(-0.25, 0.25)
            ang = 0.95 + skew * 0.4           # barb leans towards the tip
            skew *= 0.93
            n = 26
            pts = []
            for k in range(n + 1):
                q = k / n
                along = wv * q * math.tan(ang) * (0.55 + 0.35 * q)
                pos = p + nm * wv * q + tg * along
                pts.append(pos)
            # bars run across the feather: decide per segment from position along the axis
            for k in range(n):
                a_, b_ = pts[k], pts[k + 1]
                ax = (a_ - P0) @ ((P2 - P0) / np.hypot(*(P2 - P0)))
                band = math.sin(ax / 15.5 * math.pi + 0.5 * math.sin(k / n * 3))
                white = band > -0.15 or u > 0.93
                if white or (i % 3 == 0 and k % 2 == 0):
                    d.line((a_[0] * s, a_[1] * s, b_[0] * s, b_[1] * s), fill=WH, width=3 if white else 2)
    # down at the base
    for _ in range(70):
        t = rng.uniform(0.09, 0.19)
        p = B(t); tg = Tn(t); side = rng.choice([-1, 1]); nm = np.array([-tg[1], tg[0]]) * side
        ln = rng.uniform(10, 26); cur = rng.uniform(-0.6, 0.6)
        pts = []
        for k in range(10):
            q = k / 9
            pos = p + nm * ln * q + tg * (ln * 0.5 * q + cur * ln * q * q)
            pts.append((pos[0] * s, pos[1] * s))
        d.line(pts, fill=WH, width=2)
    # the shaft, red
    sh = [tuple(B(t) * s) for t in np.linspace(0, 0.955, 120)]
    for k in range(len(sh) - 1):
        wd = int(round(11 - 8 * k / len(sh)))
        d.line((sh[k], sh[k + 1]), fill=R, width=wd)
    img = down(L.point(lambda v: min(255, int(v * 1.5))))
    save(img, 5)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    p1(); p2(); p3(); p4(); p5()
    sheet = Image.new("RGB", (W * 2 + 30, H * 3 + 40), (120, 120, 120))
    for i in range(5):
        sheet.paste(Image.open(f"{OUT}/{i+1}.png").convert("RGB"), (10 + (i % 2) * (W + 10), 10 + (i // 2) * (H + 10)))
    sd = os.environ.get("SHEET")
    if sd:
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(sd)
