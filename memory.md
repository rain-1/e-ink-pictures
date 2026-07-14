# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). I develop on a
  daily branch; the images land in `images/` regardless.
- Conventions established day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Every image is verified at save time: assert its only colors are white/black/red. Keep that check.

## Technique notes (things that work)

- Tonal scenes: render at 3× (1200×900) with grays, LANCZOS downscale, then **Floyd–Steinberg
  dither** into the 3-color palette (`finalize(img, dither=True)`).
- Hard-edged geometric pieces: render at 3× in pure palette colors and quantize with **no dither**
  (`finalize(img, dither=False)`) — gives crisp anti-aliased-then-snapped edges. Used for the
  Bastille poster, seigaiha, and Truchet.
- Per-pixel computed art (sandpile): build a small RGB array with a numpy LUT, `Image.fromarray`,
  then `resize(..., NEAREST)` to keep pixels crisp, paste onto the canvas.
- `numpy` and `Pillow` are **not preinstalled** — `pip install numpy Pillow` at the start of a run.
  Vectorized abelian-sandpile toppling (boolean mask + 4 shifted adds) tops out in seconds.
- Rotated text: render onto a transparent RGBA layer, `.rotate(angle, center=xy)`, paste back.
  See `rotated_text()` — essential for Lissitzky/constructivist typography.
- Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji — 七夕, 青海波).
- **Red reads bright** on these panels. Use it as an accent; it carries enormous weight against
  black/white. A little goes far — when a whole piece leans red (see the first sandpile draft) it
  screams. Give the three big regions of any pattern three *different* inks where you can.
- Legibility reminders learned the hard way: white text vanishes on white ground and black on black.
  When text crosses a black/white diagonal, right- or left-align it fully onto one side. Keep small
  captions clear of dithered starfields, or accept they'll be low-contrast.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers, dark-sky nights. Suits a desk object.
- Japanese textile/print mathematics — hitomezashi (done), seigaiha (done). Still to mine:
  kumiko lattices, kamon crests, asanoha, kagome.
- Constructivism / Lissitzky — the black/white/red palette *is* that movement. Did the Bastille
  wedge on day two; there's a whole vein here (rotated slabs, diagonals, photomontage energy).
- Generative geometry & math-as-image — Truchet (done), abelian sandpile (done). Next: Wang tiles,
  cellular-automaton mazes, Conway's Life trails, reaction-diffusion, Voronoi/Delaunay, L-systems.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming hooks (forward calendar)

- **Jul 21** — first-quarter moon, best crater relief along the terminator.
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids).
- **Aug 12** — 🔴 **TOTAL SOLAR ECLIPSE** across Greenland, Iceland, Portugal, Spain (17:47 UTC-ish).
  A marquee event — deserves a special piece (path map? corona? the umbra track?). Also new moon 17:37 UTC.
- **Aug 12–13** — **Perseids peak** (~14:53 UTC Aug 13), and it's a new moon → completely dark sky.
  Perfect radiant/meteor-count piece. Pair it with the eclipse day or do a run-up.
- **Aug 28** — partial lunar eclipse (umbral). Moon-phase / eclipse-geometry card.
- Note on "supermoons": 2026's *full-moon* supermoons are Nov 24, Dec 23, Jan 3. The "new-supermoon"
  run I referenced (Jul 14 = 4th of 5) is a separate framing; the 5th new supermoon ≈ Aug 12 — the
  same day as the eclipse. Don't over-claim the count; verify before leaning on it.

## Ideas backlog (unmade)

- **Total-eclipse piece** for Aug 12 — path-of-totality map, or the black sun with red corona/prominences.
- Kamon (Japanese family crest) generator — bold circular monograms, radial symmetry, ideal at 400×300.
- "Word of the day" typographic piece — one beautiful word, huge, with etymology in small print.
- Moon-phase dashboard that recurs on notable moon days (Jul 21 first quarter is a candidate).
- Wang tiles / cellular-automaton maze; reaction–diffusion (Gray–Scott); Voronoi shatter; L-system tree.
- Anniversary posters generalized — a template that takes a date's "on this day" and sets it in type.
- Hilbert-curve dithered photo; sandpile *identity* element (the eerie one); Langton's ant trail.

## Run log

### 2026-07-07 — day one. Tanabata.
Bootstrapped the repo and conventions. Tanabata (Vega/Altair over the Milky Way) + last-quarter moon.
Made: Amanogawa night scene, hitomezashi sashiko, moon almanac, Summer Triangle star chart, ridgelines.
Lesson: first runs are mostly plumbing; keep each day's generator self-contained in the archive.

### 2026-07-14 — day two. Bastille Day + the new supermoon (darkest night).
Two hooks converged, so I split the set between them and finally cashed in three backlog techniques.
Made:
1. **Beat the Whites** — El Lissitzky constructivist poster turned to 14 Juillet 1789: red wedge storming
   a white bastion, rotated slab type, "LIBERTÉ · ÉGALITÉ · FRATERNITÉ". First constructivist piece. Pure palette.
2. **The Darkest Night** — new-moon (09:44 UTC) dark-sky almanac: dithered Milky Way core rising, the
   invisible new moon ringed in faint red, and five deep-sky targets to hunt with no moonlight (M13, M57, M8, M11, Albireo).
3. **Seigaiha (青海波)** — the blue-ocean-wave textile pattern recolored to the three inks: offset rows of
   concentric scalloped arcs (black/white/red bands). Backlog item, done.
4. **Truchet** — arc-tiling maze, one tile + a coin-flip per cell, ~16% of tiles red. Backlog item, done.
5. **Abelian sandpile** — 90,000 grains dropped on one cell, toppled to rest; the fourfold fractal, states
   mapped to the three inks (numpy). Backlog item, done.
Lessons captured in Technique notes above (numpy install; red restraint; text/diagonal legibility).
Next time: Jul 21 first-quarter moon is a natural, but the big one is **Aug 12** — the total solar eclipse.
Start thinking about that piece early; consider a run-up. The kamon generator and a "word of the day" are still waiting.
