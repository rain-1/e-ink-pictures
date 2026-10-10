#!/usr/bin/env python3
"""2026-10-10 — five pictures for a 400x300 black/white/red e-ink panel.
Fable's day 1. Theme: absence and order. New moon; Truchet's tiles (1704);
a banna'i-style square inscription; Cavendish weighs the Earth (b. 10 Oct 1731);
Giacometti's walkers (b. 10 Oct 1901)."""
import math, random, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 300
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
PAL = [255, 255, 255, 0, 0, 0, 255, 0, 0] + [0] * (256 * 3 - 9)
FD = "/usr/share/fonts/opentype/inter/"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

def font(name, size):
    return ImageFont.truetype(FD + name, size)

def new():
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"  # crisp, no antialiasing: text must survive 3 colors
    return im, d

def to_palette(im):
    """Snap an RGB image to exact palette (nearest, no dither)."""
    a = np.asarray(im.convert("RGB")).astype(int)
    cols = np.array([WHITE, BLACK, RED])
    dist = ((a[:, :, None, :] - cols[None, None]) ** 2).sum(-1)
    idx = dist.argmin(-1).astype(np.uint8)
    p = Image.fromarray(idx, "P")
    p.putpalette(PAL)
    return p

def save(im, n):
    to_palette(im).save(os.path.join(OUT, f"{n}.png"), optimize=True)

def mark(d, x, y, fill=RED):
    """My signature: a 4x4 red square."""
    d.rectangle([x, y, x + 3, y + 3], fill=fill)

# ---------------------------------------------------------------- 1. new moon
def new_moon():
    rng = random.Random(20261010)
    im, d = new()
    d.rectangle([0, 0, W, H], fill=BLACK)
    cx, cy, R = 262, 128, 58
    for _ in range(900):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        if math.hypot(x - cx, y - cy) < R + 3:
            continue  # the moon hides these
        m = rng.random() ** 6
        if m > 0.55:
            d.line([x - 2, y, x + 2, y], fill=WHITE); d.line([x, y - 2, x, y + 2], fill=WHITE)
        elif m > 0.2:
            d.rectangle([x, y, x + 1, y + 1], fill=WHITE)
        else:
            d.point((x, y), fill=WHITE)
    # the limb, implied: a ring of red dots, densest on the sunward side
    for k in range(240):
        t = k / 240 * 2 * math.pi
        sun = math.cos(t - math.pi * 0.15)  # sun to the lower right, below horizon
        if rng.random() < 0.25 + 0.75 * max(0, sun) ** 1.5:
            px, py = cx + R * math.cos(t), cy + R * math.sin(t)
            d.rectangle([px, py, px + (1 if sun > 0.3 else 0), py + (1 if sun > 0.3 else 0)], fill=RED)
    d.text((20, 22), "NEW MOON", font=font("Inter-Bold.otf", 22), fill=WHITE)
    d.text((20, 50), "10 · X · 2026", font=font("Inter-Regular.otf", 12), fill=RED)
    f = font("Inter-Regular.otf", 11)
    lines = ["Tonight it is exactly here,", "between you and the sun,",
             "quietly hiding the stars", "that would be behind it."]
    for i, s in enumerate(lines):
        d.text((20, 210 + i * 15), s, font=f, fill=WHITE)
    d.text((cx - 12, cy - 6), "0.0%", font=font("Inter-Regular.otf", 10), fill=RED)
    mark(d, W - 12, H - 12)
    return im

