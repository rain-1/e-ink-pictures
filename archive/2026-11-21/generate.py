#!/usr/bin/env python3
"""2026-11-21 (Saturday). Theme: paper.  Run from the repo root.
1 Aloft (Paris, 21 Nov 1783)        2 Découpure (Voltaire, b. 21 Nov 1694)
3 L/V² (Annalen der Physik, 21 Nov 1905)   4 A0 (ISO 216)   5 Bird base (crease pattern)"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, S = 400, 300, 3
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = ["images", "archive/2026-11-21"]
F = "/usr/share/fonts/truetype/"
def font(name, size):
    paths = {"mono": F+"dejavu/DejaVuSansMono.ttf", "monob": F+"dejavu/DejaVuSansMono-Bold.ttf",
             "sansb": F+"dejavu/DejaVuSans-Bold.ttf",
             "ital": F+"liberation/LiberationSerif-Italic.ttf",
             "serif": F+"liberation/LiberationSerif-Regular.ttf",
             "serifb": F+"liberation/LiberationSerif-Bold.ttf",
             "fsital": F+"freefont/FreeSerifItalic.ttf",
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
def vnoise(rng, shape, cells):
    g = rng.random((cells[1] + 1, cells[0] + 1)).astype(np.float32)
    return np.asarray(Image.fromarray(g).resize((shape[1], shape[0]), Image.BICUBIC))
def ctext(d, cx, y, s, f, fill):
    w = d.textlength(s, font=f); d.text((round(cx - w/2), y), s, font=f, fill=fill)

# ------------------------------------------------------------ 1  Aloft: the first people to fly, over Paris
def aloft():
    rng = np.random.default_rng(1783)
    yy, xx = np.mgrid[0:H, 0:W]
    # a thin November overcast, as loose grain; clear round the balloon
    T = 0.55*vnoise(rng, (H, W), (5, 3)) + 0.30*vnoise(rng, (H, W), (11, 7)) + 0.15*vnoise(rng, (H, W), (30, 20))
    T = np.clip((T - 0.42)*1.5, 0, 1)*0.34
    T *= np.clip(1.15 - yy/250, 0.1, 1)
    bx, by, R = 248, 92, 31
    T *= np.clip((np.hypot(xx - bx, yy - by - 20) - 52)/50, 0, 1)
    T += 0.20*np.exp(-((yy - 262)/16.0)**2)                       # haze over the roofs
    a = np.full((H, W, 3), 255, np.uint8)
    a[rng.random((H, W)) < T**1.1] = 0
    im = Image.fromarray(a).resize((W*S, H*S), Image.NEAREST); d = ImageDraw.Draw(im)
    # --- the roofs of Paris, as one black cut-out
    g = np.random.default_rng(21)
    x = -4
    while x < W + 4:
        w = int(g.integers(7, 19)); h = int(g.integers(8, 22))
        top = 300 - 14 - h
        if g.random() < 0.55:                                     # pitched roof
            d.polygon([(x*S, 300*S), (x*S, (top + 7)*S), ((x + w/2)*S, top*S), ((x + w)*S, (top + 7)*S), ((x + w)*S, 300*S)], fill=BLACK)
        else:                                                     # mansard
            d.polygon([(x*S, 300*S), (x*S, (top + 6)*S), ((x + 2)*S, top*S), ((x + w - 2)*S, top*S), ((x + w)*S, (top + 6)*S), ((x + w)*S, 300*S)], fill=BLACK)
        for _ in range(int(g.integers(0, 3))):                    # chimneys
            cx = x + g.integers(1, max(2, w - 2)); d.rectangle([cx*S, (top - 4)*S, (cx + 2)*S, (top + 8)*S], fill=BLACK)
        x += w - 1
    d.rectangle([0, 286*S, W*S, H*S], fill=BLACK)
    # twin towers and flèche
    for tx in (58, 76):
        d.rectangle([tx*S, 244*S, (tx + 12)*S, 300*S], fill=BLACK)
        for k in range(4):
            d.rectangle([(tx + 0.5 + 3*k)*S, 241*S, (tx + 1.8 + 3*k)*S, 245*S], fill=BLACK)
    d.rectangle([88*S, 262*S, 132*S, 300*S], fill=BLACK)
    d.polygon([(107*S, 262*S), (109*S, 232*S), (111*S, 262*S)], fill=BLACK)
    # a dome with a lantern
    dx = 318
    d.rectangle([(dx - 20)*S, 266*S, (dx + 20)*S, 300*S], fill=BLACK)
    d.rectangle([(dx - 13)*S, 256*S, (dx + 13)*S, 268*S], fill=BLACK)
    d.pieslice([(dx - 13)*S, 238*S, (dx + 13)*S, 274*S], 180, 360, fill=BLACK)
    d.rectangle([(dx - 2.5)*S, 230*S, (dx + 2.5)*S, 240*S], fill=BLACK)
    d.polygon([((dx - 2.5)*S, 230*S), (dx*S, 219*S), ((dx + 2.5)*S, 230*S)], fill=BLACK)
    # two windmills on a rise
    d.polygon([(150*S, 300*S), (168*S, 268*S), (214*S, 264*S), (240*S, 300*S)], fill=BLACK)
    for mx, my, rot in ((178, 257, 0.5), (203, 254, 1.1)):
        d.polygon([((mx - 4)*S, (my + 12)*S), ((mx - 3)*S, my*S), (mx*S, (my - 4)*S), ((mx + 3)*S, my*S), ((mx + 4)*S, (my + 12)*S)], fill=BLACK)
        for k in range(4):
            an = rot + k*math.pi/2
            ex, ey = mx + 12*math.cos(an), my - 1 + 12*math.sin(an)
            d.line([(mx*S, (my - 1)*S), (ex*S, ey*S)], fill=BLACK, width=3)
            px, py = -math.sin(an), math.cos(an)
            d.polygon([((mx + 4*math.cos(an))*S, (my - 1 + 4*math.sin(an))*S), (ex*S, ey*S),
                       ((ex + 3*px)*S, (ey + 3*py)*S), ((mx + 4*math.cos(an) + 3*px)*S, (my - 1 + 4*math.sin(an) + 3*py)*S)], fill=BLACK)
    # --- the balloon
    def rad(y):                                   # half-width at height y (y from -R at the crown)
        if y <= 0: return math.sqrt(max(R*R - y*y, 0))
        t = min(y/(1.5*R), 1); return R*(0.40 + 0.60*math.cos(t*math.pi/2)**0.9)
    ys = np.linspace(-R, 1.5*R, 80)
    env = [((bx - rad(y))*S, (by + y)*S) for y in ys] + [((bx + rad(y))*S, (by + y)*S) for y in ys[::-1]]
    d.polygon(env, fill=RED)
    def band(y0, y1, fill):
        yb = np.linspace(y0, y1, 8)
        d.polygon([((bx - rad(y))*S, (by + y)*S) for y in yb] + [((bx + rad(y))*S, (by + y)*S) for y in yb[::-1]], fill=fill)
    band(-3.5, 4.5, WHITE)                                         # the zodiac band
    for k in range(-4, 5):
        px = bx + R*math.sin(k*0.34)
        d.ellipse([(px - 1.4)*S, (by - 1)*S, (px + 1.4)*S, (by + 2)*S], fill=RED)
    band(-R + 5, -R + 7.5, WHITE)                                  # crown ring
    for k in range(-3, 4):                                         # swags under the band
        p0 = bx + R*math.sin((k - 0.5)*0.42); p1 = bx + R*math.sin((k + 0.5)*0.42)
        if abs(k) < 4:
            d.arc([p0*S, (by + 2)*S, p1*S, (by + 2 + 20)*S], 0, 180, fill=WHITE, width=4)
    for k in (-2, -1, 0, 1, 2):                                    # drapery lines down the neck
        d.line([((bx + 0.72*rad(22)*math.sin(k*0.55))*S, (by + 24)*S), ((bx + rad(1.5*R)*math.sin(k*0.55))*S, (by + 1.5*R)*S)], fill=WHITE, width=3)
    # gallery
    gy = by + 1.5*R; gw = rad(1.5*R) + 5
    d.rectangle([(bx - gw)*S, gy*S, (bx + gw)*S, (gy + 5)*S], fill=BLACK)
    for k in range(-3, 4):
        d.line([((bx + k*gw/3.2)*S, gy*S), ((bx + k*gw/3.2)*S, (gy + 5)*S)], fill=WHITE, width=1)
    d.ellipse([(bx - gw - 1.5)*S, (gy - 4)*S, (bx - gw + 1.5)*S, (gy - 1)*S], fill=BLACK)   # two heads at the rail
    d.ellipse([(bx + gw - 1.5)*S, (gy - 4)*S, (bx + gw + 1.5)*S, (gy - 1)*S], fill=BLACK)
    im = down(im)
    # straw smoke, drifting back the way they came (north-west, to the left)
    a = np.asarray(im).copy()
    sm = np.exp(-((yy - (gy + 9 + (bx - xx)*0.10))/(3 + (bx - xx)*0.035))**2)*np.clip((bx - xx)/70, 0, 1)*np.clip(1 - (bx - xx)/190, 0, 1)
    sm[xx > bx - 4] = 0
    a[(rng.random((H, W)) < sm*0.55) & (a.sum(-1) == 765)] = 0
    save(Image.fromarray(a), 1)

# ------------------------------------------------------------ 2  Découpure: Voltaire in cut paper
def decoupure():
    im = Image.new("RGB", (W*S, H*S), BLACK); d = ImageDraw.Draw(im)
    k, ox, oy = 1.86, 18, 6
    def P(x, y): return ((ox + x*k)*S, (oy + y*k)*S)
    prof = [(40,17),(35,24),(32,32),(30.5,39),(29.5,42),(31.5,45),(28,51),(23,58),(18,64),(15,68),(16.5,70.5),(22,71.5),
            (26,72),(27,75),(25.5,77.5),(29.5,79.5),(26,81.5),(28.5,85),(25,88),(21,91.5),(19.5,95.5),(21.5,99.5),
            (27,101.5),(36,99.5),(44,96),(47,105),(46,113),(41,117),(36,123),(35,129),(39,133),(34,140),(28,160),
            (112,160),(108,142),(100,131),(89,123),(78,116),(75,110),(80,106),(87,103),(91,96),(89,88),(85,84),
            (91,76),(94,64),(92,50),(86,36),(76,24),(64,16),(51,13)]
    d.polygon([P(*p) for p in prof], fill=WHITE)
    # wig: scalloped curls along the back, then the scissor-and-needle details cut out in black
    for (cx, cy, r) in [(93,70,5),(94,60,5),(92,50,5),(88,41,5),(83,33,5),(76,25,5),(68,19,5),(59,15,4.5),(50,14,4),(90,79,5),(90,92,5)]:
        d.ellipse([P(cx - r, cy - r)[0], P(cx - r, cy - r)[1], P(cx + r, cy + r)[0], P(cx + r, cy + r)[1]], fill=WHITE)
    def cut(pts, w=2.2):
        d.line([P(*p) for p in pts], fill=BLACK, width=int(w*S), joint="curve")
    # edge of the wig against the brow, temple and ear
    cut([(40,17),(44,24),(46,33),(51,41),(56,50),(57,60),(60,70),(66,78),(74,83),(84,85)], 1.6)
    for (cx, cy, r, a0, a1) in [(70,34,9,200,330),(78,50,9,220,350),(68,54,8,30,160),(80,66,8,230,20),(62,26,7,190,320),(71,68,6,40,170)]:
        d.arc([P(cx - r, cy - r)[0], P(cx - r, cy - r)[1], P(cx + r, cy + r)[0], P(cx + r, cy + r)[1]], a0, a1, fill=BLACK, width=int(1.5*S))
    cut([(79,105),(84,110),(83,117)], 1.6); cut([(76,110),(70,113)], 1.4)       # the ribbon at the nape
    cut([(45,112),(55,117),(68,117),(77,115)], 1.5)                              # collar
    cut([(41,118),(47,124),(44,131),(49,138)], 1.3)                              # jabot folds
    cut([(52,123),(50,133),(54,144),(52,160)], 1.3)                              # coat front
    for by_ in (132, 143, 154):
        d.ellipse([P(57, by_)[0], P(57, by_)[1], P(60.5, by_ + 3.5)[0], P(60.5, by_ + 3.5)[1]], fill=BLACK)
    cut([(88,123),(84,140),(86,160)], 1.3)                                       # sleeve seam
    # --- scissors, open, in red
    def scissors(cx, cy, ang, L=74, open_=0.26):
        for sgn in (1, -1):
            a = ang + sgn*open_
            ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
            tip = (cx + L*ux, cy + L*uy)
            d.polygon([(tip[0]*S, tip[1]*S), ((cx - 6*sgn*vx)*S, (cy - 6*sgn*vy)*S), ((cx - 10*ux)*S, (cy - 10*uy)*S),
                       ((cx + 4*sgn*vx)*S, (cy + 4*sgn*vy)*S)], fill=RED)
            # shank and ring on the far side of the pivot
            hx, hy = cx - 44*ux + 3*sgn*vx, cy - 44*uy + 3*sgn*vy
            d.line([(cx*S, cy*S), ((cx - 30*ux)*S, (cy - 30*uy)*S)], fill=RED, width=5*S)
            d.ellipse([(hx - 13)*S, (hy - 13)*S, (hx + 13)*S, (hy + 13)*S], outline=RED, width=4*S)
        d.ellipse([(cx - 2)*S, (cy - 2)*S, (cx + 2)*S, (cy + 2)*S], fill=BLACK)
    scissors(318, 96, math.radians(152))
    # offcuts on the table
    g = np.random.default_rng(1694)
    for _ in range(11):
        cx, cy = g.uniform(236, 386), g.uniform(160, 212); a0 = g.uniform(0, 6.28); r = g.uniform(5, 12)
        pts = [((cx + r*g.uniform(0.5, 1.2)*math.cos(a0 + j*2.1))*S, (cy + 0.6*r*g.uniform(0.5, 1.2)*math.sin(a0 + j*2.1))*S) for j in range(3)]
        d.polygon(pts, fill=WHITE)
    im = down(im); c = crisp(im)
    c.text((236, 228), "VOLTAIRE", font=font("black", 24), fill=WHITE)
    c.text((237, 258), "born 21 November 1694.", font=font("mono", 10), fill=WHITE)
    c.text((237, 270), "A profile in cut paper,", font=font("mono", 10), fill=WHITE)
    c.text((237, 282), "after Huber of Geneva.", font=font("mono", 10), fill=WHITE)
    save(im, 2)

# ------------------------------------------------------------ 3  L/V²: three pages in the Annalen
def lv2():
    im = Image.new("RGB", (W, H), WHITE); d = crisp(im)
    d.text((14, 10), "639", font=font("serif", 13), fill=BLACK)
    ctext(d, 200, 10, "13.  Ist die Trägheit eines Körpers", font("serifb", 15), BLACK)
    ctext(d, 200, 28, "von seinem Energieinhalt abhängig?", font("serifb", 15), BLACK)
    ctext(d, 200, 48, "von A. Einstein.", font("ital", 13), BLACK)
    d.line([(170, 68), (230, 68)], fill=BLACK)
    # the fraction, set large, in red
    big = font("fsital", 104)
    def glyph(s, f, cx, base):
        l, t, r, b = d.textbbox((0, 0), s, font=f)
        d.text((round(cx - (l + r)/2), base - b), s, font=f, fill=RED)
        return r - l
    glyph("L", big, 196, 142)
    d.rectangle([146, 150, 262, 154], fill=RED)
    wv = glyph("V", big, 190, 228)
    l, t, r, b = d.textbbox((0, 0), "2", font=font("fsital", 46))
    d.text((190 + wv//2 + 6 - l, 160 - t), "2", font=font("fsital", 46), fill=RED)
    it = font("ital", 13)
    d.text((14, 100), "Gibt ein Körper die", font=it, fill=BLACK)
    d.text((14, 116), "Energie L in Form", font=it, fill=BLACK)
    d.text((14, 132), "von Strahlung ab,", font=it, fill=BLACK)
    for i, s in enumerate(["so verkleinert", "sich seine Masse", "um L/V²."]):
        w = d.textlength(s, font=it); d.text((386 - w, 148 + 16*i), s, font=it, fill=BLACK)
    d.line([(14, 246), (386, 246)], fill=BLACK)
    m = font("mono", 10)
    d.text((14, 253), "Annalen der Physik 18, pages 639 to 641. Published", font=m, fill=BLACK)
    d.text((14, 265), "21 November 1905. L is the energy given off as light,", font=m, fill=BLACK)
    d.text((14, 277), "V the speed of light. Later hands wrote it E = mc²", font=m, fill=BLACK)
    save(im, 3)

# ------------------------------------------------------------ 4  A0: half, and half again
def a0():
    im = Image.new("RGB", (W, H), WHITE); d = crisp(im)
    mm = {1: "594 × 841", 2: "420 × 594", 3: "297 × 420", 4: "210 × 297", 5: "148 × 210"}
    fills = {1: WHITE, 2: BLACK, 3: WHITE, 4: RED, 5: BLACK, 6: WHITE, 7: BLACK, 8: WHITE, 9: BLACK, 10: WHITE}
    x, y, w, h = 0, 0, 400, 283
    for n in range(1, 11):
        if w >= h: rw, rh = w//2, h; nx, ny, nw, nh = x + rw, y, w - rw, h
        else:      rw, rh = w, h//2; nx, ny, nw, nh = x, y + rh, w, h - rh
        fill = fills[n]; ink = BLACK if fill == WHITE else WHITE
        d.rectangle([x, y, x + rw, y + rh], fill=fill, outline=BLACK)
        size = {1: 104, 2: 70, 3: 46, 4: 32, 5: 20, 6: 13}.get(n)
        if size:
            f = font("black", size); s = f"A{n}"
            l, t, r, b = d.textbbox((0, 0), s, font=f)
            cx, cy = x + rw/2, y + rh/2 - (9 if n in mm and n < 5 else 0)
            d.text((round(cx - (l + r)/2), round(cy - (t + b)/2)), s, font=f, fill=ink)
            if n in mm and n < 5:
                fm = font("mono", 10)
                ctext(d, cx + 1, round(cy + (b - t)/2 + 7), mm[n] + (" mm" if n < 4 else ""), fm, ink)
        x, y, w, h = nx, ny, nw, nh
    d.rectangle([0, 0, 399, 283], outline=BLACK)
    d.rectangle([0, 284, 399, 299], fill=BLACK)
    d.text((8, 286), "A0 is one square metre. Halve a sheet: the shape stays.", font=font("mono", 10), fill=WHITE)
    save(im, 4)

# ------------------------------------------------------------ 5  Bird base: the creases inside a paper crane
def birdbase():
    im = Image.new("RGB", (W*S, H*S), RED); d = ImageDraw.Draw(im)
    x0, y0, a = 20, 20, 260
    def P(u, v): return ((x0 + u*a)*S, (y0 + v*a)*S)
    def solid(p, q, col=WHITE, w=2): d.line([P(*p), P(*q)], fill=col, width=w*S)
    def dashed(p, q, col=BLACK, w=2, on=7, off=5):
        (ax, ay), (bx, by) = P(*p), P(*q); L = math.hypot(bx - ax, by - ay); n = int(L/((on + off)*S))
        if n < 1: n = 1
        step = L/(n + on/(on + off)); t = 0
        while t < L - 1:
            t1 = min(t + step*on/(on + off), L)
            d.line([(ax + (bx - ax)*t/L, ay + (by - ay)*t/L), (ax + (bx - ax)*t1/L, ay + (by - ay)*t1/L)], fill=col, width=w*S)
            t += step
    C = (0.5, 0.5); t = 0.5*math.tan(math.radians(22.5))
    corners = [(0, 0), (1, 0), (1, 1), (0, 1)]
    inc = [(0.5, t), (1 - t, 0.5), (0.5, 1 - t), (t, 0.5)]            # incentres: top, right, bottom, left
    mid = [(0.5, 0), (1, 0.5), (0.5, 1), (0, 0.5)]
    for i in range(4):                                                # valleys first, mountains over them
        dashed(corners[i], inc[i]); dashed(corners[(i + 1) % 4], inc[i])
        if i != 2: dashed(C, inc[i])
        else:      dashed(inc[i], mid[i])
    # the two thinning folds that make neck and tail (corners top-left and bottom-right)
    for (cx, cy, sx, sy) in ((0, 0, 1, 1), (1, 1, -1, -1)):
        for (du, dv) in [(1, math.tan(math.radians(q))) for q in (11.25, 33.75)] + [(math.tan(math.radians(q)), 1) for q in (11.25, 33.75)]:
            # run from the corner until it meets the inner median (u = 0.5 or v = 0.5)
            s_ = 0.5/max(du, dv)
            dashed((cx, cy), (cx + sx*du*s_, cy + sy*dv*s_), on=3, off=4, w=1)
    for i in range(4):
        solid(C, corners[i])
        if i != 2: solid(inc[i], mid[i])
        else:      solid(C, inc[i])
    d.rectangle([P(0, 0)[0] - S, P(0, 0)[1] - S, P(1, 1)[0] + S, P(1, 1)[1] + S], outline=BLACK, width=2*S)
    # the crane it becomes
    cx, cy, k = 292, 92, 1.02
    def Q(u, v): return ((cx + u*k)*S, (cy + v*k)*S)
    def part(pts): d.polygon([Q(*p) for p in pts], fill=WHITE, outline=BLACK, width=3)
    part([(60, 66), (70, 74), (96, 14)])                               # tail
    part([(44, 66), (34, 74), (12, 20)])                               # neck
    part([(12, 20), (-2, 31), (15, 27)])                               # head
    part([(30, 70), (74, 70), (52, 96)])                               # body
    part([(34, 70), (70, 70), (78, 26), (46, 44)])                     # near wing
    d.line([Q(52, 70), Q(52, 96)], fill=BLACK, width=3)
    d.line([Q(46, 44), Q(70, 70)], fill=BLACK, width=3)
    # its shadow, and one more sheet waiting
    d.ellipse([Q(18, 100)[0], Q(18, 100)[1], Q(88, 106)[0], Q(88, 106)[1]], fill=BLACK)
    sx, sy, sa = 318, 218, 62
    d.polygon([((sx)*S, sy*S), ((sx + sa)*S, (sy + 8)*S), ((sx + sa - 8)*S, (sy + sa + 8)*S), ((sx - 8)*S, (sy + sa)*S)], fill=WHITE, outline=BLACK, width=3)
    save(down(im), 5)

if __name__ == "__main__":
    aloft(); decoupure(); lv2(); a0(); birdbase()
    print("ok")
