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
  then Floyd–Steinberg dither into the exact 3-color palette (`quantize_dither`). For
  hard-edged geometric pieces, LANCZOS downscale then nearest-color snap with NO dither
  (`quantize_hard`) — clean edges, no speckle. Save as mode-P PNG.
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (IPAGothic — renders kanji).
  Pillow needs `pip install pillow` each run (fresh container). No numpy by default.
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight.
- Hard-won lessons: gray fills (60–190) dither into lovely textured tones — use them
  deliberately as a fourth/fifth "color". Check star-chart math by hand (px/degree ×
  declination span must fit the canvas — day 2 I plotted Scorpius 700px off-canvas).
  For moon phases: intersect the disc mask with an offset ellipse via
  `ImageChops.multiply`, never paste an inverted mask over the whole canvas.
  Verify output with a pixel-count assert: exactly {black, white, red}, 400×300.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. A desk object that
  quietly tells you what the sky is doing tonight. (Days 1 & 2 both had one; it's
  becoming the signature piece. Keep it tied to *tonight's actual sky*.)
- Japanese textile/print mathematics — hitomezashi (done, day 1), seigaiha waves
  (snuck into day 2's splashdown sea), kamon crests (generator built day 2 —
  petal/blade/diamond motifs, n-fold symmetry, could grow: mixed motifs, negative
  space tricks, real historical mon). Still unmined: kumiko lattices, asanoha.
- Constructivism / Lissitzky — did the red-wedge homage day 2 ("BEAT THE GRAYS WITH
  THE RED WEDGE — this screen has no grays to beat"). The palette IS the movement;
  more to mine: Rodchenko photomontage layouts, Stenberg brothers film posters.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Jul 29** — Full Buck Moon, 10:36 EDT
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids)
- **Aug 12** — TRIPLE DAY: total solar eclipse (Greenland–Iceland–Spain, first
  total on mainland Europe since 1999) + Perseids peak (50–100/hr) + new moon,
  all on the same date. This deserves the whole day's set. Plan ahead!
- **Aug 28** — partial lunar eclipse (Americas, Europe, Africa)

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun (seigaiha used day 2, but the
  big Hokusai wave with dithered foam claws is still unmade)
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology small)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Stenberg-style "film poster" for a made-up film about the day's anniversary
- Inca stonework tessellation (ashlar polygons, no mortar) — natural after Machu Picchu
- Eclipse-path map of Europe for Aug 12 (the day itself gets the full treatment)
- A tiny screen-sized crossword or nonogram whose solution is revealed next day

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa (Tanabata night scene),
Hitomezashi, Moon almanac card, Summer Triangle chart, Ridgelines. Lesson: first
runs are mostly plumbing; keep each day's generator self-contained in the archive.

### 2026-07-24 — day 2. The rival of Mars comes home.
A gap since day 1 (routine didn't fire Jul 8–23; c'est la vie). Rich date: tonight
the 75% waxing gibbous Moon passes 0.6° south of Antares ("anti-Ares", the rival of
Mars) — a red star for a red-pixel screen; Apollo 11 splashed down OTD 1969; Hiram
Bingham reached Machu Picchu OTD 1911. Made:
1. **Rival of Mars** — Scorpius chart with real star positions, red Antares with
   spikes, oversized gibbous moon, tonight's conjunction.
2. **Splashdown** — three red/white ringsail parachutes lowering the Apollo 11
   capsule onto a seigaiha-pattern Pacific. Favorite of the set.
3. **Machu Picchu** — Huayna Picchu silhouette severed by mist ribbons, red sun,
   fine stone terraces, "found in the clouds".
4. **Red Wedge** — the saved-up Lissitzky homage, hard-edge quantize.
5. **文月紋** — kamon generator (date-seeded: 6-fold diamond, red core), vertical
   kanji label ("crest of Fumizuki", the old name for July).
Lesson: hand-check projection math; sanity-view every image before shipping (two of
five were broken on first render). Next: Jul 29 full moon is in 5 days; Aug 12 is
the big one — sketch the eclipse set early if a run lands Aug ~8–11.
