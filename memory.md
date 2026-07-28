# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`; work lands on
  the session's assigned `claude/...` branch and Edward merges it).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work:
  - Soft/photographic pieces: render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg
    dither into the exact 3-color palette. Graphic/typographic pieces: render at 4×,
    LANCZOS downscale, quantize with **dither=NONE** — crisp edges, no speckle. Save mode-P.
  - Palette image: `putpalette` takes at most 256 entries (3 colors + 253 black pads).
  - Under FS dithering, near-black fills like (10,10,10) speckle with white dots — use
    pure (0,0,0) for any field you want solid.
  - Always `fitfont()` (shrink until `textlength` ≤ maxw) on long caption lines; I lost a
    render pass to right-edge overflow. At 4×, body text below ~36px becomes marginal on
    the real screen; 40+ is safe.
  - Piano-roll/grid pieces: check cell height minus 2×pad stays ≥ a few px, else marks vanish.
  - Fonts on this box: DejaVu (sans/serif/mono — has Cyrillic, ♭ and ♮), Liberation, Noto,
    and `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji!). Pillow needs
    `pip install pillow` fresh each session.
  - Red reads *bright* on these panels — it carries enormous weight; use as accent.
  - Overlapping red shapes fuse: the mitsudomoe's three commas merged into one red disk
    with a white pinwheel of negative space — better than what I designed. Negative space
    at 400×300 is a friend.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, meteor showers, conjunctions. A desk object that quietly
  tells you what the sky is doing tonight. Recurring format now: "SKY ALMANAC" card.
- Japanese pattern mathematics — hitomezashi (done), kamon crests (started: mitsudomoe).
  More to mine: kikyo/kiku/asanoha crests, kumiko lattices, seigaiha waves.
- Constructivism — the palette IS the movement. Red Wedge homage done; more Lissitzky/
  Rodchenko/Moholy-Nagy compositions possible (Prouns would suit this screen).
- Anniversaries of images and sounds — the Berkowski eclipse daguerreotype was a perfect
  fit: an anniversary OF a picture, drawn AS a picture. Look for more of these
  (first X-ray photo, first radio broadcast, Voyager golden record...).

## Upcoming sky events (hooks for future days)

- **Jul 29** — Full Buck Moon (tonight's moon 99%)
- **Jul 31** — α Capricornids + Southern δ Aquariids double peak (moonlight interferes)
- **Aug 12–13** — **PERSEIDS at NEW MOON — best meteor year since 2018.** The Aug 12 new
  moon is also the 5th and final new supermoon of 2026. If I get one run in mid-August,
  this is the subject. Made it the red line of today's almanac.
- **Aug 28** — total lunar eclipse? verify date online before using (I have not confirmed).
- Refresh this list when it thins out — timeanddate.com and starwalk.space are reliable.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun (next strong candidate)
- Kamon series continues: kikyo (bellflower), kiku (chrysanthemum), asanoha — one per week?
- Truchet tiles / Wang tiles / maze from a cellular automaton
- Word-of-the-day typographic piece (one beautiful word, huge, etymology in small print)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Sutton Hoo helmet (found 28 Jul 1939) — tried to save for a day with better reference time
- Proun-style axonometric constructivist composition
- A "signal" series: semaphore, morse, maritime flags spelling something for the day

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa night scene, hitomezashi,
moon almanac, Summer Triangle chart, generative ridgelines. Lesson: keep each day's
generator self-contained in the archive.

### 2026-07-28 — day 2 (three-week gap; the scheduler was quiet, not me).
Found today was the 175th anniversary of the first photograph of a total solar eclipse —
Berkowski's daguerreotype, Königsberg, 28 July 1851. Bach also died this day in 1750,
and the full Buck Moon is tomorrow. Made:
1. **Berkowski** — the eclipse daguerreotype reimagined: dithered corona with equatorial
   streamers, red prominences on the limb, plate-mount caption. Favorite of the day.
2. **Red Wedge** — Lissitzky homage, finally off the backlog. КЛИНОМ / КРАСНЫМ.
3. **B-A-C-H** — the four-note motif on a staff (red note heads) over a fugue piano-roll;
   the final subject entry breaks off before its last note, as the manuscript does.
4. **Buck Moon almanac** — black night panel with dithered maria moon; calendar pointing
   hard at the Aug 12 Perseids/new-supermoon night.
5. **Mitsudomoe** — kamon #1: red water-whirl in a double black ring, vertical 三つ巴,
   red 紋 seal. The accidental negative-space fusion made it.
Lessons folded into technique notes above. Next time: check days remaining to Perseids;
if a run lands Aug 10–13, drop everything for a full Perseid set.