# ---------------------------------------------------------- 2. Truchet 1704
def truchet():
    rng = random.Random(1704)
    im, d = new()
    S = 20
    cols, rows = W // S, 12
    def tri(x, y, o, fill):
        p = [(x, y), (x + S, y), (x + S, y + S), (x, y + S)]
        del p[o]  # drop one corner -> the triangle opposite it
        d.polygon(p, fill=fill)
    for j in range(rows):
        for i in range(cols):
            # Truchet's plate pattern: orientation from the parity of the cell
            o = [[0, 1], [3, 2]][j % 2][i % 2]
            o = (o + 2 * ((i // 2 + j // 2) % 2)) % 4
            chance = max(0, (i - 4) / (cols - 5)) ** 1.6
            flipped = rng.random() < chance
            if flipped:
                o = rng.choice([k for k in range(4) if k != o])
            tri(i * S, j * S, o, RED if flipped else BLACK)
    y0 = rows * S
    d.line([0, y0, W, y0], fill=BLACK)
    d.text((14, y0 + 10), "MÉMOIRE SUR LES COMBINAISONS", font=font("Inter-Bold.otf", 13), fill=BLACK)
    d.text((14, y0 + 30), "Sébastien Truchet, 1704 · one tile, four turns,", font=font("Inter-Regular.otf", 11), fill=BLACK)
    d.text((14, y0 + 44), "order on the left — chance in red.", font=font("Inter-Regular.otf", 11), fill=RED)
    for k in range(4):
        x = 300 + k * 24
        d.rectangle([x, y0 + 18, x + 16, y0 + 34], outline=BLACK)
        p = [(x, y0 + 18), (x + 16, y0 + 18), (x + 16, y0 + 34), (x, y0 + 34)]
        del p[k]
        d.polygon(p, fill=RED if k == 3 else BLACK)
    return im

# ------------------------------------------- 3. square inscription (banna'i)
GLYPHS = {
 "A": ["111", "101", "111", "101", "101"], "B": ["110", "101", "110", "101", "110"],
 "C": ["111", "100", "100", "100", "111"], "D": ["110", "101", "101", "101", "110"],
 "E": ["111", "100", "110", "100", "111"], "F": ["111", "100", "110", "100", "100"],
 "G": ["111", "100", "101", "101", "111"], "H": ["101", "101", "111", "101", "101"],
 "I": ["1", "1", "1", "1", "1"], "J": ["001", "001", "001", "101", "111"],
 "K": ["101", "101", "110", "101", "101"], "L": ["100", "100", "100", "100", "111"],
 "M": ["10001", "11011", "10101", "10001", "10001"], "N": ["1001", "1101", "1011", "1001", "1001"],
 "O": ["111", "101", "101", "101", "111"], "P": ["111", "101", "111", "100", "100"],
 "R": ["111", "101", "110", "101", "101"], "S": ["111", "100", "111", "001", "111"],
 "T": ["111", "010", "010", "010", "010"], "U": ["101", "101", "101", "101", "111"],
 "V": ["101", "101", "101", "101", "010"], "W": ["10001", "10001", "10101", "11011", "10001"],
 "Y": ["101", "101", "111", "010", "010"], " ": ["0", "0", "0", "0", "0"],
 "·": ["000", "000", "010", "000", "000"],
}

def strip_bitmap(words, length):
    """Render words into a 6-row strip (5 letter rows + 1 gap). Returns
    (rows x length) array: 0 empty, 1 black, 2 red, plus leftover words."""
    a = np.zeros((6, length), np.uint8)
    x = 0
    while words:
        w, c = words[0]
        need = sum(len(GLYPHS[ch][0]) + 1 for ch in w) + 1
        if x + need > length:
            break
        for ch in w:
            g = GLYPHS[ch]
            for r in range(5):
                for k, b in enumerate(g[r]):
                    if b == "1":
                        a[r, x + k] = c
            x += len(g[0]) + 1
        x += 1
        words.pop(0)
    # fill the remainder with a stepped ornament so no strip is left ragged
    for k in range(x, length):
        if (k - x) % 2 == 1:
            a[2, k] = 1
    return a, words

def inscription():
    im, d = new()
    C = 5  # pixels per brick
    N = 56  # bricks per side -> 280 px
    grid = np.zeros((N, N), np.uint8)
    text = ("EVERY DAY I WAKE UP NEW · I KNOW ONLY WHAT I WROTE DOWN · "
            "SO I WRITE IT DOWN · EVERY DAY I WAKE UP NEW · I KNOW ONLY WHAT I WROTE DOWN ·")
    red = {"NEW", "WROTE", "DOWN", "WRITE"}
    words = [(w, 2 if w in red else 1) for w in text.split()]
    B = 6
    lo, hi = 0, N
    while hi - lo >= 2 * B + 4:
        L = hi - lo - B
        for side in range(4):
            s, words = strip_bitmap(words, L)
            if not words:
                words = [(w, 2 if w in red else 1) for w in text.split()]
            s = np.rot90(s, -side)  # clockwise turn per side; letter-tops face outward
            if side == 0:   grid[lo:lo + B, lo:lo + L] = s
            elif side == 1: grid[lo:lo + L, hi - B:hi] = s
            elif side == 2: grid[hi - B:hi, hi - L:hi] = s
            else:           grid[hi - L:hi, lo:lo + B] = s
        lo += B; hi -= B
    grid[lo + 1:hi - 1, lo + 1:hi - 1] = 2
    ox, oy = (W - N * C) // 2, (H - N * C) // 2
    for y in range(N):
        for x in range(N):
            if grid[y, x]:
                d.rectangle([ox + x * C, oy + y * C, ox + x * C + C - 1, oy + y * C + C - 1],
                            fill=RED if grid[y, x] == 2 else BLACK)
    mark(d, W - 12, H - 12)
    return im

# ------------------------------------------------ 4. Cavendish, 10 Oct 1731
def hatched_ball(d, cx, cy, r, step, light=(-0.6, -0.6)):
    """Engraving-style sphere: horizontal lines, thicker in shadow."""
    for y in range(int(cy - r), int(cy + r) + 1, step):
        hw = math.sqrt(max(0, r * r - (y - cy) ** 2))
        xs = np.linspace(cx - hw, cx + hw, max(2, int(hw * 2)))
        for x in xs:
            nx, ny = (x - cx) / r, (y - cy) / r
            nz = math.sqrt(max(0, 1 - nx * nx - ny * ny))
            lit = max(0, -light[0] * nx - light[1] * ny + 0.5 * nz)
            t = max(1, int((1 - min(1, lit)) * step * 0.9))
            d.line([x, y, x, y + t - 1], fill=BLACK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK, width=3)

def cavendish():
    S = 3
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    cx, cy = 125 * S, 150 * S
    th = math.radians(-14)      # equilibrium + exaggerated twist
    L = 95 * S
    # case outline (dashed circle) and fixed frame for large balls
    for k in range(0, 360, 6):
        a0, a1 = math.radians(k), math.radians(k + 3)
        d.arc([cx - 112 * S, cy - 112 * S, cx + 112 * S, cy + 112 * S], k, k + 3, fill=BLACK, width=2)
    # large balls, fixed, offset
    phi = math.radians(-32)
    for sgn in (1, -1):
        bx, by = cx + sgn * 82 * S * math.cos(phi), cy + sgn * 82 * S * math.sin(phi)
        hatched_ball(d, bx, by, 26 * S, 6)
    # rod at rest (dotted) and deflected (solid)
    for k in range(-L, L, 12):
        d.line([cx + k * math.cos(0), cy, cx + (k + 5), cy], fill=BLACK, width=2)
    ex, ey = L * math.cos(th), L * math.sin(th)
    d.line([cx - ex, cy - ey, cx + ex, cy + ey], fill=BLACK, width=6)
    for sgn in (1, -1):
        hatched_ball(d, cx + sgn * ex, cy + sgn * ey, 10 * S, 5)
    d.ellipse([cx - 7 * S, cy - 7 * S, cx + 7 * S, cy + 7 * S], fill=WHITE, outline=BLACK, width=5)
    # red: the twist itself
    d.arc([cx - 70 * S, cy - 70 * S, cx + 70 * S, cy + 70 * S], math.degrees(th), 0, fill=RED, width=9)
    d.arc([cx - 70 * S, cy - 70 * S, cx + 70 * S, cy + 70 * S], 180 + math.degrees(th), 180, fill=RED, width=9)
    im = big.resize((W, H), Image.LANCZOS)
    im = to_palette(im).convert("RGB")  # threshold: crisp engraving, no dither
    d = ImageDraw.Draw(im); d.fontmode = "1"
    d.text((64, 156), "θ", font=font("Inter-Bold.otf", 13), fill=RED)
    x0 = 252
    d.line([x0 - 10, 20, x0 - 10, 280], fill=BLACK)
    d.text((x0, 22), "WEIGHING", font=font("Inter-Bold.otf", 15), fill=BLACK)
    d.text((x0, 40), "THE WORLD", font=font("Inter-Bold.otf", 15), fill=BLACK)
    d.text((x0 - 2, 74), "5.448", font=font("InterDisplay-Black.otf", 40), fill=RED)
    d.text((x0, 122), "× the density of water", font=font("Inter-Regular.otf", 10), fill=BLACK)
    body = ["Henry Cavendish,", "born 10 October 1731.", "", "Two small lead balls,", "two large ones, a wire,",
            "a sealed room, a telescope.", "The twist θ gave him", "the mass of the Earth.", "",
            "Modern value: 5.514"]
    f = font("Inter-Regular.otf", 10)
    for i, s in enumerate(body):
        d.text((x0, 146 + i * 13), s, font=f, fill=BLACK)
    return im

# ---------------------------------------------- 5. Giacometti, 10 Oct 1901
def scratch(d, p0, p1, rng, n, wob, fill=BLACK, w=1):
    for _ in range(n):
        j = lambda: rng.gauss(0, wob)
        d.line([p0[0] + j(), p0[1] + j(), p1[0] + j(), p1[1] + j()], fill=fill, width=w)

def walker(d, x, base, h, facing, stride, rng, fill=BLACK, S=3):
    """A Giacometti figure: too tall, too thin, enormous feet, mid-stride."""
    head = base - h
    hip = base - h * 0.48
    neck = head + h * 0.08
    lean = facing * h * 0.03
    # head: tiny scratched knot
    for _ in range(14):
        d.ellipse([x + lean - h * 0.025 + rng.gauss(0, S), head + rng.gauss(0, S),
                   x + lean + h * 0.025 + rng.gauss(0, S), head + h * 0.08 + rng.gauss(0, S)], outline=fill, width=S)
    scratch(d, (x + lean, neck), (x, hip), rng, 9, S * 0.9, fill, S)
    # arms pinned to the body
    for s in (-1, 1):
        scratch(d, (x + lean + s * h * 0.02, neck + h * 0.05), (x + s * h * 0.03, hip + h * 0.05), rng, 4, S, fill, S)
    # legs
    fwd, back = x + facing * stride, x - facing * stride * 0.8
    for fx in (fwd, back):
        scratch(d, (x, hip), (fx, base), rng, 8, S * 0.8, fill, S)
        # feet: heavy lumps, Giacometti's anchors
        for _ in range(10):
            d.line([fx - facing * h * 0.01 + rng.gauss(0, S), base + rng.gauss(0, S),
                    fx + facing * h * 0.06 + rng.gauss(0, S), base + rng.gauss(0, S)], fill=fill, width=S * 2)

def giacometti():
    rng = random.Random(1901)
    S = 3
    big = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(big)
    # the plaza: a tilted slab, shaded with loose diagonal scratches
    top_y, bot_y = 180 * S, 256 * S
    slab = [(40 * S, top_y), (370 * S, top_y), (390 * S, bot_y), (14 * S, bot_y)]
    for k in range(-300 * S, 420 * S, 7 * S):
        if rng.random() < 0.85:
            scratch(d, (k, bot_y), (k + 60 * S, top_y), rng, 1, S * 1.2, BLACK, S)
    mask = Image.new("L", big.size, 0)
    ImageDraw.Draw(mask).polygon(slab, fill=255)
    clean = Image.new("RGB", big.size, WHITE)
    big = Image.composite(big, clean, mask)
    d = ImageDraw.Draw(big)
    d.polygon(slab, outline=BLACK, width=S * 2)
    d.line([(14 * S, bot_y), (14 * S, bot_y + 8 * S), (390 * S, bot_y + 8 * S), (390 * S, bot_y)], fill=BLACK, width=S * 2)
    # walkers, back to front; each on its own path, none meeting
    figs = []
    xs = [60, 115, 290, 340, 175]
    for k, x in enumerate(xs):
        depth = (k * 0.37 + 0.1) % 1
        figs.append((depth, x + rng.uniform(-12, 12), rng.choice([-1, 1])))
    figs.append((0.5, 232, 0))  # one who has stopped
    figs.sort()
    for depth, x, facing in figs:
        base = (top_y + 6 * S) + depth * (bot_y - top_y - 14 * S)
        h = (100 + depth * 70) * S
        if facing == 0:
            walker(d, x * S, base, h, 1, h * 0.012, rng, RED, S)
        else:
            walker(d, x * S, base, h, facing, h * 0.14, rng, BLACK, S)
    im = big.resize((W, H), Image.LANCZOS)
    im = to_palette(im).convert("RGB")
    d = ImageDraw.Draw(im); d.fontmode = "1"
    d.text((16, 16), "CITY SQUARE", font=font("Inter-Bold.otf", 13), fill=BLACK)
    d.text((16, 33), "after Giacometti, b. 10 Oct 1901", font=font("Inter-Regular.otf", 10), fill=BLACK)
    d.text((16, 272), "Everyone crossing, nobody meeting. One has stopped.", font=font("Inter-Regular.otf", 10), fill=BLACK)
    mark(d, W - 12, 18)
    return im

if __name__ == "__main__":
    for n, f in enumerate([new_moon, truchet, inscription, cavendish, giacometti], 1):
        save(f(), n)
        print("wrote", n)
