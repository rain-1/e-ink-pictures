#!/usr/bin/env python3
"""2026-11-16 (Monday). Theme: names.  Run from the repo root.
1 M 13 (where the Arecibo message is going)   2 Mosi-oa-Tunya (line engraving)
3 A page with the words taken out (Saramago)  4 25 (echo bands round a numeral)   5 Do re mi"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = ["images", "archive/2026-11-16"]
F = "/usr/share/fonts/truetype/"
def font(name, size):
    paths = {"mono": F+"dejavu/DejaVuSansMono.ttf", "monob": F+"dejavu/DejaVuSansMono-Bold.ttf",
             "sansb": F+"dejavu/DejaVuSans-Bold.ttf",
             "ital": F+"liberation/LiberationSerif-Italic.ttf", "serif": F+"liberation/LiberationSerif-Regular.ttf", "serifb": F+"liberation/LiberationSerif-Bold.ttf",
             "free": F+"freefont/FreeSerif.ttf",
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

# ------------------------------------------------------------ 1  M 13: a globular cluster of points
def m13():
    rng = np.random.default_rng(13)
    cx, cy = 200, 128
    L = np.zeros((H, W))
    n = 16000
    u = rng.random(n)
    r = 30/np.sqrt(u**(-2/3) - 1)                         # Plummer sphere, projected
    r = r*rng.random(n)**0.25
    th = rng.random(n)*2*math.pi
    x = cx + r*np.cos(th)*1.04; y = cy + r*np.sin(th)
    lum = 0.25 + 0.9*rng.pareto(2.2, n)
    ok = (x >= 0) & (x < W-1) & (y >= 0) & (y < H-1)
    np.add.at(L, (y[ok].astype(int), x[ok].astype(int)), lum[ok])
    for _ in range(260):                                  # field stars
        L[rng.integers(0, H), rng.integers(0, W)] += 0.5 + rng.pareto(2.0)
    g = np.asarray(Image.fromarray((np.clip(L, 0, 8)*31).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1)), float)/31
    T = np.clip(0.55*L + 0.5*g, 0, 1)**0.9
    T = np.minimum(T, 0.93)
    T[T < 0.07] = 0
    im = rgb(fs_bw(T)); d = ImageDraw.Draw(im); d.fontmode = "1"
    d.rectangle([0, 248, W, H], fill=BLACK)
    f = font("mono", 10); fb = font("monob", 10)
    d.text((10, 6), "M 13", font=font("sansb", 12), fill=WHITE)
    d.text((10, 22), "in Hercules", font=f, fill=WHITE)
    x0, x1, yb = 14, 386, 266
    for xx in range(x0, x1, 4): d.point((xx, yb), fill=WHITE)   # the road still to go, dotted
    d.line([x0, yb-5, x0, yb+5], fill=WHITE)
    d.line([x1, yb-5, x1, yb+5], fill=WHITE)
    xm = x0 + (x1-x0)*52/25000                               # under one pixel along
    d.rectangle([x0+1, yb-4, x0+2, yb+4], fill=RED)
    d.text((x0+8, yb-15), "the message, 52 years out", font=fb, fill=RED)
    d.text((x0, yb+9), "Arecibo, 16 Nov 1974", font=f, fill=WHITE)
    s = "about 25,000 to go"; d.text((x1-6*len(s)+1, yb+9), s, font=f, fill=WHITE)
    save(im, 1)

# ------------------------------------------------------------ 2  Mosi-oa-Tunya: engraved in lines
def falls():
    rng = np.random.default_rng(1855)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    hz = 158
    T = np.where(yy < hz, 0.62 - 0.30*(yy/hz), 0.0)                    # sky, darker at the top
    cols = [(52, 26, 150, -0.10), (118, 34, 205, -0.16), (176, 40, 250, -0.20), (246, 36, 215, -0.24), (318, 28, 160, -0.3)]
    plume = np.zeros((H, W))
    for (px, wd, ht, lean) in cols:                                    # five columns of vapour
        t = np.clip((hz - yy)/ht, 0, 1)
        cxl = px + lean*(hz-yy)*(0.5+t) + 9*np.sin(yy/23 + px)
        wid = wd*(0.32 + 0.85*t**0.8)
        p = np.exp(-((xx-cxl)/wid)**2) * np.clip(1.25 - t**1.6*1.25, 0, 1) * (yy < hz+4)
        plume = np.maximum(plume, p)
    nz = np.asarray(Image.fromarray((rng.random((10, 14))*255).astype(np.uint8)).resize((W, H), Image.BICUBIC), float)/255
    plume = np.clip(plume*(0.8+0.5*nz), 0, 1)
    T = T*(1 - np.clip(plume*1.25, 0, 1))
    water = yy >= hz                                                   # the river
    Tw = 0.22 + 0.42*(np.clip(yy-hz, 0, None)/(H-hz))**1.3 + 0.10*np.sin(xx/31 + yy/7)*np.sin(yy/5)
    glare = np.exp(-((xx-300)/120)**2)*np.exp(-(yy-hz)/40)
    T = np.where(water, np.clip(Tw - 0.3*glare, 0.05, 0.9), T)
    # solid masses on an L mask at 3x: far bank, islands, palms, canoe, people
    S = 3; M = Image.new("L", (W*S, H*S), 0); d = ImageDraw.Draw(M)
    def poly(p, fill=255): d.polygon([(x*S, y*S) for x, y in p], fill=fill)
    def line(p, w): d.line([(x*S, y*S) for x, y in p], fill=255, width=int(w*S), joint="curve")
    def bank(x0, x1, y0, hmax, seed):
        r = np.random.default_rng(seed); pts = [(x0, y0)]
        for x in range(x0, x1+1, 3):
            e = math.sin(math.pi*(x-x0)/(x1-x0))**0.5
            pts.append((x, y0 - e*hmax*(0.55+0.45*r.random())))
        pts.append((x1, y0)); poly(pts)
    def palm(x, y, h, lean, seed):
        r = np.random.default_rng(seed); tx = x+lean; ty = y-h
        line([(x, y), (x+lean*0.3, y-h*0.5), (tx, ty)], 1.4)
        for k in range(7):
            a = math.radians(-170 + 26.6*k + r.uniform(-8, 8)); ln = h*r.uniform(0.34, 0.5)
            mx, my = tx + ln*0.6*math.cos(a), ty + ln*0.6*math.sin(a) - 3
            line([(tx, ty), (mx, my), (tx + ln*math.cos(a), ty + ln*math.sin(a) + 4)], 1.5)
    bank(0, 96, hz+2, 9, 1); bank(140, 222, hz+2, 7, 2); bank(282, 400, hz+2, 10, 3)
    for (x, h, l, s) in [(18, 34, 4, 1), (40, 26, -3, 2), (74, 30, 5, 3), (160, 24, 3, 4), (300, 28, -4, 5), (338, 36, 5, 6), (372, 27, -3, 7)]:
        palm(x, hz-3, h, l, s)
    bank(-10, 70, 300, 46, 8)                                           # near bank, bottom left
    for k in range(9):                                                  # reeds
        x = 6 + k*7; line([(x, 262), (x + (k % 3 - 1)*4, 226 - (k*5) % 13)], 1.2)
    wy = 236                                                            # the canoe: a long dugout
    poly([(132, wy-5), (150, wy-1), (300, wy-1), (322, wy-7), (304, wy+4), (150, wy+4)])
    def person(x, stand=True, cap=False, paddle=None):
        if stand:
            top = wy-40
            d.ellipse([(x-3.3)*S, (top)*S, (x+3.3)*S, (top+7)*S], fill=255)
            poly([(x-5.5, top+9), (x+5.5, top+9), (x+3.2, top+24), (x-3.2, top+24)])
            line([(x-2, top+23), (x-3.5, top+32), (x-3, wy)], 2.6); line([(x+2, top+23), (x+3.5, top+32), (x+3, wy)], 2.6)
            if paddle:
                sx = paddle
                line([(x-5, top+10), (x+sx*9, top+16), (x+sx*5, top+21)], 2.2)
                line([(x+5, top+10), (x+sx*11, top+9)], 2.2)
                line([(x+sx*13, top+1), (x+sx*3, wy+12)], 1.3)
                poly([(x+sx*3-2, wy+10), (x+sx*3+2.2, wy+10), (x+sx*1.2+1.5, wy+20), (x+sx*1.2-1.5, wy+20)])
        else:
            top = wy-24
            d.ellipse([(x-3.3)*S, top*S, (x+3.3)*S, (top+7)*S], fill=255)
            if cap: poly([(x-4, top+2), (x+4, top+2), (x+8, top+3.4), (x+4, top+0.2), (x+2, top-1.6), (x-3, top-1.4)])
            poly([(x-5.5, top+9), (x+5, top+9), (x+4.5, wy), (x-5, wy)])
            line([(x+4, top+11), (x+11, top+17)], 2.2)
    person(160, paddle=-1); person(190, paddle=1); person(222, stand=False, cap=True); person(250, stand=False)
    person(288, paddle=1)
    m = np.asarray(M.resize((W, H), Image.LANCZOS), float)/255
    # the line screen
    pitch = 4
    wob = 1.2*np.sin(xx/41 + yy/17) * (yy >= hz)                        # the water lines waver
    ph = ((yy + wob) % pitch)
    dist = np.abs(ph - pitch/2 + 0.5)
    ink = dist < (T*pitch/2 + (rng.random((H, W))-0.5)*0.35)
    sun = ((xx-362)**2 + (yy-104)**2 < 17**2)
    im = rgb(~ink); a = np.asarray(im).copy()
    a[sun & (yy < hz)] = RED
    refl = (np.abs(xx-362) < 17 - (yy-hz)*0.4) & (yy > hz+4) & (yy < hz+40) & (ph < 1) & ((xx + yy*3) % 7 < 4)
    a[refl] = RED
    a[m > 0.5] = BLACK
    im = Image.fromarray(a, "RGB"); d2 = ImageDraw.Draw(im); d2.fontmode = "1"
    fb = font("black", 15); s = "MOSI-OA-TUNYA"
    b = d2.textbbox((0, 0), s, font=fb); tw = b[2]-b[0]
    d2.rectangle([W-tw-22, 8, W-6, 46], fill=WHITE)
    d2.text((W-tw-14-b[0], 12), s, font=fb, fill=BLACK)
    s2 = "the smoke that thunders"; f = font("mono", 10)
    d2.text((W-14-6*len(s2), 32), s2, font=f, fill=BLACK)
    s3 = "16 Nov 1855: a visitor in a canoe renames it"
    d2.rectangle([W-6*len(s3)-12, H-17, W, H], fill=WHITE)
    d2.text((W-6*len(s3)-6, H-14), s3, font=f, fill=BLACK)
    save(im, 2)

# ------------------------------------------------------------ 3  Saramago: the words taken out
def page():
    rng = np.random.default_rng(1922)
    im = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(im); d.fontmode = "1"
    fp = font("serifb", 22)
    x0, x1, y, lh, adv = 40, 360, 22, 14, 5.2
    x = x0 + 18; marks = []
    lines = 16; ln = 0; clause = rng.integers(2, 7); sent = rng.integers(5, 14)
    while ln < lines:
        wl = int(rng.choice([1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 11]))
        if x + wl*adv > x1:
            ln += 1; x = x0
            if ln >= lines: break
        x += wl*adv
        clause -= 1
        if clause <= 0:
            sent -= 1
            if sent <= 0: marks.append((x, ln, ".")); sent = rng.integers(5, 14)
            else: marks.append((x, ln, ","))
            clause = rng.integers(2, 8); x += adv
        x += adv
    if marks[-1][2] == ",": marks[-1] = (marks[-1][0], marks[-1][1], ".")
    else: pass
    last = len(marks)-1
    for i, (mx, ml, ch) in enumerate(marks):
        d.text((mx, y + ml*lh), ch, font=fp, fill=RED if i == last else BLACK)
    fi = font("serif", 13)
    d.text((x0, 252), "A page in the manner of José Saramago,", font=fi, fill=BLACK)
    d.text((x0, 267), "born 16 November 1922, with the words taken out.", font=fi, fill=BLACK)
    save(im, 3)

# ------------------------------------------------------------ 4  25: echo bands round a numeral
def lsd():
    S = 3; G = Image.new("L", (W*S, H*S), 0); d = ImageDraw.Draw(G)
    f = font("black", 150*S); s = "25"
    b = d.textbbox((0, 0), s, font=f)
    d.text(((W*S-(b[2]-b[0]))/2 - b[0], (H*S-(b[3]-b[1]))/2 - b[1] - 8*S), s, font=f, fill=255)
    g3 = np.asarray(G) > 127
    edge = g3 & ~np.asarray(G.filter(ImageFilter.MinFilter(3)), bool) if False else (np.asarray(G.filter(ImageFilter.MaxFilter(3))) > 127) & ~(np.asarray(G.filter(ImageFilter.MinFilter(3))) > 127)
    ey, ex = np.nonzero(edge); sel = slice(None, None, 3)
    ex = ex[sel]/S; ey = ey[sel]/S
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    D = np.empty((H, W), np.float32)
    for r in range(0, H, 10):                                           # brute-force distance to the outline
        dx = xx[r:r+10, :, None] - ex[None, None, :]; dy = yy[r:r+10, :, None] - ey[None, None, :]
        D[r:r+10] = np.sqrt((dx*dx + dy*dy).min(axis=2))
    inside = np.asarray(G.resize((W, H), Image.LANCZOS)) > 127
    th = np.arctan2(yy-142, xx-200)
    Dw = D + 2.2*np.sin(5*th + D/21)*np.clip(D/30, 0, 1)                # the bands start to swim
    band = (np.sqrt(Dw + 1.0)*1.9 - 0.9) % 2 < 1
    a = np.where(band[..., None], np.array(BLACK, np.uint8), np.array(WHITE, np.uint8))
    a[inside] = RED
    a[(D < 2.2) & ~inside] = WHITE
    im = Image.fromarray(a.astype(np.uint8), "RGB"); d = ImageDraw.Draw(im); d.fontmode = "1"
    fm = font("mono", 10); fb = font("monob", 10)
    l1 = "LYSERGIC ACID DIETHYLAMIDE, No. 25"; l2 = "first made in Basel, 16 Nov 1938,"; l3 = "then left on the shelf for five years"
    wbox = 6*len(l3) + 14
    d.rectangle([0, H-44, wbox, H], fill=BLACK)
    d.text((7, H-40), l1, font=fb, fill=WHITE); d.text((7, H-27), l2, font=fm, fill=WHITE); d.text((7, H-14), l3, font=fm, fill=WHITE)
    save(im, 4)

# ------------------------------------------------------------ 5  Do re mi: seven children, seven notes
def doremi():
    S = 3; im = Image.new("RGB", (W*S, H*S), BLACK); d = ImageDraw.Draw(im)
    def P(p): return [(x*S, y*S) for x, y in p]
    floor = 250
    kids = [("DO", 62, "g"), ("RE", 74, "g"), ("MI", 86, "g"), ("FA", 97, "b"), ("SOL", 108, "g"), ("LA", 119, "b"), ("TI", 130, "g")]
    xs = [44 + i*52 for i in range(7)]
    top, sp = 34, 9                                                      # staff: five lines
    for k in range(5): d.line(P([(14, top+k*sp), (386, top+k*sp)]), fill=WHITE, width=S)
    for i, ((name, h, sex), x) in enumerate(zip(kids, xs)):
        u = h/100.0; y0 = floor - h
        hr = 7.5*u**0.5
        d.ellipse([(x-hr)*S, y0*S, (x+hr)*S, (y0+2*hr)*S], fill=WHITE)
        sh = y0 + 2*hr + 2.5; sw = 13*u**0.7
        if sex == "g":
            if i % 2 == 0:                                               # plaits
                d.line(P([(x-hr+1, y0+hr), (x-hr-2, sh+7*u)]), fill=WHITE, width=int(2.4*S)); d.line(P([(x+hr-1, y0+hr), (x+hr+2, sh+7*u)]), fill=WHITE, width=int(2.4*S))
            hem = floor - 30*u
            d.polygon(P([(x-sw, sh), (x+sw, sh), (x+sw*0.62, sh+26*u), (x+sw*1.5, hem), (x-sw*1.5, hem), (x-sw*0.62, sh+26*u)]), fill=WHITE)
            for sx in (-1, 1):
                d.line(P([(x+sx*sw*0.45, hem), (x+sx*sw*0.45, floor-2)]), fill=WHITE, width=int(3.2*u*S))
                d.line(P([(x+sx*sw*0.45, floor-1), (x+sx*(sw*0.45+5*u), floor-1)]), fill=WHITE, width=int(2.4*S))
                d.line(P([(x+sx*(sw-1), sh+2), (x+sx*(sw+5*u), sh+30*u)]), fill=WHITE, width=int(3.4*u*S))
        else:
            hip = sh + 34*u; knee = hip + 16*u
            d.polygon(P([(x-sw, sh), (x+sw, sh), (x+sw*0.72, hip), (x-sw*0.72, hip)]), fill=WHITE)
            d.polygon(P([(x-sw*0.8, hip-1), (x+sw*0.8, hip-1), (x+sw*0.86, knee), (x+1, knee), (x, hip+6*u), (x-1, knee), (x-sw*0.86, knee)]), fill=WHITE)
            for sx in (-1, 1):
                d.line(P([(x+sx*sw*0.45, knee), (x+sx*sw*0.45, floor-2)]), fill=WHITE, width=int(3.4*u*S))
                d.line(P([(x+sx*sw*0.45, floor-1), (x+sx*(sw*0.45+5*u), floor-1)]), fill=WHITE, width=int(2.4*S))
                d.line(P([(x+sx*(sw-1), sh+2), (x+sx*(sw+5*u), sh+30*u)]), fill=WHITE, width=int(3.4*u*S))
        ny = top + 4*sp + sp - i*sp/2                                    # C4 on a ledger line, then up by steps
        if i == 0: d.line(P([(x-14, ny), (x+14, ny)]), fill=WHITE, width=S)
        d.line(P([(x+6.2, ny), (x+6.2, ny-27)]), fill=WHITE, width=int(1.5*S))
        nh = Image.new("L", (30*S, 30*S), 0); ImageDraw.Draw(nh).ellipse([8*S, 10.6*S, 22*S, 19.4*S], fill=255)
        nh = nh.rotate(22, Image.BICUBIC)
        im.paste(RED, (int((x-15)*S), int((ny-15)*S)), nh)
    d.line(P([(0, floor+1), (W, floor+1)]), fill=WHITE, width=S)
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(int); r, g = a[..., 0], a[..., 1]
    out = np.zeros((H, W, 3), np.uint8)
    out[(r > 128) & (g > 128)] = WHITE; out[(r > 128) & (g <= 128)] = RED
    im = Image.fromarray(out, "RGB"); d = ImageDraw.Draw(im); d.fontmode = "1"
    fb = font("black", 15)
    for (name, h, sex), x in zip(kids, xs):
        b = d.textbbox((0, 0), name, font=fb); d.text((x-(b[2]-b[0])/2-b[0], floor+9), name, font=fb, fill=RED)
    s = "Broadway, 16 November 1959"; f = font("mono", 10)
    d.text((W-8-6*len(s), H-15), s, font=f, fill=WHITE)
    save(im, 5)

if __name__ == "__main__":
    m13(); falls(); page(); lsd(); doremi()
