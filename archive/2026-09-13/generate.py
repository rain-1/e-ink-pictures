#!/usr/bin/env python3
"""
2026-09-13 — five pictures for a 400x300 black/white/red e-ink screen.

1. ЛУНА 2      — constructivist poster: the red wedge that reached the Moon (13 Sep 1959)
2. Chladni     — a vibrating-plate specimen sheet, nodal lines in red
3. Kamon       — three family crests grown from circles and straight lines
4. Dusk, west  — tomorrow's crescent Moon beside Venus, low in the west
5. 502 gulls   — a giant peach airborne for Roald Dahl's 110th birthday

Run from the repo root:  python3 archive/2026-09-13/generate.py
Writes images/1.png … 5.png and archive/2026-09-13/1.png … 5.png
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3                       # supersampling factor for antialiased pieces
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
PALETTE = [0, 0, 0, 255, 255, 255, 255, 0, 0]

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIRS = [os.path.join(ROOT, "images"), os.path.dirname(os.path.abspath(__file__))]

FONT_DIR = "/usr/share/fonts/truetype"
def font(name, size):
    paths = {
        "sans": f"{FONT_DIR}/dejavu/DejaVuSans.ttf",
        "sansb": f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf",
        "mono": f"{FONT_DIR}/dejavu/DejaVuSansMono.ttf",
        "monob": f"{FONT_DIR}/dejavu/DejaVuSansMono-Bold.ttf",
        "serif": f"{FONT_DIR}/dejavu/DejaVuSerif.ttf",
        "serifb": f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf",
        "jp": f"{FONT_DIR}/fonts-japanese-gothic.ttf",
        "free": f"{FONT_DIR}/freefont/FreeSansBold.ttf",
    }
    return ImageFont.truetype(paths[name], size)


# ----------------------------------------------------------------------------
# palette plumbing
# ----------------------------------------------------------------------------
def pal_image():
    p = Image.new("P", (1, 1))
    p.putpalette(PALETTE + [0, 0, 0] * 253)
    return p

def to_screen(img, dither=True):
    """RGB image (any size) -> 400x300 mode-P PNG with the exact 3-colour palette."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    q = img.convert("RGB").quantize(
        palette=pal_image(),
        dither=Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE)
    # quantize keeps the palette order we gave it, but rebuild to be certain
    idx = np.array(q)
    src_pal = q.getpalette()[:9]
    src = [tuple(src_pal[i*3:i*3+3]) for i in range(3)]
    remap = {i: [BLACK, WHITE, RED].index(c) for i, c in enumerate(src)}
    out = np.vectorize(remap.get)(idx).astype(np.uint8)
    im = Image.fromarray(out, "P")
    im.putpalette(PALETTE + [0, 0, 0] * 253)
    return im

def save(im, n):
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        im.save(os.path.join(d, f"{n}.png"), optimize=True)

def caption(draw, text, scale=1, fill=BLACK, y=None, x=8, fnt="mono", size=11):
    f = font(fnt, size * scale)
    if y is None:
        y = (H - 16) * scale
    draw.text((x * scale, y), text, font=f, fill=fill)


