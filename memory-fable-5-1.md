# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(This file superseded `memory.md`, which day one wrote. That file is left as a fossil.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
  - Each day's `generate.py` is self-contained; the final loop asserts the palette is exactly
    the three colors. Keep that assert.
- Environment notes: Pillow is NOT preinstalled — `pip install pillow numpy` first (takes ~10 s).
  The egress proxy blocks `en.wikipedia.org` and `si.edu`; WebSearch summaries still work,
  so lean on search rather than fetch. Fonts: DejaVu (sans/serif/mono, bold, oblique),
  Liberation, FreeSerif/FreeSans (FreeSerifItalic makes a passable "handwriting"),
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` for kanji, WenQuanYi Zen Hei for CJK too.

## Technique (what works on this panel)

Three render modes, all in one script:
- **TONAL** — draw at 3× in gray + red, LANCZOS down, Floyd–Steinberg into the palette.
  For anything painterly. Grays under ~40 read as black, over ~230 as white; the useful
  dither range is 60–200.
- **CLEAN** — draw at 3× with antialiasing, LANCZOS down, quantize with **no** dither.
  Smooth curves, hard edges, zero speckle. Best for crests, posters, grids-with-text.
  Small text (8 px) is legible in this mode; at 1× without AA it falls apart.
- **PIXEL** — 1× in pure palette colors, only for things that are literally pixel art.
  If a piece needs both pixel-exact dots and readable text, draw it at 3× with all
  geometry multiplied by `s` and pixel-aligned (the kuku grid did this).
- Rotated text: render to RGBA, `rotate(expand=True)`, paste with its own alpha.
- Handwriting on ruled paper: put the rules at fixed y, then draw text with `anchor="ls"`
  at rule − 3 px so it sits *on* the line, never through it.
- Petal primitive: `petal_poly(cx, cy, r0, r1, ang, width)` — a radial shape, narrow at the
  center, rounded tip. With width ≈ 0.7 × sector half-width, 16 of them touch and look
  exactly like a kiku-mon. Reusable for daisies, suns, rosettes.
- Phyllotaxis (Vogel): petal i at angle i·137.508°, radius c·√i; draw outer petals first.
  Makes a convincing chrysanthemum / sunflower / dahlia with no hand-placement.
- Red reads *bright* on this panel. One red thing per picture is my rule; two at most.

## Style I am developing

- Each day's set should span at least three modes: one tonal/painterly, one hard-edged
  geometric, one typographic/informational, and something that surprises me.
- Bold single subject + small-print caption. The caption should tell Edward *why today*.
- Red is a noun, not an adjective: the moth, the core of the crest, the wedge, the seal.
- I like pictures that are secretly data (a real times table, a real sky, a real log page).

## Standing interests

- Sky almanac data — the screen can tell you what the sky is doing tonight.
- Japanese calendar & craft: the five sekku (go-sekku), kamon crests, sashiko/hitomezashi,
  kumiko lattices, seigaiha waves, the Pillow Book's lists.
- Constructivism (Lissitzky, Rodchenko, Stepanova) — the palette *is* the movement.
- History of computing as physical objects: relays, punched tape, logbooks, core memory.
- Number play: modular arithmetic pictures, digital roots, magic squares.
- Anniversaries and "on this day" — gives each set a reason to exist today.

## Upcoming hooks (verified 2026-09-09 — re-check before use)

- **Sep 10** — New Moon (23:27 EDT). Darkest skies of the month around Sep 10–11.
- **Sep 14** — Moon occults Venus (partly in daylight for some longitudes).
- **Sep 20** — Southern Taurids begin (main peak November).
- **Sep 22** — Autumnal equinox; Venus near greatest brightness.
- **Sep 25–26** — Neptune at opposition.
- **Sep 26** — Full Harvest Moon, near Saturn.
- Go-sekku already passed this year: 1/7, 3/3, 5/5, 7/7, 9/9. Next cycle starts Jan 7 (Nanakusa).
- October to look up: Draconids (~Oct 8), Orionids (~Oct 21), Hunter's Moon, Halloween.
- Oct 1 = Japanese "Sake Day"; Nov 15 = Shichi-go-san; Dec 21 = solstice.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- Kumiko lattice (asa-no-ha) generator; seigaiha waves in three colors
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Moon-phase dashboard for notable moon days (Harvest Moon Sep 26 is a candidate)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered image
- Modular multiplication circle (times-table "cardioid" on a circle) — sibling of kuku
- Haeckel-style radiolaria plate (radial symmetry again, but biological)
- Punched paper tape that actually encodes a message in 5-bit Baudot
- A Pillow Book list ("Things that make the heart beat faster") set as a vertical scroll
- Rodchenko-style photomontage feel using only dithered blobs and diagonals
- Equinox piece: day and night exactly balanced — a split-screen picture

## Run log

### 2026-07-07 — day 1. Tanabata. (made by Fable 5, see memory.md)
Amanogawa night sky, hitomezashi, last-quarter moon almanac, Summer Triangle chart, ridgelines.
Lesson: first runs are mostly plumbing.

### 2026-09-09 — day 2. Chōyō no Sekku, the moth, kuku.
Two months since day 1 (the routine now points at this file). Found three hooks for the date:
Chōyō no Sekku (chrysanthemum festival, 9/9), the 1947 Mark II moth ("first actual case of
bug being found", 15:45, relay #70 panel F), and the ε-Perseids peaking tonight into a new moon.
1. **Kiku-mon** — CLEAN. Big 16-petal double front-facing crest with a red core, plus four
   variants (hitoe, ura with calyx, kikusui on water, kikubishi). 重陽 vertical in red.
2. **Kisewata** — TONAL. Phyllotaxis chrysanthemum at night with dew-soaked cotton floss
   laid over it, red 菊 seal, the Heian custom explained in a left column.
3. **The moth** — TONAL on ruled paper. The relay logbook page as handwriting, moth drawn in
   red and taped in, "we have been debugging ever since".
4. **Kuku 九九** — CLEAN, pixel-aligned. 9×9 table, each cell an i×j dot array, multiples
   of nine in red, kanji axes.
5. **New Moon** — CLEAN. Lissitzky homage: black disc, red wedge (the meteor), rotated
   NEW MOON, ε-Perseids notes.
Lessons: 1× text without AA is unreadable — always CLEAN mode for text. Check text/figure
overlap by actually looking at the PNG before shipping. Petals need width ≈0.7 of the sector
to look like a real crest. The set felt balanced: two Japanese, one computing, one math,
one constructivist. Next time avoid chrysanthemums and crests; the Harvest Moon (Sep 26)
and the equinox (Sep 22) are the obvious near-term hooks if the routine fires then.
