#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-07-12.

July 12 is a strange attractor for birthdays: Julius Caesar (100 BC),
Henry David Thoreau (1817), Buckminster Fuller (1895), Pablo Neruda (1904).
Also the Etch A Sketch went on sale July 12, 1960, and the new supermoon
is two days away (Jul 14, 09:44 UTC).

Five 400x300 images in exactly three colors (white, black, red).
Tonal scenes render at 3x with AA then Floyd-Steinberg dither into the
palette; hard-edged pieces render at 1x in pure palette colors.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED)
    palette += [0, 0, 0] * (256 - 3)
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=True):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def ctext(dr, xy, s, f, fill, anchor="mm"):
    dr.text(xy, s, font=f, fill=fill, anchor=anchor)


# ------------------------------------------------- 1. Geodesic (Fuller, b. 1895)
def image1_geodesic():
    """Wireframe geodesic sphere in the manner of the Montreal Biosphere,
    rising over a red sun. Icosahedron subdivided at frequency 4."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # --- build icosahedron
    phi = (1 + 5 ** 0.5) / 2
    verts = []
    for a, b in [(1, phi), (-1, phi), (1, -phi), (-1, -phi)]:
        verts += [(a, b, 0), (0, a, b), (b, 0, a)]
    verts = [tuple(c / math.sqrt(1 + phi * phi) for c in v) for v in verts]

    def norm(v):
        l = math.sqrt(sum(c * c for c in v))
        return tuple(c / l for c in v)

    # faces by finding triangles of nearest neighbors (edge length of unit icosa)
    edge = 2 / math.sqrt(1 + phi * phi)
    n = len(verts)

    def d(i, j):
        return math.dist(verts[i], verts[j])

    faces = []
    for i in range(n):
        for j in range(i + 1, n):
            if abs(d(i, j) - edge) > 1e-6:
                continue
            for k in range(j + 1, n):
                if abs(d(i, k) - edge) < 1e-6 and abs(d(j, k) - edge) < 1e-6:
                    faces.append((i, j, k))

    # --- subdivide each face at frequency f, project to sphere, collect edges
    freq = 4
    edges = set()

    def key(p):
        return tuple(round(c, 6) for c in p)

    for (i, j, k) in faces:
        A, B, C = verts[i], verts[j], verts[k]
        grid = {}
        for r in range(freq + 1):
            for c in range(freq + 1 - r):
                a = r / freq
                b = c / freq
                g = 1 - a - b
                p = norm(tuple(A[t] * g + B[t] * a + C[t] * b for t in range(3)))
                grid[(r, c)] = p
        for r in range(freq + 1):
            for c in range(freq + 1 - r):
                for (r2, c2) in ((r + 1, c), (r, c + 1), (r + 1, c - 1)):
                    if (r2, c2) in grid:
                        e = tuple(sorted((key(grid[(r, c)]), key(grid[(r2, c2)]))))
                        edges.add(e)

    # --- rotate & orthographic projection
    rx, ry = 0.35, 0.55

    def rot(p):
        x, y, z = p
        y, z = y * math.cos(rx) - z * math.sin(rx), y * math.sin(rx) + z * math.cos(rx)
        x, z = x * math.cos(ry) + z * math.sin(ry), -x * math.sin(ry) + z * math.cos(ry)
        return x, y, z

    cx, cy, R = W * s * 0.5, H * s * 0.45, 105 * s

    def proj(p):
        x, y, z = rot(p)
        return cx + x * R, cy - y * R, z

    # red sun low behind the dome, partly clipped by horizon
    hy = int(H * s * 0.80)
    sun_r = 46 * s
    dr.ellipse([cx - 158 * s - sun_r, hy - 8 * s - sun_r,
                cx - 158 * s + sun_r, hy - 8 * s + sun_r], fill=RED)
    dr.rectangle([0, hy, W * s, H * s], fill=WHITE)
    dr.line([0, hy, W * s, hy], fill=BLACK, width=s)

    # back edges first (thin, gray -> dithers to sparse black)
    back, front = [], []
    for (p, q) in edges:
        x1, y1, z1 = proj(p)
        x2, y2, z2 = proj(q)
        (back if z1 + z2 < 0 else front).append((x1, y1, x2, y2))
    for x1, y1, x2, y2 in back:
        dr.line([x1, y1, x2, y2], fill=(185, 185, 185), width=s)
    for x1, y1, x2, y2 in front:
        dr.line([x1, y1, x2, y2], fill=BLACK, width=int(1.6 * s))

    # text
    f1 = font(FONT_SANS_B, 17 * s)
    f2 = font(FONT_SANS, 11 * s)
    ctext(dr, (W * s / 2, H * s * 0.875), "R. BUCKMINSTER FULLER", f1, BLACK)
    ctext(dr, (W * s / 2, H * s * 0.945),
          "b. July 12, 1895   ·   “We are all astronauts on Spaceship Earth”",
          f2, BLACK)
    return finalize(img)


# ------------------------------------------------- 2. Walden (Thoreau, b. 1817)
def image2_walden():
    """Walden Pond at dawn: pine woods, the one-room cabin, a red sun and its
    reflection broken on the water. Simplify, simplify."""
    rng = random.Random(18170712)
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    wl = int(H * s * 0.62)  # waterline

    # sky: gentle gradient, brightest at horizon
    for y in range(wl):
        v = 255 - int(46 * (1 - y / wl) ** 1.4)
        dr.line([0, y, W * s, y], fill=(v, v, v))

    # red sun
    scx, scy, sr = W * s * 0.70, H * s * 0.30, 34 * s
    dr.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=RED)

    # far shore treeline (soft dark gray band of bumps)
    tl = []
    y0 = wl - 26 * s
    x = 0
    while x <= W * s:
        y0 += rng.uniform(-3, 3) * s
        y0 = max(wl - 40 * s, min(wl - 12 * s, y0))
        tl.append((x, y0))
        x += 6 * s
    dr.polygon(tl + [(W * s, wl), (0, wl)], fill=(70, 70, 70))

    def pine(cx, base, h, w, ink):
        """simple layered pine silhouette"""
        layers = 4
        for i in range(layers):
            t = i / layers
            ly = base - h * t
            lw = w * (1 - t * 0.78)
            lh = h * 0.38
            dr.polygon([(cx - lw, ly), (cx + lw, ly), (cx, ly - lh)], fill=ink)
        dr.rectangle([cx - w * 0.08, base - h * 0.06, cx + w * 0.08, base], fill=ink)

    # near pines, left cluster
    for cx, hh in [(30, 105), (66, 140), (108, 120), (150, 88)]:
        pine(cx * s, wl, hh * s, (hh * 0.30) * s, BLACK)
    # one pine right
    pine(372 * s, wl, 118 * s, 34 * s, BLACK)

    # the cabin (right of center, on the shore)
    cbx, cby = W * s * 0.585, wl
    cw, ch = 52 * s, 34 * s
    dr.rectangle([cbx - cw / 2, cby - ch, cbx + cw / 2, cby], fill=BLACK)
    dr.polygon([(cbx - cw / 2 - 6 * s, cby - ch), (cbx + cw / 2 + 6 * s, cby - ch),
                (cbx, cby - ch - 24 * s)], fill=BLACK)
    # door + window in white outline
    dr.rectangle([cbx - 8 * s, cby - 20 * s, cbx + 8 * s, cby], outline=WHITE, width=s)
    # chimney
    dr.rectangle([cbx + cw * 0.22, cby - ch - 20 * s, cbx + cw * 0.22 + 7 * s, cby - ch], fill=BLACK)

    # water: white with horizontal ripple strokes; reflections
    dr.rectangle([0, wl, W * s, H * s], fill=(235, 235, 235))
    # sun reflection: broken red dashes widening downward
    for i, y in enumerate(range(wl + 4 * s, H * s - 30 * s, int(5.5 * s))):
        hw = (6 + i * 2.0) * s * rng.uniform(0.6, 1.15)
        off = rng.uniform(-6, 6) * s
        dr.line([scx - hw + off, y, scx + hw + off, y], fill=RED, width=int(2.2 * s))
    # dark ripples
    for i in range(150):
        y = wl + rng.random() ** 1.6 * (H * s - wl)
        x = rng.uniform(0, W * s)
        ln = rng.uniform(8, 46) * s * (0.4 + (y - wl) / (H * s - wl))
        v = rng.randint(90, 170)
        dr.line([x, y, x + ln, y], fill=(v, v, v), width=s)

    # quote panel bottom
    dr.rectangle([0, H * s - 27 * s, W * s, H * s], fill=WHITE)
    dr.line([0, H * s - 27 * s, W * s, H * s - 27 * s], fill=BLACK, width=s)
    fq = font(FONT_SERIF, 11 * s)
    ctext(dr, (W * s / 2, H * s - 13 * s),
          "“Simplify, simplify.”  —  H. D. Thoreau · b. July 12, 1817", fq, BLACK)
    return finalize(img)


# ------------------------------------------------- 3. Kamon sheet (generator)
def petal_poly(cx, cy, r0, ang, length, width):
    """polygon points of a petal: ellipse pointing outward at angle ang,
    inner tip at radius r0 from (cx,cy)."""
    pts = []
    ca, sa = math.cos(ang), math.sin(ang)
    for i in range(24):
        t = i / 24 * 2 * math.pi
        # ellipse in local coords, long axis +x
        ex = (1 - math.cos(t)) / 2 * length          # 0..length
        ey = math.sin(t) * width / 2
        x = cx + (r0 + ex) * ca - ey * sa
        y = cy + (r0 + ex) * sa + ey * ca
        pts.append((x, y))
    return pts


def draw_kamon(dr, cx, cy, R, seed, ink, paper, style=None):
    """One generated mon: n-fold radial symmetry inside a double ring."""
    rng = random.Random(seed)
    n = rng.choice([3, 4, 5, 6, 8])
    base = rng.uniform(0, math.pi)
    lw = max(2, R // 26)
    style = style or rng.choice(["petal", "petal", "geo", "rings"])

    # enclosure: double ring
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], outline=ink, width=lw)
    r2 = R * 0.88
    dr.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=ink, width=max(1, lw // 2))

    if style == "petal":
        # big petals
        L = r2 * rng.uniform(0.52, 0.68)
        Wd = r2 * rng.uniform(0.30, 0.46)
        r0 = r2 * rng.uniform(0.10, 0.22)
        outline_only = rng.random() < 0.4
        for i in range(n):
            a = base + i * 2 * math.pi / n
            p = petal_poly(cx, cy, r0, a, L, Wd)
            if outline_only:
                dr.polygon(p, outline=ink, width=lw)
            else:
                dr.polygon(p, fill=ink)
        # secondary small petals between
        if rng.random() < 0.7:
            for i in range(n):
                a = base + (i + 0.5) * 2 * math.pi / n
                p = petal_poly(cx, cy, r0 + L * 0.55, a, L * 0.42, Wd * 0.4)
                dr.polygon(p, fill=ink if outline_only else None,
                           outline=None if outline_only else ink,
                           width=lw)
        # center
        cr = r2 * rng.uniform(0.08, 0.16)
        if rng.random() < 0.5:
            dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=ink)
        else:
            dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=ink, width=lw)
    elif style == "geo":
        # rotated squares / diamonds
        for m, rr in [(n, r2 * 0.72), (n, r2 * 0.45)]:
            pts = []
            for i in range(m):
                a = base + i * 2 * math.pi / m
                pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
            dr.polygon(pts, outline=ink, width=lw)
        for i in range(n):
            a = base + i * 2 * math.pi / n
            x1 = cx + r2 * 0.45 * math.cos(a)
            y1 = cy + r2 * 0.45 * math.sin(a)
            x2 = cx + r2 * 0.72 * math.cos(a)
            y2 = cy + r2 * 0.72 * math.sin(a)
            dr.line([x1, y1, x2, y2], fill=ink, width=lw)
        cr = r2 * 0.16
        dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=ink)
    else:
        # ring-of-circles (like "star/coin" mon)
        rr = r2 * 0.58
        cr = r2 * rng.uniform(0.20, 0.26)
        for i in range(n):
            a = base + i * 2 * math.pi / n
            x = cx + rr * math.cos(a)
            y = cy + rr * math.sin(a)
            if rng.random() < 0.5:
                dr.ellipse([x - cr, y - cr, x + cr, y + cr], fill=ink)
                dr.ellipse([x - cr * 0.45, y - cr * 0.45, x + cr * 0.45, y + cr * 0.45], fill=paper)
            else:
                dr.ellipse([x - cr, y - cr, x + cr, y + cr], outline=ink, width=lw)
        cr2 = r2 * 0.20
        dr.ellipse([cx - cr2, cy - cr2, cx + cr2, cy + cr2], fill=ink)


def image3_kamon():
    """A specimen sheet of six generated kamon (Japanese family crests),
    seeded by today's date; the center-right one prints in red."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    R = 52 * s
    cols_x = [72, 200, 328]
    rows_y = [78, 196]
    seeds = [20260712 + i * 101 for i in range(6)]
    styles = ["petal", "geo", "rings", "rings", "petal", "geo"]
    k = 0
    for ry in rows_y:
        for cxp in cols_x:
            ink = RED if k == 4 else BLACK
            draw_kamon(dr, cxp * s, ry * s, R, seeds[k], ink, WHITE, styles[k])
            k += 1

    # caption strip
    dr.rectangle([0, H * s - 34 * s, W * s, H * s], fill=BLACK)
    fj = font(FONT_JP, 17 * s)
    fe = font(FONT_SANS, 10 * s)
    ctext(dr, (W * s * 0.24, H * s - 17 * s), "家紋六種", fj, WHITE)
    ctext(dr, (W * s * 0.66, H * s - 17 * s),
          "six invented family crests · seeded 2026-07-12", fe, WHITE)
    return finalize(img)


