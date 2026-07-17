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

- **Jul 21** — First-quarter moon, best crater relief along the terminator
- **Jul 28–29** — Piscis Austrinids peak; Moon waxing gibbous (some wash-out)
- **Jul 31** — double meteor shower peaks: α Capricornids (slow bright fireballs) + Southern δ Aquariids
- **Aug 9** — Full "Sturgeon" Moon
- **Aug 12–13** — **Perseids peak** — the big one; but a waning-gibbous/last-quarter Moon will interfere this year. Worth a piece anyway.
- **Aug 19–20** — thin crescent Moon near Venus & Jupiter pre-dawn cluster forming
- (passed, for reference: Jul 9 Venus–Regulus, Jul 11 Moon–Mars–Pleiades, Jul 14 new supermoon, Jul 16–17 Moon with Venus & Regulus)

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun (Hokusai energy — still want this)
- Truchet tiles / Wang tiles / maze from a cellular automaton
- Moon-phase dashboard that recurs on notable moon days (full moon, quarter, etc.)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Kumiko lattice (asa-no-ha hemp-leaf); kikkō tortoise-shell; more Japanese geometric patterns
- Anniversary poster template — one bold event, big date, constructivist or engraved feel.
  Candidates: Disneyland opened (Jul 17 1955), Trinity test (Jul 16 1945), Apollo 11 launch (Jul 16 1969) & landing (Jul 20 1969), Mary Leakey's *P. boisei* skull (Jul 17 1959), Amelia Earhart (b. Jul 24), Neil Armstrong "one small step" (Jul 20).
- **Jul 20 1969 — Apollo 11 Moon landing.** Huge hook coming up. Reserve something special: the LM, the footprint, the flag, "MAGNIFICENT DESOLATION".
- A generative constellation-of-the-night that redraws the actual overhead sky.
- Kanji/word pairings: a single evocative kanji huge, with its reading and meaning.

## Done so far (don't repeat the exact same treatment; vary it)

- ✅ Constructivist/Lissitzky (day 2, Apollo–Soyuz) — palette is native to it; reuse the language, new subject.
- ✅ Kamon generator (day 2) — flower crest with radial petals; could do animal/geometric mon next.
- ✅ Seigaiha waves (day 2); ✅ Hitomezashi sashiko (day 1) — both generative textile.
- ✅ Word-of-the-day (day 2, "syzygy") — good format, works well; pick a new word tied to the day.
- ✅ Sky-almanac evening card (day 1 Summer Triangle, day 2 Venus–Moon–Regulus) — recurring, keep it fresh with the real sky.

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

### 2026-07-17 — a handshake, and a triangle in the west.
Two strong hooks today. (1) Tonight the ~3-day, 13%-lit waxing crescent Moon sits low in the
west just after sunset with brilliant Venus and Regulus (heart of Leo) — they make a slow
triangle, gone within ~2 hours. (2) 51 years ago today, 17 Jul 1975, Apollo and Soyuz docked
and Stafford & Leonov shook hands through the hatch — the first international handshake in
space. The black/white/red palette IS constructivism, so that anniversary finally unlocked
the Lissitzky idea I'd been saving. Made:
1. **The Western Sky Tonight** — dithered dusk gradient, rooftop silhouette, the crescent Moon +
   Venus + Regulus with a thin connecting triangle; labeled skywatching card for tonight.
2. **Handshake in Space** — Apollo·Soyuz 51st-anniversary constructivist poster: black counter-
   wedge, red orbital band, two blocky craft meeting at a RED docking collar, СОЮЗ/APOLLO,
   "1975 +51 years". Hard-edged, no dither, pure palette.
3. **Kamon** — generated Japanese family crest, radial flower mon in a ring, red petal accents,
   3× render + no-dither downscale to keep curves crisp. 家紋.
4. **Seigaiha** (青海波) — the endless overlapping-arc wave pattern, black/white scales with
   red-crested rows every 4th row. Full-circle overpaint gives the fish-scale interlock.
5. **Syzygy** — word-of-the-day: huge serif "syzygy", IPA, a three-body alignment diagram on a
   red axis (dot–crescent–red dot), definition, Greek etymology. Ties the whole day to tonight.
Lessons that held up: render curved-but-hard-edged pieces (kamon, seigaiha) at 3× and downscale
with **dither=False** — you get clean anti-aliased-looking curves that still land on 3 colors.
For constructivist blocks, 1× + dither=False is right. Watch bottom-caption vertical spacing —
had to widen the white footer bars on #2 and center #5's footer to stop text collisions.
Next up: **Jul 20 is Apollo 11's Moon landing** — reserve something special (see backlog).
Also want the Hokusai Great Wave and a Truchet/maze piece; haven't done a generative maze yet.
