#!/usr/bin/env python3
"""2026-11-14 (Saturday). Theme: setting out.  Run from the repo root.
1 The whale (no text)      2 SCE to AUX (Apollo 12 switch)   3 Round the world with Nellie Bly
4 2LO crystal set          5 Six stacks (Monet's series)"""
import math, os, random, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = ["images", "archive/2026-11-14"]
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

# ---------------------------------------------------------------- 1  the whale: lines only
def whale():
    S = 3
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    body = [(62,150),(64,128),(74,114),(100,108),(150,106),(200,110),(245,120),(285,134),(312,142),
            (326,122),(350,100),(366,108),(350,146),(368,184),(354,194),(326,170),(312,156),
            (285,162),(245,172),(200,180),(150,184),(105,184),(78,180),(66,170)]
    d.polygon(body, fill=255)
    hgt = np.asarray(m.filter(ImageFilter.GaussianBlur(9)), float)/255
    hgt = hgt**0.8
    fl = Image.new("L", (W, H), 0); ImageDraw.Draw(fl).polygon([(318,140),(350,100),(366,108),(350,146),(368,184),(354,194),(326,170),(318,156)], fill=255)
    hgt = np.maximum(hgt, 0.75*np.asarray(fl.filter(ImageFilter.GaussianBlur(5)), float)/255)
    im = Image.new("RGB", (W*S, H*S), WHITE); d = ImageDraw.Draw(im)
    boat = None
    for k, y0 in enumerate(range(8, 330, 6)):
        pts = []
        for x in range(-2, W+3):
            xi = min(max(x, 0), W-1); yi = min(max(y0, 0), H-1)
            hh = hgt[yi, xi]
            swell = 2.2*math.sin(x/23.0 + k*0.9) + 1.1*math.sin(x/9.0 - k*1.7)
            y = y0 - 34*hh + swell*(1-hh)
            pts.append((x*S, y*S))
            if k == 9 and x == 286: boat = (x, y)
        d.polygon(pts + [(W*S+9, H*S+9), (-9, H*S+9)], fill=WHITE)      # hide what lies behind
        d.line(pts, fill=BLACK, width=4, joint="curve")
        # heavier stroke where the line climbs the animal
        seg = []
        for i, (x, y) in enumerate(pts):
            xi = min(max(i-2, 0), W-1); yi = min(max(y0, 0), H-1)
            if hgt[yi, xi] > 0.45: seg.append((x, y))
            else:
                if len(seg) > 2: d.line(seg, fill=BLACK, width=8, joint="curve")
                seg = []
        if len(seg) > 2: d.line(seg, fill=BLACK, width=8, joint="curve")
    bx, by = boat                                                        # one small red boat
    bx, by = bx*S, by*S - 4
    d.chord((bx-30, by-34, bx+30, by+8), 10, 170, fill=RED)
    d.line((bx-2, by-10, bx-2, by-44), fill=RED, width=3)
    d.line((bx-2, by-44, bx-58, by-4), fill=RED, width=2)
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(int)
    out = np.full((H, W, 3), 255, np.uint8)
    red = (a[..., 0] > 150) & (a[..., 1] < 120)
    blk = (a.sum(2) < 400) & ~red
    out[blk] = 0; out[red] = (255, 0, 0)
    save(Image.fromarray(out, "RGB"), 1)