# ------------------------------------------------- 4. Almanac (supermoon minus 2)
def image4_almanac():
    """Sky almanac card: this dawn's thin waning crescent, and the countdown
    to the Jul 14 new supermoon — the darkest, best Milky Way night."""
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)
    rng = random.Random(714)

    # star field
    for _ in range(230):
        x = rng.uniform(0, W * s)
        y = rng.uniform(0, H * s * 0.62)
        v = rng.randint(120, 255)
        r = rng.uniform(0.4, 1.3) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    # thin waning crescent, lit on the lower-left (dawn eastern sky)
    mcx, mcy, mr = W * s * 0.30, H * s * 0.30, 62 * s
    # lit disk
    dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=(230, 230, 230))
    # occluding disk shifted toward upper-right leaves a lower-left crescent
    off = mr * 0.36
    dr.ellipse([mcx - mr + off * 0.8, mcy - mr - off * 0.6,
                mcx + mr + off * 0.8, mcy + mr - off * 0.6], fill=BLACK)
    # faint earthshine dots on the dark part
    for _ in range(160):
        a = rng.uniform(0, 2 * math.pi)
        r = mr * math.sqrt(rng.random()) * 0.82
        x, y = mcx + r * math.cos(a) + off * 0.5, mcy + r * math.sin(a) - off * 0.4
        if math.dist((x, y), (mcx, mcy)) < mr * 0.95:
            dr.point((x, y), fill=(70, 70, 70))

    # headline
    fh = font(FONT_SANS_B, 17 * s)
    fs2 = font(FONT_SANS, 11 * s)
    tx = W * s * 0.535
    dr.text((tx, H * s * 0.16), "NEW SUPERMOON", font=fh, fill=WHITE, anchor="lm")
    dr.text((tx, H * s * 0.265), "in 2 days — Jul 14, 09:44 UTC", font=fs2,
            fill=WHITE, anchor="lm")
    dr.text((tx, H * s * 0.36), "4th of 5 supermoons in a row;", font=fs2,
            fill=(200, 200, 200), anchor="lm")
    dr.text((tx, H * s * 0.435), "darkest skies → best Milky Way", font=fs2,
            fill=(200, 200, 200), anchor="lm")

    # red divider
    dr.rectangle([24 * s, H * s * 0.56, W * s - 24 * s, H * s * 0.56 + 2.4 * s], fill=RED)

    # event rows
    fm = font(FONT_MONO, 11 * s)
    fmb = font(FONT_SANS_B, 11 * s)
    rows = [
        ("TONIGHT", "Venus blazing near Regulus, W after sunset"),
        ("DAWN   ", "old crescent Moon; Mars closing on Aldebaran"),
        ("JUL 21 ", "first-quarter Moon — best crater relief"),
        ("JUL 31 ", "double meteor shower: α-Cap + S δ-Aquariids"),
    ]
    y = H * s * 0.635
    for tag, txt in rows:
        dr.text((28 * s, y), tag, font=fmb, fill=RED, anchor="lm")
        dr.text((105 * s, y), txt, font=fm, fill=WHITE, anchor="lm")
        y += H * s * 0.088
    ctext(dr, (W * s / 2, H * s * 0.965),
          "sky almanac · 2026-07-12", font(FONT_SANS, 9 * s), (170, 170, 170))
    return finalize(img)


