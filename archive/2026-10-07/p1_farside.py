"""1. FAR SIDE — Luna 3 photographed the hidden face of the Moon, 7 Oct 1959.

The probe developed its film on board and scanned it line by line for the radio
link, so the Moon here is drawn as a raster: every scan line's thickness is the
brightness. The first new sea, Mare Moscoviense, is scanned in red.
"""
import numpy as np
from PIL import Image
from common import *


def moon_brightness(n, R, cx, cy, rng):
    yy, xx = np.mgrid[0:n[1], 0:n[0]].astype(np.float32)
    X, Y = (xx - cx) / R, (yy - cy) / R
    r2 = X ** 2 + Y ** 2
    disc = r2 < 1
    Z = np.sqrt(np.clip(1 - r2, 0, 1))
    # sun from the observer's side, a little to the left: nearly full phase (as on 7 Oct 1959)
    L = np.array([-0.35, -0.15, 0.92]); L /= np.linalg.norm(L)
    b = np.full(X.shape, 0.52, np.float32)

    def blob(x0, y0, rx, ry, depth, soft=0.35):
        d = ((X - x0) / rx) ** 2 + ((Y - y0) / ry) ** 2
        return depth * np.clip((1 - d) / soft, 0, 1)

    maria = np.zeros_like(b)
    # near-side maria visible on the left limb (Luna 3 saw ~1/3 near side)
    maria += blob(-0.80, -0.22, 0.17, 0.26, 0.55)   # Crisium (foreshortened)
    maria += blob(-0.93, 0.10, 0.07, 0.22, 0.45)    # Marginis
    maria += blob(-0.90, 0.40, 0.08, 0.18, 0.45)    # Smythii
    maria += blob(-0.70, 0.62, 0.18, 0.12, 0.30)    # Fecunditatis edge
    tsiol = blob(0.05, 0.42, 0.10, 0.09, 0.62, 0.2)  # Tsiolkovskiy's dark floor
    mosc = blob(0.12, -0.42, 0.13, 0.11, 0.62, 0.25)  # Mare Moscoviense
    maria += tsiol
    b = b - np.clip(maria, 0, 0.62)

    # craters: bright rims, slightly darker floors, a few with ray systems
    for i in range(420):
        u, v = rng.uniform(-1, 1, 2)
        if u * u + v * v > 0.97:
            continue
        rc = 0.012 + 0.09 * rng.random() ** 4
        d = np.hypot(X - u, Y - v) / rc
        rim = np.exp(-((d - 1) / 0.18) ** 2)
        floor = (d < 0.9)
        lit = np.clip(((X - u) * L[0] + (Y - v) * L[1]) / rc * -1, -1, 1)
        b += 0.45 * rim * (0.4 + 0.6 * lit) - 0.22 * floor * (1 - 0.5 * lit)
    # Giordano Bruno-ish ray crater
    ang = np.arctan2(Y + 0.25, X - 0.55)
    dd = np.hypot(X - 0.55, Y + 0.25)
    rays = (np.cos(ang * 9) ** 40) * np.exp(-dd / 0.35)
    b += 0.25 * rays
    # limb: shading by sun direction, mild
    shade = np.clip(X * L[0] + Y * L[1] + Z * L[2], 0, 1) ** 0.6
    # mottled highland texture (the far side is all highlands)
    for sc, amp in [(0.25, 0.16), (0.08, 0.10)]:
        k = max(2, int(2 / sc))
        g = rng.random((k, k)).astype(np.float32)
        gi = np.array(Image.fromarray((g * 255).astype(np.uint8)).resize(X.shape[::-1], Image.BICUBIC), np.float32) / 255
        b += (gi - 0.5) * amp * 2
    b = np.clip(b * (0.30 + 0.70 * shade), 0, 1)
    b[~disc] = 0
    return b, disc, mosc > 0.15


def make(path):
    s = SS
    n = (W * s, H * s)
    rng = np.random.default_rng(19591007)
    cx, cy, R = 150 * s, 140 * s, 118 * s
    b, disc, mosc = moon_brightness(n, R, cx, cy, rng)

    # downsample the tone to screen pixels, then draw the raster at 1x
    bs = np.array(Image.fromarray((b * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS), np.float32) / 255
    ds = np.array(Image.fromarray(disc.astype(np.uint8) * 255).resize((W, H), Image.LANCZOS)) > 127
    ms = np.array(Image.fromarray(mosc.astype(np.uint8) * 255).resize((W, H), Image.LANCZOS)) > 127
    P = 4                                   # scan pitch: one line per 4 screen rows
    rgb = np.zeros((H, W, 3), np.uint8)
    for k in range(H // P):
        y0 = k * P
        row = bs[min(y0 + 1, H - 1)]
        inside = ds[min(y0 + 1, H - 1)]
        err = 0.0
        for x in range(W):
            if not inside[x]:
                err = 0.0
                continue
            t = 0.5 + row[x] * 3.6 + err      # never fully zero inside: the frame is always scanned
            w = int(np.clip(round(t), 0, 4))
            err = t - w
            if w:
                top = y0 + (P - w) // 2
                col = RED if ms[min(y0 + 1, H - 1), x] else WHITE
                rgb[top:top + w, x] = col
    img = Image.fromarray(rgb)
    d = crisp(img)
    # a faint ruler of the 29 frames, along the top: 3:30 -> 4:10 UT
    x0, x1 = 292, 388
    ft = F("Inter-Medium", 9)
    fs = F("Inter-Regular", 9)
    d.text((x0, 14), "LUNA 3", font=F("InterDisplay-Black", 24), fill=WHITE)
    d.text((x0, 42), "7 OCT 1959", font=ft, fill=WHITE)
    d.text((x0, 53), "03:30–04:10 UT", font=ft, fill=WHITE)
    # label Mare Moscoviense; the leader runs outward, off the disc to the right
    mx, my = int(150 + 0.12 * 118), int(140 - 0.42 * 118)
    d.line([mx + 18, my, 286, my], fill=RED)
    d.text((x0, my - 11), "MARE", font=ft, fill=RED)
    d.text((x0, my), "MOSCOVIENSE", font=ft, fill=RED)
    for i, t in enumerate(["the first new sea", "in 350 years", "of telescopes"]):
        d.text((x0, my + 13 + i * 11), t, font=fs, fill=WHITE)
    y = 160
    for i in range(29):
        xa = x0 + (i % 10) * 10
        ya = y + (i // 10) * 10
        if i < 17:
            d.rectangle([xa, ya, xa + 6, ya + 6], fill=WHITE)
        else:
            d.rectangle([xa, ya, xa + 6, ya + 6], outline=WHITE)
    lines = ["29 frames in 40 min,", "developed on board,", "scanned like a fax.",
             "About 17 made the", "long radio fall home."]
    for i, t in enumerate(lines):
        d.text((x0, 194 + i * 11), t, font=fs, fill=WHITE)
    footer(d, 1, "The far side, first look", ink=WHITE)
    finish(img, path)


if __name__ == "__main__":
    make("1.png")
