"""fable-5-1 / 2026-10-02 — "Signals across distance".
Style: engraved hairline plates. No dithering: everything is drawn at 4x,
box-downsampled and snapped to the 3-ink palette, so edges stay crisp.
Run: python generate.py <outdir>
"""
import sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 4
W, H = 400 * S, 300 * S
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, px): return ImageFont.truetype(FD + name, px * S)
MONO = lambda px: font("DejaVuSansMono.ttf", px)
MONOB = lambda px: font("DejaVuSansMono-Bold.ttf", px)
SERIF = lambda px: font("DejaVuSerif.ttf", px)
SERIFB = lambda px: font("DejaVuSerif-Bold.ttf", px)
SERIFI = lambda px: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", int(px * S * 1.15))

def snap(img):
    """Box-downsample 4x, then snap each pixel to black/white/red (no dither)."""
    a = np.asarray(img.resize((400, 300), Image.BOX)).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    redness = r - np.maximum(g, b)
    lum = (r + g + b) / 3
    idx = np.where(redness > 90, 2, np.where(lum > 120, 1, 0)).astype(np.uint8)
    out = Image.fromarray(idx, "P")
    out.putpalette(list(BLACK + WHITE + RED) + [0] * (256 - 3) * 3)
    _draw_texts(out)
    return out

def arr_to_img(m):
    """m: HxW int array 0=black 1=white 2=red."""
    pal = np.array([BLACK, WHITE, RED], dtype=np.uint8)
    return Image.fromarray(pal[m], "RGB")

TEXTS = []
def text(d, xy, s, f, fill, anchor="la", spacing=0):
    """Queue text; it is drawn at native 1x with no antialiasing after snapping."""
    TEXTS.append(((xy[0] / S, xy[1] / S), s, f.path, f.size // S, fill, anchor, spacing))

def _draw_texts(out):
    d = ImageDraw.Draw(out)
    d.fontmode = "1"
    idx = {BLACK: 0, WHITE: 1, RED: 2}
    for (x, y), s, path, px, fill, anchor, spacing in TEXTS:
        f = ImageFont.truetype(path, px)
        if spacing:
            ws = [d.textlength(c, font=f) for c in s]
            total = sum(ws) + spacing * (len(s) - 1)
            if anchor[0] == "m": x -= total / 2
            elif anchor[0] == "r": x -= total
            for c, w in zip(s, ws):
                d.text((round(x), round(y)), c, font=f, fill=idx[fill], anchor="l" + anchor[1])
                x += w + spacing
        else:
            d.text((round(x), round(y)), s, font=f, fill=idx[fill], anchor=anchor)
    TEXTS.clear()

def _unused_text(d, xy, s, f, fill, anchor="la", spacing=0):
    x, y = xy
    if spacing:
        # letter-spaced caps
        widths = [d.textlength(c, font=f) for c in s]
        total = sum(widths) + spacing * S * (len(s) - 1)
        if anchor[0] == "m": x -= total / 2
        elif anchor[0] == "r": x -= total
        for c, w in zip(s, widths):
            d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1])
            x += w + spacing * S
    else:
        d.text((x, y), s, font=f, fill=fill, anchor=anchor)