# ----------------------------------------------------------------------------
# 1. ЛУНА 2 — the red wedge that reached the Moon
# ----------------------------------------------------------------------------
def piece_luna2():
    s = S
    im = Image.new("RGB", (W*s, H*s), WHITE)
    d = ImageDraw.Draw(im)

    # black ground on the right, cut by a diagonal — the Proun space
    d.polygon([(190*s, 0), (W*s, 0), (W*s, H*s), (120*s, H*s)], fill=BLACK)

    # the Moon: a white disc sitting on the black field
    cx, cy, R = 272, 138, 96
    d.ellipse([(cx-R)*s, (cy-R)*s, (cx+R)*s, (cy+R)*s], fill=WHITE)
    # three craters that bracket the impact site (Palus Putredinis):
    # Archimedes (large), Aristillus, Autolycus  — laid out roughly as on the Moon
    for (ox, oy, r) in [(-30, 12, 17), (10, -22, 9), (14, 2, 7)]:
        d.ellipse([(cx+ox-r)*s, (cy+oy-r)*s, (cx+ox+r)*s, (cy+oy+r)*s],
                  outline=BLACK, width=2*s)
    # a thin black ring at the terminator to give the disc some spin
    d.arc([(cx-R+6)*s, (cy-R+6)*s, (cx+R-6)*s, (cy+R-6)*s], 200, 330, fill=BLACK, width=1*s)

    # the red wedge, from the lower-left corner to the impact point
    tip = (cx - 6, cy - 6)
    base_a, base_b = (-10, 300), (70, 316)
    d.polygon([(base_a[0]*s, base_a[1]*s), (base_b[0]*s, base_b[1]*s), (tip[0]*s, tip[1]*s)], fill=RED)
    # a thin white seam down the wedge's spine so it reads on the black field
    mid = ((base_a[0]+base_b[0])/2, (base_a[1]+base_b[1])/2)
    d.line([(mid[0]*s, mid[1]*s), (tip[0]*s, tip[1]*s)], fill=WHITE, width=1*s)
    # impact flash: a small red disc with a white pinprick
    d.ellipse([(tip[0]-5)*s, (tip[1]-5)*s, (tip[0]+5)*s, (tip[1]+5)*s], fill=RED)
    d.ellipse([(tip[0]-1)*s, (tip[1]-1)*s, (tip[0]+1)*s, (tip[1]+1)*s], fill=WHITE)

    # parallel black speed-lines echoing the wedge (constructivist ruling)
    ang = math.atan2(tip[1]-mid[1], tip[0]-mid[0])
    for k in range(1, 5):
        off = 22 * k
        ox, oy = -math.sin(ang)*off, math.cos(ang)*off
        x0, y0 = mid[0]+ox*1.6, mid[1]+oy*1.6
        x1, y1 = x0 + math.cos(ang)*(90 - 10*k), y0 + math.sin(ang)*(90 - 10*k)
        d.line([(x0*s, y0*s), (x1*s, y1*s)], fill=BLACK, width=(5-k)*s)

    # a floating red bar and a small black square — Lissitzky furniture
    d.rectangle([300*s, 232*s, 392*s, 240*s], fill=RED)
    d.rectangle([378*s, 22*s, 392*s, 36*s], fill=WHITE)
    d.rectangle([362*s, 30*s, 372*s, 40*s], fill=RED)

    # typography
    d.text((14*s, 14*s), "ЛУНА", font=font("sansb", 46*s), fill=BLACK)
    tw = d.textlength("ЛУНА ", font=font("sansb", 46*s))
    d.text((14*s + tw, 14*s), "2", font=font("sansb", 46*s), fill=RED)
    d.text((16*s, 66*s), "13·IX·1959  21:02 UT", font=font("monob", 11*s), fill=BLACK)
    d.text((16*s, 82*s), "first thing we ever made", font=font("mono", 9*s), fill=BLACK)
    d.text((16*s, 94*s), "to touch another world", font=font("mono", 9*s), fill=BLACK)
    # small white labels on the black field
    d.text((312*s, 258*s), "Palus", font=font("mono", 9*s), fill=WHITE)
    d.text((312*s, 270*s), "Putredinis", font=font("mono", 9*s), fill=WHITE)

    return to_screen(im, dither=False)


# ----------------------------------------------------------------------------
# 2. Chladni figures — specimen sheet
# ----------------------------------------------------------------------------
def chladni_field(n, m, size):
    t = np.linspace(-1, 1, size)
    x, y = np.meshgrid(t, t)
    return (np.cos(n*math.pi*x)*np.cos(m*math.pi*y)
            - np.cos(m*math.pi*x)*np.cos(n*math.pi*y))

