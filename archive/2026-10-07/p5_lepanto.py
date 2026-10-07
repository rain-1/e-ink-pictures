"""5. LEPANTO — 7 October 1571, mouth of the Gulf of Patras.

An engraved-style chart: coast lines repeated outward from the shore (distance
transform contours), land stippled. One mark per ship: Holy League 212 in black
(206 galleys + 6 galleasses), Ottoman 251 in red (galleys + galliots). Coastline is
approximate and the fleets are drawn larger than life, as the old engravers did.
"""
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt
from common import *

LON0, LON1, LAT0, LAT1 = 20.92, 21.62, 38.02, 38.42
MAP_H = 285


def P(lon, lat):
    return ((lon - LON0) / (LON1 - LON0) * W, (LAT1 - lat) / (LAT1 - LAT0) * MAP_H)


NORTH = [(20.90, 38.45), (21.02, 38.45), (21.06, 38.42), (21.09, 38.40), (21.11, 38.37),
         (21.13, 38.35), (21.12, 38.33), (21.15, 38.315), (21.20, 38.322), (21.27, 38.33),
         (21.33, 38.335), (21.38, 38.33), (21.42, 38.355), (21.46, 38.345), (21.52, 38.335),
         (21.58, 38.35), (21.64, 38.36), (21.64, 38.45)]
SOUTH = [(21.22, 38.00), (21.27, 38.06), (21.31, 38.11), (21.34, 38.15), (21.37, 38.18),
         (21.40, 38.17), (21.46, 38.155), (21.53, 38.15), (21.60, 38.165), (21.64, 38.175),
         (21.64, 38.00)]
ISLANDS = [(21.04, 38.385, 4, 3), (21.075, 38.36, 3, 2), (21.02, 38.36, 2, 2),
           (21.09, 38.335, 3, 2), (21.055, 38.33, 2, 1)]