# ---------------------------------------------------------------- 1. Saturn
def saturn():
    tilt = math.radians(7.5)
    pa = math.radians(-14)                       # position angle on the page
    R = 58 * S
    cx, cy = 200 * S, 146 * S
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    X0, Y0 = xx - cx, -(yy - cy)                 # Y up
    X = X0 * math.cos(pa) + Y0 * math.sin(pa)
    Y = -X0 * math.sin(pa) + Y0 * math.cos(pa)
    m = np.zeros((H, W), int)                    # black sky

    # starfield: a few precise points
    rng = random.Random(20261002)
    for _ in range(70):
        sx, sy = rng.randrange(W), rng.randrange(H)
        m[sy:sy + S, sx:sx + S] = 1

    # rings in ring-plane coordinates
    rr = np.sqrt(X ** 2 + (Y / math.sin(tilt)) ** 2) / R
    dens = np.zeros_like(rr)
    dens[(rr > 1.24) & (rr < 1.53)] = 0.22       # C ring (crepe)
    dens[(rr >= 1.53) & (rr < 1.95)] = 0.75      # B ring, brightest
    dens[(rr >= 2.03) & (rr < 2.27)] = 0.5       # A ring
    dens[(rr >= 2.21) & (rr < 2.23)] = 0.0       # Encke gap
    # engraving: concentric line screen whose stroke weight = brightness
    phase = (rr * 34) % 1.0
    ring_on = phase < dens

    flat = 0.9
    disc = (X ** 2 + (Y / flat) ** 2) < R ** 2
    near = Y > 0                                  # near half of the rings is above centre
    # planet: latitude-line engraving, limb darkened
    rho = np.sqrt(X ** 2 + (Y / flat) ** 2) / R
    lum = np.sqrt(np.clip(1 - rho ** 2, 0, 1)) ** 0.6
    lat = Y / (R * flat)
    bands = 0.82 + 0.18 * np.sin(lat * 9.0)       # belt and zone variation
    pphase = (lat * 20) % 1.0
    planet_on = pphase < np.clip(lum * bands, 0.06, 0.94)
    m[disc & planet_on] = 1
    m[disc & ~planet_on] = 0
    show_ring = (dens > 0) & (~disc | near)
    m[show_ring & ring_on] = 1
    m[show_ring & ~ring_on] = 0

    img = arr_to_img(m)
    d = ImageDraw.Draw(img)
    # red: the tilt, measured. a hairline on the ring plane and on the line of sight
    ax = 2.55 * R
    def P(x, y):
        return (cx + x * math.cos(pa) - y * math.sin(pa), cy - (x * math.sin(pa) + y * math.cos(pa)))
    d.line([P(-ax, 0), P(-2.32 * R, 0)], fill=RED, width=S)
    d.line([P(2.32 * R, 0), P(ax, 0)], fill=RED, width=S)
    text(d, (14 * S, 16 * S), "SATURN", MONOB(13), WHITE, spacing=5)
    text(d, (14 * S, 33 * S), "at opposition · 04 Oct 2026", SERIF(10), WHITE)
    text(d, (386 * S, 270 * S), "rings open 7.5° south", MONO(10), RED, anchor="rs")
    text(d, (386 * S, 286 * S), "1.26 billion km · 70 light-min", MONO(9), WHITE, anchor="rs")
    text(d, (14 * S, 286 * S), "opening again.", MONO(9), WHITE, anchor="ls")
    text(d, (14 * S, 270 * S), "edge-on in March 2025,", MONO(9), WHITE, anchor="ls")
    return snap(img)

