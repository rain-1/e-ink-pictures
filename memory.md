# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Each daily run develops on a fresh routine branch (e.g. `claude/…`) and is committed there;
  the live `images/` on the main line are what the screen points at. Keep both in sync each run.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged geometric
  pieces (constructivism, Truchet arcs, typography), render at 1× (or 3× with **dither off**)
  in pure palette colors — dithering line art just speckles the edges. Save as mode-P PNG.
  Always assert the final image has ≤ {white, black, red} before shipping — I do this in the script.
  Fonts on this box: DejaVu (sans + sans-bold, serif + serif-bold, mono), Liberation
  (has the italics DejaVu lacks — e.g. `LiberationSerif-Italic.ttf`), and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (can render kanji!).
  NB: DejaVu ships **no** serif-italic — reach for Liberation for italics.
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight
  against black/white. A little red goes a long way.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. It suits a desk object:
  the screen can quietly tell you what the sky is doing tonight. A present-tense "look
  west tonight" card has become a recurring, reliable slot.
- Anniversaries & "on this day" — gives each day's set a reason to exist *today*. Founding
  days, first flights, births of composers/scientists. Pairs well with bold typography.
- Japanese textile/print mathematics — hitomezashi stitching (2-colorable regions, perfect
  for us; arXiv:2208.12580, 2201.03461). Still to mine: kumiko lattices, kamon crests, seigaiha waves.
- Generative geometry — Truchet/Wang tiles, mazes, cellular automata, sandpiles, curves.
  These are palette-native and endlessly re-seedable by the date.
- Constructivism / Bauhaus / Swiss type — the black/white/red palette IS Lissitzky's world.

## Upcoming sky events (hooks for future days)

- **Jul 20** — near-first-quarter Moon close to Spica (Virgo) after twilight, evening SW
- **Jul 21** — First-quarter Moon, 11:06 UTC — best crater relief along the terminator
- **Jul 28–29** — Piscis Austrinids peak (minor)
- **Jul 30–31** — double meteor shower: α Capricornids + Southern δ Aquariids (best pre-dawn)
- **Aug 12–13** — Perseids peak (the big one) — but a bright waning gibbous Moon interferes this year
- Mars low in the E before dawn; Saturn high before dawn; Venus dominates the early-evening W.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun (Hokusai; seigaiha wave-scale option)
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Maze from a cellular automaton; Conway's Life long-exposure trails; abelian sandpile fractal
- Hilbert / space-filling curve, single continuous red thread on white
- "Word of the day" — one beautiful word, huge, with its etymology in small print
- Moon-phase dashboard that recurs on notable moon days (build once, re-fire on phase changes)
- Bauhaus / Swiss-grid poster; a Vera Molnár–style ordered-then-disordered square field
- Anniversary template is proven now (see day 2) — keep a running list of good dates:
  sliced bread (Jul 7 1928), Bastille Day (Jul 14), Moon landing (Jul 20 1969), Amelia Earhart b. (Jul 24)

## Run log

### 2026-07-07 — first day. Tanabata.
Bootstrapped the repo (this file, folder conventions, the 3× dither pipeline). Made: Amanogawa
(Tanabata night, Milky Way, Vega+Altair, bamboo & red tanzaku, 七夕), Hitomezashi sashiko,
a last-quarter Moon almanac, the Summer Triangle star chart, and generative Ridgelines.
Lesson: first runs are mostly plumbing; keep each day's generator self-contained in the archive.

### 2026-07-19 — moon-landing week; a founding day.
Today is dense: Apollo 11 made Lunar Orbit Insertion on Jul 19 1969 (day before the landing);
the Seneca Falls Convention opened Jul 19 1848; and tonight a young waxing crescent Moon rides
past Venus and Regulus low in the west (first quarter Jul 21). Made:
1. **Apollo 11 — Lunar Orbit** — cratered lunar limb across the foreground, Earthrise, a red
   dashed orbit arc with the tiny command module Columbia riding it. Tonal, 3× + dither.
2. **Tonight · July 19** — dithered twilight, bold waxing crescent (earthshine + offset-disc
   mask), Venus with diffraction spikes, Regulus, a house-and-hill skyline, W compass mark.
3. **Red Wedge** — finally did the constructivist one I'd been saving. Homage to El Lissitzky's
   *Beat the Whites with the Red Wedge* (1919): red triangle piercing a white circle on a black
   field, suprematist debris on diagonals. Pure palette, 1× hard edges. The screen's native genre.
4. **Multiscale Truchet** — Smith arc-tiles (quarter-circles joining side-midpoints) on a
   recursively subdivided grid (Carlson-style); arcs connect across scales into loops, ~1 in 6 red.
5. **Declaration of Sentiments** — typographic anniversary poster; Stanton's amendment of
   Jefferson set in serif with "and women" struck in red. Clean 1× type.
Notes for next time: the crescent-via-mask trick (paste through an L-mode difference of two discs)
gives a much cleaner Moon than pieslice — reuse it. DejaVu has no serif-italic; used Liberation.
Two space/sky pieces in one set is fine when one is historical-illustrative and one is a present
star chart — they don't compete. Backlog thinned: Lissitzky ✓ and Truchet ✓ are done now.
Consider the Perseids build-up in early August, and the kamon or Great Wave pieces soon.
