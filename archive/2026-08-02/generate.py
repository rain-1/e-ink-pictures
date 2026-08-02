#!/usr/bin/env python3
"""
e-ink pictures — 2026-08-02
400x300, palette: black / white / red.

Five pieces:
  1. The Dead Man's Hand — 150 years since Wild Bill Hickok, Deadwood, Aug 2 1876
  2. The Red Wedge — homage to El Lissitzky (1919 -> 2026)
  3. Tonight's Sky — waning gibbous Moon passes Saturn; Mercury at elongation
  4. Truchet Current — filled quarter-disc Truchet tiling with a red flow field
  5. Sandpile — abelian sandpile, 2^17 grains toppled to stability
"""

import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
S = 3                      # supersample factor for smooth pieces
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

OUT = os.path.dirname(os.path.abspath(__file__))
random.seed(20260802)

FONT_DIR = "/usr/share/fonts/truetype"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

PAL_IMG = Image.new("P", (1, 1))
PAL_IMG.putpalette(list(BLACK) + list(WHITE) + list(RED) + list(BLACK) * 253)

def snap(img):
    """Nearest-palette quantize (no dither) — for flat, hard-edged art."""
    a = np.asarray(img.convert("RGB")).astype(int)
    pal = np.array([BLACK, WHITE, RED])
    d = ((a[:, :, None, :] - pal[None, None, :, :]) ** 2).sum(-1)
    idx = d.argmin(-1).astype(np.uint8)
    out = Image.fromarray(idx, "P")
    out.putpalette(PAL_IMG.getpalette())
    return out

def dither(img):
    """Floyd-Steinberg into the 3-color palette — for tonal pieces."""
    return img.convert("RGB").quantize(palette=PAL_IMG, dither=Image.FLOYDSTEINBERG)

def finish(img, path, tonal=False):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    out = dither(img) if tonal else snap(img)
    out.save(path, optimize=True)
    print("wrote", path)


# ----------------------------------------------------------------------------
# 1. THE DEAD MAN'S HAND
# ----------------------------------------------------------------------------
def pip(d, cx, cy, s, suit, col):
    if suit == "spade":
        d.polygon([(cx, cy - s), (cx - 0.92 * s, cy + 0.42 * s),
                   (cx + 0.92 * s, cy + 0.42 * s)], fill=col)
        for sx in (-0.45, 0.45):
            d.ellipse([cx + sx * s - 0.46 * s, cy - 0.04 * s,
                       cx + sx * s + 0.46 * s, cy + 0.88 * s], fill=col)
        d.polygon([(cx, cy + 0.15 * s), (cx - 0.30 * s, cy + 1.05 * s),
                   (cx + 0.30 * s, cy + 1.05 * s)], fill=col)
    elif suit == "club":
        for ang in (90, 210, 330):
            a = math.radians(ang)
            ox, oy = 0.48 * s * math.cos(a), -0.48 * s * math.sin(a)
            d.ellipse([cx + ox - 0.44 * s, cy + oy - 0.44 * s - 0.1 * s,
                       cx + ox + 0.44 * s, cy + oy + 0.44 * s - 0.1 * s], fill=col)
        d.polygon([(cx, cy), (cx - 0.30 * s, cy + 1.05 * s),
                   (cx + 0.30 * s, cy + 1.05 * s)], fill=col)

