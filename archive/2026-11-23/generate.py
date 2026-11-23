#!/usr/bin/env python3
"""2026-11-23 (Mon). Theme: counted.
Run from the repo root:  python3 archive/2026-11-23/generate.py
Writes images/1..5.png and archive/2026-11-23/1..5.png (400x300, black/white/red)."""
import math, os, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
K, Wh, R = (0, 0, 0), (255, 255, 255), (255, 0, 0)
INKS = np.array([K, Wh, R], dtype=np.int32)
OUT = "archive/2026-11-23"
F = "/usr/share/fonts/truetype/dejavu/"
MONO = F + "DejaVuSansMono.ttf"
MONOB = F + "DejaVuSansMono-Bold.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FSB = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


def snap(img):
    a = np.asarray(img.convert("RGB"), dtype=np.int32)
    d = ((a[:, :, None, :] - INKS[None, None]) ** 2).sum(-1)
    return Image.fromarray(INKS[d.argmin(-1)].astype(np.uint8), "RGB")


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


def vnoise(rng, shape, cell):
    h, w = shape
    g = rng.random((h // cell + 3, w // cell + 3)).astype(np.float32)
    im = Image.fromarray((g * 255).astype(np.uint8)).resize(((w // cell + 3) * cell, (h // cell + 3) * cell),
                                                             Image.BICUBIC)
    return np.asarray(im, dtype=np.float32)[:h, :w] / 255


# ---------------------------------------------------------------- 1. One breath
def one_breath():
    """Jacques Mayol, off Elba, 23 Nov 1976: the first breath-hold dive to 100 m. 2.5 px per metre."""
    rng = np.random.default_rng(1976)
    SURF, PXM, LX = 22, 2.5, 268
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    depth = (yy - SURF) / PXM                                   # metres
    dark = np.clip(depth / 62, 0, 1) ** 0.75
    # shafts of light fanning down from the surface, dying by ~45 m
    ang = np.arctan2(xx - 150, yy - SURF + 160)
    shaft = 0.5 + 0.5 * np.sin(ang * 46 + 2 * np.sin(ang * 9))
    shaft = shaft ** 2 * np.clip(1 - depth / 52, 0, 1)
    dark = np.clip(dark - 0.7 * shaft, 0, 1)
    dark = np.where(depth > 70, 1, dark)
    ink = rng.random((H, W)) < dark ** 1.1
    a = np.full((H, W, 3), 255, np.uint8)
    a[ink & (yy >= SURF)] = K
    # the surface: a slack black line with a little chop
    for x in range(W):
        y = SURF + int(round(1.4 * math.sin(x / 13) + 0.8 * math.sin(x / 5.1 + 1)))
        a[y:y + 2, x] = K
    img = Image.fromarray(a)
    d = pen(img)
    # float and the shot line, 100 m of it
    d.polygon([(LX - 9, SURF - 1), (LX + 9, SURF - 1), (LX + 6, SURF - 7), (LX - 6, SURF - 7)], fill=K)
    d.line([(LX, SURF - 7), (LX, SURF - 15)], fill=K)
    d.polygon([(LX, SURF - 15), (LX + 7, SURF - 12), (LX, SURF - 10)], fill=R)
    bot = SURF + int(100 * PXM)
    a = np.array(img)
    for y in range(SURF, bot + 1):
        m = (y - SURF) / PXM
        if m < 26:
            a[y, LX - 1:LX + 2] = Wh
            a[y, LX] = K
        else:
            a[y, LX] = Wh
            a[y, LX - 1] = K
            a[y, LX + 1] = K
    for m in range(10, 101, 10):                                # ten-metre marks
        y = SURF + int(m * PXM)
        L = 9 if m % 50 == 0 else 5
        c = K if m < 26 else Wh
        if m < 26:
            a[y - 1:y + 2, LX + 3:LX + 5 + L] = Wh
        else:
            a[y - 1:y + 2, LX + 3:LX + 5 + L] = K
        a[y, LX + 4:LX + 4 + L] = c
    img = Image.fromarray(a)
    d = pen(img)
    d.ellipse([LX - 7, bot, LX + 7, bot + 4], fill=Wh)           # the plate at the bottom of the line
    # the diver, head down, one hand on the line: drawn at 4x and thresholded
    S = 4
    P = Image.new("L", (30 * S, 34 * S), 0)
    p = ImageDraw.Draw(P)

    def T(pts):
        return [((15 + x) * S, (4 + y) * S) for x, y in pts]
    p.polygon(T([(-2.2, 8), (2.2, 8), (2.8, 15), (1.6, 20), (-1.6, 20), (-2.8, 15)]), fill=255)   # trunk
    p.ellipse([(15 - 2.3) * S, (4 + 19.5) * S, (15 + 2.3) * S, (4 + 24.2) * S], fill=255)         # head
    p.line(T([(1.5, 18), (4.5, 23), (6.5, 27.5)]), fill=255, width=int(1.5 * S))                  # arm to the line
    p.line(T([(-1.5, 18), (-3, 13)]), fill=255, width=int(1.4 * S))
    p.line(T([(-1, 8), (-1.6, 2), (-1.2, -2)]), fill=255, width=int(1.7 * S))                     # legs
    p.line(T([(1, 8), (1.8, 2.5), (2.6, -1.5)]), fill=255, width=int(1.7 * S))
    p.polygon(T([(-2.4, -1.5), (0, -1.5), (-0.2, -4), (-3.4, -4)]), fill=255)                     # fins
    p.polygon(T([(1.6, -1), (3.8, -1), (5, -3.6), (2, -3.6)]), fill=255)
    P = P.resize((45, 51), Image.LANCZOS).point(lambda v: 255 if v > 110 else 0)
    img.paste(R, (LX - 33, bot - 46), P)
    # quiet labels
    f = font(MONO, 10)
    d.rectangle([LX + 15, SURF + 50 * PXM - 6, LX + 30, SURF + 50 * PXM + 6], fill=K)
    d.text((LX + 17, SURF + 50 * PXM - 6), "50", font=f, fill=Wh)
    d.text((LX + 16, bot - 6), "100 m", font=f, fill=Wh)
    d.text((10, 268), "ONE BREATH, 3 min 40 s", font=font(MONOB, 10), fill=Wh)
    d.text((10, 281), "J. Mayol, off Elba, 23 Nov 1976", font=f, fill=Wh)
    save(img, 1)


# ---------------------------------------------------------------- 2. Nickel in the slot
def nickel():
    """A Liberty Head five-cent reverse at twice life size, as an embossed relief in one-bit dither."""
    S, RAD = 2, 100
    N = (2 * RAD + 8) * S
    c = N / 2
    M = Image.new("L", (N, N), 0)
    m = ImageDraw.Draw(M)

    def ring(r0, r1, v):
        m.ellipse([c - r1 * S, c - r1 * S, c + r1 * S, c + r1 * S], fill=v)
        m.ellipse([c - r0 * S, c - r0 * S, c + r0 * S, c + r0 * S], fill=0)
    ring(94, 100, 255)
    # the big roman V
    fv = font(FSB, 118 * S)
    bb = m.textbbox((0, 0), "V", font=fv)
    m.text((c - (bb[0] + bb[2]) / 2, c - (bb[1] + bb[3]) / 2 - 3 * S), "V", font=fv, fill=255)

    def stamp(tile, ang, x, y):
        t = tile.rotate(ang, resample=Image.BICUBIC, expand=True)
        M.paste(255, (int(c + x * S - t.width / 2), int(c + y * S - t.height / 2)), t)

    # wreath: two sprays of leaves, open at the top
    for side in (-1, 1):
        for i, a in enumerate(np.linspace(34, 166, 15)):
            for off, tilt, rr in ((6, 32, 13), (-6, -32, 12)):
                if (i % 2 == 0) == (off > 0):
                    continue
                th = math.radians(a) * side
                r = 61 + off
                leaf = Image.new("L", (40 * S, 40 * S), 0)
                ImageDraw.Draw(leaf).ellipse([(20 - 3.1) * S, (20 - rr / 2) * S, (20 + 3.1) * S, (20 + rr / 2) * S],
                                             fill=255)
                stamp(leaf, -math.degrees(th) + 90 + side * (90 - tilt) + (180 if side < 0 else 0),
                      r * math.sin(th), -r * math.cos(th))
        pts = [(c + 61 * S * math.sin(math.radians(a) * side), c - 61 * S * math.cos(math.radians(a) * side))
               for a in np.linspace(30, 174, 40)]
        m.line(pts, fill=255, width=int(1.6 * S))
    m.ellipse([c - 4 * S, c + 57 * S, c + 4 * S, c + 65 * S], fill=255)        # the tie

    def glyph(ch, fnt):
        t = Image.new("L", (30 * S, 30 * S), 0)
        ImageDraw.Draw(t).text((15 * S, 15 * S), ch, font=fnt, fill=255, anchor="mm")
        return t
    ft = font(SERIFB, 15 * S)
    top = "UNITED STATES OF AMERICA"
    for i, ch in enumerate(top):
        phi = -103 + 206 * i / (len(top) - 1)
        if ch != " ":
            th = math.radians(phi)
            stamp(glyph(ch, ft), -phi, 84 * math.sin(th), -84 * math.cos(th))
    for i, ch in enumerate("CENTS"):
        psi = -22 + 11 * i
        th = math.radians(psi)
        stamp(glyph(ch, ft), psi, 84 * math.sin(th), 84 * math.cos(th))
    for sgn in (-1, 1):                                                         # a dot either side of CENTS
        th = math.radians(sgn * 40)
        m.ellipse([c + 84 * S * math.sin(th) - 4, c + 84 * S * math.cos(th) - 4,
                   c + 84 * S * math.sin(th) + 4, c + 84 * S * math.cos(th) + 4], fill=255)

    h = np.asarray(M.filter(ImageFilter.GaussianBlur(1.3)), dtype=np.float32) / 255
    gy, gx = np.gradient(h)
    tone = 0.30 + 3.4 * (gx + gy) + 0.52 * h
    yy, xx = np.mgrid[0:N, 0:N]
    rr = np.hypot(xx - c + 0.5, yy - c + 0.5) / S
    tone += 0.10 * (-(xx - c) - (yy - c)) / (RAD * S) * 0.6                    # a slow sheen across the field
    tone = np.clip(tone, 0, 1)
    t1 = tone.reshape(N // S, S, N // S, S).mean((1, 3))
    bw = Image.fromarray((t1 * 255).astype(np.uint8)).convert("1")              # Floyd-Steinberg
    r1 = rr.reshape(N // S, S, N // S, S).mean((1, 3))
    coin = np.where(np.asarray(bw)[..., None], np.array(Wh, np.uint8), np.array(K, np.uint8)).astype(np.uint8)
    a = np.zeros((H, W, 3), np.uint8)
    a[:] = R
    ox, oy = 14, 150 - N // S // 2
    sub = a[oy:oy + N // S, ox:ox + N // S]
    inside = r1 <= RAD
    sub[inside] = coin[inside]
    sub[(r1 > RAD - 1.2) & (r1 <= RAD + 0.6)] = K
    # its shadow on the red, lower right
    sh = (np.hypot(xx[::S, ::S] / S - c / S - 4, yy[::S, ::S] / S - c / S - 5) <= RAD) & ~(r1 <= RAD + 0.6)
    sub[sh] = K
    img = Image.fromarray(a)
    d = pen(img)
    fi = font(INTER, 31)
    for i, wd in enumerate(("NICKEL", "IN THE", "SLOT")):
        d.text((246, 30 + i * 33), wd, font=fi, fill=Wh)
    # the slot
    d.rounded_rectangle([246, 142, 384, 166], radius=5, fill=Wh)
    d.rounded_rectangle([256, 150, 374, 158], radius=3, fill=K)
    f = font(MONOB, 10)
    for i, ln in enumerate(("Palais Royale saloon,", "San Francisco,", "Sat 23 Nov 1889:", "a phonograph with",
                            "four ear tubes,", "5c a listen.")):
        d.text((247, 180 + i * 13), ln, font=f, fill=Wh)
    d.text((247, 270), "coin shown x2", font=font(MONO, 10), fill=K)
    save(img, 2)


# ---------------------------------------------------------------- 3. Three steps missing
def moseley():
    """Moseley's law as a staircase: one tick per element, sqrt(frequency) across, atomic number up."""
    img = Image.new("RGB", (W, H), Wh)
    d = pen(img)
    X0, Y0, PZ = 46, 280, 3.9

    def y(Z):
        return int(round(Y0 - (Z - 13) * PZ))

    def xk(Z):
        return X0 + (Z - 1) * math.sqrt(3 / 4) * 8.1 - 60

    def xl(Z):
        return X0 + (Z - 7.4) * math.sqrt(5 / 36) * 8.1 + 14
    # axis: one small tick per atomic number, a longer one every ten
    d.line([(X0 - 10, y(13) + 3), (X0 - 10, y(79) - 3)], fill=K)
    f = font(MONO, 10)
    for Z in range(13, 80):
        L = 6 if Z % 10 == 0 else 2
        d.line([(X0 - 10 - L, y(Z)), (X0 - 10, y(Z))], fill=K)
    for Z, s in ((13, "Al"), (20, "Ca"), (30, "Zn"), (40, "Zr"), (50, "Sn"), (60, "Nd"), (70, "Yb"), (79, "Au")):
        d.text((X0 - 19, y(Z)), f"{s}{Z}", font=f, fill=K, anchor="rm")
    gaps = (43, 61, 75)
    for series, fx, rng_ in (("K", xk, range(13, 48)), ("L", xl, range(40, 80))):
        for Z in rng_:
            x, yy = fx(Z), y(Z)
            if Z in gaps:
                d.rectangle([x - 6, yy - 2, x + 6, yy + 1], outline=R)
                d.rectangle([x - 5, yy - 1, x + 5, yy], fill=Wh)
            else:
                d.rectangle([x - 6, yy - 1, x + 6, yy], fill=K)
                # the riser to the next step, as a hairline
                if Z + 1 in rng_:
                    d.line([(x + 6, yy), (x + 6, y(Z + 1))], fill=K)
        Zt = rng_[-1]
        d.text((fx(Zt) + 12, y(Zt) - 1), series, font=font(INTER, 15), fill=K, anchor="lm")
    # red call-outs for the empty steps
    fb = font(MONOB, 10)
    for Z in gaps:
        x = xl(Z)
        d.line([(x + 9, y(Z)), (x + 30, y(Z))], fill=R)
        d.text((x + 33, y(Z)), str(Z), font=font(INTER, 15), fill=R, anchor="lm")
    d.line([(xk(43) + 9, y(43)), (xl(43) - 9, y(43))], fill=R)
    # legend
    d.text((236, 196), "MOSELEY", font=font(INTER, 27), fill=K)
    for i, ln in enumerate(("b. 23 Nov 1887, Weymouth.", "The X-ray lines of the", "elements climb one even",
                            "step per unit of charge.", "Three steps were empty.")):
        d.text((237, 229 + i * 12), ln, font=fb if i == 4 else f, fill=R if i == 4 else K)
    d.text((398, 4), "square root of frequency  >", font=f, fill=K, anchor="ra")
    save(img, 3)


# ---------------------------------------------------------------- 4. 327
def day327():
    """23 Nov is day 327. n, 2n, 3n = 327, 654, 981: every digit 1-9 once; 327 is the largest such n."""
    img = Image.new("RGB", (W, H), K)
    d = pen(img)
    fnt = font(INTER, 122)
    rows = ("327", "654", "981")
    cw = 88
    for r, row in enumerate(rows):
        for cidx, ch in enumerate(row):
            bb = d.textbbox((0, 0), ch, font=fnt)
            x = 8 + cidx * cw + (cw - (bb[2] - bb[0])) / 2 - bb[0]
            ytop = 9 + r * 96
            d.text((x, ytop - bb[1]), ch, font=fnt, fill=R if r == 0 else Wh)
    # hairlines between the rows
    for r in (1, 2):
        yy = 9 + r * 96 - 5
        for x in range(8, 272, 2):
            img.putpixel((x, yy), Wh)
    fi = font(INTER, 24)
    for r, lab in enumerate(("n", "2n", "3n")):
        d.text((288, 9 + r * 96 + 2), lab, font=fi, fill=R if r == 0 else Wh)
    f = font(MONO, 10)
    for i, ln in enumerate(("Monday", "23 November", "is day 327.")):
        d.text((289, 46 + i * 12), ln, font=f, fill=Wh)
    for i, ln in enumerate(("Nine digits,", "each used", "once.")):
        d.text((289, 142 + i * 12), ln, font=f, fill=Wh)
    for i, ln in enumerate(("No larger n", "does this.")):
        d.text((289, 238 + i * 12), ln, font=f, fill=Wh)
    save(img, 4)


# ---------------------------------------------------------------- 5. Sewn in
def sewn_in():
    """Pascal's Memorial (night of Mon 23 Nov 1654), carried sewn into the lining of his coat. No text."""
    rng = np.random.default_rng(1654)
    yy, xx = np.mgrid[0:H, 0:W]
    CW = 26                                                     # herringbone column width
    col = xx // CW
    lx = xx % CW
    dirn = np.where(col % 2 == 0, 1, -1)
    twill = ((lx * dirn + yy) % 4) == 0                          # white hairlines on black: a dark cloth
    # a slow drape across the cloth: the weave thins towards a fold
    fold = 0.5 + 0.5 * np.sin((xx * 0.9 + yy * 0.25) / 70 + 0.6)
    keep = rng.random((H, W)) < (0.72 + 0.28 * fold)
    a = np.zeros((H, W, 3), np.uint8)
    a[twill & keep] = Wh
    # the paper under the lining: the weave lifts by one thread inside its outline, and its edge shows
    ang = math.radians(-4)
    cx, cy, hw, hh = 176, 152, 86, 56
    u = (xx - cx) * math.cos(ang) + (yy - cy) * math.sin(ang)
    v = -(xx - cx) * math.sin(ang) + (yy - cy) * math.cos(ang)
    inside = (np.abs(u) < hw) & (np.abs(v) < hh)
    tw2 = ((lx * dirn + yy + 2) % 4) <= 1
    a[inside] = K
    a[inside & tw2] = Wh
    edge = (np.abs(u) < hw + 1) & (np.abs(v) < hh + 1) & ~((np.abs(u) < hw - 1) & (np.abs(v) < hh - 1))
    a[edge] = K
    img = Image.fromarray(a)
    d = ImageDraw.Draw(img)

    def P(uu, vv):
        return (cx + uu * math.cos(ang) - vv * math.sin(ang), cy + uu * math.sin(ang) + vv * math.cos(ang))
    # hand stitches, a little uneven, all the way round
    path = []
    m = 9
    corners = [(-hw - m, -hh - m), (hw + m, -hh - m), (hw + m, hh + m), (-hw - m, hh + m)]
    for i in range(4):
        (u0, v0), (u1, v1) = corners[i], corners[(i + 1) % 4]
        L = math.hypot(u1 - u0, v1 - v0)
        t = 4.0
        while t < L - 6:
            sl = 7 + rng.random() * 3
            j0, j1 = rng.normal(0, 1.1), rng.normal(0, 1.1)
            nx, ny = -(v1 - v0) / L, (u1 - u0) / L
            p0 = P(u0 + (u1 - u0) * t / L + nx * j0, v0 + (v1 - v0) * t / L + ny * j0)
            p1 = P(u0 + (u1 - u0) * (t + sl) / L + nx * j1, v0 + (v1 - v0) * (t + sl) / L + ny * j1)
            path.append((p0, p1))
            t += sl + 5 + rng.random() * 3
    for p0, p1 in path:
        d.line([p0, p1], fill=K, width=6)
    for p0, p1 in path:
        d.line([p0, p1], fill=R, width=3)
    # the coat's own seam, machine-straight, far right
    d.rectangle([338, 0, 344, H], fill=K)
    for y0 in range(3, H, 9):
        d.line([(341, y0), (341, y0 + 5)], fill=Wh)
    save(img, 5)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    one_breath()
    nickel()
    moseley()
    day327()
    sewn_in()
    # palette check
    for n in range(1, 6):
        im = Image.open(f"images/{n}.png").convert("RGB")
        assert im.size == (W, H)
        cols = {c for _, c in im.getcolors(16)}
        assert cols <= {K, Wh, R}, cols
    print("ok")
