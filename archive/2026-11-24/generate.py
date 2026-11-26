#!/usr/bin/env python3
"""2026-11-24 — five plates: Beaver supermoon / Darwin / Spinoza / Turing / Lucy.
Five different algorithms: Poisson stipple, space colonization, ray tracing,
Gray-Scott reaction-diffusion, Penrose deflation.  Run: python3 generate.py"""
import math, cmath, random, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

W, H = 400, 300
K, WH, R = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    if name == "DejaVuSerif-Italic":
        return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", int(size * 1.15))
    return ImageFont.truetype(FD + name + ".ttf", size)
MONO = font("DejaVuSansMono", 9)

def snap(img):
    """force every pixel to nearest of the 3 inks, save-ready P image"""
    a = np.asarray(img.convert("RGB")).astype(int)
    pal = np.array([K, WH, R])
    idx = ((a[:, :, None, :] - pal[None, None]) ** 2).sum(-1).argmin(-1).astype(np.uint8)
    out = Image.fromarray(idx, "P")
    out.putpalette([0, 0, 0, 255, 255, 255, 255, 0, 0] + [0] * 759)
    return out

def caption(img, n, left, fg=K, bg=WH):
    """house style: a 13px plate strip along the bottom"""
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 13, W, H], fill=bg)
    d.line([0, H - 14, W, H - 14], fill=fg)
    d.text((4, H - 12), left, font=MONO, fill=fg)
    r = f"24·XI·2026  {n}/5"
    d.text((W - 4 - d.textlength(r, font=MONO), H - 12), r, font=MONO, fill=fg)

def save(img, n):
    snap(img).save(os.path.join(OUT, f"{n}.png"))

