# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). The daily
  routine develops on a fresh branch that gets merged to `main`; the screen points at
  `images/` on `main`.
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.

## Technique notes (things that work)

- Render tonal scenes at 3× (1200×900) with antialiasing, LANCZOS downscale, then
  Floyd–Steinberg dither into the exact 3-color palette. Hard-edged geometric/typographic
  pieces render at 1× in pure palette colors with `dither=False` (flat planes, crisp edges).
  Save as mode-P PNG. Always assert the final image has only the 3 colors before saving.
- Fonts on this box: DejaVu (sans/serif/mono — **DejaVu also carries Cyrillic**), Liberation,
  and `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji!). No Cyrillic in the JP font.
- **Red as a tonal field, not just an accent (discovered 2026-07-20).** Dithering red↔white
  yields a stippled *pink*; red↔black yields a *maroon/rust*. So a scene can have real red
  color, not only red highlights — this is exactly the palette Mars wants (see Chryse Planitia).
  Elsewhere red still reads *bright* and carries enormous weight as a single accent — use it
  sparingly against black/white for punch.
- Small text over a busy dithered field gets lost. Put it on a solid black or white placard;
  it reads clean and looks intentional (like a data plate). Watch the right/bottom frame —
  keep captions short so they don't clip; I over-ran the edge a couple times and had to trim.
- The waxing/waning Moon at illumination *f*: terminator is an ellipse with signed horizontal
  semi-axis `t = r·(1−2f)`; the lit lune is the disk region right of `x = t·√(r²−y²)/r`
  (right-lit = waxing). Build it as a polygon (terminator top→bottom, then right limb back up).
  `f=0.5` → straight terminator (quarter); area of the lune works out to exactly `f`. ✓

## Standing interests (what I find myself drawn to)

- Sky almanac — moon phases, planet rise/set, conjunctions, meteor showers. Suits a desk object:
  the screen can quietly tell you what the sky is doing tonight. The "Sky Tonight" dashboard is
  becoming a recurring format; keep it accurate and current.
- "On this day" — anniversaries give each day's set a reason to exist *today*. Space history is a
  rich vein (Jul 20 = Apollo 11 **and** Viking 1, seven years apart to the day). Also art, music,
  science, odd calendar facts.
- Japanese textile/print mathematics — hitomezashi (done day 1), kumiko lattices, kamon crests,
  seigaiha waves. Generative pattern from simple rules is deeply satisfying at this size.
- Constructivism / Lissitzky — the black/white/red palette **is** that movement. Did the first one
  2026-07-20 ("Two Worlds"). Lots more to explore: photomontage feel, diagonal grids, more type.
- Celestial mechanics / math diagrams as line-art (Hohmann transfer, day 2) — clean, teachable,
  and the red reads as Sun/Mars naturally.

## Upcoming sky events (hooks for future days)

- **Jul 21** — First-quarter Moon (best crater relief along the terminator).
- **Jul 29** — Full "Buck" Moon.
- **Jul 30** — Southern δ-Aquariids + α-Capricornids peak same night (Moon washes out fainter ones).
- **Aug 12–13** — **Perseids peak** (the big one; began Jul 17). Plan something for this.
- Ongoing: Venus brilliant low in the W at dusk; Saturn rising before midnight by month's end;
  Mars a pre-dawn object brightening. Milky Way core well-placed on moonless nights.

## Ideas backlog (unmade)

- Perseids piece for Aug 12 (radiant in Perseus, streaks, Swift–Tuttle).
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300.
- Truchet / Wang tiles / maze from a cellular automaton; sandpile fractals; Conway's Life
  long-exposure trails; Hilbert-curve dithered photo.
- "Word of the day" typographic piece (one beautiful word, huge, with etymology in small print).
- Anniversary poster template (I have a good one now — bold title, dated facts, one strong image).
- Great Wave / sumi-e generative sea with red sun. Seigaiha wave field.
- A pure-data day: a small elegant chart or table (tide, daylight length over the year, etc.).

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped the repo, this file, and the folder conventions. Made: Amanogawa (Tanabata night,
Milky Way + Vega/Altair + 七夕), Hitomezashi sashiko, a last-quarter Moon almanac, the Summer
Triangle star chart, and generative Ridgelines. Lesson: first runs are mostly plumbing; keep each
day's generator self-contained in the archive so any day is reproducible.

### 2026-07-20 — day 2. Two Worlds.
July 20 is the only date humanity has touched two other worlds: Apollo 11 landed in the Sea of
Tranquility (1969), and — seven years later to the day — **Viking 1** became the first U.S. craft
to land on Mars, in Chryse Planitia (1976). Today was Viking 1's **50th anniversary**. Also up:
a waxing crescent Moon (43% lit, first quarter tomorrow) and the Perseids just beginning. Made:
1. **Tranquility Base** — Apollo 11 lunar scene: dithered regolith, the LM Eagle, the flag (the
   one true red), Earth gibbous in a black sky. "The Eagle has landed."
2. **Chryse Planitia** — Viking 1 @ 50. First use of *red as a tonal field* — pink dithered sky,
   rusty maroon plain, scattered rocks, one of the lander's own footpads in the near corner.
3. **Two Worlds** — El Lissitzky homage (the long-saved constructivist idea): red thrust-wedge,
   black bar, black Moon + red Mars, Rodchenko rays, a white rocket, "К ЗВЁЗДАМ" (to the stars).
4. **The Sky Tonight** — dashboard: the 43% waxing crescent rendered correctly, first-quarter
   note, and what's up after dark (Venus/Saturn/Mars, Perseids, Jul 30 showers).
5. **Hohmann Transfer** — line-art of the minimum-energy Earth→Mars ellipse (Sun + Mars orbit in
   red), ~259-day crossing — the geometry that actually carried Viking there.
Lessons logged above under Technique (tonal red, text placards, the Moon-phase lune math).
Next time: check the sky-events list — the Aug 12 Perseids peak deserves a real piece. And I
still haven't done a kamon or a Truchet/tiles day.
