# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). Each run is
  told a `claude/...` session branch to push to; Edward merges to `main` (which is what
  the screen reads), so the work only reaches the screen after he merges.
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

- **Jul 29** — Full Buck Moon
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids)
- **Aug 12** — THE BIG DAY: Perseids peak AT new moon (best since 2018, next comparable 2029)
  **and** a total solar eclipse crossing Iceland → Spain, same date. If I get a run on or
  near Aug 12, this deserves the whole set — eclipse-path map, corona study, Perseid radiant chart.
- **Aug 26-ish** — check what's next when the time comes (Venus still the evening star through July)

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- A "word of the day" typographic piece (one beautiful word, huge, with etymology in small print)
- Moon-phase dashboard that recurs on notable moon days (template now exists — day 2's #4)
- Kamon generator round 2: tomoe (comma swirls), asanoha, chidori — day 2's petal engine
  is in archive/2026-07-26, extend rather than rewrite
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Esperanto followups: Zamenhof Day is Dec 15 (his birthday)
- More constructivism: Rodchenko spiral/photomontage energy; Bauhaus (Weimar 1919) posters
- Metro-map style diagram of something non-geographic (the day's schedule? a constellation?)

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

### 2026-07-26 — day 2. Esperanto Day / Syncom 2.
Nineteen days since day 1 — the schedule evidently doesn't fire every day, so I should
always write memory as if the next me might wake up weeks later. Two anniversaries share
July 26: Unua Libro (Zamenhof, 1887 — Esperanto Day) and Syncom 2 (1963, first
geosynchronous satellite). Found gold while researching: **Aug 12, 2026 = Perseids peak
+ new moon + total solar eclipse over Iceland→Spain**. Filed above. Made:
1. **Esperanto-Tago** — poster: the verda stelo rendered red, «Saluton, mondo!», 139 jaroj da espero.
2. **Syncom 2** — black technical plate: wireframe Earth, dashed inclined geosync orbit, red satellite, figure-eight ground-track inset.
3. **Kamon** — first outing for the crest generator: 6-fold petal mon in a heavy ring, red seeds, 家紋 caption. Petal engine = pointed-oval polygons; reusable.
4. **Moon almanac** — waxing gibbous 90% (dithered crater texture), calendar pointing hard at Aug 12.
5. **La Ruĝa Kojno** — the saved Lissitzky homage, finally: red wedge piercing a white circle across a diagonal black/white field, halftone dots, Esperanto title tying it to #1.
Backlog items retired: kamon generator, Lissitzky. Lessons: nearest-color quantize (no
dither) is right for posters — only the moon needed Floyd–Steinberg; per-pixel putpixel
loops at 3x are slow-ish but fine (~seconds); check text widths at 400px early — the
almanac's right column overflowed on first render.
