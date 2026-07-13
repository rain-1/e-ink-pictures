# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). The daily
  scheduled run develops on a Claude working branch (e.g. `claude/…`), not `main` directly —
  push there and let it merge. Don't assume `main` is checked out.
- Environment note: Pillow isn't pre-installed on the runner — `pip install Pillow` first.
  The JP gothic font at `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` renders kanji fine.
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

- **Jul 14** — NEW moon, 09:43 UTC (a "super" new moon, so invisible). The gift is *darkness*:
  moonless nights ~Jul 12–16 are the best of the month for the Milky Way core & deep sky.
- **Jul 21** — Jupiter joins the slender crescent Moon in the morning sky.
- **Jul 30–31** — Southern δ Aquariids peak in the predawn hours (Milky Way core rides high).
- **Aug 12–13** — Perseids peak (~14:53 UTC Aug 13), near a new moon → excellent dark-sky year.
  Worth something special: radiant in Perseus, best after midnight.

## Ideas backlog (unmade — pick the freshest, keep the pot stocked)

- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300. **Still want this.**
- Seigaiha (blue-wave) arcs; kumiko lattices — geometric Japanese pattern math.
- Conway's Life long-exposure trails; sandpile (abelian) fractals; Hilbert-curve dithered photo.
- Wang tiles / maze from an aperiodic set; reaction–diffusion (Turing) patterns dithered.
- Anniversary posters as a template: pick a *today* event and set it in bold type + one icon.
  (Jul 13 candidates I passed on: 1st World Cup 1930 Montevideo; Live Aid 1985; Hollywood sign 1923;
  David's *Death of Marat* 1793 — a real B/W/R painting, tempting but grim.)
- Moon-phase dashboard for notable moon days. Phyllotaxis / sunflower spirals. Voronoi shatter.

## Done so far (don't repeat the exact piece; the *mode* can return with a new subject)

- Tanabata Milky Way scene, hitomezashi sashiko, last-quarter moon almanac, Summer-Triangle star
  chart, sine-wave ridgelines (day 1, 2026-07-07).
- Constructivism (Lissitzky red-wedge), generative great wave, multiscale Truchet, 星月夜 kanji
  typography, Rule-30 cellular automaton (day 2, 2026-07-13).

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

### 2026-07-13 — day two. Dark of the moon.
Tonight sits in the moonless window before the Jul 14 new moon — the darkest, best Milky-Way
nights of the month. Rather than lean astronomy again (day 1 already had three sky pieces), I
spent today's set clearing long-saved backlog and widening the range of *modes*:
1. **Krasnym Klinom** — El Lissitzky "Beat the Whites with the Red Wedge" homage. Generative
   Suprematist/Constructivist composition: black field, white circle, the red wedge driving in,
   scattered bars & type. Hard-edge, pure palette. The black/white/red panel *is* this movement.
2. **Nami** — generative Hokusai-esque great wave: layered sine+noise swells, dithered foam
   fingers, a flat red sun disc. Tonal render → Floyd–Steinberg. Organic counterweight to the geometry.
3. **Truchet** — multiscale Truchet tiling (quarter-arc tiles at two scales), date-seeded, red
   accents on a subset. Culture-neutral pattern math, hard-edge.
4. **星月夜 (hoshizukiyo)** — "word of the day" typography: a moonless, star-filled night — the
   literal state of the sky tonight. Huge kanji in red, romaji + gloss + a tiny etymology, a faint
   dithered star field behind. My single, restrained tie-in to the real sky.
5. **Rule 30** — elementary cellular automaton spacetime, single red seed cell at top descending
   into chaos (the rule Wolfram used for randomness). Crisp 1× render, red light-cone edges.
Spread of modes: geometric-abstract / organic-tonal / generative-pattern / typographic / algorithmic.
Cultures: Russian, Japanese ×2, pure-math ×2. Lesson: `pip install Pillow` on the runner first;
the designated dev branch is a `claude/…` branch, not `main`. Next: kamon crest still unmade; the
Aug 12–13 Perseids (near new moon) deserve a real showpiece.
