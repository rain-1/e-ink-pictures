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
  the screen can quietly tell you what the sky is doing tonight. The crescent-moon math
  (day 2) now lives in `_lit_crescent()` — reusable for any phase; k = 1−2·frac sets the
  terminator, waxing lights the right limb.
- Japanese textile/print mathematics — hitomezashi (done day 1) and seigaiha (done day 2)
  so far. The seigaiha trick that finally worked: draw each scale's top-half disk in WHITE
  first to crop everything beneath it, THEN stroke the concentric arcs — rows marching
  downward carve crisp scallops. Still to mine: kumiko lattices, kamon crests, asanoha.
  See arXiv:2208.12580 and arXiv:2201.03461 for hitomezashi.
- Constructivism / Lissitzky — DONE day 2 (PROUN). The black/white/red palette IS this
  movement; it photographs beautifully on the panel. Room for more: Rodchenko photomontage
  geometry, Malevich pure suprematist arrangements, a "Proun" that actually tiles.
- Anniversaries & "on this day" — gives each day's set a reason to exist *today*. Best when
  the fact has a visual hook (the "1.00" scoreboard, day 2). Seven-segment digit drawer now
  lives in `_seven_seg()` — reusable for any numeric/scoreboard/clock piece.
- Generative tilings — Truchet done day 2. The arc-tile + recursive-subdivision pattern is
  a keeper (`image5_truchet`). Wang tiles, hexagonal Truchet, and CA-mazes still open.

## Upcoming sky events (hooks for future days)

- **Jul 21** — First-quarter moon, best crater relief along the terminator at dusk
- **Jul 28** — Twin meteor showers peak: γ-Draconids + Piscis Austrinids (both faint)
- **Jul 29** — Full Buck Moon
- **Aug 12–13** — Perseids peak (the big one) — worth a real showpiece; moon will interfere though
- (When a month turns, refresh this list — search "night sky <month> 2026 meteor moon".)

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun (Hokusai energy, distinct from seigaiha)
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Wang tiles / hexagonal Truchet / maze from a cellular automaton (extend day-2 Truchet)
- A "word of the day" typographic piece (one beautiful word, huge, with etymology in small print)
- Moon-phase dashboard that recurs on notable moon days (reuse `_lit_crescent`)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Rodchenko/Malevich suprematist arrangement (a second constructivist angle)
- Kumiko / asanoha lattice — hexagonal wood-joinery geometry, thin lines, very clean
- A clock/countdown face using the `_seven_seg` drawer (e.g. days to the next full moon)

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

### 2026-07-18 — a wide spread of styles. Perfect-10 day.
Eleven days on, and I finally cashed in the constructivist idea I'd been saving. Deliberately
made the five as *different from each other* as I could — the archive was getting star-chart
heavy. Today, July 18, is the 50th anniversary of Nadia Comăneci's first perfect 10 (Montreal
1976, uneven bars) — the scoreboard couldn't render four digits so a 10.0 showed as "1.00".
That story was too good not to build. Made:
1. **PROUN** — constructivist composition after Lissitzky's "Beat the Whites with the Red
   Wedge" (1919). Hard-edge, 1×, pure palette. Red wedge driving into a white circle on a
   black diagonal ground; draughtsman lines with node dots; floating squares.
2. **Waxing Crescent** — tonight's real sky: 20%-lit crescent, 4 days old, low in the west
   after sunset, plus the week ahead (Jul 21 first quarter, Jul 28 twin showers, Jul 29 Buck
   Moon). New reusable `_lit_crescent()` for any phase.
3. **Seigaiha** — the blue-ocean-wave scale pattern, recolored for three inks. See the
   textile note above for the white-crop-then-stroke trick that made the scallops crisp.
4. **One Point Oh** — the Comăneci scoreboard, "1.00" in red seven-segment digits on a black
   panel (with a faint ghost of all segments so it reads as a real display). New `_seven_seg()`.
5. **Truchet** — multiscale arc-tile labyrinth, ~14% of tiles red, cells recursively
   subdivided for varied density. Rendered 3× + dithered for smooth arcs.
Lessons: (a) render each PNG and actually *look* at it — three of five had bugs on first
pass (title hidden under a black shard, text overflow, seigaiha far too dark) that were
obvious on sight and invisible in code. (b) Factor the reusable primitives (`_lit_crescent`,
`_seven_seg`) — they'll seed future pieces. Next time: something with the crescent math on a
notable moon day, or push further into the suprematist/Rodchenko direction while the palette
is begging for it.
