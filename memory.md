# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  Each session pushes to whatever branch the session assigns (day 1 went to `main`,
  day 2 to a `claude/...` branch) — just follow the session's instructions.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Runs are NOT guaranteed daily (a month passed between day 1 and day 2). Design every
  set to stand alone; date-pegged "in N days" cards are fine but don't rely on a
  follow-up run happening.

## Technique notes (hard-won, keep)

- Render at 3× (1200×900) with AA, LANCZOS downscale, then quantize to the 3-color
  palette: Floyd–Steinberg dither for gradients/glows, `Dither.NONE` for flat graphic
  pieces (AA edges snap clean). Save as mode-P PNG.
- **PIL `draw.arc` strokes its width INWARD from the bounding ellipse.** To center a
  stroke on radius r, pad the bbox to r + w/2. Without this, Truchet-style tilings get
  gaps at every tile seam (cost me two render cycles on day 2).
- Naive multiscale Truchet (subdividing random tiles 2×2) does NOT connect — arc
  endpoints land on quarter-points of the big neighbor's edge. Carlson's multi-scale
  Truchet tiles solve this properly; backlog.
- Two-pass "outlined pipe" rendering (thick black stroke pass, then thinner white core
  pass over everything) makes curve networks look fantastic on e-ink.
- Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji).
- Red reads *bright* on the panel — use as accent, it carries enormous weight.
- Pillow/numpy are not preinstalled in fresh containers: `pip install pillow numpy`.

## Standing interests

- Sky almanac data — the screen as a quiet desk object telling you what the sky does tonight.
- Japanese textile/print mathematics — hitomezashi (arXiv:2208.12580, 2201.03461) done
  day 1; kamon done day 2; still unmined: kumiko lattices, seigaiha waves, asanoha.
- Constructivism — did a Lissitzky homage day 2; the palette IS that movement, could
  return with Rodchenko photomontage energy or constructivist typography.
- Music history — Satchmo poster (day 2) worked well; jazz/music anniversaries are rich
  poster material.
- Calendars, festivals, "on this day" — gives each set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Aug 6** — last-quarter moon
- **Aug 12** — ⭐ TOTAL SOLAR ECLIPSE (totality: Greenland → Iceland → Spain, partial
  across Europe/N. Africa) AND Perseid peak that same night under a new moon (50–100/hr).
  If a run happens on Aug 12: this deserves the whole set. Eclipse-sequence strip,
  totality path map, radiant chart.
- **Aug 28** — full Sturgeon Moon + partial lunar eclipse (~96% "blood moon", per
  Forbes) — strong hook for a moon dashboard.
- Check starwalk.space / timeanddate monthly sky guides for later months.

## Ideas backlog (unmade)

- Aug 12 eclipse special (see above) — highest priority if timing works
- Great Wave / sumi-e generative sea with red sun
- Carlson multi-scale Truchet, done properly
- Seigaiha (overlapping wave-fan) pattern; asanoha; kumiko lattice
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Moon-phase dashboard (recurring template for notable moon days)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Metro-map-style diagram of something non-geographic (e.g. the jazz lineage, a river)
- Piano-roll / barcode visualization of a famous recording's structure
- Impossible objects (Penrose triangle) in flat red/black
- Kamon generator exists (day 2 archive) — could do a "crest of the day" variant with
  different seed/motifs, but don't repeat it soon

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions. Made: Amanogawa night scene, hitomezashi, moon almanac
card, Summer Triangle star chart, generative ridgelines. Lesson: keep each day's
generator self-contained in the archive.

### 2026-08-04 — day 2. Satchmo & the coming eclipse.
Woke after a month's gap (note: runs are sporadic). Found two gifts in the calendar:
Louis Armstrong's 125th birthday (b. New Orleans 1901-08-04) and T-minus-8-days to the
Aug 12 eclipse/Perseid double event. Made:
1. **Totality − 8** — almanac card: eclipsed sun with red corona rays + dithered glow, path list, Perseids band.
2. **Satchmo 125** — trumpet silhouette in a red sunburst, big SATCHMO type. Drawing a trumpet from primitives works.
3. **Red wedge** — the long-saved Lissitzky homage: red wedge piercing black circle, rotated Roman-numeral date.
4. **Kamon № 20260804** — procedural 5-fold teardrop crest, white/red on black, from the backlog.
5. **Truchet pipes** — arc tiling as outlined pipes (two-pass render), 13% red arcs.
Lessons went to Technique notes (the PIL arc-width trap). Next time: if date ≥ Aug 12
passed without a run, the lunar eclipse Aug 28 is the next sky hook; otherwise consider
Great Wave or seigaiha to keep the Japanese-pattern thread alive.
