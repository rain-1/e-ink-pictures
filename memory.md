# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Each session is given a designated `claude/...` branch to push to; Edward merges to
  `main` (the screen reads `main`). Push there, then send a notification so he can merge.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then quantize into the exact 3-color palette — Floyd–Steinberg dither for tonal/photographic
  pieces, **no dither (nearest-color threshold)** for crisp poster/geometric pieces.
  Save as mode-P PNG. Pillow may need `pip install pillow` each run (fresh container).
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, Noto, FreeFont, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji).
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight
  against black/white.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, eclipses, meteor showers. It suits a desk object:
  the screen can quietly tell you what the sky is doing.
- Japanese textile/print mathematics — hitomezashi (done day 1), kumiko lattices,
  kamon crests (done day 2), seigaiha waves still unmined.
- Constructivism / Lissitzky — black/white/red IS that movement (finally used, day 2).
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.
  Victorian engraving / letterpress styling suits historical anniversaries well.

## Upcoming sky events (hooks for future days)

- **Aug 12–13** — TOTAL SOLAR ECLIPSE (totality over Greenland, Iceland, N. Spain; partial
  from much of Europe/N. America) *and* the Perseid peak the same night with a new moon —
  no moonlight, possibly the best Perseid year in a decade. Made the eclipse poster today;
  an eclipse-day piece on the 12th would be right (path map? countdown zero?).
- **Aug 28** — deep partial lunar eclipse, ~96% of the Sturgeon full Moon inside the umbra —
  a nearly-blood moon. A RED moon on a red-capable screen. Do not miss this one.
- Sep 21 (approx) — Saturn at opposition, brightest of the year. Verify closer to the date.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Blood-moon poster for Aug 28 (red disk, umbra geometry diagram, eclipse timeline)
- Seigaiha (blue-ocean wave) tiling — overlapping fans, reads beautifully in 2 colors + red
- Tide-table / almanac strip aesthetics; barometer & weather-glass diagrams
- Halftone portrait experiment (dither a public-domain engraving down to 3 colors)
- Kumiko lattice patterns (asanoha etc.) — the woodwork geometry, thin white lines on black

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa Tanabata scene, hitomezashi,
moon almanac card, Summer Triangle chart, generative ridgelines. Lesson: keep each day's
generator self-contained in the archive so any day is reproducible.

### 2026-08-05 — day 2. The wire, the wedge, the signal.
(No runs between Jul 7 and today — schedule gap, not a crash.) August 5 turned out to be
a gift of a date: the first transatlantic telegraph cable was completed Aug 5, **1858**
(Valentia, Ireland → Heart's Content, Newfoundland), and the world's first electric
traffic signal went live Aug 5, **1914** (Euclid Ave & E 105th St, Cleveland — red/green
lenses and a buzzer). Also the week before the Aug 12 eclipse+Perseids double event.
Made:
1. **The Red Wedge Eclipse** — the saved Lissitzky constructivist idea, spent on the Aug 12
   total solar eclipse announcement: black moon-disk overtaking red sun, diagonal wedge.
2. **The Atlantic Telegraph** — Victorian engraving-style chart: coastlines, catenary cable
   across a lined sea, the 1858 route, real Morse code as an ornamental border.
3. **Perseids chart** — real star positions (Cassiopeia's W + Perseus), radiant marked,
   meteor streaks, "new moon / no interference" almanac note.
4. **Kamon** — date-seeded generative Japanese crest, k-fold rotational symmetry, one red
   accent. First fully-generative emblem; the petal-polygon helper is in today's generate.py.
5. **STOP — 1914** — letterpress poster for the first electric traffic signal; red lens lit.
Lessons: threshold-quantize (no dither) keeps poster edges clean; dither only tonal areas.
Next time: it'll be past the eclipse — the Aug 28 blood moon is the next anchor.
