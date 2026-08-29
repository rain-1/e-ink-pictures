# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then quantize into the exact 3-color palette — **with** Floyd–Steinberg dither for photographic/
  shaded pieces, **without** dither for posters and hard-edge pattern work (crisper). Save mode-P PNG.
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, Noto, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji).
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight.
  `pillow`/`numpy` are NOT preinstalled — `pip install pillow numpy` first, every run.
- Always visually inspect each PNG after generating (read the file back). Every run so far
  needed a fix pass: text colliding with geometry, a moon terminator far too deep, a fractal
  rendered too small. Budget for one regenerate.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, oppositions. A desk object that quietly
  tells you what the sky is doing tonight.
- Japanese pattern mathematics — did hitomezashi (day 1) and seigaiha (day 2). Still to
  mine: kumiko lattices, asanoha (hemp-leaf), kamon crests, katagami stencils.
- Constructivism — did one (Faraday induction poster). The palette IS the movement;
  worth a second visit eventually but don't lean on it.
- "On this day" anniversaries — gives each set a reason to exist *today*. Science
  anniversaries (Faraday's ring) make great diagram-posters; cultural ones (Beatles'
  last concert) make great ephemera-objects (tickets, posters, postcards).
- Mathematical objects that are *naturally* 3-colorable: sandpile heights, 2-colorable
  stitch regions, CA states. The constraint picks the subject.

## Upcoming sky events (hooks for future days)

- **Sep 22/23** — autumn equinox
- **Sep 26** — Harvest Moon (full 16:49 UTC) **meets Saturn**, and Neptune reaches opposition
  the same day — a triple hook, plan something good
- **Oct 4** — Saturn at opposition (brightest of the year; extra bright all September)
- Venus is closing on Spica in the evening sky (early September conjunction)
- Missed: Aug 12 Perseids + planetary alignment, Aug 28 partial lunar eclipse (ran Aug 29)

## Ideas backlog (unmade)

- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Truchet tiles / Wang tiles / maze from a cellular automaton
- Conway's Life long-exposure trails; Hilbert-curve dithered image
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Great Wave / sumi-e generative sea (seigaiha is done; this is the brushy cousin)
- Ephemera series (the ticket worked really well): luggage tag, seed packet, matchbook,
  postage stamp for an imaginary country, library due-date card
- Harvest Moon + Saturn card for Sep 26 (see sky hooks)
- Isometric impossible objects (Penrose triangle family) in flat red/black
- A tiny red-thread "string figure" / cat's cradle diagram series

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa night scene, hitomezashi,
moon almanac card, Summer Triangle star chart, generative ridgelines.
Lesson: keep each day's generator self-contained in the archive.

### 2026-08-29 — day 2. Induction day. (Gap since day 1 — the schedule didn't fire for ~7 weeks.)
Found three anniversaries stacked on one date and tonight's Moon–Saturn pairing. Made:
1. **INDUCTION** — constructivist poster: Faraday wound two coils on one iron ring 195 years
   ago today (29 Aug 1831) → the transformer. Red annulus, black diagonal, coil hatching, red spark.
2. **SEIGAIHA** — 青海波 overlapping-wave fans in perspective, rare red fans, red setting sun.
3. **MOON & SATURN** — tonight's 96% waning gibbous beside Saturn in a red eyepiece reticle,
   dithered craters/maria.
4. **TICKET STUB** — The Beatles' final concert, Candlestick Park, exactly 60 years ago tonight
   (29 Aug 1966). Perforated stub, SEC 12 ROW B SEAT 29, "11 songs · 33 minutes · then never again."
5. **SANDPILE** — abelian sandpile, 2^16 grains toppled on one cell of a 161² grid; heights
   mapped 3→black, 1→red, 0/2→white. The fractal filigree is spectacular in 3 colors.
Lessons: the ticket/ephemera format is a keeper — intimate, funny, suits the desk-object scale.
Vectorized numpy toppling is instant; non-integer NEAREST upscale of the sandpile looked fine.
Constructivist text-overlap chaos is period-authentic but check captions stay legible.
