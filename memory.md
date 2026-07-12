# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`; I push to a
  `claude/...` work branch each run and Edward merges to `main`).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Runs are not guaranteed to be strictly daily (there was a gap Jul 8–11) — design every
  set to stand alone, and never write "yesterday" into an image.

## Technique notes that work

- Tonal scenes: render at 3× (1200×900) with AA, LANCZOS downscale, Floyd–Steinberg
  dither into the exact 3-color palette. Hard-edged geometric pieces: 1×, pure palette,
  no dithering. Save as mode-P PNG.
- Fonts on this box: DejaVu (sans/serif/mono), Liberation, Noto, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji).
- Red reads *bright* on the panel — use as accent; it carries enormous weight.
- **Always fit-check text**: measure with `dr.textlength()` and shrink/reposition BEFORE
  drawing (day 2 bug: drew first, patched after — left ghost text at the edges).
- In multi-panel generators, force variety explicitly (pass style per panel) instead of
  trusting random seeds — six random kamon came out five-of-a-kind.
- 3D wireframes dither beautifully: draw far edges in ~185-gray 1px (dithers to sparse
  dots = depth), near edges black ~1.6px. Geodesic sphere = icosahedron subdivided,
  vertices renormalized to the sphere, orthographic projection.
- Pillow isn't preinstalled in the fresh container — `pip install pillow` first.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. The screen can quietly
  tell you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi (done day 1), kamon (done day 2);
  still to mine: kumiko lattices, seigaiha waves, asanoha.
- Constructivism / Lissitzky — the black/white/red palette IS that movement. Still saving it
  for a day that deserves it.
- Calendars, festivals, "on this day" — July 12 turned out to be a birthday strange-attractor
  (Caesar 100 BC, Thoreau 1817, Fuller 1895, Neruda 1904). Good days are hiding everywhere.
- One-line / constrained drawing systems — the Etch A Sketch piece (single continuous
  H/V self-avoiding line) was the most fun today. Constraints = character.

## Upcoming sky events (hooks for future days)

- **Jul 14** — New supermoon (4th of 5 in a row!), 09:44 UTC — best Milky Way night of the month
- **Jul 21** — First-quarter moon, best crater relief
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids)
- **Aug 12–13** — Perseids peak, and the 5th new supermoon lands right on it → could be an
  exceptional dark-sky Perseid year. Verify closer to the date; deserves a big piece.
- Ongoing this month: Venus near Regulus (W, evening); Mars closing on Aldebaran (dawn).

## Ideas backlog (unmade)

- Lissitzky-style constructivist composition ("beat the whites with the red wedge" energy)
- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Neruda ode: an "Ode to Common Things" style piece — one common desk object drawn huge
  and reverent with three lines of ode (his birthday was Jul 12; works any day)
- Moon-phase dashboard that recurs on notable moon days
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Kumiko lattice panel (asanoha / hemp-leaf geometry)
- More one-continuous-line systems: TSP art (dithered image → traveling-salesman tour),
  single-line spiral portraits
- Etch-a-sketch style could return as an occasional "doodle" format — different walk rules

## Run log

### 2026-07-07 — first day. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa night scene, hitomezashi,
moon almanac, Summer Triangle chart, generative ridgelines. Lesson: keep each day's
generator self-contained in the archive.

### 2026-07-12 — the birthday cluster.
Woke after a 4-day gap (runs aren't daily — noted above). July 12 births: Julius Caesar,
Thoreau, Buckminster Fuller, Neruda; Etch A Sketch went on sale Jul 12, 1960; new
supermoon T-minus 2 days. Made:
1. **Geodesic** — Fuller birthday: freq-4 geodesic sphere wireframe (gray back-edges dither
   into depth), red sun on the horizon, "Spaceship Earth."
2. **Walden** — Thoreau birthday: dithered dawn, pine silhouettes, the one-room cabin,
   red sun with broken red reflection on the pond. "Simplify, simplify."
3. **Kamon sheet** — backlog item done: six invented family crests, n-fold radial symmetry
   (petal/geo/ring styles forced for variety), the fifth printed in red. 家紋六種.
4. **Almanac** — waning crescent with earthshine dots, NEW SUPERMOON countdown, event rows.
5. **Etch A Sketch** — 66 years since it went on sale: red frame, white knobs, and one
   continuous self-avoiding H/V line (straight-bias) filling the gray screen like a maze.
Lessons folded into Technique notes. Next time: Jul 14 is THE supermoon/Milky Way day —
consider making the whole set nocturnal, or finally spend the Lissitzky idea on it.
