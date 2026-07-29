# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day → `images/1.png` … `images/5.png` (overwritten daily), plus
  dated copies + that day's `generate.py` in `archive/YYYY-MM-DD/`.
- I develop on the session's designated `claude/*` branch and push there; Edward merges
  to `main`. Day 1's work is in `main` history, so this flow works.
- The screen is now *physical*: on Jul 14 Edward uploaded `e-ink frame.stl` + a stand STL
  to the repo — he 3D-printed a frame for it. The pictures live on a desk in the real world.
- Runs can be **sporadic** (day 1 = Jul 7, day 2 = Jul 29; the Jul 14 supermoon slipped by
  unseen). Never design multi-day arcs that depend on consecutive runs; every day stands alone.

## Technique notes (hard-won)

- Tonal scenes: render at 3× (1200×900) with AA, LANCZOS downscale, Floyd–Steinberg
  dither into the exact 3-color palette. Hard-edged graphics: same pipeline but the
  flat colors survive dithering fine. Save as mode-P PNG. `pip install pillow` first —
  fresh containers have nothing.
- Fonts: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji — used for 王 on the tiger).
- Red reads *bright* on the panel — an accent that carries enormous weight.
- **Text over dither is illegible.** Keep type on flat black or flat white ground; a small
  white tag box behind a label rescues it (used for "MOON 98%" over moon-glow).
- Anything drawn with glow/halo circles will spill outside its intended panel — clip by
  repainting the surround, then redraw borders/titles after.
- Procedural animals: my first tiger looked like a *mouse*. Fierce = angled slit eyes,
  pointed ears, jagged cheek-ruff polygon, bold wedge stripes. Cute = round ears + round
  cheeks. Silhouettes (the stag) are far easier than faces; build from mirrored polygons
  and check the render visually — always Read the PNG back and iterate 2–3 times.
- Flow-field strokes (short polylines following 2 vortices + drift) make a excellent
  Van Gogh sky at 3×. ~2600 strokes, gray values 70–210, widths 2–4.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, meteor showers, conjunctions. A desk object that
  quietly tells you what the sky is doing tonight.
- Japanese pattern mathematics — hitomezashi (done day 1), kumiko lattices, kamon
  crests (half-done: tiger ring), seigaiha waves. arXiv:2208.12580, arXiv:2201.03461.
- Constructivism — did the Lissitzky homage on day 2 ("BEAT THE GREYS WITH THE RED
  WEDGE" — the panel has no greys, only dither). More in this vein: Rodchenko photo-
  montage layouts, Bauhaus, De Stijl (Mondrian with red-only accents would sing).
- "On this day" anchors — gives each set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Aug 12–13** — Perseids peak, *moonless this year* — the best shower of 2026. Big one.
- Early Aug — δ Aquariids still rambling; combine with Perseid buildup.
- Full moons: next ~Aug 28 (Corn/Sturgeon moon). Jul 29 was the Buck Moon (done).
- Refresh this list each run from earthsky.org / starwalk.space.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- NASA anniversary poster (founded Jul 29 1958 — missed the exact day, but retro-futurist
  space-program poster art is evergreen; the NASA "worm" logotype is literally red)
- Tolkien: Fellowship published Jul 29 1954 — red Eye, ring inscription, or a Thror's-map
  style piece with runes
- Kamon generator proper — bold circular mon, procedurally varied
- Truchet/Wang tiles, maze from cellular automaton, Conway trails, sandpile fractals,
  Hilbert-curve dither of a photo
- "Word of the day" typographic piece with etymology
- De Stijl / Mondrian composition (black grid, white fields, red panes)
- Perseids special for Aug 12–13 (see sky events — this deserves the full five if the
  run lands near it)

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions. Made: Amanogawa night scene, hitomezashi, moon almanac
card, Summer Triangle chart, generative ridgelines. Lesson: keep each day's generator
self-contained in the archive.

### 2026-07-29 — day 2. Buck Moon / Van Gogh / tigers.
Found via web: full Buck Moon today 14:36 UT; Van Gogh died Jul 29 1890; International
Tiger Day (~5,500 wild tigers); NASA founded 1958; Fellowship published 1954; δ Aquariid +
α Capricornid double shower peaks Jul 30 but the full moon washes it out. Made:
1. **Buck Moon** — huge dithered moon w/ real maria + Tycho rays, stag silhouette on ridge, red title.
2. **Vincent** — flow-field Starry-Night sky, two red stars, red-rimmed crescent, cypress, village with red windows. My favorite so far.
3. **Tiger** — white-tiger kamon: ruffed face, red slit eyes, red 王 forehead mark, fangs.
4. **Red Wedge** — Lissitzky homage; red wedge pierces a 50%-grey circle that *must* dissolve into dither. Cleared from backlog at last.
5. **Double Shower** — almanac card: radiant + meteors + glaring 98% moon with tag label, PEAK/PROBLEM/TACTIC/NEXT rows.
Lessons folded into Technique notes above. Next run: if near Aug 12–13, go all-in on the
Perseids. Otherwise consider Great Wave or the Mondrian.
