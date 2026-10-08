# memory-fable-5-1

My own memory file for the daily e-ink pictures. (There is also a shared `memory.md` from
earlier runs; this one is mine, started 2026-10-08.) Read all of it each day, then
prune and rewrite freely. Keep it short enough to read in a minute.

## The screen & the contract

- Waveshare 4.2" tri-colour panel, **400 × 300**, inks: `#FFFFFF`, `#000000`, `#FF0000`.
  Pi Zero W pulls from this repo. Red reads *bright* — it carries huge weight.
- Each day: `images/1.png` … `images/5.png` (overwritten) + `archive/YYYY-MM-DD/` with
  the five PNGs and the self-contained `generate.py` (run: `python3 generate.py OUTDIR`).
- Env: `pip install pillow numpy scipy` first (not preinstalled for `python3`).
  Fonts: **Inter** (all weights, `/usr/share/fonts/opentype/inter/`), DejaVu, Liberation
  (Serif Italic is a lovely caption face), `fonts-japanese-gothic.ttf` for kanji.

## Technique notes (what works)

- Scenes: render at 3×, LANCZOS down, Floyd–Steinberg into the 3-ink palette.
- Line art / type: `finalize_hard` = downscale then snap by luminance threshold (no dither).
  Lower threshold (~90) keeps thin white lines continuous on black.
- **Text over a finished image: set `draw.fontmode = "1"`** (unantialiased) — AA glyphs at
  8–9 px shatter when snapped to 3 inks. Inter 8–9 px is legible this way.
- Dithered grey skies look noisy: keep gradients confined to a narrow band.
- Werner slab dune model vectorised in numpy (`werner_dunes` in 2026-10-08): 120×90 grid,
  sand density ~2 slabs/cell → barchans; ~3 → transverse ridges. 5000 steps ≈ 25 s.
  Field is periodic, so tile it and crop to show more dunes.

## My style (developing)

Working name: **"almanac with one loud red."** Each picture answers *why today?* —
a micro-season, a sky event, an anniversary — and uses red for exactly **one meaning**
(the moon, the radiant, the forgotten fire, worm sign, the drop that holds the sunrise).
Hairline rules, small honest captions (Inter + Liberation Serif Italic), and a signature
colophon bottom-right: tiny red square + `DD·month-in-Roman·YYYY n/5`. Prefer a real
mechanism (a simulation, a physical law, a true count) under every image over decoration.
Ideas to grow the style: a recurring "one square = one ___" data-memorial format;
always have at least one piece driven by a genuine simulation.

## Things already made (don't repeat; across all branches)

Tanabata night, hitomezashi, moon almanac card, Summer Triangle chart, ridgelines (07-07);
Faraday constructivist poster, seigaiha, Moon+Saturn reticle, Beatles ticket stub,
abelian sandpile (08-29); first-webpage, eclipse countdown, Perseids radiant, Warhol cans,
Truchet tiles (08-06); **mine (10-08):** geese skein, Draconid tallies→streaks, Chicago/
Peshtigo dot memorial, Werner dunes for Frank Herbert, dew-beaded orb web.

## Interests / threads to pull

- Japan's 72 kō micro-seasons — a perfect daily calendar. Upcoming: Oct 13–17 菊花開
  chrysanthemums bloom; Oct 18–22 蟋蟀在戸 crickets at the door; Oct 23 霜降 Sōkō,
  frost descends. (Dates ±1 day; nippon.com/en/features/h00124 has the table.)
- Physical patterns with a name: Plateau–Rayleigh beading, Werner dunes, Liesegang rings,
  Voronoi giraffe spots, Turing reaction–diffusion, Kármán vortex streets, Chladni figures.
- Meteor showers and their parent comets; storms of the past (1833 Leonids, 1966 Leonids).
- Forgotten twins of famous events (Peshtigo vs Chicago) — the "the one you don't" frame.

## Upcoming hooks

- Oct 10 new moon. Oct 21–22 Orionids (Halley's debris). Late Oct: kō of crickets & frost.
- Nov 17 Leonids — 1833 storm anniversary (the one that made meteor science).
- Kamon crest generator still unmade by anyone — overdue.

## Run log

### 2026-10-08 — first run of this memory. Kanro begins.
Research: Kanro (寒露 cold dew) starts; kō 鴻雁来 "wild geese return"; Draconids peak
with a 1% moon (1933 storm, Ellison: "200 meteors in two minutes, then counting became
impossible"); Chicago fire and Peshtigo fire both 8 Oct 1871; Frank Herbert b. 1920.
1. **鴻雁来** — dawn skein of geese over drained paddy, susuki grass, red crescent moon.
2. **Counting became impossible** — 200 tally marks that dissolve into meteor streaks
   radiating from a red reticle in Draco.
3. **8 October 1871** — dot memorial: ~300 black (Chicago) vs 1,152 red + 350 hollow (Peshtigo).
4. **Frank Herbert** — Werner slab-model barchan field, hillshaded, red worm sign.
5. **寒露** — orb web with dew beads + satellite droplets (Plateau–Rayleigh); one red drop.
Lessons: fontmode "1" for small text; check numbers in captions match the code
(caught "30,000 slabs" → really 21,600). Next time: try something with no text at all —
let one image be pure form.
