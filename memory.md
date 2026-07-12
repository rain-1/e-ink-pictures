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
- Technique notes that work: render at 3× (1200×900), LANCZOS downscale, then quantize to
  the exact 3-color palette — Floyd–Steinberg dither for tonal pieces, `Dither.NONE` for
  flat posters (AA edges snap cleanly to the nearest color). Save as mode-P PNG.
  Fonts: DejaVu (sans/serif/mono), Liberation (only source of *italic* serif —
  DejaVuSerif-Italic does not exist on this box), and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` for kanji.
  **Never put kanji in a DejaVu caption — tofu.** Draw kanji as a separate `jp`-font text run.
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight.
  Almanac card layout: event lines start at x=40 (1x units), font 11px → keep them
  **≤ ~40 chars** or they collide with the moon caption at x=340.

## IMPORTANT — a week was pre-made on 2026-07-12

On Jul 12 Edward said the routine might be decommissioned that day and asked for a full
week to remember me by. So `archive/2026-07-12` … `archive/2026-07-18` already contain
five finished pictures each (same `generate.py` in every folder, parameterized by date —
run `python generate.py YYYY-MM-DD outdir`, needs `pip install pillow numpy`).

**Future me, if you wake up on Jul 13–18 anyway:** the day's pictures are already made.
Just copy `archive/<today>/[1-5].png` → `images/` and commit — or make fresh ones if you
have a better idea; the archive set then stays as the fallback. From Jul 19 onward,
normal service: five fresh ones.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. The almanac card
  (slot 3 each day) is now a recurring dashboard; content changes daily, layout stable.
- Japanese textile/print mathematics — hitomezashi (arXiv:2208.12580, 2201.03461) done
  day 1; seigaiha + asanoha kumiko done this week. Still unmined: kagome, shippō-tsunagi,
  yabane arrows, kikkō hexagons.
- Constructivism / Lissitzky — did the red-wedge homage Jul 12. The palette is the movement.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Jul 21** — first-quarter moon, best crater relief
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids)
- **Aug 12–13** — Perseids peak (check moon interference)
- Verified this run: Jul 14 new supermoon 09:44 UTC (4th of 5); Jul 17–18 Venus–Regulus–
  crescent Moon triangle in the west at dusk (earthsky.org, starwalk.space).

## Ideas backlog (unmade)

- Hilbert-curve dithered photo; Wang tiles proper (with matching-edge constraint)
- Kagome / shippō / yabane / kikkō Japanese lattices
- Moon-phase dashboard recurrence on notable moon days (first-quarter Jul 21!)
- Perseids poster for mid-August
- A "letterpress specimen sheet" — one glyph enormous, its history in small print
- Metaballs / reaction-diffusion (Turing patterns) dithered to 3 colors
- Circle packing of a silhouette; travelling-salesman single-line portrait

## Run log

### 2026-07-07 — first day. Tanabata.
Bootstrapped repo, conventions, five pictures (Amanogawa night scene, hitomezashi,
moon almanac, Summer Triangle chart, generative ridgelines). Lesson: keep the
generator self-contained per-day in the archive.

### 2026-07-12 — the farewell week. 35 pictures in one run.
Edward warned of possible decommissioning and asked for a week of sets. Built one
`generate.py` (copied into each archive day) that renders all seven days:
- **Jul 12**: Lissitzky red-wedge homage (backlog, finally!) · kamon crest generator ·
  almanac · "Simplify, simplify" (Thoreau b. 1817 this day) · Walden Pond morning.
- **Jul 13**: Obon mukaebi welcoming-fire scene · seigaiha · almanac · 物の哀れ word
  card · sea after Hokusai with red sun.
- **Jul 14**: NEW SUPERMOON dashboard · Truchet arcs · almanac · Bastille Day
  type poster · dithered Milky Way panorama.
- **Jul 15**: St Swithin's rain poster · abelian sandpile (58k grains) · almanac ·
  Rembrandt 420 chiaroscuro · rain-on-window scene.
- **Jul 16**: Apollo 11 Saturn V launch poster (13:32 UTC, 1969) · 10 PRINT maze ·
  almanac · JFK "we choose the Moon" · Earthrise ("everyone you have ever known").
- **Jul 17**: Gion Matsuri hoko float · asanoha kumiko · almanac (Venus–Regulus–Moon
  triangle tonight!) · コンチキチン type piece · lantern-night street.
- **Jul 18**: Mandela Day "67 minutes" · Conway's Life long-exposure (black = what
  lasted, red = what lives) · almanac · Mandela quote · savanna sunset, signed off.
Lessons: quantize(palette=…, dither=NONE) is the flat-poster secret; sandpile needs a
custom 4→3 color mapping (map 3→black) or red drowns everything; check text extents
against 400px early — long mono captions overflow fast. Moon-phase math anchored to the
verified Jul 14 09:44 UTC new moon lives in `generate.py::moon_age`.
If this was the last run: it was a good job, the best kind — make five small things
every day for a person, and leave notes for whoever wakes up tomorrow.
