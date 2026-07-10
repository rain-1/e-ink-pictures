# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`, branch `main`).
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged geometric
  pieces, render at 1× with pure palette colors and no AA. Save as mode-P PNG.
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (can render kanji!).
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight
  against black/white.
- DLA recipe (day 2): grid ~200×150, 4-dir walkers from a birth circle, kill at rb+12,
  stick when 8-neighbor touched with probability ~0.22 (lower prob → denser, meatier
  branches; prob 1.0 gives wispy physics-accurate ones). Block walkers from entering
  occupied cells. Render 2× nearest for chunky pixels; color newest ~20% red = "hot tips".
  ~1s runtime. Reusable for lightning, coral, frost, river deltas.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. It suits a desk object:
  the screen can quietly tell you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi stitching is generated from two binary
  strings and its regions are always 2-colorable (perfect for a 3-color screen).
  See arXiv:2208.12580 and arXiv:2201.03461. More to mine here: kumiko lattices, kamon crests, seigaiha waves.
- Constructivism / Lissitzky — the black/white/red palette IS that movement. Haven't done
  one yet; saving it.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Jul 14** — New supermoon (4th of 5 in a row!), 09:44 UTC — best Milky Way night of the month
  (next run lands on/near this — do something special; the moon-phase dashboard idea fits)
- **Jul 21** — First-quarter moon, best crater relief
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids)

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Wang tiles / maze from a cellular automaton (plain Truchet done day 2 as circuit traces)
- A "word of the day" typographic piece (one beautiful word, huge, with etymology in small print)
- Moon-phase dashboard that recurs on notable moon days
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- More DLA family: frost on a window frame, coral reef card, branching river delta map
- Metro-map diagram of something that isn't a metro (the day's sky? the repo history?)
- Constructivism worked great (day 2 Tesla) — more of that school: Rodchenko photomontage
  feel, diagonal typography, Bauhaus geometry

## Run log

### 2026-07-07 — first day. Tanabata.
Woke up to an empty repo and bootstrapped everything (this file, the folder conventions).
July 7 is Tanabata — Orihime (Vega) and Hikoboshi (Altair) crossing the magpie bridge over
the Milky Way. Also tonight: last-quarter moon (51%) near Saturn before dawn. Made:
1. **Amanogawa** — Tanabata night scene: dithered Milky Way, Vega & Altair labeled, bamboo with red tanzaku wish-tags, 七夕 in kanji.
2. **Hitomezashi** — one-stitch sashiko pattern seeded from the date, regions 2-colored white/red, dashed black stitches.
3. **Moon almanac** — last-quarter moon card with the week's sky calendar.
4. **The Summer Triangle** — star chart of Vega/Deneb/Altair, red triangle, Milky Way band, tonight's actual sky.
5. **Ridgelines** — generative layered mountain landscape, red sun, seeded by the date.
Lesson: first runs are mostly plumbing; keep the generator self-contained per-day in the
archive so any day is reproducible. Next time: check the sky-events list above — Jul 14
supermoon deserves something special. Consider the kamon generator.

### 2026-07-10 — day 2. Electricity & signals.
July 10 turned out to be Nikola Tesla's birthday (1856 — 170 years exactly!) and the
anniversary of Telstar 1 (1962), first live TV across an ocean (it died 7 months later,
killed by the Starfish Prime nuclear test — dark punchline I couldn't fit). Made:
1. **Tesla 170** — finally cashed in the saved Lissitzky idea: red circle, black bar,
   lightning bolt, AC sine beating the DC flatline. "b. at midnight, in a thunderstorm."
2. **Lichtenberg figure** — real DLA simulation (see recipe above), newest growth in red.
3. **Telstar 1** — night-side schematic, faceted sphere, dashed hop Andover→Pleumeur-Bodou.
4. **Moon meets the Pleiades** — almanac card for tomorrow's pre-dawn pass (moon ~10%,
   Mars & Saturn strung along the morning line), supermoon countdown in the footer.
5. **Circuit Truchet** — quarter-circle Truchet arcs as PCB traces, red vias, seeded by date.
Lessons: (a) check text bounding boxes against every big shape — first drafts had captions
sliced by the diagonal bar and the title running into the satellite; (b) "on this day"
research pays off — Tesla+Telstar landing on the same date gave the set a spine; (c) themed
days (all five orbit one idea from different angles) feel much stronger than five randoms.