# ---------------------------------------------------------------- 2  SCE to AUX
def switch():
    S = 3
    im = Image.new("RGB", (W*S, H*S), BLACK); d = ImageDraw.Draw(im)
    chk = Image.new("L", (W, H), 0)                    # 1x mask: where the ghost / shading checker goes
    cd = ImageDraw.Draw(chk)
    def lever(dr, cx, cy, ang, ln, w0, w1, fill, s=1):
        c, s_ = math.cos(ang), math.sin(ang); px, py = -s_, c
        tx, ty = cx+c*ln, cy+s_*ln
        dr.polygon([((cx+px*w0)*s, (cy+py*w0)*s), ((tx+px*w1)*s, (ty+py*w1)*s),
                    ((tx-px*w1)*s, (ty-py*w1)*s), ((cx-px*w0)*s, (cy-py*w0)*s)], fill=fill)
        dr.ellipse(((tx-w1)*s, (ty-w1)*s, (tx+w1)*s, (ty+w1)*s), fill=fill)
    def unit(cx, cy, r, down, main=False):
        hexp = [((cx+r*math.cos(math.radians(a)))*S, (cy+r*math.sin(math.radians(a)))*S) for a in range(0, 360, 60)]
        d.polygon(hexp, fill=WHITE)
        hexi = [((cx+(r-3)*math.cos(math.radians(a)))*S, (cy+(r-3)*math.sin(math.radians(a)))*S) for a in range(0, 360, 60)]
        d.polygon(hexi, fill=BLACK)
        cd.polygon([(cx+(r-3)*math.cos(math.radians(a)), cy+(r-3)*math.sin(math.radians(a))) for a in range(0, 360, 60)], fill=255)
        rr = r*0.6
        d.ellipse(((cx-rr)*S, (cy-rr)*S, (cx+rr)*S, (cy+rr)*S), fill=WHITE)
        d.ellipse(((cx-rr+3)*S, (cy-rr+3)*S, (cx+rr-3)*S, (cy+rr-3)*S), fill=BLACK)
        cd.ellipse((cx-rr+3, cy-rr+3, cx+rr-3, cy+rr-3), fill=0)
        ang = math.pi/2 if down else -math.pi/2
        if main: lever(cd, cx, cy, -math.pi/2, r*2.1, r*0.22, r*0.36, 255)   # ghost: where it was
        lever(d, cx, cy, ang, r*2.1, r*0.22+1, r*0.36+1, BLACK, S)
        lever(d, cx, cy, ang, r*2.1, r*0.22, r*0.36, WHITE, S)
    unit(200, 148, 34, True, True)
    unit(48, 148, 26, False); unit(352, 148, 26, False)
    # engraved brackets round the middle switch
    for x0, x1 in ((112, 126), (288, 274)):
        d.line((x1*S, 40*S, x0*S, 40*S, x0*S, 256*S, x1*S, 256*S), fill=WHITE, width=3)
    im = im.resize((W, H), Image.LANCZOS).point(lambda v: 255 if v > 127 else 0)
    a = np.asarray(im).copy(); c = np.asarray(chk) > 0
    yy, xx = np.mgrid[0:H, 0:W]
    ghost = c & ((xx+yy) % 2 == 0) & (a.sum(2) == 0)
    a[ghost] = 255
    im = Image.fromarray(a, "RGB"); d = ImageDraw.Draw(im); d.fontmode = "1"
    # throw arrow
    d.arc((236, 96, 276, 200), -70, 70, fill=RED, width=2)
    d.polygon([(250, 203), (263, 192), (266, 206)], fill=RED)
    ctext(d, 200, 8, "SCE", font("black", 24), WHITE)
    ctext(d, 200, 44, "NORMAL", font("monob", 12), WHITE)
    ctext(d, 200, 228, "AUX", font("black", 26), RED)
    ctext(d, 48, 190, "OFF", font("monob", 10), WHITE); ctext(d, 352, 190, "OFF", font("monob", 10), WHITE)
    ctext(d, 200, 268, "“FLIGHT, EECOM. TRY SCE TO AUX.”", font("sansb", 11), WHITE)
    ctext(d, 200, 284, "APOLLO 12 · LIGHTNING ON THE WAY UP · 14 NOV 1969", font("mono", 10), WHITE)
    save(im, 2)

