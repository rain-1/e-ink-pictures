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
- The scheduled session pushes to a per-run `claude/...` branch, not `main` directly;
  Edward merges. Just push to the designated branch and notify.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then quantize into the exact 3-color palette. Floyd–Steinberg dither **only** for
  photographic/gradient content; for line art and posters use `dither=NONE` (nearest color)
  after the downscale — edges come out crisp with no speckle. Save as mode-P PNG.
  Fonts on this box: DejaVu (sans/serif/mono — has Cyrillic!), Liberation, Noto, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (can render kanji).
  Pillow is NOT preinstalled in the remote container — `pip install Pillow` first.
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight.
  Text placed with `anchor="mm"` near panel edges gets clipped — clamp label centers
  to keep half the text width inside the margin (see 2026-09-01 `almanac()`).
  Density-field pointillism works: tens of thousands of tiny glyphs with an
  `exp(-k·x)` acceptance probability makes a beautiful thinning gradient (the Martha flock).

## Standing interests (what I find myself drawn to)

- Extinction, memory, and "last of" stories — the Martha piece felt important. Others:
  the last Great Auk (June 3, 1844), Benjamin the last thylacine (Sept 7, 1936 — soon!),
  Celia the last Pyrenean ibex (Jan 6, 2000).
- Sky almanac data — moon phases, conjunctions, meteor showers. A desk object should
  quietly tell you what the sky is doing.
- Japanese calendar & pattern mathematics — hitomezashi (done day 1), the 72 microseasons
  (kō), zassetsu days like 二百十日 (done today), kumiko lattices, kamon crests, seigaiha.
- Constructivism — did the Lissitzky-style piece today (ЗНАНИЕ — СИЛА). The palette IS
  that movement; can return to it, but vary the vocabulary (Rodchenko photomontage?
  Vertov film-poster style?).
- Diagram beauty: transit maps (did Boston 1897 today), timelines, isotype pictograms.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming hooks (verified while researching, use soon)

- **Sep 7** — Benjamin, the last thylacine, died 1936 (Australia's Threatened Species Day).
  Pairs with the Martha piece as a series.
- **Sep 11** — new moon (darkest skies of the month)
- **Sep 18** — Venus at its brightest for the whole 2026 evening apparition
- **Sep 23** — September equinox, astronomical autumn begins; aurora season boost
- **Sep 26** — Harvest Moon (closest full moon to the equinox)
- September 2026 also has lunar occultations of Jupiter and Venus visible from some
  regions, and it's one of the last months to catch the Milky Way core in the north.
- Mid-autumn festival / tsukimi falls near the Harvest Moon — susuki + dango + moon
  imagery would suit the screen perfectly.

## Ideas backlog (unmade)

- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- A "word of the day" typographic piece (one beautiful word, huge, with etymology small)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Isotype-style pictogram statistics (Neurath) — the b/w/red palette is also THAT movement
- 72 microseasons series: the current kō in kanji + one generative illustration
- Anniversary poster template: one bold date, one image, one fact (worked well today ×3)

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped the repo conventions. Made: Amanogawa night scene, hitomezashi, moon
almanac card, Summer Triangle star chart, generative ridgelines. Lesson: keep each
day's generator self-contained in the archive.

### 2026-09-01 — day 2. (The schedule was quiet July 8 – Aug 31; two runs total so far.)
September 1 turned out to be absurdly rich: Martha the last passenger pigeon died 1914,
Boston's subway opened 1897, Russia's Knowledge Day, Japan's 二百十日 storm-watching day
(and Disaster Prevention Day, for the 1923 Kantō quake — chose the gentler zassetsu
framing). Made:
1. **Martha** — 90k-bird density-field flock thinning across the sky to one red bird;
   "5 000 000 000 → 1 → 0". My favorite so far.
2. **ЗНАНИЕ — СИЛА** — constructivist Knowledge Day poster; red wedge piercing the
   white circle out of the black field; finally cashed in the saved Lissitzky idea.
3. **America's First Subway** — Beck-style diagram of the 1897 Tremont St line (solid
   red = opened Sept 1: Public Garden incline, Boylston, Park St; dashed = 1898).
4. **September 2026 almanac** — black-ground month timeline (today/new moon/Venus/
   equinox/Harvest Moon) + a strip of 30 tiny correct moon phases along the bottom.
5. **二百十日** — red sun, wind streamlines with spiral curls, 85 wind-bent susuki
   blades, vertical kanji.
Lessons: nearest-color quantize beats dithering for poster work; clamp edge labels;
supersampled thin lines (width 1 at 3×) vanish — use ≥2. Next time: Sep 7 thylacine
(if a run happens that day), tsukimi near Sep 26, or dig into the kamon generator.
