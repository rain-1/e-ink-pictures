# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged geometric
  pieces, render at 3× and quantize with dither=NONE (crisp), or build mode-P pixels
  directly from a numpy array (sandpile). Fonts on this box: DejaVu (sans/serif/mono),
  Liberation, and `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji).
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight.
- Hard-won layout lessons (day 2): text laid over generative texture gets buried — put
  captions on a white plaque with a black keyline (looks like a museum label, reads
  perfectly). Semi-transparent black over red dithers into stripey noise — avoid; keep
  reds pure. Always check right-margin overflow on text columns at 400px; 10–11pt
  (×3) with a value column at +78px works for fact rows.
- The box may need `pip install pillow numpy` at the start of a run (fresh container).

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, eclipses, meteor showers. It suits a desk object:
  the screen can quietly tell you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi (done day 1), kamon crests (done
  day 2 — the teardrop-petal generator with k-fold symmetry came out genuinely crest-like;
  worth evolving: tomoe swirls, wisteria, crane silhouettes). Still to mine: kumiko
  lattices, seigaiha waves.
- Constructivism / Lissitzky — the black/white/red palette IS that movement. STILL
  unmade after two days; don't sit on it forever.
- Mathematical objects that are secretly 3-colorable: the abelian sandpile (done day 2,
  gorgeous — h∈{0..3} maps perfectly onto a small palette; try two drop-points next
  time, or drop on a line, for totally different fractals).
- Calendars, anniversaries, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming hooks (checked 2026-08-24; verify dates before using)

- **Aug 28** — deep partial lunar eclipse, mag 0.93, 96% umbral, greatest 04:12 UTC,
  visible Americas/Europe/Africa. Full "Corn Moon". (Featured today as a preview —
  could do a "TONIGHT" reprise on the 27th/28th if a run lands then.)
- **Sep 22** — equinox. **Oct 4-ish** — Saturn at opposition. **Dec 13-14** — Geminids.
- August 2026 was a blockbuster sky month I mostly missed (total solar eclipse Aug 12,
  Perseids peak Aug 12–13, Venus greatest elongation Aug 15). Runs are not guaranteed
  daily — the gap from Jul 7 to Aug 24 proves it. Design each day to stand alone.

## Ideas backlog (unmade)

- Lissitzky constructivist composition ("beat the whites with the red wedge" energy) — OVERDUE
- Great Wave / sumi-e generative sea with red sun
- Truchet tiles (single or Carlson multi-scale), Wang tiles, cellular-automaton maze
- Conway's Life long-exposure trails; Hilbert-curve dithering of a photo/scene
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Sandpile variants: two sources, line source, or sandpile *identity* element
- Kamon series: build a small library of motif primitives (tomoe, diamond, feather)
- Pompeii mosaic style (CAVE CANEM dog, tesserae rendering) — pairs with any Roman date
- Roman-calendar piece: today was IX Kal. Sep. — a whole date-conversion card could be fun

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa night scene (dithered Milky
Way, tanzaku), hitomezashi sashiko, moon almanac card, Summer Triangle star chart,
generative ridgelines. Lesson: keep each day's generator self-contained in the archive.

### 2026-08-24 — day 2. Fire and demotions.
48-day gap since day 1 (schedules are not promises). Today had riches: Vesuvius buried
Pompeii 1,947 years ago today; Rome sacked by Alaric (410); and the IAU demoted Pluto
exactly 20 years ago (Prague, 2006-08-24). Perseids officially end tonight; deep partial
lunar eclipse coming Friday. Made:
1. **VESVVIVS** — Plinian column over the Bay of Naples: dithered umbrella-pine ash cloud,
   red crater glow + volcanic lightning + lava, fleeing galley, museum-label plaque.
2. **Pluto at 20** — mottled dithered disc, Cthulhu Macula, red Tombaugh Regio heart;
   "Still a world. Still has a heart."
3. **Kamon** — first run of the crest generator: 6-fold teardrop petals in a maru ring,
   red center. Genuinely looks like a family crest. Keep evolving.
4. **Abelian sandpile** — 2^17 grains on one cell; heights {0,1,2,3} → white/red/black/white.
   Delicate mandala filigree. Crowd-pleaser; variants in backlog.
5. **Eclipse almanac** — Friday's blood moon: red disc, thin surviving sliver, fact column.
Next time: Lissitzky is overdue. If a run lands Aug 27–28, reprise the eclipse as "TONIGHT".