def card(w, h, rank=None, suit=None, back=False):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=w // 9, fill=WHITE, outline=BLACK, width=4)
    if back:
        m = w // 9
        d.rounded_rectangle([m, m, w - 1 - m, h - 1 - m], radius=w // 14, fill=RED)
        step = w // 6
        for k in range(-h // step, 2 * h // step):
            d.line([(m, m + k * step), (w - m, m + k * step + (w - 2 * m))],
                   fill=WHITE, width=5)
            d.line([(w - m, m + k * step), (m, m + k * step + (w - 2 * m))],
                   fill=WHITE, width=5)
        d.rounded_rectangle([m, m, w - 1 - m, h - 1 - m], radius=w // 14, outline=WHITE, width=5)
        return im
    f = font("dejavu/DejaVuSerif-Bold.ttf", int(w * 0.24))
    for (ax, ay, flip) in [(w * 0.14, h * 0.055, False), (w * 0.86, h * 0.945, True)]:
        tag = Image.new("RGBA", (int(w * 0.26), int(h * 0.30)), (0, 0, 0, 0))
        td = ImageDraw.Draw(tag)
        td.text((tag.width // 2, 0), rank, font=f, fill=BLACK, anchor="ma")
        pip(td, tag.width // 2, int(h * 0.20), w * 0.085, suit, BLACK)
        if flip:
            tag = tag.rotate(180)
        im.alpha_composite(tag, (int(ax - tag.width / 2), int(ay - (0 if not flip else tag.height))))
    if rank == "A":
        pip(d, w / 2, h * 0.46, w * 0.30, suit, BLACK)
    else:  # 8
        cols_x = (w * 0.32, w * 0.68)
        rows_y = (h * 0.24, h * 0.435, h * 0.625, h * 0.82)
        pts = [(x, y) for x in cols_x for y in rows_y][:6]
        pts += [(w * 0.5, h * 0.33), (w * 0.5, h * 0.72)]
        for (px, py) in pts:
            pip(d, px, py - w * 0.05, w * 0.095, suit, BLACK)
    return im

def img1_dead_mans_hand():
    im = Image.new("RGB", (W * S, H * S), BLACK)
    d = ImageDraw.Draw(im)
    # wood-plank table hints
    for y in (620, 730, 840):
        d.line([(0, y), (W * S, y)], fill=(60, 60, 60), width=3)
    f_title = font("dejavu/DejaVuSerif-Bold.ttf", 66)
    f_small = font("dejavu/DejaVuSansMono.ttf", 30)
    d.text((W * S // 2, 34), "THE DEAD MAN'S HAND", font=f_title, fill=WHITE, anchor="ma")
    d.line([(150, 122), (W * S - 150, 122)], fill=RED, width=6)
    cw, ch = 264, 372
    hand = [("A", "spade"), ("A", "club"), ("8", "spade"), ("8", "club"), None]
    n = len(hand)
    for i, spec in enumerate(hand):
        c = card(cw, ch, back=True) if spec is None else card(cw, ch, *spec)
        ang = -16 + 8 * i
        cx = W * S // 2 + int((i - (n - 1) / 2) * 205)
        cy = 520 + int(abs(i - (n - 1) / 2) ** 2 * 14)
        rc = c.rotate(-ang, expand=True, resample=Image.BICUBIC)
        im.paste(rc, (cx - rc.width // 2, cy - rc.height // 2), rc)
    d.text((W * S // 2, H * S - 96),
           "DEADWOOD, DAKOTA TERRITORY · AUGUST 2, 1876", font=f_small,
           fill=WHITE, anchor="ma")
    d.text((W * S // 2, H * S - 52), "150 YEARS AGO TONIGHT", font=f_small,
           fill=RED, anchor="ma")
    finish(im, os.path.join(OUT, "1.png"))


# ----------------------------------------------------------------------------
# 2. THE RED WEDGE (after El Lissitzky, 1919)
# ----------------------------------------------------------------------------
def img2_red_wedge():
    im = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(im)
    # black field, diagonal frontier
    d.polygon([(560, 0), (W * S, 0), (W * S, H * S), (240, H * S)], fill=BLACK)
    # white circle inside the black field
    cx, cy, r = 800, 445, 320
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    # the red wedge, piercing the circle's heart
    d.polygon([(0, 190), (0, 700), (cx + 6, cy)], fill=RED)
    # thin black wedge shadowing it
    d.polygon([(0, 740), (0, 800), (560, 585)], fill=BLACK)
    # debris: small bars scattered on both fields
    for (x, y, w_, h_, a, col) in [
            (150, 105, 130, 34, -20, BLACK), (330, 65, 70, 22, -20, RED),
            (935, 785, 150, 40, -20, WHITE), (1035, 705, 66, 22, -20, RED),
            (150, 800, 90, 26, -20, RED), (700, 105, 90, 90, 0, RED)]:
        bar = Image.new("RGBA", (w_, h_), col + (255,))
        bar = bar.rotate(a, expand=True)
        im.paste(bar, (x, y), bar)
    # small white square gate on the frontier
    d.rectangle([548, 300, 610, 362], fill=WHITE)
    d.rectangle([566, 318, 592, 344], fill=RED)
    f_big = font("dejavu/DejaVuSans-Bold.ttf", 44)
    f_sm = font("dejavu/DejaVuSans-Bold.ttf", 26)
    d.text((28, 24), "КЛИНОМ КРАСНЫМ", font=f_big, fill=BLACK)
    d.text((W * S - 28, H * S - 60), "БЕЙ БЕЛЫХ", font=f_big, fill=WHITE, anchor="rs")
    d.text((W * S - 24, 22), "after El Lissitzky · 1919 → 2026", font=f_sm,
           fill=WHITE, anchor="ra")
    finish(im, os.path.join(OUT, "2.png"))


# ----------------------------------------------------------------------------
# 3. TONIGHT'S SKY — Moon passes Saturn
# ----------------------------------------------------------------------------
def img3_moon_saturn():
    im = Image.new("RGB", (W * S, H * S), BLACK)
    d = ImageDraw.Draw(im)
    rnd = random.Random(802)
    for _ in range(210):
        x, y = rnd.randrange(W * S), rnd.randrange(H * S)
        r = rnd.choice([1, 1, 2, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(200, 200, 200))
    # waning gibbous moon (~85% lit, bright limb on the left)
    mx, my, mr = 330, 330, 225
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(235, 235, 235))
    maria = [(-60, -95, 85, 0.55), (55, -60, 95, 0.5), (10, 40, 70, 0.45),
             (-105, 25, 60, 0.5), (95, 60, 55, 0.42), (-30, 130, 45, 0.5)]
    for (ox, oy, r, g) in maria:
        gv = int(235 * g)
        d.ellipse([mx + ox - r, my + oy - r, mx + ox + r, my + oy + r],
                  fill=(gv, gv, gv))
    for _ in range(90):  # crater speckle
        a = rnd.uniform(0, 2 * math.pi); rr = mr * math.sqrt(rnd.uniform(0, 0.92))
        x, y = mx + rr * math.cos(a), my + rr * math.sin(a)
        cr = rnd.uniform(2, 9)
        gv = rnd.choice([150, 170, 255, 255])
        d.ellipse([x - cr, y - cr, x + cr, y + cr], fill=(gv, gv, gv))
    # terminator: dark sliver on the right (waning, ~85%)
    sl = Image.new("L", (W * S, H * S), 0)
    sd = ImageDraw.Draw(sl)
    sd.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=255)
    sd.ellipse([mx - mr - 155, my - mr, mx + mr - 155, my + mr], fill=0)
    dark = Image.new("RGB", (W * S, H * S), (25, 25, 25))
    im.paste(dark, (0, 0), sl)
    # Saturn, lower right of the moon
    sx, sy = 810, 620
    ring = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse([20, 118, 280, 182], outline=(255, 255, 255), width=9)
    rd.ellipse([150 - 52, 150 - 52, 150 + 52, 150 + 52], fill=(230, 230, 230))
    rd.ellipse([30, 124, 270, 176], outline=(160, 160, 160), width=4)
    ring = ring.rotate(18, resample=Image.BICUBIC)
    im.paste(ring, (sx - 150, sy - 150), ring)
    d.text((sx - 165, sy), "SATURN", font=font("dejavu/DejaVuSansMono-Bold.ttf", 32),
           fill=RED, anchor="rm")
    # text panel
    f_h = font("dejavu/DejaVuSerif-Bold.ttf", 52)
    f_b = font("dejavu/DejaVuSans.ttf", 31)
    f_m = font("dejavu/DejaVuSansMono.ttf", 29)
    f_mb = font("dejavu/DejaVuSansMono-Bold.ttf", 34)
    d.text((1168, 60), "TONIGHT", font=f_h, fill=WHITE, anchor="ra")
    d.text((1168, 124), "2 AUGUST 2026", font=f_mb, fill=RED, anchor="ra")
    d.multiline_text((1168, 190),
        "Waning gibbous Moon\nglides past Saturn,\nlate evening → dawn.\n"
        "Mercury at greatest\nelongation, predawn E.",
        font=f_b, fill=WHITE, anchor="ra", align="right", spacing=12)
    d.line([(60, 742), (1140, 742)], fill=(120, 120, 120), width=3)
    d.text((60, 768), "AUG 12", font=f_mb, fill=RED)
    d.text((222, 770), "Perseids peak + TOTAL SOLAR ECLIPSE, moonless",
           font=f_m, fill=WHITE)
    d.text((60, 814), "AUG 28", font=f_mb, fill=RED)
    d.text((222, 816), "Sturgeon Moon + partial LUNAR eclipse (96%)",
           font=f_m, fill=WHITE)
    finish(im, os.path.join(OUT, "3.png"), tonal=True)


# ----------------------------------------------------------------------------
# 4. TRUCHET CURRENT
# ----------------------------------------------------------------------------
def img4_truchet():
    t = 20 * S
    cols, rows = W // 20, H // 20
    im = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(im)
    rnd = random.Random(20260802)

    def field(cx, cy):
        x, y = cx / cols, cy / rows
        return (math.sin(4.1 * x + 1.7) + math.sin(5.3 * y - 0.6)
                + math.sin(3.7 * (x + y)) + math.sin(6.1 * (x - y) + 2.2))

    for gy in range(rows):
        for gx in range(cols):
            x0, y0 = gx * t, gy * t
            fg = RED if field(gx + 0.5, gy + 0.5) > 1.15 else BLACK
            # Sébastien Truchet's original 1704 tile: a square halved
            # along a diagonal, in one of four orientations.
            corners = [(x0, y0), (x0 + t, y0), (x0 + t, y0 + t), (x0, y0 + t)]
            k = rnd.randrange(4)
            d.polygon([corners[k], corners[(k + 1) % 4], corners[(k + 2) % 4]],
                      fill=fg)
    finish(im, os.path.join(OUT, "4.png"))


# ----------------------------------------------------------------------------
# 5. SANDPILE
# ----------------------------------------------------------------------------
def img5_sandpile():
    n_grains = 2 ** 17
    z = np.zeros((H, W), dtype=np.int64)
    z[H // 2, W // 2] = n_grains
    touched = np.zeros_like(z, dtype=bool)
    while True:
        over = z >= 4
        if not over.any():
            break
        touched |= over
        q = z >> 2
        q[~over] = 0
        z -= 4 * q
        z[1:, :] += q[:-1, :]; z[:-1, :] += q[1:, :]
        z[:, 1:] += q[:, :-1]; z[:, :-1] += q[:, 1:]
    touched |= z > 0
    rgb = np.zeros((H, W, 3), dtype=np.uint8)                 # bg black
    rgb[touched & (z == 0)] = BLACK
    rgb[touched & (z == 1)] = RED
    rgb[touched & (z == 2)] = BLACK
    rgb[touched & (z == 3)] = WHITE
    im = Image.fromarray(rgb)
    d = ImageDraw.Draw(im)
    f = font("dejavu/DejaVuSansMono.ttf", 11)
    d.text((6, H - 16), "ABELIAN SANDPILE", fill=WHITE, font=f)
    d.text((W - 6, H - 16), "2¹⁷ GRAINS", fill=RED, font=f, anchor="ra")
    finish(im, os.path.join(OUT, "5.png"))


if __name__ == "__main__":
    img1_dead_mans_hand()
    img2_red_wedge()
    img3_moon_saturn()
    img4_truchet()
    img5_sandpile()
