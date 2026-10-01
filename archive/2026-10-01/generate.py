#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-01.

Five 400x300 plates in exactly three colours (white, black, red).
House style ("the plate"): every image is a numbered plate from an imaginary
almanac — art on top, a hairline rule, then a crisp Unifont caption strip:
plate numeral, title, a line of fact, the date in red. Tone is made with
*line screens* (engraving), not dither, wherever possible.

  I   DRAWDOWN    — an 8-shaft weaving draft computed via F = TR·TU⁻¹·T (after Anni Albers)
  II  SATURN      — opposition 4 Oct, rings open 7.5°, engraved
  III MODEL T     — on sale 1 Oct 1908; constructivist poster of Ford's colour rule
  IV  DRACONIDS   — inverted star-trail plate looking north, meteors from Draco
  V   MORPHOGEN   — Gray–Scott reaction–diffusion swept across feed rate (Turing 1952)
"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
IW, IB, IR = 0, 1, 2  # palette indices
DATE = "2026-10-01"
SEED = 20261001

UNIFONT = "/usr/share/fonts/opentype/unifont/unifont.otf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
SERIF_I = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"

CAP_H = 20  # caption strip height


def palette_img():
    p = Image.new("P", (1, 1))
    p.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)
    return p


PAL = palette_img()


def to_p(rgb):
    """Exact 3-colour, nearest colour, no dither (engraving look)."""
    if rgb.size != (W, H):
        rgb = rgb.resize((W, H), Image.LANCZOS)
    return rgb.convert("RGB").quantize(palette=PAL, dither=Image.Dither.NONE)


def from_index(arr):
    """uint8 array of palette indices -> P image."""
    im = Image.fromarray(arr.astype(np.uint8), "P")
    im.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)
    return im


def caption(im, numeral, title, fact, invert=False):
    """The house caption strip, drawn pixel-crisp at 1x."""
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    f = ImageFont.truetype(UNIFONT, 16)
    bg, fg = (IB, IW) if invert else (IW, IB)
    y0 = H - CAP_H
    d.rectangle([0, y0, W, H], fill=bg)
    d.line([0, y0, W, y0], fill=fg)
    x = 4
    d.text((x, y0 + 2), numeral, font=f, fill=IR)
    x += d.textlength(numeral, font=f) + 6
    d.text((x, y0 + 2), title, font=f, fill=fg)
    x += d.textlength(title, font=f) + 8
    dt = DATE[5:].replace("-", ".")
    dw = d.textlength(dt, font=f)
    # fact squeezed between title and date, truncated if needed
    room = W - 6 - dw - 8 - x
    while fact and d.textlength(fact, font=f) > room:
        fact = fact[:-2] + "…"
    d.text((x, y0 + 2), fact, font=f, fill=fg)
    d.text((W - 4 - dw, y0 + 2), dt, font=f, fill=IR)
    return im


def small(d, xy, text, fill, size=16):
    d.fontmode = "1"
    d.text(xy, text, font=ImageFont.truetype(UNIFONT, size), fill=fill)


