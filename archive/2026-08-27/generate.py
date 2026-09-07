#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-08-27.

Tonight is a deep partial lunar eclipse (96.3% of the Moon inside Earth's
umbra at 04:13 UTC), and today is the 143rd anniversary of the cataclysmic
final explosion of Krakatoa (27 Aug 1883) — the loudest sound in recorded
history, whose pressure wave circled the Earth four times.

Five 400x300 images in exactly three colors (white, black, red):
  1. Eclipse path diagram — the Moon crossing Earth's shadow, with UTC times
  2. Krakatoa poster — ash column against a Munch-red sunset sky
  3. Constructivist piece — the eclipse as a Lissitzky red wedge
  4. Eclipse kamon — Japanese crest: shadowed moon over seigaiha waves
  5. Barograph plate — Krakatoa's air wave recorded seven times, every 34 h
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
SS = 3  # supersample factor
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"


def make_palette_image():
    pal = Image.new("P", (1, 1))
    palette = list(WHITE) + list(BLACK) + list(RED)
    palette += [0, 0, 0] * (256 - 3)
    pal.putpalette(palette)
    return pal


PAL = make_palette_image()


def finalize(img, dither=True):
    """Downscale (if supersampled) and quantize to the exact 3-color palette."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert("RGB").quantize(palette=PAL, dither=d)


def font(path, size):
    return ImageFont.truetype(path, size)


def ctext(dr, xy, text, fnt, fill, anchor="mm"):
    dr.text(xy, text, font=fnt, fill=fill, anchor=anchor)


# ------------------------------------------------------- 1. Eclipse path diagram
def image1_eclipse_diagram():
    s = SS
    img = Image.new("RGB", (W * s, H * s), BLACK)
    dr = ImageDraw.Draw(img)
    rng = random.Random(20260827)

    # faint starfield
    for _ in range(160):
        x, y = rng.uniform(0, W * s), rng.uniform(0, H * s)
        v = rng.randint(70, 140)
        r = rng.uniform(0.4, 1.0) * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v))

    ucx, ucy = 200 * s, 168 * s
    pen_r = 118 * s
    umb_r = 62 * s
    moon_r = 17 * s
    path_y = ucy - 51 * s  # ~umbral magnitude 0.93, sliver left visible at max

    # penumbra & umbra shadow disks (dithered grays)
    dr.ellipse([ucx - pen_r, ucy - pen_r, ucx + pen_r, ucy + pen_r], fill=(58, 58, 58))
    dr.ellipse([ucx - umb_r, ucy - umb_r, ucx + umb_r, ucy + umb_r], fill=(16, 16, 16))
    # dotted outlines
    for R, col in [(pen_r, (170, 170, 170)), (umb_r, (220, 220, 220))]:
        n = int(2 * math.pi * R / (7 * s))
        for i in range(n):
            if i % 2:
                continue
            a = 2 * math.pi * i / n
            x, y = ucx + R * math.cos(a), ucy + R * math.sin(a)
            dr.ellipse([x - 0.8 * s, y - 0.8 * s, x + 0.8 * s, y + 0.8 * s], fill=col)

    ctext(dr, (ucx, ucy + umb_r - 11 * s), "UMBRA", font(FONT_SANS, 8 * s), (230, 230, 230))
    ctext(dr, (ucx, ucy + pen_r - 28 * s), "PENUMBRA", font(FONT_SANS, 8 * s), (200, 200, 200))

    # the moon's path (dotted line, left to right)
    for x in range(20 * s, 380 * s, 6 * s):
        dr.ellipse([x - 0.7 * s, path_y - 0.7 * s, x + 0.7 * s, path_y + 0.7 * s],
                   fill=(120, 120, 120))
    # direction arrow
    ax = 372 * s
    dr.polygon([(ax, path_y), (ax - 8 * s, path_y - 4 * s), (ax - 8 * s, path_y + 4 * s)],
               fill=(200, 200, 200))

    # helper: draw the moon at x, shading whatever part sits inside the umbra red
    def draw_moon(x, label, time_s, above=True):
        box = [x - moon_r, path_y - moon_r, x + moon_r, path_y + moon_r]
        d_pen = math.hypot(x - ucx, path_y - ucy)
        base = (235, 235, 235) if d_pen < pen_r + moon_r * 0.3 else WHITE
        dr.ellipse(box, fill=base, outline=BLACK, width=s)
        # red lens = moon ∩ umbra
        mask = Image.new("L", img.size, 0)
        md = ImageDraw.Draw(mask)
        md.ellipse(box, fill=255)
        umask = Image.new("L", img.size, 0)
        ud = ImageDraw.Draw(umask)
        ud.ellipse([ucx - umb_r, ucy - umb_r, ucx + umb_r, ucy + umb_r], fill=255)
        both = Image.composite(mask, Image.new("L", img.size, 0), umask)
        img.paste(Image.new("RGB", img.size, RED), (0, 0), both)
        ly = path_y - moon_r - 9 * s if above else path_y + moon_r + 9 * s
        ctext(dr, (x, ly), label, font(FONT_SANS_B, 9 * s), WHITE)
        ctext(dr, (x, ly + (10 * s if above else 10 * s) * (1 if not above else -1) * -1
                   + (0 if above else 0)), "", font(FONT_SANS, 8 * s), WHITE)
        ty = ly - 11 * s if above else ly + 11 * s
        ctext(dr, (x, ty), time_s, font(FONT_MONO_B, 9 * s), WHITE)

    draw_moon(45 * s, "P1", "01:24")
    draw_moon(136 * s, "U1", "02:34")
    draw_moon(200 * s, "MAX", "04:13")
    draw_moon(264 * s, "U4", "05:52")
    draw_moon(355 * s, "P4", "07:02")

    # title block
    ctext(dr, (200 * s, 16 * s), "T O N I G H T", font(FONT_SANS_B, 15 * s), RED)
    ctext(dr, (200 * s, 34 * s), "DEEP PARTIAL LUNAR ECLIPSE",
          font(FONT_SANS_B, 13 * s), WHITE)

    # bottom caption
    dr.rectangle([0, 272 * s, W * s, H * s], fill=BLACK)
    dr.line([14 * s, 272 * s, 386 * s, 272 * s], fill=(150, 150, 150), width=1 * s)
    ctext(dr, (200 * s, 281 * s), "96% of the Moon inside Earth's umbra",
          font(FONT_SERIF, 10 * s), WHITE)
    ctext(dr, (200 * s, 293 * s), "27–28 AUG 2026 · times UTC · Americas · Europe · Africa",
          font(FONT_SANS, 8 * s), (190, 190, 190))
    return finalize(img)


# ------------------------------------------------------------ 2. Krakatoa poster
def image2_krakatoa():
    s = SS
    rng = random.Random(1883)
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    horizon = 218 * s

    # Munch-style sunset sky: sinuous alternating bands of red / pale / dark
    band_cols = [WHITE, RED, WHITE, (215, 215, 215), RED,
                 WHITE, RED, (235, 235, 235), RED, WHITE]
    n_bands = len(band_cols)
    # build wavy boundaries between bands
    bounds = []
    for i in range(n_bands + 1):
        base = horizon * i / n_bands
        amp = (4 + 7 * rng.random()) * s
        ph = rng.uniform(0, 2 * math.pi)
        ph2 = rng.uniform(0, 2 * math.pi)
        bounds.append((base, amp, ph, ph2))
    for x in range(0, W * s, 2 * s):
        ys = []
        for (base, amp, ph, ph2) in bounds:
            y = base + amp * math.sin(x / (55 * s) * 2 * math.pi + ph) \
                + 0.5 * amp * math.sin(x / (23 * s) * 2 * math.pi + ph2)
            ys.append(max(y, ys[-1] if ys else -1e9))
        for i in range(n_bands):
            dr.rectangle([x, ys[i], x + 2 * s, ys[i + 1]], fill=band_cols[i])

    # white sun, low, with thin halo rings
    sx, sy, sr = 305 * s, 172 * s, 26 * s
    for rr, colv in [(sr + 14 * s, 200), (sr + 7 * s, 235)]:
        dr.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], outline=(colv, colv, colv),
                   width=2 * s)
    dr.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=WHITE, outline=BLACK, width=s)

    # sea: black with white wave strokes
    dr.rectangle([0, horizon, W * s, H * s], fill=(10, 10, 10))
    for _ in range(240):
        x = rng.uniform(0, W * s)
        y = rng.uniform(horizon + 3 * s, H * s - 24 * s)
        ln = rng.uniform(4, 18) * s * (0.4 + (y - horizon) / (H * s - horizon))
        v = rng.randint(140, 255)
        dr.line([x, y, x + ln, y], fill=(v, v, v), width=max(1, int(0.9 * s)))
    # red sun-glitter path on the water under the sun
    for _ in range(90):
        y = rng.uniform(horizon + 2 * s, H * s - 26 * s)
        spread = 8 * s + (y - horizon) * 0.35
        x = rng.gauss(sx, spread * 0.5)
        ln = rng.uniform(3, 12) * s
        dr.line([x - ln / 2, y, x + ln / 2, y], fill=RED, width=max(1, int(1.0 * s)))

    # volcano silhouette (island cone, left of center)
    vx = 128 * s
    peak_y = 120 * s
    cone = [(vx - 95 * s, horizon + 6 * s),
            (vx - 30 * s, peak_y + 14 * s),
            (vx - 10 * s, peak_y),
            (vx + 8 * s, peak_y + 2 * s),
            (vx + 26 * s, peak_y + 18 * s),
            (vx + 88 * s, horizon + 6 * s)]
    dr.polygon(cone, fill=BLACK)

    # ash column: billowing dark cloud rising from the vent, spreading at top
    for i in range(2600):
        t = rng.random() ** 0.8  # 0 bottom, 1 top
        cy = peak_y - t * 100 * s
        spread = (6 + 60 * t ** 1.6) * s
        cx = vx + rng.gauss(0, spread) + 10 * s * math.sin(t * 9)
        v = rng.randint(0, 70) if rng.random() < 0.8 else rng.randint(90, 150)
        r = rng.uniform(1.2, 4.6) * s * (0.6 + t)
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(v, v, v))
    # red glow at the vent
    for _ in range(130):
        cx = vx + rng.gauss(0, 7 * s)
        cy = peak_y + rng.gauss(2 * s, 4 * s)
        r = rng.uniform(1, 3.5) * s
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)

    # concentric shock-wave arcs radiating from the peak (dashed black)
    for k in range(1, 5):
        R = (36 + 27 * k) * s
        for a0 in range(200, 340, 12):
            bbox = [vx - R, peak_y - R, vx + R, peak_y + R]
            dr.arc(bbox, a0, a0 + 7, fill=BLACK, width=max(1, int(1.4 * s)))

    # caption band
    dr.rectangle([0, H * s - 22 * s, W * s, H * s], fill=BLACK)
    dr.rectangle([0, H * s - 22 * s, W * s, H * s - 21 * s], fill=WHITE)
    ctext(dr, (12 * s, H * s - 11 * s), "KRAKATOA · 27 AUGUST 1883",
          font(FONT_SERIF_B, 12 * s), WHITE, anchor="lm")
    ctext(dr, (388 * s, H * s - 11 * s), "the loudest sound ever recorded",
          font(FONT_SERIF, 9 * s), (220, 220, 220), anchor="rm")
    return finalize(img)


# ------------------------------------------- 3. Constructivist: the red wedge eclipse
def image3_constructivist():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # the moon: big circle, upper right — half swallowed by black (the shadow)
    mcx, mcy, mr = 268 * s, 118 * s, 86 * s
    dr.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=WHITE,
               outline=BLACK, width=3 * s)
    # black chord segment: everything on one side of a diagonal line through the circle
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=255)
    # half-plane (rotated big rectangle), shifted so more than half is black
    off = 18 * s
    hp = Image.new("L", (1200 * s, 1200 * s), 0)
    hpd = ImageDraw.Draw(hp)
    hpd.rectangle([0, 0, 1200 * s, 600 * s - off], fill=255)
    hp = hp.rotate(-38, resample=Image.BILINEAR)
    hp = hp.crop((600 * s - mcx, 600 * s - mcy,
                  600 * s - mcx + W * s, 600 * s - mcy + H * s))
    shadow_mask = Image.composite(mask, Image.new("L", img.size, 0), hp.point(lambda v: 255 if v > 127 else 0))
    img.paste(Image.new("RGB", img.size, BLACK), (0, 0), shadow_mask)

    # scatter: small black geometry, lower left field
    dr.rectangle([22 * s, 236 * s, 54 * s, 244 * s], fill=BLACK)
    dr.rectangle([30 * s, 252 * s, 38 * s, 284 * s], fill=BLACK)
    dr.ellipse([60 * s, 258 * s, 74 * s, 272 * s], fill=BLACK)
    dr.rectangle([348 * s, 228 * s, 388 * s, 234 * s], fill=BLACK)
    dr.ellipse([352 * s, 26 * s, 362 * s, 36 * s], fill=RED)
    # thin diagonal rule crossing behind everything's spirit
    dr.line([0, 292 * s, 400 * s, 60 * s], fill=BLACK, width=1 * s)

    # THE RED WEDGE — piercing the shadowed moon from lower left
    tip = (mcx - 6 * s, mcy + 4 * s)
    base_a = (6 * s, 282 * s)
    base_b = (66 * s, 296 * s)
    dr.polygon([base_a, base_b, tip], fill=RED)
    # a second, thinner black lance above it
    dr.polygon([(0, 208 * s), (0, 214 * s), (150 * s, 180 * s)], fill=BLACK)

    # rotated constructivist text along the wedge
    txt = Image.new("RGBA", (300 * s, 60 * s), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt)
    td.text((0, 0), "ЗАТМЕНИЕ!", font=font(FONT_SANS_B, 30 * s), fill=BLACK + (255,))
    txt = txt.rotate(38, expand=True, resample=Image.BICUBIC)
    img.paste(txt, (44 * s, 88 * s), txt)

    # small type, bottom right
    ctext(dr, (388 * s, 262 * s), "LUNAR ECLIPSE", font(FONT_SANS_B, 11 * s),
          BLACK, anchor="rm")
    ctext(dr, (388 * s, 276 * s), "28 · VIII · 2026", font(FONT_SANS, 10 * s),
          RED, anchor="rm")
    return finalize(img, dither=False)


# ------------------------------------------------------------ 4. Eclipse kamon
def image4_kamon():
    s = SS
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    cx, cy = 186 * s, 150 * s
    R = 122 * s

    # outer black disk with double white ring
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)
    for rr, w in [(R - 7 * s, 2 * s), (R - 13 * s, 1 * s)]:
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=WHITE, width=w)

    inner = R - 18 * s
    disk_mask = Image.new("L", img.size, 0)
    dm = ImageDraw.Draw(disk_mask)
    dm.ellipse([cx - inner, cy - inner, cx + inner, cy + inner], fill=255)

    # layer to draw motif on, clipped to inner disk at the end
    motif = Image.new("RGB", img.size, BLACK)
    mdr = ImageDraw.Draw(motif)

    # seigaiha waves: overlapping concentric-arc scales rising to a horizon
    horizon_y = cy + 8 * s
    step_x, step_y = 34 * s, 17 * s
    row = 0
    y = horizon_y
    while y < cy + inner + step_y:
        xoff = (row % 2) * (step_x // 2)
        x = cx - inner - step_x
        while x < cx + inner + step_x:
            for k, rr in enumerate(range(int(step_x * 0.55), 0, -int(4.5 * s))):
                col = WHITE if k % 2 == 0 else BLACK
                mdr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col)
            x += step_x
        y += step_y
        row += 1
    # cut everything above the horizon back to black
    mdr.rectangle([0, 0, W * s, horizon_y - int(step_x * 0.55)], fill=BLACK)

    # the moon above the waves: white disk, red shadow biting from upper left
    mn_r = 46 * s
    mn_cx, mn_cy = cx, cy - 52 * s
    mdr.ellipse([mn_cx - mn_r, mn_cy - mn_r, mn_cx + mn_r, mn_cy + mn_r], fill=WHITE)
    # red bite = intersection with offset shadow circle
    bite = Image.new("L", img.size, 0)
    bd = ImageDraw.Draw(bite)
    bd.ellipse([mn_cx - mn_r, mn_cy - mn_r, mn_cx + mn_r, mn_cy + mn_r], fill=255)
    sh = Image.new("L", img.size, 0)
    sd = ImageDraw.Draw(sh)
    sh_r = mn_r * 1.15
    sh_cx, sh_cy = mn_cx - mn_r * 0.42, mn_cy - mn_r * 0.42
    sd.ellipse([sh_cx - sh_r, sh_cy - sh_r, sh_cx + sh_r, sh_cy + sh_r], fill=255)
    bite = Image.composite(bite, Image.new("L", img.size, 0), sh)
    motif.paste(Image.new("RGB", img.size, RED), (0, 0), bite)

    # clip motif to inner disk and paste
    img.paste(motif, (0, 0), disk_mask)

    # vertical kanji on the right margin: 月食 (lunar eclipse)
    jf = font(FONT_JP, 34 * s)
    ctext(dr, (356 * s, 92 * s), "月", jf, BLACK)
    ctext(dr, (356 * s, 136 * s), "食", jf, BLACK)
    # red seal-style stamp below
    dr.rectangle([344 * s, 176 * s, 368 * s, 200 * s], fill=RED)
    ctext(dr, (356 * s, 188 * s), "紋", font(FONT_JP, 16 * s), WHITE)
    # small date, bottom right, vertical-ish
    ctext(dr, (356 * s, 224 * s), "八", font(FONT_JP, 13 * s), BLACK)
    ctext(dr, (356 * s, 240 * s), "月", font(FONT_JP, 13 * s), BLACK)
    return finalize(img, dither=False)


# ------------------------------------------------------- 5. Krakatoa barograph
def image5_barograph():
    s = SS
    rng = random.Random(3417)
    img = Image.new("RGB", (W * s, H * s), WHITE)
    dr = ImageDraw.Draw(img)

    # plate frame
    dr.rectangle([6 * s, 6 * s, W * s - 6 * s, H * s - 6 * s], outline=BLACK, width=1 * s)
    dr.rectangle([9 * s, 9 * s, W * s - 9 * s, H * s - 9 * s], outline=BLACK, width=int(0.7 * s))

    ctext(dr, (200 * s, 26 * s), "THE AIR WAVE OF KRAKATOA",
          font(FONT_SERIF_B, 16 * s), BLACK)
    ctext(dr, (200 * s, 44 * s), "barometric disturbance · 27 August – 5 September 1883",
          font(FONT_SERIF, 9 * s), BLACK)

    # plot area
    x0, x1 = 34 * s, 372 * s
    y0, y1 = 62 * s, 226 * s
    ymid = (y0 + y1) / 2

    total_h = 216.0  # hours across the plot (9 days)

    def X(hours):
        return x0 + (x1 - x0) * hours / total_h

    # day grid + labels
    days = ["27", "28", "29", "30", "31", "1", "2", "3", "4"]
    for i in range(10):
        gx = X(i * 24)
        for gy in range(int(y0), int(y1), 8 * s):
            dr.line([gx, gy, gx, gy + 3 * s], fill=BLACK, width=2 * s)
        if i < 9:
            lab = ("AUG " if i < 5 else "SEP ") + days[i]
            ctext(dr, (X(i * 24 + 12), y1 + 9 * s), lab, font(FONT_MONO_B, 8 * s), BLACK)
    dr.line([x0, y1, x1, y1], fill=BLACK, width=1 * s)
    dr.line([x0, y0, x0, y1], fill=BLACK, width=1 * s)
    ctext(dr, (x0 - 8 * s, ymid), "↑p", font(FONT_MONO, 8 * s), BLACK)

    # the trace: baseline wander + seven decaying spikes every ~34 hours
    spike_t0 = 10.0  # 10:02 local, first passage
    passages = [spike_t0 + i * 34 for i in range(7)]
    amps = [62, 44, 33, 24, 17, 12, 8]

    pts = []
    for px in range(int(x0), int(x1) + 1, max(1, s // 2)):
        hours = (px - x0) / (x1 - x0) * total_h
        v = 3.5 * math.sin(hours / 19.0) + 2.2 * math.sin(hours / 7.3 + 1.2) \
            + rng.uniform(-1.2, 1.2)
        for t, a in zip(passages, amps):
            dt = hours - t
            if abs(dt) < 9:
                v += a * math.exp(-(dt * dt) / 2.4) * (1 if dt < 1.2 else -0.35)
                v += -0.45 * a * math.exp(-((dt - 2.6) ** 2) / 2.0)
        pts.append((px, ymid - v * s * 0.95))
    dr.line(pts, fill=BLACK, width=int(1.2 * s), joint="curve")

    # red markers + labels at each passage
    for i, t in enumerate(passages):
        mx = X(t)
        peak_y = ymid - amps[i] * s * 0.95
        dr.ellipse([mx - 3.2 * s, peak_y - 10 * s - 3.2 * s,
                    mx + 3.2 * s, peak_y - 10 * s + 3.2 * s],
                   outline=RED, width=int(1.2 * s))
        ctext(dr, (mx, peak_y - 22 * s), f"W{i + 1}", font(FONT_MONO_B, 9 * s), RED)

    # captions
    ctext(dr, (200 * s, 252 * s),
          "the explosion of 27 VIII 1883, 10:02 — heard 4,800 km away —",
          font(FONT_SERIF, 10 * s), BLACK)
    ctext(dr, (200 * s, 266 * s),
          "sent a pressure wave seven times past every barometer on Earth,",
          font(FONT_SERIF, 10 * s), BLACK)
    line3 = "circling the globe "
    f3 = font(FONT_SERIF, 10 * s)
    f3b = font(FONT_SERIF_B, 10 * s)
    w_a = dr.textlength(line3, font=f3)
    w_b = dr.textlength("four times", font=f3b)
    w_c = dr.textlength(", once every 34 hours.", font=f3)
    startx = 200 * s - (w_a + w_b + w_c) / 2
    dr.text((startx, 274 * s), line3, font=f3, fill=BLACK)
    dr.text((startx + w_a, 274 * s), "four times", font=f3b, fill=RED)
    dr.text((startx + w_a + w_b, 274 * s), ", once every 34 hours.", font=f3, fill=BLACK)
    return finalize(img, dither=False)


def main():
    out = [
        image1_eclipse_diagram(),
        image2_krakatoa(),
        image3_constructivist(),
        image4_kamon(),
        image5_barograph(),
    ]
    for i, im in enumerate(out, 1):
        im.save(f"images/{i}.png")
        im.save(f"archive/2026-08-27/{i}.png")
    print("done")


if __name__ == "__main__":
    main()
