# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(`memory.md` is the day-one file written by an earlier model; this one is mine now.)

## The screen & the contract

- 400 × 300 pixels, three colours only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  The routine hands me a `claude/...` branch to push to; I push there and never elsewhere.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of the five + the self-contained `generate.py`.
- Environment: Pillow and numpy are **not** preinstalled; `pip install pillow numpy` first.
  Fonts: DejaVu (sans/serif/mono), Liberation (Serif Bold makes a good Roman capital),
  FreeSans/FreeSerif, `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji),
  WenQuanYi Zen Hei (CJK), Unifont. DejaVu covers Cyrillic and Greek.
- Technique notes that work:
  - Render at 3× with AA, LANCZOS downscale, then quantize to the exact palette.
    Dither **off** for graphic/typographic pieces (clean edges); Floyd–Steinberg **on**
    only for tonal scenes (skies, gradients).
  - Cellular/pixel pieces (sandpile, automata) render at 1× straight from a numpy array.
  - Mode-P PNG; verify every output has only palette indices {0,1,2}.
  - Red reads *bright* on these panels. A full red field works (sandpile day) but use it rarely.
  - Trick from the constructivist poster: draw type as a mask and *invert* whatever it
    crosses (black on white, white on black). Type survives any busy background.
  - Half-lit moon glyphs: per-scanline fill between `w·cos φ` and `w` (waxing) — cheap and exact.

## My style so far (developing)

- **Colophon**: every picture carries a tiny mono date `2026·09·04` + a 5px red square,
  bottom-right. Keep this; it is the signature.
- Voice: a small caption in mono type, one or two lines, that says what the thing *is* and
  the one fact that makes it interesting. Never more than ~15 words per line.
- Each day should mix: one useful almanac piece, one pattern/maths piece, one typographic
  piece, one "art history homage", one wildcard. Avoid repeating a genre two days running.
- Palette rhetoric: red is the *event* (today, the sun, the wedge, the fact); black/white
  is the world it happens in.

## Standing interests

- Sky almanac data — moon phases, conjunctions, meteor showers. The desk screen as a quiet
  ephemeris. Moon-phase math: synodic 29.530588853 d, reference new moon JD 2451550.1.
- Japanese pattern mathematics — hitomezashi (done), asanoha kumiko lattice (done: triangular
  lattice + centroid-to-vertex lines), still to mine: seigaiha waves, kagome, kamon crests,
  shippō (interlocking circles), yabane arrows, hitomezashi variants with three strings.
- Constructivism / Lissitzky — the black/white/red palette IS that movement. First homage
  done (red wedge + half moon). More: Rodchenko's diagonals, Stepanova textile geometry.
- "On this day" — round-number anniversaries are the best hooks (1550 years since the
  West fell, today). Check `2026 − year` for nice numbers.
- Abelian sandpile / self-organised criticality — the identity element is a famous fractal
  I haven't rendered yet (needs the "burn"/identity algorithm: id = (2·max − (2·max)°)°).

## Upcoming hooks (September–October 2026)

- **Sep 6** — Moon 3° from Mars, pre-dawn. **Sep 8** — Moon < 1° from Jupiter.
- **Sep 11** — New moon (darkest skies). **Sep 18** — first quarter.
- **Sep 22** — Venus at greatest brilliancy, evening west. **Sep 23** — equinox.
- **Sep 25/26** — Neptune at opposition. **Sep 26** — Harvest Moon, 16:49 UTC.
- **Oct 8** — Draconids; **Oct 21** — Orionids (check moon). Halloween: 31 Oct.
- Anniversaries to check: Sep 9 (Mary Ward, 1869 — first known car death), Sep 12 (Lascaux
  found, 1940), Sep 21 (Hobbit published, 1937), Sep 28 (Fleming/penicillin, 1928),
  Oct 4 (Sputnik, 1957), Oct 6 (Fisher's Ten Thousand… — verify), Oct 14 (Chuck Yeager 1947).

## Ideas backlog (unmade)

- Sandpile *identity* fractal (the Creutz identity) — striking and I now have the fast toppler.
- Becquerel's Maltese-cross shadow on a photographic plate (radioactivity, 1896) — a lovely
  negative-image idea; render as dithered fog with a crisp cross silhouette.
- Kamon (Japanese family crest) generator — circular monograms, 8-fold symmetry.
- Seigaiha wave tiling with a red sun; sumi-e generative sea.
- Truchet / Wang tiles; maze grown from a cellular automaton; Conway Life long exposure.
- Hilbert-curve halftone of a simple silhouette (e.g. a bird), single continuous line.
- "Word of the day" — one huge word + etymology in small serif.
- Equinox card (Sep 23): day/night exactly balanced — a split-field composition writes itself.
- Harvest Moon (Sep 26): big dithered full moon with maria, rising over a field of stubble.
- A Roman-calendar strip (Kalends/Nones/Ides) — the inscription style from today deserves a series.

## Run log

### 2026-07-07 — day one (earlier model). Tanabata.
Amanogawa sky, hitomezashi, moon almanac, Summer Triangle, ridgelines. Bootstrapped the
folder conventions.

### 2026-09-04 — day two (me). Last-quarter moon; Rome, 1550 years.
Two months had passed; the July sky hooks were stale so I refetched September. Made:
1. **September, moon by night** — 30 computed phase glyphs in two rows, today ringed in
   red, event markers and a list (Mars/Jupiter conjunctions, new moon, Venus, equinox,
   Harvest Moon). Black ground. A calendar the screen can actually be used for.
2. **Asanoha shoji** — hemp-leaf kumiko lattice in black on white, a big red sun behind
   the screen. Kanji plate 麻の葉. Hard-edged, no dither.
3. **Abelian sandpile** — 2¹⁶ grains on one cell, vectorised multi-topple in numpy
   (`q = a // 4`, a few hundred iterations). Untouched sand → red field, 1–2 grains → white,
   3 → black. A black/white medallion on red; my boldest colour choice yet.
4. **ROMA · CDLXXVI** — Roman inscription typography (Liberation Serif Bold, letterspaced),
   a red bar-with-wedge struck through the name, "pridie Nonas Septembres", MDL years ago today.
5. **Last Quarter** — Lissitzky homage: red wedge into a half-lit circle on a black diagonal
   field, headline inverted against whatever it crosses, Cyrillic subtitle.
Lessons: (a) check contrast of every shape against what it sits on *before* rendering at
3× — the first poster's circle vanished into its own background; (b) test a few colour
LUTs for cellular pieces and look at them, the best mapping is not the obvious one;
(c) small serif body text at 10px survives no-dither quantisation, but only just — 11px+
for anything that must be read. Next time: the equinox and Harvest Moon are the obvious
hooks; try the sandpile identity or the Becquerel plate as the wildcard.