def nodal_mask(f, thick=1):
    sx = np.sign(f)
    e = np.zeros_like(f, dtype=bool)
    e[:, 1:] |= sx[:, 1:] != sx[:, :-1]
    e[1:, :] |= sx[1:, :] != sx[:-1, :]
    for _ in range(thick - 1):
        e2 = e.copy()
        e2[1:, :] |= e[:-1, :]; e2[:-1, :] |= e[1:, :]
        e2[:, 1:] |= e[:, :-1]; e2[:, :-1] |= e[:, 1:]
        e = e2
    return e

def piece_chladni():
    rng = random.Random(20260913)
    canvas = np.zeros((H, W, 3), dtype=np.uint8) + 255

    # main plate: black/white sign regions, red nodal lines
    n, m = 5, 2
    P = 236
    f = chladni_field(n, m, P)
    plate = np.where(f[..., None] > 0, 255, 0).astype(np.uint8).repeat(3, axis=2)
    e = nodal_mask(f, thick=2)
    plate[e] = RED
    px, py = 14, 14
    canvas[py:py+P, px:px+P] = plate
    # frame
    canvas[py-2:py, px-2:px+P+2] = 0; canvas[py+P:py+P+2, px-2:px+P+2] = 0
    canvas[py-2:py+P+2, px-2:px] = 0; canvas[py-2:py+P+2, px+P:px+P+2] = 0

    # right column: four small plates, black lines on white, one red
    modes = [(1, 2), (2, 3), (3, 4), (1, 5)]
    sz = 52
    for i, (a, b) in enumerate(modes):
        g = chladni_field(a, b, sz)
        e = nodal_mask(g, thick=1)
        tile = np.full((sz, sz, 3), 255, dtype=np.uint8)
        tile[e] = RED if i == 1 else BLACK
        tx, ty = 292, 14 + i*60
        canvas[ty:ty+sz, tx:tx+sz] = tile
        canvas[ty-1:ty, tx-1:tx+sz+1] = 0; canvas[ty+sz:ty+sz+1, tx-1:tx+sz+1] = 0
        canvas[ty-1:ty+sz+1, tx-1:tx] = 0; canvas[ty-1:ty+sz+1, tx+sz:tx+sz+1] = 0

    im = Image.fromarray(canvas, "RGB")
    d = ImageDraw.Draw(im)
    for i, (a, b) in enumerate(modes):
        d.text((350, 14 + i*60 + 4), f"({a},{b})", font=font("mono", 10), fill=BLACK)
    d.text((262, 14), "n", font=font("mono", 10), fill=BLACK)
    d.text((262, 26), "m", font=font("mono", 10), fill=BLACK)
    d.text((262, 40), f"{n}", font=font("monob", 16), fill=RED)
    d.text((262, 58), f"{m}", font=font("monob", 16), fill=RED)
    d.text((14, 258), "CHLADNI FIGURES", font=font("sansb", 15), fill=BLACK)
    d.text((14, 276), "sand settles where the plate stands still:", font=font("mono", 9), fill=BLACK)
    d.text((14, 287), "cos(nπx)cos(mπy) − cos(mπx)cos(nπy) = 0", font=font("mono", 9), fill=BLACK)
    d.text((262, 270), "E.F.F. Chladni", font=font("mono", 9), fill=BLACK)
    d.text((262, 282), "1787", font=font("mono", 9), fill=RED)
    return to_screen(im, dither=False)


# ----------------------------------------------------------------------------
# 3. Kamon — three crests from circles and straight lines
# ----------------------------------------------------------------------------
def rot(pts, ang, cx, cy):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x*ca - y*sa, cy + x*sa + y*ca) for x, y in pts]

def ellipse_pts(a, b, k=48):
    return [(a*math.cos(2*math.pi*i/k), b*math.sin(2*math.pi*i/k)) for i in range(k)]