# ---------------------------------------------------------------- 1. moon
def plate1():
    rnd = random.Random(241126)
    img = Image.new("RGB", (W, H), K); d = ImageDraw.Draw(img)
    cx, cy, rad = 128, 150, 112
    # darkness field: maria (low-freq noise) + craters
    rs = np.random.RandomState(7)
    n = sum(ndimage.zoom(rs.rand(H // s + 2, W // s + 2), s, order=3)[:H, :W] * w
            for s, w in ((64, .55), (32, .3), (12, .15)))
    n = (n - n.min()) / (n.max() - n.min())
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.hypot(xx - cx, yy - cy) / rad
    dark = np.clip((n - .47) * 5, 0, 1) * .8
    dark += .25 * np.clip(rr, 0, 1) ** 6            # limb
    craters = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(.02, .07)) for _ in range(40)]
    craters.append((-.25, .62, .09))                # a Tycho, with rays
    for ux, uy, cr in craters:
        if ux * ux + uy * uy > .85: continue
        q = np.hypot(xx - cx - ux * rad, yy - cy - uy * rad) / (cr * rad)
        dark = np.where(q < 1, dark * .15, dark)                      # bright floor
        dark += .9 * np.exp(-((q - 1.05) / .12) ** 2) * (xx - cx - ux * rad > -yy + cy + uy * rad)
    tx, ty = cx - .25 * rad, cy + .62 * rad
    ang = np.arctan2(yy - ty, xx - tx); dist = np.hypot(xx - tx, yy - ty)
    rays = (np.cos(ang * 9 + 1) > .93) & (dist < 95) & (dist > 12)
    dark = np.where(rays, dark * .2, dark)
    dark = np.clip(dark, 0, .95)
    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=WH)
    # variable-density Poisson stipple
    cell = 2; grid = {}
    for _ in range(140000):
        x, y = rnd.uniform(cx - rad, cx + rad), rnd.uniform(cy - rad, cy + rad)
        if (x - cx) ** 2 + (y - cy) ** 2 > rad * rad or not (0 <= y < H): continue
        dk = dark[int(y), int(x)]
        if dk < .04: continue
        md = 1.1 + 5.5 * (1 - dk) ** 2.2
        gx, gy = int(x / cell), int(y / cell); ok = True; k = int(md / cell) + 1
        for i in range(gx - k, gx + k + 1):
            for j in range(gy - k, gy + k + 1):
                for px, py in grid.get((i, j), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < md * md: ok = False; break
                if not ok: break
            if not ok: break
        if ok:
            grid.setdefault((gx, gy), []).append((x, y))
            if dk > .6: d.rectangle([x, y, x + 1, y], fill=K)
            else: d.point((x, y), fill=K)
    # Pleiades (real relative positions), in red
    stars = {"Alcyone": (56.87, 24.11, 3), "Atlas": (57.29, 24.05, 2), "Pleione": (57.30, 24.14, 1),
             "Maia": (56.46, 24.37, 2), "Electra": (56.22, 24.11, 2), "Merope": (56.58, 23.95, 2),
             "Taygeta": (56.30, 24.47, 2), "Celaeno": (56.20, 24.29, 1), "Asterope": (56.48, 24.55, 1)}
    S = 105; ox, oy = 322, 88
    for nm, (ra, de, m) in stars.items():
        x = ox - (ra - 56.75) * math.cos(math.radians(24.2)) * S
        y = oy - (de - 24.2) * S
        if m == 3:
            d.line([x - 6, y, x + 6, y], fill=R); d.line([x, y - 6, x, y + 6], fill=R)
        d.ellipse([x - m, y - m, x + m, y + m], fill=R)
        if nm in ("Alcyone", "Atlas", "Maia"):
            d.text((x - 14, y + 7), nm.lower(), font=MONO, fill=WH)
    for _ in range(70):                               # field stars
        x, y = rnd.uniform(0, W), rnd.uniform(0, H - 16)
        if (x - cx) ** 2 + (y - cy) ** 2 > (rad + 6) ** 2: d.point((x, y), fill=WH)
    f = font("DejaVuSerif-Bold", 15)
    d.text((262, 196), "BEAVER", font=f, fill=WH)
    d.text((262, 214), "SUPERMOON", font=f, fill=R)
    d.text((263, 236), "full 14:53 UTC", font=MONO, fill=WH)
    d.text((263, 247), "perigee tomorrow", font=MONO, fill=WH)
    d.text((263, 258), "meets the Pleiades", font=MONO, fill=WH)
    caption(img, 1, "LUNA · stipple", fg=WH, bg=K)
    save(img, 1)

# ---------------------------------------------------------------- 2. Darwin
def plate2():
    rnd = random.Random(1859)
    img = Image.new("RGB", (W, H), WH); d = ImageDraw.Draw(img)
    root = (150, 262)
    att = []
    while len(att) < 520:
        x, y = rnd.uniform(40, 392), rnd.uniform(14, 250)
        a = math.atan2(root[1] - y, x - root[0]); r = math.hypot(x - root[0], y - root[1])
        if .12 < a < 2.6 and 45 < r < 250 + 40 * math.sin(a * 3) and not (x < 150 and y < 95):
            att.append((x, y))
    att = np.array(att)
    nodes = [root, (root[0] + 2, root[1] - 5)]; parent = [-1, 0]
    alive = np.ones(len(att), bool)
    for it in range(400):
        P = np.array(nodes); A = att[alive]
        if len(A) == 0: break
        D = np.hypot(A[:, None, 0] - P[None, :, 0], A[:, None, 1] - P[None, :, 1])
        near = D.argmin(1); dmin = D.min(1)
        pull = {}
        for ai, (ni, dm) in enumerate(zip(near, dmin)):
            if dm < 60:
                v = (A[ai] - P[ni]) / max(dm, 1e-6); pull.setdefault(ni, []).append(v)
        if not pull: break
        for ni, vs in pull.items():
            v = np.sum(vs, 0); nv = np.hypot(*v)
            if nv < 1e-6: continue
            v = v / nv + np.array([rnd.uniform(-.25, .25), rnd.uniform(-.25, .25)])
            p = P[ni] + 4 * v / np.hypot(*v)
            nodes.append((p[0], p[1])); parent.append(ni)
        P = np.array(nodes)
        D = np.hypot(att[:, None, 0] - P[None, :, 0], att[:, None, 1] - P[None, :, 1]).min(1)
        alive &= D > 7
    n = len(nodes); kids = [0] * n; weight = [1] * n
    for i in range(n - 1, 0, -1):
        weight[parent[i]] += weight[i]; kids[parent[i]] += 1
    for i in range(1, n):
        w = 1 if weight[i] < 25 else 2 if weight[i] < 140 else 3
        d.line([nodes[parent[i]], nodes[i]], fill=K, width=w)
    tips = [i for i in range(n) if kids[i] == 0]
    rnd.shuffle(tips)
    for j, i in enumerate(tips):
        x, y = nodes[i]; px, py = nodes[parent[i]]
        if j % 5 < 2:                                 # the living: a red bud
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=R)
        elif j % 5 < 4:                               # a crossbar, as in the notebook
            vx, vy = x - px, y - py; l = math.hypot(vx, vy) or 1
            d.line([x - vy / l * 3, y + vx / l * 3, x + vy / l * 3, y - vx / l * 3], fill=K)
    fs = font("DejaVuSerif-Italic", 12)
    far = sorted(tips, key=lambda i: nodes[i][0])
    for lab, i in zip("ABCD", (far[1], far[len(far) // 3], far[2 * len(far) // 3], far[-2])):
        x, y = nodes[i]; d.text((x + 4, y - 14), lab, font=fs, fill=K)
    d.ellipse([root[0] - 8, root[1] - 2, root[0] + 8, root[1] + 14], outline=K)
    d.text((root[0] - 3, root[1]), "1", font=fs, fill=K)
    d.text((22, 18), "I think", font=font("DejaVuSerif-Italic", 34), fill=K)
    d.line([24, 60, 132, 57], fill=R, width=2)
    d.text((24, 66), "notebook B, p. 36", font=MONO, fill=K)
    d.text((24, 77), "1837", font=MONO, fill=K)
    caption(img, 2, "ORIGIN OF SPECIES, 24 Nov 1859 · space colonization")
    save(img, 2)

# ---------------------------------------------------------------- 3. Spinoza
def plate3():
    S = 3
    img = Image.new("RGB", (W * S, H * S), K); d = ImageDraw.Draw(img)
    cx, cy, Rr, t, nn = 105.0, 143.0, 140.0, 90.0, 1.5
    c1 = (cx - t / 2 + Rr, cy); c2 = (cx + t / 2 - Rr, cy)
    h = math.sqrt(Rr ** 2 - (Rr - t / 2) ** 2)
    pts = []
    a0 = math.asin(h / Rr)
    for i in range(61):
        a = -a0 + 2 * a0 * i / 60; pts.append((c2[0] + Rr * math.cos(a), cy + Rr * math.sin(a)))
    for i in range(61):
        a = a0 - 2 * a0 * i / 60; pts.append((c1[0] - Rr * math.cos(a), cy + Rr * math.sin(a)))
    d.polygon([(x * S, y * S) for x, y in pts], fill=R)
    def hit(o, v, c, far):
        ox, oy = o[0] - c[0], o[1] - c[1]
        b = ox * v[0] + oy * v[1]; q = b * b - (ox * ox + oy * oy - Rr * Rr)
        if q < 0: return None
        tt = -b + math.sqrt(q) if far else -b - math.sqrt(q)
        return (o[0] + v[0] * tt, o[1] + v[1] * tt)
    def refr(v, nrm, eta):
        ci = -(v[0] * nrm[0] + v[1] * nrm[1]); s2 = eta * eta * (1 - ci * ci)
        if s2 > 1: return None
        k = eta * ci - math.sqrt(1 - s2)
        return (eta * v[0] + k * nrm[0], eta * v[1] + k * nrm[1])
    for i in range(-24, 25):
        y0 = cy + i * 4.0
        o = (0.0, y0); v = (1.0, 0.0)
        p1 = hit(o, v, c1, False)
        if p1 is None or abs(p1[1] - cy) > h - 1:
            continue
        n1 = ((p1[0] - c1[0]) / Rr, (p1[1] - c1[1]) / Rr)
        v1 = refr(v, n1, 1 / nn)
        p2 = hit(p1, v1, c2, True)
        n2 = (-(p2[0] - c2[0]) / Rr, -(p2[1] - c2[1]) / Rr)
        v2 = refr(v1, n2, nn)
        d.line([0, y0 * S, p1[0] * S, p1[1] * S], fill=WH, width=S)
        d.line([p1[0] * S, p1[1] * S, p2[0] * S, p2[1] * S], fill=K, width=S)
        if v2:
            e = (p2[0] + v2[0] * 600, p2[1] + v2[1] * 600)
            d.line([p2[0] * S, p2[1] * S, e[0] * S, e[1] * S], fill=WH, width=S)
    img = img.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 21], fill=K); d.rectangle([0, 262, W, H], fill=K)
    f = font("DejaVuSerif-Bold", 13)
    d.text((6, 4), "DEUS SIVE NATURA", font=f, fill=WH)
    r = "B. de Spinoza, lens grinder"
    d.text((W - 6 - d.textlength(r, font=MONO), 7), r, font=MONO, fill=R)
    d.text((6, 266), "b. Amsterdam, 24 Nov 1632.  No lens is perfect:", font=MONO, fill=WH)
    d.text((6, 276), "the edge rays cross early, and draw a caustic.", font=MONO, fill=WH)
    caption(img, 3, "ETHICA · ray trace, n = 1.5", fg=WH, bg=K)
    save(img, 3)

# ---------------------------------------------------------------- 4. Turing
def plate4():
    gw, gh = 200, 150
    rs = np.random.RandomState(1952)
    U = np.ones((gh, gw)); V = np.zeros((gh, gw))
    for _ in range(90):
        x, y = rs.randint(4, gw - 4), rs.randint(4, gh - 4)
        U[y - 2:y + 3, x - 2:x + 3] = .5; V[y - 2:y + 3, x - 2:x + 3] = .25 + rs.rand() * .1
    gx = np.linspace(0, 1, gw)[None, :] * np.ones((gh, 1))
    gx = gx ** 2.2
    F = .029 + .031 * gx                      # spots (left) -> labyrinth (right)
    k = .0612 + .0018 * gx
    lap = lambda Z: (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)
    for _ in range(9000):
        uvv = U * V * V
        U += .16 * lap(U) - uvv + F * (1 - U)
        V += .08 * lap(V) + uvv - (F + k) * V
    big = ndimage.zoom(V, 2, order=3)
    ink = big > .2
    lab, nl = ndimage.label(ink)
    sizes = ndimage.sum(ink, lab, range(1, nl + 1))
    small = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s < 320])
    a = np.full((H, W, 3), 255, np.uint8)
    a[ink] = K; a[small] = R
    img = Image.fromarray(a)
    d = ImageDraw.Draw(img)
    msg = "endless forms most beautiful"
    f = font("DejaVuSerif-Italic", 15); tw = d.textlength(msg, font=f)
    d.rectangle([W - tw - 22, 250, W, 276], fill=WH); d.rectangle([W - tw - 22, 250, W, 276], outline=K)
    d.text((W - tw - 11, 253), msg, font=f, fill=K)
    caption(img, 4, "MORPHOGENESIS · Gray-Scott, after Turing 1952")
    save(img, 4)

