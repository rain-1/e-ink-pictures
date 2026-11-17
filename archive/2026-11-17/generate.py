#!/usr/bin/env python3
"""2026-11-17 (Tuesday). Theme: turns.  Run from the repo root.
1 Tracks (Lunokhod 1, 1970)   2 One edge (Moebius, b. 1790)   3 Suez (1869)
4 X-Y position indicator (the mouse patent, 1970)   5 Keys (Prague, 1989)"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
TILT, PHI = 60, 200
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = ["images", "archive/2026-11-17"]
F = "/usr/share/fonts/truetype/"
def font(name, size):
    paths = {"mono": F+"dejavu/DejaVuSansMono.ttf", "monob": F+"dejavu/DejaVuSansMono-Bold.ttf",
             "sansb": F+"dejavu/DejaVuSans-Bold.ttf",
             "ital": F+"liberation/LiberationSerif-Italic.ttf", "serif": F+"liberation/LiberationSerif-Regular.ttf",
             "serifb": F+"liberation/LiberationSerif-Bold.ttf",
             "black": "/usr/share/fonts/opentype/inter/Inter-Black.otf"}
    return ImageFont.truetype(paths[name], size)
def save(im, n):
    pal = Image.new("P", (1, 1)); pal.putpalette([0,0,0, 255,255,255, 255,0,0] + [0,0,0]*253)
    q = im.convert("RGB").quantize(palette=pal, dither=Image.Dither.NONE)
    for o in OUT:
        os.makedirs(o, exist_ok=True); q.save(f"{o}/{n}.png")
def fs_bw(a):
    a = a.copy(); h, w = a.shape; out = np.zeros((h, w), bool)
    for y in range(h):
        for x in range(w):
            v = a[y, x]; o = v >= 0.5; out[y, x] = o; e = v - (1.0 if o else 0.0)
            if x+1 < w: a[y, x+1] += e*7/16
            if y+1 < h:
                if x > 0: a[y+1, x-1] += e*3/16
                a[y+1, x] += e*5/16
                if x+1 < w: a[y+1, x+1] += e/16
    return out
def rgb(mask_white):
    return Image.fromarray(np.where(mask_white[..., None], 255, 0).astype(np.uint8).repeat(3, 2), "RGB")
def chaikin(p, n=3):
    p = np.asarray(p, float)
    for _ in range(n):
        q = 0.75*p[:-1] + 0.25*p[1:]; r = 0.25*p[:-1] + 0.75*p[1:]
        p = np.vstack([p[:1], np.stack([q, r], 1).reshape(-1, 2), p[-1:]])
    return p
def vnoise(X, Z, seed):
    tab = np.random.default_rng(seed).random((256, 256))
    xi = np.floor(X).astype(int); zi = np.floor(Z).astype(int)
    fx = X - xi; fz = Z - zi; fx = fx*fx*(3-2*fx); fz = fz*fz*(3-2*fz)
    a = tab[zi & 255, xi & 255]; b = tab[zi & 255, (xi+1) & 255]
    c = tab[(zi+1) & 255, xi & 255]; e = tab[(zi+1) & 255, (xi+1) & 255]
    return (a*(1-fx) + b*fx)*(1-fz) + (c*(1-fx) + e*fx)*fz

# ------------------------------------------------------------ 1  Tracks: Lunokhod 1 on Mare Imbrium
def tracks():
    rng = np.random.default_rng(1970)
    f, h, hy, cx = 400.0, 1.1, 100, 200
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    Z = f*h/np.maximum(yy - hy + 0.5, 0.5); X = (xx - cx)*Z/f
    fade = 1/(1 + Z/22)
    T = 0.70 + fade*(0.22*(vnoise(X*1.3, Z*1.3, 1) - 0.5) + 0.20*(vnoise(X*5, Z*5, 2) - 0.5)
                     + 0.16*(vnoise(X*19, Z*19, 3) - 0.5))
    T += 0.08*(1 - fade)
    # craters and stones, sun low on the left
    for i in range(110):
        zc = 2.5 + 55*rng.random()**1.6; xc = (rng.random()*2 - 1)*(1.2 + zc*0.55)
        r = 0.10 + 1.1*rng.random()**4 + 0.02*zc
        stone = i % 4 == 0
        if stone: r *= 0.35
        u = (X - xc)/r; v = (Z - zc)/r; d2 = u*u + v*v
        if stone:
            T += np.where(d2 < 1, 0.55*(-u) - 0.1, 0) + np.where((u > 0) & (u < 3.2) & (np.abs(v) < 1 - u/3.2), -0.45, 0)
        else:
            T += np.where(d2 < 1, 0.55*u*np.sqrt(np.clip(1 - d2, 0, 1)) - 0.06, 0)
            T += np.where((d2 >= 1) & (d2 < 1.7), -0.16*u/np.sqrt(d2), 0)
    # the track: distance from every ground pixel to a wandering centre line
    path = chaikin([(0.1, 0), (0.1, 3), (-0.7, 6), (-2.2, 9), (-3.3, 12), (-3.1, 15), (-1.6, 17.1),
                    (0.4, 18.1), (2.2, 18.4), (3.6, 18.4)], 3)
    D = np.full((H, W), 1e9); S = np.zeros((H, W)); acc = 0.0
    for (x0, z0), (x1, z1) in zip(path[:-1], path[1:]):
        dx, dz = x1 - x0, z1 - z0; L = math.hypot(dx, dz)
        t = np.clip(((X - x0)*dx + (Z - z0)*dz)/(L*L), 0, 1)
        d = np.hypot(X - x0 - t*dx, Z - z0 - t*dz)
        m = d < D; D[m] = d[m]; S[m] = (acc + t*L)[m]; acc += L
    e = np.abs(D - 0.8)
    groove = (e < 0.115) & (S < acc - 0.02)
    cleat = (S/0.17) % 1 < 0.5
    T = np.where(groove, np.where(cleat | (Z > 9), 0.10, 0.42), T)
    T = np.where((e >= 0.115) & (e < 0.15) & (S < acc - 0.02) & (Z < 9), T + 0.2, T)
    # rover shadow on the ground (thrown to the right)
    rx, rz = 3.2, 18.4
    T = np.where((np.abs(Z - rz) < 1.6) & (X > rx - 1.0) & (X < rx + 3.6 - np.abs(Z - rz)*0.8), 0.03, T)
    bump = hy + 2.5*np.sin(xx/47.0) + 1.5*np.sin(xx/13.0 + 1) + 1.0
    T = np.where(yy < bump, 0.0, np.clip(T, 0.02, 0.97))
    bw = fs_bw(T); bw[yy < bump] = False
    im = rgb(bw)
    # the rover, side-on, drawn at 3x
    s = f/rz; gx = cx + rx*s; gy = hy + f*h/rz
    k = 3; big = Image.new("RGB", (W*k, H*k), (0, 255, 0)); d = ImageDraw.Draw(big)
    P = lambda x, y: ((gx + x*s)*k, (gy - y*s)*k)
    d.polygon([P(-0.95, 0.42), P(0.95, 0.42), P(1.12, 1.0), P(-1.12, 1.0)], fill=WHITE, outline=BLACK, width=3)
    d.line([P(-1.0, 0.62), P(1.0, 0.62)], fill=BLACK, width=2)
    d.line([P(-1.08, 1.03), P(-1.55, 1.82)], fill=WHITE, width=10)       # the open lid
    d.line([P(-1.02, 1.05), P(-1.47, 1.80)], fill=RED, width=5)          # its solar cells
    d.line([P(0.75, 1.0), P(0.95, 1.75)], fill=WHITE, width=3)           # antenna mast
    d.polygon([P(0.80, 1.72), P(1.22, 1.62), P(1.05, 1.95)], fill=WHITE)
    d.line([P(0.2, 1.0), P(0.2, 1.42)], fill=WHITE, width=3)
    d.rectangle([*P(0.9, 0.92), *P(1.22, 0.7)], fill=WHITE, outline=BLACK)
    for wx in (-0.86, -0.29, 0.29, 0.86):
        x0, y0 = P(wx, 0.255); r = 0.265*s*k
        d.ellipse([x0-r, y0-r, x0+r, y0+r], fill=BLACK, outline=WHITE, width=3)
        d.ellipse([x0-4, y0-4, x0+4, y0+4], fill=WHITE)
    small = big.resize((W, H), Image.LANCZOS); a = np.asarray(small).astype(int); o = np.asarray(im).copy()
    key = (a[..., 1] > 150) & (a[..., 0] < 110) & (a[..., 2] < 110)
    o[~key] = a[~key]
    save(Image.fromarray(o.astype(np.uint8)), 1)

# ------------------------------------------------------------ 2  One edge: a Moebius band as its rulings
def moebius():
    k = 3; N, R, hw = 132, 1.0, 0.55
    tilt, phi, dist, sc = math.radians(TILT), math.radians(PHI), 6.0, 136.0
    u, v = np.meshgrid(np.linspace(0, 2*math.pi, 7000, endpoint=False), np.linspace(-hw, hw, 560))
    x = (R + v*np.cos(u/2))*np.cos(u + phi); y = (R + v*np.cos(u/2))*np.sin(u + phi); z = v*np.sin(u/2)
    ys = y*math.cos(tilt) + z*math.sin(tilt)            # up the screen
    dp = y*math.sin(tilt) - z*math.cos(tilt)            # away from the viewer
    w = dist/(dist + dp)
    px = np.rint((226 + sc*x*w)*k).astype(int).ravel(); py = np.rint((140 - sc*ys*w)*k).astype(int).ravel()
    col = np.where(np.abs(v) > hw - 0.022, 2, np.where((u*N/(2*math.pi)) % 1 < 0.34, 0, 1)).ravel()
    order = np.argsort(-dp.ravel())                     # far first, near last (near wins)
    buf = np.zeros((H*k, W*k), np.uint8)
    buf[py[order], px[order]] = col[order]
    im = Image.fromarray(np.array([BLACK, WHITE, RED], np.uint8)[buf], "RGB")
    save(im.resize((W, H), Image.LANCZOS), 2)

# ------------------------------------------------------------ 3  Suez: the long way and the short way
AFRICA = [(-6,35.8),(-2,35),(3,36.9),(10,37.3),(11,33.5),(15,32.3),(19,30.4),(20,32.6),(23,32.5),(25,31.5),(29,31),
 (32.2,31.2),(32.4,30),(33.8,27),(35.5,24),(37,21),(37.5,18.5),(39.5,15.5),(42.8,12.6),(43.5,11.4),(45,10.5),(51,12),
 (50.5,9),(48,5),(46,2.5),(42,-1.5),(40.5,-3),(39,-6),(39.5,-10),(40.5,-14.5),(38,-17.5),(35,-20),(35.5,-24),(33,-25.5),
 (32.5,-28.5),(30,-31),(27,-33.6),(22,-34.2),(20,-34.8),(18.4,-34.3),(18,-32),(17,-29),(15,-26),(14.5,-22),(12,-17),
 (13.5,-12),(12.2,-6),(9,-1),(9.5,3.5),(7,4.5),(4,6.3),(1,6),(-3,5),(-7.5,4.4),(-11,7),(-13.5,9.5),(-16.5,12.5),
 (-17.5,14.7),(-16.3,19),(-17,21),(-15,24),(-13,27.5),(-10,29.5),(-9.5,32)]
EURASIA = [(-9,43),(-9.5,38.7),(-9,37),(-6,36.25),(-5,36.4),(-2,36.8),(0,38.7),(-0.3,39.5),(3,42),(3.5,43.3),(6,43),
 (8.8,44.4),(10.5,43.5),(12.5,41.5),(15.5,40),(16,38),(17.2,39),(16.5,40.5),(18.5,40.2),(16,41.8),(13.5,43.7),(12.3,45.3),
 (13.7,45.6),(15,44.5),(19.3,41.8),(20,39.5),(21.5,37),(22.8,36.5),(23.5,38),(22.8,40.3),(24,40.8),(26,40.7),(26.3,39.5),
 (27,37),(28.5,36.7),(30.5,36.5),(32.5,36.1),(36,36.7),(35.8,35),(35,32.5),(34.3,31.3),(32.9,31.1),(33.0,29.9),(33.6,28.5),
 (34.3,27.8),(34.9,29.5),(35.5,27.5),(37.5,24.5),(39,21.5),(41,18.5),(42.7,15),(43.5,12.8),(45,12.9),(48.5,14),(52,16.5),
 (55,17.5),(57.5,19),(59.8,22.5),(58.5,23.7),(56.5,24.5),(56.3,26.2),(55.5,25.5),(54,24.2),(51.8,24),(51.5,26),(50.5,25.5),
 (50,27),(48.5,29.5),(49,30.3),(50.5,29.5),(52,27.7),(54.5,26.6),(56.5,27),(57.5,25.6),(61.5,25.2),(66.5,25.3),(67.5,24),
 (68.5,23),(69,22.2),(70.4,20.8),(72.2,21),(72.8,19),(73.5,16),(74.8,12.8),(76.3,9.5),(77.5,8.1),(78.2,9),(79.3,10.3),
 (80.2,13),(80.2,15.5),(82.3,16.6),(85,19.5),(87,21.5),(89,21.8),(91,22.5),(92.2,21),(94.3,16),(96,17),(97.5,16.5),
 (98.5,12),(98.5,8),(100.5,6.5),(103,2),(108,2),(108,62),(30,62),(30,60),(28,59.6),(23.5,59.3),(24,57.5),(21,57.5),
 (21,55.5),(18.5,54.7),(14,54),(11,54),(10,55.5),(10.5,57.7),(8.2,57),(8.3,55),(8.5,53.8),(5,53.3),(4,52),(1.6,50.9),
 (0.2,49.5),(-1.5,49.6),(-1.6,48.6),(-4.7,48.4),(-2.5,47.3),(-1.2,46),(-2,43.4),(-8,43.7)]
ISLANDS = [[(49.3,-12),(50.3,-15.5),(49,-19),(47.5,-24.5),(45.5,-25.4),(43.7,-22.5),(44.3,-19.5),(44,-16.5),(47,-14.5)],
 [(-5.5,50),(1.3,51.2),(1.7,52.7),(0,53.5),(-1.5,55),(-2,57.5),(-3.5,58.6),(-5.5,58.5),(-6,56.5),(-4.8,54.8),(-3,54),
  (-4.5,53.2),(-4.3,52),(-5.2,51.7),(-3.2,51.3)],
 [(-6,52.2),(-6,55),(-8,55.2),(-10,54),(-10,51.7)], [(80,9.7),(81.8,7.5),(81,6),(80,6.2),(79.8,8)],
 [(12.5,38),(15.5,38.2),(15,36.7)], [(8.3,41),(9.7,41),(9.5,39.2),(8.5,39)], [(23.5,35.5),(26.3,35.3),(24.5,34.9)],
 [(32.3,35),(34.5,35.6),(33.5,34.6)], [(5,60),(7,58),(11.5,59),(12,62),(5,62)]]
SEAS = [[(28,41.2),(31.5,41.2),(35,42),(38,41),(41.5,41.5),(41,43),(37,45),(36.5,45.4),(33.5,44.5),(32.5,46),(30.8,46.5),
  (28.8,44.5),(27.8,42.5)], [(50,37),(54,37),(53,40),(53,42),(51,45),(47.5,46.5),(47,44),(49.5,40.5),(49,38)]]
def suez():
    k = 3; S = 3.0
    M = lambda lo, la: ((lo + 27)*S*k, (60 - la)*S*k)
    im = Image.new("RGB", (W*k, H*k), WHITE); d = ImageDraw.Draw(im)
    for poly in [AFRICA, EURASIA] + ISLANDS: d.polygon([M(*p) for p in poly], fill=BLACK)
    for poly in SEAS: d.polygon([M(*p) for p in poly], fill=WHITE)
    shared = [(0.6,51.4),(1.6,51.25),(1.2,50.5),(-2,49.9),(-6.5,48.6),(-11,44),(-11.3,38.5)]
    cape = chaikin(shared + [(-14,34),(-21.5,24),(-23.5,14),(-19,5),(-8,-4),(2,-17),(11,-29),(16.5,-35.6),(21,-37),
            (29,-35),(36,-28.5),(40.5,-20),(42,-12.5),(45,-5),(54,5),(64,13),(72.4,18.8)], 3)
    canal = chaikin(shared + [(-9.5,36.3),(-6.6,35.98),(-5.2,36.05),(-1.5,36.2),(4,37.6),(10,37.9),(11.8,36.9),(15,35),(22,33.9),
             (28,32.4),(31.8,31.6),(32.55,31.2),(32.7,29.9),(33.5,27.9),(34.5,26),(36.3,23),(38.3,20),(40,17),(42,14.2),
             (43.2,12.65),(44,12),(46,12.1),(52,13.6),(61,16),(72.4,18.8)], 3)
    pts = [M(*p) for p in cape]; acc = 0
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0]-a[0], b[1]-a[1]); n = max(1, int(L/3))
        for j in range(n):
            t = j/n; s_ = acc + t*L
            if (s_ % 27) < 15:
                x, y = a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t; d.ellipse([x-3.5, y-3.5, x+3.5, y+3.5], fill=BLACK)
        acc += L
    pc = [M(*p) for p in canal]
    off = [(x + 9, y + 3) if i < 30 else (x, y) for i, (x, y) in enumerate(pc)]
    d.line(off, fill=WHITE, width=13, joint="curve"); d.line(off, fill=RED, width=7, joint="curve")
    for lo, la in [(0.3, 51.5), (72.8, 19)]:
        x, y = M(lo, la); d.ellipse([x-13, y-13, x+13, y+13], fill=WHITE, outline=BLACK, width=5)
    im = im.resize((W, H), Image.LANCZOS)
    pal = Image.new("P", (1, 1)); pal.putpalette([0,0,0, 255,255,255, 255,0,0] + [0,0,0]*253)
    im = im.quantize(palette=pal, dither=Image.Dither.NONE).convert("RGB")
    d = ImageDraw.Draw(im); d.fontmode = "1"
    d.text((6, 36), "LONDON", font=font("monob", 10), fill=BLACK); d.line([(44, 38), (76, 28)], fill=BLACK)
    d.text((306, 100), "BOMBAY", font=font("monob", 10), fill=WHITE)
    x0, y0 = 262, 178
    d.text((x0, y0), "17 NOV 1869", font=font("monob", 10), fill=BLACK)
    d.text((x0 - 2, y0 + 10), "SUEZ", font=font("black", 34), fill=BLACK)
    d.text((x0, y0 + 52), "London to Bombay", font=font("mono", 10), fill=BLACK)
    for i in range(0, 22, 9): d.rectangle([x0 + i, y0 + 72, x0 + i + 4, y0 + 73], fill=BLACK)
    d.text((x0 + 30, y0 + 66), "10,667 mi", font=font("monob", 10), fill=BLACK)
    d.rectangle([x0, y0 + 87, x0 + 22, y0 + 89], fill=RED)
    d.text((x0 + 30, y0 + 82), " 6,274 mi", font=font("monob", 10), fill=RED)
    d.text((x0, y0 + 100), "two-fifths gone", font=font("mono", 10), fill=BLACK)
    save(im, 3)

# ------------------------------------------------------------ 4  The mouse patent, redrawn
def patent():
    im = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(im); d.fontmode = "1"
    sb, mo, it = font("serifb", 14), font("mono", 10), font("ital", 13)
    d.text((10, 8), "Nov. 17, 1970", font=sb, fill=BLACK)
    t = "D. C. ENGELBART"; d.text((200 - d.textlength(t, font=sb)/2, 8), t, font=sb, fill=BLACK)
    t = "3,541,541"; d.text((390 - d.textlength(t, font=sb), 8), t, font=sb, fill=BLACK)
    t = "X-Y POSITION INDICATOR FOR A DISPLAY SYSTEM"; d.text((200 - 3*len(t), 28), t, font=mo, fill=BLACK)
    t = "Filed June 21, 1967"; d.text((200 - 3*len(t), 41), t, font=mo, fill=BLACK)
    d.line([(10, 57), (390, 57)], fill=BLACK)
    # FIG. 1: the box, oblique
    ox, oy, k = 34, 216, 30.0
    Lx, Dy, Hz = 3.5, 2.6, 1.5
    P = lambda x, y, z: (ox + k*(x + 0.46*y), oy - k*(z + 0.30*y))
    # wheels showing under the box
    wx, wy = P(0.9, 0, 0); d.ellipse([wx-17, wy-23, wx+17, wy+11], fill=WHITE, outline=BLACK, width=2)
    for r in (11, 4): d.ellipse([wx-r, wy-6-r, wx+r, wy-6+r], outline=BLACK)
    vx, vy = P(2.7, 0.5, 0); d.ellipse([vx-4, vy-22, vx+4, vy+11], fill=BLACK)
    front = [P(0, 0, 0), P(Lx, 0, 0), P(Lx, 0, Hz), P(0, 0, Hz)]
    side = [P(Lx, 0, 0), P(Lx, Dy, 0), P(Lx, Dy, Hz), P(Lx, 0, Hz)]
    top = [P(0, 0, Hz), P(Lx, 0, Hz), P(Lx, Dy, Hz), P(0, Dy, Hz)]
    # cord, drawn first so the box hides its start
    c0 = P(2.2, Dy, Hz*0.6); cord = []
    for i in range(60):
        t = i/59; cord.append((c0[0] + 62*t + 9*math.sin(t*7), c0[1] - 58*t - 26*math.sin(t*math.pi)*(1 - t)))
    d.line(cord, fill=BLACK, width=3); d.line(cord, fill=WHITE, width=1)
    for poly in (front, side, top): d.polygon(poly, fill=WHITE, outline=BLACK)
    for poly in (front, side, top): d.line(poly + poly[:1], fill=BLACK, width=2)
    for i in range(1, 12):                                  # shade lines on the end face
        a = P(Lx, Dy*i/12, 0); b = P(Lx, Dy*i/12, Hz); d.line([a, b], fill=BLACK)
    for z in (0.3, 0.42, 0.9, 1.06):                        # a little grain on the front
        d.line([P(0.2, 0, z), P(Lx*0.55 + z, 0, z)], fill=BLACK)
    bt = [P(0.5, 1.5, Hz), P(1.2, 1.5, Hz), P(1.2, 2.1, Hz), P(0.5, 2.1, Hz)]      # the one button
    up = [(x, y - 5) for x, y in bt]
    d.polygon([bt[0], bt[1], up[1], up[0]], fill=BLACK); d.polygon([bt[1], bt[2], up[2], up[1]], fill=BLACK)
    d.polygon(up, fill=WHITE, outline=BLACK)
    def lead(p, q, n):
        mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2; dx, dy = q[0]-p[0], q[1]-p[1]; L = math.hypot(dx, dy)
        pts = [(p[0] + dx*t + (-dy/L)*4*math.sin(t*2*math.pi), p[1] + dy*t + (dx/L)*4*math.sin(t*2*math.pi))
               for t in [i/20 for i in range(21)]]
        d.line(pts, fill=BLACK)
        d.text((q[0] - 6 + (8 if dx > 0 else -8)*(abs(dx) > abs(dy)), q[1] - 6 + (9 if dy > 0 else -9)*(abs(dy) >= abs(dx))),
               n, font=mo, fill=BLACK)
    lead(P(0.9, 0.3, Hz), (40, 84), "10"); lead((up[0][0] + 12, up[0][1] + 4), (96, 72), "12")
    lead((wx - 6, wy + 9), (22, 248), "14"); lead((vx, vy + 10), (150, 252), "16"); lead(cord[40], (236, 150), "18")
    d.text((78, 256), "FIG. 1", font=font("serifb", 13), fill=BLACK)
    # FIG. 2: from underneath
    x0, y0, x1, y1 = 262, 92, 378, 178
    d.rectangle([x0, y0, x1, y1], outline=BLACK, width=2)
    d.rectangle([x0 + 20, y0 + 22, x0 + 25, y0 + 64], fill=BLACK)                  # wheel 14
    d.line([(x0 + 25, y0 + 43), (x0 + 50, y0 + 43)], fill=BLACK, width=2)
    d.ellipse([x0 + 50, y0 + 32, x0 + 72, y0 + 54], outline=BLACK, width=2); d.ellipse([x0 + 59, y0 + 41, x0 + 63, y0 + 45], fill=BLACK)
    d.rectangle([x0 + 62, y0 + 66, x0 + 104, y0 + 71], fill=BLACK)                 # wheel 16
    d.line([(x0 + 83, y0 + 66), (x0 + 83, y0 + 36)], fill=BLACK, width=2)
    d.ellipse([x0 + 72, y0 + 14, x0 + 94, y0 + 36], outline=BLACK, width=2); d.ellipse([x0 + 81, y0 + 23, x0 + 85, y0 + 27], fill=BLACK)
    lead((x0 + 22, y0 + 60), (x0 - 12, y1 + 22), "14"); lead((x0 + 100, y0 + 71), (x1 - 4, y1 + 22), "16")
    lead((x0 + 61, y0 + 33), (x0 + 30, y0 - 12), "20"); lead((x0 + 92, y0 + 18), (x1 + 4, y0 - 12), "22")
    d.text((x0 + 36, y1 + 28), "FIG. 2", font=font("serifb", 13), fill=BLACK)
    for xa in range(x0 + 4, x0 + 112, 8): d.line([(xa, y1 + 52), (xa + 4, y1 + 52)], fill=BLACK)
    d.text((x0 + 4, y1 + 56), "two wheels,", font=mo, fill=BLACK); d.text((x0 + 4, y1 + 68), "at right angles", font=mo, fill=BLACK)
    t = "Nowhere does the patent say \"mouse\"."
    d.text((10, 276), t, font=font("ital", 15), fill=BLACK)
    # the thing it made possible
    cur = [(0, 0), (0, 16), (4, 12), (7, 19), (9.5, 18), (6.5, 11), (11.5, 11)]; cs = 2.6; cx0, cy0 = 166, 96
    pts = [(cx0 + x*cs, cy0 + y*cs) for x, y in cur]
    d.polygon(pts, fill=RED); d.line(pts + pts[:1], fill=WHITE, width=4); d.polygon(pts, fill=RED)
    d.line(pts + pts[:1], fill=BLACK, width=1)
    save(im, 4)

# ------------------------------------------------------------ 5  Keys held up (Prague, November 1989)
def keys():
    rng = np.random.default_rng(1989); k = 3
    occ = np.zeros((H, W), bool); out = np.zeros((H, W), np.uint8)       # 0 black, 1 white, 2 red
    def make(kind):
        S = 96*k; m = Image.new("L", (S, S), 0); d = ImageDraw.Draw(m); c = S/2
        if kind == 0:                                   # cylinder key: flat bow, cut blade
            r = rng.uniform(9, 11)*k; by = c + 20*k
            if rng.random() < 0.5: d.ellipse([c-r, by-r, c+r, by+r], fill=255)
            else: d.rounded_rectangle([c-r, by-r*0.85, c+r, by+r*0.85], radius=4*k, fill=255)
            d.ellipse([c-2.6*k, by+r*0.35-2.6*k, c+2.6*k, by+r*0.35+2.6*k], fill=0)
            top = c - rng.uniform(26, 32)*k; bw = 3.2*k
            cuts = [(c + bw, by - r*0.8)]; y = by - r - 2*k
            while y > top + 5*k:
                cuts.append((c + bw - rng.uniform(0.2, 2.6)*k, y)); y -= rng.uniform(2.2, 3.6)*k
            d.polygon([(c - bw, by - r*0.8), (c - bw, top + 3*k), (c - bw + 2.5*k, top)] + cuts[::-1], fill=255)
            d.line([(c - 0.6*k, by - r), (c - 0.6*k, top + 5*k)], fill=0, width=max(2, k - 1))
        else:                                           # lever key: ring bow, stem, bit
            rx, ry = rng.uniform(7, 9)*k, rng.uniform(8, 11)*k; by = c + 22*k
            d.ellipse([c-rx, by-ry, c+rx, by+ry], fill=255); d.ellipse([c-rx+3*k, by-ry+3*k, c+rx-3*k, by+ry-3*k], fill=0)
            top = c - rng.uniform(28, 34)*k
            d.rectangle([c-1.5*k, top, c+1.5*k, by-ry+k], fill=255)
            d.rectangle([c-3*k, by-ry-3*k, c+3*k, by-ry-1*k], fill=255)
            bh, bwid = rng.uniform(9, 12)*k, rng.uniform(7, 9)*k
            d.rectangle([c, top + k, c + bwid, top + k + bh], fill=255)
            for _ in range(int(rng.integers(1, 3))):
                yy = top + k + rng.uniform(2, bh/k - 3)*k; d.rectangle([c + bwid - rng.uniform(2.5, 5)*k, yy, c + bwid, yy + 2*k], fill=0)
        if rng.random() < 0.5: m = m.transpose(Image.FLIP_LEFT_RIGHT)
        m = m.rotate(rng.uniform(-38, 38), resample=Image.BICUBIC)
        return np.asarray(m.resize((96, 96), Image.LANCZOS)) > 120
    placed = 0
    for attempt in range(4000):
        m = make(int(rng.random() < 0.38))
        fat = np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
        for _ in range(12):
            x = int(rng.integers(-30, W - 66)); y = int(rng.integers(-30, H - 66))
            xs, ys = max(0, x), max(0, y); xe, ye = min(W, x + 96), min(H, y + 96)
            sub = (slice(ys - y, ye - y), slice(xs - x, xe - x)); dst = (slice(ys, ye), slice(xs, xe))
            if not (occ[dst] & fat[sub]).any():
                occ[dst] |= fat[sub]; out[dst][m[sub]] = 2 if placed % 3 == 1 else 1; placed += 1; break
        if placed >= 70: break
    col = np.array([BLACK, WHITE, RED], np.uint8)[out]
    save(Image.fromarray(col, "RGB"), 5)

if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2", "3", "4", "5"]
    for n, fn in zip("12345", (tracks, moebius, suez, patent, keys)):
        if n in which: fn()