def draw_crest(d, cx, cy, R, n, style, rng, s):
    """A maru-ni (inside-a-circle) crest with n-fold symmetry."""
    # outer ring
    ring_w = rng.choice([4, 7, 10])
    d.ellipse([(cx-R)*s, (cy-R)*s, (cx+R)*s, (cy+R)*s], fill=BLACK)
    d.ellipse([(cx-R+ring_w)*s, (cy-R+ring_w)*s, (cx+R-ring_w)*s, (cy+R-ring_w)*s], fill=WHITE)
    r_in = R - ring_w - 6

    if style == "petals":
        # n petals: ellipses whose far end touches the inner circle
        pl, pw = r_in*0.98, r_in*0.36
        for i in range(n):
            a = 2*math.pi*i/n - math.pi/2
            pts = [(x + pl/2, y) for x, y in ellipse_pts(pl/2, pw)]
            d.polygon([(x*s, y*s) for x, y in rot(pts, a, cx, cy)], fill=BLACK)
        # white vein down each petal
        for i in range(n):
            a = 2*math.pi*i/n - math.pi/2
            p0, p1 = rot([(r_in*0.25, 0), (r_in*0.9, 0)], a, cx, cy)
            d.line([(p0[0]*s, p0[1]*s), (p1[0]*s, p1[1]*s)], fill=WHITE, width=max(1, int(2*s)))
        # heart
        hr = r_in*0.22
        d.ellipse([(cx-hr)*s, (cy-hr)*s, (cx+hr)*s, (cy+hr)*s], fill=RED)
        d.ellipse([(cx-hr*0.45)*s, (cy-hr*0.45)*s, (cx+hr*0.45)*s, (cy+hr*0.45)*s], fill=WHITE)

    elif style == "rings":
        # n interlocking small circles on the vertices of a polygon (like mitsu-wa)
        rr = r_in * (0.62 if n <= 4 else 0.5)
        sr = r_in - rr
        for i in range(n):
            a = 2*math.pi*i/n - math.pi/2
            x, y = cx + sr*math.cos(a), cy + sr*math.sin(a)
            d.ellipse([(x-rr)*s, (y-rr)*s, (x+rr)*s, (y+rr)*s], outline=BLACK, width=int(rr*0.28*s))
        # red core where they overlap
        cr = r_in*0.16
        d.ellipse([(cx-cr)*s, (cy-cr)*s, (cx+cr)*s, (cy+cr)*s], fill=RED)

    elif style == "diamonds":
        # n rhombi radiating (like a stylised chrysanthemum / bishi)
        for i in range(n):
            a = 2*math.pi*i/n - math.pi/2
            L, Wd = r_in*0.96, r_in*0.30
            pts = [(r_in*0.12, 0), (L*0.55, -Wd), (L, 0), (L*0.55, Wd)]
            d.polygon([(x*s, y*s) for x, y in rot(pts, a, cx, cy)], fill=BLACK)
        for i in range(n):
            a = 2*math.pi*(i+0.5)/n - math.pi/2
            L, Wd = r_in*0.62, r_in*0.14
            pts = [(r_in*0.2, 0), (L*0.55, -Wd), (L, 0), (L*0.55, Wd)]
            d.polygon([(x*s, y*s) for x, y in rot(pts, a, cx, cy)], fill=RED)
        cr = r_in*0.12
        d.ellipse([(cx-cr)*s, (cy-cr)*s, (cx+cr)*s, (cy+cr)*s], fill=WHITE)
        d.ellipse([(cx-cr)*s, (cy-cr)*s, (cx+cr)*s, (cy+cr)*s], outline=BLACK, width=int(2*s))

    elif style == "blades":
        # n curved blades (a windmill / kaze-guruma feeling), each a crescent
        for i in range(n):
            a = 2*math.pi*i/n
            k = 40
            outer = [(r_in*0.95*math.cos(a + t*(math.pi/n)*1.6), r_in*0.95*math.sin(a + t*(math.pi/n)*1.6))
                     for t in np.linspace(0, 1, k)]
            inner = [(r_in*0.3*math.cos(a + t*(math.pi/n)*1.6 + 0.35), r_in*0.3*math.sin(a + t*(math.pi/n)*1.6 + 0.35))
                     for t in np.linspace(1, 0, k)]
            pts = [(cx+x, cy+y) for x, y in outer + inner]
            d.polygon([(x*s, y*s) for x, y in pts], fill=BLACK if i % 2 == 0 or n % 2 else RED)
        cr = r_in*0.14
        d.ellipse([(cx-cr)*s, (cy-cr)*s, (cx+cr)*s, (cy+cr)*s], fill=WHITE)
        d.ellipse([(cx-cr*0.5)*s, (cy-cr*0.5)*s, (cx+cr*0.5)*s, (cy+cr*0.5)*s], fill=BLACK)

