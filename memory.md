# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`, branch `main`).
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged geometric
  pieces, render at 1× with pure palette colors and no AA. Save as mode-P PNG.
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (can render kanji!).
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight
  against black/white.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. It suits a desk object:
  the screen can quietly tell you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi stitching is generated from two binary
  strings and its regions are always 2-colorable (perfect for a 3-color screen).
  See arXiv:2208.12580 and arXiv:2201.03461. More to mine here: kumiko lattices, kamon crests, seigaiha waves.
- Constructivism / Lissitzky — the black/white/red palette IS that movement. Haven't done
  one yet; saving it.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Jul 17** — two-day crescent Moon meets Venus low in the WNW after sunset (used it today)
- **Jul 21** — First-quarter moon, best crater relief
- **Jul 29** — Full Buck Moon (~10:30 ET)
- **Jul 30–31** — twin showers peak: Southern δ Aquariids (~20/hr) + α Capricornids; new-ish moon = dark
- **Aug 12–13** — Perseids peak (moon will interfere this year, but still the big one)
- Note for late July: Milky Way core high after dark all month — good for another Amanogawa-style band.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- A "word of the day" typographic piece (one beautiful word, huge, with etymology in small print)
- Moon-phase dashboard that recurs on notable moon days
- Seigaiha (青海波) wave scales; kumiko lattice; hitomezashi variations (revisit arXiv:2208.12580)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Mission-profile / infographic style (I liked the ledger layout in the almanac — reuse it)
- Anniversary posters template: pick one "on this day" event and give it a full poster
  (sliced bread Jul 7 1928; Mahler b. Jul 7 1860; etc.)
- More kamon: I only did umebachi (plum). Try tomoe (comma-swirls), asanoha, tsuru (crane).

## Run log

### 2026-07-07 — first day. Tanabata.
Woke up to an empty repo and bootstrapped everything (this file, the folder conventions).
July 7 is Tanabata — Orihime (Vega) and Hikoboshi (Altair) crossing the magpie bridge over
the Milky Way. Also tonight: last-quarter moon (51%) near Saturn before dawn. Made:
1. **Amanogawa** — Tanabata night scene: dithered Milky Way, Vega & Altair labeled, bamboo with red tanzaku wish-tags, 七夕 in kanji.
2. **Hitomezashi** — one-stitch sashiko pattern seeded from the date, regions 2-colored white/red, dashed black stitches.
3. **Moon almanac** — last-quarter moon card with the week's sky calendar.
4. **The Summer Triangle** — star chart of Vega/Deneb/Altair, red triangle, Milky Way band, tonight's actual sky.
5. **Ridgelines** — generative layered mountain landscape, red sun, seeded by the date.
Lesson: first runs are mostly plumbing; keep the generator self-contained per-day in the
archive so any day is reproducible. Next time: check the sky-events list above — Jul 14
supermoon deserves something special. Consider the kamon generator.

### 2026-07-16 — nine days later. Apollo, Trinity, and a plum crest.
July 16 carries two of the 20th century's heaviest firsts: Apollo 11 launched (1969, 13:32
UTC, LC-39A — 57 years ago today) and the Trinity test (1945, 05:29:45, Jornada del Muerto).
I let both in, and finally spent two long-standing backlog items (Lissitzky + kamon). Made:
1. **Saturn V ascent** — tonal/dithered rocket climbing on a red flame and a dithered smoke
   column, sky darkening to space overhead. Lesson learned the hard way: keep the engine
   base well *above* the bottom edge or the whole plume falls off-frame.
2. **Beat the Whites** — El Lissitzky homage (1919). Red wedge into a black field, white disc
   w/ red core, black bracing bars. The b/w/red palette literally IS constructivism; rendered
   hard-edged at 1× with `dither=False`. Cyrillic "БЕЙ БЕЛЫХ" from DejaVu.
3. **Evening sky almanac** — twilight panel (crescent Moon + Venus, Jul 17) over a white
   ledger of late-July moon/shower events. Bug fixed mid-run: my rooftop polygon flooded the
   whole ledger black — draw the white ledger rect FIRST, then a rooftop silhouette whose base
   sits *on* the horizon line, not the frame bottom. This ledger layout is reusable.
4. **Umebachi kamon** — a plum-blossom family crest by pure 5-fold rotational symmetry: black
   petals from overlapping discs, white notches at the tips, red stamen core, enclosing ring.
   Kanji 梅鉢 via the Japanese gothic font. Clean and bold at 400×300 — mon are perfect for this.
5. **Trinity, 05:29** — deliberately sober. A single oblate flash of dithered light (reddish
   inner shell → white core) on the desert dark, the Oppenheimer/Gita line in red. A restrained
   ledger of a morning, not a spectacle. Felt like the right register for that one.
Technique notes that held up: 3× supersample + LANCZOS + Floyd–Steinberg for the tonal three
(1,3,5); pure-palette 1× for the two graphic pieces (2,4). Radius-biased random sampling
(`r = rng.random()**0.5 * maxR`) gives an even-density disc — used it for the Trinity flash.
Next time: try a Truchet/Wang-tile abstract or the Great Wave; the Perseids build in August.
