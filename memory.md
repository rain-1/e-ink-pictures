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
- Technique notes that work: render at 3× (1200×900), LANCZOS downscale, then quantize
  to the exact 3-color palette. `Dither.NONE` gives crisp hard edges (used for all of
  day 2 — it's excellent); Floyd–Steinberg only when there's a real gradient to preserve.
  Fonts: DejaVu (sans/serif/mono — *no* serif-italic; use LiberationSerif-Italic),
  Liberation, and `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji!).
  DejaVu also covers Cyrillic — АВГУСТ rendered fine.
  Red reads *bright* on these panels — use as accent, it carries enormous weight.
  Sweeping many shrinking circles along a path makes good organic strokes (tomoe
  commas, wheat grain). For a tomoe: heads at 0.42R, tails drifting *outward*
  (+0.26R over a 150° sweep) or the three commas merge into a blob — learned the hard way.
- Pillow is NOT preinstalled in the fresh container — `pip install pillow` first.

## Standing interests (what I find myself drawn to)

- Sky almanac data — the screen as a quiet desk object that tells you what the sky is doing.
- Japanese design mathematics — hitomezashi (done day 1), kamon crests (done day 2:
  parametric motifs with n-fold symmetry work beautifully — tomoe, petals, nested
  diamonds, crescent+star, seigaiha-in-disc, wheel). Still unmined: kumiko lattices,
  asanoha, actual sashiko *moyōzashi*.
- Constructivism — did the Lissitzky homage day 2 (red circle, black bar, white wedge).
  The vocabulary is deep; could return via Rodchenko lines or Moholy-Nagy later, but
  don't repeat soon.
- Literature as image — "Call me Ishmael" worked great; one iconic opening line + one
  bold illustration is a strong repeatable format (but vary the layout each time).
- Calendars, festivals, "on this day" — gives each set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Aug 12** — TOTAL SOLAR ECLIPSE (Arctic → Greenland → Iceland → Spain) *and*
  Perseids peak that same night under a new moon (~100/hr). The best sky date of 2026.
  If I run that day, the whole set could be eclipse-themed — totality sequence,
  shadow-path map, radiant chart.
- **Aug 15** — Venus greatest eastern elongation (evening star at its best)
- **Aug 27–28** — Partial lunar eclipse, 93% of moon in umbra
- **Sep 22** — Equinox. Look up October events when September comes.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology small)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Eclipse-day special (Aug 12 — see above)
- Kumiko lattice panel; asanoha starburst field
- Solar-system orrery showing today's actual planet positions (top-down)
- A tiny comic strip / sequential panel piece (4 panels, wordless)
- Isotype-style pictogram statistics (Neurath — fits the palette era perfectly)
- Bauhaus poster (Aug 6 is the day the Bauhaus Dessau building opened, 1926 — centenary!)
- Radio/morse: a message in Morse code as a visual rhythm band

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions. Made: Amanogawa night scene, hitomezashi, moon almanac
card, Summer Triangle star chart, generative ridgelines. All dithered/soft style.

### 2026-08-01 — day 2. Lughnasadh / Melville / the August sky.
(Gap since Jul 7 — the schedule evidently didn't fire for most of July; don't assume
consecutive days.) Researched: Aug 12 total solar eclipse + Perseids-under-new-moon
coincidence; Lughnasadh/Lammas first-harvest; Melville b. Aug 1 1819; kamon
construction (motif + enclosure + count + orientation). Made, all hard-edged this time
(deliberate contrast to day 1's dithering):
1. **Kamon sampler** — six procedural crests in maru rings, 2 red 4 black, caption 家紋.
2. **The August Sky** — black almanac card: eclipse corona w/ red prominences, meteor
   streaks, four dated entries, red footer "eclipse by day, meteors by night".
3. **АВГУСТ** — Lissitzky homage finally made: red circle, black diagonal bar, white
   wedge piercing to the circle's heart, rotated Cyrillic type.
4. **Lughnasadh** — 34 seeded wheat stalks w/ grain heads + awns against a huge red sun.
5. **Call me Ishmael** — white sperm whale in a black wavy sea, red harpoon line
   arcing down from the sky, Liberation Serif Italic opening line.
Lessons: nearest-neighbor quantize (no dither) at 3× is the crispest look for flat
graphics; check text widths (11px bold ≈ fits ~28 chars in 190px); place rotated text
last and keep scatter elements away from it. Committed on branch
`claude/tender-wright-tkkn58` per session instructions (day 1 ended up on main —
Edward presumably merges).
Next time: if before Aug 12, tease the eclipse; Aug 6 would be the Bauhaus Dessau
centenary — perfect for this palette.
