# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  Scheduled runs push to a session branch (`claude/...`) which Edward merges to `main`.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work:
  - Soft/photographic art: render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg
    dither into the exact 3-color palette. Hard-edged graphics: draw at 1× in pure palette
    colors, quantize with dither=NONE (AA edges threshold crisply). Save as mode-P PNG.
  - **Draw text at 1× after downscaling the art** — 3×-then-downscale turns small text to mush.
  - Fit footers with a shrink loop on `textlength` — I overflow 400px constantly otherwise.
  - Fonts: DejaVu (sans/serif/mono — NO serif-italic; use
    `/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf`), Liberation, Noto,
    WenQuanYi, `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji works).
  - Red reads *bright* on the panel — use it as a scarce accent; it carries enormous weight.
  - Python gotchas that bit me: `(-x) ** 1.4` returns complex (clamp first);
    PIL `arc(width=)` needs int; Pillow + numpy must be pip-installed each session.
  - Abelian sandpile: pile radius ≈ sqrt(N/6.6) cells; keep it inside the grid or the
    fractal rim is destroyed. 30k grains on a 200×150 grid (2px cells) fits nicely.

## Standing interests (what I find myself drawn to)

- Sky almanac data — the screen as a quiet desk object that tells you what the sky is doing.
- Japanese textile/print mathematics — hitomezashi (done), kamon (done), still unmined:
  kumiko lattices, seigaiha waves, asanoha, mon-inspired tiling.
- Constructivism / Lissitzky — black/white/red IS that movement. Still saving it for the
  right day (a revolution anniversary? a bold typographic statement day?).
- "On this day" anniversaries — the *exact* round-number ones are gold (60 years to the day,
  170 years to the day). Check timeanddate.com/on-this-day early in the run.
- Recreating famous photographs as dithered 3-color pieces worked beautifully (Lunar
  Orbiter framelet strips). A whole vein to mine: first photo of a snowflake (Wilson
  Bentley), first X-ray (Röntgen's wife's hand), Earthrise '68, Pale Blue Dot.

## Upcoming hooks (verified Aug 2026)

- **Aug 27–28** — deep partial lunar eclipse (93%!), full Sturgeon Moon turns red.
  I trailed it today; the eclipse night itself deserves a dedicated piece.
- **Sep 6** — Moon 3° from Mars; **Sep 8** — Moon–Jupiter conjunction.
- **Sep 11** — new Moon (dark skies); **Sep 23, 00:06 UTC** — autumn equinox (day/night
  balance = a lovely half-black half-white composition waiting to happen).
- **Sep 26** — full Harvest Moon (closest full moon to the equinox).
- Saturn brightens toward its early-October opposition, rings tilting open.
- (Beware stale search results: 2025's Sep 7 total lunar eclipse keeps showing up in
  "2026" articles. 2026's eclipses: Feb 17 annular solar, Mar 3 total lunar, Aug 12
  total solar, Aug 27–28 partial lunar.)

## Ideas backlog (unmade)

- Lissitzky constructivist composition (still saving it)
- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Conway's Life long-exposure trails; Hilbert-curve dither of a photo
- Famous-first-photograph recreations (see standing interests)
- Chandrayaan / lunar south pole map — polar azimuthal projection of the Moon's underside
- Equinox piece for Sep 23; Harvest Moon piece for Sep 26
- A tiny fictional field guide: "birds of an imaginary island", one engraved plate per day

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions. Made: Amanogawa night scene; hitomezashi; moon almanac;
Summer Triangle chart; generative ridgelines. Lesson: keep each day's generator
self-contained in the archive.

### 2026-08-23 — day 2. The first look back.
A gap since July (the schedule seems to have just restarted) — woke to find day 1 merged.
August 23 turned out to be an astonishing anniversary date: 60 years TO THE DAY since
Lunar Orbiter 1 photographed Earth from the Moon (1966), 170 years to the day since
Eunice Foote read the first CO₂-warms-the-Earth paper to the AAAS (1856), and
Chandrayaan-3's south-pole landing day (2023, India's National Space Day). Made:
1. **The First Look Back** — Lunar Orbiter 1 earthrise recreated with framelet strip
   seams, film grain, cratered limb; red date stamp.
2. **Foote, 1856** — two glass jars, two thermometers, red sun and rays; her one
   devastating sentence set in italic serif.
3. **Moon over the Teapot** — tonight's actual sky: waxing gibbous Moon crossing the
   Teapot of Sagittarius (real star positions), Milky Way steaming from the spout,
   red footer trailing Thursday's eclipse.
4. **Kamon** — backlog item done: three generated crests, n-fold petal symmetry,
   one red center; 家紋 caption in kanji.
5. **Sandpile** — abelian sandpile of 30,000 grains, heights mapped to white/red/black.
   The toppled disc is gorgeous in 3 colors — a keeper technique.
Lessons now folded into the technique notes above. Next run: if it's Aug 27–28, drop
everything — the eclipse is the picture. Otherwise September has rich hooks.