# ---------------------------------------------------------- 2. One light-day
def lightday():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    cx, cy, r = 276 * S, 152 * S, 104 * S
    lt_h = 23 + 52 / 60                           # light-time today, hours
    # red sector: how far the signal has to go
    start = -90
    end = start + 360 * lt_h / 24
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    rad = np.hypot(xx - cx, yy - cy)
    ang = (np.degrees(np.arctan2(yy - cy, xx - cx)) - start) % 360
    wave = (rad % (6 * S)) >= S                       # concentric radio-wave hairlines, pixel-aligned
    disc = (rad < r * 0.8) & (ang < end - start) & wave
    base = np.asarray(img).copy()
    base[disc] = RED
    img.paste(Image.fromarray(base))
    # dial: 96 quarter-hour ticks, hours long
    for i in range(96):
        a = math.radians(-90 + i * 360 / 96)
        L = 16 * S if i % 4 == 0 else 6 * S
        if i % 24 == 0: L = 24 * S
        w = 2 * S if i % 4 == 0 else S
        r1 = r
        d.line([(cx + (r1 - L) * math.cos(a), cy + (r1 - L) * math.sin(a)),
                (cx + r1 * math.cos(a), cy + r1 * math.sin(a))], fill=BLACK, width=w)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK, width=S)
    for h, lab in [(6, "6"), (12, "12"), (18, "18")]:
        a = math.radians(-90 + h * 15)
        rl = r + 9 * S
        text(d, (cx + rl * math.cos(a), cy + rl * math.sin(a)), lab, MONO(9), BLACK, anchor="mm")
    # the missing 8 minutes: callout
    a = math.radians(end + 1)
    p0 = (cx + r * 0.84 * math.cos(a), cy + r * 0.84 * math.sin(a))
    p1 = (cx + 70 * S, 22 * S)
    d.line([p0, (p0[0], p1[1]), p1], fill=BLACK, width=S)
    text(d, (p1[0] + 4 * S, p1[1]), "8 min", MONO(9), BLACK, anchor="lm")
    # left column: words
    x = 16 * S
    text(d, (x, 40 * S), "ONE", SERIFB(30), BLACK)
    text(d, (x, 74 * S), "LIGHT-", SERIFB(30), BLACK)
    text(d, (x, 108 * S), "DAY", SERIFB(30), RED)
    lines = ["Voyager 1, launched 1977,",
             "is ~23 h 52 m away by",
             "radio today. Say hello",
             "now; it hears you",
             "tomorrow.",
             "",
             "18 Nov 2026: the gap",
             "becomes a whole day."]
    for i, s in enumerate(lines):
        text(d, (x, (160 + i * 14) * S), s, MONO(9), RED if i >= 6 else BLACK)
    # tiny probe glyph at the dial's 23:52 position
    a = math.radians(end)
    px, py = cx + (r + 0) * math.cos(a), cy + r * math.sin(a)
    return snap(img)

# ------------------------------------------------------------- 3. Charkha
def charkha():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    cx, cy, r = 130 * S, 150 * S, 98 * S
    # the wheel as a string-art figure: chords skipping k spokes, like the
    # criss-cross yarn that ties a real charkha's two rims
    n = 24
    pts = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    for i in range(n):
        j = (i + 7) % n
        d.line([pts[i], pts[j]], fill=BLACK, width=S)
    for i in range(n):
        d.line([(cx, cy), pts[i]], fill=BLACK, width=S)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK, width=3 * S)
    d.ellipse([cx - 9 * S, cy - 9 * S, cx + 9 * S, cy + 9 * S], fill=BLACK)
    # the one thread: leaves the rim, crosses to the spindle, then a spiral
    sx, sy = 330 * S, 92 * S                      # spindle tip
    top = (cx, cy - r)
    d.line([top, (sx, sy)], fill=RED, width=S)
    bot = (cx, cy + r)
    d.line([bot, (sx, sy + 4 * S)], fill=RED, width=S)
    # cop of yarn on the spindle: a dense helix of red
    for k in range(70):
        t = k / 69
        w = 34 * S * math.sin(math.pi * (0.15 + 0.85 * t)) ** 0.7
        x0 = sx + (-6 + 52 * t) * S
        d.line([(x0, sy + 2 * S - w / 2), (x0 + 3 * S, sy + 2 * S + w / 2)], fill=RED, width=S)
    d.line([(sx - 14 * S, sy + 2 * S), (sx + 60 * S, sy + 2 * S)], fill=BLACK, width=2 * S)
    # thread runs out to the right as the yarn being drawn
    text(d, (252 * S, 170 * S), "2 OCTOBER", MONOB(11), BLACK, spacing=3)
    text(d, (252 * S, 190 * S), "Gandhi Jayanti", SERIFI(14), BLACK)
    quote = ["“attending to a work", "that appears boring", "without any sense", "of boredom”"]
    for i, s in enumerate(quote):
        text(d, (252 * S, (214 + i * 14) * S), s, SERIF(10), BLACK)
    text(d, (252 * S, 278 * S), "one motion, repeated.", MONO(9), RED)
    return snap(img)

# ---------------------------------------------------- 4. Night migration
def echo(d, x, y, dx, dy, s, fill, w):
    """A radar echo: bright head, fading trail behind it (heading dx, dy)."""
    d.line([(x - dx * s * 1.6, y - dy * s * 1.6), (x, y)], fill=fill, width=w)
    h = w * 1.3
    d.ellipse([x - h, y - h, x + h, y + h], fill=fill)