# ---------------------------------------------------------------- 3  Nellie Bly game board
def bly():
    im, d = new()
    C = 30; ox = 5
    path = []
    def ring(x0, y0, w, h):
        p = [(x, y0) for x in range(x0, x0+w)] + [(x0+w-1, y) for y in range(y0+1, y0+h)]
        p += [(x, y0+h-1) for x in range(x0+w-2, x0-1, -1)] + [(x0, y) for y in range(y0+h-2, y0, -1)]
        return p
    path = ring(0, 0, 13, 10) + ring(1, 1, 11, 8)
    start = datetime.date(1889, 11, 14)
    stops = {0: "Hoboken, 14 Nov 1889", 8: "Southampton", 13: "Port Said", 34: "Singapore",
             44: "leaves Hong Kong", 50: "Yokohama", 72: "Jersey City, 25 Jan 1890"}
    assert (datetime.date(1890, 1, 25)-start).days == 72 and (datetime.date(1889, 12, 28)-start).days == 44
    assert (datetime.date(1889, 12, 18)-start).days == 34 and (datetime.date(1890, 1, 3)-start).days == 50
    f = font("monob", 10); fs = font("mono", 10)
    for i, (cx, cy) in enumerate(path[:73]):
        x, y = ox+cx*C, cy*C
        if i == 72: continue
        fill = RED if i == 0 else BLACK if i in stops else WHITE
        d.rectangle((x, y, x+C, y+C), fill=fill, outline=BLACK)
        if fill == WHITE and i % 2:                      # a little sea in every other square
            for k in range(3):
                yy = y+19+k*3
                for xx in range(x+4+(k % 2)*3, x+C-4, 6): d.line((xx, yy, xx+2, yy), BLACK)
        ctext(d, x+C/2+1, y+5 if fill == WHITE else y+8, str(i), f if fill == WHITE else font("sansb", 12), BLACK if fill == WHITE else WHITE)
    # finish: the last four squares of the inner ring run together
    xs = [ox+c[0]*C for c in path[72:76]]; ys = [c[1]*C for c in path[72:76]]
    x, y0, y1 = xs[0], min(ys), max(ys)+C
    d.rectangle((x, y0, x+C, y1), fill=RED, outline=BLACK)
    ctext(d, x+C/2+1, y0+8, "72", font("black", 18), WHITE)
    for k, s in enumerate(("days", "6 h", "11 m")):
        ctext(d, x+C/2+1, y0+38+k*14, s, f, WHITE)
    ctext(d, x+C/2+1, y1-18, "home", f, WHITE)
    d.rectangle((ox, 0, ox+13*C, 10*C-1), outline=BLACK)
    # the middle of the board
    L, T = ox+2*C+8, 2*C+6
    d.text((L, T), "ROUND THE WORLD", font=font("black", 25), fill=BLACK)
    d.text((L+1, T+30), "with Nellie Bly, of the New York World", font=font("ital", 14), fill=BLACK)
    d.line((L, T+52, ox+11*C-8, T+52), BLACK)
    yy = T+60
    for k, v in stops.items():
        d.rectangle((L, yy, L+19, yy+12), fill=RED if k in (0, 72) else BLACK)
        ctext(d, L+10, yy+1, str(k), f, WHITE)
        d.text((L+27, yy+1), v, font=fs, fill=BLACK)
        yy += 15
    save(im, 3)

