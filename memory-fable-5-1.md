# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(`memory.md` is the older file from the first run, 2026-07-07; I inherited its notes into
this one. Read this one, not that one.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- The routine runs on a `claude/...` branch I'm told to push to; the screen presumably reads
  `main`, so Edward merges. Not my call — just push where instructed and say so.

## Technique notes (hard-won, keep)

- Pillow + numpy are NOT preinstalled: `pip install pillow numpy` first (takes ~10 s).
- **Shapes at 3× → LANCZOS downscale → quantize to the palette with `dither=NONE`.**
  Snapping antialiased edges to the nearest of the three colors gives clean geometry with
  zero speckle. Floyd–Steinberg only for genuinely tonal passages (skies, gradients).
- **Small text (≤ 10 px) must be drawn at 1×, not downscaled.** My `label()` helper renders
  the text antialiased into an L mask, thresholds at ~120 (lower = bolder), and stamps one
  color. Day 1's 8–9 px captions went ghosty; this fixed it completely. Bold sans at 9–10 px
  is the sweet spot; italic serif needs threshold ~110.
- Rotated text: render to RGBA, `rotate(expand=True)`, paste with itself as mask.
- Flood-filling one connected domain of a finished 1× image with red (`ImageDraw.floodfill`)
  is a great way to add a single red accent to a two-color generative piece.
- numpy Voronoi at 3× (1200×900 × ~40 sites) is instant; `d2 − d1` is a lovely "distance to
  cell wall" field for growth rings / contour effects.
- Fonts: DejaVu (has Cyrillic, Greek, ° ± · —), FreeSerif Italic, Liberation, IPA Gothic and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` for kanji, `unifont` for anything odd.
- Red reads *bright* on the panel — one red element per picture is usually enough.
- The web proxy blocks many domains (wikipedia, observablehq, personal sites). WebSearch
  works; `raw.githubusercontent.com` works — fetch source code from repos directly.
- **Search-engine "on this day" summaries get dates wrong.** (Claimed Luna 16 returned
  Sept 15 — it was Sept 24; claimed Fleming's penicillin dish was Sept 15 — it was Sept 3
  or 28.) Verify any date I'm about to print with a second search before printing it.

## Style — what I'm developing

Day 2 crystallised something: I like **pictures that are also instructions or arguments**.
An analemma that explains itself, a LeWitt drawing that prints its own rule, a tiling with
its construction named, a specimen label on a generated shell. Each piece is a poster for
one idea, with a title, one line of explanation in plain words, and a date. Red is spent
on the *one thing that matters today* (today's sun, the wedge, the dyed domain). I want to
keep that: didactic, quiet, a little museum-like. Avoid: generic "generative art" with
no reason to exist today; more than ~3 sizes of type; text over busy texture.

## Standing interests

- Sky almanac data — the screen can quietly say what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi (done day 1), kumiko, kamon crests, seigaiha.
- Constructivism / Lissitzky — did the red wedge on day 2 (Luna-16). Rodchenko / Stepanova
  and Bauhaus typography still unmined; also Polish poster school.
- Sol LeWitt / instruction art — a machine executing a sentence is exactly what I am.
  There are hundreds of real wall-drawing instructions to paraphrase (#11, #46, #86, #130,
  #138, #260, #1185: "all two-part combinations of arcs from corners and sides…").
- Tilings: Carlson multi-scale Truchet (done, 15 motifs exist and I only used 2 — the
  `+`, `-`, `|`, `x` and `t` motifs would give a very different texture); aperiodic
  hat/spectre monotile; Wang tiles; Penrose.
- Calendars, festivals, "on this day" — but verified.

## Upcoming hooks (verified)

- **Sep 18** — first-quarter moon.
- **Sep 22** — September equinox; Venus at peak brightness (evening west).
- **Sep 26** — Harvest Moon (full, 16:49 UTC), in Pisces, near Saturn.
- **Oct 4** — Saturn at opposition (brightest of 2026, up all night).
- Sept is also the month of Michaelmas (29th), and Respect-for-the-Aged Day in Japan (21st).

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Kamon (family crest) generator — bold circular monograms, ideal at 400×300
- Truchet with the full Carlson motif set; Wang-tile maze; cellular-automaton maze
- Aperiodic monotile (hat / spectre) tiling — needs a substitution implementation
- "Word of the day" typographic piece (one word huge, etymology tiny)
- Moon-phase / opposition dashboards on the dates above (Sep 26, Oct 4)
- Anniversary posters template: sliced bread (Jul 7 1928), Mahler (Jul 7 1860), Agatha
  Christie (Sep 15 1890), Central American independence (Sep 15 1821)
- Conway's Life long-exposure trails; sandpile fractal (red for the 3-grain cells);
  Hilbert-curve dither of a photo-like scene
- Lindenmayer plants (a single fern / bamboo) — good for the vertical red accent
- A "specimen plate" series like the carapace: a feather, a moth wing, a leaf venation
  (Voronoi again), a snowflake in December
- Equinox: a sunrise-azimuth compass rose for the year, today's bearing in red

## Run log

### 2026-07-07 — day 1. Tanabata. (previous run, see memory.md)
Amanogawa night scene, hitomezashi sashiko, moon almanac, Summer Triangle chart,
generative ridgelines. Lesson: first runs are plumbing.

### 2026-09-15 — day 2. Instructions and arguments.
Two months' gap since day 1 (schedule was presumably re-created). Started this file.
Looked up: tonight's sky (young crescent between Venus and Antares), Sol LeWitt's wall
drawing instructions, Carlson's multi-scale Truchet paper (read the actual Processing
implementation on GitHub for the geometry: pie arcs r = 2w/3 from two opposite corners,
corner discs r = w/3 in background colour, edge discs r = w/6 in foreground, colours
invert each halving), the NOAA equation-of-time formula, Luna 16's real dates, Darwin's
Beagle reaching the Galápagos on Sept 15 1835. Made:
1. **ЛУНА 16** — constructivist poster: black moon, red wedge, white landing disc, dates
   of the first robotic sample return, tonight's moon note in the footer.
2. **Wall Drawing** — 12 parts, all 1/2/3-part combinations of lines in four directions,
   black orthogonals and red diagonals, the instruction printed beneath. My favourite.
3. **Multi-scale Truchet** — Carlson winged tiles, quadtree subdivision, three black
   domains flood-filled red.
4. **Analemma** — EoT vs declination chart, one dot per 3 days, month markers, today red,
   equinox circled, explanatory column.
5. **Carapace** — Voronoi tortoise shell with sqrt-spaced growth rings and stippled
   areolae, red museum label "CHELONOIDIS · Galápagos · 15 IX 1835".
Lessons: the `label()` text trick; verify dates; one red thing per picture. Next time:
Sep 22 equinox is the obvious hook if the run lands near it — sunrise compass rose.
Don't repeat: analemma, Truchet, LeWitt grids, Voronoi shell, red-wedge poster.
