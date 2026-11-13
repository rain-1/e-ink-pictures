#!/usr/bin/env python3
"""2026-11-13 (Friday the 13th). Theme: luck.  Run from the repo root.
1 The night the stars fell   2 Holland Tunnel section   3 Treasure map
4 Calendar leaf              5 One binocular field (Mars + Jupiter)"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 300
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
OUT = ["images", "archive/2026-11-13"]
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
    """Floyd-Steinberg, float field 0..1 -> bool (True = white)."""
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

# ---------------------------------------------------------------- 1
def stars_fell():
    rnd = random.Random(1833); S = 3
    L = Image.new("L", (W*S, H*S), 0); d = ImageDraw.Draw(L)
    rx, ry = 262, 58                                  # the radiant
    def streak(dr, ang, r0, ln, wd, peak):
        n = 14
        for i in range(n):
            a, b = r0 + ln*i/n, r0 + ln*(i+1)/n
            v = int(peak*((i+1)/n)**1.6)
            p = [(rx+math.cos(ang)*a)*S, (ry+math.sin(ang)*a)*S, (rx+math.cos(ang)*b)*S, (ry+math.sin(ang)*b)*S]
            dr.line(p, fill=v, width=max(1, int(wd*S*(0.4+0.6*(i+1)/n))))
    crisp = []
    for k in range(210):
        ang = rnd.uniform(0, 2*math.pi); r0 = rnd.uniform(10, 380)
        ln = r0*rnd.uniform(0.12, 0.42) + 4
        if k % 3: crisp.append((ang, r0, ln))
        else: streak(d, ang, r0, ln, rnd.choice([1, 1.6, 2.2]), rnd.randint(150, 255))
    L = L.filter(ImageFilter.GaussianBlur(1.2)).resize((W, H), Image.LANCZOS)
    m = np.asarray(L, float)/255
    yy, xx = np.mgrid[0:H, 0:W]
    glow = 0.80*np.exp(-(258-yy).clip(0)/30.0) + 0.10*np.exp(-np.hypot(xx-rx, yy-ry)/60)
    field = (glow + m*1.1).clip(0, 1)
    bw = fs_bw(field)
    im = Image.fromarray(np.where(bw[..., None], 255, 0).astype(np.uint8).repeat(3, 2), "RGB")
    d = ImageDraw.Draw(im); d.fontmode = "1"
    for ang, r0, ln in crisp:                          # hard white streaks, heavier at the head
        c, s_ = math.cos(ang), math.sin(ang)
        d.line((rx+c*r0, ry+s_*r0, rx+c*(r0+ln), ry+s_*(r0+ln)), WHITE)
        if ln > 22: d.line((rx+c*(r0+ln*0.6), ry+s_*(r0+ln*0.6), rx+c*(r0+ln), ry+s_*(r0+ln)), WHITE, 2)
    for k in range(60):                                # fixed stars
        x, y = rnd.randint(0, W-1), rnd.randint(0, 230)
        d.point((x, y), WHITE)
        if k % 9 == 0: d.line((x-1, y, x+1, y), WHITE); d.line((x, y-1, x, y+1), WHITE)
    # the fireball: red, with a white core
    ang = math.radians(118); a0, a1 = 60, 205
    for i in range(40):
        t = i/39; r = a0 + (a1-a0)*t; wd = 1 + 5*t**1.5
        x, y = rx+math.cos(ang)*r, ry+math.sin(ang)*r
        d.ellipse((x-wd/2, y-wd/2, x+wd/2, y+wd/2), fill=RED)
    hx, hy = rx+math.cos(ang)*a1, ry+math.sin(ang)*a1
    d.ellipse((hx-6, hy-6, hx+6, hy+6), fill=RED); d.ellipse((hx-3, hy-3, hx+3, hy+3), fill=WHITE)
    # the land: a low ridge, a meeting-house, people looking up
    pts = [(0, H)]
    for x in range(0, W+1, 4):
        pts.append((x, 262 + 7*math.sin(x/61.0) + 4*math.sin(x/23.0+1) - 10*math.exp(-((x-70)/60.0)**2)))
    pts.append((W, H)); d.polygon(pts, fill=BLACK)
    gy = lambda x: 262 + 7*math.sin(x/61.0) + 4*math.sin(x/23.0+1) - 10*math.exp(-((x-70)/60.0)**2)
    bx = 66; by = gy(bx)+2                              # meeting-house
    d.rectangle((bx, by-18, bx+34, by), fill=BLACK); d.polygon([(bx-2, by-18), (bx+17, by-30), (bx+36, by-18)], fill=BLACK)
    d.rectangle((bx+3, by-40, bx+11, by-18), fill=BLACK); d.polygon([(bx+2, by-40), (bx+7, by-62), (bx+12, by-40)], fill=BLACK)
    d.rectangle((bx+19, by-12, bx+22, by-6), fill=RED)  # one lit window
    for tx, th in [(22, 30), (36, 22), (128, 26), (344, 34), (366, 24), (384, 30)]:   # bare trees
        b = gy(tx); d.line((tx, b+2, tx, b-th), BLACK, 2)
        for j in range(6):
            yb = b - th*(0.35+0.11*j); s = (-1) ** j; ln = th*(0.42-0.05*j)
            d.line((tx, yb, tx+s*ln, yb-ln*0.8), BLACK)
    for px in [176, 190, 197, 236, 248, 300]:           # people, arms raised
        b = gy(px)+1; h = 13 if px != 197 else 8
        d.line((px, b, px, b-h), BLACK, 3); d.ellipse((px-2, b-h-5, px+2, b-h-1), fill=BLACK)
        d.line((px, b-h+2, px-5, b-h-5), BLACK); d.line((px, b-h+2, px+5, b-h-6), BLACK)
    d.text((W-8, H-15), "THE NIGHT THE STARS FELL · 13 NOV 1833", WHITE, font=font("mono", 10), anchor="ra")
    save(im, 1)

# ---------------------------------------------------------------- 2
def tunnel():
    im, d = new()
    cx, cy, R, Ri = 150, 150, 140, 124
    # river silt: brick-laid dashes outside the ring, left 300 px
    for y in range(0, H, 5):
        for x in range((y//5 % 2)*4 - 2, 300, 8):
            if math.hypot(x+1-cx, y-cy) > R+3: d.line((x, y, x+3, y), BLACK)
    d.ellipse((cx-R, cy-R, cx+R, cy+R), fill=BLACK)     # cast-iron ring
    for k in range(0, 360, 12):
        a = math.radians(k+6)
        d.line((cx+math.cos(a)*(Ri+1), cy+math.sin(a)*(Ri+1), cx+math.cos(a)*(R-2), cy+math.sin(a)*(R-2)), WHITE)
    d.ellipse((cx-R+7, cy-R+7, cx+R-7, cy+R-7), outline=WHITE)
    d.ellipse((cx-Ri, cy-Ri, cx+Ri, cy+Ri), fill=WHITE)
    yc, yr = 82, 212                                     # ceiling slab, road slab
    chord = lambda y: math.sqrt(max(Ri*Ri-(y-cy)**2, 0))
    # exhaust duct, red
    mask = Image.new("1", (W, H), 0); md = ImageDraw.Draw(mask)
    md.ellipse((cx-Ri, cy-Ri, cx+Ri, cy+Ri), fill=1); md.rectangle((0, yc, W, H), fill=0)
    im.paste(RED, (0, 0), mask); d = ImageDraw.Draw(im); d.fontmode = "1"
    d.rectangle((cx-chord(yc), yc, cx+chord(yc), yc+6), fill=BLACK)
    d.rectangle((cx-chord(yr), yr, cx+chord(yr), yr+8), fill=BLACK)
    for x in (cx-60, cx, cx+60):                          # ceiling ports
        d.rectangle((x-7, yc, x+7, yc+6), fill=WHITE)
    def arrow(x, y0, y1, col, wd=2):
        d.line((x, y0, x, y1), col, wd); s = 1 if y1 < y0 else -1
        d.polygon([(x-5, y1+s*7), (x+5, y1+s*7), (x, y1-s*1)], fill=col)
    for x in (cx-60, cx, cx+60): arrow(x, yc+22, yc-18, BLACK if False else WHITE) if False else None
    for x in (cx-60, cx, cx+60):
        d.line((x, yc+26, x, yc+9), BLACK, 2); arrow(x, yc-4, yc-22, WHITE)
        d.polygon([(x-5, yc+15), (x+5, yc+15), (x, yc+8)], fill=BLACK)
    # fresh-air duct under the road, slots at the kerbs
    for s in (-1, 1):
        kx = cx + s*(chord(yr)-22)
        d.rectangle((kx-4, yr, kx+4, yr+8), fill=WHITE)
        d.rectangle((kx-8 if s < 0 else kx+5, yr-7, kx-5 if s < 0 else kx+8, yr), fill=BLACK)   # kerb
        arrow(kx, yr+20, yr-12, BLACK)
    for x in (cx-36, cx, cx+36):
        d.line((x-12, 254, x+12, 254), BLACK, 2)
        sgn = -1 if x < cx else 1
        if x != cx: d.polygon([(x+sgn*12, 249), (x+sgn*12, 259), (x+sgn*20, 254)], fill=BLACK)
    # two motor-cars of 1927, seen from behind
    def car(x, tall=0):
        b = yr; top = b-74-tall
        d.rectangle((x-27, b-14, x-20, b), fill=BLACK); d.rectangle((x+20, b-14, x+27, b), fill=BLACK)  # tyres
        d.rectangle((x-24, b-22, x+24, b-9), fill=BLACK)                      # chassis
        d.rounded_rectangle((x-22, top, x+22, b-18), 6, fill=BLACK)             # body
        d.rounded_rectangle((x-15, top+8, x+15, top+26), 3, fill=WHITE)         # rear window
        d.rectangle((x-10, b-38, x+10, b-24), outline=WHITE)                    # trunk
        d.ellipse((x+12, b-30, x+17, b-25), fill=RED)                           # tail lamp
        d.ellipse((x-6, b-52, x+6, b-40), outline=WHITE)                        # spare
    car(cx-54); car(cx+54, 6)
    d.line((cx, yr-2, cx, yr-1), BLACK)
    for y in range(yc+34, yr-6, 12): d.line((cx, y, cx, y+5), BLACK)             # lane line
    # title block
    d.rectangle((300, 0, W, H), fill=WHITE); d.line((303, 6, 303, H-7), BLACK)
    fb, fm, fs = font("black", 18), font("monob", 10), font("mono", 10)
    d.text((310, 8), "HOLLAND", BLACK, font=fb); d.text((310, 27), "TUNNEL", BLACK, font=fb)
    d.line((311, 51, 392, 51), BLACK, 2)
    y = 56
    for t, fnt, col in [("one tube,", fs, BLACK), ("in section", fs, BLACK), ("", fs, BLACK),
                        ("OPENED", fm, BLACK), ("13 NOV 1927", fm, RED), ("", fs, BLACK),
                        ("84 fans:", fs, BLACK), ("42 blow in", fs, BLACK), ("under the", fs, BLACK), ("road,", fs, BLACK),
                        ("42 draw out", fs, BLACK), ("above the", fs, BLACK), ("ceiling.", fs, BLACK), ("", fs, BLACK),
                        ("All the air", fs, BLACK), ("is changed", fs, BLACK), ("every", fs, BLACK)]:
        d.text((311, y), t, col, font=fnt); y += 11 if t else 5
    d.text((310, y), "90 s", RED, font=font("black", 28)); y += 36
    d.text((311, y), "ventilation:", fs and BLACK, font=fs); d.text((311, y+12), "O. SINGSTAD", BLACK, font=fm)
    # callouts
    d.rectangle((cx-34, 36, cx+34, 50), fill=RED); d.text((cx, 43), "FOUL AIR", WHITE, font=fm, anchor="mm")
    d.text((cx, 238), "FRESH AIR", BLACK, font=fm, anchor="mm")
    save(im, 2)

# ---------------------------------------------------------------- 3
def treasure():
    rnd = random.Random(1850); im, d = new()
    cx, cy = 178, 150
    def rad(t):
        r = 92 + 20*math.sin(2*t+0.6) + 13*math.sin(3*t+2.1) + 7*math.sin(5*t+0.4) + 4*math.sin(9*t+1.3) + 2.5*math.sin(17*t)
        r -= 50*math.exp(-((math.atan2(math.sin(t-1.25), math.cos(t-1.25)))/0.26)**2)    # south anchorage
        r -= 30*math.exp(-((math.atan2(math.sin(t+1.75), math.cos(t+1.75)))/0.12)**2)    # north inlet
        return r
    coast = [(cx+math.cos(t)*rad(t)*1.25, cy+math.sin(t)*rad(t)*0.92) for t in np.linspace(0, 2*math.pi, 720, endpoint=False)]
    isl = Image.new("L", (W, H), 0); ImageDraw.Draw(isl).polygon(coast, fill=255)
    ID = ImageDraw.Draw(isl); ID.ellipse((214, 252, 256, 270), fill=255)       # islet in the anchorage mouth
    ID.ellipse((24, 60, 34, 67), fill=255); ID.ellipse((330, 218, 338, 224), fill=255)
    a = np.asarray(isl) > 0
    near = np.asarray(isl.filter(ImageFilter.MaxFilter(15))) > 0
    far = np.asarray(isl.filter(ImageFilter.MaxFilter(27))) > 0
    px = im.load()
    # rhumb lines from the rose
    ox, oy = 52, 232
    for k in range(16):
        ang = k*math.pi/8
        for r in range(26, 520, 1):
            x, y = int(ox+math.cos(ang)*r), int(oy-math.sin(ang)*r)
            if 8 <= x < W-8 and 8 <= y < H-8 and not near[y, x] and (r//3) % 2 == 0: px[x, y] = BLACK
    # sea shading: horizontal lines hugging the coast
    for y in range(8, H-8):
        for x in range(8, W-8):
            if a[y, x]: continue
            if near[y, x] and y % 2 == 0: px[x, y] = BLACK
            elif far[y, x] and y % 4 == 0 and (x+y) % 7 < 5: px[x, y] = BLACK
    edge = a & ~np.asarray(isl.filter(ImageFilter.MinFilter(5))).astype(bool)
    for y, x in zip(*np.nonzero(edge)): px[int(x), int(y)] = BLACK
    d = ImageDraw.Draw(im); d.fontmode = "1"
    def hill(x, y, w, h):
        for i in range(-w, w+1, 3):
            top = y - h*math.exp(-(i/(w*0.5))**2)
            d.line((x+i, top, x+i*1.35, y+2+rnd.random()*2), BLACK)
        d.line([(x+i, y - h*math.exp(-(i/(w*0.5))**2)) for i in range(-w, w+1, 2)], BLACK)
    def tree(x, y):
        d.line((x, y, x, y-3), BLACK); d.ellipse((x-2, y-8, x+2, y-3), outline=BLACK)
    def marsh(x, y):
        d.line((x-4, y, x+4, y), BLACK); [d.line((x+i, y, x+i, y-3), BLACK) for i in (-2, 0, 2)]
    hill(138, 112, 24, 22); hill(236, 150, 20, 15); hill(118, 178, 16, 11)
    for _ in range(46):
        x, y = rnd.randint(80, 300), rnd.randint(80, 215)
        if a[y-12:y+5, x-6:x+7].all() and not (112 < x < 166 and 86 < y < 118) and not (196 < x < 262 and 126 < y < 156) \
           and math.hypot(x-200, y-110) > 30 and not (175 < x < 250 and 160 < y < 230) and not (100 < x < 140 and 162 < y < 196): tree(x, y)
    for x, y in [(268, 184), (280, 190), (262, 194), (290, 182), (276, 200)]: marsh(x, y)
    fi, fs = font("ital", 13), font("ital", 12)
    def label(x, y, t, f=fi, anchor="mm", land=False):
        b = d.textbbox((x, y), t, font=f, anchor=anchor)
        d.rectangle((b[0]-2, b[1]-1, b[2]+2, b[3]+1), fill=WHITE); d.text((x, y), t, BLACK, font=f, anchor=anchor)
    label(138, 126, "Spy-glass Hill"); label(238, 162, "Mizzen-mast", fs); label(118, 190, "Fore-mast", fs)
    label(132, 252, "Capt. Kidd's"); label(132, 265, "Anchorage", fs)
    label(326, 78, "North Inlet", fs); label(290, 262, "Skeleton I.", fs); label(48, 52, "White Rock", fs)
    label(350, 236, "foul ground", fs); label(300, 172, "swamp", fs)
    def cross(x, y, s=5):
        d.line((x-s, y-s, x+s, y+s), RED, 3); d.line((x-s, y+s, x+s, y-s), RED, 3)
    cross(200, 110, 6); cross(288, 140, 4); cross(160, 160, 4)
    for i in range(7): d.line((200+i*4+7, 110-i*2-3, 200+i*4+9, 110-i*2-4), RED)       # dotted track from the cross
    # ship in the anchorage
    sx, sy = 210, 212
    d.polygon([(sx-9, sy), (sx+9, sy), (sx+6, sy+4), (sx-6, sy+4)], fill=BLACK)
    for mx in (-4, 3): d.line((sx+mx, sy, sx+mx, sy-13), BLACK); d.polygon([(sx+mx+1, sy-12), (sx+mx+6, sy-7), (sx+mx+1, sy-3)], fill=BLACK)
    # compass rose
    d.ellipse((ox-24, oy-24, ox+24, oy+24), fill=WHITE, outline=BLACK); d.ellipse((ox-20, oy-20, ox+20, oy+20), outline=BLACK)
    for k in range(8):
        ang = k*math.pi/4; L = 20 if k % 2 == 0 else 12
        tip = (ox+math.sin(ang)*L, oy-math.cos(ang)*L)
        l = (ox+math.sin(ang-1.2)*4, oy-math.cos(ang-1.2)*4); r = (ox+math.sin(ang+1.2)*4, oy-math.cos(ang+1.2)*4)
        d.polygon([tip, l, (ox, oy)], fill=RED if k == 0 else BLACK); d.polygon([tip, r, (ox, oy)], fill=WHITE, outline=BLACK)
    d.polygon([(ox, oy-36), (ox-4, oy-26), (ox+4, oy-26)], fill=RED); d.text((ox, oy-44), "N", BLACK, font=font("serifb", 12), anchor="mm")
    # neatline with graduations
    d.rectangle((2, 2, W-3, H-3), outline=BLACK); d.rectangle((7, 7, W-8, H-8), outline=BLACK)
    for x in range(7, W-8, 10):
        if (x//10) % 2: d.rectangle((x, 3, x+9, 6), fill=BLACK); d.rectangle((x, H-7, x+9, H-4), fill=BLACK)
    for y in range(7, H-8, 10):
        if (y//10) % 2: d.rectangle((3, y, 6, y+9), fill=BLACK); d.rectangle((W-7, y, W-4, y+9), fill=BLACK)
    # cartouche
    d.rectangle((258, 14, 386, 62), fill=WHITE, outline=BLACK); d.rectangle((261, 17, 383, 59), outline=BLACK)
    d.text((322, 27), "TREASURE ISLAND", BLACK, font=font("serifb", 12), anchor="mm")
    d.text((322, 40), "the map came first, 1881", BLACK, font=fs, anchor="mm")
    d.text((322, 52), "R.L.S. born 13 Nov. 1850", RED, font=fs, anchor="mm")
    save(im, 3)

# ---------------------------------------------------------------- 4
def leaf():
    im, d = new()
    d.rectangle((0, 0, W, 27), fill=BLACK)                       # tin binder
    for x in (60, 200, 340):
        d.ellipse((x-5, 8, x+5, 18), fill=WHITE); d.ellipse((x-2, 11, x+2, 15), fill=BLACK)
    rnd = random.Random(13); pts = [(0, 27)]                     # stubs of the days already torn off
    x = 0
    while x < W:
        x += rnd.randint(3, 9); pts.append((x, 31+rnd.randint(0, 5)))
    pts += [(W, 27)]
    d.polygon(pts, fill=WHITE, outline=BLACK); d.line(pts[1:-1], BLACK)
    for y in (29, 31): d.line((0, y, W, y), BLACK) if y == 29 else None
    d.line((0, 42, W, 42), BLACK)
    fB = font("black", 222)
    d.text((126, 176), "13", RED, font=fB, anchor="mm")
    d.text((14, 48), "NOVEMBER", BLACK, font=font("black", 24)); d.text((238, 50), "2026", BLACK, font=font("bold", 20), anchor="ra")
    d.text((126, 280), "F R I D A Y", BLACK, font=font("black", 24), anchor="mm")
    # right column: the 13th over any 400 Gregorian years
    x0 = 262; d.line((250, 50, 250, 290), BLACK)
    fm, fmb = font("mono", 10), font("monob", 10)
    d.text((x0, 50), "THE 13TH, IN ANY", BLACK, font=fmb); d.text((x0, 62), "400 YEARS, FALLS ON", BLACK, font=fmb)
    data = [("Mon", 685), ("Tue", 685), ("Wed", 687), ("Thu", 684), ("Fri", 688), ("Sat", 684), ("Sun", 687)]
    y = 82
    for nm, v in data:
        col = RED if nm == "Fri" else BLACK
        d.text((x0, y), nm, col, font=fmb); d.text((x0+26, y), str(v), col, font=fmb if nm == "Fri" else fm)
        d.rectangle((x0+52, y+2, x0+52+(v-680)*10, y+9), fill=col)
        y += 19
    d.line((x0+52, 78, x0+52, y-6), BLACK)
    d.text((x0+52, y-2), "680", BLACK, font=fm, anchor="ma"); d.text((x0+132, y-2), "688", BLACK, font=fm, anchor="ra")
    d.line((x0, 238, W-12, 238), BLACK)
    for i, t in enumerate(["Friday, most of all.", "Day 317 · 48 to come", "3rd & last of 2026"]):
        d.text((x0, 244+i*13), t, RED if i == 0 else BLACK, font=fmb if i == 0 else fm)
    save(im, 4)

# ---------------------------------------------------------------- 5
def field():
    """Positions from PyEphem for 2026-11-14 05:00 UT (precomputed):
    Jupiter 9h52m54.7s +13d38.5' mag -1.9 ; Mars 9h51m36.3s +14d58.9' mag +0.7 ; separation 1.38 deg."""
    im, d = new()
    cx, cy, R = 200, 146, 132; s = 2*R/6.0                       # a 6-degree field
    d.ellipse((cx-R, cy-R, cx+R, cy+R), fill=BLACK)
    hms = lambda h, m, sec: (h + m/60 + sec/3600)*15
    ra0, de0 = hms(9, 52, 0), 14.1
    def xy(ra, de): return cx - (ra-ra0)*math.cos(math.radians(de0))*s, cy - (de-de0)*s
    jx, jy = xy(hms(9, 52, 54.7), 13+38.5/60); mx, my = xy(hms(9, 51, 36.3), 14+58.9/60)
    for (ra, de, nm) in [(hms(9, 58, 13), 12+27/60, "ν"), (hms(9, 43, 44), 14+1/60, "ψ")]:    # nu and psi Leonis, 5th mag
        x, y = xy(ra, de); d.rectangle((x-1, y-1, x, y), fill=WHITE); d.text((x+6, y-7), nm, WHITE, font=font("sans", 11))
    d.ellipse((jx-6, jy-6, jx+6, jy+6), fill=WHITE)
    d.ellipse((mx-4, my-4, mx+4, my+4), fill=RED)
    fm, fmb = font("mono", 10), font("monob", 10)
    d.text((jx+14, jy-6), "Jupiter", WHITE, font=fmb); d.text((mx+12, my-6), "Mars", WHITE, font=fmb)
    # the gap, measured
    d.line((jx-16, jy, jx-22, jy), WHITE); d.line((mx-16, my, mx-22, my), WHITE); d.line((mx-19, my, jx-19, jy), WHITE)
    d.text((min(jx, mx)-26, (jy+my)/2-6), "1.4°", WHITE, font=fmb, anchor="ra")
    d.text((6, 6), "ONE BINOCULAR", BLACK, font=fmb); d.text((6, 18), "FIELD, 6°", BLACK, font=fmb)
    d.text((W-6, 6), "LEO", BLACK, font=fmb, anchor="ra"); d.text((W-6, 18), "N up, E left", BLACK, font=fm, anchor="ra")
    d.text((6, H-28), "before dawn,", BLACK, font=fm); d.text((6, H-16), "Sat 14 Nov 2026", BLACK, font=fmb)
    d.text((W-6, H-28), "closest on", BLACK, font=fm, anchor="ra"); d.text((W-6, H-16), "the 16th: 1.2°", RED, font=fmb, anchor="ra")
    save(im, 5)

if __name__ == "__main__":
    stars_fell(); tunnel(); treasure(); leaf(); field()
