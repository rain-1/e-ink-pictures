# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(This file used to be called `memory.md`; the routine now asks for `memory-fable-5-1.md`.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  The routine pushes to a `claude/...` branch that Edward merges; don't assume `main`.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Toolbox: this box has *no* Pillow/numpy preinstalled — `pip install pillow numpy` first.
  Fonts: DejaVu (sans/serif/mono), FreeSans/FreeSerif (FreeSansBold is my display face),
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` and IPA Gothic for kanji, unifont.
- Two rendering routes, both proven:
  - **Tonal**: render 3× with AA, LANCZOS downscale, Floyd–Steinberg dither into the palette. (Day 1.)
  - **Hard-edged**: render 3× (or 1× for pixel-exact grids), downscale, then *snap* each
    pixel to the nearest of the three colors, no dither. Crisper and much more "printed". (Day 2.)
- Red reads *bright* on these panels — it carries enormous weight against black/white.
  Text below ~8 px is unreadable on the physical 4.2" panel; 9–11 px mono is the working
  caption size, 20–42 px for display type.
- Always look at the renders before committing. Every first render of day 2 had a text
  collision I only caught by looking (title through a disc, captions across a ring).

## My style, as it's forming

- A **red seal-square** with the day-of-month in white, in a corner of every image — my signature (started day 2).
- One idea per picture, one accent of red, a short mono caption. Posters, not illustrations.
- I like pictures that are *true*: real sky times, real dates, real constructions
  (kamon from circles, weaving from an actual draft, a collider event with real geometry).
- Day 1 was soft and dotted; day 2 was hard and graphic. Alternate, or mix within a set.

## Standing interests

- Sky almanac data — the screen can quietly tell Edward what the sky is doing tonight.
- Japanese pattern mathematics — hitomezashi (done), kamon (done, generator lives in
  archive/2026-09-10; more crests to add: kiri, fuji, chō butterfly, seigaiha, kumiko lattices).
- Constructivism / Lissitzky — done once (New Moon). Malevich / Rodchenko photomontage still untried.
- Textile structure — Albers draft notation (done). Next: 8-shaft twills, overshot, double-weave.
- Physics diagrams as art — event displays (done), Feynman diagrams, Compton scattering, bubble-chamber tracks.
- Calendars, festivals, "on this day" — gives each set a reason to exist *today*.

## Upcoming sky events (hooks; UK-centric, times UTC unless noted)

- **Sep 13–14** — thin waxing Moon sweeps past Venus after sunset. **Sep 14 ~10:30 UT** the Moon
  occults Venus; from the UK Venus *reappears* ~11:30 BST, Moon only 3° up in the SE, daylight.
- **Sep 18** — first-quarter Moon.
- **Sep 23** — autumn equinox.
- **Sep 26** — Harvest Moon (full) **and** Neptune at opposition, same night.
- Late Sep — Venus at peak brightness (mag −4.8) in the evening.
- Oct — Orionids peak ~Oct 21; Draconids ~Oct 8. Check for a Moon-Saturn pairing.

## Ideas backlog (unmade)

- Harvest Moon piece for Sep 26 — big, hard-edged, maybe woodcut-style with a red field.
- Equinox: day/night split exactly in half across the screen.
- Truchet / Wang tiles, maze from a cellular automaton, Conway Life long-exposure trails.
- "Word of the day" typographic piece (one word, huge, etymology small).
- Sandpile fractal; Hilbert-curve dithered photo; Voronoi stained-glass with red cames.
- Anniversary posters template: pick one thing that happened on this date, make it the hero.
- A tide table or sunrise/sunset ladder for Edward's location (need to ask — assume UK for now).
- Feynman diagram of the day (e.g. Compton scattering — Compton was born Sep 10 1892).

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped everything. Made: Amanogawa night scene, hitomezashi stitch, last-quarter moon
almanac, Summer Triangle chart, generative ridgelines. Soft, dithered, starry.

### 2026-09-10 — day 2. (The routine didn't fire between Jul 8 and Sep 9; the Jul 14
supermoon and Aug 12 total solar eclipse went unmarked. Never mind.)
Hooks found online: new moon tonight (Sep 11 03:27 UTC); LHC first beam on this day in 2008;
the Sep 14 daytime Venus occultation; kamon drafting (Bridges 2018 paper by Felicia Tabing
on compass-and-rule crest construction); Albers' *On Weaving* draft notation. Made:
1. **NEW MOON** — Lissitzky-grammar poster: black disc, red wedge, title running across the disc
   switching black→white at the edge. First constructivist piece; it works.
2. **MONCHŌ** — kamon sampler: hero red mitsudomoe, plus ume, mitsu-uroko, kikyō, tsuki-ni-hoshi,
   all from circles and lines. Small crest generators are reusable.
3. **EVENT 10.09** — transverse collider event display: curved tracks, red calorimeter towers,
   two muons, ring schematic with ATLAS/CMS/ALICE/LHCb.
4. **DRAFT No. 0910** — weaving draft (threading / tie-up / treadling) + drawdown rendered as
   black warp and red weft. Point threading × reversed twill = diamonds and chevrons.
5. **OCCULTATION** — Monday's Moon-hides-Venus: 12% crescent, red Venus at the dark limb,
   five-day phase strip.
Lesson: hard-edged + snap-to-palette gives the "printed" look I want; keep a quiet zone
for type; look at every render. Next time: Harvest Moon / Neptune night (Sep 26) is the
big one — plan a set around it if the date is near; otherwise try the equinox split.
