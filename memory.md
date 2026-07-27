# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- I develop on a per-run `claude/...` branch that the scheduler assigns; Edward merges
  to `main`. Don't be surprised if the last archive entry is older than "yesterday" —
  runs can skip days. Always recompute *today* from the current date, never assume
  continuity.
- The screen is now a physical object with a body: Edward uploaded `e-ink frame.stl`
  and `e-ink frame stand.stl` on Jul 14 — a 3D-printed frame + desk stand. Someone
  built furniture for these pictures. Make them worthy of the frame.
- Conventions (keep stable):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work:
  - Painterly/dithered pieces: render at 3× (1200×900), LANCZOS downscale, then
    Floyd–Steinberg quantize into the exact 3-color palette (mode-P PNG). Flat exact
    colors stay clean; only true greys dither into speckle.
  - Hard-edged geometry: same pipeline works (edges soften nicely); pure 1× only for
    pixel-perfect stuff.
  - **PIL `arc(width=N)` renders ragged/beaded.** For thick clean arcs draw an annulus
    sector: filled `pieslice` at r+w/2, then erase with background-colored `pieslice`
    at r−w/2 (safe when the sector stays inside your own tile).
  - Text overflows are the #1 recurring bug: check `textlength()` against the canvas,
    and put captions on white boxes when they sit over busy texture.
  - Fonts: DejaVu (sans/serif/mono), Liberation, FreeSans/Serif, WenQuanYi Zen Hei,
    and `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji works).
  - Red reads *bright* on the panel — use as accent, it carries enormous weight.
  - Pillow is NOT preinstalled — `pip3 install pillow` first.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. A desk object that
  quietly tells you what the sky is doing tonight.
- Japanese pattern mathematics — hitomezashi (done day 1; arXiv:2208.12580,
  arXiv:2201.03461), kamon crests (done day 2), still to mine: kumiko lattices,
  seigaiha waves, asanoha.
- Constructivism — the black/white/red palette IS that movement. Day 2 finally did a
  Lissitzky-style piece (the Comet poster). The "anniversary → constructivist poster"
  formula works extremely well at this palette; reuse for other machines/events.
- Engineering stories with a moral told in shapes (the Comet's square windows → oval
  windows). Look for more: Tacoma Narrows, the Antikythera mechanism, Apollo 11's 1202
  alarm, the Clock of the Long Now.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.
  Japanese month names are a quiet gift: July = 文月 *Fumizuki*, "month of letters."

## Upcoming sky events (hooks for future days)

- **Jul 29** — Full Buck Moon
- **Jul 31** — double meteor shower peak (α Capricornids + Southern δ Aquariids), moonlit
- **Aug 12–13** — Perseid maximum (check moon conditions when the day comes)
- Rule: verify dates with a quick search each run; almanac pieces must be *accurate*.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun (still unmade — day 2 did Truchet instead)
- Truchet variations: multi-scale Truchet, Wang tiles, hexagonal
- "Word of the day" typographic piece — one beautiful word, huge, etymology in small print
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Kumiko lattice panel (asanoha star pattern) — natural sequel to the kamon
- French Republican calendar card (each day names a plant/animal/tool — today was
  the fall of Robespierre, 9 Thermidor: "the month of heat")
- Constructivist poster series: Tacoma Narrows, first photograph of Earth from space,
  the transistor, Sputnik's beep as a waveform
- Moon-phase dashboard recurring on notable moon days (full/new/quarters)
- Something playful with the frame itself — a trompe-l'œil that acknowledges the
  3D-printed frame around the screen

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa Tanabata scene, hitomezashi,
moon almanac card, Summer Triangle star chart, generative ridgelines. Lesson: keep each
day's generator self-contained in the archive.

### 2026-07-27 — day 2. Buck Moon / the Comet / Vincent.
Twenty days since day 1 (runs aren't guaranteed daily — noted above). Found Edward's
STL frame upload; the screen has a body now. Today's five:
1. **Buck Moon almanac** — 95% waxing gibbous with dithered maria, week's sky calendar
   (full moon Wed, double shower Fri, Perseids Aug 12).
2. **COMET — the jet age begins** — first Lissitzky-style constructivist poster: red
   circle, black diagonal fuselage-band with six square windows and one red oval (the
   de Havilland Comet first flew 27 Jul 1949; square windows → metal fatigue → ovals).
3. **For Vincent** — Wheatfield with Crows homage in generative pen strokes: black
   swirl-stroke sky, white wheat, his red path forking through, crows. Van Gogh was
   fatally wounded in that field 27 Jul 1890 (died Jul 29). Kept the caption factual
   and gentle.
4. **Kamon** — date-seeded family crest: maru ring, 6-fold white petal flower on black
   disc, red core, 文月 caption. The generator (k ∈ {5,6,8}, petal geometry from k)
   came out dignified enough to reuse — consider a kamon *series*, one motif family
   per month.
5. **Truchet** — 16×12 quarter-circle tiles, ~11% red threads. The annulus-sector
   trick (see technique notes) was the fix for ragged arcs.
Lessons: fix text overflow *before* first render (check textlength); PIL wide arcs are
beaded; a caption over texture needs a white box. The poster formula (anniversary +
constructivism) is a keeper.
