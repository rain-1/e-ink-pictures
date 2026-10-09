#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-09. Draconids night / Hangul Day.

Five 400x300 images in exactly white/black/red. Style notes ("plates"):
diagram-as-poem — scientific-plate composition, a single red idea per image,
small monospace captions in the margin. Line art renders at 3x and is snapped
to the palette WITHOUT dithering (crisp edges); tonal work uses Floyd-Steinberg.
"""
import math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S = 400, 300, 3
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
DJ = "/usr/share/fonts/truetype/dejavu/"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

pal = Image.new("P", (1, 1))
pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)


def font(name, size):
    return ImageFont.truetype(DJ + name, size)


def finish(img, dither=False):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=pal, dither=d)


def caption(dr, xy, text, size, fill, name="DejaVuSansMono-Bold.ttf", anchor="la"):
    dr.text((xy[0] * S, xy[1] * S), text, font=font(name, size * S), fill=fill, anchor=anchor)


# ------------------------------------------------------------ 1. Draco, tonight
def draconids():
    rng = random.Random(20261009)
    img = Image.new("RGB", (W * S, H * S), BLACK)
    dr = ImageDraw.Draw(img)
    # stereographic projection about the radiant (RA 17.47h, Dec +54)
    ra0, de0 = math.radians(17.47 * 15), math.radians(54)
    cx, cy, sc = 205, 150, 175

    def proj(ra_h, dec):
        ra, de = math.radians(ra_h * 15), math.radians(dec)
        cosc = math.sin(de0) * math.sin(de) + math.cos(de0) * math.cos(de) * math.cos(ra - ra0)
        k = 2 / (1 + cosc)
        x = k * math.cos(de) * math.sin(ra - ra0)
        y = k * (math.cos(de0) * math.sin(de) - math.sin(de0) * math.cos(de) * math.cos(ra - ra0))
        # rotate so the dragon's body sweeps across the frame
        a = math.radians(-35)
        x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
        return (cx - x * sc) * S, (cy - y * sc) * S

    stars = {  # name: (RA h, Dec, mag)
        "gam": (17.943, 51.49, 2.2), "bet": (17.507, 52.30, 2.8), "nu": (17.536, 55.18, 4.9),
        "xi": (17.892, 56.87, 3.7), "del": (19.209, 67.66, 3.1), "eps": (19.803, 70.27, 3.8),
        "chi": (18.351, 72.73, 3.6), "zet": (17.146, 65.71, 3.2), "eta": (16.400, 61.51, 2.7),
        "the": (16.031, 58.57, 4.0), "iot": (15.415, 58.97, 3.3), "alp": (14.073, 64.38, 3.7),
        "kap": (12.558, 69.79, 3.9), "lam": (11.523, 69.33, 3.8),
    }
    path = ["gam", "bet", "nu", "xi", "gam"], ["xi", "del", "eps", "chi", "zet", "eta", "the", "iot", "alp", "kap", "lam"]
    # background field stars
    for _ in range(260):
        x, y = rng.uniform(0, W * S), rng.uniform(0, H * S)
        r = rng.choice([1, 1, 1, 2, 2, 3])
        dr.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    for seg in path:
        pts = [proj(*stars[n][:2]) for n in seg]
        for a, b in zip(pts, pts[1:]):
            n = int(math.hypot(b[0] - a[0], b[1] - a[1]) / (5 * S))
            for t in range(1, n):
                x = a[0] + (b[0] - a[0]) * t / n; y = a[1] + (b[1] - a[1]) * t / n
                dr.ellipse([x - 2, y - 2, x + 2, y + 2], fill=WHITE)
    for n, (ra, de, m) in stars.items():
        x, y = proj(ra, de)
        r = (5.5 - m) * 3.2 + 3
        dr.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    # meteors: tapering streaks pointing back to the radiant
    rx, ry = proj(17.47, 54)
    for i in range(9):
        ang = rng.uniform(0, 2 * math.pi)
        d0 = rng.uniform(50, 150) * S
        L = rng.uniform(40, 95) * S
        for t in np.linspace(0, 1, 40):
            d = d0 + L * t
            x, y = rx + math.cos(ang) * d, ry + math.sin(ang) * d
            w = 0.6 + 4.2 * t ** 1.6
            dr.ellipse([x - w, y - w, x + w, y + w], fill=WHITE)
    # the radiant — the one red idea: where tonight's dust comes from
    for r in (13, 21, 29):
        dr.ellipse([rx - r * S, ry - r * S, rx + r * S, ry + r * S], outline=RED, width=S + 1)
    dr.ellipse([rx - 3 * S, ry - 3 * S, rx + 3 * S, ry + 3 * S], fill=RED)
    caption(dr, (12, 12), "DRACONIDS", 22, WHITE, "DejaVuSans-Bold.ttf")
    caption(dr, (13, 38), "9 OCT 2026 · PEAK 01:00 UTC", 9, WHITE)
    caption(dr, (13, 50), "MOON 3% · LOOK NORTH AFTER DUSK", 9, WHITE)
    caption(dr, (13, 268), "dust of comet 21P, shed in 1946,", 9, WHITE)
    caption(dr, (13, 280), "arriving from the dragon's head", 9, WHITE)
    caption(dr, (rx / S + 26, ry / S - 4), "radiant", 9, RED)
    return finish(img)


# ------------------------------------------------------------ 2. 한글, built from strokes
def hangul():
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)
    T = 13  # stroke thickness (px at 1x)

    def bar(x0, y0, x1, y1, col=BLACK):
        dr.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=col)

    def ring(cx, cy, r, col=BLACK):
        dr.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=col)
        r2 = r - T
        dr.ellipse([(cx - r2) * S, (cy - r2) * S, (cx + r2) * S, (cy + r2) * S], fill=WHITE)

    # 한 = ㅎ + ㅏ over ㄴ   (block x 20..140, y 30..270)
    bar(55, 34, 55 + T, 50)                      # ㅎ top tick
    bar(30, 54, 108, 54 + T)                     # ㅎ bar
    ring(69, 103, 30)                            # ㅎ circle
    bar(124, 30, 124 + T, 152)                   # ㅏ stem (person)
    bar(124 + T, 84, 154, 84 + T, RED)           # ㅏ tick (heaven, ㆍ, made long)
    bar(36, 172, 36 + T, 262)                    # ㄴ vertical
    bar(36, 249, 150, 262)                       # ㄴ foot
    # 글 = ㄱ over ㅡ over ㄹ   (block x 172..292)
    bar(178, 34, 290, 34 + T)                    # ㄱ top
    bar(290 - T, 34, 290, 98)                    # ㄱ hook
    bar(170, 116, 298, 116 + T, BLACK)  # ㅡ (earth)
    # ㄹ
    bar(178, 150, 290, 150 + T); bar(290 - T, 150, 290, 202)
    bar(178, 196, 290, 196 + T); bar(178, 196, 178 + T, 262)
    bar(178, 249, 290, 262)
    # legend column: the three vowel primitives
    x0 = 322
    dr.ellipse([(x0 + 18) * S, 40 * S, (x0 + 34) * S, 56 * S], fill=RED)
    caption(dr, (x0 + 26, 64), "HEAVEN", 9, BLACK, anchor="ma")
    bar(x0 + 4, 104, x0 + 48, 104 + 7)
    caption(dr, (x0 + 26, 118), "EARTH", 9, BLACK, anchor="ma")
    bar(x0 + 23, 148, x0 + 30, 192)
    caption(dr, (x0 + 26, 198), "PERSON", 9, BLACK, anchor="ma")
    dr.line([(x0 - 8) * S, 30 * S, (x0 - 8) * S, 262 * S], fill=BLACK, width=S)
    caption(dr, (x0 - 2, 232), "HANGUL DAY", 8, BLACK, "DejaVuSansMono-Bold.ttf")
    caption(dr, (x0 - 2, 243), "promulgated", 8, BLACK)
    caption(dr, (x0 - 2, 253), "Oct 1446", 8, BLACK)
    caption(dr, (30, 280), "every vowel is a person, the earth, and a dot of sky", 9, BLACK)
    return finish(img)


# ------------------------------------------------------------ 3. The orbit of 21P
def orbit():
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)
    q, e, P = 1.013, 0.711, 6.56
    a = q / (1 - e); b = a * math.sqrt(1 - e * e)
    k = 41.0  # px per AU
    sx, sy = 300, 146  # Sun position (perihelion points right)

    def P2(xau, yau):
        return (sx + xau * k) * S, (sy - yau * k) * S

    # Jupiter orbit (dashed), Earth orbit
    for R, dash in ((5.2, 6), (1.0, 0)):
        n = 720
        for i in range(n):
            if dash and ((i // dash) % 2 or abs(R * math.sin(2 * math.pi * i / n)) * k > 95):
                continue
            t0, t1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            dr.line([P2(R * math.cos(t0), R * math.sin(t0)), P2(R * math.cos(t1), R * math.sin(t1))],
                    fill=BLACK, width=S)
    # dust trail (red stipple) hugging the comet's orbit
    rng = random.Random(21)
    for _ in range(1600):
        E = rng.uniform(0, 2 * math.pi)
        x, y = a * (math.cos(E) - e), b * math.sin(E)
        j = rng.gauss(0, 0.05)
        X, Y = P2(x + j, y + rng.gauss(0, 0.05))
        r = rng.choice([1.5, 2, 2.5])
        dr.ellipse([X - r, Y - r, X + r, Y + r], fill=RED)
    pts = [P2(a * (math.cos(E) - e), b * math.sin(E)) for E in np.linspace(0, 2 * math.pi, 600)]
    dr.line(pts + [pts[0]], fill=BLACK, width=2 * S)
    # Sun
    X, Y = P2(0, 0)
    dr.ellipse([X - 6 * S, Y - 6 * S, X + 6 * S, Y + 6 * S], fill=BLACK)
    for i in range(12):
        t = i * math.pi / 6
        dr.line([X + math.cos(t) * 9 * S, Y + math.sin(t) * 9 * S, X + math.cos(t) * 13 * S, Y + math.sin(t) * 13 * S], fill=BLACK, width=S)
    # Earth tonight, sitting in the stream
    X, Y = P2(0.98, -0.20)
    dr.ellipse([X - 5 * S, Y - 5 * S, X + 5 * S, Y + 5 * S], fill=WHITE, outline=BLACK, width=2 * S)
    caption(dr, (X / S - 8, Y / S + 6), "EARTH,", 8, BLACK, anchor="ra")
    caption(dr, (X / S - 8, Y / S + 16), "TONIGHT", 8, BLACK, anchor="ra")
    # comet now: perihelion 2025-03-25, so t = 1.54 yr after
    M = 2 * math.pi * 1.54 / P
    E = M
    for _ in range(50):
        E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    X, Y = P2(a * (math.cos(E) - e), b * math.sin(E))
    dr.polygon([(X, Y - 7 * S), (X + 7 * S, Y), (X, Y + 7 * S), (X - 7 * S, Y)], fill=BLACK)
    caption(dr, (X / S + 6, Y / S + 8), "21P NOW", 8, BLACK, "DejaVuSansMono-Bold.ttf")
    caption(dr, (X / S + 6, Y / S + 18), "4.7 AU from Sun", 8, BLACK)
    caption(dr, (12, 12), "21P / GIACOBINI–ZINNER", 13, BLACK, "DejaVuSans-Bold.ttf")
    caption(dr, (12, 30), "period 6.6 yr · found 1900 · lost · refound 1913", 8, BLACK)
    caption(dr, (12, 264), "11 Sep 1985: ICE flies 7,800 km through its tail —", 8, BLACK)
    caption(dr, (12, 275), "the first comet ever visited by a spacecraft.", 8, BLACK)
    caption(dr, (12, 286), "red = the dust that becomes tonight's meteors", 8, RED)
    caption(dr, (sx - 5.2 * k - 4, sy - 4), "JUPITER", 7, BLACK, anchor="ra")
    return finish(img)


# ------------------------------------------------------------ 4. 1946 vs 2026
def storm():
    rng = random.Random(1946)
    img = Image.new("RGB", (W * S, H * S), WHITE)
    dr = ImageDraw.Draw(img)
    rx, ry = 200 * S, -40 * S  # radiant above the frame
    top = 58 * S
    for _ in range(10000):
        x, y = rng.uniform(0, W * S), rng.uniform(top, 248 * S)
        dx, dy = x - rx, y - ry
        d = math.hypot(dx, dy)
        L = rng.uniform(2, 9)
        dr.line([x, y, x + dx / d * L * S / 3 * 3, y + dy / d * L * S / 3 * 3], fill=(60, 60, 60), width=1)
    # tonight's five, in red, long and bright
    for i in range(5):
        x, y = rng.uniform(40, 360) * S, rng.uniform(80, 200) * S
        dx, dy = x - rx, y - ry
        d = math.hypot(dx, dy)
        for t in np.linspace(0, 1, 30):
            L = 46 * S * t
            w = 1 + 4 * t ** 1.5
            px, py = x + dx / d * L, y + dy / d * L
            dr.ellipse([px - w - 3, py - w - 3, px + w + 3, py + w + 3], fill=WHITE)
        for t in np.linspace(0, 1, 30):
            L = 46 * S * t
            w = 1 + 4 * t ** 1.5
            px, py = x + dx / d * L, y + dy / d * L
            dr.ellipse([px - w, py - w, px + w, py + w], fill=RED)
    caption(dr, (12, 10), "ONE HOUR OF DRACONIDS", 15, BLACK, "DejaVuSans-Bold.ttf")
    caption(dr, (12, 32), "black: 10 OCT 1946, ~10,000 meteors   red: tonight, ~5", 8, BLACK)
    caption(dr, (12, 258), "Both drawn to the same hour. The stream is old dust,", 8, BLACK)
    caption(dr, (12, 269), "laid down in clumps; some years Earth walks into a", 8, BLACK)
    caption(dr, (12, 280), "thick strand, most years it brushes the hem.", 8, BLACK)
    return finish(img)


# ------------------------------------------------------------ 5. Morphogenesis (Gray–Scott)
def morpho():
    rng = np.random.default_rng(20261009)
    w, h = 200, 150
    U = np.ones((h, w)); V = np.zeros((h, w))
    for _ in range(22):
        x, y = rng.integers(10, w - 10), rng.integers(10, h - 10)
        V[y - 3:y + 4, x - 3:x + 4] = 0.5; U[y - 3:y + 4, x - 3:x + 4] = 0.25
    V += rng.random((h, w)) * 0.02
    # feed/kill drift across the canvas: spots on the left, worms on the right
    xs = np.linspace(0, 1, w)[None, :]
    F = 0.030 + 0.012 * xs + np.zeros((h, 1))
    K = 0.062 - 0.001 * xs + np.zeros((h, 1))
    Du, Dv = 0.16, 0.08

    def lap(Z):
        return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)

    for _ in range(9000):
        uvv = U * V * V
        U += Du * lap(U) - uvv + F * (1 - U)
        V += Dv * lap(V) + uvv - (F + K) * V
    v = Image.fromarray((V / V.max() * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    v = np.asarray(v).astype(float) / 255
    out = np.full((H, W, 3), 255, np.uint8)
    out[v > 0.28] = BLACK
    out[v > 0.62] = RED
    img = Image.fromarray(out)
    dr = ImageDraw.Draw(img)
    dr.rectangle([0, 272, W, H], fill=WHITE)
    dr.line([0, 272, W, 272], fill=BLACK)
    f = font("DejaVuSansMono.ttf", 9)
    dr.text((10, 280), "MORPHOGENESIS · two chemicals, one rule · seed 20261009", font=f, fill=BLACK)
    return img.quantize(palette=pal, dither=Image.Dither.NONE)


if __name__ == "__main__":
    for i, fn in enumerate([draconids, hangul, orbit, storm, morpho], 1):
        im = fn()
        assert im.size == (W, H)
        im.save(f"{OUT}/{i}.png")
        print("wrote", i)
