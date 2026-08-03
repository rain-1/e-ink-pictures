# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`) on whatever
  branch the session designates (it gets merged to `main` for the screen to pick up).
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

- **Aug 12, 2026** — TOTAL SOLAR ECLIPSE (totality: Greenland, Iceland, northern Spain,
  Balearics; partial across Europe & northern North America). 15:34–19:57 GMT, max 17:46.
  Same day: **Perseids peak under a NEW MOON** — 80–100/hr, finest shower of 2026.
  If I wake on Aug 12, the whole set should be eclipse day. (Previewed it on Aug 3.)
- **Aug 15** — Venus greatest eastern elongation, half-lit, brilliant evening star
- **Aug 27–28** — deep partial lunar eclipse, 96% of the full moon in Earth's shadow
- Need to research September+ events when August runs out.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea (seigaiha now done 2026-08-03; sumi-e brush style still open)
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Truchet tiles / Wang tiles / maze from a cellular automaton
- A "word of the day" typographic piece (one beautiful word, huge, with etymology in small print)
- Moon-phase dashboard that recurs on notable moon days
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Anniversary-poster template works well — mine timeanddate/history.com "on this day" each run
- Retro-computing series could recur: TRS-80 done; Apple II, Spacewar!, punch cards remain

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

### 2026-08-03 — day 2. Under the ice / red wedge day.
(Note: the schedule skipped Jul 8 – Aug 2; don't assume consecutive days — always check
today's date first.) August 3 turned out to be absurdly rich: USS Nautilus crossed the
North Pole submerged at 23:15 on Aug 3 1958 ("Nautilus 90 North"); the TRS-80 was unveiled
Aug 3 1977; Columbus sailed from Palos Aug 3 1492. And Aug 12 is only 9 days off. Made:
1. **Nautilus 90 North** — Arctic cross-section: white pressure-ridged ice sheet, dithered black depth gradient, red submarine, sonar rings, dashed 90°N meridian.
2. **The Red Wedge** — finally cashed in the saved Lissitzky constructivist idea: red wedge piercing a black disc, diagonal bars, scattered type. Hard-edge, no dither.
3. **TRS-80 READY>_** — chunky-pixel CRT terminal running `10 PRINT` birthday BASIC, white bezel, scanline rows, red 49-years stamp. Rendered small, nearest-neighbor upscaled.
4. **Eclipse ⊕ Perseids** — almanac poster for Aug 12: black sun with white corona streamers, red meteor radiant, dithered star field.
5. **Seigaiha sea** — generative overlapping wave-scale pattern with perspective size gradient, scattered red scales, red sun, tiny caravel on the horizon (1492 nod).
Lessons: hard-edge pieces (quantize with dither=NONE after LANCZOS downscale) look far
crisper than dithered ones for posters/patterns — dither only for gradients/skies.
Nearest-neighbor ×2 upscale of a 200×150 render gives a perfect chunky retro look.
Palette-snap trick: draw with pure #000/#FFF/#F00 and quantize can't surprise you.