def migration():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    rng = random.Random(1013)
    cx, cy = 200 * S, 330 * S                    # radar below the frame: we see the top of its sweep
    # range rings
    for k in range(1, 8):
        rk = k * 48 * S
        d.arc([cx - rk, cy - rk, cx + rk, cy + rk], 180, 360, fill=WHITE, width=S)
    # 'birds': small chevrons all heading SSW (down-left), density highest
    # in a band 2-4 h after sunset -> we map that to a mid-range annulus
    count = 0
    while count < 260:
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        dist = math.hypot(x - cx, y - cy) / S
        density = math.exp(-((dist - 200) / 70) ** 2)
        if rng.random() > density: continue
        count += 1
        s = rng.uniform(3.5, 5.5) * S
        ang = math.radians(rng.gauss(205, 9))       # heading on page, pointing down-left
        dx, dy = math.cos(ang), -math.sin(ang)
        echo(d, x, y, dx, dy, s, WHITE, S)
    # the one going the other way
    x, y = 268 * S, 112 * S
    s = 9 * S
    ang = math.radians(25)
    dx, dy = math.cos(ang), -math.sin(ang)
    echo(d, x, y, dx, dy, s, RED, S)
    d.ellipse([x - 14 * S, y - 14 * S, x + 14 * S, y + 14 * S], outline=RED, width=S)
    # sweep line
    a = math.radians(-62)
    d.line([(cx, cy), (cx + 400 * S * math.cos(a), cy + 400 * S * math.sin(a))], fill=RED, width=S)
    # caption plate
    d.rectangle([0, 0, 168 * S, 50 * S], fill=BLACK)
    text(d, (12 * S, 14 * S), "NOCTURNAL", MONOB(11), WHITE, spacing=3)
    text(d, (12 * S, 30 * S), "MIGRATION", MONOB(11), WHITE, spacing=3)
    d.rectangle([232 * S, 248 * S, 400 * S, 300 * S], fill=BLACK)
    text(d, (390 * S, 264 * S), "peak: 2–4 h after dusk,", MONO(9), WHITE, anchor="rm")
    text(d, (390 * S, 278 * S), "mid-October. all south —", MONO(9), WHITE, anchor="rm")
    text(d, (390 * S, 292 * S), "but one.", MONO(9), RED, anchor="rm")
    return snap(img)

# ---------------------------------------------------- 5. Interference
def interference():
    # two point sources (two antennas, two stones in a pond) — their summed
    # wave crests drawn as black/white; red marks the nodal lines of silence
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    s1 = (170 * S, 150 * S); s2 = (230 * S, 150 * S)
    lam = 15 * S
    d1 = np.hypot(xx - s1[0], yy - s1[1]); d2 = np.hypot(xx - s2[0], yy - s2[1])
    w1 = np.cos(2 * np.pi * d1 / lam); w2 = np.cos(2 * np.pi * d2 / lam)
    amp = np.abs(np.cos(np.pi * (d1 - d2) / lam))      # local envelope
    m = np.where(w1 + w2 > 0, 1, 0)
    node = amp < 0.09
    m[node] = 2
    # frame: everything outside an inner rectangle is quiet black
    frame = (xx < 14 * S) | (xx > 386 * S) | (yy < 14 * S) | (yy > 268 * S)
    m[frame] = 0
    img = arr_to_img(m.astype(int))
    d = ImageDraw.Draw(img)
    for s in (s1, s2):
        d.ellipse([s[0] - 5 * S, s[1] - 5 * S, s[0] + 5 * S, s[1] + 5 * S], fill=BLACK, outline=RED, width=S)
    text(d, (14 * S, 285 * S), "TWO SOURCES, ONE SILENCE", MONOB(9), WHITE, anchor="lm", spacing=2)
    text(d, (386 * S, 285 * S), "red = where the waves cancel", MONO(8), RED, anchor="rm")
    return snap(img)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    for i, fn in enumerate([saturn, lightday, charkha, migration, interference], 1):
        fn().save(f"{out}/{i}.png")
        print("wrote", i, fn.__name__)
