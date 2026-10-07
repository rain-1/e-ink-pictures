"""2. NEVERMORE — Edgar Allan Poe died 7 Oct 1849.

The whole of The Raven, set in a 3x5 pixel face I drew for it, fills the page.
Where the raven and the bust of Pallas stand, the text reverses to white on black.
All eleven "nevermore"s are in red, and so is the eye.
"""
import re
import numpy as np
from PIL import Image, ImageDraw
from common import *

# 3x5 caps (1 = ink). Narrow glyphs are given as their real width.
GLYPHS = {
    "A": ["010", "101", "111", "101", "101"], "B": ["110", "101", "110", "101", "110"],
    "C": ["011", "100", "100", "100", "011"], "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"], "F": ["111", "100", "110", "100", "100"],
    "G": ["011", "100", "101", "101", "011"], "H": ["101", "101", "111", "101", "101"],
    "I": ["1", "1", "1", "1", "1"], "J": ["001", "001", "001", "101", "010"],
    "K": ["101", "101", "110", "101", "101"], "L": ["100", "100", "100", "100", "111"],
    "M": ["10001", "11011", "10101", "10001", "10001"], "N": ["1001", "1101", "1011", "1001", "1001"],
    "O": ["010", "101", "101", "101", "010"], "P": ["110", "101", "110", "100", "100"],
    "Q": ["010", "101", "101", "110", "011"], "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"], "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"], "V": ["101", "101", "101", "101", "010"],
    "W": ["10001", "10001", "10101", "11011", "10001"], "X": ["101", "101", "010", "101", "101"],
    "Y": ["101", "101", "010", "010", "010"], "Z": ["111", "001", "010", "100", "111"],
    ".": ["0", "0", "0", "0", "1"], ",": ["0", "0", "0", "1", "1"],
    ";": ["0", "1", "0", "1", "1"], ":": ["0", "1", "0", "1", "0"],
    "!": ["1", "1", "1", "0", "1"], "?": ["11", "01", "10", "00", "10"],
    "'": ["1", "1", "0", "0", "0"], '"': ["101", "101", "000", "000", "000"],
    "-": ["00", "00", "11", "00", "00"], "—": ["0000", "0000", "1111", "0000", "0000"],
    " ": ["00", "00", "00", "00", "00"], "/": ["001", "001", "010", "100", "100"],
}
GLYPHS["—"] = GLYPHS["—"]


def glyph(ch):
    return GLYPHS.get(ch.upper(), GLYPHS[" "])


