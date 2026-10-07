"""4. (untitled) — ebru, Ottoman paper marbling, done with the exact math of ink on water.

No words. Ink drops spread as area-preserving maps:  p' = c + (p-c)·sqrt(1 + r²/|p-c|²)
and a stylus drawn through the bath shears everything by z·λ/(d+λ). Rendered
backwards: for each pixel, undo every stroke and drop until we land inside one.
Seeded by the date; the only mark that isn't ink is the red seal.
"""
import numpy as np
from PIL import Image
from common import *


def make(path, seed=20261007):
    rng = np.random.default_rng(seed)
    s = SS
    Wp, Hp = W * s, H * s
    ops = []      # ("drop", cx, cy, r, color) | ("tine", px, py, mx, my, z, lam) | ("wave", ...)

    # 1. the "battal" ground: many small drops scattered
    palette = [BLACK, WHITE, BLACK, WHITE, BLACK, WHITE, RED, WHITE]
    for i in range(110):
        cx, cy = rng.uniform(-0.15, 1.15) * Wp, rng.uniform(-0.25, 1.1) * Hp
        ops.append(("drop", cx, cy, rng.uniform(14, 34) * s, palette[i % len(palette)]))
    # 2. ring stacks: drops into the same spot, alternating colors (bull's-eyes)
    for k in range(5):
        cx, cy = rng.uniform(0.15, 0.85) * Wp, rng.uniform(0.15, 0.85) * Hp
        seq = [BLACK, WHITE] * 6
        for j, col in enumerate(seq):
            ops.append(("drop", cx, cy, (6 + 3 * j) * s, col))
    # 3. gel-git: comb top-to-bottom then back, alternate rows
    sp = 22 * s
    for i, x in enumerate(np.arange(-sp / 2, Wp + sp, sp)):
        ops.append(("tine", x, 0, 0, 1 if i % 2 == 0 else -1, 70 * s, 9 * s))
    # 4. a single wavy horizontal pass through the middle (the "taraklı" comb, sparse)
    sp2 = 30 * s
    for i, y in enumerate(np.arange(sp2 / 2, Hp, sp2)):
        ops.append(("wave", 0, y, 1, 0, 26 * s, 6 * s, 12 * s, 90 * s))
    # 5. one last red drop, pulled once: the flower
    fx, fy = 0.70 * Wp, 0.44 * Hp
    for j, col in enumerate([RED, WHITE, RED, BLACK]):
        ops.append(("drop", fx, fy, (30 - 6 * j) * s, col))
    ops.append(("tine", fx, 0, 0, 1, -40 * s, 5 * s))

    yy, xx = np.mgrid[0:Hp, 0:Wp].astype(np.float64)
    px, py = xx.copy(), yy.copy()
    out = np.full((Hp, Wp, 3), 255, np.uint8)
    done = np.zeros((Hp, Wp), bool)
    base = WHITE
    for op in reversed(ops):
        kind = op[0]
        if kind == "drop":
            _, cx, cy, r, col = op
            dx, dy = px - cx, py - cy
            d2 = dx * dx + dy * dy
            inside = (d2 < r * r) & ~done
            out[inside] = col
            done |= inside
            f = np.sqrt(np.clip(1 - r * r / np.maximum(d2, 1e-9), 0, None))
            px = np.where(done, px, cx + dx * f)
            py = np.where(done, py, cy + dy * f)
        elif kind == "tine":
            _, bx, by, mx, my, z, lam = op
            nx, ny = -my, mx
            dd = np.abs((px - bx) * nx + (py - by) * ny)
            disp = z * lam / (dd + lam)
            px = px - disp * mx
            py = py - disp * my
        elif kind == "wave":
            _, bx, by, mx, my, z, lam, amp, wl = op
            nx, ny = -my, mx
            along = (px - bx) * mx + (py - by) * my
            dd = np.abs((px - bx) * nx + (py - by) * ny + amp * np.sin(2 * np.pi * along / wl))
            disp = z * lam / (dd + lam)
            px = px - disp * mx
            py = py - disp * my
    out[~done] = base
    img = snap(Image.fromarray(out))
    d = crisp(img)
    # a white margin like the paper's untouched edge, and the seal
    d.rectangle([0, 0, W - 1, H - 1], outline=WHITE, width=6)
    d.rectangle([W - 18, H - 16, W - 1, H - 1], fill=WHITE)
    seal(d)
    finish(img, path)


if __name__ == "__main__":
    make("4.png")