# ------------------------------------------------- 5. Etch A Sketch (Jul 12 1960)
def image5_etchasketch():
    """The Etch A Sketch went on sale July 12, 1960. One continuous line,
    horizontal and vertical moves only — exactly what the two knobs allow —
    wanders the screen: a self-avoiding walk seeded by today's date."""
    img = Image.new("RGB", (W, H), RED)
    dr = ImageDraw.Draw(img)

    # frame & screen
    m = 26
    sx0, sy0, sx1, sy1 = m + 8, m + 6, W - m - 8, H - m - 26
    dr.rounded_rectangle([6, 4, W - 6, H - 4], radius=18, outline=BLACK, width=2)
    dr.rounded_rectangle([sx0 - 5, sy0 - 5, sx1 + 5, sy1 + 5], radius=6, fill=BLACK)
    dr.rectangle([sx0, sy0, sx1, sy1], fill=(226, 226, 226))

    # self-avoiding H/V walk on a grid
    rng = random.Random(19600712)
    step = 9
    gw = (sx1 - sx0 - 12) // step
    gh = (sy1 - sy0 - 12) // step
    ox, oy = sx0 + 7, sy0 + 7
    visited = {(0, 0)}
    px, py = 0, 0
    path = [(0, 0)]
    heading = (1, 0)
    for _ in range(2600):
        moves = []
        for dxy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = px + dxy[0], py + dxy[1]
            if 0 <= nx <= gw and 0 <= ny <= gh and (nx, ny) not in visited:
                # bias: prefer continuing straight (etch-a-sketch long strokes)
                w = 5 if dxy == heading else 1
                moves += [dxy] * w
        if not moves:
            # back up along the path to find a spot with a free neighbor
            for bi in range(len(path) - 2, -1, -1):
                bx, by = path[bi]
                free = [(bx + d[0], by + d[1]) for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]
                        if 0 <= bx + d[0] <= gw and 0 <= by + d[1] <= gh
                        and (bx + d[0], by + d[1]) not in visited]
                if free:
                    # retrace (a real etch-a-sketch must redraw over its line)
                    path += path[bi:len(path) - 1][::-1]
                    px, py = bx, by
                    break
            else:
                break
            continue
        heading = rng.choice(moves)
        px, py = px + heading[0], py + heading[1]
        visited.add((px, py))
        path.append((px, py))

    pts = [(ox + x * step, oy + y * step) for (x, y) in path]
    dr.line(pts, fill=BLACK, width=2, joint="curve")

    # knobs
    for kx in (m + 12, W - m - 12):
        dr.ellipse([kx - 14, H - 30, kx + 14, H - 2], fill=WHITE, outline=BLACK, width=2)
        dr.ellipse([kx - 5, H - 21, kx + 5, H - 11], outline=BLACK, width=1)

    # caption on the frame, sized to fit between the knobs
    f1 = font(FONT_SANS_B, 13)
    caption = "ETCH A SKETCH · on sale July 12, 1960"
    avail = (W - m - 26) - (m + 26) - 20
    while dr.textlength(caption, font=f1) > avail and f1.size > 9:
        f1 = font(FONT_SANS_B, f1.size - 1)
    ctext(dr, (W / 2, H - 16), caption, f1, WHITE)

    return finalize(img, dither=False)


if __name__ == "__main__":
    import os
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    makers = [image1_geodesic, image2_walden, image3_kamon,
              image4_almanac, image5_etchasketch]
    for i, mk in enumerate(makers, 1):
        im = mk()
        im.save(os.path.join(outdir, f"{i}.png"), optimize=True)
        print(f"saved {i}.png")