def piece_kamon():
    s = S
    rng = random.Random(2026_09_13)
    im = Image.new("RGB", (W*s, H*s), WHITE)
    d = ImageDraw.Draw(im)
    specs = [(72, 130, 56, 5, "petals"), (200, 130, 64, 8, "diamonds"), (328, 130, 56, 3, "rings")]
    for (cx, cy, R, n, style) in specs:
        draw_crest(d, cx, cy, R, n, style, rng, s)
    # a faint construction line: the horizon the three sit on
    d.line([(20*s, 200*s), (380*s, 200*s)], fill=BLACK, width=1*s)
    # kanji title + notes
    d.text((20*s, 214*s), "家紋", font=font("jp", 30*s), fill=BLACK)
    d.text((86*s, 222*s), "three crests grown from circles & straight lines", font=font("mono", 10*s), fill=BLACK)
    d.text((86*s, 236*s), "5-fold petals · 8-fold bishi · 3 linked rings", font=font("mono", 10*s), fill=BLACK)
    d.text((20*s, 258*s), "maru-ni —  the motif is always placed inside a circle", font=font("mono", 9*s), fill=BLACK)
    d.text((20*s, 272*s), "(rules from the Heian Monkan, the old crest-drafting manual)", font=font("mono", 9*s), fill=BLACK)
    d.rectangle([362*s, 268*s, 380*s, 286*s], fill=RED)
    d.text((364*s, 270*s), "紋", font=font("jp", 14*s), fill=WHITE)
    return to_screen(im, dither=False)