# ------------------------------------------------------------- I. DRAWDOWN
def plate_drawdown():
    rng = random.Random(SEED)
    S = 8                      # shafts / treadles
    c = 5                      # cell size px
    ncol, nrow = 60, 42
    x0, ty0 = 8, 6             # drawdown left, threading top
    dy0 = ty0 + S * c + 4      # drawdown top
    rx0 = x0 + ncol * c + 4    # treadling / tie-up left

    # Threading: a reflecting ±1 walk (point / "curve" draft), seeded by date,
    # mirrored so the cloth is symmetric about its centre.
    def walk(n, seed):
        r = random.Random(seed)
        s, out, v = 0, [], 1
        for _ in range(n):
            out.append(s)
            if r.random() < 0.18:
                v = -v
            s += v
            if s < 0:
                s, v = 1, 1
            if s >= S:
                s, v = S - 2, -1
        return out

    half = walk(ncol // 2, SEED)
    thread = half + half[::-1]
    half_t = walk(nrow // 2, SEED + 7)
    tread = half_t + half_t[::-1]
    # Tie-up: an 8-shaft 4/4 twill, rotated per treadle
    base = [1, 1, 1, 1, 0, 0, 0, 0]
    tie = [[base[(sh - tr) % S] for sh in range(S)] for tr in range(S)]

    # F = TR · TU⁻¹ · T : warp up where treadle row lifts the thread's shaft
    F = np.array([[tie[tread[r]][thread[q]] for q in range(ncol)] for r in range(nrow)])

    a = np.zeros((H, W), np.uint8)
    # drawdown: warp up = black thread, weft = red thread; white hairline grid
    for r in range(nrow):
        for q in range(ncol):
            col = IB if F[r, q] else IR
            a[dy0 + r * c: dy0 + r * c + c - 1, x0 + q * c: x0 + q * c + c - 1] = col

    def grid(gx, gy, cols, rows, filled):
        for i in range(cols + 1):
            a[gy:gy + rows * c + 1, gx + i * c] = IB
        for j in range(rows + 1):
            a[gy + j * c, gx:gx + cols * c + 1] = IB
        for (i, j) in filled:
            a[gy + j * c + 1: gy + j * c + c, gx + i * c + 1: gx + i * c + c] = IB

    # threading (shaft 1 at bottom), tie-up, treadling
    grid(x0, ty0, ncol, S, [(q, S - 1 - thread[q]) for q in range(ncol)])
    grid(rx0, ty0, S, S, [(tr, S - 1 - sh) for tr in range(S) for sh in range(S) if tie[tr][sh]])
    grid(rx0, dy0, S, nrow, [(tread[r], r) for r in range(nrow)])

    im = from_index(a)
    d = ImageDraw.Draw(im)
    # marginal notes in the narrow right column
    xn = rx0 + S * c + 5
    f = ImageFont.truetype(UNIFONT, 16)
    d.fontmode = "1"
    for k, ch in enumerate("DRAFT"):
        d.text((xn + 3, dy0 + 6 + k * 16), ch, font=f, fill=IB)
    d.text((xn + 3, dy0 + 6 + 6 * 16), "8", font=f, fill=IR)
    d.text((xn + 3, dy0 + 6 + 7 * 16), "×", font=f, fill=IR)
    d.text((xn + 3, dy0 + 6 + 8 * 16), "8", font=f, fill=IR)
    caption(im, "I", "DRAWDOWN", "F = TR·TU⁻¹·T  after Anni Albers")
    return im


# ------------------------------------------------------------- II. SATURN
def plate_saturn():
    s = 3
    w, h = W * s, (H - CAP_H) * s
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    cx, cy = 200 * s, 128 * s
    R = 62 * s
    tilt = math.radians(7.5)
    br = math.sin(tilt)
    X, Y = xx - cx, yy - cy

    out = np.zeros((h, w), np.uint8)  # 0 white, 1 black, 2 red

    # --- rings: concentric ellipse line screen, density from ring brightness
    rr = np.sqrt(X ** 2 + (Y / br) ** 2) / R          # ring-plane radius in R_saturn
    def ring_density(r):
        d = np.zeros_like(r)
        d = np.where((r > 1.24) & (r < 1.53), 0.22, d)              # C ring, faint
        d = np.where((r >= 1.53) & (r < 1.95), 0.55 + 0.25 * (r - 1.53) / 0.42, d)  # B ring
        d = np.where((r >= 2.03) & (r < 2.27), 0.5, d)              # A ring
        d = np.where((r > 2.205) & (r < 2.225), 0.0, d)             # Encke gap
        return d
    rd = ring_density(rr)
    # line screen across ring radius
    P = 4.0 * s / R  # period in R units ≈ 4 px at 1x
    phase = (rr / P) % 1.0
    ring_ink = (np.abs(phase - 0.5) * 2 < rd) & (rd > 0)

    # --- globe: oblate disc, horizontal line screen with limb darkening + belts
    gy_scale = 0.90
    gr = np.sqrt((X / R) ** 2 + (Y / (R * gy_scale)) ** 2)
    globe = gr < 1.0
    lat = np.clip(Y / (R * gy_scale), -1, 1)
    belts = 0.5 + 0.5 * np.sin(lat * 13.0 + 0.6) ** 2
    shade = 0.06 + 0.55 * np.clip(gr, 0, 1) ** 5 + 0.14 * belts * (np.abs(lat) < 0.85)
    shade += np.where(lat < -0.80, 0.35, 0)            # dusky south polar cap
    Pg = 4.0 * s
    gphase = (yy / Pg) % 1.0
    globe_ink = np.abs(gphase - 0.5) * 2 < shade
    edge = globe & (gr > 0.985)

    behind = Y < 0  # we view the south face: near side of rings below centre
    ring_area = rd > 0
    # back rings
    m = ring_area & behind & ~globe
    out[m & ring_ink] = 2
    # globe
    out[globe & globe_ink] = 1
    out[globe & ~globe_ink] = 0
    out[edge] = 1
    # globe's shadow on the rings (just beyond the limb, behind, at opposition minimal) – skip
    # front rings over globe (thin white gap first so the ring reads as in front)
    front = ring_area & ~behind
    rim = front & globe
    out[rim] = 0
    out[front & ring_ink] = 2
    # ring shadow on the globe: thin black band just above the front ring
    sh = globe & ~ring_area & (np.sqrt(X ** 2 + ((Y + 0.05 * R) / br) ** 2) / R > 1.53) \
        & (np.sqrt(X ** 2 + ((Y + 0.05 * R) / br) ** 2) / R < 1.95) & ~behind
    out[sh] = 1

    img = np.zeros((h, w, 3), np.uint8) + 255
    img[out == 1] = BLACK
    img[out == 2] = RED
    big = Image.fromarray(img).resize((W, H - CAP_H), Image.LANCZOS)
    full = Image.new("RGB", (W, H), WHITE)
    full.paste(big, (0, 0))
    im = to_p(full)
    d = ImageDraw.Draw(im)

    # starfield of Cetus-ish faint stars + moons (Titan etc. as dots on the ring line)
    rng = random.Random(SEED + 2)
    for _ in range(26):
        x, y = rng.randrange(6, 394), rng.randrange(6, 270)
        if abs(y - 128) < 70 and abs(x - 200) < 150:
            continue
        d.point((x, y), fill=IB)
        if rng.random() < 0.2:
            d.point([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)], fill=IB)
    for mx, lab in ((200 + 168, "TITAN"), (200 - 160, "RHEA")):
        my = 128 + 3
        d.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=IB)
        small(d, (mx - len(lab) * 4, my + 6), lab, IB)

    # opposition diagram, top-left: sun · earth · saturn in a line
    small(d, (8, 6), "SATURN", IB)
    small(d, (8, 22), "at opposition", IB)
    small(d, (8, 38), "4 OCT 12h UTC", IR)
    oy = 66
    d.line([10, oy, 110, oy], fill=IB)
    d.ellipse([7, oy - 4, 15, oy + 4], fill=IR)          # sun
    d.ellipse([34, oy - 2, 38, oy + 2], fill=IB)         # earth
    d.ellipse([104, oy - 3, 110, oy + 3], outline=IB)    # saturn
    d.line([100, oy, 114, oy], fill=IB)
    # right column facts
    for k, t in enumerate(["mag +0.3", "1.26 bn km", "in CETUS"]):
        tw = d.textlength(t, font=ImageFont.truetype(UNIFONT, 16))
        small(d, (W - 8 - tw, 6 + 16 * k), t, IB)
    caption(im, "II", "SATURN", "rings tilted 7.5°, opening again")
    return im