def galley(d, x, y, facing, col, big=False):
    L = 6 if big else 4
    h = 1 if not big else 2
    if facing > 0:
        d.polygon([(x - L // 2, y - h), (x + L // 2 - 1, y - h), (x + L // 2 + 1, y), (x + L // 2 - 1, y + h),
                   (x - L // 2, y + h)], fill=col)
    else:
        d.polygon([(x + L // 2, y - h), (x - L // 2 + 1, y - h), (x - L // 2 - 1, y), (x - L // 2 + 1, y + h),
                   (x + L // 2, y + h)], fill=col)


def squadron(d, n, x0, y0, cols, facing, col, dx=5, dy=4, curve=0.0):
    rows = int(np.ceil(n / cols))
    k = 0
    for r in range(rows):
        for c in range(cols):
            if k >= n:
                return y0 + rows * dy
            # rows bow forward slightly at the middle, like a crescent
            t = (r / max(rows - 1, 1)) - 0.5
            bow = curve * (1 - 4 * t * t)
            x = x0 + facing * (bow - c * dx)
            galley(d, round(x), y0 + r * dy, facing, col)
            k += 1
    return y0 + rows * dy


def make(path):
    s = SS
    land = Image.new("L", (W * s, MAP_H * s), 0)
    dl = ImageDraw.Draw(land)
    for poly in (NORTH, SOUTH):
        dl.polygon([(P(*p)[0] * s, P(*p)[1] * s) for p in chaikin(poly, 2, closed=True)], fill=255)
    for lon, lat, rx, ry in ISLANDS:
        x, y = P(lon, lat)
        dl.ellipse([(x - rx) * s, (y - ry) * s, (x + rx) * s, (y + ry) * s], fill=255)
    landm = np.array(land.resize((W, MAP_H), Image.LANCZOS)) > 127

    rgb = np.full((H, W, 3), 255, np.uint8)
    # engraved water: contour lines at growing spacing away from every shore
    dist = distance_transform_edt(~landm)
    lines = np.zeros_like(landm)
    for lev in [2, 5, 9, 14, 20, 27]:
        lines |= (np.abs(dist - lev) < 0.5)
    rgb[:MAP_H][lines & ~landm] = BLACK
    # land: ordered stipple, denser near the coast
    dland = distance_transform_edt(landm)
    yy, xx = np.mgrid[0:MAP_H, 0:W]
    bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16
    th = bayer[yy % 4, xx % 4]
    tone = np.clip(0.30 - dland / 120, 0.07, 0.30)
    rgb[:MAP_H][landm & (th < tone)] = BLACK
    # coastline: crisp black edge
    edge = landm & (dland <= 1.0)
    rgb[:MAP_H][edge] = BLACK
    img = Image.fromarray(rgb)
    d = crisp(img)

    # ---- the fleets ------------------------------------------------------
    # Holy League (black), facing east. North wing Barbarigo, centre Don Juan, south Doria, reserve.
    hx = 74
    y = squadron(d, 53, hx, 90, 5, +1, BLACK, curve=2)
    y = squadron(d, 62, hx + 4, y + 7, 5, +1, BLACK, curve=3)
    squadron(d, 53, hx, y + 7, 5, +1, BLACK, curve=2)
    squadron(d, 38, hx - 38, 140, 3, +1, BLACK)
    for gy in (98, 124, 158, 186, 214, 236):      # six galleasses, out in front
        galley(d, hx + 18, gy, +1, BLACK, big=True)
    # Ottoman (red), facing west, a long crescent. Right wing (north) hugs the shore.
    ox = 138
    y = squadron(d, 56, ox, 88, 5, -1, RED, curve=-3)
    y = squadron(d, 87, ox - 2, y + 7, 6, -1, RED, curve=2)
    squadron(d, 63, ox, y + 7, 5, -1, RED, curve=-3)
    squadron(d, 45, ox + 40, 150, 3, -1, RED)

    # ---- labels ------------------------------------------------------------
    fi = F("Inter-Italic", 9)
    fm = F("Inter-Medium", 9)
    fr = F("Inter-Regular", 9)

    def label(text, lon, lat, font=fi, col=BLACK):
        x, y = P(lon, lat)
        w = tw(d, text, font)
        d.rectangle([x - 1, y - 1, x + w + 1, y + 10], fill=WHITE)
        d.text((x, y), text, font=font, fill=col)

    label("ECHINADES", 20.94, 38.405)
    label("Gulf of Patras", 21.42, 38.26)
    label("ACHAIA", 21.47, 38.10)
    label("Cape Araxos", 21.285, 38.172)
    for i, t in enumerate(["to Lepanto →", "40 km east"]):
        d.text((W - 8 - tw(d, t, fi), 86 + i * 10), t, font=fi, fill=BLACK)

    # title cartouche on the Aetolian shore (top right)
    bx0, by0, bx1, by1 = 200, 5, 394, 74
    d.rectangle([bx0, by0, bx1, by1], fill=WHITE, outline=BLACK)
    d.rectangle([bx0 + 2, by0 + 2, bx1 - 2, by1 - 2], outline=BLACK)
    d.text((bx0 + 8, by0 + 5), "LEPANTO", font=F("InterDisplay-Black", 22), fill=BLACK)
    d.text((bx0 + 116, by0 + 8), "7 · X · 1571", font=fm, fill=RED)
    d.text((bx0 + 116, by0 + 18), "five hours", font=fr, fill=BLACK)
    for i, t in enumerate(["One mark per ship: Holy League 212,",
                           "Ottoman 251 in red. On the Marquesa,",
                           "Cervantes, 24, lost the use of a hand."]):
        d.text((bx0 + 8, by0 + 33 + i * 11), t, font=fr, fill=BLACK)
    # scale bar bottom-left
    km10 = 10 / (111.32 * np.cos(np.radians(38.25))) / (LON1 - LON0) * W
    sx, sy = 12, MAP_H - 12
    d.rectangle([sx, sy, sx + km10, sy + 2], fill=BLACK)
    d.text((sx + km10 + 4, sy - 4), "10 km", font=fr, fill=BLACK)
    footer(d, 5, "The other side of the line")
    finish(img, path)


if __name__ == "__main__":
    make("5.png")
