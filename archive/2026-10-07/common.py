"""Shared helpers for 2026-10-07 (house style: almanac woodcut)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, SS = 400, 300, 3
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
INTER = "/usr/share/fonts/opentype/inter/"
FOLIO_DATE = "07·X·26"


def F(name, size):
    return ImageFont.truetype(INTER + name + ".otf", size)


_pal = Image.new("P", (1, 1))
_pal.putpalette(list(WHITE) + list(BLACK) + list(RED) + [0, 0, 0] * 253)


def dither(img):
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img.convert("RGB").quantize(palette=_pal, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")


def snap(img):
    """Downscale (if needed) and snap to the palette with NO dithering: crisp shapes."""
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img.convert("RGB").quantize(palette=_pal, dither=Image.Dither.NONE).convert("RGB")


def crisp(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return d


def finish(img, path):
    img.convert("RGB").quantize(palette=_pal, dither=Image.Dither.NONE).save(path, optimize=True)


def footer(d, n, title, ink=BLACK, bg=None):
    f = F("Inter-Medium", 9)
    if bg is not None:
        d.rectangle([0, H - 14, W, H], fill=bg)
    d.line([8, H - 15, W - 8, H - 15], fill=ink)
    d.text((8, H - 13), title.upper(), font=f, fill=ink)
    folio = f"{FOLIO_DATE}  {n}/5"
    w = d.textlength(folio, font=f)
    d.text((W - 8 - w - 8, H - 13), folio, font=f, fill=ink)
    seal(d)


def seal(d):
    d.rectangle([W - 13, H - 11, W - 9, H - 7], fill=RED)


def tw(d, s, f):
    return d.textlength(s, font=f)


def chaikin(pts, n=3, closed=True):
    for _ in range(n):
        out = []
        m = len(pts) if closed else len(pts) - 1
        for i in range(m):
            p, q = pts[i], pts[(i + 1) % len(pts)]
            out += [(0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]),
                    (0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1])]
        if not closed:
            out = [pts[0]] + out + [pts[-1]]
        pts = out
    return pts