# ------------------------------------------------------------- III. MODEL T
def rot_text(text, font_path, size, color, angle, pad=4):
    f = ImageFont.truetype(font_path, size)
    l, t, r, b = f.getbbox(text)
    tile = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((pad - l, pad - t), text, font=f, fill=color + (255,))
    return tile.rotate(angle, resample=Image.BICUBIC, expand=True)


def plate_model_t():
    s = 3
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)
    S = lambda *v: [int(x * s) for x in v]

    # the wheel: black disc, 12 wooden spokes as white wedges' complement, red hub
    wc, wr = (150, 165), 96
    d.ellipse(S(wc[0] - wr, wc[1] - wr, wc[0] + wr, wc[1] + wr), fill=BLACK)
    d.ellipse(S(wc[0] - wr + 12, wc[1] - wr + 12, wc[0] + wr - 12, wc[1] + wr - 12), fill=WHITE)
    for k in range(12):
        a = math.radians(k * 30 + 9)
        a1, a2 = a - 0.07, a + 0.07
        pts = [(wc[0] + 14 * math.cos(a1), wc[1] + 14 * math.sin(a1)),
               (wc[0] + (wr - 10) * math.cos(a - 0.035), wc[1] + (wr - 10) * math.sin(a - 0.035)),
               (wc[0] + (wr - 10) * math.cos(a + 0.035), wc[1] + (wr - 10) * math.sin(a + 0.035)),
               (wc[0] + 14 * math.cos(a2), wc[1] + 14 * math.sin(a2))]
        d.polygon([(x * s, y * s) for x, y in pts], fill=BLACK)
    d.ellipse(S(wc[0] - 20, wc[1] - 20, wc[0] + 20, wc[1] + 20), fill=RED)
    d.ellipse(S(wc[0] - 6, wc[1] - 6, wc[0] + 6, wc[1] + 6), fill=WHITE)

    # the red wedge driving in from the upper right
    d.polygon([(x * s, y * s) for x, y in [(400, 92), (400, 146), (176, 162)]], fill=RED)

    # diagonal bars
    def bar(p0, p1, width, color):
        (x0, y0), (x1, y1) = p0, p1
        ang = math.atan2(y1 - y0, x1 - x0)
        nx, ny = -math.sin(ang) * width / 2, math.cos(ang) * width / 2
        d.polygon([((x0 + nx) * s, (y0 + ny) * s), ((x1 + nx) * s, (y1 + ny) * s),
                   ((x1 - nx) * s, (y1 - ny) * s), ((x0 - nx) * s, (y0 - ny) * s)], fill=color)
    bar((180, 326), (430, 130), 34, BLACK)
    bar((-10, 52), (120, -10), 10, BLACK)

    # text: diagonal on the black bar (white), stacked block upper-right
    ang = -math.degrees(math.atan2(130 - 326, 430 - 180))
    t1 = rot_text("SO LONG AS IT IS BLACK", SANS_B, 16 * s, WHITE, ang)
    mx, my = 322, 214  # centre of the visible stretch of the bar
    img.paste(t1, (int(mx * s - t1.width / 2), int(my * s - t1.height / 2)), t1)
    big = rot_text("ANY", SANS_B, 46 * s, BLACK, 0)
    img.paste(big, (int(268 * s), int(2 * s)), big)
    big2 = rot_text("COLOUR", SANS_B, 28 * s, BLACK, 0)
    img.paste(big2, (int(268 * s), int(50 * s)), big2)
    yr = rot_text("1908", SANS_B, 28 * s, RED, 90)
    img.paste(yr, (int(6 * s), int(150 * s)), yr)
    im = to_p(img)

    dd = ImageDraw.Draw(im)
    small(dd, (130, 6), "MODEL T  $850", IB)
    small(dd, (130, 22), "on sale 1.X.1908", IB)
    caption(im, "III", "MODEL T", "Henry Ford's colour chart")
    return im


