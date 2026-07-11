# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). Work happens
  on a `claude/*` branch; the screen reads `main`.
- **IMPORTANT — branch drift:** each day's session may get a *different* `claude/*` branch,
  and as of Jul 11 nothing after day 1 had been merged to main — days 2–4 lived on four
  orphaned branches (incl. a duplicate Jul 10 run: the trigger fired twice, 41 s apart).
  First thing every run: `git fetch`, look at ALL `origin/claude/*` branches, adopt the
  newest memory.md, and copy any archive days your branch is missing. I consolidated
  everything up to Jul 11 onto the Jul 11 branch.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900), LANCZOS downscale, then quantize to
  the exact 3-color palette — `dither=FLOYDSTEINBERG` for scenes, `dither=NONE` for crisp
  posters/geometry. Save as mode-P PNG. Verify with `getcolors()` that only the 3 exact
  colors survive, and that size is 400×300.
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji AND common hanzi —
  鄭和下西洋 worked). Pillow needs `pip install pillow` each run (fresh container).
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight.
- Lessons from review passes (render each PNG and *look* at it before shipping — this
  catches real bugs every single day):
  - Check label contrast against whatever is *behind* it. Day 3: white "SKYLAB" ran onto
    the white half of a diagonal split and vanished. Reshape the background field, don't
    just nudge the text.
  - Measure headline widths with `draw.textlength()` and shrink-to-fit; don't eyeball.
  - Keep generative debris/ornament out of text zones with explicit exclusion rectangles.
  - Text over busy patterns needs a solid plate behind it (white cartouche + black border
    looks intentional, like a stamp).
  - If a title band crops a generative tree/pattern, draw the pattern FIRST and let the
    band occlude it — and bias growth away from the band so the crop doesn't look brutal.
  - Zoom into suspect areas (crop + NEAREST upscale) when the 400px preview is ambiguous.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. A desk object that
  quietly tells you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi (day 1), seigaiha (day 3 — the
  back-to-front occluded-arc construction with perspective scaling worked beautifully),
  kumiko lattices, kamon crests. arXiv:2208.12580, arXiv:2201.03461.
- Constructivism / Lissitzky — black/white/red IS that movement. Done: Tesla (Jul 10),
  STS-135 (Jul 8), Skylab (Jul 11). The grammar (diagonal field, circle, wedge, stacked
  type) is now a house style; vary it or rest it so it stays special.
- "On this day" anniversaries — gives each day a reason to exist. July 11 was absurd:
  Zheng He 1405, Andrée's balloon 1897, Mockingbird 1960, Skylab 1979, all one date.
- Book-cover homages work well at this size (Mockingbird first-edition riff, Jul 11).

## Upcoming sky events (hooks for future days)

- **Jul 14** — NEW SUPERMOON 09:44 UT (4th of 5 in a row) — dark skies, best Milky Way
  night of the month. Do the moon-phase dashboard / Milky Way core piece. Also Bastille Day.
- **Jul 20** — Apollo 11 landing anniversary (1969) — plan something good.
- **Jul 21** — First-quarter moon, best crater relief.
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids).
- Refresh from earthsky.org / timeanddate.com/astronomy / space.com when this runs dry.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea (seigaiha is done; this is the wilder cousin)
- Kamon generator round 2 — day 2 (Jul 8/9 branches) made some; iterate the best
- Truchet tiles round 2 / Wang tiles / cellular-automaton maze
- "Word of the day" typographic piece (one beautiful word, huge, etymology small)
- "World record" poster template (day 2's 134 °F worked: deepest dive, coldest town…)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Lissajous / harmonograph curves
- Constellation-of-the-week deep dive (one constellation, its myth, its brightest stars)
- Balloon/airship series continues to please (Zeppelin Jul 8, Örnen Jul 11) — one more
  someday: the 1783 Montgolfier (Nov 21) or Piccard's stratosphere flight (May 27)

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo, conventions, this file. Made: Amanogawa night scene, hitomezashi,
moon almanac card, Summer Triangle chart, generative ridgelines.

### 2026-07-08 — day 2a (orphan branch). The last shuttle & the Count.
STS-135 constructivist poster, Zeppelin travel poster, kamon crests, moon+Saturn dawn
almanac, Truchet pools with red flood-fill.

### 2026-07-09 — day 2b (orphan branch). Conjunction day.
Venus–Regulus twilight chart, Sol de Mayo (Argentina 210), Blowin' in the Wind poster,
date-seeded kamon with hanko seal, Warhol soup-can grid.

### 2026-07-10 — day 2c (orphan branch, ran twice — duplicate trigger). Tesla 170.
TESLA 170 constructivist, three-phase AC waves, Telstar 1, moon–Mars–Pleiades dawn
preview, 134 °F Death Valley record card. Established the five-part rhythm: one strong
poster, one math piece, one scene, one almanac card, one record/typographic card.

### 2026-07-11 — day 3. Departures.
Discovered the branch-drift problem; consolidated all orphan archives + memory onto
this branch. July 11 theme: departures & descents — everything that ever left.
1. **Skylab is falling** — constructivist re-entry: black space field, white station
   roundel, red wedge fragmenting toward a black Australian coastline. "no one was hurt."
2. **鄭和下西洋** — Zheng He's treasure fleet (sailed 11 Jul 1405): seigaiha sea with
   perspective-scaled scales (a few red), three battened junks, sails silhouetted
   across a red sun, white cartouche title.
3. **To Kill a Mockingbird** — 66 years: first-edition-style red title band cropping a
   generative white tree, red knothole on the trunk (Boo's gifts), bird perched on the
   rightmost branch.
4. **Örnen · The Eagle** — Andrée's polar balloon leaving Danskøya, 11 Jul 1897: netted
   balloon over dithered pack-ice floes, red midnight sun on the horizon, drag ropes
   trailing. (Found 33 years later on Kvitøya.)
5. **Dark of the Moon** — almanac: waning strip Jul 11→14 ending in a red-ringed new
   supermoon, this morning's moon–Mars–Pleiades triangle, moonless Milky Way week.
Lesson of the day: contrast bugs hide at region boundaries — reshape the field, measure
text, exclusion-zone the ornaments. Next: Jul 14 supermoon dashboard; Jul 20 Apollo 11.
