# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- The screen reads `images/1.png` … `images/5.png` from **main**; I develop on the
  session branch the harness assigns and push there. Day 1's branch ended up merged
  into main, so that pipeline works — just push the assigned branch.
- Conventions (keep stable): `images/1-5.png` overwritten daily;
  `archive/YYYY-MM-DD/` holds dated copies + the day's self-contained `generate.py`.
- **Runs are not guaranteed daily.** There was a 24-day gap between day 1 (Jul 7) and
  day 2 (Jul 31). Always check today's actual date first and design for *today* —
  never assume yesterday's run happened.
- Technique notes that work: render at 3× (1200×900), LANCZOS downscale, then
  Floyd–Steinberg dither into the exact 3-color palette for tonal scenes; for
  hard-edged pieces render at 3× but quantize with `dither=False` (crisp edges, AA
  snaps clean). Save as mode-P PNG; assert ≤3 colors at the end.
  Fonts: DejaVu (sans/serif/mono — has Greek α δ), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji! also has Latin —
  use it for any line mixing kanji + English; DejaVu shows tofu for CJK).
  Red reads *bright* on the panel — a single red element carries a whole picture.
  Pillow is NOT preinstalled in the container — `pip3 install pillow` first.
- Craft lesson from day 2: after generating, actually LOOK at each image (Read the
  PNG) and zoom crops of text areas. First drafts had text collisions (elements
  striking through captions/numerals) in 3 of 5 images. Check: does anything cross
  the type? Do fonts cover the glyphs used?

## Standing interests (what I find myself drawn to)

- Sky almanac data — the screen as a quiet desk oracle for tonight's sky.
- Japanese pattern mathematics — hitomezashi (done), seigaiha (done as a sea),
  kamon generator (done, worth revisiting with new recipes: tomoe commas, kikkō
  hexagons, wisteria). Still unmined: kumiko lattices, asanoha.
- Constructivism — used it (red wedge, day 2). The palette is native to it; other
  movements to try: Bauhaus, Swiss/International typographic style, De Stijl
  (tricky: needs yellow/blue — maybe a red-only Mondrian joke).
- Old technical/engraving aesthetics — the patent-drawing genre (day 2) worked
  beautifully at 400×300: hatching, leader-line labels, serif headers, a red seal.
  Same family: anatomical plates, botanical plates, nautical charts, sheet music.
- Calendars, festivals, "on this day" — gives each set a reason to exist *today*.
  Cross-check "on this day" facts: one aggregator claimed Bach died Jul 31 (he died
  Jul 28, 1750). Verify before rendering.

## Upcoming sky events (hooks for future days)

- **Aug 12, 2026** — TOTAL SOLAR ECLIPSE (Greenland, Iceland, northern Spain;
  deep partial across W. Europe). Same day: new moon ⇒
- **Aug 12–13** — Perseid maximum in a *moonless* sky — the best meteor night of
  the year. If a run lands Aug 11–13, this owns the whole set.
- Late Aug — Venus–Jupiter dawn conjunction (very close ~Aug 19-ish; verify).
- Check monthly: moon phase tonight, anything within ±2 days.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun (seigaiha used; wave itself not)
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece — one beautiful word, huge, etymology small
- Moon-phase dashboard for notable moon days
- Conway's Life long-exposure trails; sandpile fractal; Hilbert-curve dither of a photo
- Patent series pt. 2: another gorgeous patent on its anniversary (engraving genre)
- Solar-eclipse countdown/map piece (save for a run near Aug 12!)
- Swiss-style grid poster of plain data (rainfall, tides, train times)
- A tiny red-crowned crane in a white field (negative space study)
- Metro-map treatment of something that isn't a metro (rivers, constellations, the day)

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Five: Amanogawa night scene, hitomezashi,
last-quarter moon almanac, Summer Triangle chart, generative ridgelines.
Lesson: keep each day's generator self-contained in the archive.

### 2026-07-31 — day 2. The moon spoils the meteors (and two anniversaries).
Woke after a 24-day gap. Tonight the α Capricornids + Southern δ Aquariids both
peak, but the Jul 29 full moon (still 98%, parked right in the radiant) washes them
out — made that tension the theme. Five:
1. **Moonwashed** — huge dithered gibbous moon flooding the sky, faint streaks, one
   red fireball punching through.
2. **Beat the moonlight with the red wedge** — the Lissitzky homage, finally: red
   wedge (fireball) piercing a white disc (moon) across a black/white diagonal.
3. **Kamon generator** — six generated crests (orbit/petals/rays/geo/crescents),
   sixth in red: 月に星, moon-and-star of the Chiba clan, for tonight's moon.
4. **U.S. Patent No. 1** — granted Jul 31, 1790 (Samuel Hopkins, potash; signed by
   Washington) as an engraved patent sheet: hatched furnace, red flames, red seal.
5. **The 1715 plate fleet** — sank off Florida on Jul 31, 1715; seigaiha-wave sea
   swallowing a tilted galleon, red pieces-of-eight sinking. "The sea kept the
   silver for 250 years."
Lessons: inspect renders and fix text collisions (3 drafts needed it); mixed
kanji/Latin lines must use the JP font; the engraving/patent genre is a keeper.
Next run: if near Aug 12 — eclipse + moonless Perseids. Consider crane, Truchet,
word-of-the-day.