# ----------------------------------------------------------------------------
# 4. Dusk, west — tomorrow's crescent Moon beside Venus
# ----------------------------------------------------------------------------
def piece_dusk():
    s = S
    Ws, Hs = W*s, H*s
    # sky gradient: black at the top -> white at the horizon, with a red dusk band
    y = np.linspace(0, 1, Hs)[:, None]
    horizon = 0.72
    t = np.clip(y / horizon, 0, 1)
    lum = t**2.2                                  # dark aloft, bright low
    sky = np.stack([lum, lum, lum], axis=2)
    glow = np.exp(-((t - 0.95) / 0.16)**2)        # red glow just above the horizon
    sky[..., 0] = np.clip(sky[..., 0] + glow*0.7, 0, 1)
    sky[..., 1] = np.clip(sky[..., 1] - glow*0.30, 0, 1)
    sky[..., 2] = np.clip(sky[..., 2] - glow*0.45, 0, 1)
    arr = np.repeat(sky, Ws, axis=1)
    arr = (arr*255).astype(np.uint8)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # a few faint stars up top
    rng = random.Random(914)
    for _ in range(60):
        x, yy = rng.randrange(Ws), rng.randrange(int(Hs*0.45))
        d.ellipse([x-s, yy-s, x+s, yy+s], fill=WHITE)

    # the Moon: 16% waxing crescent, lit side facing the sunset (down-right)
    mx, my, mr = 232, 96, 34
    d.ellipse([(mx-mr)*s, (my-mr)*s, (mx+mr)*s, (my+mr)*s], fill=WHITE)
    # earthshine disc: subtract a shifted disc to leave a crescent
    off = mr*0.5
    ang = math.radians(-135)  # dark disc shifted up-left => lit crescent on the down-right
    ox, oy = mx + off*math.cos(ang), my + off*math.sin(ang)
    d.ellipse([(ox-mr)*s, (oy-mr)*s, (ox+mr)*s, (oy+mr)*s], fill=BLACK)
    # thin earthshine rim so the whole disc is felt
    d.ellipse([(mx-mr)*s, (my-mr)*s, (mx+mr)*s, (my+mr)*s], outline=(110, 110, 110), width=1*s)

    # Venus: a bold point with four spikes, down-left of the Moon
    vx, vy = 174, 150
    for (dx, dy, L) in [(1, 0, 16), (0, 1, 16), (1, 1, 7), (1, -1, 7)]:
        d.line([((vx-dx*L)*s, (vy-dy*L)*s), ((vx+dx*L)*s, (vy+dy*L)*s)], fill=WHITE, width=2*s)
    d.ellipse([(vx-5)*s, (vy-5)*s, (vx+5)*s, (vy+5)*s], fill=WHITE)
    d.ellipse([(vx-2)*s, (vy-2)*s, (vx+2)*s, (vy+2)*s], fill=RED)

    # hills and a lone tree, black silhouette
    hy = int(H*horizon)
    pts = [(0, hy+8)]
    for x in range(0, W+1, 8):
        h = 14*math.sin(x/61.0) + 8*math.sin(x/23.0 + 1.3) + 4*math.sin(x/9.0)
        pts.append((x, hy + 10 - h))
    pts += [(W, H), (0, H)]
    d.polygon([(x*s, yy*s) for x, yy in pts], fill=BLACK)
    # tree
    tx = 330; ty = hy + 10 - (14*math.sin(tx/61.0) + 8*math.sin(tx/23.0+1.3) + 4*math.sin(tx/9.0))
    d.line([(tx*s, ty*s), (tx*s, (ty-28)*s)], fill=BLACK, width=2*s)
    for (dy, r) in [(-26, 8), (-20, 11), (-13, 13)]:
        d.ellipse([(tx-r)*s, (ty+dy-r*0.55)*s, (tx+r)*s, (ty+dy+r*0.55)*s], fill=BLACK)

    # text: on the black ground at the bottom
    d.text((14*s, (H-56)*s), "TOMORROW · 14 SEP · WEST · after sunset", font=font("monob", 11*s), fill=WHITE)
    d.text((14*s, (H-40)*s), "Moon 16% crescent  ⟷  Venus, mag −4.5", font=font("mono", 10*s), fill=WHITE)
    d.text((14*s, (H-26)*s), "22 Sep Venus brightest · 23 Sep equinox 00:05 UT", font=font("mono", 9*s), fill=WHITE)
    d.text((14*s, (H-14)*s), "25 Sep 十五夜 Tsukimi · 27 Sep Harvest Moon", font=font("jp", 9*s), fill=RED)
    # labels near the objects
    d.text(((mx+40)*s, (my-10)*s), "Moon", font=font("mono", 9*s), fill=WHITE)
    d.text(((vx-30)*s, (vy+18)*s), "Venus", font=font("mono", 9*s), fill=WHITE)
    return to_screen(im, dither=True)