# ---------------------------------------------------------------- 5. Lucy
def plate5():
    phi = (1 + 5 ** .5) / 2
    tris = []
    for i in range(10):
        b = cmath.rect(1, (2 * i - 1) * math.pi / 10); c = cmath.rect(1, (2 * i + 1) * math.pi / 10)
        if i % 2 == 0: b, c = c, b
        tris.append((0, 0j, b, c))
    for _ in range(6):
        nxt = []
        for col, a, b, c in tris:
            if col == 0:
                p = a + (b - a) / phi
                nxt += [(0, c, p, b), (1, p, c, a)]
            else:
                q = b + (a - b) / phi; r = b + (c - b) / phi
                nxt += [(1, r, c, a), (1, q, r, b), (0, r, q, a)]
        tris = nxt
    S = 3; sc = 290 * S; off = complex(200 * S, 128 * S)
    img = Image.new("RGB", (W * S, H * S), K); d = ImageDraw.Draw(img)
    P = lambda z: ((z * sc + off).real, (z * sc + off).imag)
    rnd = random.Random(288)
    def key(z): return (round(z.real * 1e4), round(z.imag * 1e4))
    redset = {}
    for col, a, b, c in tris:
        m = (b + c) / 2; rr = abs(m) * 290
        if col == 0:      # thin rhomb = a diamond
            kk = key(m)
            if kk not in redset: redset[kk] = rnd.random() < max(.0, .8 - rr / 210)
            fill = R if redset[kk] else WH
        else:
            fill = K
        d.polygon([P(a), P(b), P(c)], fill=fill)
    for col, a, b, c in tris:
        d.line([P(c), P(a), P(b)], fill=WH if col else K, width=S)
    img = img.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 236, W, H], fill=WH); d.line([0, 236, W, 236], fill=K, width=2)
    d.text((8, 238), "LUCY", font=font("DejaVuSans-Bold", 40), fill=K)
    x = 138
    d.text((x, 243), "in the sky, with diamonds.", font=font("DejaVuSerif-Italic", 13), fill=R)
    d.text((x, 261), "AL 288-1 · Hadar, Afar · 3.2 million years", font=MONO, fill=K)
    d.text((x, 272), "found 24 Nov 1974, the tape still playing", font=MONO, fill=K)
    caption(img, 5, "AUSTRALOPITHECUS · Penrose deflation ×6")
    save(img, 5)

if __name__ == "__main__":
    for p in (plate1, plate2, plate3, plate4, plate5): p()
    import shutil
    for n in range(1, 6):
        shutil.copy(os.path.join(OUT, f"{n}.png"), os.path.join(OUT, "..", "..", "images", f"{n}.png"))