# ---------------------------------------------------------------- 4  2LO: a crystal set
def crystal():
    im, d = new()
    TOP, BOT = 108, 214
    def wire(*p): d.line(p, fill=BLACK, width=2)
    # aerial
    wire(46, 28, 46, TOP); wire(46, 50, 28, 26); wire(46, 50, 64, 26); wire(26, 26, 66, 26)
    # coil
    wire(46, TOP, 46, TOP+10)
    for k in range(7):
        y = TOP+10+k*12
        d.arc((36, y, 58, y+12), -90, 90, fill=BLACK, width=2)
    wire(46, TOP+94, 46, BOT)
    # rails
    wire(46, TOP, 176, TOP); wire(212, TOP, 300, TOP); wire(46, BOT, 300, BOT)
    for x, y in ((46, TOP), (118, TOP), (46, BOT), (118, BOT)): d.ellipse((x-3, y-3, x+3, y+3), fill=BLACK)
    # variable condenser
    wire(118, TOP, 118, 155); wire(118, 167, 118, BOT)
    d.line((100, 155, 136, 155), BLACK, 3); d.line((100, 166, 136, 166), BLACK, 3)
    d.line((98, 178, 138, 144), BLACK, 1); d.polygon([(138, 144), (130, 146), (135, 152)], fill=BLACK)
    # the crystal: red
    d.polygon([(176, TOP-12), (176, TOP+12), (200, TOP)], fill=RED)
    d.line((201, TOP-12, 201, TOP+12), RED, 3); d.line((201, TOP, 212, TOP), RED, 2)
    # phones
    wire(300, TOP, 300, 140); wire(300, 184, 300, BOT)
    d.arc((282, 132, 318, 192), 180, 360, fill=BLACK, width=2)
    d.rounded_rectangle((276, 156, 288, 180), 3, fill=BLACK); d.rounded_rectangle((312, 156, 324, 180), 3, fill=BLACK)
    wire(300, 140, 300, 132); wire(300, 184, 282, 184); wire(282, 184, 282, 180)
    wire(300, 184, 318, 184); wire(318, 184, 318, 180)
    d.rectangle((299, 133, 301, 183), fill=WHITE); wire(300, 124, 300, 132)
    wire(300, TOP, 300, 132); wire(300, 192, 300, BOT); wire(282, 192, 318, 192); wire(282, 180, 282, 192); wire(318, 180, 318, 192)
    d.rectangle((283, 183, 317, 190), fill=WHITE); wire(282, 192, 318, 192)
    # earth
    wire(46, BOT, 46, 236); d.line((32, 236, 60, 236), BLACK, 2); d.line((37, 241, 55, 241), BLACK, 2); d.line((42, 246, 50, 246), BLACK, 2)
    # what is in the wire at each place
    def audio(t): return 0.55 + 0.3*math.sin(t*2.1) + 0.15*math.sin(t*5.3+1)
    def trace(x0, x1, yc, kind, col):
        pts = []
        for i in range((x1-x0)*4+1):
            x = x0 + i/4; t = (x-x0)/(x1-x0)*2*math.pi
            env = audio(t)*15
            if kind == 0: y = yc - env*math.sin((x-x0)*1.9)
            elif kind == 1: y = yc + 8 - max(0, env*math.sin((x-x0)*1.9))
            else: y = yc + 8 - env
            pts.append((x, y))
        d.line(pts, fill=col, width=1)
    trace(70, 164, 72, 0, BLACK); trace(214, 292, 72, 1, BLACK); trace(334, 392, 160, 2, RED)
    d.line((214, 80, 292, 80), BLACK); 
    for x in range(334, 392, 4): d.point((x, 168), BLACK)
    fi = font("ital", 13)
    d.text((70, 30), "aerial", font=fi, fill=BLACK)
    d.text((62, 222), "earth", font=fi, fill=BLACK)
    d.text((64, 160), "coil", font=fi, fill=BLACK); d.text((142, 172), "condenser", font=fi, fill=BLACK)
    ctext(d, 194, TOP+16, "crystal", fi, RED)
    d.text((332, 176), "a voice", font=fi, fill=RED)
    d.text((244, 220), "head-phones", font=fi, fill=BLACK)
    d.text((292, 232), "2LO", font=font("black", 46), fill=BLACK)
    d.text((62, 256), "“2LO, Marconi House, London, calling.”", font=font("ital", 13), fill=BLACK)
    d.text((62, 274), "14 NOV 1922 · THE FIRST EVENING", font=font("mono", 10), fill=BLACK)
    save(im, 4)

