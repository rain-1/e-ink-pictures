#!/usr/bin/env python3
"""2026-11-15 (Sunday). Theme: unseen.  Run from the repo root.
1 Mars, 1580-1596 (one line, after Kepler)   2 Beyond the red (Herschel's thermometers)
3 4004, about actual size                    4 Charcoal (for O'Keeffe)      5 Buran: nobody aboard"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = ["images", "archive/2026-11-15"]
F = "/usr/share/fonts/truetype/"
def font(name, size):
    paths = {"mono": F+"dejavu/DejaVuSansMono.ttf", "monob": F+"dejavu/DejaVuSansMono-Bold.ttf",
             "sans": F+"dejavu/DejaVuSans.ttf", "sansb": F+"dejavu/DejaVuSans-Bold.ttf",
             "ital": F+"liberation/LiberationSerif-Italic.ttf", "serif": F+"liberation/LiberationSerif-Regular.ttf",
             "serifb": F+"liberation/LiberationSerif-Bold.ttf",
             "black": "/usr/share/fonts/opentype/inter/Inter-Black.otf",
             "bold": "/usr/share/fonts/opentype/inter/Inter-Bold.otf"}
    return ImageFont.truetype(paths[name], size)
def new(bg=WHITE):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im); d.fontmode = "1"; return im, d
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
def ctext(d, cx, y, s, f, fill):
    b = d.textbbox((0, 0), s, font=f); d.text((cx-(b[2]-b[0])/2-b[0], y), s, font=f, fill=fill)
def vnoise(rng, w, h, cells_x, cells_y):
    g = Image.fromarray((rng.random((cells_y, cells_x))*255).astype(np.uint8), "L")
    return np.asarray(g.resize((w, h), Image.BICUBIC), float)/255

# ---------------------------------------------------------------- 1  Mars from a still Earth: one line
def helio(a, e, peri_deg, L0_deg, period, t):
    """position at t years after J2000 (planar two-body orbit)"""
    M = math.radians(L0_deg - peri_deg) + 2*math.pi*t/period
    E = M
    for _ in range(8): E = M + e*math.sin(E)
    v = 2*math.atan2(math.sqrt(1+e)*math.sin(E/2), math.sqrt(1-e)*math.cos(E/2))
    r = a*(1-e*math.cos(E)); th = v + math.radians(peri_deg)
    return r*math.cos(th), r*math.sin(th)
def mars():
    S = 3; im = Image.new("RGB", (W*S, H*S), WHITE); d = ImageDraw.Draw(im)
    cx, cy, k = 200, 150, 53.0
    pts = []
    n = 6000
    for i in range(n+1):
        t = (1580.0 - 2000.0) + 16.0*i/n
        ex, ey = helio(1.00000, 0.0167, 102.94, 100.46, 1.00002, t)
        mx, my = helio(1.52368, 0.0934, 336.04, 355.45, 1.88085, t)
        pts.append(((cx + (mx-ex)*k)*S, (cy - (my-ey)*k)*S))
    for a in range(0, 360, 3):                                  # the Sun's circle, dotted
        x = cx + k*math.cos(math.radians(a)); y = cy + k*math.sin(math.radians(a))
        d.ellipse([x*S-2, y*S-2, x*S+2, y*S+2], fill=BLACK)
    d.line(pts, fill=BLACK, width=5, joint="curve")
    im = im.resize((W, H), Image.LANCZOS).convert("L").point(lambda v: 255 if v > 150 else 0).convert("RGB")
    d = ImageDraw.Draw(im); d.fontmode = "1"
    d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=RED)               # the Earth, standing still
    x0, y0 = pts[0][0]/S, pts[0][1]/S; x1, y1 = pts[-1][0]/S, pts[-1][1]/S
    d.ellipse([x0-3, y0-3, x0+3, y0+3], fill=BLACK)
    d.ellipse([x1-3, y1-3, x1+3, y1+3], fill=WHITE, outline=BLACK)
    f = font("mono", 10)
    d.text((6, 5), "MARS", font=font("monob", 10), fill=BLACK)
    d.text((6, 17), "1580-1596", font=f, fill=BLACK)
    d.text((W-6-6*11, H-27), "seen from a", font=f, fill=BLACK)
    d.text((W-6-6*11, H-15), "still Earth", font=f, fill=BLACK)
    save(im, 1)

# ---------------------------------------------------------------- 2  Herschel's thermometers
def herschel():
    im, d = new()
    # sunbeam and prism
    d.polygon([(0, 30), (0, 40), (70, 72), (72, 64)], fill=WHITE, outline=BLACK)
    for i in range(0, 70, 6): d.line([(i, 33+i*0.46), (i+3, 37+i*0.46)], fill=BLACK)
    ex, ey = 88, 72
    xs = np.linspace(116, 284, 7)
    for i, x in enumerate(xs):
        d.line([(ex, ey), (x, 257)], fill=BLACK, width=1)
    d.polygon([(56, 92), (78, 46), (100, 92)], fill=WHITE, outline=BLACK)
    d.line([(57, 92), (99, 92)], fill=BLACK, width=2)
    d.line([(71, 66), (ex, ey)], fill=BLACK)
    # the spectrum on the table: seven hatched cells, then an empty one
    edges = np.linspace(104, 296, 8)
    for i in range(7):
        a, b = int(edges[i]), int(edges[i+1])
        pitch = 2 + i                      # violet dense -> red open
        for x in range(a, b, pitch): d.line([(x, 258), (x, 270)], fill=BLACK)
        d.line([(a, 258), (a, 270)], fill=BLACK)
    d.line([(104, 258), (296, 258)], fill=BLACK); d.line([(296, 258), (296, 270)], fill=BLACK)
    for x in range(300, 372, 5): d.point([(x, 258), (x+1, 258)], fill=BLACK)
    for y in range(258, 271, 4): d.point([(371, y), (371, y+1)], fill=BLACK)
    d.line([(0, 271), (W, 271)], fill=BLACK, width=2)
    # thermometers
    def thermo(x, level, col):
        top = 104; by = 262
        d.rounded_rectangle([x-5, top, x+5, by], radius=5, fill=WHITE, outline=BLACK)
        for k, yy in enumerate(range(by-18, top+6, -7)):
            d.line([(x+5, yy), (x+(10 if k % 5 == 0 else 8), yy)], fill=BLACK)
        d.rectangle([x-1, by-level, x+1, by], fill=col)
        d.ellipse([x-8, by-8, x+8, by+8], fill=col, outline=BLACK)
    thermo(130, 44, BLACK); thermo(200, 66, BLACK); thermo(272, 102, BLACK); thermo(336, 138, RED)
    f = font("monob", 10)
    for x, s in [(130, "VIOLET"), (200, "GREEN"), (272, "RED")]: ctext(d, x, 277, s, f, BLACK)
    ctext(d, 336, 277, "NO LIGHT", f, RED)
    d.text((172, 10), "Beyond the red", font=font("serifb", 30), fill=BLACK)
    fi = font("ital", 14)
    d.text((174, 46), "W. Herschel, 1800: the thermometer", font=fi, fill=BLACK)
    d.text((174, 62), "left in the dark climbed highest.", font=fi, fill=BLACK)
    save(im, 2)

# ---------------------------------------------------------------- 3  the 4004 at about actual size (4.72 px/mm)
def chip():
    im, d = new()
    x0, x1, y0, y1 = 155, 246, 124, 155
    for i in range(8):
        px = 158 + 12*i
        d.rectangle([px, y0-6, px+4, y0], fill=BLACK); d.rectangle([px, y1, px+4, y1+6], fill=BLACK)
        d.rectangle([px+1, y0-9, px+3, y0-6], fill=BLACK); d.rectangle([px+1, y1+6, px+3, y1+9], fill=BLACK)
    d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=BLACK)
    d.pieslice([x0-4, 135, x0+4, 144], -90, 90, fill=BLACK)            # pin-1 notch
    lx0, lx1, ly0, ly1 = 174, 227, 128, 151                          # the lid, a 50 % screen
    for y in range(ly0, ly1+1):
        for x in range(lx0, lx1+1):
            if (x+y) % 2 == 0: d.point((x, y), fill=BLACK)
    d.rectangle([lx0, ly0, lx1, ly1], outline=BLACK)
    d.rectangle([191, 133, 209, 146], fill=RED)                      # the die: 4 mm x 3 mm
    # scale bar, 10 mm
    bx = 177; d.line([(bx, 188), (bx+47, 188)], fill=BLACK)
    d.line([(bx, 185), (bx, 191)], fill=BLACK); d.line([(bx+47, 185), (bx+47, 191)], fill=BLACK)
    ctext(d, 200.5, 193, "10 mm", font("mono", 10), BLACK)
    ctext(d, 200, 236, "Intel 4004, about actual size.", font("ital", 15), BLACK)
    ctext(d, 200, 254, "The red part is the computer.", font("ital", 15), BLACK)
    ctext(d, 200, 280, "2,300 TRANSISTORS  -  ANNOUNCED 15 NOV 1971", font("mono", 10), BLACK)
    save(im, 3)

# ---------------------------------------------------------------- 4  charcoal: an unfurling form and three hills
def charcoal():
    rng = np.random.default_rng(1887)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    cx, cy, r0, b = 158.0, 138.0, 7.0, 0.185
    dx, dy = xx-cx, yy-cy
    r = np.hypot(dx, dy) + 1e-6; th = np.arctan2(-dy, dx)
    tot = np.log(r/r0)/b                                  # angle along a log spiral reaching radius r
    u = (tot - th)/(2*math.pi); f = u - np.floor(u)
    ang = (np.floor(u) + 1)*2*math.pi + th                # unwrapped angle of the outer edge of this band
    def prof(f):
        up = np.clip((f-0.42)/0.52, 0, 1)**2.3            # soft inner side
        dn = np.clip((1.0-f)/0.045, 0, 1)                 # hard outer edge
        return up*dn
    amax = 2*math.pi*3.05
    fade = np.clip((amax - ang)/3.2, 0, 1)*np.clip(ang/2.0, 0, 1)
    D = prof(f)*fade*(r > r0)
    D = np.maximum(D, np.clip(1 - r/(r0+3), 0, 1)**0.5)   # the bud
    # three hills, back to front, dark along the crest and fading down
    for hx, hy, R in [(312, 330, 110), (392, 322, 96), (238, 352, 92)]:
        dist = np.hypot(xx-hx, yy-hy); ins = dist < R
        shade = 0.92*np.exp(-(R-dist)/15.0) + 0.06
        D = np.where(ins, shade, D)
    # two long wavering strokes rising on the right
    for x0, amp, ph, wd in [(338, 9, 0.3, 3.4), (364, 6, 1.9, 2.2)]:
        xc = x0 + amp*np.sin(yy/38.0 + ph) - (yy-110)*0.10
        s = np.exp(-((xx-xc)/wd)**2)*np.clip((215-yy)/30, 0, 1)*np.clip((yy-14)/40, 0, 1)
        D = np.maximum(D, 0.85*s)
    Dm = np.asarray(Image.fromarray((np.clip(D, 0, 1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1)), float)/255
    grain = 0.55*rng.random((H, W)) + 0.45*vnoise(rng, W, H, 100, 75)
    laid = 1.0 - 0.10*((yy.astype(int) % 4) == 0)         # laid-paper lines
    tone = np.clip(Dm*(0.62 + 0.76*grain)*laid, 0, 1)
    tone = np.where(Dm > 0.88, np.maximum(tone, 0.97), tone)
    tone = np.where(tone < 0.06, 0.0, tone)
    ink = fs_bw(tone)
    a = np.where(ink, 0, 255).astype(np.uint8)
    save(Image.fromarray(a, "L").convert("RGB"), 4)

# ---------------------------------------------------------------- 5  Buran on the runway, from above
def buran():
    im, d = new()
    ry0, ry1 = 58, 242
    d.rectangle([0, ry0, W, ry1], fill=BLACK)
    d.line([(0, ry0+7), (W, ry0+7)], fill=WHITE, width=2); d.line([(0, ry1-7), (W, ry1-7)], fill=WHITE, width=2)
    for x in range(-10, W, 52): d.rectangle([x, 148, x+30, 152], fill=WHITE)
    ax = 147                                              # the orbiter's axis: a little off the centre line
    xn = 356
    half = [(0, 0), (3, 5), (10, 9), (24, 12), (52, 12), (78, 19), (100, 32), (120, 47), (133, 47),
            (136, 20), (139, 12), (146, 12), (146, 7), (152, 7), (152, 0)]
    poly = [(xn-u, ax-v) for u, v in half] + [(xn-u, ax+v) for u, v in reversed(half)]
    d.polygon(poly, fill=WHITE)
    # black nose cap and leading edges
    d.polygon([(xn, ax), (xn-3, ax-5), (xn-9, ax-8), (xn-9, ax+8), (xn-3, ax+5)], fill=BLACK)
    for s in (-1, 1):
        d.line([(xn-52, ax+s*11), (xn-78, ax+s*18), (xn-100, ax+s*31), (xn-120, ax+s*46)], fill=BLACK, width=2)
        d.line([(xn-136, ax+s*20), (xn-133, ax+s*46)], fill=BLACK)                 # elevon hinge
        d.line([(xn-128, ax+s*14), (xn-128, ax+s*46)], fill=BLACK)
        d.rectangle([xn-22, ax+s*3-1, xn-17, ax+s*3+1], fill=BLACK)               # cockpit windows
        d.line([(xn-34, ax+s*9), (xn-118, ax+s*9)], fill=BLACK)                   # payload-bay doors
        d.ellipse([xn-150, ax+s*6-3, xn-140, ax+s*6+3], fill=BLACK)               # engine pods
    d.line([(xn-34, ax), (xn-118, ax)], fill=BLACK)
    d.polygon([(xn-112, ax), (xn-148, ax-2), (xn-148, ax+2)], fill=BLACK)         # the fin, edge on
    # crosswind
    for x in (40, 78, 116):
        d.line([(x, 76), (x, 122)], fill=RED, width=3)
        d.polygon([(x-7, 118), (x+7, 118), (x, 132)], fill=RED)
    d.text((28, 178), "CROSSWIND", font=font("monob", 10), fill=WHITE)
    d.text((28, 190), "NO PILOT", font=font("monob", 10), fill=WHITE)
    # type
    d.text((8, 6), "БУРАН", font=font("black", 40), fill=BLACK)
    f = font("mono", 10)
    for i, s in enumerate(["15 NOV 1988 - BAIKONUR", "TWO ORBITS, 206 MINUTES,", "LANDED BY ITSELF"]):
        d.text((W-8-6*24, 10+12*i), s, font=f, fill=BLACK)
    ctext(d, 200, 252, "NOBODY ABOARD", font("black", 38), BLACK)
    save(im, 5)

if __name__ == "__main__":
    mars(); herschel(); chip(); charcoal(); buran()
    sheet = Image.new("RGB", (W*2+30, H*3+40), (120, 120, 120))
    for i in range(5):
        sheet.paste(Image.open(f"images/{i+1}.png").convert("RGB"), (10 + (i % 2)*(W+10), 10 + (i//2)*(H+10)))
    sp = os.environ.get("SHEET")
    if sp: sheet.resize((sheet.width*2, sheet.height*2), Image.NEAREST).save(sp)