def raven_mask():
    """Raven perched on a bust of Pallas, facing left. Returns 1x boolean mask + eye."""
    s = SS
    m = Image.new("L", (W * s, H * s), 0)
    d = ImageDraw.Draw(m)
    body = [(96, 84), (122, 72), (140, 64), (150, 54), (164, 46), (182, 43), (198, 47),
            (210, 57), (222, 68), (244, 80), (268, 96), (290, 114), (318, 136), (352, 160),
            (368, 174), (344, 176), (318, 166), (296, 160), (272, 170), (246, 176),
            (220, 172), (196, 160), (176, 140), (164, 120), (156, 102), (146, 94),
            (124, 90)]
    body = [(x - 20, y + 4) for x, y in body]
    d.polygon([(x * s, y * s) for x, y in chaikin(body, 3)], fill=255)
    # shaggy throat feathers
    for i, (x, y) in enumerate([(142, 100), (148, 112), (152, 124), (158, 134)]):
        d.polygon([((x - 6) * s, (y - 8) * s), ((x - 14 - i) * s, (y + 2) * s),
                   ((x + 2) * s, (y - 2) * s)], fill=255)
    # legs
    for x in (214, 232):
        d.rectangle([(x - 2) * s, 170 * s, (x + 2) * s, 192 * s], fill=255)
        d.polygon([((x - 10) * s, 192 * s), ((x + 8) * s, 192 * s), ((x + 2) * s, 186 * s)], fill=255)
    # bust of Pallas: plain classical bust on a round socle
    hx, hy = 222, 212
    d.ellipse([(hx - 20) * s, (hy - 22) * s, (hx + 20) * s, (hy + 24) * s], fill=255)       # head
    d.polygon([((hx + 16) * s, (hy - 6) * s), ((hx + 27) * s, (hy + 7) * s),
               ((hx + 17) * s, (hy + 9) * s)], fill=255)                                 # nose: she looks right
    d.polygon([((hx - 22) * s, (hy - 4) * s), ((hx - 8) * s, (hy - 30) * s),
               ((hx + 14) * s, (hy - 26) * s), ((hx - 4) * s, (hy - 18) * s)], fill=255)   # helmet crest
    d.rectangle([(hx - 10) * s, (hy + 14) * s, (hx + 10) * s, (hy + 36) * s], fill=255)     # neck
    d.chord([(hx - 46) * s, (hy + 28) * s, (hx + 46) * s, (hy + 84) * s], 180, 360, fill=255)  # shoulders
    d.polygon([((hx - 14) * s, (hy + 56) * s), ((hx + 14) * s, (hy + 56) * s),
               ((hx + 8) * s, (hy + 62) * s), ((hx - 8) * s, (hy + 62) * s)], fill=255)  # waist
    d.rectangle([(hx - 24) * s, (hy + 62) * s, (hx + 24) * s, (hy + 66) * s], fill=255)
    d.rectangle([(hx - 30) * s, (hy + 66) * s, (hx + 30) * s, (hy + 72) * s], fill=255)
    k = 0.83                                       # shrink about the socle's foot
    ax, ay = 222, 284
    small = m.resize((int(W * k), int(H * k)), Image.LANCZOS)
    m = Image.new("L", (W, H), 0)
    m.paste(small, (int(ax - ax * k), int(ay - ay * k)))
    eye = (round(ax + (150 - ax) * k), round(ay + (62 - ay) * k))
    return np.array(m) > 127, eye


def make(path):
    text = open("raven.txt", encoding="utf-8").read().strip()
    start = text.index("Then this ebony bird")     # from the moment the bird speaks
    text = text[start:].replace("\n", "/ ")
    text = re.sub(r"\s+", " ", text)
    # positions of every "nevermore" (case-insensitive)
    red = np.zeros(len(text), bool)
    for mt in re.finditer(r"nevermore", text, re.I):
        red[mt.start():mt.end()] = True
    nn = len(re.findall(r"nevermore", text, re.I))

    mask, eye = raven_mask()
    # text flows around the bird: block any column the silhouette touches (plus a gutter)
    from scipy.ndimage import binary_dilation
    block = binary_dilation(mask, iterations=3)
    ink = np.zeros((H, W), np.uint8)          # 0 none, 1 black ink, 2 red
    top, bottom, left, right, pitch = 2, H - 18, 3, W - 3, 6
    x, y, i = left, top, 0

    def free(x0, x1, y0):
        if x1 > right:
            return False
        return not block[max(0, y0 - 1):y0 + 6, x0:x1].any()

    while i < len(text) and y + 5 <= bottom:
        j = i
        while j < len(text) and text[j] != " ":
            j += 1
        word = text[i:j]
        wpx = sum(len(glyph(c)[0]) + 1 for c in word) - 1
        while not free(x, x + wpx, y):
            x += 1
            if x + wpx > right:
                x, y = left, y + pitch
                if y + 5 > bottom:
                    break
        if y + 5 > bottom:
            break
        for k, c in enumerate(word):
            g = glyph(c)
            for r in range(5):
                for q, bit in enumerate(g[r]):
                    if bit == "1":
                        ink[y + r, x + q] = 2 if red[i + k] else 1
            x += len(g[0]) + 1
        x += 2 if not word.endswith("/") else 3
        i = j + 1
    consumed = i
    lines_used = (y - top) // pitch

    rgb = np.full((H, W, 3), 255, np.uint8)
    rgb[ink == 1] = BLACK
    rgb[ink == 2] = RED
    rgb[mask] = BLACK
    img = Image.fromarray(rgb)
    d = crisp(img)
    ex, ey = eye
    d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=WHITE)
    d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=RED)
    footer(d, 2, f"Poe, d. 7 Oct 1849 · The Raven, st. 8–18 · {nn} nevermores")
    finish(img, path)
    return consumed, len(text), lines_used


if __name__ == "__main__":
    print(make("2.png"))