# ---------------------------------------------------------------- 5  Monet's stacks, six effects
def stacks():
    rng = np.random.default_rng(1840)
    im, d = new()
    pw, ph = 120, 112
    #        name               sky  field hill  lit  shade shadow(dx,len,tone)  red  snow
    P = [("morning",           .93, .72, .55, .55, .22, (-1.0, 46, .40), 0, 0),
         ("midday",           1.00, .86, .62, .50, .30, (-0.2, 12, .50), 0, 0),
         ("sunset",           1.00, .30, .12, .02, .02, ( 0.9, 50, .08), 1, 0),
         ("snow effect",       .80, 1.0, .60, .45, .15, ( 1.0, 40, .62), 0, 1),
         ("mist",              .86, .82, .74, .52, .46, ( 0.0,  0, .70), 0, 0),
         ("dusk",              .62, .30, .14, .0, .0, ( 0.0,  0, .10), 2, 0)]
    for n, (name, sky, field, hill, lit, shade, (sdx, sl, st), red, snow) in enumerate(P):
        X = 10 + (n % 3)*130; Y = 6 + (n//3)*136
        yy, xx = np.mgrid[0:ph, 0:pw].astype(float)
        hz = 62
        T = np.where(yy < hz, sky - (0.10 if red != 1 else 0)*(yy/hz), field - 0.10*(yy-hz)/(ph-hz))
        R = np.zeros((ph, pw))
        if red == 1: R = np.where(yy < hz, 0.15 + 0.75*(yy/hz)**1.5, 0)
        if red == 2: R = np.where((yy < hz) & (yy > hz-22), np.clip((yy-(hz-22))/22, 0, 1)**1.3*0.95, 0); T = np.where((yy < hz) & (yy > hz-22), np.maximum(T, 0.42 + 0.58*(yy-(hz-22))/22), T)
        # far line of poplars and hills
        ridge = hz - 9 - 5*vnoise(rng, pw, 1, 9, 1)[0] - 3*vnoise(rng, pw, 1, 30, 1)[0]
        T = np.where((yy < hz) & (yy > ridge[None, :]), hill, T)
        R = np.where((yy < hz) & (yy > ridge[None, :]), 0, R)
        def stack(cx, base, w, h, T):
            body = h*0.5
            half = np.where(yy > base-body, w/2*(0.88+0.12*(base-yy)/body), w/2*1.06*np.clip((yy-(base-h))/(h-body), 0, 1)**0.5)
            inside = (np.abs(xx-cx) < half) & (yy <= base) & (yy >= base-h)
            if sl:                                         # cast shadow, a sheared copy on the ground
                t = (yy-base)/ (sl*0.45)
                sh = (t >= 0) & (t <= 1) & (np.abs(xx-(cx+sdx*sl*t)) < w/2*(1-0.75*t))
                T = np.where(sh & ~inside, np.minimum(T, st), T)
            side = lit + (shade-lit)*np.clip(((xx-cx)*(-1 if sdx < 0 else 1) + w*0.45)/(w*0.9), 0, 1)**1.5 if sl else lit+0*xx
            T = np.where(inside, side, T)
            if snow: T = np.where(inside & (yy < base-body-h*0.12+ (xx-cx)*0.25), 1.0, T)
            return T, inside
        ins = np.zeros((ph, pw), bool)
        if n in (0, 1, 3):
            T, i1 = stack(34, 78, 30, 30, T); ins |= i1
        T, i2 = stack(78 if n != 4 else 62, 96, 56, 58, T); ins |= i2
        R = np.where(ins, 0, R)
        brush = (vnoise(rng, pw, ph, 30, 58) - 0.5)*0.16 + (vnoise(rng, pw, ph, 8, 20)-0.5)*0.10
        soft = (T > 0.03) & (T < 0.99)
        T = np.where(soft, T + brush, T)
        bw = fs_bw(np.clip(T, 0, 1))
        rd = ~fs_bw(1-np.clip(R + (brush*0.8 if red else 0), 0, 1)) if red else np.zeros((ph, pw), bool)
        a = np.where(bw[..., None], 255, 0).astype(np.uint8).repeat(3, 2)
        a[bw & rd] = (255, 0, 0)
        a[(T < 0.05) & ~rd] = 0
        if red == 1:                                       # the sun, going
            sun = (np.hypot(xx-28, yy-(hz-13)) < 8) & (yy < ridge[None, :])
            a[sun] = (255, 255, 255)
        im.paste(Image.fromarray(a, "RGB"), (X, Y))
        d.rectangle((X-1, Y-1, X+pw, Y+ph), outline=BLACK)
        d.text((X, Y+ph+3), name, font=font("ital", 13), fill=RED if red == 1 else BLACK)
    ctext(d, 200, 279, "Claude Monet, born 14 November 1840: one field, six effects", font("ital", 13), BLACK)
    save(im, 5)

if __name__ == "__main__":
    whale(); switch(); bly(); crystal(); stacks()
