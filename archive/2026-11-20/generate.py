#!/usr/bin/env python3
"""2026-11-20 (Friday). Theme: readings.  Run from the repo root.
1 Waggle (von Frisch, b. 1886)   2 Asterisks (Mandelbrot, b. 1924; Brooks & Matelski 1978)
3 6:05 (Astapovo, 1910)   4 VAR! (Hubble, b. 1889)   5 Zarya (1998)"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, S = 400, 300, 3
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = ["images", "archive/2026-11-20"]
F = "/usr/share/fonts/truetype/"
def font(name, size):
    paths = {"mono": F+"dejavu/DejaVuSansMono.ttf", "monob": F+"dejavu/DejaVuSansMono-Bold.ttf",
             "sansb": F+"dejavu/DejaVuSans-Bold.ttf",
             "ital": F+"liberation/LiberationSerif-Italic.ttf",
             "serifb": F+"liberation/LiberationSerif-Bold.ttf",
             "black": "/usr/share/fonts/opentype/inter/Inter-Black.otf"}
    return ImageFont.truetype(paths[name], size)
def save(im, n):
    pal = Image.new("P", (1, 1)); pal.putpalette([0,0,0, 255,255,255, 255,0,0] + [0,0,0]*253)
    q = im.convert("RGB").quantize(palette=pal, dither=Image.Dither.NONE)
    for o in OUT:
        os.makedirs(o, exist_ok=True); q.save(f"{o}/{n}.png")
def down(big):
    """3x RGB -> 1x, every pixel snapped to the nearest ink."""
    a = np.asarray(big.resize((W, H), Image.LANCZOS)).astype(int)
    inks = np.array([BLACK, WHITE, RED])
    idx = ((a[:, :, None, :] - inks[None, None])**2).sum(-1).argmin(-1)
    return Image.fromarray(inks[idx].astype(np.uint8), "RGB")
def crisp(im):
    d = ImageDraw.Draw(im); d.fontmode = "1"; return d
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
def ell(cx, cy, a, b, n=60, t0=0, t1=2*math.pi):
    return [(cx + a*math.cos(t0 + (t1-t0)*i/n), cy + b*math.sin(t0 + (t1-t0)*i/n)) for i in range(n+1)]

# ------------------------------------------------------------ 1  Waggle: the dance, read by von Frisch
def waggle():
    ANG = math.radians(40)
    fwd = (math.sin(ANG), -math.cos(ANG)); prp = (math.cos(ANG), math.sin(ANG))
    C = (150, 152)
    def P(u, v, s=S):                       # dance coords (u along the run, v to its right) -> canvas
        return ((C[0] + u*fwd[0] + v*prp[0])*s, (C[1] + u*fwd[1] + v*prp[1])*s)
    im = Image.new("RGB", (W*S, H*S), WHITE); d = ImageDraw.Draw(im)
    # comb: dotted hexagons at 1x so they stay a quiet grey
    comb = Image.new("RGB", (W, H), WHITE); cd = ImageDraw.Draw(comb)
    r = 13; dx = r*math.sqrt(3); row = 0; y = -r
    while y < H + r:
        x = -dx + (dx/2 if row % 2 else 0)
        while x < 290:
            cd.polygon([(x + r*math.sin(k*math.pi/3), y + r*math.cos(k*math.pi/3)) for k in range(6)], outline=BLACK)
            x += dx
        y += 1.5*r; row += 1
    ca = np.asarray(comb).copy(); yy, xx = np.mgrid[0:H, 0:W]
    ca[(xx + yy) % 2 == 1] = 255; ca[:, 281:] = 255
    im.paste(Image.fromarray(ca).resize((W*S, H*S), Image.NEAREST))
    # return loops (dashed), then the waggle run
    L, RV = 95, 62
    for side in (1, -1):
        pts = [P(L*math.cos(t), side*RV*math.sin(t)) for t in np.linspace(0, math.pi, 90)]
        d.line(pts, fill=WHITE, width=9*S//3*3)
        for i in range(2, 86, 6):
            d.line(pts[i:i+4], fill=BLACK, width=2*S)
        for i in (30, 62):                                         # arrowheads: back toward the start
            (x0, y0), (x1, y1) = pts[i], pts[i+3]; a = math.atan2(y1-y0, x1-x0)
            d.polygon([(x1 + 9*S*math.cos(a), y1 + 9*S*math.sin(a)),
                       (x1 + 6*S*math.cos(a+2.4), y1 + 6*S*math.sin(a+2.4)),
                       (x1 + 6*S*math.cos(a-2.4), y1 + 6*S*math.sin(a-2.4))], fill=BLACK)
    s0 = P(-L, 0)
    d.line([s0, (s0[0], s0[1] - 150*S)], fill=WHITE, width=5*S)
    for k in range(0, 150, 8):
        d.line([(s0[0], s0[1] - k*S), (s0[0], s0[1] - (k+4)*S)], fill=BLACK, width=S)
    d.arc([s0[0]-46*S, s0[1]-46*S, s0[0]+46*S, s0[1]+46*S], 270, 310, fill=BLACK, width=S)
    zig = [P(u, 7*(1 if i % 2 else -1)) for i, u in enumerate(np.linspace(-L, 8, 22))]
    d.line(zig, fill=WHITE, width=9*S); d.line(zig, fill=RED, width=3*S, joint="curve")
    # the bee, head at +u
    B = 46
    def bp(pts): return [P(B + u, v) for u, v in pts]
    for sgn in (1, -1):                                            # legs
        for u0, sw, ln in ((16, 0.9, 20), (8, 0.1, 22), (2, -0.8, 26)):
            k = (u0 + 9*math.cos(sw)*0 + sw*8, sgn*(14 + 4))
            f = (u0 + sw*20, sgn*(14 + ln*0.75))
            d.line(bp([(u0, sgn*6), k, f]), fill=BLACK, width=2*S, joint="curve")
            d.line(bp([f, (f[0] + (3 if sw > 0 else -3), f[1] + sgn*3)]), fill=BLACK, width=S)
    for sgn in (1, -1):                                            # waggle marks beside the abdomen
        for k, rr in enumerate((24, 30, 36)):
            d.line(bp([(-26 + rr*0.55*math.cos(t), sgn*rr*math.sin(t)) for t in np.linspace(1.15, 1.95, 12)]),
                   fill=BLACK, width=S)
    abd = [(-6 - 46*t, w) for t, w in [(i/30, 13.5*math.sin(math.pi*(i/30)**0.62)) for i in range(31)]]
    outline = abd + [(u, -v) for u, v in abd[::-1]]
    d.polygon(bp(outline), fill=WHITE)
    for k in range(6):                                             # stripes
        t0, t1 = 0.10 + k*0.15, 0.10 + k*0.15 + 0.085
        seg = [(-6 - 46*t, 13.5*math.sin(math.pi*t**0.62)) for t in np.linspace(t0, min(t1, 1), 6)]
        d.polygon(bp(seg + [(u, -v) for u, v in seg[::-1]]), fill=BLACK)
    d.line(bp(outline + outline[:1]), fill=BLACK, width=2*S)
    for sgn in (1, -1):                                            # wings, drawn over the abdomen
        for ln, wd, a in ((50, 10, 0.30), (34, 8, 0.62)):
            ca_, sa_ = math.cos(a), math.sin(a)
            wing = []
            for t in np.linspace(0, 2*math.pi, 40):
                lu = ln/2 - ln/2*math.cos(t); lv = wd*math.sin(t)*(0.55 + 0.45*lu/ln)
                wing.append((4 - lu*ca_ + lv*sa_, sgn*(5 + lu*sa_ + lv*ca_)))
            d.polygon(bp(wing), fill=WHITE); d.line(bp(wing), fill=BLACK, width=S)
            d.line(bp([(4, sgn*5), (4 - ln*0.8*ca_, sgn*(5 + ln*0.8*sa_))]), fill=BLACK, width=S)
            d.line(bp([(4 - ln*0.35*ca_, sgn*(5 + ln*0.35*sa_)),
                       (4 - ln*0.7*ca_ + wd*0.6*sa_, sgn*(5 + ln*0.7*sa_ + wd*0.6*ca_))]), fill=BLACK, width=S)
    rng = np.random.default_rng(1886)
    th = [(8 + (11.5 + rng.uniform(-1.2, 1.6))*math.cos(t), (11 + rng.uniform(-1.2, 1.6))*math.sin(t))
          for t in np.linspace(0, 2*math.pi, 70)]
    d.polygon(bp(th), fill=BLACK)                                  # furry thorax
    d.polygon(bp(ell(23, 0, 6.5, 9)), fill=BLACK)                  # head
    for sgn in (1, -1):
        d.polygon(bp(ell(24, sgn*6.5, 4, 3.2)), fill=WHITE); d.polygon(bp(ell(24.5, sgn*6.8, 2.6, 2)), fill=BLACK)
        d.line(bp([(28, sgn*3), (35, sgn*6), (44, sgn*13)]), fill=BLACK, width=int(1.5*S), joint="curve")
    # the little map: hive, sun, food
    hx, hy = 322*S, 122*S
    d.line([(hx, hy), (hx, hy - 78*S)], fill=BLACK, width=S)
    fx, fy = hx + 92*math.sin(ANG)*S, hy - 92*math.cos(ANG)*S
    d.line([(hx, hy), (fx, fy)], fill=RED, width=2*S)
    d.arc([hx-34*S, hy-34*S, hx+34*S, hy+34*S], 270, 310, fill=BLACK, width=S)
    sx, sy = hx, hy - 92*S
    d.ellipse([sx-8*S, sy-8*S, sx+8*S, sy+8*S], fill=WHITE, outline=BLACK, width=2*S)
    for k in range(12):
        a = k*math.pi/6
        d.line([(sx + 11*S*math.cos(a), sy + 11*S*math.sin(a)), (sx + 15*S*math.cos(a), sy + 15*S*math.sin(a))],
               fill=BLACK, width=S)
    for k in range(6):
        a = k*math.pi/3
        d.ellipse([fx + 5*S*math.cos(a) - 3.4*S, fy + 5*S*math.sin(a) - 3.4*S,
                   fx + 5*S*math.cos(a) + 3.4*S, fy + 5*S*math.sin(a) + 3.4*S], fill=RED)
    d.ellipse([fx-2.5*S, fy-2.5*S, fx+2.5*S, fy+2.5*S], fill=WHITE)
    d.rectangle([hx-9*S, hy-3*S, hx+9*S, hy+11*S], fill=BLACK)
    d.rectangle([hx-11*S, hy-6*S, hx+11*S, hy-3*S], fill=BLACK)
    d.rectangle([hx-3*S, hy+6*S, hx+3*S, hy+8*S], fill=WHITE)
    d.line([(284*S, 0), (284*S, H*S)], fill=BLACK, width=2*S)
    im = down(im); t = crisp(im); m, mb = font("mono", 10), font("monob", 10)
    t.text((s0[0]/S + 9, s0[1]/S - 66), "40°", font=mb, fill=BLACK)
    t.text((s0[0]/S - 8, s0[1]/S - 164 + 2), "up", font=m, fill=BLACK)
    t.text((330, 78), "40°", font=mb, fill=BLACK)
    t.text((296, 46), "sun", font=m, fill=BLACK); t.text((362, 22), "food", font=m, fill=RED)
    t.text((338, 124), "hive", font=m, fill=BLACK)
    for i, s in enumerate(["In the dark, on", "the hanging", "comb, straight", "up stands for", "the sun.", "",
                           "Longer waggle,", "farther food:", "roughly a", "second for", "each kilometre."]):
        t.text((294, 148 + i*11), s, font=m, fill=BLACK)
    t.text((294, 274), "K. von Frisch", font=mb, fill=BLACK); t.text((294, 285), "b. 20 Nov 1886", font=m, fill=BLACK)
    save(im, 1)

# ------------------------------------------------------------ 2  Asterisks: the set as a line-printer saw it
def asterisks():
    im = Image.new("RGB", (W, H), RED); t = crisp(im)
    fb, m, mb = font("monob", 11), font("mono", 10), font("monob", 10)
    cols, rows, cw, rh = 62, 33, 6, 8
    x0 = (W - cols*cw)//2
    for j in range(rows):
        ci = (j - rows//2)*(-0.0625)
        for i in range(cols):
            c = complex(-2.05 + i*0.0455, ci); z = 0j; inside = True
            for _ in range(300):
                z = z*z + c
                if abs(z) > 2: inside = False; break
            if inside:
                t.text((x0 + i*cw, 3 + j*rh - 1), "*", font=fb, fill=WHITE)
    t.text((14, 271), "z -> z*z + c", font=mb, fill=BLACK)
    t.text((14, 284), "First printed, in asterisks, by Brooks & Matelski, 1978.", font=m, fill=WHITE)
    s = "B. Mandelbrot, b. 20 Nov 1924"
    t.text((W - 14 - t.textlength(s, font=m), 271), s, font=m, fill=WHITE)
    save(im, 2)

# ------------------------------------------------------------ 3  6:05: the station clock at Astapovo
def clock():
    rng = np.random.default_rng(1910)
    im = Image.new("RGB", (W*S, H*S), BLACK); d = ImageDraw.Draw(im)
    cx, cy, R = 200*S, 120*S, 90*S
    d.rectangle([cx-3*S, 0, cx+3*S, cy-R], fill=WHITE)
    d.rectangle([cx-9*S, cy-R-9*S, cx+9*S, cy-R+2*S], fill=WHITE)
    d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=WHITE)
    d.ellipse([cx-R+3*S, cy-R+3*S, cx+R-3*S, cy+R-3*S], outline=BLACK, width=5*S)
    d.ellipse([cx-R+11*S, cy-R+11*S, cx+R-11*S, cy+R-11*S], outline=BLACK, width=S)
    for k in range(60):
        a = k*math.pi/30; r0 = R - (20*S if k % 5 == 0 else 16*S)
        d.line([(cx + r0*math.sin(a), cy - r0*math.cos(a)), (cx + (R-12*S)*math.sin(a), cy - (R-12*S)*math.cos(a))],
               fill=BLACK, width=(3*S if k % 5 == 0 else S))
    d.rectangle([104*S, 226*S, 296*S, 256*S], fill=WHITE)
    d.rectangle([107*S, 229*S, 293*S, 253*S], outline=BLACK, width=S)
    d.text((200*S, 241*S), "АСТАПОВО", font=font("black", 20*S), fill=RED, anchor="mm")
    im = down(im); a = np.asarray(im).copy()
    yy, xx = np.mgrid[0:H, 0:W]; dist = np.hypot(xx - 200, yy - 120)
    p = 0.0035 + 0.075*np.exp(-np.maximum(dist - 96, 0)/38)       # snow, thick where the lamp reaches
    flakes = (rng.random((H, W)) < p) & (a.sum(-1) == 0) & (yy < 264) & (dist > 95)
    big = flakes & (rng.random((H, W)) < 0.35*np.exp(-np.maximum(dist - 90, 0)/60))
    flakes |= np.roll(big, 1, 1) | np.roll(big, 1, 0)
    flakes &= (a.sum(-1) == 0) & (yy < 264) & (dist > 95)
    a[flakes] = 255
    im = Image.fromarray(a); t = crisp(im); m = font("mono", 10)
    f = font("serifb", 17)
    for k, s in enumerate(["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]):
        an = k*math.pi/6
        t.text((200 + 57*math.sin(an), 120 - 57*math.cos(an)), s, font=f, fill=BLACK, anchor="mm")
    hd = Image.new("L", (W*S, H*S), 0); d = ImageDraw.Draw(hd)        # hands go over the numerals
    def hand(a_, ln, wd, tail):
        ca, sa = math.sin(a_), -math.cos(a_); px, py = -sa, ca
        pts = [(-tail, wd*0.5), (ln*0.55, wd), (ln*0.72, wd*1.9), (ln, 0), (ln*0.72, -wd*1.9), (ln*0.55, -wd), (-tail, -wd*0.5)]
        d.polygon([(cx + u*ca + v*px, cy + u*sa + v*py) for u, v in pts], fill=255)
    hand(math.radians(6*30 + 5*0.5), 46*S, 3.2*S, 10*S); hand(math.radians(30), 70*S, 2.2*S, 14*S)
    d.ellipse([cx-6*S, cy-6*S, cx+6*S, cy+6*S], fill=255)
    hm = np.asarray(hd.resize((W, H), Image.LANCZOS)); a = np.asarray(im).copy()
    a[np.asarray(Image.fromarray(hm).filter(ImageFilter.MaxFilter(3))) > 100] = 255; a[hm > 120] = 0
    a[119:122, 199:202] = 255
    im = Image.fromarray(a); t = crisp(im)
    s = "6:05 a.m., 7 (20) November 1910. Leo Tolstoy, 82,"
    t.text(((W - t.textlength(s, font=m))//2, 270), s, font=m, fill=WHITE)
    s = "in the stationmaster's house."
    t.text(((W - t.textlength(s, font=m))//2, 283), s, font=m, fill=WHITE)
    save(im, 3)

# ------------------------------------------------------------ 4  VAR!: a negative plate of M31
def var():
    rng = np.random.default_rng(335)
    X0, Y0, X1, Y1 = 8, 8, 392, 268
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    gx, gy, pa = 150.0, 168.0, math.radians(-33)
    u = (xx - gx)*math.cos(pa) + (yy - gy)*math.sin(pa); v = -(xx - gx)*math.sin(pa) + (yy - gy)*math.cos(pa)
    r = np.hypot(u, v/0.30); th = np.arctan2(v/0.30, u)
    arms = 0.62 + 0.38*np.sin(2*th - 4.6*np.log(r + 6))
    lane = 1 - 0.55*np.exp(-((v - 7 - 0.04*np.abs(u))/3.0)**2)*np.exp(-r/120)
    T = 1.6*np.exp(-np.hypot(u, v/0.62)/11) + 1.0*np.exp(-r/105)*arms*lane
    for sx, sy, a, q in ((178, 196, 5.0, 0.8), (88, 92, 11.0, 0.55)):          # M32 and M110
        T += 0.9*np.exp(-np.hypot(xx - sx, (yy - sy)/q)/a)
    edge = np.minimum.reduce([xx - X0, X1 - xx, yy - Y0, Y1 - yy])
    T += 0.015 + 0.16*np.exp(-edge/9)                                         # fog toward the plate edge
    T *= 0.8 + 0.4*rng.random((H, W))
    ns = 420; sx = rng.uniform(X0, X1, ns); sy = rng.uniform(Y0, Y1, ns); sm = rng.pareto(1.6, ns)
    ink = rng.random((H, W)) < np.clip(T, 0, 0.97)**1.15           # silver grain
    ink &= (xx >= X0) & (xx <= X1) & (yy >= Y0) & (yy <= Y1)
    im = Image.fromarray(np.where(ink[..., None], 0, 255).astype(np.uint8).repeat(3, 2), "RGB")
    big = Image.new("L", (W*S, H*S), 0); bd = ImageDraw.Draw(big)
    for x, y, mag in zip(sx, sy, sm):
        rr = min(0.45 + 0.42*mag, 3.4)
        bd.ellipse([(x-rr)*S, (y-rr)*S, (x+rr)*S, (y+rr)*S], fill=255)
    marked = [(301, 88), (236, 58), (330, 150)]
    for x, y in marked:
        bd.ellipse([(x-1.3)*S, (y-1.3)*S, (x+1.3)*S, (y+1.3)*S], fill=255)
    stars = np.asarray(big.resize((W, H), Image.LANCZOS)) > 120
    a = np.asarray(im).copy(); a[stars] = 0
    im = Image.fromarray(a)
    # ink annotations, by hand
    hb = Image.new("L", (W*S, H*S), 0); hr = Image.new("L", (W*S, H*S), 0)
    def write(layer, strokes, x, y, h, wd=2.0, slant=0.12, seed=0):
        g = np.random.default_rng(seed); dd = ImageDraw.Draw(layer)
        for st in strokes:
            pts = [((x + (px + (1-py)*slant)*h + g.normal(0, 0.5))*S, (y + py*h + g.normal(0, 0.5))*S) for px, py in st]
            dd.line(pts, fill=255, width=int(wd*S), joint="curve")
            for q in (pts[0], pts[-1]):
                dd.ellipse([q[0]-wd*S/2, q[1]-wd*S/2, q[0]+wd*S/2, q[1]+wd*S/2], fill=255)
    N = [[(0, 1), (0.02, 0), (0.55, 1), (0.6, 0)]]
    Vv = [[(0, 0), (0.3, 1), (0.62, 0)]]
    A = [[(0.85, 1), (1.18, 0), (1.5, 1)], [(0.98, 0.62), (1.4, 0.62)]]
    Rr = [[(1.75, 1), (1.75, 0), (2.1, 0.02), (2.25, 0.25), (2.1, 0.47), (1.75, 0.5)], [(1.95, 0.5), (2.3, 1)]]
    EX = [[(2.62, 0), (2.6, 0.68)], [(2.59, 0.97), (2.6, 1.0)]]
    def ticks(layer, x, y):
        dd = ImageDraw.Draw(layer)
        dd.line([((x-9)*S, y*S), ((x-4)*S, y*S)], fill=255, width=S+1)
        dd.line([(x*S, (y+4)*S), (x*S, (y+9)*S)], fill=255, width=S+1)
    for x, y in marked: ticks(hb, x, y)
    write(hb, N, 243, 40, 13, 1.6, seed=1); write(hb, N, 338, 133, 13, 1.6, seed=2)
    write(hb, N, 309, 70, 13, 1.6, seed=3)
    hx = Image.new("L", (W*S, H*S), 0)
    write(hx, [[(-0.3, 0.95), (0.9, 0.05)]], 309, 70, 13, 1.3, slant=0, seed=4)
    write(hr, Vv + A + Rr + EX, 322, 42, 24, 2.6, seed=5)
    a = np.asarray(im).copy()
    for layer, col in ((hb, BLACK), (hx, RED), (hr, RED)):
        mk = np.asarray(layer.resize((W, H), Image.LANCZOS)) > 110
        if layer is hr:
            moat = np.asarray(layer.resize((W, H), Image.LANCZOS).filter(ImageFilter.MaxFilter(3))) > 60
            a[moat] = 255
        a[mk] = col
    im = Image.fromarray(a); t = crisp(im)
    t.rectangle([X0, Y0, X1, Y1], outline=BLACK)
    m, mb = font("mono", 10), font("monob", 10)
    t.text((8, 273), "Plate H335H, Mount Wilson 100-inch, 5-6 Oct 1923.", font=m, fill=BLACK)
    t.text((8, 285), "The nova that wasn't.", font=m, fill=BLACK)
    s = "Edwin Hubble, b. 20 Nov 1889"
    t.text((W - 8 - t.textlength(s, font=mb), 285), s, font=mb, fill=BLACK)
    save(im, 4)

# ------------------------------------------------------------ 5  Zarya: "dawn", sixteen times a day
def zarya():
    rng = np.random.default_rng(1998)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    ex, ey, ER = 215.0, 1108.0, 900.0
    dl = np.hypot(xx - ex, yy - ey) - ER                 # height above the limb, px
    sunx = 118.0; suny = ey - math.sqrt(ER**2 - (sunx - ex)**2)
    ds = np.hypot(xx - sunx, yy - suny)
    G = 1.15*np.exp(-ds/26) + 0.55*np.exp(-np.maximum(dl, 0)/5.5)*np.exp(-np.abs(xx - sunx)/95)
    G[dl < 0] = 0
    lit = rng.random((H, W)) < np.clip(G, 0, 1)**1.3
    a = np.zeros((H, W, 3), np.uint8); a[lit] = 255
    stars = (rng.random((H, W)) < 0.0022) & (dl > 6) & (G < 0.04)
    a[stars] = 255
    band = 1.0 + 6.5*np.exp(-((xx - sunx)/85)**2)        # the red line of air, thickest at the sun
    a[(dl >= -band) & (dl < 0.6)] = RED
    a[(dl >= 0.6) & (dl < 0.6 + 0.35*band) & (np.abs(xx - sunx) < 120)] = 255
    im = Image.fromarray(a).resize((W*S, H*S), Image.NEAREST); d = ImageDraw.Draw(im)
    for k in range(16):                                  # rays
        an = -math.pi*(k + 0.5)/16; ln = (58 if k % 2 == 0 else 34)
        d.line([((sunx + 13*math.cos(an))*S, (suny + 13*math.sin(an))*S),
                ((sunx + ln*math.cos(an))*S, (suny + ln*math.sin(an))*S)], fill=WHITE, width=S)
    d.pieslice([(sunx-9)*S, (suny-9)*S, (sunx+9)*S, (suny+9)*S], 180, 360, fill=WHITE)
    # the module, side on: 12.56 m long, arrays 10.67 m each way; 5 px to the metre
    k = 5.0*S; mx, my = 262*S, 84*S; tilt = math.radians(-8)
    def Q(u, v): return (mx + (u*math.cos(tilt) - v*math.sin(tilt))*k, my + (u*math.sin(tilt) + v*math.cos(tilt))*k)
    body = [(-6.28, -1.0), (-5.2, -1.45), (-0.4, -1.45), (0.4, -2.05), (4.2, -2.05), (4.9, -1.2), (5.6, -1.0),
            (6.28, -0.75), (6.28, 0.75), (5.6, 1.0), (4.9, 1.2), (4.2, 2.05), (0.4, 2.05), (-0.4, 1.45),
            (-5.2, 1.45), (-6.28, 1.0)]
    for sgn in (1, -1):
        d.line([Q(1.6, sgn*2.05), Q(1.6, sgn*3.0)], fill=WHITE, width=S)
        pan = [Q(-0.1, sgn*3.0), Q(3.3, sgn*3.0), Q(3.3, sgn*13.6), Q(-0.1, sgn*13.6)]
        d.polygon(pan, fill=BLACK); d.line(pan + pan[:1], fill=WHITE, width=S)
        for j in range(1, 8):
            vv = sgn*(3.0 + j*10.6/8); d.line([Q(-0.1, vv), Q(3.3, vv)], fill=WHITE, width=S)
        d.line([Q(1.6, sgn*3.0), Q(1.6, sgn*13.6)], fill=WHITE, width=S)
    d.polygon([Q(*p) for p in body], fill=WHITE)
    for u in (-5.2, -0.4, 0.4, 4.2):
        d.line([Q(u, -1.3), Q(u, 1.3)], fill=BLACK, width=S)
    d.text((24*S, 264*S), "ЗАРЯ", font=font("black", 30*S), fill=WHITE, anchor="ls")
    im = down(im); t = crisp(im); m, it = font("mono", 10), font("ital", 14)
    t.text((122, 249), "\u201cdawn\u201d", font=it, fill=RED)
    t.text((24, 272), "20 Nov 1998, 06:40 UTC: the first piece of the space", font=m, fill=WHITE)
    t.text((24, 284), "station. About sixteen dawns a day ever since.", font=m, fill=WHITE)
    save(im, 5)

if __name__ == "__main__":
    waggle(); asterisks(); clock(); var(); zarya()
    sheet = Image.new("RGB", (W*2 + 30, H*3 + 40), (128, 128, 128))
    for i in range(5):
        sheet.paste(Image.open(f"images/{i+1}.png").convert("RGB"), (10 + (i % 2)*(W+10), 10 + (i//2)*(H+10)))
    if os.environ.get("SHEET"): sheet.save(os.environ["SHEET"])