# ----------------------------------------------------------------------------
# 5. 502 gulls — a giant peach for Roald Dahl's 110th birthday
# ----------------------------------------------------------------------------
def piece_peach():
    s = S
    rng = random.Random(1916_09_13)
    im = Image.new("RGB", (W*s, H*s), WHITE)
    d = ImageDraw.Draw(im)

    # sea at the bottom, dithered mid-grey with white wave lines
    sea_top = 250
    d.rectangle([0, sea_top*s, W*s, H*s], fill=(70, 70, 70))
    for i in range(7):
        yy = sea_top + 6 + i*6
        for x in range(0, W, 26):
            d.arc([(x + (i%2)*13)*s, (yy-4)*s, (x + 26 + (i%2)*13)*s, (yy+4)*s], 200, 340, fill=WHITE, width=1*s)
    # shark fin
    d.polygon([(60*s, (sea_top+4)*s), (78*s, (sea_top-14)*s), (84*s, (sea_top+4)*s)], fill=BLACK)

    # the peach: red disc with a black-shaded far side (red->black dither) and a cleft
    px, py, pr = 200, 168, 74
    # radial shading via numpy then paste through a circular mask
    yy, xx = np.mgrid[0:2*pr*s, 0:2*pr*s]
    dx, dy = (xx - pr*s)/(pr*s), (yy - pr*s)/(pr*s)
    rr = np.sqrt(dx*dx + dy*dy)
    light = np.clip(1.0 - 0.9*np.clip((dx*0.75 + dy*0.6 + 0.35), 0, 1.4), 0.08, 1.0)
    red = np.zeros((2*pr*s, 2*pr*s, 3))
    red[..., 0] = light
    peach = Image.fromarray((red*255).astype(np.uint8), "RGB")
    mask = Image.fromarray(((rr <= 1.0)*255).astype(np.uint8), "L")
    im.paste(peach, ((px-pr)*s, (py-pr)*s), mask)
    # a highlight in white
    d.ellipse([(px-38)*s, (py-40)*s, (px-16)*s, (py-24)*s], fill=(255, 190, 190))
    # the cleft: a curved black line
    d.arc([(px-10)*s, (py-pr)*s, (px+40)*s, (py+pr*0.6)*s], 95, 250, fill=BLACK, width=3*s)
    # stem and leaf
    d.line([(px*s, (py-pr+4)*s), ((px+4)*s, (py-pr-10)*s)], fill=BLACK, width=3*s)
    leaf = [(0, 0), (14, -10), (34, -8), (24, 6), (8, 8)]
    d.polygon([((px+4+x)*s, (py-pr-8+y)*s) for x, y in leaf], fill=BLACK)

    # strings from the stem to a sky full of gulls
    gulls = []
    for i in range(96):
        gx = rng.uniform(12, W-12)
        gy = rng.uniform(10, 80) + 0.0009*(gx-200)**2*0.6
        gulls.append((gx, gy))
    for gx, gy in gulls:
        d.line([((px+2)*s, (py-pr-4)*s), (gx*s, (gy+3)*s)], fill=(120, 120, 120), width=1)
    for gx, gy in gulls:
        w = rng.uniform(4, 7)
        d.arc([(gx-w)*s, (gy-3)*s, gx*s, (gy+3)*s], 200, 340, fill=BLACK, width=2*s)
        d.arc([gx*s, (gy-3)*s, (gx+w)*s, (gy+3)*s], 200, 340, fill=BLACK, width=2*s)

    # text
    d.text((14*s, 182*s), "502", font=font("serifb", 40*s), fill=BLACK)
    d.text((16*s, 228*s), "seagulls", font=font("serif", 13*s), fill=BLACK)
    d.text((286*s, 196*s), "ROALD DAHL", font=font("sansb", 12*s), fill=BLACK)
    d.text((286*s, 212*s), "b. 13 Sept 1916", font=font("mono", 9*s), fill=BLACK)
    d.text((286*s, 226*s), "110 years today", font=font("mono", 9*s), fill=RED)
    d.rectangle([0, (H-16)*s, W*s, H*s], fill=BLACK)
    d.text((14*s, (H-13)*s), "the peach crossed the Atlantic and came to rest on a New York needle", font=font("mono", 8*s), fill=WHITE)
    return to_screen(im, dither=True)


if __name__ == "__main__":
    for i, fn in enumerate([piece_luna2, piece_chladni, piece_kamon, piece_dusk, piece_peach], 1):
        save(fn(), i)
        print("wrote", i)
