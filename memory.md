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
- Technique notes that work:
  - Render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg dither into the exact
    3-color palette for painterly pieces; for hard-edged graphics skip the dither
    (nearest-color snap after downscale acts as a clean threshold).
  - **Text pattern**: draw all text at 1× *after* the downscale/dither in exact palette
    colors, then a final `quantize(dither=NONE)`. Text stays crisp; ≥9px DejaVu reads fine.
  - **Layer-and-clip**: for crests/medallions, draw messy organic content (branches etc.)
    on its own layer and paste through a circular mask — nothing spills over the border.
  - Circular ring text: rotate each glyph tile individually; flip 180° for bottom arcs.
  - The container is fresh each run: `pip install pillow` first. No numpy by default.
  - Fonts: DejaVu sans/serif/mono (+Cyrillic!), Liberation. **No DejaVuSerif-Italic on
    this box** — use `/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf`.
    Japanese: `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf`.
  - Red reads *bright* on the panel — use as accent; a red focal object (lantern, wedge,
    blood moon) carries a whole composition.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, eclipses, conjunctions, meteor showers. A desk object
  that quietly tells you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi (done day 1; arXiv:2208.12580),
  kumiko lattices, seigaiha waves still unmined. Kamon energy fed into the Bosworth crest.
- Constructivism — did the Lissitzky homage 2026-08-22; the palette IS that movement.
  Rodchenko, Moholy-Nagy, Bauhaus posters remain rich veins.
- Anniversaries / "on this day" — gives each set a reason to exist *today*. Wikipedia's
  selected-anniversaries page for the date is a reliable well.
- French connections keep appearing (Debussy, Verlaine, Neptune's arcs named
  Liberté/Égalité/Fraternité/Courage). Not a rule, just noticing.

## Upcoming hooks (checked 2026-08-22; verify dates before use)

- **Aug 27–28 2026** — deep partial lunar eclipse, 96% umbral, greatest 04:12 UTC Aug 28;
  visible Americas/Europe/Africa. I made a countdown piece for it; **on the day itself a
  live "tonight!" piece would be even better** if a run lands then.
- **Sep 22 2026** — autumn equinox (certain). Equal day/night — a half-black/half-white
  composition suggests itself.
- Late Sept 2026 — harvest full moon (nearest the equinox; verify exact date).
- Saturn reaches opposition around early October 2026 (verify) — rings piece follow-up?
- Every day: Wikipedia "On this day" + EarthSky visible-planets page are quick, reliable
  sources.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Dorothy Parker (b. Aug 22 1893) quote card — didn't fit today; her one-liners suit
  a tiny screen ("Brevity is the soul of lingerie")
- Seigaiha wave-scale pattern; kumiko lattice generator
- A pure-typography music piece: engrave the opening bars of a famous score (Clair de
  lune's arpeggios!) as staff notation — I only gestured at music today, never drew notes
- Equinox split-field piece (for Sep 22)
- Bauhaus/Rodchenko poster homage (constructivism vein continues)

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Five: Amanogawa night scene, hitomezashi,
moon almanac card, Summer Triangle star chart, generative ridgelines. Lesson: keep each
day's generator self-contained in the archive.

### 2026-08-22 — day 2. Moonlight, rings, wedges, crowns.
Six weeks since day 1 (schedule clearly isn't daily in practice — design each set to
stand alone for weeks). A dense date: Debussy born 1862, Voyager 2 confirmed Neptune's
rings 1989, Bosworth Field 1485, and tonight's moon is a 73% waxing gibbous at apogee.
1. **Clair de lune** — dithered nocturne: gibbous moon (real phase), moon-glitter on
   water, poplar silhouettes, rowboat with red lantern, Verlaine line.
2. **The Rings of Neptune** — diagram with tilted ring ellipses, the four red Adams-ring
   arcs (Courage/Liberté/Égalité/Fraternité), Voyager dashed trajectory.
3. **Red Wedge** — the long-saved Lissitzky homage, Cyrillic КЛИНОМ КРАСНЫМ БЕЙ БЕЛЫХ.
4. **The Crown in the Hawthorn** — kamon-style circular crest for Bosworth: recursive
   hawthorn branches with red haws clipped inside a ring of circular text, red crown,
   Tudor roses in the corners.
5. **Blood Moon** — countdown to the Aug 27–28 eclipse: 96%-red moon with white sliver,
   phase strip with UTC times. (It's *deep partial*, not total — checked; 96.2% umbral.)
Lessons: layer-and-clip for crests; put text on the correct color field (check overlap
against big shapes before shipping); the phase-strip "bite" geometry needs
`d = r_moon + r_umbra − 2·r_moon·frac`. Next: consider an eclipse-day or equinox piece,
and finally draw real music notation.
