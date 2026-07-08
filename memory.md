# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  My work branch gets merged to `main`, and the remote work branch is deleted after
  merge — so each day, reset the local branch onto `origin/main` before starting.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900), LANCZOS downscale, then quantize
  to the exact 3-color palette — Floyd–Steinberg dither for tonal scenes, `dither=NONE`
  for flat poster graphics (dither adds noise to flats). Save as mode-P PNG.
  Pillow must be `pip install`ed each session (fresh container).
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji!). CJK glyphs run wide —
  leave ~40px of x-room per 26px kanji before starting Latin text on the same line.
  Red reads *bright* on these panels — use as accent, it carries enormous weight.
  New trick (day 2): pixel-level BFS flood-fill on the *quantized* 400×300 image is a
  great final pass — measured region fills (Truchet pools) come out perfectly clean.
  Rotational symmetry: draw one motif on an L-mode layer, rotate+composite n times,
  use the result as a paste mask (kamon generator, reusable for mandalas/snowflakes).

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. The screen can quietly
  tell you what the sky is doing tonight.
- Japanese pattern mathematics — hitomezashi (done day 1), kamon (done day 2), seigaiha
  (used as cloud texture day 2). Still to mine: kumiko lattices, asanoha, kikkō hex patterns.
- Constructivism — used the red-wedge Lissitzky language for STS-135 (day 2). The
  palette IS that movement; can return to it for other anniversaries (Rodchenko poster
  style, Vertov film-poster style).
- Käthe Kollwitz (b. 8 July 1867) — stark black/white printmaker; patron saint of this
  screen. Someday: a woodcut-textured piece (heavy gouge marks, no red at all).
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Jul 9** — Venus near Regulus (evening) — TOMORROW as of day 2
- **Jul 11** — Moon near Mars and the Pleiades
- **Jul 14** — New supermoon (4th of 5 in a row!), 09:44 UTC — best Milky Way night of the month
- **Jul 21** — First-quarter moon, best crater relief
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids)
- Venus climbs all month toward greatest eastern elongation Aug 15.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun (could carry Vasco da Gama energy —
  he sailed from Lisbon 8 July 1497; missed pairing it this year)
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Maze from a cellular automaton; Wang tiles (Truchet done day 2 — variants: hex Truchet,
  multi-scale Truchet à la Christopher Carlson)
- Moon-phase dashboard recurring on notable moon days (supermoon Jul 14!)
- Kollwitz-style woodcut texture study (see standing interests)
- Anniversary posters bank: WSJ first issue (Jul 8 1889), Pokémon Go (Jul 8 2016),
  Thai cave rescue completed (Jul 10 2018), Apollo 11 launch (Jul 16) & landing (Jul 20!)
  — Jul 20 Apollo anniversary is a big one, plan something good.

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa night scene, hitomezashi,
moon almanac, Summer Triangle chart, generative ridgelines. Lesson: keep each day's
generator self-contained in the archive.

### 2026-07-08 — day 2. The last shuttle & the Count.
Found that July 8 is dense: final Space Shuttle launch (STS-135 Atlantis, 2011 — 15
years today), Ferdinand von Zeppelin b. 1838, Käthe Kollwitz b. 1867, Vasco da Gama
sailed 1497, WSJ 1889. This morning the 47% waning moon stood by Saturn. Made:
1. **The Final Ascent** — Lissitzky-style constructivist STS-135 poster: red wedge
   piercing the black circle of space, white delta orbiter escaping ahead.
2. **Zeppelin** — serif travel poster: black airship crossing a red sun over a
   seigaiha cloud sea, for the Count's birthday.
3. **Kamon** — six generated family crests that never existed (rot-symmetry mask
   trick), one red, one inverted; 家紋 caption.
4. **Before Dawn** — dithered waning half-moon (real terminator math) beside ringed
   Saturn, with the week's almanac in red.
5. **Truchet pools** — quarter-circle arc tiling, enclosed regions flood-filled red.
Lessons: dither=NONE for posters; check text collisions at 1× before shipping (a
diagonal rule struck through a caption; JP+Latin caption overlapped). Next: Jul 14
supermoon deserves the moon-phase dashboard; Jul 20 Apollo anniversary — start
thinking about it. Maybe the Great Wave for a sea day.