# ------------------------------------------------------------- IV. DRACONIDS
def plate_draconids():
    rng = random.Random(SEED + 4)
    s = 3
    img = Image.new("RGB", (W * s, H * s), WHITE)
    d = ImageDraw.Draw(img)
    pole = (214, 118)          # Polaris
    sweep = math.radians(42)   # ~2h48m exposure
    # star trails: concentric arcs, random-ish stars, brightness -> width
    for _ in range(520):
        r = math.sqrt(rng.random()) * 330
        th = rng.random() * 2 * math.pi
        mag = rng.random() ** 3
        wdt = 1 if mag < 0.55 else (2 if mag < 0.85 else 3)
        if rng.random() < 0.55 and wdt == 1:
            continue
        bbox = [(pole[0] - r) * s, (pole[1] - r) * s, (pole[0] + r) * s, (pole[1] + r) * s]
        d.arc(bbox, math.degrees(th), math.degrees(th + sweep), fill=BLACK, width=wdt * s)
    # Polaris: tiny tight arc, a dot really
    d.ellipse([(pole[0] - 2) * s, (pole[1] - 2) * s, (pole[0] + 2) * s, (pole[1] + 2) * s], fill=BLACK)

    # radiant in Draco's head: ~36° from the pole, high in the NW in the evening
    rad = (118, 52)
    # meteors: red streaks, radial from radiant, starting some distance away
    for _ in range(9):
        a = rng.uniform(0, 2 * math.pi)
        r0 = rng.uniform(25, 140)
        L = rng.uniform(18, 55)
        x0, y0 = rad[0] + r0 * math.cos(a), rad[1] + r0 * math.sin(a)
        x1, y1 = rad[0] + (r0 + L) * math.cos(a), rad[1] + (r0 + L) * math.sin(a)
        if y1 > 240:
            continue
        steps = 24
        for k in range(steps):  # tapering streak: thin at start, fat then gone
            t0, t1 = k / steps, (k + 1) / steps
            wdt = 1 + 3.2 * math.sin(math.pi * t0) ** 1.5
            d.line([(x0 + (x1 - x0) * t0) * s, (y0 + (y1 - y0) * t0) * s,
                    (x0 + (x1 - x0) * t1) * s, (y0 + (y1 - y0) * t1) * s],
                   fill=RED, width=int(wdt * s))
    # radiant marker
    d.line([(rad[0] - 6) * s, rad[1] * s, (rad[0] + 6) * s, rad[1] * s], fill=RED, width=s)
    d.line([rad[0] * s, (rad[1] - 6) * s, rad[0] * s, (rad[1] + 6) * s], fill=RED, width=s)

    # ground: black hill silhouette with pines and a lit window
    gl = []
    for x in range(0, W + 1, 2):
        y = 236 + 10 * math.sin(x / 47.0) + 6 * math.sin(x / 13.0 + 1)
        gl.append((x * s, y * s))
    d.polygon(gl + [(W * s, H * s), (0, H * s)], fill=BLACK)
    for _ in range(18):
        x = rng.uniform(0, W)
        if 250 < x < 330:
            continue
        base = 236 + 10 * math.sin(x / 47.0) + 6 * math.sin(x / 13.0 + 1)
        th = rng.uniform(14, 34)
        for k in range(5):
            yk = base - th * k / 5
            wk = th * 0.32 * (1 - k / 5)
            d.polygon([((x - wk) * s, yk * s), ((x + wk) * s, yk * s), (x * s, (yk - th * 0.32) * s)], fill=BLACK)
    hx, hy = 286, 226
    d.rectangle([hx * s, hy * s, (hx + 26) * s, (hy + 18) * s], fill=BLACK)
    d.polygon([((hx - 4) * s, hy * s), ((hx + 30) * s, hy * s), ((hx + 13) * s, (hy - 12) * s)], fill=BLACK)
    d.rectangle([(hx + 5) * s, (hy + 5) * s, (hx + 11) * s, (hy + 11) * s], fill=RED)
    im = to_p(img)
    dd = ImageDraw.Draw(im)
    small(dd, (rad[0] + 9, rad[1] - 20), "radiant", IR)
    small(dd, (pole[0] + 6, pole[1] + 2), "Polaris", IB)
    caption(im, "IV", "DRACONIDS", "8-9 Oct, moonless, look N")
    return im


