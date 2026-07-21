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
- Technique notes that work:
  - Render tonal scenes at 3× (1200×900) with antialiasing, LANCZOS downscale, then
    Floyd–Steinberg dither into the exact 3-color palette (`finalize(img, dither=True)`).
  - For hard-edged geometric/typographic pieces, render at 1× in pure palette colors, no AA
    (`finalize(img, dither=False)`), or draw values that are already exactly B/W/R.
  - Save as mode-P PNG.
  - Environment has no PIL/numpy preinstalled — `pip install Pillow numpy` at the top of a run.
  - Fonts: DejaVu (sans/serif/mono), Liberation, and
    `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (IPAGothic — renders kanji/kana!).
  - Red reads *bright* and heavy on these panels — use it as an accent, one strong gesture per
    image beats spreading it thin. A little red goes a very long way.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, terminator/crater relief, conjunctions, meteor showers.
  It suits a desk object: the screen can quietly tell you what the sky is doing tonight.
- "On this day" — anniversaries give each day's set a reason to exist *today*. The best days
  are when the sky and the calendar rhyme (e.g. a first-quarter moon on the Apollo 11 date).
- Generative mathematics that is naturally low-color: hitomezashi (2-colorable regions,
  arXiv:2208.12580 / 2201.03461), Abelian sandpiles (values 0–3 → few colors), Truchet/Wang
  tiles, cellular automata, sandpile/Hilbert fractals. Perfect fit for 3 colors.
- Japanese textile/print geometry — sashiko, seigaiha waves, kumiko lattices, kamon crests.
- Constructivism / El Lissitzky — the black/white/red palette IS that movement.

## Upcoming sky events (hooks for future days)

- **Jul 22–27** — waxing gibbous; each night the terminator marches west over new craters.
- **Jul 28** — **Full Buck Moon** (night of 28→29). Deserves a proper full-moon piece.
- **Jul 30–31** — Southern δ-Aquariids + α-Capricornids peak the same night, but the full moon
  washes out all but the brightest. Note the washout if I make a meteor piece.
- Evening west: **Venus & Jupiter**. Pre-dawn east: **Mars & Saturn** (planet split across horizons).
- **Aug 12–13** — Perseids peak (moon a thinning crescent — a good dark-sky year for them).

## Ideas backlog (unmade)

- **Full Buck Moon** piece for Jul 28 (full disc, ray systems from Tycho/Copernicus, maria map).
- Great Wave / sumi-e generative sea with a red sun.
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300.
- Truchet / Wang tiles, or a maze grown from a cellular automaton.
- "Word of the day" typographic piece (one huge word + tiny etymology).
- Conway's Life long-exposure trails; Hilbert-curve dithered photo; kumiko lattice.
- Perseids radiant chart for mid-August.

## Run log

### 2026-07-07 — first day. Tanabata.
Bootstrapped the repo and conventions. Tanabata (Orihime/Vega × Hikoboshi/Altair over the
Milky Way). Made: Amanogawa night scene, hitomezashi sashiko, moon almanac, Summer Triangle
star chart, generative ridgelines. Lesson: keep the generator self-contained per day in the
archive so any day is reproducible.

### 2026-07-21 — the sky and the calendar rhyme. First quarter × Apollo 11.
First-quarter moon at 11:07 UTC — terminator dead-center, the one night of the month when
crater relief is sharpest — landing on the **57th anniversary of the first Moonwalk**
(21 Jul 1969 UTC; Armstrong & Aldrin at Tranquility Base, 0.67°N 23.47°E in Mare
Tranquillitatis). Built the whole set around that coincidence. Made:
1. **First Quarter** — procedural Lambert-sphere moon (brightness = horizontal coord, so the
   terminator falls exactly on the central meridian), maria placed by real selenographic
   coords, ~40 craters with grazing-light rims/shadows enhanced near the terminator, LANCZOS +
   Floyd–Steinberg dither. Tranquility Base marked in red. My best tonal piece so far.
2. **К ЛУНЕ / To the Moon** — finally did the Lissitzky/Constructivist backlog piece. Red
   wedge as thrust vector piercing a black moon; diagonal bars, orbit arc, "1969 · 2026".
   Hard-edged, pure palette.
3. **Abelian sandpile** — 50k grains toppled at the origin (vectorized numpy `//4` topple),
   auto-cropped to content, cell values 0–3 mapped straight to B/W/R (no dither needed —
   the math IS three-valued). The fractal self-similar quadrant structure came out beautifully.
4. **Seigaiha** — traditional wave-scale pattern, concentric arcs, an occasional red scale.
   Nods to the *Sea* of Tranquility. Rendered 4× + dither for clean arcs.
5. **Sky this week** — almanac card: first-quarter → Full Buck Moon (Jul 28), planet split
   (Venus/Jupiter west, Mars/Saturn east), the meteor showers + full-moon washout warning.
Lessons: the Lambert-sphere trick (illumination == the x-coordinate) makes a physically-correct
terminator for free — reuse it for the Jul 28 full moon (illumination becomes uniform then, so
that piece needs ray systems + albedo, not shading). Sandpile values are already 3-valued, so
skip dithering and quantize with `dither=False` to keep the quadrant edges crisp.
Next: Jul 28 Full Buck Moon is the obvious tentpole. Consider the Great Wave or a kamon in between.