# ------------------------------------------------------------- V. MORPHOGEN
def plate_morphogen():
    rng = np.random.default_rng(SEED)
    gw, gh, m = 216, 156, 8  # margin cropped off later
    U = np.ones((gh, gw))
    V = np.zeros((gh, gw))
    # seed: scattered square drops
    for _ in range(60):
        x, y = rng.integers(2, gw - 8), rng.integers(2, gh - 8)
        U[y:y + 5, x:x + 5] = 0.5
        V[y:y + 5, x:x + 5] = 0.25
    V += rng.random((gh, gw)) * 0.02
    # feed rate sweeps left->right: spots -> worms -> labyrinth
    F = np.linspace(0.026, 0.046, gw)[None, :] * np.ones((gh, 1))
    k = 0.0605 + 0.0015 * np.cos(np.linspace(0, math.pi, gh))[:, None]
    Du, Dv = 0.16, 0.08

    def lap(Z):
        return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)

    for _ in range(14000):
        uvv = U * V * V
        U += Du * lap(U) - uvv + F * (1 - U)
        V += Dv * lap(V) + uvv - (F + k) * V

    V = V[m:-m, m:-m]
    vim = Image.fromarray((V / V.max() * 255).astype(np.uint8)).resize((W, H - CAP_H), Image.BICUBIC)
    v = np.asarray(vim).astype(np.float64) / 255.0
    a = np.zeros((H, W), np.uint8)
    body = v > 0.42
    rim = (v > 0.26) & ~body
    a[:H - CAP_H][rim] = IR
    a[:H - CAP_H][body] = IB
    im = from_index(a)
    caption(im, "V", "MORPHOGEN", "Turing 1952 · feed rate →")
    return im


if __name__ == "__main__":
    import os, sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    for i, fn in enumerate([plate_drawdown, plate_saturn, plate_model_t,
                            plate_draconids, plate_morphogen], 1):
        im = fn()
        assert im.size == (W, H) and im.mode == "P"
        assert set(np.unique(np.asarray(im))) <= {0, 1, 2}
        im.save(os.path.join(out, f"{i}.png"), optimize=True)
        print("wrote", i, fn.__name__)
